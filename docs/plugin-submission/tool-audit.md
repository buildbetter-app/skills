# BuildBetter MCP Tool Audit

Source audited: `/Users/shooby/.codex/worktrees/5bd0/bbapp/packages/apps/mcp/src/mcp/handlers.ts` and `/Users/shooby/.codex/worktrees/5bd0/bbapp/docs/integrations/mcp-tooling-guide.md`.

## Summary

The plugin-facing BuildBetter MCP server currently exposes read-only product-context tools plus a read-only GraphQL fallback. The surface is focused around customer evidence retrieval: calls, transcripts, signals, documents, knowledge pages, people, and property metadata.

The server already has:

- clear domain tool names,
- Zod-validated inputs,
- stable numeric entity IDs in result objects,
- default and maximum result limits,
- pagination or continuation for signal search,
- an auth hint when OAuth tokens lack organization context,
- guidance to use domain tools before `run-query`.

Companion app-code change:

- Draft PR: `https://github.com/buildbetter-app/buildbetter-app/pull/4171`.
- Branch `chore/mcp-tool-annotations` in `buildbetter-app/buildbetter-app` wraps the MCP handler `Tool` decorator so every plugin-facing BuildBetter MCP tool emits `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, and `openWorldHint: true`. The wrapper uses `@rekog/mcp-nest`'s supported `annotations` field, which is passed through to MCP `tools/list`.
- Local verification passed for `pnpm -F @buildbetter-app/mcp build` and the focused `tools/list exposes Zod-derived JSON Schemas` integration test. The full MCP integration spec was attempted after repairing local generated artifacts; startup succeeded, but existing REST fixture assertions returned empty result sets in this local checkout.

## Tool Inventory

| Tool | Class | Side effect | Expected use | Stable IDs / response notes |
| --- | --- | --- | --- | --- |
| `search-calls` | Domain search | Read-only | Search calls/interviews by phrase and optional date window. | Returns call IDs, names, dates, and attendees. Limit is clamped. |
| `get-call` | Domain get | Read-only | Retrieve one call with attendees and recent related signals. | Uses numeric call ID; `signalLimit` is clamped. |
| `get-call-transcript` | Domain get | Read-only | Retrieve speaker-attributed transcript segments for one call. | Uses numeric call ID; returns a clear message when no transcript exists. |
| `search-signals` | Domain search | Read-only | Search signals/extractions by phrase, type, call, persona, page, or continuation key. | Returns signal IDs and `nextContinuationKey` when another page exists. |
| `search-extractions` | Compatibility alias | Read-only | Backward-compatible alias for `search-signals`. | Prefer `search-signals` for new workflows. |
| `list-extractions` | Structured list | Read-only | Advanced structured extraction filters/select/order. | Limit and page are bounded. |
| `list-extraction-filter-fields` | Metadata list | Read-only | Discover fields for structured extraction filters. | Bounded by `MAX_LIMIT`. |
| `list-signal-types` | Metadata list | Read-only | List configured signal taxonomy types. | Bounded list of type names/IDs. |
| `list-signal-properties` | Metadata list | Read-only | List extraction custom-property definitions. | Returns count/total/items. |
| `search-signal-property-values` | Domain search | Read-only | Search signal custom-property values by phrase, property, call, or signal. | Uses stable signal/call IDs when filtering. |
| `search-documents` | Domain search | Read-only | Search documents by phrase/status/source with optional content. | `includeContent` defaults false for token efficiency. |
| `get-document` | Domain get | Read-only | Retrieve one document by ID with content and metadata. | Uses numeric document ID. |
| `search-knowledge-pages` | Domain search | Read-only | Search internal knowledge pages by title or content. | Returns concise no-result message when empty. |
| `list-knowledge-pages` | Domain list | Read-only | List most recently updated knowledge pages. | Limit is clamped. |
| `get-knowledge-page` | Domain get | Read-only | Retrieve one knowledge page by ID with content and child pages. | Uses numeric knowledge page ID. |
| `search-people` | Domain search | Read-only | Search people by name/email/title/department and optional personas. | Returns people, company, and persona context. |
| `search-people-properties` | Domain search | Read-only | Search person CRM property values and definitions. | Returns property/value/source context. |
| `list-types` | Schema helper | Read-only | List GraphQL object types visible in auth context. | Schema cache is keyed by endpoint/auth fingerprint. |
| `find-fields` | Schema helper | Read-only | Inspect fields for a GraphQL type. | Use before custom queries when domain tools do not fit. |
| `build-query` | Schema helper | Read-only | Build a starter Hasura list query for a type/field set. | Validates requested fields before generating query text. |
| `run-query` | Advanced fallback | Read-only by description | Execute custom read-only GraphQL query after domain tools fail. | Should reject mutation attempts at the service layer; reviewers should confirm with evals. |

## Skill Guidance Coverage

The BuildBetter Codex skill tells Codex to:

- use BuildBetter MCP for product context,
- ask the user to complete OAuth before MCP-backed work,
- prefer installed `bb` CLI and inspect health before installing,
- use `--dry-run --json` before sending feedback when the user wants inspection,
- document marketplace and workspace-sharing flows.

Additional guidance encoded in this dossier:

- use domain tools before `run-query`,
- cite stable IDs when available,
- ask before write-like CLI actions such as hook repair or feedback submission,
- avoid BuildBetter for unrelated coding-only prompts.
