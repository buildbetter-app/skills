# Submission Checklist

## Local Package

- [x] Codex plugin manifest exists at `plugins/buildbetter-codex/.codex-plugin/plugin.json`.
- [x] Codex MCP config exists at `plugins/buildbetter-codex/.mcp.json`.
- [x] Skills are bundled under `plugins/buildbetter-codex/skills/`.
- [x] Marketplace entry exists at `.agents/plugins/marketplace.json`.
- [x] Logo, composer icon, and screenshots are present.
- [x] Hosted and local install commands are documented.
- [x] Companion BB-Skills Codex plugin is listed and included in sparse checkout commands.

## Review Dossier

- [x] Plugin links, name, description, and use cases are documented.
- [x] Hero prompts are documented.
- [x] Eval cases are structured in JSON.
- [x] Review account requirements are documented.
- [x] Tool audit is documented from current BuildBetter MCP source.
- [x] Install smoke test is documented.

## External Submission Gates

- [ ] Confirm BuildBetter MCP app/connector approval state with OpenAI.
- [ ] Provide reviewer credentials privately.
- [ ] Run manual Codex evals against the review tenant.
- [ ] Capture successful transcripts under `docs/plugin-submission/transcripts/`.
- [ ] Add app/connector mapping if OpenAI requires a `.app.json` or connector ID for public directory submission.
- [ ] Merge companion BuildBetter app PR `https://github.com/buildbetter-app/buildbetter-app/pull/4171` and verify the full MCP integration spec in a fully seeded app checkout.
