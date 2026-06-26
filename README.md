# Alliance Documentation MCP Server

A Model Context Protocol (MCP) server that provides programmatic access to the Digital Research Alliance of Canada's technical documentation. This server mirrors the documentation from the MediaWiki site and exposes it through MCP resources and tools for use with MCP-compatible clients.

## Features

- **Documentation Mirroring**: Syncs documentation from the Alliance MediaWiki site
- **MCP Resources**: Page content served lazily via a resource template
  (`alliance-docs://page/{slug}`), plus an `alliance-docs://pages` discovery index
- **Full-Text Search**: Whoosh-backed content and title search with highlights and scoring
- **Related Pages**: Whoosh content-similarity ("more like this") related-page discovery with heuristic fallback
- **Search & Query Tools**: Provides search, categorization, and querying capabilities
- **Startup Refresh**: Container entrypoint triggers an incremental sync on boot; schedule additional runs as needed
- **Markdown Storage**: Stores documentation as markdown files with metadata

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

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) for package management

### Installation

1. **Clone and setup the repository:**
   ```bash
   git clone <repository-url>
   cd alliance-docs-mcp
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure environment (optional):**
   Create a `.env` file (or export the variables directly) if you want to override defaults. For example:
   ```env
   MEDIAWIKI_API_URL=https://docs.alliancecan.ca/mediawiki/api.php
   DOCS_DIR=./docs
   USER_AGENT=AllianceDocsMCP/1.0
   ```

4. **Initial documentation sync:**
   ```bash
   uv run python scripts/sync_docs.py
   ```
   _Note: Docker images built from this repository automatically run this full sync during the image build so containers start with a warm cache._

5. **Start the MCP server:**
   ```bash
   uv run python -m alliance_docs_mcp.server
   ```

## Usage

### MCP Resources

The server exposes documentation pages as MCP resources:

- **Resource URI**: `alliance-docs://page/{slug}`
- **Content**: Markdown content of the documentation page

Example:
```
alliance-docs://page/technical_documentation
```

### MCP Tools

The server provides several tools for querying documentation:

#### `search_docs(query: str, category: Optional[str] = None, limit: int = 20, search_content: bool = True, fuzzy: bool = False)`
Search documentation pages by title (fallback) or full-text index when available. Full-text results include relevance scores and highlighted snippets.

**Parameters:**
- `query`: Search query string
- `category`: Optional category filter
- `limit`: Maximum number of results
- `search_content`: Use full-text index when available (default: True)
- `fuzzy`: Enable fuzzy matching for typo tolerance (full-text only)

**Returns:** List of matching pages with metadata, highlights, and scores (when indexed)

#### `list_categories()`
List all available documentation categories.

**Returns:** List of category names

#### `get_page_by_title(title: str)`
Find a specific page by its title.

**Parameters:**
- `title`: Page title to search for

**Returns:** Page metadata or None if not found

#### `list_recent_updates(limit: int = 10)`
List recently updated pages.

**Parameters:**
- `limit`: Maximum number of pages to return

**Returns:** List of recent pages with metadata

#### `get_page_info(slug: str)`
Get detailed information about a specific page.

**Parameters:**
- `slug`: Page slug

**Returns:** Detailed page information including metadata

#### `list_all_pages()`
List all available documentation pages.

**Returns:** List of all pages with basic metadata

#### `find_related_pages(slug: str, limit: int = 5)`
Finds related pages via Whoosh content similarity ("more like this"), with automatic fallback to a lightweight title/category heuristic.

**Parameters:**
- `slug`: Source page slug
- `limit`: Max related pages to return

**Returns:** List of related pages with relevance scores (or heuristic scores when falling back)

### MCP Prompts

The server provides reusable prompt templates that guide LLMs on how to effectively query and use the documentation system. These prompts can be used by MCP clients to structure queries and improve consistency.

#### `documentation_search_guide(query: str, category: Optional[str] = None)`
Guide for effectively searching Alliance documentation. Provides instructions on using the `search_docs` tool, interpreting search results, and filtering by category.

