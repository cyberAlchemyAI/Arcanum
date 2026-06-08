---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/distill/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: distill
description: "Use when: reducing a broad model, architecture, design, implementation plan, or workflow into the smallest coherent concept unit that still fits the user's target context and can recompose into the larger system."
argument-hint: "<seed-point> [--mode compact|standard|tournament|deep|validate] [--rounds <n>] [--tracks <n>]"
tier: arcana
domain: planning-optimization
version: 0.1.0
origin: created through Arcanum invoke and sigil-development planning from Distill design packet
allowed-tools: Read, Write, Glob, Grep, Agent, AskUserQuestion
---

# Sigil: Distill

<objective>
Distill a model, architecture, design, or plan by recursively extracting concept layers, selecting the smallest coherent unit that still fits the user's target context, and proving how that unit recomposes into the larger system before downstream implementation begins.
</objective>

<logic-type>
Arcana: recursive planning optimization with role-based critique, finite reduction rounds, technique gates, and lifecycle routing.
</logic-type>

<applicability>
Use this sigil when:

- an idea, architecture, model, plan, or workflow is too broad to implement responsibly,
- the user wants planning before committing to one solution,
- a solution may be overbuilt, underbuilt, or prematurely optimized,
- the work needs a clear relationship between broad concept layers and the first coherent unit,
- multiple possible designs should compete before convergence,
- the output needs a navigable next route such as implementation-layering, robot-talks, decision-gate, invoke design, invoke plan, or task-session.
</applicability>

<non-applicability>
Do not use this sigil when:

- the user already has one small deterministic edit,
- direct implementation is safer than conceptual decomposition,
- the request only needs a summary or explanation,
- there is no meaningful output artifact to optimize toward,
- the user needs factual discovery as the primary work rather than planning optimization.
</non-applicability>

<inputs>
Expected inputs, if available:

- seed point: starting concept, model, architecture, design, plan, problem, or workflow,
- target context: the size and purpose the result must serve,
- output artifact: data model, architecture design, implementation plan, code structure, decision record, research map, technique spec, or other concrete artifact,
- optimization goal: clarity, scope, architecture, planning depth, model quality, implementation readiness, or another stated goal,
- constraints: time, cost, quality, governance, risk, implementation, audience, or domain limits,
- existing artifacts: specs, notes, code, diagrams, plans, or decisions that should count as evidence,
- budget preference: Compact, Standard, Tournament, Deep, or Validate.
</inputs>

<first-action>
Before decomposing, confirm intent and budget:

```text
I understand the design intent as: <seed point>.
Target context: <context size and purpose>.
Expected output artifact: <artifact shape>.
Optimization goal: <goal>.
Recommended budget: Standard - one proposal track, Proposer and Balancer roles,
two recursive rounds, then reconciliation.
Do you want Compact, Standard, Tournament, Deep, or Validate?
```

If the user does not choose, proceed with Standard and record that assumption.
</first-action>

<modes>
| Mode | Use When | Budget |
| --- | --- | --- |
| Compact | The user wants a quick bounded pass. | One proposal track, one recursive round, always-on gates only. |
| Standard | Default planning depth is enough. | One proposal track, Proposer and Balancer roles, two recursive rounds, one reconciliation pass. |
| Tournament | Multiple designs should compete. | Three proposal tracks by default, each balanced independently, then set-based pitch-off. |
| Deep | The context is broad, high-risk, or strategically important. | Two or more tracks, three rounds by default, stronger cycle checks, premortem, and possible human gates. |
| Validate | An existing design needs review. | Balancer-led critique with optional Proposer repair and pass, flag, or block verdict. |

All modes must keep finite proposal tracks, finite recursive rounds, cycle guards, and skipped-technique reasons.
</modes>

<runtime-role-policy>
Use true subagents whenever the active runtime supports them for Proposer and Balancer roles. If subagents are unavailable, run labeled Proposer and Balancer passes in one agent.

Both paths must preserve the same role trace:

- Proposer claim,
- evidence or assumption,
- Balancer objection category,
- reconciliation decision,
- stable disagreement, if one remains.
</runtime-role-policy>

<process>
1. Confirm design intent, target context, output artifact, optimization goal, and budget.
2. Build a discovery baseline from provided artifacts, constraints, blocker unknowns, non-blocker unknowns, and assumptions.
3. Resolve the mode profile: proposal tracks, role conversations, recursive rounds, pitch-off behavior, human gates, and closeout policy.
4. Identify the broadest concept layer that contains the user's frame and label its abstraction level.
5. For each proposal track, run a Proposer pass that suggests a concept layer split and candidate smallest coherent unit.
6. Run always-on techniques:
   - abstraction-level guard,
   - recomposition proof,
   - evolution profile when future scale or extensibility appears,
   - frame-expiry note,
   - navigable result check.
