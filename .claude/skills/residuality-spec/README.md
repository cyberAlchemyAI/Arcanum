# Residuality Spec

Residuality Spec is an Arcana sigil for defining or hardening specifications through stressor and residue analysis.

It helps users move beyond ordinary functional requirements. Instead of only asking what the system should do when everything works, the sigil asks what should remain true when the system is stressed, degraded, overloaded, partially failing, socially disrupted, or surprised.

## Problem It Solves

Many specifications say what the happy path should do but stay vague about degradation. They use phrases like "must be resilient" without naming what survives, what degrades, what stops, what users see, what operators do, and what signals prove the behavior.

Residuality Spec turns resilience into concrete specification material: stressors, residues, degradation behavior, observability signals, verification ideas, and decisions.

## Use When

- a feature, workflow, product area, or architecture slice needs resilience requirements,
- the user wants to define how a system should degrade,
- unknown or chaotic stresses matter more than a fixed list of known risks,
- social, operational, or organizational stressors could affect behavior,
- the spec needs concrete non-functional behavior rather than vague resilience claims.

## Do Not Use When

- the task only needs a happy-path feature description,
- the system is too small for resilience analysis to add value,
- the user wants implementation before resolving degradation behavior,
- the team is not willing to make trade-off decisions,
- the output would become fear-driven overengineering.

## Core Concepts

- Stressor: a pressure, disruption, surprise, or adverse condition that changes how the system behaves.
- Residue: the behavior, data, capability, trust, or signal that should remain after a stressor occurs.
- Degradation: the acceptable reduced behavior when the ideal behavior cannot continue.
- Attractor: a recurring vulnerability cluster revealed by multiple stressors.

## Output

The sigil produces a resilience-oriented spec package:

- stressor map,
- residue table,
- degradation spec,
- attractor report,
- resilience decisions,
- spec patch plan.

## Integration

Use [context-builder](../../transmutations/context-builder/) before this sigil when requirements and architecture evidence are scattered.

Use [architecture-pattern-inventory](../architecture-pattern-inventory/) when resilience findings depend on current architecture boundaries.

Use [decision-gate](../decision-gate/) when residue trade-offs create blocker decisions.

Use [inventory](../inventory/) to store recurring stressors, residues, incidents, attractors, and resilience decisions as reusable knowledge.

## Why This Is Arcana

Residuality Spec coordinates uncertainty exploration, human decision points, stressor synthesis, residue trade-offs, spec patching, and downstream verification. It governs how a system should survive stress, not just how one artifact should be formatted.