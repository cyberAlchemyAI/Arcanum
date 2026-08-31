# Invoke Plan Mode

## Identity

- Spell: `invoke`
- Mode: `plan`
- Status: implemented (L2 contract, work-pack hierarchy evidence pending)

## Purpose

Plan mode converts approved design outputs into a governed work-pack and implementation-layering artifact without executing implementation work.

Plan mode makes implementation layering a first-class planning boundary: every plan has one global implementation-layering artifact, and the work-pack must map waves, tasks, and SWUs back to those layer decisions before execution handoff.

Plan mode is non-mutating. It does not edit source code, update upstream design artifacts, promote glossary entries, or perform task execution. Corrections to upstream artifacts become patch requests, blocker decisions, or explicit gap-ledger entries.

Plan mode must also prevent vague execution handoffs. For medium and high complexity plans, task decomposition is not sufficient when tasks only say to "implement this bundle" or name an outcome. Each execution task must carry enough implementation detail for the next worker to understand the intended algorithm, data flow, interface behavior, edge cases, and validation evidence without reopening product/design discovery.

For medium and high complexity work-packs, plan mode must decompose execution tasks into Smallest Working Units (SWUs). SWUs sit below tasks and above source edits: each SWU is the smallest executable implementation step that can be assigned, given a write scope, accepted with evidence, and verified with a command or reviewable check.

Plan mode also owns the execution contract for those SWUs. If later execution uses subagents, `invoke plan` must have already defined the one-SWU handoff: explicit write scope, dependencies, done criteria, validation, source context, and expected result shape.

Plan mode should make future Task Session runs context-builder-ready. It should include source anchors, validation surfaces, write scope, and handoff notes, but it must not pre-generate task context packs. Context packs and runtime handoff packs are generated at execution time as session evidence.

Plan mode also makes Task Session closeout executable before implementation
begins. Every mutation-capable SWU must declare the terminal source receipt
contract, exact synchronization target inventory, baseline binding, admitted
delta classes, lifecycle-owner validation, expected owner receipt, and
deterministic successor policy. Task Session must be able to preflight this
contract without inferring targets after code mutation.

Plan mode also performs automatic Distill validation before mutation-capable handoff. The validation checks whether the draft implementation plan, layering artifact, work-pack, and handoff route identify the smallest coherent executable unit, preserve recomposition into the approved design, expose hidden gaps, and avoid overbuilt or vague task/SWU structure.

For newly authored Work Packs, Plan mode also emits one execution-entry
projection. The default admission timing is
`selected-unit-at-task-session`: expected future material is
`selection-ready`, not an Invoke Refresh defect. The projection includes a
canonical digest of exact allowed internal routes. A direct request to run or
finish the Work Pack is later bound to this projection by Implementation
Readiness; it does not create a second per-route approval step.

Every newly authored or refreshed mutation-capable Work Pack is also an
`execution-candidate`. Before Plan may report a pass-ready handoff, Invoke
must run the exact final WPRA config and report through Implementation
Readiness `plan-readiness-preflight` and persist
`IMPLEMENTATION-READINESS-PREFLIGHT.json`. The proof covers the complete
ordered frontier, one exact Task Session route and typed validation-contract
digest per unit, and a real in-memory `proceed/TASK_READY` guard result for the
first unfinished unit. The persisted receipt contains only bound digests and
is explicitly non-reusable for execution. Conceptual, research-only, and
other non-executing plans must instead declare `executionDesignation:
non-executing` with a reason; they do not receive an execution receipt or Task
Session route.

## Implementation Coverage

- The L2 plan contract is implemented as a mode-level governance contract.
- The authoritative executable planning baseline is `WORK-PACK.md` plus the standalone `IMPLEMENTATION-LAYERING.md` companion.
- Low complexity plans may remain single-file when the scope stays inside the low-complexity threshold.
- Medium and high complexity plans require split work-pack handoff, execution-pack handoff, and layer-mapped waves.
- Medium and high complexity plans require implementation-detail specs for execution tasks, with algorithm details where the task contains domain logic, ranking, scoring, classification, policy evaluation, state transition, optimization, parsing, reconciliation, or data transformation.
- Medium and high complexity plans require SWU decomposition for non-exempt execution tasks.
- Runtime execution, registry release, `full`, and `validate` remain gated by validation evidence and explicit approval.

