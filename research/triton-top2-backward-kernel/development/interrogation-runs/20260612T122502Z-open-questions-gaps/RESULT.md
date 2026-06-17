# Interrogation Result - Open Questions And Gaps

Status: `pass`

## Final Synthesis

We can decide enough to move. The correct split is:

```text
V0 baseline = test now
CAP2 novelty hypothesis = design next
Triton kernel = later
```

The V0 baseline is not novel, but it is rigorous and safe. CAP2 is the possible
novel direction, but it must survive prior-art comparison before we believe in it.

## Decided For V0

- Use `lambda_rec` for the ambiguous leading `W`.
- Treat `FFN(X)` as precomputed `H`.
- Use saved top-2 mask/gates.
- Use `A = M * P`.
- Treat `f_j` as fixed for the auxiliary gradient.
- Treat capacity as check/flag, not gradient.

## Decided For Design

- Explore CAP2: `Capacity-Aware Pairwise Relaxation for Top-2 Routing`.
- CAP2 must be top-2-specific, proof-first, capacity-aware, and kernel-friendly.
- CAP2 must compare against entmax/sparsemax, convex sparse top-k, ReLU routing,
  and fixed-mask Top2.

## Still Open

- CAP2 forward formula.
- CAP2 exact backward/Jacobian.
- Whether exact 2-sparsity is required during training.
- Target GPU/Triton version.
- Benchmark acceptance criteria.

## Next Action

Run a CAP2 design pass whose explicit goal is:

```text
Define the operator or kill it as prior-art-equivalent.
```
