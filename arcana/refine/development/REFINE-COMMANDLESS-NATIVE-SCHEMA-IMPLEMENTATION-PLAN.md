---
module: refine-commandless-native-schema
status: implemented-with-known-flag
docType: implementation-plan
owner: refine
authoredBy: invoke-plan-through-refine-strategy
dispatch: arcana/refine/development/REFINE-COMMANDLESS-NATIVE-SCHEMA-DISPATCH.json
---

# Refine Commandless Native Schema Implementation Plan

## Invoke Result

- Mode: `plan`
- Spell: `invoke`
- Canonical ID: `invoke`
- Scope: library
- Phase status: `pass`
- Mode contract: `spells/invoke/plan.md`
- Outputs: this implementation plan and `arcana/refine/development/REFINE-COMMANDLESS-NATIVE-SCHEMA-DISPATCH.json`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Glossary consistency: `pass`, using existing Arcanum terms `native skill`, `dispatch-spec`, `subagent_strategy`, `receipt`, `generated-runtime-package`, and `historical evidence`
- Implementation layering: included inline
- Work-pack: split-ready single-file plan
- Complexity: `medium`
- Per-layer planning: L0, L1, L2, L3
- Implementation detail: task specs complete
- Smallest working units: complete
- Refresh: proposal-only refresh plan
- Target artifact: Refine and Invoke active governance surfaces, dispatch-spec schema enforcement, generated native runtime packages, and validation fixtures
- Template or recipe selection: standalone implementation-layering plus work-pack structure from `spells/invoke/plan.md`
- Decisions: remove deprecated command-interface dependency from active Refine/Invoke governance; enforce route and receipt evidence through dispatch-spec schemas/validators and native skill/subagent receipts; preserve historical evidence as classified history
- Unresolved gaps: implementation not yet executed; generated/live install mutation still requires a later approved task-session; exact installed package refresh scope must be selected before mutation
- Next route: `task-session`

## Refine Run Strategy Proposal

- Target: `arcana/refine`, `spells/invoke`, `formulae/dispatch-spec`, and generator/validation surfaces that still encode command-interface execution proof
- Desired outcome: implementation-ready, non-executed plan to remove deprecated command-interface dependency and enforce schema-backed native skill/subagent execution evidence
- Preset: `standard`
- Research: `no-research`
- Dispatch route: `arcana/refine/development/REFINE-COMMANDLESS-NATIVE-SCHEMA-DISPATCH.json`
- Selected overlays:
  - `route_menu_for_policy_tension`: existing plans kept compatibility language, while the operator now wants active command-interface dependency removed.
  - `subagent_schema_receipts`: the work spans active contracts, schemas, validators, generated packages, and validation fixtures.
- Subagent strategy: `recommended`
- Proposed subagents:
  - `active-contract-auditor`: active Refine/Invoke/generated-package wording inventory and replacement categories.
  - `schema-validator-auditor`: schema, validator, fixture, and receipt enforcement gaps.
  - `install-surface-auditor`: bootstrap/generated-runtime-package assumptions and live install refresh risks.
- Join policy: `parent_synthesis`
- Receipt requirements: `agent_id`, `role_id`, `spawn_status`, `join_status`, `close_status`, `residue`, `reroute`, `files_or_surfaces_reviewed`, `findings`, `validation_impact`
- Runtime plan after confirmation: execute one SWU at a time through `task-session`; spawn subagents only for audit or disjoint implementation lanes with explicit write scopes and receipts.
- Deferred work: source mutation, live installed package refresh, and generated-runtime-package mutation until an approved task-session selects the first SWU.
- Confirmation prompt: approve the plan, then start `SWU-RCNS-001` through Task Session.

## Current Problem

The active Refine contract and validation package still contain command-interface assumptions:

- Active Refine text still says runtime-backed stages resolve through `tools/arcanum --resolve` and may use `tools/arcanum --exec`.
- Refine validation currently blocks when `tools/arcanum --resolve refine`, `/refine`, `invoke`, or `interrogation` fail.
- The Refine dispatch template still has a `g03-command-resolution` gate.
- Some example prompts and expected fixtures still require deterministic `tools/arcanum` stage dispatch as proof.
- Existing migration plans already moved toward native skill/subagent execution, but they preserve `tools/arcanum` as a deterministic resolver/compatibility surface. The operator's current direction is stricter: command interface is deprecated and should not be required by active Refine/Invoke governance.

This plan does not delete historical refinement runs. Historical run folders can continue to mention command surfaces as preserved evidence. The implementation work must change active contracts, validators, templates, generated packages, and validation fixtures so command-interface resolution cannot satisfy or block active Refine/Invoke success.

## Definition Refresh

| Term | Refreshed Definition | Enforcement |
| --- | --- | --- |
| Active command interface | Deprecated `.codex/commands`, slash-command, command-file, or `tools/arcanum --resolve <command>` surface used as execution proof. | Must be removed from active Refine/Invoke success gates. |
| Native capability handle | Stable skill/sigil/spell id resolved by the current host runtime or generated native package metadata. | Required for stage ownership and receipt attribution. |
| Native receipt | Artifact or structured record returned by a native skill, parent coordinator, or approved subagent with status, verdict/blocker, owner, mode, and artifact path. | Required before a stage can be marked `pass`. |
| Dispatch route | Schema-validated route document that owns ordering, gates, subagent strategy, technique use, receipts, and observability grouping. | Must validate before runtime-backed work. |
| Legacy compatibility surface | Explicitly marked adapter or installer path kept for migration tests or old integrations. | Preserved but cannot be a default or active success dependency. |
| Historical evidence | Prior generated runs, dry-run records, benchmark attempts, or blocked command-surface evidence. | Preserved and excluded from active readiness blockers unless imported by a current contract. |

## Architecture Refresh

### Context View

Refine remains the discovery/design orchestrator. Invoke remains the authoring front door for define, design, and plan artifacts. Dispatch Spec becomes the enforceable route and receipt schema. Native skills and approved subagents provide execution evidence.

### High-Level Structure

```text
operator intent
  -> refine strategy proposal
  -> dispatch-spec route validation
  -> invoke-authored definition/design/plan artifacts
  -> task-session implementation SWUs
  -> native skill/subagent receipts
  -> manifest/index/readiness validation
```

The command interface leaves this active chain. It can remain only in a legacy compatibility lane outside Refine/Invoke success criteria.

### Low-Level Components

| Component | Owner | Required Change |
| --- | --- | --- |
| `arcana/refine/SKILL.md` | Refine | Replace command-resolution/stage-dispatch requirements with native capability handle and receipt requirements. |
| `arcana/refine/REFINEMENT-LOOP.md` | Refine | Rewrite runtime section around native skills/subagents and dispatch receipts. |
| `arcana/refine/templates/refine-dispatch.json` | Refine + Dispatch Spec | Remove command-resolution gate; add native capability/receipt gates. |
| `arcana/refine/templates/run-manifest.md` | Refine | Replace `Command` / `Command file` fields with capability handle, receipt kind, owner, status, and artifact path. |
| `arcana/refine/templates/evidence-index.json` | Refine | Replace `command` and `command_file` keys with native capability and receipt keys. |
| `arcana/refine/templates/reflection-report.md` | Refine | Replace command-dispatch observability checks with native receipt and subagent lifecycle checks. |
| `arcana/refine/scripts/generate-refine-dispatch.py` | Refine | Replace "before command-backed stage execution" and permission prompts with native runtime wording. |
| `arcana/refine/development/run-validation-fixtures.sh` | Refine | Stop blocking on `tools/arcanum --resolve`; validate native package metadata, dispatch route, receipt fields, and final artifact completeness. |
| `arcana/refine/development/VALIDATION.md` | Refine | Refresh stale command-resolution validation commands and promotion criteria. |
| `spells/invoke/README.md`, mode contracts | Invoke | Ensure plan/design/define route through native capability handles and no command-interface success gates. |
| `formulae/dispatch-spec/dispatch.schema.yml` | Dispatch Spec | Add explicit native capability and receipt shape where current schema is too permissive. |
| `formulae/dispatch-spec/scripts/validate-dispatch.py` | Dispatch Spec | Block command-interface execution gates in active routes unless marked legacy compatibility. |
| `tools/arcanum` | Legacy/deterministic runtime helper | Stop using command-resolution failure as native Refine stage proof failure when native capability execution is available; otherwise mark as legacy compatibility. |
| `tools/bootstrap_arcanum.sh` | Runtime package generator | Generate native packages without `.codex/commands` by default and avoid active guidance that treats command interface as default. |