## Activation Gate

Normal plan mode requires:

- approved and stable design outputs,
- source design references,
- explicit delivery boundary,
- implementation objective,
- implementation-layering artifact or approval to create it,
- work-pack artifact or approval to create it,
- validation strategy,
- lifecycle owner approval for L2 plan work,
- template/profile selection evidence.

Plan mode blocks when approved design references are missing, required standalone companions are unavailable without recorded deferral, or unresolved blocker gates affect acceptance criteria.

## Required Sigils

| Sigil | Role In Mode | Required Mode |
| --- | --- | --- |
| `context-builder` | Build bounded planning context from approved design outputs, source design refs, constraints, and existing companion artifacts. | lean or standard |
| `structured-interview-kits` | Clarify missing planning inputs one question at a time and capture approvals. | gap-check or equivalent one-question interview mode |
| `inventory` | Resolve work-pack, implementation-layering, and execution-pack templates and record selection evidence. | lookup, ingest, validate |
| `dispatch-spec` | Select the planning technique trace and validate a dispatch document when the route crosses capabilities, delegation, subagents, or protected boundaries. | technique trace or dispatch validation |
| `distill` | Validate the draft plan against smallest coherent unit, SWU, recomposition, hidden-gap, and deferred-complexity expectations. | validate |
| `work-pack-readiness-audit` | Audit the exact final Work Pack frontier and emit the immutable plan-semantic report and selection handoff consumed by readiness proof. | audit v2, selected-unit-at-task-session |
| `implementation-readiness` | Compile the exact final WPRA evidence and prove Task Session contract compatibility without granting execution admission. | plan-readiness-preflight |

## Optional Sigils

| Sigil | Use When | Notes |
| --- | --- | --- |
| `decision-gate` | A blocker-level planning decision cannot be resolved from available evidence. | Route only consequential unresolved choices. |
| `task-session` | Approved work-pack is ready for bounded execution outside invoke. | Invoke emits handoff context only. |
| `spellcraft` | Planned work targets spell authoring or spell revision. | Invoke emits handoff context; Spellcraft owns spell lifecycle mutation, validation, install/adaptation, observation, and reflection. |
| `sigil-development` | Planned work targets sigil authoring or sigil revision. | Invoke emits handoff context; Sigil Development owns sigil lifecycle mutation, validation, observability, reflection, and promotion readiness. |

## Inputs

- approved design artifact path,
- source design refs,
- glossary consistency report,
- design decision and gap ledger,
- delivery boundary,
- implementation objective,
- implementation constraints and dependencies,
- existing implementation-layering seed or artifact,
- work-pack artifact path or creation approval,
- validation strategy requirements,
- implementation detail requirements for algorithmic or domain-logic tasks,
- SWU requirements for medium/high work-packs,
- Task Session closeout synchronization contract for every mutation-capable
  SWU,
- admission timing (`selected-unit-at-task-session` by default for new plans,
  or `full-frontier` with a named reason),
- execution policy with exact allowed capability/mode/target/write/effect/input/
  receipt tuples and automatic/stop decision classes,
- execution designation (`execution-candidate` for mutation-capable Work Packs,
  or `non-executing` with an exact reason),
- target artifact type (`spell`, `sigil`, or neutral),
- Dispatch Spec technique trace requirements,
- Distill validation target and gap ownership rules,
- optional execution-pack requirement.

## Template And Profile Selection

| Selection | Use When | Required Output |
| --- | --- | --- |
| standalone `implementation-layering` companion | Any `plan`, `full`, or `validate` flow is active. | global L0-L3 layer decision artifact. |
| standalone `work-pack` companion | Any `plan` or `full` flow is active. | canonical executable plan with objective, delivery slices, tasks, SWUs, gates, validation, current state, and single-file or split output mode. |
| `domainspec-spec` execution-pack | Medium/high complexity requires wave planning. | execution-pack handoff with wave and parallelization boundaries. |

## Dispatch Technique Trace Policy

Every plan output must include a Dispatch Spec technique trace. The trace is not a decorative list; each selected technique must map to a planning phase, output artifact, gate, evidence check, or unresolved gap.

Default plan trace:

