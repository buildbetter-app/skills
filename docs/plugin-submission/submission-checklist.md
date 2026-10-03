# Submission Checklist

## Local Package

- [x] Codex plugin manifest exists at `plugins/buildbetter-codex/.codex-plugin/plugin.json`.
- [x] Codex MCP config exists at `plugins/buildbetter-codex/.mcp.json`.
- [x] Skills are bundled under `plugins/buildbetter-codex/skills/`.
- [x] Marketplace entry exists at `.agents/plugins/marketplace.json`.
- [x] Logo, composer icon, and screenshots are present.
- [x] Hosted and local install commands are documented.
- [x] Companion BuildBetter Skills Codex plugin is listed and included in sparse checkout commands.

## Review Dossier

- [x] Plugin links, name, description, and use cases are documented.
- [x] Hero prompts are documented.
- [x] Eval cases are structured in JSON.
- [x] Review account requirements are documented.
- [ ] Audit analytics, evidence UI/selection, and Events on the final backend and deployed revision; the older research inventory is documented.
- [x] Install smoke test is documented.

## Current Submission Candidate

- [x] Package 0.6.0 uses Productivity and three focused starter prompts.
- [x] Maintained public skills cover support, feedback, surveys, recordings, analytics, interactive evidence, and user-selected monitoring.
- [x] The reproducible ZIP excludes app references, lifecycle hooks, private organization skills, and credentials.
- [x] The manifest contains eight authored positive cases and three authored negative cases. These are scenarios, not execution receipts.
- [x] [The release candidate ledger](2026-10-01-release-candidate.md) names the backend stack and proof boundaries.

## External Submission Gates

- [ ] Sign in with the developer identity that owns the existing BuildBetter plugin; select the verified organization/project and existing listing.
- [ ] Obtain separate authorization to merge and deploy the backend stack, complete applicable gates, and read back the deployed endpoint revision. Audit every additions surface in [tool-audit.md](tool-audit.md), including `get-job`, `show-job-progress` and the optional progress component.
- [ ] Provide a dedicated sample-data reviewer account privately. It must work without MFA approvals, one-time codes, magic links, or private-network access.
- [ ] Grant Events to the review workspace only after the MCP and both workers are deployed with the migration.
- [ ] Execute all eight positive and three negative manifest cases in ChatGPT, including analytics, interactive evidence, and the operator-triggered future Events fixture. Save sanitized transcripts under `docs/plugin-submission/transcripts/`.
- [ ] Capture an accessible walkthrough URL and actual ChatGPT screenshots.
- [ ] Rebuild and inspect the final ZIP from the selected source revision; upload it and complete the MCP scan against the deployed endpoint.
- [ ] Resolve required metadata, skills, authentication, and MCP findings; complete applicable human attestations.
- [ ] Submit the new version of the existing plugin and record the version/draft identifier and submission receipt.
