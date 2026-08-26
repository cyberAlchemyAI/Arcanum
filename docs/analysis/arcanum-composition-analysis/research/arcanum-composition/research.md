# Research returns — Arcanum Composition

The explorer returns below are preserved verbatim in dispatch order. Stable
section identifiers are the explorer `RETURN-ID` values. These returns retain
their original evidence classes and limitations; they are collected research
inputs, not accepted findings by themselves.

## Return `contract-ownership-cartographer`

RETURN-ID: contract-ownership-cartographer
# Research receipt

- agent_id: `contract-ownership-cartographer`
- role_id: `explorer`
- dispatch_id: `2026-08-25-arcanum-composition-research`
- step_id: `s1`
- capability_ref: `research`
- capability_target: `Arcanum composition canonical contracts`
- capability_mode: `internal-contract-explore`
- wave_id: `explorers`
- write_scope: `[]`
- status: `pass`
- artifacts: `[]`
- validation: `research-initial-definitions.md` validator passed; SHA-256 `c8c98ba825a1a3443962aa8385d98db4523284099e5f3a5309011e47e7d6c26f`
- observer_status: `not-run; read-only explorer return`
- blockers: `none`
- evidence: canonical contracts and registries cited below
- limitations: contract inspection only; runtime implementations, generated surfaces, and historical execution receipts were not audited
- residue: unresolved ownership/activation gaps listed below
- reroute: `writer/synthesis wave`
- handoff_note: Use the matrix as documentary contract evidence only. It does not establish universal automation or observed integration.

## RQ-linked contract and ownership matrix

| RQ | Contract result | Owners, artifacts, inputs, outputs, activation, readiness, and write-back | Evidence status |
|---|---|---|---|
| **RQ-0 — Present composition** | Arcanum documents several bounded compositions, not one universal pipeline. Invoke authors preparation artifacts and hands them to lifecycle/execution owners; Task Session executes one bounded unit and routes decisions or closeout synchronization; Goal is an explicit Craft-backed multi-node router; Continuation Router provides one-hop inter-owner routing. | Invoke owns intent-to-artifact authoring, while Task Session owns bounded execution (`spells/invoke/README.md:112-121`). The ordinary documented chain is `invoke define/design/plan -> task-session to WORK-PACK.md` (`spells/invoke/README.md:137-141`). Goal activates only when a Craft scope has open work and the user asks to continue (`spells/goal/README.md:19-26`); it reads the frontier, routes owners, stages deltas, and promotes only after approval (`spells/goal/README.md:97-105`). Continuation Router consumes one receipt, dispatches at most one owner, and does not perform owner mutation (`arcana/continuation-router/SKILL.md:14-20`). | **Documented contract only.** |
| **RQ-1 — Scope and ownership** | The core ownership split is explicit. Craft owns durable project ledger state; Invoke owns preparation/refresh authoring; Task Session owns one bounded execution and its evidence; Decision Gate owns blocker-level decision governance and a durable decision record; Goal owns its frontier snapshot, routing loop, and staged proposals; Continuation Router owns ranking, admission, one-hop dispatch, and receipt joining. | Craft’s source of truth is `.craft/ledger.yml`; Markdown and index are derivative (`arcana/craft/SKILL.md:56-71`). Craft records local ledger state but does not rewrite native capability results (`arcana/craft/SKILL.md:312-317`). Invoke owns define/design/plan/work-pack/handoff authoring, while the target lifecycle owns the produced subject (`spells/invoke/README.md:112-121`, `spells/invoke/README.md:255-270`). Task Session’s objective is one bounded task with synchronized evidence (`arcana/task-session/SKILL.md:14-20`). Decision Gate owns decision resolution and persistence (`arcana/decision-gate/SKILL.md:14-20`, `arcana/decision-gate/SKILL.md:92-101`). Goal’s state ownership table assigns the ledger to Craft, frontier snapshot and proposal state to Goal, approval record to Decision Gate, and runtime receipts to delegated owners (`spells/goal/README.md:58-68`). Router ownership excludes selected-owner semantic work and mutation (`arcana/continuation-router/SKILL.md:169-170`). | **Documented contract only.** |
| **RQ-2 — Meanings of communication/composition** | Four operational meanings are documented: artifact handoff, dispatch-route binding, receipt joining, and owner-mediated state synchronization. None alone implies automatic activation or mutation authority. | Artifact handoff: Invoke names target owner, output paths, gaps, and recommended route (`spells/invoke/README.md:255-268`). Dispatch binding: Dispatch Spec records how one capability’s output becomes another’s input and validates explicit composition shape (`formulae/dispatch-spec/SKILL.md:21-38`). Receipt joining: Continuation Router validates a separate owner receipt and preserves the source result (`arcana/continuation-router/SKILL.md:147-160`). State synchronization: Craft may receive receipt evidence but retains local ledger ownership (`arcana/craft/SKILL.md:312-317`); Goal stages proposals and applies them through Craft only after approval (`spells/goal/README.md:82-105`). A route string itself is destination evidence, not mutation authority (`arcana/continuation-router/SKILL.md:169-170`). | **Documented contract only.** |
| **RQ-3 — Cross-capability relations** | Material relations carry typed artifacts rather than shared implicit state. | **Invoke → Task Session:** work pack, implementation plan/layering, validation and handoff context (`spells/invoke/README.md:221-239`, `spells/invoke/README.md:272-297`). **Task Session → Decision Gate:** exact context, option cards, recommendation, and decision artifact path for an unresolved consequential blocker (`arcana/task-session/SKILL.md:227-247`). **Task Session → Continuation Router → Invoke Refresh:** terminal receipt, target inventory, baselines, typed deltas, validation commands, exact closeout authorization, and separate joined owner receipt (`arcana/task-session/SKILL.md:402-435`). **Decision Gate → caller/Craft:** durable decision artifact and result; a ledger-owned item is separately recorded through Craft `decide` (`arcana/decision-gate/SKILL.md:92-101`, `arcana/craft/SKILL.md:147-149`). **Goal → delegated owner:** dispatch route and read-only Craft context; owner returns an execution receipt (`spells/goal/README.md:126-142`). **Goal → Craft:** staged delta plus framed diff and approval evidence (`spells/goal/README.md:132-155`). | **Documented contract only.** |
| **RQ-4 — Activation and coordination** | Activation is caller-, orchestrator-, or explicit-user-mediated; interfaces do not self-activate universally. | Invoke’s mode router resolves the requested mode and executes its gates (`spells/invoke/README.md:245-253`). Task Session detects blocker decisions and invokes Decision Gate before consequential continuation (`arcana/task-session/SKILL.md:227-253`). Task Session derives exact authorization for qualifying closeout bookkeeping and dispatches it through Continuation Router (`arcana/task-session/SKILL.md:414-435`). Optional continuation requires `--follow-next-route`; without it, no optional dispatch occurs (`arcana/task-session/SKILL.md:268-276`). Continuation Router dispatch requires `--dispatch`, all owner inputs, and exact authorization or a validated Work-Pack binding (`arcana/continuation-router/SKILL.md:22-28`, `arcana/continuation-router/SKILL.md:56-82`); it selects only when evidence is unambiguous and owner gates pass (`arcana/continuation-router/SKILL.md:136-153`). Goal activation requires user goal/context selection (`spells/goal/README.md:19-26`, `spells/goal/README.md:48-56`). | **Documented contract only.** |
| **RQ-5 — Task Session readiness** | Invoke artifacts can establish a governed preparation path, but Task Session does not universally require the full Invoke lifecycle. Exact live task readiness and later mutation admission remain Task Session responsibilities. | Task Session accepts either an explicit task contract or an optional Work Pack (`arcana/task-session/SKILL.md:88-113`). It must re-read the selected work pack and prove the unit exists, is unfinished and selected/next-ready, has satisfied dependencies/blockers, and declares write scope, done criteria, and validation (`arcana/task-session/SKILL.md:129-162`). Context Builder then supplies the task/SWU contract, source links, architecture/spec references, constraints, write scope, done criteria, and validation surface; missing or contradictory coverage blocks before mutation (`arcana/task-session/SKILL.md:220-225`). Invoke requires mutation-capable work packs to pass WPRA plus Implementation Readiness preflight before pass-ready handoff (`spells/invoke/README.md:318-344`). That proof remains non-reusable, non-mutation-ready, and authority-free (`spells/invoke/README.md:318-324`). Implementation Readiness says `task-ready` admits the SWU into Task Session and Context Builder, not mutation (`spells/implementation-readiness/README.md:61-70`). WPRA similarly says plan readiness is selection readiness, not runtime mutation readiness (`spells/work-pack-readiness-audit/README.md:199-215`). | **Documented contract only.** |
| **RQ-6 — Craft and Decision Gate** | A write-back convention exists, but no universal direct Craft↔Decision Gate runtime binding is documented. | Craft says that when another sigil such as Decision Gate resolves an item already owned by a ledger scope, the outcome must be recorded back through Craft `decide` (`arcana/craft/SKILL.md:135-149`). `decide` requires `decision_id`, selected option, rationale, and evidence, and writes the closed ledger decision (`arcana/craft/SKILL.md:215-227`). Decision Gate instead consumes caller/validator structural verdicts and relevant context (`arcana/decision-gate/SKILL.md:32-41`, `arcana/decision-gate/SKILL.md:51-73`) and persists its own decision record (`arcana/decision-gate/SKILL.md:92-101`). Neither contract assigns Decision Gate direct ledger mutation. The caller/coordinator responsible for invoking Craft `decide` is not named generically. | **Documented contract only.** |
| **RQ-7 — State transition and write-back** | Native results do not inherently become Craft state. Goal documents a complete approval-gated Craft write-back path; the general Task Session/Decision Gate/Invoke paths require owner-mediated synchronization and leave some generic Craft application responsibility unresolved. | Craft’s interaction boundary permits handoffs, receipts, and receipt evidence but preserves native-result ownership (`arcana/craft/SKILL.md:312-317`). Goal stages proposed deltas, obtains a Decision Gate approval record, and applies through Craft validation only after approval (`spells/goal/README.md:82-105`, `spells/goal/README.md:132-155`). Task Session requires synchronization for changed evidence, blockers, status, routes, work packs, checklists, Dispatch, registry, or declared Craft projections; qualifying automatic closeout is exactly one `invoke:refresh:apply-approved` hop through Continuation Router, and Task Session never edits owner targets directly (`arcana/task-session/SKILL.md:402-440`). Invoke Refresh defaults delegated/continuation activation to proposal-only and does not edit targets (`spells/invoke/refresh.md:100-113`); apply requires exact approval, inventory, package, validation, and a passing owner-bound receipt (`spells/invoke/refresh.md:185-213`). Refresh phase success does not itself grant durable runtime readiness (`spells/invoke/refresh.md:334-347`). | **Documented contract only.** |

