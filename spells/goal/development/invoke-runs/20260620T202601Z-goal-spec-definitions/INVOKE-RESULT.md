# Invoke Result: Goal Spec And Definitions

## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/define.md`
- Outputs:
  - `arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/SPEC.md`
  - `arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/DEFINITIONS.md`
  - `arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/DISPATCH-TECHNIQUE-TRACE.json`
  - `arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/INVOKE-RESULT.md`
- Template selection: spell template family, adapted to a define-stage spec baseline because `arcanum/spells/goal/README.md` is already the source spell contract.
- Dispatch techniques: `concrete_path_evidence`, `artifact_contract_bridge`, `owner_boundary_check`, `residue_ledger`; full dispatch JSON not required because no runtime delegation, subagents, or protected mutation were introduced.
- Distill validation: not required; the request is a bounded spec/definition pass for one existing spell and not mutation-capable execution.
- Decisions: promote only reusable Arcanum-wide terms to `arcanum/definitions`; keep detailed goal-package vocabulary local.
- Unresolved gaps:
  - Runtime implementation SWUs remain future `task-session` work.
  - Reusable behavior proof remains future `experiment-harness` work.
  - Generated runtime package remains deferred to runtime installer.
  - ADO design move remains approval-gated.
- Next route: `spellcraft validate`

## Definitions Governance Summary

- Definitions updated: `DEF-ARC-GOAL-SPELL`, `DEF-ARC-STAGED-DELTA`, `DEF-ARC-APPROVAL-TOKEN`
- Definition voices complete: yes
- Index synced: yes
- Drift found: yes, non-blocking local references now have canonical terms available.
- Undefined critical terms: 0 for this goal spec baseline
- Conflicting consumers: 0
- Domain context surface: `arcanum/spells/goal/`
- Concept registry aggregated: n/a
- Registry duplicates/drift: n/a
- Validation: pass
- Canonical source: `arcanum/definitions/DEFINITIONS.md`
- Follow-ups:
  1. Spellcraft should validate the goal README, spec, local definitions, and canonical definitions together.
  2. Experiment Harness should later prove the reusable fail-closed behavior before promotion.

## Public Boundary

The Invoke outputs are public-safe. They reference the existence of private
runtime data only as a boundary; they do not copy filled profile content,
private corpus detail, or absolute private paths.
