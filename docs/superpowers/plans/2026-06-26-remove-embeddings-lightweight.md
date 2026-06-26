# Remove Embeddings Stack — Lightweight Server Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the heavy embeddings stack (sentence-transformers, torch, chromadb, numpy) and re-back `find_related_pages` with a lightweight Whoosh "more like this" method, shrinking the image from ~2–3 GB to ~300–500 MB.

**Architecture:** Add a content-similarity method to the existing Whoosh `SearchIndex`, repoint the `find_related_pages` tool at it (keeping the existing `_heuristic_related()` as fallback), then delete the `related` subpackage and all of its plumbing across `server.py`, `scripts/sync_docs.py`, dependencies, tests, and docs.

**Tech Stack:** Python 3.11+, FastMCP v3, Whoosh, pytest, `uv`.

## Global Constraints

- Use `uv` for all dependency and execution commands (`uv run pytest`, `uv lock`). Never `pip`.
- Final `dependencies` in `pyproject.toml` must NOT contain `chromadb`, `sentence-transformers`, or `numpy`. `fastmcp>=3.0,<4` stays.
- `find_related_pages` final signature is exactly `find_related_pages(slug, limit=5)`. The `min_score` parameter is removed (the one client-visible breaking change).
- Keep the `RelatedPage` model and the `related_content_discovery` prompt — both remain in use.
- `SearchIndex.more_like_this()` returns a `List[Dict]` whose items have exactly these keys: `title`, `slug`, `url`, `category`, `score`, `last_modified` (same shape as `SearchIndex.search()` minus `highlights`).
- When mapping a Whoosh `last_modified` (a `datetime`) into a model, convert with `.isoformat()` guarded by `is not None`, matching the existing `_search_docs_impl` pattern.
- TDD: write the failing test first, watch it fail, implement, watch it pass, commit. Frequent commits.

---

### Task 1: Add `SearchIndex.more_like_this()`

Purely additive — introduces the Whoosh content-similarity method that will back related-pages. No existing behavior changes.

**Files:**
- Modify: `src/alliance_docs_mcp/search_index.py` (add a method to the `SearchIndex` class, after `search()` which ends at line 137)
- Test: `tests/test_search_index_mlt.py` (create)

**Interfaces:**
- Consumes: existing `SearchIndex.__init__(index_dir, enabled=True)`, `SearchIndex.index_page(slug, title, content, category, url, last_modified)`, and `SearchIndexUnavailable`.
- Produces: `SearchIndex.more_like_this(slug: str, limit: int = 5) -> List[Dict]` — returns up to `limit` pages most similar by content to `slug`, excluding `slug` itself; `[]` when the slug is not indexed or has empty content; raises `SearchIndexUnavailable` when the index is disabled/unavailable.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_search_index_mlt.py`:

```python
import pytest

from alliance_docs_mcp.search_index import SearchIndex, SearchIndexUnavailable


def _populate(index: SearchIndex) -> None:
    index.index_page(
        slug="slurm_a",
        title="Running Slurm Jobs",
        content="Submit Slurm jobs with sbatch and gpus-per-node on the cluster.",
        category="Technical",
        url="https://example.com/a",
        last_modified="2025-01-01T00:00:00Z",
    )
    index.index_page(
        slug="slurm_b",
        title="Slurm Scheduling",
        content="Slurm jobs use sbatch and gpus-per-node to request cluster resources.",
        category="Technical",
        url="https://example.com/b",
        last_modified="2025-01-02T00:00:00Z",
    )
    index.index_page(
        slug="cooking",
        title="Cooking at Home",
        content="Recipes for soup and bread baking in the kitchen.",
        category="Food",
        url="https://example.com/c",
        last_modified="2025-01-03T00:00:00Z",
    )


def test_more_like_this_returns_similar_excluding_self(tmp_path):
    index = SearchIndex(tmp_path / "search_index")
    _populate(index)

    results = index.more_like_this("slurm_a", limit=5)

    slugs = [hit["slug"] for hit in results]
    assert "slurm_a" not in slugs  # query page excluded
    assert "slurm_b" in slugs  # content-similar page surfaces
    top = results[0]
    assert set(top.keys()) == {
        "title",
        "slug",
        "url",
        "category",
        "score",
        "last_modified",
    }
    assert top["score"] is not None


