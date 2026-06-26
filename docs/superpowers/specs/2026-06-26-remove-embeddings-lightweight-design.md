# Remove Embeddings Stack — Lightweight Server Design

**Date:** 2026-06-26
**Status:** Approved (design); pending implementation plan
**Component:** `alliance-docs-mcp` MCP server

## Context

The server depends on a heavy machine-learning stack — `sentence-transformers`
(which pulls `torch`), `chromadb`, and `numpy` — used solely by the `related`
subpackage to power semantic "related pages" discovery. This stack dominates
the deployment footprint:

- Container image ~2–3 GB (torch + transformers + chromadb).
- Runtime RAM ~1 GB (embedding model + Chroma vector store + Whoosh index).
- Startup loads torch and a sentence-transformer model and builds/loads a
  vector index — the slow, fragile part of cold starts.

This footprint is the root cause of the reliability and cold-start problems
that prompted a re-evaluation of hosting. Removing it makes the server light
enough to run on the smallest tier of any managed PaaS.

The key enabler: `find_related_pages` already has a dependency-free fallback
(`_heuristic_related()` — category match + title-token overlap). And the
existing Whoosh full-text index already stores page content, so it can back a
content-aware "more like this" without any new heavy dependency.

## Goals (locked decisions)

- Remove the entire `related` subpackage and the `chromadb`,
  `sentence-transformers`, and `numpy` dependencies (torch falls away with
  them; it was only transitive).
- **Keep `find_related_pages`**, re-backed by a new Whoosh "more like this"
  method, with the existing `_heuristic_related()` retained as fallback.
- **Drop the `min_score` parameter** from `find_related_pages` — the only
  client-visible API change. Whoosh relevance scores are not normalized to
  0–1, so a cosine-style threshold would mislead. `RelatedPage.score` is still
  populated with the raw Whoosh score for information.

### Out of scope (deferred)

- Choosing/migrating the actual hosting platform — that re-evaluation resumes
  after this lightweight refactor lands.
- Any schema change to the Whoosh index (the `text=`-based `more_like` works
  against the already-stored `content` field).

## Design

### 1. Delete the heavy stack

- Delete `src/alliance_docs_mcp/related/` in full (`__init__.py`, `embedder.py`,
  `index.py`, `vector_store.py`).
- `pyproject.toml`: remove `chromadb`, `sentence-transformers`, and `numpy`
  from `dependencies`. Confirm via grep that nothing outside the deleted
  package imports `numpy`, `chromadb`, `sentence_transformers`, or `torch`.
  Run `uv lock`.

### 2. New `SearchIndex.more_like_this(slug, limit)`

In `src/alliance_docs_mcp/search_index.py`:

- Raise `SearchIndexUnavailable` when the index is disabled/unavailable
  (mirrors `search()`).
- Resolve the document number via `searcher.document_number(slug=slug)`;
  return `[]` if the slug is not indexed.
- Read the page's stored `content` (`searcher.stored_fields(docnum)`); return
  `[]` if empty.
- Run `searcher.more_like(docnum, "content", text=content, top=limit + 1)`.
  The `text=` form does not require term vectors, so the existing schema is
  untouched.
- Return a list of dicts in the **same shape as `search()`** — `title`, `slug`,
  `url`, `category`, `score` (`hit.score`), `last_modified` (raw stored
  datetime) — excluding the query page itself, capped at `limit`.
- Wrap backend failures: re-raise `SearchIndexUnavailable`; on any other
  exception, log a warning and raise `SearchIndexUnavailable`.

### 3. Rewrite `find_related_pages`

In `src/alliance_docs_mcp/server.py`:

- Tool signature becomes `find_related_pages(slug, limit=5)` — `min_score`
  removed.
- `_find_related_pages_impl(slug, limit=5)`:
  - `page = storage.get_page_by_slug(slug)`; raise `ToolError` if missing
    (unchanged).
  - If `search_index` is available, try `search_index.more_like_this(slug,
    limit=limit)`. On non-empty results, map each to `RelatedPage`, converting
    `last_modified` via `.isoformat()` with a `None` guard (matching the
    `search_docs` path). Return them.
  - On `SearchIndexUnavailable` (log warning) or any other exception (log
    error) or empty results, fall back to `_heuristic_related(page, limit)`.
- `_heuristic_related()` is unchanged. The tool therefore still works with
  `DISABLE_SEARCH_INDEX=1`.

### 4. State & configuration cleanup

In `server.py`:

- Remove `related_index` from the `ServerState` dataclass, the module-level
  global, and the `_apply_state()` assignment.
- Remove `_build_related_index()` and its call in `build_state()`.
- Remove the `RELATED_INDEX_DIR`, `RELATED_MODEL_NAME`, `RELATED_BACKEND`, and
  `DISABLE_RELATED_INDEX` env vars and the `from .related import ...` line.

### 5. `sync_docs.py` cleanup

- Remove `_prepare_related_index()` and the `from alliance_docs_mcp.related
  import ...` line.
- Remove per-page `related_index.upsert_page(...)` and `related_index.cleanup(...)`
  calls in both `sync_documentation()` and `sync_incremental()`.
- Remove the `related_index/` directory removal in `_rebuild_all()`.
- Remove the `--no-related-index`, `--rebuild-related-index`,
  `--related-index-dir`, `--related-model-name`, `--related-backend` CLI args
  and their env-var defaults; remove the `enable_related_index` / model /
  backend arguments threaded into the sync calls.

### 6. Docker, gitignore, docs

- `.gitignore`: remove the `docs/related_index/` line.
- `Dockerfile` / `docker-entrypoint.sh`: no logic change required. The seed
  build (`scripts/sync_docs.py`) simply stops producing an embeddings index
  and no longer downloads torch or a model.
- `README.md`: reframe the "Related Pages" feature as Whoosh-backed
  (content-aware "more like this") with heuristic fallback; remove the
  embeddings/model-download note and the `RELATED_*` environment-variable rows.
  The `related_content_discovery` prompt is retained.

### 7. Tests

- Delete `tests/test_related_index.py`.
- `tests/test_server_search.py`: remove `DummyRelatedIndex` and the
  embeddings-path tests. Add tests that exercise the `more_like_this` path
  (returns related pages, excludes self) and the heuristic fallback (when the
  search index is absent/unavailable).
- `tests/test_server_state.py`: remove `DISABLE_RELATED_INDEX` assertions and
  any `related_index` expectations.
- `tests/test_models.py`: `RelatedPage` is still used — keep its test.
- Add direct `SearchIndex.more_like_this` tests: returns content-similar pages,
  excludes the query page, returns `[]` for an unknown slug, raises
  `SearchIndexUnavailable` when disabled.

## Net impact

- Image ~2–3 GB → ~300–500 MB.
- Runtime RAM ~1 GB → ~150–250 MB.
- Startup no longer loads torch or a sentence-transformer model — cold starts
  become "open a Whoosh index," directly resolving the reliability/cold-start
  concerns.

## Risks / call-outs

- **Breaking change:** `find_related_pages` loses its `min_score` parameter.
  Clients passing it will error. Noted in the README.
- **Relatedness quality shifts** from semantic embeddings to Whoosh term
  similarity over page content. For an internal docs corpus this is close to
  the original intent and far better than the title-only heuristic, but it is
  not identical to embedding-based results.
- `more_like` with `text=` relies on Whoosh key-term extraction over the
  stored `content` field; verified not to need term vectors, so no schema
  migration is required.
