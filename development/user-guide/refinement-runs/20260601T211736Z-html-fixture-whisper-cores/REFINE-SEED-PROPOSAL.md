# Refine Seed Proposal: HTML Guide And Whisper-Core Fixture

Status: strategy proposal, pending operator confirmation before runtime-backed Refine stages.

## Target

- Target folder: `development/user-guide`
- Source guide: `development/user-guide/ARCANUM-DEVELOPMENT-USAGE-GUIDE.md`
- Residue being refined:
  - A future HTML version could make the loop more approachable for non-technical users.
  - A future fixture could demonstrate one complete idea-to-MVP run.
- Requested exemplar: Whisper rollout `019e6556-940e-7501-ab97-8dc127a624a9`
- Local proof corpus:
  - `spells/whisper/README.md`
  - `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml`
  - `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/WORK-PACK.md`
  - `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/TASK-SESSION-PARETO-REPORT.md`
  - `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md`

## Desired Outcome

Create a refined route for two approachable artifacts:

1. A non-technical HTML guide that makes the Arcanum idea-to-MVP loop feel usable by designers, founders, researchers, writers, and product builders.
2. A complete idea-to-MVP fixture using the Whisper example as a worked case, showing how a broad creative idea becomes a substrate, candidate set, composition plan, work-pack, task-session evidence, validator checks, and follow-up residue.

The refined result should help users understand that Arcanum is not only a project-management flow. It is a way to explore ideas by giving them operational shape.

## Core Parallel To Whisper

Whisper uses three Smallest Coherent Unit cores:

| Whisper Core | Writing Meaning | General Arcanum Idea-Exploration Parallel |
| --- | --- | --- |
| `resonance_core` | The felt meaning the text should carry. | The experiential promise of the idea: what should the user feel, trust, notice, or become energized by? |
| `relevance_core` | Why the text belongs to this audience and domain. | The fit question: who is this for, why now, what world does it enter, and what objections must it respect? |
| `trajectory_core` | The movement the text performs. | The transformation path: where the user starts, what sequence the system guides them through, and what proof shows movement happened. |

This gives the guide a reusable exploration grammar:

```text
idea_resonance
  -> What human energy, meaning, or relief should this idea create?

idea_relevance
  -> Who is it really for, in what context, with what constraints and objections?

idea_trajectory
  -> What movement does it perform from first prompt to MVP evidence?
```

The HTML guide should make these cores visible as a thinking surface. A non-technical user should be able to write a rich idea, inspect these three cores, compare candidate directions, and see how the winning candidate becomes a plan.

## How We Can Really Explore Ideas

The fixture should show exploration as a staged practice:

1. Name the idea.
2. Extract the three cores.
3. Generate several candidate routes that combine all three cores.
4. Reject candidates that optimize only one dimension, such as usefulness without resonance or beauty without implementation proof.
5. Apply hard gates before selection, such as audience legibility, citation integrity, or scope safety.
6. Select a non-dominated candidate that balances the cores.
7. Decompose the selected candidate into parts.
8. Give each part a responsibility, dependencies, must-do rules, must-not-do rules, and validation checks.
9. Run one task-session-sized unit.
10. Preserve evidence and residue for the next loop.

Whisper demonstrates this pattern through:

- `resonance`, `relevance`, and `trajectory` objectives,
- a `two_tier` Pareto model,
- hard gates like opening-contract compliance and citation integrity,
- candidate sets with known strengths, trade-offs, failure modes, objective scores, and selected/rejected status,
- `composition_parts` for part-level responsibilities and mini-tournament triggers,
- validator-backed evidence instead of prose-only confidence.

The Arcanum guide can generalize the same method beyond writing:

