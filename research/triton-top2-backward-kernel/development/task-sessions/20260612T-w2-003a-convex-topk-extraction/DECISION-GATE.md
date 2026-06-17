# Decision Gate - Convex Sparse Top-k Router Composition

Status: blocked
Date: 2026-06-12

## Target Scope

`TASK-W2-003B`: Decide and implement convex sparse top-k router composition.

## Blocker Question

How should the extracted relaxed top-k mask enter the router combine weights?

## Options

1. Use the relaxed mask directly:

```text
A = M_relaxed
```

Benefit: closest to the sparse soft top-k mask source.
Cost/risk: no longer uses the prompt's `softmax(Z)` probability semantics.
Choose when: comparing pure convex sparse top-k as a standalone router.

2. Multiply relaxed mask by softmax probabilities:

```text
A = M_relaxed * softmax(Z)
```

Benefit: closest to the original fixed-mask baseline shape, replacing hard mask
with relaxed mask.
Cost/risk: active weights need not sum to one; behavior mixes two probability
maps.
Choose when: preserving the original prompt structure matters most.

3. Normalize masked softmax probabilities:

```text
A = normalize(M_relaxed * softmax(Z))
```

Benefit: keeps selected support and per-token weight normalization.
Cost/risk: adds an extra normalization not directly present in the prompt.
Choose when: comparing against normalized selected-pair routing is important.

## Recommendation

Use option 2 first as the closest analog to the existing V0 fixed-mask graph:

```text
A = M_relaxed * softmax(Z)
```

Then add option 3 as a comparison variant if needed. Do not use option 1 as the
only comparator unless the task is reframed as replacing the router with the
prior-art mask operator itself.
