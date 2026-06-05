---
module: skill-surface-dispatch-canonicalization
version: current
status: pass
updatedAt: 2026-06-05
docType: task-session-result
task: SWU-DISP-SURF-002
runId: arcanum-hook-019e9859-0500-7192-9409-995311049f25
---

# Task Session Result: SWU-DISP-SURF-002

## Verdict

`PASS`: active skill contracts no longer require command-surface invocation for model-backed stage execution. Refine and adjacent runtime guidance now route stage work through native skill/subagent execution, capability handles, dispatch validation, and receipt metadata.

## Changes

| File | Change |
| --- | --- |
| `arcana/refine/SKILL.md` | Replaced command-file and command-resolution requirements with capability-handle resolution; clarified that `tools/arcanum --exec` is only a deterministic handoff/receipt surface for native adapters, not the stage execution primitive. |
| `arcana/refine/README.md` | Reframed runtime dispatch around deterministic capability handles and parent native skill/subagent execution. |
| `arcana/refine/development/codex-skill-install/SKILL.md` | Updated installed Refine package source to prefer the native `refine` skill package and canonical source contract; `.codex/commands/` is not required for normal Refine execution. |
| `spells/observed-invocation-loop/README.md` | Clarified that deterministic wrappers may prepare receipt metadata while native skill/subagent execution remains the primary runtime surface. |
| `spells/whisper/README.md` | Removed `tools/arcanum --exec` as an alternate model-backed execution route; kept deterministic handoff wrappers as receipt metadata only. |
| `arcana/invoke-example-runner/SKILL.md` | Removed `arcanum-invoke` alias language and kept only the active native `invoke` package, with `.codex/commands` limited to explicit legacy compatibility validation. |

## Remaining Hit Classification

| Class | Remaining Hits | Classification |
| --- | --- | --- |
| Deterministic handoff/receipt metadata | `arcana/refine/SKILL.md`, `arcana/refine/README.md`, `arcana/refine/development/codex-skill-install/SKILL.md`, `spells/observed-invocation-loop/README.md` | Allowed: `tools/arcanum --exec` appears only as native adapter handoff/receipt metadata and explicitly does not replace native skill execution. |
| Explicit legacy installer ownership | `arcana/sigil-runtime-installer/SKILL.md`, `arcana/sigil-runtime-installer/README.md` | Allowed: this sigil owns explicit legacy `.codex/commands/` installation. |
| Explicit legacy compatibility validation | `arcana/invoke-example-runner/SKILL.md`, `arcana/distill/README.md`, `arcana/experiment-harness/README.md` | Allowed: command files are described only for compatibility validation or older adapter compatibility. |
| Bootstrap adapter documentation | `spells/arcanum-bootstrap/README.md` | Allowed: bootstrap documents optional legacy command adapters and runtime adapter interchange, not default skill execution. |

## Validation

| Check | Result |
| --- | --- |
| Active surface grep run and remaining hits classified | pass |
| `bash -n tools/bootstrap_arcanum.sh` | pass |
| Direct dispatch validator on `pass-refine-dispatch.json` | pass |
| Full dispatch-spec fixture suite | pass, ended with `DISPATCH_SPEC_VALIDATION=pass` |

## Commands Run

```bash
rg -n "tools/arcanum --exec|\\.codex/commands|command-backed|command file|resolved command|command used" arcana spells transmutations formulae --glob 'SKILL.md' --glob 'README.md'
bash -n tools/bootstrap_arcanum.sh
python3 formulae/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/fixtures/pass-refine-dispatch.json --json
formulae/dispatch-spec/development/run-validation-fixtures.sh
```

## Synchronization

- Context pack: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-002-CONTEXT.md`
- Work-pack synchronized: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-WORK-PACK.md`
- Live installs not mutated.

## Follow-Up

`SWU-DISP-SURF-005` is the next route, but it is blocked until the user explicitly approves mutation of `/mnt/c/Users/vlad_/.codex/skills`.
