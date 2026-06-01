## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/define.md`
- Outputs: `benchmark/development/refinement-runs/20260527T093001Z-benchmark/invoke-define/spec.md`, `benchmark/development/refinement-runs/20260527T093001Z-benchmark/invoke-define/glossary.md`, `benchmark/development/refinement-runs/20260527T093001Z-benchmark/invoke-define/implementation-layering-seed.md`, `benchmark/development/refinement-runs/20260527T093001Z-benchmark/invoke-define/transport-report.md`
- Template selection: `invoke.generic` selected; specialized families checked and rejected because this is a run-local refinement validation definition, not a module, research brief, architecture artifact, implementation plan, spell, sigil, or UX plan.
- Decisions: target `benchmark`; preset `standard`; use completed local benchmark smoke/audit evidence only; preserve no benchmark source mutation and no score recomputation; defer external research because no named evidence gap appeared; next owner is `refine`.
- Unresolved gaps: downstream Refine stages still need to prove interrogation, distill, design, repair, plan, and final synthesis quality; prior run block at Invoke Define remains historical risk evidence but is not a blocker for this stage.
- Next route: refine

## Validation

- Read `.codex/commands/invoke.md`: pass
- Read `spells/invoke/define.md`: pass
- Read seed proposal: pass
- Read context-builder stage and persisted context pack/index: pass
- Materialized define artifacts under current refinement run folder: pass
- Preserved benchmark non-mutation boundary: pending final `git diff --name-only` review

## Observability Closeout

- OBSERVATION: Invoke Define authored run-local definition artifacts from the supplied seed and context-builder baseline without nested model-backed command execution.
- LEDGER: Stage artifact is `benchmark/development/refinement-runs/20260527T093001Z-benchmark/stages/02-invoke-define.md`; primary outputs are under `benchmark/development/refinement-runs/20260527T093001Z-benchmark/invoke-define/`.
- REFLECTION_TRIGGER: false
- RECOMMENDATION: Continue the canonical Refine loop with interrogation/research-decision and Distill stages, preserving the no-rerun/no-rescore boundary.
- DEDUPE_KEY: `invoke:define:benchmark:20260527T093001Z-benchmark`
