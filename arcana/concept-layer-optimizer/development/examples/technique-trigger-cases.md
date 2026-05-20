# Example: Technique Trigger Cases

## Purpose

These compact fixtures validate that techniques activate for concrete reasons and do not become mandatory clutter.

The current TechniqueSpec pack maps older literature labels into package-native techniques:

| Literature Label | Package Technique |
| --- | --- |
| Cynefin-style complexity sensemaking | `concept_vs_knowledge_status` and `boundary_object_check` |
| TRIZ contradiction search | `requisite_variety_check` |
| Morphological analysis | `set_based_tournament` and proposal-track comparison |
| Set-based design | `set_based_tournament` |
| Wardley-map style evolution/context placement | `evolution_profile` and `frame_expiry_note` |
| Navigable-result review | `navigable_result_check` |

## Case A: Boundary And Knowledge Status Trigger

### Prompt

Optimize a governance workflow used by product, compliance, and infrastructure teams. Output artifact: decision record.

### Expected Output Body

```markdown
## Concept Layer Optimizer Result

- Target context: multi-team governance workflow.
- Objective and output artifact: clarify the first shared unit; output artifact is a decision record.
- Mode and budget: Standard.
- Verdict: flag.
- Current smallest coherent unit: shared approval checkpoint.
- Technique pack trace:
  - boundary_object_check: triggered because product, compliance, and infrastructure use "approval" differently; flag until shared meaning and local variation are recorded.
  - concept_vs_knowledge_status: triggered because compliance constraints are asserted but not evidenced; classify as concept claim, not knowledge-backed unit.
  - recomposition_proof: pass with caveat; checkpoint recomposes only if role-specific local meanings are preserved.
- Tension ledger:
  - unresolved: approval authority differs by actor.
- Navigation guide: start by recording the decision question and actor meanings, then route unresolved authority to decision-gate.
- Next route: decision-gate.
```

### Expected Verdict

flag

## Case B: Requisite Variety And TRIZ-Style Contradiction Trigger

### Prompt

Optimize a lightweight support triage design that must handle urgent incidents but stay simple for a two-person team.

### Expected Output Body

```markdown
## Concept Layer Optimizer Result

- Target context: support triage for a two-person team.
- Objective and output artifact: select a first workflow; output artifact is a workflow design.
- Mode and budget: Standard.
- Verdict: pass.
- Current smallest coherent unit: severity-tagged intake queue.
- Technique pack trace:
  - requisite_variety_check: triggered; external variety is incident urgency, customer impact, and escalation need; internal variety is severity tag plus owner assignment; verdict is proportionate.
  - cognitive_load_check: pass; one severity field and one owner field avoid a full incident-management platform.
  - evolution_profile: pass; expected variants are escalation policy and SLA review after repeated incidents.
- Deferred complexity: rota automation, dashboards, and full incident command.
- Next route: task-session.
```

### Expected Verdict

pass

## Case C: Morphological / Set-Based Tournament Trigger

### Prompt

Compare three ways to structure a planning artifact: by lifecycle phase, by actor, or by concept layer.

### Expected Output Body

```markdown
## Concept Layer Optimizer Result

- Target context: planning artifact structure.
- Objective and output artifact: choose structure; output artifact is an architecture design.
- Mode and budget: Tournament.
- Proposal tracks: 3.
- Verdict: pass.
- Technique pack trace:
  - set_based_tournament: triggered by multiple viable structures.
  - Track lifecycle phase: strong for execution, weak for conceptual discovery.
  - Track actor: strong for responsibility, weak for recomposition.
  - Track concept layer: strong for reduction and recomposition, selected.
  - morphological-analysis mapping: represented by comparing structure dimensions across tracks.
- Current smallest coherent unit: concept-layer map with responsibility and recomposition note.
- Next route: implementation-layering.
```

### Expected Verdict

pass

## Case D: Wardley-Style Evolution Placement Trigger

### Prompt

Optimize whether to build custom telemetry storage or start with a repository-local JSONL ledger.

### Expected Output Body

```markdown
## Concept Layer Optimizer Result

- Target context: early observability storage.
- Objective and output artifact: choose storage boundary; output artifact is implementation plan.
- Mode and budget: Standard.
- Verdict: pass.
- Current smallest coherent unit: repository-local JSONL signal ledger.
- Technique pack trace:
  - evolution_profile: triggered; storage may evolve from local evidence to queryable reporting.
  - frame_expiry_note: pass; custom storage becomes relevant when retention, query volume, or multi-repo reporting invalidates JSONL.
  - requisite_variety_check: pass; current external variety is low enough for JSONL.
- Deferred complexity: database, dashboard, and cross-repo sync.
- Next route: implementation-layering.
```

### Expected Verdict

pass

## Case E: Navigable Result Downgrade Trigger

### Prompt

Review an output that includes a correct concept map but no start point, decisions, or next action.

### Expected Output Body

```markdown
## Concept Layer Optimizer Result

- Target context: validation of existing concept map.
- Objective and output artifact: review navigability; output artifact is validation report.
- Mode and budget: Validate.
- Verdict: flag.
- Technique pack trace:
  - navigable_result_check: triggered always; downgrade because the result lacks start-here, use guidance, unresolved tensions, and next action.
- Current smallest coherent unit: existing concept map, usable only after navigation closeout is added.
- Navigation guide: start at the selected unit, read recomposition proof, then follow next route.
- Next route: invoke plan.
```

### Expected Verdict

flag
