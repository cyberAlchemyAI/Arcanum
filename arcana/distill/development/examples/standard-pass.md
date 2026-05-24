# Example: Standard Mode Pass

## Prompt

Use Distill in Standard mode.

Seed point: design a repository-local agent observability system.
Target context: a small open-source framework where agent runs should leave reusable evidence.
Expected output artifact: implementation plan.
Optimization goal: find the smallest coherent unit that proves useful observability without overbuilding a full analytics platform.

## Relevant Input Context

- The system should record which capability ran.
- It should preserve enough evidence for reflection later.
- The first version should be easy to validate manually.
- The user expects future growth into thresholds and reflection.

## Expected Output

```markdown
## Distill Result

- Target context: repository-local agent observability for a small framework.
- Objective and output artifact: prove useful invocation evidence; output artifact is an implementation plan.
- Mode and budget: Standard; one proposal track, Proposer and Balancer roles, two recursive rounds.
- Proposal tracks: 1 track, role simulation acceptable unless runtime subagents are available.
- Recursive rounds: 2 / 2.
- Verdict: pass.
- Role conversation trace:
  - Proposer claim: start with a local invocation envelope and append-only signal ledger.
  - Evidence or assumption: framework already has reusable capabilities and wants operational memory.
  - Balancer objection: avoid analytics dashboards, dashboards are premature complexity.
  - Reconciliation decision: accept envelope plus JSONL ledger as the unit; defer dashboards.
- Current smallest coherent unit: invocation signal recorder.
- Optimization point: the recorder is small enough to validate in one run but large enough to preserve capability id, mode, target artifact, result status, and reflection recommendation.
- Concept layer map:
  - Agent capability governance
  - Repository-local observability
  - Invocation evidence capture
  - Invocation signal recorder
- Technique pack trace:
  - abstraction_level_guard: pass; selected unit is operational evidence capture, not governance policy.
  - recomposition_proof: pass; signal recorder recomposes into observability by feeding ledgers and reflection.
  - evolution_profile: pass; expected evolution is thresholds, reflection reports, and adapter coverage.
  - cognitive_load_check: pass; one envelope and one ledger are easier to operate than dashboard/report/threshold stack.
  - premortem_pass: pass; likely failure is missing fields, guardrail is a required signal schema.
  - navigable_result_check: pass; next route and start point are explicit.
- Closure and recomposition proof: the recorder has a clear input, an invocation summary; a clear output, a signal row; and it recomposes upward into reflection by giving future runs comparable evidence.
- Evolution profile: grows through signal fields, thresholds, and reflection reports after the first recorder proves meaningful execution.
- Deferred complexity: dashboards, automated reflection, cross-repository sync, and analytics queries are deferred.
- Tension ledger:
  - resolved: observability should be operational evidence first, not analytics product.
  - unresolved: exact threshold values need real usage.
- Premortem: the first version may emit noisy fields; guardrail is a meaningful-execution definition.
- Frame-expiry note: if the framework needs multi-repo compliance reporting, this unit must be revisited.
- Navigation guide: start with the invocation envelope template, validate one run, then add threshold rules.
- Next route: implementation-layering.
```

## Expected Verdict

pass

## Acceptance Notes

- The output names an implementation plan as the artifact.
- It selects a smallest coherent unit that is not a meaningless fragment.
- It defers future scale while preserving an evolution boundary.
- It gives a navigable next route.
