---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: transmutations/feature-glossary/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
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
