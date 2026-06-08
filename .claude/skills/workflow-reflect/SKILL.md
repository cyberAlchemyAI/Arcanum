---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/workflow-reflect/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: workflow-reflect
description: "Use when: analyzing accumulated sigil observability signals to produce evidence-backed workflow improvement proposals."
argument-hint: "<sigil-name | --all> [--signals <path>] [--since <date>] [--min-signals <n>] [--dry-run]"
tier: arcana
domain: reflective-maintenance
version: 0.1.0
origin: generalized from recurring accumulated-signal reflection practice
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion, Agent
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
