# BuildBetter MCP Tool Audit

Source audited: `packages/apps/mcp/src/mcp/handlers.ts` and `packages/apps/mcp/src/__tests__/mcp.integration.spec.ts` on the BuildBetter MCP `main` branch.

## Summary

The plugin-facing BuildBetter MCP server exposes organization-scoped product-context tools plus a read-only GraphQL fallback. The universal read surface covers calls, transcripts, signals, documents, knowledge pages, people, property metadata, projects, and triage. Connected integrations, feature-gated tools, and mutating workflows are outside the portable research skills.

The server already has:

- clear domain tool names,
- Zod-validated inputs,
- stable numeric entity IDs in result objects,
- default and maximum result limits,
- page or continuation traversal for signal search,
- stable continuation traversal for default-order structured extraction lists,
- explicit aggregate tools for totals and grouped counts,
- an auth hint when OAuth tokens lack organization context,
- guidance to use domain tools before `run-query`.

## Tool Inventory

| Tool | Class | Side effect | Expected use | Stable IDs / response notes |
| --- | --- | --- | --- | --- |
| `search-calls` | Domain search | Read-only | Search calls/interviews by phrase and optional date window. | Returns call IDs, names, dates, and attendees. Limit is clamped. |
| `get-call` | Domain get | Read-only | Retrieve one call with attendees and recent related signals. | Uses numeric call ID; `signalLimit` is clamped. |
| `get-call-transcript` | Domain get | Read-only | Retrieve speaker-attributed transcript segments for one call. | Uses numeric call ID; returns a clear message when no transcript exists. |
| `search-signals` | Domain search | Read-only | Search signals/extractions by natural-language `query` or structured phrase, type, call, persona, page, or continuation key. | Returns signal IDs and `nextContinuationKey` when another page exists. Send the continuation key alone for later pages. |
| `search-extractions` | Compatibility alias | Read-only | Backward-compatible alias for `search-signals`. | Prefer `search-signals` for new workflows. |
| `get-list-extractions-schema` | Schema helper | Read-only | Return the current structured input contract for `list-extractions`. | Use before constructing strict filters; this is the registered MCP tool name. |
| `list-extractions` | Structured list | Read-only | Advanced structured extraction filters/select/order. | Numbered `page` remains available. With default ordering, omit `page` for stable keyset traversal and send only the returned `nextContinuationKey` as `continuationKey` on later requests. |
| `aggregate-extractions` | Structured aggregate | Read-only | Count matching extractions and optionally group by tag, topic, keyword, or type. | Use for totals and grouped counts instead of paginating rows. |
| `aggregate-signals` | Structured aggregate | Read-only | Return signal, call, person, and company totals plus common distributions for a structured filter. | `topLimit` bounds top people and companies. |
| `aggregate-signals-by-tags` | Tag aggregate | Read-only | Roll up exact smart-tag metrics and optional time buckets. | `buckets` are explicit named filter windows. |
| `list-extraction-tags` | Metadata list | Read-only | Discover the organization's reusable extraction tags. | Returns public UUIDs accepted by structured tag filters. |
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
