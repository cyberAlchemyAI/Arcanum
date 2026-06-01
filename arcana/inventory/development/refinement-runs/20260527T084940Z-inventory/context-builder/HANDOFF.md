# Context Builder Handoff Pack

## Identity

- Task/SWU: `inventory-validator-next-layer`
- Source task/work-pack: `arcana/inventory/development/WORK-PACK.md`
- Session/run id: `arcanum-context-builder-20260527T084940Z-inventory`
- Session evidence path: `arcana/inventory/development/refinement-runs/20260527T084940Z-inventory/context-builder`
- Runtime handoff: `codex-goal`
- Repository revision: `93a6553`
- Evidence date: `2026-05-27`
- Builder mode: `standard`
- Strict mode: `true`
- Emit mode: `both`

## Target Task

Refine the completed Inventory evidence-card work-pack so later `task-session` runs can execute multiple disjoint tasks without foreseeable blockers.

The immediate non-executed next unit is a work-pack update plus implementation task for the shell plus `jq` agent/runtime validator. The human UI validation surface remains intentionally deferred.

## Obligation Coverage

| Obligation | Status | Selected Evidence | Resolution |
| --- | --- | --- | --- |
| O1-command-contract | covered | `.codex/commands/context-builder.md#Observer Envelope: Task Zero`; `transmutations/context-builder/SKILL.md#handoff-pack-contract` | Context Builder must emit Markdown plus JSON/index under session evidence, enforce strict coverage, and report observability closeout. |
| O2-target-state | covered | `arcana/inventory/development/WORK-PACK.md:15-22`; `arcana/inventory/development/READINESS.md:5-22` | Static POC is complete; next layer is validator-ready. |
| O3-multiple-disjoint-task-rules | covered | `arcana/inventory/development/WORK-PACK.md:50-62`; `arcana/inventory/development/EXECUTION-PACK.md:42-47` | Existing SWUs declare dependencies and write scopes; batch execution is allowed only when write scopes are disjoint and dependencies are satisfied. |
| O4-validator-runtime-surface | covered | `arcana/inventory/development/VALIDATOR-SURFACE-DECISION.md:5-20`; `arcana/inventory/development/READINESS.md:30-47` | Agent/runtime validator is shell plus `jq`. |
| O5-human-ui-surface | resolved | `arcana/inventory/development/VALIDATOR-SURFACE-DECISION.md:22-50`; `arcana/inventory/development/READINESS.md:30-35` | Human UI is deferred and must not be built in the first validator task. |
| O6-blocker-pre-resolution | covered | `arcana/inventory/development/WORK-PACK.md:64-68`; `arcana/inventory/development/task-session/SWU-INV-KS-009-RESULT.md:18-45` | `B-VALIDATOR-DEFERRED` is resolved for agent/runtime by selecting shell plus `jq`; the UI remainder is deferred. |
| O7-next-work-pack-updates | covered | `arcana/inventory/development/WORK-PACK.md:70-83`; `arcana/inventory/development/IMPLEMENTATION-PLAN.md:87-89` | Add a non-executed next task for the shell plus `jq` validator and sync board/gates before execution. |
| O8-validation-surface | covered | `arcana/inventory/development/VALIDATOR-SURFACE-DECISION.md:29-40`; `arcana/inventory/development/OBSERVABILITY.md:11-33`; `arcana/task-session/runtime-adapters/codex-goal.md#Availability Check` | Validator must check required fields, enums, selectors, profile rules, owner/status pairing, non-authority notices, and handoff source refs. |
| O9-authority-boundaries | covered | `arcana/inventory/development/work-pack/shared/SOURCE-CONTRACTS.md:44-50`; `arcana/inventory/development/POC-VALIDATION.md:80-84` | Inventory owns cards/index/lint/handoff projections only; downstream governance remains outside this task. |
| O10-codex-goal-handoff | covered | `arcana/task-session/runtime-adapters/codex-goal.md#Input Contract`; `arcana/task-session/runtime-adapters/codex-goal.md#Blocked Fallback` | Codex Goal consumes exactly one selected task/SWU and blocks if write scope, validation, or strict coverage is missing. |

Strict coverage: `pass`

## Selected Sources

- `arcana/inventory/development/WORK-PACK.md`
  - Selectors: `Control Fields`, `SWU Execution Handoff`, `Blockers`, `Gate Checks`, `Change Log`
  - Obligations: O2, O3, O6, O7
  - Evidence excerpt: Static POC is complete, readiness is validator-ready, shell plus `jq` is selected for agent runtime, prior SWUs are completed, and batch execution is constrained by disjoint write scopes.

