# Craft Validation Examples

## Purpose

This companion explains the candidate example suite in `CRAFT-VALIDATION-EXAMPLES.yml`.

The YAML file is the structured authority. This Markdown file is the readable walkthrough for reviewers and later task-session runs.

## Coverage Summary

| Example | Claim | Expected Result | Recomposition Target |
| --- | --- | --- | --- |
| EX-001 | SCU selection | pass | `CRAFT-ARCHITECTURE.md#Validation Example-Suite Shape` |
| EX-002 | SWU planning | pass | `CRAFT-ARCHITECTURE-WORK-PACK.md#Task Status Board` |
| EX-003 | Residue classification | flag | `CRAFT-ARCHITECTURE-INPUTS.md#Runtime Boundary Contract` |
| EX-004 | Recomposition | pass | `CRAFT-ARCHITECTURE-WORK-PACK.md#Delivery Slices` |
| EX-005 | Blocker refinement gate | pass | `LEDGER-VALIDATION.md#Blocker Lifecycle Review` |
| EX-006 | Cross-context relation | pass | `LEDGER.md#Relation Rows` |
| EX-007 | Route boundary | pass | `CRAFT-ARCHITECTURE.md#Route Integration Contract` |
| EX-008 | Runtime side-thread boundary | pass | `CRAFT-ARCHITECTURE-INPUTS.md#Non-Blocking Runtime Statement` |
| EX-009 | Promotion decision | flag | `CRAFT-PROMOTION-READINESS.md` |
| EX-010 | Role-hint review | pass | `CRAFT-ARCHITECTURE.md#Deferred Automation Evidence` |

## Examples

### EX-001: SCU Selection

Broad Craft architecture work could expand into examples, validation, promotion, runtime integration, scoring, generated indexes, or role delegation. Craft should select the validation example suite as the next Smallest Coherent Unit because it is the smallest unit that still recomposes into the architecture acceptance gate.

### EX-002: SWU Planning

The architecture-to-plan step decomposes example creation into ordered SWUs. `SWU-CRAFT-ARCH-002`, `SWU-CRAFT-ARCH-003`, and `SWU-CRAFT-ARCH-004` each have dependencies, write scope, done criteria, validation, and handoff notes.

### EX-003: Residue Classification

If validation finds that runtime observation-envelope capture is still unproven, Craft should classify that as runtime side-thread residue. It is a flag, not a local validation blocker, when the owner artifacts are cited and no runtime mutation is claimed.

### EX-004: Recomposition

After example creation passes, the examples must reconnect to the parent architecture by unlocking the validation guide task. The file existing is not enough; the task-session result should record coverage, validation, and the next recomposition target.

### EX-005: Blocker Refinement Gate

`BLK-RAW-RELATION-001` remains active and raw with `blocker_refiner` as primary lane. That demonstrates the shortcut is blocked: raw blockers do not resolve directly unless refined or explicitly waived.

### EX-006: Cross-Context Relation

`REL-BLOCKS-002` and `BLK-SCORING-001` show a relation across contexts: schema readiness blocks priority scoring. The context tree alone cannot express that relation, so the ledger records it explicitly.

### EX-007: Route Boundary

When a bounded task is executable, Craft recommends `task-session` and records outcome evidence. It does not take over task-session's authority for context building, gates, mutation, validation, or evidence synchronization.

### EX-008: Runtime Side-Thread Boundary

Runtime/refine strategy and skill runtime interface work are relevant to Craft, but they remain owned by separate artifacts. Craft may cite them as external dependencies, but it must not mutate commands, runtime adapters, registries, sigils, spells, or skills.

### EX-009: Promotion Decision

Local validation can justify a promotion readiness review. It does not promote Craft automatically. The readiness review must compare actual evidence against the architecture's promotion checklist and recommend a future route.

### EX-010: Role-Hint Review

Type plus lane can suggest responsibility, but it is still a review hint. Role delegation automation waits for broader example coverage and explicit authority.

## Non-Goals Preserved

- No runtime mutation.
- No registry mutation.
- No promotion mutation.
- No scoring implementation.
- No generated index implementation.
- No role delegation automation.
