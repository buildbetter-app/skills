# Install Smoke Test

Run this before submitting or after any plugin packaging change.

## Hosted Marketplace

```bash
codex plugin marketplace add buildbetter-app/skills --ref main --sparse .agents/plugins --sparse plugins/skills --sparse plugins/buildbetter-codex
codex plugin marketplace upgrade buildbetter
codex plugin add buildbetter@buildbetter
codex plugin add skills@buildbetter
```

Expected:

- Marketplace source `buildbetter` is listed.
- `BuildBetter` and `BuildBetter Skills` appear in the plugin directory.
- `plugins/buildbetter-codex/.mcp.json` loads with `mcp_servers.buildbetter`.
- `plugins/skills/.mcp.json` loads with `mcp_servers.playwright`.
- A new Codex thread can invoke `@BuildBetter`.
- OAuth prompts for BuildBetter MCP auth and requires organization selection.
- BuildBetter Skills prompts are available after install.

## Local Checkout

```bash
codex plugin marketplace add /path/to/skills
codex plugin add buildbetter@buildbetter
codex plugin add skills@buildbetter
```

Expected:

- Same plugin discovery behavior as hosted install.
- Asset paths in both plugin manifests resolve locally.
- No marketplace entry points to a sparse path missing from the install command.

## Failure Handling

- If BuildBetter MCP auth fails, reconnect through the plugin/auth flow and choose an organization.
- If Playwright tools are missing, confirm `@playwright/mcp@0.0.75` is reachable from the environment.
- If only one plugin appears from the hosted marketplace, re-run the marketplace add command with all three sparse paths.
