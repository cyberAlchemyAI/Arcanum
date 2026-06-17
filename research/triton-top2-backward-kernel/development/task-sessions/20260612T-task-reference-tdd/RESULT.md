# Task Session Result - Reference/TDD/Math Validation Scaffold

Task: first implementation-readiness task from
`development/invoke-runs/20260612T123402Z-baselines-tdd-math-validation/RUNTIME-HANDOFF.md`

Result: `PASS`

## Decisions

| Decision | Selection | Reason |
| --- | --- | --- |
| Runtime | local | No runtime delegation needed for this bounded scaffold. |
| Test framework | `unittest` | `pytest` is not installed locally. |
| Tensor backend | standard-library Python | `torch` is not installed locally. |
| Scope | V0 fixed-mask plus soft-routing baseline | Matches handoff and avoids Triton/CAP2 overreach. |

## Context Pack

Context pack: `CONTEXT-PACK.md`

Strict coverage: `pass-with-substitution`

Substitution:

PyTorch-specific autograd/gradcheck is deferred because `torch` is not installed.
The session implemented a pure Python oracle plus finite-difference validation.

## Files Updated

- `reference/__init__.py`
- `reference/router_reference.py`
- `tests/test_router_reference.py`
- `FORMAL-MATH-STUBS.md`
- `CONTEXT-PACK.md`
- `RESULT.md`
- `evidence-index.json`

## Validation

```bash
python3 research/triton-top2-backward-kernel/reference/router_reference.py
```

Result:

```text
loss=1.227485799788
max_abs_diff_manual_vs_fd_dW=8.037905757652e-11
```

```bash
python3 -m unittest discover -s research/triton-top2-backward-kernel/tests -v
```

Result:

```text
Ran 9 tests
OK
```

```bash
python3 -m py_compile \
  research/triton-top2-backward-kernel/reference/router_reference.py \
  research/triton-top2-backward-kernel/tests/test_router_reference.py
```

Result: `pass`

## Completion Criteria

| Criterion | Status |
| --- | --- |
| Tests can be run locally | pass |
| V0 fixed-mask baseline is a working oracle | pass |
| No test claims hard Top2 differentiability | pass |
| Next CAP2 design gap is explicit | pass |

## Follow-Up

1. Install or select an environment with PyTorch.
2. Add PyTorch autograd/gradcheck parity against the pure Python oracle.
3. Add entmax/sparsemax or another prior-art baseline.
4. Run CAP2 design-or-kill before any novelty claim.
5. Start Triton only after reference parity and target GPU/Triton version are known.