- `sequence`: approved design refs feed plan artifacts and handoff.
- `scu_swu_reduction`: the plan selects the smallest coherent unit or SWU boundary before execution routing.
- `recomposition_proof`: the selected unit or SWU must recompose into the approved design and delivery boundary.
- `validation_loop`: every delivery slice and SWU has validation evidence.
- `owner_boundary_check`: Invoke authors the plan, while Task Session, Spellcraft, or Sigil Development owns downstream lifecycle work.
- `handle_handoff`: handoffs use artifact paths and handles instead of copying source context into another owner.
- `residue_ledger`: unresolved blockers and non-blocking gaps remain visible.
- `execution_receipt_handoff`: mutation-capable next routes state expected receipts before execution begins.

Create and validate a full dispatch document when the plan route has parallel subagent strategy, multiple lifecycle owners, protected context, external evidence, reusable route intent, or cross-capability delegation beyond a straightforward Task Session handoff. Missing technique trace blocks plan pass; unused technique citations flag.

## Automatic Distill Validation

Before returning a pass or flag plan, run Distill in validate mode over:

- the implementation objective,
- approved design refs and delivery boundary,
- implementation-layering artifact,
- implementation plan artifact,
- work-pack and SWU manifest,
- execution-pack or handoff route when present,
- unresolved blocker/gap ledger.

Distill validation must inspect:

- smallest coherent unit or SWU boundary,
- SWU atomicity: one primary behavior, one independently reviewable acceptance boundary, and no bundled responsive, projection, interaction, or region changes that can pass separately,
- split analysis for every medium/high SWU, including candidate child units and the reason the retained boundary is still the smallest coherent executable unit,
- first-unit narrowness: the selected first SWU is the smallest reversible trust-building step, not a task-shaped bundle,
- recomposition proof into the approved design,
- hidden acceptance-critical gaps,
- overbuilt abstractions or premature future scale,
- vague task descriptions and weak implementation-detail specs,
- missing navigation from plan to first executable unit.

Verdict handling:

- `pass`: plan may route to the next owner if all other gates pass.
- `flag`: plan may route only with named Distill gaps, owners, and repair paths in the gap ledger.
- `block`: plan cannot route to mutation-capable work until the SCU/SWU boundary, recomposition proof, acceptance-critical gap, or navigation failure is repaired.

## Planning Artifact Boundary Policy

Detailed boundary contract: [PLAN-ARTIFACT-BOUNDARIES.md](PLAN-ARTIFACT-BOUNDARIES.md).

- `IMPLEMENTATION-LAYERING.md` owns L0-L3 decision boundaries, promotion evidence, and deferrals.
- `WORK-PACK.md` owns the canonical executable plan and current execution state: objective, slices, tasks, SWUs, validation strategy, blockers, gate status, output mode, active layer window, task board, and links to split execution files.
- `work-pack/tasks/TASK-*.md` owns one task's executable contract: task objective, dependencies, SWUs, write scope, done criteria, validation, subagent handoff, and synchronization notes.
- `work-pack/waves/W*.md` owns execution ordering, layer mapping, wave gates, dependency order, and parallelization boundaries.
- `EXECUTION-PACK.md` owns cross-task choreography for medium/high complexity, but not the source-of-truth SWU definitions.

Split task files must be useful. If they only repeat task titles while the work-pack carries all execution detail, the work-pack is not execution-ready.

Work-pack tables must be navigable. Task-board task IDs should link to task contracts when task files exist, and SWU manifest rows should link to the parent task contract plus source contract or local context needed to execute the SWU.

Work-packs must carry a Task Session closeout synchronization contract for every
mutation-capable SWU. The contract binds exact owner targets and receipts; it is
not deferred implementation detail.

## Work-Pack Execution Entry Policy

Every new mutation-capable Work Pack must declare:

- `admissionTiming`, defaulting to `selected-unit-at-task-session`;
- a finite frontier and exact `allowedRoutes` projection;
- a canonical `allowedRoutesDigest`;
- automatic decisions limited to internal tool/owner routing, declared
  reversible fallbacks, one typed same-route retry, and fresh Task Session
  resumption;
- stop decisions for semantic choice, scope expansion, protected effects, and
  failed acceptance-critical validation;
- exactly one entry state: `selection-ready`, `owner-prerequisite`,
  `task-ready`, or `blocked`;
- a next owner consistent with that state.

