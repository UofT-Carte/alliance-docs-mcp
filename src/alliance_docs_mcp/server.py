"""FastMCP server for Alliance documentation."""

import gzip
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, List, Optional

from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError, ToolError
from fastmcp.server.lifespan import lifespan
from mcp.types import ToolAnnotations
from pydantic import Field
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from .models import PageIndexEntry, PageInfo, PageSummary, RelatedPage, SearchHit
from .related import RelatedIndex, RelatedIndexUnavailable
from .search_index import SearchIndex, SearchIndexUnavailable
from .storage import DocumentationStorage

logger = logging.getLogger(__name__)


def _discover_docs_directory() -> Path:
    """Determine the directory that contains mirrored documentation files."""
    configured_docs_dir = os.getenv("DOCS_DIR")
    candidates = []

    if configured_docs_dir:
        configured_path = Path(configured_docs_dir)
        candidates.append(configured_path)

    module_path = Path(__file__).resolve()
    candidates.extend(
        [
            Path.cwd() / "docs",
            module_path.parent / "docs",
            module_path.parents[1] / "docs",
            module_path.parents[2] / "docs",
        ]
    )

    for candidate in candidates:
        if candidate and candidate.is_dir():
            return candidate.resolve()

    raise FileNotFoundError(
        "Documentation directory not found. Set DOCS_DIR environment variable to the docs path."
    )


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


def _resolve_page_path(file_path: str) -> Path:
    """Resolve a page path to an absolute location on disk."""
    path_obj = Path(file_path)

    if path_obj.is_absolute():
        return path_obj

    # Allow paths that already include the docs/ prefix
    if path_obj.parts and path_obj.parts[0] == "docs":
        path_obj = Path(*path_obj.parts[1:])

    candidate = docs_path / path_obj
    return candidate.resolve()


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
                    last_modified=(
                        hit["last_modified"].isoformat()
                        if hit.get("last_modified") is not None
                        else None
                    ),
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


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
async def list_categories() -> List[str]:
    """List all available documentation categories."""
    return storage.get_categories()


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


# MCP Prompts

@mcp.prompt(
    name="documentation_search_guide",
    description="Guide for effectively searching Alliance documentation",
    tags=["search", "documentation"]
)
def documentation_search_guide(query: str, category: Optional[str] = None) -> str:
    """Generate a prompt template for searching documentation.
    
    Args:
        query: The user's search query
        category: Optional category filter
    """
    prompt = f"""Search the Alliance documentation for information about: {query}

Use the search_docs tool to find relevant documentation pages. When searching:
- Use the query parameter: "{query}"
"""
    
    if category:
        prompt += f"- Filter results by category: {category}\n"
    else:
        prompt += "- Consider filtering by category if you get too many results\n"
    
    prompt += """- Review the search results, paying attention to:
  * Relevance scores (higher scores indicate better matches)
  * Highlighted snippets showing where the query matches
  * Categories to understand the context of each result

If you find relevant pages, use get_page_content to read the full content for detailed information.
If the search returns many results, consider using a category filter or refining the query."""
    
    return prompt


@mcp.prompt(
    name="technical_question_template",
    description="Template for answering technical questions using documentation",
    tags=["technical", "question", "documentation"]
)
def technical_question_template(question: str, context: Optional[str] = None) -> str:
    """Generate a prompt template for answering technical questions.
    
    Args:
        question: The technical question to answer
        context: Additional context about what the user is trying to accomplish
    """
    prompt = f"""Answer this technical question using the Alliance documentation: {question}
"""
    
    if context:
        prompt += f"\nContext: {context}\n"
    
    prompt += """
Follow these steps:
1. Use search_docs to find relevant documentation pages related to the question
2. Review the search results and identify the most relevant pages
3. Use get_page_content to read the full content of relevant pages
4. If you find a specific page that seems directly relevant, use find_related_pages to discover additional related documentation
5. Synthesize information from multiple sources to provide a comprehensive answer

Focus on:
- Practical steps and procedures from the documentation
- Specific configurations, commands, or code examples
- Any prerequisites or requirements mentioned
- Related topics that might be helpful"""
    
    return prompt


