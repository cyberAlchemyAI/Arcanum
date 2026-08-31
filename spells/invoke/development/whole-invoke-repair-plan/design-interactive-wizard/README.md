# Interactive Design Wizard Seed

## Status

This is an inert, resumable design seed. Implementation is deferred until the
current Invoke Design producer fix has been freshly validated. Nothing in this
directory registers a command, changes a schema, starts a session, or alters
the current Design artifact chain.

The future wizard should make Design clarification visible and durable across
both a terminal session and its coordinating chat. It should wrap the existing
stateless deterministic `tools/arcanum invoke design` surface rather than
replace, fork, or weaken it. The deterministic CLI remains the only machine
authoring, production, admission, and status surface.

## Evidence Anchors

- The Invoke contract defines `tools/arcanum invoke` as stateless and
  deterministic and requires one-question clarification when context is
  missing: `spells/invoke/README.md`.
- The Structured Interview Kits contract requires evidence-backed questions,
  exactly one question at a time, an artifact update after a consequential
  answer, and a traceable decision record:
  `arcana/structured-interview-kits/SKILL.md`.
- The current repair frontier and authority ceiling remain governed by
  [WORK-PACK.md](../WORK-PACK.md) and [GAP-LEDGER.md](../GAP-LEDGER.md).
- The wizard must preserve the two-source separation and monotonic artifact
  chain in [PROCESS-DEFINITION.md](../design-process/PROCESS-DEFINITION.md).

## Proposed Boundary

The wizard is a persistent interaction layer around the deterministic Design
pipeline:

```text
terminal view ----\
                   -> canonical question record -> structured decision record
chat view --------/                                 -> draft authoring request
                                                       -> existing stateless CLI
```

Both views must render the same `question_id` and `revision` from the same
canonical question record. They must not maintain separate question banks or
infer that a conversational transcript is a decision. At most one question may
have `active` status in a session. The next question cannot become active until
the current one is answered, explicitly waived when permitted, superseded, or
marked stale.

The future session should persist these structured records:

| Record | Purpose | Authority boundary |
| --- | --- | --- |
| `SESSION.json` | Session identity, target, format version, state, and revision. | Interaction state only. |
| `QUESTIONS.jsonl` | Immutable question revisions and their evidence-backed fields. | Does not decide an answer. |
| `DECISIONS.jsonl` | Selected option or bounded free-form answer, rejected alternatives, rationale, and affected targets. | Records a user decision; does not create approval or reviewer evidence. |
| `EVIDENCE.jsonl` | Exact source refs, digests, observation state, and freshness classification. | Evidence index only; cannot manufacture missing evidence. |
| `EVIDENCE-COVERAGE.json` | Declared historical-evidence boundary and denominator, total classification of discovered refs, coverage digests, evidence gaps, and source-to-question/source-to-draft traces. | Proves coverage only relative to its declared boundary; never repository-global or whole-history completeness. |
| `CHECKPOINT.json` | Last durable revision, active question, evidence snapshot, and next safe action. | Resume cursor only. |
| `DRAFT-REQUEST.json` | Incrementally assembled complete request for the existing deterministic CLI. | Draft input, not a produced or admitted Design. |
| `EVENTS.jsonl` | Operational events such as render, answer receipt, conflict, interruption, or invalidation. | Diagnostic record only. |

Raw terminal or chat transcripts may be retained separately for operator
convenience, but they are never the authority source. A decision becomes
canonical only when a structured decision record is written against the exact
active `question_id`, question `revision`, and session revision.

## Historical Evidence Coverage Contract

Preventing detail loss requires a coverage contract, not only an evidence
index. `EVIDENCE-COVERAGE.json` should declare a finite selected boundary before
questions are formed. That boundary should identify the target, source roots,
selectors, required evidence classes, relevant session or thread locators,
time or revision bounds when applicable, discovery methods, and explicit
out-of-scope rules. The resulting denominator is every evidence reference
discovered under those declared rules.

Every denominator reference must have exactly one current classification:

- `included` with the exact source identity and digest;
- `explicitly_excluded` with a reason and the rule authorizing exclusion;
- `stale` with the newer or missing identity that prevents current use;
- `unavailable` with the failed locator or access reason; or
- `conflicting` with all known incompatible refs and the unresolved issue.

Coverage is complete only when every discovered denominator reference is
classified and every required evidence class is represented or recorded as a
blocking gap. That statement is always relative to the declared boundary. The
wizard must never claim repository-global completeness, whole-history
completeness, or knowledge of evidence outside that boundary.

