# Constraints And Boundaries

Combined write scope:

- `research/mogt-agentic-conversation/development/fixtures/`
- `research/mogt-agentic-conversation/tools/`
- `research/mogt-agentic-conversation/experiments/*/context.md` only if fixture references need clarification
- `research/mogt-agentic-conversation/experiments/*/results/`
- `research/mogt-agentic-conversation/development/WORK-PACK.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-002-RESULT.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-003-RESULT.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-004-RESULT.md`
- `research/mogt-agentic-conversation/development/fixture-validation-report.md`

Guardrails:

- Do not run live experiments.
- Do not update `research/mogt-agentic-conversation/results/MOGT-EVIDENCE-STATUS.md` to supported or partially supported.
- Do not rewrite result-facing paper sections.
- Do not mutate canonical Experiment Harness, Dispatch Spec, Whisper, Refine, Invoke, Research Tower, or Research Evidence Harness contracts.
- If a reusable Experiment Harness extension is needed, produce a proposal or handoff rather than direct canonical mutation.
- Use the composite context pack first, then stage packs. Extra sources are allowed only for named gaps and must be reported.
