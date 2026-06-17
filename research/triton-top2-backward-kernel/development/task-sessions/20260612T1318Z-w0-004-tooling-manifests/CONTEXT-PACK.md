# Task Session Context - W0-004 Tooling Manifests

Date: 2026-06-12
Work pack: `research/triton-top2-backward-kernel/WORK-PACK.md`
Task: `TASK-W0-004`
SWU: `SWU-W0-004`

## Controlling Context

- `WORK-PACK.md` marks `TASK-W0-004` ready.
- `TOOLING-PLAN.md` requires CPU and GPU dependency manifests plus a fast
  environment gate test.
- W0 prior evidence says PyTorch, pytest, Triton, and NVIDIA runtime are missing
  from the active Python environment.

## Write Scope

- `requirements-cpu.txt`
- `requirements-gpu.txt`
- `tests/test_environment.py`
- local generated-file ignore rules
- task-session evidence and synchronized W0 rows

## Validation

- `python3 -m unittest discover -s research/triton-top2-backward-kernel/tests -v`
- `jq empty` on the task-session evidence index.
