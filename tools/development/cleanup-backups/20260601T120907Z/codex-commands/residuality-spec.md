# Arcanum Sigil: residuality spec

<!-- arcanum:capability-id residuality-spec -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command residuality-spec -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-residuality-spec-<UTC timestamp>`.
- `capability.id`: `residuality-spec`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `residuality-spec` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `residuality-spec`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/residuality-spec/README.md

````markdown
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
````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/residuality-spec/SKILL.md

````markdown
---
name: residuality-spec
description: "Use when: defining or hardening a specification through stressor analysis, desired residue, degradation behavior, attractor discovery, and resilience decisions."
argument-hint: "<target-scope> [--output <path>] [--mode interview|audit|patch-plan] [--dry-run]"
tier: arcana
domain: resilience-specification
version: 0.1.0
origin: inspired by residuality-style stressor and residue analysis for resilient specification
allowed-tools: Read, Write, Glob, Grep, Bash, AskQuestions, Task
---

# Sigil: Residuality Spec

<objective>
Help the user define or revise a specification by identifying stressors, deciding desired residue, specifying degradation behavior, surfacing attractors, and producing concrete spec implications.
</objective>

<logic-type>
Arcana: uncertainty exploration, resilience decision governance, and specification synthesis.
</logic-type>

<modes>
- `interview`: guide the user through stressor and residue questions.
- `audit`: inspect an existing spec and identify missing resilience behavior.
- `patch-plan`: produce exact spec additions without mutating source docs.
- `--dry-run`: return planned outputs and open decisions without writing files.
</modes>

<applicability>
Use this sigil when:

- a spec needs resilience or survivability behavior,
- a system should define acceptable degradation,
- unknown or surprising stress matters,
- non-functional behavior must be first-class in the spec,
- social, operational, environmental, or organizational stressors may change the system outcome.
</applicability>

<inputs>
Expected inputs, if available:

- target scope or feature name,
- existing spec, requirements, or product notes,
- architecture notes,
- operations notes,
- incident notes,
- support or user feedback,
- tests and monitoring docs,
- inventory entries,
- known decisions or constraints.
</inputs>

<default-output>
If the user does not provide `--output`, use the first suitable location:

1. `docs/resilience/<target-scope>-residuality.md` when `docs/resilience/` exists,
2. `docs/specs/<target-scope>-resilience.md` when `docs/specs/` exists,
3. `<feature-or-scope-folder>/RESILIENCE-SPEC.md` when a scope folder exists,
4. return a markdown report and ask where to persist it when no docs structure exists.
</default-output>

<process>
## Step 1 - Resolve Scope And Evidence

1. Resolve the target scope: feature, workflow, system, architecture slice, or spec artifact.
2. Gather relevant context without broad dumping: existing spec, architecture notes, requirements, operations notes, incidents, tests, monitoring docs, and inventory entries.
3. Establish normal intent: what the system should do under ordinary conditions.
4. Separate observed evidence, stated intent, inferred stressors, and open questions.

## Step 2 - Identify Stressors

5. Generate a stressor set across multiple dimensions:
   - technical: outage, latency, data loss, dependency failure, stale cache, deploy fault, concurrency, capacity pressure,
   - social: user misuse, unclear ownership, support load, policy conflict, operator error,
   - environmental: traffic spike, regulation change, external API behavior change, market event,
   - organizational: team handoff, missing expertise, deployment freeze, incident fatigue,
   - adversarial or accidental misuse when relevant and safe.
6. Do not claim the stressor map is exhaustive. Mark unknown or weakly evidenced areas explicitly.

## Step 3 - Decide Residue

7. For each significant stressor, ask what residue should remain:
   - behavior that must survive,
   - data that must remain trustworthy,
   - capability that may degrade,
   - capability that may stop,
   - user-visible communication,
   - operational response,
   - observability signal,
   - recovery expectation.
8. Ask one blocker-level residue decision at a time. Use concise option cards when there are multiple viable residues.
9. Route unresolved blocker trade-offs to `decision-gate` or record them as blockers.

## Step 4 - Find Attractors

10. Cluster stressors that point to the same vulnerability area.
11. Name attractors as vulnerability clusters, not isolated incidents.
12. For each attractor, identify the spec or architecture implication.

## Step 5 - Produce Spec Implications

13. Convert residues into concrete specification material:
   - resilience requirements,
   - invariants,
   - degradation behavior,
   - fallback behavior,
   - user communication rules,
   - operational response rules,
   - observability signals,
   - verification ideas,
   - decisions and open questions.
14. Create a spec patch plan or write the resilience spec when output is approved.
15. If inventory exists, recommend entries for recurring stressors, residues, attractors, incidents, and decisions.

## Step 6 - Report

16. Return a concise result with stressors analyzed, residues defined, attractors found, decisions, blockers, spec outputs, verification ideas, and next action.
</process>

<quality-bar>
A successful execution must:

- map every significant stressor to a desired residue or explicit open question,
- turn every residue into at least one concrete spec implication,
- distinguish known risks from preparation for unknown or surprising stress,
- avoid pretending the whole system can be fully mapped,
- separate observed evidence, user intent, inferred stressor, and selected residue,
- identify attractors as clusters rather than isolated anecdotes,
- avoid vague requirements like "the system must be resilient",
- avoid fear-driven overengineering.
</quality-bar>

<anti-patterns>
Avoid:

- predicting one exact future incident and calling that resilience,
- listing stressors without deciding residues,
- treating all degradation as unacceptable failure,
- hardening every component equally instead of identifying attractors,
- writing non-functional requirements without observable behavior,
- ignoring social, operational, environmental, or organizational stressors,
- mutating specs without recording decisions and trade-offs,
- presenting theoretical terms without converting them into specification behavior.
</anti-patterns>

<observability>
When `.arcanum/observability/` exists, emit post-run signals for:

- target scope,
- stressor count,
- residue count,
- attractor count,
- decisions created,
- blockers remaining,
- spec outputs created,
- verification ideas created,
- follow-up sigils recommended.
</observability>

<output-contract>
Return:

```markdown
## Residuality Spec Result

- Target scope: <scope>
- Mode: interview | audit | patch-plan
- Stressors analyzed: <count>
- Residues defined: <count>
- Degradation behaviors specified: <count>
- Attractors identified: <count>
- Decisions resolved: <count>
- Blockers remaining: <count>
- Spec output: <path or dry-run>
- Verification ideas: <count>
- Inventory updates recommended: <yes | no>
- Next action: <action>
```
</output-contract>
````
