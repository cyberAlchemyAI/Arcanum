# Architecture Plan: Distill Mode And Technique Surface

## Architecture Intent

Design the surface layers and interface rules that let Distill keep a stable core while supporting configurable modes and techniques.

The design must make these properties possible:

- Modes change orchestration budget and run shape without rewriting the core sigil.
- Every run keeps the objective-output artifact pair visible so discovery can adjust the target result without losing orientation.
- Techniques attach to explicit phases as gates, lenses, classifiers, checks, closeout passes, or mode mechanics.
- The core sigil owns concept state, closure, recomposition, tension routing, and readiness verdicts.
- Runtime adapters use true subagents when available; when unavailable, they simulate Proposer and Balancer roles while preserving the same trace contract.
- Every mode and technique leaves auditable evidence in the final result and observability signals.

## Source Contracts

| Contract ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SC-001 | arcana/distill/development/SIGIL-HANDOFF.md | yes | Defines identity, modes, technique pack, output contract, role trace, runtime expectations, and observability. |
| SC-002 | arcana/distill/development/GLOSSARY.md | yes | Defines local vocabulary for concept units, modes, techniques, traces, and tensions. |
| SC-003 | arcana/distill/development/LITERATURE-RESEARCH.md | yes | Supplies source techniques and rationale for recomposition, evolution, cognitive load, requisite variety, boundary objects, premortem, and set-based tournament. |
| SC-004 | arcana/distill/development/INTERROGATION-REVIEW.md | yes | Confirms broad design readiness and identifies lifecycle packaging as the next route. |
| SC-005 | spells/invoke/design.md | yes | Requires six design views, source contracts, interface rules, decision log, risks, and design transport notes. |
| SC-006 | arcana/distill/development/techniques/README.md | yes | Defines detailed TechniqueSpec contracts for each included technique. |
| SC-007 | framework/CYBERALCHEMY-METHOD.md | yes | Adds objective-output orientation, discovery baseline, and navigable work surface expectations. |

## View 1: Context View

Distill sits between user intent and downstream lifecycle routes. It is not an implementation executor. It is a planning optimizer that receives a seed point, target context, objective-output artifact pair, constraints, and optional artifacts, then returns a proportionate concept structure and route recommendation.

External actors and neighboring systems:

| Actor Or System | Relationship |
| --- | --- |
| User | Supplies seed point, context, constraints, budget choice, and blocker decisions. |
| Runtime adapter | Presents mode and budget surface, runs role conversations, records traces, and emits observability. |
| Proposer role | Builds candidate concept layers, reduction paths, and optimization points. |
| Balancer role | Challenges proposals through named objection categories and triggered techniques. |
| Technique pack | Provides phase-bound techniques and gates that sharpen the core loop. |
| Robot-Talks | Receives cross-layer tensions that need independent investigation. |
| Decision-Gate | Receives blocker choices that prevent selecting an optimization point. |
| Implementation Layering | Receives a selected concept unit when the user wants build sequencing. |
| Invoke design or plan | Receives a design-ready or plan-ready concept map for lifecycle authoring. |
| Task Session | Receives a bounded next action when execution is ready. |

Ownership boundary:

- The core sigil owns concept-layer state, closure tests, recomposition proof, optimization-point selection, and readiness verdict.
- Modes own run shape only.
- Techniques own local checks only.
- Runtime adapters own execution mechanics and trace capture.
- Downstream sigils own any follow-up lifecycle work.

## View 2: High-Level Structure View

The surface architecture has six layers.

| Layer | Responsibility | Must Not Own |
| --- | --- | --- |
| Invocation surface | Parse user intent, ask first-turn design intent and budget question, normalize overrides. | Concept decomposition or verdicts. |
| Mode surface | Convert budget choice into a finite mode profile: tracks, rounds, role model, pitch-off, human gates, closeout policy. | Technique semantics or concept state. |
| Technique surface | Select and run techniques through explicit phase hooks. | Independent orchestration or hidden mode changes. |
| Core sigil engine | Maintain run frame, concept layers, candidate units, closure, recomposition, tensions, and verdict. | Runtime-specific subagent mechanics. |
| Trace surface | Preserve role trace, technique trace, reduction trace, tension ledger, and final result envelope. | Decision authority. |
| Handoff surface | Route pass, flag, or block outcomes to implementation-layering, robot-talks, decision-gate, invoke design, invoke plan, task-session, or deferred follow-up. | Reinterpreting the verdict. |

High-level collaboration:

