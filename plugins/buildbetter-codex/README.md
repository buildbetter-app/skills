# BuildBetter for Codex

This Codex plugin bundles BuildBetter MCP configuration, reliable multi-source research guidance, and local `bb` CLI workflows.

Bundled skills:

- `buildbetter`: connect MCP, operate the CLI, and manage hooks.
- `buildbetter-mcp-research`: route open-ended research through domain tools and return traceable evidence.

Install from the BuildBetter Skills marketplace:

```bash
codex plugin marketplace add buildbetter-app/skills --ref main --sparse .agents/plugins --sparse plugins/skills --sparse plugins/buildbetter-codex
codex plugin add buildbetter@buildbetter
```

After installation, start a new Codex thread so the skill and MCP server are loaded.
