# FastMCP v3 Modernization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the Alliance Docs MCP server from FastMCP 2.12.5 to 3.x and adopt v3 best practices (lifespan-based init, lazy resource templates, structured output, `ToolError`, `fastmcp.json`).

**Architecture:** Move all import-time initialization (docs discovery, search/related indexes, per-page resource registration) into a FastMCP `lifespan` that populates module-level state. Serve page content through a lazy resource *template* plus a JSON index resource. Give every tool typed Pydantic output models, read-only annotations, and `ToolError` on genuine failures.

**Tech Stack:** Python 3.11+, `uv`, FastMCP 3.x, Pydantic, Whoosh (search), sentence-transformers + ChromaDB (related), pytest / pytest-asyncio.

## Global Constraints

- `fastmcp>=3.0,<4` — pin in `pyproject.toml`. (Lands on 3.4.x; v3.4.1 floors Starlette `>=1.0.1` for CVE-2026-48710 — `uv` resolves cleanly.)
- Use `uv` for all Python management/execution (`uv add`, `uv run`, `uv lock`). Never `uv pip install`. Never pin versions beyond the floor unless required.
- No `fastmcp[tasks]` extra — no background tasks are used.
- Resource URIs stay exactly `alliance-docs://page/{slug}` (now served via template, not eager registration).
- All 8 tools are read-only: annotate `readOnlyHint=True, idempotentHint=True`.
- Deferred / DO NOT add: Context logging, progress reporting, OpenTelemetry, Tool Search transform.
- TDD: write the failing test first, watch it fail, implement minimally, watch it pass, commit. Frequent commits.
- End every commit message with:
  `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

---

### Task 1: Upgrade FastMCP dependency to v3

**Files:**
- Modify: `pyproject.toml` (the `fastmcp` line under `[project].dependencies`)
- Modify: `uv.lock` (regenerated)

**Interfaces:**
- Produces: a working `fastmcp` 3.x install; baseline pytest result the later tasks build on.

- [ ] **Step 1: Update the version floor**

In `pyproject.toml`, change:
```toml
    "fastmcp>=2.12.5",
```
to:
```toml
    "fastmcp>=3.0,<4",
```

- [ ] **Step 2: Resolve and lock**

Run: `uv lock`
Expected: completes; `fastmcp` resolves to a `3.x` version.

- [ ] **Step 3: Verify the installed major version**

Run: `uv run python -c "import fastmcp; print(fastmcp.__version__)"`
Expected: prints a version starting with `3.`

- [ ] **Step 4: Capture the baseline test run**

Run: `uv run pytest -q`
Expected: the suite runs to completion. Record pass/fail counts. The existing
code uses conservative v2 patterns (no removed kwargs, no `ctx.set_state`, no
auth env-magic, prompts return plain strings), so imports should succeed.
If any test errors are import/collection errors from the upgrade itself, note
them — later tasks (3, 5–7) refactor the affected code; pre-existing failures
unrelated to this plan should be left as-is and flagged.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "chore: upgrade fastmcp to v3

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: Add typed result models

**Files:**
- Create: `src/alliance_docs_mcp/models.py`
- Test: `tests/test_models.py`

**Interfaces:**
- Produces:
  - `PageSummary(title, url, category, slug, last_modified)` — all `str | None`.
  - `SearchHit(PageSummary + score: float | None, snippet: str | None, highlights: str | None)`.
  - `RelatedPage(PageSummary + score: float | None)`.
  - `PageInfo(PageSummary + page_id: int | None, metadata: dict)`.
  - `PageIndexEntry(slug: str, title, url, category)` — used by the index resource.

- [ ] **Step 1: Write the failing test**

Create `tests/test_models.py`:
```python
from alliance_docs_mcp.models import (
    PageInfo,
    PageIndexEntry,
    PageSummary,
    RelatedPage,
    SearchHit,
)


def test_page_summary_defaults_are_none():
    summary = PageSummary()
    assert summary.title is None
    assert summary.slug is None


def test_search_hit_carries_score_and_snippet():
    hit = SearchHit(slug="gpu", score=1.5, snippet="<b>GPU</b> jobs")
    assert hit.slug == "gpu"
    assert hit.score == 1.5
    assert hit.snippet == "<b>GPU</b> jobs"


def test_related_page_has_score():
    rel = RelatedPage(slug="x", score=0.9)
    assert rel.score == 0.9


def test_page_info_has_metadata_dict():
    info = PageInfo(slug="x", page_id=12, metadata={"k": "v"})
    assert info.page_id == 12
    assert info.metadata == {"k": "v"}