```text
User intent
  -> Invocation surface
  -> Mode surface
  -> Technique surface
  -> Core sigil engine
  -> Trace surface
  -> Handoff surface
```

## View 3: Low-Level Components View

### Core Data Objects

| Object | Fields | Owner |
| --- | --- | --- |
| RunFrame | seed point, target context, objective, output artifact, optimization goal, discovery baseline, constraints, evidence boundary, selected mode, active techniques | Core sigil engine |
| ModeProfile | mode id, proposal tracks, role conversations, recursive round budget, technique policy, pitch-off policy, human-gate policy, closeout policy | Mode surface |
| TechniqueSpec | technique id, type, phase, trigger, input contract, output contract, failure behavior, trace fields | Technique surface |
| PhaseHook | hook id, phase, allowed technique types, required state, emitted trace | Technique surface |
| TrackState | track id, proposer claims, balancer objections, candidate units, stable disagreements, local verdict | Core sigil engine |
| ConceptLayer | label, abstraction level, responsibility, child units, recomposition note | Core sigil engine |
| CandidateUnit | name, responsibility, inputs, outputs, abstraction level, closure result, evolution profile, risks | Core sigil engine |
| TensionEntry | category, source role, affected unit, severity, reconciliation decision, route | Trace surface |
| ResultEnvelope | mode, budget, objective, output artifact, tracks, rounds, verdict, selected unit, traces, proofs, deferred complexity, navigation guide, next route | Trace surface |

### Surface Components

| Component | Responsibility | Interface |
| --- | --- | --- |
| IntentNormalizer | Converts raw request into seed point, target context, objective, output artifact, optimization goal, and constraints. | Produces RunFrame draft. |
| ModeResolver | Selects Compact, Standard, Tournament, Deep, or Validate from user choice or safe default. | Produces ModeProfile. |
| DiscoveryBaselineBuilder | Records provided evidence, searched sources, blocker unknowns, non-blocker unknowns, and assumptions before recursive reduction. | Updates RunFrame discovery baseline. |
| TechniqueSelector | Activates always-on techniques and triggered conditional techniques. | Produces ordered TechniqueSpec list by phase. |
| RoleRunner | Runs Proposer and Balancer turns through true subagents when supported, or role simulation when unsupported. | Produces Role conversation trace. |
| ReductionLoop | Runs recursive rounds within ModeProfile limits. | Produces ConceptLayer and CandidateUnit updates. |
| GateEvaluator | Applies closure, recomposition, cycle, and readiness rules. | Produces pass, flag, or block decisions. |
| PitchOffResolver | Compares proposal tracks in Tournament mode. | Produces proposal comparison and convergence rationale. |
| HandoffRouter | Maps verdict and tensions to next route. | Produces next-route recommendation. |

## View 4: Workflow Process View

### Main Flow

1. Invocation surface captures seed point, target context, objective, output artifact, optimization goal, and constraints.
2. Invocation surface confirms design intent and offers budget profiles.
3. DiscoveryBaselineBuilder records provided evidence, searched sources, blocker unknowns, non-blocker unknowns, and assumptions.
4. Mode surface resolves ModeProfile.
5. Technique surface resolves always-on techniques and mode-required techniques.
6. Core engine creates RunFrame.
7. For each proposal track, RoleRunner runs Proposer pass.
8. Technique surface runs phase hooks that apply after proposal formation.
9. RoleRunner runs Balancer pass with named objection categories.
10. Core engine reconciles accept, revise, reject, defer, or route decisions.
11. GateEvaluator applies closure, recomposition, cycle, and complexity rules.
12. ReductionLoop continues until round budget, closure, cycle guard, or blocker gate ends the track.
13. Tournament mode runs PitchOffResolver when more than one track remains viable.
14. Closeout techniques run: frame-expiry always, premortem when required, and navigable result check.
15. Core engine selects verdict and optimization point.
16. Trace surface emits ResultEnvelope.
17. Handoff surface recommends next route.

### Failure And Compensation Paths

| Failure | Compensation |
| --- | --- |
| Missing seed point or target context | Ask one blocker question or return block. |
| Mode override removes finite limits | Reject override and require finite tracks and rounds. |
| Technique trigger is unclear | Skip only if not always-on and record skipped reason. |
| Always-on technique cannot run | Return flag or block based on whether readiness depends on it. |
| Role loop repeats same tension | Record stable disagreement and route if blocker. |
| Pitch-off cannot justify a winner | Ask human gate or return flag with preserved alternatives. |
| Selected unit lacks recomposition proof | Reject unit or return block. |

## View 5: Decision Flow View

### Mode Selection

