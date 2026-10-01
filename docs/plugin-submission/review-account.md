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

## Reviewer Instructions

1. Install the selected review version through the ChatGPT review flow; Git-backed marketplace installation remains available for separate Codex checks.
2. Start a new ChatGPT chat and complete BuildBetter OAuth.
3. Choose the designated sample review organization.
4. Run the manifest's positive and negative cases, including analytics, interactive selection, and an explicitly requested Events monitor.
5. Compare the actual answer, selected sources, tool path, and refusal behavior with the manifest. Record unsupported client/workspace capabilities explicitly.
6. Save sanitized ChatGPT transcripts and a real walkthrough. Keep the existing Codex hero cases as separate client evidence.

## Private review setup

- Reviewer username/password or SSO access must be supplied outside git.
- Select the existing verified OpenAI organization, project, and developer identity before uploading the new version.
- Provide a dedicated account that works without MFA approval, one-time codes, magic links, or private-network access.
- Run the five positive and three negative manifest cases using that account and capture an accessible walkthrough URL.
- Upload the generated ZIP, complete the MCP scan, resolve required findings, and submit the selected draft for review. Auth details are entered separately in Review details, never in the ZIP.
