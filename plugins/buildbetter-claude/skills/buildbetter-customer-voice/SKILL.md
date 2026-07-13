---
name: buildbetter-customer-voice
description: Retrieve defensible customer-voice evidence from BuildBetter MCP. Use when researching customer complaints, objections, praise, feature requests, needs, themes, exact quotes, account feedback, or changes over time, especially when direct external statements must be separated from internal commentary and supported with traceable signal or call evidence.
---

# BuildBetter Customer Voice

Use BuildBetter as an evidence layer. Separate direct customer statements from internal interpretations, and preserve enough scope and identifiers for another researcher to reproduce the result.

This skill composes the general-purpose read tools shipped on the current MCP surface. It does not replace MCP behavior, encode a tenant's taxonomy, or depend on feature-gated domains and mutation workflows.

Use `buildbetter-mcp-research` instead when the request primarily concerns internal documents, Projects Hub, or triage rather than customer evidence.

## Evidence Standard

Rank evidence in this order:

1. Transcript text from an identified external speaker.
2. A signal's `exactQuote` with an external person boundary and unambiguous speaker attribution.
3. A signal summary, clearly labeled as a paraphrase.
4. Internal commentary, clearly separated as context rather than customer voice.

Never turn a summary into a quotation. If identity, boundary, or speaker attribution is missing, mark the evidence unverified and do not silently count it as direct customer voice.

## Workflow

1. Define the population, product area, source set, time window, and whether the user wants direct external evidence, internal interpretation, or both. For a relative window, default to a rolling UTC interval with an exclusive end and state the exact timestamps.
2. Discover the organization's current taxonomy. Start with `get-list-extractions-schema` and `list-signal-types`; search `list-extraction-tags` with a targeted term and bounded limit. Use `list-signal-properties` plus `search-signal-property-values` only when a custom dimension matters. Use `list-extraction-filter-fields` only when source metadata is needed. Do not assume names or meanings from another organization.
3. Establish coverage with `aggregate-signals`, `aggregate-extractions`, or `aggregate-signals-by-tags`. Prefer unique calls, people, and companies over raw signal counts when discussing prevalence, and treat grouped type counts as overlapping when a signal can have multiple types.
4. Retrieve a bounded evidence set with `list-extractions`, using the same structured filter as the aggregate query. Start with 20 to 40 rows and omit `page` for stable keyset traversal. Send only the returned continuation key on each later request.
5. Inspect boundaries, dates, source kinds, call IDs, people, companies, types, and truncation metadata. Exclude rows with a missing person or unverified boundary from direct-voice evidence even if the structured external filter returned them. Deduplicate repeated signals from the same call before drawing conclusions.
6. Deepen only representative evidence with `get-call` and, when needed, `get-call-transcript`. Verify the transcript before quoting when `exactQuote` contains multiple speakers or unclear attribution. Sample across leading themes, companies, dates, and viewpoints rather than selecting only the newest calls.
7. Synthesize conclusions in proportion to evidence strength. Report sparse, conflicting, permission-limited, or truncated coverage explicitly.

## Retrieval Patterns

- Known call: `get-call` -> `get-call-transcript` when exact context is required.
- Find relevant calls: `search-calls` -> `get-call` -> optional transcript.
- Cross-call themes: aggregate external signals -> `list-extractions` -> selected calls/transcripts.
- Fast exploration: `search-signals`; verify candidates with structured `list-extractions` before making exact-scope claims.
- Account or person feedback: resolve identity with `search-people`, preferring an exact email, then filter calls and signals.

For direct customer evidence, use an explicit external-boundary filter and discovered taxonomy fields:

```json
{
  "where": {
    "AND": [
      { "person": { "boundary": { "eq": "external" } } },
      { "date": { "gte": "<START_ISO>", "lt": "<END_ISO>" } },
      { "<SCHEMA_SUPPORTED_FIELD>": { "<OPERATOR>": "<DISCOVERED_VALUE>" } }
    ]
  },
  "select": ["id", "sourceKind", "summary", "context", "exactQuote", "date", "types", "person", "company", "data"],
  "orderBy": [["date", "desc"]],
  "limit": 40
}
```

Replace the placeholder field, operator, and value with a clause supported by the live schema. If no reliable topic/type/tag exists, use a schema-supported content predicate or a literal `phrase` search and disclose the weaker filter. If a server version rejects omission of `page`, fall back to unchanged numbered pages and disclose the weaker pagination contract.

## Reliability Rules

- Treat signal types, tags, topics, and custom properties as organization-specific. Discover them and inspect sample results before relying on their semantics.
- An `external` boundary does not prove that a person is a current customer. Inspect available person, account, persona, or lifecycle metadata; separate prospects, partners, and advisors when identifiable. If customer status cannot be verified, describe the population as external people rather than customers.
- Search tags with a targeted term and bounded limit, following its continuation key only when more taxonomy coverage is needed. A zero tag count means no visible extractions are currently attached to that tag; it does not prove that the underlying feedback is absent.
- When using `tagIds`, pass the public UUID returned by `list-extraction-tags`; do not reuse numeric tag IDs embedded in extraction rows.
- Resolve relevant custom-property values with `search-signal-property-values`; do not infer hierarchy nodes from a property definition alone.
- Treat `phrase` as literal matching. Combine it with discovered structured types/tags or use `list-extractions`; do not use the OAuth-only `query` argument in this universal workflow.
- Use continuation keys only for the next page of an unchanged search. Restart pagination after changing any filter.
- Treat continuation keys as opaque, short-lived traversal state rather than durable citations. Cite stable signal and call IDs in the answer.
- Compare raw signal counts with unique call and company counts. Multiple extractions from one conversation do not represent multiple independent customers.
- Treat grouped type totals as non-additive unless the live schema guarantees mutually exclusive groups.
- An `exactQuote` may contain both sides of a dialogue. Quote only the clearly attributed customer fragment, using the transcript to verify ambiguous speaker boundaries.
- Distinguish absence of evidence from verified absence. Empty results may reflect permissions, source exclusions, unsupported filters, truncation, or ingestion gaps.
- Minimize unnecessary personal data. Include names, emails, or account details only when required to answer the request.
- Keep this customer-voice workflow read-only. Do not call tools annotated as mutating; hand off to an explicit mutation workflow only after user approval.

## Output Contract

Return:

- Scope: population, boundary rule, dates, sources, taxonomy, filters, pages, and coverage counts.
- Findings: concise themes ordered by directness, prevalence, and recency.
- Evidence: exact quotes only when supported, otherwise labeled paraphrases; include stable signal/call IDs, dates, and companies when useful.
- Counterevidence: meaningful disagreement or examples that weaken a theme.
- Caveats: sparse coverage, duplication, missing identity/boundary, permissions, truncation, ingestion gaps, or weak filters.
