---
name: buildbetter-customer-issue-triage
description: Triage, investigate, resolve, and communicate BuildBetter customer issues. Use when the user asks to look into a Linear Customer Support issue with prefix CUS-, a support ticket, customer escalation, or plain-language customer symptom such as video will not play, import is broken, transcript is missing, integration is failing, or an agent/search result looks wrong; also use for customer complaints from Linear, Slack, Gmail, recordings, transcripts, imports, integrations, or AI behavior, affected-customer incident mapping, customer/vendor follow-up, and evidence-backed data repair, code fix, Linear/GitHub updates, or customer-safe handoff.
---

# BuildBetter Customer Issue Triage

## Operating Contract

Treat `CUS-` as the primary signal that the source of truth is a Linear Customer Support issue. Start by reading the Linear issue, comments, attachments, linked Slack thread, customer, org, status, assignee, and any related issues or PRs before touching code or data.

Reconstruct the customer source material before deciding. Verify the underlying Slack thread, recording, transcript, email, attachment, or live product state instead of trusting a title, summary, or adjacent memory. If exact search fails, widen to participant, customer, time-window, and concept searches, then confirm with transcript or source context.

Build an evidence packet before acting. Include issue key/link, customer/org/user/recording identifiers, source thread or attachment, impact, timeline, live state, code paths, logs, related Linear/GitHub/Sentry coverage, diagnosis, proposed action, verification plan, customer-safe response, and remaining uncertainty.

Use explicit live-state surfaces for production work. For BuildBetter production data, prefer production Hasura, direct DB paths, CloudWatch, or `kubectl --context production ...` as appropriate. Keep environment, time window, query ids, and exact counts visible in the handoff.

Avoid duplicate tracking. Search exact issue keys, customer names, Sentry short IDs, SQL families, PR markers, and existing Linear issues before creating anything new. Update the existing issue or PR when the evidence belongs to an existing lane.

Resolve along the narrowest correct lane: answer/support explanation, customer/vendor comms, guarded data repair, code fix with tests, incident customer mapping, or coordinator/remote-thread handoff. Do not convert notes into transcripts, invent customer impact, or ship speculative fixes when the source evidence is weak.

For code changes, follow the repository `AGENTS.md`, `docs/rules/codebase-standards.md`, area-specific `AGENTS.md`, and repo PR workflow. Use focused tests that prove the touched behavior, and publish evidence-rich Linear/PR comments while keeping PR bodies concise.

## Workflow

1. Anchor the request.
   - Fetch the `CUS-*` issue or source thread first.
   - Record customer/org, source, reported symptom, requested outcome, and whether the issue is active, closed, duplicate, or already linked to a PR.

2. Recover source evidence.
   - Read linked Slack/Gmail/recording/transcript/attachment context.
   - Validate identifiers against production or the stated environment.
   - Separate confirmed facts, inference, and blocked claims.

3. Classify the issue.
   - Data/import/recording/transcript repair.
   - Product/UI bug requiring live browser proof.
   - Provider/integration failure requiring logs and provider semantics.
   - AI/agent behavior requiring production tool/log proof.
   - Incident impact mapping and outbound communication.
   - Existing engineering/Sentry/DB lane that should be reused.

4. Investigate with the smallest decisive surface.
   - Read the nearest code paths and tests before editing.
   - Query live state only for the entities and time windows needed.
   - Preserve exact counts, ids, timestamps, log query ids, and URLs.

5. Decide and act.
   - If the customer needs an explanation, draft the response with confirmed facts and next action.
   - If data must change, dry-run the target set, inspect foreign keys or dependent rows, then perform the guarded repair and re-read visible state. Irreversible production changes (hard deletes, overwrites) require Nikhil's explicit direction; until then the deliverable is the dry-run evidence and proposed statement set.
   - If code must change, branch/fix/test/publish narrowly and follow the repository's `AGENTS.md` for GitHub identity and reviewer selection.
   - If another workstream should continue it, send a concrete coordinator or child-thread handoff with evidence and acceptance criteria.

6. Publish and close.
   - Update Linear with evidence, action taken, verification, and remaining risk.
   - Keep customer-facing or vendor-facing text free of internal paths, secrets, raw SQL, implementation trivia, and speculative blame.
   - End with the issue in one of: resolved, fixed-awaiting-release, existing-lane-updated, blocked-with-missing-evidence, or handed off with a concrete owner/path.

## Reference

Read [playbook.md](references/playbook.md) when the issue touches production data, recordings, transcripts, provider media, incidents, outbound customer/vendor communication, or when you need example evidence packet shapes from prior BuildBetter sessions.
