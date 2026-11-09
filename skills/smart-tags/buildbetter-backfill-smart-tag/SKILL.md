---
name: buildbetter-backfill-smart-tag
description: Preview and run a bounded BuildBetter Smart Tag backfill for one canonical tag-group member with explicit approval, durable polling, and exact metered-credit reporting.
---

# Backfill a Smart Tag

Requires the BuildBetter MCP release that exposes `list-tag-groups`,
`list-tag-group-tags`, and the durable Smart Tag workflow tools below. Do not
install or distribute this skill against an older production MCP inventory.

## Workflow

1. Resolve the tag with `list-tag-groups` and `list-tag-group-tags`, then call `get-smart-tag-workflow` using its canonical `memberId`.
2. Require a published workflow and confirm the same group remains visible and writable. Never substitute a same-name group or create a new group for replay.
3. Collect an inclusive start, exclusive end, and maximum record count. The member's group owns the target. Keep `allowLargeReplay` false unless the user explicitly approves a large cohort.
4. Call `preview-smart-tag-backfill` with `memberId`, current revision, dates, limit, and large-replay setting. Report matched objects, existing exact associations, replay candidates, truncation, and maximum credits.
5. Explain billing: each newly inserted AI-produced tag association costs one credit. Existing associations, filtered-out objects, and no-match results cost zero. The preview is an upper bound; operation status is exact.
6. Obtain explicit approval for the exact preview. Generate one idempotency UUID and call `start-smart-tag-backfill` with the same member, revision, scope, and the approved preview. Reuse the UUID only after an unknown result for that identical start.
7. Report the operation ID immediately. Poll `get-smart-tag-backfill` with the same member and operation IDs until terminal when completion is requested. Report pending/running/completed/failed/cancelled objects, inserted associations, and exact credits.
8. Use `cancel-smart-tag-backfill` or `resume-smart-tag-backfill` on that same operation only when requested.

## Guardrails

- Never widen dates, increase the limit, or enable large replay after approval.
- Preview again when the member revision, target, dates, or limit changes.
- Never create another group, tag, member, or workflow identity for backfill.
- Use the member-bound backfill tools, not the group-level compatibility replay tools.
