# UX Evidence Validator Work Pack

Status: seed development route.
Owner: Sigil Development.
Target sigil: `arcana/ux-evidence-validator`.

## Goal

Move the UX Playwright evidence research into a dedicated Arcana sigil and develop it toward a calibrated Playwright evidence validator for finished frontend interfaces.

## Current Evidence

| Artifact | Status |
| --- | --- |
| `README.md` | Seed contract created. |
| `SKILL.md` | Seed execution contract created. |
| `development/UX-EVIDENCE-REFERENCE-CARDS.yml` | Research pass completed with 25 cards. |
| `development/UX-EVIDENCE-CLAIM-MAP.md` | Claim map completed. |
| `development/UX-PLAYWRIGHT-VALIDATOR-SPEC.md` | Validator contract completed. |
| `development/UX-PLAYWRIGHT-FIXTURE-PLAN.md` | Fixture plan completed. |
| `development/task-sessions/20260601T141642Z-ux-playwright-evidence-research/` | Research receipt and evidence index completed. |

## Layers

| Layer | Objective | Status |
| --- | --- | --- |
| L0 Seed package | Dedicated sigil folder, README, SKILL, moved research artifacts, registry entry. | completed |
| L1 Fixture corpus | Implement known-good, known-bad, domain, and false-positive fixture pages. | pending |
| L2 Harness skeleton | Implement Playwright runner, scenario parser, output root, and finding model. | pending |
| L3 Deterministic gates | Implement smoke, accessibility, layout, interaction, and evidence-output checks. | pending |
| L4 Soft UX proxies | Implement explainable density, memory-burden, salience, and domain flags. | pending |
| L5 Calibration report | Run fixtures, tune thresholds, prove false-positive boundaries. | pending |
| L6 Promotion review | Experiment Harness report plus Sigil Development review. | pending |

## Small Work Units

| SWU | Task | Prerequisite | Done Evidence |
| --- | --- | --- | --- |
| UEV-SWU-001 | Create seed sigil package from research artifacts. | Research task-session pass. | Completed: README, SKILL, development artifacts, experiment profile, registry entry, validation pass. |
| UEV-SWU-002 | Implement fixture corpus from `UX-PLAYWRIGHT-FIXTURE-PLAN.md`. | UEV-SWU-001. | Fixture files, expected findings, fixture index, static smoke. |
| UEV-SWU-003 | Implement Playwright scenario and evidence-output skeleton. | UEV-SWU-002. | `run-metadata.json`, screenshots, traces, findings JSON for fixture runs. |
| UEV-SWU-004 | Add deterministic L0-L3 gate checks. | UEV-SWU-003. | Known bad fixtures block; known good fixture passes. |
| UEV-SWU-005 | Add L4-L5 soft flag checks. | UEV-SWU-004. | Soft flags cite source cards and false-positive trap does not block. |
| UEV-SWU-006 | Run calibration and write promotion review. | UEV-SWU-005. | Calibration report, Experiment Harness report, Sigil Development decision. |

## Gates

| Gate | Rule |
| --- | --- |
| Source evidence required | Every UX claim must cite an evidence card. |
| Automation honesty | Browser-observable failures must remain separate from proxy and human-study claims. |
| Fixture first | Reusable hard gates require known-good and known-bad fixtures. |
| False-positive trap | L4/L5 rules must not block dense expert interfaces by default. |
| No promotion from spec alone | README and SKILL are seed contracts until live evidence exists. |

## Next Task

Run `UEV-SWU-002`: implement the fixture corpus first. This gives the later Playwright validator a truth set before code decisions harden.