## Material adjacent capabilities

- **Context Builder** owns bounded evidence selection and runtime handoff-pack construction. A runtime pack is runnable only with complete obligation coverage, write scope, and validation; persisted packs are execution evidence, not canonical planning state (`transmutations/context-builder/SKILL.md:14-19`, `transmutations/context-builder/SKILL.md:32-48`).

- **Dispatch Spec** owns route-shape validation and makes producer-output/consumer-input relationships explicit; it does not choose the capabilities or become the orchestrator (`formulae/dispatch-spec/SKILL.md:21-38`).

- **Implementation Readiness** owns Work-Pack execution binding/reduction between selection, owner prerequisites, and Task Session entry. Its `TASK_READY` evidence does not authorize mutation (`spells/implementation-readiness/README.md:47-88`).

- **Work Pack Readiness Audit** owns audit-only frontier readiness evidence. It neither selects a unit nor authorizes Task Session or Invoke Refresh (`spells/work-pack-readiness-audit/README.md:8-28`).

## Unresolved contract gaps

1. **No generic Craft write-back actor is named.** Craft requires external decision outcomes to be recorded via `decide`, but Decision Gate does not claim that call and the general caller/coordinator responsibility remains unspecified (`arcana/craft/SKILL.md:147-149`; `arcana/decision-gate/SKILL.md:92-101`).

2. **Declared Craft projection closeout is not fully reconciled with ownership.** Task Session routes qualifying closeout through Invoke Refresh, while Craft says ledger mutation remains Craft-owned. The inspected contracts do not state when Invoke Refresh may directly update `.craft/ledger.yml` versus prepare evidence for a later Craft operation (`arcana/task-session/SKILL.md:410-435`; `arcana/craft/SKILL.md:312-317`).

