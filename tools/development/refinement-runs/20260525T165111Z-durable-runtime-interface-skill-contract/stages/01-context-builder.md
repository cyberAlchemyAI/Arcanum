## Context Pack Summary

- Task: Design a generic Arcanum durable runtime interface for refine/task-session execution.
- Mode: standard
- Files selected: 7
- Snippets selected: 11
- Obligation coverage: 100%
- Noise ratio: low
- Output markdown: `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/stages/01-context-builder.md`
- Output index: `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/evidence-index.json`
- Handoff pack: runtime
- Session evidence path: `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/`
- Strict coverage: pass
- Blockers: 0

### Obligation Matrix

| Obligation | Coverage | Evidence |
| --- | --- | --- |
| O1: Remove Codex Goal and native `/goal` from the core refine/task-session runtime model. | covered | `arcana/refine/SKILL.md`, `.codex/commands/task-session.md`, `arcana/task-session/runtime-adapters/codex-goal.md` |
| O2: Preserve refine's canonical ten-stage loop. | covered | `arcana/refine/SKILL.md`, `arcana/refine/REFINEMENT-LOOP.md` |
| O3: Design durable execution runs with parent/child support. | covered | user prompt, prior `RESULT.md` |
| O4: Support multiple refinement loops as sibling, nested, candidate, repair, or continuation runs. | covered | user prompt, prior local run result |
| O5: Treat Codex as one adapter, not the runtime identity. | covered | prior failed `tools/arcanum --exec` run, `tools/arcanum` current direct Codex path |
| O6: Produce a decision-complete implementation handoff. | covered | final synthesis requirements |

### Included Context

- `arcana/refine/SKILL.md` - current refine contract; selected because it shows the useful loop and stale Codex Goal coupling - selectors: objective, required capabilities, stage configuration, run-manifest contract - obligations: O1, O2.
- `arcana/refine/REFINEMENT-LOOP.md` - canonical loop and stage budgets - selectors: Canonical Default Loop, Stage Configuration, Run Manifest - obligations: O2.
- `.codex/commands/context-builder.md` - context-pack output contract - selectors: Output Contract - obligations: O6.
- `.codex/commands/invoke.md` - Invoke output contract - selectors: Root Output Contract - obligations: O6.
- `.codex/commands/interrogation.md` - Structured Interview output contract - selectors: Output Contract - obligations: O6.
- `arcana/distill/SKILL.md` - Distill output contract and role trace policy - selectors: runtime-role-policy, output-contract - obligations: O4, O6.
- `tools/arcanum` - current command resolver/executor behavior - selectors: `prepare_codex_home`, `build_prompt`, `--exec` execution path - obligations: O5.

### Excluded Candidates

- `transmutations/codex-goal-profile/` - excluded from the active design baseline because the user explicitly removed native `/goal` from the model; useful only as stale-language cleanup surface.
- Historical task-session development evidence - excluded from the core baseline unless active validation consumes it.

### Next Actions

1. Define the runtime contract as an Arcanum-wide infrastructure layer.
2. Use Invoke Define to name the exact runtime concepts and boundaries.
3. Preserve the skill output contracts in all subsequent stage artifacts.

### Observability Closeout

- OBSERVATION: skipped
- LEDGER: n/a
- REFLECTION_TRIGGER: none
- RECOMMENDATION: local-skill-contract-run
- DEDUPE_KEY: local-skill-contract-context-builder-20260525T165111Z
