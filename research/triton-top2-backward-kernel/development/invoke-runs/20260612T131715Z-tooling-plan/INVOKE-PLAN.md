# Invoke Plan - Add Necessary Tools

Status: pass
Date: 2026-06-12

## Target

`research/triton-top2-backward-kernel`

## Intent

Plan the tools needed to unblock the Triton Top2 backward challenge after W0
showed the local environment lacks PyTorch, pytest, Triton, and a visible NVIDIA
runtime.

## Output

- `TOOLING-PLAN.md`

## Decision

Use a two-track tool strategy:

1. CPU reference/TDD tooling with `uv`, `pytest`, `numpy`, `hypothesis`, and
   CPU PyTorch.
2. GPU/Triton tooling only on a CUDA-capable host or container.

This keeps W1-W3 unblocked by local CPU tooling while preserving the honest
blocker for W5-W7 GPU kernel validation.

## Next Route

`task-session` should execute `TASK-W0-004` from the updated work pack:

```text
Add isolated dependency manifests and environment check tests.
```
