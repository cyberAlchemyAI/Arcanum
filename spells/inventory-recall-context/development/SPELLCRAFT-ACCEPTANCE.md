---
spell: inventory-recall-context
status: accepted-for-candidate-development
accepted_at: 2026-08-07
authority_effect: none
---

# Spellcraft Acceptance

## Decision

Spellcraft accepts `inventory-recall-context` as the canonical local path for
candidate development at:

`spells/inventory-recall-context/`

The accepted unit is a spell because it composes existing Inventory and Context
Builder capabilities with a candidate-owned current-source verifier, derived
injection gate, and receipt boundary. The internal operation/type name is
`VerifiedRecallTurn`; it is not a second spell identity or alias.

Acceptance does not register, install, generate, promote, release, deploy, or
prove the runtime.

## Preflight receipt

| Check | Result | Evidence |
| --- | --- | --- |
| canonical ID | pass | `inventory-recall-context` is kebab-case |
| candidate path | pass | target was absent before initialization |
| canonical collision | pass | no exact canonical ID or alias collision in `registry/SPELLS.md` |
| required Inventory contract | pass | `arcana/inventory/SKILL.md` exposes `lookup` |
| required Context Builder contract | pass | `transmutations/context-builder/SKILL.md` exposes strict lean runtime handoff |
| complete spell contract | pass | `../README.md` carries required lifecycle fields |
| Experiment Harness | pass for initialization | standard `spellcraft` profile exists under this directory |
| runtime/reuse evidence | flag | no native output or timestamped validation report exists |

The bounded preflight helper performed read-only identity, dependency, registry,
and harness checks. The parent owns this acceptance decision and final claims.

## Accepted boundary

Included for L0 preparation:

- explicit request intake;
- Inventory lookup packet validation;
- current path/selector/digest verification;
- strict lean Context Builder pack contract;
- derived fail-closed injection decision;
- a receipt for allowed and denied outcomes;
- positive, stale, missing, contradictory, unsafe, over-budget, and
  blocked-index scenarios.

Excluded:

- daemon, automatic prompt/session hook, cache, embeddings, vector store,
  ranking optimization, writeback, post-run attachment, durable model memory,
  network transport, installation, generated host mirrors, registry change,
  promotion, publication, deployment, and production operation.

## Ownership

| Concern | Owner | Candidate responsibility |
| --- | --- | --- |
| discovery/read model | Inventory | consume its current lookup contract; never rewrite it |
| context selection/packaging | Context Builder | consume strict lean handoff; never redefine its pack semantics |
| source truth | owning current source | verify and retain source handles; never elevate Inventory summaries |
| composition lifecycle | Spellcraft | own this contract, harness, lifecycle state, and promotion gates |
| bounded implementation | Task Session | execute at most one selected SWU after admission |
| experiment mechanics | Experiment Harness | validate harness shape and later collect real outputs/reports |

## Acceptance gates

- Candidate lifecycle acceptance: **pass**.
- Design authored completeness: **pass** with a two-pass fixed point in
  `DESIGN-SELECTION-RESULT.json`.
- Work Pack preparation: **pass** for `WP-IRC-L0-001`.
- Execution-entry projection: **selection-ready** for `SWU-IRC-001`; no unit
  is selected.
- Task Session admission: **not granted**.
- Runtime behavior: **not proven**.
- Reusable-spell promotion: **blocked** until real native runs and harness
  evidence satisfy Spellcraft.

## Claim ceiling

This artifact supports only: “Spellcraft accepted a bounded candidate identity,
owner boundary, and L0 preparation scope.” It does not support “agent memory is
built,” “the runtime works,” or “the spell is reusable/released.”
