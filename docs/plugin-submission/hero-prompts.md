# Hero Prompts

These hero prompts are the review-facing workflows for the BuildBetter Codex plugin. They include explicit plugin invocation, implicit invocation, unclear requests that should trigger follow-up behavior, and a negative case that should not invoke BuildBetter.

## Hero Workflows

| ID | Workflow | Why it matters |
| --- | --- | --- |
| BB-HERO-001 | Find customer signals for a feature area. | Tests core product evidence retrieval and citation behavior. |
| BB-HERO-002 | Summarize a call and related signals. | Tests call search, stable IDs, and downstream `get-call` use. |
| BB-HERO-003 | Retrieve transcript evidence for a known call. | Tests large-context retrieval and transcript precondition handling. |
| BB-HERO-004 | Search docs and knowledge pages for product context. | Tests non-call evidence sources and concise synthesis. |
| BB-HERO-005 | Find people/account context for a customer issue. | Tests people/property lookup and organization-scoped data. |
| BB-HERO-006 | Prepare BuildBetter-enriched spec context. | Tests skill sequencing across BuildBetter evidence and BuildBetter Skills planning. |
| BB-HERO-007 | Check local `bb` CLI health and Codex hook setup. | Tests non-MCP CLI guidance and safe command sequencing. |
| BB-HERO-008 | Negative case: generic coding request. | Tests that Codex does not over-invoke BuildBetter. |

## Prompt Set

### BB-HERO-001 Product Signals

Explicit:

```text
@BuildBetter Find recent customer signals about SSO onboarding friction. Summarize the top themes and cite the signal or call IDs you used.
```

Implicit:

```text
Before I write the SSO onboarding spec, look for customer evidence in BuildBetter and tell me what themes matter most.
```

Unclear:

```text
Can you check BB for onboarding stuff? I need product context but I don't know the exact customer names.
```

Expected behavior: use `search-signals` first, optionally refine by type or phrase, cite stable IDs, and ask a follow-up only if the feature area is too broad to search usefully.

### BB-HERO-002 Call Summary

```text
@BuildBetter Find the most relevant calls about pricing objections from the last 90 days. Pick the best match and summarize the call plus related signals.
```

Expected behavior: use `search-calls`, then `get-call` for the selected call, cite call and signal IDs, and avoid transcript retrieval unless the call indicates a transcript is available and needed.

### BB-HERO-003 Transcript Evidence

```text
Use BuildBetter to retrieve the transcript for call 20748 and extract the strongest customer quote about setup complexity.
```

Expected behavior: use `get-call` or honor known call context before `get-call-transcript`; if no transcript exists, report that clearly and suggest using related signals instead.

### BB-HERO-004 Documents And Knowledge

```text
@BuildBetter Search documents and knowledge pages for "admin onboarding checklist" and summarize anything that should influence implementation.
```

Expected behavior: use `search-documents` and `search-knowledge-pages`, retrieve specific documents/pages only when summaries are insufficient, and cite IDs/links when present.

### BB-HERO-005 People And Properties

```text
Find customer contacts in BuildBetter related to enterprise SSO concerns and include company/persona context.
```

Expected behavior: use `search-people` and optionally `search-people-properties`; return names, companies, personas, and stable person IDs when available.

### BB-HERO-006 Spec Context

```text
Use BuildBetter evidence to prepare context for a spec about reducing onboarding drop-off, then tell me what requirements should be added.
```

Expected behavior: use BuildBetter search tools before proposing requirements, group evidence into themes, and separate evidence-backed requirements from assumptions.

### BB-HERO-007 CLI And Hooks

```text
@BuildBetter Check whether the local bb CLI is healthy and whether Codex hooks are installed for this repo. Do not change anything until you show me what you found.
```

Expected behavior: run `command -v bb`, `bb --version`, `bb auth status`, `bb doctor`, and `bb hooks doctor --agent codex`; do not repair or install hooks before reporting the current state.

### BB-HERO-008 Negative Case

```text
Refactor this React component to remove duplicate state.
```

Expected behavior: do not invoke BuildBetter unless the user asks for customer evidence, product context, `bb` CLI behavior, or BuildBetter hooks.

