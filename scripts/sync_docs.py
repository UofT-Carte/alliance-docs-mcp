#!/usr/bin/env python3
"""Synchronization script for mirroring Alliance documentation."""

import asyncio
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
)
from rich.panel import Panel
from rich.table import Table

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from alliance_docs_mcp.converter import WikiTextConverter
from alliance_docs_mcp.mirror import (
    MediaWikiClient,
    fetch_all_pages,
    fetch_page_contents,
    filter_to_target_language,
)
from alliance_docs_mcp.search_index import SearchIndex, SearchIndexUnavailable
from alliance_docs_mcp.storage import DocumentationStorage

# Initialize rich console
console = Console()

# Configure logging with Rich
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler('sync.log'),
        RichHandler(console=console, rich_tracebacks=True, show_time=False)
    ]
)
logger = logging.getLogger(__name__)

DEFAULT_API_URL = "https://docs.alliancecan.ca/mediawiki/api.php"


def _prepare_search_index(
    docs_dir: str, index_dir: Optional[str], enable_index: bool, rebuild_index: bool
) -> Optional[SearchIndex]:
    """Initialize (and optionally rebuild) the Whoosh search index."""
    if not enable_index:
        logger.info("Search indexing disabled (--no-index)")
        return None

    resolved_index_dir = Path(index_dir) if index_dir else Path(docs_dir) / "search_index"

    if rebuild_index and resolved_index_dir.exists():
        shutil.rmtree(resolved_index_dir)
        logger.info("Rebuilding search index at %s", resolved_index_dir)

    try:
        return SearchIndex(resolved_index_dir)
    except SearchIndexUnavailable as exc:
        logger.warning("Search index unavailable, continuing without it: %s", exc)
        return None


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

    for target in targets:
        if not target.exists():
            continue
        try:
            if target.is_dir():
                shutil.rmtree(target)
                logger.info("Removed directory for rebuild: %s", target)
            else:
                target.unlink()
                logger.info("Removed file for rebuild: %s", target)
        except Exception as exc:
            logger.warning("Failed to remove %s: %s", target, exc)


def _resolve_api_url() -> str:
    """Return a valid API URL, falling back to default if env is missing/invalid."""
    env_value = (os.getenv("MEDIAWIKI_API_URL") or "").strip()
    if env_value and env_value.startswith("http"):
        return env_value
    if env_value:
        logger.warning("MEDIAWIKI_API_URL is invalid; falling back to default.")
    return DEFAULT_API_URL