3. **Preparation is conditional, not universal.** Task Session accepts an explicit task without requiring every Invoke definition/design/plan artifact; the complete Invoke/WPRA/Implementation Readiness chain applies to authored mutation-capable Work Packs (`arcana/task-session/SKILL.md:88-113`; `spells/invoke/README.md:318-344`).

4. **Invoke registry presence is unresolved.** `spells/invoke/README.md` declares canonical ID `invoke` (`spells/invoke/README.md:14-24`), but the current Spell Registry table lists its installed spells without an Invoke row (`registry/SPELLS.md:7-22`). This receipt does not determine whether that is intentional, stale registry state, or a release-axis distinction.

5. **Implementation and observation are untested here.** The contracts specify routes, gates, and receipts, but this read-only explorer did not inspect runtime code or replay any execution. No relation above should be upgraded beyond documentary assertion.

## Return `runtime-witness-verifier`

RETURN-ID: runtime-witness-verifier
# Runtime witness verifier receipt

- `agent_id=runtime-witness-verifier`
- `agent_name=Peirce, Charles Sanders`
- `role_id=runtime-witness-verifier`
- `dispatch_id=2026-08-25-arcanum-composition-research`
- `step_id=s2`
- `capability_ref=research`
- `capability_target=Arcanum composition implementation and execution evidence`
- `capability_mode=internal-runtime-explore`
- `wave_id=explorers`
- `write_scope=[]`
- `status=pass`
- `artifacts=[]`
- `validation=Validated baseline read completely; SHA-256 c8c98ba825a1a3443962aa8385d98db4523284099e5f3a5309011e47e7d6c26f. Repository inspection remained read-only; no tests that write results were run.`
- `observer_status=not_run`
- `blockers=[]`
- `limitations=Runtime code, deterministic validators, stored fixtures, receipts, and historical runs were inspected. Historical and synthetic evidence is treated only as a bounded witness; absence claims are limited to the inspected current packages and named relations.`
- `reroute=s4 composition-synthesis-writer`

Evidence notation:

- **DC / documentary assertion**: current canonical owner contract.
- **IB / executable source**: deterministic implementation exists, whether or not a live owner hop was observed.
- **OE / executable observation**: stored result, receipt, or report records a completed bounded execution.

## Relation-by-relation implementation/execution matrix

