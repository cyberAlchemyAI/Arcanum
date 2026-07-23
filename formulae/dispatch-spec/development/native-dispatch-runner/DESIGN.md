# Native Dispatch Runner — Design

Status: proposed

Machine sources: [native-dispatch-runner.contract.json](native-dispatch-runner.contract.json), [ARCHITECTURE.json](ARCHITECTURE.json)

## 1. Context View

```text
operator
   |
   | orchestrate execute dispatch.json
   v
Orchestrate native driver
   |              ^
   | actions      | action receipts
   v              |
deterministic coordinator ----> run evidence
   |
   | validate
   v
Dispatch Spec validator
```

The runner exists inside Orchestrate. Dispatch Spec supplies a validated route but never performs work. Capability owners receive bounded tasks and return receipts; they do not control the parent gate.

## 2. Container View

| Container | Responsibility | Input | Output |
| --- | --- | --- | --- |
| Validator adapter | Run canonical Dispatch Spec validation. | source dispatch | validation receipt |
| Action compiler | Find eligible roles and emit the next exact action set. | valid dispatch + state | action files |
| Native host driver | Perform emitted host-native operations. | action file | host action receipt |
| State reducer | Bind receipts and calculate gate/next state. | state + receipts | next state + gate decision |
| Evidence writer | Persist causal evidence. | transitions and host outcomes | JSON/JSONL run artifacts |
| Bootstrap generator | Project canonical Orchestrate source into installed skill surfaces. | `runtime/orchestrate/` | generated packages |

## 3. Component View

The coordinator is a deterministic state machine. It knows dispatch dependencies and receipt requirements, but cannot invent work results or call host-native APIs. The native driver is deliberately thin: it asks the coordinator for permitted actions, performs them, writes immediate receipts, and returns control to the reducer.

```text
prepare
  -> validate
  -> authorize
  -> compile actions
  -> perform native actions
  -> join receipts
  -> reduce gate
  -> next wave OR block
  -> validate closeout
```

Permitted actions are `spawn`, `wait`, `join`, `close`, `block`, and `complete`. An action identifies its dispatch, run, wave, step, role, capability, target, mode, write scope, and expected receipt.

## 4. Runtime Sequence View

### Failure withholding

```text
execute -> validate pass -> authorization pass -> spawn wave 0
        -> join non-pass receipt -> gate block
        -> record zero eligible dependent actions -> close blocked
```

### Successful progression

```text
execute -> validate pass -> authorization pass -> spawn wave 0
        -> join passing receipts -> gate pass
        -> compile dependent action -> spawn exactly once
        -> join pass -> closeout validation -> complete
```

An event must be appended before or with each host action attempt. A final script cannot synthesize an event stream and call it causal evidence.

## 5. Data and Evidence View

Each run owns an isolated namespace:

```text
runs/<dispatch-id>/<run-id>/
  source.dispatch.json
  validation.json
  run-plan.json
  state.json
  actions/
  events.jsonl
  receipts/
  gate-decisions/
  closeout.dispatch.json
  result.json
```

The coordinator validates identifiers and declared scopes when accepting receipts. A receipt from the wrong agent, role, step, wave, capability, target, or run is non-pass evidence. Historical runs are immutable; corrections use a separate adjudication artifact.

## 6. Deployment and Generation View

Canonical runtime source belongs in `runtime/orchestrate/`. `tools/bootstrap_arcanum.sh` must install or render that source into supported host surfaces. The current hardcoded Orchestrate skill body is a drift risk and is replaced as part of this work pack.

The first causal integration target is the current native Codex host because it exposes the required subagent operations. Other host packages may receive the contract and deterministic coordinator, but no host receives a parity claim without its own integration canary.

## Authority and Interface Contracts

| Boundary | Producer | Consumer | Contract | Violation |
| --- | --- | --- | --- | --- |
| route validation | Dispatch Spec | coordinator | validation receipt | block |
| action compilation | coordinator | native driver | exact action file | block |
| native execution | native driver | reducer | host-bound action receipt | block |
| delegated work | capability owner | reducer | task receipt | block dependents |
| gate decision | reducer | coordinator | gate decision | block on ambiguity |
| generation | canonical source | bootstrap | drift-checkable installed surface | fail validation |
| lifecycle | human/capability owner | runtime | explicit decision outside execution result | never infer promotion |

## Decisions

1. Keep validator and executor authority separate.
2. Use a deterministic coordinator/native-driver split because host operations are not portable shell APIs.
3. Make failure withholding a pre-spawn gate property, not only a final status.
4. Require live causal events and immutable historical evidence.
5. Prove one host before designing cross-host parity.

## Rejected Alternatives

| Alternative | Reason rejected |
| --- | --- |
| Make Dispatch Spec spawn agents. | Collapses route validation and runtime authority. |
| Use only prose in the Orchestrate skill. | Repeats the current gap: a parent may or may not perform the route. |
| Put all logic in a shell script. | The shell does not own host-native subagent calls. |
| Manually spawn agents and finalize receipts. | Does not prove dispatch-to-spawn causality. |
| Implement all hosts at once. | Expands proof surface before the core path is stable. |

## Risks and Controls

| Risk | Control |
| --- | --- |
| Driver performs an uncompiled action. | Require action identifier and pre-action event. |
| Failed receipt arrives after dependent spawn. | Reducer opens a wave only after all required receipts pass. |
| Missing native API silently falls back. | Block; nested model-backed CLI is prohibited. |
| Generated skill drifts from source. | Bootstrap generation and deterministic drift check. |
| Canary proof is synthesized after execution. | Single public entry point plus ordered live events and host identifiers. |
| Partial spawn leaves agents alive. | Join/interrupt known agents, record residue, block the run. |

## Relationship to Existing Runtime Work

`ORCHESTRATION-RUNTIME-ARCHITECTURE.md` and `ORCHESTRATION-RUNTIME-PLAN.md` remain broad migration context. This package is canonical for the narrower missing executor slice. Completion here does not complete the repo-wide legacy CLI migration.
