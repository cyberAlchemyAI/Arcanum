# Craft Architecture Implementation Layering

## Purpose

Define the decision-first layer model for turning `CRAFT-ARCHITECTURE.md` into validated Craft method evidence without promoting Craft or mutating runtime surfaces.

This is an Invoke plan companion. It does not execute tasks, edit runtime commands, update registries, or promote glossary terms.

## Source Contract

| Source | Use |
| --- | --- |
| `CRAFT-ARCHITECTURE.md` | Approved six-view Craft method architecture and next planning source. |
| `CRAFT-ARCHITECTURE-GLOSSARY-CONSISTENCY.md` | Vocabulary consistency gate. |
| `CRAFT-ARCHITECTURE-DESIGN-TRANSPORT.md` | Design transport and planning obligations. |
| `CRAFT-ARCHITECTURE-INPUTS.md` | Architecture-owned acceptance questions and runtime boundary rules. |
| `CRAFT-GLOSSARY.md` | Candidate local vocabulary. |
| `LEDGER.md` and `LEDGER-VALIDATION.md` | MVP evidence for recursive ledger and blocker lifecycle behavior. |

## Target And Scope

| Field | Value |
| --- | --- |
| Target | Craft method architecture hardening |
| Scope | process/method capability |
| Current state | architecture-approved candidate |
| Execution boundary | documentation, examples, validation reports, package state sync |
| Excluded scope | runtime adapters, command routes, registries, sigils, spells, canonical promotion, scoring automation, generated index automation, role delegation automation |

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether the architecture can be carried into an executable plan without losing source contracts or boundaries. | Planning baseline and traceability review. | Confirm architecture bundle, companion reports, source contracts, and side-thread boundaries. | Creating validation examples and package sync. | `CRAFT-ARCHITECTURE-WORK-PACK.md`, `CRAFT-ARCHITECTURE-EXECUTION-PACK.md`, and task contracts exist. | Continue to example-suite build or block on missing contract. |
| L1 | After this layer, we know whether Craft's method claims can be shown through a minimal validation example suite. | Example suite covering SCU, SWU, residue, recomposition, blocker refinement, route boundary, runtime boundary, promotion, and role-hint review. | Create `CRAFT-VALIDATION-EXAMPLES.yml` and a readable companion. | Automated validators and promotion. | Example suite maps every architecture-required example to source anchors and expected evidence. | Harden validation or narrow claims. |
| L2 | After this layer, we know whether validation and recomposition rules are reviewable enough for repeated task-session execution. | Validation guide and manual checklist. | Create `CRAFT-VALIDATION.md`, checklist rules, evidence expectations, and recomposition gate. | Generated indexes, scoring, and role automation. | Manual validation report can pass/fail the examples without reopening architecture discovery. | Prepare readiness review or remediate gaps. |
| L3 | After this layer, we know whether Craft is ready for a promotion decision or should stay local. | Promotion readiness review and package state sync. | Create readiness report, sync README/session ledger, and name next route. | Actual promotion and runtime integration. | `CRAFT-PROMOTION-READINESS.md` and package state agree on promote/defer/stay-local recommendation. | Route to promotion review, further examples, or deferred maintenance. |

## Non Regression Guardrails

- Later layers must preserve source-contract traceability from `CRAFT-ARCHITECTURE.md`.
- Validation examples must not redefine Craft terms outside `CRAFT-GLOSSARY.md`.
- Runtime/interface gaps stay external unless their owner thread explicitly returns accepted artifacts.
- Automation terms remain evidence-gated; no scoring, index, or role delegation implementation is included.
- Promotion requires an explicit future decision; local pass evidence is not promotion.

## Recommended Next Layer

| Field | Value |
| --- | --- |
| Next layer | L0 |
| Key decision unlocked | Whether the architecture package is executable by task-session/SWU without reopening design. |
| Major deferred scope | Runtime integration, canonical promotion, scoring, generated indexes, role delegation automation. |
