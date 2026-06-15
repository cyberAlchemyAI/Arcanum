# Design Transport: Craft Canonical Schema Stack

## Transport Summary

- Capability: `invoke`
- Mode: `design`
- Target owner: `arcana/craft`
- Target artifact: canonical Craft schema stack proposal
- Status: pass-with-gated-implementation
- Next route: `invoke plan` or `task-session`

## Produced Artifacts

- `INVOKE-DESIGN-SCHEMA-STACK.md`
- `SCHEMA-CANDIDATE-INVENTORY.md`
- `GLOSSARY-CONSISTENCY.md`
- `IMPLEMENTATION-LAYERING-SEED.md`
- `DESIGN-TRANSPORT.md`
- `RUN-MANIFEST.md`

## Design View Coverage

| View | Status |
| --- | --- |
| Context view | pass |
| High-level structure view | pass |
| Low-level components view | pass |
| Workflow process view | pass |
| Decision flow view | pass |
| Dependency interface view | pass |

## Source Contracts

- `arcana/craft/ARCHITECTURE.md`
- `arcana/craft/SKILL.md`
- `arcana/craft/README.md`
- `arcana/craft/templates/ledger.schema.yml`
- `arcana/craft/examples/body-war-ledger.yml`
- `arcana/craft/examples/goldenquill-ledger.yml`
- `development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml`
- `development/craft/CRAFT-INTERACTION-LEDGER-SCHEMA.yml`

## Target-Artifact Gaps

| Gap | Owner | Next Route |
| --- | --- | --- |
| Missing formal schemas for example-backed rows. | Craft schema stack | P0 implementation slice |
| Missing index object and generated-index schema. | Craft schema stack | P0 implementation slice |
| Missing interface schema for `CRAFT.md`, `state all`, and `Craft Result`. | Craft interface schema | P1 design/implementation slice |
| Missing route-exchange schema for handoffs, receipts, and events. | Craft route-exchange schema | P1 design/implementation slice |
| Missing projection and row-update schemas. | Craft projection/planner schema | P2 after source/index schemas |
| Missing artifact manifest and validation report schemas. | Craft validation/artifact schema | P2 after route/interface needs are settled |

## Handoff Recommendation

Proceed with the smallest source/index schema slice before projection or row
updater work. Do not implement CSV import or YAML apply behavior from this
design bundle.
