# Open Residue

| ID | Residue | Why It Matters | Resolution |
| --- | --- | --- | --- |
| R001 | Meaning of leading `W` in `W ||X - ...||^2`. | Changes reconstruction gradient scale and may imply weighted norm. | Ask requester or inspect benchmark prompt if available. |
| R002 | Exact shape and meaning of `FFN(X)`. | Determines whether kernel returns `dH`, `dX`, expert parameter gradients, or only router gradients. | Decide scope before implementation. |
| R003 | Top-2 combine semantics. | Masked probabilities and renormalized selected probabilities have different backward equations. | Specify `A = M*P` vs `A = M*P/sum(M*P)`. |
| R004 | Continuous relaxation identity. | "Exact backward" depends on the chosen relaxation. | Pick fixed-mask, soft top-k, sparsemax/entmax-like, Gumbel/perturbation, or straight-through. |
| R005 | Capacity constraint semantics. | Hard constraints do not produce gradients without projection or penalty. | Choose check, enforce, penalty, or barrier. |
| R006 | Whether top-2 indices/gates are saved from forward. | Recomputing top-2 in backward can diverge under ties or stochastic routing. | Save indices/gates or define deterministic recomputation contract. |
| R007 | Target GPU and Triton version. | Block sizes, atomics, FP16 behavior, and supported features vary by hardware/backend. | Capture environment before performance work. |
| R008 | Which continuous relaxation is the challenge expecting us to choose? | This is likely part of the challenge, not a side detail. Different relaxations imply different exact backward kernels and proof targets. | Compare candidates in `RELAXATION-CANDIDATES.md`; choose one named relaxation before implementation. |
| R009 | Is exact 2-sparsity required during training, or is sparse-ish differentiable routing acceptable? | Entmax/sparsemax may be sparse but not exactly two active experts; convex top-k/SOFT top-k are more top-k-shaped but heavier. | Ask benchmark owner or run candidate references side by side. |

## Interrogation Update - 2026-06-12

See `OPEN-QUESTIONS-DECISION-LEDGER.md`.

Resolved for V0 baseline:

- R001: use `lambda_rec` as scalar reconstruction weight.
- R002: treat `FFN(X)` as precomputed expert outputs `H`.
- R003: use `A = M * P` for fixed-mask baseline.
- R005: capacity is check/flag only in V0.
- R006: require saved forward top-2 mask/gates.

Still open for CAP2/design:

- R004/R008: exact continuous relaxation identity.
- R009: exact 2-sparsity vs sparse-ish training.
- R007: target GPU/Triton version for performance/kernel claims.
