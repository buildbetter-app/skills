---
name: buildbetter-customer-voice
description: Retrieve direct customer-voice evidence from BuildBetter via MCP. Use when researching customer complaints, objections, feature requests, product feedback, call evidence, discovery themes, or customer-voice synthesis from BuildBetter data, especially when the user needs reliable citations or repeatable retrieval for a product/research workflow.
---

# BuildBetter Customer Voice

## Overview

Use BuildBetter as the evidence layer. Favor deterministic MCP retrieval over vague agent guessing, show the filters you used, and separate direct customer voice from internal commentary about customers.

## Retrieval Workflow

1. Classify the request:
   - Specific call content: use `get-call-transcript` when the user gives call IDs or asks what happened in one to five calls.
   - Find relevant calls: use `search-calls`, then `get-call-transcript` for the selected calls.
   - Cross-call/customer themes: use `search-signals` or `list-extractions`.
   - Precise evidence set or compliance/research output: prefer `list-extractions` with explicit `where` filters.

2. Start with a broad, typed customer-voice query. Do not overfit the first search to a long natural-language prompt.

3. Inspect results before synthesis:
   - Confirm result IDs change when changing an important phrase.
   - Confirm `person.boundary` is external when the user wants direct customer voice.
   - Confirm type values match the intended taxonomy.
   - Use continuation keys only to fetch the next page of the same query. If the phrase, type, call, or persona changes, start over without the old continuation key.

4. Synthesize with evidence:
   - State the retrieval scope and filters used.
   - Cite signal IDs, call IDs, people, company, and dates when available.
   - Distinguish verbatim quote evidence from paraphrased signal summaries.
   - Mention meaningful gaps, such as sparse results or a search phrase that did not narrow results.

## Customer Voice Filters

For direct customer voice, prefer external speaker filters plus customer-facing signal types:

- `person.boundary: external`
- `types.name` values such as `complaint`, `objection`, `featureRequest`, `issue`, `feedback`, `bug`, `improvement`, `idea`, `inquiry`, `question`

Do not treat `customerInsight` as direct customer voice by default. In BuildBetter taxonomy it usually means internal employees describing customer behavior or feedback. Use it only when the user explicitly asks for internal customer insights, research/team interpretation, or employee commentary about customers.

Use exact type casing. `featureRequest` and `customerInsight` are camel-cased.

## Tool Patterns

Use `search-signals` for fast structured searches:

```json
{
  "phrase": "pricing",
  "type": "objection",
  "limit": 40
}
```

Use `list-extractions` when you need exact customer-voice scoping:

```json
{
  "where": {
    "AND": [
      { "person": { "boundary": { "eq": "external" } } },
      { "types": { "name": { "in": ["complaint", "objection", "featureRequest", "issue"] } } },
      {
        "OR": [
          { "summary": { "contains": "pricing" } },
          { "context": { "contains": "pricing" } },
          { "name": { "contains": "pricing" } },
          { "exactQuote": { "contains": "pricing" } },
          { "keywords": { "name": { "contains": "pricing" } } },
          { "topics": { "name": { "contains": "pricing" } } }
        ]
      }
    ]
  },
  "limit": 40,
  "page": 1
}
```

When unsure about filter fields, call `get-list-extractions-schema`, `list-extraction-filter-fields`, and `list-signal-types` before constructing a complex filter.

## Reliability Rules

Use email addresses when identifying internal people because names are less reliable. For example, find calls involving `doug.baker@zywave.com` rather than only "Doug".

Keep limits modest at first, usually 20 to 40. If requests time out, narrow filters or reduce the limit before retrying. If the analysis needs more coverage, page through stable queries with `continuationKey` rather than changing the query between pages.

Treat `phrase` as literal text matching, not guaranteed semantic retrieval. If two meaningfully different phrases return byte-identical results in the same type bucket, do not assume the phrase worked. Re-run with explicit `list-extractions` filters, compare returned IDs, and report the behavior as a retrieval limitation or suspected bug.

For customer-voice synthesis, avoid one narrow query per topic unless the user asks for a specific topic comparison. Start with a broad typed search, then cluster and summarize the returned evidence.

## Output Shape

Use this structure for synthesis:

- Scope searched: filters, limits, pages, and date/source constraints if any.
- Findings: concise themes ordered by customer evidence strength.
- Evidence: signal/call citations with customer/company/date when available.
- Caveats: missing coverage, internal-vs-external ambiguity, phrase/filter anomalies, or follow-up retrieval needed.
