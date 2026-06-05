---
module: skill-surface-dispatch-canonicalization
version: current
status: pass
updatedAt: 2026-06-05
docType: task-session-context
task: SWU-DISP-SURF-002
runId: arcanum-hook-019e9859-0500-7192-9409-995311049f25
---

# Task Session Context: SWU-DISP-SURF-002

## Objective

Rewrite active skill contracts so model-backed stage execution uses native skill/subagent execution and capability handles rather than command-surface invocation.

## Source Anchors

| Anchor | Role |
| --- | --- |
| `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-WORK-PACK.md` | SWU definition, done criteria, and command-surface classification rule. |
| `arcana/refine/SKILL.md` | Primary active stage-dispatch contract. |
| `arcana/refine/README.md` | Dispatch-spec narrative and handoff wording. |
| `arcana/refine/development/codex-skill-install/SKILL.md` | Generated installed Refine package source. |
| `spells/observed-invocation-loop/README.md` | Runtime observability handoff wording. |
| `spells/whisper/README.md` | Long model-backed runtime guidance. |
| `arcana/invoke-example-runner/SKILL.md` | Invoke example execution surface guidance. |

## Gate Checks

| Gate | Status | Evidence |
| --- | --- | --- |
| S-001 complete before contract rewrite | pass | Work-pack records `SWU-DISP-SURF-001` as completed. |
| S-003/S-004 staged dispatch-spec validation available | pass | Work-pack records generated package and staged validation as completed. |
| Active contract rewrite stays scoped to source contracts | pass | Edits are limited to active skill/source contract files and generated package source text. |
| Legacy command ownership preserved | pass | `sigil-runtime-installer` and explicit compatibility docs are classified, not rewritten as native defaults. |

## Validation Plan

Run the active surface grep required by the work-pack:

```bash
rg -n "tools/arcanum --exec|\\.codex/commands|command-backed|command file|resolved command|command used" arcana spells transmutations formulae --glob 'SKILL.md' --glob 'README.md'
```

Remaining hits must classify as one of:

- deterministic handoff or receipt metadata;
- explicit legacy installer ownership;
- explicit legacy compatibility validation;
- bootstrap adapter documentation;
- historical or migration note.

Run dispatch-spec validation after edits:

```bash
bash -n tools/bootstrap_arcanum.sh
python3 formulae/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/fixtures/pass-refine-dispatch.json --json
formulae/dispatch-spec/development/run-validation-fixtures.sh
```

## Blocker Scan

`SWU-DISP-SURF-002` has no remaining blocker. The next live refresh task remains blocked because mutating `/mnt/c/Users/vlad_/.codex/skills` requires explicit user approval.
