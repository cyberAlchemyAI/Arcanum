# Task CRAFT-ARCH-002: Create Validation Example Suite

## Objective

Create a minimal Craft validation example suite that proves the architecture's required method claims through source-backed examples.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L1 |
| Slice | S-ARCH-002 |
| Wave | W1 |
| Complexity | medium |

## Source Contracts

- `development/craft/CRAFT-ARCHITECTURE.md#Validation Example-Suite Shape`
- `development/craft/CRAFT-GLOSSARY.md`
- `development/craft/LEDGER.md`
- `development/craft/LEDGER-VALIDATION.md`
- `development/craft/CRAFT-LEDGER-TYPE-SYSTEM.md`
- `development/craft/CRAFT-ARCHITECTURE-INPUTS.md`
- `development/craft/CRAFT-REFINE-RUNTIME-STRATEGY.md`
- `development/craft/ARCANUM-SKILL-RUNTIME-HANDOFF.md`

## Dependencies

- CRAFT-ARCH-001 must pass.

## Implementation Detail

Create two companion artifacts:

- `development/craft/CRAFT-VALIDATION-EXAMPLES.yml`
- `development/craft/CRAFT-VALIDATION-EXAMPLES.md`

The YAML should be the structured authority. The Markdown should be the readable walkthrough. Keep both local and candidate.

Suggested YAML shape:

```yaml
examples:
  - id: EX-001
    claim: scu_selection
    source_contracts: []
    scenario: ""
    expected_behavior: ""
    validation_evidence: ""
    recomposition_target: ""
    status: candidate
```

## Smallest Working Units

### SWU-CRAFT-ARCH-002

Goal: create examples EX-001 through EX-004 for SCU selection, SWU planning, residue classification, and recomposition.

Dependencies: SWU-CRAFT-ARCH-001.

Write scope:

- `development/craft/CRAFT-VALIDATION-EXAMPLES.yml`
- `development/craft/CRAFT-VALIDATION-EXAMPLES.md`

Done criteria:

- EX-001 proves SCU selection from broad intent.
- EX-002 proves SWU planning from approved design.
- EX-003 proves residue classification after validation.
- EX-004 proves recomposition after child-unit completion.
- Each example has source contracts, expected behavior, validation evidence, and recomposition target.

Acceptance evidence:

- YAML parses.
- Markdown names the same EX IDs.

Validation surface:

- `python3 - <<'PY'` YAML parse check using available standard library or local parser if present.
- Manual coverage review against `CRAFT-ARCHITECTURE.md`.

Execution owner: subagent.

Handoff note:

Focus on core method behavior before ledger-specific or runtime-boundary examples.

### SWU-CRAFT-ARCH-003

Goal: add examples EX-005 through EX-007 for blocker refinement, cross-context relation behavior, and route boundary behavior.

Dependencies: SWU-CRAFT-ARCH-002.

Write scope:

- `development/craft/CRAFT-VALIDATION-EXAMPLES.yml`
- `development/craft/CRAFT-VALIDATION-EXAMPLES.md`

Done criteria:

- EX-005 proves raw blocker refinement before resolution.
- EX-006 proves cross-context blocker or enabler representation.
- EX-007 proves Craft calls existing Arcanum routes without replacing them.
- Examples cite ledger/type-system evidence where applicable.

Acceptance evidence:

- YAML parses.
- Markdown remains synchronized with YAML.

Validation surface:

- YAML parse check.
- Manual coverage review against `LEDGER.md`, `LEDGER-VALIDATION.md`, and route boundary table.

Execution owner: subagent.

Handoff note:

Reuse the validated recursive-ledger MVP evidence. Do not invent new runtime behavior.

### SWU-CRAFT-ARCH-004

Goal: add examples EX-008 through EX-010 for runtime side-thread boundary, promotion decision, and type plus lane role-hint review.

Dependencies: SWU-CRAFT-ARCH-003.

Write scope:

- `development/craft/CRAFT-VALIDATION-EXAMPLES.yml`
- `development/craft/CRAFT-VALIDATION-EXAMPLES.md`

Done criteria:

- EX-008 proves runtime/interface gaps remain external and non-blocking.
- EX-009 proves local validation leads to explicit promotion review, not automatic promotion.
- EX-010 proves role hints are manually reviewable before automation.
- Deferred automation and runtime terms remain deferred.

Acceptance evidence:

- YAML parses.
- Markdown remains synchronized with YAML.

Validation surface:

- YAML parse check.
- Manual review against `CRAFT-ARCHITECTURE-INPUTS.md` and side-thread artifacts.

Execution owner: subagent.

Handoff note:

These examples should prevent future overreach: no runtime mutation, no promotion mutation, no role delegation automation.

## Synchronization Rules

After this task, do not update README or SESSION-LEDGER yet. Those sync in CRAFT-ARCH-005 after validation and readiness review.
