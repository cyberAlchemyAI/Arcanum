# Sigil Handoff: Concept Layer Optimizer

## Sigil Identity

- Name: concept-layer-optimizer
- Display name: Concept Layer Optimizer
- Candidate tier: Arcana
- Purpose: interactively optimize a model, architecture, design, or plan by reducing an initial idea into concept layers, finding the smallest coherent unit that still makes sense in the user's target context, and recomposing those units into a proportionate design.
- Owning surface: arcana/concept-layer-optimizer/
- Lifecycle owner: sigil-development

## Define Intent Record

The sigil should act like planning before committing to a solution. Its first move is not decomposition; it is intent and budget confirmation.

Recommended first prompt shape:

```text
I understand the design intent as: <seed point>.
Target context: <context size and purpose>.
Expected output artifact: <data model, architecture design, implemented code structure,
plan, decision record, research map, technique spec, or other concrete result>.
Optimization goal: <clarity, scope, architecture, planning depth, model quality,
implementation readiness, or other explicit goal>.
Recommended budget: Standard - one proposal track, two role conversations
(Proposer and Balancer), two recursive rounds, then reconciliation.
Do you want Compact, Standard, Tournament, or Deep?
```

Default when the user does not choose a budget:

- Budget profile: Standard
- Proposal tracks: 1
- Role conversations per track: 2
- Roles: Proposer and Balancer
- Recursive rounds: 2
- Pitch-off: disabled unless there are multiple proposal tracks
- Human gate: required only when blocker ambiguity remains or the best optimization point is contested

## Budget Profiles

| Budget | Proposal Tracks | Role Conversations | Recursive Rounds | Technique Pack | Pitch-Off | Human Gates |
| --- | --- | --- | --- | --- | --- | --- |
| Compact | 1 | Proposer and Balancer | 1 | always-on gates only | no | blockers only |
| Standard | 1 | Proposer and Balancer | 2 | always-on gates plus triggered Balancer checks | no | blockers or contested optimization point |
| Tournament | 3 by default, configurable | Proposer and Balancer per track | 2 per track | always-on gates plus set-based tournament mechanics | yes | no justified winner or blocker tension |
| Deep | 2 by default, configurable | Proposer and Balancer per track | 3 by default, configurable | always-on gates, triggered techniques, premortem, stronger cycle checks | optional | after each contested round and final synthesis |
| Validate | 1 existing solution | Balancer-led review with optional Proposer repair | 1 to 2 | always-on gates plus risk-triggered checks | no | blocker ambiguity or readiness downgrade |

Budget overrides must keep finite proposal tracks, finite recursive rounds, cycle guards, and a recorded reason for every skipped always-on or triggered technique.

## Inputs

| Input | Required | Validation Rule |
| --- | --- | --- |
| Seed point | yes | A starting model, architecture, design, plan, problem, or concept is stated. |
| Target context | yes | The user states or implies the context size the design must serve. |
| Output artifact | yes | The run names the concrete result it is optimizing toward, such as a data model, architecture design, implemented code structure, plan, decision record, research map, or technique spec. The artifact may be revised when discovery shows a better shape. |
| Optimization goal | yes | The run names what should be optimized: clarity, scope, architecture, planning depth, model quality, implementation readiness, or another explicit goal. |
| Budget profile | no | Defaults to Standard; must resolve proposal tracks, role conversations, recursive rounds, and pitch-off behavior. |
| Constraints | no | Any cost, time, implementation, governance, quality, or domain constraints are recorded and cannot be silently optimized away. |
| Existing artifacts | no | Referenced specs, plans, diagrams, code, or notes are treated as evidence, not as optional background. |
| Stop-rule overrides | no | User overrides may tighten max depth or round count, but may not remove cycle guards. |

## Outputs

