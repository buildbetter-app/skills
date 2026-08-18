# BuildBetter for Codex

This Codex plugin bundles BuildBetter MCP configuration, MCP research/customer-voice retrieval guidance, and local `bb` CLI guidance.

Install from the BuildBetter Skills marketplace:

```bash
codex plugin marketplace add buildbetter-app/skills --ref main --sparse .agents/plugins --sparse plugins/skills --sparse plugins/buildbetter-codex
codex plugin add buildbetter@buildbetter
```

After installation, start a new Codex thread so the skill and MCP server are loaded.
