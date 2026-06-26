"""Full-text search index using Whoosh."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from whoosh import index
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import DATETIME, ID, KEYWORD, TEXT, Schema
from whoosh.qparser import FuzzyTermPlugin, MultifieldParser, OrGroup
from whoosh.query import Term

logger = logging.getLogger(__name__)


class SearchIndexUnavailable(Exception):
    """Raised when the search index cannot be used."""


class SearchIndex:
    """Lightweight Whoosh-based full-text search."""

    def __init__(self, index_dir: Path, enabled: bool = True) -> None:
        """
        Args:
            index_dir: Directory where the Whoosh index lives.
            enabled: If False, the index is not created or used.
        """
        self.enabled = enabled
        self.index_dir = Path(index_dir)
        self.schema = self._build_schema()
        self._index = self._create_or_open_index() if enabled else None

    def _build_schema(self) -> Schema:
        return Schema(
            slug=ID(stored=True, unique=True),
            title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            content=TEXT(stored=True, analyzer=StemmingAnalyzer()),
            category=KEYWORD(stored=True, lowercase=True, commas=True, scorable=True),
            url=ID(stored=True),
            last_modified=DATETIME(stored=True),
        )

    def _create_or_open_index(self):
        self.index_dir.mkdir(parents=True, exist_ok=True)
        try:
            if index.exists_in(self.index_dir):
                return index.open_dir(self.index_dir)
            return index.create_in(self.index_dir, self.schema)
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Unable to initialize search index: %s", exc)
            raise SearchIndexUnavailable(str(exc))

    def _normalize_datetime(self, value) -> Optional[datetime]:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return None
        return None

    def index_page(
        self,
        slug: str,
        title: str,
        content: str,
        category: str,
        url: str,
        last_modified,
    ) -> None:
        """Add or update a page in the index."""
        if not self.enabled or not self._index:
            return

        normalized_dt = self._normalize_datetime(last_modified)

        try:
            writer = self._index.writer()
            writer.update_document(
                slug=slug,
                title=title or slug,
                content=content or "",
                category=category or "General",
                url=url or "",
                last_modified=normalized_dt,
            )
            writer.commit()
        except Exception as exc:
            logger.warning("Failed to index page %s: %s", slug, exc)

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 20,
        fuzzy: bool = False,
    ) -> List[Dict]:
        """Search the index with relevance ranking and highlights."""
        if not self.enabled or not self._index:
            raise SearchIndexUnavailable("Search index disabled or unavailable")

        try:
            with self._index.searcher() as searcher:
                parser = MultifieldParser(
                    ["title", "content"],
                    schema=self._index.schema,
                    group=OrGroup.factory(0.9),
                )
                if fuzzy:
                    parser.add_plugin(FuzzyTermPlugin())

                parsed_query = parser.parse(query)
                category_filter = Term("category", category.lower()) if category else None

                results = searcher.search(parsed_query, limit=limit, filter=category_filter)
                return [
                    {
                        "title": hit.get("title"),
                        "slug": hit.get("slug"),
                        "url": hit.get("url"),
                        "category": hit.get("category"),
                        "score": hit.score,
                        "highlights": hit.highlights("content", top=3),
                        "last_modified": hit.get("last_modified"),
                    }
                    for hit in results
                ]
        except SearchIndexUnavailable:
            raise
        except Exception as exc:
            logger.warning("Search failed: %s", exc)
            raise SearchIndexUnavailable(str(exc))

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

    def is_empty(self) -> bool:
        """Check if the index is empty (has no documents)."""
        if not self.enabled or not self._index:
            return True
        try:
            with self._index.searcher() as searcher:
                return searcher.doc_count() == 0
        except Exception as exc:
            logger.debug("Error checking if index is empty: %s", exc)
            return True

    def populate_from_storage(self, storage) -> int:
        """Populate the index from existing documentation storage.
        
        Args:
            storage: DocumentationStorage instance to load pages from
            
        Returns:
            Number of pages indexed
        """
        if not self.enabled or not self._index:
            return 0
        
        pages = storage.get_all_pages()
        indexed_count = 0
        
        logger.info(f"Populating search index from {len(pages)} pages...")
        
        for page in pages:
            try:
                file_path = page.get("file_path")
                if not file_path:
                    continue
                
                # Load page content
                page_data = storage.load_page(file_path)
                if not page_data:
                    logger.debug(f"Skipping page {page.get('slug')}: could not load content")
                    continue
                
                content = page_data.get("content", "")
                # Remove frontmatter from content for indexing
                # (frontmatter is already in metadata)
                if content.startswith("---\n"):
                    lines = content.split('\n')
                    end_marker = None
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip() == "---":
                            end_marker = i
                            break
                    if end_marker is not None:
                        content = '\n'.join(lines[end_marker + 1:])
                
                # Index the page
                self.index_page(
                    slug=page.get("slug", ""),
                    title=page.get("title", ""),
                    content=content,
                    category=page.get("category", "General"),
                    url=page.get("url", ""),
                    last_modified=page.get("last_modified"),
                )
                indexed_count += 1
                
            except Exception as exc:
                logger.warning(f"Failed to index page {page.get('slug', 'unknown')}: {exc}")
                continue
        
        # Optimize the index after bulk population
        if indexed_count > 0:
            try:
                self.optimize()
            except Exception as exc:
                logger.debug(f"Index optimization failed after population: {exc}")
        
        logger.info(f"Populated search index with {indexed_count} pages")
        return indexed_count

    def optimize(self) -> None:
        """Optimize the index storage."""
        if not self.enabled or not self._index:
            return
        try:
            self._index.optimize()
        except Exception as exc:
            logger.debug("Index optimize failed: %s", exc)


__all__ = ["SearchIndex", "SearchIndexUnavailable"]




