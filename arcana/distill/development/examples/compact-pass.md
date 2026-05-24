# Example: Compact Mode Pass

## Prompt

Use Distill in Compact mode.

Seed point: improve a small task handoff checklist.
Target context: one maintainer handing work to another agent.
Expected output artifact: checklist structure.
Optimization goal: find the smallest checklist that still makes the handoff usable.

## Relevant Input Context

- The user wants a quick pass.
- The handoff only needs enough structure to continue work.
- There is no multi-team governance or high-risk architecture decision.

## Expected Output

```markdown
## Distill Result

- Target context: one maintainer handing a task to another agent.
- Objective and output artifact: make handoff usable; output artifact is checklist structure.
- Mode and budget: Compact; one proposal track, one recursive round, always-on gates only.
- Proposal tracks: 1.
- Recursive rounds: 1 / 1.
- Verdict: pass.
- Role conversation trace:
  - Proposer claim: use a five-field handoff checklist.
  - Balancer objection: avoid adding validation matrix or registry route for a small handoff.
  - Reconciliation decision: accept minimal checklist.
- Current smallest coherent unit: task continuation checklist.
- Optimization point: five fields are enough to preserve next action without turning the handoff into a full work-pack.
- Concept layer map:
  - Work continuity
  - Task handoff
  - Task continuation checklist
- Technique pack trace:
  - abstraction_level_guard: pass; checklist is an artifact-level unit.
  - recomposition_proof: pass; the checklist recomposes into handoff by preserving goal, current state, changed files, validation, and next action.
  - frame_expiry_note: pass; expires when the task gains multiple owners or release gates.
  - navigable_result_check: pass; start-here and next action are present.
  - premortem_pass: skipped-with-reason; Compact mode and low risk.
  - set_based_tournament: skipped-with-reason; only one option requested.
- Closure and recomposition proof: the checklist has bounded inputs and outputs and can be used by a future agent without the original conversation.
- Evolution profile: grows into a task-session record only when validation or ownership complexity appears.
- Deferred complexity: validation matrix, registry route, and release notes.
- Tension ledger: none.
- Premortem: skipped with reason.
- Frame-expiry note: revisit when more than one owner or release gate appears.
- Navigation guide: start by filling the five checklist fields, then continue the task.
- Next route: task-session.
```

## Expected Verdict

pass

## Acceptance Notes

- Compact mode keeps one round and records skipped techniques.
- The selected unit is smaller than a full work-pack but still closed.
