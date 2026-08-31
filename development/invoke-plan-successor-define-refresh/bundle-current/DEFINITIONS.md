# Invoke Plan Successor Candidate Definitions

Status: candidate
Owner route: definitions-governance
Scope: feature:invoke-plan-successor
Authority effect: none

## Candidate Definitions

### PLAN-D5: Invoke Plan

Aliases: governed implementation plan
Status: candidate

#### Normative voice

An Invoke Plan is a governed translation of one admitted Design into ordered, bounded, and verifiable implementation work without revising that Design or executing the work.

#### Plain-language voice

The checked map from an approved design to the exact work people or agents can perform next.

#### Domain context

Invoke Plan sits after Define and Design and before Implementation Readiness or Task Session; it authors executable planning evidence but performs no implementation mutation.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/plan.md` (heading `Purpose`; sha256 `b447d50d0cb023965c85a28f468faec360d261505e73c20a8bb48b3f3f577c5c`)

### PLAN-D1: Plan authoring source

Aliases: Plan semantic source, Plan source document
Status: candidate

#### Normative voice

The Plan authoring source is the sole machine-readable source of Plan meaning: it owns the admitted Design binding, objective, decomposition, implementation details, validation obligations, residue, eligible routes, and closeout obligations.

#### Plain-language voice

The one JSON file where the Plan is actually written; everything readable is generated from it and every later result points back to it.

#### Domain context

Invoke Plan replaces scattered author-controlled Markdown and status fields with one semantic source while retaining the current plan-execution-source v1 as migration evidence.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Authoring Source`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/schemas/plan-execution-source-v1.schema.json` (json-pointer `/properties`; sha256 `c401f799453a662f4bb5a1fb18538c8fdef8265d727afa4c19c421d927cdbc2a`)
- evidence: `arcanum/spells/invoke/scripts/compile_plan_execution_source.py` (symbol `compile_source`; sha256 `d3e06c232d3ce2060b7846b9c8dabdae8955cab64b6ef4dec5ac350ee2107f82`)
- evidence: `arcanum/spells/invoke/design.md` (heading `Activation Gate`; sha256 `5651f9e5d0fe5fe66af4c1fced08ebabe8fd18f714824163f352ba9d27fe68f6`)

### PLAN-D6: Work Pack

Aliases: Plan coordinator view
Status: candidate

#### Normative voice

A Work Pack is a deterministic coordinator view of one exact Plan authoring source; it summarizes objective, decomposition, navigation, gate summary, blockers, gaps, and the next eligible boundary without owning Plan meaning or lifecycle state.

#### Plain-language voice

The readable control panel for the Plan, generated from the real source rather than becoming another place to edit it.

#### Domain context

`WORK-PACK.md` is always a generated coordinator view; simple Plans keep it compact, while larger Plans link generated wave, task, and Execution Pack views.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Work Pack`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/PLAN-ARTIFACT-BOUNDARIES.md` (heading `Artifact Boundary Summary`; sha256 `7f8aa4d74af790e9afed0501944596c2d21cdc9ae26cb18b1fe6c098a513b1a7`)

### PLAN-D7: Delivery slice

Aliases: Plan delivery slice
Status: candidate

#### Normative voice

A delivery slice is one coherent outcome that can be demonstrated or evaluated as part of an Invoke Plan's implementation objective.

#### Plain-language voice

A meaningful piece of the result we can show, separate from the order in which we build it.

#### Domain context

Delivery slices organize Work Pack outcomes while waves organize execution and SWUs define atomic work.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Delivery Slice`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/plan.md` (heading `Planning Artifact Boundary Policy`; sha256 `b447d50d0cb023965c85a28f468faec360d261505e73c20a8bb48b3f3f577c5c`)

### PLAN-D8: Implementation layer

Aliases: Plan layer
Status: candidate

#### Normative voice

An implementation layer is one L0-L3 decision boundary that names the question being resolved, required promotion evidence, and deferred concerns.

#### Plain-language voice

A checkpoint in implementation where we answer one kind of question before taking on the next kind.

#### Domain context

`IMPLEMENTATION-LAYERING.md` governs L0-L3 decisions and waves but does not own task status or SWU contracts.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Implementation Layer`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/plan.md` (heading `Layering Policy`; sha256 `b447d50d0cb023965c85a28f468faec360d261505e73c20a8bb48b3f3f577c5c`)

### PLAN-D9: Plan wave

Aliases: execution-order wave
Status: candidate

#### Normative voice

A Plan wave is an authored layer-aligned execution-order record that names included tasks and SWUs, dependencies, safe parallel work, entry conditions, and exit evidence; any wave file is a deterministic view of that record.

#### Plain-language voice

A batch of work that can proceed together after its prerequisites and before the next checkpoint.

#### Domain context

The Plan source owns wave ordering and parallelization; optional wave Markdown is generated navigation, while task and SWU records retain detailed contracts.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Wave`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/PLAN-ARTIFACT-BOUNDARIES.md` (heading `Artifact Boundary Summary`; sha256 `7f8aa4d74af790e9afed0501944596c2d21cdc9ae26cb18b1fe6c098a513b1a7`)

### PLAN-D10: Plan task

Aliases: implementation task contract
Status: candidate

#### Normative voice

A Plan task is one authored implementation responsibility with an objective, dependencies, write scope, done criteria, validation, and SWU decomposition when it is not already atomic; any task file is a deterministic view of that record.

#### Plain-language voice

One responsibility in the plan, detailed enough that its smaller work units can be assigned and checked.

#### Domain context

Split `TASK-*.md` files are generated task-local views and must contain useful detail when present; they never become a second authoring surface.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Task`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/PLAN-ARTIFACT-BOUNDARIES.md` (heading `Split Work-Pack Minimum Useful Content`; sha256 `7f8aa4d74af790e9afed0501944596c2d21cdc9ae26cb18b1fe6c098a513b1a7`)

### PLAN-D11: Smallest Working Unit

Aliases: SWU
Status: candidate

#### Normative voice

A Smallest Working Unit is the smallest independently executable and reviewable change or decision owned by exactly one Plan task.

#### Plain-language voice

The smallest piece of work that can be assigned, completed, and proved correct on its own.

#### Domain context

SWUs are the preferred handoff boundary for Goal, Task Session, subagents, or a labeled local fallback.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Smallest Working Unit`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/PLAN-ARTIFACT-BOUNDARIES.md` (heading `SWU Responsibility`; sha256 `7f8aa4d74af790e9afed0501944596c2d21cdc9ae26cb18b1fe6c098a513b1a7`)

### PLAN-D12: Implementation detail contract

Aliases: task implementation specification
Status: candidate

#### Normative voice

An implementation detail contract records the concrete algorithm, interfaces, data flow, inputs, outputs, edge cases, failures, constraints, and checks required to make a Plan task executable.

#### Plain-language voice

The practical instructions that turn a task name into work someone can implement safely.

#### Domain context

Medium and high complexity Plan tasks require useful implementation-detail specifications rather than outcome-only prose.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Implementation Detail Contract`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/plan.md` (heading `Implementation Detail Policy`; sha256 `b447d50d0cb023965c85a28f468faec360d261505e73c20a8bb48b3f3f577c5c`)

### PLAN-D13: Validation obligation

Aliases: Plan verification requirement
Status: candidate

#### Normative voice

A validation obligation is one exact command, deterministic check, or reviewable observation required to prove a Plan unit or gate.

#### Plain-language voice

The specific check and result we need before we can say a piece of the Plan worked.

#### Domain context

Plan validation distinguishes pre-execution, post-produce, and post-apply checks so a validator is never required before its producing SWU runs.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Validation Obligation`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/plan.md` (heading `Mode Gates`; sha256 `b447d50d0cb023965c85a28f468faec360d261505e73c20a8bb48b3f3f577c5c`)

### PLAN-D14: Plan gate

Aliases: Plan evidence gate
Status: candidate

#### Normative voice

A Plan gate is a typed condition that consumes named evidence before a layer, wave, task, or handoff may advance.

#### Plain-language voice

A checkpoint that opens only when the exact proof it asks for is present and valid.

#### Domain context

Plan gates control layer promotion, wave exit, Work Pack status, and execution handoff without converting confidence or prose into evidence.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Gate`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/PLAN-ARTIFACT-BOUNDARIES.md` (heading `Execution Readiness Gate`; sha256 `7f8aa4d74af790e9afed0501944596c2d21cdc9ae26cb18b1fe6c098a513b1a7`)

### PLAN-D15: Plan blocker

Aliases: blocking Plan condition
Status: candidate

#### Normative voice

A Plan blocker is a known condition that prevents a bounded Plan state, selected unit, gate, or handoff from proceeding.

#### Plain-language voice

A specific problem that must be fixed before this part of the Plan can move forward.

#### Domain context

Acceptance-critical ambiguity, missing evidence, invalid structure, dependency conflict, and unsafe execution scope are Plan blockers.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Blocker`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/plan.md` (heading `Mode Gates`; sha256 `b447d50d0cb023965c85a28f468faec360d261505e73c20a8bb48b3f3f577c5c`)

### PLAN-D16: Plan gap

Aliases: non-blocking Plan gap
Status: candidate

#### Normative voice

A Plan gap is known missing information or evidence that remains owned but does not prevent the current bounded Plan state from proceeding.

#### Plain-language voice

Something still missing that we can safely carry for now, with a named owner and a clear point where it would stop us.

#### Domain context

Distill flags and non-acceptance-critical detail omissions may become Plan gaps; unsafe or acceptance-critical omissions may not.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Gap`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/plan.md` (heading `Automatic Distill Validation`; sha256 `b447d50d0cb023965c85a28f468faec360d261505e73c20a8bb48b3f3f577c5c`)

### PLAN-D17: Execution entry

Aliases: Plan execution-entry boundary
Status: candidate

#### Normative voice

An execution entry is an authored eligibility contract for handing one task or SWU class from Invoke Plan to an execution-readiness or Task Session owner; downstream selection evidence binds the exact unit for one attempt.

#### Plain-language voice

The Plan defines which doorways into execution are allowed; a later receipt chooses the exact doorway and unit for this run.

#### Domain context

New mutation-capable Plans default to selected-unit admission at Task Session; selected unit, live baselines, and single-use admission remain external to Plan authoring.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Execution Entry`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/plan.md` (heading `Work-Pack Execution Entry Policy`; sha256 `b447d50d0cb023965c85a28f468faec360d261505e73c20a8bb48b3f3f577c5c`)

### PLAN-D18: Execution Pack

Aliases: Plan choreography view
Status: candidate

#### Normative voice

An Execution Pack is a deterministic medium/high-complexity choreography view projected from one exact Plan authoring source; it orders waves and cross-task dependencies without owning Plan or lifecycle state.

#### Plain-language voice

The coordination map for a larger Plan, showing what runs when without becoming a second set of task instructions.

#### Domain context

`EXECUTION-PACK.md` is an optional generated view for medium/high complexity; the Plan source retains normative wave, task, and SWU records.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Execution Pack`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/PLAN-ARTIFACT-BOUNDARIES.md` (heading `Artifact Boundary Summary`; sha256 `7f8aa4d74af790e9afed0501944596c2d21cdc9ae26cb18b1fe6c098a513b1a7`)

### PLAN-D2: Plan candidate bundle

Aliases: generated Plan bundle
Status: candidate

#### Normative voice

A Plan candidate bundle is the complete ordered set of files deterministically generated from one exact Plan authoring source and its bound predecessor evidence.

#### Plain-language voice

All Plan files produced together from one source, held for checking before anyone treats them as accepted.

#### Domain context

The bundle contains the Work Pack and its supporting planning, layering, trace, and producer evidence; it is not the execution of that Work Pack.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Candidate Bundle`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/PLAN-ARTIFACT-BOUNDARIES.md` (heading `Artifact Boundary Summary`; sha256 `7f8aa4d74af790e9afed0501944596c2d21cdc9ae26cb18b1fe6c098a513b1a7`)
- evidence: `arcanum/spells/invoke/plan.md` (heading `Mode Output Contract`; sha256 `b447d50d0cb023965c85a28f468faec360d261505e73c20a8bb48b3f3f577c5c`)

### PLAN-D3: Plan bundle admission

Aliases: Plan admission result
Status: candidate

#### Normative voice

Plan bundle admission is an independent point-in-time result that replays one exact Plan authoring source, compares every required bundle member, and runs the declared structural and consumer checks for that exact candidate.

#### Plain-language voice

A second checker proves that this exact generated Plan still matches its source and works with the checks that depend on it.

#### Domain context

Plan admission sits after deterministic generation and before capability status. Work Pack Readiness Audit and Implementation Readiness remain separate later proofs.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Bundle Admission`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/scripts/prepare_plan_implementation_readiness.py` (symbol `main`; sha256 `e83d0d264df0f606be993f6dfd8372af9c23cdeab7eb0c07b906ae078546893c`)
- evidence: `arcanum/spells/work-pack-readiness-audit/README.md` (heading `Purpose`; sha256 `7942d0e7d80b74bc9a400773244ad071b79fe93c54ba204ab6ab3a31f3359401`)
- evidence: `arcanum/spells/implementation-readiness/README.md` (heading `Work-Pack Execution Outer Loop`; sha256 `1556cee05fc11bcc553ba4760f4c85edfa0136927961d43bd967537d54b34bca`)

### PLAN-D4: Plan evidence state

Aliases: Plan proof state
Status: candidate

#### Normative voice

A Plan evidence state is the typed statement of the highest Plan claim established by exact current receipts, while preserving all later unproved or unauthorized states as separate fields.

#### Plain-language voice

A precise answer to what we have proved about the Plan so far, without turning 'written' into 'ready' or 'approved.'

#### Domain context

Invoke uses this state to hand a Plan successor into later readiness and execution workflows without collapsing artifact PASS into permission to mutate a product.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Evidence State`; sha256 `c289c423d20c4626e0f488f6a4597c8d0310b7ff346acb23f10a7b67df7000c1`)
- evidence: `arcanum/spells/invoke/README.md` (heading `Evidence Capability Contract`; sha256 `489c0208cec0cceb9f7af8b98debfafe7aeabd36dea395007fd4bd8df3dcdcba`)
- evidence: `arcanum/spells/invoke/scripts/capability_status_resolver.py` (symbol `resolve_capability_status`; sha256 `4bf4de651f6c747c54c9c76eddb558fa2a7635cd7d71ce1f0857a52074ad277f`)

