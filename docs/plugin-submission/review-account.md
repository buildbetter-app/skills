# Review Account And Auth Plan

BuildBetter MCP uses OAuth and requires organization context. Review credentials must be provided privately through the submission form or a secure reviewer channel; do not commit credentials to this repository.

## Review Tenant Requirements

Create or designate one production-like tenant:

- Organization name: BuildBetter Review Sandbox
- Auth path: OAuth through `https://mcp.buildbetter.app`
- Role: read access to recordings, signals, surveys/responses, connected analytics, documents, Knowledge, people, personas, companies, and custom properties; any draft-writing permission is scoped to sample data
- Data: realistic dummy customer data only; no real customer PII
- Availability: tenant remains stable for the review window

## Fixture Data Checklist

Seed enough data for the hero cases:

- Imported support conversations with source provenance.
- A native survey with sample responses, plus a draft that is safe to inspect.
- A sample analytics connection for analytics cases after those tools deploy.
- At least 5 recordings from the last 90 days.
- At least 1 call with transcript and `hasTranscript` true.
- At least 10 signals covering SSO, onboarding, pricing, setup complexity, and enterprise concerns.
- At least 2 signal types such as `featureRequest` and `complaint`.
- At least 3 people with company and persona context.
- At least 3 documents and 3 knowledge pages relevant to onboarding/admin workflows.
- At least 2 custom property definitions and property values for signals or people.

The Codex hero suite also needs the following case-specific fixtures. A sandbox
operator prepares them before the reviewer starts and records actual IDs,
permissions, date bounds, and expected results privately. Missing fixtures mean
BLOCKED setup; they must not be invented or created implicitly by a read case.

| Case | Required fixture and permissions |
| --- | --- |
| BB-HERO-010 | An accessible analytics connection/project with a real signup event and timestamped synthetic events covering each of the last seven days. Record the event's actual name, project timezone, daily expected counts, and read permissions. Refresh the rolling fixture before a later rerun. |
| BB-HERO-011 | An accessible recording/transcript with an exact quote, its verified timestamp, and known media availability. Execute the hero JSON's setup steps and record the actual recording ID before substituting the prompt. |
| BB-HERO-012 | A uniquely identifiable synthetic person named James, with company/persona context and accessible onboarding or preparation signals linked to that person inside the last 90 days. Record expected signal IDs and pagination bounds; refresh rolling dates for later reruns. |
| BB-HERO-013 | An existing job receipt owned by the connected OAuth user and organization. Obtain it from previously authorized sandbox work or an explicitly authorized disposable fixture; verify it with `get-job` and substitute its actual UUID. A completed receipt covers only completed-state rendering. |
| BB-HERO-014 | An accessible existing Smart Tag group and sample tags. Permit creating a draft in that sandbox group for this requested case; evaluation, publication, backfill, and credit spending remain excluded. Record the group ID and remove the owned draft after QA. |
| BB-HERO-015 | A supported provider test account, privately supplied provider access, and permission for the reviewer to add a sandbox integration. Complete actual provider consent in the supported sign-in flow; never paste credentials into chat. Discover advertised setup tools or record the exact supported handoff. Record resulting connection/project IDs and have the operator remove the owned test connection after QA. |
| BB-HERO-016 | Accessible lifecycle property definitions, actual stage values, and sample evidence linked to those values, including onboarding and retention. Record property/stage IDs and expected evidence counts. Grant read access; this case must not modify the taxonomy. |

## Reviewer Instructions

1. Install the selected review version through the ChatGPT review flow; Git-backed marketplace installation remains available for separate Codex checks.
2. Start a new ChatGPT chat and complete BuildBetter OAuth.
3. Choose the designated sample review organization.
4. Run the manifest's positive and negative cases, including analytics, interactive selection, and an explicitly requested Events monitor.
5. Compare the actual answer, selected sources, tool path, and refusal behavior with the manifest. Record unsupported client/workspace capabilities explicitly.
6. Save sanitized ChatGPT transcripts and a real walkthrough. Keep the existing Codex hero cases as separate client evidence.

For the separate Codex suite, load
[`evals/plugin-submission/hero-cases.json`](../../evals/plugin-submission/hero-cases.json),
complete the fixture checklist and each case's `setup_steps`, then substitute
verified fixture values into its prompt. Confirm that `{{recordingId}}`,
`{{quote}}`, `{{jobId}}`, and any other fixture placeholders are fully replaced
before sending it. Save the setup receipt with the sanitized case transcript.
Apply each case's stated permission boundary: only the requested sandbox draft
and integration-connection cases permit their narrow writes. Read cases and the
Events reviewer remain read-only; paid processing and external delivery need
their own explicit authorization.

## Private review setup

- Reviewer username/password or SSO access must be supplied outside git.
- Select the existing verified OpenAI organization, project, and developer identity before uploading the new version.
- Provide a dedicated account that works without MFA approval, one-time codes, magic links, or private-network access.
- Run all five positive and three negative manifest cases using that account and capture an accessible walkthrough URL.
- Upload the generated ZIP, complete the MCP scan, resolve required findings, and submit the selected draft for review. Auth details are entered separately in Review details, never in the ZIP.

## Deterministic future-event fixture

The reviewer stays read-only. A separately authorized sandbox operator supplies the
event after the reviewer subscribes; pre-seeded historical records do not count.

1. Prepare a fresh synthetic support conversation in the sandbox support
   provider with one unmistakable feature request and a unique review-run marker.
   Keep it unimported until the monitor is active; a recording-derived signal
   does not match this support-scoped manifest case.
2. The reviewer explicitly requests a `signal.created` monitor with
   `arguments: {sourceType: "support"}` in the designated review workspace. Record its subscription ID, activation time, filter, and
   granted expiration from the Events response.
3. After activation, the sandbox operator runs the sandbox support integration
   sync to import the new conversation through the normal authorized product
   flow and waits for its normal signal extraction to complete.
   The operator must use their own account; never grant writes to the reviewer.
4. Record the completed producer job and the new signal's public ID and immutable
   occurrence time. Require an occurrence after activation and before expiration.
5. Verify the host receives a notification for that ID with
   `sourceType: "support"`. The reviewer retrieves
   its current accessible evidence through `search-signals` and checks the marker.
6. Save sanitized producer, delivery, and retrieval receipts. Retry with a fresh
   marker only after diagnosing a missing producer or delivery; do not backdate
   records or manually POST a webhook and call that producer acceptance.
7. Unsubscribe and have the operator remove the owned sample data after review.

Until the endpoint and operator are available, Events execution remains pending.
The same approach can separately exercise `survey.response.submitted` by having
an authorized test respondent submit one new response to the selected dummy
survey after activation, and `recording.completed` by completing a fresh import.
