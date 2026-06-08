---
name: buildbetter
description: Use when working with BuildBetter's MCP server, bb CLI, Claude Code hooks, product-signal context, or preparing the BuildBetter Claude plugin for marketplace submission.
---

# BuildBetter

Use this skill when the user asks Claude Code to use BuildBetter product context, verify the local `bb` CLI, install BuildBetter hooks, or prepare/share the BuildBetter plugin.

## MCP

The plugin bundles the production BuildBetter MCP server:

```text
https://mcp.buildbetter.app
```

The MCP server uses OAuth and requires a BuildBetter account with an organization. If the server shows as unauthenticated, ask the user to run `/mcp` and complete the OAuth flow.

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
${CLAUDE_PLUGIN_ROOT}/scripts/install-bb-cli.sh /path/to/buildbetter-app
```

The repo-local source lives at `packages/apps/cli-go`. The install helper runs the package build and installs `dist/bb` to `~/.local/bin/bb`.

## Hooks

To install BuildBetter end-of-turn hooks for a repo:

```bash
bb hooks install --agent claude
bb hooks doctor --agent claude
```

Use `bb hooks repair --agent claude` when the hook exists but doctor reports drift. Use `bb hooks uninstall --agent claude` only when the user wants the BuildBetter-managed hook removed.

## Feedback

To send agent feedback to BuildBetter:

```bash
bb feedback --agent --provider claude --message "Feedback text"
```

Use `--dry-run --json` before sending when the user wants to inspect the payload.

## Plugin Distribution

Claude Code install flow:

```bash
claude plugin marketplace add buildbetter-app/skills --sparse .claude-plugin plugins/buildbetter-claude
claude plugin install buildbetter@buildbetter
```

Public Claude plugin directory submission requires a public GitHub repo or zip upload, `claude plugin validate`, and the in-app submission form. If the submission is only for the MCP server rather than the plugin wrapper, use the Connectors Directory remote MCP submission flow instead.