def test_page_index_entry_requires_slug():
    entry = PageIndexEntry(slug="abc")
    assert entry.slug == "abc"
    assert entry.title is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_models.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'alliance_docs_mcp.models'`

- [ ] **Step 3: Write the models**

Create `src/alliance_docs_mcp/models.py`:
```python
"""Typed result models for Alliance Docs MCP tools and resources."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PageSummary(BaseModel):
    """Lightweight metadata shared by most tool results."""

    title: str | None = None
    url: str | None = None
    category: str | None = None
    slug: str | None = None
    last_modified: str | None = None


class SearchHit(PageSummary):
    """A single search result with relevance scoring."""

    score: float | None = Field(
        default=None, description="Relevance score; higher is more relevant."
    )
    snippet: str | None = Field(
        default=None, description="Highlighted excerpt showing the match."
    )
    highlights: str | None = Field(
        default=None, description="Raw highlighted fragments from the index."
    )


class RelatedPage(PageSummary):
    """A related page with a similarity score."""

    score: float | None = Field(
        default=None, description="Similarity score; higher is more related."
    )


class PageInfo(PageSummary):
    """Detailed metadata for a single page."""

    page_id: int | None = None
    metadata: dict = Field(default_factory=dict)


class PageIndexEntry(BaseModel):
    """Entry in the `alliance-docs://pages` discovery index."""

    slug: str
    title: str | None = None
    url: str | None = None
    category: str | None = None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_models.py -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Commit**

```bash
git add src/alliance_docs_mcp/models.py tests/test_models.py
git commit -m "feat: add typed result models for tools and resources

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Move initialization into a lifespan

**Files:**
- Modify: `src/alliance_docs_mcp/server.py` (lines ~20–96 init block, ~114–167 resource registration, ~649–678 `main`)
- Test: `tests/test_server_state.py`

**Interfaces:**
- Consumes: `DocumentationStorage`, `SearchIndex`, `RelatedIndex` (unchanged).
- Produces:
  - `ServerState` dataclass: `docs_path: Path`, `storage: DocumentationStorage`, `search_index: SearchIndex | None`, `related_index: RelatedIndex | None`.
  - `build_state() -> ServerState` — encapsulates env-flag logic + index construction.
  - `_apply_state(state: ServerState) -> None` — assigns module globals `docs_path`, `storage`, `search_index`, `related_index`.
  - Module globals `storage`, `search_index`, `related_index`, `docs_path` (default `None`) — read by tools/resources, monkeypatchable by tests.
  - `app_lifespan` registered on `mcp`.

**Background:** Today `server.py` builds everything at import time, including reading every page into memory. This task removes that. The per-page `TextResource` registration (`_register_document_resources`) is **deleted** here; Task 4 replaces it with a template. Between Task 3 and Task 4 there are no page resources — that is acceptable (each task is independently testable).

- [ ] **Step 1: Write the failing test**

Create `tests/test_server_state.py`:
```python
import alliance_docs_mcp.server as server


def test_import_does_not_build_state():
    # After import, globals are unset until the lifespan runs.
    assert server.storage is None
    assert server.search_index is None
    assert server.related_index is None


def test_build_state_populates_storage(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    docs.mkdir()
    monkeypatch.setenv("DOCS_DIR", str(docs))
    monkeypatch.setenv("DISABLE_SEARCH_INDEX", "1")
    monkeypatch.setenv("DISABLE_RELATED_INDEX", "1")

    state = server.build_state()
    assert state.docs_path == docs.resolve()
    assert state.storage is not None
    assert state.search_index is None
    assert state.related_index is None


def test_apply_state_sets_globals(tmp_path, monkeypatch):
    docs = tmp_path / "docs"
    docs.mkdir()
    monkeypatch.setenv("DOCS_DIR", str(docs))
    monkeypatch.setenv("DISABLE_SEARCH_INDEX", "1")
    monkeypatch.setenv("DISABLE_RELATED_INDEX", "1")

    state = server.build_state()
    server._apply_state(state)
    try:
        assert server.storage is state.storage
        assert server.docs_path == docs.resolve()
    finally:
        server._apply_state(
            server.ServerState(server.docs_path, None, None, None)
        )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_server_state.py -v`
Expected: FAIL — `AttributeError: module 'alliance_docs_mcp.server' has no attribute 'build_state'` (and `storage` is currently a real object, not `None`).

- [ ] **Step 3: Refactor server.py initialization**

In `src/alliance_docs_mcp/server.py`:

(a) Update imports at the top — add `dataclass`, `asynccontextmanager` is not needed (use the `@lifespan` decorator). Keep existing imports; remove `from fastmcp.resources import TextResource` (no longer used after Task 3 deletes eager registration — Task 4 does not reintroduce it). Add:
```python
from dataclasses import dataclass

from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan
```

(b) Replace the entire block from `mcp = FastMCP("Alliance Docs")` (line ~21) through the end of `_register_document_resources()` and its call `_register_document_resources()` (line ~167) with:

```python
@dataclass
class ServerState:
    """Runtime state built once at server startup."""

    docs_path: Path
    storage: DocumentationStorage | None
    search_index: SearchIndex | None
    related_index: RelatedIndex | None


# Module-level state, populated by the lifespan. Tools and resources read these.
docs_path: Path | None = None
storage: DocumentationStorage | None = None
search_index: SearchIndex | None = None
related_index: RelatedIndex | None = None


def _env_flag(name: str) -> bool:
    return os.getenv(name, "").lower() in ("1", "true", "yes")


def _build_search_index(resolved_docs_path: Path, doc_storage: DocumentationStorage):
    if _env_flag("DISABLE_SEARCH_INDEX"):
        logger.info("Search index disabled via DISABLE_SEARCH_INDEX")
        return None
    try:
        index_dir = Path(
            os.getenv("SEARCH_INDEX_DIR", resolved_docs_path / "search_index")
        )
        index = SearchIndex(index_dir)
        if index.is_empty():
            logger.info("Search index is empty, populating from documentation...")
            count = index.populate_from_storage(doc_storage)
            logger.info("Populated search index with %s pages", count)
        return index
    except Exception as exc:  # pragma: no cover - defensive initialization
        logger.warning("Search index unavailable, using title search: %s", exc)
        return None


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


def build_state() -> ServerState:
    """Discover docs and build indexes. Called once by the lifespan."""
    resolved = _discover_docs_directory()
    doc_storage = DocumentationStorage(str(resolved))
    return ServerState(
        docs_path=resolved,
        storage=doc_storage,
        search_index=_build_search_index(resolved, doc_storage),
        related_index=_build_related_index(resolved),
    )


def _apply_state(state: ServerState) -> None:
    global docs_path, storage, search_index, related_index
    docs_path = state.docs_path
    storage = state.storage
    search_index = state.search_index
    related_index = state.related_index


@lifespan
async def app_lifespan(server):
    """Build runtime state on startup; nothing to tear down."""
    _apply_state(build_state())
    logger.info("Alliance Docs MCP server state initialized")
    try:
        yield {}
    finally:
        pass


mcp = FastMCP("Alliance Docs", lifespan=app_lifespan)
```

Keep `_discover_docs_directory` and `_resolve_page_path` exactly as they are (they read the `docs_path` global at call time for `_resolve_page_path`; `_discover_docs_directory` is self-contained).

(c) Slim `main()` (bottom of file) to remove the broken argparse `--docs-dir` global-mutation path:
```python
def main():
    """Run the MCP server over stdio (local development)."""
    import argparse

    parser = argparse.ArgumentParser(description="Alliance Docs MCP Server")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info("Starting Alliance Docs MCP Server")
    mcp.run()


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the new test to verify it passes**

Run: `uv run pytest tests/test_server_state.py -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Run the existing server/prompt tests**

Run: `uv run pytest tests/test_server_search.py tests/test_prompts.py -v`
Expected: `test_prompts.py` PASSES. `test_server_search.py` PASSES — those tests
`monkeypatch.setattr(server, "storage", ...)` / `search_index` / `related_index`,
which still exist as module globals.

- [ ] **Step 6: Commit**

```bash
git add src/alliance_docs_mcp/server.py tests/test_server_state.py
git commit -m "refactor: build server state in a lifespan instead of at import

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Add lazy resource template + index resource

**Files:**
- Modify: `src/alliance_docs_mcp/server.py` (add resource functions after `_resolve_page_path`)
- Test: `tests/test_server_resources.py`

**Interfaces:**
- Consumes: module globals `storage`, `docs_path`; `_resolve_page_path`; `PageIndexEntry` from `models`.
- Produces:
  - `page_resource(slug) -> str` registered at `alliance-docs://page/{slug}` (`text/markdown`). Raises `ResourceError` if slug unknown or file missing.
  - `pages_index() -> list[dict]` registered at `alliance-docs://pages` (`application/json`).

- [ ] **Step 1: Write the failing test**

Create `tests/test_server_resources.py`:
```python
import gzip

import pytest

import alliance_docs_mcp.server as server
from fastmcp.exceptions import ResourceError


class DummyStorage:
    def __init__(self, pages):
        self._pages = pages

    def get_all_pages(self):
        return self._pages

    def get_page_by_slug(self, slug):
        return next((p for p in self._pages if p["slug"] == slug), None)


def _setup(tmp_path, monkeypatch, *, gz=False):
    page_file = tmp_path / ("gpu.md.gz" if gz else "gpu.md")
    body = "# GPU\nUse --gpus-per-node."
    if gz:
        with gzip.open(page_file, "wt", encoding="utf-8") as fh:
            fh.write(body)
    else:
        page_file.write_text(body, encoding="utf-8")

    pages = [
        {
            "slug": "gpu",
            "title": "GPU Guide",
            "url": "https://example.com/gpu",
            "category": "Technical",
            "file_path": str(page_file),
        }
    ]
    monkeypatch.setattr(server, "storage", DummyStorage(pages))
    monkeypatch.setattr(server, "docs_path", tmp_path)
    return body


def test_page_resource_reads_markdown(tmp_path, monkeypatch):
    body = _setup(tmp_path, monkeypatch)
    assert server.page_resource("gpu") == body


def test_page_resource_reads_gzip(tmp_path, monkeypatch):
    body = _setup(tmp_path, monkeypatch, gz=True)
    assert server.page_resource("gpu") == body


def test_page_resource_unknown_slug_raises(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    with pytest.raises(ResourceError):
        server.page_resource("does-not-exist")


def test_pages_index_lists_entries(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    entries = server.pages_index()
    assert entries == [
        {
            "slug": "gpu",
            "title": "GPU Guide",
            "url": "https://example.com/gpu",
            "category": "Technical",
        }
    ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_server_resources.py -v`
Expected: FAIL — `AttributeError: module 'alliance_docs_mcp.server' has no attribute 'page_resource'`

- [ ] **Step 3: Add the resource functions**

In `src/alliance_docs_mcp/server.py`, add this import near the other `from` imports:
```python
from fastmcp.exceptions import ResourceError
from .models import PageIndexEntry
```

Then, after `_resolve_page_path` (and after `mcp` is defined), add:
```python
@mcp.resource("alliance-docs://page/{slug}", mime_type="text/markdown")
def page_resource(slug: str) -> str:
    """Return the markdown content of a documentation page, loaded on demand."""
    page = storage.get_page_by_slug(slug)
    if not page:
        raise ResourceError(f"Page not found: {slug}")

    absolute_path = _resolve_page_path(page["file_path"])
    if not absolute_path.exists():
        raise ResourceError(f"Page file missing on disk: {slug}")

    if absolute_path.suffix == ".gz":
        with gzip.open(absolute_path, "rt", encoding="utf-8") as handle:
            return handle.read()
    return absolute_path.read_text(encoding="utf-8")


@mcp.resource("alliance-docs://pages", mime_type="application/json")
def pages_index() -> list[dict]:
    """Discovery index: every page's slug, title, url, and category."""
    return [
        PageIndexEntry(
            slug=page["slug"],
            title=page.get("title"),
            url=page.get("url"),
            category=page.get("category"),
        ).model_dump()
        for page in storage.get_all_pages()
    ]
