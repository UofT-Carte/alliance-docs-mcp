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


def test_page_resource_missing_file_raises(tmp_path, monkeypatch):
    missing_path = tmp_path / "never_created.md"
    pages = [
        {
            "slug": "ghost",
            "title": "Ghost Page",
            "url": "https://example.com/ghost",
            "category": "General",
            "file_path": str(missing_path),
        }
    ]
    monkeypatch.setattr(server, "storage", DummyStorage(pages))
    monkeypatch.setattr(server, "docs_path", tmp_path)
    with pytest.raises(ResourceError):
        server.page_resource("ghost")


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