| Relation | Evidence status | Caller, detection, and context assembly | Result application and mutation owner | Scope, contrary evidence, and unresolved witness gap |
| --- | --- | --- | --- | --- |
| **Invoke Plan → Task Session** | **DC + IB + bounded OE.** Invoke owns plan/work-pack authoring; Task Session owns bounded execution. The deterministic Task Session runner requires exact work-pack, SWU, controls, execution contract, owner, and closeout references. | Invoke Plan assembles design-derived implementation plans, work packs, source anchors, write scopes, validation, SWUs, and closeout contracts, but explicitly does not pre-generate execution-time context packs (`spells/invoke/plan.md:11-30`). The Plan readiness producer runs WPRA and Implementation Readiness, producing non-reusable, authority-free compatibility evidence (`spells/invoke/plan.md:257-292`). A later user/coordinator calls Task Session; its governance CLI receives `--request` and `--run-dir` (`arcana/task-session/scripts/task-session-governance-runner.py:2885-2944`). | Task Session, not Invoke, owns execution. The runner binds exact inputs into an execution ticket (`arcana/task-session/scripts/task-session-governance-runner.py:1677-1845`) and can commit admitted staged outputs (`arcana/task-session/scripts/task-session-governance-runner.py:2817-2869`). | The relation is not universal. General Task Session accepts an explicit task and lists `WORK-PACK.md` as optional (`arcana/task-session/SKILL.md:88-103`), while this deterministic runner is narrower and requires `work_pack_ref` and `swu_ref` (`arcana/task-session/schemas/governance-run-request.schema.json:7-19`). A stored Invoke run is planning-only and initially routes through Sigil Development, not directly to Task Session (`arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/INVOKE-RESULT.json:21-50`). Later work-pack receipts witness Task Session execution of specific SWUs only (`arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/WORK-PACK.md:54-101`). |
| **Task Session → Decision Gate** | **DC + partial IB + bounded OE.** | Task Session detects unresolved blocker-level choices after building context and option cards, then is contractually required to invoke Decision Gate (`arcana/task-session/SKILL.md:220-247`, `arcana/task-session/SKILL.md:249-253`). Decision Gate consumes caller/owner-supplied structural verdicts; it does not establish application-specific validity (`arcana/decision-gate/SKILL.md:51-73`). | Decision Gate owns option admissibility and the durable decision artifact, not execution or downstream mutation (`arcana/decision-gate/SKILL.md:85-101`). Its deterministic prefilter implements zero/direct/gate cardinality (`arcana/decision-gate/scripts/prefilter-options.py:70-140`); its override consumer mutates only the exact override artifact for non-protected, one-use consumption (`arcana/decision-gate/scripts/consume-override.py:117-123`, `arcana/decision-gate/scripts/consume-override.py:193-231`). | Current Task Session governance-runner phases do not call Decision Gate; the CLI exposes prepare, prerequisite resume, executor join, reconcile, commit, and status only (`arcana/task-session/scripts/task-session-governance-runner.py:2885-2946`). A historical Goal-development Task Session reports a Decision Gate PASS and a decision artifact (`spells/goal/development/spellcraft-runs/20260621T024138Z-workpack-one-shot-w0/W0-RESULT.md:1-18`, `spells/goal/development/spellcraft-runs/20260621T024138Z-workpack-one-shot-w0/W0-RESULT.md:48-58`), but it is a caller-mediated local run, not proof of a generic runner binding. |
| **Craft-backed decision → Decision Gate → Craft write-back** | **DC + bounded OE; no packaged general IB.** | Craft says an external sigil’s resolution of a ledger-owned item must be recorded back through Craft `decide` (`arcana/craft/SKILL.md:129-150`). A user/operator or lifecycle agent detects and invokes Decision Gate; Craft does not ship an automatic detector or dispatcher. | Decision Gate owns its decision record. Craft owns `.craft/ledger.yml` and the subsequent `decide` mutation (`arcana/craft/SKILL.md:67-71`, `arcana/craft/SKILL.md:215-227`). Craft records native receipts without rewriting their verdicts (`arcana/craft/SKILL.md:312-317`). | Craft explicitly has no automated command runner (`arcana/craft/SKILL.md:14-19`) and no stable CLI, row updater, or route-exchange schema (`arcana/craft/ARCHITECTURE.md:241-259`). A historical decision record says the user invoked Decision Gate after a Craft live test (`docs/decisions/craft-distill-receipt-route.md:3-17`) and records the selected option (`docs/decisions/craft-distill-receipt-route.md:150-166`). This witnesses manual coordination, not a universal Craft↔Decision Gate runtime binding. |
| **Task Session terminal result → Invoke Refresh closeout** | **DC + partial/generic IB + strong bounded OE.** | Task Session detects synchronization need from terminal deltas. It assembles source receipt, exact target inventory and baselines, allowed delta classes, validation, expected owner receipt, and unique-successor policy (`arcana/task-session/SKILL.md:402-430`). Continuation Router is the declared dispatcher; Invoke Refresh is the owner (`arcana/task-session/SKILL.md:431-440`). | Invoke owns refresh mutation of Invoke-authored workflow artifacts; Task Session must not edit those targets directly (`arcana/task-session/SKILL.md:469-471`). Refresh accepts only exact `apply-approved` material evidence and scope equality (`spells/invoke/refresh.md:185-213`). | A generic manifest-bound owner-hook launcher exists (`arcana/task-session/scripts/run-owner-hook.py:141-252`, `arcana/task-session/scripts/run-owner-hook.py:382-423`), but no current shipped Invoke adapter manifest was found, and the main runner returns `next_action: owner-hooks-not-implemented` after commit (`arcana/task-session/scripts/task-session-governance-runner.py:2870-2881`). The plan-once closeout controller is explicitly fixture-only and does not invoke Refresh or mutate canonical targets (`arcana/task-session/scripts/plan-once-material-controller.py:1-8`); it only waits for and validates a separately produced Invoke receipt (`arcana/task-session/scripts/plan-once-material-controller.py:437-472`). A historical SWU result explicitly hands off to `invoke:refresh:apply-approved` (`arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/work-pack/results/SWU-TSGR-005-RESULT.json:39-48`). Its stored material package binds four exact Invoke-owned targets (`arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/refreshes/20260730T211000Z-swu-tsgr-005-producer/task-session-apply/closeout/material-package.json:29-65`), and the owner receipt records PASS and the next Task Session route (`arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/work-pack/closeout/SWU-TSGR-005-INVOKE-OWNER-RECEIPT.json:1-38`). This is a specific historical chain, not current universal automation. |
| **Invoke Refresh → workflow artifact mutation** | **DC + validator IB + bounded OE.** | Direct-user activation defaults to `apply-approved`; delegated or continuation activation defaults to `proposal-only` (`spells/invoke/refresh.md:100-113`). The caller supplies source evidence, exact target inventory, scope, approval, package and receipt (`spells/invoke/refresh.md:21-34`, `spells/invoke/refresh.md:52-70`). | Invoke owns refresh reports and approved changes. `refresh_material_handoff.py` only resolves readiness; it returns `mutationReady` after validating receipt identity and gates (`spells/invoke/scripts/refresh_material_handoff.py:118-219`). It is not a target-file applicator. | The historical closeout handoff reports continuation activation, `apply-approved`, four exact validated paths, and `mutationReady=true` (`arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/refreshes/20260730T211000Z-swu-tsgr-005-producer/task-session-apply/closeout/refresh-material-handoff.json:1-36`). The associated owner receipt attributes the result to Invoke. The stored evidence does not establish that every Refresh activation is automatically dispatched or applied. |
| **Goal → Craft frontier read** | **DC + partial IB + fixture OE.** | The Goal contract says the user selects a Craft context; Goal then reads the current frontier (`spells/goal/README.md:19-26`, `spells/goal/README.md:82-94`). | Craft owns the ledger; Goal owns only its frontier snapshot (`spells/goal/README.md:58-68`). | Current runtime does not open or parse a Craft ledger. It merely requires caller payload fields `goal_context_id` and `source_ref`, then copies caller-supplied nodes into a snapshot (`spells/goal/runtime/goal_loop.py:68-87`). Its main writes snapshots/results to an output directory, never Craft state (`spells/goal/runtime/goal_loop.py:451-464`). Stored fixture results witness PASS/STOP/BLOCK for synthetic inputs only (`spells/goal/validation/results/fixture-report.md:1-7`). No current direct Craft frontier adapter was witnessed. |
| **Goal → Task Session node dispatch and receipt join** | **DC + route-construction IB + fixture OE only.** | Goal selects the first non-T3 caller-supplied node and constructs a dispatch route whose default owner is Task Session (`spells/goal/runtime/goal_loop.py:121-137`). | Task Session should own execution evidence; Goal should audit the returned receipt (`spells/goal/README.md:32-37`, `spells/goal/README.md:134-142`). | The fixture runtime does not invoke Task Session. `build_execution_receipt` fabricates a terminal receipt inside Goal from the constructed route (`spells/goal/runtime/goal_loop.py:235-249`), and the validation harness calls route-builder, synthetic receipt-builder, audit, and staging functions sequentially (`spells/goal/validation/run-fixtures.py:103-131`). The stored dispatch even labels its native-stage row `observer_status: not_run` (`spells/goal/validation/results/delegation_staging.dispatch.json:70-87`). Historical Task Sessions under Goal development exercised Goal’s package work, not canonical Goal-loop node dispatch. |
| **Goal → Decision Gate approval record** | **DC + token-check IB + bounded historical OE.** | Goal detects a staged batch requiring approval and is documented to send the framed diff to Decision Gate/user approval (`spells/goal/README.md:92-105`, `spells/goal/README.md:139-141`). | Decision Gate owns the approval record; Craft owns eventual ledger application. | Runtime `evaluate_approval_boundary` consumes an already supplied token and `decision_record_ref`; it does not call Decision Gate or create the record (`spells/goal/runtime/goal_loop.py:286-334`). Fixture evidence reaches only `ready-for-craft-apply`, with `direct_apply_performed=false` (`spells/goal/validation/results/approval_exact.apply-boundary.json:1-9`). A historical Goal-development decision artifact and token witness one user-mediated approval (`spells/goal/development/spellcraft-runs/20260621T024138Z-workpack-one-shot-w0/DECISION-GATE-GOAL-PUBLIC-BOUNDARY.md:15-24`), not automatic Goal→Decision Gate activation. |
| **Goal staged delta → Craft apply** | **DC + staging/token IB + one bounded OE.** | Goal constructs staged proposal state only after audit (`spells/goal/runtime/goal_loop.py:252-283`). The approval checker can emit `craft_apply_request=true` but always reports `direct_apply_performed=false` (`spells/goal/runtime/goal_loop.py:286-334`). | Declared owner is Craft after approval. | Current Goal runtime contains no Craft apply operation. Fixture report proves staged/no-stage and approval-boundary behavior only (`spells/goal/validation/results/fixture-report.md:9-21`). One historical W0 receipt records actual changes to `spells/goal/CRAFT.md` and `.craft/ledger.yml`, but attributes the applying capability to `local-fallback`, not a packaged Craft runner (`spells/goal/development/spellcraft-runs/20260621T024138Z-workpack-one-shot-w0/SWU-GOAL-002-APPLY-RECEIPT.yml:1-14`). The token scopes exactly those two files (`spells/goal/development/spellcraft-runs/20260621T024138Z-workpack-one-shot-w0/APPROVAL-TOKEN-GOAL-PUBLIC-BOUNDARY-001.json:1-11`). This witnesses a manually coordinated special case. |
| **Task Session / Decision Gate / Invoke Refresh / Goal outcome → generic Craft-backed state transition** | **DC boundary; no universal IB; specific OE only.** | The producing capability returns its native receipt. A caller or lifecycle coordinator must decide that a Craft-owned row is implicated, resolve the owning workspace, and route a Craft operation. Task Session’s closeout contract permits a declared Craft projection among exact synchronization targets (`arcana/task-session/SKILL.md:404-425`). | Craft alone owns generic ledger state. Native capabilities retain their artifact and verdict ownership (`arcana/craft/SKILL.md:312-317`). | Task Session’s generic transaction engine can write admitted target files (`arcana/task-session/scripts/task-session-governance-runner.py:2817-2869`), but that is not a Craft-semantic row-update binding and its current owner-hook continuation remains unimplemented. The observed Invoke Refresh chain updated work-pack artifacts, not Craft. The only inspected direct Craft write-back witness is the bounded Goal W0 local-fallback receipt above. |
| **Source authority when surfaces disagree** | **Documented authority rules plus evidence-class ceiling.** | The consuming analysis must resolve authority per owner and concern before inferring behavior. | Canonical owner contract governs allowed responsibility; current executable implementation governs what is actually bound; an exact receipt/result governs only the observed run it names. | Craft explicitly declares its current canonical package and says historical development material is not runtime authority (`arcana/craft/SKILL.md:33-54`); its architecture distinguishes the operating contract, schemas, examples, and derived views (`arcana/craft/ARCHITECTURE.md:39-53`). Goal declares its README the reusable spell source contract and generated runtime surfaces installer-owned (`spells/goal/README.md:173-178`). Invoke separates authored, registry-released, and mutation-runtime-ready evidence axes and forbids an earlier axis from implying a later one (`spells/invoke/README.md:60-90`). Therefore registry entries, generated mirrors, fixtures, and historical runs cannot upgrade a missing current binding into implemented universal composition. |

