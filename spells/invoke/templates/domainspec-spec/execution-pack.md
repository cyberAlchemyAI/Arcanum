# Execution Pack: {module-name}

## Purpose
Execution-first planning manifest for medium/high complexity DomainSpec work. Plan-stage companion to the DomainSpec template family. Single-document for small scope; split into waves + task files for larger scope.

## Planning Control Fields
| Field | Value | Notes |
| --- | --- | --- |
| planningGateStatus | pass or block | Must be pass before mutation-capable stages. |
| complexity | low, medium, or high | Current complexity level. |
| baselineWave | W0 | Mandatory first wave for medium/high complexity. |
| activePlanRef | {path} | Current wave or plan reference. |
| workPackManifest | ../work-pack.md | Standalone invoke companion. |
| layeringArtifact | ../implementation-layering.md | Standalone invoke companion. |
| specRef | SPEC.md | The DomainSpec feature spec this plan executes. |
| activeLayerWindow | L0, L1, L2, or L3 | Primary layer focus for current slice. |
| lastPlannedAt | {iso-timestamp} | Last planning update time. |
| readinessProfile | pilot, release-candidate, production | Completion target profile. |

## Task Board
| Task ID | Goal | Layer | Complexity | Waves | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-A | {goal summary} | L0–L3 | medium | W1, W2 | ready | not-started |
| TASK-VERIFY | Completion verification | L2/L3 | high | W3+ | ready-after-implementation | not-started |
| TASK-AUDIT-ALIGNMENT | Spec↔code alignment audit (DomainSpec audit-alignment) | L2/L3 | high | W3+ | ready-after-mutation | not-started |
| TASK-AUDIT-LAYERING | Domain/orchestration layering audit | L2/L3 | high | W3+ | ready-after-mutation | not-started |

## Wave Rules
- Each wave maps to an L0–L3 layer decision and names the promotion evidence it creates.
- Tasks reference Concept Registry IDs and aspect-doc anchors from `SPEC.md` — no concept invented at plan stage.
- Closure tasks (VERIFY / AUDIT-*) carry SWU exemptions.

## Derivation hooks (DomainSpec)
Where the feature's aspect docs are stable, the M2 capabilities derive obligations automatically — test-derivation (TEST-SPEC), obs-derivation (metric obligations), sync-user-stories (STORIES + coverage). Reference those as validation evidence rather than re-authoring by hand.
