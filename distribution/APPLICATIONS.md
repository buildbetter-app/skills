# BuildBetter marketplace application packet

Prepared November 2, 2026. These are public application materials, not submission
receipts. Use the reviewed, merged revision when applying. The existing
Grok/Cursor package is already on `main`; the new Registry/Microsoft materials
must land before citing their default-branch URLs in an application.

Build the prepared folders with:

```sh
python3 scripts/build_mcp_distribution.py --submissions --output artifacts/buildbetter-submissions.zip
```

Each platform folder contains a copy-ready `FORM.json` and applicable attachments.
These drafts are not provider upload schemas. Required unknown fields remain
null, with a concrete `missing_inputs` list. The archive has shared reviewer
instructions and `SHA256SUMS`; no test IDs or credentials are substituted.

## Shared form values

| Field | Value |
| --- | --- |
| Product / publisher | BuildBetter |
| Website | https://buildbetter.ai |
| Public repository | https://github.com/buildbetter-app/skills |
| Plugin directory | `plugins/buildbetter-grok` |
| Support | https://github.com/buildbetter-app/skills/issues |
| Technical contact | eng@buildbetter.app |
| Privacy policy | https://docs.buildbetter.ai/pages/Legal/privacy-policy |
| Terms | https://docs.buildbetter.ai/pages/Legal/terms-of-service |
| Production MCP | https://mcp.buildbetter.app |
| Transport | Remote Streamable HTTP over HTTPS |
| Authentication | Per-user OAuth authorization code flow with PKCE S256 |
| Account requirements | BuildBetter account and an authorized workspace; existing product entitlements apply |

Use [`listing.json`](listing.json) for the canonical short description, long
description and keywords. For Google's console, use its separate
[`google/listing.json`](google/listing.json); this is form copy, not an upload
manifest. Its prompts include the required `@BuildBetter` invocations.

**Product pitch:** BuildBetter helps teams research customer feedback, support
conversations, recordings, surveys and connected product analytics. Users can
investigate recurring requests and onboarding friction, compare evidence, and
receive answers with citations and explicit coverage limits.

**Three demonstration prompts:**

- Find recurring onboarding complaints and cite representative source evidence.
- Compare survey responses about our latest release and explain search coverage.
- Find customer feature requests and verify quotations against original sources.

Available tools depend on the connected user's permissions, entitlements and data
sources. A listing does not provide free access to paid BuildBetter features.
Do not promise platform-specific UI, Events or background automation until that
host's native tests establish support.

## Public OAuth information

Public discovery returned these values on November 2, 2026:

| Field | Value |
| --- | --- |
| Protected-resource metadata | https://mcp.buildbetter.app/.well-known/oauth-protected-resource |
| Resource | `https://mcp.buildbetter.app` |
| Authorization server / issuer | `https://mcp.buildbetter.app/oauth` |
| Issuer metadata | https://mcp.buildbetter.app/.well-known/oauth-authorization-server/oauth |
| Authorization endpoint | https://mcp.buildbetter.app/authorize |
| Token endpoint | https://mcp.buildbetter.app/token |
| Dynamic client registration endpoint | https://mcp.buildbetter.app/register |

Refresh discovery before configuring an application. Use user-delegated
authorization, the host's documented callback and the minimum scopes required by
that integration. Do not select a service-account or password flow merely because
the issuer advertises it. Platform registration IDs and redirect allowlists must
come from the actual provider setup; this packet does not invent them. Successful
discovery does not establish authenticated native-host acceptance.

## Platform application inventory

All public-store submissions remain unsubmitted by this change. Account access,
agreements and product-specific compatibility must be established separately.

