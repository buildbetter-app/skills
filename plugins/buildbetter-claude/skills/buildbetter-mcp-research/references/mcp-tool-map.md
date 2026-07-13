# BuildBetter MCP Tool Map

Use this reference to select domain tools and stable argument shapes. Tool availability is organization- and release-dependent; use the MCP tool inventory as the source of truth when it differs.

This reference covers general-purpose, organization-scoped research reads on the current MCP surface. Feature-gated organization workflows and mutating automation are intentionally outside this skill. Built-in MCP prompts are convenience shortcuts; they do not replace the taxonomy discovery, coverage checks, and evidence validation in these skills.

## Global Rules

- Prefer domain tools over `run-query`.
- Discover organization metadata before inventing names or IDs.
- Start with limits of 20 to 40. Domain tools generally cap lists at 100.
- Use aggregate tools for totals and distributions rather than paging every row.
- Use `run-query` only after `list-types`, `find-fields`, or `build-query` confirms that no domain tool fits.
- Use structured reads with the available authenticated organization context.

## Calls And Transcripts

- `search-calls`: `{ "phrase": "pricing review", "fromDate": "2026-06-01T00:00:00Z", "toDate": "2026-07-01T00:00:00Z", "limit": 20 }`
- `get-call`: `{ "id": 12345, "signalLimit": 20 }`
- `get-call-transcript`: `{ "id": 12345 }`

Use transcripts for exact statements from a small known set of calls; use signal/extraction tools for cross-call patterns. If a selected call has no transcript, `get-call-transcript` returns that state without changing data.

## Signals And Extractions

- `search-signals`: fast discovery with structured `phrase`, `type`, `callId`, `personaIds`, and `tagNames`.
- `search-extractions`: compatibility alias; prefer `search-signals`.
- `list-extractions`: exact structured filters and selected fields.
- `get-list-extractions-schema`: current structured input contract.
- `list-extraction-filter-fields`: organization metadata fields.
- `list-signal-types`, `list-signal-properties`, `search-signal-property-values`: configured taxonomy and values.
- `list-extraction-tags`: public tag IDs/names and optional counts.

Do not use the OAuth-only `query` argument in this universal skill. Build the search from discovered structured fields instead.
Treat a zero tag count as “no visible attached signals for this tag,” not proof that the underlying topic is absent; compare literal and structured evidence searches.

Fast structured search:

```json
{
  "phrase": "pricing",
  "type": "configured-type-name",
  "limit": 40
}
```

Exact structured filter:

```json
{
  "where": {
    "AND": [
      { "person": { "boundary": { "eq": "external" } } },
      { "date": { "gte": "2026-06-01T00:00:00Z", "lt": "2026-07-01T00:00:00Z" } }
    ]
  },
  "select": ["id", "sourceKind", "summary", "context", "exactQuote", "date", "types", "person", "company", "data"],
  "orderBy": [["date", "desc"]],
  "limit": 40
}
```

Omit `page` to use stable keyset pagination. For the next `list-extractions` page, send only the returned `nextContinuationKey` as `continuationKey`; the key carries the original query. If a server version rejects the omission, fall back to unchanged numbered pages and disclose the weaker pagination contract.

## Counts And Trends

- `aggregate-signals`: total signals, unique calls/people/companies, recency, distributions, and top people/companies for a structured filter.
- `aggregate-extractions`: counts, date buckets, and grouped counts by tag, topic, keyword, or type.
- `aggregate-signals-by-tags`: exact smart-tag rollups with optional time buckets.

Signal coverage and top entities with `aggregate-signals`:

```json
{
  "where": { "person": { "boundary": { "eq": "external" } } },
  "topLimit": 10
}
```

Grouped extraction counts with `aggregate-extractions`:

```json
{
  "where": { "person": { "boundary": { "eq": "external" } } },
  "groupBy": "type",
  "limit": 25
}
```

Exact tag rollups with `aggregate-signals-by-tags`:

```json
{
  "tagNames": ["<DISCOVERED_TAG_NAME>"],
  "where": { "person": { "boundary": { "eq": "external" } } },
  "buckets": [
    { "name": "recent", "fromDate": "2026-06-01", "toDate": "2026-07-01" }
  ],
  "topLimit": 10
}
```

Bucket end timestamps are exclusive. State bucket boundaries in the answer. `aggregate-extractions` returns bucket counts on grouped results, so include `groupBy` when requesting `buckets`. Grouped counts can overlap when one signal has multiple types, tags, topics, or keywords; do not add them as though they were mutually exclusive.

## People And Companies

- `search-people`: `{ "phrase": "person@example.com", "limit": 10 }`
- `search-people-properties`: `{ "phrase": "enterprise", "limit": 20 }`

Prefer an exact email for a known person. Verify company and boundary metadata before treating a match as the intended identity.

## Documents, Knowledge, And Folders

- `search-documents`: `{ "phrase": "onboarding", "includeContent": false, "limit": 20 }`
- `get-document`: `{ "id": 501 }`
- `search-knowledge-pages`: `{ "query": "onboarding", "limit": 20 }`
- `list-knowledge-pages`: `{ "limit": 20 }`
- `get-knowledge-page`: `{ "id": 123 }`
- `get-folder`: `{ "id": 123, "limit": 100 }`

Fetch full content only for selected candidates. An exact folder ID can reveal its calls, signals, documents, child folders, or conversations.

## Projects And Triage

- `list-project-types`: `{}`
- `list-projects`: `{ "phrase": "billing", "limit": 20 }`
- `get-project`: `{ "id": 123 }`
- `triage-count`: `{}`
- `list-triage-items`: `{ "phrase": "billing", "limit": 20 }`
- `get-triage-item`: `{ "id": 123 }`

Projects Hub and triage are separate coverage surfaces. Search each relevant surface and state any exclusion.
Use a `typeSlug` only after discovering it with `list-project-types`; project taxonomies vary by organization.

## GraphQL Helpers

- `list-types`: discover schema types.
- `find-fields`: inspect one type's fields.
- `build-query`: generate a bounded query.
- `run-query`: execute only the reviewed query and variables.

## Common Flows

### What are customers saying about a product area?

1. Discover configured signal types and tags.
2. Aggregate external evidence for coverage and distributions.
3. List a bounded evidence set with the same filter.
4. Fetch call context or transcripts only for the strongest candidates.

### What did this person or account say?

1. Resolve identity with `search-people`, preferring email.
2. Find relevant calls and signals.
3. Fetch transcripts only when exact statements are required.

### What context exists for this initiative?

1. Search signals/extractions for evidence.
2. Search documents and knowledge pages for internal context.
3. Query Projects Hub and triage.
4. State which surfaces were and were not searched; linked integration data returned by project detail is supporting context, not proof that an external system was searched.
