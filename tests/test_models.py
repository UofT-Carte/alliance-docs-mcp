import pytest
from pydantic import ValidationError

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


def test_page_index_entry_missing_slug_raises():
    with pytest.raises(ValidationError):
        PageIndexEntry()
