# Run Manifest: Craft Canonical Schema Stack

## Invocation

- Timestamp: `20260615T161047Z`
- Skill: `invoke`
- Mode: `design`
- Target: `arcana/craft`
- Request: create canonical schemas for each Craft layer and identify other
  artifacts/concepts needing schema coverage.

## Inputs Read

- `.agents/skills/invoke/SKILL.md`
- `.agents/skills/invoke/design.md`
- `.agents/skills/invoke/plan.md`
- `arcana/craft/ARCHITECTURE.md`
- `arcana/craft/SKILL.md`
- `arcana/craft/README.md`
- `arcana/craft/templates/ledger.schema.yml`
- `arcana/craft/examples/body-war-ledger.yml`
- `arcana/craft/examples/body-war-CRAFT.md`
- `arcana/craft/examples/goldenquill-ledger.yml`
- `arcana/craft/examples/goldenquill-CRAFT.md`
- `arcana/craft/development/refinement-runs/20260615T121512Z-craft-ledger-csv-json-indexes/RESULT.md`
- `arcana/craft/development/invoke-runs/20260615T123257Z-craft-index-improvements/INVOKE-DESIGN-ARCHITECTURE.md`
- `arcana/craft/development/invoke-runs/20260615T152120Z-craft-row-update-planner-architecture/INVOKE-DESIGN-ARCHITECTURE.md`
- `development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml`
- `development/craft/CRAFT-INTERACTION-LEDGER-SCHEMA.yml`

## Outputs

- `INVOKE-DESIGN-SCHEMA-STACK.md`
- `SCHEMA-CANDIDATE-INVENTORY.md`
- `GLOSSARY-CONSISTENCY.md`
- `IMPLEMENTATION-LAYERING-SEED.md`
- `DESIGN-TRANSPORT.md`
- `RUN-MANIFEST.md`

## Gates

- Canonical schema mutation: not run.
- Runtime tool implementation: not run.
- Generated mirror refresh: not run.
- Public-boundary scan: local path and sensitive-term scan required before
  final report.
- Next route: `invoke plan` or `task-session`.
