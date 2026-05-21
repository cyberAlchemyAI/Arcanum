# Codex Goal Profile Work Pack

Status: ready for implementation.

## Purpose

Build the transmutation that converts one Arcanum work-pack task or SWU into a native Codex `/goal` profile.

## Control Fields

| Field | Value |
| --- | --- |
| workPackGateStatus | pass |
| complexity | low |
| outputMode | single-file |
| activeLayerWindow | L0-L2 |
| readinessProfile | pilot |

## Task Board

| Task | Layer | Source | Status | Gate |
| --- | --- | --- | --- | --- |
| [CGP-001](WORK-PACK.md#cgp-001-define-profile-contract) | L0 | [Design](DESIGN.md), [Template](../templates/codex-goal-profile.md) | complete | Profile contract maps SWU fields to native Codex Goal fields. |
| [CGP-002](WORK-PACK.md#cgp-002-author-skill-contract) | L1 | [SKILL](../SKILL.md) | complete | Skill contract names inputs, process, quality bar, anti-patterns, and output contract. |
| [CGP-003](WORK-PACK.md#cgp-003-create-examples) | L1 | [Template](../templates/codex-goal-profile.md), [Examples](../examples/passing.md) | complete | Examples include pass and blocked cases. |
| [CGP-004](WORK-PACK.md#cgp-004-validate-against-goal-swu) | L2 | [Validation](VALIDATION.md), [Invoke Boundary](../../../spells/invoke/development/PLAN-ARTIFACT-BOUNDARIES.md) | complete | One SWU becomes a paste-ready native Codex Goal or blocks honestly. |

## SWU Manifest

| SWU | Parent Task | Source | Dependencies | Write Scope | Done Criteria | Validation | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-CGP-001-001 | [CGP-001](WORK-PACK.md#cgp-001-define-profile-contract) | [Design](DESIGN.md) | none | `transmutations/codex-goal-profile/templates/codex-goal-profile.md` | Template covers outcome, verification, constraints, boundaries, iteration policy, and blocked stop condition. | Review template. | local-fallback |
| SWU-CGP-002-001 | [CGP-002](WORK-PACK.md#cgp-002-author-skill-contract) | [SKILL](../SKILL.md) | CGP-001 | `transmutations/codex-goal-profile/SKILL.md` | Skill contract can generate or block a native Goal profile. | Review skill. | local-fallback |
| SWU-CGP-003-001 | [CGP-003](WORK-PACK.md#cgp-003-create-examples) | [Template](../templates/codex-goal-profile.md) | CGP-002 | `transmutations/codex-goal-profile/examples/` | Passing and blocked examples exist. | Review examples. | local-fallback |
| SWU-CGP-004-001 | [CGP-004](WORK-PACK.md#cgp-004-validate-against-goal-swu) | [Invoke Boundary](../../../spells/invoke/development/PLAN-ARTIFACT-BOUNDARIES.md) | CGP-003 | `transmutations/codex-goal-profile/development/VALIDATION.md` | Validation records that an SWU can become a native Codex Goal profile or block. | Review validation. | local-fallback |

## CGP-001 Define Profile Contract

Define the reusable output template and field mapping.

## CGP-002 Author Skill Contract

Make the transmutation callable as a skill and keep it bounded to profile generation.

## CGP-003 Create Examples

Create one passing profile and one blocked profile.

## CGP-004 Validate Against Goal SWU

Use an Arcanum SWU-style row as test input and confirm the produced `/goal` is auditable.

## Blockers

| Blocker | Status | Rule |
| --- | --- | --- |
| B-CGP-001 | resolved | Native Codex owns runtime goal lifecycle. |
| B-CGP-002 | deferred | Runtime availability check may be manual until Codex version inspection is needed. |

## Next Action

Use the transmutation on the next ready SWU that benefits from native Codex continuation.
