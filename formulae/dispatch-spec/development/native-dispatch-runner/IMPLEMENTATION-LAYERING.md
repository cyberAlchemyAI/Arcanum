# Native Dispatch Runner — Implementation Layering

Status: proposed

## Layer Strategy

The layers advance one kind of proof at a time. A later layer may not compensate for a missing earlier proof with a manually assembled result.

| Layer | Capability added | Proof earned | Explicitly not yet claimed |
| --- | --- | --- | --- |
| L0 — deterministic coordination | Validate a dispatch, compile eligible actions, reduce bound receipts, and decide gates. | Route state deterministically produces the correct next action or block. | Native subagents ran. |
| L1 — native execution | Orchestrate executes compiled actions through one host's native subagent API and records live events. | Dispatch invocation causally reaches native spawn/join. | Robust failure recovery or cross-host parity. |
| L2 — evidence and failure hardening | Handle non-pass, malformed, missing, timed-out, and partially spawned waves; validate event ordering. | Dependents are withheld and known agents are reconciled under failure. | Every host behaves identically. |
| L3 — generation and integration proof | Generate installed surfaces from canonical source and run failure-first then success canaries. | The installed public entry point satisfies both scenarios without bespoke spawning. | Repo-wide legacy runtime migration is complete. |

## First Unit

`SWU-NDR-001` compiles one valid dispatch in `prepared` state into the exact first-wave `spawn` actions. It performs no host calls and mutates only a temporary run namespace. It is the narrowest reversible unit that proves the dispatch can control what would run.

## Recomposition

```text
SWU-NDR-001 action compilation
  + SWU-NDR-002 receipt reduction
  = deterministic coordinator

deterministic coordinator
  + SWU-NDR-003..005 native driver
  = causal host execution

causal host execution
  + SWU-NDR-008..010 hardening
  + SWU-NDR-011..013 integration evidence
  = Native Dispatch Runner acceptance boundary
```

If a unit cannot reconnect to this chain through machine evidence, it does not belong in this work pack.

## Layer Gates

### L0 gate

- invalid dispatch emits no executable actions;
- valid dispatch emits only dependency-free authorized first-wave roles;
- bound passing/non-passing receipts deterministically produce gate pass/block;
- fixtures run without a model or host-native API.

### L1 gate

- `orchestrate execute` is an explicit grammar branch;
- missing native host capability or execution authorization blocks before spawn;
- each emitted `spawn` action maps to exactly one native host call;
- native results are bound to action, agent, role, step, wave, and run.

### L2 gate

- malformed, missing, timed-out, and non-pass required receipts withhold dependents;
- partial wave creation reconciles known agents and leaves a residue receipt;
- event ordering proves actions were recorded as they happened.

### L3 gate

- installed Orchestrate surfaces derive from `runtime/orchestrate/`;
- drift validation passes;
- failure canary passes before success canary is attempted;
- historical manual canary receives a separate truthful adjudication;
- Dispatch Spec validator passes the closeout document.

## Stop Conditions

Stop and return a blocker if:

- the host cannot expose native spawn/join operations to the driver;
- execution authorization semantics cannot be distinguished from lifecycle approval;
- existing schema cannot bind actions and receipts without an authority-breaking change;
- a canary needs bespoke parent spawning instructions;
- a dependent native action occurs before its gate evidence.
