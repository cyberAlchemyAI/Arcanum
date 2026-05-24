# Distill Review: Skill-Aware Observation Plan

## Target Context

Repository-local observability design and plan for deterministic explicit Codex skill telemetry.

## Objective And Output Artifact

- Objective: validate whether the current development plan selects the smallest coherent implementation unit and preserves the right telemetry.
- Output artifact: this review, plus targeted revisions to the design and work-pack.

## Mode And Budget

- Mode: Standard, inferred from user request.
- Proposal tracks: one role-simulated Proposer and Balancer track.
- Recursive rounds: two of two.
- Verdict: flag.

## Discovery Baseline

Inputs reviewed:

- [SKILL-AWARE-OBSERVATION-DESIGN.md](SKILL-AWARE-OBSERVATION-DESIGN.md)
- [SKILL-AWARE-OBSERVATION-WORK-PACK.md](SKILL-AWARE-OBSERVATION-WORK-PACK.md)
- [SKILL-AWARE-OBSERVATION-LAYERING.md](SKILL-AWARE-OBSERVATION-LAYERING.md)
- [../scripts/observe-invocation.sh](../scripts/observe-invocation.sh)

Assumptions:

- Explicit `$skill-name` observation is the implementation target.
- Implicit platform-level skill selection remains unavailable to hooks.
- Existing command observation behavior must not regress.

## Role Conversation Trace

### Round 1 Proposer

Claim: the smallest coherent implementation unit is the UserPromptSubmit skill route detector.

Evidence:

- The design already reuses the existing Stop hook and generic observer.
- L0 can prove value by opening a valid pending envelope for `$distill`.

### Round 1 Balancer

Objection category: output-contract gap.

The pending envelope contains `skill` and `skill_detection`, but the current `observe-invocation.sh` normalizes only standard fields. Without an observer update, final telemetry loses the reason this was a skill route.

Reconciliation: accept. Add observer preservation of optional `skill` and `skill_detection` as a first-class L1 task.

### Round 2 Proposer

Revised claim: the smallest coherent unit is still the explicit skill route, but it must include observer preservation of skill-specific metadata to close the telemetry contract.

Evidence:

- A run that opens a skill envelope but drops skill detection at append time is observable but not explainable.
- The implementation can preserve optional objects without changing command envelopes.

### Round 2 Balancer

Objection category: privacy and determinism.

The design examples show raw prompt and changed files. Raw prompt storage must be bounded, and changed files must not be inferred from assistant prose.

Reconciliation: accept. The design now states raw text must be short/safe or redacted, and `files_changed` should remain empty unless derived from deterministic tool evidence.

## Current Smallest Coherent Unit

**Explicit Skill Observation Route**

Responsibility:

- detect an explicit `$skill-name`,
- resolve `.agents/skills/<name>/SKILL.md`,
- open a skill-mode pending envelope,
- preserve skill-specific metadata through observer normalization,
- close through the existing observer pipeline.

## Optimization Point

This unit is small enough to implement safely in one task-session slice while still preserving the actual purpose: deterministic, explainable skill telemetry. A detector-only implementation is smaller but loses meaning when the observer drops the skill route data.

## Distill Layer Map

```text
Repository learning system
  -> Observability package
    -> Observed invocation envelope pipeline
      -> Explicit skill observation route
        -> Skill detector + metadata-preserving observer normalization
```

## Technique Pack Trace

| Technique | Activation Reason | Inspected State | Outcome | Readiness Effect |
| --- | --- | --- | --- | --- |
| abstraction-level guard | Plan risked mixing platform-level implicit detection with explicit token detection. | Design and work-pack route rules. | Explicit-only remains the selected layer. | pass |
| recomposition proof | Need to prove detector plus observer changes recompose into ledger/reflection loop. | `observe-invocation.sh` normalizer. | Added observer metadata preservation task. | flag -> pass after revision |
| evolution profile | Future platform skill metadata may arrive. | Deferred scope in layering. | Keep platform metadata as L3/deferred. | pass |
| boundary-object check | Telemetry examples became a schema boundary between hooks and observer. | Pending and final event examples. | Added explicit data contract and preservation rule. | pass |
| premortem | Failure would be silent loss of skill route evidence. | Current observer drops unknown optional fields. | Added `TASK-OBS-003`. | flag |

## Closure And Recomposition Proof

Closure:

- Inputs: prompt, skill folder, frontmatter, hook session metadata.
- Process: detect, resolve, open envelope, record tools, close, normalize, append.
- Outputs: central ledger row with capability, skill, skill detection, execution status, observer status, and dedupe key.

Recomposition:

- Skill route shares the same observer append authority as commands.
- `workflow-reflect` can group by `capability.id`, `capability.kind`, and `capability.mode`.
- Maintainers can audit why a run was classified as skill-native.

## Evolution Profile

Expected evolution:

- multiple skill token patterns,
- richer frontmatter,
- possible platform-native skill-use metadata,
- migration of old command adapters to skill-first usage.

Smallest extension boundary:

- preserve optional `skill` and `skill_detection` in ledger now,
- defer implicit/platform metadata until Codex exposes it structurally.

## Deferred Complexity

- full YAML parser for frontmatter,
- automatic raw prompt redaction engine,
- changed-file inference from arbitrary tool responses,
- native platform post-skill events,
- deleting `.codex/commands`.

## Tension Ledger

Resolved:

- Explicit skill route is the correct implementation unit.
- Observer preservation is required for useful telemetry.
- Raw prompt and changed-file fields must be bounded by deterministic evidence.

Unresolved:

- Existing PostToolUse hook still stores broad tool input/response metadata. A future privacy-hardening pass should review this separately.
- Current ledger has older unknown-kind rows; migration remains separate from this bridge.

## Premortem

Likely failure:

The hook opens skill envelopes and the ledger records `mode: "skill"`, but maintainers cannot tell which token or skill file triggered the run because normalization dropped `skill_detection`.

Guardrail:

Make `skill` and `skill_detection` preservation part of the first implementation wave and validate it with a ledger query.

## Frame-Expiry Note

This optimization point expires if Codex exposes structured skill invocation metadata to hooks. At that point, prompt-token detection should be replaced or augmented by platform-provided skill ids.

## Navigation Guide

Start here:

1. Implement `SWU-OBS-001`.
2. Implement `SWU-OBS-003` before treating the bridge as telemetry-complete.
3. Then run route regression checks from `TASK-OBS-004`.

Next route: task-session.