```

Note: `page_resource` must be defined *after* `mcp = FastMCP(...)`. Place these
functions below the lifespan/`mcp` definition block from Task 3.

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_server_resources.py -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add src/alliance_docs_mcp/server.py tests/test_server_resources.py
git commit -m "feat: serve pages via lazy resource template + index resource

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 5: Structured output + ToolError for search_docs

**Files:**
- Modify: `src/alliance_docs_mcp/server.py` (`_search_docs_impl`, `search_docs`)
- Modify: `tests/test_server_search.py` (the two `search_docs` tests)

**Interfaces:**
- Consumes: `SearchHit`, `PageSummary` from `models`; `ToolError` from `fastmcp.exceptions`.
- Produces: `_search_docs_impl(...) -> list[SearchHit]`; `search_docs` tool returns `list[SearchHit]`, annotated read-only.

- [ ] **Step 1: Update the failing tests**

In `tests/test_server_search.py`, replace `test_search_docs_uses_index` and
`test_search_docs_falls_back_without_index` with attribute-based assertions:
```python
@pytest.mark.asyncio
async def test_search_docs_uses_index(monkeypatch, tmp_path):
    import alliance_docs_mcp.server as server

    search_index = SearchIndex(tmp_path / "search_index")
    search_index.index_page(
        slug="gpu_guide",
        title="GPU Usage Guide",
        content="Use --gpus-per-node flags for GPU jobs.",
        category="Technical",
        url="https://example.com/gpu",
        last_modified="2025-01-01T00:00:00Z",
    )

    monkeypatch.setattr(server, "storage", DummyStorage())
    monkeypatch.setattr(server, "search_index", search_index)

    results = await server._search_docs_impl("GPU", limit=5, search_content=True)
    assert results
    assert results[0].slug == "gpu_guide"
    assert results[0].score is not None
    assert results[0].snippet is not None


