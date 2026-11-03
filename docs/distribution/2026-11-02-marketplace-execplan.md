# Prepare MCP marketplace distribution

## Purpose / Big Picture

Deliver the [distribution spec](2026-11-02-marketplace-spec.md) as one reviewed
source change in the public skills repo.

### Work Plan

Reuse the existing Grok generator, add missing manifests and provider copy, test
real archives and schema boundaries, then open the PR. No store submission occurs.

### Milestone Table of Contents

- [Provider requirements](#provider-requirements)
- [Distribution artifacts](#distribution-artifacts)
- [Validation and delivery](#validation-and-delivery)

## Progress

- [x] (2026-11-02) Verified merged Grok/Cursor package and primary provider docs.
- [x] (2026-11-02) Defined acceptance and wrote archive regression tests first.
- [x] (2026-11-02) Implement manifests, shared metadata, guide and builder.
- [x] (2026-11-02) Validate schemas, archives, existing tests and generation drift.
- [x] (2026-11-02) Prepare PR source and record remaining external gates.
- [x] (2026-11-02) Complete independent public-package and provider reviews;
  prepare the application packet and correct Google's example prompts.
- [x] (2026-11-02) Build separate application folders for all eight providers,
  add reviewer instructions, verified public PNG artwork and file checksums.

## Surprises & Discoveries

The Grok/Cursor package already exists. Google requires preview admission and a
reviewed schema snapshot. Microsoft supports dynamic per-user MCP discovery.
AWS requires seller/subscription integration even for marketplace preparation.
The official Microsoft app schema caught an overlength short description. A
regression assertion reproduced it before the description was shortened.

## Decision Log

Use the existing production MCP and generated public skills. Keep eight provider
routes in one sourced guide. Build complete Microsoft app manifests only when
registered IDs and valid icons are supplied. Do not change shared OAuth/catalogs
without a reproduced client compatibility failure.

## Outcomes & Retrospective

Implemented a reproducible public kit, remote-only Registry entry, shared/Google
listing copy and a complete Microsoft 365 app builder. Reused the existing nine
Grok/Cursor workflows. The public archive also carries the repository license.
All 139 repository tests passed; the generated Grok package matched its maintained
sources. Official JSON schemas passed for the Registry entry, Microsoft v2.4
plugin, v1.6 agent and v1.22 application manifest. Microsoft validation used
synthetic IDs and icons, establishing packaging only. Privacy and terms URLs
returned HTTP 200 at their configured URLs.
Two independent reviews found no material security or provider-contract issue.
`distribution/APPLICATIONS.md` supplies copy-ready values, public OAuth discovery,
application routes and specific missing inputs without storing review credentials.
The `--submissions` ZIP contains eight copy-ready form drafts and applicable
attachments. Its 70 files include public 512px/192px app icons, maintained
Grok/Cursor packages, reviewer instructions and checksums. Null fields identify
real publisher/registration inputs; the Microsoft outline icon remains required.

This source change is for PR review. No provider submission, agreement,
installed-host acceptance, merge, deployment or public listing is claimed.
External onboarding, registered Microsoft IDs and publisher assets, Google domain
verification/compatibility, and native-host OAuth QA remain the gates listed in
`distribution/README.md`.

## Provider requirements

`distribution/README.md` records verified routes and gates. Social-post connector
counts and automatic syndication are not acceptance evidence.

## Distribution artifacts

Add `server.json`, `distribution/` and `scripts/build_mcp_distribution.py`.
Keep maintained skill copies unchanged. Validate all inputs before writing output.

## Validation and delivery

Run `python3 -m pytest tests/ -q`, `python3 scripts/build_grok_plugin.py --check`,
and `python3 scripts/build_mcp_distribution.py`. Read back and compare archives;
validate provider schemas. Commit and open the PR. Hosted tests run on that PR.

## Recovery

Writes are atomic and do not modify client settings. Preserve a previous artifact
on invalid input. Retry with the same source and publisher inputs. Keep live-host
QA evidence and secrets outside the public kit.