| Platform and application entry point | Prepared materials | Concrete remaining inputs |
| --- | --- | --- |
| [Official MCP Registry](https://modelcontextprotocol.io/registry/authentication) | `server.json`: `io.github.buildbetter-app/buildbetter`, entry version `0.1.0` | Publisher GitHub device authorization for the organization namespace; check the exact name/version, publish and save a Registry readback. A bounded public search returned no BuildBetter matches on the preparation date. |
| [Cursor Marketplace](https://cursor.com/marketplace/publish) | Public repository URL, `plugins/buildbetter-grok`, root `.cursor-plugin/marketplace.json`, existing SVG logo and workflows | A real Cursor install/sign-in/tool-call transcript, sanitized screenshots if requested, publisher login and the submitted revision. Native QA has not been recorded for this application. |
| [Grok Connectors](https://grok.com/connectors) | HTTPS MCP URL, existing portable plugin and product pitch | Official-client OAuth/tool-call QA; an organization admin for Business/Enterprise provisioning; confirmation of xAI's public-catalog admission route. The documented custom-connector setup does not submit a public listing. |
| [Google Connected Console](https://connected.google.com) | Google description, capabilities, example prompts, legal URLs and OAuth discovery | Console admission; owner-accepted agreement; intentional category selection (immutable later); actual domain-verification token; 512×512 PNG/JPEG under 1 MB; reviewer account; authenticated tool sync and Gemini QA. Confirm naming/protocol compatibility before submission. |
| [Meta AI Connectors](https://dev.meta.ai/products/connectors) | Product pitch, company/contact details and MCP/OAuth description | Preview application/account access and Meta's product-specific connector contract. Confirm whether the intended Muse surface is covered; do not label Meta AI preview access as Muse catalog approval. |
| [Microsoft Partner Center](https://partner.microsoft.com/dashboard) | Declarative agent, dynamic MCP wrapper, ZIP builder, legal/support information | Microsoft 365 and Copilot publisher enrollment; supported offer type; registered app UUID and OAuth vault reference; registered redirect URI and scopes; 192×192 color and 32×32 white/transparent outline PNGs; tenant sideload/OAuth/tool-call QA; listing screenshots and reviewer access. |
| [Salesforce Partner Console](https://partners.salesforce.com) | Shared listing copy, MCP configuration, demonstration and review plan | Partner access; supported solution registration; external-MCP/Agentforce compatibility and QA; listing assets; reviewer access and applicable security review. Existing Slack distribution is not proof of this listing. |
| [AWS Marketplace Management Portal](https://aws.amazon.com/marketplace/management/) | Shared listing copy, remote MCP setup and error-handling instructions | Seller access and commercial model; supported listing assets; buyer registration/fulfillment, subscription and cancellation/access handling; seller validation. QuickLaunch requires its credential-delivery integration; the existing OAuth server alone is insufficient. |

## Meta early-access form inputs

The current [preview form](https://dev.meta.ai/products/connectors) asks for an
individual's name and work email, company and website, role, team-size range,
industry, live API status/protocol, product description, intended Meta surfaces
and a start timeframe. The shared pitch and URLs above cover the product fields.
Use the publisher's actual role, current team size and intended start timeframe;
do not invent staffing or delivery commitments. The form's protocol choices list
REST, GraphQL and Other, so describe the existing MCP interface under Other when
applicable. Existing OpenAI/Anthropic integration source is not proof of approval
by Meta or by any new target platform.

## Assets and review access

The existing public logo is
[`buildbetter-app-icon.svg`](../plugins/buildbetter-grok/assets/buildbetter-app-icon.svg).
The bundle also includes the production app's [512px and 192px raster icons](assets/README.md)
for Google and Microsoft's color icon. Supply Microsoft's 32px white outline PNG
with transparent background separately, and verify all artwork before upload.
Test fixture icons and identifiers are never publisher assets.

Supply reviewer credentials privately through each platform's approved review
channel. Designate a stable sample workspace with synthetic evidence, working
user-delegated sign-in and the permissions needed for the chosen demonstration
cases. See the existing [review-account plan](https://github.com/buildbetter-app/skills/blob/main/docs/plugin-submission/review-account.md)
for fixture preparation. Do not copy passwords, tokens, customer data, reviewer
email addresses, private tenant IDs or screenshots containing them into git or
the public ZIP. Record actual tenant setup and native QA privately.

Capture a sanitized walkthrough covering connection, source-backed research,
pagination/coverage, cross-workspace access denial, reconnection and revocation.
Only describe the host experiences actually tested. Account creation, support
commitments, countries/languages, pricing and agreements require the publisher's
real details; they are not guessed in this packet.

## Preview-interest copy

For Grok catalog admission or Meta preview forms, adapt this unsent draft:

> BuildBetter provides a hosted, permissioned MCP server for customer research,
> support evidence, surveys and connected product analytics. We have a public
> integration package and per-user OAuth at https://mcp.buildbetter.app. We would
> like to apply for your connector program and confirm the supported publication
> route, authentication requirements and review process for our integration.

Do not attach reviewer credentials to general-interest or support requests.

## Submission order and receipts

The official Registry's interactive GitHub login currently cannot verify
organization ownership. For `io.github.buildbetter-app/buildbetter`, use the
manual **Publish MCP Registry** GitHub Actions workflow on `main`. It uses the
Registry's recommended GitHub OIDC authentication, a version-pinned publisher
with a fixed SHA-256 check, and no personal access token. Run it only when the
entry version is ready to publish, then save the Registry API readback.

After source review/merge and publication authorization, publish the Registry
entry and complete Cursor/Grok native QA first. Prepare the Google, Meta and
Microsoft applications in their owner accounts. Resolve AWS/Salesforce partner
and fulfillment requirements before representing those listings as ready.

For each actual submission, keep a private record of the provider, application
or offer ID, exact submitted source/package version, evidence links, owner,
submission date, status and next required action. Record approval and public
availability separately from submission.

Primary requirements: [Google registration](https://developers.google.com/connected-apps/gpc/perform-the-steps),
[Cursor plugin submission](https://cursor.com/docs/reference/plugins),
[Grok connectors](https://docs.x.ai/grok/connectors),
[Meta developer FAQ](https://developers.meta.com/wearables/faq/),
[Microsoft Marketplace publication](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/publish-plugin-publicly),
[Salesforce listings](https://developer.salesforce.com/docs/platform/isvforce/guide/appexchange-publish-listings.html),
[AWS integration](https://docs.aws.amazon.com/marketplace/latest/userguide/integrating-api-ai-agents-tools.html),
[Registry authentication](https://modelcontextprotocol.io/registry/authentication).