def test_more_like_this_unknown_slug_returns_empty(tmp_path):
    index = SearchIndex(tmp_path / "search_index")
    _populate(index)

    assert index.more_like_this("does_not_exist") == []


def test_more_like_this_raises_when_disabled(tmp_path):
    index = SearchIndex(tmp_path / "search_index", enabled=False)
    with pytest.raises(SearchIndexUnavailable):
        index.more_like_this("slurm_a")
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_search_index_mlt.py -v`
Expected: FAIL with `AttributeError: 'SearchIndex' object has no attribute 'more_like_this'`.

- [ ] **Step 3: Implement `more_like_this`**

In `src/alliance_docs_mcp/search_index.py`, insert this method into the `SearchIndex` class immediately after the `search()` method (after line 137, before `is_empty()`):

```python
    def more_like_this(self, slug: str, limit: int = 5) -> List[Dict]:
        """Return pages whose content is most similar to the given page.

        Uses Whoosh term-similarity ("more like this") over the stored
        ``content`` field. The query page itself is excluded. Returns an
        empty list when the slug is not indexed or has no stored content.
        """
        if not self.enabled or not self._index:
            raise SearchIndexUnavailable("Search index disabled or unavailable")

        try:
            with self._index.searcher() as searcher:
                docnum = searcher.document_number(slug=slug)
                if docnum is None:
                    return []

                stored = searcher.stored_fields(docnum) or {}
                content = stored.get("content") or ""
                if not content:
                    return []

                results = searcher.more_like(
                    docnum, "content", text=content, top=limit + 1
                )
                hits: List[Dict] = []
                for hit in results:
                    if hit.get("slug") == slug:
                        continue
                    hits.append(
                        {
                            "title": hit.get("title"),
                            "slug": hit.get("slug"),
                            "url": hit.get("url"),
                            "category": hit.get("category"),
                            "score": hit.score,
                            "last_modified": hit.get("last_modified"),
                        }
                    )
                    if len(hits) >= limit:
                        break
                return hits
        except SearchIndexUnavailable:
            raise
        except Exception as exc:
            logger.warning("more_like_this failed for %s: %s", slug, exc)
            raise SearchIndexUnavailable(str(exc))
```

Note: `content` is `stored=True` in the schema (line 41), so `stored_fields` returns it; the `text=` form of `more_like` therefore needs no term vectors and no schema change.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `uv run pytest tests/test_search_index_mlt.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add src/alliance_docs_mcp/search_index.py tests/test_search_index_mlt.py
git commit -m "feat: add Whoosh more_like_this content-similarity method"
```

---

### Task 2: Repoint `find_related_pages` at Whoosh; drop `min_score`

Rewrite the tool and its impl to use `more_like_this` with the existing heuristic as fallback, and remove the `min_score` parameter. The `related_index` global still exists after this task (removed in Task 3) but is no longer referenced by the tool.

**Files:**
- Modify: `src/alliance_docs_mcp/server.py:336-366` (the `find_related_pages` tool at 336-345 and `_find_related_pages_impl` at 348-366)
- Test: `tests/test_server_search.py` (replace the two related-pages tests and delete `DummyRelatedIndex`)

**Interfaces:**
- Consumes: `SearchIndex.more_like_this(slug, limit)` (Task 1), `SearchIndexUnavailable`, the module global `search_index`, `storage.get_page_by_slug(slug)`, the existing `_heuristic_related(page, limit)` (server.py:271-299), and the `RelatedPage` model.
- Produces: `find_related_pages(slug, limit=5) -> List[RelatedPage]` and `_find_related_pages_impl(slug, limit=5) -> List[RelatedPage]`.

- [ ] **Step 1: Update the tests first**

In `tests/test_server_search.py`:

(a) Delete the `DummyRelatedIndex` class (lines 35-42):

```python
class DummyRelatedIndex:
    def __init__(self, results=None):
        self.results = results or []
        self.called = False

    def find_related(self, slug, limit=5, min_score=0.0):
        self.called = True
        return self.results
