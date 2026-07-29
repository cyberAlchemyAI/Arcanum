---
name: subagent-strategy
description: "Use when deciding whether work merits a governed multi-agent dispatch and, when it does, proposing, tension-checking, confirming, registering, running, closing, and observing that dispatch through repository-local bindings."
argument-hint: "<goal> [--type <dispatch-type>] [--profile <path>] [--propose | --run | --close]"
tier: arcana
domain: multi-agent-governance
version: 0.2.0
origin: extracted from a governed repository-local subagent dispatch router and generalized for public reuse
allowed-tools: Read, Write, Glob, Grep, Task, Bash
---

# Sigil: Subagent Strategy

<objective>
Decide when multi-agent work is justified and govern every real dispatch through a tensioned proposal, explicit human confirmation, deterministic registration, dependency-aware execution, complete closeout, and evidence-backed observation.
</objective>

<logic-type>
Arcana: multi-agent lifecycle orchestration with human authority, local owner bindings, dependency scheduling, and append-only evidence.
</logic-type>

<applicability>
Use this sigil when:

- three or more sources, lenses, or returns must be synthesized,
- raw exploration would overwhelm the parent context,
- exploration should be isolated, discardable, or independently checked,
- two or more independent work lanes can run concurrently,
- the user asks for a governed subagent strategy, proposal, or dispatch,
- repository rules require tension checks, registration, and closeout evidence.
</applicability>

<non-applicability>
Do not use this sigil when:

- direct inline work is smaller than the coordination cost,
- one helper can complete a bounded task inside its parent's scope,
- the task is only to validate a dispatch document; use the local dispatch validator,
- the dispatch type has no live owner,
- required tension, registration, or agent-lifecycle mechanisms are unavailable,
- the human has not explicitly confirmed the complete strategy sheet.
</non-applicability>

<inputs>
Expected inputs, when available:

- goal and evidence boundary,
- expected outputs and artifact destination,
- proposed dispatch type,
- candidate groups, roles, and angles,
- runtime profile following `templates/runtime-profile.md`,
- type-owner contracts, preflight requirements, and stage-handoff readiness criteria,
- strategy-sheet schema and validator,
- non-mutating confirmation-readiness validation mode,
- deterministic agent-eligibility and final-approver admission rules,
- digest-owned tension-evidence representation,
- callable subagent mechanism,
- tension-check, registration, ledger, inventory, and observability bindings.
</inputs>

<ownership-boundary>
Subagent Strategy owns the universal dispatch lifecycle. It does not own:

- dispatch-sheet field definitions,
- type-specific research, review, experiment, code, or planning judgment,
- local agent eligibility,
- a consuming repository's constitution or ledger schema,
- another capability's output semantics,
- project-specific artifact placement or publication policy.

Resolve those concerns through the repository-local runtime profile and the named owner capability. Never copy private owner prose or paths into this public contract.
</ownership-boundary>

<dispatch-trigger>
A dispatch is justified only when at least one trigger holds:

1. Synthesis: three or more sources, lenses, or returns must be combined.
2. Context protection: raw work would be much larger than the parent should carry.
3. Isolation: exploration should be independently checked or safely discarded.
4. Parallelism: independent work can proceed concurrently.

A single helper spawned inside one agent's bounded scope is not a dispatch. Report it post-hoc in the parent's helper closeout. It becomes a dispatch when it fans out to two or more agents or outgrows the parent's scope.
</dispatch-trigger>