Before Plan reports a pass-ready handoff, its machine-readable
`arcanum.work-pack-execution-entry/v1` projection must pass the installed
Implementation Readiness validator:

```text
python3 <implementation-readiness-package>/scripts/validate_work_pack_execution_entry.py --projection <EXECUTION-ENTRY.json>
```

The route effect vocabulary is closed. Work-Pack-bound implementation and
closeout routes use `repository-local-reversible`; destructive, external,
authority, promotion, publication, and deployment effects remain stop
decisions. `closeout-only` is not an effect class. Express that restriction
through the Invoke Refresh mode, exact closeout target and write scope,
Closeout Contract, expected owner receipt, and derived authorization boundary.
An unknown effect or automatic-decision token, stale route digest, unsafe path,
unknown frontier reference, or contradictory entry state blocks Plan handoff.

`selection-ready` routes to `implementation-readiness:execute`. It must not
route to Task Session while selection or another prerequisite remains. A real
semantic-plan change routes to `invoke:refresh`; expected missing material does
not. Work-Pack-bound internal routes require no additional `--authorize-route`
flag, while ad hoc routes keep their existing exact authorization behavior.
When a Work Pack declares `declared-retry`, the only retryable owner result is
`REPAIRABLE_OWNER_CONDITION`; it retries the unchanged route once, consumes the
normal step budget, preserves replay history, and does not request another
authorization.

An `owner-prerequisite` entry must preserve which execution boundary owns the
return. A generic outer-loop owner join that occurs before Task Session exists
may reclassify the entry and then start one fresh Task Session. In contrast, a
declared `PreExecutionOwnerPrerequisite` is instantiated for an already
resolved Task Session attempt. Its Router handoff uses
`source_phase=pre-execution-prerequisite`, returns the bound control handle to
that same attempt, and resumes exactly once at
`resume_point=task-session:context-build`; it never starts a second Task
Session. The plan must bind the typed prerequisite record and its exact
authorization-evidence selector rather than treating the execution entry or a
bare Work-Pack declaration as apply authority.

## Plan Implementation Readiness Producer

### Canonical Plan Execution Source

An execution-candidate Plan must author exactly one
`invoke.plan-execution-source.v1` machine source. Models populate this source;
they do not author a separate WPRA configuration or human Work Pack view.

The installed `scripts/compile_plan_execution_source.py` producer must validate
the source schema and its embedded canonical WPRA v2 contract, enforce exact
frontier/route/write/budget/effect equality, emit the WPRA configuration without
semantic invention, and derive `WORK-PACK.md` from the same validated bytes.
Plan handoff remains blocked unless two deterministic no-effect WPRA rehearsals
over that emitted configuration both pass with one equal projection digest.
Post-produce validators are declarations at this boundary and must not be
executed or required to exist before their producing SWU runs.

For `execution-candidate`, Invoke Plan must persist the exact final WPRA audit
config, then run one producer command:

```text
python3 <invoke-package>/scripts/prepare_plan_implementation_readiness.py \
  --audit-config <audit-config.json> \
  --audit-output-dir <new-readiness-run>/audit-output \
  --proof-invocation-id <invoke-plan-run-id> \
  --proof-created-at <iso-timestamp> \
  --output <IMPLEMENTATION-READINESS-PREFLIGHT.json>
```

The command first runs the installed Work Pack Readiness Audit against those
exact bytes and preserves its nonzero status. Only a passing audit is then
delegated to Implementation Readiness; Invoke reimplements neither owner's
semantics. A passing receipt must prove:

- one exact Task Session route for every unit in the ordered finite frontier;
- nonempty typed validation contracts for every unit, bound by canonical
  digest rather than rendered shell prose;
- exact Work Pack semantic, policy, route, WPRA config, and WPRA report
  digests;
- the real fast-entry guard returned `proceed/TASK_READY` with zero mutation
  for the first unfinished unit;
- `reusable_for_execution: false`, `mutation_ready: false`, and
  `authority_effect: none`.

The proof is acceptance-critical compatibility evidence, not the eventual
FastExecutionEntryReceipt. After final plan generation, one exact owner
acceptance must bind the candidate artifact inventory. When execution is
later requested, Implementation Readiness must derive a fresh direct-intent
selection binding and Task Session receipt from the current bytes. A semantic
change, route change, frontier change, validation-contract change, or byte
drift invalidates the Plan proof.

