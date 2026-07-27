# Implementation Plan: Distill Runtime-Event Emission

## Objective

Implement the missing Distill-owned runtime-event producer, direct-run
telemetry, and evidence-emission status; prove both role paths; update
readiness truthfully; regenerate runtime profiles from canonical sources.

## Complexity

Medium. The change spans a sigil lifecycle, runtime event ledger behavior,
observability, two execution paths, generated packages, and cross-capability
validation. Output mode is split.

## Delivery Slices

| Slice | Outcome | Layer | Units | Exit Gate |
| --- | --- | --- | --- | --- |
| S-DRE-0 | one accepted event is emitted append-only | L0 | DRE-001 | positive append passes; schema/digest failures block |
| S-DRE-1 | both role paths emit complete resolvable sequences | L1 | DRE-002, DRE-003 | true-subagent and simulation suites pass with one shared shape |
| S-DRE-2 | direct telemetry and emission status are truthful | L2 | DRE-004, DRE-005 | direct dedupe and status matrix pass |
| S-DRE-3 | canonical readiness reflects runtime evidence | L2 | DRE-006 | full canonical suite passes; gap close is evidence-bound |
| S-DRE-4 | generated profiles reproduce canonical behavior | L3 | DRE-007, VERIFY | parity, public boundary, and integrated closeout pass |

## Ordered Implementation

1. Sigil Development accepts `DEC-DRE-001` and selects `SWU-DRE-001`.
2. Add the Distill runtime emitter with schema validation and optimistic-digest
   append; prove one event and fail-closed negatives.
3. Wire and validate the complete true-subagent boundary sequence.
4. Wire and validate the complete role-simulation boundary sequence.
5. Resolve both ledgers through the existing Invoke consumer and compare role
   boundary shapes.
6. Add a direct Distill observer helper and exactly-once direct signal fixtures.
7. Add evidence-emission status to Distill closeout/telemetry, including
   configured failure and non-required states.
8. Update canonical validation/readiness and close `GAP-DEE-002` only when
   integrated evidence is present.
9. Regenerate Codex and Claude Distill mirrors from the canonical sigil.
10. Run integrated closeout, public-boundary scan, link validation, JSON/JSONL
    parsing, and scoped diff checks.

## Failure Modes

| Failure | Required Behavior |
| --- | --- |
| accepted schema is absent for an evidence-gated run | emission status `not-configured`; handoff remains blocked |
| event schema or run identity fails | no append; deterministic diagnostic |
| ledger digest changed | no append; caller must re-read before retry |
| true-subagent roles share one invocation ID | evidence blocks |
| role simulation claims native IDs | evidence blocks |
| partial sequence exists | preserve ledger; status `partial`; handoff blocks |
| direct signal repeats one run ID | observer dedupes |
| invoked run uses direct helper | helper blocks before append |
| canonical validation fails | no readiness or gap closure |
| mirror parity fails | no runtime-profile completion claim |

## Validation Strategy

- shell/Python syntax checks;
- JSON Schema validation against the accepted Invoke event schema;
- single-event append and digest-race negatives;
- complete true-subagent and role-simulation sequence fixtures;
- same-ID, invented-ID, missing-boundary, sequence, and run/path drift negatives;
- existing event resolver, semantic, provenance, and active-mode suites;
- direct telemetry record/dedupe and invoked-route rejection;
- evidence-emission status matrix;
- Distill semantic non-regression assertions;
- isolated bootstrap and exact generated parity;
- complete Distill execution-evidence closeout;
- Markdown links, public-boundary scan, and `git diff --check`.

## Ownership And Handoff

Invoke owns this plan only. Sigil Development owns acceptance and canonical
Distill mutation. The Invoke lifecycle remains owner of the accepted evidence
consumer. Bootstrap owns generated projection after canonical validation.
Implementation proceeds one selected SWU at a time.