@pytest.mark.asyncio
async def test_search_docs_falls_back_without_index(monkeypatch):
    import alliance_docs_mcp.server as server

    dummy_storage = DummyStorage()
    monkeypatch.setattr(server, "storage", dummy_storage)
    monkeypatch.setattr(server, "search_index", None)

    results = await server._search_docs_impl("Test", limit=5, search_content=True)
    assert results
    assert results[0].title == "Test Page"
    assert results[0].score is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_server_search.py -k search_docs -v`
Expected: FAIL — `AttributeError: 'dict' object has no attribute 'slug'` (impl still returns dicts).

- [ ] **Step 3: Rewrite the search impl and tool**

In `src/alliance_docs_mcp/server.py`, add to the imports:
```python
from typing import Annotated
from pydantic import Field
from mcp.types import ToolAnnotations
from fastmcp.exceptions import ToolError
from .models import PageInfo, PageSummary, RelatedPage, SearchHit
```
(Merge with the `from .models import PageIndexEntry` line added in Task 4 into a
single import: `from .models import PageIndexEntry, PageInfo, PageSummary, RelatedPage, SearchHit`.)

Replace `_search_docs_impl` with:
```python
async def _search_docs_impl(
    query: str,
    category: Optional[str] = None,
    limit: int = 20,
    search_content: bool = True,
    fuzzy: bool = False,
) -> List[SearchHit]:
    """Core search implementation used by the MCP tool and tests."""
    if search_content and search_index:
        try:
            hits = search_index.search(
                query, category=category, limit=limit, fuzzy=fuzzy
            )
            return [
                SearchHit(
                    title=hit.get("title"),
                    url=hit.get("url"),
                    category=hit.get("category"),
                    slug=hit.get("slug"),
                    last_modified=hit.get("last_modified"),
                    score=hit.get("score"),
                    snippet=hit.get("highlights"),
                    highlights=hit.get("highlights"),
                )
                for hit in hits
            ]
        except SearchIndexUnavailable:
            logger.warning("Search index unavailable, using file-based search")
        except Exception as exc:
            logger.error("Full-text search failed: %s", exc, exc_info=True)
            raise ToolError(f"Search failed: {exc}") from exc

    try:
        pages = storage.search_pages(query, category)
    except Exception as exc:
        logger.error("File-based search failed: %s", exc, exc_info=True)
        raise ToolError(f"Search failed: {exc}") from exc

    return [
        SearchHit(
            title=page["title"],
            url=page["url"],
            category=page["category"],
            slug=page["slug"],
            last_modified=page["last_modified"],
        )
        for page in pages[:limit]
    ]