| Output | Consumer | Contract |
| --- | --- | --- |
| Intent and budget record | User, downstream planner | Confirms seed point, target context, output artifact, selected budget, and assumptions before recursive work begins. |
| Discovery baseline | User, Proposer, Balancer | Names available evidence, blocker unknowns, non-blocker unknowns, and assumptions before recursive reduction begins. |
| Concept layer map | User, designer, implementation-layering | Shows layers from broad frame to smaller concept units, including why each layer belongs together. |
| Reduction trace | Reviewer, future sigil run | Records accepted splits, rejected splits, balancer objections, and reconciliation decisions. |
| Role conversation trace | Reviewer, future sigil run | Records Proposer claims, Balancer objections, reconciliation decisions, and stable disagreements. |
| Technique pack trace | Reviewer, future sigil run | Records active techniques, skipped techniques, trigger reasons, and gate or technique outcomes. |
| Smallest coherent unit | User, implementation-layering, task-session | Names the smallest closed concept that remains meaningful in the target context. |
| Composition model | User, architecture/design consumers | Explains how smaller concepts add or combine into the upper layer without hidden glue. |
| Tension ledger | User, robot-talks, decision-gate | Preserves unresolved conflicts, premature-complexity risks, and contested optimization points. |
| Proposal comparison | User, downstream planner | Required when multiple proposal tracks are enabled; compares candidates by fit, cost, depth, and risk. |
| Next-route recommendation | invoke, sigil-development, task-session | Recommends implementation-layering, robot-talks, decision-gate, design, plan, or task-session. |

## Output Contract

The sigil should return this shape:

```markdown
## Concept Layer Optimizer Result

- Target context: <context summary>
- Objective and output artifact: <objective being solved; artifact shape currently being optimized>
- Mode and budget: <compact | standard | tournament | deep | validate>
- Proposal tracks: <count and role summary>
- Recursive rounds: <count completed / budget>
- Verdict: pass | flag | block
- Role conversation trace: <Proposer claims, Balancer objections, reconciliation decisions>
- Current smallest coherent unit: <unit name and responsibility>
- Optimization point: <why this unit is the best size for the target context>
- Concept layer map: <broad layer to selected unit>
- Technique pack trace: <techniques run, skipped, triggered, and outcomes>
- Closure and recomposition proof: <how the unit closes and recomposes upward>
- Evolution profile: <expected evolution and smallest extension boundary>
- Deferred complexity: <what was deferred and why>
- Tension ledger: <resolved and unresolved tensions>
- Premortem: <likely failure reason and guardrail | skipped with reason>
- Frame-expiry note: <context change that invalidates this optimization point>
- Navigation guide: <where to start, what changed, what remains unresolved, and how to use the result>
- Next route: implementation-layering | robot-talks | decision-gate | invoke design | invoke plan | task-session | deferred
```

Readiness rules:

- `pass`: the selected unit is closed, recomposable, proportionate, and has no blocker tension.
- `flag`: the selected unit is usable, but a non-blocker tension, deferred decision, or validation gap remains.
- `block`: no responsible optimization point can be selected without a user decision, missing evidence, or cross-layer investigation.

## Modes

| Mode | Trigger | Behavior |
| --- | --- | --- |
| standard | Default run or one proposal requested | Uses one Proposer and one Balancer, two recursive rounds, and one reconciliation pass. |
| compact | User asks for a quick bounded pass | Uses one proposal track, one recursive round, always-on gates only, and strict deferral of uncertain complexity. |
| tournament | User wants multiple possible designs | Runs set-based proposal tracks, each with Proposer and Balancer roles, then performs evidence-based pitch-off and synthesis. |
| deep | User approves higher reasoning budget | Allows more recursive rounds, proposal tracks, conditional techniques, stronger cycle checks, premortem pass, and periodic human gates. |
| validate | Existing design needs optimization review | Tests a provided architecture, model, or plan against coherence, closure, recomposition, and premature-complexity rules. |

## Mode And Technique Model

Modes control the run shape: budget, orchestration pattern, proposal count, recursive depth, and human-gate frequency.

Techniques are internal instruments attached to phases. They do not become separate modes unless they change the whole run shape. A technique can be:

- Gate: must pass, flag, or block before the run can claim readiness.
- Lens: perspective used by the Proposer, Balancer, or Orchestrator.
- Classifier: label that prevents cross-level or evidence-status confusion.
- Check: conditional method enabled by context, risk, budget, or user request.
- Closeout: final synthesis method that affects readiness or route.
- Mode mechanic: required behavior for a specific mode.

