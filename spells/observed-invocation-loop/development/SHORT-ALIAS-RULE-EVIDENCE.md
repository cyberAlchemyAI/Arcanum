# Short Alias Rule Evidence

## Summary

- Change: Arcanum sigils and spells can be invoked without the `arcanum-sigil-` or `arcanum-spell-` prefix.
- Date: 2026-05-18
- Status: implemented for Codex and GitHub Copilot command surfaces.

## Rule

Prefixed commands remain stable compatibility names:

- `arcanum-sigil-<id>`
- `arcanum-spell-<id>`

Sigils and spells also get bare-id aliases when no collision exists:

- `<id>`
- examples: `invoke`, `interrogation`, `context-builder`, `spellcraft`

## Files Changed

| Path | Purpose |
| --- | --- |
| `arcana/sigil-runtime-installer/SKILL.md` | Updated installer rule and validation criteria for bare aliases. |
| `arcana/sigil-runtime-installer/README.md` | Documented bare-id alias behavior. |
| `spells/observed-invocation-loop/README.md` | Documented OIL-compatible short aliases. |
| `framework/observability/scripts/attach-observed-invocation.sh` | Added short alias generation and validation. |
| `.codex/commands/<id>.md` | Added Codex bare-id alias bridges. |
| `.github/skills/<id>/SKILL.md` | Added GitHub Copilot bare-id alias bridges. |
| `spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-SHORT-ALIASES-VALIDATE.md` | Captured validation evidence. |

## Verification Commands

```bash
bash -n framework/observability/scripts/attach-observed-invocation.sh
framework/observability/scripts/attach-observed-invocation.sh \
  --runtime codex \
  --apply \
  --output spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-CODEX-ALIASES-IDEMPOTENT.md
framework/observability/scripts/attach-observed-invocation.sh \
  --runtime github-copilot \
  --apply \
  --output spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-GITHUB-ALIASES.md
framework/observability/scripts/attach-observed-invocation.sh \
  --runtime all \
  --validate \
  --output spells/observed-invocation-loop/development/OIL-AUTO-ATTACHMENT-SHORT-ALIASES-VALIDATE.md
```

## Results

| Check | Result |
| --- | --- |
| shell syntax | pass |
| Codex bare aliases | 30 |
| GitHub Copilot bare aliases | 30 |
| final attached adapters | 66 |
| missing adapters or aliases | 0 |
| conflicts | 0 |
| planned Claude aliases/adapters | 33 |

## Example Aliases

| Alias | Runtime Bridge | Target Adapter |
| --- | --- | --- |
| `invoke` | `.codex/commands/invoke.md` | `.arcanum/runtimes/codex/commands/arcanum-spell-invoke.md` |
| `interrogation` | `.codex/commands/interrogation.md` | `.arcanum/runtimes/codex/commands/arcanum-sigil-interrogation.md` |
| `invoke` | `.github/skills/invoke/SKILL.md` | `.arcanum/runtimes/github-copilot/skills/arcanum-spell-invoke/SKILL.md` |
| `interrogation` | `.github/skills/interrogation/SKILL.md` | `.arcanum/runtimes/github-copilot/skills/arcanum-sigil-interrogation/SKILL.md` |

## Acceptance

Pass. Users can invoke Arcanum sigils and spells through bare-id command aliases while prefixed commands remain available for compatibility.