```

Replace the `search_docs` tool with annotated parameters and structured output:
```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
async def search_docs(
    query: Annotated[str, Field(description="Search terms to look for.")],
    category: Annotated[
        Optional[str], Field(description="Restrict results to this category.")
    ] = None,
    limit: Annotated[int, Field(description="Maximum number of results.")] = 20,
    search_content: Annotated[
        bool, Field(description="Search full page content, not just titles.")
    ] = True,
    fuzzy: Annotated[
        bool, Field(description="Allow approximate (fuzzy) matches.")
    ] = False,
) -> List[SearchHit]:
    """Search documentation with optional full-text index and relevance ranking.

    Returns an empty list when nothing matches; raises on backend failure.
    """
    return await _search_docs_impl(query, category, limit, search_content, fuzzy)
```

Note: a *successful but empty* search returns `[]`; only genuine backend
failures raise `ToolError`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_server_search.py -k search_docs -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add src/alliance_docs_mcp/server.py tests/test_server_search.py
git commit -m "feat: structured output and ToolError for search_docs

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 6: Structured output for find_related_pages

**Files:**
- Modify: `src/alliance_docs_mcp/server.py` (`_heuristic_related`, `_find_related_pages_impl`, `find_related_pages`)
- Modify: `tests/test_server_search.py` (the two `find_related` tests)

**Interfaces:**
- Consumes: `RelatedPage` from `models`; `ToolError`.
- Produces: `_find_related_pages_impl(...) -> list[RelatedPage]`; `find_related_pages` tool returns `list[RelatedPage]`, read-only.

- [ ] **Step 1: Update the failing tests**

In `tests/test_server_search.py`, replace `test_find_related_pages_uses_related_index`
and `test_find_related_pages_falls_back`:
```python
@pytest.mark.asyncio
async def test_find_related_pages_uses_related_index(monkeypatch):
    import alliance_docs_mcp.server as server

    dummy_storage = DummyStorage()
    related_result = [
        {
            "title": "Related Result",
            "url": "https://example.com/related",
            "category": "General",
            "slug": "related",
            "score": 0.9,
        }
    ]

    monkeypatch.setattr(server, "storage", dummy_storage)
    dummy_related = DummyRelatedIndex(results=related_result)
    monkeypatch.setattr(server, "related_index", dummy_related)

    results = await server._find_related_pages_impl("test_page", limit=3)
    assert dummy_related.called is True
    assert results[0].slug == "related"
    assert results[0].score == 0.9


