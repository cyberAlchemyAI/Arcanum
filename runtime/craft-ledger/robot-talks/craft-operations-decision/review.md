# Robot-Talks — Craft Operations Decision

Status: investigation complete; proposal accepted by the operator and recorded in the scoped discovery and Craft ledger.

Dispatch: `2026-08-31-craft-operations-robot-talks`
Question: Which Craft operations beyond `add_gap` are necessary for a useful and coherent ledger runtime without representing partial support as complete coverage?

## Scope definition

The investigation compared four layers:

1. the canonical Craft method contract;
2. observed repository-local ledger practice;
3. lifecycle states and invariants modeled by the schemas;
4. the intended boundary of `runtime/craft-ledger`.

The review challenged the assumptions that the declared method list is exactly the required runtime inventory, that every row family needs one operation, that `add_gap` mechanics generalize without family adapters, that read and projection belong to the mutation protocol, that missing lifecycle transitions can safely remain manual, and that implementing every declared method is preferable to delivering a smaller complete lifecycle.

No implementation, schema authoring, Craft decision closure, or technology selection was in scope.

## Coverage

| investigator | concern | principal evidence checked | result |
| --- | --- | --- | --- |
| Beer, Stafford | canonical contract and operation fidelity | `arcana/craft/SKILL.md`, `README.md`, `ARCHITECTURE.md`, schemas, examples, runtime discovery and ledger | The 16 declared methods are a mixed operating contract, not a mutation-runtime inventory. |
| Turing, Alan | observed usage and mutation sequences | all three repository-local Craft spaces, human views, examples, session evidence | Actual updates are coordinated manual bundles; source, indexes, statuses, and views already drift. |
| Rittel, Horst | lifecycle completeness | context, typed-item, gap, decision, artifact, relation, definition, description, and recomposition lifecycles | Several modeled states are unreachable through declared methods; CRUD parity is not required, but explicit transitions are. |
| Ashby, W. Ross | runtime boundary and minimal coherent slice | canonical boundaries, mutation discovery, Define v1, schema/index contracts | Shared `inspect`/`plan`/`apply` belongs to authoritative mutations only; `add_gap` proves the kernel but does not complete a useful lifecycle. |

The parent rechecked the load-bearing locators before synthesis.

## Normalized investigator reports

### Canonical contract

#### Key findings

