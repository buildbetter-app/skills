# BuildBetter 0.6.1 update preparation

Prepared package source, not a submission or approval receipt.

## Listing

Display name: BuildBetter. Category: Productivity. Subtitle: Research customer feedback.

The listing highlights recurring pain points, feature requests, onboarding friction, churn concerns and evidence-backed prioritization. The agent retrieves, filters, selects representative evidence and synthesizes in chat. Evidence browsing and compact job-progress views are optional. Support conversations, surveys, recordings, signals and Knowledge are accessible only through the connected workspace's permissions; analytics requires connected PostHog or Amplitude accounts.

The maintained manifest contains the complete listing, public links, icons, three starter prompts and positive/negative reviewer cases. Version 0.6.1 includes the chat-first guidance and optional progress description. No broad accuracy or guaranteed recommendation claim is made.

## Reproducible upload

For the existing OpenAI 2.0.0 draft, run `python3 scripts/build_plugin_submission.py --submission-version 2.0.0 --output artifacts/buildbetter-2.0.0-openai.zip`, inspect both manifest versions in the ZIP, and preserve its hash. The explicit override changes only the artifact version; the maintained Codex install source stays 0.6.1. Omitting the override produces a 0.6.1 ZIP. Upload to the existing BuildBetter plugin identity at https://platform.openai.com/plugins; do not create a duplicate listing or change its server URL. Package changes require their own checks and review outcome.

Hosted MCP updates are evaluated separately through server scans. Rescan after deploying the production backend; staging availability does not establish production tool approval. Preserve existing approved schemas until new definitions are available. Normal server updates should not require reconnecting unchanged OAuth clients, but host acceptance must be verified rather than assumed.

## Remaining external gates

- Verify the current published version and owning developer identity in the dashboard.
- Confirm the final production backend revision and feature availability; do not ship the staging endpoint in the public ZIP.
- Execute the manifest cases using a dedicated sample-data reviewer account, with no private-network or interactive MFA requirement.
- Record actual host component rendering and Events delivery separately from ordinary tool success.
- Provide the walkthrough URL and private reviewer credentials through the dashboard, outside the repository and ZIP.
- Resolve package/skill/MCP scan findings; complete the applicable attestations and record the submission receipt.

The package is prepared for this process; those checks are not marked passed by creating a ZIP. [OpenAI submission and update rules](https://developers.openai.com/plugins/deploy/submission).

## Claude compatibility and distribution

The maintained Claude Code package candidate is 0.6.1. Its bundled public skills change in this update: customer-voice, research, onboarding and survey descriptions reflect the focused use cases, and all focused workflows treat organization-skill discovery as optional reference data. The Claude copies are synchronized with the maintained Codex workflows. Its MCP configuration and server identity are unchanged. The new Grok package is a separate distribution; it does not replace the Claude package or alter OAuth clients, tokens, scopes, SAML or workspace permissions.

Existing remote connectors continue to use the same server. A version bump in this repository does not publish a Claude directory update. Anthropic states that existing directory skills, connectors and plugins need no changes for the new directory system. Do not submit a duplicate connector just for this update. Distribute these changed bundled skills through the owning publisher's existing Claude plugin listing and applicable update/review flow; do not skip the package update because the remote connector URL is unchanged. Verify the live package version first: if 0.6.1 has already been distributed, increment the Claude package version before publishing the changed skills. After publication, update a client installation and verify that its installed focused skills contain the new descriptions and optional-discovery guidance. Git merge and successful package tests do not establish that directory or client installations received the update.

Source: [Anthropic directory submission announcement](https://claude.com/blog/build-plugins-for-claude). Claude supports MCP Apps; support and actual rendering must still be verified in Claude. Do not infer Events support or Claude host acceptance from successful MCP calls in another host.