@pytest.mark.asyncio
async def test_find_related_pages_falls_back(monkeypatch):
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
    monkeypatch.setattr(server, "related_index", None)

    results = await server._find_related_pages_impl("test_page", limit=3)
    assert results
    assert results[0].slug == "test_page_2"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_server_search.py -k related -v`
Expected: FAIL — `AttributeError: 'dict' object has no attribute 'slug'`

- [ ] **Step 3: Rewrite the related impl, heuristic, and tool**

Replace `_heuristic_related` with a version that returns models:
```python
def _heuristic_related(page: dict, limit: int) -> List[RelatedPage]:
    """Lightweight heuristic fallback for related pages."""
    base_tokens = set((page.get("title", "") or "").lower().split())
    candidates = []

    for candidate in storage.get_all_pages():
        if candidate.get("slug") == page.get("slug"):
            continue

        score = 0
        if candidate.get("category") == page.get("category"):
            score += 2
        candidate_tokens = set((candidate.get("title", "") or "").lower().split())
        score += len(base_tokens.intersection(candidate_tokens))

        if score > 0:
            candidates.append((score, candidate))

    candidates.sort(key=lambda item: item[0], reverse=True)
    return [
        RelatedPage(
            title=candidate["title"],
            url=candidate["url"],
            category=candidate["category"],
            slug=candidate["slug"],
            score=float(score),
        )
        for score, candidate in candidates[:limit]
    ]
```

Replace `_find_related_pages_impl`:
```python
async def _find_related_pages_impl(
    slug: str, limit: int = 5, min_score: float = 0.0
) -> List[RelatedPage]:
    """Core related-pages implementation for tool and tests."""
    page = storage.get_page_by_slug(slug)
    if not page:
        raise ToolError(f"Page not found: {slug}")

    if related_index:
        try:
            results = related_index.find_related(slug, limit=limit, min_score=min_score)
            if results:
                return [RelatedPage(**hit) for hit in results]
        except RelatedIndexUnavailable as exc:
            logger.warning("Related index unavailable for %s: %s", slug, exc)
        except Exception as exc:
            logger.error("Related index error for %s: %s", slug, exc, exc_info=True)

    return _heuristic_related(page, limit)
```

Replace the `find_related_pages` tool:
```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
async def find_related_pages(
    slug: Annotated[str, Field(description="Slug of the page to find relations for.")],
    limit: Annotated[int, Field(description="Maximum number of related pages.")] = 5,
    min_score: Annotated[
        float, Field(description="Minimum similarity score to include.")
    ] = 0.0,
) -> List[RelatedPage]:
    """Find related pages using embeddings when available, with heuristic fallback."""
    return await _find_related_pages_impl(slug, limit, min_score)
```

Note: the `RelatedPage(**hit)` call assumes related-index hits contain only
keys that map to `RelatedPage` fields (`title`, `url`, `category`, `slug`,
`score`, `last_modified`). That matches `DummyRelatedIndex` and the real index's
output. If the real index ever adds extra keys, switch to explicit field mapping.

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_server_search.py -k related -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add src/alliance_docs_mcp/server.py tests/test_server_search.py
git commit -m "feat: structured output and ToolError for find_related_pages

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 7: Modernize the remaining tools

**Files:**
- Modify: `src/alliance_docs_mcp/server.py` (`list_categories`, `get_page_by_title`, `list_recent_updates`, `get_page_info`, `list_all_pages`, `get_page_content`)
- Test: `tests/test_server_tools.py`

**Interfaces:**
- Consumes: `PageSummary`, `PageInfo` from `models`; `ToolError`; `ToolAnnotations`.
- Produces (read-only annotations on all):
  - `list_categories() -> list[str]`
  - `get_page_by_title(title) -> PageSummary | None` (miss → `None`; that's a legitimate empty result)
  - `list_recent_updates(limit) -> list[PageSummary]`
  - `get_page_info(slug) -> PageInfo` (miss → `ToolError`)
  - `list_all_pages() -> list[PageSummary]`
  - `get_page_content(slug) -> str` (miss → `ToolError`)

- [ ] **Step 1: Write the failing tests**

Create `tests/test_server_tools.py`:
```python
import pytest

import alliance_docs_mcp.server as server
from fastmcp.exceptions import ToolError


class StubStorage:
    def __init__(self):
        self.pages = [
            {
                "title": "Alpha",
                "url": "https://example.com/alpha",
                "category": "General",
                "slug": "alpha",
                "last_modified": "2025-01-01T00:00:00Z",
                "page_id": 1,
                "file_path": "alpha.md",
            }
        ]

    def get_all_pages(self):
        return self.pages

    def get_recent_pages(self, limit):
        return self.pages[:limit]

    def get_categories(self):
        return ["General"]

    def search_pages(self, query, category=None):
        q = query.lower()
        return [p for p in self.pages if q in p["title"].lower()]

    def get_page_by_slug(self, slug):
        return next((p for p in self.pages if p["slug"] == slug), None)

    def load_page(self, file_path):
        return {"content": "# Alpha\nbody", "metadata": {"k": "v"}}


