# SWU-OIL-AUTO-004 Evidence

## Summary

- SWU: `SWU-OIL-AUTO-004`
- Parent task: `T-AUTO-004`
- Goal: Validate OIL attachment coverage.
- Status: completed
- Date: 2026-05-18

## Files Changed

| Path | Purpose |
| --- | --- |
| `framework/observability/scripts/attach-observed-invocation.sh` | Added `--validate` behavior with non-zero exit on missing or conflicted attachments. |
| `spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-VALIDATE-GITHUB-COPILOT.md` | Repository validation evidence for GitHub Copilot adapters. |
| `spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-VALIDATE-ALL.md` | All-runtime validation evidence, including planned Codex and Claude surfaces. |
| `spells/observed-invocation-loop/development/AUTO-ATTACH-WORK-PACK.md` | Marked T-AUTO-004 and SWU-OIL-AUTO-004 complete. |

## Verification Commands

```bash
framework/observability/scripts/attach-observed-invocation.sh \
  --runtime github-copilot \
  --validate \
  --output spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-VALIDATE-GITHUB-COPILOT.md
framework/observability/scripts/attach-observed-invocation.sh \
  --runtime all \
  --validate \
  --output spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-VALIDATE-ALL.md
```

Negative fixture:

```bash
tmp_repo="$(mktemp -d)"
mkdir -p "$tmp_repo/.arcanum/runtimes/github-copilot/skills/arcanum-sigil-fixture"
mkdir -p "$tmp_repo/.github/skills/arcanum-sigil-fixture"
printf '<process>\n1. Run fixture.\n</process>\n' > "$tmp_repo/.arcanum/runtimes/github-copilot/skills/arcanum-sigil-fixture/SKILL.md"
framework/observability/scripts/attach-observed-invocation.sh \
  --repo "$tmp_repo" \
  --runtime github-copilot \
  --validate \
  --output "$tmp_repo/manifest.md"
```

## Results

| Check | Result |
| --- | --- |
| GitHub Copilot validation | pass |
| GitHub Copilot attached adapters | 33 |
| GitHub Copilot missing adapters | 0 |
| all-runtime validation | pass with planned Codex/Claude rows |
| all-runtime attached adapters | 33 |
| all-runtime planned adapters | 66 |
| negative missing-marker fixture | pass; validator exited non-zero with `MISSING=1` |

## Learning From Previous Task

`SWU-OIL-AUTO-003` made the installed GitHub Copilot adapters attached and idempotent. This task turned that status into a gate: missing markers now fail validation for installed adapters, while uninstalled Codex and Claude command surfaces remain planned instead of blocking the current runtime.

## Next Route

Proceed to `SWU-OIL-AUTO-005`: add Codex command adapter support as a runtime target.