<process>
1. Resolve the active repository and the nearest applicable runtime profile. Treat generated adapters as non-authoritative when a canonical local owner exists.
2. Make the preliminary trigger decision before designing groups. If no trigger holds, work inline and return the reason.
3. Resolve the dispatch type. Read only its named owner contract and run only its configured read-only preflights. Preflight evidence informs strategy design but never authorizes the dispatch.
4. Draft and persist the strategy sheet using the local form owner. Include goal, evidence boundary, groups, agents, roles, angles, expected outputs, artifact destination, dependency edges, loop ceilings, final approver, validation, and stop conditions required by the local schema. Every load-bearing tension claim, including each predicted pairwise disagreement, must live inside the digest-bound sheet rather than companion prose.
5. Run the form owner's non-mutating confirmation-readiness validator against the exact persisted sheet. Continue only when the current schema and all deterministic admission rules pass and the validator returns the exact sheet digest without writing registration state. Confirmation readiness is one composite checkpoint: form and version, live type-owner prerequisites, agent eligibility and identity uniqueness, final-approver admission, complete digest-owned tension evidence, and configured publication boundaries must all close before the human gate. If a runtime or candidate declares a stale form version, emit a visible warning, rematerialize from the canonical local owner, and rerun this step before tension or confirmation. Other admission errors block.
6. For every group with two or more agents, name the anti-bias axis and the concrete question on which the agents are expected to disagree. Persist one predicted-disagreement record for every unordered pair in the sheet representation owned by the local schema. Reject redundant angles, nominal disagreement, incomplete pair coverage, or companion-only evidence.
7. Run the configured tension gate against only the admitted sheet bytes and the gate rubric; companion files, parent summaries, and unstored chat context cannot satisfy the gate. Phase 1 launches two independent checkers in parallel and preserves each independent verdict bound to the same sheet digest. If either reports defects, Phase 2 may give the frozen checker report to the reviewer solely to compare the apontamentos; the reviewer must not revise its independent verdict. Both independent verdicts must pass. Any revision returns to Step 5 before both checks rerun. If the runtime cannot call independent checkers, stop at an explicitly ungated proposal.
8. Present the complete admitted strategy in chat, including the trigger decision, lanes, agents, dependency flow, preflight consequences, artifact destination, readiness state, gate state, ledger state, and next human action.
9. Wait for explicit human confirmation. Silence, discussion, a question, or authorization to revise the draft is not dispatch confirmation. Ask only after composite readiness and both independent tension verdicts pass, so a normal run presents exactly one confirmation request. Confirmation freezes the exact admitted sheet bytes. Any later byte change returns to Step 5, reruns both tension checks, and requires new confirmation.
10. Validate and append the dispatch event through the profile's deterministic registrar before launching working agents. Never hand-edit an append-only ledger when a registrar exists.
11. Launch groups by dependency. A group is ready only when every incoming blocking edge has produced what the target must answer **and** the dispatch type owner's declared stage-handoff gate returns `ready` for those exact upstream artifacts. Output existence alone is not readiness. A gate may return `needs_feedback` only with a typed defect, repair-owner stage, eligible already-confirmed edge, and remaining loop capacity; otherwise it returns `blocked`. `sequential` and forward `zig-zag` edges block by default; `feedback` edges do not. On `needs_feedback`, traverse only the named declared feedback or revision edge and keep the consumer blocked. On `blocked`, propagate the gap and confidence limit to the final approver without inventing a new edge or exceeding a loop ceiling. Agents within a ready group run in parallel.
12. Preserve partial results. If an agent fails or a stage-handoff gate blocks, downstream groups and the final approver receive the failure or typed gap, available evidence, and resulting confidence limit.
13. Enforce final approval. The parent approves by default; a dedicated one-agent auditor may approve only when the local profile and deterministic registrar admit that exact shape. Working-group members do not self-approve their collective result.
14. Join and close every spawned agent. Report open, joined, failed, and closed counts plus the configured exit reason. Append exactly one close event paired to the dispatch event.
15. Run configured post-result hooks. Inventory and other read models record the strategy result and evidence links, not merely the dispatch machinery. Observability records behavior without becoming dispatch authority.
16. Return the result using the output contract and name any unresolved residue.
</process>

<dependency-semantics>
- `sequential`: the target waits for the source result.
- `zig-zag`: the target waits for the source to open the exchange; bounded returns follow the declared loop cap.
- `feedback`: advisory return edge that never makes a group unready.
- no connections: groups are independent and may start together after registration.

Dependency completion and stage readiness are separate checks. The source group
finishing satisfies the edge only provisionally; the target still waits for the
dispatch type owner's declared handoff criteria. This sigil routes that verdict
but never invents type-specific evidence rules.

Keep scopes distinct: layers belong to groups, edge loop caps belong to zig-zag or feedback edges, and the global maximum loop count belongs to the whole dispatch.
</dependency-semantics>

<observability>
A meaningful execution is any trigger decision, proposed strategy, tension-gate attempt, registered run, or closeout that produces a user-facing decision or artifact.

Emit or preserve:

- profile identifier and dispatch type,
- trigger decision and matching triggers,
- group, agent, role, angle, and dependency counts,
- preflight status and its concrete design consequence,
- confirmation-readiness status and obligations closed, expected and observed form versions, projection-drift warnings, and pre-confirmation revision count,
- tension-check results and revision count,
- confirmation request count, avoidable confirmation request count, preventable post-confirmation revision count, and freeze state,
- registration and close event identifiers,
- stage-handoff readiness verdicts, typed gaps, feedback or revision routes used, and remaining loop capacity,
- agent lifecycle counts and partial failures,
- final approver and approval status,
- result artifacts and validation,
- Quality Bar status, Anti-Pattern hits, workflow gaps, output-contract drift, and reflection trigger.

