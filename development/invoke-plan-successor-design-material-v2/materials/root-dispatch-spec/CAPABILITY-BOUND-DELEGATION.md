# Capability-Bound Delegation

Status: contract implemented and fixture-validated in Dispatch Spec 0.3.0;
host-specific causal integration proven on the installed Codex Orchestrate path.
Cross-host parity and lifecycle promotion remain unproven.

## Problem

The earlier subagent strategy could name useful roles, but it could not prove
which Arcanum capability governed each worker, when a dependent worker was
allowed to start, or where each worker could write. That was sufficient for a
recommendation and insufficient for an executable parent-owned dispatch.

## Decision

Keep Dispatch Spec as a deterministic route contract. Add an opt-in
`binding_mode: capability-bound` for routes that a parent orchestrator will
execute through native subagents.

The change is additive. Existing descriptive `subagent_strategy` documents
remain valid. Capability-bound routes carry stricter proof:

| Contract part | What it establishes in the validated route |
| --- | --- |
| Role capability, target, and mode | Which lifecycle or execution contract governs the worker |
| `agent_count` | How many runtime workers must appear in closeout |
| Inputs and outputs | Which exact receipts cross worker boundaries |
| Mutation policy and scopes | What the worker may and may not change |
| Role dependencies | Which producer receipts a consumer requires |
| Execution waves | Which roles may run together and which must wait |
| Wave join and gate | What must pass before a later wave starts |
| Lifecycle capability, target, mode, wave, and scope | Which runtime agent satisfied which declared role and mutation boundary |

## Concrete Route

The passing fixture models this workflow:

```text
operator approval
       |
       v
wave: lifecycle-updates (parallel, join all)
  +-- Sigil Development -- target: x-ray  -- writes: arcana/x-ray/
  |      returns receipts/xray-iteration.json
  |
  +-- Spellcraft -------- target: whisper -- writes: spells/whisper/
         returns receipts/whisper-iteration.json
       |
       v
gate: both workers passed, joined, and closed
       |
       v
wave: artifact-repair
  Task Session -- artifact-only
  consumes both lifecycle receipts
  writes only examples/architecture-explainer/index.html
  returns receipts/artifact-repair.json
```

The two lifecycle workers may run concurrently because their write scopes do
not overlap. The artifact worker cannot run concurrently with either producer:
it declares both roles and both receipts as dependencies.

## Runtime Boundary

Dispatch Spec validates the graph; it does not spawn agents. The generated
Orchestrate skill is the parent execution contract. It must:

1. validate the dispatch document;
2. require approved authorization;
3. spawn the declared native workers with capability, target, mode, inputs, and scopes;
4. join each wave and enforce its gate;
5. pass exact receipt artifacts into dependent roles;
6. close all workers and populate `subagent_lifecycle`.

The lifecycle skills retain authority over their own artifacts. The final
Task Session worker cannot rewrite X-Ray or Whisper lifecycle surfaces.

## Validator Evidence

- [capability-bound-artifact-repair.json](examples/capability-bound-artifact-repair.json)
  validates the complete synthetic three-worker, two-wave route and closeout shape.
- `block-capability-bound-dependency-same-wave.json` checks that a receipt consumer
  cannot share an execution wave with its producer.
- `run-capability-bound-mutation-tests.py` checks that missing dependency receipts,
  overlapping concurrent writes, missing authorization, incomplete agent
  closeout, capability mismatch, non-receipt outputs, duplicate receipt
  producers, runtime scope drift, failed or absent native receipts, unrelated
  wave gates, aliased paths, and blocked required spawns all block.
- The full fixture runner preserves compatibility with existing descriptive
  subagent strategies.

## Host Integration Evidence

The causal canary starts from the installed `orchestrate execute` entry point and
records native host identifiers at the moment each persisted action is spawned.

- [Failure-withholding result](development/runtime-integration/native-dispatch-runner-canary/failure/retry-001/result.json)
  records one native helper, a joined non-pass receipt, `gate_block`, zero emitted
  dependent actions, and zero open agents. Its full lifecycle stream passes the
  [run-evidence validator](development/runtime-integration/native-dispatch-runner-canary/failure/retry-001/run/evidence-validation-receipt.json).
- [Success-progression result](development/runtime-integration/native-dispatch-runner-canary/success/result.json)
  records a first-wave pass receipt before `gate_pass`, exactly one reducer-emitted
  dependent action, exactly one dependent native spawn, and a complete final state.
  Its full lifecycle stream passes the
  [run-evidence validator](development/runtime-integration/native-dispatch-runner-canary/success/run/evidence-validation-receipt.json).
- The [historical canary adjudication](development/runtime-integration/20260722T063407Z-native-host-canary/adjudication.json)
  preserves the earlier run as host-tool behavior evidence while withdrawing it
  as automatic dispatch-integration proof.

This evidence supports one bounded claim: the installed Codex Orchestrate path
causally enforces failure withholding and successful dependent progression for
the checked fixtures. It does not establish portable behavior on another host.

Run:

```bash
formulae/dispatch-spec/development/run-validation-fixtures.sh
```

## Deliberate Limits

- Dispatch Spec does not choose worker roles; the caller or a routing skill does.
- Dispatch Spec does not decide that lifecycle receipts are semantically good;
  each owning capability supplies its own validation.
- Dispatch Spec does not merge simultaneous edits. Concurrent write-scope
  overlap is blocked instead.
- Runtime thread limits remain parent-owned residue. A blocked spawn must be
  recorded and rerouted rather than silently treated as success.
- The causal canary proves native spawning only for the installed Codex host path;
  cross-host parity remains a separate follow-up.
- The evidence does not authorize lifecycle promotion and does not turn host
  operations into a stable portable API.
