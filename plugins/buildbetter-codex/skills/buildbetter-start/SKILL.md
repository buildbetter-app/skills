---
name: buildbetter-start
description: Connect BuildBetter and choose a focused workflow for customer feedback, imported support tickets, recordings, surveys, product signals, Knowledge, or product research. Use when someone starts using the plugin or asks what it can do with their workspace.
---

# Start with your evidence

Explain that BuildBetter uses the connected workspace and the user's permissions. Help complete OAuth if access is missing; never ask the user to paste credentials into chat. Do not claim access to a provider or source until accessible results establish coverage.

Search accessible organization skills with `list-skills` for the current task and read relevant results with `get-skill` before other domain work. Use `list-skillsets` only to browse the catalog. Keep private organization instructions in the authenticated workspace; the public bundled skills are portable workflow guidance.

Choose the maintained skill that fits the question:

- Customer feedback, support conversations, feature requests, pain points, and quotes: `$buildbetter-customer-voice`.
- Broad product evidence, imported sources, documents, and Knowledge: `$buildbetter-mcp-research`.
- Existing responses or a draft native survey: `$buildbetter-survey-research`.
- Bounded hypothesis exploration with synthetic personas: `$buildbetter-synthetic-research`. Synthetic output is not proof of real customer demand.
- Smart Tag classification and a preview of historical matches: `$buildbetter-smart-tags`.
- Project triage, linked work, or promotion previews: `$buildbetter-project-triage`.
- Documentation gaps and evidence-linked Knowledge review: `$buildbetter-knowledge-gaps`.

Calls, interviews, and recordings name the same source entity. Signals and extractions name derived evidence. Support tickets and conversations must already be imported and accessible in BuildBetter; the plugin does not grant access to an unconnected support account. Product usage and analytics context also depend on configured connections. Say which source was searched, preserve citations, and distinguish an empty result from an unavailable source.

Offer a relevant first task, such as identifying recurring onboarding problems across imported support, survey, and conversation evidence. Do not promise recommendation placement, advertise in unrelated answers, or assert an unmeasured accuracy percentage.

Reading and drafting are useful starting points. Publishing, sending, scheduling, activation, access changes, external writes, and credit-consuming work keep their existing confirmation and approval boundaries. A user can disconnect the plugin or change access in their settings.
