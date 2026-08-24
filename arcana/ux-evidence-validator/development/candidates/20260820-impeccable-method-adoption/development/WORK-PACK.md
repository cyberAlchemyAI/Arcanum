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
| `development/work-packs/uev-deterministic-kernel/` | A bounded terminal-outcome kernel task has passing development evidence; this is not Playwright harness or fixture-calibration evidence. |
| `development/task-sessions/20260601T141642Z-ux-playwright-evidence-research/` | Research receipt and evidence index completed. |

## External Method Adoption Gate

Before `UEV-SWU-002`, admit an external method only when its evidence card:

1. pins a public source revision and source class;
2. states its allowed use and hard-gate ceiling;
3. separates scenario-generation value from evidence authority;
4. rejects aggregate scores, aesthetic bans, synthetic personas as evidence,
   detector output as authority, and uncalibrated universal numbers; and
5. requires independent standards or product authority plus known-good and
   known-bad fixtures before any L0-L3 promotion candidate.

No external package, hook, detector, browser runtime, root artifact protocol,
visual system, or copied implementation is needed to satisfy this gate.

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
| UEV-SWU-002 | Implement fixture corpus from `UX-PLAYWRIGHT-FIXTURE-PLAN.md`, including declared content, context, state, fault, adaptation, and aesthetic false-positive profiles. | UEV-SWU-001 plus External Method Adoption Gate. | Fixture files, expectation-authority bindings, expected findings, fixture index, static smoke, and known-good/bad witnesses for each promoted candidate. |
| UEV-SWU-003 | Implement Playwright scenario and evidence-output skeleton. | UEV-SWU-002. | `run-metadata.json`, screenshots, traces, findings JSON for fixture runs. |
| UEV-SWU-004 | Add deterministic L0-L3 gate checks. | UEV-SWU-003. | Known bad fixtures block; known good fixture passes. |
| UEV-SWU-005 | Add L4-L5 soft flag checks. | UEV-SWU-004. | Soft flags cite source cards and false-positive trap does not block. |
| UEV-SWU-006 | Run calibration and write promotion review. | UEV-SWU-005. | Calibration report, Experiment Harness report, Sigil Development decision. |

## Gates

| Gate | Rule |
| --- | --- |
| Source evidence required | Every UX claim must cite an evidence card. |
| External authority ceiling | An external expert method can propose coverage or review prompts but cannot independently authorize a hard gate. |
| Automation honesty | Browser-observable failures must remain separate from proxy and human-study claims. |
| Fixture first | Reusable hard gates require known-good and known-bad fixtures. |
| False-positive trap | L4/L5 rules must not block dense expert interfaces by default. |
| No promotion from spec alone | README and SKILL are seed contracts until live evidence exists. |

## Next Task

Review and accept the seven-artifact method-adoption candidate, regenerate the
native skill packages from canonical source if applied, and then run
`UEV-SWU-002`: implement the expanded fixture corpus first. This gives the later
Playwright validator a truth set before code decisions harden.