| Exploration Layer | Whisper Example | General Tool/Design Example |
| --- | --- | --- |
| Core extraction | Resonance, relevance, trajectory cores. | Promise, audience/domain fit, transformation path. |
| Candidate comparison | Substack candidate sets. | Product route candidates, interface concepts, workflow designs, validator strictness modes. |
| Hard gates | Opening contract, citation integrity, audience legibility. | Accessibility, evidence safety, scope boundary, user trust, runtime feasibility. |
| Composition parts | Article sections with roles and dependencies. | UI screens, research lanes, workflow stages, validator checks, documentation sections. |
| Task-session unit | Draft, schema refresh, second draft. | One fixture, one HTML section, one validator proof, one guide interaction. |
| Residue | Publication gaps and next transport pressure. | Next feature, unresolved decision, research gap, or fixture expansion. |

## Route Menu

| Route | Description | Trade-off |
| --- | --- | --- |
| HTML-first | Build the approachable HTML guide first, using the Whisper example as embedded story and diagrams. | Fast user-facing value, but the fixture may remain illustrative instead of executable. |
| Fixture-first | Build the complete idea-to-MVP fixture first, then use it as source material for the HTML guide. | Stronger evidence, but less immediately approachable for non-technical users. |
| Parallel spine | Define a shared Whisper-core spine, then build the HTML guide and fixture together from the same structure. | Best coherence, but needs stricter scope control. |

Recommended route: `parallel spine`.

Reason: the HTML guide should teach from a real worked fixture, and the fixture should be shaped to be teachable. The shared spine prevents the two artifacts from drifting.

## Proposed Output Shape

### HTML Guide

Potential path: `development/user-guide/arcanum-development-loop.html`

Required sections:

- First-screen loop map for non-technical users.
- "Start with your wild idea" prompt surface.
- Three-core idea exploration panel: promise, fit, movement.
- Candidate comparison view inspired by Whisper's Pareto model.
- Blocker router as an interactive visual.
- Whisper worked example lane.
- "Your next move" cards for `refine`, `invoke`, `decision-gate`, `dispatch-spec`, `x-ray`, and `task-session`.

### Fixture

Potential folder: `development/user-guide/fixtures/whisper-idea-to-mvp/`

Required artifacts:

- `README.md`: what the fixture demonstrates.
- `idea-substrate.yml`: generalized core extraction from the Whisper example.
- `candidate-routes.yml`: candidate directions, objective scores, hard gates, selected route, rejected alternatives.
- `composition-parts.yml`: parts, dependencies, must-do, must-not-do, validation checks.
- `WORK-PACK.md`: task-session-ready units.
- `EVIDENCE-LEDGER.md`: source files, validations, unresolved residue.
- `PLAYBOOK.md`: how a user can reuse this structure for their own idea.

## Done Criteria

- The HTML version is readable by a non-technical user without assuming they know Arcanum vocabulary.
- The Whisper example is concrete enough to show the loop from idea to MVP evidence, not just describe it.
- The three-core parallel is explicit and reusable.
- Candidate comparison preserves rejected alternatives instead of hiding them.
- The fixture includes hard gates, part responsibilities, and validation expectations.
- The output does not claim the guide or fixture is a completed full Refine execution until runtime-backed stages actually run.

## Research Decision

Mode: `no-research`.

Reason: this refinement is grounded in local Arcanum and Whisper evidence. External academic or market research is not needed for this route. If the HTML guide later makes claims about UX, cognition, neuroscience, or market practices, that should be routed separately through `dispatch-spec`.

## Proposed Stage Configuration

Preset: `full`.

Selected overlays:

- `baseline_sequence`: preserve the canonical ten-stage Refine loop.
- `route_menu_for_ambiguity`: the work has multiple plausible starting routes.
- `tournament_for_alternatives`: the guide should compare exploration routes and candidate concept shapes.
- `xray_for_hidden_structure`: non-technical users need the hidden Arcanum lifecycle made visible.
- `toy_game_for_low_cost_falsification`: the fixture should prove the abstraction with one small worked example.
- `memory_residue_for_context_recovery`: the Whisper rollout is controlling evidence and must remain cited rather than paraphrased from memory alone.

## Permission Gate

The dispatch route validates, and subagent review is recommended. Do not execute the runtime-backed Refine loop until the operator confirms the strategy and delegated reviewer roles.
