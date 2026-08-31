# TASK-DV2-MODES — Finite Mode Catalog

## Objective

Publish each ModeSpec as a finite run-shape program without redefining technique
semantics, closure rules, or verdict authority.

## Entry And Write Scope

Requires SWU-DV2-017 PASS. Each SWU writes one
`profiles/v2/modes/<mode_id>.json` and focused fixtures only.

| SWU | Mode | Required focused proof |
| --- | --- | --- |
| SWU-DV2-018 | Compact | one track/round, always-on policy, explicit skips, blocker gate |
| SWU-DV2-019 | Standard | one track, two rounds, Proposer/Balancer, reconciliation, no pitch-off |
| SWU-DV2-020 | Tournament | selected finite default/max tracks, two rounds/track, required pitch-off |
| SWU-DV2-021 | Deep | selected finite default/max tracks/rounds, stronger cycle/human gates |
| SWU-DV2-022 | Validate | one existing solution, finite one/two-round policy, Balancer-led optional repair |

Every denominator rejects absent maxima, excess overrides, removed cycle guards,
free-form role programs, technique redefinition, or mode-owned verdict rules.
SWU-DV2-022 proves unique IDs and the complete five-mode catalog.

## Claim Ceiling And Successor

Finite mode catalog conformance only. The only successor is SWU-DV2-023.