```

(b) Replace the two related tests (`test_find_related_pages_uses_related_index` and `test_find_related_pages_falls_back`, lines 84-130) with:

```python
@pytest.mark.asyncio
async def test_find_related_pages_uses_more_like_this(monkeypatch, tmp_path):
    import alliance_docs_mcp.server as server

    # The companion page shares NO title tokens and a DIFFERENT category, so the
    # title/category heuristic scores it 0 and would never surface it. Only the
    # content-similarity path (more_like_this) can relate it to the query page.
    storage = DummyStorage()
    storage.pages.append(
        {
            "title": "Provisioning Compute Nodes",
            "url": "https://example.com/companion",
            "category": "Technical",
            "slug": "companion",
            "last_modified": "2025-01-02T00:00:00Z",
        }
    )

    search_index = SearchIndex(tmp_path / "search_index")
    search_index.index_page(
        slug="test_page",
        title="Test Page",
        content="Slurm scheduling on the cluster with sbatch and partitions.",
        category="General",
        url="https://example.com/test",
        last_modified="2025-01-01T00:00:00Z",
    )
    search_index.index_page(
        slug="companion",
        title="Provisioning Compute Nodes",
        content="Slurm scheduling uses sbatch and partitions on the cluster.",
        category="Technical",
        url="https://example.com/companion",
        last_modified="2025-01-02T00:00:00Z",
    )

    monkeypatch.setattr(server, "storage", storage)
    monkeypatch.setattr(server, "search_index", search_index)

    results = await server._find_related_pages_impl("test_page", limit=3)
    slugs = [r.slug for r in results]
    assert "test_page" not in slugs
    assert "companion" in slugs  # surfaced by content similarity, not the heuristic


@pytest.mark.asyncio
async def test_find_related_pages_falls_back_to_heuristic(monkeypatch):
    import alliance_docs_mcp.server as server

    dummy_storage = DummyStorage()
    dummy_storage.pages.append(
        {
            "title": "Test Page Guide",
            "url": "https://example.com/test2",
            "category": "General",
            "slug": "test_page_2",
            "last_modified": "2025-01-02T00:00:00Z",
        }
    )

    monkeypatch.setattr(server, "storage", dummy_storage)
    monkeypatch.setattr(server, "search_index", None)

    results = await server._find_related_pages_impl("test_page", limit=3)
    assert results
    assert results[0].slug == "test_page_2"
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `uv run pytest tests/test_server_search.py -v`
Expected: FAIL on `test_find_related_pages_uses_more_like_this` — the unmodified impl never consults `search_index` for related lookups, so it falls through to `_heuristic_related`, which scores `companion` at 0 (no shared title tokens, different category) and never surfaces it, so `assert "companion" in slugs` fails. (`test_find_related_pages_falls_back_to_heuristic` already passes — it exercises the fallback that is unchanged.)

- [ ] **Step 3: Rewrite the tool and impl**

In `src/alliance_docs_mcp/server.py`, replace the entire block from line 336 through line 366 (the `@mcp.tool` decorator above `find_related_pages` through the end of `_find_related_pages_impl`) with:

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
async def find_related_pages(
    slug: Annotated[str, Field(description="Slug of the page to find relations for.")],
    limit: Annotated[int, Field(description="Maximum number of related pages.")] = 5,
) -> List[RelatedPage]:
    """Find related pages via content similarity, with heuristic fallback."""
    return await _find_related_pages_impl(slug, limit)


