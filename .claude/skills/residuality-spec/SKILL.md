---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/residuality-spec/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: residuality-spec
description: "Use when: defining or hardening a specification through stressor analysis, desired residue, degradation behavior, attractor discovery, and resilience decisions."
argument-hint: "<target-scope> [--output <path>] [--mode interview|audit|patch-plan] [--dry-run]"
tier: arcana
domain: resilience-specification
version: 0.1.0
origin: inspired by residuality-style stressor and residue analysis for resilient specification
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion, Agent
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
