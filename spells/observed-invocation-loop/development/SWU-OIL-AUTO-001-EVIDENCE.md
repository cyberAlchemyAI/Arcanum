# SWU-OIL-AUTO-001 Evidence

## Summary

- SWU: `SWU-OIL-AUTO-001`
- Parent task: `T-AUTO-001`
- Goal: Generate an Observed Invocation Loop attachment manifest in dry-run mode.
- Status: completed
- Date: 2026-05-18

## Files Changed

| Path | Purpose |
| --- | --- |
| `framework/observability/scripts/attach-observed-invocation.sh` | Added read-only attachment manifest generator. |
| `spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-MANIFEST.md` | Captured dry-run adapter attachment manifest. |
| `spells/observed-invocation-loop/development/AUTO-ATTACH-WORK-PACK.md` | Marked T-AUTO-001 and SWU-OIL-AUTO-001 complete. |

## Verification Commands

```bash
bash -n framework/observability/scripts/attach-observed-invocation.sh
framework/observability/scripts/attach-observed-invocation.sh \
  --runtime all \
  --dry-run \
  --output spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-MANIFEST.md
```

## Results

| Check | Result |
| --- | --- |
| shell syntax | pass |
| dry-run manifest command | pass |
| GitHub Copilot adapters scanned | 33 |
| GitHub Copilot adapters attached | 3 |
| GitHub Copilot adapters missing OIL attachment | 30 |
| Codex command surface | planned; runtime command directory not installed |
| Claude command surface | planned; runtime command directory not installed |

## Manifest

- Manifest: `spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-MANIFEST.md`

The attached GitHub Copilot adapters are the existing pilot targets:

- `arcanum-orchestrate`
- `arcanum-sigil-signal-observer`
- `arcanum-spell-invoke`

## Acceptance

Pass. The repository now has a read-only command that inventories installed runtime adapters and classifies OIL attachment status before any refresh mutation occurs.

## Next Route

Proceed to `SWU-OIL-AUTO-002`: add the observed invocation marker to generated adapter templates so new installs receive OIL closeout by default.
