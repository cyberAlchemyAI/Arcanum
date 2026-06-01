# Dispatch Spec Implementation Layering Seed

Status: define-stage seed. Full implementation layering is deferred until `invoke plan`.

## L0 - Contract Proof

Goal: prove that a dispatch document can describe a useful Arcanum sequence without executing it.

Evidence:

- `dispatch.schema.yml` is valid JSON Schema.
- Embedded abstraction-research sample validates.
- README and SKILL separate validation from route interpretation.

Current status: pass.

## L1 - Validation Behavior

Goal: add a deterministic validator script and fixtures.

Candidate work:

- `scripts/validate-dispatch.py` and `development/run-validation-fixtures.sh`.
- Valid fixture for sequence.
- Valid fixture for tournament/dialectic.
- Invalid fixture for missing handoff.
- Invalid fixture for false promotion authority.

Exit evidence:

- validator returns pass/flag/block report shape,
- fixtures run in CI or local validation command.

## L2 - Spellcraft And Necronomicon Integration

Goal: prove dispatch documents are useful at composition boundaries.

Candidate work:

- Spellcraft design mode can reference a dispatch document.
- Necronomicon route planning can emit a dispatch candidate.
- Observed Invocation Loop can group step telemetry by `dispatch_id`.

Exit evidence:

- one local spell design uses dispatch-spec,
- one Necronomicon route record references dispatch-spec,
- grouped telemetry can be read by signal observer.

## L3 - Reusable Validation Evidence

Goal: make the package promotion-ready.

Candidate work:

- initialize Experiment Harness profile,
- run low/medium/complex examples,
- add quality bar and anti-pattern checks,
- route registry update through explicit sigil lifecycle approval.

Exit evidence:

- experiment report passes,
- unresolved gaps are non-blocking,
- promotion decision is recorded by owner.
