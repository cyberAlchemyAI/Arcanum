---
title: LongMemEval Reproducibility Evidence Harness
status: fixture-ready
selected_unit: OR1
evidence_class: synthetic_fixture
claim_status_effect: none
---

# LongMemEval Reproducibility Evidence Harness

This project-local bundle converts the tower's OR1 residue into deterministic
evidence mechanics. It can validate the shape and integrity of a future
LongMemEval reproduction run; it does not perform that run or support the
paper's reported 92.0% result.

## Selected Unit

- Residue: `OR1`
- Claim binding: `C10`, `R1`, `R2`, `R3`
- Question: can the reported `460 / 500 = 92.0%` LongMemEval result be
  independently reproduced under a pinned, reviewable protocol?
- Current mode: `dry-run + validate + summarize`
- Live execution: not authorized

## Bundle

| Artifact | Role |
| --- | --- |
| [PROTOCOL.md](PROTOCOL.md) | Finite claim, inputs, record types, and adjudication rules |
| [schema/longmemeval-run.schema.json](schema/longmemeval-run.schema.json) | Project-local JSONL row contract |
| [tools/validate_longmemeval_jsonl.py](tools/validate_longmemeval_jsonl.py) | Dependency-free row and cross-row validator |
| [tools/summarize_longmemeval_run.py](tools/summarize_longmemeval_run.py) | Validated-data-only metric and summary renderer |
| [fixtures/passing.synthetic.jsonl](fixtures/passing.synthetic.jsonl) | Synthetic fixture that must pass |
| [fixtures/failing.synthetic.jsonl](fixtures/failing.synthetic.jsonl) | Synthetic fixture that must fail |
| [results/passing-fixture-summary.md](results/passing-fixture-summary.md) | Deterministic fixture-only result summary |
| [CLAIM-ADJUDICATION.md](CLAIM-ADJUDICATION.md) | Claim-update guard and live readiness criteria |
| [data/README.md](data/README.md) | Append-only live-data boundary; contains no run data |
| [VALIDATION.md](VALIDATION.md) | Commands, outputs, and proof ceiling |

## Commands

Run from this bundle directory:

```bash
python3 tools/validate_longmemeval_jsonl.py fixtures/passing.synthetic.jsonl
python3 tools/validate_longmemeval_jsonl.py fixtures/failing.synthetic.jsonl
python3 tools/summarize_longmemeval_run.py fixtures/passing.synthetic.jsonl
```

The first command must exit `0`, the second must exit non-zero, and the third
must exactly reproduce the committed fixture summary.

## Evidence Boundary

Synthetic fixture success proves only that the schema, validator, cross-row
checks, metric arithmetic, summary generation, and claim-status guard behave as
declared. It does not validate Maximem Synap, `gpt-5-mini`, LongMemEval answers,
retrieval quality, judge reliability, or the paper's reported score.
