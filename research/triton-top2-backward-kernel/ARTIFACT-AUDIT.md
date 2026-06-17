# Artifact Audit - Triton Top2 Backward Kernel

Status: `pass-with-warnings`
Date: 2026-06-15

## Purpose

Separate intended challenge evidence from generated, local, private, or unrelated
workspace state before any share, export, or commit.

## Include - Challenge Source And Specs

These files are part of the challenge evidence package:

- `README.md`
- `TOWER.md`
- `WORK-PACK.md`
- `definitions.md`
- `derivation.md`
- `glossary.md`
- `LEARNING-PACK.md`
- `claim-ledger.md`
- `open-residue.md`
- `FINAL-QUESTION-RESOLUTION.md`
- `RIGOR-VALIDATION-MAP.md`
- `SAFE-EXPLANATION-BRIEF.md`
- `FORMAL-MATH-SPEC.md`
- `FORMAL-MATH-STUBS.md`
- `W4-PROOF-NOTES.md`
- `W4-PO004-PO005-VALIDATION.md`

## Include - Implementations And Tests

- `reference/`
- `tests/`
- `scripts/cuda_runner_probe.py`
- `scripts/benchmark_triton_paths.py`
- `<cuda-runner-iteration-command>`
- `requirements-cpu.txt`
- `requirements-gpu.txt`
- `.gitignore`

## Include - Research, Baselines, And Reports

- `PRIOR-ART-MAP.md`
- `RELAXATION-CANDIDATES.md`
- `NOVELTY-SEARCH-MAP.md`
- `CAP2-CANDIDATE-SPEC.md`
- `CAP2-REFERENCE.md`
- `CAP2-PRIOR-ART-COMPARISON.md`
- `CAP2-W6-PARITY-REPORT.md`
- `TRITON-BENCHMARK-REPORT.md`
- `FINAL-PRIOR-ART-NOVELTY-REPORT.md`
- `CONVEX-SPARSE-TOPK-*.md`

## Include - Execution Evidence

Keep task-session, decision-gate, dispatch, invoke, and refinement receipts that
support the challenge. In particular:

- `development/task-sessions/20260614T063208Z-runpod-cuda-probe/`
- `development/task-sessions/20260614T070808Z-w5-001-triton-dw-bugfix/`
- `development/task-sessions/20260614T072022Z-w5-002-triton-dx-dh/`
- `development/task-sessions/20260614T072236Z-w7-001-zero-allocation/`
- `development/task-sessions/20260614T072412Z-w7-002-fp16-tolerance/`
- `development/task-sessions/20260614T073520Z-w6-001a-cap2-reference-vjp/`
- `development/task-sessions/20260614T073920Z-w6-001b-cap2-row-backward/`
- `development/task-sessions/20260614T074112Z-w6-001c-cap2-dw-reduction/`
- `development/task-sessions/20260614T074226Z-w6-001d-contract-closure/`
- `development/task-sessions/20260614T074500Z-w7-003-benchmark/`
- `development/task-sessions/20260614T074650Z-w8-001-final-report/`
- `development/refinement-runs/20260615T025930Z-review-hardening-refine/`

## Exclude - Local Runtime And Caches

Do not include in a public/share package:

- `.venv/`
- `.pytest_cache/`
- `__pycache__/`
- `.mypy_cache/`, `.ruff_cache/`, or similar caches if created later
- generated build outputs

## Review Before Including

- `notebooks/free_cuda_runner_smoke.ipynb`: include only if notebook outputs are
  cleared or intentionally retained.
- `development/runner-bundles/`: private/archive evidence unless explicitly
  needed for reproducibility.
- cloud/runpod runbooks: useful for reproducibility, but review for tokens,
  hostnames, cost notes, or private operational details before public sharing.

## Exclude - Unrelated Parent Worktree State

Do not stage with broad `git add .`. The parent worktree also contains:

- generated Arcanum skill/runtime surfaces under `.agents/`, `.arcanum/`,
  `.claude/`, `.codex/`, and `tools/arcanum`;
- unrelated project work under `redacted private workspace path`, `redacted private workspace path`,
  `projects/domainspec-v2/`, `projects/industrial-bid-brasil/`, and
  `research/jusbrasil-call/`;
- submodule changes under `arcanum` and `implementation/domainspec`;
- other research or operations files outside this challenge package.

## Evidence Manifest Warnings

The MARS paper evidence manifest currently references:

- `research/projects/mars/definitions/MARS-PIPELINE.md`
- `research/projects/mars/definitions/PAPER-DERIVATION-RULES.md`

Those paths should be verified or reconciled before publication because the
visible MARS project definitions live under `research/projects/mars/definitions/`.

## Safe Staging Shape

Use pathspecs, not broad adds:

```sh
git status --short -- \
  research/triton-top2-backward-kernel \
  research/projects/mars/papers/triton-top2-backward-kernel \
  research/projects/mars/development
```

Only after reviewing this audit, stage approved paths explicitly.
