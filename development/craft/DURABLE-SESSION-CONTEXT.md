# Craft Development Durable Session Context

## Purpose

This session is dedicated to developing `Craft` as a method primitive and candidate Arcanum/CyberAlchemy capability.

Use this file as the durable baseline for future work in this thread or for new handoff threads that continue Craft development. The session should stay scoped to turning the initial Craft definition into a governed, usable development method with clear lifecycle phases, route boundaries, artifact contracts, validation gates, and promotion criteria.

## Scope Boundary

In scope:

- `development/craft/`
- Craft as an outer method for schema/data translation, residue handling, SCU/SWU selection, validation, reflection, and recomposition
- Craft's relationship to existing Arcanum capabilities such as `invoke`, `refine`, `distill`, `context-builder`, `task-session`, `workflow-reflect`, `signal-observer`, `sigil-development`, and `spellcraft`
- candidate artifacts that clarify Craft's method, glossary, lifecycle, architecture, work-pack, examples, or promotion path
- source evidence from Arcanum, DomainSpec, and CyberAlchemy only when it helps bound or validate Craft

Out of scope unless explicitly routed through a separate handoff:

- mutating canonical Arcanum sigils, spells, commands, registry entries, runtime adapters, or observability hooks
- promoting Craft as canonical method authority
- renaming existing capabilities to Craft-owned names
- implementing unrelated runtime behavior
- rewriting the initial definition for style alone
- converting philosophical horizon material into operational authority before validation

## Current Session Decision

This chat should contain only Craft development work.

If a related but separate idea appears, create a handoff artifact instead of expanding this session. The handoff should include:

- the user's new-session prompt,
- the source session reference,
- the target lifecycle owner,
- selected source context,
- excluded context,
- target boundary,
- next route.

## Active Development Focus

Current focus:

- preserve the initial Craft definition as source evidence,
- turn Craft from concept into a session-governed development method,
- separate operational method claims from philosophical horizon claims,
- define the first durable artifact set needed for future Craft development,
- identify the next smallest coherent unit for Craft work,
- keep Craft as a composing method rather than a replacement for existing Arcanum lifecycle authorities.

## Relevant Context Pack

Primary source artifact:

- [CRAFT-INITIAL-DEFINITION.md](CRAFT-INITIAL-DEFINITION.md)

Primary local method references:

- [../../framework/CYBERALCHEMY-METHOD.md](../../framework/CYBERALCHEMY-METHOD.md)
- [../../arcana/distill/README.md](../../arcana/distill/README.md)
- [../../arcana/refine/REFINEMENT-LOOP.md](../../arcana/refine/REFINEMENT-LOOP.md)
- [../../spells/invoke/README.md](../../spells/invoke/README.md)
- [../../arcana/task-session/README.md](../../arcana/task-session/README.md)
- [../../arcana/task-session/SKILL.md](../../arcana/task-session/SKILL.md)

Session artifacts:

- [SESSION-LEDGER.md](SESSION-LEDGER.md)
- [README.md](README.md)

## Operating Rules

1. Treat Craft as candidate development method until explicit promotion.
2. Keep canonical method, sigil, spell, registry, command, and runtime changes outside this session unless a later task explicitly approves them.
3. Preserve the initial definition as evidence; create derived artifacts instead of repeatedly rewriting the source definition.
4. Separate four layers in every artifact: concept, method contract, route integration, and promotion readiness.
5. Do not let Craft absorb specialist authorities. Craft may route to `invoke`, `refine`, `distill`, `task-session`, `spellcraft`, or `sigil-development`; it does not replace them.
6. Use SCU/SWU reasoning before execution: every concrete next move needs inputs, outputs, validation, failure behavior, and recomposition path.
7. Classify residue explicitly before deciding whether to repair locally, split the layer, route to another capability, or ask for a human decision.
8. Keep philosophical claims as horizon material unless they can be translated into an operational rule, test, example, or decision gate.

## Initial Session State

| Field | Value |
| --- | --- |
| Target | Craft |
| Stage | start / define-to-design transition |
| Status | active candidate development session |
| Source baseline | `CRAFT-INITIAL-DEFINITION.md` |
| Current artifact gap | no durable session scaffolding, no method architecture, no work-pack |
| Current next route | build a Craft development work-pack or architecture package |
| Promotion status | not canonical, not approved for registry or command mutation |

## First SCU

Recommended first smallest coherent unit:

```text
Create the Craft method architecture package under development/craft/.
```

Inputs:

- `CRAFT-INITIAL-DEFINITION.md`
- this durable session context
- existing Arcanum method references listed above

Outputs:

- Craft method architecture
- Craft glossary
- Craft lifecycle contract
- route integration map
- validation and promotion gates
- implementation or documentation work-pack

Validation:

- all operational claims trace to source evidence or are marked candidate,
- Craft does not replace existing lifecycle authorities,
- each lifecycle phase has input, output, gate, failure behavior, and recomposition path,
- residue handling rules are actionable,
- next tasks are bounded enough for `task-session`.

## Open Decisions

| Decision | Current Recommendation | Status |
| --- | --- | --- |
| Should Craft become an Arcanum sigil, spell, framework chapter, or cross-cutting method? | Defer until architecture package compares authority and route fit. | open |
| Should Craft own a runtime command? | No until method contract, examples, and validation pass. | deferred |
| Should Craft absorb `invoke`, `refine`, or `distill` behavior? | No. Craft should route to them. | candidate rule |
| Should philosophical horizon claims affect operational gates? | Only after translation into testable method rules. | candidate rule |

## Latest Verification

Review performed:

- confirmed `development/craft/` contains only the initial definition artifacts before session setup,
- read the initial definition's core model, lifecycle, residue classification, route map, stop criteria, and formal model,
- compared durable-session shape against existing ontology-vault durable session precedent,
- noted a dirty worktree with many unrelated existing changes and left them untouched.

## Durable Handoff Note

When resuming this session, start from this file, then inspect the current git diff for `development/craft/` only.

Suggested resume prompt:

```text
Continue the durable Craft development session. Use development/craft/DURABLE-SESSION-CONTEXT.md as the scope boundary. Focus only on Craft method development unless a separate idea is explicitly routed through a handoff.
```
