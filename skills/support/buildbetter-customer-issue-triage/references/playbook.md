# Customer Issue Triage Playbook

## Evidence Packet

Use this shape before data changes, code changes, external comms, or Linear closure:

- Request: exact user ask, `CUS-*` key, Linear link, current status, assignee, customer, org, source channel.
- Source material: linked Slack thread, email, attachment, recording, transcript, browser page, or vendor thread. Note what was actually read.
- Impact: affected users, orgs, recordings, imports, integrations, time window, customer-visible symptom, and severity.
- Live state: production/staging/local environment, query/log commands, exact ids, counts, timestamps, and URLs.
- Code path: files/services/controllers/workers/UI components that explain the behavior.
- Related coverage: existing Linear issues, PRs, Sentry short IDs, DB-query families, release/deploy boundaries, and comments already present.
- Diagnosis: confirmed cause, plausible contributing factors, and rejected hypotheses.
- Action: support response, vendor question, data repair, code fix, rollback, release state update, or handoff.
- Verification: focused tests, live UI checks, production re-reads, queue/log checks, or no-run reason.
- Customer-safe note: wording that can be sent externally, stripped of internal implementation details.
- Uncertainty: missing access, stale logs, provider ambiguity, unverifiable customer claims, or approval needed.

## Source-Recovery Rules

- If a Linear CUS issue is created from Slack, read the Slack source or attachment before interpreting the title.
- If a source summary seems off-topic, pause ticket creation or closure and verify the underlying recording, email, or full source.
- If exact text search for a recording or complaint fails, widen to participants, customer name, time window, and concepts, then confirm with transcript/source context.
- If a customer file is an archive, inspect file count, date range, headers, format, and semantic type before mapping it to product objects.
- If customer text is recap notes rather than speaker-turn transcripts, do not synthesize transcript structure unless Nikhil explicitly accepts that product tradeoff.

## Investigation Lanes

### Customer Data Or Import Repair

Use for archive ingestion, mistaken import, missing rows, bad metadata, and cleanup requests.

- Identify the canonical org/workspace before modifying rows. Watch for duplicate orgs.
- Compare source files to existing rows and soft-deleted rows before creating anything.
- Preserve source semantics: notes stay notes; transcripts require transcript evidence.
- Hard deletes and other irreversible production changes require Nikhil's explicit direction. Default to soft-delete/restore paths and present dry-run evidence first.
- Before deletes, enumerate dependent rows and restrictive foreign keys. Check transcript rows, signals, folders, tags, uploads, topic groups, materialized permissions, and set-null references where relevant.
- After writes, verify as a normal customer/user-visible path when possible.

Prior example: `CUS-1289` restored 93 TXT interview-note files for `OurRitual / org 59030`, kept transcript states unavailable because the files were recaps, then hard-deleted 94 target upload-text rows only after Nikhil explicitly redirected to removal and after confirming no dependent transcript, extraction, folder, tag, upload, topic-group, or set-null cleanup remained.

### Recording, Video, Transcript, And Provider Media

Use for unavailable videos, stuck processing, Recall/Gong/Fireflies/Fathom/Deepgram/Mux media, and transcript gaps.

- Start from the customer-visible UI guard, then trace to recording data fields (the legacy `interview` storage model).
- Query production rows for `asset_state`, `asset_uri`, `asset_url`, transcript status, provider ids, org ids, and affected recording ids.
- Check worker queues and CloudWatch/provider logs for terminal versus transient provider failures.
- Distinguish terminal provider authorization/content errors from transient 429/5xx/network errors.
- If the provider is the blocker, draft vendor/customer follow-up with concrete examples, timestamps, states, missing media artifacts, and exact questions.

Prior example: `CUS-1256` proved signal video rendering depended on `signal.call.asset_url`, traced affected Gong calls to `asset_state = error` and no `asset_uri`, then found CloudWatch `asset-url-retrieval-forbidden` 403 failures and handed off the terminal provider-side path.

