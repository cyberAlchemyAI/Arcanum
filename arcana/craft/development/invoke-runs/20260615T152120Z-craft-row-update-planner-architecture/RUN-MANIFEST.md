# Invoke Run Manifest: Craft Row Update Planner Architecture

| Field | Value |
| --- | --- |
| run_id | `20260615T152120Z-craft-row-update-planner-architecture` |
| target | `arcana/craft` |
| invoke_modes | `design` |
| status | `pass` |
| template_profile | Module Formulae architecture bundle |
| public_boundary | active |

## Outputs

| Path | Purpose |
| --- | --- |
| `INVOKE-DESIGN-ARCHITECTURE.md` | Six-view proposal architecture bundle. |
| `GLOSSARY-CONSISTENCY.md` | Term alignment and candidate-local vocabulary notes. |
| `IMPLEMENTATION-LAYERING-SEED.md` | Design-stage L0-L3 seed for later plan/task routes. |
| `DESIGN-TRANSPORT.md` | Invoke design transport and next-route handoff. |

## Source Refine Run

- `../refinement-runs/20260615T131737Z-craft-deterministic-row-updater/`

## Boundary

This public bundle must not include sensitive decision material, local
absolute paths, parent-only workspace evidence, unpublished product details, or
parent-only state. It does not mutate canonical Craft files.

## Validation

- Six required design views are present in `INVOKE-DESIGN-ARCHITECTURE.md`.
- `GLOSSARY-CONSISTENCY.md`, `IMPLEMENTATION-LAYERING-SEED.md`, and
  `DESIGN-TRANSPORT.md` are present.
- `git -C arcanum diff --check -- arcana/craft/development/invoke-runs/20260615T152120Z-craft-row-update-planner-architecture`
  passed.