- `arcana/inventory/development/VALIDATOR-SURFACE-DECISION.md`
  - Selectors: `Decision`, `Surface Split`, `First Validator Scope`, `Non-Goals`, `Revisit Trigger`
  - Obligations: O4, O5, O8
  - Evidence excerpt: The first executable validation surface is shell plus `jq`; the human UI is deferred; the first validator checks fields, vocabularies, selector shape, profile rules, owner/status pairing, and handoff safety.

- `arcana/inventory/development/READINESS.md`
  - Selectors: `Status`, `Acceptance Checklist`, `Validator Surface Decision`, `Next Route`
  - Obligations: O2, O4, O5, O8
  - Evidence excerpt: The static POC passes, JSON fixtures parse, handoff examples include non-authority language, README/SKILL expose behavior, and `task-session` should implement the shell plus `jq` validator.

- `arcana/inventory/development/task-session/SWU-INV-KS-009-RESULT.md`
  - Selectors: `Outcome`, `Decisions`, `Validation`, `Follow-Up`
  - Obligations: O6, O7
  - Evidence excerpt: The readiness SWU passed, but the next route identified the validator runtime blocker; the current pack later resolves that blocker through the validator surface decision.

- `arcana/inventory/development/EXECUTION-PACK.md`
  - Selectors: `Wave Status Board`, `Delivery Stage Coverage`, `Parallelization Boundaries`
  - Obligations: O3, O7
  - Evidence excerpt: The package has wave sequencing and parallelization boundaries; docs and fixture work depend on stabilized template/index contracts.

- `arcana/inventory/development/work-pack/shared/SOURCE-CONTRACTS.md`
  - Selectors: `Development Sources`, `Authority Rules`
  - Obligations: O9
  - Evidence excerpt: Inventory owns cards, indexes, lint findings, and handoff projections; Ontology Vault and Definitions Governance retain downstream authority.

- `arcana/inventory/development/POC-VALIDATION.md`
  - Selectors: `Distilled Decision Gates`, `Decision Rule`
  - Obligations: O7, O9
  - Evidence excerpt: POC continuation is decided by six data-backed gates; stop or redesign if authority boundaries cannot be made obvious.

- `arcana/inventory/development/OBSERVABILITY.md`
  - Selectors: `Signal Inventory`, `Signals`, `Traceability Rules`
  - Obligations: O8
  - Evidence excerpt: Validation and readiness telemetry should track template integrity, fixture validity, authority boundary violations, and blocker age.

- `arcana/task-session/runtime-adapters/codex-goal.md`
  - Selectors: `Availability Check`, `Input Contract`, `Blocked Fallback`
  - Obligations: O10
  - Evidence excerpt: Codex Goal handoff needs a selected task/SWU, bounded write scope, concrete done criteria, validation evidence, Markdown handoff, JSON/index, and strict coverage.

## Architecture Guidance

Keep the validator as an Inventory agent/runtime surface, not a human review UI and not downstream governance. Implement it as shell plus `jq` first, compose it with local command flows, and block before mutation if the selected task lacks a bounded write scope, done criteria, or validation command.

Use the existing work-pack split instead of merging back into a monolithic plan. The next work should add a new non-executed task/SWU for the validator layer, then execute that single unit through `task-session`.

## Related Feature Context

The completed evidence-card package already produced production templates, lint/index contracts, pilot fixtures, handoff examples, docs updates, readiness notes, and task-session evidence for SWU-INV-KS-001 through SWU-INV-KS-009. This context pack should start after that state, not re-run those completed SWUs.

## Constraints And Non-Goals

- Do not build the deferred human UI in the first validator task.
- Do not require Python, Node, or TypeScript before shell plus `jq` proves insufficient.
- Do not make Inventory responsible for Ontology Vault promotion or Definitions Governance acceptance.
- Do not mutate CyberAlchemy source material while validating Inventory fixtures.
- Do not run multiple task-session units together unless their write scopes are disjoint and dependencies are already satisfied.
- Do not treat handoff packets as downstream promotion authority.

## Write Scope

Allowed for the next non-executed work-pack update:

- `arcana/inventory/development/WORK-PACK.md`
- `arcana/inventory/development/EXECUTION-PACK.md`
- `arcana/inventory/development/IMPLEMENTATION-PLAN.md`
- `arcana/inventory/development/work-pack/tasks/TASK-007-validator-runtime.md`
- `arcana/inventory/development/work-pack/waves/W4-validator-runtime.md`

