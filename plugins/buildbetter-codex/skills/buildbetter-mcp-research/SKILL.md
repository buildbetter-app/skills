---
name: buildbetter-mcp-research
description: Research BuildBetter data accurately through BuildBetter MCP. Use for open-ended questions about customer evidence, signals, calls, transcripts, people, companies, documents, knowledge pages, Projects Hub, or triage, and whenever an agent must choose reliable BuildBetter MCP read tools and return traceable evidence.
---

# BuildBetter MCP Research

Use BuildBetter domain tools before GraphQL helpers. Use `run-query` only when discovery confirms that no domain tool expresses the request.

Read `references/mcp-tool-map.md` when exact tool names, arguments, pagination rules, or multi-source examples are needed.

This skill adds reusable routing and evidence discipline over the MCP's general-purpose read tools. It does not replace MCP behavior or encode a tenant's taxonomy. Feature-scoped and mutating workflows route to dedicated skills when those skills and their tools are available.

## Research Workflow

1. Translate the question into a retrieval plan: evidence source, organization-specific metadata, filters, time range, and the minimum detail needed to answer.
2. Discover before guessing. List configured signal types, tags, properties, project types, or GraphQL fields when the request depends on them.
3. Choose the narrowest domain tool. Use aggregate tools for totals or distributions, search/list tools for candidate discovery, and detail tools for exact evidence.
4. Start with a stable page of 20 to 40 results unless the user requests an export. Keep filters unchanged while paging.
5. Inspect returned IDs, dates, boundaries, people, companies, source kinds, types, and truncation metadata before synthesizing.
6. Deepen only the best candidates with call, transcript, document, knowledge-page, or project detail tools.
7. Answer with the scope searched, evidence identifiers, findings, and material coverage limitations. Never imply that unqueried sources were searched.

## Routing

- Calls and meetings: `search-calls` -> `get-call` -> `get-call-transcript`.
- Cross-call evidence: `search-signals` for fast discovery; `list-extractions` for exact filters.
- Counts, trends, and distributions: `aggregate-signals`, `aggregate-extractions`, or `aggregate-signals-by-tags` before listing every row.
- Direct customer evidence: use `buildbetter-customer-voice` when installed.
- Synthetic persona profiles, panels, studies, and chats: use `buildbetter-synthetic-research` when installed.
- Native survey authoring, delivery, intercepts, and responses: use `buildbetter-survey-research` when installed.
- Smart Tag drafting, evaluation, publishing, and backfills: use `buildbetter-smart-tags` when installed.
- People and accounts: `search-people`; use `search-people-properties` for CRM or integration attributes.
- Documents and knowledge: `search-documents` -> `get-document`; `search-knowledge-pages` or `list-knowledge-pages` -> `get-knowledge-page`.
- Exact folder contents: `get-folder`.
- Projects and triage: `list-project-types`, `list-projects`, `get-project`, `triage-count`, `list-triage-items`, `get-triage-item`. When the user asks for active work context, search promoted projects and triage separately.
- Project and Linear promotion workflows: use `buildbetter-project-triage` when installed.
- Knowledge-gap review, attachments, rechecks, and release readiness: use `buildbetter-knowledge-gaps` when installed.

## Reliability Rules

- If authentication or organization context fails, ask the user to connect BuildBetter MCP. Do not substitute guessed data.
- Prefer exact public IDs. Prefer email addresses over names when identifying a known person.
- Treat organization taxonomies as dynamic. Discover signal types, tags, and properties instead of assuming another account's names or meanings.
- Treat boundary labels as retrieval hints, not proof of customer identity. Verify returned people and companies before describing evidence as direct customer voice.
- Treat `phrase` as literal matching. Combine it with discovered structured types, tags, or `list-extractions` filters when exact scope matters. Do not use the OAuth-only `query` argument in this universal workflow.
- Use a continuation key only for the next page of the identical query. Drop it when any phrase, type, call, persona, tag, or filter changes.
- If a filter appears ineffective, compare returned IDs and verify with `list-extractions`; report the limitation rather than claiming the result was narrowed.
- Establish recurrence from signal, call, person, and company evidence. Do not rely on project or triage `customerCount` fields when attached evidence is sparse or contradictory.
- Distinguish an empty verified result from missing permissions, truncated coverage, unsupported filters, or a failed request.
- Treat an unavailable feature flag or disconnected integration as an unavailable surface, not an empty result.
- Keep this research workflow read-only. Do not call tools annotated as mutating; hand off to an explicit mutation workflow only after user approval.

## Output Contract

Return:

- Scope: sources, filters, dates, limits, pages, and organization metadata used.
- Findings: concise conclusions ordered by evidence strength.
- Evidence: stable signal, call, document, or project identifiers with dates and people/companies when available.
- Caveats: truncation, sparse coverage, ambiguous identity, internal-versus-external ambiguity, permission gaps, or filter anomalies.
