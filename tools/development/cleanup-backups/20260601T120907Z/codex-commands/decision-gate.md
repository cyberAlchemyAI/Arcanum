# Arcanum Sigil: decision gate

<!-- arcanum:capability-id decision-gate -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command decision-gate -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-decision-gate-<UTC timestamp>`.
- `capability.id`: `decision-gate`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `decision-gate` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `decision-gate`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/decision-gate/README.md

````markdown
# Decision Gate

Decision Gate is an Arcana sigil for resolving blocker-level multi-option decisions before planning, implementation, document mutation, or other consequential changes continue.

It prevents an agent from silently choosing among viable options when the choice belongs to the user, project owner, or reviewer. The sigil identifies unresolved decisions, presents options with trade-offs, records the selected path, and returns a clear pass or block result.

## Problem It Solves

Agents often encounter choices that look small but shape the rest of the work: scope boundaries, persistence strategy, fallback behavior, rollout mode, verification level, ownership, naming, or policy strictness.

If those decisions are guessed, later work may be technically correct but aligned to the wrong assumption. Decision Gate solves this by making blocker decisions explicit before mutation happens.

## Use When

- a task has more than one viable path,
- a choice will affect future implementation, documentation, governance, cost, risk, or user experience,
- the agent cannot responsibly infer the user's preference,
- work should stop until a decision is made,
- a reusable decision record is needed.

## Do Not Use When

- the choice is purely local and reversible,
- the user already made the decision clearly,
- the task only needs factual lookup,
- the decision can be safely handled by a deterministic rule,
- asking would add delay without changing the outcome.

## Decision Model

Decision Gate uses a simple pass/block model:

- `PASS`: all blocker-level decisions are resolved and recorded.
- `BLOCK`: at least one blocker-level decision remains unresolved, so consequential mutation should not proceed.

Non-blocking choices can be recorded as assumptions or deferred decisions, but they must not be mixed with blocker decisions.

## Output

The sigil produces a decision record with:

- decision question,
- options considered,
- trade-offs,
- selected option,
- rationale,
- source of decision,
- timestamp,
- remaining blockers, if any.

## Why This Is Arcana

The sigil governs whether other work may proceed. It coordinates ambiguity, user choice, persistence, and stop/go authority across a task lifecycle. Its value is not just the decision artifact; it is the gate that prevents hidden assumptions from becoming implementation facts.
````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/decision-gate/SKILL.md

````markdown
---
name: decision-gate
description: "Use when: resolving blocker-level multi-option decisions before planning, implementation, document mutation, or other consequential changes continue."
argument-hint: "<target-scope> [--profile generic|pilot|release|custom] [--output <path>]"
tier: arcana
domain: decision-governance
version: 0.1.0
origin: generalized from recurring pre-mutation decision governance practice
allowed-tools: Read, Write, Glob, Grep, AskQuestions
---

# Sigil: Decision Gate

<objective>
Resolve every blocker-level multi-option decision before consequential work proceeds, and persist a reusable decision record.
</objective>

<logic-type>
Arcana: decision governance with human gatekeeping and pass/block authority.
</logic-type>

<applicability>
Use this sigil when:

- a task has multiple viable options,
- the choice affects future scope, implementation, documentation, rollout, policy, verification, cost, or risk,
- the agent cannot responsibly infer the correct option,
- downstream work should stop until the decision is explicit,
- a durable decision record is needed.
</applicability>

<inputs>
Expected inputs, if available:

- target scope or task name,
- existing request, plan, notes, requirements, architecture docs, or implementation files,
- known constraints,
- options already proposed by the user,
- preferred output path,
- decision profile, if the project has one.
</inputs>

<default-output>
If the user does not provide `--output`, write or update the decision record at the first suitable location:

1. `docs/decisions/{target-scope}.md` when a docs folder exists,
2. `decisions/{target-scope}.md` when a decisions folder exists,
3. `DECISIONS.md` at the repository root when no better location exists.
</default-output>

<process>
1. Identify the target scope and the consequential work that is blocked by unresolved decisions.
2. Gather only relevant context: user request, current plan, requirements, architecture notes, related docs, implementation files, tests, and known constraints.
3. Enumerate unresolved decisions with more than one viable option.
4. Classify each decision:
   - blocker: must be resolved before consequential mutation,
   - deferrable: can be recorded and revisited later,
   - assumption: can proceed if clearly labeled.
5. For each blocker decision, prepare concrete options with concise trade-offs:
   - option name,
   - benefit,
   - cost or risk,
   - when to choose it,
   - downstream impact.
6. Ask the user each blocker decision:
   - prefer an ask-questions interface when available,
   - otherwise use plain conversation with numbered options.
7. Continue until all blocker decisions are resolved or the user explicitly defers/stops.
8. If any blocker decision remains unresolved, return `BLOCK` and do not proceed with consequential mutation.
9. Persist the decision record with:
   - decision question,
   - considered options,
   - selected option,
   - rationale,
   - source of decision,
   - timestamp,
   - remaining blockers,
   - deferred decisions or assumptions.
10. Return a decision-gate summary with `PASS` or `BLOCK`, resolved decisions, remaining blockers, and the decision artifact path.
</process>

<authority-rule>
When this sigil returns `BLOCK`, consequential mutation should not proceed until the blocker decisions are resolved or the user explicitly overrides the gate.
</authority-rule>

<observability>
For reusable use, emit a post-run invocation signal using the repository-local observability package when available.

Recommended signals:

- decision count,
- blocker count,
- unresolved blocker count,
- pass/block result,
- output path,
- user override, if any,
- follow-up reflection trigger when the same decision type repeats.
</observability>

<quality-bar>
A successful execution of this sigil must:

- identify every visible blocker-level multi-option decision,
- separate blocker decisions from deferrable decisions and assumptions,
- present options with meaningful trade-offs,
- avoid choosing on the user's behalf when the decision is consequential,
- persist a reviewable decision record,
- return a clear `PASS` or `BLOCK` result,
- preserve enough context for future reviewers to understand why each decision was made.
</quality-bar>

<anti-patterns>
Avoid:

- asking the user to decide trivial or fully reversible details,
- bundling multiple independent decisions into one vague question,
- presenting options without trade-offs,
- treating silence as consent for a blocker decision,
- proceeding with consequential mutation after a `BLOCK` result,
- hiding assumptions inside implementation or documentation,
- writing a decision record that cannot be traced back to the user choice or source context.
</anti-patterns>

<output-contract>
Return:

```markdown
## Decision Gate Result

- Target scope: <scope>
- Result: PASS | BLOCK
- Decisions resolved: <count>
- Blockers remaining: <count>
- Decision artifact: <path>
- Deferred decisions: <summary or none>
- Assumptions recorded: <summary or none>
- Validation: <checks performed>
- Next step: <proceed | ask remaining decision | stop>
```
</output-contract>
````
