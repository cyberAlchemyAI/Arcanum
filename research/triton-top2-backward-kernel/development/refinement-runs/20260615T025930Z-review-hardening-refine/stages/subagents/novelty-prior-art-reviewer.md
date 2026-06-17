# Subagent Receipt - novelty-prior-art-reviewer

agent_id: `<runtime-assigned-placeholder>`
role_id: `novelty-prior-art-reviewer`
spawn_status: `spawned`
join_status: `completed`
close_status: `closed`
dispatch_id: `refine-20260615T025930Z-review-hardening`
step_id(s): `s4`, `s5`, `s9`
capability_ref: `refine/subagent-review`
status: `flag`
validation_result: `completed-local-first-review-with-bounded-source-check; novelty-not-established`

## Scope

Ownership for this receipt:

- CAP2 novelty gap.
- Soft-rank/top-k prior-art comparison.
- Novelty non-claim guard.

Mutation boundary honored: only this receipt file was written.

## Finding

CAP2-v0 should remain framed as a candidate engineering relaxation, not a novel method. The local evidence already reaches this conclusion, and the bounded source check reinforces it.

The strongest defensible statement is:

```text
CAP2-v0 is a selected smooth, fixed-load, capacity-aware relaxation candidate with validated reference and Triton backward parity for its named graph.
```

The statement that is not yet supported is:

```text
CAP2-v0 is a novel differentiable Top2 router.
```

## Local Evidence Summary

Local artifacts already establish the novelty guard:

- `research/triton-top2-backward-kernel/CAP2-CANDIDATE-SPEC.md` says CAP2-v0 is `promoted-candidate-no-novelty-claim`, may be equivalent to or a minor variant of soft-rank/NeuralSort-style relaxations plus capacity-adjusted logits, and does not guarantee exact 2-sparsity.
- `research/triton-top2-backward-kernel/CAP2-PRIOR-ART-COMPARISON.md` compares CAP2-v0 against fixed-mask Top2, normalized selected pair, sparsemax, normalized ReLU, convex sparse top-k direct mask, and convex sparse top-k normalized masked-softmax. It concludes CAP2 survives as a candidate but should not be promoted as novel.
- `research/triton-top2-backward-kernel/FINAL-PRIOR-ART-NOVELTY-REPORT.md` explicitly records the rigorous non-claim: no hard-Top2 differentiability, no CAP2 novelty, no exact 2-sparsity, no dynamic-load gradients, and no production performance claim.
- `research/triton-top2-backward-kernel/paper/CLAIM-GUARDS.md` includes `NC-002`: this package does not claim CAP2 is novel.
- `research/triton-top2-backward-kernel/RELAXATION-CANDIDATES.md` already maps the relevant prior-art families and positions CAP2 near soft-rank, sparse differentiable top-k, sparsemax/entmax, SOFT top-k, Gumbel top-k, and ReLU routing.

## Bounded Source Check

Source-backed prior-art families that must remain in the comparison set:

1. Differentiable sorting and soft-rank relaxations.
   - NeuralSort proposes a continuous relaxation of sorting from permutation matrices to unimodal row-stochastic matrices, enabling gradient-based optimization through sorting-like structure: https://arxiv.org/abs/1903.08850
   - Fast Differentiable Sorting and Ranking constructs differentiable sorting/ranking operators as projections onto the permutahedron with efficient isotonic optimization: https://proceedings.mlr.press/v119/blondel20a.html
   - SoftSort is another continuous argsort relaxation and should be cited if the paper describes CAP2 as pairwise/soft-rank-shaped: https://proceedings.mlr.press/v119/prillo20a/prillo20a.pdf

