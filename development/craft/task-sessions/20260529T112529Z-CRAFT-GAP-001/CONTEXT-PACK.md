# Task Session Context Pack: CRAFT-GAP-001

## Scope

| Field | Value |
| --- | --- |
| Work-pack | `development/craft/CRAFT-GAP-CLOSURE-WORK-PACK.md` |
| Task | `CRAFT-GAP-001` |
| Goal | Create `development/craft/CRAFT-GLOSSARY.md` as the candidate Craft method glossary. |
| Runtime | local |
| Strict coverage | pass |

## Controlling Task Contract

Create `CRAFT-GLOSSARY.md` from current Craft vocabulary evidence. The glossary must define at minimum:

`Craft`, `Craft Space`, `context`, `artifact`, `recursive ledger`, `blocker`, `gate`, `enabler`, `condition type`, `lane`, `role hint`, `blocker refiner`, `SCU`, `SWU`, `residue`, `entropy`, `reflection`, `recomposition`, `validation`, `promotion`, `handoff`, `route`, and `waiver`.

Every term needs a concise definition, status, and source anchor. Terms must remain local/candidate unless already validated by the MVP. No canonical registry, ontology, runtime, command, sigil, or spell surface may be mutated.

## Source Evidence

| Source | Evidence Used |
| --- | --- |
| `CRAFT-GAP-CLOSURE-WORK-PACK.md` | Task objective, done criteria, required terms, gate checks, write scope. |
| `CRAFT-GAP-CLOSURE-IMPLEMENTATION-LAYERING.md` | L0 exit criteria and pre-architecture blocker classification. |
| `CRAFT-INITIAL-DEFINITION.md` | Craft, Craft Space, schema/data translation, residue, SCU, entropy, reflection, recomposition. |
| `CRAFT-RECURSIVE-LEDGER-GLOSSARY.md` | Recursive ledger, context tree, cross-context relation, blockers, enablers, work-pack boundary. |
| `CRAFT-LEDGER-TYPE-SYSTEM.md` | Condition type, operational lane, role hint, blocker refiner, lane-role distinction. |
| `LEDGER.md` | MVP-validated context, artifact, relation, typed item, decision, blocker lifecycle, waiver rows. |
| `LEDGER-VALIDATION.md` | Manual validation pass, blocker lifecycle pass, lane evidence, deferred index/scoring/automation. |

## Hard Constraints

1. Work stays under `development/craft/`.
2. Do not mutate runtime adapters, command surfaces, registries, sigils, spells, or canonical ontology artifacts.
3. Do not mark architecture-owned inputs as solved in this task.
4. Do not sync README or SESSION-LEDGER yet; those belong to CRAFT-GAP-004/005 after later tasks.
5. It is acceptable to update this work-pack's task status after evidence supports completion.

## Decisions

No blocker decisions remain. The work-pack already selects the compact local glossary route.

## Gate Verdict

`pass`: source evidence is present, write scope is clear, validation is reviewable, and the task can proceed locally without runtime delegation.