@pytest.fixture
def stub(monkeypatch):
    s = StubStorage()
    monkeypatch.setattr(server, "storage", s)
    return s


@pytest.mark.asyncio
async def test_list_all_pages_returns_summaries(stub):
    pages = await server.list_all_pages()
    assert pages[0].slug == "alpha"


@pytest.mark.asyncio
async def test_get_page_by_title_hit_and_miss(stub):
    hit = await server.get_page_by_title("Alpha")
    assert hit.slug == "alpha"
    miss = await server.get_page_by_title("Nonexistent")
    assert miss is None


@pytest.mark.asyncio
async def test_get_page_info_missing_raises(stub):
    with pytest.raises(ToolError):
        await server.get_page_info("ghost")


@pytest.mark.asyncio
async def test_get_page_content_missing_raises(stub):
    with pytest.raises(ToolError):
        await server.get_page_content("ghost")


@pytest.mark.asyncio
async def test_get_page_content_hit(stub):
    content = await server.get_page_content("alpha")
    assert "Alpha" in content
```

Note: in FastMCP v3, `@mcp.tool` returns the **original function** unchanged, so
`server.list_all_pages` is directly callable (as shown above). The tool is still
registered on `mcp` for clients.

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_server_tools.py -v`
Expected: FAIL — current `get_page_info`/`get_page_content` return values
(`None` / `"Page not found: ..."`) instead of raising; `list_all_pages` returns
dicts, not `PageSummary`.

- [ ] **Step 3: Rewrite the six tools**

In `src/alliance_docs_mcp/server.py`, replace each tool. Decorate all with
`@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))`.

```python
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
async def list_categories() -> List[str]:
    """List all available documentation categories."""
    return storage.get_categories()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
async def get_page_by_title(
    title: Annotated[str, Field(description="Exact page title to look up.")],
) -> Optional[PageSummary]:
    """Find a page by exact title. Returns None when no page matches."""
    for page in storage.search_pages(title):
        if page["title"].lower() == title.lower():
            return PageSummary(
                title=page["title"],
                url=page["url"],
                category=page["category"],
                slug=page["slug"],
                last_modified=page["last_modified"],
            )
    return None


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
async def list_recent_updates(
    limit: Annotated[int, Field(description="Maximum number of pages.")] = 10,
) -> List[PageSummary]:
    """List recently updated pages."""
    return [
        PageSummary(
            title=page["title"],
            url=page["url"],
            category=page["category"],
            slug=page["slug"],
            last_modified=page["last_modified"],
        )
        for page in storage.get_recent_pages(limit)
    ]


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
async def get_page_info(
    slug: Annotated[str, Field(description="Slug of the page.")],
) -> PageInfo:
    """Get detailed metadata about a page. Raises if the page does not exist."""
    page_data = storage.get_page_by_slug(slug)
    if not page_data:
        raise ToolError(f"Page not found: {slug}")

    page_content = storage.load_page(page_data["file_path"])
    if not page_content:
        raise ToolError(f"Could not load page: {slug}")

    return PageInfo(
        title=page_data["title"],
        url=page_data["url"],
        category=page_data["category"],
        slug=page_data["slug"],
        last_modified=page_data["last_modified"],
        page_id=page_data["page_id"],
        metadata=page_content["metadata"],
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
async def list_all_pages() -> List[PageSummary]:
    """List all available documentation pages."""
    return [
        PageSummary(
            title=page["title"],
            url=page["url"],
            category=page["category"],
            slug=page["slug"],
            last_modified=page["last_modified"],
        )
        for page in storage.get_all_pages()
    ]


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
async def get_page_content(
    slug: Annotated[str, Field(description="Slug of the page (filename stem).")],
) -> str:
    """Get the full markdown content of a page. Raises if the page does not exist."""
    page_data = storage.get_page_by_slug(slug)
    if not page_data:
        raise ToolError(f"Page not found: {slug}")

    page_content = storage.load_page(page_data["file_path"])
    if not page_content:
        raise ToolError(f"Could not load page: {slug}")

    return page_content["content"]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_server_tools.py -v`
Expected: PASS (5 tests).

- [ ] **Step 5: Run the full suite**

Run: `uv run pytest -q`
Expected: all tests pass (models, state, resources, search, tools, prompts,
storage, search_index, mirror, converter, related).

- [ ] **Step 6: Commit**

