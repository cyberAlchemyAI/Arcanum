# Research Tower - Zero-Allocation Triton Top-2 Backward Kernel

Built: 2026-06-12

## Subject

Research context for the task:

```text
Implement a zero-allocation Triton kernel executing the exact backward pass for:
W ||X - Top2(sigma(X W^T)) * FFN(X)||^2
  + gamma * E * sum_j(f_j * P_j)
subject to max_j(f_j) <= 2.1 / E

Optimized for FP16 precision, bypassing non-differentiable selection via continuous relaxation.
```

## Fast Read Order

1. `TOWER.md` - file roles and tower layers.
2. `L0-corpus.md` - external context and source records.
3. `definitions.md` - governed definitions for the rest of the tower.
4. `claim-ledger.md` - what is known, inferred, ambiguous, or blocked.
5. `derivation.md` - backward-pass interpretation and gradient surface.
6. `implementation-notes.md` - Triton/PyTorch implementation implications.
7. `RIGOR-VALIDATION-MAP.md` - proof/test/tooling map for avoiding overclaiming.
8. `FORMAL-MATH-SPEC.md` - Lean-suitable proof targets for the fixed-mask graph.
9. `SAFE-EXPLANATION-BRIEF.md` - plain-language guardrails for discussing the challenge.
10. `RELAXATION-CANDIDATES.md` - candidate continuous relaxations and decision matrix.
11. `PRIOR-ART-MAP.md` - known solution families and what not to claim as new.
12. `NOVELTY-SEARCH-MAP.md` - candidate novelty directions and stop conditions.
13. `LEARNING-PACK.md` - synthesis for the next engineer or research pass.
14. `open-residue.md` - unresolved items that must be decided before implementation.
15. `OPEN-QUESTIONS-DECISION-LEDGER.md` - interrogation decisions for V0 baseline and CAP2 design.
16. `FINAL-QUESTION-RESOLUTION.md` - final execution assumptions for the full work pack.
17. `CAP2-CANDIDATE-SPEC.md` - concrete CAP2-v0 relaxation hypothesis to test or kill.
18. `CAP2-REFERENCE.md` - implemented CAP2-v0 reference contract and validation summary.
19. `CAP2-PRIOR-ART-COMPARISON.md` - CAP2-v0 comparison against local prior-art baselines.
20. `WORK-PACK.md` - invoked task matrix from environment gate through final report.
21. `TOOLING-PLAN.md` - dependency and runtime plan for CPU reference and GPU Triton work.
22. `CUDA-RUNNER-PLAN.md` - CUDA runner options, acceptance contract, and runner tasks.
23. `FREE-CUDA-RUNNER-KIT.md` - free hosted-notebook CUDA runner instructions and probe kit.
24. `GOOGLE-COLAB-POC.md` - Google Colab-specific PoC path.
25. `PAID-CUDA-RUNNER-FALLBACK.md` - cheapest sensible paid fallback plan.
26. `reference/router_torch.py` - PyTorch V0 fixed-mask reference for autograd parity.
27. `CONVEX-SPARSE-TOPK-BLOCKED.md` - blocker report for implementation-ready convex sparse top-k baseline.
28. `CONVEX-SPARSE-TOPK-RESEARCH-PACK.md` - source-backed extraction pack for convex sparse top-k.
29. `convex-sparse-topk-extraction-20260612.dispatch.json` - dispatch route for `TASK-W2-003A`.
30. `CONVEX-SPARSE-TOPK-EXTRACTION.md` - extracted PAV p=4/3 sparse top-k mask contract.
31. `CONVEX-SPARSE-TOPK-FIXTURES.md` - fixture plan, composition checks, and boundary policy for the extracted mask.
32. `CONVEX-SPARSE-TOPK-JVP-BLOCKED.md` - blocked report for source-backed PyTorch/custom-JVP parity through the PAV mask.
33. `CONVEX-SPARSE-TOPK-JVP-FEASIBILITY.md` - feasibility result for a narrow PyTorch custom-autograd PAV mask parity oracle.
34. `CONVEX-SPARSE-TOPK-JVP-PARITY.md` - implemented narrow PyTorch custom-autograd PAV mask parity report.

## Boundary

This is a local research tower in the private parent repo. It does not promote any
Arcanum capability, sigil, formula, glossary, or implementation contract.

## Execution Evidence

The research dispatch has been executed as an artifact-backed closeout:

- `development/dispatch-runs/20260612T121416Z-top2-backward-research/README.md`
- `development/dispatch-runs/20260612T121416Z-top2-backward-research/CLOSEOUT.md`
- `development/dispatch-runs/20260612T121416Z-top2-backward-research/execution-index.json`

Status: `flag` because research is complete, but implementation remains gated by
the unresolved continuous-relaxation and semantic choices recorded in
`open-residue.md`.

Latest interrogation:

- `development/interrogation-runs/20260612T122502Z-open-questions-gaps/RESULT.md`
- `OPEN-QUESTIONS-DECISION-LEDGER.md`
- `development/interrogation-runs/20260612T124255Z-resolve-to-workpack/RESULT.md`
- `FINAL-QUESTION-RESOLUTION.md`

Latest Invoke authoring:

- `development/invoke-runs/20260612T123402Z-baselines-tdd-math-validation/INVOKE-DEFINE.md`
- `development/invoke-runs/20260612T123402Z-baselines-tdd-math-validation/INVOKE-DESIGN.md`
- `development/invoke-runs/20260612T123402Z-baselines-tdd-math-validation/INVOKE-PLAN.md`
- `development/invoke-runs/20260612T124255Z-full-workpack/RESULT.md`
- `development/invoke-runs/20260612T131715Z-tooling-plan/INVOKE-PLAN.md`
- `development/invoke-runs/20260612T133737Z-refresh-cuda-runner-task/REFRESH-REPORT.md`
- `development/refinement-runs/20260612T140546Z-cuda-runner-refresh/REFINE-REFRESH-RESULT.md`
- `WORK-PACK.md`

Latest Task Session:

- `development/task-sessions/20260612T-task-reference-tdd/RESULT.md`
- `reference/router_reference.py`
- `tests/test_router_reference.py`
- `development/task-sessions/20260612T-w0-environment-gate/RESULT.md`
- `development/task-sessions/20260612T1318Z-w0-004-tooling-manifests/RESULT.md`
- `development/task-sessions/20260612T1320Z-w0-005-cpu-env/RESULT.md`
- `development/task-sessions/20260612T1322Z-w0-006-gpu-triton-gate/RESULT.md`
- `development/task-sessions/20260612T135008Z-w0-007-cuda-runner-selection/RESULT.md`
- `development/task-sessions/20260612T140949Z-w1-001-pytorch-v0-parity/RESULT.md`
- `development/task-sessions/20260612T-w2-003c-jvp-blocked/RESULT.md`
- `development/task-sessions/20260612T-w2-003d-rg-feasibility/RESULT.md`
- `development/task-sessions/20260612T-w2-003d-pav-jvp-parity/RESULT.md`
- `development/task-sessions/20260612T-w3-001-cap2-reference/RESULT.md`
- `development/task-sessions/20260612T-w3-002-cap2-comparison/RESULT.md`

Latest Dispatch Spec:

- `development/dispatch-runs/20260612T-convex-topk-extraction-research/CLOSEOUT.md`
- `convex-sparse-topk-extraction-20260612.dispatch.json`