The coverage record should bind at least a boundary digest, denominator digest,
classification digest, and traceability digest. Each included source must map
to every canonical question it informed and every draft request field it
supports. Conversely, each evidence-backed question and draft field must point
back to its source refs. Unused included evidence remains visible rather than
being silently dropped.

Conversation compaction, a missing prior thread, a truncated handoff, or an
unreadable historical source is an evidence gap. The expected ref is classified
`unavailable` with the loss reason and affected questions or draft fields. The
wizard must not reconstruct missing details from inference, a partial summary,
or an unbound transcript and present them as recovered evidence.

## Canonical Question Record

Each question revision should contain, at minimum:

- `question_id`, `session_id`, `revision`, `stage`, and `status`;
- the prompt and concise context;
- why the answer matters;
- a recommended default only when evidence makes one safe;
- bounded choices or an explicitly typed free-form answer contract;
- evidence references and the evidence snapshot digest;
- the relevant boundary, denominator, classification, and traceability digests
  from `EVIDENCE-COVERAGE.json`;
- source-to-question trace refs for every evidence-backed assertion;
- target JSON pointers or decision records affected by the answer;
- the unresolved effect if unanswered.

The terminal and chat renderers may format that record differently, but neither
may change its meaning, choices, recommendation, evidence, or identity.

## Session Boundaries

### Resume and interruption

- Persist the question and checkpoint before presenting the question.
- Persist a valid structured answer and its checkpoint before selecting the
  next question.
- An interrupt leaves the session resumable from the last complete checkpoint;
  it does not discard an active question or synthesize an answer.
- Resume verifies the session format, target identity, session revision, and
  evidence snapshot and relevant coverage digests before displaying the active
  question again.

### Conflict

- Every mutation uses an expected session revision.
- An answer for a non-active question, stale question revision, or already
  advanced session must fail closed and preserve both submitted information
  and the canonical record without overwriting either.
- If terminal and chat submit competing answers, the second submission becomes
  a visible conflict requiring explicit reconciliation; arrival order alone
  must not silently settle a semantic disagreement.

### Staleness

- Evidence changes recompute the evidence snapshot.
- Boundary, denominator, classification, or traceability changes recompute the
  applicable coverage digests.
- A changed relevant source marks affected unanswered questions and prior
  decisions stale and invalidates dependent draft fields.
- Stale decisions are never silently reused. The wizard reopens the earliest
  affected question and records why.

### Finalize

Finalize must block while any consequential question is active or unanswered,
any required decision is stale or conflicted, evidence identity has changed,
the draft request is incomplete, any required evidence is missing or
unclassified, any evidence conflict is unresolved, a required evidence class
is represented only by a compaction or thread-loss gap, or required owner or
independent evidence is absent. It must also verify bidirectional
source-to-question and source-to-draft-field coverage against the bound
traceability digest. A successful wizard finalization may only freeze a
complete request for the existing deterministic CLI. It cannot claim Design
production, admission, acceptance, registry release, runtime readiness,
execution, publication, or deployment.

## Non-Operative Command Sketch

These commands are design placeholders only. They are not registered and must
not be run as if implemented:

```text
tools/arcanum invoke design wizard start --request <draft-request> --session-root <path>
tools/arcanum invoke design wizard next --session <session-id>
tools/arcanum invoke design wizard answer --session <session-id> --question <question-id> --expected-revision <n> --answer <record>
tools/arcanum invoke design wizard status --session <session-id>
tools/arcanum invoke design wizard resume --session <session-id>
tools/arcanum invoke design wizard finalize --session <session-id> --output <complete-request>
```

## Post-Fix Resume Criteria

Implementation planning may resume only when all of the following are true:

1. The current Design producer fix has a fresh passing validation over its
   exact post-fix bytes and its declared real consumers.
2. The Design process definition and deterministic CLI contracts used by this
   seed are re-read from the validated post-fix baseline.
3. Any changed Design stages, request fields, evidence identities, or authority
   boundaries are reconciled into a new wizard candidate rather than assumed
   compatible.
4. Session storage location, record schemas, chat bridge ownership, conflict
   policy, historical-evidence boundary ownership, coverage classification and
   traceability rules, privacy policy, and cleanup/retention policy receive
   explicit design decisions.
5. Implementation has its own bounded work unit, acceptance checks, and
   independent review; this seed is not that authorization.

Until those conditions hold, the next route is deferred Design-wizard
refinement after the current producer repair, not runtime implementation.

## Explicit Non-Claims

This seed is not a registered schema, accepted Design artifact, implementation
plan, command contract, executable candidate, capability receipt, approval,
independent review, publication request, or deployment instruction. It grants
no authority and changes no current Invoke capability status. It also proves
no repository-global or whole-history evidence completeness.
