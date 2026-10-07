# BuildBetter ChatGPT and Codex Plugin Submission Overview

This dossier prepares the maintained BuildBetter package for ChatGPT and Codex review: useful product capabilities, portable public skills, realistic cases, and a clear reviewer path. The maintained install candidate is 0.6.1; the existing OpenAI draft uses an explicit 2.0.0 artifact version. [The update preparation](2026-10-05-update-preparation.md) separates shipped PRs and runtime proof from pending deployment and submission.

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

Subtitle: Research customer feedback

Plugin description: Research customer feedback across support tickets, survey responses, calls, interviews, recordings, product signals, and Knowledge in your connected BuildBetter workspace. Find recurring pain points, feature requests, onboarding friction, and renewal or churn concerns. Compare what customers say with connected PostHog or Amplitude events, usage trends, and saved insights. Get an evidence-backed answer with source citations, account context, a clear timeframe, and coverage limits. The agent searches, filters, selects representative evidence, and synthesizes in chat; manual evidence selection is optional. Draft follow-up surveys, refine Smart Tags and taxonomy, inspect project triage, and identify Knowledge gaps. Keep synthetic persona research separate from real customer evidence. Optional evidence browsing, progress cards, and supported signal, recording, or survey-response monitoring improve specific workflows when the client supports them. Coverage depends on your sources and permissions. OAuth connects your account. Sending, publishing, access changes, and credit-consuming actions keep their existing approval gates. Public skills provide portable workflows; private workspace skills are retrieved at runtime.

Example prompts (matching the maintained manifest):

- Find recurring customer pain points and feature requests across our support tickets, surveys, and calls.
- Compare onboarding friction with product usage and cite the evidence.
- Summarize customer feedback for prioritization, including counterevidence and affected accounts.

The maintained manifest is the source of truth for upload fields; synchronize this dossier when those fields change.

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

For the existing OpenAI draft, run `python3 scripts/build_plugin_submission.py --submission-version 2.0.0 --output artifacts/buildbetter-2.0.0-openai.zip`. The override changes both artifact manifests to 2.0.0 without changing the maintained 0.6.1 install source. Omitting it preserves the source version. The reproducible archive bundles the maintained public skills, normalizes the remote MCP configuration, and applies the requested artifact-version override. Do not upload the whole repository or include credentials, app references, or hooks.

Metadata and skills updates require a new version/ZIP. Runtime organization skills remain private and are retrieved using permissioned MCP tools; submission-time skill imports are static snapshots. Review cases in the manifest are authored scenarios, not execution receipts. Supply a dedicated sample-data reviewer account and a real walkthrough URL in the dashboard before submitting.
