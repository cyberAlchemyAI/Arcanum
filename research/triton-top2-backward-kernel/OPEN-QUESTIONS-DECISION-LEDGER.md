# Open Questions Decision Ledger

Purpose: convert open residue into decisions, design requirements, or blockers.

Interrogation run: `development/interrogation-runs/20260612T122502Z-open-questions-gaps/`

## Decision Summary

| ID | Question | Decision | Status | Effect |
| --- | --- | --- | --- | --- |
| R001 | Meaning of leading `W` in `W ||...||^2` | Treat as scalar `lambda_rec` for V0; do not claim original prompt intended this. | decided-for-v0 | Reference tests can proceed with scalar reconstruction weight. |
| R002 | Scope of `FFN(X)` | Treat `H = FFN(X)` as precomputed expert outputs for V0. | decided-for-v0 | Router backward can be isolated from expert FFN backward. |
| R003 | Top-2 combine semantics | Use `A = M * P` for fixed-mask baseline; require a separate decision for normalized pair weights. | decided-for-v0 | Simplifies proof/reference; normalized variant becomes comparison test. |
| R004 | Continuous relaxation identity | Use two tracks: fixed-mask baseline plus CAP2 novelty hypothesis. | partially-decided | Baseline can be tested now; CAP2 requires design before implementation. |
| R005 | Capacity semantics | V0 treats capacity as check/flag, not gradient. CAP2 must be capacity-aware by design. | split-decision | Avoids fake gradients in baseline; creates novelty requirement. |
| R006 | Saved top-2 state | Require saved forward mask/gates for fixed-mask baseline. | decided-for-v0 | Prevents backward recomputation drift and tie ambiguity. |
| R007 | Target GPU/Triton version | Not decided. | blocker-for-performance | Correctness/reference work can proceed; perf/kernel tuning cannot. |
| R008 | Expected relaxation | Assume the challenge expects choosing a relaxation; choose CAP2 as the design hypothesis, with convex sparse top-k and entmax as baselines. | decided-for-design | Next design run can focus on CAP2. |
| R009 | Exact 2-sparsity during training | For CAP2, target top-2-specific sparsity or near-2 active support; record whether exactness holds. | design-requirement | CAP2 must state exact, expected, or asymptotic 2-sparsity. |

## V0 Baseline Contract

This contract is safe to test now:

```text
sigma = softmax
lambda_rec = scalar reconstruction weight
H = precomputed expert outputs
M = saved top-2 mask from forward
A = M * P
f_j = fixed hard load, no gradient through f
capacity = checked/flagged, not differentiated
```

Claim allowed:

```text
Exact backward for the fixed-mask post-selection graph.
```

Claim not allowed:

```text
Exact backward through hard Top2 selection.
```

## CAP2 Design Contract

CAP2 is a hypothesis, not a solution yet.

Working name:

```text
CAP2: Capacity-Aware Pairwise Relaxation for Top-2 Routing
```

CAP2 must define:

1. forward operator;
2. exact backward/Jacobian;
3. capacity/load term;
4. whether support is exactly 2, expected near 2, or sparse-ish;
5. row-local vs batch/global state;
6. proof targets;
7. PyTorch reference;
8. comparisons against fixed-mask, entmax/sparsemax, convex sparse top-k, and ReLU routing.

## Remaining Hard Gaps

| Gap | Why It Remains |
| --- | --- |
| CAP2 operator formula | Not invented yet. |
| CAP2 Jacobian | Depends on the operator formula. |
| Novelty against convex sparse top-k | Must be checked after CAP2 exists. |
| GPU/Triton version | Needed for final kernel and FP16 performance claims. |
| Benchmark acceptance criteria | Needed to know whether sparse-ish training is acceptable. |

## Next Route

Run a design session for CAP2. Completion criterion:

```text
Either produce a precise forward/backward spec for CAP2, or kill it as prior-art-equivalent.
```
