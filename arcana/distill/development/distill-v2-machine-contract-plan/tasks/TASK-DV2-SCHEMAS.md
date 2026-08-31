# TASK-DV2-SCHEMAS — Eight-Schema Machine Grammar

## Objective

Create separately reviewable Draft 2020-12 grammars with positive and
mutation-negative fixtures. This task proves representation only, not a complete
executable semantic run.

## Entry Gate

TASK-DV2-DECISIONS has one selected, independently reviewed digest; source
anchors and every create/modify target have fresh baselines.

## Shared Rules

- Closed objects by default; explicit `$id`; repository-local `$ref` closure.
- `distill-common-v2` contains structural primitives only.
- Every SWU runs schema meta-validation, one positive fixture, unknown-field and
  type/enum mutation negatives, exact changed inventory, and `git diff --check`.
- A partial schema family is not advertised as usable until SWU-DV2-007 PASS.

## SWU-DV2-001

Behavior: prove one TechniqueSpec slice end to end.

Write scope: `schemas/distill-common-v2.schema.json`,
`schemas/distill-technique-spec-v2.schema.json`,
`profiles/v2/techniques/abstraction_level_guard.json`, the technique schema
fixtures, and the schema-fixture runner/tests.

Acceptance: canonical underscore ID, allowed type/hook/activation/input/output/
failure fields validate; unknown ID form, forbidden hook, missing trace output,
unknown field, and semantic content in common primitives reject.

## SWU-DV2-002

Behavior: define finite ModeSpec grammar.

Write scope: `schemas/distill-mode-spec-v2.schema.json` and its fixtures.
Acceptance: finite default/max tracks and rounds, role program, pitch-off,
human-gate, cycle, and closeout fields validate; unbounded and closure-owning
mode mutations reject.

## SWU-DV2-003

Behavior: define exact-reference Profile grammar.

Write scope: `schemas/distill-profile-v2.schema.json` and its fixtures.
Acceptance: profile accepts exact mode/technique refs and composition policy;
embedded ModeSpec/TechniqueSpec definitions reject.

## SWU-DV2-004

Behavior: define complete normalized RunFrame/source grammar.

Write scope: `schemas/distill-source-v2.schema.json` and its fixtures.
Acceptance: every input group in `SCHEMA-PLAN.md` is represented; missing intent,
discovery, profile binding, revision lineage, or invalid exact refs reject.

## SWU-DV2-005

Behavior: define append-only semantic trace-event grammar.

Write scope: `schemas/distill-trace-event-v2.schema.json` and its fixtures.
Acceptance: setup, proposal, objection, reconciliation, technique, round,
termination, and verdict-candidate variants are discriminated; mutable summary,
unknown event, or authority-bearing event rejects.

## SWU-DV2-006

Behavior: define substantive ResultEnvelope grammar.

Write scope: `schemas/distill-result-v2.schema.json` and its fixtures.
Acceptance: complete SKILL output fields and `authority_effect: none` validate;
structural verdict/selected-unit/route contradictions reject.

## SWU-DV2-007

Behavior: define exact stage-receipt grammar and prove the eight-schema denominator.

Write scope: `schemas/distill-stage-receipt-v2.schema.json`, receipt fixtures,
and aggregate schema-runner coverage.

Acceptance: producer/finalizer/schema identities, exact inventory, validation
state, atomic publication, and explicit receipt digest method validate; missing
or self-referential digest law rejects; all eight schemas/fixtures pass together.

## Receipt And Successor

One receipt per SWU records accepted decision digest, baselines, changed bytes,
commands, denominator counts, authority ceiling, and successor. SWU-DV2-007 may
route only to SWU-DV2-008; it does not claim configuration or runtime readiness.