## Existing Enforcement To Reuse

Dispatch Spec already has useful schema and validator support:

- `subagent_strategy` and `subagent_lifecycle` are present in `formulae/dispatch-spec/dispatch.schema.yml`.
- The validator already blocks missing subagent lifecycle receipt fields, pending joins/closes, missing completed receipts, bad step references, validation evidence gaps, false promotion authority, unknown techniques, and direct execution-evidence-to-canonical-promotion paths.
- `boundary_evidence.receipts`, `state_namespaces`, and `promotion_splits` already provide a schema-backed place to express cross-capability evidence and authority boundaries.
- Invoke Plan already defines SWU-level execution-owner recommendations, source anchors, and an expected subagent result shape.

The remaining work is not to invent dispatch governance from scratch. It is to remove command-interface dependency from active Refine/Invoke governance and make native capability handles and richer receipts first-class validator targets.

### Workflow Process View

1. Refresh definitions and active policy boundaries.
2. Refresh Refine architecture and dispatch template to native capability/receipt terms.
3. Refresh Invoke define/design/plan contracts where command-interface assumptions remain.
4. Harden dispatch schema and validator.
5. Update Refine validation fixtures and expected examples.
6. Update generator/bootstrap package text and install profiles.
7. Run staged validation.
8. Run live install refresh only after explicit approval.
9. Run final active-surface audit.

### Decision Flow View

| Decision | Default | Reason |
| --- | --- | --- |
| Should active Refine/Invoke require `tools/arcanum --resolve`? | No | The operator marked command interface deprecated. |
| Should `tools/arcanum` be deleted? | Not in this plan | It may remain as legacy compatibility or deterministic tooling, but outside Refine/Invoke success gates. |
| Should historical evidence be rewritten? | No | It is prior-run evidence and should be classified, not mutated. |
| Should subagents be used? | Recommended for audit and disjoint implementation lanes | The migration spans independent surfaces and benefits from receipt-backed review. |
| Should live installed packages be mutated now? | No | That requires a later approved task-session. |

### Dependency Interface View

| Dependency | Required Interface |
| --- | --- |
| Dispatch Spec schema | Validates route shape, subagent strategy, receipts, gates, observability, and boundaries. |
| Dispatch Spec validator | Enforces governance beyond schema shape. |
| Native Codex skill packages | Provide capability ids and runtime guidance. |
| Subagent runtime | Optional execution support with explicit permission and receipts. |
| Task Session | Executes approved SWUs one at a time after this plan. |
| Bootstrap generator | Regenerates native runtime packages from canonical source. |

## Implementation Layering

| Layer | Question | Work | Promotion Evidence |
| --- | --- | --- | --- |
| L0 policy proof | Can active command-interface dependency be removed without touching historical evidence? | Update definitions, classify active vs historical references, and rewrite validation target language. | Active grep report has no unclassified command-interface success gates. |
| L1 Refine route proof | Can Refine represent the canonical loop through native capability handles and receipts? | Update Refine skill, loop doc, dispatch template, generator, and validation fixture expectations. | Refine dispatch validates and validation fixtures no longer require command resolution. |
| L2 Invoke authoring proof | Can Invoke produce define/design/plan artifacts for this migration without command-interface assumptions? | Refresh Invoke docs/contracts and add plan/readiness wording for native receipts and SWU subagent handoff. | Invoke validation passes and no active Invoke contract depends on `.codex/commands`. |
| L3 schema enforcement | Can dispatch-spec block drift instead of relying on prose? | Add schema/validator rules for native receipts, command-interface deprecation, and subagent lifecycle closeout. | New pass/block fixtures prove enforcement. |
| L4 generated/install rollout | Can generated native packages and live installs reflect the new architecture? | Update bootstrap generator, staged installs, and optional live package refresh after approval. | Staged validation passes; live refresh has backup and smoke evidence if approved. |

