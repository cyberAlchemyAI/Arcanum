---
module: inventory-whole-arcanum
slice: whole-arcanum.composition
swu: SWU-WAI-009
status: candidate
updatedAt: 2026-06-01
docType: coverage-report
---

# Coverage Report: Composition Families

## Captured

This slice captures high-value composition surfaces across spells,
transmutations, and formulae:

| Family | Representative Sources | Card |
| --- | --- | --- |
| Authoring front door | `spells/invoke/README.md` | `inventory.card.whole-arcanum.composition.invoke-authoring-front-door` |
| Repository setup and telemetry loop | `arcanum-bootstrap`, `repository-harness`, `observed-invocation-loop` | `inventory.card.whole-arcanum.composition.repository-install-and-harness` |
| Discovery and readiness spell flow | `discovery-to-inventory`, `implementation-readiness` | `inventory.card.whole-arcanum.composition.discovery-and-readiness-spells` |
| Evidence-to-artifact transmutations | `context-builder`, `implementation-layering`, `codex-goal-profile`, `feature-glossary` | `inventory.card.whole-arcanum.composition.transmutation-context-and-planning` |
| Deterministic formulae support | `dispatch-spec`, `observability-setup` | `inventory.card.whole-arcanum.composition.formulae-validation-and-setup` |

## Intentional Omissions

This slice does not capture every composition artifact:

- `guide-architecture`, `ontology-harness`, `sigil-maintenance-loop`, and
  `whisper` are left for later focused slices because they are either narrower
  domain workflows or need their own lifecycle context.
- `necronomicon` is omitted from this slice because its current role crosses
  repository memory and routing; it should be indexed with runtime or governance
  support after its authority boundary is rechecked.
- Development fixtures and generated example outputs are excluded by the source
  policy unless promoted by a nearby readiness or validation artifact.

## Duplicate And Ownership Risks

| Risk | Status | Handling |
| --- | --- | --- |
| `context-builder` appears as both a required Task Session dependency and a transmutation. | expected overlap | Composition card indexes conversion role; Task Session remains the execution gate. |
| `observability-setup` and `observed-invocation-loop` both touch telemetry. | managed | Formulae card covers package setup; spell card covers managed invocation flow. |
| `invoke` can route to `task-session`, `spellcraft`, or `sigil-development`. | managed | Invoke card records handoff behavior and does not claim lifecycle completion. |
| `codex-goal-profile` may look like runtime execution. | managed | Transmutation card records goal-profile synthesis only; native Codex owns goal runtime. |

## Validation Surface

Run:

```bash
bash arcana/inventory/scripts/validate-evidence-card-slice.sh arcana/inventory/development/whole-arcanum/cards/composition
```

Expected result: `RESULT: pass`.

