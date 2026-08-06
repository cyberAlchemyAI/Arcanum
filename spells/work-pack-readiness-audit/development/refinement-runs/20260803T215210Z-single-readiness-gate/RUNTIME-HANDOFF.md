# Runtime Handoff

## Runtime Boundary

- Runtime: native Codex capability surface
- Adapter: parent-owned native skills and one approved native read-only helper
- Owner: `refine`
- Status: `pass`
- Runtime run folder: this refinement-run directory

## Runtime Objective

Run the canonical Refine loop for a reusable plan-readiness receipt and selected-unit live-admission boundary. Produce definition, design, critique, and a non-executed implementation plan only.

## Dispatch Route

- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch schema: `arcanum/formulae/dispatch-spec/dispatch.schema.yml`
- Dispatch validation: `pass`
- Dispatch ID: `20260803T215210Z-single-readiness-gate`
- Technique catalog: `arcanum/formulae/dispatch-spec/TECHNIQUE-CATALOG.md`
- Technique overlays: `baseline_sequence`, `dialectic_for_tension`
- Subagent authorization: operator-confirmed for one read-only `admission-boundary-critic`

## Stage Receipt Contract

Each stage records dispatch ID, step ID, capability, status, artifact path, validation, blockers, and residue in `RUN-MANIFEST.md` and `evidence-index.json`. The reviewer additionally returns spawn, join, close, scope, findings, invariants, and mutation statement fields.

## Handoff Requirements

- Context Builder handoff pack: `stages/01-context-builder.md`
- Handoff index: `stages/01-context-builder-index.json`
- Strict coverage: `pass`
- Runtime status: `pass`
- Dispatch route validation: `pass`
- Run manifest: `RUN-MANIFEST.md`
- Evidence index: `evidence-index.json`

## Blocked Fields

- Canonical mutation: outside Refine authority; route only after final synthesis.
- Generated mirrors: outside this authoring run.
- External research: not authorized or needed.
- Project execution: no SWU is selected and no Task Session is started.

## Generator residue

The Refine generator wrote the dispatch successfully, but its integrated `--validate` call resolved the repository-relative output from the `arcanum/` subdirectory and failed with `FileNotFoundError`. Direct canonical validation from the repository root passed. This path-resolution defect is recorded as tooling residue and does not change the dispatch verdict.