## RQ-3 through RQ-9 classification

| RQ | Status | Finding and evidence boundary |
| --- | --- | --- |
| **RQ-3** | answered | Material relations exist through artifact handoffs: Invoke Plan→Work Pack→Task Session; Task Session→Decision Gate; Task Session→Invoke Refresh; Craft-owned decision→Decision Gate→Craft `decide`; and Goal→frontier/owner/approval/staged-delta/Craft paths. The transferred objects are exact work-pack/SWU contracts, context and controls, decision records, terminal receipts, material packages, refresh receipts, frontier snapshots, approval tokens, and staged deltas. |
| **RQ-4** | answered | Activation is predominantly caller/coordinator-mediated. Contracts assign detection to Task Session or Goal, but current deterministic implementations often validate caller-assembled artifacts rather than invoking the next owner. The strongest current counterexamples to automaticity are Task Session’s `owner-hooks-not-implemented` status and Goal’s synthetic in-process receipt builder. |
| **RQ-5** | answered | An Invoke-authored execution-candidate becomes Task-Session-ready only after exact work-pack/SWU, route, write scope, validation, closeout, WPRA, and non-reusable readiness proof. This preparation is sufficient for that route but not universally required by all Task Session use: the general contract admits explicit tasks and optional work packs, while the current deterministic governance runner is specifically work-pack-bound. |
| **RQ-6** | answered | No universal operational Craft→Decision Gate binding was found. The documented binding is caller-mediated: detect a ledger-owned decision, invoke Decision Gate with relevant context, then record the result through Craft `decide`. Historical decision artifacts witness that pattern, not automatic direct consumption or mutation of the Craft ledger by Decision Gate. |
| **RQ-7** | answered | Native outcomes become durable Craft state only through a separately owned, scoped write-back operation. Goal documents an approval-gated Craft apply path, but current runtime stops at `craft_apply_request`. Task Session can declare a Craft projection as a closeout target, but no generic Craft-semantic adapter was witnessed. One historical Goal W0 local-fallback receipt records an exact two-file Craft mutation. |
| **RQ-8** | answered | The matrix distinguishes DC, IB, and OE. The most fully witnessed cross-owner chain is the bounded Task Session result→Invoke Refresh closeout receipt sequence. Goal’s current cross-owner behavior is mostly documented plus synthetic fixture observation. Generic Craft write-back and Task Session→Decision Gate remain contractually defined with partial tooling and caller-specific historical witnesses. |
| **RQ-9** | answered | Authority is concern-specific and evidence cannot be promoted across classes: canonical owner contract for responsibility and permitted boundary; current code/schema for implemented binding; exact receipts/results for that execution only. Registry and generated surfaces establish discoverability or parity, not execution; historical runs remain bounded witnesses. |

