# Refresh Patch Proposal - W5 Triton dW Bug

Mutation mode: `proposal-only`

## Proposed Work-Pack Delta

Keep `TASK-W5-001` out of `pass` and annotate that the first external RunPod validation failed:

```diff
-| TASK-W5-001 | W5 | Implement Triton fixed-mask `dW` kernel. | TASK-W1-002,TASK-W0-008 | ready | Triton `dW` matches reference |
+| TASK-W5-001 | W5 | Implement Triton fixed-mask `dW` kernel. | TASK-W1-002,TASK-W0-008 | blocked-runpod-bug | First RunPod validation failed: `tl.dot` requires physical M/N/K >= 16 on the pod target, and fixture parity exceeded strict FP32 tolerance. Fix `reference/router_triton.py` and re-run remote validation. |
```

Keep `SWU-W5-001` aligned:

```diff
-| SWU-W5-001 | TASK-W5-001 | Triton fixed-mask `dW`. | ready |
+| SWU-W5-001 | TASK-W5-001 | Triton fixed-mask `dW`. | blocked-runpod-bug |
```

## Proposed Implementation Delta

In `reference/router_triton.py`:

- Use physical tile sizes that satisfy Triton target lower bounds for `tl.dot`, even when logical `E`, `D`, or token block sizes are smaller.
- Mask loads/stores so output remains only `[E, D]`.
- Consider setting `input_precision="ieee"` for FP32 parity if strict reference agreement is required on the fixture.
- Preserve output dtype as `float32`.

In `tests/test_router_triton.py`:

- Stop requesting `block_e=8` or `block_d=8` for a `tl.dot` kernel unless the wrapper rounds them up safely.
- Keep small logical shape tests because they caught the real bug.
- Split strict FP32 parity from approximate FP16/TF32 tolerance expectations.

## Proposed Evidence Delta

In `development/task-sessions/20260614T-w5-001-triton-dw/RESULT.md`, add a RunPod failure section:

```md
## External Validation

RunPod validation failed on 2026-06-14.

- `tests/test_router_triton.py`: 3 failures.
- Primary compile failure: Triton `tl.dot` requires physical `M`, `N`, and `K` dimensions at least 16 on the pod target.
- Numeric fixture failure: maximum absolute difference about `4.2e-05` exceeded `atol=1e-6`.

Status remains `pending-runpod-validation` until the bug-fix continuation passes the pod suite.
```

## Next Route

Run:

```text
[$task-session](<repo>/.agents/skills/task-session/SKILL.md) fix TASK-W5-001 RunPod Triton dW bug using invoke refresh 20260614T070302Z-refresh-w5-triton-dw-bug
```
