---
name: dispatch-spec
description: "Use when: validating or designing an Arcanum dispatch route that chains sigils, spells, owner capabilities, handoffs, gates, observability, techniques, and optional boundary/evidence contracts."
argument-hint: "<dispatch.json|route intent> [--validate] [--fixtures]"
tier: formulae
domain: dispatch-governance
version: 0.3.0
origin: Formulae package for Arcanum route-shape validation and boundary/evidence contracts
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Dispatch Spec Skill

## Identity

- Canonical ID: `dispatch-spec`
- Tier: Formulae
- Status: draft
- Scope: repository-local validation package

## Purpose

Validate a dispatch document that describes a sequence, fan-out, tournament, dialectic, validation loop, or synthesis graph over Arcanum sigils and spells.

This skill does not decide which sigils should be used. It checks whether a proposed composition is explicit enough for Spellcraft, Necronomicon, Invoke, Task Session, Experiment Harness, and observability tooling to consume safely.

## Use When

- A user wants to chain sigils by name into a repeatable route.
- Necronomicon proposes an execution route and needs a schema-valid handoff.
- Spellcraft is designing a spell and needs a phase/step contract before lifecycle work.
- Robot-Talks, Distill tournament, or another multi-agent pattern needs sibling steps tied by one `dispatch_id`.
- A run should record how outputs from one sigil become inputs to another.
- A route needs to cite reusable techniques from [TECHNIQUE-CATALOG.md](TECHNIQUE-CATALOG.md), including Arcanum composition techniques or POLE-inspired standards-catalog techniques.
- Refine needs a route artifact for its canonical ten-stage loop without making the Refine process itself the orchestrator.
- Refine or another orchestrating capability needs a visible subagent strategy before asking permission to run delegated or parallel stage work.
- An orchestrator needs to bind each delegated role to one lifecycle or execution capability, order roles into waves, and prevent downstream mutation before upstream receipts pass.
- A route needs optional `boundary_evidence` for cross-capability handoffs, authority owners, receipts, state namespaces, or promotion splits.

## Do Not Use When

- The task needs interpretation but no reusable dispatch artifact.
- The user asks for immediate execution of a single, obvious sigil.
- A blocker decision exists about the route itself; use `decision-gate` first.
- The workflow would copy sigil internals instead of referencing sigils by id.

## Required Input

A JSON document conforming to [dispatch.schema.yml](dispatch.schema.yml).

## Deterministic Validator

Use the repository-local validator when available:

```bash
formulae/dispatch-spec/scripts/validate-dispatch.py <dispatch.json>
```

For package fixtures:

```bash
formulae/dispatch-spec/development/run-validation-fixtures.sh
```

## Validation Rules

1. The document must include `dispatch_id`, `intent`, `mode`, `steps`, and `gates`.
2. Each step must reference a known or candidate `capability_ref`.
3. Each step must declare a `pattern`: `route`, `sequential`, `fanout`, `dialectic`, `tournament`, `distill`, `xray`, `decision`, `validation`, `toy_game`, `synthesis`, or `handoff`.
4. Non-first steps must name at least one input source: prior `frame`, `handle`, `decision`, `ledger`, `receipt`, `artifact`, `human_answer`, or `external_context`.
5. Any step with `parallel: true` must declare `join_policy`.
6. Tournament and dialectic steps must declare proposal roles and convergence criteria.
7. Validation and toy-game steps must declare an expected evidence artifact.
8. The dispatch must name stop conditions and at least one observability event.
9. The dispatch must not claim promotion authority for inventory, ontology, glossary, sigil, or spell artifacts.
10. Any cited technique must either appear in `TECHNIQUE-CATALOG.md` or include a local-extension source and validation note.
11. A dispatch that cites techniques without connecting them to steps, gates, evidence, or validation should return `flag`.
12. Technique overlays must name a trigger, technique ids, affected steps, and validation expectation.
13. Dialectic and tournament techniques require roles and convergence criteria even when they are used as step techniques rather than step patterns.
14. X-ray techniques require a handle or artifact output; toy-game techniques require an evidence artifact.
15. Boundary/evidence techniques should be backed by `boundary_evidence`; otherwise the route should return `flag`.
16. `boundary_evidence.boundaries[].applies_to_steps` must reference existing step ids.
17. `state_namespace_boundary` should include `boundary_evidence.state_namespaces`.
18. `memory_promotion_split` should include `boundary_evidence.promotion_splits`.
19. `execution_receipt_handoff` should include `boundary_evidence.receipts`.
20. Execution evidence must not directly promote Inventory, Ontology, glossary, sigil, or spell knowledge.
21. `subagent_strategy.status=recommended|required` must name roles, join policy, authorization, and the reason subagents fit the problem shape.
22. Recommended or required subagent execution should default to `authorization=requires_user_permission` until the operator approves the run.
23. Recommended or required subagent execution must include lifecycle receipt fields: `agent_id`, `role_id`, `spawn_status`, `join_status`, `close_status`, `residue`, and `reroute`.
24. A `subagent_lifecycle.status=pass` ledger must prove every spawned agent reached a terminal join state and terminal close state.
25. Blocked spawn, timed-out join, blocked join, or thread-cap failure only passes as named residue with a reroute or handoff.
26. `binding_mode=capability-bound` requires an `execution_owner`, capability-bound roles, and ordered `execution_waves`.
27. Every capability-bound role must name its `capability_ref`, `capability_target`, `capability_mode`, `agent_count`, mutation policy, applied steps, and output receipts.
28. A role's capability must match the capability of every step it owns; its input and output refs must be present on those steps.
29. `lifecycle-owned` and `artifact-only` roles require explicit write scopes; read-only roles cannot declare a write scope.
30. Write scopes must be normalized repository-relative paths. Concurrent roles cannot have overlapping write scopes, and a role's write scope cannot overlap its forbidden scopes.
31. Role dependencies must be in earlier execution waves, be mirrored by `depends_on_waves`, and consume at least one receipt from each dependency.
32. Every non-final wave requires a named `gate_after` that identifies the wave and its required role receipts; later waves cannot start until their declared joins and gate pass.
33. A capability-bound lifecycle closeout requires prior authorization and must identify each agent's capability, target, mode, wave, and effective write scope.
34. A passing capability-bound closeout must contain exactly the declared number of agent records for every role.
35. Every agent in a passing capability-bound closeout must have spawned, completed its join, closed, and returned its declared receipt; every applied step must also have a passing native-stage receipt containing the role output.