### Product Or UI Bug

Use when the issue claims a user-visible flow is broken.

- Reproduce the exact role/org/user path when feasible.
- Inspect the live UI or screenshots in addition to data rows.
- Validate the fix in the real product surface, not only through unit tests.
- Keep customer-facing labels and screenshots separate from internal debug evidence.

Prior example: `CUS-1265` person-merge validation was only proven after live production People UI testing; the underlying bug was duplicate key failure when the chosen merge email belonged to another non-selected person in the org.

### AI, Agent, Metadata, Or Search Behavior

Use when a customer says an agent, search, tagging, metadata, or classification flow failed.

- Separate tool availability from tool execution. A prompt/tool loaded log is not proof the agent used it.
- Search production logs for the exact tool/function/event that would prove execution.
- Tie the complaint to the likely customer ticket by matching domain language, not only status or recency.
- Check the product data source the agent should have used, then decide whether this is product behavior, prompt/tooling, missing sync, or customer education.

Prior example: `CUS-1211` matched a Salesforce ICP/segment metadata complaint; production logs showed the metadata tool was loaded on the deployed image but had zero actual execution hits in the checked window.

### Incident Customer Mapping And Outreach

Use when an incident thread names provider objects or bot ids and Nikhil asks for affected customers, owners, or email drafts.

- Map provider ids through the strongest production join path, then use secondary paths to confirm.
- Deduplicate customers and recipients before outreach.
- For Recall bot incidents, the durable path was `recall_calendar_bot.recall_bot_id -> calendar_event -> organization`, with the legacy recording table `interview` as secondary confirmation.
- For Recall-created recordings, prefer `permission_user.is_owner = true` as owner signal; for scheduled bots without recording rows in the legacy `interview` table, fall back to mapped calendar users or organizers.
- Preserve relative-time wording. If Nikhil says it is the next day, say "yesterday" in the email rather than sounding same-day.
- If CC/BCC is required and the local wrapper cannot do it, use raw Gmail RFC 2822 send after verifying the active Gmail account and corrected addresses.

## Linear And Publication Rules

- Search existing Linear issues before creating a new one. For repeated families, comment on the live issue with fresh evidence.
- Keep exact issue links, comment URLs, Sentry URLs, event URLs, CloudWatch query ids, PR URLs, and release/deploy boundaries in internal comments.
- Use `searchIssues(term: ..., first: ...)` for Linear GraphQL searches when applicable; avoid stale `issueSearch` assumptions unless the live schema confirms it.
- Shell-quoted comments must not let zsh expand SQL placeholders like `$4`; build comment bodies safely or paraphrase placeholders.
- For PRs in BuildBetter repos, follow the repository's `AGENTS.md` for GitHub identity and reviewer selection, keep PR bodies concise, and put verification in PR comments.
- Customer-facing responses should state the confirmed customer impact, what changed, what the customer should expect next, and any action requested. Omit raw SQL, internal file paths, Linear titles, secret names, and operational breadcrumbs.

## Common Pitfalls

- Duplicate issue: triage started from memory instead of live Linear/GitHub/Sentry/source state. Reconcile first.
- Wrong customer/org: the first matching org or summary was adjacent but not canonical. Verify the customer source and org id.
- Fake transcript: notes or summaries were forced into transcript tables. Preserve source semantics.
- Overbroad outage claim: active in-progress recordings were mixed with stale or terminal failures. Split states before summarizing impact.
- Silent closure: a Sentry/provider issue disappeared but no merge/deploy/provider boundary proves it is fixed. Keep it awaiting proof.
- Stale review state: GitHub says `CHANGES_REQUESTED` but no unresolved thread remains. Inspect review threads directly.
- No owner in outreach: provider ids were mapped only to orgs. Resolve owners/recipients before drafting or sending.
- Missing CC: the simple Gmail wrapper dropped CC/BCC. Use raw Gmail send when CC matters.
