# WORK-PACK: x-ray Sigil Seed

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Seed input exists so Task Session can resolve the requested task. |
| complexity | medium | Creates one new Arcana sigil seed and experiment harness surface. |
| outputMode | single-package | Initial work is contained under `arcana/x-ray/` plus registry/docs links. |
| executionPackRef | n/a | This work-pack is the initial execution input. |
| seedRef | [REFINE-SEED.md](REFINE-SEED.md) | Materialized from the `refine` x-ray live experiment. |
| activeLayerWindow | L0-L1 | Create initial package and validation harness seed; do not promote. |
| readinessProfile | seed | Not a promoted sigil. |

## Objective Summary

- Objective: prepare the initial `x-ray` Arcana sigil package and development harness seed from the `refine` experiment output.
- Primary inputs: [REFINE-SEED.md](REFINE-SEED.md), `arcana/refine/development/example-outputs/sigil-new-low.output.md`, `arcana/sigil-development/SKILL.md`, and `arcana/experiment-harness/SKILL.md`.
- Success condition: `x-ray` has an initial README, SKILL, development harness seed, and validation notes that preserve the boundary between seed creation and promotion.

## Task Status Board

| Task ID | Goal | Layer | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- |
| TASK-XRAY-SIGIL-001 | Prepare the `x-ray` sigil package and development harness seed. | L0-L1 | [REFINE-SEED.md](REFINE-SEED.md) | ready | completed |

## Task Contract: TASK-XRAY-SIGIL-001

### Objective

Create the initial `x-ray` sigil package from the refined seed, without treating the sigil as mature or promoted.

### Inputs

- [REFINE-SEED.md](REFINE-SEED.md)
- `arcana/refine/development/example-outputs/sigil-new-low.output.md`
- `arcana/sigil-development/SKILL.md`
- `arcana/experiment-harness/SKILL.md`
- `registry/SIGILS.md`
- `arcana/README.md`

### Write Scope

- `arcana/x-ray/README.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/development/`
- `arcana/x-ray/examples/`
- `registry/SIGILS.md`
- `arcana/README.md`

### Required Behavior

The initial `x-ray` package must describe a sigil that:

- accepts arbitrary user-supplied context,
- helps the user understand what kind of context they supplied,
- creates an HTML explanation page as the target output form,
- explains actors, entities, data flow, transformations, process steps, and relationships,
- uses stepwise, user-driven clarification before producing final explanation structure,
- supports constructed visual or diagram-like explanations where useful,
- keeps generated visuals explainable and tied to the user's context,
- routes lifecycle validation through Sigil Development and Experiment Harness.

### Non-Goals

- Do not implement a complete HTML renderer.
- Do not promote `x-ray` in the registry as ready.
- Do not claim live behavior evidence before experiment outputs exist.
- Do not bypass Task Session execution ownership.

### Done Criteria

- `arcana/x-ray/README.md` describes purpose, boundary, inputs, outputs, and lifecycle owner.
- `arcana/x-ray/SKILL.md` defines objective, applicability, process, quality bar, anti-patterns, and output contract.
- `arcana/x-ray/development/VALIDATION.md` records seed validation and promotion gates.
- `arcana/x-ray/development/EXPERIMENT-SEED.md` defines at least three future live example branches: component, process, and architecture or plan.
- `arcana/x-ray/examples/` contains at least one example input/output-shape stub.
- `registry/SIGILS.md` and `arcana/README.md` include `x-ray` as seed or pilot, not promoted.

### Validation Surface

```bash
test -f arcana/x-ray/README.md
test -f arcana/x-ray/SKILL.md
test -f arcana/x-ray/development/VALIDATION.md
test -f arcana/x-ray/development/EXPERIMENT-SEED.md
test -d arcana/x-ray/examples
rg -n "x-ray|HTML|context|data flow|actors|relationships|sigil-development|experiment-harness" arcana/x-ray registry/SIGILS.md arcana/README.md
git diff --check -- arcana/x-ray registry/SIGILS.md arcana/README.md
```

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Dependencies | Write Scope | Done Criteria | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-XRAY-001 | TASK-XRAY-SIGIL-001 | [REFINE-SEED.md](REFINE-SEED.md) | none | `arcana/x-ray/README.md`, `arcana/x-ray/SKILL.md` | Initial sigil contract exists and preserves seed boundary. | README/SKILL review and `rg` checks. | task-session | completed |
| SWU-XRAY-002 | TASK-XRAY-SIGIL-001 | Experiment seed requirements | SWU-XRAY-001 | `arcana/x-ray/development/`, `arcana/x-ray/examples/` | Validation and example stubs exist. | file existence and `rg` checks. | task-session | completed |
| SWU-XRAY-003 | TASK-XRAY-SIGIL-001 | Discoverability requirements | SWU-XRAY-001 | `registry/SIGILS.md`, `arcana/README.md` | `x-ray` is discoverable as seed or pilot. | registry and README `rg` checks. | task-session | completed |

## Blockers

| Blocker ID | Scope | Description | Next Action |
| --- | --- | --- | --- |
| B-XRAY-001 | `--via goal` | resolved | Strict handoff coverage was persisted under `development/session-evidence/20260524T223119Z-codex-goal-handoff.md` and `.json`. |

## Gate Checks

1. Work-pack path must resolve before Task Session starts.
2. Task Session owns execution.
3. Sigil Development owns lifecycle quality and promotion readiness.
4. Experiment Harness evidence is required before any promotion claim.
5. The first task creates a seed package only.

## Next Route

```text
/task-session to arcana/x-ray/development/WORK-PACK.md --task TASK-XRAY-SIGIL-001 --runtime codex --via goal
```

## Runtime Evidence

```yaml
runtime: codex
adapter: codex-goal
source_task: TASK-XRAY-SIGIL-001
result: pass
handoff_pack: arcana/x-ray/development/session-evidence/20260524T223119Z-codex-goal-handoff.md
handoff_index: arcana/x-ray/development/session-evidence/20260524T223119Z-codex-goal-handoff.json
goal_profile: arcana/x-ray/development/session-evidence/20260524T223119Z-codex-goal-profile.md
files_touched:
  - arcana/x-ray/README.md
  - arcana/x-ray/SKILL.md
  - arcana/x-ray/development/VALIDATION.md
  - arcana/x-ray/development/EXPERIMENT-SEED.md
  - arcana/x-ray/examples/context-to-html-shape.md
  - registry/SIGILS.md
  - arcana/README.md
validation:
  - test -f arcana/x-ray/README.md
  - test -f arcana/x-ray/SKILL.md
  - test -f arcana/x-ray/development/VALIDATION.md
  - test -f arcana/x-ray/development/EXPERIMENT-SEED.md
  - test -d arcana/x-ray/examples
  - rg -n "x-ray|HTML|context|data flow|actors|relationships|sigil-development|experiment-harness" arcana/x-ray registry/SIGILS.md arcana/README.md
  - git diff --check -- arcana/x-ray registry/SIGILS.md arcana/README.md
experiment_harness:
  status: not_run
  next_step: initialize or run live examples from development/EXPERIMENT-SEED.md
remaining_blockers:
  - promotion requires live Experiment Harness evidence
lifecycle_owner_next_step: validate
```
