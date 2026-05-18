# SWU-OIL-AUTO-003 Evidence

## Summary

- SWU: `SWU-OIL-AUTO-003`
- Parent task: `T-AUTO-003`
- Goal: Refresh existing adapters idempotently by OIL marker block.
- Status: completed
- Date: 2026-05-18

## Files Changed

| Path | Purpose |
| --- | --- |
| `framework/observability/scripts/attach-observed-invocation.sh` | Added `--apply` mode for marker-based GitHub Copilot adapter refresh. |
| `.arcanum/runtimes/github-copilot/skills/*/SKILL.md` | Added OIL marker to previously missing adapters. |
| `spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-APPLY.md` | First apply manifest. |
| `spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-APPLY-IDEMPOTENT.md` | Second apply manifest proving idempotence. |
| `spells/observed-invocation-loop/development/AUTO-ATTACH-WORK-PACK.md` | Marked T-AUTO-003 and SWU-OIL-AUTO-003 complete. |

## Verification Commands

```bash
bash -n framework/observability/scripts/attach-observed-invocation.sh
framework/observability/scripts/attach-observed-invocation.sh \
  --runtime github-copilot \
  --apply \
  --output spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-APPLY.md
framework/observability/scripts/attach-observed-invocation.sh \
  --runtime github-copilot \
  --apply \
  --output spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-APPLY-IDEMPOTENT.md
```

## Results

| Check | Result |
| --- | --- |
| shell syntax | pass |
| first apply changed adapters | 30 |
| first apply attached adapters | 33 |
| first apply missing adapters | 0 |
| first apply conflicts | 0 |
| second apply changed adapters | 0 |
| second apply attached adapters | 33 |
| second apply missing adapters | 0 |
| second apply conflicts | 0 |

## Learning From Previous Task

`SWU-OIL-AUTO-002` established the marker shape. This task used that marker shape as the only mutation boundary, so the refresh can be rerun without duplicating content.

## Next Route

Proceed to `SWU-OIL-AUTO-004`: validate attachment coverage and make missing markers fail or flag deterministically.