## Semantic Applications

| Probe | Disposition | Candidate definitions | Authority bindings |
| --- | --- | --- | --- |
| probe:plan-authoring-source | new-scoped-term | PLAN-D1 | none |
| probe:plan-candidate-bundle | new-scoped-term | PLAN-D2 | none |
| probe:plan-bundle-admission | new-scoped-term | PLAN-D3 | none |
| probe:plan-evidence-state | new-scoped-term | PLAN-D4 | none |
| probe:invoke-plan | new-scoped-term | PLAN-D5 | none |
| probe:work-pack | new-scoped-term | PLAN-D6 | none |
| probe:delivery-slice | new-scoped-term | PLAN-D7 | none |
| probe:implementation-layer | new-scoped-term | PLAN-D8 | none |
| probe:plan-wave | new-scoped-term | PLAN-D9 | none |
| probe:plan-task | new-scoped-term | PLAN-D10 | none |
| probe:smallest-working-unit | new-scoped-term | PLAN-D11 | none |
| probe:implementation-detail-contract | new-scoped-term | PLAN-D12 | none |
| probe:validation-obligation | new-scoped-term | PLAN-D13 | none |
| probe:plan-gate | new-scoped-term | PLAN-D14 | none |
| probe:plan-blocker | new-scoped-term | PLAN-D15 | none |
| probe:plan-gap | new-scoped-term | PLAN-D16 | none |
| probe:execution-entry | new-scoped-term | PLAN-D17 | none |
| probe:execution-pack | new-scoped-term | PLAN-D18 | none |