Surface interface design is captured in arcana/concept-layer-optimizer/development/MODE-TECHNIQUE-SURFACE-DESIGN.md. Sigil-development should treat that artifact as the contract between the invocation surface, mode surface, technique surface, core sigil engine, trace surface, and handoff surface.

Detailed technique behavior is specified in arcana/concept-layer-optimizer/development/techniques/README.md. Sigil-development should treat the Technique Pack Contract below as the summary and techniques/README.md as the detailed technique source.

## Technique Pack Contract

| Technique | Type | Phase | Trigger | Output | Failure Behavior |
| --- | --- | --- | --- | --- | --- |
| Abstraction-level guard | always-on classifier | concept mapping | every concept layer and candidate unit | level label: purpose, value/constraint, capability, function, workflow/process, policy/rule, interface, artifact, or operation | Flag cross-level confusion and reject splits that treat one level as another. |
| Recomposition proof | always-on gate | recursive reduction | every accepted concept split | explanation of how smaller units combine back into the upper layer | Reject the split or record a hidden-glue tension. |
| Evolution profile | always-on lens | complexity balance | any future-scale, extensibility, or open-endedness decision | named evolution pressure and smallest extension boundary | Preserve boundary and defer heavier mechanism when profile is unknown. |
| Frame-expiry note | always-on closeout | final synthesis | optimization point selected | context change that would invalidate the current smallest coherent unit | Flag brittle finality if no expiry condition can be stated. |
| Cognitive load check | Balancer check | reduction balancing | a split creates several parts, roles, rules, or coordination paths | whether the split reduced or increased what the user must hold in mind | Merge, defer, or reject fragments that increase coordination burden without value. |
| Requisite variety check | Balancer check | complexity balance | risk of underbuilding or overbuilding appears | external variety, internal variety, fit verdict, smallest adjustment | Adjust the unit or record overfit/underfit tension. |
| Boundary-object check | conditional check | multi-actor framing | multiple roles, teams, institutions, or audiences must share the concept | stable shared meaning plus local-variation allowance | Flag stakeholder-boundary tension or route to robot-talks. |
| Concept-vs-knowledge status | uncertainty classifier | candidate assessment | a unit depends on weak evidence, novelty, or unresolved domain knowledge | status: concept claim or knowledge-backed unit | Route blocker uncertainty to research, decision-gate, or deferred gap. |
| Premortem pass | closeout | final synthesis | standard, tournament, deep, or medium/high-risk validate runs | likely failure reason for the selected optimization point | Add guardrail, route tension, or downgrade readiness. |
| Set-based tournament | mode mechanic | tournament mode | multiple proposal tracks are enabled | assumptions, option value, elimination condition, and convergence rationale for each track | Keep options open or ask for a human gate if no winner is justified. |
| Navigable result check | closeout | final synthesis | every run | where to start, what changed, unresolved gaps, and how to use the result | Flag outputs that are technically complete but hard for a user or future agent to act on. |

## Balancer Objection Categories

The Balancer should not object vaguely. Every objection should name at least one category:

- lost recomposition,
- missing input or output,
- wrong abstraction level,
- unconfirmed evolution profile,
- excessive cognitive load,
- external variety not handled,
- internal complexity greater than needed,
- stakeholder boundary ambiguity,
- concept claim treated as knowledge,
- validation burden,
- hidden glue,
- premature complexity,
- brittle minimalism.

## Role Trace Contract

Each proposal track should record:

- Proposer claim: candidate layer split, selected unit, and rationale.
- Evidence or assumption: what the claim depends on.
- Balancer objection: category, concrete concern, and affected unit.
- Reconciliation decision: accept, revise, reject, defer, or route.
- Stable disagreement: any repeated tension that did not change after a round.

Stable disagreement is not a failure by itself. It becomes a block only when it prevents selecting a responsible optimization point.

## Interaction Contract

