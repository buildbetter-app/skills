# BuildBetter connector review instructions

Use this text in each platform's private review form, adapting only the host's
actual install steps and recording the submitted package/version. These are test
instructions, not a claim that a native walkthrough has passed.

## Access supplied separately

The publisher supplies a stable sample workspace and reviewer sign-in through
the platform's approved private channel. Use synthetic evidence with known source
links, timestamps and expected results. No passwords, tokens, tenant identifiers
or customer information belong in this public package. Review access must work
for the whole review window; follow the platform's requirements for its dedicated
test account without weakening a real user's account.

## Connection and research

1. Install the submitted package or preview app in the target host. Connect
   `https://mcp.buildbetter.app` using the host's per-user OAuth flow. Select the
   supplied sample workspace and verify that its tools are discovered.
2. Ask: “Find recurring onboarding complaints and cite representative source
   evidence.” Verify quotations and citations against the supplied sample data.
3. Ask: “Compare survey responses about our latest release and explain search
   coverage.” Verify the filters, dates, pagination and counts. If the sample
   workspace has no survey data, record that setup gap instead of inventing it.
4. Ask: “Compare feedback with connected product usage.” Only expect analytics
   when the reviewer account has an actual sample analytics connection. Missing
   sources and partial coverage must be explicit.
5. Request a Smart Tag draft without saving, evaluating, publishing or backfilling
   it. Initial review does not need paid processing or external writes.

## Permission and lifecycle checks

1. Request inaccessible evidence from a separate synthetic workspace. Expect
   denial without content disclosure. The publisher supplies any necessary
   negative-case reference privately; do not guess a real customer's identifier.
2. Reconnect, then revoke the dedicated test connection and verify that further
   calls are denied. Restore reviewer access through normal OAuth if additional
   review is needed.
3. Test any write capability included in the submission only with explicit
   sandbox authorization and the host's required confirmation. Record precisely
   what changed and have the fixture owner clean up owned sample changes.

## Evidence and troubleshooting

Record the host/client version, submitted source/package version, timestamp,
connection result, test case and sanitized result. Include a walkthrough URL and
screenshots only after real execution; never substitute test fixture images for
native evidence. Keep organization IDs and reviewer details in private records.

On HTTP 401, use the host's OAuth reconnect flow. On 403, verify workspace access.
On 429, honor retry/backoff hints. Surface server failures without fabricating
results. Unsupported embedded UI or Events must be recorded as a host capability
limit rather than represented as a verified feature. For support, use
https://github.com/buildbetter-app/skills/issues; report security or credential
details through a private channel instead of a public issue.