`non-executing` is allowed only when the plan has no mutation-capable Work Pack
and records why execution does not apply. It cannot expose Task Session as the
next route. `blocked` or incomplete execution plans cannot use the exemption.

## Implementation Detail Policy

- Low complexity plans may keep implementation detail inline with each task when the task is self-evident and locally bounded.
- Medium and high complexity plans must include an implementation-detail spec for every execution task.
- A task description is insufficient when it only names a bundle, layer, component, or outcome without explaining how the work should be implemented.
- Algorithmic or domain-logic tasks must include:
  - purpose and decision owned by the task,
  - inputs and outputs,
  - data model or state touched,
  - step-by-step algorithm or pseudocode,
  - ordering, precedence, scoring, classification, transition, or reconciliation rules,
  - edge cases and failure modes,
  - acceptance checks and validation evidence.
- If required implementation details are unavailable and affect acceptance criteria, plan mode blocks or routes through `decision-gate`.
- If details are useful but not acceptance-critical, plan mode may flag and carry a named detail gap into the work-pack blocker/gap ledger.

## Smallest Working Unit Policy

- Low complexity plans may omit SWUs when each task is already a smallest executable step.
- Medium and high complexity plans must include a shared SWU manifest and task-local SWU lists.
- SWU IDs use `SWU-{FEATURE-CODE}-{NNN}` when a feature code is known; otherwise use a stable local code derived from the work-pack name.
- Each SWU maps to exactly one parent task.
- Each SWU owns exactly one primary behavior or decision and has one independently reviewable acceptance boundary. Shared files do not make otherwise independent behaviors atomic.
- Each medium/high SWU must record a split analysis: name plausible child units, then explain why splitting further would break executability, acceptance closure, or semantic coherence. If plausible child units can pass independently, split the SWU.
- A SWU is task-shaped and must block when it bundles independently verifiable concerns such as semantic structure, responsive layout, state projection, interaction behavior, or multiple workspace regions under one goal.
- The first selected SWU must be the narrowest reversible trust-building step. It must not combine baseline structure with later responsive, projection, or interaction work merely to preserve task order.
- Each SWU must include goal, dependencies, write scope, done criteria, acceptance evidence, and verification command or reviewable check.
- Each SWU must include an execution-owner recommendation: `subagent`, `local-fallback`, or `manual`.
- Each SWU must include a handoff note with the exact context needed by a worker or subagent.
- Each SWU intended for Task Session or runtime-goal handoff must include enough source anchors for Context Builder to produce a strict Markdown plus JSON/index handoff pack at execution time.
- Each non-exempt execution task must list its SWUs in a `Smallest Working Units` section.
- Closure-only tasks may use a `Smallest Working Unit Exemption` only when the task ID includes `VERIFY`, `AUDIT`, `SIGNAL`, or `READINESS`.
- Medium/high implementation handoff should target one SWU at a time. If a task has multiple SWUs and no SWU is selected, the execution route must ask for a specific SWU before mutation-capable work starts.
- Unknown SWU IDs, duplicate SWU IDs, missing acceptance evidence, missing verification commands, or invalid exemptions block execution handoff.

## SWU Subagent Handoff Policy

When a task is composed of SWUs, the SWU is the preferred execution boundary for later `goal`, `task-session`, or runtime subagent work.

Invoke plan must make every non-exempt SWU assignable by providing:

- one parent task,
- one objective,
- one primary behavior or decision,
- one independently reviewable acceptance boundary,
- split analysis with candidate child units and retained-boundary rationale,
- explicit dependencies,
- explicit write scope,
- done criteria,
- validation command or reviewable check,
- source contract links,
- source anchors for Context Builder selection,
- related-context hints for architecture, feature, or prior-decision context that should be considered before runtime exploration,
- acceptance evidence required before task/work-pack synchronization,
- known blockers/gaps affecting the SWU,
- expected execution owner,
- expected result shape.

The expected subagent result shape is:

```yaml
swu_id: <id>
result: pass | flag | block | interrupted
capability_ref: <native capability handle or owner id>
receipt_kind: native-stage | subagent | local-fallback | blocked
receipt_artifact: <path or none>
files_touched:
  - <path>
validation:
  - <command or review check and result>
blockers:
  - <blocker or none>
residue:
  - <unresolved evidence or none>
reroute: <next owner or none>
handoff_note: <what the parent coordinator needs next>
```

