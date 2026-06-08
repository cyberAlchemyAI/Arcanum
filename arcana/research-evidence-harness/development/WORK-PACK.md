---
name: Research Evidence Harness Development Pack
description: Initial development plan for the draft research-evidence-harness sigil.
status: draft
created: 2026-06-07
---

# Research Evidence Harness Development Pack

## Objective

Create and validate a reusable sigil for project-local research evidence
mechanics, seeded by MOGT and MARS.

## SWU Manifest

| SWU ID | Status | Objective | Acceptance Evidence |
| --- | --- | --- | --- |
| SWU-REH-001 | ready | Validate the draft sigil against MOGT `SWU-MOGT-HARNESS-001`. | MOGT schema/validator fixtures pass and sigil gaps are recorded. |
| SWU-REH-002 | blocked-on-001 | Add objective-vector and Pareto/frontier calculator guidance. | MOGT synthetic E2 fixture can classify dominated/frontier selections. |
| SWU-REH-003 | blocked-on-001 | Add result-summary and claim-boundary template validation. | Dry-run summary distinguishes fixture evidence from live evidence. |
| SWU-REH-004 | blocked-on-001,002,003 | Decide whether to promote, revise, or keep as draft. | Sigil-development report with promotion blockers or approval path. |

## Guardrails

- Do not mutate `arcana/experiment-harness` from this pack.
- Do not mark MOGT evidence status as supported from dry-run fixtures.
- Treat MARS as reference evidence, not canonical Arcanum authority.
