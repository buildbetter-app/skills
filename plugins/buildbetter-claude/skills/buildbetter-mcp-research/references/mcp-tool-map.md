# BuildBetter MCP Tool Map

Use this reference to pick accurate MCP tools and argument shapes for open-ended BuildBetter questions.

## Global Rules

- Prefer domain tools over `run-query`.
- Use discovery tools before inventing field names or IDs.
- Most domain tools clamp limits to 100. Start with 20 to 40 for interactive answers.
- OAuth user auth is required for natural-language `search-signals.query` and mutating tools.
- API-key and structured clients can use `phrase`, `type`, `callId`, `personaIds`, and `list-extractions`.
- Use `run-query` only after `list-types`, `find-fields`, or `build-query` show that no domain tool fits.

## Calls And Transcripts

Use calls tools when the user asks about meetings, recordings, participants, transcripts, or what happened on a specific call.

- `search-calls`: `{ "phrase": "pricing review", "fromDate": "2026-06-01T00:00:00Z", "toDate": "2026-06-30T23:59:59Z", "limit": 20 }`
- `get-call`: `{ "id": 12345, "signalLimit": 20 }`
- `get-call-transcript`: `{ "id": 12345 }`

Use `get-call-transcript` for one to five known calls when the user asks what was said. Use `search-signals` or `list-extractions` for cross-call patterns.

## Signals And Extractions

Signals are extracted product/customer evidence. Use these tools for complaints, objections, feature requests, bugs, themes, sentiment, severity, topics, keywords, and extracted snippets.

- `search-signals`: fast search. Use natural-language `query` for OAuth users or structured `phrase`, `type`, `callId`, and `personaIds`.
- `search-extractions`: compatibility alias for `search-signals`; prefer `search-signals`.
- `list-extractions`: precise structured filter endpoint.
- `get-list-extractions-schema`: inspect the `list-extractions` input contract.
- `list-extraction-filter-fields`: discover metadata fields that can be used in structured filters.
- `list-signal-types`: discover configured signal type names.
- `list-signal-properties`: discover custom properties configured for signals.
- `search-signal-property-values`: search actual signal property values; supports `phrase`, `propertyName`, `propertySlug`, `callId`, and `signalId`.

Fast structured signal search:

```json
{
  "phrase": "pricing",
  "type": "objection",
  "limit": 40
}
```

Natural-language signal search for OAuth users:

```json
{
  "query": "customer complaints about onboarding from enterprise accounts",
  "limit": 40
}
```

Exact signals from one call:

```json
{
  "callId": 12345,
  "limit": 40
}
```

Structured extraction query with explicit customer voice scope:

```json
{
  "where": {
    "AND": [
      { "person": { "boundary": { "eq": "external" } } },
      { "types": { "name": { "in": ["complaint", "objection", "featureRequest", "issue"] } } }
    ]
  },
  "orderBy": [["date", "desc"]],
  "limit": 40,
  "page": 1
}
```

For `search-signals`, use `page` for direct page jumps or `nextContinuationKey` as `continuationKey` for the next page of the same search. Do not pass a continuation key while changing search arguments.

## People And Customer Records

Use people tools when the question is about a person, contact, customer/user identity, persona, title, department, or CRM attributes.

- `search-people`: `{ "phrase": "ada@example.com", "limit": 10 }`
- `search-people-properties`: `{ "phrase": "enterprise", "limit": 20 }`

Prefer emails over names when searching for internal employees or known contacts.

## Documents And Knowledge Pages

Use documents for uploaded/source documents and knowledge pages for internal wiki-style pages.

- `search-documents`: `{ "phrase": "onboarding", "includeContent": false, "limit": 20 }`
- `get-document`: `{ "id": 501 }`
- `search-knowledge-pages`: `{ "query": "onboarding", "limit": 20 }`
- `list-knowledge-pages`: `{ "limit": 20 }`
- `get-knowledge-page`: `{ "id": 123 }`

Use `includeContent: true` only when the search result itself needs full document text; otherwise fetch exact documents with `get-document`.

## Folders And Collections

Use folders when the user has an exact folder/collection ID and wants the calls, signals, documents, child folders, or conversation IDs inside it.

- `get-folder`: `{ "id": 123, "limit": 100 }`

## Projects Hub, Triage, And Linear

Use Projects Hub tools for promoted project context and triage tools for unpromoted tracked items.

- `list-project-types`: `{}`
- `list-projects`: `{ "phrase": "billing", "typeSlug": "feature_request", "limit": 20 }`
- `get-project`: `{ "id": 123 }`
- `triage-count`: `{}`
- `list-triage-items`: `{ "phrase": "billing", "typeSlug": "bug", "limit": 20 }`
- `get-triage-item`: `{ "id": 123 }`

Use Linear tools for ticket triage:

- `list-linear-teams`: `{}`
- `list-linear-projects`: `{ "teamId": "team-id" }`
- `list-linear-workflow-states`: `{ "teamId": "team-id" }`
- `list-linear-tickets`: `{ "query": "billing", "includeAlreadyAttached": false, "limit": 20 }`
- `get-linear-ticket`: `{ "id": "linear-issue-id" }`

Use `promote-triage-item` and `promote-linear-tickets` only after explicit user approval.

## Organization Skillsets

Use skillset tools when the user asks about BuildBetter-managed organization skills, workflows, or how agents should perform a repeated task.

- `list-skillsets`: `{ "phrase": "research", "limit": 20 }`
- `list-skills`: `{ "phrase": "customer voice", "limit": 20 }`
- `get-skill`: `{ "id": "00000000-0000-0000-0000-000000000000" }`
- `propose-skill-update`: requires explicit user approval and a unified diff patch.

## GraphQL Helpers

Use this path only after domain tools are insufficient.

- `list-types`: `{}`
- `find-fields`: `{ "typeName": "extraction" }`
- `build-query`: `{ "typeName": "extraction", "fields": ["id", "summary"], "limit": 20 }`
- `run-query`: `{ "query": "query { ... }", "variables": {} }`

## Common Open-Ended Flows

### "What are customers complaining about?"

1. Use `search-signals` with broad customer-voice terms or `list-extractions` with external speaker and complaint-like types.
2. Use `get-call` for the strongest call IDs if meeting context matters.
3. Summarize by theme and cite signal IDs, customers, and dates.

### "What did this customer/person say?"

1. Use `search-people` with email/name/company.
2. Use `search-calls` with the person or company phrase.
3. Use `get-call-transcript` for exact call content or `search-signals` scoped by `callId` for extracted snippets.

### "What context exists for this product area?"

1. Use `search-signals` or `list-extractions` for evidence.
2. Use `search-documents` and `search-knowledge-pages` for internal docs.
3. Use `get-folder` if the user provides a folder ID.
4. Use `list-projects` and `get-project` for promoted work and linked tickets.

### "What tickets/projects should we look at?"

1. Use `list-project-types`, `triage-count`, `list-triage-items`, and `list-projects`.
2. Use Linear discovery tools to get team/project/state IDs.
3. Use `list-linear-tickets` and `get-linear-ticket` for ticket details.
4. Ask for explicit approval before any promote action.
