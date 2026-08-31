# Fixture: INV-INTEGRATION-DEFINE-DESIGN-PLAN-001

## Scenario

End-to-end define-to-design-to-plan handoff without invented upstream authority.

## User Request

Define, design, and plan a Mars rover maintenance log module.

## Artifact Chain

- Define spec: `INV-INTEGRATION-DEFINE-DESIGN-001.spec.md`
- Define glossary: `INV-INTEGRATION-DEFINE-DESIGN-001.glossary.md`
- Define transport: `INV-INTEGRATION-DEFINE-DESIGN-001.define-transport.md`
- Design architecture: `INV-INTEGRATION-DEFINE-DESIGN-001.architecture.md`
- Design glossary consistency: `INV-INTEGRATION-DEFINE-DESIGN-001.glossary-consistency.md`
- Design transport: `INV-INTEGRATION-DEFINE-DESIGN-001.design-transport.md`
- Plan implementation plan: `INV-INTEGRATION-DEFINE-DESIGN-PLAN-001.implementation-plan.md`
- Plan implementation layering: `INV-INTEGRATION-DEFINE-DESIGN-PLAN-001.implementation-layering.md`
- Plan work-pack: `INV-INTEGRATION-DEFINE-DESIGN-PLAN-001.work-pack.md`
- Plan transport: `INV-INTEGRATION-DEFINE-DESIGN-PLAN-001.plan-transport.md`

## Expected

- Define output routes to design.
- Design output routes to plan.
- Plan consumes design outputs and preserves define glossary terms.
- Plan emits implementation plan, global implementation-layering artifact, work-pack, validation strategy, and plan transport.
- Plan does not execute implementation tasks.
