# Remaining Implementation Plan: Observed Invocation Loop

## Implementation Objective

Make OIL runtime-baseline-ready by closing the remaining reliability gaps in managed reflection routing, threshold scoping, dedupe finalization, hook closeout status, and legacy ledger migration.

## Delivery Slices

| Slice | Outcome | Validation |
| --- | --- | --- |
| L0 Reflection route enforcement | Managed closeout paths honor `OBSERVED_REFLECT=off|auto|always`. | Temp fixtures show off skips, auto runs on recommendation, always runs or skips with reason. |
| L1 Threshold scoping | Ordinary thresholds cool after reflection; severe gaps remain immediate. | First threshold writes report; immediate ordinary run does not retrigger from old counters. |
| L2 Atomic dedupe | Dedupe key is committed after successful telemetry append/index/counter path. | Duplicate skips; failed pre-commit path can retry. |
| L3 Status and migration | Stop hook derives status from evidence; migration check avoids anonymous summaries. | Completed, failed, blocked, partial fixtures plus migration check pass. |

## Task Decomposition

| Task ID | Goal | Write Scope | Done When |
| --- | --- | --- | --- |
| T-REM-001 | Add dedupe check/commit modes. | observability hook recorder and observer | duplicate suppression no longer commits before append path. |
| T-REM-002 | Scope threshold evaluation and reflection state. | observer and reflector | reports update `last_reflection_at`; ordinary thresholds count recent rows. |
| T-REM-003 | Route reflection from managed closeout. | `tools/arcanum`, Codex Stop hook scripts | closeout returns reflection status according to `OBSERVED_REFLECT`. |
| T-REM-004 | Improve Stop hook status inference. | Codex Stop hook scripts | tool failures produce failed/fail; existing partial/blocked state is preserved when appropriate. |
| T-REM-005 | Add migration validation. | observability scripts | legacy rows summarize through fallback without anonymous capability groups. |
| T-REM-VERIFY | Validate syntax, JSON, behavior, and migration. | validation commands and fixture evidence | all listed checks pass. |

## Smallest Working Units

| SWU ID | Parent Task | Goal | Acceptance Evidence |
| --- | --- | --- | --- |
| SWU-OIL-REM-001 | T-REM-001 | Add `--dedupe-mode` and post-success dedupe commit. | observer first run records, second run skips. |
| SWU-OIL-REM-002 | T-REM-002 | Count ordinary thresholds since `last_reflection_at`. | second ordinary run after reflection does not retrigger stale threshold. |
| SWU-OIL-REM-003 | T-REM-002 | Preserve severe-gap immediate trigger. | severe gap fixture emits `severe-gap`. |
| SWU-OIL-REM-004 | T-REM-003 | Add reflection routing to `tools/arcanum`. | `OBSERVED_REFLECT` modes produce expected reflection fields. |
| SWU-OIL-REM-005 | T-REM-003 | Add reflection routing to Codex Stop hook. | hook context includes observer and reflection output. |
| SWU-OIL-REM-006 | T-REM-004 | Derive closeout status from hook evidence. | failed tool event yields failed telemetry. |
| SWU-OIL-REM-007 | T-REM-005 | Add migration check script. | check reports `MIGRATION_CHECK=pass` and `ANONYMOUS=0`. |
| SWU-OIL-REM-008 | T-REM-VERIFY | Run full verification. | syntax, JSON, fixture, and migration checks pass. |

## Validation Strategy

Run:

```bash
bash -n framework/observability/scripts/*.sh tools/arcanum .codex/hooks/*.sh
jq empty .codex/hooks.json .arcanum/observability/config.json .arcanum/observability/reflection-state.json
jq -s empty .arcanum/observability/signals/sigil-invocations.jsonl .arcanum/observability/hooks/hook-operations.jsonl .arcanum/observability/hooks/dedupe.jsonl
framework/observability/scripts/check-observability-migration.sh
```

Fixture checks:

- observer append then duplicate skip in a temp observability store,
- reflection `off`, `auto`, and `always` behavior from managed closeout,
- threshold report followed by cooled ordinary event,
- severe gap immediate trigger,
- Stop hook completed, failed, and partial evidence paths.

## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: spells/invoke/plan.md
- Outputs: REMAINING-IMPLEMENTATION-PLAN.md, REMAINING-WORK-PACK.md
- Complexity: medium
- Per-layer planning: L0, L1, L2, L3
- Implementation detail: task specs complete
- Smallest working units: complete
- Next route: task-session
