# OR1 LongMemEval Reproducibility Protocol

Protocol version: `0.1.0`

Status: `fixture-ready; live-blocked`

## Objective

Capture enough immutable run evidence to distinguish:

1. re-analysis of the author's original run artifacts;
2. an independent run under a protocol-equivalent configuration;
3. a non-equivalent run that must not adjudicate the reported result.

The target claim is the paper's reported `460 / 500 = 92.0%` on the full
`LongMemEval_S` distribution.

## Source Pins

| Source | Pin | Meaning |
| --- | --- | --- |
| Paper PDF | `sha256:107f18872b8f58c6992c3ff8ac1beb0b08131bcdb4622cc2fdcd4701f40f77e0` | Tower's primary-source identity |
| Checked public harness | `1dbbcfe025d64c84146ff4c316ed492c5fb760de` | Companion revision observed by the tower; not proven to be the published run revision |
| Checked results repository | `6d9754245eec3e8c29e053cb15d04ea57fd41ef5` | Companion results revision observed by the tower |
| Published run harness revision | unresolved | Must be resolved before a claim-bearing live reproduction |

## Live Protocol Lock

A claim-adjudication candidate must declare and capture:

- `LongMemEval_S`, official full distribution, exactly 500 unique questions;
- category counts: 70 single-session-user, 30 single-session-preference,
  78 knowledge-update, 133 temporal-reasoning,
  56 single-session-assistant, and 133 multi-session;
- dataset revision and ordered question-set SHA-256;
- exact harness commit and results-repository commit;
- provider/adapter revision and complete configuration hash;
- retrieval mode and isolation mode;
- exact answer-model and judge-model identifiers, not mutable aliases;
- answer, judge, retrieval, and query prompt hashes;
- raw retrieved-context, answer, and judge-artifact references plus hashes;
- one `question_result` row per question;
- one derived `run_summary` row whose counts exactly match the question rows;
- every protocol deviation, including retries, skipped questions, or manual
  intervention.

The paper names `gpt-5-mini` for both answer and judge roles. A future run must
also record the exact available model revision; the alias alone is insufficient
for reproducibility.

## Record Sequence

Each JSONL file owns one run and is append-only:

```text
record 0             one run_manifest
records 1..N         N unique question_result rows
record N+1           one run_summary
```

The validator requires contiguous record indices, non-decreasing timestamps,
one run ID, one evidence class, unique question IDs, manifest/summary agreement,
and recomputed overall/category metrics.

## Fixture Profile

The passing fixture uses two synthetic questions so mechanics can be tested
without copying benchmark data or calling a provider. Synthetic fixtures must:

- use `evidence_class=synthetic_fixture`;
- use synthetic provider/model identifiers;
- keep `claim_status_update_allowed=false` on every row;
- never be written under `data/` as live evidence.

## Adjudication Outcomes

| Outcome | Mechanical condition | Claim consequence |
| --- | --- | --- |
| `matched` | Valid live run, protocol equivalence accepted, exactly 460/500 | Eligible for separate human/owner adjudication; no automatic claim update |
| `not-matched` | Valid live run, protocol equivalence accepted, score differs | Eligible for separate discrepancy analysis; no automatic claim update |
| `invalid` | Integrity failure, unresolved source pin, protocol deviation that breaks equivalence, or missing raw artifact | Cannot adjudicate the claim |
| `fixture-ready` | Synthetic pass and negative-control rejection | Mechanics only; claim status unchanged |

## Live Blockers

1. The exact harness revision used for the paper's run is not established.
2. The checked harness/results surfaces disagree on 50 versus 500 questions.
3. Original per-question answers, retrieved contexts, and judge verdicts are
   request-only.
4. Credentials, provider authorization, cost approval, and live-run ownership
   are absent from this unit.
5. No task-session has admitted live execution.
