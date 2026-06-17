# Refine Seed Proposal - Review Hardening For Triton Top2 Challenge

Run ID: `20260615T025930Z-review-hardening-refine`
Status: `executed-through-refine-result`

## Target

Primary target:

- `research/triton-top2-backward-kernel/`

Related presentation target:

- `research/triton-top2-backward-kernel/paper/`

## Operator Intent

Research and refine each currently missing point from the Triton Top2/CAP2 work,
using a dispatch route with subagent strategy and full Refine loop nodes.

## Desired Outcome

A non-executed, review-ready plan that turns the remaining caveats into clear
research or validation tasks:

1. CAP2 novelty is not claimed yet.
2. CAP2 is not exact 2-sparse.
3. Dynamic-load gradients are not included.
4. CAP2 zero-allocation evidence is weaker than fixed-mask evidence.
5. Benchmark evidence is smoke-level only.
6. Entmax remains named but not implemented.
7. The paper package needs evidence/presentation polish.
8. Dirty/untracked repository state needs an artifact inventory before sharing.

## Source Context

Evidence anchors:

- `WORK-PACK.md`: tower status is `complete-ready-for-review`.
- `FINAL-PRIOR-ART-NOVELTY-REPORT.md`: supported claims and non-claims.
- `CAP2-W6-PARITY-REPORT.md`: CAP2 fixed-load parity and remaining limits.
- `TRITON-BENCHMARK-REPORT.md`: smoke benchmark and CAP2 zero-allocation limits.
- `open-residue.md`: original semantic residue and decisions.
- `glossary.md`: beginner-facing and pending contract terminology.
- `research/triton-top2-backward-kernel/paper/`: paper package.

## Write Scope

This refine proposal may write only inside:

```text
research/triton-top2-backward-kernel/development/refinement-runs/20260615T025930Z-review-hardening-refine/
```

No implementation, paper, glossary, work-pack, or evidence artifact should be
mutated until the operator approves the route and any runtime-backed stages.

## Preset And Research Mode

- Preset: `full`
- Research: `bounded-research`

Bounded research is appropriate because novelty, entmax, and benchmark framing
depend on comparing local evidence against prior-art or external expectations.
External research must remain source-backed and cannot override local evidence.

## Planned Stage Configuration

Use the canonical ten-stage Refine loop:

1. Context Builder evidence baseline.
2. Invoke Define.
3. Interrogation refine-review.
4. Research decision.
5. Distill.
6. Invoke Redefine / Design.
7. Interrogation refine-design-review.
8. Distill Repair.
9. Invoke Plan.
10. Final Interrogation and Refine synthesis.

Subagents are recommended after operator approval for role-bound review of
novelty, math/relaxation, systems evidence, baseline coverage, paper evidence,
and repository artifact state.

## Done Criteria

The approved refine run is done when it produces:

- a point-by-point gap ledger;
- a research plan for novelty and entmax;
- a validation plan for exact 2-sparsity, dynamic-load gradients, CAP2
  zero-allocation, and larger benchmarks;
- a paper hardening plan with claim guards;
- an artifact inventory plan that separates tower evidence, paper evidence,
  generated skill surfaces, and unrelated repository dirt;
- recommended next `invoke` or `task-session` routes only after final synthesis.