async def _find_related_pages_impl(slug: str, limit: int = 5) -> List[RelatedPage]:
    """Core related-pages implementation for tool and tests."""
    page = storage.get_page_by_slug(slug)
    if not page:
        raise ToolError(f"Page not found: {slug}")

    if search_index:
        try:
            results = search_index.more_like_this(slug, limit=limit)
            if results:
                return [
                    RelatedPage(
                        title=hit.get("title"),
                        url=hit.get("url"),
                        category=hit.get("category"),
                        slug=hit.get("slug"),
                        score=hit.get("score"),
                        last_modified=(
                            hit["last_modified"].isoformat()
                            if hit.get("last_modified") is not None
                            else None
                        ),
                    )
                    for hit in results
                ]
        except SearchIndexUnavailable as exc:
            logger.warning("Search index unavailable for related %s: %s", slug, exc)
        except Exception as exc:
            logger.error("Related lookup error for %s: %s", slug, exc, exc_info=True)

    return _heuristic_related(page, limit)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `uv run pytest tests/test_server_search.py -v`
Expected: PASS (4 passed — the two search tests plus the two rewritten related tests).

- [ ] **Step 5: Commit**

```bash
git add src/alliance_docs_mcp/server.py tests/test_server_search.py
git commit -m "feat: back find_related_pages with Whoosh more_like_this, drop min_score"
```

---

### Task 3: Remove related-index plumbing from `server.py`

Delete the `related` import and all `related_index` state from the server now that nothing reads it.

**Files:**
- Modify: `src/alliance_docs_mcp/server.py` (lines 19, 61, 68, 94-107, 118, 123-127)
- Test: `tests/test_server_state.py` (full-file replacement below; covers the import test, build_state, and apply_state)

**Interfaces:**
- Consumes: nothing new.
- Produces: `ServerState(docs_path, storage, search_index)` (3 fields); `build_state()` and `_apply_state()` no longer reference `related_index`; the module global `related_index` no longer exists.

- [ ] **Step 1: Update the tests first**

(a) In `tests/test_server_state.py`, replace the whole file with:

```python
import alliance_docs_mcp.server as server


def test_import_does_not_build_state():
    # After import, globals are unset until the lifespan runs.
    assert server.storage is None
    assert server.search_index is None


def test_build_state_populates_storage(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    docs.mkdir()
    monkeypatch.setenv("DOCS_DIR", str(docs))
    monkeypatch.setenv("DISABLE_SEARCH_INDEX", "1")

    state = server.build_state()
    assert state.docs_path == docs.resolve()
    assert state.storage is not None
    assert state.search_index is None


def test_apply_state_sets_globals(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    docs.mkdir()
    monkeypatch.setenv("DOCS_DIR", str(docs))
    monkeypatch.setenv("DISABLE_SEARCH_INDEX", "1")

    state = server.build_state()
    server._apply_state(state)
    try:
        assert server.storage is state.storage
        assert server.docs_path == docs.resolve()
    finally:
        server._apply_state(server.ServerState(server.docs_path, None, None))
```

(b) Check whether `tests/test_server.py` (or any other test file) references `server.related_index` or `related_index`:

Run: `grep -rn "related_index" tests/`
Expected after this edit: no matches in `tests/` except `tests/test_search_index_mlt.py`/`tests/test_server_search.py`? Those don't use `related_index`. If any other reference remains (e.g. in `tests/test_server.py`), remove that assertion line as part of this step.

- [ ] **Step 2: Run the test to verify it fails**

Run: `uv run pytest tests/test_server_state.py -v`
Expected: FAIL — `server.ServerState(server.docs_path, None, None)` raises `TypeError` (the dataclass still has 4 fields: `__init__()` missing nothing, but passing 3 positional args to a 4-field dataclass errors), and/or the build still constructs a `related_index`.

- [ ] **Step 3: Apply the server.py removals**

In `src/alliance_docs_mcp/server.py`:

(a) Delete line 19 entirely:

```python
from .related import RelatedIndex, RelatedIndexUnavailable
```

(b) In the `ServerState` dataclass (lines 54-61), delete the `related_index` field so it reads:

```python
@dataclass
class ServerState:
    """Runtime state built once at server startup."""

    docs_path: Path
    storage: DocumentationStorage | None
    search_index: SearchIndex | None
```

(c) Delete the module global on line 68:

```python
related_index: RelatedIndex | None = None
```