## Work Pack

### TASK-RCNS-001: Active Surface Inventory And Boundary Refresh

- Owner route: `task-session`
- Layer: L0
- Write scope:
  - `arcana/refine/development/`
  - report-only grep inventory
- Goal: Identify active command-interface dependencies and classify historical/legacy references.
- Steps:
  1. Search active canonical files for `.codex/commands`, slash command resolution, `command-backed`, `command file`, `tools/arcanum --resolve`, and `tools/arcanum --exec`.
  2. Classify each hit as `remove`, `rewrite-native-receipt`, `legacy-compatibility`, `historical-preserve`, or `deterministic-tooling-outside-success-gate`.
  3. Update this plan if a blocker-level unknown appears.
- Validation:
  - `rg -n "tools/arcanum --resolve|tools/arcanum --exec|\\.codex/commands|command-backed|command file|slash command|/refine|/invoke" arcana/refine spells/invoke formulae/dispatch-spec tools/bootstrap_arcanum.sh --glob '!**/development/refinement-runs/**'`

### TASK-RCNS-002: Refresh Refine Active Contract To Native Receipts

- Owner route: `task-session`
- Layer: L1
- Write scope:
  - `arcana/refine/SKILL.md`
  - `arcana/refine/README.md`
  - `arcana/refine/REFINEMENT-LOOP.md`
  - `arcana/refine/templates/runtime-handoff.md`
  - `arcana/refine/templates/run-manifest.md`
  - `arcana/refine/templates/evidence-index.json`
  - `arcana/refine/templates/reflection-report.md`
- Goal: Remove command-interface execution requirements from the canonical Refine contract.
- Implementation detail:
  - Replace command terms with `capability handle`, `native skill receipt`, `subagent receipt`, and `dispatch step`.
  - Keep `tools/arcanum` only if clearly labelled legacy compatibility or deterministic helper outside active stage proof.
  - Refine stage evidence must be artifact-backed native receipts or explicit blocked reasons.
  - Run manifest, evidence index, runtime handoff, and reflection templates must all use the same native receipt vocabulary.
  - Simple operator sentence policy must still stop at strategy proposal before execution.
- Validation:
  - Active Refine docs contain no unclassified command-interface success gates.
  - Refine quality bar names native receipt evidence and subagent closeout.

### TASK-RCNS-003: Refresh Refine Dispatch Template And Generator

- Owner route: `task-session`
- Layer: L1
- Write scope:
  - `arcana/refine/templates/refine-dispatch.json`
  - `arcana/refine/scripts/generate-refine-dispatch.py`
- Goal: Make generated `REFINE-DISPATCH.json` commandless by default.
- Implementation detail:
  - Replace `g03-command-resolution` with `g03-native-capability-receipts`.
  - Replace permission prompts that mention command-backed stages.
  - Add or preserve `subagent_strategy` with lifecycle receipt requirements.
  - Ensure generated dispatch still validates against dispatch-spec.
- Validation:
  - `python3 arcana/refine/scripts/generate-refine-dispatch.py --seed arcana/refine/development/fixtures/refine-dispatch-seed.json --output /tmp/refine-commandless-dispatch.json --validate`
  - `formulae/dispatch-spec/scripts/validate-dispatch.py /tmp/refine-commandless-dispatch.json`

### TASK-RCNS-004: Refresh Refine Validation Fixtures

