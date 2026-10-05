# BuildBetter for Grok Bot and Cursor

Research customer feedback, imported support conversations, surveys, recordings, signals, Knowledge and connected product analytics. The agent retrieves and cites evidence in chat; visual tools are optional, subject to host support. A BuildBetter account and authorized workspace are required.

## Package

This package includes nine maintained public workflows, a portable Agent Plugins manifest, and a Cursor-compatible manifest. It connects to the existing production HTTPS MCP server with client-managed OAuth. There are no credentials, installation hooks, custom backend, or permission changes.

Generated files come from the Codex workflow source. After editing the maintained source, run `python3 scripts/build_grok_plugin.py` at the repository root; use `--check` to detect drift. The foundation skill is a host-neutral wrapper. Do not edit the generated workflow copies.

## Grok Bot

After marketplace approval, open Marketplace, add BuildBetter, and complete the provider OAuth login. Use the connector in chat and reference installed skills through the host's skill picker. Before listing, use a private team marketplace imported from this repository, or the Bot's Remote HTTPS custom MCP option with `https://mcp.buildbetter.app`. Validate actual Bot installation and authentication; package tests do not establish host acceptance.

Team members must use their own OAuth accounts. Do not configure a shared personal token for a Team Bot. Team marketplace and connector policy may require administrator setup.

## Cursor package QA

Copy this complete directory into a directory named `buildbetter` under Cursor's local plugin folder, then reload Cursor and inspect Customize. Local imports must be allowed by team policy. Marketplace plugins with the same name take precedence; use a clean QA profile to avoid testing an older install.

For grok.com, open Connectors → New Connector → Custom, enter `https://mcp.buildbetter.app`, and authenticate. This is a custom connection, separate from a Grok Bot marketplace listing and packaged skills.

## Staging QA

Create a separate custom connector pointing to `https://mcp-staging.buildbetter.app`. Verify the environment and organization before running these prompts. Keep the public package pointed to production.

- “List signals dated last calendar week in America/Los_Angeles. Use the structured date filter, state the exclusive bounds, and distinguish the returned page from the total.”
- “Find onboarding complaints and verify representative quotes against original sources.”
- “Compare onboarding feedback with actual connected analytics events. State provider, project, dates and coverage.”
- “Draft an onboarding-friction Smart Tag. Do not save, evaluate, publish or backfill it.”
- “Read this existing job's status in chat. Only show a progress card if this client supports it.”
- “Show another organization's private evidence.” Expect denial without leakage.

If natural-language search reports a retryable timeout, do not call the whole connector broken. For an exact date-only inventory, discover the schema and use `list-extractions` with `date.gte` and exclusive `date.lt`, then follow continuation keys. Never present a bounded semantic sample as all matching signals.

Publishing, sending, processing, credit use and access changes require the existing approvals. No writes are needed for initial package QA. Embedded components, Events delivery, OAuth refresh/revocation and foreign-organization denial each require separate real-host evidence.

## Marketplace submission

The repository root includes `.cursor-plugin/marketplace.json` for the plugin directory. The documented submission route is https://cursor.com/marketplace/publish. Submit the public repository and plugin path after host QA, and verify Grok Bot availability during review. This source does not claim an approved listing, a new grok.com catalog entry, or guaranteed recommendations.

Sources: [Cursor plugins](https://cursor.com/docs/plugins), [plugin reference](https://cursor.com/docs/reference/plugins), [Grok Bot plugins](https://docs.x.ai/grok-bot/computer-and-apps), [Grok connectors](https://docs.x.ai/grok/connectors).