7. Run triggered techniques when conditions appear:
   - cognitive load check,
   - requisite variety check,
   - boundary-object check,
   - concept-vs-knowledge status,
   - premortem pass,
   - set-based tournament.
8. Run a Balancer pass using named objection categories.
9. Reconcile each objection as accept, revise, reject, defer, or route.
10. Test candidate units for closure:
    - responsibility,
    - named inputs and outputs,
    - explicit abstraction level,
    - recomposition into the upper layer,
    - no hidden glue,
    - no smuggled future scale,
    - no meaning loss when split further.
11. Continue recursive rounds until the selected budget ends, closure is reached, a cycle guard fires, or a blocker appears.
12. In Tournament mode, compare viable tracks by fit, option value, risk, cost, assumptions, and elimination conditions.
13. Select the optimization point where the unit is small enough to work with and large enough to remain meaningful in context.
14. Run closeout techniques: recomposition proof, frame-expiry note, premortem when required, navigable result check.
15. Return pass, flag, or block and route the result to the next lifecycle owner.
</process>

<technique-pack>
Use the detailed TechniqueSpec contracts in `development/techniques/README.md`.

Technique activation trace must include:

- technique id,
- hook,
- activation reason,
- inspected state,
- emitted output,
- decision,
- readiness effect.
</technique-pack>

<cycle-guards>
Stop or gate when:

- the recursive round budget is reached,
- the same split reappears with new names but no new structure,
- a round adds terminology without improving closure, recomposition, or risk handling,
- Proposer and Balancer keep trading the same tension without new evidence,
- a smaller concept fails closure but is repeatedly reintroduced,
- further reduction would damage the user-selected context.

When a guard triggers, record the reason and either choose the current best optimization point or ask for one blocker decision.
</cycle-guards>

<complexity-balance>
Do not introduce complexity because it is elegant, reusable, or theoretically complete.

Complexity is allowed only when the current context has:

- a named tension,
- a concrete failure mode, or
- a confirmed evolution pressure that the simpler unit cannot responsibly handle.

Before deferring future scale, ask what kind of evolution the system, solution, or plan is likely to have. Natural evolution pressure can justify a small extension boundary when it is concrete: expected variants, repeated integrations, growing policy rules, multiple actors, scaling volume, migration needs, or governance review.

When the evolution profile is unknown, preserve a clear boundary and defer the heavier mechanism.
</complexity-balance>

<quality-bar>
A successful execution must:

- confirm objective and output artifact before recursive decomposition,
- select or infer a finite mode budget,
- build a discovery baseline before proposing layers,
- preserve Proposer/Balancer trace,
- classify Balancer objections by named category,
- run always-on techniques or record why readiness is downgraded,
- activate conditional techniques only when their trigger is present,
- stop infinite reduction through cycle guards,
- select a smallest coherent unit with closure and recomposition proof,
- defer complexity that lacks a named tension or confirmed evolution profile,
- return a navigable result with start-here guidance, unresolved tensions, and next route.
</quality-bar>

<anti-patterns>
Avoid:

- reducing concepts into tiny fragments that no longer carry behavior,
- adding abstractions for elegance, reuse, or hypothetical scale,
- letting the Balancer object vaguely without a concrete category,
- treating a concept claim as knowledge-backed when evidence is weak,
- skipping the output artifact because the concept map feels complete,
- running Tournament mode without assumptions and elimination conditions,
- letting true-subagent and role-simulation paths produce different trace contracts,
- claiming pass readiness when the result has no navigation guide,
- routing to implementation when a blocker decision or cross-layer tension remains.
</anti-patterns>

<observability>
For meaningful executions, emit or prepare usage telemetry when the local observability package is available.

Recommended signal fields:

- objective-output confirmation,
- target context,
- selected mode,
- proposal tracks,
- recursive rounds,
- role execution path: true subagents or role simulation,
- techniques triggered and skipped,
- verdict,
- objective-output drift,
- navigation closeout status,
- next route.
</observability>

<output-contract>
Return:

```markdown
## Distill Result

- Target context: <context summary>
- Objective and output artifact: <objective; artifact shape>
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
</output-contract>