| Interaction | Producer | Consumer | Failure Behavior |
| --- | --- | --- | --- |
| Intent confirmation | Orchestrator | User | Block if the seed point or target context is contradictory. |
| Budget offer | Orchestrator | User | Default to Standard when unanswered; record the assumption. |
| Proposal pass | Proposer | Balancer, Orchestrator | Flag if a proposal introduces concepts that do not serve the target context. |
| Counter-balance pass | Balancer | Proposer, Orchestrator | Record objections as tensions; do not discard proposals without rationale. |
| Recursive reduction | Proposer and Balancer | Orchestrator | Stop when splitting loses meaning, repeats a prior state, or exceeds budget. |
| Pitch-off | Proposal tracks | Orchestrator, User | Required only for multiple proposal tracks; defer to human gate if no winner is justified. |
| Tension resolution | Orchestrator or Robot-Talks | User, downstream route | Route to robot-talks when cross-layer conflict needs independent investigation. |

## Operating Model

1. Confirm design intent and budget.
2. Confirm the objective-output artifact pair: what problem is being solved and what artifact shape should exist after the run.
3. Build a cheap discovery baseline from provided artifacts, known constraints, blocker unknowns, and assumptions.
4. Normalize the seed point into a working frame with target context, desired outcome, output artifact, and constraints.
5. Identify the broadest concept layer that can reasonably contain the frame and label its abstraction level.
6. Ask what smaller concepts must combine to make that layer work.
7. For each candidate smaller concept, test whether it has a coherent responsibility, inputs, outputs, abstraction level, evolution profile, and recomposition path.
8. Run always-on Technique Pack gates and any triggered conditional techniques.
9. Reject reductions that only create naming fragments, hidden glue, premature optimization, context-free abstractions, or unnecessary cognitive load.
10. Continue recursive rounds within the approved budget.
11. Select the optimization point where the unit is smallest enough to work with but large enough to remain meaningful in context.
12. Run closeout techniques, including frame-expiry, premortem when enabled, and navigable result check.
13. Recompose the selected unit upward and verify that adding or combining units explains the original layer.
14. Return the concept map, technique pack trace, smallest coherent unit, deferred complexity, tensions, navigation guide, and next route.

## Closure Test

A candidate smallest unit is closed only when all of these hold:

- It has one clear responsibility in the target context.
- Its inputs and outputs can be named without inventing unexplained support systems.
- Its abstraction level is explicit and not confused with another level.
- It can be combined with sibling units to reconstruct the next upper layer.
- Its recomposition proof does not depend on hidden glue.
- Splitting it further would remove behavior, meaning, or decision value needed by the current context.
- It does not smuggle future scale, governance, automation, or optimization into the first workable unit.

## Complexity Balance Rule

The sigil should not introduce complexity because it is elegant, reusable, or theoretically complete. It may introduce complexity only when the current context has a named tension that the simpler unit cannot responsibly handle.

The sigil should still strive for open-endedness. Before deferring future scale, it should ask what kind of evolution the system, solution, or plan is likely to have. Natural evolution pressure can justify a small extension boundary when the pressure is concrete, such as expected variants, repeated integrations, growing policy rules, multiple actors, scaling volume, migration needs, or governance review.

Future scale is in scope only when the evolution profile is named and the proposed complexity is the smallest structure that keeps the current unit from becoming brittle. When the evolution profile is unknown, the sigil should preserve a clear boundary and defer the heavier mechanism.

When the Balancer suspects overbuilding or underbuilding, it should run the requisite variety check: name the external variation the unit must handle, name the internal mechanisms proposed to handle it, and classify the result as underfit, overfit, or proportionate.

Complexity is deferred when:

- it only benefits hypothetical future scale,
- it assumes an evolution profile the user has not confirmed,
- it requires concepts that the user has not asked to reason about yet,
- it makes the first coherent unit harder to validate,
- it creates more coordination cost than it removes,
- the Balancer cannot tie it to a concrete failure mode.

## Cycle And Infinite Reduction Guards

The sigil must stop or gate when any guard triggers:

- Max recursive rounds for the selected budget are reached.
- The same concept split appears twice with different names but no new structure.
- A round adds terminology without improving closure, recomposition, or risk handling.
- The Proposer and Balancer keep trading the same tension without new evidence.
- A smaller concept fails the closure test but is repeatedly reintroduced.
- The user-selected context would be damaged by further reduction.

When a guard triggers, the sigil records the reason and either chooses the current best optimization point or asks the user for a single blocker decision.

## Runtime Adapter Expectations

