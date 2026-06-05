---
module: inventory-whole-arcanum
version: 0.1.0
status: pass
updatedAt: 2026-06-03
docType: invoke-refresh-report
invokeMode: refresh
mutationMode: apply-approved
---

# Invoke Refresh Report: Native Runtime Proof

## Scope

Refresh whole-Arcanum Inventory from the approved runtime-surface decision:
legacy `.codex/commands` are no longer live proof for Inventory. The live test
surface is generated native skill packages plus canonical source contracts.

## Source Signals

| ID | Type | Claim | Confidence | Safety |
| --- | --- | --- | --- | --- |
| refresh-signal-native-runtime-proof | route_changed | Legacy command files are excluded from the live proof path. | high | safe |
| refresh-signal-validator-recovered | blocker_resolved | The stale `.codex/commands/inventory.md` source-ref blocker is gone. | high | safe |
| refresh-signal-external-install-smoke | evidence_added | A repository-style target installs Inventory/Invoke/Task Session as native Codex skills with zero legacy command files. | high | safe |

## Applied Changes

| Artifact | Delta |
| --- | --- |
| `source-manifest.json` | Removed `.codex/commands` as a source family. |
| `SOURCE-POLICY.md` | Added legacy command files to default exclusions and documented native package runtime treatment. |
| `cards/runtime/cards.json` | Reframed the runtime card around native packages replacing legacy command-file proof. |
| `cards/runtime/index.json` | Replaced `commands` tag lookup with `native-skill`. |
| `cards/runtime/retrieval.json` | Updated query filters and selected-card reason for native runtime testing. |
| `cards/runtime/COVERAGE.md` | Recorded `.codex/commands` as intentionally omitted legacy adapter state. |
| `WORK-PACK.md` and task-session evidence | Synchronized wording from command surfaces to native runtime surfaces. |

## Validation

| Check | Result |
| --- | --- |
| `jq empty arcana/inventory/development/whole-arcanum/refresh-report.json` | pass |
| `bash arcana/inventory/scripts/validate-evidence-card-slice.sh arcana/inventory/development/whole-arcanum/cards/runtime` | pass |
| `bash arcana/inventory/development/whole-arcanum/scripts/validate-whole-arcanum-inventory.sh` | pass |
| Temp repo-style install with `--profiles repo-codex,repo-local` | pass |
| Temp target `tools/arcanum --resolve inventory` and `--resolve invoke` | pass |
| Temp target legacy command files | pass: 0 files |

The Artifact Constitution validator still reports pre-existing benchmark
generated-artifact warnings, but it returns `result: pass`; the Inventory suite
returns `RESULT: pass`.

## Skipped Changes

| Change | Reason |
| --- | --- |
| EvidenceSet promotion | Still requires repeated real task-session reuse evidence. |
| Human UI | Deferred; shell plus `jq` remains enough for agent POC. |
| Legacy command generation | Explicitly out of scope for live proof. |
| Real implementation task in another repository | Next user-run step; this refresh proved install/runtime surface only. |

## Next Route

Install into the target repository with native profiles and run one real task:

```bash
bash tools/bootstrap_arcanum.sh --target <repo> --sigils inventory,task-session --spells invoke --profiles repo-codex,repo-local --clean-legacy-codex-commands --force --no-necronomicon
```

Then use `$inventory`, `$invoke`, and `$task-session` from the target repo and
record whether cards or candidate EvidenceSets were useful, stale, or missing.
