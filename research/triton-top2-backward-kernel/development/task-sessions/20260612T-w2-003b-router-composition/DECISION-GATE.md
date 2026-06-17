# Decision Gate - TASK-W2-003B Router Composition

Status: pass
Date: 2026-06-12

## Target Scope

`TASK-W2-003B`: Decide and implement convex sparse top-k router composition.

## Decision Question

How should the extracted relaxed top-k mask enter the router combine weights?

## Considered Options

1. Use the relaxed mask directly:

```text
A = M_relaxed
```

2. Multiply relaxed mask by softmax probabilities:

```text
A = M_relaxed * softmax(Z)
```

3. Normalize masked softmax probabilities:

```text
A = normalize(M_relaxed * softmax(Z))
```

## Selected Option

The operator selected:

```text
1 AND 3
```

Implementation scope:

- implement option 1 as a mask-direct convex sparse top-k baseline;
- implement option 3 as a normalized masked-softmax convex sparse top-k
  baseline;
- do not implement option 2 in this task-session.

## Rationale

Option 1 keeps a pure prior-art-mask comparison. Option 3 keeps per-token weight
normalization and compares naturally against the existing normalized selected
pair variant.

Option 2 remains unselected even though it was previously recommended as closest
to the fixed-mask baseline.

## Remaining Blockers

None for standard-library forward baselines.

PyTorch/custom-JVP parity for the PAV mask remains outside this task and should
be tracked separately before making differentiable-backward claims for the
convex sparse top-k baseline.
