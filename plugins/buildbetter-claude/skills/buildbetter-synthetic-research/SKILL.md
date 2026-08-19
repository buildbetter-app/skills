---
name: buildbetter-synthetic-research
description: Run BuildBetter synthetic-persona research with bounded source previews, explicit credit confirmation, panels, studies, responses, and chat follow-up. Use when the user asks to create or update synthetic personas, generate persona companies, test concepts or creative with a persona panel, or explore hypotheses before real-customer research.
---

# BuildBetter Synthetic Research

## Safety Contract

Synthetic research generates hypotheses; it does not prove real customer demand, prevalence, willingness to pay, or causal impact. Search organization skills with list-skills and get-skill first. Confirm every metered operation from its returned estimate, and obtain separate exact approval before non-disposable deletion.

If any named tool is absent from the registered MCP inventory, report that the workflow is not available in this environment. Do not approximate a missing mutation through run-query.

## Workflow

1. Inspect before creating: list-personas, list-persona-companies, list-persona-panels, and list-persona-type-templates.
2. Define the research decision, real evidence already available, target segment, source boundary, unknowns, and what synthetic output may and may not establish.
3. Use preview-persona-generation to inspect source counts and sample evidence without consuming credits. Tighten the source filter when it mixes incompatible segments.
4. For AI-generating tools, call once to receive the estimate. When requiresConfirmation is true, read back estimatedCredits and scope, obtain approval, then rerun the exact call with its confirmationToken.
5. Create or update personas and companies only after reviewing drafts. Preserve source evidence, assumptions, and unsupported fields.
6. Create a focused panel with deliberate variation. Use replica-set respondents only when the study benefits from within-persona variation.
7. Create a persona test run with a clear question, options or stimuli, and decision rule. Poll the returned operation when asynchronous, then inspect get-persona-test-run and list-persona-test-run-responses.
8. Use persona chats for follow-up exploration, not to manufacture consensus. Preserve thread and message IDs.
9. Synthesize findings as hypotheses, disagreements, segment effects, and real-customer validation needs.

## Tool Routes

- Persona profile: preview-persona-generation -> generate-persona-profile -> create-persona.
- Persona types: list-persona-type-templates -> recommend-persona-type-templates or generate-persona-type-concepts -> bulk-create-personas-from-person-types, bulk-create-personas-from-recommendations, or bulk-create-personas-from-generated-concepts.
- Companies: list-persona-companies -> suggest-persona-company-briefs -> generate-persona-companies.
- Study: create-persona-panel -> create-persona-test-run -> get-persona-test-run -> list-persona-test-run-responses.
- Chat: create-persona-chat -> send-persona-chat-message -> list-persona-chat-messages.

## Output

Report the research question, source preview, personas and panel IDs, exact estimated and consumed credits when returned, run and operation IDs, response coverage, findings, disagreement, caveats, and the next real-evidence test.

## Approval Boundaries

The user's explicit request for a bounded synthetic study authorizes reviewed draft creation and the agreed test scope, subject to the MCP credit confirmation. It does not authorize deleting reusable personas or panels, expanding the credit budget, contacting customers, or presenting synthetic output as customer evidence.
