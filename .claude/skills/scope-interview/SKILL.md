---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/scope-interview/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: scope-interview
description: "Use when: interviewing a greenfield idea, brownfield repository, or mixed project scope into a structured discovery baseline."
argument-hint: "[greenfield|brownfield|auto] <project-or-scope> [--output <folder>]"
tier: arcana
domain: scope-discovery
version: 0.1.0
origin: generalized from recurring project discovery interview practice
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
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