Use `templates/usage-telemetry.md`. Reflect after five meaningful executions, ten generated artifacts, three related workflow gaps, or one severe gap. Missing confirmation, unregistered execution, unpaired ledger events, unsafe scope expansion, private evidence leakage, unclosed agents, companion-only gate evidence, or a repeated confirmation caused by a deterministically discoverable pre-confirmation defect are severe gaps.
</observability>

<quality-bar>
A successful execution must:

- decide and explain whether a dispatch trigger holds before fan-out,
- keep a bounded one-helper case outside the dispatch lifecycle,
- resolve a live type owner and valid runtime profile before registration,
- persist and pass the exact sheet through the live form owner's non-mutating confirmation-readiness validator before tension or confirmation,
- close every configured deterministic admission obligation at one composite readiness point,
- treat stale runtime or schema projections as visible pre-confirmation warnings that still fail closed until rematerialized,
- expose the full strategy and artifact destination to the human,
- define real anti-bias tension for every multi-agent group,
- keep all load-bearing tension evidence inside the admitted sheet bytes,
- receive two independent PASS results before confirmation,
- require exactly one explicit confirmation request on a normal ready proposal and freeze the confirmed sheet,
- register before spawning working groups,
- honor blocking and non-blocking dependency semantics,
- require the type owner's stage-handoff readiness verdict before launching a consuming group,
- route correctable handoff gaps only through declared edges and remaining loop capacity,
- propagate partial failures and confidence limits,
- use an independent final approver,
- join and close every agent,
- append one dispatch event and one paired close event,
- keep project-specific and private authority in the consuming profile,
- update configured result and observability hooks,
- return evidence, residue, and the next human action.
</quality-bar>

<anti-patterns>
Avoid:

- dispatching because subagents are available rather than because a trigger holds,
- treating a single bounded helper as a registered fan-out,
- inventing sheet fields or type-specific judgment inside this router,
- using duplicated roles as fake tension,
- presenting a sheet before its tension checks pass,
- asking for confirmation before the exact persisted sheet passes the live form owner,
- treating syntactic form validation as complete when agent eligibility, approver admission, tension-evidence coverage, type-owner prerequisites, or publication checks are still unresolved,
- satisfying a tension gate with companion prose, parent summaries, or evidence not included in the admitted sheet digest,
- treating a form-version warning as permission to admit a stale sheet,
- treating silence, continued discussion, or draft-revision authorization as dispatch confirmation,
- making a reviewer react to checker findings before preserving the reviewer's independent verdict,
- editing the frozen sheet without rerunning readiness, both tension checks, and confirmation,
- spawning working agents before deterministic registration,
- treating an upstream file or return as stage-ready merely because it exists,
- spending a downstream approval or revision loop on an upstream evidence gap when the declared feedback route can still repair it,
- inventing a feedback edge or exceeding a loop ceiling to repair a handoff,
- treating read-model or Inventory evidence as authority,
- hiding agent failures from downstream groups,
- letting working agents approve their own collective result,
- leaving agents open or ledger events unpaired,
- copying a consuming repository's private names, paths, or evidence into Arcanum,
- claiming promotion readiness from contract prose without experiment evidence.
</anti-patterns>

<output-contract>
Return:

```markdown
## Subagent Strategy Result

- Mode: inline | propose | run | close
- Runtime profile: <profile-id and path | unavailable>
- Dispatch type / owner: <type / owner | not applicable>
- Trigger decision: inline | dispatch | blocked
- Trigger evidence: <matching triggers or reason none apply>
- Preflight: <status, selected evidence, exclusions, gaps, design consequence | not configured>
- Confirmation readiness: <pass with schema and digest | warning and rematerialization required | blocked | not configured>
- Confirmation requests: <total, avoidable, and preventable post-confirmation revisions>
- Groups / lanes: <purpose, role, anti-bias axis, parallel or dependent>
- Subagents: <names or handles, roles, angles, expected outputs>
- Dependency flow: <sequential, zig-zag, feedback, final approval>
- Tension gate: <PASS/PASS | revision required | unavailable | not applicable>
- Human gate: <awaiting confirmation | confirmed/frozen | not applicable>
- Registration: <unregistered | registered with evidence | blocked | not applicable>
- Execution: <not started | completed | partial | failed | not applicable>
- Stage handoffs: <ready | needs_feedback with typed gaps, repair owner, edge, and loops remaining | blocked | not applicable>
- Agent closeout: <open/joined/failed/closed counts and residue>
- Ledger closeout: <paired | pending | blocked | not applicable>
- Result artifacts: <paths or inline>
- Validation: <checks and status>
- Reflection trigger: none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap
- Next human action: <confirm, revise, decline, inspect, or none>
```
</output-contract>
