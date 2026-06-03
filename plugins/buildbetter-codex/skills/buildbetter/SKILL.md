---
name: buildbetter
description: Use when working with BuildBetter's MCP server, bb CLI, Codex hooks, product-signal context, or preparing the BuildBetter Codex plugin for local sharing or submission.
---

# BuildBetter

Use this skill when the user asks Codex to use BuildBetter product context, verify the local `bb` CLI, install BuildBetter Codex hooks, or prepare/share the BuildBetter plugin.

## MCP

The plugin bundles the production BuildBetter MCP server:

```text
https://mcp.buildbetter.app
```

The MCP server uses OAuth and requires a BuildBetter account with an organization. If MCP authentication is not complete, ask the user to connect the BuildBetter MCP server from the Codex plugin/auth flow before attempting MCP-backed work.

For staging-only testing, use the BuildBetter app repo docs at `docs/instructions/mcp-setup.md` and the staging server URL:

```text
https://mcp-staging.buildbetter.app
```

## bb CLI

Prefer the installed `bb` binary when it exists:

```bash
command -v bb
bb --version
bb auth status
bb doctor
```

If `bb` is missing or stale, install it from a local BuildBetter app checkout:

```bash
${PLUGIN_ROOT}/scripts/install-bb-cli.sh /path/to/buildbetter-app
```

The repo-local source lives at `packages/apps/cli-go`. The install helper runs the package build and installs `dist/bb` to `~/.local/bin/bb`.

## Hooks

To install BuildBetter end-of-turn hooks for a repo:

```bash
bb hooks install --agent codex
bb hooks doctor --agent codex
```

Use `bb hooks repair --agent codex` when the hook exists but doctor reports drift. Use `bb hooks uninstall --agent codex` only when the user wants the BuildBetter-managed hook removed.

## Feedback

To send agent feedback to BuildBetter:

```bash
bb feedback --agent --provider codex --message "Feedback text"
```

Use `--dry-run --json` before sending when the user wants to inspect the payload.

## Plugin Distribution

Codex install flow:

```bash
codex plugin marketplace add buildbetter-app/BB-Skills --ref main --sparse .agents/plugins --sparse plugins/buildbetter-codex
codex plugin add buildbetter@buildbetter
```

Workspace sharing flow:

1. Open Plugins in the Codex app.
2. Open Created by you.
3. Open BuildBetter.
4. Select Share.
5. Add workspace members or copy the share link.

Official public Codex Plugin Directory publishing is not yet self-serve. Until public publishing opens, use workspace sharing for teammates or distribute through this Git-backed marketplace entry.
