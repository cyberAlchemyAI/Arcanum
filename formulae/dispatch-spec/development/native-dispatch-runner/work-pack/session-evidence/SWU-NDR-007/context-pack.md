# Context Pack — SWU-NDR-007

Status: pass

Mode: standard, strict obligation mapping

Session evidence: controls one local Task Session across canonical Arcanum source and its two generated repository consumers. It is not reusable design authority.

## Task

Regenerate the repository's `.agents/skills/orchestrate/` and `.claude/skills/orchestrate/` packages from canonical `runtime/orchestrate/`, prove manifest-based drift is zero, and state native execution support without inflating generation parity into host parity.

## Obligations

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Audit both installed consumers before refresh and preserve any genuine local-only deviation. | covered |
| O2 | Adjudicate existing generated-file edits before replacing them. | covered |
| O3 | Regenerate only the two Orchestrate consumer packages from isolated bootstrap output. | covered |
| O4 | Ensure both packages contain execute mode plus manifest-selected support files. | covered |
| O5 | Prove generated skill semantics/body and support bytes match canonical source. | covered |
| O6 | Record before/after manifests and a zero-drift receipt. | covered |
| O7 | Record Codex as partially proven pending full canaries, not complete. | covered |
| O8 | Record Claude native execution as unsupported/blocking until a native profile and canary exist. | covered |
| O9 | Do not add runtime behavior or perform a live dispatch. | covered |

## Selected Evidence

| Source | Selector | Obligations |
| --- | --- | --- |
| `work-pack/tasks/TASK-NDR-003.md` | SWU-NDR-007 | O1–O9 |
| `work-pack/session-evidence/SWU-NDR-006/receipt.json` | generation pass dependency | O3–O6 |
| `runtime/orchestrate/generation-manifest.json` | selected files and parity rule | O3–O8 |
| `work-pack/shared/cross-task-gaps.md` | cross-host parity limitation | O7, O8 |
| repository `.agents/skills/orchestrate/SKILL.md` | pre-refresh generated Codex consumer | O1, O2, O6, O7 |
| repository `.claude/skills/orchestrate/SKILL.md` | pre-refresh generated Claude consumer | O1, O2, O6, O8 |
| `tools/bootstrap_arcanum.sh` | isolated deterministic generator | O3–O6 |

## Deviation Adjudication

Both installed files declare `surface_kind: generated-native-runtime-package` and `mutation_policy: regenerate-from-canonical-source`. Their current diff is the previous generator's smaller capability list and capability-bound process prose. No local-only host rule, user-authored extension, or separate authority was found. The stronger canonical `runtime/orchestrate/SKILL.md` supersedes that generated content, so replacement is approved inside this Task Session.

## Decisions

1. Bootstrap all declared surfaces in a temporary root, then mechanically copy only the two Orchestrate packages into the current repository.
2. Do not invoke full in-place bootstrap because it would rewrite unrelated skill packages outside this SWU.
3. Treat support-file byte equality plus normalized skill semantic/body equality as zero drift.
4. Codex generation status is pass; native runtime status remains partial until SWU-NDR-011/012.
5. Claude generation status is pass; native execution status is unsupported/blocking because the selected Codex operation profile is unavailable there and no Claude canary exists.

## Write Scope

- repository `.agents/skills/orchestrate/`
- repository `.claude/skills/orchestrate/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/session-evidence/SWU-NDR-007/`
- `formulae/dispatch-spec/development/native-dispatch-runner/work-pack/swu-manifest.json` for evidence synchronization only

## Validation Surface

- before/after package manifests;
- package file-set equality with the generation manifest;
- normalized skill semantic and exact body comparison;
- byte equality for host, schema, script, and manifest support;
- execute grammar present in both packages;
- current repository drift check;
- host capability matrix with explicit proof limits;
- no live dispatch.

No blocker remains. If mechanical generation changes anything outside the two packages, the refresh must stop.

## Provenance

- Built: `2026-07-22T15:27:16Z`
- Source digests: `context-pack.json`
