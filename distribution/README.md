# BuildBetter MCP distribution

Prepared November 2, 2026. These files prepare submissions; they do not establish
store approval, installation, or native-client OAuth acceptance. The Grok/Cursor
plugin already exists from [skills #14](https://github.com/buildbetter-app/skills/pull/14).
All channels reuse `https://mcp.buildbetter.app` with per-user OAuth. A BuildBetter
account and access to an authorized workspace are required.

Use the [application packet](APPLICATIONS.md) for submission fields, public OAuth
details, reviewer requirements and the remaining account-specific inputs.

## Build and install

From the repository root:

```sh
python3 scripts/build_grok_plugin.py --check
python3 scripts/build_mcp_distribution.py --output artifacts/mcp-distribution.zip
python3 scripts/build_mcp_distribution.py --submissions --output artifacts/buildbetter-submissions.zip
python3 -m pytest tests/test_mcp_distribution.py tests/test_grok_plugin.py -q
```

The reproducible kit contains the portable Grok/Cursor plugin, Cursor marketplace
entry, Registry manifest, shared listing copy, Google form copy and Microsoft
templates. It excludes the private/CLI packages, hooks, tokens and local host
settings. The Google JSON is copy for console fields, not a Google upload schema.
The Microsoft template is deliberately unconfigured; it is not an installable app.

The `--submissions` archive groups copy-ready `FORM.json` drafts and actual
attachments into eight platform folders, with reviewer instructions and file
checksums. These forms are preparation records, not provider upload schemas.
Unknown owner/registration fields stay null and each draft lists missing inputs.
It includes the production app's 512px and 192px PNG icons; see their
[source and hashes](assets/README.md). Microsoft still needs a 32px white outline.

For **grok.com**, open [Connectors](https://grok.com/connectors), choose New
Connector → Custom, enter the production MCP URL and complete OAuth. This does
not create a public catalog listing or install packaged skills. For **Grok
Build**, load the existing plugin directory with the official client's
`--plugin-dir` option. For **Grok Bot/Cursor**, follow
[the package installation and QA guide](../plugins/buildbetter-grok/README.md).

## Publication routes and remaining gates

| Channel | Prepared artifact | Required next steps | Primary reference |
| --- | --- | --- | --- |
| Official MCP Registry | Root `server.json`, remote-only entry `io.github.buildbetter-app/buildbetter` | Check existing entries, prove namespace ownership, authorize publication, publish and read back the exact version | [Remote servers](https://modelcontextprotocol.io/registry/remote-servers) |
| Grok | Existing portable plugin and custom MCP setup | Native-host sign-in/tool-call QA; confirm xAI catalog submission route. Custom connections and public catalog distribution are separate | [Connectors](https://docs.x.ai/grok/connectors), [plugins](https://docs.x.ai/build/features/skills-plugins-marketplaces) |
| Cursor Marketplace | `.cursor-plugin/marketplace.json`, `plugins/buildbetter-grok` | Native installation QA, submit public repo and plugin path at [Publish](https://cursor.com/marketplace/publish), await review | [Submission requirements](https://cursor.com/docs/reference/plugins) |
| Google Connected Apps | `google/listing.json`, shared endpoint | Preview admission at [Connected Console](https://connected.google.com), owner-accepted terms, domain verification, 512px icon, authenticated compatibility and seeded review access | [Prerequisites](https://developers.google.com/connected-apps/gpc/prerequisites), [registration](https://developers.google.com/connected-apps/gpc/perform-the-steps) |
| Meta Muse / Meta AI | Shared listing copy and permissioned MCP | Confirm product-specific admission and connector contract through the official early-access route; do not assume the Meta AI preview is Muse catalog admission | [Meta AI Connectors](https://dev.meta.ai/products/connectors), [developer FAQ](https://developers.meta.com/wearables/faq/) |
| Microsoft 365 Agent Store | Declarative agent, OAuth MCP wrapper and app ZIP builder | Registered app/vault IDs, publisher icons, tenant sideload QA, publisher verification, Partner Center review | [Dynamic MCP discovery](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/plugin-dynamic-tool-discovery), [Agent Store](https://learn.microsoft.com/en-us/microsoft-365/copilot/copilot-agent-store) |
| Salesforce AgentExchange | Shared listing and MCP setup/QA cases | Partner enrollment, supported solution registration and external-MCP auth, Agentforce QA, applicable security review and publication | [Listing guide](https://developer.salesforce.com/docs/platform/isvforce/guide/appexchange-publish-listings.html), [security review](https://developer.salesforce.com/docs/platform/isvforce/guide/security-review-how-it-works.html) |
| AWS Marketplace AI Agents & Tools | Shared listing and usage instructions | Seller account, commercial choice, buyer registration/fulfillment integration and cancellation handling, seller validation/review | [API-based MCP products](https://docs.aws.amazon.com/marketplace/latest/userguide/integrating-api-ai-agents-tools.html) |

Connector counts in the original social post are not verified and do not determine
eligibility. Registry publication can feed other directories, but Glama,
PulseMCP, and mcp.directory each control ingestion, review and placement; verify
each separately. A free Marketplace listing does not make paid BuildBetter access
free, and no paid pricing/contract change is configured here.

## Official MCP Registry

The Registry hosts discovery metadata; no npm package or duplicate server is
needed for this remote-only entry. Version `0.1.0` is the Registry entry's own
version, independent from the existing plugin and backend release versions.

Before publishing, check for an existing BuildBetter entry to avoid duplicate
identity. Follow the [publisher authentication guide](https://modelcontextprotocol.io/registry/authentication)
to authenticate with an account authorized for the `buildbetter-app` namespace.
After publication is authorized, run the official `mcp-publisher login github`
and `mcp-publisher publish` from the repository root. Record the resulting name,
version and Registry readback. This kit never invokes publication or login.

## Google compatibility

Google supports Streamable HTTP and currently MCP through `2025-11-25`. It
snapshots the tools for each reviewed app version. Its naming guidance specifies
snake_case or camelCase; BuildBetter's established catalog has hyphenated names.
Verify the authenticated catalog in Gemini Developer Mode before submission.
Do not rename/remove shared tools or break existing workflows to satisfy a host.
If Google requires adaptation, implement a separately versioned provider surface
and verify its OAuth resource/audience and execution permissions independently.

See [integration standards](https://developers.google.com/connected-apps/mcp/server-optimization).
Google also requires a no-redirect verification file at
`/.well-known/google-connected-apps`, a seeded test account, a 512×512 PNG/JPEG
under 1 MB and reviewer instructions. The existing Claude icon is 1024px and is
not represented as satisfying Google's icon requirement. A program agreement and
domain challenge cannot be invented or completed by this source package.

## Microsoft 365 app ZIP

Create the application and OAuth configuration in Microsoft's Developer Portal.
Register BuildBetter authorization endpoints and Microsoft's redirect URI using
the provider's instructions. The vault reference ID is a non-secret configuration
identifier; never supply an access token, password or client secret to the builder.

```sh
python3 scripts/build_mcp_distribution.py --copilot \
  --copilot-app-id "$BB_COPILOT_APP_ID" \
  --copilot-oauth-reference-id "$BB_COPILOT_OAUTH_REFERENCE_ID" \
  --copilot-color-icon publisher-assets/color-192.png \
  --copilot-outline-icon publisher-assets/outline-32.png \
  --output artifacts/buildbetter-copilot.zip
```

Use the registered app's actual ID, a 192×192 color PNG and a 32×32 white outline
PNG with a transparent background. The builder verifies file structure and
dimensions; visual branding and outline appearance require human/native review.
The ZIP references `declarativeAgent.json` → `ai-plugin.json` → the production MCP.
Dynamic discovery preserves workspace-specific tools and execution authorization;
it does not bypass store/runtime validation. Use tenant policy to limit pilot
access. Do not claim a fixture package is a registered or accepted agent.

Follow [OAuth configuration](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/plugin-authentication-oauth)
and [app publishing](https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/deploy-and-publish/appsource/publish).

## Read-only host QA and submission evidence

For every supported native host, record client version, installed package/entry
version, endpoint, test-workspace identity and timestamp. Keep customer content
and reviewer credentials out of this public repository.

1. Connect with a dedicated test user; verify sign-in and initial tool discovery.
2. Ask for recent onboarding complaints, verify quotations against original
   accessible sources, and record actual pagination and coverage.
3. Compare survey responses; compare usage only if an analytics source is really
   connected. Missing sources must be explicit gaps.
4. Attempt access to unavailable/foreign-workspace evidence and verify denial.
5. Reconnect/refresh, then revoke access and verify cached tool calls are denied.
6. Ask for a Smart Tag draft without saving or processing it. Existing write,
   publication, messaging and credit-use confirmation remains required.

Keep separate evidence for OAuth, tool execution, optional UI, Events, store
submission, approval and installation. Normal MCP compatibility does not prove
that a particular host supports our HTML bridge or Events. An HTTP 401 without
credentials is expected and does not prove authenticated scanner acceptance.

Shared usage instructions: clients send JSON-RPC `initialize`, `tools/list` and
`tools/call` to the HTTPS endpoint; tool schemas are authoritative. On 401 use
the host's OAuth reconnect flow; on 403 verify workspace access; on 429 honor
retry hints/backoff; surface server errors without fabricating results. No API
keys in URLs or shared service-account tokens are part of this integration.