- Owner route: `task-session`
- Layer: L1
- Write scope:
  - `arcana/refine/development/run-validation-fixtures.sh`
  - `arcana/refine/development/fixtures/*`
  - `arcana/refine/development/example-prompts/*`
  - `arcana/refine/development/VALIDATION.md`
  - `tools/arcanum` only where native Refine helper behavior still blocks on command resolution
- Goal: Stop treating deprecated command resolution as required live evidence.
- Implementation detail:
  - Remove blocking checks for `tools/arcanum --resolve refine`, `/refine`, `invoke`, and `interrogation`.
  - Add checks for dispatch validation, native package metadata or capability ids, receipt fields, manifest/index artifact completeness, and subagent lifecycle closeout when subagents are used.
  - Update example prompts and expected outputs so they request native skill/subagent receipts.
  - If `tools/arcanum` keeps a native Refine helper, it must report native capability unavailability separately from deprecated command-resolution failure.
- Validation:
  - `arcana/refine/development/run-validation-fixtures.sh`

### TASK-RCNS-005: Refresh Invoke Authoring Contracts

- Owner route: `task-session`
- Layer: L2
- Write scope:
  - `spells/invoke/README.md`
  - `spells/invoke/define.md`
  - `spells/invoke/design.md`
  - `spells/invoke/plan.md`
  - `spells/invoke/development/VALIDATION.md`
- Goal: Ensure Invoke can author refreshed definitions, designs, and implementation plans without relying on command-interface availability.
- Implementation detail:
  - Define mode records native capability and receipt vocabulary where it authors lifecycle artifacts.
  - Design mode requires architecture bundles to state runtime substrate and receipt strategy.
  - Plan mode requires SWU subagent handoff to include native receipt result shape.
  - Validation no longer treats `.codex/commands` or command resolution as active readiness evidence.
- Validation:
  - `rg -n "tools/arcanum --resolve|tools/arcanum --exec|\\.codex/commands|command-backed|command file" spells/invoke --glob '!**/development/refinement-runs/**'`
  - Remaining hits are explicitly historical, legacy compatibility, or migration notes.

### TASK-RCNS-006: Harden Dispatch Schema And Validator

- Owner route: `task-session`
- Layer: L3
- Write scope:
  - `formulae/dispatch-spec/dispatch.schema.yml`
  - `formulae/dispatch-spec/dispatch.schema.json`
  - `formulae/dispatch-spec/scripts/validate-dispatch.py`
  - `formulae/dispatch-spec/development/fixtures/*`
- Goal: Enforce commandless native capability and receipt semantics through schema and validator rules.
- Implementation detail:
  - Add explicit receipt shape or strengthen `boundary_evidence.receipts` for native stage receipts. Today's dispatch schema only permits generic receipt fields (`run_id`, `session_id`, `artifacts`, `validation_result`, `approval_record`, `audit_reference`, `residue`), so this task should decide whether to extend the enum or add a dedicated `native_stage_receipts` object.
  - Enforce that every `subagent_lifecycle.agents[].role_id` matches a role declared in `subagent_strategy.roles`.
  - Upgrade important `subagent_strategy` fields from soft guidance to hard blockers when status is `recommended` or `required`: `trigger`, `parallelism`, `permission_prompt`, role list, join policy, authorization, and receipt requirements.
  - Require `subagent_lifecycle` when a route claims pass after approved delegated execution.
  - Add native receipt fields for `dispatch_id`, `step_id`, `capability_ref`, `status`, `artifacts`, `validation`, `observer_status`, `blockers`, `residue`, and `handoff_note`.
  - Define a native capability-handle validation rule independent of `.codex/commands`: dispatch `capability_ref` must match installed/native skill handles, known canonical Arcanum capability ids, or explicit candidate metadata.
  - Add validator rule: active dispatch gates must not require command-interface resolution unless the route is explicitly marked `legacy-compatibility`.
  - Add validator rule: a `pass` subagent lifecycle requires terminal join and close status plus receipt or residue/reroute.
  - Add block fixture for command-interface required as active proof.
  - Add pass fixture for native capability/receipt route.