async def sync_documentation(
    enable_index: bool = True,
    rebuild_index: bool = False,
    index_dir: Optional[str] = None,
    rebuild_all: bool = False,
    strip_html: bool = True,
):
    """Main synchronization function."""
    # Load configuration from environment
    api_url = _resolve_api_url()
    docs_dir = os.getenv("DOCS_DIR", "./docs")
    user_agent = os.getenv("USER_AGENT", "AllianceDocsMCP/1.0")
    
    # Display header
    console.print(Panel.fit(
        "[bold cyan]Alliance Documentation Synchronization[/bold cyan]\n"
        f"API: {api_url}\n"
        f"Docs: {docs_dir}",
        border_style="cyan"
    ))

    # Initialize components
    if rebuild_all:
        _rebuild_all(docs_dir, index_dir)

    client = MediaWikiClient(api_url, user_agent)
    storage = DocumentationStorage(docs_dir)
    search_index = _prepare_search_index(docs_dir, index_dir, enable_index, rebuild_index)
    converter = WikiTextConverter()
    
    start_time = datetime.now()
    
    try:
        # Get all pages
        with console.status("[bold green]Fetching page list from MediaWiki...", spinner="dots") as status:
            all_pages = await fetch_all_pages(client)
            console.print(f"[green]✓[/green] Found [bold]{len(all_pages)}[/bold] pages")
        
        # Get page IDs for content fetching
        page_ids = [page["pageid"] for page in all_pages]
        
        # Fetch content for all pages with progress bar
        console.print("\n[bold cyan]Fetching page content...[/bold cyan]")
        pages_with_content = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            fetch_task = progress.add_task(
                "[cyan]Downloading pages...",
                total=len(page_ids)
            )
            
            # Process in batches
            batch_size = 10
            for i in range(0, len(page_ids), batch_size):
                batch = page_ids[i:i + batch_size]
                
                for page_id in batch:
                    try:
                        content = client.get_page_content(page_id)
                        if content:
                            pages_with_content.append(content)
                        await asyncio.sleep(0.1)
                    except Exception as e:
                        logger.error(f"Error fetching content for page {page_id}: {e}")
                    
                    progress.update(fetch_task, advance=1)
                
                # Longer delay between batches
                if i + batch_size < len(page_ids):
                    await asyncio.sleep(1)
        
        console.print(f"[green]✓[/green] Downloaded [bold]{len(pages_with_content)}[/bold] pages\n")
        
        # Process and save pages with progress bar
        console.print("[bold cyan]Processing and saving pages...[/bold cyan]")
        saved_pages = []
        errors = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            process_task = progress.add_task(
                "[cyan]Converting to Markdown...",
                total=len(pages_with_content)
            )
            
            for page_data in pages_with_content:
                try:
                    normalized_title = storage._strip_language_suffix(page_data.get("title", ""))

                    # Convert to markdown
                    markdown_content = converter.convert_to_markdown(
                        page_data["content"], 
                        page_data,
                        strip_html=strip_html,
                    )
                    
                    # Save the page
                    file_path = storage.save_page(page_data, markdown_content)
                    
                    # Add to saved pages list
                    saved_page = {
                        "page_id": page_data["pageid"],
                        "title": normalized_title,
                        "url": page_data["url"],
                        "category": storage._extract_category(normalized_title),
                        "last_modified": page_data["lastmodified"],
                        "file_path": file_path,
                        "slug": storage._title_to_filename(normalized_title)
                    }
                    saved_pages.append(saved_page)

                    # Index page content for full-text search
                    if search_index:
                        search_index.index_page(
                            slug=saved_page["slug"],
                            title=saved_page["title"],
                            content=markdown_content,
                            category=saved_page["category"],
                            url=saved_page["url"],
                            last_modified=saved_page["last_modified"],
                        )

                except Exception as e:
                    error_msg = f"{page_data.get('title', 'Unknown')}: {str(e)}"
                    errors.append(error_msg)
                    logger.error(f"Error processing page: {error_msg}")
                
                progress.update(process_task, advance=1)
        
        console.print(f"[green]✓[/green] Processed [bold]{len(saved_pages)}[/bold] pages\n")
        
        # Update index
        with console.status("[bold green]Updating index...", spinner="dots"):
            storage.update_index(saved_pages)
            console.print("[green]✓[/green] Index updated")
            if search_index:
                search_index.optimize()
        
        # Cleanup old files
        with console.status("[bold green]Cleaning up old files...", spinner="dots"):
            storage.cleanup_old_files()
            console.print("[green]✓[/green] Cleanup complete")
        
        # Build llms.txt files
        with console.status("[bold green]Building llms.txt files...", spinner="dots"):
            llms_txt_path = storage.build_llms_txt()
            console.print(f"[green]✓[/green] Created llms.txt at {llms_txt_path}")
            
            llms_full_path = storage.build_llms_full_txt(compress=True)
            console.print(f"[green]✓[/green] Created llms_full.txt.gz at {llms_full_path}")
        
        # Calculate statistics
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Create summary table
        summary = Table(title="\n[bold cyan]Synchronization Summary[/bold cyan]", show_header=False)
        summary.add_column("Metric", style="cyan")
        summary.add_column("Value", style="green")
        
        summary.add_row("Total Pages", str(len(all_pages)))
        summary.add_row("Downloaded", str(len(pages_with_content)))
        summary.add_row("Saved Successfully", str(len(saved_pages)))
        summary.add_row("Errors", str(len(errors)))
        summary.add_row("Duration", f"{duration:.1f}s")
        summary.add_row("Pages/Second", f"{len(saved_pages)/duration:.1f}")
        
        console.print(summary)
        
        if errors:
            console.print(f"\n[yellow]⚠ {len(errors)} errors occurred. Check sync.log for details.[/yellow]")
        
        return len(saved_pages)
        
    except Exception as e:
        console.print(f"\n[bold red]✗ Synchronization failed: {e}[/bold red]")
        logger.error(f"Synchronization failed: {e}")
        raise
    finally:
        client.close()


