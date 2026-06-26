import pytest

import alliance_docs_mcp.server as server
from alliance_docs_mcp.models import PageInfo, PageSummary
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


@pytest.mark.asyncio
async def test_list_categories_returns_general(stub):
    categories = await server.list_categories()
    assert categories == ["General"]


@pytest.mark.asyncio
async def test_list_recent_updates_returns_page_summaries(stub):
    updates = await server.list_recent_updates()
    assert len(updates) > 0
    assert isinstance(updates[0], PageSummary)
    assert updates[0].slug == "alpha"


@pytest.mark.asyncio
async def test_get_page_info_returns_page_info(stub):
    info = await server.get_page_info("alpha")
    assert isinstance(info, PageInfo)
    assert info.slug == "alpha"
    assert info.page_id == 1
    assert info.metadata == {"k": "v"}
