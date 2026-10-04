# Review Account And Auth Plan

BuildBetter MCP uses OAuth and requires organization context. Review credentials must be provided privately through the submission form or a secure reviewer channel; do not commit credentials to this repository.

## Review Tenant Requirements

Create or designate one production-like tenant:

- Organization name: BuildBetter Review Sandbox
- Auth path: OAuth through `https://mcp.buildbetter.app`
- Role: read access to calls, signals/extractions, documents, knowledge pages, people, personas, companies, and custom properties
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

1. Install the plugin from the Git-backed marketplace.
2. Start a new Codex thread.
3. Connect BuildBetter when Codex prompts for MCP auth.
4. Choose the BuildBetter Review Sandbox organization during OAuth.
5. Run the hero prompts from `hero-prompts.md`.
6. Compare the final answer and tool path against `eval-plan.md` and `hero-cases.json`.

## Private review setup

- Reviewer username/password or SSO access must be supplied outside git.
- Select the existing verified OpenAI organization, project, and developer identity before uploading the new version.
- Provide a dedicated account that works without MFA approval, one-time codes, magic links, or private-network access.
- Run the five positive and three negative manifest cases using that account and capture an accessible walkthrough URL.
- Upload the generated ZIP, complete the MCP scan, resolve required findings, and submit the selected draft for review. Auth details are entered separately in Review details, never in the ZIP.

