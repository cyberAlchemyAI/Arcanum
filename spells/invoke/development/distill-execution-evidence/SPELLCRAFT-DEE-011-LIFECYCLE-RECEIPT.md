# Spellcraft Lifecycle Receipt: SWU-DEE-011

## Identity

- Spellcraft mode: `validate`
- Spell: `invoke`
- Canonical ID: `invoke`
- Source SWU: `SWU-DEE-011`
- Decision: **accept bootstrap-derived generated parity with bounded overlays**
- Lifecycle status: resolved

## Accepted Responsibility

`SWU-DEE-011` owns regeneration and parity of the accepted Invoke evidence contracts across the
repo-local Codex and Claude runtime surfaces. It uses the repository bootstrap generator in an
isolated target, compares generated support files byte-for-byte, and checks that explicit local
atomicity overlays retain the DEE evidence contract.

The generator is never run in-place with force over unrelated generated skills. No private
authority prose is promoted into the public Arcanum package.

## Binding

Canonical owner: `arcanum/spells/invoke/` through the repository bootstrap generator.

Execution owner: Spellcraft/bootstrap owner, one SWU only.

Exact implementation and evidence scope:

- `arcanum/tools/bootstrap_arcanum.sh`
- `arcanum/spells/invoke/development/run-distill-generated-parity-fixture.sh`
- generated Codex surface `.agents/skills/invoke/`
- generated Claude surface `.claude/skills/invoke/`

The parity projection covers `README.md`, active/deferred mode contracts,
`mode-capabilities.json`, and the four Distill schemas. Existing user-owned atomicity overlays
in `.agents/skills/invoke/SKILL.md`, `plan.md`, and `templates/work-pack.md` are preserved and
explicitly marker-checked.

Task Session governance and completion-evidence scope:

- `arcanum/spells/invoke/development/distill-execution-evidence/SPELLCRAFT-DEE-011-LIFECYCLE-RECEIPT.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/WORK-PACK.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/tasks/TASK-DEE-06-MIRRORS.md`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/SWU-DEE-011-RESULT.md`

## Acceptance Conditions

- isolated bootstrap completes for Invoke with repo-local Codex and Claude profiles;
- every selected support file matches both generated mirrors byte-for-byte;
- the machine capability table and Distill schemas are present in both mirrors;
- local atomicity overlays are retained and contain the DEE evidence markers;
- no unrelated generated skill is removed or rewritten.

## Next Route

`task-session` must bind and execute `SWU-DEE-012` replay validation over the current Workbench
package. DEE-013 remains blocked and unselected until replay evidence exists.
