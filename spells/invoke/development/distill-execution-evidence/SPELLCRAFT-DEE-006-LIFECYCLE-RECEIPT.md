# Spellcraft Lifecycle Receipt: SWU-DEE-006

## Identity

- Spellcraft mode: `validate`
- Spell: `invoke`
- Canonical ID: `invoke`
- Alias used: none
- Source SWU: `SWU-DEE-006`
- Decision: **accept bounded mode capability and deferred fail-close contract**
- Lifecycle status: resolved

## Accepted Responsibility

`SWU-DEE-006` owns the explicit Invoke mode capability table and its early resolver boundary.
The resolver may describe active-mode obligations, but it does not process an active lifecycle or
consume validator evidence; that projection remains DEE-007.

`full` and `validate` remain deferred. A request for either mode returns `unsupported` at the
capability gate, marks lifecycle processing false, does not evaluate Dispatch or Distill, and
sets `mutation_handoff_allowed=false`.

## Binding

Canonical lifecycle owner: `invoke` through Spellcraft.

Execution owner: Spellcraft, one SWU only.

Exact implementation and evidence scope:

- `arcanum/spells/invoke/README.md`
- `arcanum/spells/invoke/mode-capabilities.json`
- `arcanum/spells/invoke/development/invoke_mode_capabilities.py`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-capability-deferred-full.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-capability-deferred-validate.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-capability-active-design.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-capability-unknown.json`
- `arcanum/spells/invoke/development/run-distill-mode-capability-fixtures.sh`

Task Session governance and completion-evidence scope:

- `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-DEE-006-LIFECYCLE-RECEIPT.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/tasks/TASK-DEE-04-MODE-COMPOSITION.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/SWU-DEE-006-RESULT.md`

No active-mode evidence projection, mode mutation, generated mirror, Workbench, or deferred-mode
implementation is selected.

## Acceptance Conditions

- every Invoke mode has `implementation_status`, `dispatch_trace`, `distill`, and
  `mutation_handoff_allowed` rules;
- `full` and `validate` stop before lifecycle processing and never imply readiness;
- active mode resolution reports obligations without claiming execution or handoff;
- unknown modes fail closed;
- the table and resolver remain deterministic and model-free;
- DEE-007 owns active-mode evidence consumption and remains blocked until separately selected.

## Next Route

`spellcraft` must bind `SWU-DEE-007` active-mode evidence projection and exact paths. `SWU-DEE-007`
through `SWU-DEE-013` remain blocked and unselected.
