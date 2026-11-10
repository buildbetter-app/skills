---
name: buildbetter-review-improve-smart-tag
description: Review a canonical Smart Tag's evaluation cases, record false positives and false negatives, calculate readiness, and run a bounded prompt-improvement regression on the same tag-group member.
---

# Review and improve a Smart Tag

Requires the BuildBetter MCP release that exposes `list-tag-groups`,
`list-tag-group-tags`, and the durable Smart Tag workflow tools below. Do not
install or distribute this skill against an older production MCP inventory.

## Workflow

1. Call `list-tag-groups` and `list-tag-group-tags` to resolve the canonical `memberId`, then call `get-smart-tag-workflow`. Do not create a separate tag or group.
2. If the live tag is published, call `create-smart-tag-revision` or resume its existing candidate. The candidate keeps the same member, tag, group, and target while the published revision continues live.
3. Poll any pending evaluation or improvement with `get-smart-tag-operation`; do not edit the candidate or start concurrent work.
4. To run a fresh regression, disclose the bounded date range, example limit, and maximum credits, obtain approval, generate an idempotency UUID, and call `run-smart-tag-evaluation` with `includeAlreadyProcessed: true` when recently classified records should be eligible.
5. After the requested run completes, present every case with its prediction and evidence. Ask the user to mark `should match` or `should not match` when their intent is not already explicit. Capture a concrete exclusion reason for false positives and a positive pattern for false negatives.
6. Call `review-smart-tag-evaluation` with the complete set of judgments and current revision. Report true/false positives and negatives, precision, recall, pre-filter recall, F1, corpus balance, and readiness.
7. If pre-filter recall is weak, revise approved terms and run a new evaluation. Instruction-only improvement cannot recover examples filtered out before classification.
8. For a fully reviewed but unready corpus, let `N` be the locked-corpus size. Show the approved ceiling: one improvement iteration costs `N` credits and three iterations can cost `3N`. Obtain approval, generate an idempotency UUID, and call `improve-smart-tag` with `memberId`, current revision, `maxCreditBudget`, and at most five iterations.
9. Poll the operation until terminal. Report exact credits, instruction diff, rationale, metrics, and remaining errors. Stop when the user accepts the quality, the target is met, the cap is reached, or quality stops improving.

## Guardrails

- Never invent judgments or let the model silently grade disputed cases.
- Every evaluated object is billed once per iteration, including rejected and no-match predictions.
- Keep the same canonical member ID across revisions and product/MCP handoffs.
- Do not publish, backfill, pause, archive, create a group, or create another tag as part of improvement.
- Publication and backfill require separate explicit approval.
