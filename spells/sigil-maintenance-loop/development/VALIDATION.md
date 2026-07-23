# Sigil Maintenance Loop Validation

Date: 2026-07-22
Status: pass
Lifecycle owner: `spellcraft`

## Checks

| Check | Evidence | Result |
| --- | --- | --- |
| Spellcraft contract completeness | Canonical README defines identity, purpose, triggers, required and optional sigils, inputs, prerequisites, shared state, authority boundaries, handoffs, phases, gates, failure policy, local customization, observability, experiment harness, output contract, Quality Bar, and Anti-Patterns. | pass |
| Referenced sigils | Required `inventory`, `signal-observer`, `workflow-reflect`, and `sigil-development` plus optional `experiment-harness` and `observability-setup` resolve in Arcanum. | pass |
| Inventory-first boundary | Phase 1 is unconditional, reads `index.json` first, emits a named lookup packet, asks no extra permission for read-only lookup, and forbids implicit Inventory mutation modes. | pass |
| File-backed scenarios | `development/validate-scenarios.sh` checks relevant match, no match, `index.md` fallback, unavailable Inventory, insufficient signal, and rejected approval. | pass; 6/6 |
| Experiment profile | `spellcraft` profile metadata, four prompts, four regimes, and fixture pairs validate. | pass |
| Native examples | Design, install/adapt, validate, and reflect result bodies are non-empty, contract-shaped, and not save summaries. | pass; 4/4 |
| Timestamped report | Final report `development/runs/20260722T061232Z.md`. | pass |
| Generated runtime mirrors | Isolated bootstrap generation produced Codex and Claude packages whose bodies match the canonical README exactly. | pass; 2/2 |
| Documentation and publication boundary | Markdown links, diff checks, and private-path/email scans over the public spell and registry. | pass |

## Commands

```bash
bash -n arcanum/spells/sigil-maintenance-loop/development/*.sh
bash arcanum/spells/sigil-maintenance-loop/development/run-validation-fixtures.sh
```

The final harness result is `VALIDATION=pass`,
`PROFILE_VALIDATION=pass`, and `SCENARIO_VALIDATION=pass`.

## Known Harness Limitation

The generic `check-contract-output.sh` currently extracts XML-style Quality Bar
and Anti-Pattern sections only from a target `SKILL.md`. Library spells use a
canonical `README.md`, so its aggregate field reports
`QUALITY_BAR_STATUS=not_checked` even though the Spellcraft review and scenario
checks above evaluate the spell contract. This limitation is reported rather
than promoted into false machine-checked evidence.

## Promotion Boundary

This validation supports the Inventory-first maintenance-loop revision and its
generated runtime mirrors. It does not promote Inventory matches into sigil
authority, waive explicit mutation approval, or authorize silent Inventory
installation or mutation.
