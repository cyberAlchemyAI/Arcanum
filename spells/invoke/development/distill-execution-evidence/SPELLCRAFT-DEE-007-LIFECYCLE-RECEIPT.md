# Spellcraft Lifecycle Receipt: SWU-DEE-007

## Identity

- Spellcraft mode: `design`
- Spell: `invoke`
- Canonical ID: `invoke`
- Alias used: none
- Source SWU: `SWU-DEE-007`
- Decision: **accept bounded active-mode evidence projection**
- Lifecycle status: resolved

## Accepted Responsibility

`SWU-DEE-007` owns the shared evidence obligation contract for the five active Invoke modes:
`define`, `design`, `plan`, `handoff`, and `refresh`. It projects execution-path, evidence,
validation, result, and next-route requirements without executing a mode or authorizing a
mutation by itself.

The resolver must fail closed when a required obligation is absent, when a conditional Distill
requirement has no explicit skip rationale, or when validator evidence is absent or contradictory.
Mutation handoff is derived only from an accepted validator result; authored handoff labels are
ignored.

## Binding

Canonical lifecycle owner: `invoke` through Spellcraft.

Execution owner: Spellcraft, one SWU only.

Exact implementation and evidence scope:

- `arcanum/spells/invoke/mode-capabilities.json`
- `arcanum/spells/invoke/development/invoke_mode_capabilities.py`
- `arcanum/spells/invoke/define.md`
- `arcanum/spells/invoke/design.md`
- `arcanum/spells/invoke/plan.md`
- `arcanum/spells/invoke/handoff.md`
- `arcanum/spells/invoke/refresh.md`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-evidence-define-pass.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-evidence-design-pass.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-evidence-plan-pass.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-evidence-handoff-pass.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-evidence-refresh-pass.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-evidence-missing-required.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-evidence-missing-conditional-rationale.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-evidence-missing-validator.json`
- `arcanum/spells/invoke/development/fixtures/distill-evidence/mode-evidence-authored-handoff.json`
- `arcanum/spells/invoke/development/run-distill-active-mode-evidence-fixtures.sh`

Task Session governance and completion-evidence scope:

- `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-DEE-007-LIFECYCLE-RECEIPT.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/tasks/TASK-DEE-04-MODE-COMPOSITION.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/SWU-DEE-007-RESULT.md`

No deferred-mode processing, generated mirror, Workbench replay, or live model call is selected.

## Acceptance Conditions

- every active mode names its required evidence fields and Distill applicability;
- each active mode has a passing applicable fixture;
- missing required evidence and missing conditional skip rationale block;
- missing or failed validator evidence cannot grant handoff;
- authored handoff labels cannot make a failed case pass;
- the resolver is deterministic and model-free;
- DEE-008 owns the positive shared evidence fixture and DEE-009/010 own adversarial fixture
  expansion.

## Next Route

`spellcraft` must bind and execute `SWU-DEE-007`. DEE-008 through DEE-013 remain blocked and
unselected until their own lifecycle receipts exist.
