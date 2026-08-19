# BuildBetter for Claude Code

This Claude Code plugin bundles BuildBetter MCP configuration, local `bb` CLI guidance, and focused product-operations skills.

Bundled skills:

- `buildbetter`: connect MCP, operate the CLI, and manage hooks.
- `buildbetter-mcp-research`: route open-ended research through domain tools and return traceable evidence.
- `buildbetter-customer-voice`: retrieve defensible direct customer evidence while separating internal commentary.
- `buildbetter-synthetic-research`: run bounded synthetic persona studies with credit confirmation.
- `buildbetter-survey-research`: draft, launch, and analyze native surveys with audience safeguards.
- `buildbetter-smart-tags`: draft, evaluate, publish, and backfill Smart Tags with approval gates.
- `buildbetter-project-triage`: inspect Projects Hub and explicitly promote triage or Linear work.
- `buildbetter-knowledge-gaps`: review documentation gaps and release knowledge readiness.

The mutating workflows use explicit approval, credit, audience, idempotency, and verification gates. Each skill stops when its required tool is not registered instead of approximating a missing mutation.

Install from the BuildBetter Skills marketplace:

```bash
claude plugin marketplace add buildbetter-app/skills --sparse .claude-plugin plugins/buildbetter-claude
claude plugin install buildbetter@buildbetter
```

After installation, run `/reload-plugins` or start a new Claude Code session. The plugin installs disabled by default because it connects to an authenticated external service; enable it from the plugin UI when you want BuildBetter tools active.

If the MCP server shows as unauthenticated, run `/mcp` in Claude Code and complete the OAuth flow.
