# SWU-OIL-AUTO-002 Evidence

## Summary

- SWU: `SWU-OIL-AUTO-002`
- Parent task: `T-AUTO-002`
- Goal: Add the observed invocation marker to generated adapter templates.
- Status: completed
- Date: 2026-05-18

## Files Changed

| Path | Purpose |
| --- | --- |
| `arcana/sigil-runtime-installer/templates/github-copilot-skill.md` | Added generated GitHub Copilot OIL closeout marker. |
| `arcana/sigil-runtime-installer/templates/command-adapter-plan.md` | Added command adapter OIL marker for Codex/Claude plans. |
| `spells/observed-invocation-loop/development/AUTO-ATTACH-WORK-PACK.md` | Marked T-AUTO-002 and SWU-OIL-AUTO-002 complete. |

## Verification Commands

```bash
rg -n "arcanum:observed-invocation|OBSERVED-INVOCATION.md" \
  arcana/sigil-runtime-installer/templates/github-copilot-skill.md \
  arcana/sigil-runtime-installer/templates/command-adapter-plan.md
```

## Result

Pass. New generated adapters now have a stable `arcanum:observed-invocation` marker and point to the runtime-local OIL contract instead of relying on a loose observability reminder.

## Learning From Previous Task

The manifest from `SWU-OIL-AUTO-001` showed most existing adapters were missing explicit OIL attachment. This task prevents that gap from recurring for newly generated adapters before refreshing the existing installed set.

## Next Route

Proceed to `SWU-OIL-AUTO-003`: refresh existing adapters idempotently by marker block.
