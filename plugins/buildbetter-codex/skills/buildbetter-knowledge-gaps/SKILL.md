---
name: buildbetter-knowledge-gaps
description: Review and operate BuildBetter knowledge-gap recommendations, project attachments, durable rechecks, and release-readiness analysis with explicit evidence and mutation approval. Use when the user asks what documentation is missing, wants to approve or decline a gap, attach a gap to product work, re-run documentation checks, or assess release knowledge readiness.
---

# BuildBetter Knowledge Gaps

## Safety Contract

Search organization skills with list-skills and get-skill first. list-knowledge-gaps is observational. Review state changes, project attachments, rechecks, source sync, and release analysis create or mutate durable records and require approval for the exact gaps, project, release, or source scope.

Use release-readiness tools only when they appear in the registered MCP inventory. If a named tool is unavailable, report that state instead of guessing or using GraphQL mutation.

## Gap Review

1. Use list-knowledge-gaps with the relevant approval state, source, project, or date scope. State filters and page coverage.
2. Inspect recommendation, evidence, current state, related artifact, and whether the underlying customer or release evidence is still current.
3. Classify the next action: needs investigation, approve, decline, attach, recheck, mark done, or no-op.
4. Before review-knowledge-gap, read back the exact gap ID, current state, intended new state, and rationale. Obtain approval.
5. Before attach-knowledge-gap-to-project, verify the exact project_v2 ID with get-project, show the attachment, and obtain approval.
6. For recheck-knowledge-gap, provide a client-generated UUID idempotency key, reuse it only after an unknown outcome, and poll the returned durable receipt with get-job or the operation tool named by the response.
7. Verify final state with list-knowledge-gaps and project detail where relevant.

## Release Readiness

When registered, use sync-release-sources to refresh the explicitly approved source scope, estimate-release-knowledge-gaps for a no-surprise estimate, and analyze-release-knowledge-gaps only after reviewing the estimate and cost or work bounds. Preserve release identifier, source SHAs or versions, operation ID, and exact completion state.

## Output

Report searched scope, gap IDs and states, evidence, proposed actions, approval state, mutation receipts, operation or job IDs, project attachments, release source identifiers, completed analysis, and remaining unknowns. Distinguish recommendation reviewed, approved, attached, recheck queued, recheck completed, and documentation verified.
