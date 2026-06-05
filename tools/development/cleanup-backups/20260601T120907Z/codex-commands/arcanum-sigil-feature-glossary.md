# Arcanum Sigil: feature glossary

<!-- arcanum:capability-id feature-glossary -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier transmutations -->
<!-- arcanum:command arcanum-sigil-feature-glossary -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-sigil-feature-glossary-<UTC timestamp>`.
- `capability.id`: `feature-glossary`
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

Run the installed Arcanum sigil `feature-glossary` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `feature-glossary`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/transmutations/feature-glossary/README.md

````markdown
# Feature Glossary

Feature Glossary is a Transmutation sigil for creating or updating a concise vocabulary layer for a feature, workflow, product area, or bounded project scope.

It turns scattered terminology into a reviewable glossary that starts with plain-language terms and then lists formal concepts when the source material supports them.

## Problem It Solves

Teams often reuse words like baseline, gate, variant, account, session, policy, or revision without defining what they mean in the current feature. Formal concepts may exist too, but readers need the everyday vocabulary first.

Feature Glossary gives readers a stable language layer while preserving links back to authoritative source material.

## Use When

- a feature or workflow has recurring terms that need shared meaning,
- source docs contain concept tables, requirements, UI terms, states, operations, or policies,
- onboarding readers need plain-language definitions,
- duplicate or conflicting terms are creating ambiguity,
- formal concept definitions should be summarized without becoming the authority source.

## Do Not Use When

- the source material is too unstable to define terms,
- new behavior needs to be invented inside the glossary,
- the glossary would replace the authoritative source document,
- the task requires global definitions governance instead,
- there are no recurring terms to clarify.

## Output

The glossary should include:

- feature language terms,
- formal concepts when present,
- source links,
- related terms,
- unresolved terms,
- duplicate or conflict notes.

## Why This Is A Transmutation

Feature Glossary transforms scattered vocabulary into a bounded, evidence-linked artifact. It requires interpretation, but it does not coordinate a long-running governance loop.
````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/transmutations/feature-glossary/SKILL.md

````markdown
---
name: feature-glossary
description: "Use when: creating or updating a concise glossary for a feature, workflow, product area, or bounded project scope from source evidence."
argument-hint: "<scope> [--update] [--output <path>]"
tier: transmutations
domain: vocabulary-synthesis
version: 0.1.0
origin: generalized from recurring feature vocabulary distillation practice
allowed-tools: Read, Write, Glob, Grep
---

# Sigil: Feature Glossary

<objective>
Create or update a concise human-readable glossary that explains plain-language terms first and formal concepts second, while linking each definition to source evidence.
</objective>

<logic-type>
Transmutation: vocabulary extraction, synthesis, and evidence-linked explanation.
</logic-type>

<process>
1. Resolve the target scope and output path.
2. Read relevant source material such as requirements, design docs, UI docs, state docs, operation docs, interface docs, tests, decisions, and existing glossary files.
3. Extract candidate terms from:
   - repeated words with local meaning,
   - formal concept tables or schemas,
   - UI labels and workflow states,
   - policies and constraints,
   - domain-specific nouns and verbs.
4. Separate candidates into:
   - plain-language feature terms,
   - formal concepts,
   - cross-scope terms,
   - unresolved terms.
5. Write plain-language definitions that teach the term in this scope.
6. Write formal concept rows only when source evidence supports them.
7. Link each definition to its source evidence.
8. Do not introduce new behavior in the glossary; if behavior is missing, report a source-doc gap.
9. Detect duplicate terms, conflicting definitions, missing sources, and stale anchors.
10. Summarize glossary coverage and unresolved terms.
</process>

<quality-bar>
A successful execution must:

- define important local terms before formal concepts,
- keep definitions explanatory and non-normative,
- link definitions to source evidence,
- avoid inventing behavior,
- identify duplicate or conflicting terms,
- report unresolved vocabulary gaps,
- keep the glossary concise enough to read.
</quality-bar>

<anti-patterns>
Avoid:

- turning the glossary into the authority source for behavior,
- copying source tables without explanation,
- defining every common word regardless of relevance,
- hiding missing source decisions behind vague definitions,
- mixing global definitions governance into a feature glossary,
- leaving terms without evidence links.
</anti-patterns>

<output-contract>
Return:

```markdown
## Feature Glossary Result

- Scope: <scope>
- Output: <path>
- Plain-language terms: <count>
- Formal concepts: <count>
- Cross-scope terms: <count>
- Unresolved terms: <count>
- Validation: <checks performed>
- Follow-up: <source gaps or none>
```
</output-contract>
````