(d) Delete the entire `_build_related_index` function (lines 94-107):

```python
def _build_related_index(resolved_docs_path: Path):
    if _env_flag("DISABLE_RELATED_INDEX"):
        logger.info("Related index disabled via DISABLE_RELATED_INDEX")
        return None
    try:
        index_dir = Path(
            os.getenv("RELATED_INDEX_DIR", resolved_docs_path / "related_index")
        )
        model_name = os.getenv("RELATED_MODEL_NAME", "all-MiniLM-L6-v2")
        backend = os.getenv("RELATED_BACKEND", "chroma")
        return RelatedIndex(index_dir, model_name=model_name, backend=backend)
    except Exception as exc:  # pragma: no cover - defensive initialization
        logger.warning("Related index unavailable, using heuristic fallback: %s", exc)
        return None
```

(e) In `build_state()`, remove the `related_index=...` line so it reads:

```python
def build_state() -> ServerState:
    """Discover docs and build indexes. Called once by the lifespan."""
    resolved = _discover_docs_directory()
    doc_storage = DocumentationStorage(str(resolved))
    return ServerState(
        docs_path=resolved,
        storage=doc_storage,
        search_index=_build_search_index(resolved, doc_storage),
    )
```

(f) Rewrite `_apply_state()` (lines 122-127) to drop `related_index`:

```python
def _apply_state(state: ServerState) -> None:
    global docs_path, storage, search_index
    docs_path = state.docs_path
    storage = state.storage
    search_index = state.search_index
```

Leave the `RelatedPage` import on line 18 untouched (still used by `find_related_pages`).

- [ ] **Step 4: Run the tests to verify they pass**

Run: `uv run pytest tests/test_server_state.py tests/test_server_search.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/alliance_docs_mcp/server.py tests/test_server_state.py
git commit -m "refactor: remove related-index state from server"
```

---

### Task 4: Remove related-index plumbing from `scripts/sync_docs.py`

Strip the embeddings index out of the sync script: its import, the `_prepare_related_index` helper, per-page upsert/cleanup, the `_rebuild_all` target, and all CLI flags.

**Files:**
- Modify: `scripts/sync_docs.py` (lines 37, 79-108, 111-126, 152-192, 302-326, 372-406, 480-503, 520-627)

**Interfaces:**
- Consumes: nothing new.
- Produces: `_rebuild_all(docs_dir, index_dir)` (2 args); `sync_documentation(...)` and `sync_incremental(...)` no longer accept any `*_related*` parameters.

- [ ] **Step 1: Delete the import (line 37)**

Remove:

```python
from alliance_docs_mcp.related import RelatedIndex, RelatedIndexUnavailable
```

- [ ] **Step 2: Delete `_prepare_related_index` (lines 79-108)**

Remove the entire function:

```python
def _prepare_related_index(
    docs_dir: str,
    related_index_dir: Optional[str],
    enable_related_index: bool,
    rebuild_related_index: bool,
    related_model_name: str,
    related_backend: str,
) -> Optional[RelatedIndex]:
    """Initialize (and optionally rebuild) the embeddings-based related index."""
    if not enable_related_index:
        logger.info("Related-page indexing disabled (--no-related-index)")
        return None

    resolved_index_dir = (
        Path(related_index_dir) if related_index_dir else Path(docs_dir) / "related_index"
    )

    if rebuild_related_index and resolved_index_dir.exists():
        shutil.rmtree(resolved_index_dir)
        logger.info("Rebuilding related index at %s", resolved_index_dir)

    try:
        return RelatedIndex(
            resolved_index_dir,
            model_name=related_model_name,
            backend=related_backend,
        )
    except RelatedIndexUnavailable as exc:
        logger.warning("Related index unavailable, continuing without it: %s", exc)
        return None
```

- [ ] **Step 3: Update `_rebuild_all` (lines 111-126)**

Replace the signature and `targets` list so the related index is no longer a target:

