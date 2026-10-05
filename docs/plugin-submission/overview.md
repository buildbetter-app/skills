# BuildBetter ChatGPT and Codex Plugin Submission Overview

This dossier prepares the maintained BuildBetter package for ChatGPT and Codex review: useful product capabilities, portable public skills, realistic cases, and a clear reviewer path. The current candidate is 0.6.1; [its update preparation](2026-10-05-update-preparation.md) separates shipped PRs and runtime proof from pending deployment and submission.

## Plugin Links

- Plugin repository: https://github.com/buildbetter-app/skills
- Plugin homepage: https://github.com/buildbetter-app/skills/tree/main/plugins/buildbetter-codex
- Public product homepage: https://buildbetter.ai/
- Privacy policy: https://docs.buildbetter.ai/pages/Legal/privacy-policy
- Terms of service: https://docs.buildbetter.ai/pages/Legal/terms-of-service

## Packages In This Repo

| Package | Purpose | Submission role |
| --- | --- | --- |
| `plugins/buildbetter-codex` | Shared ChatGPT/Codex package for BuildBetter MCP and portable workflows; local CLI guidance also works in Codex. | Primary public ZIP submission source. |
| `plugins/skills` | Codex plugin for BuildBetter Skills spec workflow and browser verification. | Supporting workflow plugin and optional companion listing. |
| `plugins/buildbetter-claude` | Claude Code plugin variant with Claude-specific manifest and MCP shape. | Not part of Codex submission; maintained separately for Claude distribution. |

## Directory Submission Fields

Plugin name: BuildBetter

Plugin description: Research customer feedback, imported support conversations, survey responses, recordings, product signals, analytics, and Knowledge with cited evidence and focused workflows. Inspect selected signals interactively and monitor updates the user chooses when the client and workspace support Events. The directory package serves ChatGPT and Codex; local CLI setup remains available in Codex.

Example use cases:

- Find recurring pain points across imported support, survey, feedback, and recording evidence.
- Compare qualitative evidence with connected PostHog or Amplitude usage and saved insights.
- Complete evidence research in chat; optionally inspect cited signals in the evidence browser when requested.
- Monitor selected new signals, completed recordings, or submitted survey responses in an Events-capable client.
- Search recordings, transcripts, documents, people, and Knowledge for product context.
- Draft a product spec or implementation plan with cited BuildBetter evidence.
- Check local `bb` CLI health, install BuildBetter Codex hooks, and inspect feedback payloads before sending.
- Prepare a repository for BuildBetter-assisted agent workflows.

## Install Paths

Hosted Git-backed marketplace:

```bash
codex plugin marketplace add buildbetter-app/skills --ref main --sparse .agents/plugins --sparse plugins/skills --sparse plugins/buildbetter-codex
codex plugin add buildbetter@buildbetter
```

Local checkout:

```bash
codex plugin marketplace add /path/to/skills
codex plugin add buildbetter@buildbetter
```

## Submission Status

Done locally:

- Codex plugin manifest, metadata, logo, composer icon, screenshots, skills, and remote MCP config.
- Repo marketplace entry for Git-backed distribution.
- Hero use cases and eval cases in this dossier.
- Review account requirements and manual testing flow.
- MCP tool audit based on the BuildBetter app source.

External prerequisites before public review include the owning publisher identity, a deployed verified backend, dedicated sample reviewer credentials, executed ChatGPT cases, an accessible walkthrough, completed scan findings, and a submission receipt. See the [checklist](submission-checklist.md).

## Public ZIP

Run `python scripts/build_plugin_submission.py --output artifacts/buildbetter-0.6.1.zip`. The reproducible archive bundles the maintained public skills and normalizes only its MCP configuration. Do not upload the whole repository or include credentials, app references, or hooks.

Metadata and skills updates require a new version/ZIP. Runtime organization skills remain private and are retrieved using permissioned MCP tools; submission-time skill imports are static snapshots. Review cases in the manifest are authored scenarios, not execution receipts. Supply a dedicated sample-data reviewer account and a real walkthrough URL in the dashboard before submitting.
