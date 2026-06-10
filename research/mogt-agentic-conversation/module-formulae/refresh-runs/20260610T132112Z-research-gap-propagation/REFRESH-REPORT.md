---
name: Invoke Refresh Report - MOGT Research Gap Propagation
description: Refresh report reconciling stale module-formulae gaps and propagating genuinely-open gaps into the research project as new contracts and governed work.
created: 2026-06-10
mode: refresh
phase_status: pass
mutation_mode: apply-approved
---

# Invoke Refresh Report

## Scope

Drive a refresh from the documented open gaps in the MOGT Module Formulae model
and propagate the genuinely-open ones into the research project. Reconcile gaps
that are already resolved by completed SWUs rather than re-proposing them as work.

Target root:

- `research/mogt-agentic-conversation/`

## Reconciliation Finding

The driver gaps (from `module-formulae/INVOKE-RESULT.md` Unresolved Gaps and the
2026-06-08 `runtime-definition-refresh` report) were partly **stale**. Verified
against repo state:

| Claimed Gap | Actual State | Verdict |
| --- | --- | --- |
| `SWU-MOGT-HARNESS-002` needs runtime-receipt fixtures | `TASK-MOGT-HARNESS-002-RESULT.md` PASS; `development/fixtures/mogt-runtime-decision-receipts.jsonl` (4 rows) | resolved |
| `SWU-MOGT-HARNESS-003` needs objective/Pareto calculator | `TASK-MOGT-HARNESS-003-RESULT.md` PASS; `tools/calculate-pareto-frontier.py`; `mogt-pareto-metrics-e2.json` | resolved |
| No runtime receipt JSON Schema | Receipts stored as `MOGTRunRow` and validated only by run-row validator; receipt structure unvalidated | genuinely open |
| No objective estimator contract | Invariant RR-2 names it as enforcement; no contract existed | genuinely open |
| No production runtime adapter | Out of scope for the public research repo by README dependency policy | boundary, not work |

## Source Signals

| Signal ID | Type | Claim | Target Artifacts | Confidence | Mutation Safety |
| --- | --- | --- | --- | --- | --- |
| REFRESH-MOGT-RESEARCH-001 | artifact_drift | `INVOKE-RESULT.md` lists SWU-002/003 as pending, but both are completed. | `module-formulae/INVOKE-RESULT.md` | high | safe |
| REFRESH-MOGT-RESEARCH-002 | evidence_added | Runtime receipts need a dedicated JSON Schema; receipt structure is currently unvalidated. | `experiments/schema/mogt-runtime-decision-receipt.schema.json`, `registry/ARTIFACT-INDEX.md`, `README.md`, `PROJECT.yaml` | high | safe |
| REFRESH-MOGT-RESEARCH-003 | evidence_added | Invariant RR-2 references an objective estimator contract that does not exist. | `module-formulae/objective-estimator-contract.md`, `module-formulae/module-spec.md` | high | safe |
| REFRESH-MOGT-RESEARCH-004 | route_changed | Propagate the two open contracts into governed work as `SWU-MOGT-HARNESS-006/007`. | `development/WORK-PACK.md` | high | safe |
| REFRESH-MOGT-RESEARCH-005 | artifact_drift | `runtime-decision-receipt.md` shape table marks `decision_state` required while its minimal example omits it. | `module-formulae/runtime-decision-receipt.md` | medium | needs_review |
| REFRESH-MOGT-RESEARCH-006 | no_op | No fixture/live evidence was produced; claim evidence status must not change. | `claims/CLAIMS.md`, `results/MOGT-EVIDENCE-STATUS.md` | high | safe |

## Delta Summary

| Delta Class | Count | Summary |
| --- | ---: | --- |
| `artifact_drift` | 2 | Stale SWU gaps reconciled; receipt-contract table/example drift flagged. |
| `evidence_added` | 2 | New runtime receipt JSON Schema and objective estimator contract. |
| `route_changed` | 1 | Two new ready SWUs propagate the open contracts. |
| `no_op` | 1 | Claims and evidence status unchanged by design. |

## Applied Changes

| Path | Change | Signal |
| --- | --- | --- |
| `experiments/schema/mogt-runtime-decision-receipt.schema.json` | New JSON Schema for runtime decision receipts (draft 2020-12); validated against the contract's minimal example. | 002 |
| `module-formulae/objective-estimator-contract.md` | New design contract satisfying invariant RR-2. | 003 |
| `module-formulae/INVOKE-RESULT.md` | Reconciled stale gaps to resolved; added new outputs; repointed next route. | 001 |
| `module-formulae/module-spec.md` | Added receipt schema + estimator contract as supporting contracts; change-history entry. | 002, 003 |
| `registry/ARTIFACT-INDEX.md` | Indexed receipt schema and estimator contract. | 002, 003 |
| `README.md` | Added receipt schema and estimator contract to canonical file map. | 002, 003 |
| `PROJECT.yaml` | Surfaced module-formulae spec, runtime definition, receipt, estimator contract, and receipt schema in the canonical map. | 002, 003 |
| `development/WORK-PACK.md` | Added ready `SWU-MOGT-HARNESS-006` (wire receipt schema) and `SWU-MOGT-HARNESS-007` (objective estimator). | 004 |

## Skipped Changes

- Did not edit `runtime-decision-receipt.md` to resolve the table-vs-example
  `decision_state` drift (signal 005, `needs_review`); the schema keeps
  `decision_state` optional and the drift is flagged for the contract owner.
- Did not change `claims/CLAIMS.md` or `results/MOGT-EVIDENCE-STATUS.md` (signal 006).
- Did not implement the validator receipt mode or the estimator (routed to SWU-006/007).
- Did not run live experiments.

## Validation

Review checks:

- every applied change maps to a refresh signal;
- resolved gaps are evidenced by completed task results and present files;
- no evidence-status or paper claim upgrade was applied;
- the new schema validates the receipt contract's own minimal example.

Command checks:

```bash
# Receipt schema validates the contract's minimal example and rejects malformed receipts
python3 - <<'PY'
import json, jsonschema
s = json.load(open("research/mogt-agentic-conversation/experiments/schema/mogt-runtime-decision-receipt.schema.json"))
print("schema loaded:", s["title"])
PY

# Cross-reference the new artifacts and SWUs
rg -n "mogt-runtime-decision-receipt.schema.json|objective-estimator-contract|SWU-MOGT-HARNESS-006|SWU-MOGT-HARNESS-007" \
  research/mogt-agentic-conversation
```

## Decisions

1. Reconcile stale gaps instead of re-proposing completed SWUs as new work.
2. Author the two genuinely-missing contracts (receipt schema, objective estimator).
3. Keep the production runtime adapter out of scope per the public-repo dependency policy.
4. Flag the receipt-contract table/example drift rather than silently editing the contract.
5. Hold the claim evidence boundary: no claim or evidence-status change.

## Unresolved Gaps

- Receipt contract `decision_state` table-vs-example drift (owner: receipt contract).
- No executable estimator or receipt validation pass yet (routed to SWU-006/007).
- Live experiment approval remains blocked.

## Next Route

`task-session` for `SWU-MOGT-HARNESS-006`, then `SWU-MOGT-HARNESS-007`.