If subagents are unavailable at runtime, this same SWU contract is used by `task-session` or a labeled local fallback. Plan mode does not execute the SWU; it makes the SWU executable.

## Layering Policy

- Every plan must include a global implementation-layering artifact defining L0, L1, L2, and L3 decision boundaries.
- Low complexity plans keep layer mapping compact inside the single-file work-pack.
- Medium and high complexity plans must include explicit waves that map to layers.
- The composability path is work-pack -> waves -> tasks -> SWUs.
- The L0 slice defines the smallest proof and decision unlocked.
- The L1 slice defines repeatability or hardening work.
- The L2 slice defines governance, reliability, validation, or degraded-mode work.
- The L3 slice defines packaging, scale, release, or rollout work.
- Each layer-mapped wave maps tasks, dependencies, validation evidence, blockers, and promotion criteria.
- Each wave must name the layer question it answers and the promotion evidence it creates.
- Each medium/high layer-mapped wave must link its tasks to implementation-detail specs.
- Each medium/high layer-mapped wave must map to one or more SWUs or an allowed closure-only exemption.
- Layer promotion must cite evidence from the previous layer; preference alone is not sufficient promotion evidence.

## Complexity Policy

Low complexity requires all of the following:

- five or fewer tasks,
- two or fewer output artifacts,
- no cross-repository changes,
- no runtime or durable-state migration,
- no unresolved blocker gates.

Any scope exceeding one or more low-complexity limits is medium or high complexity and uses split work-pack output. High complexity is flagged when medium-complexity work also has cross-team ownership, irreversible migration risk, or multiple unresolved gate dependencies.

## Execution Phases

| Phase | Sigil | Input | Output | Gate | Failure Policy |
| --- | --- | --- | --- | --- | --- |
| 1 | `context-builder` | approved design outputs, source design refs, constraints, companion state | bounded planning context | mandatory planning inputs are identified | block on missing approved design refs or contradictory delivery boundary |
| 2 | `structured-interview-kits` | bounded planning context | approved planning intent and missing-input decisions | one-question cadence and explicit approvals captured | block on unresolved blocker ambiguity |
| 3 | `inventory` | approved planning intent and local template inventory | work-pack, layering, and execution-pack selection record | eligibility evidence is explicit and tie cases request user choice | flag when candidate template is usable but not promoted |
| 4 | `dispatch-spec` | approved planning intent and route shape | technique trace or dispatch validation result | selected techniques affect phases, gates, evidence, or gaps | block on missing trace; flag on unused technique citations |
| 5 | `invoke plan` | approved planning intent, template record, and technique trace | work-pack, global layering artifact, blocker ledger, validation strategy, plan transport report | required companions, complexity policy, and layer mapping are satisfied | block on violated governance rule; otherwise return partial with unresolved gaps |
| 6 | `distill` | draft implementation plan, layering artifact, work-pack, SWU manifest, handoff route, gap ledger | Distill validation verdict, recomposition proof status, and gap recommendations | selected unit closes and recomposes, hidden gaps are owned, navigation is clear | block on failed SCU/SWU closure, recomposition, acceptance-critical gap, or navigation failure |
| 7 | `work-pack-readiness-audit` for execution candidates | exact final Work Pack, routes, typed unit contracts, and audit config | immutable v2 audit report, semantic manifest, and selection handoff | plan-semantic verdict is pass over the exact final frontier | block and preserve the audit exit status; route genuine repair evidence to Invoke Refresh |
| 8 | `implementation-readiness` for execution candidates | exact final WPRA config/report and Invoke Plan run identity | `IMPLEMENTATION-READINESS-PREFLIGHT.json` | full route/validation coverage and real proof-only `TASK_READY` guard result | block execution-candidate handoff; do not reinterpret the proof as acceptance or mutation admission |
| 9 | optional `decision-gate` | unresolved planning blocker | decision record and next route | blocker resolved or explicitly deferred | keep blocker in gap ledger with recommended next action |
| 10 | optional handoff (`task-session`, `spellcraft`, `sigil-development`, or `full`) | approved plan outputs plus readiness proof when execution-designated | execution or lifecycle-authoring handoff context | target route is explicit and accepted | defer handoff if target authority is unavailable |

