# FastMCP v2 → v3 Modernization — Design

**Date:** 2026-06-26
**Status:** Approved (design); pending implementation plan
**Component:** `alliance-docs-mcp` MCP server

## Context

The server currently depends on `fastmcp>=2.12.5`. FastMCP is now at 3.4.x — a
ground-up rebuild around components / providers / transforms. The existing code
uses conservative patterns, so the breaking-change surface is small; the real
opportunity is best-practice alignment and the architecture the new version
enables.

The most fragile thing in the current code is not FastMCP-specific: all of
`server.py`'s work happens at **module import time** — discovering the docs
directory, building the Whoosh search index, building the embeddings related
index, and reading **every mirrored page into memory** as a `TextResource`.
This is brittle, scales poorly with corpus size, and makes testing awkward.

Deployment runs over HTTP in Docker via
`fastmcp run server_entrypoint.py:mcp --transport http --host 0.0.0.0 --port 8080 --path /mcp/ -- --docs-dir ...`.

## Goals (locked decisions)

- Upgrade `fastmcp` to `>=3.0,<4` (lands on 3.4.x).
- **Hybrid resources**: a lazy resource *template* for page content plus a
  lightweight listing for discoverability.
- **`ToolError`** raised on genuine failures; legitimately empty results stay `[]`.
- **Structured output** models (TypedDict/Pydantic) on every tool.
- **`fastmcp.json`** as the single deployment source of truth.

### Out of scope (deferred)

- Context-based logging / progress reporting.
- OpenTelemetry tracing.
- Tool Search transform (pointless at ~8 tools).

## Design

### 1. Server lifecycle (core refactor)

Replace import-time side effects with FastMCP's `lifespan`:

- A `build_state()` factory returns a `ServerState` dataclass holding
  `storage`, `search_index` (or `None`), `related_index` (or `None`), and
  `docs_path`. It encapsulates today's env-flag logic (`DISABLE_SEARCH_INDEX`,
  `DISABLE_RELATED_INDEX`, auto-populate-when-empty, index-dir/model/backend
  resolution).
- `@asynccontextmanager async def lifespan(server)` calls `build_state()`,
  stashes the result in a module-level holder, `yield`s, and tears down on
  shutdown.
- Tool and resource *impl* functions read state from that holder. The existing
  testable `_impl` pattern is preserved — tests call `build_state()` against a
  temporary docs directory instead of relying on import-time globals.

**Why:** eliminates brittle import-time side effects and the eager full-corpus
memory load; makes startup and tests deterministic.

### 2. Resources — hybrid model

Replace the loop that registers N `TextResource` objects with:

- `@mcp.resource("alliance-docs://page/{slug}")` — a resource **template** that
  reads the file on demand (gzip-aware), returns `text/markdown`, and attaches
  per-page `meta` (title, url, category, last_modified, page_id). A missing or
  invalid slug raises `ResourceError`.
- `@mcp.resource("alliance-docs://pages")` — a single **index resource**
  returning a JSON array of `{slug, title, url, category}` so clients browsing
  the resource list still get discoverability without enumerating hundreds of
  entries.
- Keep the `list_all_pages` tool for tool-only clients.

Resource URIs are unchanged (`alliance-docs://page/{slug}`), so existing
references keep working; the change is that content is served lazily via a
template rather than pre-registered eagerly.

### 3. Tools — quality pass

For each of the 8 tools (`search_docs`, `list_categories`, `get_page_by_title`,
`list_recent_updates`, `find_related_pages`, `get_page_info`, `list_all_pages`,
`get_page_content`):

- **Param descriptions** via `Annotated[T, Field(description=...)]`.
- **Annotations**: `readOnlyHint=True`, `idempotentHint=True` (all read-only).
- **Structured output**: define result models — `SearchHit`, `PageSummary`,
  `PageInfo`, `RelatedPage` — and return `list[SearchHit]`, `PageInfo | None`,
  etc., so FastMCP emits real output schemas.
- **Errors**: raise `ToolError` on real failures (e.g. index error,
  page genuinely missing in `get_page_content` / `get_page_info`); a legitimate
  "no matches" still returns `[]`.
- Drop empty-paren `@mcp.tool()` → `@mcp.tool` where there are no decorator args.

Prompts already return plain strings (valid in v3) and are left essentially
as-is.

### 4. Deployment — `fastmcp.json` + entrypoint simplification

- Add **`fastmcp.json`**:
  - `source`: `src/alliance_docs_mcp/server.py`, entrypoint `mcp`.
  - `deployment`: transport `http`, host `0.0.0.0`, port (default 8080), path
    `/mcp/`, and `env` for `DOCS_DIR` / `MEDIAWIKI_API_URL` / `USER_AGENT` via
    `${VAR}` interpolation.
- `docker-entrypoint.sh` collapses its long `fastmcp run ...` invocation to
  **`fastmcp run fastmcp.json`** (the background documentation-sync loop and
  signal forwarding are unchanged).
- Fix the **dead `--docs-dir` path**: `fastmcp run ...:mcp` imports the object
  and never executes `main()`'s argparse, so that flag is a silent no-op today.
  Configuration standardizes on the `DOCS_DIR` environment variable. `main()`
  slims to a stdio dev launcher; the broken `global storage` mutation is removed.

### 5. Dependencies

- `pyproject.toml`: `fastmcp>=3.0,<4`; `uv lock`.
- No `fastmcp[tasks]` extra required (no background tasks used).
- v3 3.4.1 floors Starlette `>=1.0.1` (CVE-2026-48710 fix); `uv` resolves cleanly.

## Testing

- Update tests that relied on import-time globals to use `build_state()` against
  a temporary/fixture docs directory.
- New tests:
  - Resource-template read — hit returns markdown; missing slug raises error.
  - Index resource (`alliance-docs://pages`) returns the expected shape.
  - `ToolError` raised on simulated failure paths.
  - Structured-output result shapes for each tool.
- Run the full existing suite (search, related, storage, converter, mirror,
  prompts) to confirm behavior parity.

## Risks / call-outs

- `ToolError` and structured output **change what clients observe** — this is
  intended and will be noted in the README.
- The hybrid resource model removes per-page entries from the enumerable
  resource list; discoverability is preserved via the `alliance-docs://pages`
  index resource and the `list_all_pages` / `search_docs` tools.
- Behavior parity for search/related ranking is verified by the existing suite.
