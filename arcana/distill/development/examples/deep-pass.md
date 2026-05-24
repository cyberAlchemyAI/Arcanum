# Example: Deep Mode Pass

## Prompt

Use Distill in Deep mode.

Seed point: design the first responsible slice for an agent capability governance system.
Target context: a framework where capabilities may be reused by humans and agents across repositories.
Expected output artifact: architecture design.
Optimization goal: find a first slice that supports evolution without prematurely building the whole governance platform.

## Relevant Input Context

- The system has multiple actors: users, agents, maintainers, and lifecycle owners.
- It needs validation, observability, and promotion rules.
- Overbuilding the whole system would make the first unit hard to validate.
- Underbuilding would make future reuse brittle.

## Expected Output

```markdown
## Distill Result

- Target context: reusable agent capability governance across repositories.
- Objective and output artifact: choose the first responsible slice; output artifact is architecture design.
- Mode and budget: Deep; two proposal tracks, three recursive rounds, stronger cycle checks, premortem, and human-gate readiness.
- Proposal tracks: 2.
- Recursive rounds: 3 / 3.
- Verdict: pass.
- Role conversation trace:
  - Track A Proposer: start with full capability registry, runtime adapters, observability, validation, and promotion dashboard.
  - Track A Balancer: premature complexity; first slice cannot validate all governance layers.
  - Track A reconciliation: reject as first slice, preserve as evolution map.
  - Track B Proposer: start with capability package contract plus validation and promotion gate.
  - Track B Balancer: underbuild risk if observability is ignored.
  - Track B reconciliation: accept package contract plus observability hook as extension boundary.
- Current smallest coherent unit: capability package with validation and promotion gate.
- Optimization point: the package contract is small enough to validate with examples but large enough to preserve future registry, runtime, and reflection pathways.
- Concept layer map:
  - Agent capability governance
  - Reusable capability lifecycle
  - Candidate package with validation
  - Package contract plus promotion gate
- Technique pack trace:
  - abstraction_level_guard: pass; package contract is lifecycle architecture, not runtime execution.
  - recomposition_proof: pass; package recomposes into registry, runtime adapter, observability, and maintenance.
  - boundary_object_check: pass; users, agents, maintainers, and lifecycle owners share the package contract but use it differently.
  - requisite_variety_check: pass; validation and promotion gate handle reuse variation without building dashboard machinery.
  - cognitive_load_check: pass; one package contract plus gate reduces coordination compared with full platform.
  - premortem_pass: pass; likely failure is unvalidated promotion, guardrail is final approval gate.
  - frame_expiry_note: pass; revisit if cross-repository installs become the dominant use.
  - navigable_result_check: pass; start point, decisions, unresolved tensions, and next route are explicit.
- Closure and recomposition proof: the package has named inputs, output contract, quality bar, examples, validation, and approval gate; it recomposes upward into registry and runtime once evidence exists.
- Evolution profile: expected variants are runtime adapters, registry exposure, cross-repository install, and reflection tuning.
- Deferred complexity: promotion dashboard, multi-repo sync, automated mutation from reflection.
- Tension ledger:
  - resolved: package plus validation before registry.
  - unresolved: exact promotion owner remains a final gate.
- Premortem: unvalidated promotion may overstate readiness; guardrail is B-CLO-002.
- Frame-expiry note: if install automation becomes the first user need, revisit runtime priority.
- Navigation guide: start with package contract, validate examples, then prepare promotion recommendation.
- Next route: implementation-layering.
```

## Expected Verdict

pass

## Acceptance Notes

- Deep mode uses more rounds and tracks because the context has multiple actors and lifecycle risk.
- It still avoids building the full governance platform first.
- It names the human/final gate rather than silently resolving it.
