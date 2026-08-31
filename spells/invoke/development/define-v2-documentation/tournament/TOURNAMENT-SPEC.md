# Tournament Protocol

## Experimental Unit

One fresh agent receives one opaque guide, all three task cases, and one empty
trial source directory. It authors exactly three JSON sources and returns a
structured receipt. It does not run the compiler, inspect schemas, view other
candidates, or revise a source after parent scoring.

## Replication And Waves

Six trials run in two waves of three. Each wave contains one alpha, one beta,
and one gamma trial. The waves balance candidate ordering while respecting the
host concurrency limit.

| Wave | Trials | Join |
| --- | --- | --- |
| 1 | alpha-01, beta-01, gamma-01 | all |
| 2 | alpha-02, beta-02, gamma-02 | all |

Wave 2 may start only after every wave-1 agent reaches a terminal join and
close state. A missing or blocked trial makes the tournament incomplete; it is
not silently replaced.

## Blinding

Each agent may read:

- its assigned file under `guides/`;
- `cases/case-01-simple/`;
- `cases/case-02-relations/`;
- `cases/case-03-structural/`;
- its own `runs/<trial-id>/TRIAL.json`;
- its own `runs/<trial-id>/sources/`.

The agent must not read `content/`, `oracle/`, `dispatch/`, `render_candidates.py`,
`build_oracle_sources.py`, `score_tournament.py`, another guide, another trial,
the Invoke schemas/compiler/tests, or any generated scorecard.

This is a governed read policy, not a claim of operating-system sandboxing. A
receipt must disclose any accidental forbidden read; that makes the run
`INVALID` under the criterion.

## First-Attempt Rule

Agents may use ordinary local tools to inspect allowed task files and compute
SHA-256 digests, byte sizes, line spans, headings, JSON pointers, and schema
validity of the supplied structural schema. They may not invoke the Define
compiler or its validators. When all three source files exist, their first
returned bytes are frozen for scoring.

## Root-Owned Scoring

The parent runs `score_tournament.py` after joining all six receipts. The
scorer invokes the canonical v2 compiler against an absent temporary output
directory, checks the intended semantic projection from `oracle/cases.json`,
counts category errors, and writes one re-derivable `SCORECARD.json`.

Timing is not scored because concurrent scheduling and model latency are not a
stable documentation-quality measure.

## Claim Ceiling

A result can compare these three orderings for this model, these cases, this
compiler, and these six first attempts. It cannot authorize a documentation
promotion by itself or establish performance across other agents or schemas.
