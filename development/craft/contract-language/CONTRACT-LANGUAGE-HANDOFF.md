# Contract Language Handoff

Mode: invoke handoff
Handoff type: new-lifecycle-thread
Phase status: pass
Date: 2026-06-08
Target folder: `development/craft/contract-language/`
Context Builder coverage: pass

## New Project Intent

Create a new formal language for writing contracts that can be validated.

The language should grow from Craft's distinction:

- contract: behavior, ownership, methods, invariants, gates, boundaries, and
  lifecycle meaning;
- schema: shape, row families, fields, enums, references, and validation rules;
- iteration: examples, validation, residue, recomposition, and versioned repair.

The first lifecycle should define the language before any parser, validator,
runtime, sigil, or spell implementation.

## Source Session Reference

Source artifacts are local repository artifacts from the Craft interface and
interaction work in `development/craft/`.

Context Builder selected evidence:

- `development/craft/contract-language/CONTEXT-PACK.md`
- `development/craft/contract-language/context-index.json`

## Route Rationale

This is a `new-lifecycle-thread` because it is a related idea that emerged from
Craft but needs its own define/design/plan lifecycle.

Recommended next route:

```text
invoke define development/craft/contract-language/CONTRACT-LANGUAGE-HANDOFF.md
```

Do not start with implementation. The first output should be a definition
baseline for the language: purpose, users, contract concepts, schema concepts,
validation semantics, examples, non-goals, and open decisions.

## Context Builder Selection Summary

Files selected: 10.

Obligation coverage: 100%.

Strict coverage: pass.

Selected context focuses on:

- Craft interface contract as behavioral authority;
- Craft interface schema as structural authority;
- Craft interaction contract as owner-boundary authority;
- Craft interaction schema as handoff/receipt/route-event shape;
- examples that show contract plus schema in use;
- validation guides that show how contract claims can be checked;
- Dispatch Spec schema as an existing validateable Arcanum route language;
- Invoke Handoff mode as the correct split-thread pattern.

## Starting Questions For Define

1. What is the smallest useful unit in the new language: a method contract, an
   interaction contract, a lifecycle contract, or a generic contract block?
2. Should the language be YAML-native, Markdown with structured blocks, or a DSL
   that compiles to YAML/JSON?
3. What does a validateable contract require beyond schema validation?
4. How should contract examples prove behavior, not just field shape?
5. What is the first validation target: completeness, consistency, executable
   checks, or owner-boundary safety?

## Required Definition Outputs

The next `invoke define` pass should create:

- a language purpose statement;
- a glossary for contract/schema/iteration terms;
- a source-contract register;
- a minimal language concept model;
- examples of valid and invalid contract fragments;
- validation vocabulary: `pass`, `flag`, `block`, `deferred`, `waived`;
- non-goals and deferred implementation choices;
- blocker decisions for syntax shape and validator target.

## Non-Goals For The Next Thread

- Do not implement a parser yet.
- Do not choose runtime integration yet.
- Do not promote the language as a sigil or spell yet.
- Do not mutate Craft's existing contract/schema artifacts except by explicit
  later refresh.
- Do not treat examples as canonical until the define/design lifecycle validates
  them.

## Gaps And Blockers

Current blockers: none for starting `invoke define`.

Open definition-stage gaps:

- grammar choice is unresolved;
- parser/validator implementation route is unresolved;
- canonical contract schema does not exist;
- relationship to Dispatch Spec schema should be studied but not copied blindly;
- whether contracts compile to schemas or schemas validate contracts is still an
  open design question.

## Next Session Start Prompt

```text
We are starting development/craft/contract-language as a new lifecycle thread.
Use CONTRACT-LANGUAGE-HANDOFF.md, CONTEXT-PACK.md, and context-index.json.
Run invoke define for a new formal language for writing validateable contracts.
The language should distinguish contract behavior from schema shape and include
iteration through examples, validation, residue, and recomposition. Do not
implement a parser yet; produce the definition baseline and open decisions.
```

## Output Paths

- Handoff: `development/craft/contract-language/CONTRACT-LANGUAGE-HANDOFF.md`
- Context pack: `development/craft/contract-language/CONTEXT-PACK.md`
- Context index: `development/craft/contract-language/context-index.json`
