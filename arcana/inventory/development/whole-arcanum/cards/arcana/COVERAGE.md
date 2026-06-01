---
module: inventory-whole-arcanum
slice: whole-arcanum.arcana
swu: SWU-WAI-008
status: candidate
updatedAt: 2026-06-01
docType: coverage-report
---

# Coverage Report: Arcana Capability Family

## Captured

This slice captures high-value `arcana/` capability families as clustered cards:

| Family | Representative Sources | Card |
| --- | --- | --- |
| Decision and scope governance | `decision-gate`, `scope-interview` | `inventory.card.whole-arcanum.arcana.decision-and-scope-governance` |
| Concept optimization and interview | `distill`, `structured-interview-kits` | `inventory.card.whole-arcanum.arcana.concept-optimization-and-interview` |
| Lifecycle authoring | `sigil-development`, `spellcraft` | `inventory.card.whole-arcanum.arcana.lifecycle-authoring-family` |
| Observability and reflection | `experiment-harness`, `signal-observer`, `workflow-reflect` | `inventory.card.whole-arcanum.arcana.observability-reflection-family` |
| Knowledge and resilience | `ontology-vault`, `architecture-pattern-inventory`, `residuality-spec` | `inventory.card.whole-arcanum.arcana.knowledge-and-resilience-family` |

## Intentional Omissions

The slice does not create one card per `arcana/` package yet. The following
packages are covered only indirectly or left for a later deeper slice:

- `constitution-governance`, already represented in the W1 governance slice.
- `definitions-governance`, likely belongs in a deeper knowledge-governance
  expansion beside `ontology-vault`.
- `inventory`, already represented in the Inventory self-slice.
- `invoke-example-runner`, likely belongs with experiment/runtime evidence.
- `robot-talks`, likely belongs with later multi-agent research and conflict
  surfacing cards.
- `sigil-runtime-installer`, `skill-decomposer`, `skill-transcriptor`, and
  `x-ray`, which need separate cards only when a concrete implementation query
  needs their exact contracts.

## Duplicate And Ownership Risks

| Risk | Status | Handling |
| --- | --- | --- |
| `experiment-harness` appears in both lifecycle and observability contexts. | expected overlap | Indexed as observability in this slice; lifecycle cards cite it only as a closure dependency. |
| `distill`, `refine`, and `structured-interview-kits` can all appear before execution. | expected overlap | This slice captures `distill` plus interview routing; the existing lifecycle slice keeps `refine` authority. |
| Governance concepts can overlap with W1 Artifact Constitution and Schema Constitution cards. | managed | This slice routes decisions and scope; W1 governance cards remain source-policy/schema authority references. |
| Spell and sigil lifecycle ownership can be confused with Task Session execution. | managed | The lifecycle authoring card explicitly keeps runtime execution evidence separate from reusable-behavior validation. |

## Validation Surface

Run:

```bash
bash arcana/inventory/scripts/validate-evidence-card-slice.sh arcana/inventory/development/whole-arcanum/cards/arcana
```

Expected result: `RESULT: pass`.
