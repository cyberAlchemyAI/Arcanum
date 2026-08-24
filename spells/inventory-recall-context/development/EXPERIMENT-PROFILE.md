# Experiment Profile

- Profile ID: spellcraft
- Artifact type: spell
- Lifecycle owner: spellcraft
- Artifact path: spells/inventory-recall-context
- Contract path: spells/inventory-recall-context/README.md
- Scenario pack: spellcraft-lifecycle
- Required modes: design, install/adapt, validate, observe/reflect
- Prompt set: spellcraft-design-low, spellcraft-install-medium, spellcraft-validate-complex, spellcraft-reflect-complex
- Regime set: LIVE-SPELLCRAFT-DESIGN-001, LIVE-SPELLCRAFT-INSTALL-001, LIVE-SPELLCRAFT-VALIDATE-001, LIVE-SPELLCRAFT-REFLECT-001
- L0 scenario pack: inventory-recall-context-l0 (positive plus six fail-closed controls)
- Validation focus: Spellcraft output contract is represented; aliases resolve to stable canonical ids; referenced sigils remain references; local adaptation does not rewrite upstream contracts; validation produces a clear next action
- Observability focus: spell lifecycle evidence; install/adapt boundary; validation status; reflection recommendation
- Promotion gate: lifecycle owner review
- Current evidence ceiling: initialized candidate harness; no live runtime output or reusable-behavior proof

## Ownership Boundary

Experiment Harness owns experiment mechanics. The lifecycle owner owns artifact meaning and promotion judgment.
