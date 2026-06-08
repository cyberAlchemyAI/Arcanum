---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/signal-observer/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: signal-observer
description: "Use when: deriving post-run behavior signals from a sigil invocation envelope and appending reusable observability telemetry."
argument-hint: "--envelope <path> [--ledger <path>] [--mode new|update|observe|reflect|execute]"
tier: arcana
domain: observability
version: 0.1.0
origin: generalized from recurring post-session observability practice
allowed-tools: Read, Write, Glob, Grep, Bash, Agent
---

# Sigil: Signal Observer

<objective>
Provide independent post-run observation of sigil executions by reading an invocation envelope, deriving behavior-level signals, appending telemetry, and recommending follow-up.
</objective>

<logic-type>
Arcana: asynchronous observation and reflection routing over execution evidence.
</logic-type>

<applicability>
Use this sigil when:

- a sigil execution has completed, blocked, or failed,
- an invocation envelope exists or can be assembled safely,
- the run produced meaningful user-facing output, decision, validation, or orchestration result,
- the project has or wants a repository-local observability ledger,
- reflection thresholds should be evaluated from real usage.
  </applicability>

<inputs>
Expected inputs:

- invocation envelope path, preferably matching `framework/observability/templates/invocation-envelope.json`,
- optional telemetry ledger path,
- optional hook operations ledger path,
- visible execution summary,
- changed artifact list,
- validation results,
- Quality Bar and Anti-Patterns for the invoked sigil, when available,
- reflection state, when available.
  </inputs>

<default-paths>
Use these defaults when the user does not provide explicit paths:

- envelope: `.arcanum/observability/tmp/latest-invocation.json`
- ledger: `.arcanum/observability/signals/sigil-invocations.jsonl`
- reflection state: `.arcanum/observability/reflection-state.json`
  </default-paths>

<process>
1. Load the invocation envelope.
2. Validate that the envelope contains:
   - timestamp,
   - sigil,
   - tier,
   - mode,
   - request summary or safe raw request,
   - execution status,
   - outputs,
   - changed files,
   - validation entries,
   - observer section or enough evidence to build one.
3. Refuse to store secrets, credentials, tokens, private keys, or unnecessary raw content.
4. Derive behavior-level signals:
   - `quality-pass`: Quality Bar appears satisfied,
   - `quality-gap`: Quality Bar is partial, failed, or unchecked without reason,
   - `anti-pattern-hit`: observed workflow violated an Anti-Pattern,
   - `output-drift`: output differs from the sigil output contract,
   - `workflow-gap`: trigger, input, process, template, validation, observability, or reflection gap,
   - `rework`: failure, correction, and pass sequence is visible,
   - `useful-pattern`: repeated behavior appears worth preserving.
5. Set reflection trigger state:
   - `none`,
   - `manual`,
   - `usage-threshold`,
   - `output-threshold`,
   - `gap-threshold`,
   - `severe-gap`.
6. Append exactly one JSON object to the configured JSONL ledger.
7. Record observer hook activity in the hook operations ledger with `observe: false` when hook self-tracking is enabled.
8. Update reflection counters if reflection state is available.
9. Validate appended telemetry when a JSON or JSONL checker is available.
10. Return a concise observation report.
</process>

<authority-rule>
This sigil is non-blocking by default. It appends observability signals and updates reflection counters only. It must not modify application source code, user artifacts, or the observed sigil unless explicitly delegated by a separate maintenance workflow.
</authority-rule>

<loop-guard>
Signal Observer must not observe its own hook operation as a normal capability run.

Use `.arcanum/observability/hooks/hook-operations.jsonl` for observer start, completion, skip, failure, and dedupe events. These rows must carry `observe: false`.
</loop-guard>

<privacy-rules>
- Do not store secrets, credentials, tokens, private keys, or sensitive raw content.
- Prefer summaries over raw request text when the request contains private details.
- Prefer file paths and artifact names over large content excerpts.
- Mark missing evidence as `not_checked` rather than inferring success.
</privacy-rules>

<quality-bar>
A successful execution of this sigil must:

- read or assemble a valid invocation envelope,
- derive signals only from visible evidence,
- append one valid JSON object per observed invocation,
- preserve privacy and avoid sensitive raw content,
- classify Quality Bar status and Anti-Pattern hits when evidence exists,
- evaluate reflection trigger state,
- avoid blocking or changing the primary task outcome.
  </quality-bar>

<anti-patterns>
Avoid:

- rewriting the observed sigil during observation,
- storing secrets or large raw conversation excerpts,
- inventing quality status without evidence,
- appending invalid JSONL,
- treating observability failure as primary task failure unless observability was the requested task,
- producing many telemetry rows for one invocation,
- hiding severe workflow gaps behind a generic success note.
  </anti-patterns>

<output-contract>
Return:

```markdown
## Signal Observer Result

- Observed sigil: <name>
- Result: recorded | skipped | failed
- Ledger: <path>
- Signals: <counts by type>
- Quality Bar: pass | partial | fail | not_checked
- Anti-Pattern hits: <count and summary>
- Reflection trigger: none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap
- Recommendation: none | targeted-update | reflect-now
- Validation: <checks performed>
```

</output-contract>
