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
