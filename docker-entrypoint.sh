#!/usr/bin/env bash
set -euo pipefail

export DOCS_DIR="${DOCS_DIR:-/data/docs}"
PORT="${PORT:-8080}"
RUN_SYNC_ON_START="${RUN_SYNC_ON_START:-1}"
SYNC_MODE="${SYNC_MODE:-incremental}"

mkdir -p "${DOCS_DIR}"

DOCS_SEED_DIR="${DOCS_SEED_DIR:-}"
if [[ -n "${DOCS_SEED_DIR}" && "${DOCS_SEED_DIR}" != "${DOCS_DIR}" && -d "${DOCS_SEED_DIR}" ]]; then
  if [[ -z "$(ls -A "${DOCS_DIR}" 2>/dev/null)" ]]; then
    echo "[entrypoint] Priming documentation directory from baked seed at ${DOCS_SEED_DIR}"
    cp -a "${DOCS_SEED_DIR}/." "${DOCS_DIR}/"
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
if [[ "${RUN_SYNC_ON_START}" != "0" ]]; then
  start_sync &
  SYNC_PID=$!
else
  echo "[entrypoint] Skipping startup sync (RUN_SYNC_ON_START=${RUN_SYNC_ON_START})"
fi

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

echo "[entrypoint] Starting MCP server on port ${PORT}"
fastmcp run fastmcp.json --port "${PORT}" &

SERVER_PID=$!
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
