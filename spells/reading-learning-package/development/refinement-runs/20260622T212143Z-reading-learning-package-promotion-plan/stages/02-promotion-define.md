# Stage 02: Promotion Delta Definition

Status: pass
Owner: `invoke`
Mode: define

## Promotion Delta

`reading-learning-package` needs a promotion delta with four parts:

1. Registry discoverability in `arcanum/registry/SPELLS.md`.
2. Runtime surface resolution proof through `bootstrap_arcanum.sh`.
3. Final promotion receipt connecting Spellcraft, experiment harness, fixture
   evidence, registry, and publication gates.
4. Submodule-first publication receipts.

## Default Registry Shape

| Field | Proposed Value |
| --- | --- |
| Spell | `Reading Learning Package` |
| Aliases | none by default |
| Purpose | Compose reader-facing learning packages from completed `research-tower` output through a Whisper-compatible substrate. |
| Sigils/spells composed | `research-tower`, `whisper`, optional `experiment-harness`, optional `task-session` |
| Use when | A completed tower should become a readable learning package with source trace and HTML/PDF fallback. |
| File | `../spells/reading-learning-package/README.md` |

## Defined Non-Goals

- Do not add deterministic PDF renderer work to promotion.
- Do not promote generated manuscripts, HTML, PDFs, or source traces into tower
  authority.
- Do not mutate `research-tower` or `whisper`.
- Do not push a parent gitlink before the public submodule commit is pushed.

