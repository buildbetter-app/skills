---
name: buildbetter-survey-research
description: Design, draft, test, launch, and analyze BuildBetter native surveys with evidence-backed questions, audience controls, delivery safeguards, and response synthesis. Use when the user asks to create a survey, add recipients, schedule or activate delivery, configure an in-app intercept, inspect responses, or connect survey results to a BuildBetter View.
---

# BuildBetter Survey Research

## Safety Contract

Search organization skills with list-skills and get-skill first. Treat survey creation, audience changes, activation, scheduling, invitations, respondent links, intercept configuration, settings, View connections, and deletion as mutations. Never activate, schedule, send, resend, or attach an audience without explicit approval and a readback of survey, recipients, channel, and timing.

If any named tool is absent from the registered MCP inventory, report that limitation. Do not use run-query to imitate survey mutations.

## Workflow

1. Define the research decision, target population, evidence gap, sample limitations, analysis plan, and action each result may trigger.
2. Inspect existing surveys with list-surveys and get-survey. Reuse or update only when the user intends to change that exact survey.
3. Draft questions manually or with suggest-survey-questions. Remove leading, double-barreled, unnecessary, or non-actionable questions. Put sensitive questions last and make them optional when possible.
4. Create-survey in an inactive, audience-free state unless the user explicitly approved a bounded audience and activation in the same request.
5. Review delivery copy, subject, preview text, branding, questions, required fields, consent, thank-you state, View connections, and target channel.
6. Add recipients only after showing the exact count and identity source. Active email surveys may queue invitations immediately, so keep the survey inactive during audience assembly.
7. Use send-survey-test-email only after approval of the exact preview address. A test email is a real external message.
8. For a launch, read back channel, audience count, exclusions, timing, and survey state. Then use update-survey for activation or schedule-survey for one future launch. Verify with get-survey and list-survey-schedules.
9. For in-app delivery, list-feedback-widgets before configure-survey-intercept. Target only verified recipient identities; review state with list-survey-intercepts.
10. Analyze through list-survey-responses and get-survey-response. Separate response count, delivery state, answer evidence, AI follow-up text, nonresponse, and sample bias.

## Tool Routes

- Draft: suggest-survey-questions -> create-survey with activation off -> get-survey.
- Questions and design: replace-survey-questions -> customize-survey -> get-survey.
- Audience and launch: add-survey-recipients -> send-survey-test-email -> update-survey or schedule-survey -> list-survey-schedules.
- In-app: list-feedback-widgets -> configure-survey-intercept -> list-survey-intercepts.
- Results: list-survey-responses -> get-survey-response -> connect-survey-to-view when explicitly approved.

## Output

Report survey ID and state, research goal, question and audience review, channel, exact approved recipient scope, schedule or activation state, test evidence, response coverage, findings, bias, and next decision. Distinguish drafted, tested, scheduled, active, delivered, responded, and analyzed.
