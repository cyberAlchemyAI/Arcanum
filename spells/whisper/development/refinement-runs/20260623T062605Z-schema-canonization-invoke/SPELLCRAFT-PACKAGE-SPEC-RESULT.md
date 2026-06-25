# Spellcraft Result - Whisper Schema Package Spec Gate

- Mode: validate
- Spell: whisper
- Canonical ID: whisper
- Alias used: none
- Scope: library
- Spell file: `arcanum/spells/whisper/README.md`
- Gate evidence: `SCHEMA-ARTIFACT-AUDIT.md`
- Work-pack: `WORK-PACK.md`
- Validation: pass for `SWU-WSC-002` package-spec Task Session handoff; flag for canonical package creation
- Observability: configured
- Next action: `task-session` for `SWU-WSC-002`

## Lifecycle Decision

Spellcraft accepts `SCHEMA-ARTIFACT-AUDIT.md` as sufficient lifecycle evidence
to open the L1 package-specification lane.

Accepted now:

- Execute `SWU-WSC-002`.
- Write a canonical schema package specification as a review/design artifact
  under this refinement-run folder.
- Use the audit matrix to decide target files, field ownership, example policy,
  validation commands, and promotion blockers.
- Preserve the stable package home target:
  `arcanum/spells/whisper/schemas/`.
- Treat `readability_dynamics` as optional candidate-stable evidence, not as a
  fully promoted base requirement.

Still blocked:

- Creating `arcanum/spells/whisper/schemas/`.
- Refreshing `arcanum/spells/whisper/README.md`.
- Editing or regenerating `.agents/skills/whisper/`.
- Treating generated review/public HTML as schema authority.
- Promoting `readability_dynamics` without broader fixture or experiment
  evidence.

## Audit Consumption

| Audit Finding | Spellcraft Decision |
| --- | --- |
| Whisper has no stable schema home. | Package spec must target `arcanum/spells/whisper/schemas/`. |
| Canonical authority is split across README, development substrates, validator, and readability evidence. | Package spec must separate base contract, transport profile, examples, provenance, and generated consumers. |
| Main `text-intent-substrate.yaml` is both canonical-source candidate and example candidate. | Package spec must not copy it wholesale; it must extract stable field families and preserve article values as examples. |
| `validate-whisper-draft.py` is executable evidence for current behavior. | Package spec must name validator-compatible examples and commands. |
| Object sequel substrate is an example candidate. | Package spec should include it as a compatibility example, not as base authority. |
| `readability_dynamics` is candidate-stable optional evidence. | Package spec may include an optional example or extension note, but must not make it mandatory for the base schema. |
| Review payload fields are deferred. | Package spec should keep review payload schema out of the first base package unless explicitly scoped. |

## Accepted Task Session Boundary

`SWU-WSC-002` is accepted as the only mutation-capable next unit.

Execution owner: `task-session`

Allowed write scope:

- This refinement-run folder.
- A new package-spec artifact, recommended path:
  `CANONICAL-SCHEMA-PACKAGE-SPEC.md`.
- Synchronized work-pack/task-session receipt artifacts for `SWU-WSC-002`.

Forbidden write scope:

- `arcanum/spells/whisper/schemas/**`
- `arcanum/spells/whisper/README.md`
- `.agents/skills/whisper/**`
- Generated review/public HTML files

Expected receipt:

```yaml
runtime: codex
source_swu: SWU-WSC-002
result: pass | flag | block | interrupted
files_touched:
  - arcanum/spells/whisper/development/refinement-runs/20260623T062605Z-schema-canonization-invoke/CANONICAL-SCHEMA-PACKAGE-SPEC.md
validation:
  - review against SCHEMA-ARTIFACT-AUDIT.md
  - review against arcanum/spells/whisper/README.md lifecycle contract
  - path-scope check proving schemas/ was not created
remaining_blockers:
  - task-session acceptance required before canonical package creation
lifecycle_owner_next_step: task-session
```

## Package-Spec Constraints

The package spec must decide the smallest canonical form that current evidence
supports. The recommended default is a human-readable schema contract plus YAML
example fixtures, because the current validator enforces behavior from YAML
substrates rather than a standalone JSON Schema engine.

The spec must explicitly classify:

- base field contract;
- `substack_research_post` transport profile;
- example fixtures;
- optional `readability_dynamics` extension;
- deferred review-payload schema;
- provenance-only development artifacts;
- generated runtime and rendered surfaces.

## Work-Pack Sync

The L1 package-spec owner gate is accepted. `SWU-WSC-002` may now move from
blocked to ready. Later SWUs remain blocked by their named dependencies and
promotion evidence gates.

## Recommended Next Action

Run Task Session on `SWU-WSC-002`.

