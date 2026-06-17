# Refine Result: Database Selection And Migration Commands

Status: pass-with-residue
Run ID: 20260616T204823Z-database-selection-migration-commands-refine
Dispatch ID: refine-20260616T204823Z-database-selection-migration-commands
Preset: full
Research: bounded-research

## Final Synthesis

Model database selection as an **IntegrationSpec-local data-resource decision record** and model migration commands as an **IntegrationSpec-local migration command profile**.

Use DomainSpec for host application meaning:

- `Operation` and `Query`: why the host reads or writes data.
- `Interface`: how callers access the host behavior.
- `Mapping`: data transformations between host models, schemas, projections, payloads, and query shapes.
- `Policy`: consistency, retention, privacy, timeout, idempotency, backfill, rollback, and operational constraints.
- `Workflow`, `Saga`, `Event`: multi-step behavior, compensation, projections, and reconciliation.

Use IntegrationSpec-local vocabulary for resource and command machinery:

```text
DomainSpec Operation/Query/Workflow
  -> Data Resource Boundary
  -> Integration Data Resource Decision Record
  -> selected Data Resource
  -> Database Migration Command Profile
  -> Evidence Anchors and Failure Fixtures
```

## Data Resource Decision

Required fields:

- `resource_role`
- `resource_family`
- `source_of_truth_role`
- `workload_access_patterns`
- `data_shape`
- `consistency_model`
- `atomicity_scope`
- `latency_throughput_targets`
- `volume_growth`
- `retention_lifecycle`
- `migration_backfill_plan`
- `security_governance`
- `failure_modes`
- `alternatives_rejected`
- `evidence_anchors`

Special resource roles such as cache, search, vector, and analytics need extra freshness, rebuild, lineage, privacy propagation, and fallback fields.

## Migration Command Profile

Required fields:

- `tool`
- `environment`
- `target_database`
- `command_class`
- `command`
- `migration_artifacts`
- `schema_history_resource`
- `checksum_policy`
- `drift_precheck`
- `lock_policy`
- `dry_run_artifact`
- `apply_policy`
- `rollback_or_roll_forward_policy`
- `expand_contract_stage`
- `backfill_plan`
- `destructive_gate`
- `approval_record`
- `evidence_fixtures`

Production defaults:

- apply reviewed artifacts only;
- separate drift/status validation from deploy;
- block reset/clean/drop by default;
- prefer roll-forward recovery;
- allow rollback only when reversible logic, data limits, and target revision semantics are documented;
- gate repair/baseline/stamp/fake/resolve/lock-release commands because they mutate migration truth.

## Validator Scope

A future validator can check required fields, local relation shape, links, fixture classes, and evidence anchors. It must not claim architecture correctness, runtime truth, or DomainSpec taxonomy promotion.

## Bridge Decisions

| Claim | Decision |
| --- | --- |
| Database selection needs explicit IntegrationSpec modeling | promotion-candidate |
| Migration commands need environment-scoped command profiles | promotion-candidate |
| Data-resource families as DomainSpec meta-types | block |
| Migration commands as DomainSpec meta-types | block |
| Runtime receipts as canonical spec truth | block |
| Runtime receipts as task-session evidence | borrow-carefully |
| Formula validator after examples | promotion-candidate |
| Tool-specific migration profiles | future-work |

## Recommended Next Route

Build L0 first:

1. Draft `INTEGRATION-BOUNDARY-DISCIPLINE.md`.
2. Add `Integration Data Resource Decision Record`.
3. Add `Database Migration Command Profile`.
4. Fill the payment/database example.
5. Add pass/flag/block fixtures for source-of-truth gaps, cache/search/vector/analytics authority mistakes, prod destructive commands, lock release, checksum repair, drift omissions, and runtime-truth promotion.
6. Route `integrations.md` and formula validator work only after the L0 fields stabilize.

## Stage Evidence

| Stage | Status | Artifact |
| --- | --- | --- |
| Context Builder evidence baseline | pass | `stages/01-context-builder/context-pack.md` |
| Invoke Define | pass | `stages/02-invoke-define.md` |
| Interrogation refine-review | pass | `stages/03-refine-review.md` |
| Research decision | pass | `stages/04-bounded-research.md` |
| Distill | pass | `stages/05-distill.md` |
| Invoke Redefine / Design | pass | `stages/06-invoke-design.md` |
| Interrogation refine-design-review | pass-with-residue | `stages/07-refine-design-review.md` |
| Distill Repair | pass | `stages/08-distill-repair.md` |
| Invoke Plan | pass | `stages/09-invoke-plan.md` |
| Final Interrogation | pass-with-residue | `stages/10-final-interrogation.md` |

## Subagent Receipts

| Role | Status | Receipt |
| --- | --- | --- |
| `data-resource-selection-mapper` | pass-with-residue | `stages/subagent-receipts/data-resource-selection-mapper.md` |
| `migration-command-governor` | pass | `stages/subagent-receipts/migration-command-governor.md` |
| `domainspec-data-boundary-guardian` | pass-with-boundary-warnings | `stages/subagent-receipts/domainspec-data-boundary-guardian.md` |

## Residue

- Exact local names remain L0 decisions.
- Tool-specific profiles are deferred.
- No live database commands were executed.
- No canonical DomainSpec definitions were mutated.
