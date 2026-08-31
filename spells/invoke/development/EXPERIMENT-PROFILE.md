# Experiment Profile

- Profile ID: invoke-live
- Artifact type: spell
- Lifecycle owner: invoke
- Artifact path: spells/invoke
- Contract path: spells/invoke/README.md
- Scenario pack: invoke-live-promotion
- Required modes: define, design, plan, define-design, define-design-plan, semantic-intent-low, semantic-intent-medium, semantic-intent-complex, observability
- Prompt set: invoke-define-live-pass, invoke-design-live-pass, invoke-plan-live-pass, invoke-define-design-live-pass, invoke-define-design-plan-live-pass, invoke-semantic-intent-low, invoke-semantic-intent-medium, invoke-semantic-intent-complex, invoke-observability-live-pass
- Regime set: LIVE-DEFINE-001, LIVE-DESIGN-001, LIVE-PLAN-001, LIVE-DEFINE-DESIGN-001, LIVE-DEFINE-DESIGN-PLAN-001, LIVE-SEMANTIC-INTENT-LOW-001, LIVE-SEMANTIC-INTENT-MEDIUM-001, LIVE-SEMANTIC-INTENT-COMPLEX-001, LIVE-OBSERVABILITY-001
- Validation focus: invoke output contract; define/design/plan handoff evidence; parsed semantic-intent coverage; live pass; observability telemetry
- Observability focus: semantic receipt; quality bar status; anti-pattern hits; workflow gaps; reflection trigger
- Promotion gate: two consecutive semantic-validator passes at low, medium, and complex plus lifecycle-owner review

## Semantic Validator Hook

The `invoke-live` profile may call the repository-owned semantic validator over
`development/live-intent-evidence/*/artifact.json`. The validator parses each
artifact against the checked fixture oracle; headings and keyword presence do
not establish a pass. Six passing artifacts are required: two consecutive runs
for each low, medium, and complex target. The hook is validation-only and does
not invoke or patch the experiment loop.

## Ownership Boundary

Experiment Harness owns experiment mechanics. The lifecycle owner owns artifact meaning and promotion judgment.
