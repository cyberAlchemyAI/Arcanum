# Arcanum Sigil: scope interview

<!-- arcanum:capability-id scope-interview -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command scope-interview -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-scope-interview-<UTC timestamp>`.
- `capability.id`: `scope-interview`
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

Run the installed Arcanum sigil `scope-interview` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `scope-interview`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/scope-interview/README.md

````markdown
# Scope Interview

Scope Interview is an Arcana sigil for turning a vague idea or existing repository into a discovery baseline.

It supports greenfield work, brownfield work, and mixed contexts. The sigil inspects available evidence, asks focused questions, separates observed facts from stated intent and hypotheses, records blocker decisions, and returns a readiness verdict.

## Problem It Solves

Early project work often mixes what exists, what someone wants, and what the team hopes is true. That confusion makes later planning brittle.

Scope Interview creates a stable discovery baseline before detailed specification or implementation. It clarifies actors, goals, workflows, boundaries, decisions, metrics, risks, and unknowns.

## Use When

- a new idea needs structured discovery,
- an existing repository needs a brownfield scope audit,
- project boundaries are unclear,
- business, product, or workflow assumptions need to be surfaced,
- a team needs a readiness verdict before planning.

## Do Not Use When

- the scope is already stable and documented,
- the user wants implementation now,
- the question is local to one task,
- the repository cannot be inspected and the user cannot answer questions,
- the work needs a narrow decision gate rather than broad discovery.

## Discovery Baseline

The output package should separate:

- observed evidence,
- stated intent,
- inferred hypotheses,
- decisions made,
- blocker decisions,
- in-scope boundaries,
- out-of-scope boundaries,
- candidate validation activities.

## Why This Is Arcana

Scope Interview coordinates repository inspection, human discovery, evidence classification, decision capture, and readiness routing. It is a strategic entrypoint, not a single artifact transformation.
````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/scope-interview/SKILL.md

````markdown
---
name: scope-interview
description: "Use when: interviewing a greenfield idea, brownfield repository, or mixed project scope into a structured discovery baseline."
argument-hint: "[greenfield|brownfield|auto] <project-or-scope> [--output <folder>]"
tier: arcana
domain: scope-discovery
version: 0.1.0
origin: generalized from recurring project discovery interview practice
allowed-tools: Read, Write, Glob, Grep, AskQuestions
---

# Sigil: Scope Interview

<objective>
Turn a vague idea or existing project into a usable discovery baseline that separates observed evidence, stated intent, hypotheses, decisions, and readiness gaps.
</objective>

<logic-type>
Arcana: discovery orchestration with evidence inspection, human interview, and readiness gates.
</logic-type>

<process>
1. Detect mode:
   - `greenfield`: little or no implementation or documentation exists,
   - `brownfield`: implementation or documentation already exists,
   - `auto`: inspect available materials and choose.
2. Build a cheap evidence baseline:
   - read project summaries, docs, tests, source entrypoints, existing decisions, and relevant notes when present,
   - avoid asking questions already answered by evidence.
3. Interview the user one focused question at a time about:
   - users or actors,
   - goals and jobs,
   - workflows,
   - policies and constraints,
   - integrations,
   - success metrics,
   - failure modes,
   - boundaries,
   - blocker decisions.
4. Separate every finding into one of these categories:
   - observed,
   - stated,
   - hypothesized,
   - decided,
   - unresolved.
5. Draft or update the discovery baseline package.
6. For brownfield or mixed mode, enforce scope gates:
   - in-scope areas have observed evidence or explicit user confirmation,
   - out-of-scope boundaries are documented,
   - blocker decisions are recorded with selected option or blocked status.
7. Add counter-positioning for central assumptions: plausible alternative explanations, downsides, or invalidation conditions.
8. Return a readiness verdict:
   - `ready for planning`,
   - `needs more discovery`,
   - `blocked on scope gate`,
   - `blocked on decisions`.
</process>

<quality-bar>
A successful execution must:

- distinguish observed, stated, hypothesized, decided, and unresolved content,
- cite repository evidence when available,
- document in-scope and out-of-scope boundaries,
- record blocker decisions or blocked status,
- make hypotheses falsifiable,
- avoid implementation planning before the baseline is stable,
- return a readiness verdict with concrete next actions.
</quality-bar>

<anti-patterns>
Avoid:

- treating user hopes as observed facts,
- inspecting code so broadly that the interview never starts,
- producing implementation tasks before scope is understood,
- hiding out-of-scope boundaries,
- omitting counter-positions for central assumptions,
- marking readiness while blocker decisions remain unresolved.
</anti-patterns>

<output-contract>
Return:

```markdown
## Scope Interview Result

- Mode: greenfield | brownfield | auto
- Scope: <scope>
- Evidence inspected: <summary>
- Discovery artifacts: <paths>
- Decisions recorded: <count>
- Blockers: <count>
- Verdict: ready for planning | needs more discovery | blocked on scope gate | blocked on decisions
- Next actions: <ordered list>
```
</output-contract>
````
