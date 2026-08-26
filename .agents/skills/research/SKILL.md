---
surface_kind: generated-native-runtime-package
runtime: codex
canonical_source: arcana/research/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
name: research
description: Run governed, evidence-backed research through internal or external source work, tensioned multi-agent synthesis, skeptic gates, and cited findings. Use for research questions, precedent sweeps, multi-perspective audits, falsification, or synthesis that exceed a direct inline lookup. Every governed research dispatch must use a topic folder beneath a repo-local directory named research and first create or validate its research-initial-definitions.md.
---

# Research

<objective>
Produce bounded, citable findings without inflating claims, confusing ownership
with truth, or designing a dispatch before the informational starting point is
explicit.
</objective>

<initial-definitions-precondition>
This is a hard precondition for every governed research dispatch. It does not
apply to a trivial lookup completed inline without a dispatch.

Before designing, proposing, registering, or running a research dispatch:

1. Resolve the containing `repository_root`; research never lives outside it.
2. Resolve a `research_root`: a directory literally named `research` at any
   depth inside the repository. Any repository directory may contain this
   research container; parent directory names have no special semantics.
3. Resolve the research `working_folder` beneath that container, normally
   `<research_root>/<research-id>`. Never use an arbitrary project directory or
   the shared `research_root` itself as one research's working folder.
4. Prefer the `research` container nearest to the user's explicit work target,
   regardless of what that target directory represents or is named.
   If the target is already inside a research subtree, retain its nearest
   `research` ancestor. If no scoped container is indicated, use
   `<repository_root>/research`. Do not guess between unrelated candidates.
5. Require `<working_folder>/research-initial-definitions.md`.
6. If the file is absent, or the user materially changed the topic, scope, or
   confirmed constraints, use the sibling `research-initial-definitions` skill
   to create or revise it.
7. Resolve the sibling skill directory independently of the process current
   directory, then run its validator with absolute paths:

   ```text
   python "<research-initial-definitions-skill-dir>/scripts/validate_initial_definitions.py" "<absolute-working-folder>" --repo-root "<absolute-repository-root>" --json
   ```
8. Read the validated file completely before shaping the research strategy.
9. Preserve the validated repository root, research root, working folder,
   artifact path, and SHA-256 as preflight evidence in the strategy or dispatch
   record.
10. Stop with `block` while the location or file is invalid. Never bypass this gate
   because the intended agents, sources, or solution already appear obvious.

The initial-definitions file is informational context only. It must not contain
candidate vocabulary, hypotheses, methods, workstreams, source plans, agent
roles, topology, budgets, success criteria, stopping conditions, outputs,
findings, handoffs, implementation steps, or proposed solutions.
</initial-definitions-precondition>

<applicability>
Use this skill when:

- three or more sources, lenses, or returns require synthesis;
- internal and external evidence must be reconciled;
- independent challenge is needed before accepting a candidate conclusion;
- the raw investigation should remain isolated from the parent context;
- the user asks for a governed research dispatch.

Keep a single bounded lookup inline. Use `review` when the target already exists
and the requested deliverable is a set of verified change requests.
</applicability>

<ownership-boundary>
Research owns research-type judgment: evidence discipline, research roles,
skeptic gates, synthesis, and findings. The repository-local `subagent-strategy`
skill owns whether a dispatch is justified, proposal and confirmation, runtime
bindings, dependency execution, final approval, closeout, and observability.
The consuming repository owns its registrar, sheet schema, agent eligibility,
artifact destination, privacy boundary, and source authority.
</ownership-boundary>

<research-judgment>
Research seeks what is supported and usable, not novelty for its own sake.

- `explorer`: investigates one tensioned angle and returns resolvable evidence.
- `writer`: synthesizes the collected returns without erasing dissent.
- `skeptic`: attacks exactly one gate: precedent, non-vacuity, or definitional
  soundness.
- `auditor`: checks coverage, citations, dissent preservation, and verdicts.

Ownership is a label, never a negative verdict. An owned result may be
`build-from-owned` or `already-deployed`. `novel-attempt` is allowed only after
a bounded precedent search returns clean and must not be restated as a novelty
claim. A candidate is killed only by `no-witness` or `tautological`.

Use pairwise-tensioned explorer angles and distinct skeptic gates. Every
load-bearing external claim cites a retrieved primary or authoritative source;
every repository claim cites the exact artifact inspected. Claim strength stays
at or below the evidence.
</research-judgment>

<process>
1. Satisfy the initial-definitions precondition.
2. Ask `subagent-strategy` whether the work merits a dispatch and resolve the
   repository-local runtime profile.
3. Design independent explorer angles and explicit skeptic gates. Keep internal
   and external source work distinct when both are needed.
4. Pass the local tension and human-confirmation gates before spawning working
   agents.
5. Execute groups by declared dependencies and preserve partial failures.
6. For two or more research agents, persist collected returns verbatim in
   `<working_folder>/research.md`; for one agent, this file is optional.
7. Produce `<working_folder>/findings.md` with cited conclusions, implications,
   dissent, limitations, and a verdict per candidate.
8. Obtain final approval and close every agent and dispatch record through
   `subagent-strategy`.
</process>

<findings-contract>
For each candidate, record:

| candidate | owner | witnessed? | sound? | verdict | use-mode |
|---|---|---|---|---|---|

- `GO`: witnessed and sound; use-mode is `build-from-owned`,
  `already-deployed`, or `novel-attempt`.
- `KILL`: only `no-witness` or `tautological`, preserved as a typed negative
  naming what would have contributed and the fact that zeroed it.

Close with the one-line answer to the research goal and state the evidence
boundary.
</findings-contract>

<quality-bar>
- The initial-definitions validator passes before strategy design.
- The working folder resolves inside the repository and beneath a directory
  literally named `research` without using that shared container directly.
- The exact validated file is read and its hash is preserved as preflight
  evidence.
- Sources are retrieved or inspected, not merely recalled.
- Explorer angles are genuinely tensioned and skeptic gates are distinct.
- Every load-bearing finding cites its evidence.
- Dissent, reversals, empty searches, and typed negatives remain visible.
- Research agents write only inside the confirmed working folder unless the
  user separately authorizes implementation.
</quality-bar>

<anti-patterns>
Avoid bypassing initial definitions, placing a research plan inside the
informational baseline, treating an empty search as novelty, treating ownership
as truth, inventing force from evidence kind, dispatching redundant agents,
persisting unsupported schemas, or allowing findings to mutate source artifacts.
</anti-patterns>
