# Refine Seed Proposal: EvidenceSet Schema

## Target

Inventory `EvidenceSet` candidate schema.

## Source Context

- `arcana/inventory/development/decisions/POC-GATES-DECISION.md`
- `arcana/inventory/development/decisions/EVIDENCESET-DECISION.md`
- `arcana/inventory/development/pilot/evidence-card/pilot-retrieval.json`
- `arcana/inventory/development/pilot/evidence-card/craft-stressor-retrieval.json`
- `arcana/inventory/development/pilot/evidence-card/evidenceset-comparison.md`
- `arcana/inventory/development/READINESS.md`
- `arcana/inventory/development/WORK-PACK.md`

## Refinement Question

What is the smallest useful `EvidenceSet` schema that preserves grouped evidence reuse for agents without turning Inventory into a ledger, synthesis system, ontology authority, or UI workflow?

## Write Scope

This refine run may write only refinement evidence under:

`arcana/inventory/development/refinement-runs/20260527T160759Z-evidenceset-schema/`

It must not mutate production Inventory templates, runtime scripts, or canonical schemas.

## Done Criteria

- Define the coherent unit for `EvidenceSet`.
- Name required fields and strict non-goals.
- Identify validation criteria against both existing candidate sets.
- Decide whether the next route is Task Session, Decision Gate, or stop/refine.

## Validation Surface

- Existing fixture validator remains authoritative for current evidence-card fixtures:

```sh
bash arcana/inventory/scripts/validate-evidence-card-fixtures.sh arcana/inventory/development/pilot/evidence-card
```

- Refined schema proposal should be checkable against:
  - `evidence-set.evidenceset-need`
  - `evidence-set.craft-recursive-ledger`

## Preset

standard

## Research Mode

no-research

Local repository evidence is sufficient for this schema decision. External research is not required because the blocker is a local artifact boundary question.

## Planned Stage Configuration

1. Context Builder evidence baseline: standard, strict, local evidence only.
2. Invoke Define: define the schema candidate and authority boundary.
3. Interrogation refine-review: test if the candidate hides unresolved choices.
4. Research decision: no-research.
5. Distill: select smallest coherent concept unit.
6. Invoke Redefine / Design: design schema fields, non-goals, and validation.
7. Interrogation refine-design-review: critique design completeness.
8. Distill Repair: remove overreach and preserve agent performance surface.
9. Invoke Plan: non-executed Task Session plan.
10. Final Interrogation and Synthesis: produce final recommendation.
