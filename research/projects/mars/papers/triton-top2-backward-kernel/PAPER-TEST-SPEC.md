# Paper Test Spec

Status: `complete`

## Obligations

| Test ID | Obligation | Method | Expected |
| --- | --- | --- | --- |
| TST-001 | No hard Top2 differentiability claim appears as a positive claim. | Review `paper.md` against NC-001. | Pass. |
| TST-002 | Exact-backward language is scoped to fixed-mask or CAP2 fixed-load relaxation. | Review abstract, CAP2, conclusion. | Pass. |
| TST-003 | Benchmark values match raw JSON. | Compare `DATA-APPENDIX.md` with EV-DATA-001. | Pass. |
| TST-004 | Lean claims are limited to theorem-specific formal validation: router/fixed-mask identities, finite softmax coordinate derivative, CAP2 definition/slice evidence, and explicit non-claims. | Run `lake build`; inspect formal report. | Pass. |
| TST-005 | Every major paper claim maps to manifest evidence. | Cross-check paper citations against `EVIDENCE-MANIFEST.md`. | Pass. |
| TST-006 | Non-claims are visible before presentation. | Inspect limitations and presentation package. | Pass. |
| TST-007 | Fixed-mask formal proof is named without implying gradients through hard mask selection. | Inspect `FixedMaskBackward.lean`, `FORMAL-VALIDATION-REPORT.md`, and `paper.md`. | Pass. |
| TST-008 | Softmax coordinate derivative is cited as completed finite-softmax theorem evidence without implying hard Top2 differentiability or a packaged full Jacobian theorem. | Inspect `SoftmaxCoordinate.lean`, formal report, evidence manifest, and claim guards. | Pass. |
| TST-009 | CAP2 definition/scalar theorem slices are cited without implying full CAP2 calculus. | Inspect `CAP2Definition.lean`, `CAP2FixedLoadScalar.lean`, and claim guards. | Pass. |

## Reproducibility Command Ladder

| Layer | Environment | Command | Expected Evidence | Interpretation |
| --- | --- | --- | --- | --- |
| CPU reference tests | local Python environment with project test deps | `cd <repo>/research/triton-top2-backward-kernel && .venv/bin/python -m pytest tests/test_router_reference.py tests/test_router_torch.py -q` | PyTorch/reference tests pass locally. | Supports reference/autograd behavior, not Triton parity. |
| Full local test suite | local Python environment; Triton tests may skip without CUDA | `cd <repo>/research/triton-top2-backward-kernel && .venv/bin/python -m pytest tests -q` | CPU tests pass; CUDA-only tests either pass on GPU or skip locally. | Local CPU success does not prove GPU behavior. |
| RunPod CUDA iteration | NVIDIA CUDA/Triton runner with SSH access | `cd <repo>/research/triton-top2-backward-kernel && <cuda-runner-iteration-command>` | Remote probe and tests pass; see RunPod receipts. | Supports CUDA/Triton parity on the recorded runner. |
| Focused Triton tests | inside CUDA runner after upload/bootstrap | `/usr/local/bin/python -m pytest tests/test_router_triton.py -q` | Focused Triton tests pass. | Supports Triton parity for implemented kernels. |
| Benchmark generation | inside CUDA runner | `/usr/local/bin/python scripts/benchmark_triton_paths.py --json-out development/task-sessions/<run>/artifacts/benchmark.json --markdown-out development/task-sessions/<run>/artifacts/BENCHMARK.md` | Benchmark JSON and Markdown are produced. | Supports smoke timing only unless sweep is expanded. |
| Benchmark JSON syntax | local or CUDA runner | `cd <repo> && jq empty research/triton-top2-backward-kernel/development/task-sessions/20260614T074500Z-w7-003-benchmark/artifacts/benchmark.json` | `jq` exits successfully. | Checks data file parseability, not benchmark correctness. |
| Formal build | Lean/Lake environment | `cd <repo>/research/projects/mars/papers/triton-top2-backward-kernel/formal && lake build` | Lean package builds. | Supports theorem-specific real-valued formal claims only. |

## Minimal Required Commands

```bash
cd <repo>/research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

```bash
cd <repo>
jq empty research/triton-top2-backward-kernel/development/task-sessions/20260614T074500Z-w7-003-benchmark/artifacts/benchmark.json
```
