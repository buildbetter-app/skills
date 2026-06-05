# BuildBetter Codex Plugin Submission Overview

This dossier prepares the BuildBetter Codex plugin package for review against the Codex plugin quality bar: useful product capabilities, skill guidance, realistic evals, and a clear reviewer path.

## Plugin Links

- Plugin repository: https://github.com/buildbetter-app/BB-Skills
- Plugin homepage: https://github.com/buildbetter-app/BB-Skills/tree/main/plugins/buildbetter-codex
- Public product homepage: https://buildbetter.ai/
- Privacy policy: https://docs.buildbetter.ai/pages/Legal/privacy-policy
- Terms of service: https://docs.buildbetter.ai/pages/Legal/terms-of-service

## Packages In This Repo

| Package | Purpose | Submission role |
| --- | --- | --- |
| `plugins/buildbetter-codex` | Codex plugin for BuildBetter MCP and `bb` CLI workflows. | Primary Codex plugin submission candidate. |
| `plugins/bb-skills` | Codex plugin for BB-Skills spec workflow and browser verification. | Supporting workflow plugin and optional companion listing. |
| `plugins/buildbetter-claude` | Claude Code plugin variant with Claude-specific manifest and MCP shape. | Not part of Codex submission; maintained separately for Claude distribution. |

## Directory Submission Fields

Plugin name: BuildBetter

Plugin description: Connect Codex to BuildBetter product-ops context, customer signals, call evidence, documents, knowledge pages, and local `bb` CLI workflows so engineering agents can ground product work in customer evidence and repository feedback loops.

Example use cases:

- Find customer signals and call evidence for a planned feature.
- Search calls, transcripts, documents, people, and knowledge pages for product context.
- Draft a product spec or implementation plan with cited BuildBetter evidence.
- Check local `bb` CLI health, install BuildBetter Codex hooks, and inspect feedback payloads before sending.
- Prepare a repository for BuildBetter-assisted agent workflows.

## Install Paths

Hosted Git-backed marketplace:

```bash
codex plugin marketplace add buildbetter-app/BB-Skills --ref main --sparse .agents/plugins --sparse plugins/bb-skills --sparse plugins/buildbetter-codex
codex plugin add buildbetter@buildbetter
```

Local checkout:

```bash
codex plugin marketplace add /path/to/BB-Skills
codex plugin add buildbetter@buildbetter
```

## Submission Status

Done locally:

- Codex plugin manifest, metadata, logo, composer icon, screenshots, skills, and remote MCP config.
- Repo marketplace entry for Git-backed distribution.
- Hero use cases and eval cases in this dossier.
- Review account requirements and manual testing flow.
- MCP tool audit based on the BuildBetter app source.

External prerequisites before public review:

- Confirm the BuildBetter MCP app/connector approval state with OpenAI.
- Provide reviewer credentials through a private channel, not in this repository.
- Run and capture at least one successful Codex transcript against the review tenant.