- Validation:
  - `formulae/dispatch-spec/development/run-validation-fixtures.sh`
  - `formulae/dispatch-spec/scripts/validate-dispatch.py arcana/refine/development/REFINE-COMMANDLESS-NATIVE-SCHEMA-DISPATCH.json`

### TASK-RCNS-007: Refresh Bootstrap And Generated Runtime Packages

- Owner route: `task-session`
- Layer: L4
- Write scope:
  - `tools/bootstrap_arcanum.sh`
  - generated package templates and profile text
  - staged install roots under `/tmp`
- Goal: Generated native packages should not reinstall deprecated command-interface dependencies by default.
- Implementation detail:
  - Ensure `.codex/commands` generation requires an explicit legacy flag.
  - Generated `refine` and `invoke` packages should point to canonical source and native receipt/schema behavior.
  - Bootstrap smoke should validate native package presence, dispatch schema assets, and receipt guidance instead of slash commands.
- Validation:
  - `bash -n tools/bootstrap_arcanum.sh`
  - staged personal and repo installs in `/tmp`
  - package grep for unclassified command-interface requirements

### TASK-RCNS-008: Final Active Readiness Audit

- Owner route: `task-session`
- Layer: L4
- Write scope:
  - `arcana/refine/development/`
  - `formulae/dispatch-spec/development/`
- Goal: Produce a final report proving active Refine/Invoke governance is commandless and schema-enforced.
- Validation:
  - Active grep has no unclassified command-interface success gates.
  - Refine validation passes or flags only non-blocking live execution evidence.
  - Dispatch-spec fixtures pass.
  - Generated staged packages pass smoke.
  - Any live installed package refresh is backed up and explicitly approved.

## Smallest Working Units

| SWU | Parent Task | Goal | Write Scope | Dependencies | Execution Owner | Acceptance Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-RCNS-001 | TASK-RCNS-001 | Inventory active command-interface dependencies and classify them. | report only | none | local-fallback | classification report has no unknown active hits. |
| SWU-RCNS-002 | TASK-RCNS-002 | Rewrite Refine skill and loop docs to native receipts. | `arcana/refine/SKILL.md`, `README.md`, `REFINEMENT-LOOP.md` | SWU-RCNS-001 | subagent or local-fallback | active Refine wording has no command-interface execution requirement. |
| SWU-RCNS-003 | TASK-RCNS-003 | Make generated Refine dispatch commandless. | template and generator | SWU-RCNS-002 | local-fallback | generated dispatch validates and contains native receipt gate. |
| SWU-RCNS-004 | TASK-RCNS-004 | Update Refine validation and examples. | validation fixtures and examples | SWU-RCNS-003 | subagent or local-fallback | Refine validation no longer blocks on command resolution. |
| SWU-RCNS-005 | TASK-RCNS-005 | Refresh Invoke contracts for native receipt planning. | `spells/invoke/*` active contracts | SWU-RCNS-001 | subagent or local-fallback | Invoke grep has no unclassified command-interface readiness gates. |
| SWU-RCNS-006 | TASK-RCNS-006 | Add dispatch validator command-interface block rule and native receipt fixtures. | dispatch schema, validator, fixtures | SWU-RCNS-003 | local-fallback | pass and block fixtures prove enforcement. |
| SWU-RCNS-007 | TASK-RCNS-007 | Refresh bootstrap generated package behavior. | `tools/bootstrap_arcanum.sh`, staged installs | SWU-RCNS-002, SWU-RCNS-005, SWU-RCNS-006 | local-fallback | staged packages do not generate deprecated commands unless explicitly requested. |
| SWU-RCNS-008 | TASK-RCNS-008 | Final active readiness audit. | report only | SWU-RCNS-004, SWU-RCNS-006, SWU-RCNS-007 | local-fallback | final audit proves commandless active governance or records exact blockers. |

## Subagent Execution Strategy For Implementation

Use subagents only after the plan is approved and only when the SWU has disjoint write scope.

