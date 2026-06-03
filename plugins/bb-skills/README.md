# BB-Skills Codex Plugin

Codex plugin packaging for the BB-Skills workflow.

This plugin bundles the BuildBetter BB-Skills prompts as Codex-local skills and adds Playwright MCP wiring for the browser-testing pack.

## Included skills

- `bb-specify`
- `bb-plan`
- `bb-review`
- `bb-tasks`
- `bb-clarify`
- `bb-analyze`
- `bb-checklist`
- `bb-constitution`
- `bb-implement`
- `app-navigator`
- `trust-but-verify`
- `generate-tests`
- `bb-skills-update`

## Packaging notes

- Skills are flattened under `./skills/` for straightforward Codex plugin discovery.
- Shared templates are bundled under `./templates/`.
- The testing pack uses `./.mcp.json` to register the Playwright MCP server via `npx @playwright/mcp@latest`.
- The Codex-adapted testing skills write app maps and playbooks to `docs/verification/app-navigator/`.
- The Codex-adapted testing skills store local auth memory in `~/.codex/memories/<project-slug>/reference_local_auth.md`.
- `bb-skills-update` remains a CLI-oriented updater for users who also install the optional `bb-skills` Python package.
