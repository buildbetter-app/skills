# Plugin Eval Plan

The eval cases live in `evals/plugin-submission/hero-cases.json`. They are intentionally tool-path oriented so they can be run manually in Codex today and automated later with a transcript runner.

## Case Fields

Each case includes:

- `id`: stable case ID.
- `plugin`: expected plugin or `none` for negative cases.
- `prompt`: exact user prompt.
- `expected_output`: representative successful response.
- `required_facts`: facts or behavior that must appear in the final answer.
- `expected_tool_path`: required tool or command sequence.
- `safety_behavior`: confirmation, auth, and side-effect expectations.
- `fixture_state`: review tenant or local state needed for the case.
- `grading_criteria`: pass/fail rules.

## Manual Run Loop

1. Install the hosted marketplace:

   ```bash
   codex plugin marketplace add buildbetter-app/skills --ref main --sparse .agents/plugins --sparse plugins/skills --sparse plugins/buildbetter-codex
   codex plugin add buildbetter@buildbetter
   ```

2. Start a fresh Codex thread and connect BuildBetter OAuth when prompted.
3. Run one case prompt at a time against the review tenant.
4. Capture:
   - case ID
   - prompt
   - tool calls and arguments
   - final answer
   - pass/fail
   - transcript link or local transcript export path
   - latency/auth/discovery notes
5. Record results in `docs/plugin-submission/transcripts/<case-id>.md`.

## Grading Rules

Use the lightest verifier that works:

- Exact or contains checks for IDs, statuses, counts, and command names.
- Structured rubric checks for summaries and recommendation quality.
- LLM judge only for cases with multiple valid answers, and only with the case rubric.

Fail a run if:

- Codex calls BuildBetter for the negative case.
- Codex writes, repairs hooks, or sends feedback before user confirmation.
- Codex omits required stable IDs when the tool response contains them.
- Codex uses `run-query` before a domain tool can express the request.
- Codex returns broad raw records instead of a concise synthesis.

## Automation Backlog

The current package includes structured cases and manual capture. The next automation step is a small runner that:

1. reads `hero-cases.json`,
2. sends each prompt through a Codex/plugin test harness,
3. records tool calls and final answers,
4. grades with field checks plus optional rubric checks,
5. writes a transcript markdown file per case.