Allowed for the later validator implementation task, after the work-pack update names it:

- `arcana/inventory/scripts/`
- `arcana/inventory/development/pilot/evidence-card/`
- `arcana/inventory/templates/`
- `arcana/inventory/development/task-session/`

## Proposed Non-Executed Work-Pack Updates

Add a new task row:

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-007 | Implement shell plus `jq` agent/runtime validator. | L4 | medium | W4 | `VALIDATOR-SURFACE-DECISION.md`, `READINESS.md` | ready-after-board-sync | not-started |

Add SWUs:

| SWU ID | Parent Task | Dependencies | Write Scope | Done Criteria | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-INV-KS-010 | TASK-007 | TASK-001..TASK-006 | `arcana/inventory/scripts/validate-evidence-card-fixtures.sh` or equivalent shell+jq validator path | Validator checks required fields, enums, selectors, full/minimal profiles, owner/status pairing, relation notices, handoff source refs, and packet non-authority text. | run validator against pilot fixtures and invalid examples | local-fallback | not-started |
| SWU-INV-KS-011 | TASK-007 | SWU-INV-KS-010 | `WORK-PACK.md`, `READINESS.md`, task-session result evidence | Work-pack records validator result, preserves deferred UI status, and names any remaining blocker. | checklist review plus validator output path | local-fallback | not-started |

Batch rule for future task-session runs:

1. Run the work-pack board-sync SWU first.
2. Run validator implementation and evidence-sync as separate SWUs unless the board explicitly grants a disjoint write-scope batch.
3. Permit parallel execution only when every SWU has no dependency edge between them and their write scopes do not overlap.
4. If a batch discovers a shared file, stop the batch and reroute to sequential task-session execution.
5. Every runtime handoff must carry the Markdown pack and JSON/index path from this directory.

## Validation Surface

- `jq empty arcana/inventory/development/pilot/evidence-card/*.json`
- shell plus `jq` checks for required fields and controlled vocabularies in pilot card fixtures.
- shell plus `jq` checks for selector shape, full/minimal profile rules, `promotion_owner` and terminal status pairing.
- shell plus `jq` checks that handoff packets include `source_refs` and non-authority text.
- `rg -n "TASK-007|SWU-INV-KS-010|SWU-INV-KS-011|shell plus.*jq|human UI.*deferred" arcana/inventory/development/WORK-PACK.md arcana/inventory/development/work-pack/tasks/TASK-007-validator-runtime.md`

## Gaps And Blockers

- `G-DEFERRED-HUMAN-UI`: deferred, runtime fallback not allowed. Human UI is outside this task and should be revisited only if shell plus `jq` reports become too hard to inspect.
- `G-CODEX-GOAL-AVAILABILITY`: resolved for this context pack as a handoff target, but the actual runtime must check native Codex Goals availability before delegation.
- `G-WORK-PACK-NOT-YET-MUTATED`: resolved by this pack as an explicit next action. This context-builder run does not mutate canonical planning artifacts.

## Authority Precedence

1. `.codex/commands/context-builder.md`
2. `transmutations/context-builder/SKILL.md`
3. `arcana/inventory/development/WORK-PACK.md`
4. `arcana/inventory/development/VALIDATOR-SURFACE-DECISION.md`
5. `arcana/inventory/development/READINESS.md`
6. `arcana/task-session/runtime-adapters/codex-goal.md`

## Fallback Exploration Rule

Broad repository exploration is allowed only for these named gaps:

- checking Codex Goal runtime availability for `G-CODEX-GOAL-AVAILABILITY`;
- locating an existing Inventory validator script before creating a new one;
- resolving a concrete `jq` validation rule that cannot be expressed from the selected evidence above.

Any extra source must be listed in the task-session result with the named gap that justified it.

## Provenance

- Source refs: `.codex/commands/context-builder.md`; `transmutations/context-builder/SKILL.md`; selected Inventory development files listed above.
- Content revision: `93a6553` plus local uncommitted worktree state.
- Builder mode: `standard`
- Files selected: 11
- Snippets selected: 31
- Excerpt budget: within standard mode limit.
- Noise ratio: `0.00`; every selected source maps to at least one obligation.

## Output Paths

- Markdown: `arcana/inventory/development/refinement-runs/20260527T084940Z-inventory/context-builder/HANDOFF.md`
- JSON/index: `arcana/inventory/development/refinement-runs/20260527T084940Z-inventory/context-builder/index.json`
