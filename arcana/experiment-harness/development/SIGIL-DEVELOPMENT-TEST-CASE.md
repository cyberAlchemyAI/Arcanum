# Sigil Development Test Case For Generalized Experiment Harness

Status: planned proof case.

## Purpose

Use `sigil-development` as the first lifecycle authority to prove that the generalized Experiment Harness can create experiments and validate work done, without Experiment Harness taking ownership of sigil meaning.

## Recommended Target

Primary candidate: `arcana/concept-layer-optimizer`, first copied into `/tmp` or another explicitly approved sandbox target.

Reason:

- it has a fresh `README.md` and `SKILL.md`,
- it already has examples and validation artifacts,
- it has clear Proposer/Balancer behavior that can be tested,
- it has known lifecycle gates and a final approval boundary,
- it is complex enough to prove the harness without requiring a brand-new sigil.

Fallback candidate: a small toy sigil under `/tmp` or a local sandbox artifact when the real repository should not be touched.

The real `arcana/concept-layer-optimizer` target should not be modified during the first proof run unless the worktree scope is clean or the lifecycle owner explicitly approves the write scope.

## Test Question

Can Sigil Development request a `sigil-development` experiment profile, generate useful experiment artifacts for a target sigil, validate those artifacts, and produce a clear lifecycle recommendation?

## Test Flow

1. Run Sigil Development in update/validation mode against the target sigil.
2. Ask it to initialize or refresh the target's experiment harness using Experiment Harness with the `sigil-development` profile.
3. Confirm generated files include:
   - `development/EXPERIMENT-PROFILE.md`,
   - validation experiment,
   - task matrix,
   - fixtures,
   - low/medium/complex prompts,
   - live regimes,
   - wrapper scripts,
   - observability-ready report path.
4. Run deterministic harness validation.
5. Run one mock loop for a generated regime.
6. Record a report that separates:
   - Experiment Harness mechanics,
   - Sigil Development lifecycle judgment,
   - target sigil gaps.
7. Route next action as promote, hold, revise, or request live Codex budget.

## Expected Generated Scenarios

| Scenario | Purpose | Expected Evidence |
| --- | --- | --- |
| `sigil-new-low` | Prove a small sigil authoring request can produce contract-shaped output. | Output includes target sigil, tier, files changed, validation, and next lifecycle step. |
| `sigil-update-medium` | Prove update mode can revise a sigil without changing its core contract unnecessarily. | Output names evidence, applied edits, rejected changes, and validation checks. |
| `sigil-observe-medium` | Prove observer pass can classify gaps from usage evidence. | Output distinguishes signal evidence from observer inference. |
| `sigil-reflect-complex` | Prove reflection can propose targeted lifecycle updates. | Output includes trigger state, patterns found, proposed changes, rejected changes, and next trigger. |
| `sigil-harness-validation-complex` | Prove Sigil Development can judge whether a generated harness is promotion evidence. | Output names pass/flag/block and routes unresolved gaps. |

## Acceptance Criteria

- The generated experiment pack is navigable by a maintainer.
- The profile does not duplicate the full Sigil Development process.
- The target sigil's `SKILL.md` remains authoritative for Quality Bar, Anti-Patterns, and output contract.
- Validation catches missing prompts, missing regimes, save-summary outputs, and profile drift.
- `development/EXPERIMENT-PROFILE.md` names `profile_id`, `artifact_type`, `lifecycle_owner`, `contract_path`, scenario pack, and promotion gate.
- The final report gives a clear lifecycle recommendation.

## Failure Conditions

Return `block` if:

- the target sigil lacks a readable `SKILL.md`,
- generated prompts cannot identify the lifecycle owner,
- `development/EXPERIMENT-PROFILE.md` is missing or contradicts the selected profile,
- validation passes without checking Quality Bar or Anti-Patterns,
- generated outputs are treated as editable implementation files,
- Sigil Development and Experiment Harness disagree about ownership and the report hides the disagreement.

Return `flag` if:

- the harness is structurally valid but lacks live Codex evidence,
- profile prompts are useful but incomplete,
- validation is deterministic-only,
- observability is unavailable but the evidence is otherwise usable.

## Report Shape

```markdown
## Generalized Harness Test Result

- Lifecycle authority: sigil-development
- Target sigil: <path>
- Experiment profile: sigil-development
- Profile metadata: pass | flag | block
- Generated artifacts: <paths>
- Deterministic validation: pass | flag | block
- Mock loop validation: pass | flag | block | not run
- Live loop validation: pass | flag | block | not approved
- Ownership separation: pass | flag | block
- Target sigil gaps: <list>
- Harness gaps: <list>
- Recommendation: promote generalized profile | hold | revise | request live budget
- Next route: experiment-harness | sigil-development | concept-layer-optimizer | decision-gate
```

## Next Action

Implement profile-aware harness initialization, run this test case against a sandbox copy with mock loop validation, then ask for live Codex budget only if the deterministic report is useful.
