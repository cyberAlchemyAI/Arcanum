# Interactive Design Wizard Implementation Plan

## Outcome

This package plans the fix, but it is not yet an admitted Invoke Plan.

| Field | Value |
| --- | --- |
| Target | Interactive Design wizard |
| Planning state | `blocked-before-plan-v2` |
| Why blocked | The wizard seed is not an admitted Design, and the current Invoke package-closure baseline is not yet fresh. |
| First route | `invoke design` |
| Implementation authority | none |

The plan becomes eligible for deterministic Plan v2 authoring only after a
fresh Wizard Design stage and independent admission receipt exist. Until then,
the waves below are a concrete planning candidate, not an execution candidate.

## Objective

Prevent Design from silently losing useful details from selected historical
evidence. Keep one evidence-backed question durable across process restarts and
show the same canonical question in the terminal and coordinating chat. Turn
accepted answers into a complete draft request for the existing deterministic
Design CLI without inventing architecture, approval, or reviewer evidence.

## Fixed V1 Decisions

1. **The CLI does not invent semantic questions.** The native Invoke agent,
   using Structured Interview Kits, authors a candidate question. The CLI
   validates, persists, orders, and renders it.
2. **There is no direct chat transport in v1.** The native agent calls the same
   CLI, reads the canonical question record, and renders that record in chat.
   Terminal and chat bind the same `question_id`, question revision, session
   revision, evidence refs, and coverage digests.
3. **Session state is always explicit.** Every mutating command receives a
   caller-selected `--session-root`. No home-directory default, daemon, hidden
   cache, network service, or implicit working directory is permitted.
4. **Revisions are immutable.** A command creates one absent revision directory
   containing a complete valid snapshot, then advances a small `HEAD.json`
   pointer atomically. `--expected-revision` rejects stale writers.
5. **Evidence completeness is boundary-relative.** A finite boundary and
   denominator are declared first. Every discovered ref is classified as
   included, explicitly excluded, stale, unavailable, or conflicting.
6. **A transcript is never decision authority.** A decision is effective only
   as a validated record bound to the active question and expected session
   revision.
7. **Finalize is an authoring handoff only.** It may freeze a complete Design
   authoring request and run the existing read-only `check` path. It cannot
   produce, admit, approve, publish, or execute a Design.

## Architecture

```text
declared evidence boundary
  -> deterministic evidence denominator and classifications
  -> evidence coverage and traceability digests
  -> agent-authored candidate question
  -> CLI validation and single-active-question queue
  -> immutable session revision + atomic HEAD pointer
  -> terminal renderer / native-agent chat renderer
  -> revision-guarded structured answer
  -> mapped draft-request fields
  -> existing `invoke design check|author` surface
```

The CLI owns structure, identity, hashing, state transitions, conflict
detection, persistence, and diagnostics. The agent or responsible owner owns
the content of semantic questions and answers.

## Ordered Waves

### W0 — Re-establish the admissible baseline

Purpose: make later implementation planning truthful.

- Re-run the current selective Invoke package preview and classify every
  remaining mixed-owner delta.
- Freeze the exact canonical CLI, stage catalog, Design contracts, generated
  packages, and wizard seed bytes that the new Design will reference.
- Author and independently admit one Wizard Design that selects the session
  model, evidence contract, question lifecycle, v1 chat bridge, privacy
  boundary, and final Design-request handoff.
- Convert this planning candidate into a current
  `invoke.plan-source-v2-authoring-request.v1` bound to that exact stage and
  admission pair.

Gate `G0`: fresh Design/package closure and Wizard Design admission both PASS.
Failure route: remain in `invoke design`; do not create a Plan v2 source.

### W1 — Minimum vertical proof

Purpose: prove the user-visible concept with the smallest coherent unit.

- Add the minimum session, evidence-boundary, evidence-coverage, question,
  answer, decision, checkpoint, and transition schemas.
- Add a deterministic session engine using absent immutable revisions and an
  atomically replaced `HEAD.json` pointer.
- From two local evidence fixtures, classify one source as included and one as
  unavailable; bind their coverage digests to one agent-authored question.
- Show the same canonical question through the terminal result and the native
  agent's chat projection.
- Accept one answer with `--expected-revision`, restart the process, resume the
  session, and prove that one draft Design-request field is frozen.

Gate `G1`: two independent runs produce byte-identical revision contents; the
question ID/revision and coverage digests are identical in terminal and chat
projections; stale revision submission blocks without changing `HEAD.json`.

### W2 — Evidence and session hardening

Purpose: prove that evidence is not silently dropped and concurrent surfaces
cannot corrupt the session.

- Implement total denominator classification, required evidence classes,
  bidirectional source-to-question and source-to-draft-field traceability, and
  unused-included-source reporting.
- Implement source drift invalidation, earliest-dependent-question reopening,
  competing-answer conflicts, interrupted-write recovery, safe symlink/path
  handling, and explicit unavailable-history gaps.
- Add status and resume views that always return the current active question,
  blocking gaps, conflicts, and next safe action.

Gate `G2`: property and mutation tests cover every state transition and
classification. Relevant evidence drift invalidates dependent decisions;
unrelated drift does not.

### W3 — Design authoring bridge

Purpose: connect the durable interview to existing Design authoring without
creating a second producer.

- Map each accepted decision to exact JSON Pointers in a draft Design request.
- Make question selection operate over a validated queue: deterministic
  mechanical gaps first, then agent-authored semantic questions with explicit
  priority and dependencies.
- Add finalize checks for unanswered questions, stale decisions, incomplete
  coverage, conflicts, missing evidence, and incomplete request fields.
