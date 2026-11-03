# Distribute the existing BuildBetter MCP

## Outcome and scope

Build a reproducible, credential-free kit for the eight requested distribution
channels. Reuse the existing Grok/Cursor package merged in skills #14. Add a
remote-only MCP Registry entry, shared listing copy, Google form preparation,
and a Microsoft 365 declarative-agent wrapper with a complete ZIP builder.

This implementation changes no backend, tools, prompts, permission checks,
GraphQL compatibility, credentials or deployed endpoints. All installable
configurations use the production MCP and per-user OAuth. No mandatory workspace
skill loading, credential-reading helpers or installation hooks are added.

The builder must require real Microsoft application and OAuth vault IDs plus
192px/32px icons before producing a Microsoft app. It must not invent IDs or
fall back to anonymous authentication. Dynamic MCP discovery preserves the
server's permissioned tool surface. Provider acceptance requires native-host QA.

## External boundaries

Google preview access, domain verification, fixed reviewed schemas and protocol
compatibility remain explicit gates. Meta product/catalog admission requires
confirmation. Salesforce and AWS require partner/seller onboarding and applicable
integration/review. MCP Registry publication does not guarantee downstream listing.
Store agreements, submissions, paid seller services, identity changes, merge and
deployment are outside this source implementation request.

## Acceptance

Build and read back deterministic kit and Microsoft ZIPs. Validate the Registry,
Microsoft plugin, agent and app JSON schemas. Reject incomplete registration,
malformed icons and symlinks without replacing a previous archive. Run existing
public-package tests and generated-Grok drift checks, then open a PR. Fixture IDs
and icons prove packaging only; they must never be represented as a live install.

No implementation decision is unresolved. The exact provider gates and primary
sources live in `distribution/README.md`.