@mcp.prompt(
    name="category_exploration_guide",
    description="Guide for exploring documentation by category",
    tags=["category", "exploration", "documentation"]
)
def category_exploration_guide(category: str, purpose: Optional[str] = None) -> str:
    """Generate a prompt template for exploring documentation by category.
    
    Args:
        category: The category to explore
        purpose: What the user is trying to accomplish
    """
    prompt = f"""Explore the Alliance documentation in the "{category}" category.
"""
    
    if purpose:
        prompt += f"\nPurpose: {purpose}\n"
    
    prompt += f"""
Available categories include: Getting Started, Technical Reference, User Guide, and others.

To explore the {category} category:
1. Use list_categories to see all available categories (if needed)
2. Use search_docs with category="{category}" to find pages within this category
3. Review the results to understand what documentation is available
4. Use get_page_content to read specific pages of interest
5. Use find_related_pages to discover additional related content

Common categories:
- Getting Started: For new users learning the basics
- Technical Reference: Technical specifications and detailed information
- User Guide: Step-by-step guides and tutorials"""
    
    return prompt


@mcp.prompt(
    name="related_content_discovery",
    description="Guide for finding related documentation pages",
    tags=["related", "discovery", "documentation"]
)
def related_content_discovery(topic: str, goal: Optional[str] = None) -> str:
    """Generate a prompt template for finding related documentation.
    
    Args:
        topic: The topic or page slug to find related content for
        goal: The user's goal (learning, troubleshooting, etc.)
    """
    prompt = f"""Find documentation pages related to: {topic}
"""
    
    if goal:
        prompt += f"\nGoal: {goal}\n"
    
    prompt += """
To discover related content:
1. First, use search_docs or get_page_by_title to find the main page about this topic
2. Once you have the page slug, use find_related_pages to discover related documentation
3. Review the similarity scores:
   - Higher scores (closer to 1.0) indicate more closely related content
   - Scores above 0.7 typically indicate highly relevant related pages
4. Use get_page_content to read the related pages for additional context
5. You can also combine related pages with additional searches to build a comprehensive understanding

Related pages are useful when:
- You want to explore a topic in depth
- You're learning about a subject and want to see related concepts
- You're troubleshooting and need to understand related systems or procedures"""
    
    return prompt


@mcp.prompt(
    name="getting_started_helper",
    description="Template for helping new users get started",
    tags=["getting-started", "onboarding", "documentation"]
)
def getting_started_helper(use_case: str) -> str:
    """Generate a prompt template for helping new users get started.
    
    Args:
        use_case: What the user wants to do (e.g., "set up account", "run first job", "install software")
    """
    prompt = f"""Help a new user get started with: {use_case}

The Alliance documentation includes a "Getting Started" category with guides for new users.

Follow these steps:
1. Use list_categories to confirm available categories
2. Search in the "Getting Started" category using: search_docs(query="{use_case}", category="Getting Started")
3. Also check list_recent_updates to see if there are recent updates to getting started documentation
4. Review the results and use get_page_content to read relevant getting started guides
5. Use find_related_pages to discover additional helpful documentation

Common getting started topics include:
- Setting up an account and authentication
- Connecting to systems via SSH
- Running your first job
- Installing software
- Understanding the file system structure
- Learning about available systems and resources

Provide clear, step-by-step guidance based on the documentation found."""
    
    return prompt


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    """Simple health endpoint for platform probes."""
    return PlainTextResponse("ok")


@mcp.custom_route("/", methods=["GET"])
async def root(request: Request) -> PlainTextResponse:
    """Return a basic status message for root requests."""
    return PlainTextResponse("Alliance Docs MCP server is running. Try /health for probe status.")


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