| Condition | Mode |
| --- | --- |
| User asks for quick pass, draft pass, or low budget | Compact |
| User gives no budget and asks for one solution | Standard |
| User asks for multiple options, competing designs, or proposal comparison | Tournament |
| User asks for maximum depth, high uncertainty, or deep review | Deep |
| User provides an existing design or plan to test | Validate |

### Technique Activation

| Technique | Activation Rule |
| --- | --- |
| Abstraction-level guard | Always active for every concept layer and candidate unit. |
| Recomposition proof | Always active for every accepted split and final selected unit. |
| Evolution profile | Always active for future-scale, extensibility, or open-endedness decisions. |
| Frame-expiry note | Always active at final synthesis. |
| Cognitive load check | Triggered when a split creates multiple fragments or coordination rules. |
| Requisite variety check | Triggered when Balancer sees overbuilding or underbuilding risk. |
| Boundary-object check | Triggered when multiple roles, teams, institutions, or audiences must share a concept. |
| Concept-vs-knowledge status | Triggered when a unit depends on weak evidence or unresolved domain knowledge. |
| Premortem pass | Active in Standard, Tournament, Deep, and medium/high-risk Validate; skipped in Compact unless requested. |
| Set-based tournament | Active only in Tournament mode. |
| Navigable result check | Active in every mode before verdict. |

### Readiness Decision

| Evidence | Verdict |
| --- | --- |
| Selected unit is closed, recomposable, proportionate, and no blocker tension remains. | pass |
| Selected unit is usable, but non-blocker tensions, deferred decisions, or validation gaps remain. | flag |
| No responsible optimization point can be selected without user decision, missing evidence, or cross-layer investigation. | block |

## View 6: Dependency Interface View

### ModeProfile Interface

```text
mode_id: compact | standard | tournament | deep | validate
proposal_tracks: finite integer
role_conversations: Proposer and Balancer, or Balancer-led validate with optional Proposer repair
recursive_rounds: finite integer or finite range
technique_policy: always-on, triggered, mode-required, skipped-with-reason
pitch_off_policy: none | required | optional
human_gate_policy: blockers | contested optimization | no justified winner | periodic
closeout_policy: frame-expiry, premortem requirement, route recommendation
```

### TechniqueSpec Interface

```text
technique_id: stable id
type: gate | lens | classifier | mode mechanic | check | closeout
phase: setup | concept mapping | proposal | balance | closure | pitch-off | final synthesis | handoff
trigger: always | condition | mode-required | risk-required | user-requested
inputs: state fields the technique may inspect
outputs: trace fields the technique must emit
failure_behavior: pass | flag | block | skip-with-reason | route
```

Detailed contracts for each included technique live in arcana/distill/development/techniques/README.md.

### Core Hook Interface

| Hook | Phase | Allowed Technique Types | Required State |
| --- | --- | --- | --- |
| after_intent_confirmation | setup | lens, classifier | RunFrame draft |
| before_layer_split | concept mapping | classifier, lens | parent ConceptLayer |
| after_proposer_pass | proposal | gate, check, lens | TrackState and candidate units |
| after_balancer_pass | balance | check, lens | Balancer objections |
| before_accept_split | closure | gate, classifier | CandidateUnit and recomposition proof |
| before_pitch_off | pitch-off | mode mechanic | viable TrackStates |
| before_verdict | final synthesis | closeout, gate | selected CandidateUnit |
| after_verdict | handoff | closeout, route | ResultEnvelope |

### Trace Interface

Every run must emit:

- mode profile snapshot,
- objective-output artifact pair and revision reason when changed,
- discovery baseline,
- technique activation list,
- role conversation trace,
- reduction trace,
- technique pack trace,
- closure and recomposition proof,
- tension ledger,
- final ResultEnvelope.

Trace entries should be append-only within a run. Later reconciliation may supersede a decision, but it should not erase prior claims, objections, or tensions.

## Constraints

| Constraint | Source | Impact |
| --- | --- | --- |
| Modes are not technique packs | SIGIL-HANDOFF.md | Modes may change orchestration, but not redefine technique semantics. |
| Techniques are phase-bound | SIGIL-HANDOFF.md and LITERATURE-RESEARCH.md | Techniques must have triggers, outputs, and failure behavior. |
| Core owns verdicts | SIGIL-HANDOFF.md | Techniques and modes can flag conditions but cannot independently declare readiness. |
| No unbounded recursion | SIGIL-HANDOFF.md | All mode profiles must keep finite tracks and finite rounds. |
| Objective-output pair remains visible | CYBERALCHEMY-METHOD.md | The run may revise the target artifact, but must record why. |
| No silent promotion | invoke design contract | Registry, glossary, and runtime adapter promotion remain explicit downstream decisions. |

