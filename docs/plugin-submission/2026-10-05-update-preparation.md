# BuildBetter 0.6.1 update preparation

Prepared package source, not a submission or approval receipt.

## Listing

Display name: BuildBetter. Category: Productivity. Subtitle: Turn feedback into decisions.

The listing now states that the agent retrieves, filters and cites evidence in chat. Evidence browsing and compact job-progress views are optional. Support conversations, surveys, recordings, signals and Knowledge are accessible only through the connected workspace's permissions; analytics requires connected PostHog or Amplitude accounts.

The maintained manifest contains the complete listing, public links, icons, three starter prompts and positive/negative reviewer cases. Version 0.6.1 includes the chat-first guidance and optional progress description. No broad accuracy or guaranteed recommendation claim is made.

## Reproducible upload

Run `python3 scripts/build_plugin_submission.py --output artifacts/buildbetter-0.6.1-openai.zip`, inspect the ZIP, and preserve its hash. Upload to the existing BuildBetter plugin identity at https://platform.openai.com/plugins; do not create a duplicate listing or change its server URL. Package changes require their own checks and review outcome.

Hosted MCP updates are evaluated separately through server scans. Rescan after deploying the production backend; staging availability does not establish production tool approval. Preserve existing approved schemas until new definitions are available. Normal server updates should not require reconnecting unchanged OAuth clients, but host acceptance must be verified rather than assumed.

## Remaining external gates

- Verify the current published version and owning developer identity in the dashboard.
- Confirm the final production backend revision and feature availability; do not ship the staging endpoint in the public ZIP.
- Execute the manifest cases using a dedicated sample-data reviewer account, with no private-network or interactive MFA requirement.
- Record actual host component rendering and Events delivery separately from ordinary tool success.
- Provide the walkthrough URL and private reviewer credentials through the dashboard, outside the repository and ZIP.
- Resolve package/skill/MCP scan findings; complete the applicable attestations and record the submission receipt.

The package is prepared for this process; those checks are not marked passed by creating a ZIP. [OpenAI submission and update rules](https://developers.openai.com/plugins/deploy/submission).
