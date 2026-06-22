# Invoke Result: Goal Architecture, Rules, Schemas, Contracts

## Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/design.md`
- Outputs:
  - `ARCHITECTURE.md`
  - `RULES.md`
  - `SCHEMAS.md`
  - `CONTRACTS.md`
  - `GLOSSARY-CONSISTENCY.md`
  - `IMPLEMENTATION-LAYERING-SEED.md`
  - `schemas/*.schema.json`
  - `DISPATCH-TECHNIQUE-TRACE.json`
  - `INVOKE-RESULT.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface.
- Template/profile selection: design-stage spell architecture companion, grounded in the goal README and define-stage SPEC/DEFINITIONS.
- Dispatch techniques: `artifact_contract_bridge`, `owner_boundary_check`, `validation_loop`, `residue_ledger`; full dispatch JSON not required.
- Distill validation: pass; the coherent unit is one design bundle for the existing `goal` spell, with runtime implementation and promotion explicitly deferred.
- Glossary consistency: pass
- Implementation layering: seed emitted in `IMPLEMENTATION-LAYERING-SEED.md`; full implementation layering remains a later plan-mode concern.
- Work-pack: n/a
- Decisions:
  - Keep schemas under the Invoke run until Spellcraft validates whether they should promote to `spells/goal/schemas/`.
  - Keep rule and contract documents design-stage, not runtime enforcement claims.
  - Keep all protected operations gated.
- Unresolved gaps:
  - Runtime implementation SWUs remain future `task-session` work.
  - Reusable behavior proof remains future `experiment-harness` work.
  - Generated runtime package remains deferred to runtime installer.
- Next route: `spellcraft validate`

## Validation Summary

Pending final command checks at authoring time:

- JSON parse for dispatch trace and schema files: pass.
- Required design-view headings present: pass.
- Public-boundary scan for private paths and filled profile details: pass.
- Glossary consistency report present: pass.
- Implementation-layering seed present: pass.
- Diff hygiene checks: pass.

## Public Boundary

The design bundle is public-safe. It references private runtime data only as a
boundary and does not include filled profile content, private corpus details, or
absolute private paths.