- `evidence=Current canonical contracts, deterministic runtime sources, schemas, stored fixture reports, owner receipts, Task Session results, Invoke run artifacts, Goal development decision records, and Craft architecture were inspected with exact citations above.`
- `residue=No current universal Craft row-update adapter; no current canonical Goal-to-Craft frontier adapter or Task Session execution join; no current Goal-to-Decision-Gate invocation; Task Session’s generic owner-hook launcher lacks a witnessed shipped Invoke adapter and is not integrated into the main runner; observed Craft write-back is historical and local-fallback-attributed.`
- `handoff_note=Use this receipt to keep documentary contract, executable binding, and bounded observed execution separate in synthesis. Do not generalize the Task Session→Invoke historical closeout chain or Goal W0 Craft mutation beyond their exact scopes.`

## Return `authority-boundary-falsifier`

# Explorer Receipt

- `agent_id`: `authority-boundary-falsifier`
- `role_id`: `authority-boundary-falsifier`
- `role`: `explorer`
- `dispatch_id`: `2026-08-25-arcanum-composition-research`
- `step_id`: `s3`
- `capability_ref`: `research`
- `capability_target`: `Arcanum composition authority and boundary claims`
- `capability_mode`: `internal-falsification`
- `wave_id`: `explorers`
- `write_scope`: `[]`
- `status`: `pass`
- `artifacts`: `[]`
- `validation`: Baseline validator passed; repository root, research root, working folder, and artifact resolved correctly. Validated baseline SHA-256: `c8c98ba825a1a3443962aa8385d98db4523284099e5f3a5309011e47e7d6c26f`. Read-only inspection covered the README, method, canonical skills/spells, registries, schemas, generated surfaces, runtime implementations, fixture reports, and bounded development evidence.
- `observer_status`: `not-emitted`; read-only explorer work produced no observability mutation.
- `blockers`: `none`
- `evidence`: Documentary contracts, executable source, fixture reports, and bounded historical receipts cited below.
- `limitations`: Repository-only inspection; no web; no files edited; no live end-to-end capability run was initiated. Negative searches are used only with positive contrary contracts, explicit “absent/deferred” declarations, or exhaustive registry/schema surfaces.
- `residue`: Full relation-by-relation runtime witnessing remains owned by `runtime-witness-verifier`; the synthesis writer should reconcile any newer concrete runtime witness against the counterclaims below.
- `reroute`: `composition-synthesis-writer`
- `handoff_note`: Preserve this ledger as adversarial dissent. Do not restate a documented handoff as direct, universal, automatic, or implemented unless a caller, activation condition, owner receipt, and current runtime witness are all cited.

## Counter-claim ledger

### 1. “Craft, Invoke, Task Session, Decision Gate, and Goal form one linear composition.”

**Verdict: rejected.**

The repository supports composition as a family of caller-specific routes, spells, graphs, and handoffs, not one universal sequence.

- The method says to choose the smallest governing route and later route the result to the correct owner; it does not prescribe one mandatory capability chain (`framework/CYBERALCHEMY-METHOD.md:69-73`, `framework/CYBERALCHEMY-METHOD.md:87-98`).
- Dispatch Spec explicitly admits sequence, fan-out, tournament, dialectic, validation loop, or synthesis graph shapes (`formulae/dispatch-spec/SKILL.md:23-25`).
- `implementation-readiness` composes Layering, Decision Gate, Continuation Router, and Task Session, with no Craft requirement (`spells/implementation-readiness/README.md:18-25`). Its simple documented phase order is Layering → Decision Gate → Task Session (`spells/implementation-readiness/README.md:38-45`).
- `goal` is a different composition around a Craft frontier and several owners (`registry/SPELLS.md:22`), while its own state table distributes state across Craft, Goal, Dispatch Spec, Decision Gate, delegated owners, and observability (`spells/goal/README.md:58-68`).
- Invoke itself offers multiple exits: sigil lifecycle, spell lifecycle, ordinary Task Session, reflection, research, or deferred refresh (`spells/invoke/README.md:123-157`).

**Survived narrow interpretation:** Arcanum supports authority-bound composition in which a spell, bridge, or orchestrator sequences capabilities while owners retain their contracts (`framework/CYBERALCHEMY-METHOD.md:234-240`). That is a composition principle, not one topology.

**Discriminating evidence still needed:** A canonical artifact declaring an exhaustive mandatory route for the named five capabilities, including entry/exit conditions and exceptions. None of the inspected governing surfaces supplies that.

### 2. “The named capabilities communicate directly.”

**Verdict: rejected as a general interpretation; weakened to artifact/receipt-mediated communication.**

Supported operational meanings are:

1. output artifact becomes another step’s input;
2. a caller passes a handoff or dispatch object;
3. a route joins a separate owner receipt;
4. multiple owners operate over named state namespaces.

Dispatch Spec requires non-first steps to name an input source such as a prior frame, handle, decision, ledger, receipt, artifact, human answer, or external context (`formulae/dispatch-spec/SKILL.md:67-74`). Its boundary schema separately represents `capability_handoff`, `evidence_return`, and `state_write`, with `from_owner` and `to_owner` fields (`formulae/dispatch-spec/dispatch.schema.yml:878-911`). State namespaces each carry their own owner and write policy (`formulae/dispatch-spec/dispatch.schema.yml:972-988`).

The repository’s own example describes Invoke → Task Session as a boundary object: Task Session consumes a handoff and returns validation evidence (`formulae/dispatch-spec/README.md:77-105`). Dispatch Spec validates that claim but does not execute it (`formulae/dispatch-spec/README.md:120`; `formulae/dispatch-spec/README.md:52-62`).

**Caller-mediated alternative:** The parent orchestrator owns spawning, joining, gating, and synthesis; Dispatch Spec only validates the route (`formulae/dispatch-spec/SKILL.md:136-143`).

**Discriminating evidence still needed:** A current runtime trace showing one named capability directly invoking another without a parent/orchestrator, route artifact, host runtime, or user gate, plus the exact API/process boundary that makes “direct” meaningful.

### 3. “Relations activate automatically whenever adjacent capability contracts mention each other.”

**Verdict: rejected.**

Most relations require a user request, caller decision, exact authorization, or scoped trigger.