- Craft declares 16 methods: `start_project`, `state`, `describe`, `add_blocker`, `refine_blocker`, `add_enabler`, `next`, `open_decision`, `decide`, `add_gap`, `add_definition`, `open_child_context`, `link`, `validate`, `recompose`, and `export_ledger` ([architecture](../../../../arcana/craft/ARCHITECTURE.md#current-operation-flow)).
- The list mixes initialization, read, mutation, validation, recomposition, and projection. The canonical package does not expose those methods as a CLI or library; it depends on disciplined file editing ([architecture](../../../../arcana/craft/ARCHITECTURE.md#explicitly-absent-today)).
- Runtime phases `inspect`, `plan`, `apply`, and outcome classification are control mechanics around a selected semantic mutation, not additional Craft row-family operations ([discovery](../../docs/features/ledger-mutation/discovery.md#52-fluxo-de-execução)).
- Method inputs and persisted rows diverge. Examples include `context_id → scope_id`, `owner_route → owner`, and `meaning → statement`; each supported mutation therefore needs a governed mapping rather than generic serialization ([discovery](../../docs/features/ledger-mutation/discovery.md#33-divergências-de-interface)).

#### Gaps and inconsistencies

- `open_decision` omits `selected`, `rationale`, and `status`, although the current row schema requires them.
- `link` omits required persisted relation fields such as `status` and `reason`.
- `recompose` omits required persisted `residue` and `status`.
- Examples contain handoff and receipt rows while their route-exchange schema remains deferred.

#### Local tension

The canonical semantic inventory is already known, but `DEC-LEDGER-MUTATION-OPERATION-INVENTORY` is worded as if the inventory itself were unknown. The actual decision is which subset the mutation runtime will support, plus which missing lifecycle transitions must first become canonical.

#### Synthesis question

Should “Craft operation inventory” name the canonical method contract, while “runtime-supported mutation subset” names admitted executable coverage?

### Observed usage

#### Key findings

- Three Craft spaces were found: root, `spells/goal`, and `runtime/craft-ledger`. The runtime space remains untracked working state; history is therefore a weak operation-level witness.
- Observed additive updates are bundles: add rows, update `by_id` and current-state indexes, change context next moves, register artifacts, and update `CRAFT.md`.
- Observed consolidation updates change context, artifact, typed-item, decision, and gap states together. Snapshots often contain only the final state, so they cannot prove that separate declared operations occurred.
- Recursive contexts, relations, handoffs, receipts, and recomposition appear mainly in synthetic examples. Their low observed frequency does not prove they are unnecessary.

#### Gaps and inconsistencies

- `spells/goal/.craft/ledger.yml` lists `BLK-GOAL-SUBMODULE-001` in `active_blockers` while the row says `status: closed` ([index](../../../../spells/goal/.craft/ledger.yml#L30), [row](../../../../spells/goal/.craft/ledger.yml#L158)).
- Its human view renders that blocker as active and a promotion gate as closed, while the authoritative ledger says blocker closed and gate active ([view](../../../../spells/goal/CRAFT.md#blockers--gates), [ledger](../../../../spells/goal/.craft/ledger.yml#L158)).
- No sampled space has `.craft/index.json`; only embedded indexes are operationally observed.
- The goal ledger is `0.2.0`, while the other two are `0.3.0`, limiting uniform lifecycle conclusions.

#### Local tension

Craft assigns semantic judgment to a model or human but also makes that actor manually preserve YAML syntax, references, lifecycle rules, embedded indexes, and a non-authoritative view. The existing drift is evidence that the combined burden is already too large.

#### Synthesis question

Is the atomic mutation unit only the authoritative row plus embedded indexes, or should context state, artifact registration, trace memory, and the human view be part of the same semantic operation?

### Lifecycle completeness

#### Key findings

- Contexts have stages and gates, but no method explicitly advances or closes them. Examples show closed contexts without a declared transition operation.
- Blockers model raw, typed, refined, resolution-proposed, resolved, waived, and rejected behavior, while declared methods stop at `refine_blocker`. Gates have no creation method.
- Gaps support `active`, `planned`, `resolved`, `waived`, and `superseded`, but `add_gap` only creates `active`; there is no declared transition operation ([schema](../../../../arcana/craft/templates/schemas/ledger-core.schema.yml#L126), [method](../../../../arcana/craft/SKILL.md#L229)).
- Descriptions, definitions, relations, decisions, artifacts, enablers, and recomposition also expose modeled statuses without complete declared transitions.
- Index refresh is a required effect of meaningful mutation, not an optional user-facing CRUD command.

#### Gaps and inconsistencies

Lifecycle evidence supports explicit capabilities for context transition, gap transition, typed-item transition, artifact registration/status, description succession, definition progression, relation transition, decision supersession, and recomposition outcome handling. It does not support delete, arbitrary edit, rollback, reopen, or generic CRUD parity.

#### Local tension

The canonical method contract promises lifecycle governance but exposes mostly creation methods. Current examples reach terminal states through hidden manual edits, while the proposed runtime is supposed to reject policy invention.

#### Synthesis question

Are non-initial enum values intended to be reachable through Craft-owned operations, or merely imported states written by external/manual owners?

### Runtime boundary

#### Key findings

- `runtime/craft-ledger` should own authoritative mutations. Read/status, standalone validation, human-view export, orchestration, and external capability execution remain separate surfaces even when they reuse internal components.
- `inspect`/`plan`/`apply` can share resolution, revision binding, candidate construction, whole-ledger validation, index derivation, no-op detection, plan identity, and compare-and-commit. Semantic payloads and mappings remain operation-specific ([discovery](../../docs/features/ledger-mutation/discovery.md#52-fluxo-de-execução), [family validation](../../docs/features/ledger-mutation/discovery.md#55-validação-por-família)).
- Embedded indexes are derived in meaning but reside inside authoritative `ledger.yml`; they must be validated and published atomically with source rows. `CRAFT.md` and `.craft/index.json` remain post-commit projections.
- `add_gap` is a valid transaction-kernel fixture but an incomplete user lifecycle because the runtime cannot progress or close the gap it creates.
- If only existing canonical methods may be added next, `open_decision` + `decide` is the smallest complete family. If contract evolution is allowed, gap transition/closure must precede claims of a useful gap runtime.

#### Gaps and inconsistencies

- Define v1 accepts a caller-supplied gap `status`, while the canonical `add_gap` method promises an active row. The v1 contract must either fix `status=active` or redefine the semantic operation.
- `start_project` is a special bootstrap kernel because there is no existing ledger to inspect.
- Migration is a separate special operation, not an ordinary row mutation.

#### Local tension

Reuse favors one universal mutation engine; semantic fidelity forbids one universal payload. A kernel may be generic, but admitted operations remain explicitly versioned adapters.

#### Synthesis question

Is the next milestone only a transaction-kernel proof, or must it be a minimally useful domain lifecycle?

## Cross-layer tensions

| tension | layer A | layer B | severity | consequence |
| --- | --- | --- | --- | --- |
| Mixed method list versus mutation boundary | Craft lists 16 methods in one operating flow. | Runtime control applies only to authoritative mutations; read, validation, projection, and orchestration have different authority and effects. | MAJOR | Copying all 16 into one mutation protocol would overclaim coverage and distort responsibilities. |
| Modeled lifecycle versus reachable operations | Schemas define terminal and intermediate states for contexts, gaps, typed items, artifacts, definitions, relations, and decisions. | Declared methods mostly create rows and omit the transitions needed to reach those states. | MAJOR | A runtime faithful only to existing method names would preserve hidden manual edits and could not complete its own lifecycles. |
| Semantic method versus persisted row | Public methods use smaller or differently named inputs. | Persisted rows require additional fields and status semantics. | MAJOR | A generic serializer must invent values or fail; each operation needs an admitted adapter and defaults. |
| Atomic source/index contract versus manual practice | Rows and embedded indexes must appear together in authoritative `ledger.yml`. | Current editing is manual and sampled ledgers already contain stale indexes and views. | MAJOR | Incorrect pending state and misleading human status can survive ordinary updates. |
| Kernel proof versus user usefulness | `add_gap` exercises request, candidate, index, plan, and apply mechanics. | It can only create an active gap and cannot progress or close it. | MAJOR | Calling the first slice a generally useful runtime would be an evidence overclaim. |
| Observed frequency versus lifecycle obligation | Current ledgers mostly show additive rows and final consolidated states. | Examples and schemas contain recursive and transition-heavy lifecycles not frequently observed. | MINOR | Frequency can order implementation but cannot decide semantic necessity by itself. |
| Local recording versus external ownership | Craft records artifact and receipt references. | External capabilities retain their native artifacts, verdicts, and execution authority. | MAJOR | A broad runtime could accidentally absorb orchestration or external authority. |

## Findings

| # | artifact and locator | evidence | severity | consequence | proposed fix |
| --- | --- | --- | --- | --- | --- |
| F1 | `runtime/craft-ledger/docs/features/ledger-mutation/discovery.md`, open question 2 | The discovery names examples but leaves the supported inventory open. | MAJOR | Design cannot distinguish kernel proof, first useful lifecycle, and eventual coverage. | Add an explicit classified and phased runtime-supported operation inventory without defining payload fields yet. |
| F2 | `arcana/craft/SKILL.md`, core methods versus ledger lifecycle enums | Gap, context, typed-item, artifact, definition, relation, and decision transitions are not fully exposed. | MAJOR | Runtime fidelity to the current method list still requires manual policy invention. | Open canonical Craft maintenance work for evidence-backed lifecycle operations; do not silently create them only inside the runtime. |
| F3 | Define v1 `add_gap` semantics | Caller payload contains `status`, but canonical `add_gap` promises an active row. | MAJOR | The same named operation can mean create-active or arbitrary gap transition. | Fix the first operation to `status=active`; handle later state changes through a separate admitted transition operation. |
| F4 | `spells/goal` ledger and view | Active-index and human-view state contradict source rows. | MAJOR | Current manual mutation already produces incorrect operational summaries. | Make embedded-index derivation part of candidate validation/commit and keep view rendering post-commit and explicitly fallible. |
| F5 | `DEC-LEDGER-MUTATION-OPERATION-INVENTORY` | Its question conflates the canonical inventory with runtime-supported coverage. | MINOR | Decision closure may argue about the wrong denominator. | Rename or interpret it as “runtime-supported mutation subset and phases.” |

## Operation decision proposal

### Boundary decision

The mutation protocol should accept only authoritative semantic mutations. Shared runtime control remains:

```text
inspect -> plan -> apply -> outcome
```

Keep these outside the mutation-operation discriminator:

- `state` and repository-wide status: read surface;
- standalone `validate`: readiness/diagnostic surface;
- `export_ledger`, `CRAFT.md`, and optional `.craft/index.json`: projection surface;
- route execution and external capability calls: orchestration/external owners.

Embedded ledger indexes are not separate semantic operations; they are mandatory atomic effects derived for every mutation.

### Recommended supported slices

#### S0 — transaction kernel already defined

- `add_gap`, constrained to creating `status: active`.

Claim ceiling: proves deterministic mutation mechanics, not a useful complete gap lifecycle.

#### S1 — first minimally useful lifecycle

Support next:

1. `transition_gap` — new canonical capability name is provisional; it must govern legal movement to `planned`, `resolved`, `waived`, or `superseded` with evidence and index effects.
2. `next` — updates the context's single current next move and exercises deterministic field replacement rather than append-only creation.
3. `open_decision` — creates an active question with explicit pending semantics.
4. `decide` — closes the question with selection, rationale, and evidence.

This set lets the runtime record residue, progress or close it, preserve the next action, and obtain an explicit human/governance choice when closure depends on one. It also exercises three distinct mutation shapes: row addition, row transition, and existing-row update.

#### S2 — evidence and local knowledge

- `register_artifact` — currently missing from the method contract;
- `transition_artifact` — currently missing;
- `link`;
- `describe` with explicit description succession;
- `add_definition` plus a local definition-transition capability.

#### S3 — blockers, gates, and enablers

- `add_blocker`;
- `refine_blocker`;
- a typed-item transition capability for resolution proposal, resolution, waiver, rejection, and completion;
- `add_enabler`;
- `add_gate`, currently missing if gates are Craft-created state.

#### S4 — recursive context lifecycle

- `open_child_context`;
- a context stage/gate transition capability, currently missing;
- `recompose` with explicit child-closure semantics;
- `start_project` through a distinct bootstrap kernel.

#### Later or separately governed

- relation status transitions;
- decision supersession;
- migration between ledger schema versions;
- recording external receipts without assuming their native authority;
- any route-exchange rows after their deferred schema becomes admitted.

No evidence supports delete, arbitrary generic edit, rollback, reopen, or generic CRUD parity as runtime requirements.

## Artifact verdicts

| artifact | verdict | rationale |
| --- | --- | --- |
| Runtime discovery | FIX | Direction and mechanics are strong, but the operation inventory and boundary are not explicit. |
| Define v1 | KEEP WITH NARROWING | Suitable transaction kernel; clarify `add_gap` as create-active only and its claim ceiling. |
| Canonical Craft method contract | FIX IN SEPARATE MAINTENANCE | It needs evidence-backed lifecycle transitions, but this runtime investigation does not authorize canonical mutation. |
| Runtime Craft ledger decision | FIX AFTER HUMAN GATE | Reframe the open decision around the supported mutation subset and phased coverage. |

## Change requests

1. Add the classified operation boundary and phased inventory above to the discovery.
2. Narrow Define v1 `add_gap` to active-row creation.
3. Treat `transition_gap`, `next`, `open_decision`, and `decide` as the proposed S1 set.
4. Open separate canonical Craft maintenance for missing lifecycle operations rather than inventing them only in runtime adapters.
5. Preserve read, validation, projection, orchestration, and external-owner boundaries outside the mutation discriminator.
6. Update and close `DEC-LEDGER-MUTATION-OPERATION-INVENTORY` only after the human accepts or revises this phased set.

## Evidence boundary

The investigation used repository-local canonical Craft documentation, schemas, examples, the three discovered Craft spaces, the ledger-mutation discovery, Define v1, and current working-tree state. It did not use external sources. Repository history does not preserve operation receipts consistently, so observed final states cannot prove that declared operation sequences occurred. The `spells/goal` ledger is version `0.2.0` and was used as evidence of current manual practice and drift, not as proof of `0.3.0` semantics.

## Human gate

Disposition recorded on 2026-08-31:

- the runtime boundary and S0/S1 inventory are real and actionable;
- the S2-S4 ordering is accepted as deferred coverage, not current runtime support;
- missing canonical lifecycle operations require separate Craft maintenance before runtime admission;
- the operator authorized updating the scoped discovery and closing `DEC-LEDGER-MUTATION-OPERATION-INVENTORY` in the ledger.

This disposition does not by itself authorize canonical Craft changes or claim implementation of any operation.
