# W4 PO-004/PO-005 Validation

Task: `TASK-W4-002`

Status: `manual-and-numeric-pass`

This artifact validates the two targeted proof obligations without expanding the
claim beyond the fixed-mask V0 graph in `FORMAL-MATH-SPEC.md`.

## Scope

The validation assumes:

- `M` is a fixed saved top-2 mask;
- `f_j` is fixed with respect to `P`;
- `H = FFN(X)` is precomputed expert output for this proof slice;
- all identities are real-number / finite-sum identities;
- no claim is made about hard `Top2` differentiability, FP16, Triton memory
  behavior, or full FFN backward.

## PO-004 - Auxiliary Gradient Into P

Given:

```text
L_aux = gamma * E * sum_j f_j * ((1/T) * sum_t P_tj)
```

Expand the mean:

```text
L_aux = gamma * E * sum_j f_j * (1/T) * sum_t P_tj
```

For one coordinate `P_t0j0`, all expert summands with `j != j0` are constant.
Inside the `j0` summand, all token terms with `t != t0` are constant. The only
remaining coefficient multiplying `P_t0j0` is:

```text
gamma * E * f_j0 / T
```

Therefore:

```text
dL_aux/dP_tj = gamma * E * f_j / T
```

Executable evidence:

```text
tests/test_router_reference.py::FixedMaskReferenceTests::test_auxiliary_gradient_into_p_matches_constant_coefficient
```

That test perturbs one `P_tj` coordinate in the auxiliary term and checks the
finite-difference slope against `gamma * E * f_j / T`.

## PO-005 - Router Weight Gradient

Given:

```text
Z_tj = sum_d X_td * W_jd
```

For one coordinate `W_j0d0`:

```text
dZ_tj/dW_j0d0 = X_td0   when j = j0
dZ_tj/dW_j0d0 = 0       when j != j0
```

Reverse accumulation over all token logits gives:

```text
dL/dW_jd = sum_t dL/dZ_tj * X_td
```

Executable evidence:

```text
tests/test_router_reference.py::FixedMaskReferenceTests::test_manual_d_w_matches_finite_difference
```

That existing test compares `fixed_mask_manual_backward()["d_w"]` against a
finite-difference oracle over `W`.

## Verdict

`PO-004` and `PO-005` are manually validated for the fixed-mask V0 graph and
covered by standard-library finite-difference tests. This does not prove any
Triton implementation, zero-allocation behavior, FP16 tolerance, CAP2 novelty,
or gradient through hard top-2 selection.