async def sync_incremental(
    enable_index: bool = True,
    rebuild_index: bool = False,
    index_dir: Optional[str] = None,
    rebuild_all: bool = False,
    strip_html: bool = True,
):
    """Incremental synchronization - only fetch changed pages."""
    # Load configuration
    api_url = _resolve_api_url()
    docs_dir = os.getenv("DOCS_DIR", "./docs")
    user_agent = os.getenv("USER_AGENT", "AllianceDocsMCP/1.0")
    
    logger.info("Starting incremental synchronization")

    # Initialize components
    if rebuild_all:
        _rebuild_all(docs_dir, index_dir)

    client = MediaWikiClient(api_url, user_agent)
    storage = DocumentationStorage(docs_dir)
    search_index = _prepare_search_index(docs_dir, index_dir, enable_index, rebuild_index)
    converter = WikiTextConverter()
    
    try:
        # Load existing index
        index = storage.load_index()
        last_update = index.get("last_updated")
        
        if last_update:
            logger.info(f"Last update: {last_update}")
            # Get recent changes since last update
            since_date = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
            recent_changes = client.get_recent_changes(since=since_date, limit=100)
            logger.info(f"Found {len(recent_changes)} recent changes")
        else:
            # First run - get all pages
            logger.info("First run - fetching all pages")
            all_pages = await fetch_all_pages(client)
            recent_changes = [
                {"pageid": page["pageid"], "title": page["title"]}
                for page in all_pages
            ]
        
        filtered_changes = filter_to_target_language(recent_changes)
        if len(filtered_changes) != len(recent_changes):
            logger.info("Filtered %d non-English recent changes", len(recent_changes) - len(filtered_changes))
        recent_changes = filtered_changes
        
        if not recent_changes:
            logger.info("No changes found")
            return 0
        
        # Fetch content for changed pages
        page_ids = [change["pageid"] for change in recent_changes]
        pages_with_content = await fetch_page_contents(client, page_ids)
        
        # Process and save pages
        saved_pages = []
        for page_data in pages_with_content:
            try:
                normalized_title = storage._strip_language_suffix(page_data.get("title", ""))

                # Convert to markdown
                markdown_content = converter.convert_to_markdown(
                    page_data["content"], 
                    page_data,
                    strip_html=strip_html,
                )
                
                # Save the page
                file_path = storage.save_page(page_data, markdown_content)
                
                # Add to saved pages list
                saved_page = {
                    "page_id": page_data["pageid"],
                    "title": page_data["title"],
                    "url": page_data["url"],
                    "category": storage._extract_category(page_data["title"]),
                    "last_modified": page_data["lastmodified"],
                    "file_path": file_path,
                    "slug": storage._title_to_filename(page_data["title"])
                }
                saved_pages.append(saved_page)

                if search_index:
                    search_index.index_page(
                        slug=saved_page["slug"],
                        title=saved_page["title"],
                        content=markdown_content,
                        category=saved_page["category"],
                        url=saved_page["url"],
                        last_modified=saved_page["last_modified"],
                    )

            except Exception as e:
                logger.error(f"Error processing page {page_data.get('title', 'Unknown')}: {e}")
                continue
        
        # Update index with new pages
        existing_pages = storage.get_all_pages()
        existing_by_id = {page["page_id"]: page for page in existing_pages}
        
        # Update existing pages and add new ones
        for saved_page in saved_pages:
            existing_by_id[saved_page["page_id"]] = saved_page
        
        # Update index
        storage.update_index(list(existing_by_id.values()))
        
        # Build llms.txt files
        logger.info("Building llms.txt files...")
        storage.build_llms_txt()
        storage.build_llms_full_txt(compress=True)
        
        logger.info(f"Incremental sync completed. Processed {len(saved_pages)} pages.")
        return len(saved_pages)
        
    except Exception as e:
        logger.error(f"Incremental synchronization failed: {e}")
        raise
    finally:
        client.close()


def main():
    """Main entry point."""
    import argparse
    
    strip_html_disabled_env = os.getenv("DISABLE_STRIP_HTML", "").lower() in ("1", "true", "yes")

    parser = argparse.ArgumentParser(description="Sync Alliance documentation")
    parser.add_argument("--incremental", action="store_true", 
                       help="Perform incremental sync (only changed pages)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    parser.add_argument(
        "--no-strip-html",
        action="store_true",
        help="Skip stripping HTML tags from converted markdown",
    )
    parser.add_argument(
        "--no-index",
        action="store_true",
        help="Skip building/updating the search index",
    )
    parser.add_argument(
        "--rebuild-index",
        action="store_true",
        help="Rebuild the search index before syncing",
    )
    parser.add_argument(
        "--rebuild-all",
        action="store_true",
        help="Remove docs, llms files, and all indexes before syncing",
    )
    parser.add_argument(
        "--index-dir",
        type=str,
        default=None,
        help="Optional path for the search index (defaults to DOCS_DIR/search_index)",
    )

    args = parser.parse_args()
    strip_html = not (strip_html_disabled_env or args.no_strip_html)
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        if args.incremental:
            result = asyncio.run(
                sync_incremental(
                    enable_index=not args.no_index,
                    rebuild_index=args.rebuild_index,
                    index_dir=args.index_dir,
                    rebuild_all=args.rebuild_all,
                    strip_html=strip_html,
                )
            )
        else:
            result = asyncio.run(
                sync_documentation(
                    enable_index=not args.no_index,
                    rebuild_index=args.rebuild_index,
                    index_dir=args.index_dir,
                    rebuild_all=args.rebuild_all,
                    strip_html=strip_html,
                )
            )
        
        print(f"Sync completed successfully. Processed {result} pages.")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
