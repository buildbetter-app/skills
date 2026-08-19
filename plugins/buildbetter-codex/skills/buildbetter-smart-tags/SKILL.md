---
name: buildbetter-smart-tags
description: Create, evaluate, review, improve, publish, backfill, and govern BuildBetter Smart Tags using durable revisions, real bounded corpora, exact credit receipts, and approval gates. Use when the user asks to build or change a Smart Tag, test classification instructions, review predictions, publish a tag, run historical tagging, or manage tag access and lifecycle.
---

# BuildBetter Smart Tags

## Safety Contract

Search organization skills with list-skills and get-skill first. Always discover existing groups and members before creating anything. A bounded request to draft and test a Smart Tag authorizes dormant draft edits, the agreed evaluation, review, and disposable draft cleanup. Publishing, historical backfills, access changes, lifecycle changes, group creation, and deletion of non-disposable resources each require exact approval.

If a named tool is missing from the registered MCP inventory, stop that path. Never emulate Smart Tag mutations through GraphQL.

## Workflow

1. Call list-tag-groups and list-tag-group-tags. Show candidate groups and exact public IDs. Reuse an existing group unless the user explicitly requests a new one.
2. Restate target object, category breadth, inclusion and exclusion rules, ambiguity handling, evidence sources, and whether multiple or skipped tags are allowed.
3. Use get-smart-tag-workflow for an existing member. Create-smart-tag-draft for a dormant first version or create-smart-tag-revision for a candidate based on a live tag.
4. Use suggest-smart-tag-prefilter when a bounded unfiltered sample would be irrelevant. Review accepted and rejected terms; pass accepted keywords directly to run-smart-tag-evaluation rather than adding a redundant draft mutation.
5. Queue run-smart-tag-evaluation with a client-generated UUID idempotencyKey. Reuse the exact key only after an unknown outcome. Read back the bounded corpus and metered credit scope.
6. Poll get-smart-tag-operation. Report operation ID, state, evaluated objects, exact credits, errors, and product path.
7. Review every prediction needed for a trustworthy corpus with review-smart-tag-evaluation. Explain disagreements. Use improve-smart-tag only with a caller-approved maximum credit budget, then poll its operation.
8. Publish only after the revision is reviewed and the user approves the exact member, revision, readiness exception if any, and backfill choice.
9. For a backfill, run the matching preview immediately before approval. Present source-scope, prefilter-matched, eligible counts, and maximum credits. Start or publish with the unchanged approved planning receipt and a new idempotency key.
10. Monitor get-smart-tag-backfill. Cancellation, resume, lifecycle, access, archive, and deletion are separate decisions.

## State Discipline

Use exact states: dormant draft, candidate revision, evaluation queued or running or completed, reviewed, ready, published, backfill previewed, backfill approved, backfill running, and backfill completed. A local reasoning sample is not a BuildBetter evaluation.

## Output

Report group and member IDs, revision, instructions, corpus scope, operation and planning IDs, idempotency keys without secrets, review metrics, exact credits, approval state, publish state, backfill progress, links, and remaining blockers.
