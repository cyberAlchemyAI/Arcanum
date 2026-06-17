# Invoke Plan - W6 CAP2 Exact Backward

Mode: `plan`
Complexity: `medium`
Output mode: split local invoke packet plus work-pack proposal.

## Objective

Turn `TASK-W6-001` from a vague selected-relaxation implementation task into
execution-ready SWUs for exact CAP2-v0 backward with fixed load.

## Work Slices

### Slice W6A - Reference Exact Backward

Task: `TASK-W6-001A`

Goal: implement and validate CAP2 manual/reference backward before Triton.

SWUs:

- `SWU-W6-001A-001`: add `cap2_manual_backward` reference helper.
- `SWU-W6-001A-002`: add autograd parity for `dW`, `dH`, and exposed `dZ`.
- `SWU-W6-001A-003`: add finite-difference check for `dW`.

Validation:

```sh
.venv/bin/python -m pytest tests/test_router_torch.py tests/test_router_reference.py -q
.venv/bin/python -m pytest tests -q
```

### Slice W6B - Triton Row Backward

Task: `TASK-W6-001B`

Goal: implement Triton CAP2 row-local backward producing `dZ`, `dX_router`, and
`dH` against the reference.

SWUs:

- `SWU-W6-001B-001`: add Triton CAP2 forward/intermediate row computation.
- `SWU-W6-001B-002`: add Triton row-local VJP for `dZ`.
- `SWU-W6-001B-003`: add Triton `dX_router` and `dH` parity.

Validation:

```sh
<cuda-runner-iteration-command>
```

### Slice W6C - CAP2 dW Reduction

Task: `TASK-W6-001C`

Goal: compute CAP2 `dW = dZ^T @ X` using the validated reduction style.

SWUs:

- `SWU-W6-001C-001`: wire CAP2 `dZ` scratch into existing Triton dW reduction.
- `SWU-W6-001C-002`: compare CAP2 `dW` against reference/autograd on RunPod.

Validation:

```sh
<cuda-runner-iteration-command>
```

### Slice W6D - Contract Closure

Task: `TASK-W6-001D`

Goal: decide whether CAP2 W6 passes, passes-with-scratch, or remains blocked for
zero-allocation optimization.

SWUs:

- `SWU-W6-001D-001`: write CAP2 W6 parity report.
- `SWU-W6-001D-002`: update `WORK-PACK.md` with pass/block status.
- `SWU-W6-001D-003`: unblock or reroute `TASK-W7-003`.

Validation:

```sh
jq empty development/task-sessions/*/evidence-index.json
.venv/bin/python -m pytest tests -q
```

## Implementation Detail

### Manual VJP Algorithm

For each token row:

1. Compute `U`, `P`, `Q`, `Srank`, `G`, `B`, `N`, `A`, `Y`, and residual.
2. Compute `dY`, `dA`, and `dH`.
3. Backprop through `A = B / N`:
   - `C = sum_j dA_j * B_j`;
   - `dB_j = (dA_j * N - C) / N^2`.
4. Split `dB` into `dG` and `dP`.
5. Add auxiliary contribution to `dP`.
6. Backprop softmax into `dU_from_softmax`.
7. Backprop pairwise rank into `dU_from_rank`.
8. Set `dZ = dU_from_softmax + dU_from_rank`.
9. Reduce:
   - `dW = dZ^T @ X`;
   - `dX_router = dZ @ W`.

### Edge Cases

- `tau_rank`, `tau_gate`, `tau_cap` must be positive.
- `epsilon` must be positive.
- `E < 2` is not top-2-shaped; block or reject.
- Pairwise rank diagonal must not contribute.
- Small `E` and `D` must still pass using Triton-safe physical tile sizes.

## Work-Pack Patch Proposal

Replace the single vague W6 row with these rows:

```text
TASK-W6-001A | W6 | Implement CAP2 exact-backward reference VJP. | TASK-W3-003,TASK-W5-001 | ready | autograd and finite-difference parity
TASK-W6-001B | W6 | Implement CAP2 Triton row-local backward for dZ, dX_router, dH. | TASK-W6-001A | pending | RunPod Triton parity
TASK-W6-001C | W6 | Implement CAP2 Triton dW reduction from dZ. | TASK-W6-001B | pending | RunPod dW parity
TASK-W6-001D | W6 | Close CAP2 W6 contract and unblock benchmark scope. | TASK-W6-001C | pending | W6 parity report and WORK-PACK sync
```

## Next Route

`task-session --task TASK-W6-001A`

Do not start Triton CAP2 code until `TASK-W6-001A` passes.
