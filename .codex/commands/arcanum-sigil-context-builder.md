# Arcanum Sigil: context builder

<!-- arcanum:capability-id context-builder -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier transmutations -->
<!-- arcanum:command arcanum-sigil-context-builder -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-sigil-context-builder-<UTC timestamp>`.
- `capability.id`: `context-builder`
- `capability.kind`: `sigil`
- `capability.tier`: `transmutations`
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

Run the installed Arcanum sigil `context-builder` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `context-builder`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/transmutations/context-builder/README.md

````markdown
# Context Builder

Context Builder is a Transmutation sigil for creating a compact task-ready context pack from existing project evidence.

It selects only the source excerpts needed to execute a task, maps each excerpt to a concrete obligation, and rejects context that is merely interesting. The result is a smaller, more useful bundle for agents, reviewers, or implementation sessions.

For runtime delegation, Context Builder can emit a handoff pack. A handoff pack is a context pack prepared for a runtime adapter or native goal. It is stored as session evidence, emitted as Markdown plus JSON/index, and blocks when strict obligation coverage is not satisfied.

## Problem It Solves

Large repositories often bury the relevant facts under too much background material. Agents can waste time reading whole files, miss the exact obligation, or carry unrelated context into the task.

Context Builder solves this by using link-first retrieval, selector-level evidence, obligation coverage, and noise limits.

For Codex Goal handoff, it also prevents weak runtime prompts by requiring every obligation to be covered or explicitly resolved before delegation.

## Use When

- a task needs a focused evidence pack before execution,
- requirements, architecture notes, code snippets, tests, and decisions are scattered,
- a later agent or reviewer should not reread the whole repository,
- the task has explicit obligations or completion criteria,
- context size must stay bounded,
- a runtime adapter needs selected context without doing broad repository exploration.

## Do Not Use When

- the task is simple enough to execute directly,
- no source material exists,
- the user wants a broad codebase map rather than task context,
- the work requires autonomous orchestration rather than bounded synthesis,
- selected excerpts cannot be linked to concrete obligations,
- a runtime handoff would need to proceed with uncovered, contradictory, stale, unsafe, missing write-scope, or missing validation obligations.

## Output

The sigil produces a context pack with:

- target task,
- obligation matrix,
- selected excerpts,
- selectors or anchors,
- obligation coverage,
- excluded candidates,
- unresolved gaps,
- optional machine-readable index.

When `--handoff codex-goal` is used, the sigil produces both:

- a Markdown handoff pack for human review and task-session reporting,
- a JSON or structured index for adapters and goal-profile handoff.

Persisted handoff packs should live under a run/session evidence path. They are audit evidence for a specific execution, not canonical planning documents.

## Why This Is A Transmutation

Context Builder transforms scattered project material into a bounded, evidence-linked artifact. It requires judgment, but the output is a concrete context package rather than a long-running orchestration loop.
````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/transmutations/context-builder/SKILL.md

````markdown
---
name: context-builder
description: "Use when: building a compact, task-ready context pack from selector-level evidence and obligation-linked excerpts."
argument-hint: "<task-reference> [--mode lean|standard|deep] [--max-files <n>] [--strict] [--emit markdown|json|both] [--handoff codex-goal] [--persist <session-evidence-path>] [--dry-run]"
tier: transmutations
domain: context-synthesis
version: 0.2.0
origin: generalized from recurring task-context retrieval practice
allowed-tools: Read, Write, Glob, Grep, Bash, AskQuestions
---

# Sigil: Context Builder

<objective>
Produce a minimal task-ready context bundle that maximizes relevance, preserves evidence selectors, and minimizes reading overhead. When requested for runtime delegation, emit a strict handoff pack as session evidence in both Markdown and structured JSON/index form.
</objective>

<logic-type>
Transmutation: bounded evidence selection and structured context synthesis.
</logic-type>

<flags>
- `--mode lean|standard|deep`: control excerpt budget. Default: `standard`.
- `--max-files <n>`: override the file count budget.
- `--strict`: require every selected item to map to an obligation. Default: on.
- `--emit markdown|json|both`: choose output format. Default: `markdown`.
- `--handoff codex-goal`: emit a runtime handoff pack suitable for Codex Goal delegation. This implies strict obligation coverage and `--emit both`.
- `--persist <session-evidence-path>`: write handoff artifacts under a run/session evidence path. Persisted packs are execution evidence, not canonical planning documents.
- `--dry-run`: preview selected context without writing artifacts.
</flags>

<handoff-pack-contract>
When `--handoff codex-goal` is used, Context Builder produces a handoff pack with identity, obligations, selected sources, architecture guidance, related feature context, constraints, non-goals, write scope, done criteria, validation surface, gaps, blockers, contradictions, authority precedence, fallback exploration rule, provenance, and Markdown plus JSON/index output paths.

Strict coverage rule: a Codex Goal handoff pack is runnable only when every obligation is covered by selected evidence or explicitly resolved as not applicable/deferred. Uncovered, contradictory, stale, unsafe, missing write-scope, or missing validation obligations return `BLOCK`.

Persistence rule: persisted handoff packs live under session/run evidence. They are audit artifacts for that execution, not reusable source-of-truth documents.
</handoff-pack-contract>

<process>
1. Resolve the target task and its expected output.
2. Parse task obligations from the request, task file, requirements, checklist, acceptance criteria, or completion criteria.
3. Build an obligation matrix where each obligation has an ID, required evidence, and unresolved status.
4. Seed retrieval from explicit links and references first.
5. Extract selectors before inclusion:
   - markdown headings, anchors, tables, or bullet ranges,
   - code symbols, declarations, tests, endpoint contracts, or minimal snippet windows,
   - config keys, scripts, schemas, or command references.
6. Expand search only for uncovered obligations and scope searches to relevant folders or filenames.
7. Exclude any candidate that does not close at least one obligation.
8. Rank selected evidence by relevance, cost, and ambiguity.
9. Enforce budgets:
   - `lean`: up to 8 files and 140 excerpt lines,
   - `standard`: up to 14 files and 280 excerpt lines,
   - `deep`: up to 24 files and 520 excerpt lines.
10. If `--handoff codex-goal` is set, enforce strict coverage and prepare Markdown plus JSON/index handoff outputs.
11. Persist handoff outputs under the requested session evidence path when `--persist` is provided.
12. Emit the context pack and optional index.
13. Return blockers for obligations that lack sufficient evidence.
</process>

<quality-bar>
A successful execution must:

- include only selector-level evidence,
- map every selected item to at least one obligation,
- keep the noise ratio low,
- separate evidence from inference,
- report uncovered obligations,
- block runtime handoff packs unless all obligations are covered or explicitly resolved,
- avoid repository-wide context dumps,
- produce a compact artifact another agent can use immediately,
- emit Markdown plus JSON/index for Codex Goal handoff packs,
- label persisted handoff packs as session evidence rather than canonical docs.
</quality-bar>

<anti-patterns>
Avoid:

- copying whole files when a selector would suffice,
- including background material because it is interesting,
- running broad unbounded searches,
- omitting why each item was selected,
- hiding unresolved obligations,
- allowing a Codex Goal handoff from incomplete, stale, contradictory, unsafe, or validation-missing context,
- persisting handoff packs beside canonical planning docs without labeling them session evidence,
- exceeding the selected mode budget without explanation.
</anti-patterns>

<output-contract>
Return:

```markdown
## Context Pack Summary

- Task: <task-reference>
- Mode: lean | standard | deep
- Files selected: <count>
- Snippets selected: <count>
- Obligation coverage: <percent>
- Noise ratio: <value>
- Output markdown: <path or dry-run>
- Output index: <path or none>
- Handoff pack: <none | codex-goal>
- Session evidence path: <path | none | dry-run>
- Strict coverage: pass | block | n/a
- Blockers: <count>

### Included Context

- <path> - <why included> - <selectors> - <obligation refs>

### Excluded Candidates

- <path> - <why excluded>

### Next Actions

1. <action>
```
</output-contract>
````
