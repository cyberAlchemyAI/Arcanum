# Invoke Template Validation Tasks

This matrix defines realistic low, medium, and complex validation tasks for every invoke-owned template family or standalone companion.

These are not promotion examples by themselves. They are the task inventory used to decide which template fixtures must exist before a template family can be considered broadly validated.

## Complexity Scale

| Complexity | Meaning |
| --- | --- |
| low | One bounded artifact, few actors, no cross-stage ambiguity. |
| medium | Several artifacts or actors, real decisions, some handoff risk. |
| complex | Multi-stage, cross-domain, high ambiguity, or multiple ownership boundaries. |

## Template Task Matrix

| Task ID | Template | Complexity | Realistic User Task | Expected Invoke Use |
| --- | --- | --- | --- | --- |
| module-formulae-low | module-formulae | low | Define a Mars sample catalog module with sample ID, source mission, curation state, and search notes. | Use discovery profile to emit module spec and glossary. |
| module-formulae-medium | module-formulae | medium | Define and design an ecommerce order module with carts, payments, inventory reservation, fulfillment state, and refund terms. | Use discovery plus architecture profiles with concept model, flows, interfaces, and glossary. |
| module-formulae-complex | module-formulae | complex | Define and design a Facebook-like social graph module with profiles, posts, reactions, follows, feed visibility, moderation state, and privacy constraints. | Use full profile candidates across spec, glossary, concepts, flows, interfaces, architecture, observability, and planning handoff. |
| implementation-layering-low | implementation-layering | low | Layer a small search filter feature into L0 proof, L1 hardening, and deferred analytics. | Emit a compact layer decision table. |
| implementation-layering-medium | implementation-layering | medium | Layer ecommerce checkout changes across payment authorization, inventory holds, refund state, and rollout gates. | Emit layer boundaries, deferred scope, promotion evidence, and risks. |
| implementation-layering-complex | implementation-layering | complex | Layer a social platform feed rewrite across ranking, privacy enforcement, moderation, migrations, and staged release. | Emit multi-layer promotion decisions with irreversible-risk callouts. |
| work-pack-low | work-pack | low | Plan one small admin setting change with two tasks and one validation check. | Emit single-file work-pack. |
| work-pack-medium | work-pack | medium | Plan ecommerce checkout readiness with payment, inventory, order history, and support handoff tasks. | Emit split-ready work-pack with gates and blockers. |
| work-pack-complex | work-pack | complex | Plan a Facebook-like notification system across mobile, web, ranking, privacy, and migration dependencies. | Emit split work-pack with waves, shared context, blockers, and execution-pack reference. |
| generic-low | generic | low | Clarify a vague request to organize a team's deployment checklist. | Emit neutral define artifact and next route. |
| generic-medium | generic | medium | Turn an ecommerce returns workflow idea into scope, actors, acceptance criteria, and open decisions. | Emit generic spec-like artifact with gaps and route recommendation. |
| generic-complex | generic | complex | Frame a multi-tenant marketplace expansion where business, architecture, UX, and planning needs are unclear. | Emit broad lifecycle baseline and route to research, architecture, or plan as needed. |
| research-low | research | low | Compare two payment tax API docs and identify which claims are verified. | Emit research brief with evidence table and gaps. |
| research-medium | research | medium | Investigate whether a Facebook-like feed should rank by recency, engagement, or follow graph signals. | Emit claim status, contradictions, and architecture decision inputs. |
| research-complex | research | complex | Research Mars habitat dust contamination risks across mission notes, sensor reports, and operational constraints. | Emit multi-source research brief with unresolved claims and decision gates. |
| refresh-low | refresh | low | Refresh invoke validation artifacts from a repeated passing report already represented in the docs. | Emit a no-op refresh report. |
| refresh-medium | refresh | medium | Refresh a work-pack from a setup proof that opens a blocker for real score evidence. | Emit proposal-only refresh report and patch proposal. |
| refresh-complex | refresh | complex | Refresh a split work-pack with contradictory board and task-file status after ambiguous session evidence. | Emit artifact-drift flag and owner-review route. |
| architecture-low | architecture | low | Design a read-only product catalog page service with search and category filters. | Emit six-view architecture plan. |
| architecture-medium | architecture | medium | Design ecommerce checkout architecture with cart, payment, inventory, order, and failure compensation boundaries. | Emit six-view architecture plus interface and decision rules. |
| architecture-complex | architecture | complex | Design a Facebook-like social platform architecture with feed, graph, privacy, moderation, notifications, and observability. | Emit six-view architecture with dependency/interface map and risks. |
| implementation-plan-low | implementation-plan | low | Plan implementation for adding saved filters to a reporting screen. | Emit small delivery slice and validation checklist. |
| implementation-plan-medium | implementation-plan | medium | Plan ecommerce checkout refactor from approved architecture and glossary. | Emit staged implementation plan with source design refs and gates. |
| implementation-plan-complex | implementation-plan | complex | Plan migration from legacy social feed storage to a privacy-aware feed service. | Emit layered implementation plan with migrations, blockers, and wave boundaries. |
| spell-low | spell | low | Create a daily research-summary spell that composes inventory and context-builder. | Emit spellcraft handoff context. |
| spell-medium | spell | medium | Create an ecommerce release-readiness spell that composes implementation-layering, decision-gate, and task-session. | Emit spell design handoff with phases, gates, and observability needs. |
| spell-complex | spell | complex | Create a full lifecycle product-discovery spell for a Facebook-like platform that routes define, research, architecture, planning, and validation. | Emit spellcraft handoff with authority boundaries and unresolved lifecycle decisions. |
| sigil-low | sigil | low | Create a deterministic CSV column normalization sigil. | Emit sigil-development handoff with inputs, outputs, and quality bar. |
| sigil-medium | sigil | medium | Create a fixture validation sigil that checks realistic requests, expected outputs, and run reports. | Emit sigil-development handoff with validation and observability requirements. |
| sigil-complex | sigil | complex | Create an observability reflection sigil that reads repeated execution signals, classifies gaps, and proposes lifecycle updates. | Emit sigil-development handoff with subagent/observer boundaries and reflection gates. |
| session-handoff-low | session-handoff | low | Create a new lifecycle thread from a short source session reference and a prompt about a deployment checklist idea. | Emit a compact session handoff with prompt, selected context, and next route to `invoke define`. |
| session-handoff-medium | session-handoff | medium | Create a workflow-reflection thread from an invoke planning session where the user feels handoffs are too execution-heavy. | Emit a Context Builder-backed reflection handoff that routes to `workflow-reflect`. |
| session-handoff-complex | session-handoff | complex | Create a cross-project research-direction thread from a long session with decisions, unresolved questions, and unrelated implementation details. | Emit a research handoff that separates known session evidence from new investigation questions. |
| ux-plan-low | ux-plan | low | Plan a settings form for notification preferences. | Emit UX plan with actors, states, and accessibility checks. |
| ux-plan-medium | ux-plan | medium | Plan ecommerce checkout UX across guest checkout, payment errors, address validation, and order confirmation. | Emit UX plan with flows, state handling, and architecture handoff notes. |
| ux-plan-complex | ux-plan | complex | Plan Facebook-like content moderation UX across reporting, review queues, appeal states, notifications, and accessibility. | Emit UX plan with surface map, state model, content rules, and risk handoffs. |

## Fixture Requirements

Each task family should eventually have:

- one low-complexity fixture,
- one medium-complexity fixture,
- one complex fixture,
- one expected user-facing output for each fixture,
- at least one negative fixture for missing inputs or unsupported routing,
- runner coverage that checks the expected output shape.

## Current Coverage Use

This matrix is the template coverage backlog. The validation runner checks that every declared template has low, medium, and complex task IDs. Dedicated executable fixtures can then be added in waves without losing the complete coverage map.
