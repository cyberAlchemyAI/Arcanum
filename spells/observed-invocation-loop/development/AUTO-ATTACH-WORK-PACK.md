# Work-Pack: OIL Automatic Runtime Attachment

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Ready for implementation by SWU. |
| complexity | medium | Cross-runtime adapter propagation with generated commands. |
| outputMode | split | Required for medium complexity. |
| implementationPlanRef | `spells/observed-invocation-loop/development/AUTO-ATTACH-IMPLEMENTATION-PLAN.md` | Source plan. |
| defineRef | `spells/observed-invocation-loop/development/AUTO-ATTACH-DEFINE-SPEC.md` | Source define. |
| designRef | `spells/observed-invocation-loop/development/AUTO-ATTACH-DESIGN.md` | Source design. |
| activeLayerWindow | L0-L3 | Full rollout. |

## Objective

Automatically attach Observed Invocation Loop closeout to every generated Arcanum runtime adapter, including installed sigils, and prepare Codex commands as a first-class runtime target.

## Task Status Board

| Task ID | Goal | Layer | Complexity | Gate Status | Status |
| --- | --- | --- | --- | --- | --- |
| T-AUTO-001 | Attachment manifest dry-run | L0 | medium | ready | completed |
| T-AUTO-002 | Template default attachment | L1 | medium | ready-after-T-AUTO-001 | completed |
| T-AUTO-003 | Existing adapter refresh | L2 | medium | ready-after-T-AUTO-002 | completed |
| T-AUTO-004 | Attachment validation | L2 | medium | ready-after-T-AUTO-003 | completed |
| T-AUTO-005 | Codex command adapter support | L3 | medium | ready-after-T-AUTO-004 | completed |
| T-AUTO-VERIFY | End-to-end verification | L3 | medium | ready-after-implementation | completed |

## Smallest Working Units

| SWU ID | Parent Task | Goal | Write Scope | Acceptance Evidence | Verification Command | Status |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-OIL-AUTO-001 | T-AUTO-001 | Generate attachment manifest in dry-run mode. | attachment script/evidence | manifest lists adapters | manifest command | completed |
| SWU-OIL-AUTO-002 | T-AUTO-002 | Add OIL marker to generated templates. | installer templates | generated adapter includes marker | template fixture | completed |
| SWU-OIL-AUTO-003 | T-AUTO-003 | Refresh existing adapters idempotently. | refresh script/installer | second run has no diff | double-run fixture | completed |
| SWU-OIL-AUTO-004 | T-AUTO-004 | Validate attachment coverage. | validator | missing marker fails | validation fixture | completed |
| SWU-OIL-AUTO-005 | T-AUTO-005 | Add Codex command plan/generation. | codex runtime templates | Codex plan includes marker | Codex dry-run fixture | completed |
| SWU-OIL-AUTO-006 | T-AUTO-VERIFY | Verify telemetry after attached pilot. | evidence docs | pilot appends telemetry | adapter pilot command | completed |

## Per-Task SWU Mapping

### T-AUTO-001

## Smallest Working Units

- SWU-OIL-AUTO-001: manifest dry-run

### T-AUTO-002

## Smallest Working Units

- SWU-OIL-AUTO-002: template marker

### T-AUTO-003

## Smallest Working Units

- SWU-OIL-AUTO-003: idempotent refresh

### T-AUTO-004

## Smallest Working Units

- SWU-OIL-AUTO-004: attachment validation

### T-AUTO-005

## Smallest Working Units

- SWU-OIL-AUTO-005: Codex command plan/generation

### T-AUTO-VERIFY

## Smallest Working Units

- SWU-OIL-AUTO-006: end-to-end verification

## Gate Checks

1. Do not overwrite adapter content outside OIL marker blocks without explicit approval.
2. Every installed sigil adapter must be `attached`, `conflict`, or explicitly `exempt`.
3. Codex command support must remain generated from installer/runtime templates.
4. Telemetry proof must come from adapter or deterministic hook path, not a manual observer call.
5. Reflection remains non-mutating.

## Next Implementation SWU

No remaining SWUs in this work-pack. Automatic OIL attachment is ready for review or the next runtime expansion wave.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-05-18 | SWU-OIL-AUTO-001 completed with dry-run attachment manifest command. | Codex |
| 2026-05-18 | SWU-OIL-AUTO-002 completed with OIL marker added to runtime adapter templates. | Codex |
| 2026-05-18 | SWU-OIL-AUTO-003 completed with idempotent GitHub Copilot adapter refresh. | Codex |
| 2026-05-18 | SWU-OIL-AUTO-004 completed with attachment validation and negative fixture. | Codex |
| 2026-05-18 | SWU-OIL-AUTO-005 completed with generated Codex command adapters and bridges. | Codex |
| 2026-05-18 | SWU-OIL-AUTO-006 completed with final attachment validation and telemetry pilot. | Codex |