```python
def _rebuild_all(
    docs_dir: str,
    index_dir: Optional[str],
) -> None:
    """Remove docs content and indexes for a clean rebuild."""
    docs_path = Path(docs_dir)
    targets = [
        docs_path / "pages",
        docs_path / "index.json",
        docs_path / "llms.txt",
        docs_path / "llms_full.txt",
        docs_path / "llms_full.txt.gz",
        Path(index_dir) if index_dir else docs_path / "search_index",
    ]
```

(The `for target in targets:` loop below it is unchanged.)

- [ ] **Step 4: Update `sync_documentation` (lines 152-192)**

(a) Replace its signature (lines 152-163) with:

```python
async def sync_documentation(
    enable_index: bool = True,
    rebuild_index: bool = False,
    index_dir: Optional[str] = None,
    rebuild_all: bool = False,
    strip_html: bool = True,
):
```

(b) Change the `_rebuild_all` call (line 180) to:

```python
    if rebuild_all:
        _rebuild_all(docs_dir, index_dir)
```

(c) Delete the `related_index = _prepare_related_index(...)` assignment (lines 185-192):

```python
    related_index = _prepare_related_index(
        docs_dir,
        related_index_dir,
        enable_related_index,
        rebuild_related_index,
        related_model_name,
        related_backend,
    )
```

- [ ] **Step 5: Remove per-page upsert and cleanup in `sync_documentation` (lines 302-326)**

(a) Delete the related upsert block (lines 302-309):

```python
                    if related_index:
                        try:
                            related_index.upsert_page(saved_page, markdown_content)
                        except RelatedIndexUnavailable as exc:
                            logger.warning("Related index unavailable, skipping: %s", exc)
                        except Exception as exc:  # pragma: no cover - defensive
                            logger.warning("Failed to index related page %s: %s", saved_page["slug"], exc)
```

(b) Delete the related cleanup lines (lines 325-326):

```python
            if related_index:
                related_index.cleanup({page["slug"] for page in saved_pages})
```

(The `if search_index: search_index.optimize()` line directly above stays.)

- [ ] **Step 6: Update `sync_incremental` (lines 372-503)**

(a) Replace its signature (lines 372-383) with:

```python
async def sync_incremental(
    enable_index: bool = True,
    rebuild_index: bool = False,
    index_dir: Optional[str] = None,
    rebuild_all: bool = False,
    strip_html: bool = True,
):
```

(b) Change the `_rebuild_all` call (line 394) to:

```python
    if rebuild_all:
        _rebuild_all(docs_dir, index_dir)
```

(c) Delete the `related_index = _prepare_related_index(...)` assignment (lines 399-406):

```python
    related_index = _prepare_related_index(
        docs_dir,
        related_index_dir,
        enable_related_index,
        rebuild_related_index,
        related_model_name,
        related_backend,
    )
```

(d) Delete the related upsert block (lines 480-487):

```python
                if related_index:
                    try:
                        related_index.upsert_page(saved_page, markdown_content)
                    except RelatedIndexUnavailable as exc:
                        logger.warning("Related index unavailable, skipping: %s", exc)
                    except Exception as exc:  # pragma: no cover - defensive
                        logger.warning("Failed to index related page %s: %s", saved_page["slug"], exc)
```

(e) Delete the related cleanup lines (lines 502-503):

```python
        if related_index:
            related_index.cleanup({page["slug"] for page in existing_by_id.values()})
```

- [ ] **Step 7: Clean up `main()` (lines 520-627)**

(a) Delete the related env-var defaults (lines 524-527), keeping the `strip_html_disabled_env` line:

```python
    related_model_env = os.getenv("RELATED_MODEL_NAME", "all-MiniLM-L6-v2")
    related_index_dir_env = os.getenv("RELATED_INDEX_DIR")
    related_backend_env = os.getenv("RELATED_BACKEND", "chroma")
    related_disabled_env = os.getenv("DISABLE_RELATED_INDEX", "").lower() in ("1", "true", "yes")
```

(b) Delete the five related CLI argument definitions (lines 561-588):

