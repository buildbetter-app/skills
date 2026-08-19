# BuildBetter for Codex

This Codex plugin bundles BuildBetter MCP configuration, local `bb` CLI guidance, and focused product-operations skills.

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
codex plugin marketplace add buildbetter-app/skills --ref main --sparse .agents/plugins --sparse plugins/skills --sparse plugins/buildbetter-codex
codex plugin add buildbetter@buildbetter
```

After installation, start a new Codex thread so the skill and MCP server are loaded.
