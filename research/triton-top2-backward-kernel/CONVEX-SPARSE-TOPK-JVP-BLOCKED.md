# Convex Sparse Top-k JVP/Backward Blocker

Status: feasibility-pass-implementation-decision-needed
Date: 2026-06-12

## Task

`TASK-W2-003C`: Add differentiable/JVP-backed convex sparse top-k parity or
blocked report.

## Gate Verdict

Blocked for implementation. Blocked report produced.

The tower now has a source-backed standard-library forward extraction for the
official PAV p=4/3 sparse soft top-k mask and two selected router compositions:

```text
A = M_relaxed
A = normalize(M_relaxed * softmax(Z))
```

That is sufficient for forward fixture comparison. It is not sufficient to
claim a differentiable end-to-end backward through the PAV mask.

## Why This Is Blocked

The local extraction in `reference/router_reference.py` is intentionally a
small standard-library CPU oracle. It computes the relaxed mask values, but it
does not expose a PyTorch graph or a source-backed custom VJP/JVP for the PAV
partition operation.

The primary-source research pack points at the official Google Research
implementation, where the exact PAV path is implemented with JAX custom VJP
and Numba-backed routines. Porting that backward into this tower requires
extracting and validating the derivative behavior, not guessing it from the
forward code.

## Missing Inputs

Before this baseline can be used as differentiable backward evidence, pin:

1. the exact VJP or JVP contract for `sparse_soft_topk_mask_pav` with p=4/3;
2. the active-block/partition derivative behavior produced by PAV;
3. the tie and support-boundary policy for gradient tests;
4. a PyTorch implementation route, either `torch.autograd.Function` or a
   differentiable adapter whose derivative is source-backed;
5. finite-difference or official-implementation oracle fixtures for gradients
   with respect to router scores;
6. whether both selected router compositions need backward parity, or whether
   one composition is the official comparison target.

## Non-Claims

- Do not claim hard Top2 differentiability.
- Do not claim Triton backward readiness for convex sparse top-k.
- Do not claim CAP2 novelty against convex sparse top-k backward behavior.
- Do not treat the current standard-library PAV extraction as a differentiable
  PyTorch operator.

## Allowed Current Use

The current convex sparse top-k artifacts may be used for:

- source-backed forward mask checks;
- forward comparison of selected router compositions;
- support-size, sparsity, and hard-top-k-limit fixture behavior;
- deciding whether CAP2 is worth comparing further.

They may not be used for:

- end-to-end differentiable parity claims;
- exact backward-kernel requirements;
- zero-allocation Triton derivative claims.

## Unblock Action

Add a new extraction task:

```text
TASK-W2-003D: Extract source-backed PyTorch/custom-JVP parity for convex sparse top-k PAV.
```

Done criteria:

- source-backed VJP/JVP notes from the official implementation or paper;
- PyTorch score-gradient parity on non-boundary fixtures;
- finite-difference or official oracle comparison;
- explicit support-boundary/tie skip policy;
- clear statement of which selected router composition is covered.

## Feasibility Update

`TASK-W2-003D-RG` found a source-backed implementation route for a narrow
PyTorch custom-autograd parity oracle. See
`CONVEX-SPARSE-TOPK-JVP-FEASIBILITY.md`.

This changes the blocker from "missing derivative evidence" to "implementation
scope decision needed."
