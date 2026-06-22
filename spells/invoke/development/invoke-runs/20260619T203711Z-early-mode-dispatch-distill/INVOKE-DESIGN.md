# Invoke Design Artifact

## Design Goal

Add mode-specific Dispatch/Distill behavior to `invoke define` and `invoke design` while preserving the lifecycle boundary:

- `define` owns spec/glossary baseline shaping.
- `design` owns architecture/design bundle shaping.
- `plan` owns implementation planning and mandatory automatic Distill validation before mutation-capable handoff.
- `task-session` owns execution of bounded SWUs.

## Source Contracts

| Source | Contract Use |
| --- | --- |
| `arcanum/spells/invoke/README.md` | Root Invoke discipline: every mode records Dispatch trace; plan/full/validate run automatic Distill validation. |
| `arcanum/spells/invoke/define.md` | L0 define mode contract to harden. |
| `arcanum/spells/invoke/design.md` | L1 design mode contract to harden. |
| `arcanum/spells/invoke/plan.md` | Reference for stronger mutation-handoff Distill discipline. |
| `arcanum/formulae/dispatch-spec/TECHNIQUE-CATALOG.md` | Technique vocabulary. |
| `arcanum/spells/invoke/development/run-validation-fixtures.sh` | Validation harness. |

## Architecture View

### Context View

The root Invoke contract now defines cross-mode discipline. `define` and `design` need local contract language and fixture evidence so the rule is executable for early outputs.

### High-Level Structure View

1. Canonical mode contracts define required Dispatch/Distill fields.
2. Fixture expected outputs demonstrate those fields for pass, flag, block, and integration paths.
3. Validation harness checks early-mode fixture outputs and canonical contract phrases.
4. Generated skill mirrors receive the same mode contract text.

### Low-Level Components View

| Component | Change |
| --- | --- |
| `define.md` | Add optional `distill` sigil, Dispatch/Distill gates, handoff fields, and output contract fields. |
| `design.md` | Add optional `distill` sigil, design-unit Distill gate, Dispatch/Distill handoff fields, and output contract fields. |
| `run-validation-fixtures.sh` | Require early-mode contract phrases and expected output fields. |
| Fixture expected outputs | Add `Dispatch techniques:` and `Distill validation:` lines to define/design fixtures. |
| `.agents/skills/invoke/*.md` | Sync generated mirror contracts. |

### Workflow Process View

1. Patch canonical `define.md` and `design.md`.
2. Patch generated `.agents` mirror files.
3. Patch validation harness requirements.
4. Patch expected fixture outputs for standalone and integration define/design paths.
5. Run shell syntax and full fixture validation.

### Decision Flow View

- If output is `define`: record Dispatch techniques always; record Distill as `not required`, `pass`, `flag`, or `block`.
- If output is `design`: record Dispatch techniques always; run design-unit Distill unless the mode blocks before design material exists.
- If Distill finds multiple coherent units: flag or block and record split/gap route instead of pretending one plan can safely consume it.
- If the route requires mutation: defer to `plan` and then `task-session`.

### Dependency Interface View

| Producer | Consumer | Interface |
| --- | --- | --- |
| `define` | `design` | Spec/glossary baseline, Dispatch techniques, Distill validation status, unresolved gaps. |
| `design` | `plan` | Architecture bundle, source contracts, Dispatch techniques, design-unit Distill status, unresolved gaps. |
| `plan` | `task-session` | Work-pack/SWU and mandatory automatic Distill validation evidence. |
| Validation harness | Maintainers | Fixture pass/fail report and run evidence. |

## Risks

- Overrequiring Distill in `define` could slow simple definitions. Mitigation: make it conditional at define depth.
- Underrequiring Distill in `design` could leave broad designs for plan mode. Mitigation: require a design-unit check unless design blocks before material exists.
- Generated mirrors may drift. Mitigation: sync `.agents/skills/invoke/define.md` and `.agents/skills/invoke/design.md` in the same task.

## Dispatch Technique Trace

| Technique | Use |
| --- | --- |
| `owner_boundary_check` | Preserves early-mode and Task Session boundaries. |
| `artifact_contract_bridge` | Maps mode contract language to fixture expectations. |
| `validation_loop` | Full invoke fixture validation is the completion gate. |
| `concrete_path_evidence` | All changed contracts and validation artifacts are path-scoped. |
| `recomposition_proof` | Confirms early-mode fields recombine with root Invoke discipline. |

## Distill Validation

- Status: pass
- Unit: early-mode Dispatch/Distill contract hardening.
- Gap check: no need to change Task Session or plan ownership.
- Split avoided: `define` optional sanity check and `design` design-unit check are distinct from plan automatic Distill validation.

## Next Route

Proceed to plan/work-pack for `TASK-IDD-001`.