## Subagent Strategy

Use `subagent_strategy` when the route shape implies role-bound sibling agents,
parallel critique, tournament comparison, x-ray exploration, memory recovery, or
delegated verification.

Dispatch Spec may recommend or require the strategy, but it does not execute
subagents. The orchestrating capability, usually Refine, must show the strategy
with context and ask permission before runtime execution.

Minimum fields:

- `status`: `none`, `recommended`, `required`, or `blocked`.
- `trigger`: the problem-shape signal that caused the strategy.
- `explanation`: why these roles are useful for this target.
- `context`: target-specific evidence or uncertainty that informed the choice.
- `roles`: role id, purpose, ownership, and affected steps.
- `parallelism`: `none`, `fanout`, `dialectic`, `tournament`, or `mixed`.
- `join_policy`: how returned receipts are joined.
- `authorization`: `not_needed`, `requires_user_permission`, `approved`, or `blocked`.
- `permission_prompt`: the prompt the orchestrator should show before execution.
- `receipt_requirements`: evidence each subagent must return.

### Capability-Bound Delegation

Use `binding_mode: capability-bound` when the dispatch must be executable by a
parent orchestrator rather than merely describe useful roles. Each role names
one governing capability and target. `execution_waves` then define which roles
may run together, where the parent must join them, and which gate unlocks the
next wave.

The parent orchestrator owns spawning, joining, gating, and synthesis.
Dispatch Spec validates that contract but does not spawn agents itself. A
typical route is:

```text
wave 1 (parallel)
  sigil-development -> x-ray receipt
  spellcraft         -> whisper receipt
  join all -> lifecycle gate

wave 2
  task-session -> artifact-only repair consuming both receipts
```

See
[capability-bound-artifact-repair.json](examples/capability-bound-artifact-repair.json)
for a complete executable-shape instance.

## Subagent Lifecycle

Use `subagent_lifecycle` only after a runtime or parent route has attempted
delegated execution. It is the closeout ledger for AFK-safe dispatches: the
parent cannot report success while a spawned sibling agent remains open,
unjoined, hidden, or only implicitly abandoned.

Minimum fields:

- `status`: `none`, `pass`, `flag`, or `block`.
- `agents`: one entry per attempted delegated agent.
- `agent_id`: stable runtime or parent-assigned identifier.
- `role_id`: matching role from `subagent_strategy.roles`.
- `spawn_status`: `spawned` or `blocked`.
- `join_status`: `completed`, `timed_out`, `blocked`, `handed_off`, `closed_without_result`, `pending`, or `not_needed`.
- `close_status`: `closed`, `already_closed`, `handed_off`, `blocked`, `pending`, or `not_needed`.
- `receipt_artifact`: required when `join_status=completed`.
- `residue`: required for blocked spawn, timed-out join, blocked join, or other non-happy-path closeout.
- `reroute`: required when work is handed off, blocked, timed out, or capped by runtime/thread limits.

`status=pass` is only valid when every spawned agent has a terminal join and
terminal close state. Hidden open subagents, pending joins, and pending close
states return `block`.

## Output Contract

```markdown
## Dispatch Spec Result

- Dispatch ID: <dispatch_id>
- Status: pass | flag | block
- Mode: <mode>
- Step count: <n>
- Patterns: <patterns found>
- Gates: <pass | flag | block with reasons>
- Handoffs: <frame/handle/decision/ledger summary>
- Subagent strategy: <none | recommended | required | blocked, roles, join policy, authorization>
- Capability bindings: <descriptive | capability-bound, execution owner, waves, dependencies, write scopes>
- Subagent lifecycle: <n/a | pass | flag | block, open agents, residue, reroute>
- Observability: <dispatch_id coverage and trace events>
- Promotion guardrail: pass | flag | block
- Required repairs: <none or list>
- Next route: necronomicon | spellcraft | invoke | task-session | experiment-harness | decision-gate | deferred
```

## Failure Policy

- Return `block` when required fields are missing, step dependencies are impossible, promotion authority is falsely claimed, or delegated subagents remain unjoined/unclosed.
- Return `flag` when the document is usable but has weak evidence names, candidate capabilities, or incomplete observability metadata.
- Return `pass` only when the route is explicit, gated, observable, and handoff-ready.