**Parameters:**
- `query`: The user's search query
- `category`: Optional category filter

**Use Case**: When an LLM needs to help a user search for documentation on a specific topic.

#### `technical_question_template(question: str, context: Optional[str] = None)`
Template for answering technical questions using documentation. Guides the LLM through searching, reading relevant pages, finding related content, and synthesizing information.

**Parameters:**
- `question`: The technical question to answer
- `context`: Additional context about what the user is trying to accomplish

**Use Case**: When an LLM needs to answer technical questions based on the documentation.

#### `category_exploration_guide(category: str, purpose: Optional[str] = None)`
Guide for exploring documentation by category. Helps discover pages within a specific category and understand the documentation structure.

**Parameters:**
- `category`: The category to explore
- `purpose`: What the user is trying to accomplish

**Use Case**: When an LLM needs to help users explore documentation in a specific category (e.g., "Getting Started", "Technical Reference").

#### `related_content_discovery(topic: str, goal: Optional[str] = None)`
Guide for finding related documentation pages. Provides instructions on using the `find_related_pages` tool and interpreting similarity scores.

**Parameters:**
- `topic`: The topic or page slug to find related content for
- `goal`: The user's goal (learning, troubleshooting, etc.)

**Use Case**: When an LLM needs to help users discover related documentation after finding a relevant page.

#### `getting_started_helper(use_case: str)`
Template for helping new users get started. Guides LLMs to point users to getting started documentation and common first steps.

**Parameters:**
- `use_case`: What the user wants to do (e.g., "set up account", "run first job", "install software")

**Use Case**: When an LLM needs to help new users with onboarding and initial setup tasks.

### Synchronization

#### Manual Sync

Run a full synchronization (with rich progress bars and visual feedback):
```bash
uv run python scripts/sync_docs.py
```

Run an incremental sync (only changed pages):
```bash
uv run python scripts/sync_docs.py --incremental
```

Index controls:
```bash
uv run python scripts/sync_docs.py --rebuild-index       # Rebuild Whoosh index
uv run python scripts/sync_docs.py --no-index            # Skip indexing
uv run python scripts/sync_docs.py --index-dir /tmp/idx  # Custom index location
```

The `weekly-sync` GitHub Action runs an incremental sync on a schedule and commits the updated `docs/` to `main`; on the Fly.io deployment that change auto-deploys (see [docs/deploy-fly.md](docs/deploy-fly.md)), so the hosted server mirrors the latest content. You can also run a sync command above locally and commit `docs/` for an out-of-band refresh.

The sync script provides:
- **Colored output** with rich formatting
- **Progress bars** for download and processing phases
- **Real-time statistics** including pages/second
- **Summary table** with detailed metrics
- **Error tracking** with warnings for failed pages

> **Note:** Markdown pages larger than 10 MB are stored as `.md.gz` files. The server automatically decompresses them at runtime, so no additional configuration is required.

#### LLM-Optimized Documentation Files

The sync process automatically generates two files for LLM consumption:

- **`docs/llms.txt`**: A simple directory listing all page names, categories, and URLs (~35 KB)
- **`docs/llms_full.txt.gz`**: Complete documentation content in a single compressed file (~2.6 MB compressed, ~393 MB uncompressed)

These files are regenerated on every sync (both full and incremental) and committed to the repository, making it easy for LLMs to access the entire documentation corpus.

#### Automated Sync

Set up a cron job for weekly updates:
```bash
# Add to crontab (runs every Sunday at 2 AM)
0 2 * * 0 cd /path/to/alliance-docs-mcp && uv run python scripts/sync_docs.py --incremental
```

This repository also ships with `.github/workflows/weekly-sync.yml`, which performs the same incremental sync on Sundays using GitHub Actions and pushes any changes back to `main`.

## Configuration

### Environment Variables