- On successful finalize, freeze one complete authoring request and invoke only
  the existing read-only `tools/arcanum invoke design check <stage>` contract.
  A later explicit command may call the existing `author` stage into an absent
  output; the wizard never calls `produce`, `admit`, or `status` implicitly.

Gate `G3`: a complete fixture reaches a byte-stable authoring request accepted
by the existing Design `check` path; every incomplete or stale fixture blocks
before authoring output.

### W4 — Compatibility, documentation, and package closure

Purpose: make the approved behavior available without overwriting unrelated
owner work.

- Document the terminal workflow, native-agent chat rendering contract,
  evidence limits, recovery behavior, and operator-visible diagnostics in
  concrete language.
- Run canonical regression suites for Define, Design, Plan, and Invoke routing.
- Generate Codex and Claude Invoke packages in isolated targets, compare the
  exact dependency-closed wizard delta, and apply only after owner review.
- Run one canary from selected historical evidence through answer, resume,
  finalize, Design `check`, and optional explicit `author` twice.

Gate `G4`: canonical and generated canaries are byte-identical across the
declared outputs, package parity is exact for the allowlist, and no unrelated
canonical or generated bytes change.

## Smallest Working Units

| SWU | Primary behavior | Write boundary | Acceptance boundary |
| --- | --- | --- | --- |
| `SWU-WIZ-000` | Freeze and admit the Wizard Design baseline. | New Design run artifacts only. | Current Design stage and admission pair PASS; no implementation writes. |
| `SWU-WIZ-001` | Prove the complete durable-question loop. | Minimum wizard schemas, engine, CLI/chat projections, and one focused vertical fixture. | Evidence boundary, one canonical question, dual rendering, guarded answer, restart/resume, and one draft field pass together. |
| `SWU-WIZ-002` | Generalize evidence coverage and drift invalidation. | Evidence boundary/coverage contracts and tests. | Every denominator ref has exactly one classification and trace; relevant drift reopens dependents. |
| `SWU-WIZ-003` | Harden concurrency and interrupted-write recovery. | Transition/conflict/recovery code and tests. | Stale or competing answers cannot overwrite the decision; interrupted writes preserve the prior revision. |
| `SWU-WIZ-004` | Queue validated questions and map accepted decisions. | Question queue and draft-mapping code and tests. | Mechanical gaps and agent-authored semantic questions map deterministically to exact request fields. |
| `SWU-WIZ-005` | Freeze a complete draft request and call Design `check`. | Draft mapping/finalize code and integration tests. | Missing evidence or decisions block; complete fixture passes existing check. |
| `SWU-WIZ-006` | Close compatibility and generated-package parity. | Docs, exact generated allowlist, and canary evidence. | Canonical/Codex/Claude behavior agrees without unrelated deltas. |

Each implementation run selects one SWU only. No SWU may inherit mutation,
publication, or execution authority from this planning candidate.

## Expected Future Target Families

These are candidate targets to freeze in W0, not an authorization to create or
modify them now:

- `spells/invoke/schemas/design-wizard-session-v1.schema.json`
- `spells/invoke/schemas/design-wizard-evidence-boundary-v1.schema.json`
- `spells/invoke/schemas/design-wizard-evidence-coverage-v1.schema.json`
- `spells/invoke/schemas/design-wizard-question-v1.schema.json`
- `spells/invoke/schemas/design-wizard-answer-v1.schema.json`
- `spells/invoke/schemas/design-wizard-decision-v1.schema.json`
- `spells/invoke/schemas/design-wizard-checkpoint-v1.schema.json`
- `spells/invoke/schemas/design-wizard-transition-v1.schema.json`
- `spells/invoke/scripts/design_wizard.py`
- `spells/invoke/scripts/invoke_cli.py`
- `spells/invoke/invoke-cli-stage-catalog.json`
- `spells/invoke/design-wizard.md`
- `spells/invoke/development/test_design_wizard.py`
- `spells/invoke/development/test_invoke_cli.py`
- reviewed generated Invoke package counterparts after W4 admission

## Proposed Non-Operative Commands

The final grammar is owned by the admitted Wizard Design. This sketch is not
registered:

```text
tools/arcanum invoke design wizard start --request SESSION-REQUEST.json --session-root ABSENT_DIR
tools/arcanum invoke design wizard evidence-refresh --session-root DIR --request EVIDENCE-REQUEST.json --expected-revision N
tools/arcanum invoke design wizard question-add --session-root DIR --request QUESTION-REQUEST.json --expected-revision N
tools/arcanum invoke design wizard next --session-root DIR
tools/arcanum invoke design wizard answer --session-root DIR --request ANSWER.json --expected-revision N
tools/arcanum invoke design wizard status --session-root DIR
tools/arcanum invoke design wizard resume --session-root DIR
tools/arcanum invoke design wizard finalize --session-root DIR --expected-revision N --output ABSENT_REQUEST.json
```

## Boundaries

- No direct chat API, push channel, daemon, socket, network call, or background
  process is part of v1.
- No question content is inferred by the deterministic CLI.
- No raw transcript is evidence or decision authority.
- No session default or automatic retention cleanup is introduced.
- No existing Define, Design, Plan, or historical schema is rewritten.
- No generated package is synchronized before W4 review.
- No owner request, approval, admission, Task Session selection, execution,
  publication, or deployment is created by this plan.

## Next Route

Start at `SWU-WIZ-000` through `invoke design`. After its exact stage and
admission pair pass, materialize this candidate through the deterministic Plan
v2 authoring, production, and admission chain.