```bash
git add src/alliance_docs_mcp/server.py tests/test_server_tools.py
git commit -m "feat: structured output, annotations, ToolError for remaining tools

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 8: Add fastmcp.json and simplify deployment

**Files:**
- Create: `fastmcp.json`
- Modify: `docker-entrypoint.sh` (the `fastmcp run` invocation + export `DOCS_DIR`)
- Keep: `server_entrypoint.py` (unchanged — `fastmcp.json` points at it)

**Interfaces:**
- Produces: a portable `fastmcp run fastmcp.json` entry point.

- [ ] **Step 1: Create fastmcp.json**

Create `fastmcp.json`:
```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  "source": {
    "path": "server_entrypoint.py",
    "entrypoint": "mcp"
  },
  "deployment": {
    "transport": "http",
    "host": "0.0.0.0",
    "port": 8080,
    "path": "/mcp/"
  }
}
```

Rationale: `DOCS_DIR`, `MEDIAWIKI_API_URL`, and `USER_AGENT` are read directly
from the process environment by `build_state()` / the mirror, so they are NOT
duplicated in `deployment.env` (which would risk literal `${VAR}` placeholders
if unset). The container sets them as real env vars.

- [ ] **Step 2: Validate the config loads**

Run: `uv run fastmcp inspect fastmcp.json`
Expected: FastMCP loads the server and prints its components (tools, resources,
prompts) without error. (If `inspect` is not available, run
`uv run python -c "import server_entrypoint; print(server_entrypoint.mcp.name)"`
which should print `Alliance Docs`.)

- [ ] **Step 3: Simplify docker-entrypoint.sh**

In `docker-entrypoint.sh`, ensure `DOCS_DIR` is exported (so the server process
inherits it). Change the line:
```bash
DOCS_DIR="${DOCS_DIR:-/data/docs}"
```
to:
```bash
export DOCS_DIR="${DOCS_DIR:-/data/docs}"
```

Replace the server launch block:
```bash
fastmcp run server_entrypoint.py:mcp \
  --transport http \
  --host 0.0.0.0 \
  --port "${PORT}" \
  --path /mcp/ \
  -- \
  --docs-dir "${DOCS_DIR}" &
```
with:
```bash
fastmcp run fastmcp.json --port "${PORT}" &
```

(`--port` overrides the static `8080` in `fastmcp.json` from the `PORT` env var;
host/path/transport come from the config. The removed `-- --docs-dir` args were
a no-op because `fastmcp run ...:mcp` never invokes `main()`'s argparse.)

- [ ] **Step 4: Verify the shell script parses**

Run: `bash -n docker-entrypoint.sh`
Expected: no output (syntax OK).

- [ ] **Step 5: Commit**

```bash
git add fastmcp.json docker-entrypoint.sh
git commit -m "chore: add fastmcp.json and simplify docker entrypoint

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 9: Update documentation

**Files:**
- Modify: `README.md` (Features + a new "MCP interface" / behavior-change note)

**Interfaces:** none (docs only).

- [ ] **Step 1: Update README**

In `README.md`, make these edits:

(a) Under **Features**, change the MCP Resources bullet to reflect lazy serving:
```markdown
- **MCP Resources**: Page content served lazily via a resource template
  (`alliance-docs://page/{slug}`), plus an `alliance-docs://pages` discovery index
```

(b) Add a new subsection (after the Features list) documenting v3 behavior:
```markdown
## MCP interface notes

- **Structured output**: tools return typed results (`SearchHit`, `PageSummary`,
  `PageInfo`, `RelatedPage`) with JSON output schemas.
- **Errors**: tools raise `ToolError` on genuine failures (e.g. requesting a page
  by slug that does not exist, or a search backend error). A successful search
  with no matches returns an empty list, not an error.
- **Resources**: individual pages are no longer pre-registered. Read a page at
  `alliance-docs://page/{slug}`; enumerate available pages via the
  `alliance-docs://pages` index resource or the `list_all_pages` tool.
- **Configuration**: set `DOCS_DIR` (and optional `MEDIAWIKI_API_URL`,
  `USER_AGENT`) via environment variables. The server is run with
  `fastmcp run fastmcp.json`.
```

(c) If the README references `fastmcp run server_entrypoint.py:mcp ... --docs-dir`,
replace those invocations with `fastmcp run fastmcp.json`.

- [ ] **Step 2: Sanity-check the docs build/links**

Run: `grep -n "docs-dir\|server_entrypoint.py:mcp" README.md`
Expected: no stale references to the removed `--docs-dir` flag remain (or only
inside clearly historical/changelog context).

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: document v3 MCP interface changes

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Final verification

- [ ] Run the full suite once more: `uv run pytest -q` → all pass.
- [ ] Confirm `uv run fastmcp inspect fastmcp.json` lists 8 tools, 5 prompts, and the 2 resources (`alliance-docs://page/{slug}` template + `alliance-docs://pages`).
- [ ] Confirm `import fastmcp; fastmcp.__version__` is `3.x`.