```python
    parser.add_argument(
        "--no-related-index",
        action="store_true",
        help="Skip building/updating the related-page embeddings index",
    )
    parser.add_argument(
        "--rebuild-related-index",
        action="store_true",
        help="Rebuild the related-page index before syncing",
    )
    parser.add_argument(
        "--related-index-dir",
        type=str,
        default=related_index_dir_env,
        help="Optional path for the related-page index (defaults to DOCS_DIR/related_index)",
    )
    parser.add_argument(
        "--related-model-name",
        type=str,
        default=related_model_env,
        help="Sentence-transformer model to use for related-page embeddings",
    )
    parser.add_argument(
        "--related-backend",
        type=str,
        default=related_backend_env,
        help="Related index backend (currently only 'chroma' is supported)",
    )
```

(c) Delete the `disable_related_index` line (line 591):

```python
    disable_related_index = related_disabled_env or args.no_related_index
```

(d) Remove the related kwargs from BOTH `asyncio.run(...)` calls. The incremental call (lines 599-612) becomes:

```python
            result = asyncio.run(
                sync_incremental(
                    enable_index=not args.no_index,
                    rebuild_index=args.rebuild_index,
                    index_dir=args.index_dir,
                    rebuild_all=args.rebuild_all,
                    strip_html=strip_html,
                )
            )
```

The full-sync call (lines 614-627) becomes:

```python
            result = asyncio.run(
                sync_documentation(
                    enable_index=not args.no_index,
                    rebuild_index=args.rebuild_index,
                    index_dir=args.index_dir,
                    rebuild_all=args.rebuild_all,
                    strip_html=strip_html,
                )
            )
```

- [ ] **Step 8: Verify the script imports and parses cleanly**

Run: `uv run python scripts/sync_docs.py --help`
Expected: argparse help prints with NO `--related-*` / `--no-related-index` options listed, and no import error (it must not import `alliance_docs_mcp.related`).

Also confirm no stray references remain:
Run: `grep -n "related" scripts/sync_docs.py`
Expected: no matches.

- [ ] **Step 9: Commit**

```bash
git add scripts/sync_docs.py
git commit -m "refactor: remove related-index plumbing from sync script"
```

---

### Task 5: Delete the `related` package and its dependencies

With no remaining importers, delete the package, its test, and the three heavy dependencies.

**Files:**
- Delete: `src/alliance_docs_mcp/related/` (whole directory), `tests/test_related_index.py`
- Modify: `pyproject.toml` (dependencies array, lines 7-20)

**Interfaces:**
- Consumes: nothing.
- Produces: a dependency set with no `chromadb`, `sentence-transformers`, or `numpy`.

- [ ] **Step 1: Confirm there are no remaining importers**

Run:
```bash
grep -rn "alliance_docs_mcp.related\|from .related\|import RelatedIndex\|RelatedIndexUnavailable\|sentence_transformers\|chromadb\|^import numpy\|import numpy\b\|from numpy" src/ scripts/ tests/
```
Expected: no matches. (`RelatedPage` is a different symbol and will not appear here.) If anything matches, stop and fix that reference before deleting the package.

- [ ] **Step 2: Delete the package and its test**

```bash
git rm -r src/alliance_docs_mcp/related
git rm tests/test_related_index.py
```

- [ ] **Step 3: Remove the dependencies from `pyproject.toml`**

In `pyproject.toml`, delete these three lines from the `dependencies` array (lines 9, 12, 17):

```python
    "chromadb>=0.6.3",
    "numpy>=1.26.0",
    "sentence-transformers>=2.2.0",
```

The resulting `dependencies` array must be:

```toml
dependencies = [
    "beautifulsoup4>=4.12.0",
    "fastmcp>=3.0,<4",
    "langdetect>=1.0.9",
    "python-dotenv>=1.1.1",
    "pyyaml>=6.0.3",
    "requests>=2.32.5",
    "rich>=14.2.0",
    "whoosh>=2.7.4",
    "wikitextparser>=0.56.0",
]
```

- [ ] **Step 4: Re-lock dependencies**

