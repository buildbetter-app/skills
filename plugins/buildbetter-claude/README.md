# BuildBetter for Claude Code

This Claude Code plugin bundles BuildBetter MCP configuration, reliable multi-source research guidance, and local `bb` CLI workflows.

Bundled skills:

- `buildbetter`: connect MCP, operate the CLI, and manage hooks.
- `buildbetter-mcp-research`: route open-ended research through domain tools and return traceable evidence.

Install from the BuildBetter Skills marketplace:

```bash
claude plugin marketplace add buildbetter-app/skills --sparse .claude-plugin plugins/buildbetter-claude
claude plugin install buildbetter@buildbetter
```

After installation, run `/reload-plugins` or start a new Claude Code session. The plugin installs disabled by default because it connects to an authenticated external service; enable it from the plugin UI when you want BuildBetter tools active.

If the MCP server shows as unauthenticated, run `/mcp` in Claude Code and complete the OAuth flow.
