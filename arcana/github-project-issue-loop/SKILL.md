---
surface_kind: canonical-sigil-source
runtime: codex
canonical_source: arcana/github-project-issue-loop/SKILL.md
alias_of: null
name: github-project-issue-loop
description: "Use when: claiming one GitHub Project issue, refining its context, invoking define/design/plan as needed, executing through Task Session, and opening a linked PR with verification evidence."
argument-hint: "<github-project-url-or-owner/project-number> [--repo owner/name] [--issue <number>] [--dry-run] [--limit <count>]"
tier: arcana
domain: github-delivery-governance
version: 0.1.0
origin: created from a live GitHub Project issue loop that assigned one issue, refined it, invoked artifacts, executed a task session, and opened a linked PR
allowed-tools: Read, Write, Glob, Grep, Task
---

# Sigil: GitHub Project Issue Loop

<objective>
Claim one ready GitHub Project issue, convert it into governed repository execution context, run the appropriate Arcanum lifecycle path, and open a verified pull request linked back to the ticket.
</objective>

<logic-type>
Arcana: project-board intake, repository evidence synthesis, lifecycle routing, task execution, validation, PR publication, and board synchronization.
</logic-type>

<applicability>
Use this sigil when:

- the user provides a GitHub Project view, project number, or issue queue;
- open issues should be assigned to the current operator before implementation;
- the ticket needs `refine` to understand context, acceptance criteria, and solution shape;
- `invoke` define/design/plan artifacts should be created based on issue risk and ambiguity;
- `task-session` should execute the bounded implementation work;
- the final result should be a branch, commit, PR, issue link, verification summary, and project status update.
</applicability>

<inputs>
Expected inputs, if available:

- GitHub Project URL, project owner, and project number;
- target repository or repository filter;
- issue number, priority filter, status filter, or selection rule;
- authenticated GitHub CLI/app state;
- local checkout path and base branch;
- Arcanum skills available in the repository;
- known upstream callers, downstream consumers, generated mirrors, and dependency boundaries for the target area;
- existing regression tests, expected failing/covering tests, and validation commands;
- user assignment policy, board status policy, and PR target branch;
- validation commands and CI expectations;
- whether the run is dry-run, plan-only, or execution-authorized.
</inputs>

<chain-boundary>
GitHub Project Issue Loop owns the delivery orchestration from project-board intake to PR creation.

- GitHub CLI/app owns external issue, project, branch, and PR operations.
- `refine` owns discovery, seed shaping, dispatch, and handoff artifacts.
- `invoke` owns define, design, plan, and related templates.
- `task-session` owns bounded implementation execution and local validation.
- `domainspec-subagents-strategy` or another subagent strategy owns live subagent dispatch governance when research, review, or experiment subagents are required.
- This sigil must not silently bypass human gates required by subagent strategies, branch protection, project policy, or destructive repo operations.
</chain-boundary>

<process>
1. Resolve operating context:
   - identify the GitHub Project owner/number/view;
   - identify the target repository and local checkout;
   - verify GitHub auth, required scopes, base branch, and clean/durable work area;
   - read relevant repo instructions before mutation.
2. Intake candidate issues:
   - list project items with issue content, status, priority, labels, assignees, linked PRs, and repository;
   - filter out done/closed items and items that already have active linked PRs unless the user asks to continue them;
   - prefer explicit issue selection; otherwise select one ready issue using priority, unassigned/assigned-to-user state, repository availability, and boundedness.
3. Claim the ticket:
   - assign to the operator when allowed;
   - move the project item to In Progress when allowed;
   - record if either operation is blocked and decide whether execution may continue.
4. Refine the ticket:
   - read the issue body, linked docs, related code, tests, and prior artifacts;
   - produce or update a refinement run with issue objective, evidence index, dispatch rationale, and runtime handoff;
   - keep local evidence separate from external assumptions.
5. Map the regression boundary before implementation:
   - identify upstream dependencies that feed the target behavior, such as callers, routes, data contracts, configuration, generated sources, and existing tests;
   - identify downstream dependents that may observe the behavior, such as UI surfaces, APIs, artifacts, docs, generated packages, CI jobs, and external consumers;
   - define the intended write scope, non-goals, and affected-only hypothesis;
   - create, update, or explicitly identify focused tests before the fix so the regression and adjacent behavior are observable;
   - include at least one containment check, snapshot, focused assertion, or existing invariant that helps prove the fix did not spill into unrelated behavior;
   - record the dependency map and test plan in refinement, invoke, or task-session artifacts before code mutation.
6. Select lifecycle depth:
   - direct Task Session for low-risk, clear issues;
   - Invoke Define for unclear outcome or acceptance criteria;
   - Invoke Design for architecture, UX, data, integration, governance choices, or unclear upstream/downstream boundaries;
   - Invoke Plan for multi-step implementation, dependency-risk sequencing, or validation sequencing;
   - subagent dispatch only when the active strategy permits it and the user confirmation gate is satisfied.
7. Prepare execution:
   - create or reuse an isolated branch or worktree;
   - define write scope and validation surface;
   - preserve unrelated local changes.
