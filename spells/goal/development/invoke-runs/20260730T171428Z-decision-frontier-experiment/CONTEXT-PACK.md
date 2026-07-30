# Bounded Context Pack

## Objective

Author a fixture-only experiment plan for a decision frontier spanning Invoke,
Craft, and Goal while preserving authority and execution boundaries.

## Included Authority

| Source | Role |
| --- | --- |
| `spells/invoke/README.md` | Invoke authoring and lifecycle boundary |
| `spells/invoke/define.md` | Define contract |
| `spells/invoke/design.md` | Design denominator and selection contract |
| `spells/invoke/plan.md` | work-pack, Distill, SWU, and closeout contract |
| `spells/goal/README.md` | Goal spell contract |
| `spells/goal/runtime/goal_loop.py` | current frontier consumption behavior |
| `spells/goal/schemas/frontier-snapshot.schema.json` | current frontier projection |
| `arcana/craft/SKILL.md` | canonical Craft ownership and ledger behavior |
| `arcana/craft/templates/schemas/ledger-core.schema.yml` | current decision and relation shapes |
| `formulae/dispatch-spec/TECHNIQUE-CATALOG.md` | route validation techniques |

Paths are relative to the public `arcanum/` repository root.

## Supporting Non-Authority Evidence

- the Inventory index validated as lookup-ready;
- historical Invoke synthesis entries supplied design rationale, but their
  statements about missing machinery were excluded where contradicted by live
  canonical files;
- the immutable Wayfinder source supplied the external mechanism.

## Explicit Exclusions

- consumer-private project material;
- issue-tracker adapters or issue mutation;
- canonical Craft, Goal, or Invoke changes;
- implementation execution or SWU selection;
- publication, deployment, and production-readiness claims.

## Context Sufficiency

The included sources define the existing ownership boundaries, the current
frontier shape, the planning requirements, and the lifecycle route. No
repository-wide architecture load is necessary for this experiment.
