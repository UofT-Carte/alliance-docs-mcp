#!/usr/bin/env bash
set -euo pipefail

# Timestamped boot logging so deploy logs show exactly where startup time goes
# (boot -> prime -> server bind). Critical for diagnosing slow-boot deploy
# timeouts on the small Fly machine.
ts() { echo "[entrypoint $(date -u +%H:%M:%S)] $*"; }

ts "Entrypoint start"

export DOCS_DIR="${DOCS_DIR:-/data/docs}"
PORT="${PORT:-8080}"
RUN_SYNC_ON_START="${RUN_SYNC_ON_START:-1}"
SYNC_MODE="${SYNC_MODE:-incremental}"

mkdir -p "${DOCS_DIR}"

DOCS_SEED_DIR="${DOCS_SEED_DIR:-}"
if [[ -n "${DOCS_SEED_DIR}" && "${DOCS_SEED_DIR}" != "${DOCS_DIR}" && -d "${DOCS_SEED_DIR}" ]]; then
  if [[ -z "$(ls -A "${DOCS_DIR}" 2>/dev/null)" ]]; then
    ts "Priming documentation directory from baked seed at ${DOCS_SEED_DIR}"
    cp -a "${DOCS_SEED_DIR}/." "${DOCS_DIR}/"
    ts "Priming complete"
  fi
fi

start_sync() {
  echo "[entrypoint] Starting documentation sync (${SYNC_MODE}) in background..."
  if [[ "${SYNC_MODE}" == "full" ]]; then
    if python scripts/sync_docs.py; then
      echo "[entrypoint] Documentation sync (full) completed successfully"
    else
      echo "[entrypoint] Documentation sync (full) failed"
    fi
    return
  fi

  if python scripts/sync_docs.py --incremental; then
    echo "[entrypoint] Documentation sync (incremental) completed successfully"
    return
  fi

  echo "[entrypoint] Incremental sync failed, attempting full sync..."
  if python scripts/sync_docs.py; then
    echo "[entrypoint] Documentation sync (full) completed successfully"
  else
    echo "[entrypoint] Documentation sync (full) failed"
  fi
}

SYNC_PID=""

forward_signal() {
  local signal=$1
  if [[ -n "${SERVER_PID:-}" ]]; then
    kill "-${signal}" "${SERVER_PID}" 2>/dev/null || true
  fi
  if [[ -n "${SYNC_PID:-}" ]]; then
    kill "-${signal}" "${SYNC_PID}" 2>/dev/null || true
  fi
}

trap 'forward_signal TERM' TERM
trap 'forward_signal INT' INT

# Start the MCP server FIRST and let it bind before doing anything heavy.
# Running the docs sync concurrently with startup starves the small machine's
# single core / 512 MB and contends on the Whoosh writer lock (both the sync
# and the server build the same DOCS_DIR/search_index), delaying the port bind
# by minutes and tripping Fly's deploy health-check timeout. So: bind, become
# healthy, THEN run the catch-up sync in the background.
ts "Launching MCP server on port ${PORT}"
fastmcp run fastmcp.json --transport http --host 0.0.0.0 --port "${PORT}" &
SERVER_PID=$!

server_healthy() {
  HEALTH_URL="http://127.0.0.1:${PORT}/health" python -c '
import os, sys, urllib.request
try:
    urllib.request.urlopen(os.environ["HEALTH_URL"], timeout=2).read()
except Exception:
    sys.exit(1)
'
}

wait_for_health() {
  for _ in $(seq 1 "${HEALTH_WAIT_SECONDS:-180}"); do
    if server_healthy; then
      return 0
    fi
    # Bail out early if the server process died.
    kill -0 "${SERVER_PID}" 2>/dev/null || return 1
    sleep 1
  done
  return 1
}

if [[ "${RUN_SYNC_ON_START}" != "0" ]]; then
  if wait_for_health; then
    ts "Server is healthy; starting deferred documentation sync"
    start_sync &
    SYNC_PID=$!
  else
    ts "Server did not become healthy in time; skipping startup sync"
  fi
else
  ts "Skipping startup sync (RUN_SYNC_ON_START=${RUN_SYNC_ON_START})"
fi

wait "${SERVER_PID}"
SERVER_EXIT=$?

if [[ -n "${SYNC_PID}" ]]; then
  if wait "${SYNC_PID}"; then
    :
  else
    echo "[entrypoint] Documentation sync process exited with an error"
  fi
fi

exit "${SERVER_EXIT}"
