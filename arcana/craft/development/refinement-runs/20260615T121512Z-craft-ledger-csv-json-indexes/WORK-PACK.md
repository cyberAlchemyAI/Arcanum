# WORK-PACK: Craft Ledger Projection Layer

## Purpose

Implement generated JSON and CSV projection support for Craft without weakening
YAML ledger authority.

## Control Fields

| Field | Value |
| --- | --- |
| workPackGateStatus | flag |
| activeLayerWindow | L0 |
| currentExecutionTarget | `SWU-CLP-001` |
| blockedMutationScope | import-writeback, generated-runtime-refresh, publication |
| blockedPublicationScope | commit, push, parent-gitlink |

## Task Status Board

| Task | Goal | Layer | Status |
| --- | --- | --- | --- |
| `TASK-CLP-001` | Add projection contract. | L0 | planned |
| `TASK-CLP-002` | Add public-safe fixture. | L1 | planned |
| `TASK-CLP-003` | Add build/validate tooling. | L2 | planned |
| `TASK-CLP-004` | Add import dry-run. | L3 | planned |
| `TASK-CLP-005` | Refresh mirrors and publication gates. | L4 | blocked |

## SWU Manifest

| SWU | Goal | Write Scope | Verification |
| --- | --- | --- | --- |
| `SWU-CLP-001` | Add projection contract to schema/docs. | `arcana/craft/templates/ledger.schema.yml`, `arcana/craft/README.md`, `arcana/craft/SKILL.md` | grep for projection contract and YAML authority language. |
| `SWU-CLP-002` | Add toy fixture with expected projections. | `arcana/craft/fixtures/` | YAML/JSON parse and CSV header checks. |
| `SWU-CLP-003` | Add `craft-index build` and `validate`. | `arcana/craft/scripts/` | fixture generation and stale detection. |
| `SWU-CLP-004` | Add `import-csv --dry-run`. | `arcana/craft/scripts/` | dry-run patch plan blocks unsafe edits. |
| `SWU-CLP-005` | Refresh runtime mirrors and publication checks. | generated runtime packages | `git diff --check`; parent `make bump-check`. |

## Execution Rules

- Start with exactly one SWU.
- Do not enable writeback before dry-run fixture proof.
- Do not hand-edit generated projections.
- Do not publish the parent gitlink until the public submodule commit is pushed.
