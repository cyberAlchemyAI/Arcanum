---
name: guide-architecture
description: "Guide a user through a software architecture target by composing context selection, structure inspection, optional translation, explanation sequencing, active-understanding validation, and User-ledger update proposals."
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: spells/guide-architecture/README.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
---

# Guide Architecture

## Identity

- Canonical ID: `guide-architecture`
- Aliases: `guide architecture`, `/guide this architecture`
- Scope: library
- Lifecycle owner: `spellcraft`
- Status: candidate

## Purpose

Guide a user through a software architecture target by composing context selection, structure inspection, optional translation, explanation sequencing, active-understanding validation, and User-ledger update proposals.

This spell is the first narrow slice of the broader Guide family. It is intentionally architecture-specific so it can be validated before generalizing to a generic `guide` spell.

## Source Handoff

| Source | Role |
| --- | --- |
| `development/user-guide/packages/guide/SPELLCRAFT-HANDOFF.md` | Approved spellcraft handoff selecting `guide-architecture`. |
| `development/user-guide/packages/guide/GUIDE-ROUTE-FIXTURE.md` | Static route fixture for `/guide this architecture`. |
| `development/user-guide/packages/guide/DISPATCH-GOVERNANCE.md` | Dispatch budget and stop-condition seed. |
| `development/user-guide/packages/translate/GUIDE-CALL-CONTRACT.md` | Translate call boundary. |
| `development/user-guide/packages/user-ledger/USER-LEDGER-SCHEMA.yml` | User-ledger handle and receipt boundary. |

## Trigger Conditions

Use this spell when:

- the user asks to understand a software architecture, architecture decision, dependency boundary, system structure, or design trade-off,
- the target is an artifact, code area, diagram, decision note, work-pack, or architecture package,
- the user wants explanation rather than implementation,
- vocabulary/domain translation may help understanding,
- a guide receipt should propose User-ledger updates after clarification.

Do not use this spell when:

- the user asks for code mutation or task execution,
- the target is not architecture-shaped,
- the request needs broad learning design rather than one architecture guide route,
- the user asks for canonical definition promotion.

## Required Sigils

| Sigil / Capability | Status | Role |
| --- | --- | --- |
| `context-builder` | canonical | Select bounded target context and source anchors. |
| `x-ray` | canonical | Explain hidden architecture structure when needed. |
| `inventory` | canonical | Look up existing concept, artifact, or architecture evidence when needed. |
| `decision-gate` | canonical | Resolve blocker-level choices such as unsafe route breadth or missing target scope. |
| `user-ledger` | local candidate | Provide user handles and receive update proposals. |
| `translate` | local candidate | Map architecture concepts into a source-domain vocabulary while preserving target truth. |

## Optional Sigils

| Sigil / Capability | Use When |
| --- | --- |
| `architecture-pattern-inventory` | Reusable architecture patterns or relations need lookup. |
| `task-session` | A later approved work-pack asks to execute a bounded Guide implementation task. |
| `experiment-harness` | Reusable prompt fixtures or live validation examples are run. |
| `signal-observer` | Spell-level run telemetry should be recorded. |
| `workflow-reflect` | Repeated Guide telemetry suggests workflow revisions. |

## Prerequisites

- Target architecture artifact or bounded repository area.
- Context Builder can select source context or name the missing target scope.
- User-ledger fixture handles exist or the route can proceed with no user handles.
- Translate contract exists when a vocabulary/domain bridge is needed.
- No live research or subagent dispatch occurs unless dispatch budget and stop conditions are explicit.

## Shared State

| State | Owner | Updated By | Consumed By |
| --- | --- | --- | --- |
| Guide route frame | `guide-architecture` | phase 1 | all later phases |
| Architecture context pack | `context-builder` | phase 2 | x-ray, translate, explanation assembly |
| Structure notes | `x-ray` or local inspection | phase 2 | explanation assembly |
| Translation receipt | `translate` | phase 3 | guide receipt and explanation assembly |
| User handles and update proposals | `user-ledger` | read in phase 1; proposed in phase 6 | translate and future guide sessions |
| Guide receipt | `guide-architecture` | phase 6 | user-ledger and observability |

## Execution Phases

### Phase 1: Frame Target And User Goal

Input:

- user request,
- target artifact or target scope,
- optional user handles.

Output:

- guide request frame with `target_ref`, `target_type`, `user_goal`, and known handles.

Gate:

- Block if no architecture target or target scope can be identified.

Failure policy:

- Ask for the target artifact or return a route menu: architecture artifact, repo area, decision note, or diagram.

### Phase 2: Select Context And Inspect Architecture

Input:

- guide request frame,
- target artifact/scope.

Output:

- bounded context pack,
- structure notes: boundaries, dependencies, data, behavior, failure modes, and open uncertainties.

Gate:

- Block when context is missing or contradictory.
- Flag when structure is inspectable but incomplete.

Failure policy:

- Route to `context-builder` or `x-ray`; preserve missing context as residue rather than inventing structure.

### Phase 3: Translate When Needed

Input:

- structure notes,
- user handles,
- target concept.

Output:

- Translate request and optional Translate receipt.

Gate:

- Translate must include target-domain definition and mapping limits.
- Translate must return `research_need` rather than dispatching research itself.

Failure policy:

- If Translate is unavailable, continue with target-domain plain explanation and record a translation gap.

### Phase 4: Assemble Guide Explanation

Input:

- structure notes,
- optional translation receipt,
- target-domain definitions.

Output:

- ordered guide sections:
  1. concrete frame,
  2. structure map,
  3. target-domain definition,
  4. mapping limits,
  5. system-thinking abstraction,
  6. next reasoning move.

Gate:

- Do not hide uncertainty or omit mapping limits.

Failure policy:

- Return a flagged explanation with explicit unresolved gaps.

### Phase 5: Validate Understanding

Input:

- guide explanation.

Output:

- active evidence prompt.

Gate:

- Passive "I understand" can only support `clarified`, not `mastered`.

Failure policy:

- If the user declines active evidence, emit a clarified-only receipt proposal.

### Phase 6: Emit Guide Receipt

Input:

- route frame,
- explanation sections,
- validation response status,
- translation receipt.

Output:

- Guide receipt with proposed User-ledger update.

Gate:

- User-ledger writes remain proposals unless accepted by the User-ledger owner/rules.

Failure policy:

- Record residue instead of forcing a concept-state update.

## Handoff Artifacts

- `development/user-guide/packages/guide/GUIDE-ROUTE-SCHEMA.yml`
- `development/user-guide/packages/guide/GUIDE-ROUTE-FIXTURE.md`
- `development/user-guide/packages/guide/GUIDE-TRANSLATE-INTEGRATION.md`
- `development/user-guide/packages/guide/DISPATCH-GOVERNANCE.md`
- `spells/guide-architecture/development/VALIDATION-EXPERIMENT.md`
- `spells/guide-architecture/development/VALIDATION.md`
- `spells/guide-architecture/development/fixtures/ARCHITECTURE-BOUNDARY-GUIDE.md`

## Gates

| Gate ID | Condition | On Fail |
| --- | --- | --- |
| GA-G01 | Target scope is architecture-shaped and bounded. | block |
| GA-G02 | Context selection cites source artifacts or explicitly flags missing context. | block |
| GA-G03 | Translate output preserves target-domain definition and mapping limits. | flag |
| GA-G04 | No live research/subagent dispatch without explicit budget and stop conditions. | block |
| GA-G05 | User-ledger update remains a proposal, not a direct write. | block |
| GA-G06 | Mastery requires active evidence. | flag |

## Failure Policy

- Missing target: block and ask for target scope.
- Missing context: block before explanation.
- Missing Translate capability: flag and continue only with target-domain explanation.
- Unsafe analogy: flag and preserve target-domain definition.
- User memory write attempted directly: block.
- Runtime dispatch requested without budget: block.

## Local Customization

This library spell currently references `user-ledger` and `translate` as local candidate packages under `development/user-guide/packages/`. When those candidates become canonical sigils, update this spell to reference their canonical IDs.

## Observability

Record spell-level telemetry when available:

- target type,
- context source count,
- phases attempted,
- Translate called or skipped,
- x-ray/inventory called or skipped,
- gates passed/flagged/blocked,
- guide receipt emitted,
- user-ledger proposal emitted,
- validation prompt outcome,
- unresolved residue.

## Output Contract

Return:

```markdown
## Guide Architecture Result

- Spell: guide-architecture
- Target: <artifact or scope>
- Status: pass | flag | block
- Context: <context pack or blocked reason>
- Translate: <called | skipped | unavailable | flagged>
- Explanation sections: <count>
- Active evidence prompt: <prompt or none>
- Guide receipt: <path or summary>
- User-ledger proposal: <summary or none>
- Residue: <items or none>
- Next route: continue | translate | user-ledger | task-session | decision-gate | stop
```