## Mode Gates

- WPRA proves executable contract completeness, not future output correctness.
  A declared create target may be absent when its parent boundary, collision
  policy, producer, output contract, validation phase, failure behavior, and
  closeout destination are explicit.
- Validation commands must be classified as `pre-execution`, `post-produce`,
  or `closeout`. Invoke must not require a declared post-produce output or
  validator to exist before its producing SWU runs.
- Implementation Readiness owns selected-unit inputs, baselines, runner
  identity, authority and admission. Task Session owns materialization and
  post-produce validation; closeout owns exact-write and terminal/continuity
  evidence.

- Plan blocks without approved design outputs and source design refs.
- Template/profile selection must include eligibility evidence and explicit user choice on tie cases.
- Dispatch Spec technique trace is required; any cited technique must affect a phase, output artifact, gate, evidence check, or unresolved gap.
- Implementation-layering and work-pack companions are required.
- Work-pack output mode must follow the complexity policy.
- Low complexity plans must include compact layer mapping in the single-file work-pack.
- Medium/high complexity plans must include explicit waves that map to L0-L3 layer decisions.
- Medium/high complexity plans must include implementation-detail specs for execution tasks.
- Medium/high complexity plans must include SWU decomposition for non-exempt execution tasks.
- Medium/high SWUs must pass atomicity, independent-acceptance, and split-analysis checks; task-shaped SWUs block mutation-capable handoff.
- The first selected SWU must pass the narrow-first-unit gate.
- Algorithmic or domain-logic tasks must include algorithm steps or pseudocode, inputs, outputs, edge cases, failure modes, and validation evidence.
- Medium/high complexity plans must include execution-pack handoff or a recorded blocker.
- Validation strategy is required for every delivery slice.
- Automatic Distill validation is required before mutation-capable handoff; pass, flag, or block verdict must be recorded.
- A Distill flag must add named gaps, owners, and repair paths; a Distill block prevents `task-session`, runtime-goal, or other mutation-capable next routes.
- SWUs must each include one parent task, write scope, acceptance evidence, and verification command or reviewable check.
- SWUs must each include dependencies, done criteria, execution-owner recommendation, and subagent/local fallback handoff context.
- Mutation-capable SWUs must each include a complete Task Session closeout
  synchronization contract. Missing target inventory, baseline binding,
  admitted delta classes, owner validation, expected owner receipt, or
  deterministic successor policy blocks handoff before source mutation.
- The machine-readable execution-entry projection must pass the installed
  Implementation Readiness authoring validator; prose, template resemblance,
  or a later readiness failure is not substitute evidence.
- Every mutation-capable Work Pack must declare `execution-candidate` and
  produce a schema-valid `PLAN_IMPLEMENTATION_READY` receipt from the actual
  final WPRA bytes. Missing, stale, incomplete-route, or non-`TASK_READY`
  proof blocks Plan handoff.
- `non-executing` requires a concrete reason, no mutation-capable Work Pack,
  and no Task Session next route. It is not an exemption for incomplete or
  blocked implementation planning.
- SWUs must include source context links, and parent task references should link to task contracts when split task files exist.
- SWUs intended for runtime-goal handoff must include source anchors, validation surface, write scope, and handoff notes; Invoke must not pre-generate context packs during planning.
- Split task files must contain useful task-local SWU execution contracts, not just task titles.
- Task descriptions that only say to implement a bundle, layer, component, or outcome must block or flag until converted into implementation-detail specs.
- Any blocker that affects acceptance criteria keeps phase status at `block`.
- Candidate templates, glossary terms, registry entries, and Necronomicon concepts are never promoted automatically.
- Plan-stage transport appends stage reports and complements matching Necronomicon sections only when they already exist.
- Plan mode must not execute tasks, mutate source code, or silently edit upstream define/design artifacts.
- Spell and sigil lifecycle work routes to `spellcraft` or `sigil-development`; plan only prepares handoff context.
- If a plan output targets a spell or sigil lifecycle, the next route must name the lifecycle owner and stop before pretending Invoke completed that lifecycle.

## Handoff Artifacts

