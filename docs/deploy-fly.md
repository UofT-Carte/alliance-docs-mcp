# Deploying to Fly.io

The server runs as a **single, always-on, stateless** machine on Fly.io.
Configuration lives in [`fly.toml`](../fly.toml). This replaces the previous
Prefect Horizon (FastMCP Cloud) deployment.

## Why this shape

- **Stateless (no volume):** the docs seed is baked into the image and the
  Whoosh search index is rebuilt on boot in a few seconds, so there is nothing
  to persist. This keeps deploys zero-downtime and avoids pinning the app to a
  single machine/region.
- **Always-on (`auto_stop_machines = "off"`, `min_machines_running = 1`):** no
  scale-to-zero, so there are no cold starts and the in-container background
  documentation-sync loop always has CPU.
- **512 MB `shared-cpu-1x`:** runtime footprint is ~150–250 MB; the extra
  headroom covers the boot-time index build. ≈ $3.50/mo.

## One-time setup

These commands need your Fly account and run a remote image build, so run them
yourself (in this session you can prefix a line with `!` to run it inline).

```bash
# 1. Install flyctl if needed:  https://fly.io/docs/flyctl/install/
# 2. Authenticate (interactive):
fly auth login

# 3. Create the app (name must match `app` in fly.toml):
fly apps create alliance-docs-mcp

# 4. Deploy (builds the Dockerfile remotely; this takes a few minutes):
fly deploy
```

No secrets are required for the default configuration — `MEDIAWIKI_API_URL`
and `USER_AGENT` are non-secret and set in `fly.toml [env]`. If you later add
authentication or any real secret, set it with `fly secrets set NAME=value`
(secrets override `[env]` and are not baked into the image).

## Verify

```bash
fly status                                   # machine should be "started"
curl https://alliance-docs-mcp.fly.dev/health   # -> ok
fly logs                                      # watch boot: prime seed, build index, sync loop
```

The MCP endpoint is then:

```
https://alliance-docs-mcp.fly.dev/mcp/
```

Point MCP clients (Claude Code, Cursor, etc.) at that URL. Health checks /
load balancers should target `/health`, not the MCP path.

## Keeping content fresh

There is **no periodic sync inside the running container** — it syncs only at
boot. The live corpus stays current through deploys:

1. **`weekly-sync.yml`** (cron, Sundays 06:00 UTC) runs an incremental
   MediaWiki sync and commits the refreshed `docs/` to `main`.
2. That triggers **`deploy.yml`**, which runs `fly deploy` — rebuilding the
   image with a freshly-baked seed and shipping it.
3. On boot, the entrypoint runs one more incremental sync, catching anything
   changed since the image was built.

So the live corpus refreshes **weekly, automatically** (plus on any other push
to `main` — a merge, a manual `manual-rebuild-all` run, or code changes). For
an out-of-band refresh, trigger `Weekly Docs Sync` manually (it commits and
auto-deploys) or run `fly deploy` yourself.

> Note: the weekly-sync commit is pushed with the default `GITHUB_TOKEN`, which
> by design does not trigger `push` workflows. `deploy.yml` therefore also
> triggers on the **completion** of the `Weekly Docs Sync` workflow, so the
> weekly refresh still ships.

## Operations

```bash
fly logs                      # tail logs
fly status                    # machine state
fly releases                  # deploy history
fly releases rollback         # roll back to the previous release
fly ssh console               # shell into the machine (debugging)
```

## MCP-over-HTTP notes

The MCP Streamable HTTP transport uses long-lived/SSE connections. Fly's proxy
passes streaming responses through without buffering and does not impose a
short request timeout, so no extra configuration is needed. After the first
deploy, confirm a real MCP client can connect and stream a tool response.

The endpoint is currently **unauthenticated** (same as before). If this server
should not be public, add auth (e.g. a FastMCP auth provider or a bearer token
checked in middleware) before sharing the URL — that's a separate change from
this migration.

## Activating continuous deploy

`.github/workflows/deploy.yml` runs `fly deploy` on push to `main`, on
completion of `Weekly Docs Sync`, and on manual dispatch — this is what keeps
the live docs fresh (see "Keeping content fresh" above). It needs one secret to
work:

```bash
fly tokens create deploy        # prints a deploy token
```

Add the printed value as a repo secret named **`FLY_API_TOKEN`**
(Settings → Secrets and variables → Actions). Until that secret and the Fly app
exist, the deploy workflow will fail harmlessly; create the app (one-time setup
above) and the secret as part of cutover.
