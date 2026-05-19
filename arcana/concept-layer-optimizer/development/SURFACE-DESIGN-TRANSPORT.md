# Invoke Design Transport: Concept Layer Optimizer Surface Design

## Observer Envelope

- run_id: arcanum-invoke-design-20260519T112133Z
- capability.id: invoke
- capability.kind: spell
- capability.tier: spell
- capability.mode: design
- target_artifact: arcana/concept-layer-optimizer/development/MODE-TECHNIQUE-SURFACE-DESIGN.md
- request summary: design the technique and mode surface layers and their interface with the Concept Layer Optimizer sigil.
- expected outputs: architecture design artifact, glossary consistency report, design transport report.

## Design Context Summary

The Concept Layer Optimizer handoff already defines modes and a technique pack. The missing design layer is the interface architecture that prevents modes, techniques, runtime adapters, and the core sigil loop from collapsing into one tangled process.

This design uses layered surfaces:

- invocation surface,
- mode surface,
- technique surface,
- core sigil engine,
- trace surface,
- handoff surface.

## Template Selection Evidence

- Selected template family: invoke.architecture
- Template path: spells/invoke/templates/architecture/architecture.md
- Eligibility: the user requested a design for interfaces and surface layers, which requires six design views, dependency/interface rules, decisions, and risks.
- Tie cases: none. The sigil template was not selected because the sigil definition already exists; this run designs architecture around it.

## Outputs

- Architecture design: arcana/concept-layer-optimizer/development/MODE-TECHNIQUE-SURFACE-DESIGN.md
- Detailed technique specifications: arcana/concept-layer-optimizer/development/techniques/README.md
- Glossary consistency report: arcana/concept-layer-optimizer/development/SURFACE-GLOSSARY-CONSISTENCY.md
- Design transport report: arcana/concept-layer-optimizer/development/SURFACE-DESIGN-TRANSPORT.md

## Design Views

- Context view: pass
- High-level structure view: pass
- Low-level components view: pass
- Workflow process view: pass
- Decision flow view: pass
- Dependency interface view: pass

## Decisions

- Modes compile into ModeProfile objects.
- Techniques compile into TechniqueSpec objects attached to PhaseHook points.
- Each included technique has a stable id, activation rule, inputs, emitted trace fields, pass/flag/block criteria, failure behavior, and anti-patterns.
- Core sigil engine owns concept state, closure, recomposition, and readiness verdicts.
- Trace surface preserves role and technique reasoning as append-only run evidence.
- Handoff surface routes outcomes based on verdict and tension ownership.

## Glossary Consistency

- Status: pass
- Reason: Existing terms are consistent, and new local interface terms were added to GLOSSARY.md.

## Implementation Layering

- Seed update recommended: Layer 1 candidate package should use MODE-TECHNIQUE-SURFACE-DESIGN.md as an interface contract.
- Work-pack: n/a

## Unresolved Gaps

- Non-blocking: choose representation for ModeProfile and TechniqueSpec during sigil-development.
- Non-blocking: runtime adapter still needs true-subagent versus role-simulation decision.
- Non-blocking: validation examples must prove Compact, Standard, Tournament, and technique-trigger behavior using techniques/README.md.

## Recommended Next Route

sigil-development

Use this design as the bridge between the define handoff and candidate README.md/SKILL.md authoring.
