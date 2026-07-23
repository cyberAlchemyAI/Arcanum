# Context Pack — SWU-NDR-006

Status: pass

Mode: standard, strict obligation mapping

Session evidence: controls one local Task Session. It is not reusable design authority.

## Task

Replace the hardcoded bootstrap Orchestrate body with generation from canonical `runtime/orchestrate/` source, then prove isolated repository Codex and repo-local installations contain the declared skill, host, schemas, scripts, and generation manifest.

## Obligations

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Remove the hardcoded canonical Orchestrate skill body from bootstrap. | covered |
| O2 | Render generated `SKILL.md` from canonical source while adding generated-surface provenance. | covered |
| O3 | Copy the declared runtime support paths: host profiles, schemas, scripts, and generation manifest. | covered |
| O4 | Exclude authoring tests and runtime cache files from generated packages. | covered |
| O5 | Generate a repository Codex package under `.agents/skills/orchestrate/`. | covered |
| O6 | Generate a repo-local runtime package under `.arcanum/runtime/orchestrate/`. | covered |
| O7 | Validate isolated installations through byte comparison and semantic skill comparison. | covered |
| O8 | Do not refresh the current repository's installed `.agents` or `.claude` consumers in this SWU. | covered |
| O9 | Preserve the intent of the pre-existing hardcoded-heredoc edit by using the stronger current canonical skill. | covered |

## Selected Evidence

| Source | Selector | Obligations |
| --- | --- | --- |
| `work-pack/tasks/TASK-NDR-003.md` | SWU-NDR-006 | O1–O9 |
| `work-pack/session-evidence/SWU-NDR-005/receipt.json` | pass dependency and next route | O8 |
| `tools/bootstrap_arcanum.sh` | `write_orchestrate_skill_file`, package writers, repo-local install | O1–O7, O9 |
| `runtime/orchestrate/SKILL.md` | canonical runtime contract | O1–O3, O7, O9 |
| `ARCHITECTURE.json` | canonical source and generation rule | O1–O8 |
| `DESIGN.md` | deployment/generation view and drift risk | O1–O8 |

## Decisions

1. Add `runtime/orchestrate/generation-manifest.json` as the canonical selection contract for generated files.
2. Generate `SKILL.md` from the canonical file with only host-surface provenance/name rewriting; compare its semantic contract after removing those generated fields.
3. Copy `hosts/`, `schemas/`, and `scripts/` byte-for-byte, excluding caches; do not ship `tests/`.
4. Install the selected package both into host-native skill surfaces and into `.arcanum/runtime/orchestrate/` for repo-local execution support.
5. Treat the existing hardcoded-heredoc edit as superseded by the stronger canonical skill rather than discarding its intent.

## Write Scope

- `tools/bootstrap_arcanum.sh`
- `runtime/orchestrate/`
- `runtime/orchestrate/tests/bootstrap-generation/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/session-evidence/SWU-NDR-006/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/swu-manifest.json` for evidence synchronization only

## Validation Surface

- hardcoded Orchestrate body absent from bootstrap;
- repo-codex and repo-local bootstrap into an isolated temporary target;
- generated manifest present;
- selected support files byte-equal to canonical source;
- generated skill body/frontmatter contract semantically equals canonical source after generated provenance normalization;
- generated package excludes `tests/` and `__pycache__/`;
- all existing runtime tests remain green;
- current installed consumers remain untouched.

No blocker remains. Current-repository consumer refresh and drift enforcement remain SWU-NDR-007.

## Provenance

- Built: `2026-07-22T15:21:27Z`
- Source digests: `context-pack.json`
