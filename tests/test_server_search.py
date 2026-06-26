import tempfile
from pathlib import Path

import pytest

from alliance_docs_mcp.search_index import SearchIndex


class DummyStorage:
    def __init__(self):
        self.pages = [
            {
                "title": "Test Page",
                "url": "https://example.com/test",
                "category": "General",
                "slug": "test_page",
                "last_modified": "2025-01-01T00:00:00Z",
            }
        ]

    def search_pages(self, query, category=None):
        query_lower = query.lower()
        return [page for page in self.pages if query_lower in page["title"].lower()]

    def get_all_pages(self):
        return self.pages

    def get_page_by_slug(self, slug: str):
        for page in self.pages:
            if page.get("slug") == slug:
                return page
        return None


class DummyRelatedIndex:
    def __init__(self, results=None):
        self.results = results or []
        self.called = False

    def find_related(self, slug, limit=5, min_score=0.0):
        self.called = True
        return self.results


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
    assert results == related_result


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
    assert results[0]["slug"] == "test_page_2"

