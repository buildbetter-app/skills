---
name: buildbetter-create-smart-tag
description: Create or configure a canonical BuildBetter tag inside an existing tag group, run a bounded metered evaluation, and continue the same tag in the product wizard. Use when a user wants to create, configure, or test a Smart Tag through BuildBetter MCP.
---

# Create and test a Smart Tag

Requires the BuildBetter MCP release that exposes `list-tag-groups`,
`list-tag-group-tags`, and the durable Smart Tag workflow tools below. Do not
install or distribute this skill against an older production MCP inventory.

A Smart Tag is an existing tag inside an existing tag group. Its `memberId` is the stable identity used by MCP and the product wizard. Never create a parallel definition or a temporary tag group.

## Workflow

1. Require an OAuth-authenticated user for mutations.
2. Call `list-tag-groups`, have the user select a writable group, then call `list-tag-group-tags`. Organization Groups are permission principals; tag groups organize tags.
3. Reuse the returned `memberId` when the tag already exists. If the user explicitly wants a new tag, call `preview-smart-tag-setup` with the selected `tagGroupId`, one tag name, description, labeling instructions, `activateNewTags: false`, and `updateExisting: false`. Confirm the preview will add a dormant tag to that exact group, obtain approval, then call `apply-smart-tag-setup` with the unchanged input. Use the created member ID from `members`; do not create another group. The tag becomes live only after publication.
4. Write labeling instructions that define positive conditions, exclusions, and ambiguous mentions. The group already owns the target: signals use the legacy contract value `extraction`; full recordings use `interview`. Keep those exact values when invoking tools.
5. Call `create-smart-tag-draft` with the canonical `memberId`, instructions, and initial pre-filter. If the tag already has a published workflow, use `create-smart-tag-revision`; never mutate the live revision. If a candidate already exists, resume it.
6. Return `productPath`. It opens this same tag and workflow in the visual wizard.
7. Keep the first evaluation bounded, normally 10–15 examples and no more than 100 candidates. Use exhaustive sampling when false negatives matter. Use keyword pre-filtering when the concept has reliable vocabulary.
8. When useful, call `suggest-smart-tag-prefilter` for the current member and revision. Show the proposed keywords and real-corpus estimate, then persist only approved terms with `update-smart-tag-draft`.
9. Explain the maximum cost and obtain approval: each object evaluated costs one credit per iteration, including no-match predictions. Objects outside the evaluation cohort cost zero.
10. Generate an idempotency UUID and call `run-smart-tag-evaluation` with `memberId`, current revision, explicit date bounds, candidate limit, and example limit. Reuse the same UUID only after an unknown result or an approved retry of that identical operation.
11. Poll `get-smart-tag-operation` with the same member and operation IDs until terminal when completion is requested. Report case counts, exact credits, errors, and the product review link. Use `cancel-smart-tag-operation` only when the user asks to stop it.

Hand completed evidence to `buildbetter-review-improve-smart-tag`. Evaluation is not publication approval. Publishing and historical backfill each require separate explicit approval.

## Guardrails

- Never choose a group by name when a public ID is available.
- Never create a group as a side effect of creating, testing, revising, or backfilling a tag.
- Never create a second Smart Tag identity for a tag-group member.
- Preserve the returned member ID and revision across MCP and product handoffs.
- Never publish automatically.
