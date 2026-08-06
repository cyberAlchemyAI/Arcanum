# Work Pack

## Identity

- Work Pack ID: `WP-PEP-20260804`
- Objective: make declared pre-execution owner prerequisites resolve before expensive Task Session work while preferring the existing plan-once route.
- Complexity: medium
- Output mode: split
- Current state: plan-ready, unselected
- Selected SWU: none

## Source artifacts

- `SPEC.md`
- `architecture-bundle.md`
- `implementation-layering.md`
- `IMPLEMENTATION-PLAN.md`
- `execution-pack.md`

## SWU frontier

| SWU | Parent task | Primary behavior | Dependency | Successor |
| --- | --- | --- | --- | --- |
| `SWU-PEP-001` | `TASK-PEP-CONTRACT` | define typed prerequisite/classification contracts | none | `SWU-PEP-002` |
| `SWU-PEP-002` | `TASK-PEP-CLASSIFIER` | classify unmet prerequisites under a structural effort bound | 001 | `SWU-PEP-003` |
| `SWU-PEP-003` | `TASK-PEP-ROUTER` | route one pre-execution owner hop without owner impersonation | 002 | `SWU-PEP-004` |
| `SWU-PEP-004` | `TASK-PEP-ROUTER` | join, revalidate, and resume the same attempt once | 003 | `SWU-PEP-005` |
| `SWU-PEP-005` | `TASK-PEP-ADOPTION` | align Invoke Plan and Implementation Readiness entry semantics | 004 | `SWU-PEP-006` |
| `SWU-PEP-006` | `TASK-PEP-INTEGRATION` | prove end-to-end behavior, regressions, public safety, and generated parity | 005 | none |

## Global constraints

- Preserve current digest, baseline, material-package, and mutation-admission checks.
- Bare work-pack prerequisite declarations never grant apply authority.
- One prerequisite phase may perform at most one owner hop.
- Do not recursively invoke Task Session or absorb arbitrary prerequisite DAGs.
- Keep all canonical examples product-neutral and public-safe.
- The current Arcanum worktree contains unrelated pending changes; every SWU must inventory exact targets and block on unexpected overlap before mutation.
- Sync generated `.agents` and `.claude` packages only after canonical validation.

## Acceptance matrix

| Case | Required result |
| --- | --- |
| unique unmet, no authorization | fast block; exact route; no Context Builder or writes |
| exact authorized hop | one owner dispatch; joined receipt; recheck; one Context Builder entry |
| already satisfied | no duplicate owner work |
| plan-once current | zero expected pre-execution Refresh calls |
| stale/expanded targets | block before owner mutation or Task Session mutation |
| ambiguous owner | block without confidence-based selection |
| repeated fingerprint/attempt | no second dispatch |
| legacy strict profile | current fail-closed behavior preserved |
| public boundary | no private identifiers or consuming-project prose |

## Validation commands

```bash
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py arcanum/arcana/task-session/development/invoke-runs/20260804T184514Z-pre-execution-owner-prerequisite-fast-path/execution.dispatch.json
bash arcanum/arcana/continuation-router/development/run-validation-fixtures.sh
python3 arcanum/spells/work-pack-readiness-audit/development/test_plan_once_end_to_end.py
python3 arcanum/arcana/task-session/development/test_plan_once_admission.py
python3 arcanum/arcana/task-session/development/test_plan_once_governance.py
git -C arcanum diff --check -- arcana/task-session arcana/continuation-router spells/invoke spells/implementation-readiness spells/work-pack-readiness-audit
```

Package-local fixture commands named in task files are planned and do not exist yet.

## Selection and next owner

No SWU is selected. The narrowest reversible first unit is `SWU-PEP-001`. Because implementation crosses existing sigil and spell lifecycle owners, validate `execution.dispatch.json`, obtain exact dispatch authorization, then route through Orchestrate. Do not start ordinary Task Session directly from this plan.
