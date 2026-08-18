# BuildBetter Plugin Packages

This directory contains platform-specific plugin packages for BuildBetter.

## Codex

The BuildBetter Skills workflow plugin lives at `plugins/skills/`.

The BuildBetter MCP and CLI plugin lives at `plugins/buildbetter-codex/` and is listed in `.agents/plugins/marketplace.json`. It includes BuildBetter-specific skills for MCP tool routing and reliable customer-voice retrieval.

Install from the hosted marketplace:

```bash
codex plugin marketplace add buildbetter-app/skills --ref main --sparse .agents/plugins --sparse plugins/skills --sparse plugins/buildbetter-codex
codex plugin add skills@buildbetter
codex plugin add buildbetter@buildbetter
```

Install locally from this checkout:

```bash
codex plugin marketplace add /path/to/skills
codex plugin add skills@buildbetter
codex plugin add buildbetter@buildbetter
```

## Claude Code

The Claude Code BuildBetter MCP and CLI plugin lives at `plugins/buildbetter-claude/` and is listed in `.claude-plugin/marketplace.json`. It includes BuildBetter-specific skills for MCP tool routing and reliable customer-voice retrieval.

Install from the hosted marketplace:

```bash
claude plugin marketplace add buildbetter-app/skills --sparse .claude-plugin plugins/buildbetter-claude
claude plugin install buildbetter@buildbetter
```

Install locally from this checkout:

```bash
claude plugin marketplace add /path/to/skills
claude plugin install buildbetter@buildbetter
```

## Why Separate Variants

Codex and Claude Code use different plugin manifest directories and different remote MCP configuration schemas. Keeping separate packages prevents one platform's validation and runtime expectations from breaking the other while preserving the same user-facing plugin name.