- Goal activates when a user asks Codex to continue toward a goal; protected mutations stop for approval (`spells/goal/README.md:19-26`).
- Invoke routes to Task Session only when plan output is ready; Invoke emits handoff context and Task Session owns execution (`spells/invoke/README.md:103-110`).
- Task Session invokes Decision Gate only for unresolved blocker-level choices (`arcana/task-session/SKILL.md:239-253`).
- Optional Task Session continuation requires `--follow-next-route` and exact route authorization (`arcana/task-session/SKILL.md:72-73`).
- Invoke Refresh distinguishes direct-user, delegated, and continuation activation; delegated/continuation activation defaults to proposal-only, while direct-user defaults to apply-approved (`spells/invoke/refresh.md:100-113`, `spells/invoke/refresh.md:189-200`).

**Survived narrow automaticity:** Task Session’s current contract admits one narrowly bounded automatic closeout route, exactly `invoke:refresh:apply-approved`, only for declared targets and five allowed delta classes (`arcana/task-session/SKILL.md:402-430`). It still dispatches through Continuation Router, runs Invoke’s gates, joins a separate owner receipt, and forbids direct Task Session edits (`arcana/task-session/SKILL.md:431-440`).

**Authority conflict:** That narrow automatic closeout is contractual but not fully present in the current production runner; see item 7.

### 4. “The composition has one shared state owner.”

**Verdict: rejected.**

- Goal’s “Shared State” table assigns different owners to the Craft ledger, frontier snapshot, dispatch route, staged deltas, approval record, runtime receipts, and telemetry (`spells/goal/README.md:58-68`).
- Invoke separately owns authoring artifacts and handoff context, while Task Session owns bounded execution (`spells/invoke/README.md:112-121`).
- Craft owns only local ledger state and route memory; called capabilities retain their native artifact, validation, and verdict (`arcana/craft/SKILL.md:312-317`).
- The framework explicitly treats collapsing multiple lifecycle authorities into one oversized workflow as an anti-pattern (`framework/CYBERALCHEMY-METHOD.md:352-361`).

**Survived narrow interpretation:** Craft can be the source of truth for one selected project ledger (`arcana/craft/SKILL.md:67-71`), but that does not make it owner of native Decision Gate records, Task Session receipts, Invoke artifacts, Goal proposal state, or runtime telemetry.

### 5. “Decision Gate directly consumes and mutates Craft-backed ledger state.”

**Verdict: rejected as a universal binding.**

The positive contract is caller-mediated write-back:

- When another sigil such as Decision Gate resolves an item already in a Craft ledger, the outcome must be recorded back through Craft’s `decide` operation (`arcana/craft/SKILL.md:147-149`).
- Craft may prepare handoffs and receive/apply receipt evidence, while the called capability owns its native result (`arcana/craft/SKILL.md:312-317`).
- Decision Gate accepts generic plans, notes, requirements, files, constraints, and proposed options; no Craft ledger input is required (`arcana/decision-gate/SKILL.md:32-40`).
- Decision Gate persists a generic decision record and returns its artifact path (`arcana/decision-gate/SKILL.md:92-101`).
- Decision Gate consumes structural verdicts from the caller or owning validator and does not manufacture application-specific validity (`arcana/decision-gate/SKILL.md:54-60`).

Craft’s decision row and Decision Gate’s record are compatible in concept but not bound by a current shared decision-record schema. Craft requires fields such as `scope_id`, `decision_type`, `selected`, `rationale`, and `status` (`arcana/craft/templates/ledger.schema.yml:729-783`), while Decision Gate’s machine schemas cover option admissibility and overrides rather than a Craft row adapter.

**Caller-specific counterexample:** Goal uses Decision Gate for an approval record, then separately stages and later asks Craft to apply ledger changes (`spells/goal/README.md:62-67`, `spells/goal/README.md:92-105`).

**Discriminating evidence still needed:** A typed Decision-Gate-to-Craft adapter, schema mapping, current caller implementation, and observed receipt proving the exact ledger row transition.

### 6. “Task Session, Decision Gate, Invoke Refresh, or Goal outcomes automatically become Craft state.”

**Verdict: rejected universally; survived only for bounded caller-specific proposals.**

- Goal expressly stages deltas as proposals and permits active ledger apply only after approval through Craft (`spells/goal/README.md:92-105`, `spells/goal/README.md:126-140`).
- Goal’s staged-delta schema is generic and identifies source authority, target, operation, diff, validation expectation, promotion state, and creating receipt (`spells/goal/schemas/staged-delta.schema.json:7-60`); it is not itself a Craft row-update schema.
- Goal’s approval token requires only a string `decision_record_ref`, not a validated Decision Gate record or Craft decision row (`spells/goal/schemas/approval-token.schema.json:7-41`).
- Task Session forbids directly performing Invoke Refresh, Decision Gate, Goal, or another owner’s mutation (`arcana/task-session/SKILL.md:620-636`).
- Craft’s compatibility schema explicitly marks route-exchange and row-update schemas as deferred (`arcana/craft/templates/ledger.schema.yml:24-47`, `arcana/craft/templates/ledger.schema.yml:944-955`).

**Interpretation:** Current authority supports proposal, receipt, and explicit owner-apply semantics. Outcome production alone does not prove durable Craft mutation.

### 7. “The full documented composition is presently implemented and observed.”

**Verdict: rejected. Partial executable witnesses survive.**

**Goal conflict:**

- Goal’s README describes an autonomous fail-closed loop routing owners, staging deltas, and promoting after approval (`spells/goal/README.md:8-17`).
- Its current runtime calls itself a read-only skeleton, reads caller payload/fixtures, returns a non-mutating result, and never writes Craft state (`spells/goal/runtime/goal_loop.py:2-7`).
- Its frontier reader consumes nodes already present in the caller payload rather than loading a Craft ledger (`spells/goal/runtime/goal_loop.py:68-87`).
- Its main run path only reads the frontier and builds a result (`spells/goal/runtime/goal_loop.py:404-463`).
- The fixture report proves synthetic frontier, delegation/staging, approval-boundary, gap-discovery, and telemetry cases (`spells/goal/validation/results/fixture-report.md:1-36`), not a live end-to-end cross-capability loop.
- Historical closeout explicitly says generated surfaces had dry-run evidence only, publication and registry promotion were not run (`spells/goal/development/FINAL-WORKPACK-REPORT-20260621T032135Z.md:3-12`).

