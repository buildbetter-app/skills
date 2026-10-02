---
name: buildbetter
description: Use when working with BuildBetter's MCP server, bb CLI, Codex hooks, product-signal context, or preparing the BuildBetter Codex plugin for local sharing or submission.
---

# BuildBetter

For customer feedback, imported support conversations, surveys, analytics context, recordings, signals, and Knowledge, use `$buildbetter-start` to choose a focused workflow. Source coverage depends on connected data and permissions.

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

If `bb` is missing or stale, follow the CLI installation instructions in the BuildBetter documentation at https://docs.buildbetter.ai/. Local CLI setup applies only to coding environments that provide a terminal; never require it for ChatGPT evidence workflows.

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
codex plugin marketplace add buildbetter-app/skills --ref main --sparse .agents/plugins --sparse plugins/skills --sparse plugins/buildbetter-codex
codex plugin add buildbetter@buildbetter
```

Workspace sharing flow:

1. Open Plugins in the Codex app.
2. Open Created by you.
3. Open BuildBetter.
4. Select Share.
5. Add workspace members or copy the share link.

The public plugin directory serves ChatGPT and Codex. Maintainers can upload a validated plugin ZIP at https://platform.openai.com/plugins. Metadata and bundled-skill changes require a new package version; hosted MCP changes are scanned separately. Keep reviewer credentials out of public packages.
