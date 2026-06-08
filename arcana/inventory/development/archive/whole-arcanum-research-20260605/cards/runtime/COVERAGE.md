---
module: inventory-whole-arcanum
slice: whole-arcanum.runtime
swu: SWU-WAI-010
status: candidate
updatedAt: 2026-06-01
docType: coverage-report
---

# Coverage Report: Runtime And Governance Support

## Captured

This slice captures high-value runtime and governance support surfaces:

| Family | Representative Sources | Card |
| --- | --- | --- |
| Artifact classification and validation | `framework/ARTIFACT-CONSTITUTION.md` | `inventory.card.whole-arcanum.runtime.artifact-constitution-boundary` |
| Durable runtime and adapters | `framework/runtime/README.md` | `inventory.card.whole-arcanum.runtime.durable-runtime-handoff` |
| Observability support | `framework/observability/README.md` | `inventory.card.whole-arcanum.runtime.observability-support` |
| Registry navigation | `registry/SIGILS.md` | `inventory.card.whole-arcanum.runtime.registry-navigation` |
| Native runtime and adapter boundary | `tools/arcanum` | `inventory.card.whole-arcanum.runtime.command-surface` |

## Intentional Omissions

This slice does not capture every file under the runtime families:

- Individual `.codex/commands/*.md` files are omitted because legacy command
  files are no longer the live runtime invocation proof. Native/generated skill
  packages and canonical source contracts own the current cross-repository test
  surface.
- Individual observability scripts are omitted because
  `framework/observability/README.md` and the observed-invocation spell cards
  already capture the operating model.
- `registry/SPELLS.md` and `registry/PACKS.md` should be added only when a query
  needs spell/package navigation beyond the sigil registry.
- `tools/bootstrap_arcanum.sh` and `tools/install_arcanum.sh` are covered
  indirectly through Arcanum Bootstrap composition cards and can receive focused
  operational cards later if installer behavior becomes the active task.

## Duplicate And Ownership Risks

| Risk | Status | Handling |
| --- | --- | --- |
| `.codex/commands` may still exist as local or cleanup-era adapter files and look authoritative. | managed | Runtime card states legacy command files are excluded from the live proof; canonical source stays in skill and spell contracts plus generated native packages. |
| `.arcanum/observability/**` exists locally but is generated telemetry. | managed | Artifact Constitution and observability cards keep ledgers/indexes excluded from source inventory. |
| Runtime adapter docs and `tools/arcanum` both describe adapter behavior. | expected overlap | Runtime docs own the conceptual model; `tools/arcanum` owns command resolution and adapter profile mechanics. |
| Registry summaries can drift from capability contracts. | managed | Registry card records maintenance rule and non-authority boundary. |

## Validation Surface

Run:

```bash
bash arcana/inventory/scripts/validate-evidence-card-slice.sh arcana/inventory/development/whole-arcanum/cards/runtime
```

Expected result: `RESULT: pass`.