8. Execute via Task Session:
   - run or document the focused regression test baseline before the fix when practical;
   - implement the bounded change;
   - keep artifacts, code, and tests aligned with the ticket result;
   - run focused validation first, including upstream/downstream containment checks, then broader validation proportional to risk;
   - compare changed files against the dependency map and explain any expansion.
9. Publish:
   - commit only the intended files;
   - push the branch;
   - open a PR against the target base branch;
   - include summary, verification, artifacts, and `Closes #<issue>` when appropriate.
10. Sync and observe:
   - verify issue assignment, project status, linked PR, and CI state;
   - emit telemetry using `templates/usage-telemetry.md`;
   - report unresolved CI, project, or review blockers.
</process>

<observability-model>
A meaningful execution is any run that claims or attempts to claim a project issue and produces one of: a refinement artifact, invoke artifact, task-session receipt, branch, commit, PR, validation result, or board status update.

Telemetry should capture:

- project owner/number/view;
- repository and issue number;
- selection reason;
- claim result and board status result;
- lifecycle route used;
- artifact paths created;
- upstream and downstream dependency map status;
- regression tests created, updated, reused, or blocked;
- scope containment result;
- files changed count;
- validation commands and statuses;
- PR URL;
- CI status at final poll;
- blockers and workflow gaps;
- reflection trigger state.

Use `templates/usage-telemetry.md` as the default JSONL schema. When repository observability is installed, append telemetry to `.arcanum/observability/signals/sigil-invocations.jsonl`.

Use `templates/regression-boundary-map.md` when a run needs a durable dependency map or when the issue touches code, UI behavior, generated artifacts, runtime configuration, data contracts, or shared tests.
</observability-model>

<reflection-policy>
Run reflection when any of these triggers occur:

- Manual trigger: the user asks to improve the issue loop.
- Usage threshold: 5 meaningful executions.
- Output threshold: 10 generated artifacts since the last reflection.
- Gap threshold: 3 related workflow gaps, such as repeated project-field ambiguity or repeated CI polling uncertainty.
- Severe gap: 1 severe workflow gap, such as claiming the wrong issue, mutating the wrong repository, opening a PR against the wrong base, losing user changes, bypassing a required gate, or reporting CI as settled when it is still running.

Reflection must produce a report using `templates/reflection-report.md` and must name which contract area should change before editing the sigil.
</reflection-policy>

<quality-bar>
A successful execution must:

- operate on exactly one issue unless the user explicitly authorizes batch mode;
- show the issue selection reason before mutation when selection was inferred;
- assign or explicitly explain why assignment was blocked;
- keep project status and linked PR state observable;
- read local repo instructions before code mutation;
- create a branch or worktree that protects unrelated local changes;
- map upstream dependencies and downstream dependents before implementation;
- create, update, or explicitly identify focused regression tests before the fix, or record why no meaningful test can be created;
- include containment validation that proves the fix affected only the intended behavior as far as local evidence can show;
- route through `refine`, `invoke`, and `task-session` according to issue risk rather than always using the same depth;
- preserve human gates required by subagent strategy or project policy;
- produce durable artifacts for non-trivial issues;
- run and report validation commands;
- open or update a PR with issue linkage and verification evidence;
- record telemetry or explain why telemetry storage was unavailable.
</quality-bar>

<anti-patterns>
Avoid:

- processing several issues in one branch without explicit batch authorization;
- choosing a ticket only because it appears first on the board;
- claiming a ticket without checking repository availability and local checkout state;
- treating `gh project item-list` output as stable without verifying issue state;
- skipping refine when the ticket body points to docs, audits, or acceptance criteria;
- implementing before mapping upstream/downstream dependencies and intended write scope;
- relying only on a broad full suite without a focused regression test or explicit existing-test rationale;
- widening the fix into adjacent behavior just because a nearby test is convenient;
- creating define/design/plan artifacts for trivial issues just to satisfy ritual;
- using Task Session to execute vague or unresolved work;
- opening a PR without local validation evidence;
- marking CI as passed while checks are still running;
- editing generated `.agents/skills` surfaces instead of canonical sigil sources.
</anti-patterns>

<output-contract>
Return:

```markdown
## GitHub Project Issue Loop Result

- Project: <owner/project-number/view-or-url>
- Repository: <owner/name>
- Issue: #<number> <title>
- Selection reason: <reason>
- Claim result: <assigned|already-assigned|blocked>
- Project status: <status|blocked|not-updated>
- Lifecycle route: <refine|invoke-define|invoke-design|invoke-plan|task-session|subagent-review>
- Dependency map: <upstream/downstream summary or artifact path>
- Regression tests: <created|updated|reused|blocked with rationale>
- Scope containment: <pass|flag|block with evidence>
- Artifacts: <paths>
- Branch/commit: <branch> / <sha>
- PR: <url|not-opened>
- Validation: <commands and status>
- CI: <summary at final poll>
- Telemetry: <written path|not written reason>
- Blockers: <none|list>
- Next step: <review|merge|wait-ci|reflect|continue-loop>
```
</output-contract>
