---
module: concept-layer-optimizer
version: current
status: draft
updatedAt: 2026-05-20
docType: implementation-layering
---

# Implementation Layering: Concept Layer Optimizer Sigil Development

## Purpose

Plan the full sigil-development lifecycle for Concept Layer Optimizer from approved design packet to reusable, observed, registry-ready Arcana sigil.

This artifact applies Concept Layer Optimizer to its own development plan: it chooses the smallest coherent development unit, recomposes that unit upward into the full lifecycle, and uses implementation layering to prevent runtime and registry machinery from arriving before the manual sigil behavior is proven.

## Objective-Output Pair

- Objective: develop Concept Layer Optimizer into a validated reusable Arcana sigil without losing the design's recursive optimization, Proposer/Balancer, technique pack, and navigation contracts.
- Output artifact: a sigil-development plan bundle containing implementation layering, implementation plan, work-pack, task/SWU handoff, and plan transport.

## Concept Layer Optimizer Result

- Target context: Arcanum sigil-development lifecycle for `arcana/concept-layer-optimizer/`.
- Mode and budget: Standard planning pass with Concept Layer Optimizer lens and implementation layering companion.
- Proposal tracks: 1 track; Proposer selects lifecycle layers, Balancer checks premature runtime complexity and missing validation.
- Recursive rounds: 2 conceptual rounds.
- Verdict: pass.
- Current smallest coherent unit: manual executable candidate sigil package.
- Optimization point: start with `README.md` + `SKILL.md` + one representative Standard-mode example before runtime adapter or registry work.
- Concept layer map:
  - Reusable Arcana sigil lifecycle
  - Candidate package
  - Behavior examples and validation
  - Runtime adapter and observability
  - Registry and release readiness
  - Reflection and maintenance loop
- Closure and recomposition proof: the candidate package is closed because it contains user-facing usage, executable process, quality bar, anti-patterns, and output contract. It recomposes upward because examples validate behavior, runtime adapts it, registry exposes it, and reflection maintains it.
- Evolution profile: expected evolution is additional modes, refined technique triggers, runtime-specific subagent support, and telemetry-driven tuning.
- Deferred complexity: command adapter, registry promotion, and automated reflection are deferred until manual examples show pass/flag/block behavior.
- Runtime role policy: subagent-first. Use true subagents when the runtime supports them; otherwise use labeled role simulation with the same trace contract.
- Tension ledger: runtime implementation must prove the subagent-first/fallback policy preserves the same output contract; validation examples must include objective-output drift and navigable-result downgrade cases.
- Navigation guide: start at Layer 0, then promote only when exit evidence is present.
- Next route: sigil-development.

## Source Contract

- Transmutation contract: [../../../transmutations/implementation-layering/SKILL.md](../../../transmutations/implementation-layering/SKILL.md)
- Invoke plan contract: [../../../spells/invoke/plan.md](../../../spells/invoke/plan.md)
- Sigil-development lifecycle: [../../sigil-development/README.md](../../sigil-development/README.md)
- Candidate design packet:
  - [SIGIL-HANDOFF.md](SIGIL-HANDOFF.md)
  - [MODE-TECHNIQUE-SURFACE-DESIGN.md](MODE-TECHNIQUE-SURFACE-DESIGN.md)
  - [techniques/README.md](techniques/README.md)
  - [DESIGN-CONTINUATION-REVIEW.md](DESIGN-CONTINUATION-REVIEW.md)

## Target And Scope

- Target: concept-layer-optimizer
- Scope: reusable Arcana sigil package and lifecycle plan
- Current state: design packet approved; package and validation not yet authored

## Layer Boundary Rule

Each layer must answer:

```text
After this layer, we know whether <decision unlocked>.
```

## Nested Layering Rule

Top-level layers may receive their own implementation layering when the layer contains enough internal complexity that a flat task list would hide sequencing, risk, or validation boundaries.

Nested layering is justified when at least one of these is true:

- the layer contains multiple independently verifiable units,
- the layer has a deferred decision that can be unlocked progressively,
- the layer mixes design, implementation, validation, runtime, registry, or maintenance concerns,
- the layer contains a risk that needs earlier evidence before later work is worth doing,
- the layer's output must be navigable by another user or agent without relying on conversation memory.

Nested layering is not added because recursion is elegant. It stops when the next unit is directly executable as a Smallest Working Unit. Each nested layer must declare its parent layer, decision question, smallest unit, exit evidence, and stop condition.

Default recursion budget:

- L0 and L1: use nested layering by default because package behavior and validation examples are the first proof of the sigil.
- L2: use nested layering by default because runtime and observability mix implementation, policy, and telemetry decisions.
- L3 and L4: use nested layering only when a checklist would hide an approval, governance, or maintenance decision.
- Maximum default depth: top-level layer plus one nested layer. A deeper pass requires a named blocker or named evolution pressure.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 Candidate Package | After this layer, we know whether the sigil can be run manually from its own package. | `README.md` + `SKILL.md` with modes, technique pack, objective-output setup, navigation closeout, quality bar, anti-patterns, and output contract. | User-facing README, executable SKILL, tier rationale, lifecycle expectations, local links. | Examples, runtime adapter, observability hook, registry. | Human review confirms package can guide a manual Standard run. | Promote to examples when package is navigable and contract-complete. |
| L1 Behavior Validation | After this layer, we know whether the sigil behaves consistently across compact, standard, tournament, validate, and failure cases. | Validation examples with real output bodies for pass, flag, and block. | Passing examples, negative examples, technique-trigger examples, validation runbook, validation report. | Runtime adapter and registry. | Examples demonstrate objective-output drift, finite recursion, closure/recomposition, navigation check, and pass/flag/block readiness. | Promote to runtime only when examples reveal no blocker contract gaps. |
| L2 Runtime And Observability | After this layer, we know whether the sigil can be invoked through local command surfaces and observed after meaningful use. | Runtime adapter plus observability signal model. | Codex command adapter, subagent-first role policy with simulation fallback, signal schema, usage telemetry, reflection thresholds. | Registry promotion and release. | `tools/arcanum --resolve` can find adapter and representative run records observability closeout. | Promote to registry candidate work only when manual and runtime behavior agree. |
| L3 Registry Candidate | After this layer, we know whether Concept Layer Optimizer has enough evidence for a final promotion decision. | Registry candidate entry with validation evidence. | Candidate metadata, README links, install/routing check, promotion recommendation record. | Final promotion approval and wider ecosystem rollout. | Registry links validate and recommendation names promote, hold, or revise. | Route final approval to L4 readiness as the last gate. |
| L4 Reflection And Maintenance | After this layer, we know whether usage signals can improve the sigil without breaking its core contract and whether final promotion is approved. | Reflection-ready telemetry loop plus final approval record. | Usage thresholds, reflection report template or link, maintenance trigger, iteration policy, final promotion gate. | Future technique expansion. | Reflection policy can identify output drift, repeated gaps, and targeted updates; B-CLO-002 approval state is explicit. | Maintain through sigil-development observe/reflect mode. |

## Layer Micro-Layering Plan

This section applies implementation layering inside each top-level layer. It is a planning aid, not a requirement to create separate artifacts for every row. A row becomes its own task or artifact only when the work is not directly executable as an existing Smallest Working Unit.

### L0 Candidate Package Micro-Layers

| Micro-Layer | Decision Question | Smallest Unit | Exit Evidence | Stop Condition |
| --- | --- | --- | --- | --- |
| L0.1 README Surface | After this micro-layer, we know whether a user can understand when and why to use the sigil. | `README.md` with purpose, fit, inputs, modes, technique pack summary, and output contract. | Reader can identify the sigil's objective-output pair and choose Compact, Standard, Tournament, or Validate mode. | Stop when README gives enough orientation to start a manual run. |
| L0.2 SKILL Execution Contract | After this micro-layer, we know whether an agent can execute the sigil without hidden conversation context. | `SKILL.md` with trigger rules, first action, role model, recursion budget, cycle guards, and closeout format. | Agent can produce a valid first-turn confirmation and complete a Standard-mode run envelope. | Stop when the execution process is explicit enough for manual use. |
| L0.3 Balance And Complexity Contract | After this micro-layer, we know whether the package prevents premature complexity while preserving open-endedness. | Quality bar, anti-patterns, complexity exception rule, and evolution-profile prompt. | Every added abstraction must cite a named tension, concrete failure mode, or confirmed evolution pressure. | Stop when complexity decisions have a pass/flag/block rule. |
| L0.4 Navigation Closeout | After this micro-layer, we know whether future users and agents can continue from the result. | Navigable result check wired into README/SKILL output contract. | Final output includes start-here, result artifact, decisions, unresolved tensions, and next action. | Stop when closeout is usable without rereading the full session. |

### L1 Behavior Validation Micro-Layers

| Micro-Layer | Decision Question | Smallest Unit | Exit Evidence | Stop Condition |
| --- | --- | --- | --- | --- |
| L1.1 Golden Runs | After this micro-layer, we know whether normal runs produce the intended optimization artifact. | At least one Standard-mode example and one Compact-mode example. | Examples show layer extraction, smallest coherent unit, recomposition proof, and balanced complexity. | Stop when successful behavior is concrete enough to compare against. |
| L1.2 Technique Trigger Runs | After this micro-layer, we know whether techniques activate without becoming mandatory clutter. | Examples for Cynefin, TRIZ, morphological analysis, set-based design, Wardley mapping, and navigable result check where relevant. | Each technique has activation reason, contribution, and deactivation or deferral rationale. | Stop when technique behavior can be inspected independently. |
| L1.3 Drift And Failure Runs | After this micro-layer, we know whether the sigil catches bad plans. | Negative examples for objective-output drift, infinite reduction, premature abstraction, missing evolution profile, and navigation downgrade. | Validation can produce flag or block verdicts with concrete repair guidance. | Stop when failure behavior is visible, not only described. |
| L1.4 Validation Report | After this micro-layer, we know whether the package is ready for runtime work. | `VALIDATION.md` or equivalent report summarizing cases, verdicts, gaps, and promotion decision. | Report states pass/flag/block and names remaining blockers before L2. | Stop when L2 has clear entry evidence. |