Run: `uv lock`
Expected: lock succeeds; `uv.lock` no longer pins `torch`, `chromadb`, `sentence-transformers`, or `numpy` as project deps. Verify with:
Run: `grep -c "name = \"torch\"" uv.lock`
Expected: `0`.

- [ ] **Step 5: Run the full test suite**

Run: `uv run pytest -v`
Expected: PASS — all remaining tests green, no collection/import errors (in particular no module tries to import the deleted `related` package).

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "chore: delete embeddings package and heavy dependencies (chromadb, sentence-transformers, numpy)"
```

---

### Task 6: Update docs and `.gitignore`

Reframe the related-pages feature as Whoosh-backed and remove all embeddings/model references.

**Files:**
- Modify: `README.md`, `.gitignore` (line 50)

**Interfaces:** none (docs only).

- [ ] **Step 1: Update `.gitignore`**

Delete line 50:

```
docs/related_index/
```

- [ ] **Step 2: Update the Features bullet in `README.md`**

Replace:

```markdown
- **Related Pages**: Embeddings-backed related-page discovery with heuristic fallback
```

with:

```markdown
- **Related Pages**: Whoosh content-similarity ("more like this") related-page discovery with heuristic fallback
```

- [ ] **Step 3: Update the `find_related_pages` tool docs in `README.md`**

Replace this block:

```markdown
#### `find_related_pages(slug: str, limit: int = 5)`
Embeddings-backed related-pages helper (Chroma + sentence-transformers) with automatic fallback to lightweight heuristics.

**Parameters:**
- `slug`: Source page slug
- `limit`: Max related pages to return
- `min_score`: Optional similarity threshold when embeddings are available

**Returns:** List of related pages with similarity scores (or heuristic scores when falling back)
```

with:

```markdown
#### `find_related_pages(slug: str, limit: int = 5)`
Finds related pages via Whoosh content similarity ("more like this"), with automatic fallback to a lightweight title/category heuristic.

**Parameters:**
- `slug`: Source page slug
- `limit`: Max related pages to return

**Returns:** List of related pages with relevance scores (or heuristic scores when falling back)
```

- [ ] **Step 4: Remove the related-index sync commands and model note in `README.md`**

In the "Index controls" code block, delete these four lines:

```bash
uv run python scripts/sync_docs.py --rebuild-related-index     # Rebuild related-page embeddings
uv run python scripts/sync_docs.py --no-related-index          # Skip related-page embeddings
uv run python scripts/sync_docs.py --related-index-dir /tmp/rel# Custom related index location
uv run python scripts/sync_docs.py --related-model-name all-MiniLM-L6-v2
```

And delete the model-download note that follows the block:

```markdown
The related-page index downloads the configured sentence-transformer model (default: `all-MiniLM-L6-v2`, ~90 MB) the first time it runs.
```

- [ ] **Step 5: Remove the related env vars in `README.md`**

In the "Environment Variables" list, delete these four lines:

```markdown
- `RELATED_INDEX_DIR` (optional; overrides default `DOCS_DIR/related_index`)
- `RELATED_MODEL_NAME` (sentence-transformer model, default `all-MiniLM-L6-v2`)
- `RELATED_BACKEND` (default `chroma`)
- `DISABLE_RELATED_INDEX` (set to `1/true/yes` to skip related-page embeddings)
```

- [ ] **Step 6: Verify no stale references remain in docs**

Run: `grep -rn "embedding\|sentence-transformer\|sentence_transformer\|chroma\|RELATED_\|min_score\|related-page index\|related_index" README.md .gitignore`
Expected: no matches.

- [ ] **Step 7: Commit**

```bash
git add README.md .gitignore
git commit -m "docs: reframe related pages as Whoosh-backed; drop embeddings references"
```

---

## Final verification (after all tasks)

- [ ] Run the full suite once more: `uv run pytest -v` → all green.
- [ ] Confirm the dependency removal end-to-end: `grep -c "name = \"torch\"" uv.lock` → `0`.
- [ ] Confirm the tool surface: `grep -n "min_score" src/alliance_docs_mcp/server.py` → no matches.