| Role | Recommended SWUs | Write Scope | Parent Join Rule |
| --- | --- | --- | --- |
| `active-contract-auditor` | SWU-RCNS-001, SWU-RCNS-002, SWU-RCNS-005 | audit report or active contract docs only | parent verifies grep and reconciles wording. |
| `schema-validator-auditor` | SWU-RCNS-006 | dispatch schema, validator, fixtures | parent runs fixture suite and reviews block/pass behavior. |
| `install-surface-auditor` | SWU-RCNS-007 | bootstrap/generator and staged install report | parent runs staged install and ensures live mutation is not performed without approval. |

Every subagent result must return:

```yaml
swu_id: <id>
result: pass | flag | block | interrupted
files_touched:
  - <path or none>
validation:
  - <command or review check and result>
blockers:
  - <blocker or none>
handoff_note: <what the parent coordinator needs next>
```

## Gates

| Gate | Owner | Condition | On Fail |
| --- | --- | --- | --- |
| G-RCNS-001 | Refine | Active Refine governance no longer requires command interface for stage proof. | block |
| G-RCNS-002 | Invoke | Invoke define/design/plan authoring no longer treats command interface as readiness evidence. | block |
| G-RCNS-003 | Dispatch Spec | Schema and validator enforce native receipts, subagent lifecycle, and command-interface deprecation. | block |
| G-RCNS-004 | Bootstrap | Deprecated `.codex/commands` generation requires explicit legacy selection. | block |
| G-RCNS-005 | Task Session | Historical run evidence is preserved and excluded from active blocker counts. | flag |
| G-RCNS-006 | User | Live installed package mutation requires explicit approval and backup. | block |

## Validation Commands

```bash
formulae/dispatch-spec/scripts/validate-dispatch.py arcana/refine/development/REFINE-COMMANDLESS-NATIVE-SCHEMA-DISPATCH.json
arcana/refine/development/run-validation-fixtures.sh
formulae/dispatch-spec/development/run-validation-fixtures.sh
rg -n "tools/arcanum --resolve|tools/arcanum --exec|\\.codex/commands|command-backed|command file|slash command|/refine|/invoke" arcana/refine spells/invoke formulae/dispatch-spec tools/bootstrap_arcanum.sh --glob '!**/development/refinement-runs/**'
bash -n tools/bootstrap_arcanum.sh
python3 arcana/refine/scripts/generate-refine-dispatch.py --seed arcana/refine/development/fixtures/refine-dispatch-seed.json --output /tmp/refine-commandless-dispatch.json --validate
```

## Blockers And Gaps

| ID | Status | Gap | Owner | Clear By |
| --- | --- | --- | --- | --- |
| B-RCNS-001 | closed | Active Refine validation no longer blocks on command resolution. The current example output still flags missing native receipt proof. | Refine | SWU-RCNS-004 |
| B-RCNS-002 | closed | Refine dispatch template now uses `g03-native-capability-receipts`. | Refine + Dispatch Spec | SWU-RCNS-003 |
| B-RCNS-003 | closed | Dispatch validator blocks active command-interface proof gates unless the route is explicitly legacy compatibility. | Dispatch Spec | SWU-RCNS-006 |
| B-RCNS-004 | closed | Validator now checks native capability handle shape and flags non-canonical handles without candidate metadata. | Dispatch Spec | SWU-RCNS-006 |
| B-RCNS-005 | closed | Dispatch schema and validator now support/enforce native stage receipt fields. | Dispatch Spec | SWU-RCNS-006 |
| B-RCNS-006 | closed | Bootstrap default staged installs do not generate `.codex/commands`; deprecated command generation remains behind explicit legacy flags. | Runtime package generator | SWU-RCNS-007 |
| B-RCNS-007 | deferred | Live installed packages under user Codex home may need refresh after source changes. | User + Task Session | approve live refresh after staged proof |

## Recommended Next Route

All source-level SWUs in this plan have been executed through the local Task Session route. Remaining work is limited to refreshing a non-blocked live Refine example that produces native receipts and optionally refreshing live installed packages under `$CODEX_HOME` after explicit approval and backup.
