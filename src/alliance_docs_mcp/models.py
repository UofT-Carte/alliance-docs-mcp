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