## Dependency And Interface Rules

| Rule ID | Rule | Applies To | Enforcement |
| --- | --- | --- | --- |
| R-001 | Every mode must compile into a ModeProfile before reduction begins. | Mode surface | Block or ask one clarification question when unresolved. |
| R-002 | Every technique must declare phase, trigger, output, and failure behavior. | Technique surface | Reject technique or record design gap. |
| R-003 | Always-on techniques cannot be skipped without a recorded gate reason. | Technique surface | Flag or block depending on readiness impact. |
| R-004 | Techniques may inspect core state only through the hook's allowed state. | Technique surface and core engine | Prevent hidden mutation and phase leakage. |
| R-005 | Mode mechanics may orchestrate tracks but cannot alter closure rules. | Mode surface | GateEvaluator owns closure and verdict. |
| R-006 | Role traces must preserve claims and objections even when reconciled. | Trace surface | Append-only trace entries. |
| R-007 | Handoff routes must follow verdict and tension ownership. | Handoff surface | Robot-Talks for cross-layer tension; Decision-Gate for blocker choice; implementation-layering or invoke plan only after usable optimization point. |
| R-008 | Result envelopes must be navigable. | Trace surface | Include where to start, what changed, unresolved gaps, and next action before pass readiness. |

## Decision Log

| Decision ID | Decision | Options Considered | Reason |
| --- | --- | --- | --- |
| D-001 | Use layered surface architecture. | Monolithic sigil process, separate mode sigils, layered surfaces. | Layered surfaces let sigil-development implement modes and techniques without blurring responsibilities. |
| D-002 | Treat modes as ModeProfiles. | Modes as commands, modes as freeform prompts, modes as profiles. | Profiles are finite, traceable, and adapter-friendly. |
| D-003 | Treat techniques as TechniqueSpecs attached to hooks. | Techniques as modes, techniques as loose advice, techniques as hook specs. | Hook specs preserve phase boundaries and auditability. |
| D-004 | Add objective-output and navigation as design-level contracts. | Leave them implicit, add as optional notes, or make them required setup and closeout evidence. | Required evidence keeps the optimizer oriented toward a usable final artifact while still allowing discovery to revise the target result. |
| D-004 | Keep verdict authority in the core engine. | Techniques decide readiness, modes decide readiness, core decides readiness. | Closure and recomposition require global run state. |
| D-005 | Require append-only traces within a run. | Mutable summary only, append-only trace, separate external log. | The sigil needs auditable role and technique reasoning. |

## Risks

| Risk ID | Risk | Mitigation | Owner |
| --- | --- | --- | --- |
| RK-001 | Technique surface becomes too heavy for Compact mode. | Compact runs always-on gates only and records skipped triggered techniques. | Sigil-development |
| RK-002 | True subagents and role simulation produce different trace quality. | Prefer true subagents when available and require the same Role Trace Contract in both paths. | Runtime adapter |
| RK-003 | Tournament mode becomes a debate without convergence. | Require option value, elimination condition, pitch-off rationale, and human gate when no winner is justified. | Core sigil engine |
| RK-004 | Techniques mutate concept state implicitly. | Restrict techniques to hook-allowed state and require emitted outputs. | Technique surface |
| RK-005 | Surface design over-specifies implementation. | Keep interfaces conceptual and defer code mechanics to sigil-development. | Invoke design |

## Downstream Planning Notes

- Sigil-development should author README.md and SKILL.md around the six surface layers.
- Runtime adapter planning should decide whether ModeProfile and TechniqueSpec are represented as explicit tables, prompt sections, or simple structured state.
- README.md and SKILL.md should summarize the technique registry but link to or preserve the detailed TechniqueSpec contracts.
- Validation examples should include one run for Standard, one Compact skip case, one Tournament convergence case, one technique-trigger case, and one block caused by missing recomposition proof.
- Implementation-layering should treat this design as Layer 1 input for candidate package authoring.

## Design Transport Notes

Carry this design into sigil-development as the interface contract between user-facing modes, techniques, and the core sigil loop.

Do not promote this design into a runtime adapter until README.md, SKILL.md, and validation examples demonstrate that the surface model is usable.

## Gate Result

- Status: pass
- Reason: The surface design defines six required views, explicit source contracts, mode and technique interfaces, dependency rules, decisions, risks, and downstream planning notes. Remaining work belongs to sigil-development packaging and validation.
