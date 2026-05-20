# Example: Negative And Drift Cases

## Case A: Infinite Reduction Block

### Prompt

Keep reducing an approval workflow until every term is atomic.

### Expected Output Body

```markdown
## Concept Layer Optimizer Result

- Target context: approval workflow design.
- Objective and output artifact: find a first workflow unit; output artifact is workflow design.
- Mode and budget: Standard.
- Recursive rounds: 2 / 2.
- Verdict: block.
- Current smallest coherent unit: none selected.
- Technique pack trace:
  - abstraction_level_guard: block; proposed fragments "approve", "review", "yes", and "no" are operations or labels without workflow responsibility.
  - recomposition_proof: block; fragments require hidden glue to reconstruct the approval workflow.
  - cycle_guard_triggered: same split reappeared with different names and no new structure.
- Tension ledger:
  - blocker: user goal asks for atomization beyond meaningful closure.
- Navigation guide: stop reduction at "approval checkpoint" or ask user to change the objective.
- Next route: decision-gate.
```

### Expected Verdict

block

## Case B: Premature Complexity Flag

### Prompt

Design the first unit for a personal note review workflow, but include plugin APIs, role permissions, audit logging, and multi-workspace sync.

### Expected Output Body

```markdown
## Concept Layer Optimizer Result

- Target context: personal note review workflow.
- Objective and output artifact: choose first coherent unit; output artifact is implementation plan.
- Mode and budget: Standard.
- Verdict: flag.
- Current smallest coherent unit: review queue with status and next action.
- Technique pack trace:
  - cognitive_load_check: flag; proposed plugin APIs, permissions, audit logging, and sync increase coordination burden.
  - evolution_profile: flag; future scale is hypothetical and user has not confirmed multi-actor use.
  - requisite_variety_check: overfit; internal mechanisms exceed external variety.
- Deferred complexity: plugin APIs, permissions, audit logging, multi-workspace sync.
- Navigation guide: implement review queue first, then validate repeated multi-workspace need.
- Next route: implementation-layering.
```

### Expected Verdict

flag

## Case C: Missing Evolution Profile Flag

### Prompt

Create an extensible policy engine for a two-rule content checklist.

### Expected Output Body

```markdown
## Concept Layer Optimizer Result

- Target context: two-rule content checklist.
- Objective and output artifact: choose first structure; output artifact is architecture design.
- Mode and budget: Standard.
- Verdict: flag.
- Current smallest coherent unit: explicit checklist evaluator.
- Technique pack trace:
  - evolution_profile: flag; "extensible policy engine" assumes future variants without named pressure.
  - requisite_variety_check: overfit; two rules do not justify engine abstraction.
  - frame_expiry_note: pass; engine may become valid when rules grow, actors differ, or governance review appears.
- Deferred complexity: policy engine, plugin rules, versioned governance.
- Next route: task-session.
```

### Expected Verdict

flag

## Case D: Lost Recomposition Block

### Prompt

Split a data import workflow into parser, validator, normalizer, mapper, resolver, writer, and notifier, but do not define how they combine.

### Expected Output Body

```markdown
## Concept Layer Optimizer Result

- Target context: data import workflow.
- Objective and output artifact: select first implementation structure; output artifact is architecture design.
- Mode and budget: Standard.
- Verdict: block.
- Current smallest coherent unit: none selected.
- Technique pack trace:
  - recomposition_proof: block; split names components but does not prove ordering, ownership, inputs, outputs, or error flow.
  - cognitive_load_check: flag; seven fragments increase coordination without a verified first unit.
  - abstraction_level_guard: flag; mapper and resolver mix function and policy levels.
- Navigation guide: repair by selecting "validated import transaction" as the first coherent unit or define the missing recomposition contract.
- Next route: invoke design.
```

### Expected Verdict

block

## Case E: Objective-Output Artifact Drift

### Prompt

Optimize an architecture design for a new sigil, but discovery shows the real blocker is choosing whether the output should be a decision record or implementation plan.

### Expected Output Body

```markdown
## Concept Layer Optimizer Result

- Target context: new sigil development.
- Objective and output artifact: original artifact was architecture design; revised artifact is decision record because discovery found a blocker choice.
- Mode and budget: Validate.
- Verdict: flag.
- Current smallest coherent unit: decision on lifecycle route.
- Technique pack trace:
  - concept_vs_knowledge_status: triggered; architecture assumptions depend on unresolved lifecycle choice.
  - navigable_result_check: pass after artifact revision is recorded.
- Tension ledger:
  - unresolved: whether the next artifact is implementation plan or decision record.
- Navigation guide: start with the decision record; architecture can resume after the route is selected.
- Next route: decision-gate.
```

### Expected Verdict

flag

## Case F: Navigation Downgrade

### Prompt

Return a concept map and selected unit, but omit what the user should do next.

### Expected Output Body

```markdown
## Concept Layer Optimizer Result

- Target context: plan review.
- Objective and output artifact: improve a plan; output artifact is validation report.
- Mode and budget: Validate.
- Verdict: flag.
- Current smallest coherent unit: selected plan slice.
- Technique pack trace:
  - navigable_result_check: flag; technically complete result lacks start-here path, artifact use, unresolved tensions, and next action.
- Navigation guide: start with the selected plan slice, apply the recomposition proof, resolve listed tensions, then route to implementation-layering.
- Next route: implementation-layering.
```

### Expected Verdict

flag
