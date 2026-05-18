# SWU-OIL-AUTO-005 Evidence

## Summary

- SWU: `SWU-OIL-AUTO-005`
- Parent task: `T-AUTO-005`
- Goal: Add Codex command adapter support as a runtime target.
- Status: completed
- Date: 2026-05-18

## Files Changed

| Path | Purpose |
| --- | --- |
| `framework/observability/scripts/attach-observed-invocation.sh` | Added Codex apply support using the existing adapter inventory. |
| `.arcanum/runtimes/codex/OBSERVED-INVOCATION.md` | Added Codex runtime-local OIL contract. |
| `.arcanum/runtimes/codex/commands/*.md` | Added canonical Codex runtime command adapters. |
| `.codex/commands/*.md` | Added thin Codex discovery bridges. |
| `spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-CODEX-DRY-RUN.md` | Codex planned command evidence. |
| `spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-CODEX-APPLY.md` | Codex generation evidence. |
| `spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-CODEX-IDEMPOTENT.md` | Codex idempotence evidence. |
| `spells/observed-invocation-loop/development/AUTO-ATTACH-WORK-PACK.md` | Marked T-AUTO-005 and SWU-OIL-AUTO-005 complete. |

## Verification Commands

```bash
bash -n framework/observability/scripts/attach-observed-invocation.sh
framework/observability/scripts/attach-observed-invocation.sh \
  --runtime codex \
  --dry-run \
  --output spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-CODEX-DRY-RUN.md
framework/observability/scripts/attach-observed-invocation.sh \
  --runtime codex \
  --apply \
  --output spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-CODEX-APPLY.md
framework/observability/scripts/attach-observed-invocation.sh \
  --runtime codex \
  --apply \
  --output spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-CODEX-IDEMPOTENT.md
```

## Results

| Check | Result |
| --- | --- |
| shell syntax | pass |
| Codex dry-run planned commands | 33 |
| Codex first apply changed files | 67 |
| Codex first apply attached commands | 33 |
| Codex first apply missing commands | 0 |
| Codex first apply conflicts | 0 |
| Codex second apply changed files | 0 |
| Codex second apply attached commands | 33 |
| Codex runtime contract | created |
| Codex bridges | created |

## Learning From Previous Task

`SWU-OIL-AUTO-004` showed Codex was planned but not installed. This task converted the planned rows into generated canonical command adapters and `.codex/commands` bridges while preserving the same OIL marker contract used by GitHub Copilot.

## Next Route

Proceed to `SWU-OIL-AUTO-006`: verify end-to-end attachment and telemetry after the adapter rollout.