Set the following environment variables (via `.env`, shell exports, or your hosting platform's secret manager) to customize behavior:

- `MEDIAWIKI_API_URL` (default `https://docs.alliancecan.ca/mediawiki/api.php`)
- `DOCS_DIR` (default `./docs`, or `/data/docs` in the container)
- `USER_AGENT` (default `AllianceDocsMCP/1.0`)
- `SEARCH_INDEX_DIR` (optional; overrides default `DOCS_DIR/search_index`)
- `DISABLE_SEARCH_INDEX` (set to `1/true/yes` to force title-only fallback)

### Server Configuration

Run the server locally over stdio (the default MCP transport):

```bash
uv run python -m alliance_docs_mcp.server [--verbose]
```

`--verbose` is the only accepted flag. All runtime configuration is done via environment variables — see the [Environment Variables](#environment-variables) section above for the full list. The most commonly needed ones are `DOCS_DIR`, `MEDIAWIKI_API_URL`, and `USER_AGENT`.

### Docker Deployment

The provided Docker image ships with a pre-synced documentation cache baked into `/app/docs_seed`. When the container starts, the entrypoint primes the configured `DOCS_DIR` from this seed (if empty) and then launches the MediaWiki sync in the background so the MCP server begins accepting connections immediately. You can configure startup behavior with:

- `RUN_SYNC_ON_START=0` to skip the background sync (useful when running in read-only environments)
- `SYNC_MODE=full` to force a full resync instead of the default incremental sync
- The container starts the server via `fastmcp run fastmcp.json --port 8080`; transport, host, and path are read from `fastmcp.json` rather than passed as CLI flags. Additional FastMCP CLI flags can be injected by overriding `CMD` in your own image if needed.
- A lightweight `/health` endpoint is exposed for platform probes; point load balancer checks there instead of MCP protocol paths.

## Project Structure

```
alliance-docs-mcp/
├── src/
│   └── alliance_docs_mcp/
│       ├── __init__.py
│       ├── server.py        # FastMCP server implementation
│       ├── mirror.py        # MediaWiki API client
│       ├── converter.py     # WikiText to Markdown converter
│       └── storage.py       # File storage and retrieval
├── docs/                    # Mirrored markdown files
│   ├── pages/               # Organized by category
│   └── index.json           # Page metadata index
├── scripts/
│   └── sync_docs.py         # Synchronization script
├── tests/                   # Test files
├── pyproject.toml           # Project configuration
└── README.md
```

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black src/
uv run ruff check src/
```

### Deployment Options

**Fly.io (recommended)**
- Runs as a single always-on, stateless machine. Configuration is in [`fly.toml`](fly.toml); the full runbook (one-time setup, cutover, operations) is in [docs/deploy-fly.md](docs/deploy-fly.md).
- `.github/workflows/deploy.yml` ships `main` to Fly on push and on completion of the weekly docs sync, so the live corpus refreshes weekly. Requires a `FLY_API_TOKEN` repo secret.

**Self-managed container/VM**
- Build the Docker image in this repo and run it anywhere that can expose HTTP on port `8080`.
- Provide the same environment variables via your scheduler or container runtime.
- Point load balancer health checks at `/health` and connect MCP clients to the `/mcp/` path served by `fastmcp run`.

### Adding New Features

1. **New MCP Tools**: Add new tool functions to `server.py`
2. **Storage Enhancements**: Extend `storage.py` for new functionality
3. **API Improvements**: Modify `mirror.py` for different API interactions

## Troubleshooting

### Common Issues

1. **Sync Failures**: Check API access and network connectivity
2. **Missing Pages**: Verify MediaWiki API responses
3. **Conversion Errors**: Ensure `beautifulsoup4`/`wikitextparser` are installed and valid HTML is being stripped (use `--no-strip-html` to disable)

### Logs

Check the `sync.log` file for synchronization issues:
```bash
tail -f sync.log
```

### Debug Mode

Run with verbose logging:
```bash
uv run python scripts/sync_docs.py --verbose
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Digital Research Alliance of Canada](https://alliancecan.ca/) for providing the documentation
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP server framework
- [uv](https://github.com/astral-sh/uv) for Python package management