| Expectation | Required | Notes |
| --- | --- | --- |
| First-turn intent and budget confirmation | yes | Must occur before recursive decomposition. |
| Objective-output artifact confirmation | yes | Must name what the run is solving and what artifact shape the result should support. |
| Configurable role conversations | yes | Default is two role conversations: Proposer and Balancer. |
| Multiple proposal tracks | yes | Required for tournament mode; optional elsewhere. |
| Recursive round budget | yes | Each run must have a finite round limit. |
| Technique pack execution | yes | Adapter must run always-on techniques and record conditional techniques that were triggered or skipped. |
| Balancer objection categories | yes | Objections must cite concrete categories, not generic skepticism. |
| Set-based tournament behavior | yes for tournament mode | Proposal tracks must state assumptions, option value, and elimination conditions. |
| Premortem support | yes | Required for standard, tournament, deep, and medium/high-risk validate runs; skipped in compact unless requested. |
| Cycle detection | yes | Adapter must track repeated concepts, repeated tensions, and budget exhaustion. |
| Role simulation fallback | yes | If subagents are unavailable, run labeled Proposer and Balancer passes in one agent. |
| Robot-Talks handoff | no | Use when unresolved tensions span multiple layers or need independent investigation. |
| Decision-Gate handoff | no | Use when a blocker-level choice prevents selecting an optimization point. |

## Observability

| Signal | Trigger | Payload Summary |
| --- | --- | --- |
| budget_selected | After setup | Selected profile, proposal tracks, role conversations, recursive rounds, pitch-off setting. |
| objective_output_confirmed | After setup | Objective, output artifact, whether it was user-stated or inferred, and any revision reason. |
| reduction_round_completed | After each recursive round | Layer count, candidate units, accepted splits, rejected splits, balancer objections. |
| technique_pack_completed | After each technique pack pass | Techniques run, techniques skipped, triggers, and gate/technique outcomes. |
| closure_test_completed | For each candidate smallest unit | Closure result, failure reasons, recomposition evidence. |
| premortem_completed | When premortem runs | Likely failure reason, added guardrail, downgraded readiness, or routed tension. |
| cycle_guard_triggered | Any guard fires | Guard type, repeated state summary, selected remediation. |
| optimization_point_selected | Final synthesis | Chosen unit, context fit, deferred complexity, confidence, unresolved tensions. |
| handoff_recommended | Closeout | Next route and rationale. |

## Validation Examples

| Example | Expected Result |
| --- | --- |
| User asks to optimize a broad architecture plan with no budget choice. | Sigil confirms intent, defaults to Standard, produces one concept layer map and one smallest coherent unit. |
| User asks for three competing designs. | Sigil runs tournament mode with three proposal tracks, each balanced independently, then returns pitch-off comparison. |
| Proposer keeps reducing "approval workflow" into terms that no longer carry behavior. | Balancer flags loss of closure; sigil stops at the last meaningful unit and records rejected splits. |
| Balancer identifies that the smallest unit depends on contradictory product and infrastructure assumptions. | Sigil records a tension and routes to robot-talks or decision-gate instead of pretending the unit is ready. |
| A split turns one meaningful workflow into six fragments and more coordination rules. | Cognitive load check flags increased burden; sigil merges or defers fragments. |
| A multi-team governance design has different meanings for policy, operations, and review roles. | Boundary-object check records stable shared meaning and local variation, or routes unresolved tension. |
| A tournament proposal remains attractive but cannot name its elimination condition. | Set-based tournament keeps it open only if budget allows; otherwise asks for a human gate or records the gap. |
| User starts by asking for an architecture, but discovery shows the first responsible output is a decision record. | Sigil revises the objective-output pair, records the reason, and optimizes toward the decision record before downstream architecture. |
| Final output contains a correct concept map but no reading path or next action. | Navigable result check flags the result and adds a navigation guide before pass readiness is claimed. |

## Sigil-Development Handoff

- Handoff status: ready
- Handoff notes: This define artifact is ready for sigil-development to turn into README.md and SKILL.md. Do not register or promote the sigil until lifecycle validation examples pass.

## Gate Result

- Status: pass
- Reason: Sigil identity, purpose, inputs, outputs, mode model, technique pack, interaction contract, runtime expectations, observability, and validation examples are explicit. Remaining naming and budget refinements are non-blocking lifecycle decisions.