- planning context summary,
- source design refs,
- Dispatch Spec technique trace and dispatch validation path when a full dispatch document is required,
- global implementation-layering artifact path,
- work-pack artifact path and output mode,
- Distill validation verdict, recomposition proof status, and gap summary,
- execution-pack handoff path or blocker,
- compact layer mapping or layer-mapped waves,
- implementation-detail specs for medium/high execution tasks,
- SWU manifest and task-local SWU lists for medium/high work-packs,
- subagent/local fallback handoff contract for each non-exempt SWU,
- Task Session closeout synchronization contract coverage,
- validation strategy,
- dependency plan,
- blocker and unresolved gap ledger entries,
- plan transport report,
- execution designation and implementation-readiness preflight receipt or an
  exact non-executing reason,
- recommended next route (`task-session`, `full`, `spellcraft`, `sigil-development`, or deferred follow-up).

## Observability

When `.arcanum/observability/` exists, record:

- spell name and mode,
- phases attempted,
- sigils invoked,
- selected templates,
- complexity and output mode,
- selected Dispatch Spec techniques and full dispatch validation status,
- Distill validation verdict and gap count,
- Distill child run ID and telemetry append status,
- layer coverage status,
- layer-mapped wave status for medium/high complexity,
- implementation-detail coverage status,
- SWU coverage status,
- SWU atomicity status and task-shaped SWU count,
- first-unit narrowness status,
- Task Session closeout synchronization coverage,
- gates passed, flagged, or blocked,
- artifact-redundancy gaps,
- navigation-efficiency gaps,
- artifact paths produced,
- transport status,
- unresolved gaps and blocker decisions,
- next route recommendation.

## Mode Output Contract

Return:

```markdown
## Outcome Brief

<Two to five plain-language sentences explaining what Plan tried to make
executable, what it prepared or why it stopped, and why that matters.>

- Objective: <what Plan was trying to accomplish>
- Result: <what is now planned, flagged, or blocked>
- Why it matters: <practical consequence for the operator or next owner>

## Boundary and Next Decision

- Changed: <planning artifacts, evidence, or state changed>
- Unchanged: <implementation, authority, promotion, publication, deployment, or other explicit boundaries>
- Open questions: <remaining uncertainty or none>
- User decision: <exact decision needed or none>
- Next action: <next bounded action and owner>

## Technical Details

## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass | flag | block
- Mode contract: spells/invoke/plan.md
- Outputs: <implementation-layering path>, <work-pack path>, <plan transport report path>
- Design views: <coverage summary | n/a>
- Glossary consistency: <pass | flag | block | n/a>
- Dispatch techniques: <ids selected, validation status, full dispatch path | n/a>
- Distill validation: <pass | flag | block, recomposition status, gap count>
- Distill telemetry: <recorded child run id | failed with residue | not configured>
- Implementation layering: <artifact path and layer coverage summary>
- Work-pack: <artifact path and single-file | split>
- Complexity: low | medium | high
- Per-layer planning: compact | layer-mapped waves | blocked
- Implementation detail: inline | task specs complete | detail gaps recorded | blocked
- Smallest working units: n/a | complete | gaps recorded | blocked
- SWU atomicity: n/a | pass | flag | block, task-shaped count <n>
- First-unit narrowness: n/a | pass | flag | block
- Task Session closeout sync: pass | block
- Execution designation: execution-candidate | non-executing
- Implementation readiness: <PLAN_IMPLEMENTATION_READY receipt path | n/a with reason | block>
- Exact acceptance: required after final candidate hashing | n/a
- Template/profile selection: <selected templates and eligibility evidence>
- Validation strategy: <summary>
- Decisions: <summary>
- Unresolved gaps: <summary>
- Capability ceilings: <capability-status result path or not evaluated>
- Next route: task-session | full | spellcraft | sigil-development | deferred
```

## Evidence Capability Contract

Active plan output must carry `execution_path`, `dispatch_trace`, `work_pack`,
`implementation_layering`, `swu_manifest`, `validation_strategy`, `result`, and `next_route`
evidence. An execution-candidate must additionally carry the exact
Implementation Readiness preflight receipt. Plan Distill is required and must pass. When capability status is
requested, pass the Plan artifact receipt to
`scripts/capability_status_resolver.py`. A passing Plan artifact can set only
`artifact_authored=pass`; it cannot set `registry_released` or
`mutation_runtime_ready`. Those axes require their own current receipts. The
active-mode validator result remains a run-level handoff decision and is not a
collapsed capability label.