**Task Session conflict:**

- The canonical skill requires Continuation Router → Invoke Refresh closeout (`arcana/task-session/SKILL.md:402-440`).
- The current deterministic runner states that whole-run closeout, owner hooks, continuation, and observation are intentionally absent (`arcana/task-session/scripts/task-session-governance-runner.py:2-7`) and returns `next_action: owner-hooks-not-implemented` after commit (`arcana/task-session/scripts/task-session-governance-runner.py:2765-2778`, `arcana/task-session/scripts/task-session-governance-runner.py:2870-2882`).
- The only split precloseout controller identifies itself as fixture-only and explicitly does not invoke Refresh or canonical mutation (`arcana/task-session/scripts/plan-once-material-controller.py:2-7`).
- Bounded development evidence reports green fixture counts but names orchestration as the production gap and says the counts do not prove the runner exists (`arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/CONTEXT-PACK.md:29-40`).
- That same run ended blocked for a missing production Continuation Router readiness receipt (`arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/CONTINUATION.json:4-27`).

**Evidence ceiling:** Contract assertion and executable fixture behavior exist. A universal implemented binding or observed production composition does not follow.

### 8. “Source conflicts can be resolved by a simple README > skill > registry > runtime hierarchy.”

**Verdict: unresolved; no universal precedence rule was found.**

The promotion framework says capability behavior may be owned across `SKILL.md`, README, templates, validation files, or registry row, but does not define precedence among those surfaces (`framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md:35-42`).

Material conflicts include:

- README claims `.agents/skills/` uses symlinked canonical folders (`README.md:132-138`, `README.md:179-191`), but the checked-out Codex entries are one-line link representations. More seriously, `.agents/skills/craft:1` targets `../../development/craft`, while Craft says that older development package is historical and not the runtime contract (`arcana/craft/SKILL.md:33-53`).
- The generated Claude Task Session package declares `canonical_source: arcana/task-session/SKILL.md` but is version `0.3.1` with the old objective (`.claude/skills/task-session/SKILL.md:2-21`), while canonical Task Session is version `0.8.3` and contains materially newer routing/closeout behavior (`arcana/task-session/SKILL.md:1-15`).
- Generated Decision Gate is version `0.1.0` (`.claude/skills/decision-gate/SKILL.md:2-21`), while canonical Decision Gate is `0.4.0` (`arcana/decision-gate/SKILL.md:1-15`).
- Generated Invoke is `0.2.0` (`.claude/skills/invoke/SKILL.md:2-14`), while canonical Invoke is `0.3.1` (`spells/invoke/README.md:1-9`).
- The Spell Registry’s exhaustive current table includes Goal and Implementation Readiness but not Invoke (`registry/SPELLS.md:9-22`), despite README presenting Invoke as the lifecycle authoring spell (`README.md:148-161`).

Generated packages identify themselves as regenerable projections, so canonical sources should bound intended behavior. Runtime implementation still bounds claims of implementation and execution. The repository does not currently state how to resolve a canonical contract/runtime disagreement into a single “current behavior” verdict; the evidence class must remain explicit.

### 9. “Any incomplete cross-capability relation is necessarily an architectural defect.”

**Verdict: rejected.**

Several separations are deliberate governance boundaries:

- Invoke is an authoring front door, not the lifecycle owner (`spells/invoke/README.md:22-26`).
- Decision Gate does not execute a sole route or manufacture consent (`arcana/decision-gate/SKILL.md:61-70`).
- Craft records local state without rewriting native owner results (`arcana/craft/SKILL.md:312-317`).
- Goal is a router and does not own delegated behavior or direct protected mutation (`spells/goal/README.md:10-17`).
- Task Session attributes every mutation and receipt to its owner (`arcana/task-session/SKILL.md:469-470`).
- Dispatch Spec validates composition shape and is not an execution engine (`formulae/dispatch-spec/README.md:52-62`, `formulae/dispatch-spec/README.md:72-75`).

**Weakened defect interpretation:** Some incompleteness can materially limit a documented purpose—e.g. deferred Craft route-exchange/row-update schemas, stale generated packages, and absent Task Session owner hooks. Evidence of incompleteness alone does not determine whether the intended repair is direct integration, a typed adapter, a coordinator, narrower documentation, or preservation of the boundary.

**Discriminating evidence still needed:** For each gap, a named product obligation, owner-approved acceptance criterion, current failed end-to-end scenario, frequency/impact evidence, and a statement of whether the relation is expected to be direct, caller-mediated, optional, or intentionally absent.

### 10. “Arcanum presently supports no meaningful composition at all.”

**Verdict: rejected.**

A narrower conclusion survives falsification: Arcanum supports documented, authority-bound, artifact- and receipt-mediated compositions selected by a caller or spell. Spell contracts identify phases, shared-but-partitioned state, gates, handoffs, and owners (`README.md:140-146`). Dispatch Spec supplies a shared route object and typed boundary vocabulary (`formulae/dispatch-spec/README.md:5-17`; `formulae/dispatch-spec/dispatch.schema.yml:664-682`). Goal and Implementation Readiness are concrete but materially different compositions (`registry/SPELLS.md:15-22`).

What does **not** survive is the stronger claim that these artifacts establish one universal, linear, direct, automatic, single-owner, fully implemented and observed system.

## RQ-focused handoff

- **RQ-0:** Present support is best bounded as a plural family of authority-bound routes and spells, not one unified mandatory pipeline.
- **RQ-2:** Supported “communication” is artifact transfer, dispatch/route mediation, receipt joining, state-namespace coordination, and explicit user/caller gating; “direct capability communication” is unsupported without a narrower runtime definition.
- **RQ-6:** Craft ↔ Decision Gate is contractually caller-mediated write-back, not a proven universal direct binding.
- **RQ-7:** Durable Craft transitions require Craft-owned application; native results and staged proposals do not themselves mutate the ledger.
- **RQ-8:** Documentary contracts and fixture-level executable observations exist; full production integration and observed universal composition do not.
- **RQ-9:** Canonical sources, generated projections, registries, and runtime implementations currently conflict. Claims must retain source type and evidence class rather than silently select the preferred surface.
- **RQ-10:** Ownership separations are often deliberate. Actual improvement need remains unresolved until a documented purpose, expected relation type, and failed witness are joined.