### L2 Runtime And Observability Micro-Layers

| Micro-Layer | Decision Question | Smallest Unit | Exit Evidence | Stop Condition |
| --- | --- | --- | --- | --- |
| L2.1 Command Surface | After this micro-layer, we know whether local invocation can resolve the sigil. | Command adapter or routing entry for Concept Layer Optimizer. | `tools/arcanum --resolve` or equivalent route finds the sigil surface. | Stop when the command can find the package without changing behavior. |
| L2.2 Role Execution Policy | After this micro-layer, we know whether Proposer/Balancer behavior is delegated or simulated for the active runtime. | Runtime policy for subagent-first execution, simulation fallback, two-agent default, and optional tournament configuration. | Runtime uses true subagents when supported and states when it falls back to role simulation. | Stop when role behavior is honest, reproducible, and trace-equivalent across both paths. |
| L2.3 Signal Schema | After this micro-layer, we know whether useful usage signals can be collected. | Observability schema for objective-output confirmation, mode, techniques, recursion rounds, verdict, drift, and navigation result. | Representative run can emit or document expected signal fields. | Stop when telemetry supports reflection without collecting noisy trivia. |
| L2.4 Runtime Validation | After this micro-layer, we know whether runtime behavior matches manual behavior. | One representative runtime run compared to L1 golden behavior. | Runtime result preserves objective-output pair, recursion budget, technique trace, and navigation closeout. | Stop when runtime adds access without changing the sigil contract. |

### L3 Registry Candidate Micro-Layers

| Micro-Layer | Decision Question | Smallest Unit | Exit Evidence | Stop Condition |
| --- | --- | --- | --- | --- |
| L3.1 Candidate Metadata | After this micro-layer, we know whether the sigil is describable as a reusable Arcana entry. | Registry candidate entry with name, purpose, route, tier, dependencies, and validation links. | Candidate entry is complete enough for review. | Stop when metadata does not require behavior changes. |
| L3.2 Routing And Link Check | After this micro-layer, we know whether the listed sigil is navigable. | Link and route verification for README, SKILL, examples, validation, and adapter. | Review can reach every referenced artifact from the registry path. | Stop when registry navigation is reliable. |
| L3.3 Promotion Recommendation | After this micro-layer, we know what recommendation should go to the final approval gate. | Promotion recommendation with evidence, risks, and approval-pending status. | Recommendation names promote, hold, or revise. | Stop when registry candidate status is explicit without silently promoting. |

### L4 Reflection And Maintenance Micro-Layers

| Micro-Layer | Decision Question | Smallest Unit | Exit Evidence | Stop Condition |
| --- | --- | --- | --- | --- |
| L4.1 Reflection Signals | After this micro-layer, we know which usage patterns should trigger review. | Reflection thresholds for repeated drift, blocked runs, technique overuse, navigation failures, and missing evolution profiles. | Signals map to specific review questions. | Stop when reflection can start from evidence instead of vibes. |
| L4.2 Maintenance Change Classes | After this micro-layer, we know which changes are safe refinements versus redesign. | Change taxonomy for wording fixes, examples, technique tuning, mode changes, runtime changes, and contract changes. | Each class names required evidence and approval level. | Stop when maintainers know how much process a change needs. |
| L4.3 Evolution Loop | After this micro-layer, we know how the sigil can grow without breaking itself. | Maintenance loop linking observability, reflection report, design update, validation rerun, and release note. | Future evolution keeps objective-output, complexity balance, and navigability intact. | Stop when the loop can be followed by another agent. |

## Non-Regression Guardrails

- Later layers must preserve first-turn intent, target context, objective-output artifact, and budget confirmation.
- Later layers must preserve finite recursive rounds and cycle guards.
- Nested layers must preserve the parent layer's decision question and stop when work becomes directly executable as a Smallest Working Unit.
- Runtime adapter must not weaken technique pack trace requirements.
- Registry promotion must not imply global glossary promotion.
- Reflection changes must cite usage evidence before altering the core contract.

## Recommended Next Layer

- Next layer: L0 Candidate Package.
- Key decision unlocked: whether the approved design packet can become a self-contained manual sigil.
- Major deferred scope: runtime adapter, registry entry, and automated reflection.

## Gate Result

- Status: pass
- Reason: Layer boundaries cover the full sigil-development lifecycle from package to validation, runtime, registry, and reflection while preserving the smallest responsible start. Nested micro-layers now refine execution detail without exceeding the default recursion budget.
