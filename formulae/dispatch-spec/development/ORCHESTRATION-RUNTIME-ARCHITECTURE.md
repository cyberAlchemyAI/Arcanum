# Orchestration Runtime Architecture

## Invoke Design Result

- Mode: `design`
- Spell: `invoke`
- Target artifact: `dispatch-spec` orchestration and Codex-exec surface migration strategy
- Target type: Formulae-backed architecture for orchestration sigils and spells
- Phase status: `pass`
- Mode contract: `spells/invoke/design.md`
- Source contracts:
  - `formulae/dispatch-spec/README.md`
  - `formulae/dispatch-spec/dispatch.schema.yml`
  - `formulae/dispatch-spec/TECHNIQUE-CATALOG.md`
  - `spells/observed-invocation-loop/README.md`
  - `tools/arcanum`
- Template/profile selection: lightweight Formulae architecture bundle with six required views
- Work-pack: `formulae/dispatch-spec/development/ORCHESTRATION-RUNTIME-PLAN.md`
- Surface inventory: `formulae/dispatch-spec/development/CODEX-EXEC-SURFACE-INVENTORY.md`
- Dispatch profile: `formulae/dispatch-spec/development/orchestration-runtime.dispatch.json`
- Next route: `task-session` for migration slices

## 1. Context View

The current runtime failure mode comes from treating nested `codex exec` as the execution substrate for orchestration stages. That makes Refine, Invoke, Distill, Interrogation, Task Session, Spellcraft, and Experiment Harness depend on a second model-backed CLI process from inside a model-backed run.

The migration scope is broader than orchestration. Every repository surface that invokes, configures, documents, tests, installs, observes, or preserves `codex exec`, `codex-exec`, `codex-bypass`, `CODEX_BIN`, or `tools/arcanum --exec` must be inventoried and classified. Some historical evidence can remain immutable as prior-run evidence; active runtime surfaces must either migrate to native skill/subagent execution, become deterministic wrappers, or be marked legacy explicit opt-in.

The replacement architecture is:

```text
operator request
  -> native Codex skill invocation
  -> parent orchestration sigil or spell
  -> dispatch-spec route document
  -> native subagent or local inline stage execution
  -> stage artifact plus telemetry receipt
  -> parent synthesis and observed invocation closeout
```

`dispatch-spec` remains a Formulae validator. It validates the route shape, stage owners, handoffs, gates, and observability requirements. It does not execute subagents and does not promote any sigil, spell, ontology, inventory, glossary, or runtime state.

The local runtime skill surface becomes the preferred execution substrate. `tools/arcanum` remains useful as the repository-local resolver, validator, and compatibility surface, but it should stop being the primary way to spawn model-backed Codex children.

## 2. High-Level Structure View

```text
dispatch-spec
  owns route schema, technique catalog, and validation rules

orchestration parent skill
  owns stage order, fanout, joins, retries, and final synthesis

native subagent workers
  own bounded stage work and return artifacts plus receipts

observed invocation loop
  owns telemetry append, reflection thresholds, and dedupe

tools/arcanum
  owns command resolution, deterministic validation, legacy compatibility,
  and local runtime metadata, not nested model orchestration

codex-exec surface inventory
  owns the repo-wide list of active, legacy, generated, and historical references
  that must be migrated, quarantined, or preserved as evidence
```

### Runtime Surfaces

| Surface | New responsibility | Not responsible for |
| --- | --- | --- |
| Native skill execution | Run the parent orchestration sigil or spell in the current Codex context. | Shelling out to nested `codex exec`. |
| Native subagent execution | Run bounded stages with explicit input, output, write scope, and telemetry receipt. | Owning parent synthesis or lifecycle promotion. |
| `dispatch-spec` | Validate composition shape before or during orchestration. | Choosing or executing the route. |
| `tools/arcanum` | Resolve commands, print skill prompts, validate dispatch files, run deterministic adapters, and support legacy compatibility. | Acting as the model-backed process supervisor for orchestration loops. |
| Observed Invocation Loop | Record telemetry from deterministic hooks or returned receipts. | Reconstructing missing primary outputs. |
| Surface inventory | Classify every `codex exec` reference by owner and migration action. | Treating historical run evidence as active runtime policy. |

## 3. Low-Level Components View

### Dispatch Document

Each orchestration sigil or spell should emit or reference one dispatch document when it chains multiple capabilities, fans out subagents, or needs auditable stage gates.

Required orchestration extensions are allowed through `additionalProperties` in the current schema:

```yaml
runtime:
  preferred_surface: native-skill
  model_backed_cli: legacy-only
  fallback: local-inline
subagents:
  strategy: parent-owned-fanout
  parent_owns_join: true
  child_subagents_allowed: false
telemetry_contract:
  required: true
  source_priority:
    - local-observability-package
    - subagent-returned-receipt
    - parent-blocked-gap
```

### Stage Receipt

Every subagent-backed stage must return this receipt even when `.arcanum/observability/` is unavailable:

```yaml
dispatch_id: <dispatch id>
step_id: <dispatch step id>
capability_ref: <sigil or spell id>
mode: <mode or none>
execution_surface: native-subagent | local-inline | deterministic-tool | legacy-codex-exec
status: pass | flag | block | interrupted | timeout
artifacts:
  - <path or handle>
validation:
  - check: <command or review check>
    result: pass | flag | block | not-run
telemetry:
  observer_available: true | false
  observer_result: appended | skipped | unavailable | returned-receipt
  dedupe_key: <key or none>
blockers:
  - <blocker or none>
handoff_note: <what the parent coordinator needs next>
```

