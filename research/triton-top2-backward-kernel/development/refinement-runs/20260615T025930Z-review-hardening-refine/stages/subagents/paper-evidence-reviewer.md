# Paper Evidence Reviewer Receipt

- agent_id: `paper-evidence-reviewer-PLACEHOLDER`
- role_id: `paper-evidence-reviewer`
- spawn_status: `spawned`
- join_status: `completed`
- close_status: `closed`
- dispatch_id: `refine-20260615T025930Z-review-hardening`
- step_id(s): `s1`, `s5`, `s7`, `s8`, `s9`, `s10`
- capability_ref: `refine/subagent:paper-evidence-reviewer`
- status: `flag`
- validation_result: `paper package is reviewable with guarded claims, but needs appendix/reproducibility polish and a few stale guard updates before presentation`

## Artifacts

- Receipt artifact: `research/triton-top2-backward-kernel/development/refinement-runs/20260615T025930Z-review-hardening-refine/stages/subagents/paper-evidence-reviewer.md`
- Inspected paper package: `research/projects/mars/papers/triton-top2-backward-kernel/`
- Inspected tower reports: `research/triton-top2-backward-kernel/`

## Evidence Paths

- `research/projects/mars/papers/triton-top2-backward-kernel/paper.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/CLAIM-GUARDS.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/PAPER-REVIEW.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/PAPER-TEST-SPEC.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/DATA-APPENDIX.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/MATH-APPENDIX.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/REFERENCE-LEDGER.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/CAP2Definition.lean`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/CAP2FixedLoadScalar.lean`
- `research/triton-top2-backward-kernel/WORK-PACK.md`
- `research/triton-top2-backward-kernel/CAP2-W6-PARITY-REPORT.md`
- `research/triton-top2-backward-kernel/TRITON-BENCHMARK-REPORT.md`
- `research/triton-top2-backward-kernel/FINAL-PRIOR-ART-NOVELTY-REPORT.md`
- `research/triton-top2-backward-kernel/reference/router_torch.py`
- `research/triton-top2-backward-kernel/reference/router_triton.py`
- `research/triton-top2-backward-kernel/tests/test_router_torch.py`
- `research/triton-top2-backward-kernel/tests/test_router_triton.py`
- `research/triton-top2-backward-kernel/scripts/benchmark_triton_paths.py`
- `research/triton-top2-backward-kernel/<cuda-runner-iteration-command>`

## Findings

1. The paper's central claim boundary is mostly sound.
   - `paper.md` scopes exact backward to fixed-mask or CAP2 fixed-load relaxation paths.
   - `FINAL-PRIOR-ART-NOVELTY-REPORT.md` explicitly forbids hard Top2, CAP2 novelty, exact 2-sparsity, dynamic-load gradients, and production-performance claims.
   - `CLAIM-GUARDS.md` lists supported claims and non-claims in a useful reviewer-facing table.

2. The paper package has a stale formal-guard mismatch that should be polished before presentation.
   - `CLAIM-GUARDS.md` still has `NC-008` saying the package does not claim a completed formal softmax derivative proof and `NC-009` saying the CAP2 derivative proof is feasibility-only.
   - The same file also adds `CL-008`, `CL-009`, `NC-010`, and `NC-011`, which correctly reflect the newer theorem slices.
   - `FORMAL-VALIDATION-REPORT.md` says the finite softmax coordinate derivative theorem now builds and CAP2 definition/adjusted-logit slices build.
   - Recommended correction: retire or rewrite `NC-008` and `NC-009` so they say "no packaged full softmax Jacobian theorem" and "no full CAP2 calculus proof", rather than implying the completed coordinate/CAP2 definition slices do not exist.

3. The reproducibility appendix is too thin for a challenge/paper handoff.
   - `paper.md` includes `lake build` and `jq empty benchmark.json`.
   - `PAPER-TEST-SPEC.md` repeats only those two commands.
   - Missing from the paper-facing appendix are the direct CPU/reference test command, Triton test command, benchmark command, RunPod iteration script command, and expected pass-count examples from `WORK-PACK.md`, `CAP2-W6-PARITY-REPORT.md`, and `FINAL-PRIOR-ART-NOVELTY-REPORT.md`.
   - Recommended correction: add a reproducibility command table with environment requirement, command, expected evidence, and interpretation guard.

4. The evidence manifest is complete enough for review, but it should map the newest formal claims more explicitly to paper sections.
   - `EVIDENCE-MANIFEST.md` includes `EV-FORMAL-006` through `EV-FORMAL-010`.
   - `paper.md` cites the formal evidence as a range, which is acceptable but not ideal for a skeptical reviewer.
   - Recommended correction: in `paper.md` or an appendix, add a theorem-to-claim table mapping `softmaxCoord_coordLine_hasDerivAt`, `CAP2Definition.lean`, and `cap2AdjustedLogit_coordLine_self/of_ne` to the exact sentence they support and the exact sentence they do not support.

5. CAP2 zero-allocation remains under-presented as a guarded gap.
   - `TRITON-BENCHMARK-REPORT.md` says CAP2 zero-allocation memory behavior is partially supported through preallocated outputs but is not a separate W7 acceptance claim.
   - `CAP2-W6-PARITY-REPORT.md` says CAP2 zero-allocation behavior was not measured as W7 acceptance.
   - Recommended correction: keep this as a visible non-claim and add a future-work task named "CAP2 zero-allocation acceptance check" with the same strength as the fixed-mask W7 check.

6. FP16 behavior needs a paper-facing boundary paragraph.
   - `WORK-PACK.md` supports fixed-mask FP16 tolerance checks with FP32 outputs.
   - `FORMAL-VALIDATION-REPORT.md` explicitly defers FP16 numeric error analysis.
   - The paper conclusion mentions an FP16 numerical error story as future work, but the reproducibility appendix does not list the FP16 test surface.
   - Recommended correction: add a short "FP16 boundary" paragraph: fixed-mask empirical tolerance exists; CAP2 FP16 and formal numeric error bounds are not claimed unless separately validated.

7. Appendix references are present but not yet reviewer ergonomic.
   - `DATA-APPENDIX.md` has the raw timing table and environment.
   - `MATH-APPENDIX.md` explains `Z`, `P`, `A`, `dZ`, `dW`, and `dX_router`.
   - Recommended correction: add "What this appendix proves / does not prove" boxes to both appendices, with direct manifest IDs.

8. The repository state is still uncommitted/untracked for both the tower and paper package.
   - `git status --short research/projects/mars/papers/triton-top2-backward-kernel research/triton-top2-backward-kernel` reports both roots as untracked.
   - Recommended correction: before external sharing, run an artifact inventory task that records which files are intended evidence, generated/cache noise, or local-only runtime residue.

## Blockers

- No hard blocker for paper review.
- Presentation blocker: stale non-claim wording around formal softmax/CAP2 proof progress could confuse a reviewer.
- Reproducibility blocker: paper appendix does not yet include the full command ladder for CPU tests, Triton tests, RunPod iteration, benchmark production, and formal build.
- Evidence-hygiene blocker: tower and paper roots are untracked as a group, so publication packaging needs an inventory/commit boundary before sharing.

## Residue

- CAP2 novelty remains candidate-only and should stay guarded unless a separate prior-art reviewer produces stronger evidence.
- CAP2 exact 2-sparsity is not claimed.
- Dynamic-load gradients are not claimed.
- CAP2 zero-allocation acceptance is not promoted to W7-level evidence.
- Benchmark scope remains smoke-level: two sizes, one recorded RunPod GPU.
- Lean proves real-valued theorem slices, not Triton/CUDA memory behavior or FP16 numerical equivalence.

## Reroute

- Reroute to `invoke` for a paper-hardening work-pack if the parent refine synthesis chooses execution.
- Reroute to `task-session` for each bounded edit task after the work-pack exists.
- Reroute to `research-evidence-harness` if the parent wants machine-checkable claim-to-evidence linting before presentation.

## Recommended Next Tasks

1. `TASK-PAPER-GUARDS-001`: rewrite stale `NC-008` and `NC-009` in `CLAIM-GUARDS.md` to match the completed softmax coordinate derivative and CAP2 definition/scalar theorem slices while preserving non-claims for full Jacobian/full CAP2 calculus.
2. `TASK-PAPER-REPRO-001`: expand the reproducibility appendix with commands for `pytest`, focused Triton tests, `<cuda-runner-iteration-command>`, `scripts/benchmark_triton_paths.py`, `jq empty`, and `lake build`, including expected pass-count/evidence references.
3. `TASK-PAPER-EVIDENCE-001`: add a theorem-to-claim table connecting formal theorem names to paper sentences, manifest IDs, and non-claims.
4. `TASK-PAPER-FP16-001`: add an FP16 boundary paragraph distinguishing fixed-mask empirical tolerance, CAP2 FP16 status, FP32 accumulation/output behavior, and deferred formal numeric analysis.
5. `TASK-PAPER-ZALLOC-001`: add a CAP2 zero-allocation non-claim/future-work row, separate from fixed-mask W7 zero-allocation evidence.
6. `TASK-PAPER-APPENDIX-001`: add "proves / does not prove" boxes to `MATH-APPENDIX.md` and `DATA-APPENDIX.md`.
7. `TASK-PAPER-INVENTORY-001`: produce an artifact inventory that separates intended evidence files from generated caches and local runtime residue before any share/publish step.
