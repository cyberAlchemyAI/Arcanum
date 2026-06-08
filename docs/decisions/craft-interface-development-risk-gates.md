# Craft Interface Development Risk Gates

Date: 2026-06-07
Status: pass
Scope: `development/craft/CRAFT-INTERFACE-WORK-PACK.md`

## Decision Gate Result

Target scope: Craft interface and interaction development.

Result: PASS.

Decisions resolved: 4.

Blockers remaining: 0 for the local interface and interaction artifact build.

Decision artifact: `docs/decisions/craft-interface-development-risk-gates.md`

## Decisions

### D-001: Should local interface work wait for aggregate Refine receipt pass?

Selected option: no, continue local interface work.

Options considered:

- Wait for aggregate Refine receipt pass.
  - Benefit: maximum alignment with the current Refine continuation.
  - Cost/risk: blocks a local design/fixture slice on unrelated internal Refine
    evidence.
  - Choose when: the work claims Refine readiness or promotion.
  - Downstream impact: delays interface testing.
- Continue local interface work while preserving the Refine receipt block.
  - Benefit: allows local Craft testing while staying honest about Refine state.
  - Cost/risk: reviewers may confuse local interface readiness with Refine
    completion unless the boundary is explicit.
  - Choose when: the work only creates Craft-local contracts and fixtures.
  - Downstream impact: interface tasks can proceed; promotion remains blocked.

Rationale: `CRAFT-INTERFACE-001` and `CRAFT-INTERACTION-001` do not claim Refine
completion. The aggregate Refine block remains active background state.

### D-002: Should runtime, CLI, or skill helper shape be selected now?

Selected option: defer.

Options considered:

- Select runtime/CLI/helper now.
  - Benefit: clearer implementation target for later automation.
  - Cost/risk: prematurely expands the task into runtime or install-surface work.
  - Choose when: the next task explicitly implements an execution helper.
  - Downstream impact: requires broader validation and owner approval.
- Defer and keep the current task file-backed.
  - Benefit: protects the local interface slice and avoids command-surface drift.
  - Cost/risk: later task must revisit helper shape.
  - Choose when: current deliverables are contracts, YAML fixtures, and
    validation guides.
  - Downstream impact: task remains bounded.

Rationale: the current work-pack explicitly excludes runtime adapters, command
refresh, and promotion.

### D-003: Can receipt validation be prose/manual in this slice?

Selected option: yes, with YAML parsing and explicit review checks.

Options considered:

- Require executable receipt validation now.
  - Benefit: stronger proof.
  - Cost/risk: introduces a validator implementation before the row shape has
    live-test evidence.
  - Choose when: multiple interaction fixtures exist.
  - Downstream impact: expands implementation scope.
- Use manual validation with parseable fixtures.
  - Benefit: proves the contract shape at low cost.
  - Cost/risk: behavior can drift until executable validation exists.
  - Choose when: schema and examples are still candidate local artifacts.
  - Downstream impact: follow-up gap remains visible.

Rationale: executable validation is useful but not required to complete the
local design slice.

### D-004: Can Craft close contexts from external capability receipts?

Selected option: only after Craft recomposition evidence is recorded.

Options considered:

- Close directly from owner capability pass.
  - Benefit: simpler implementation.
  - Cost/risk: collapses Craft's recomposition rule and hides parent-context
    fit.
  - Choose when: Craft is not tracking recursive contexts.
  - Downstream impact: violates Craft architecture.
- Require recomposition evidence after owner pass.
  - Benefit: preserves Craft's recursive property and parent-context closure.
  - Cost/risk: adds one more ledger operation.
  - Choose when: contexts can have children and cross-context relations.
  - Downstream impact: keeps closure auditable.

Rationale: Craft is specifically a recursive ledger; closure needs parent-fit
evidence.

## Deferred Decisions

- Whether route handoffs become a helper library, CLI, or skill-native helper.
- Whether receipt validation becomes executable.
- Whether generated `CRAFT.md` views are required.
- Whether Craft can later run selected routes through a runtime owner.

## Assumptions Recorded

- Interface and interaction work remains local to `development/craft/`.
- `.craft/ledger.yml` remains the target-project storage model.
- `CRAFT.md` remains a human-readable view, not canonical source.
- Promotion, registry mutation, runtime adapter work, and command-surface refresh
  remain out of scope.

## Validation

- Reviewed Craft README and session ledger current state.
- Reviewed promotion readiness gaps.
- Reviewed interface and interaction work-pack rules.
- Confirmed dispatch validation already passes for interface and interaction
  dispatch artifacts.

## Next Step

Proceed with `CRAFT-INTERFACE-001`, then `CRAFT-INTERACTION-001`.