If the local observability package exists, the parent or hook should append this receipt through the existing observer path. If it does not exist, the receipt remains the minimum telemetry evidence and the parent records an observability gap rather than hiding the primary result.

### Parent Manifest

The parent orchestration run owns one manifest:

```yaml
dispatch_id: <id>
parent_capability: <refine | invoke | spellcraft | task-session | experiment-harness | ...>
runtime_surface: native-skill
steps:
  - step_id: <id>
    subagent_id: <runtime id or none>
    receipt_path: <path or none>
    artifact_paths: []
    status: pass | flag | block | interrupted | timeout
join_result: pass | flag | block
observability_status: appended | partial | unavailable
```

## 4. Workflow Process View

```text
1. Parent skill resolves the target request and decides whether dispatch-spec is required.
2. Parent writes or selects a dispatch document.
3. Parent validates the dispatch document with dispatch-spec.
4. Parent starts task zero observer envelope when local observability exists.
5. Parent runs each step locally, through deterministic tools, or through native subagents.
6. Each subagent returns the required receipt and artifact handles.
7. Parent validates receipts against dispatch steps and join policy.
8. Parent appends observer telemetry when available.
9. Parent synthesizes result from artifacts and receipts.
10. Parent routes unresolved gaps to the lifecycle owner.
```

This keeps model reasoning inside the native Codex skill/subagent runtime and keeps shell tools deterministic.

## 5. Decision Flow View

| Decision | Rule |
| --- | --- |
| Is the route a single local capability? | Run the native skill directly; dispatch-spec is optional unless audit evidence is needed. |
| Does the route chain, fan out, debate, tournament, validate, or synthesize multiple stages? | Require a dispatch document. |
| Is a stage model-backed? | Prefer a native subagent with a receipt contract. |
| Is a stage deterministic? | Run the local script or validator directly and wrap its output in a receipt. |
| Is `.arcanum/observability/` present? | Append telemetry through Observed Invocation Loop. |
| Is observability missing or hook append unavailable? | Require the subagent or parent to return receipt telemetry and flag the observability gap. |
| Does a stage try to call `tools/arcanum --exec`, `codex exec`, or a nested model-backed runtime? | Block unless the stage is explicitly marked `legacy-codex-exec` and approved for migration testing. |
| Does the dispatch claim promotion authority? | Block. Promotion remains with the lifecycle owner. |

## 6. Dependency Interface View

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| Dispatch document | Parent orchestration skill | `dispatch-spec` validator and parent run | `dispatch.schema.yml` plus runtime extension fields. |
| Subagent prompt | Parent orchestration skill | Native subagent | Step objective, inputs, write scope, output artifact, receipt schema. |
| Stage artifact | Native subagent or local tool | Parent orchestration skill | Capability-owned artifact path or handle. |
| Stage receipt | Native subagent or local tool | Parent and observer | Required telemetry receipt fields. |
| Observer envelope | Hook, parent, or wrapper | `signal-observer` | Existing observed invocation envelope. |
| Parent manifest | Parent orchestration skill | Workflow Reflect, Task Session, maintainer | Dispatch id, stage statuses, artifact handles, receipt paths. |
| Surface inventory | Refine / Task Session | capability owners | Reference class, owner, action, and migration gate for every active `codex exec` surface. |
| Migration report | Task Session | `tools/arcanum` and capability owners | Remaining `codex-exec` references and replacement status. |

## Architecture Decisions

| ID | Decision | Reason |
| --- | --- | --- |
| ADR-ORCH-001 | `dispatch-spec` becomes the shared stage and subagent strategy contract for orchestration sigils and spells. | It already validates sequence, fanout, gates, observability grouping, runtime adapter boundaries, and owner guardrails. |
| ADR-ORCH-002 | The default model-backed runtime is native skill/subagent execution, not nested `codex exec`. | Nested model-backed CLI calls have proven environment-sensitive and hard to observe reliably. |
| ADR-ORCH-003 | `tools/arcanum --exec` is migrated toward deterministic dispatch support and legacy compatibility. | Shell tools are best for resolution, schema validation, receipts, and deterministic scripts. |
| ADR-ORCH-004 | Observability is always attempted, but the required minimum is a returned receipt. | This preserves evidence even when hooks, `.arcanum/observability/`, or ledger writes are unavailable. |
| ADR-ORCH-005 | Parent orchestration owns fanout joins and synthesis. | Subagents should not recursively create unbounded orchestration trees. |
| ADR-ORCH-006 | The migration scope includes all active `codex exec` surfaces, not only orchestration loops. | Installers, experiment harnesses, framework runtime docs, command prompts, and observed-run helpers can reintroduce the nested runtime failure if left out. |

## Risks

| Risk | Mitigation |
| --- | --- |
| Dispatch documents become busywork for single-stage calls. | Require dispatch-spec only for multi-stage or audit-heavy orchestration. |
| Subagents omit telemetry. | Parent prompt includes the receipt schema as a hard output contract and blocks missing receipts. |
| Hook telemetry and returned receipts duplicate events. | Use `dispatch_id`, `step_id`, and dedupe keys. |
| `tools/arcanum` still defaults to `codex-exec`. | Migrate default adapter and command docs in small task-session slices. |
| Existing benchmark smoke tests depend on old adapter behavior. | Keep legacy adapter available behind explicit opt-in until parity fixtures pass. |
| Historical generated artifacts dominate grep results. | Classify historical run evidence separately and do not rewrite it unless a cleanup task explicitly owns generated artifacts. |

## Plan-Ready Handoff

The implementation plan is in `ORCHESTRATION-RUNTIME-PLAN.md`. The first execution slice should add dispatch validation fixtures and a no-mutation runtime receipt contract before touching `tools/arcanum` defaults.