2. Differentiable top-k relaxations.
   - SOFT top-k approximates top-k through entropic optimal transport and is directly relevant to the "differentiable top-k" framing: https://proceedings.neurips.cc/paper_files/paper/2020/hash/ec24a54d62ce57ba93a531b460fa8d18-Abstract.html
   - Fast, Differentiable and Sparse Top-k proposes differentiable sparse top-k operators via convex analysis and reports use as a sparse MoE router; this is the highest-risk prior-art family for any Top2 novelty claim: https://arxiv.org/abs/2302.01425
   - Differentiable Top-k Classification Learning and `difftopk` provide a broader library/paper context for differentiable sorting/ranking/top-k methods: https://proceedings.mlr.press/v162/petersen22a/petersen22a.pdf and https://github.com/Felix-Petersen/difftopk

3. Sparse probability mappings.
   - Sparsemax is a sparse probability transformation, already implemented locally as a baseline: https://utstat.utoronto.ca/droy/icml16/publish/martins16.pdf
   - Entmax generalizes softmax/sparsemax and is sparse for alpha greater than 1; local coverage is still partial because entmax is named but not implemented: https://aclanthology.org/P19-1146/ and https://github.com/deep-spin/entmax

4. MoE-specific continuous routing alternatives.
   - ReMoE replaces conventional TopK+Softmax routing with a ReLU router and explicitly targets fully differentiable MoE routing: https://openreview.net/forum?id=4D0f16Vwc3
   - Expert Choice routing changes the routing direction so experts choose tokens and capacity is enforced differently; useful as a boundary case rather than a direct CAP2 equivalent: https://proceedings.neurips.cc/paper_files/paper/2022/file/2f00ecd787b432c1d36f3de9800728eb-Paper-Conference.pdf

## What Is Missing Before Novelty Framing

CAP2 cannot be framed as novel until these are done:

1. Formal equivalence or non-equivalence check against NeuralSort/SoftSort/soft-rank style relaxations.
   - CAP2's pairwise sigmoid rank score must be compared algebraically with known soft-rank formulas.
   - The paper needs a table that says whether CAP2 differs in operator, regularizer, capacity coupling, normalization, gradient, or implementation boundary.

2. Direct comparison against convex sparse top-k.
   - The local convex sparse top-k work is partial. It has source-backed mask and parity pieces, but not full composed backward coverage for every router composition.
   - Since convex sparse top-k is sparse and directly top-k-shaped, it is the strongest prior-art challenge to CAP2.

3. Entmax implementation or explicit deferral.
   - The paper currently has sparsemax but not entmax.
   - Because entmax is a known sparse probability family with gradients and exact zeros, leaving it unimplemented weakens any sparse-routing comparison.

4. Exact 2-sparsity result.
   - CAP2-v0 currently uses all three experts on the shared fixture in `CAP2-PRIOR-ART-COMPARISON.md`.
   - Novelty cannot rely on "Top2" unless CAP2 either guarantees exact two active experts, proves an asymptotic top-2 limit, or avoids that claim entirely.

5. Dynamic-load gradient boundary.
   - CAP2-v0 is fixed-load. The capacity adjustment is useful, but no gradient through changing load is claimed.
   - A novelty claim around "capacity-aware differentiable routing" would need either dynamic-load gradients or a precise statement that capacity enters only as fixed-load score adjustment.

6. Broader empirical comparison.
   - The current comparison is a shared fixture plus RunPod parity/smoke benchmarks.
   - A novelty claim would need larger benchmark tasks and side-by-side metrics against sparsemax/entmax, convex sparse top-k, ReLU routing, and fixed-mask baselines.

## Required Non-Claims To Keep

These non-claims should remain in the paper and review package:

- Do not claim CAP2 is novel.
- Do not claim differentiability through hard Top2.
- Do not claim exact 2-sparsity for CAP2-v0.
- Do not claim dynamic-load gradients.
- Do not claim production-optimized performance.
- Do not claim Lean proves CUDA/Triton memory behavior.
- Do not claim convex sparse top-k is new; it is prior art.
- Do not claim entmax comparison is complete until an entmax baseline is implemented or explicitly deferred as out of scope.

## Artifacts

Receipt artifact:

- `research/triton-top2-backward-kernel/development/refinement-runs/20260615T025930Z-review-hardening-refine/stages/subagents/novelty-prior-art-reviewer.md`

Primary local evidence paths:

