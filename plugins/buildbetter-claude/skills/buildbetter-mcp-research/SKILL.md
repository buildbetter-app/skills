---
name: buildbetter-mcp-research
description: Query BuildBetter accurately through its MCP tools. Use when a user asks open-ended questions about BuildBetter data, customer signals, calls, transcripts, people, documents, knowledge pages, Projects Hub, triage, Linear tickets, organization skillsets, or when choosing the right BuildBetter MCP tool for a research/product-ops answer.
---

# BuildBetter MCP Research

## Core Rule

Use BuildBetter domain tools first. Use GraphQL helpers and `run-query` only when the domain tools cannot express the request.

Read `references/mcp-tool-map.md` when you need exact tool names, arguments, or common workflow examples.

## Routing

- Call or meeting lookup: `search-calls` -> `get-call` -> `get-call-transcript`.
- Cross-call signal analysis: `search-signals`; use `list-extractions` for precise structured filters.
- Direct customer voice: use `buildbetter-customer-voice` when available.
- Documents and docs-backed context: `search-documents` -> `get-document`; `search-knowledge-pages` or `list-knowledge-pages` -> `get-knowledge-page`.
- Folder or collection contents: `get-folder` when the user provides an exact folder ID.
- People or accounts: `search-people`; use `search-people-properties` for CRM/person property values.
- Projects Hub and triage: `list-project-types`, `list-projects`, `get-project`, `triage-count`, `list-triage-items`, `get-triage-item`.
- Linear ticket triage: discover filter IDs with Linear list tools, then use `list-linear-tickets` and `get-linear-ticket`.
- Organization-managed skills: `list-skillsets`, `list-skills`, `get-skill`; use `propose-skill-update` only after explicit user approval.

## Research Workflow

1. Convert the user question into a retrieval plan: source type, likely filters, and the evidence needed to answer.
2. Discover metadata before guessing names or IDs. Use list/discovery tools for signal types, signal properties, extraction filter fields, project types, Linear teams/projects/states, and GraphQL schema fields.
3. Retrieve a small, stable first page. Prefer limits between 20 and 40 unless the user asks for a broad export.
4. Inspect returned IDs, dates, people, companies, types, and source fields before synthesizing.
5. Deepen with detail tools only for the best candidates: `get-call`, transcript, document, knowledge page, project, or ticket detail.
6. Answer with the scope searched, evidence IDs, and caveats. Do not imply BuildBetter searched data sources you did not query.

## Reliability

- If authentication or organization context fails, ask the user to complete BuildBetter MCP OAuth instead of attempting fallback guesses.
- Use exact IDs when available. Use email addresses for people when possible.
- Do not reuse a `search-signals` continuation key after changing phrase, type, call, persona, or page intent.
- Treat `search-signals.query` as natural-language filter generation for OAuth users. Treat `phrase` as literal text matching.
- If a phrase appears ignored, verify with `list-extractions` or report the anomaly instead of pretending the phrase narrowed results.
- Mutating tools require explicit user approval: `promote-triage-item`, `promote-linear-tickets`, and `propose-skill-update`.
