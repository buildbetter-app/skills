---
name: buildbetter-project-triage
description: Inspect and route BuildBetter Projects Hub, triage items, and Linear tickets with rich evidence, metadata discovery, and explicit promotion approval. Use when the user asks what is in triage, wants project context, needs to review linked tickets, compare product work, or promote a triage item or Linear ticket into a project.
---

# BuildBetter Project Triage

## Safety Contract

Search organization skills with list-skills and get-skill first. Reading Projects Hub, triage, and connected ticket evidence is observational. promote-triage-item and promote-linear-tickets create project state and require explicit approval for the exact source items and target type.

If a required domain tool is unavailable, report the missing surface. Do not fall back to guessed GraphQL mutations.

## Read Workflow

1. Use triage-count for inbox volume and list-project-types for current type IDs, slugs, and rules.
2. Use list-triage-items for unpromoted work and get-triage-item for rich detail: evidence, taxonomy, linked metadata, tickets, timeline, metrics, waiting-on rows, and agent sessions when present.
3. Use list-projects for promoted work and get-project for the authoritative project_v2 detail. Keep triage item IDs, legacy tracked item IDs, and project_v2 IDs distinct.
4. For Linear, discover filters with list-linear-teams, list-linear-projects, and list-linear-workflow-states. Then use list-linear-tickets and get-linear-ticket.
5. Compare candidates on customer evidence, strategic fit, type, existing project coverage, linked-ticket state, owner, dependencies, and uncertainty. Do not infer priority from source system order.

## Promotion Workflow

1. Identify exact triage or Linear IDs, current state, proposed project type, duplicates, and already-attached items.
2. Show a readback: source title and ID, evidence summary, selected type and ID, expected created project count, and skipped or duplicate behavior.
3. Obtain explicit approval.
4. Call promote-triage-item for one triage item or promote-linear-tickets for the approved Linear external IDs.
5. Read the result. Treat returned projectId values as project_v2 IDs; legacy trackedItemId may be an alias.
6. Verify with get-project and report created, skipped, failed, or ambiguous results exactly.

## Output

Report scope and filters, counts, item or project IDs, evidence, linked-ticket state, recommended next action, approval state, promotion receipt, created project IDs, skipped items, and verification. A recommendation is not a promotion.
