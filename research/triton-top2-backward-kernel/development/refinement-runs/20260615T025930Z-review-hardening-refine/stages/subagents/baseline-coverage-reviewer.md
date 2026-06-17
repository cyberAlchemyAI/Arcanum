# Baseline Coverage Reviewer Receipt

agent_id: `placeholder-baseline-coverage-reviewer`
role_id: `baseline-coverage-reviewer`
spawn_status: `spawned`
join_status: `completed`
close_status: `closed`
dispatch_id: `refine-20260615T025930Z-review-hardening`
step_id(s): `stage-04-research-decision`, `stage-05-distill`, `stage-06-invoke-design`, `stage-09-invoke-plan`
capability_ref: `refine.subagent.baseline-coverage-reviewer`
status: `flag`
validation_result: `completed-local-inspection-no-code-execution`

## Ownership

This receipt covers the entmax implementation gap, baseline comparison matrix, and CAP2 candidate-kill criteria. It does not modify implementation, tests, paper files, or route manifests.

## Baseline Coverage Finding

Current local coverage is enough for a bounded engineering paper claim, but not enough for a CAP2 novelty claim.

The baseline matrix currently has concrete local evidence for:

| Baseline family | Local status | Evidence |
| --- | --- | --- |
| Fixed-mask Top2 backward | pass | `research/triton-top2-backward-kernel/WORK-PACK.md`, `research/triton-top2-backward-kernel/tests/test_router_reference.py`, `research/triton-top2-backward-kernel/reference/router_reference.py` |
| Soft routing | pass as sanity oracle | `research/triton-top2-backward-kernel/tests/test_router_reference.py`, `research/triton-top2-backward-kernel/reference/router_reference.py` |
| Normalized selected pair | pass as combine-rule comparison | `research/triton-top2-backward-kernel/tests/test_router_reference.py`, `research/triton-top2-backward-kernel/reference/router_reference.py` |
| Sparsemax | pass | `research/triton-top2-backward-kernel/tests/test_router_reference.py`, `research/triton-top2-backward-kernel/reference/router_reference.py` |
| Entmax | gap | `research/triton-top2-backward-kernel/WORK-PACK.md` marks sparsemax pass while entmax remains a named family gap; `research/triton-top2-backward-kernel/FINAL-PRIOR-ART-NOVELTY-REPORT.md` repeats that status. |
| Normalized ReLU / ReMoE-style routing | pass | `research/triton-top2-backward-kernel/tests/test_router_reference.py`, `research/triton-top2-backward-kernel/reference/router_reference.py` |
| Convex sparse top-k / PAV direct mask | partial-pass | `research/triton-top2-backward-kernel/CONVEX-SPARSE-TOPK-JVP-PARITY.md`, `research/triton-top2-backward-kernel/tests/test_router_reference.py`, `research/triton-top2-backward-kernel/tests/test_router_torch.py` |
| Convex sparse top-k normalized masked-softmax | partial | forward composition exists; whole-router backward remains unclaimed per `research/triton-top2-backward-kernel/CONVEX-SPARSE-TOPK-JVP-PARITY.md`. |
| CAP2-v0 | candidate-pass | `research/triton-top2-backward-kernel/CAP2-PRIOR-ART-COMPARISON.md`, `research/triton-top2-backward-kernel/CAP2-W6-PARITY-REPORT.md`, `research/triton-top2-backward-kernel/TRITON-BENCHMARK-REPORT.md` |

## Enough Coverage For Paper Standing

Enough for the current paper standing means:

1. The paper claims CAP2 only as a selected candidate relaxation, not as novel.
2. The baseline table separates implemented baselines from named-but-unimplemented baselines.
3. Every comparison uses the same fixture family or clearly labels when it is only a taxonomy/prior-art comparison.
4. Entmax is either implemented as an executable reference baseline or explicitly moved to a limitation/future-work row.
5. Convex sparse top-k coverage distinguishes mask-level JVP parity from full router backward parity.
6. CAP2 comparisons report support size, row sums, loss terms, capacity-response behavior, backward availability, Triton availability, and zero-allocation/performance status.

Under these criteria, the current package is acceptable for a bounded implementation paper, because `FINAL-PRIOR-ART-NOVELTY-REPORT.md`, `CLAIM-GUARDS.md`, and `PAPER-REVIEW.md` already keep the non-claims visible. It is not acceptable for a novelty paper without the entmax and full-router convex-top-k gaps closed or explicitly scoped out.

## CAP2 Kill / Promote Criteria

Promote CAP2 beyond "candidate only" only if all of the following pass:

1. Entmax baseline is implemented and CAP2 is not trivially dominated on the shared fixtures by entmax in reconstruction loss, sparsity/support behavior, and load response.
2. Convex sparse top-k normalized masked-softmax gets whole-router backward parity or is replaced by a documented reason why mask-level parity is the fair comparison.
3. CAP2 maintains a clear capacity-pressure advantage on probes where overloaded experts should lose weight.
4. CAP2 backward parity remains stable against PyTorch/autograd and finite differences across at least a small sweep of `T`, `E`, `D`, `tau_rank`, `tau_gate`, `tau_cap`, and `mu`.
5. CAP2 Triton remains within an agreed slowdown envelope versus fixed-mask and does not introduce hidden allocation behavior beyond the accepted boundary.
6. Prior-art review can explain why CAP2 is not merely soft-rank / NeuralSort-style gating plus a standard capacity penalty.

Kill CAP2 as a novelty route if any of these occur:

1. Entmax or convex sparse top-k matches or beats CAP2 on the shared fixture suite while offering simpler math, stronger sparsity, or stronger prior-art grounding.
2. CAP2 cannot produce near-top-2 behavior except at temperatures that make gradients unstable or numerically fragile.
3. CAP2's capacity response is explainable as a trivial logit shift with no contribution beyond existing load-penalized soft routing.
4. Full backward validation requires assumptions that the paper cannot state honestly, especially around dynamic load gradients or selection boundaries.

Keep CAP2 as candidate-only if:

1. It remains useful as an engineering relaxation with validated fixed-load backward.
2. It does not yet have novelty evidence.
3. It remains not exactly 2-sparse and not dynamically load-differentiated.

## Artifacts

- This receipt: `research/triton-top2-backward-kernel/development/refinement-runs/20260615T025930Z-review-hardening-refine/stages/subagents/baseline-coverage-reviewer.md`

## Evidence Paths

- `research/triton-top2-backward-kernel/WORK-PACK.md`
- `research/triton-top2-backward-kernel/RELAXATION-CANDIDATES.md`
- `research/triton-top2-backward-kernel/CAP2-CANDIDATE-SPEC.md`
- `research/triton-top2-backward-kernel/CAP2-REFERENCE.md`
- `research/triton-top2-backward-kernel/CAP2-PRIOR-ART-COMPARISON.md`
- `research/triton-top2-backward-kernel/CAP2-W6-PARITY-REPORT.md`
- `research/triton-top2-backward-kernel/CONVEX-SPARSE-TOPK-JVP-PARITY.md`
- `research/triton-top2-backward-kernel/FINAL-PRIOR-ART-NOVELTY-REPORT.md`
- `research/triton-top2-backward-kernel/TRITON-BENCHMARK-REPORT.md`
- `research/triton-top2-backward-kernel/reference/router_reference.py`
- `research/triton-top2-backward-kernel/tests/test_router_reference.py`
- `research/triton-top2-backward-kernel/paper/EVIDENCE-MANIFEST.md`
- `research/triton-top2-backward-kernel/paper/CLAIM-GUARDS.md`
- `research/triton-top2-backward-kernel/paper/PAPER-REVIEW.md`

## Blockers

- Entmax reference implementation is missing.
- Entmax tests and shared-fixture comparison row are missing.
- Convex sparse top-k normalized masked-softmax has no whole-router backward parity claim.
- CAP2 novelty remains unsupported by the local evidence.

## Residue

The current baseline evidence is strong enough to defend the fixed-mask and CAP2 fixed-load implementation story, but the "prior-art baseline matrix" is not balanced enough to defend a stronger novelty story. Entmax is the most visible hole because it is named repeatedly as part of the sparsemax/entmax family while only sparsemax is implemented.

## Reroute

Reroute to `invoke` for a small baseline-hardening work pack if the parent Refine synthesis wants to close this gap before paper release. Reroute to `task-session` if the next move is direct implementation of the entmax reference and tests.

## Recommended Next Tasks

1. Add an entmax reference baseline with a pinned formula/source and tests on the shared fixture.
2. Extend `CAP2-PRIOR-ART-COMPARISON.md` with an entmax row using the same metrics as the existing variants.
3. Add a baseline comparison matrix appendix to the paper package that marks each row as `implemented`, `partial`, `taxonomy-only`, or `future work`.
4. Decide whether convex sparse top-k normalized masked-softmax needs whole-router backward parity for this paper, or whether mask-level parity is enough for the scoped claim.
5. Add a CAP2 kill/promote checklist to the next work pack so future claims cannot drift from candidate-only to novelty without evidence.
