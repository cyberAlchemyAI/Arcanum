# Arcanum Sigil: workflow reflect

<!-- arcanum:capability-id workflow-reflect -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command workflow-reflect -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-workflow-reflect-<UTC timestamp>`.
- `capability.id`: `workflow-reflect`
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

Run the installed Arcanum sigil `workflow-reflect` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `workflow-reflect`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/workflow-reflect/README.md

````markdown
# Workflow Reflect

Workflow Reflect is an Arcana sigil for turning accumulated sigil observability signals into evidence-backed improvement proposals.

It is the retrospective outer loop for sigil maintenance. It reads telemetry, detects repeated gaps and useful patterns, computes simple trend metrics, compares current behavior to previous reflections, and writes a reflection report with concrete recommendations.

## Problem It Solves

One failed run can be noise. Repeated failures, output drift, user corrections, or anti-pattern hits are signals that the sigil itself may need improvement.

Workflow Reflect prevents maintenance from being driven only by memory or vibes. It uses accumulated telemetry to decide whether a sigil needs no change, a targeted update, a major revision, or retirement.

## Use When

- a reflection threshold has been reached,
- a user asks for a retrospective on sigil behavior,
- repeated workflow gaps appear in observability ledgers,
- a sigil has generated enough outputs to review quality trends,
- maintainers need evidence before changing a sigil contract.

## Do Not Use When

- there are too few signals to support a useful pattern claim,
- the user only needs the latest run observed by [signal-observer](../signal-observer/),
- the sigil itself should be edited immediately by a separate maintenance workflow,
- telemetry contains sensitive content that has not been summarized or redacted,
- the desired outcome is implementation work rather than reflection.

## Reflection Loop

1. Load signal ledgers and reflection state.
2. Apply filters such as sigil name, date range, or minimum signal count.
3. Group signals by type, severity, sigil, mode, output contract, and gap category.
4. Detect recurring workflow gaps, quality failures, anti-pattern hits, output drift, and useful patterns.
5. Compare current patterns against previous reflection reports.
6. Generate evidence-backed proposals.
7. Write a reflection report.
8. Recommend no change, targeted update, major revision, or retirement.

## Output

The sigil produces a reflection report with:

- signal summary,
- triggered thresholds,
- repeated patterns,
- gap analysis,
- proposed iterations,
- rejected changes,
- contract preservation notes,
- updated reflection policy,
- recommended next lifecycle step.

## Related Docs

- [Signal Observer](../signal-observer/)
- [Sigil Observability Hook](../../framework/observability/SIGIL-OBSERVABILITY-HOOK.md)
- [Repository Observability Package](../../framework/observability/REPOSITORY-PACKAGE.md)

## Why This Is Arcana

Workflow Reflect coordinates cross-run evidence analysis, threshold interpretation, proposal generation, and lifecycle routing. It changes the future of the workflow by interpreting accumulated behavior, not by executing a single local transformation.

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/workflow-reflect/SKILL.md

````markdown
---
name: workflow-reflect
description: "Use when: analyzing accumulated sigil observability signals to produce evidence-backed workflow improvement proposals."
argument-hint: "<sigil-name | --all> [--signals <path>] [--since <date>] [--min-signals <n>] [--dry-run]"
tier: arcana
domain: reflective-maintenance
version: 0.1.0
origin: generalized from recurring accumulated-signal reflection practice
allowed-tools: Read, Write, Glob, Grep, Bash, AskQuestions, Task
---

# Sigil: Workflow Reflect

<objective>
Analyze accumulated observability signals across sigil executions, detect repeated patterns, compute lightweight trends, and produce evidence-backed improvement proposals without directly mutating the observed sigils.
</objective>

<logic-type>
Arcana: retrospective outer loop for governed workflow improvement.
</logic-type>

<flags>
- `--all`: analyze all sigils in the available ledgers.
- `--signals <path>`: read signals from an explicit JSONL ledger.
- `--since <date>`: analyze only signals after an ISO date.
- `--min-signals <n>`: require a minimum signal count before writing a report. Default: `5`.
- `--dry-run`: show the analysis path and candidate findings without writing a report.
</flags>

<applicability>
Use this sigil when:

- reflection thresholds are reached,
- a maintainer requests a retrospective on sigil behavior,
- repeated workflow gaps, quality failures, user corrections, or output drift appear,
- there is enough telemetry to support pattern-level claims,
- changes to a sigil should be proposed from evidence rather than a single anecdote.
</applicability>

<inputs>
Expected inputs:

- signal ledger path, usually `.arcanum/observability/signals/sigil-invocations.jsonl`,
- optional per-sigil ledger path,
- reflection state path,
- previous reflection reports, if available,
- target sigil name or `--all`,
- threshold configuration,
- report output path.
</inputs>

<default-paths>
Use these defaults when explicit paths are not provided:

- signals: `.arcanum/observability/signals/sigil-invocations.jsonl`
- reflection state: `.arcanum/observability/reflection-state.json`
- reports: `.arcanum/observability/reflections/`
</default-paths>

<process>
## Step 1 - Load Signals

1. Read the configured JSONL signal ledger.
2. Parse each line as one JSON object.
3. Validate required fields where possible.
4. Apply target sigil, mode, and `--since` filters.
5. If the remaining signal count is below `--min-signals`, return insufficient evidence and do not write a report unless the user explicitly requests a dry-run summary.

## Step 2 - Group Evidence

6. Group signals by:
   - sigil,
   - tier,
   - mode,
   - execution status,
   - Quality Bar status,
   - Anti-Pattern hit,
   - workflow gap category,
   - severity,
   - output-contract drift,
   - observer recommendation.
7. Identify repeated patterns using exact matches first and concise human review for similar summaries.

## Step 3 - Evaluate Thresholds

8. Evaluate reflection thresholds from configuration or defaults:
   - meaningful executions,
   - generated outputs,
   - related workflow gaps,
   - severe workflow gaps,
   - Quality Bar failures,
   - output-contract drift events,
   - user corrections.
9. Separate threshold-backed findings from weak signals.

## Step 4 - Generate Proposals

10. For each threshold-backed finding, generate a concrete proposal with:
    - evidence,
    - affected sigil section or contract area,
    - recommended change,
    - expected prevention effect,
    - priority,
    - compatibility impact.
11. Preserve the sigil's core contract unless evidence shows the contract itself is failing.
12. Record rejected or deferred changes with reasons.

## Step 5 - Write Reflection Report

13. Write a reflection report to the configured reports folder unless `--dry-run` is set.
14. Include:
    - reflection context,
    - signal summary,
    - patterns found,
    - gap analysis,
    - proposed iterations,
    - rejected changes,
    - contract preservation notes,
    - updated reflection policy,
    - decision and next lifecycle step.
15. Update reflection state only after a report is successfully written.

## Step 6 - Return Actionable Summary

16. Return a compact summary with analyzed signal counts, thresholds triggered, proposal counts, report path, and recommended next action.
</process>

<authority-rule>
This sigil writes reflection reports and may update reflection state. It must not directly modify the observed sigil, application source code, or user-facing artifacts unless the user explicitly starts a separate maintenance task.
</authority-rule>

<quality-bar>
A successful execution of this sigil must:

- analyze only valid, relevant signal evidence,
- avoid making pattern claims from insufficient data,
- distinguish threshold-backed findings from weak signals,
- generate concrete and actionable proposals,
- preserve the observed sigil's core contract unless evidence justifies a contract change,
- write a report that a maintainer can act on,
- keep direct sigil mutation out of the reflection step.
</quality-bar>

<anti-patterns>
Avoid:

- editing the observed sigil during reflection,
- treating one anecdote as a trend,
- ignoring severe gaps because aggregate counts are low,
- proposing vague improvements without target sections,
- preserving raw sensitive content in reports,
- resetting reflection counters before a report is written,
- hiding compatibility impact when recommending contract changes.
</anti-patterns>

<output-contract>
Return:

```markdown
## Workflow Reflect Result

- Scope: <sigil-name | all>
- Signals analyzed: <count>
- Thresholds triggered: <list or none>
- Patterns found: <count and summary>
- Proposals generated: <count by priority>
- Report: <path or dry-run>
- Reflection state: <updated | unchanged | unavailable>
- Recommended next action: <none | targeted update | major revision | retire | gather more signal>
```
</output-contract>
````
