# Design Transport: Durable Arcanum Runtime Interface

## Source Inputs

- `INVOKE-DEFINE.md`
- `RUNTIME-GLOSSARY.md`
- `RESULT.md`
- `evidence-index.json`
- `stages/06-invoke-design.md`
- `stages/07-interrogation-design-review.md`
- `stages/08-distill-repair.md`
- `RUNTIME-ADAPTER-INTERROGATION-REVIEW.md`
- `RUNTIME-ADAPTER-DISTILL-REVIEW.md`
- `tools/development/context-packs/20260525-knowledge-taxonomy-types-schemas.md`
- `tools/development/handoffs/20260525-schema-discipline-arcanum-cyberalchemy-handoff.md`

## Produced Design Outputs

- `INVOKE-DESIGN.md`
- `ARCHITECTURE-BUNDLE.md`
- `GLOSSARY-CONSISTENCY.md`
- `ADAPTER-CONTRACT-DECISIONS.md`
- `SCHEMA-DISCIPLINE-INTEGRATION.md`
- `DESIGN-TRANSPORT.md`

## Approved Design

Use a two-folder model:

- target-local orchestrator evidence folders,
- `.arcanum/runtime/runs/<id>/` execution-state folders.

Adapter repair decisions:

- runtime runs record adapter profile evidence,
- runner owns `events.jsonl`,
- adapters classify raw runtime outcomes before runner status mutation,
- validation uses `contract`, `adapter-safety`, and `execution` grades.
- runtime artifacts adopt lightweight schema discipline through field tiers, inline enums, stable ids/paths, provenance, and shell/`jq` validation.

## Next Route

`invoke plan`
