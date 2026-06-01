# Codex Goal Handoff: TASK-XRAY-SIGIL-001

## Identity

- Task: `TASK-XRAY-SIGIL-001`
- Source work-pack: `arcana/x-ray/development/WORK-PACK.md`
- Seed: `arcana/x-ray/development/REFINE-SEED.md`
- Runtime: `codex`
- Adapter: `codex-goal`
- Session evidence index: `arcana/x-ray/development/session-evidence/20260524T223119Z-codex-goal-handoff.json`

## Strict Coverage

Status: pass.

Every obligation needed for this seed package task is covered by the work-pack, seed, or lifecycle contracts listed below. The task may proceed within the declared write scope.

## Obligations

| ID | Obligation | Source | Coverage |
| --- | --- | --- | --- |
| O1 | Create the initial `x-ray` package, not a promoted sigil. | `WORK-PACK.md` Task Contract, Non-Goals | covered |
| O2 | README describes purpose, boundary, inputs, outputs, and lifecycle owner. | `WORK-PACK.md` Done Criteria | covered |
| O3 | SKILL defines objective, applicability, process, quality bar, anti-patterns, and output contract. | `WORK-PACK.md` Done Criteria | covered |
| O4 | Validation artifact records seed validation and promotion gates. | `WORK-PACK.md` Done Criteria | covered |
| O5 | Experiment seed defines component, process, and architecture or plan branches. | `WORK-PACK.md` Done Criteria; `REFINE-SEED.md` Promotion Constraint | covered |
| O6 | Examples include at least one input/output-shape stub. | `WORK-PACK.md` Done Criteria | covered |
| O7 | Registry and Arcana README list `x-ray` as seed or pilot, not promoted. | `WORK-PACK.md` Done Criteria | covered |
| O8 | Validation commands are available. | `WORK-PACK.md` Validation Surface | covered |

## Selected Sources

- `arcana/x-ray/development/WORK-PACK.md`
  - Selectors: Control Fields, Task Status Board, Task Contract, Done Criteria, Validation Surface, Gate Checks.
  - Covers: O1-O8.
- `arcana/x-ray/development/REFINE-SEED.md`
  - Selectors: Refined Intent, Expected Explanation Surface, Seed Boundary, Promotion Constraint.
  - Covers: O1, O2, O5.
- `arcana/sigil-development/SKILL.md`
  - Selectors: chain boundary, default output, process, quality bar.
  - Covers: lifecycle ownership and promotion boundary.
- `arcana/experiment-harness/SKILL.md`
  - Selectors: process, validation-loop, output contract.
  - Covers: experiment evidence expectations.
- `registry/SIGILS.md`
  - Selectors: Registry Table, By Tier, Entry Requirements.
  - Covers: discoverability format.
- `arcana/README.md`
  - Selectors: Example Sigil list and Quality Bar.
  - Covers: Arcana index format and tier rationale.

## Write Scope

- `arcana/x-ray/README.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/development/`
- `arcana/x-ray/examples/`
- `registry/SIGILS.md`
- `arcana/README.md`

## Constraints

- Do not implement a complete HTML renderer.
- Do not promote `x-ray`.
- Do not claim live behavior evidence before experiment outputs exist.
- Keep Task Session as execution owner.
- Keep Sigil Development as lifecycle owner after seed creation.

## Validation Surface

```bash
test -f arcana/x-ray/README.md
test -f arcana/x-ray/SKILL.md
test -f arcana/x-ray/development/VALIDATION.md
test -f arcana/x-ray/development/EXPERIMENT-SEED.md
test -d arcana/x-ray/examples
rg -n "x-ray|HTML|context|data flow|actors|relationships|sigil-development|experiment-harness" arcana/x-ray registry/SIGILS.md arcana/README.md
git diff --check -- arcana/x-ray registry/SIGILS.md arcana/README.md
```

## Fallback Exploration Rule

Fallback exploration is limited to named gaps in registry format, Arcana index style, or sigil package conventions. Extra sources must be reported in the Task Session result.

## Blockers

None for local seed package execution.
