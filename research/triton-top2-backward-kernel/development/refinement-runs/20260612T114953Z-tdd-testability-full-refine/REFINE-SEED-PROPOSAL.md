# Refine Seed Proposal - TDD/Testability for Triton Top-2 Backward Kernel

## Target

`research/triton-top2-backward-kernel/`

## Request

Run a full Refine pass asking whether the Triton top-2 backward kernel problem is
testable, and how to do TDD for it.

## Source Context

- `README.md` defines the research tower entrypoint.
- `LEARNING-PACK.md` frames the differentiability problem and mixed routing bridge.
- `definitions.md` defines tensor/load/zero-allocation terms.
- `derivation.md` gives the fixed-mask backward surface.
- `implementation-notes.md` gives the existing validation plan.
- `open-residue.md` names semantic blockers.
- `top2-backward-research.dispatch.json` is Dispatch Spec validated.

## Preset And Research Mode

- Preset: `full`.
- Research mode: `research-if-gap-appears`.
- External research confirmation: not requested during this run. Use local tower
  and already cited source records only unless a later operator confirms a
  bounded external pass.

## Refinement Question

Is this problem testable before the Triton kernel exists, and what is the TDD
shape that prevents the usual failure mode: optimizing a fast kernel for the
wrong mathematical graph?

## Working Thesis

Yes, it is testable, but only if tests are layered by semantic contract:

1. Decide the differentiable routing graph under test.
2. Build a PyTorch reference for that graph.
3. Test mathematical gradients before Triton.
4. Test Triton against the reference.
5. Test allocation and performance only after semantic parity.

## Write Scope

Allowed:

- Add refinement evidence under this run folder.
- Produce a non-executed TDD plan.
- Recommend next routes.

Not allowed:

- Implement Triton code.
- Modify public `arcanum` package files.
- Promote tower findings into canonical Arcanum definitions.

## Done Criteria

- The canonical ten-stage Refine loop is represented.
- Each command-backed stage has a resolved artifact or an explicit blocked reason.
- The final synthesis answers "is it possible to test this?"
- The final synthesis gives a TDD plan with test layers, fixtures, assertions,
  and red/green sequencing.
- Open semantic decisions are separated from implementable test scaffolding.

## Validation Surface

- Command resolution evidence from `arcanum/tools/arcanum`.
- Existing dispatch validation: `VALIDATION=pass` for
  `top2-backward-research.dispatch.json`.
- Local artifact review of tower files.
- Future validation recommended by this refine:
  PyTorch reference tests, gradcheck, Triton parity tests, allocation checks,
  and benchmark thresholds.

## Planned Stage Configuration

1. Context Builder evidence baseline: `context-builder`, mode `standard`, dry-run
   adapter if available.
2. Invoke Define: `invoke`, mode `define`.
3. Interrogation refine-review: `interrogation`, mode `refine-review`.
4. Research decision: Refine-owned `research-if-gap-appears`.
5. Distill: `distill`, mode `standard`, dry-run adapter if available.
6. Invoke Redefine / Design: `invoke`, mode `design`.
7. Interrogation refine-design-review: `interrogation`, mode `refine-design-review`.
8. Distill Repair: `distill`, mode `validate`, dry-run adapter if available.
9. Invoke Plan: `invoke`, mode `plan`.
10. Final Interrogation and Synthesis: `interrogation`, mode `refine-final`;
    Refine owns the final synthesis when interrogation route is blocked.
