# Work Pack Proposal - W6 CAP2 Exact Backward

Status: `proposal`

## Task Matrix

| Task ID | Wave | Objective | Dependencies | Status | Validation |
| --- | --- | --- | --- | --- | --- |
| TASK-W6-001A | W6 | Implement CAP2 exact-backward reference VJP. | TASK-W3-003,TASK-W5-001 | pass-local | autograd and finite-difference parity |
| TASK-W6-001B | W6 | Implement CAP2 Triton row-local backward for `dZ`, `dX_router`, and `dH`. | TASK-W6-001A | pass-runpod | RunPod Triton parity |
| TASK-W6-001C | W6 | Implement CAP2 Triton `dW` reduction from `dZ`. | TASK-W6-001B | pass-runpod | RunPod `dW` parity |
| TASK-W6-001D | W6 | Close CAP2 W6 contract and unblock benchmark scope. | TASK-W6-001C | pass | W6 parity report and work-pack sync |

## SWU Manifest

| SWU ID | Parent Task | Goal | Validation |
| --- | --- | --- | --- |
| SWU-W6-001A-001 | TASK-W6-001A | Add CAP2 manual VJP helper and outputs. | reference import and local unit tests |
| SWU-W6-001A-002 | TASK-W6-001A | Compare manual VJP against PyTorch autograd. | pytest |
| SWU-W6-001A-003 | TASK-W6-001A | Compare manual `dW` against finite differences. | pytest |
| SWU-W6-001B-001 | TASK-W6-001B | Add Triton CAP2 row forward/intermediate computation. | RunPod focused tests |
| SWU-W6-001B-002 | TASK-W6-001B | Add Triton CAP2 row-local `dZ` VJP. | RunPod focused tests |
| SWU-W6-001B-003 | TASK-W6-001B | Add Triton CAP2 `dX_router` and `dH`. | RunPod focused tests |
| SWU-W6-001C-001 | TASK-W6-001C | Wire CAP2 `dZ` scratch into W5 `dW` reduction. | RunPod parity |
| SWU-W6-001C-002 | TASK-W6-001C | Compare CAP2 Triton `dW` against reference. | RunPod parity |
| SWU-W6-001D-001 | TASK-W6-001D | Write W6 CAP2 parity report. | reviewable artifact |
| SWU-W6-001D-002 | TASK-W6-001D | Update canonical work-pack status. | markdown/json checks |
| SWU-W6-001D-003 | TASK-W6-001D | Unblock or reroute W7 benchmark scope. | work-pack sync |

## Execution Notes

Use one `task-session` per parent task. If a task becomes too large, execute one
SWU at a time and synchronize evidence before continuing.

## Execution Update - TASK-W6-001A

`TASK-W6-001A` passed locally in
`development/task-sessions/20260614T073520Z-w6-001a-cap2-reference-vjp/`.

Validation:

```sh
.venv/bin/python -m py_compile reference/router_torch.py tests/test_router_torch.py
.venv/bin/python -m pytest tests/test_router_torch.py -q
.venv/bin/python -m pytest tests -q
```

Results: `24 passed` for the focused PyTorch suite; `54 passed, 11 skipped` for
the full local suite.

## Execution Update - TASK-W6-001B

`TASK-W6-001B` passed on RunPod in
`development/task-sessions/20260614T073920Z-w6-001b-cap2-row-backward/`.

Validation:

```sh
.venv/bin/python -m py_compile reference/router_triton.py tests/test_router_triton.py
.venv/bin/python -m pytest tests/test_router_triton.py -q
.venv/bin/python -m pytest tests -q
<cuda-runner-iteration-command>
```

Results: RunPod focused Triton suite `14 passed`; RunPod full suite `67 passed`.

## Execution Update - TASK-W6-001C

`TASK-W6-001C` passed on RunPod in
`development/task-sessions/20260614T074112Z-w6-001c-cap2-dw-reduction/`.

Validation:

```sh
.venv/bin/python -m py_compile reference/router_triton.py tests/test_router_triton.py
.venv/bin/python -m pytest tests/test_router_triton.py -q
.venv/bin/python -m pytest tests -q
<cuda-runner-iteration-command>
```

Results: RunPod focused Triton suite `15 passed`; RunPod full suite `68 passed`.

## Execution Update - TASK-W6-001D

`TASK-W6-001D` passed by writing `CAP2-W6-PARITY-REPORT.md`, synchronizing
`WORK-PACK.md`, and making `TASK-W7-003` ready.
