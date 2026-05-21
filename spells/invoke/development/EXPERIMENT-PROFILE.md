# Experiment Profile

- Profile ID: invoke-live
- Artifact type: spell
- Lifecycle owner: invoke
- Artifact path: spells/invoke
- Contract path: spells/invoke/README.md
- Scenario pack: invoke-live-promotion
- Required modes: define, design, define-design, observability
- Prompt set: invoke-define-live-pass, invoke-design-live-pass, invoke-define-design-live-pass, invoke-define-live-pass
- Regime set: LIVE-DEFINE-001, LIVE-DESIGN-001, LIVE-DEFINE-DESIGN-001, LIVE-OBSERVABILITY-001
- Validation focus: invoke output contract; define/design handoff evidence; live loop pass; observability telemetry
- Observability focus: live loop report; quality bar status; anti-pattern hits; workflow gaps; reflection trigger
- Promotion gate: live loop pass plus observed report

## Ownership Boundary

Experiment Harness owns experiment mechanics. The lifecycle owner owns artifact meaning and promotion judgment.