- `research/triton-top2-backward-kernel/CAP2-CANDIDATE-SPEC.md`
- `research/triton-top2-backward-kernel/CAP2-PRIOR-ART-COMPARISON.md`
- `research/triton-top2-backward-kernel/FINAL-PRIOR-ART-NOVELTY-REPORT.md`
- `research/triton-top2-backward-kernel/RELAXATION-CANDIDATES.md`
- `research/triton-top2-backward-kernel/CONVEX-SPARSE-TOPK-JVP-FEASIBILITY.md`
- `research/triton-top2-backward-kernel/CONVEX-SPARSE-TOPK-JVP-BLOCKED.md`
- `research/triton-top2-backward-kernel/development/decision-gates/20260612T-w3-003-cap2-decision/DECISION.md`
- `research/triton-top2-backward-kernel/paper/CLAIM-GUARDS.md`
- `research/triton-top2-backward-kernel/paper/EVIDENCE-MANIFEST.md`

External source URLs checked:

- `https://arxiv.org/abs/1903.08850`
- `https://proceedings.mlr.press/v119/blondel20a.html`
- `https://proceedings.mlr.press/v119/prillo20a/prillo20a.pdf`
- `https://proceedings.neurips.cc/paper_files/paper/2020/hash/ec24a54d62ce57ba93a531b460fa8d18-Abstract.html`
- `https://arxiv.org/abs/2302.01425`
- `https://proceedings.mlr.press/v162/petersen22a/petersen22a.pdf`
- `https://github.com/Felix-Petersen/difftopk`
- `https://utstat.utoronto.ca/droy/icml16/publish/martins16.pdf`
- `https://aclanthology.org/P19-1146/`
- `https://github.com/deep-spin/entmax`
- `https://openreview.net/forum?id=4D0f16Vwc3`
- `https://proceedings.neurips.cc/paper_files/paper/2022/file/2f00ecd787b432c1d36f3de9800728eb-Paper-Conference.pdf`

## Blockers

- No CAP2 novelty proof or prior-art non-equivalence proof exists.
- Entmax is not implemented locally.
- Convex sparse top-k full router-composition backward remains partially blocked/deferred.
- Exact 2-sparsity is not proven and is contradicted by the local shared fixture for CAP2-v0.
- Dynamic-load gradients are out of current CAP2 scope.

## Residue

- CAP2 may still be valuable as an engineering contribution if framed as a compact fixed-load continuous relaxation with Triton parity, but that is not the same as method novelty.
- The paper should treat prior-art comparison as a claim guard, not as decoration.
- If the team wants a "novel solution" attempt, the most promising direction is not to overclaim CAP2-v0; instead, design a next version whose distinguishable property is explicit and testable, such as exact/sparse support control plus capacity-aware differentiable load coupling.

## Reroute

Recommended route: `invoke` a focused novelty-comparison work-pack before any paper wording upgrade.

Suggested route target:

```text
research/triton-top2-backward-kernel/development/invoke-runs/<timestamp>-cap2-novelty-comparison/WORK-PACK.md
```

## Recommended Next Tasks

1. Create `CAP2-NOVELTY-COMPARISON-MATRIX.md` comparing CAP2 against NeuralSort, SoftSort, Fast Differentiable Sorting/Ranking, SOFT top-k, convex sparse top-k, sparsemax, entmax, and ReMoE.
2. Implement or explicitly defer entmax with a paper-visible reason.
3. Add a small algebra note: `CAP2-SOFT-RANK-EQUIVALENCE-CHECK.md`, with formulas and verdicts for equivalence, partial overlap, or unknown.
4. Add a small fixture suite for CAP2 temperature limits: active count, mass outside top-2, gradient stability, and capacity response.
5. Keep `NC-002` and related non-claims in `CLAIM-GUARDS.md` until the comparison matrix and equivalence check are complete.
6. If novelty is still desired, design CAP2-v1 only after the matrix identifies a specific gap not already covered by soft-rank, convex sparse top-k, entmax, or ReLU routing.
