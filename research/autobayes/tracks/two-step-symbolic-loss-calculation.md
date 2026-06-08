---
profile: autobayes-research
name: Two-Step Symbolic Loss Calculation
description: Worked symbolic closure for local loss composition across two AutoBayes statistical games.
type: worked-example
status: pass
lane: two-step-symbolic-loss-calculation
last_updated: 2026-06-07
promotion_scope: local-research-only
---

# Two-Step Symbolic Loss Calculation

## Source Kind

- AutoBayes paper: section 4, "Composing Complex Loss Functions."
- Local receipt: [local-loss-composition-distill.md](local-loss-composition-distill.md).

## Setup

Take two statistical games:

```text
c : X -> Y
d : Y -> Z
```

Each game has:

```text
Bayesian lens + energy + entropy
```

For `c`:

```text
F^c(pi, y)
  = E_{(x,a) ~ c'_pi(y)} [ l^c(x,a,y) ]
    - H^c(pi,y)
```

For `d`:

```text
F^d(rho, z)
  = E_{(y,b) ~ d'_rho(z)} [ l^d(y,b,z) ]
    - H^d(rho,z)
```

where `rho` is the prior/belief state for `d`.

## Step 1 - Push The Prior Forward

The prior for `d` is not arbitrary. It is:

```text
rho = c_* pi
```

That is the belief over `Y` obtained by pushing `pi` through `c`.

## Step 2 - Downstream Reverse Pass

Evidence arrives at `z`. The downstream inverse reconstructs the intermediate
state under the pushed-forward prior:

```text
(y,b) ~ d'_(c_* pi)(z)
```

This is the state under which upstream loss is averaged.

## Step 3 - Compose Energies

Energy composes additively:

```text
l^(dc)(x,a,y,b,z)
  = l^c(x,a,y) + l^d(y,b,z)
```

Local reading:

```text
cost of upstream explanation
+ cost of downstream explanation
```

## Step 4 - Compose Entropy

Entropy is not just an unindexed sum. It is:

```text
H^(dc)(pi,z)
  = E_{(y,b) ~ d'_(c_* pi)(z)} [ H^c(pi,y) ]
    + H^d(c_* pi,z)
```

The upstream entropy is evaluated under the downstream reconstruction of the
intermediate value. The downstream entropy uses the pushed-forward prior.

## Step 5 - Compose Free Energy

The composite free energy is:

```text
F^(dc)(pi,z)
  = E_{(y,b) ~ d'_(c_* pi)(z)} [ F^c(pi,y) ]
    + F^d(c_* pi,z)
```

This is the key closure:

```text
global free energy
  = expected upstream local free energy
  + downstream local free energy
```

The parent does not add two detached numbers. It composes local losses through
the same state discipline that made inversion lawful.

## Arcanum Reading

```text
Parent synthesis should not invent a global verdict from prose.
It should join local receipts under the state that makes each receipt legal.
```

Arcanum analogy:

- `F^c`: upstream local evidence/objective receipt;
- `F^d`: downstream local evidence/objective receipt;
- `c_* pi`: state namespace carried from upstream declaration into downstream interpretation;
- expectation over `d'`: downstream reconstruction of hidden intermediate evidence.

## Misuse Warnings

- Do not say AutoBayes losses simply add.
- Do not call every Arcanum validation metric a free energy.
- Do not hide the pushed-forward state.
- Do not treat this symbolic example as a numeric proof or implementation algorithm.

## Status

`closed-distill`
