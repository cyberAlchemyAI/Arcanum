# Open Residue

The tower is closed for standard source-backed understanding. Four empirical or
governance questions remain deliberately open.

| ID | Residue | Why still open | Needed evidence | Next owner route |
| --- | --- | --- | --- | --- |
| OR1 | Reproduce the 92.0% LongMemEval result | Public surfaces disagree on 50 versus 500 questions; per-run traces are request-only. | Pinned harness revision, exact config, full inputs, answers, retrieval traces, judge outputs, and repeated run summary | `research-evidence-harness` |
| OR2 | Reproduce the 93.2% LoCoMo categories 1–4 result | Category exclusion and judge configuration are stated, but per-run artifacts are not public. | Pinned dataset revision, filters, prompts, judge protocol, raw outputs, and variance | `research-evidence-harness` |
| OR3 | Test validated compaction fidelity and cost | The validator and preservation score are proprietary. | Declared invariants, adversarial fixtures, token accounting, false-accept/false-reject rates, and drift across repeated compactions | `research-evidence-harness` |
| OR4 | Consider any vocabulary or runtime adoption | Research artifacts have no promotion authority. | Separate owner decision, collision analysis, definitions governance, fixtures, and explicit promotion effect | governed promotion route |

## Handoff Trigger

Do not extend this tower with invented benchmark conclusions. Route to
`research-evidence-harness` when a future question depends on measured latency,
token efficiency, context-rot resistance, compaction fidelity, or score
adjudication.
