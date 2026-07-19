# Implementation Plan: Distill Execution Evidence

## Objective

Turn the accepted review findings into an accepted, deterministic, non-gameable evidence path
from Distill execution to Invoke handoff, then use that path to replay Workbench without
rewriting history.

## Complexity

Medium. The plan spans multiple lifecycle owners, public canonical contracts, runtime events,
deterministic validation, generated mirrors, fixtures, observability, and Workbench replay.

## Delivery Slices

| Slice | Outcome | Layer | Tasks | Exit Gate |
| --- | --- | --- | --- | --- |
| S-DEE-0 | lifecycle-selected evidence architecture | L0 | TASK-DEE-01 | DEC-DEE-001 accepted or narrowed |
| S-DEE-1 | deterministic evidence substrate discriminates valid from fabricated runs | L0 | SWU-DEE-002 through SWU-DEE-005, SWU-DEE-008, SWU-DEE-010 | positive passes; isolated and combined fabrication blocks |
| S-DEE-2 | Invoke modes consume validator-owned evidence and deferred modes fail closed | L1 | SWU-DEE-006, SWU-DEE-007, SWU-DEE-009 | canonical mode fixtures pass |
| S-DEE-3 | generated surfaces and Workbench replay agree without history rewrite | L2 | TASK-DEE-06, TASK-DEE-07 | parity and replay checks pass |
| S-DEE-4 | integrated closeout proves contract, fixtures, mirrors, replay, and boundaries | L2 | TASK-DEE-VERIFY | independent closeout evidence |

## Ordered Algorithm

1. Spellcraft adjudicates `DEC-DEE-001` and returns an acceptance/narrowing receipt.
2. Translate the accepted architecture into schemas for request, events, receipt, and result.
3. Implement event resolution for both true-subagent and role-simulation paths.
4. Implement semantic validation in fail-closed order:
   1. parse/schema;
   2. request/receipt/run identity;
   3. event existence and ordering;
   4. role-path consistency and role separation;
   5. finite rounds and termination;
   6. categorized objections and reconciliation coverage;
   7. technique activation/skips;
   8. reviewed-input provenance under the accepted mechanism;
   9. cross-artifact verdict, gap, work-pack, and count agreement;
   10. derive mutation handoff eligibility.
5. Prove discrimination with a resolvable positive, isolated one-corruption-at-a-time
   semantic/provenance negatives, and one combined fail-closed integration negative.
6. Compose active Invoke mode contracts with common evidence handles; make deferred Invoke
   modes return `unsupported/deferred` before lifecycle work.
7. Add the missing-evidence fixture and run the full Invoke fixture suite.
8. Regenerate installed runtime mirrors and prove canonical parity.
9. Replay Workbench against the current eleven-SWU package, append a superseding record, and
   recalculate handoff eligibility from the validator result.
10. Run integrated verification and inventory/observability closeout.

## Failure Modes

| Failure | Required Behavior |
| --- | --- |
| Lifecycle rejects architecture | stop; preserve proposal and rejection residue |
| Receipt parses but events do not resolve | block with event diagnostics |
| Same invocation identity appears for both true-subagent roles | block |
| Simulation claims native agent identities | block |
| Objection lacks category or reconciliation | block or owned flag only if accepted contract permits |
| Reviewed-input provenance is stale or insufficient | block |
| Receipt and Invoke/Workbench counts disagree | block |
| Generated mirrors drift | block canonical rollout and replay |
| Workbench replay fails | preserve history; append blocked result; do not route Task Session |

## Validation Strategy

- JSON Schema validation for each accepted evidence shape.
- Deterministic semantic validator unit tests.
- One resolvable positive fixture.
- One missing-evidence negative fixture.
- Isolated schema-complete fabricated-evidence negatives plus one combined fail-closed witness.
- Existing Invoke validation fixture suite.
- Canonical/generated parity checks.
- Workbench eleven-SWU count and input-provenance checks.
- JSON/JSONL parse and append-only history checks.
- `git diff --check` and public/private boundary scan.

## Ownership And Handoff

Invoke authored this plan. `spellcraft` owns `SWU-DEE-001` and subsequent Invoke spell
lifecycle changes. Any Distill source change routes through `sigil-development`. Accepted
implementation SWUs may then route one at a time through `task-session`.
