FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app

# Copy dependency manifests and README first for better caching
COPY pyproject.toml uv.lock README.md ./

# Create project virtual environment
ENV UV_PROJECT_ENVIRONMENT=.venv
RUN uv sync --frozen --no-dev

# Ensure the environment is on PATH for runtime commands
ENV PATH="/app/.venv/bin:${PATH}"

# Copy the remainder of the application source
COPY . .

# Seed the documentation cache from the repo's committed, weekly-refreshed docs.
# No live MediaWiki sync at build time: that re-downloaded the whole corpus on
# every build and made deploys hostage to an external, rate-limited API. The
# entrypoint primes DOCS_DIR from this seed on boot, then runs ONE incremental
# sync (bounded, in the background) to catch changes since the last weekly sync.
ENV DOCS_SEED_DIR=/app/docs

# Set defaults for runtime configuration
ENV DOCS_DIR=/data/docs
ENV MEDIAWIKI_API_URL=https://docs.alliancecan.ca/mediawiki/api.php
ENV USER_AGENT=AllianceDocsMCP/1.0
ENV PYTHONUNBUFFERED=1

# Create volume mount point for documentation cache
VOLUME ["/data"]

# Make the entrypoint executable (just in case git permissions are lost)
RUN chmod +x docker-entrypoint.sh

EXPOSE 8080

CMD ["/app/docker-entrypoint.sh"]
