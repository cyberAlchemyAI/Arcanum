# SWU-OIL-AUTO-006 Evidence

## Summary

- SWU: `SWU-OIL-AUTO-006`
- Parent task: `T-AUTO-VERIFY`
- Goal: Verify telemetry after attached adapter rollout.
- Status: completed
- Date: 2026-05-18

## Files Changed

| Path | Purpose |
| --- | --- |
| `spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-FINAL-VALIDATE.md` | Final all-runtime validation manifest. |
| `spells/observed-invocation-loop/development/AUTO-ATTACH-WORK-PACK.md` | Marked T-AUTO-VERIFY and SWU-OIL-AUTO-006 complete. |

## Verification Commands

```bash
bash -n framework/observability/scripts/attach-observed-invocation.sh
bash -n framework/observability/scripts/observe-invocation.sh
bash -n framework/observability/scripts/reflect-invocation-signals.sh
bash -n framework/observability/scripts/run-observed-adapter-pilot.sh
framework/observability/scripts/attach-observed-invocation.sh \
  --runtime all \
  --validate \
  --output spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-FINAL-VALIDATE.md
tmp_dir="$(mktemp -d)"
framework/observability/scripts/run-observed-adapter-pilot.sh \
  --observability-dir "$tmp_dir/observability"
```

## Results

| Check | Result |
| --- | --- |
| shell syntax checks | pass |
| all-runtime validation | pass |
| attached runtime adapters | 66 |
| missing runtime adapters | 0 |
| planned runtime adapters | 33 Claude command adapters |
| conflicts | 0 |
| GitHub Copilot marker/direct attachment coverage | 33 |
| Codex command marker coverage | 33 |
| Codex discovery bridges | 33 |
| observed adapter pilot | pass |

Pilot output:

```text
PILOT=pass
SKILL=arcanum-orchestrate
SIGIL=signal-observer
SPELL=invoke
```

## Learning From Previous Task

`SWU-OIL-AUTO-005` made Codex concrete instead of planned. Final validation now shows GitHub Copilot and Codex attached with zero missing adapters. Claude remains planned because its command runtime directory is not installed in this repo.

## Acceptance

Pass. OIL automatic attachment is now implemented for generated templates, refreshed across installed GitHub Copilot adapters, generated for Codex commands, validated by manifest, and backed by the existing telemetry pilot.
