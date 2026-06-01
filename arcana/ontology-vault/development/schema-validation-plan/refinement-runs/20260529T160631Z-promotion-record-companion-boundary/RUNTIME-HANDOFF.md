# Runtime Handoff: PromotionRecord Companion Boundary Refinement

Status: local-dry-run
Adapter: dry-run
Run id: `20260529T160631Z-promotion-record-companion-boundary`

## Objective

Run the canonical Refine loop as local evidence artifacts to decide companion-model boundaries before the first development-only JSON Schema candidate.

## Dispatch

- `REFINE-DISPATCH.json`

## Runtime Boundary

This refinement does not delegate to an external model runtime. Command-backed stages may be represented as dry-run command-surface evidence; Refine owns the final synthesis.

## Blocked Fields

- `dispatch-spec` does not resolve as a repository command through `tools/arcanum --resolve dispatch-spec`.

## Validation Substitute

Validate `REFINE-DISPATCH.json` directly against `formulae/dispatch-spec/dispatch.schema.json`.
