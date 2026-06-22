# GitHub Project Issue Loop

GitHub Project Issue Loop is an Arcana sigil for claiming one ready GitHub Project issue, refining it into bounded execution context, invoking define/design/plan artifacts when useful, executing through Task Session, and opening a pull request with ticket-linked results.

It is useful when a repository uses GitHub Issues and Projects as the work intake surface, but implementation still needs Arcanum governance before mutation. The sigil keeps the loop honest: select one issue, claim it visibly, understand it through repository evidence, materialize the right design/plan artifacts, execute one bounded work package, verify, open the PR, and sync the board.

## Problem It Solves

Project-board execution can drift in two directions:

- the agent grabs a ticket and jumps straight into code without enough context;
- the agent over-plans a ticket and never leaves a PR-shaped result.

This sigil ties the intake, refinement, lifecycle artifacts, implementation, verification, PR, and board status into one governed delivery loop.

It also prevents accidental blast-radius creep: before any fix, the loop maps upstream dependencies, downstream dependents, intended write scope, non-goals, and focused regression tests so the final PR can show that the change affected only the intended behavior.

## Use When

- the user points to a GitHub Project view and wants open issues processed;
- the issue should be assigned to the current operator before work begins;
- the issue needs context from the repository, docs, tickets, or prior artifacts;
- `refine`, `invoke`, and `task-session` should be composed according to the situation;
- the expected result is a branch, commit, PR, and ticket-linked evidence.

## Do Not Use When

- the user wants only issue triage with no execution;
- the issue is blocked on a product decision the agent cannot resolve;
- the work spans several independent issues that need separate PRs;
- the repository cannot be accessed or validated;
- a project item requires a human approval gate before assignment or mutation.

## Tier Rationale

Selected tier: Arcana.

The loop coordinates external state, repository context, Arcanum lifecycle sigils, implementation execution, validation, pull request publication, and project-board synchronization. It is not a deterministic Formulae check or a bounded Transmutation artifact; it is a governed delivery workflow with stateful gates.

## Lifecycle Expectations

- Every meaningful run should emit a compact telemetry record.
- Reflection should occur after 5 meaningful executions, 10 output artifacts, 3 related workflow gaps, or 1 severe gap.
- Promotion readiness requires at least low, medium, and complex experiment outputs plus a validation report.
- If a live subagent dispatch is needed, use the applicable subagent strategy and preserve the human gate before dispatch.

## Typical Flow

1. Confirm GitHub and repository access.
2. Read the requested project view and list candidate issues.
3. Select one ready issue using explicit criteria.
4. Assign the issue to the operator and move the project item to In Progress when allowed.
5. Refine the ticket against repository evidence.
6. Map upstream and downstream dependencies, define write scope, and create or identify focused regression tests before implementation.
7. Invoke define/design/plan only to the depth the issue needs, escalating when dependency boundaries are unclear.
8. Execute one bounded task session on a branch or worktree.
9. Validate focused regression behavior, upstream/downstream containment, and then broader suite health.
10. Commit, push, and open a PR that links the issue.
11. Check project status, linked PR, and CI state.
12. Emit telemetry and report the next lifecycle step.

## Outputs

- Claimed issue and board status.
- Refinement evidence or rationale for skipping deeper refinement.
- Define/design/plan artifacts when created.
- Dependency map and regression test plan.
- Task-session receipt.
- Branch, commit, and PR.
- Verification summary.
- Scope-containment evidence.
- Telemetry record.
