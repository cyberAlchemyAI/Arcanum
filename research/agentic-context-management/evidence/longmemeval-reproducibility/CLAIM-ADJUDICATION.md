# Claim-Adjudication Readiness

Claim: `C10` — the source reports `460 / 500 = 92.0%` on LongMemEval.

Current evidence class: `synthetic_fixture`

Current claim effect: `none`

## Mechanical Readiness

| Requirement | Status | Evidence |
| --- | --- | --- |
| Project-local JSONL schema | ready | `schema/longmemeval-run.schema.json` |
| Deterministic validator | ready | `tools/validate_longmemeval_jsonl.py` |
| Passing fixture accepted | ready | Validator pass: 4 rows, 2 question results |
| Failing fixture rejected | ready | Negative control exits 1 with 16 integrity errors |
| Validated-data-only summary | ready | Renderer byte-matches `results/passing-fixture-summary.md` |
| Append-only live-data boundary | ready | `data/README.md` |

## Claim-Bearing Readiness

| Requirement | Status | Blocker |
| --- | --- | --- |
| Exact published-run harness revision | blocked | Paper and public result surface do not expose a confirmed run pin |
| Full official 500-question identity | blocked | Public companion surfaces disagree on 50 versus 500 |
| Original per-question artifacts | blocked | Available on request, not in the checked public repositories |
| Exact model revisions | blocked | Paper gives `gpt-5-mini` alias, not an immutable model revision |
| Live provider authorization | blocked | No credentials, cost approval, or admitted execution unit |
| Independent repeated run | blocked | No live run executed |
| Owner adjudication | blocked | Requires validated live analysis after the above gates |

## Status Rule

`claim_status_update_allowed` is fixed to `false` in the raw evidence schema.
Neither a fixture pass nor a live-data validator pass may update C10. A later,
separately approved analysis owner must compare the pinned protocol, deviations,
raw artifacts, computed metrics, and uncertainty before proposing any claim
change.

## Outcomes

- `fixture-ready`: evidence mechanics work; C10 unchanged.
- `invalid`: run cannot adjudicate C10.
- `matched`: valid protocol-equivalent run yields exactly 460/500; human/owner
  adjudication still required.
- `not-matched`: valid protocol-equivalent run differs; discrepancy analysis
  required, with C10 still unchanged until owner decision.
