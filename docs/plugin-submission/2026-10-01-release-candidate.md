# BuildBetter 0.6.0 submission candidate

The package describes the proposed prerelease source changes across feedback, imported
support, native surveys, recordings, analytics, signals, documents, and
Knowledge. It bundles maintained public skills; private organization skills
remain permissioned at runtime. Metadata/skill changes require a new ZIP/version.
OpenAI controls recommendations and ranking; the package promises no placement
or unmeasured accuracy percentage.

## Progressive PRs

| Slice | PR | Evidence |
|---|---|---|
| Portable package/discovery | [skills #11](https://github.com/buildbetter-app/skills/pull/11) | 104 local tests and hosted Python 3.11–3.13 checks passed for 0.5.0 |
| Connected analytics and task metadata | [#7078](https://github.com/buildbetter-app/buildbetter/pull/7078) | Provider HTTP cases, MCP boundary and committed-source quick compile passed |
| Interactive evidence browser | [#7080](https://github.com/buildbetter-app/buildbetter/pull/7080) | Four browser interaction cases, guarded resource/catalog HTTP case and quick compile passed |
| Stateless MCP 2.0 transport | [#7081](https://github.com/buildbetter-app/buildbetter/pull/7081) | Six authenticated HTTP cases, runtime build and quick compile passed |
| Durable Events | [#7082](https://github.com/buildbetter-app/buildbetter/pull/7082) | Eight Postgres/TLS delivery cases, seven modern/Events HTTP cases, four workflow cases, both worker composition checks and quick compile passed |
| Chat-first interactions and optional progress | [#7178](https://github.com/buildbetter-app/buildbetter/pull/7178) | Owner-scoped `get-job` and optional `show-job-progress`; combined source verification passed, native rendering remains a separate QA gate |

The backend merge order is #7078, #7080, #7081, #7082, #7178. Each successor
depends on its predecessor; #7178 includes the Events layer from #7082. After
merging a parent, retarget its successor to `main` before merging that successor.
Combined candidate `418a144d869e2e2cdce0a9f4e1d9f840b504ebfd` passed all 2,530
verification tasks on BuildBot3 (1,208 executed, 1,322 restored from cache) against pinned main
`3bcc3992d1fe6409992eccec7b2afba0b62c017d` on October 3. All five individual
heads also passed compile/typecheck. Hosted backend verification remains
paused/skipped; deployed behavior and native rendering remain unverified. The backend PRs and this package require
separate merge/deployment authorization before public submission.

The final analytics correction preserves supported bulk PostHog identity pages
with a bounded 16 MiB default response budget. MCP queries retain their explicit
1 MiB response budget and 500-row cap. The real HTTP regression for a synthetic
10,000-row identity page and the MCP integration suite executed successfully in
the combined run.

## Candidate behavior

- Discover configured PostHog/Amplitude projects, execute bounded read-only
  queries, and read existing insights with source/project/timezone/truncation context.
- Answer routine evidence questions in chat. Open the optional evidence
  component when visual browsing and curation are explicitly requested.
- Read an existing job receipt in chat, with an optional compact progress card.
  Neither receipt tool starts processing or spends credits.
- In an Events-capable client and enabled workspace, monitor `signal.created`,
  `recording.completed`, or one survey's `survey.response.submitted` updates.
  Subscription grants expire; delivery rechecks permissions and supports unsubscribe.
- Continue using native survey, synthetic research, Smart Tag, project-triage,
  Knowledge-gap and customer-voice skills with their existing approval boundaries.

Analytics changes, custom signals, and Knowledge updates have no Events producer
in this version. Notifications carry public IDs and concise context rather than
source bodies or instructions. Synthetic research remains separate from real
customer evidence.

## Proof and remaining gates

The ZIP builder's packaging tests exercise the actual archive boundary and
verify reproducibility, path safety and excluded credentials/hooks/app references.
The public skills' routing and parity checks cover the maintained package source.
The release PR's verification comment records the 0.6.0 ZIP hash and local/hosted
results; the earlier 0.5.0 hash is not this candidate's hash.

The manifest contains eight authored positive scenarios and three negatives.
They are not executed ChatGPT transcripts. Browser screenshots in #7080 prove
the component harness using synthetic fixtures, including escaped malicious
source text; they are not production or live ChatGPT screenshots.

At the latest publisher readback, OpenAI required sign-in. The owning developer
identity/organization/project, dedicated reviewer account, deployed endpoint,
executed ChatGPT cases, real walkthrough URL, MCP scan and final submission
receipt remain unverified. Follow [the checklist](submission-checklist.md) and
[review account requirements](review-account.md); keep credentials outside git
and the ZIP.

## Review correction status

The backend correction batch is published, and its review threads were resolved
at readback. The current BuildBot3 receipt above verifies the combined candidate;
earlier browser screenshots still describe their own source and host. Deployed
contract checks and actual ChatGPT/Codex rendering remain separate acceptance
gates. The reviewer runs all eight positive manifest cases and three negatives,
with a separate authorized operator producing a future event. The sixteen Codex
hero cases in `evals/plugin-submission/hero-cases.json` are a separate suite; run
their fixture setup and substitute verified values before sending their prompts.

Current local package: `artifacts/buildbetter-0.6.0.zip`, 25 entries. SHA256:
`61e17ce570de047d8f1e4a813954aec79c31481c642c335c5b0caa875f680faa`.
All 108 Python tests passed for this packaging correction. The artifact stays
local and is not an OpenAI submission receipt.

### Reproducible QA setup correction (2026-10-02)

BB-HERO-011 and BB-HERO-013 now define setup steps and explicit fixture substitutions. Capture accessible recording/job identities and their original receipts privately; blocked setup must not trigger invented IDs, processing or credit spending. The additions audit now includes both progress tools and their optional native component. Rebuilt archive SHA256: `61e17ce570de047d8f1e4a813954aec79c31481c642c335c5b0caa875f680faa`. Archive identity is separate from deployed/native acceptance and submission.
