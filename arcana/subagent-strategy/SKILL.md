---
name: subagent-strategy
description: "Use when deciding whether work merits a governed multi-agent dispatch and, when it does, proposing, tension-checking, confirming, registering, running, closing, and observing that dispatch through repository-local bindings."
argument-hint: "<goal> [--type <dispatch-type>] [--profile <path>] [--propose | --run | --close]"
tier: arcana
domain: multi-agent-governance
version: 0.1.0
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
- type-owner contracts and preflight requirements,
- strategy-sheet schema and validator,
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
4. Draft the strategy sheet using the local form owner. Include goal, evidence boundary, groups, agents, roles, angles, expected outputs, artifact destination, dependency edges, loop ceilings, final approver, validation, and stop conditions required by the local schema.
5. For every group with two or more agents, name the anti-bias axis and the concrete question on which the agents are expected to disagree. Reject redundant angles or nominal disagreement.
6. Run the configured tension gate with two independent checkers. Both must pass the same sheet. If a checker flags it, revise and rerun both. If the runtime cannot call independent checkers, stop at an explicitly ungated proposal.
7. Present the complete strategy in chat, including the trigger decision, lanes, agents, dependency flow, preflight consequences, artifact destination, gate state, ledger state, and next human action.
8. Wait for explicit human confirmation. Silence, discussion, or a question is not confirmation. Confirmation freezes the sheet; any material edit re-enters Step 6.
9. Validate and append the dispatch event through the profile's deterministic registrar before launching working agents. Never hand-edit an append-only ledger when a registrar exists.
10. Launch groups by dependency. A group is ready only when every incoming blocking edge has produced what it must answer. `sequential` and forward `zig-zag` edges block by default; `feedback` edges do not. Agents within a ready group run in parallel.
11. Preserve partial results. If an agent fails, downstream groups and the final approver receive the failure, available evidence, and resulting confidence limit.
12. Enforce final approval. The parent approves by default; a dedicated one-agent auditor may approve when the frozen sheet names it. Working-group members do not self-approve their collective result.
13. Join and close every spawned agent. Report open, joined, failed, and closed counts plus the configured exit reason. Append exactly one close event paired to the dispatch event.
14. Run configured post-result hooks. Inventory and other read models record the strategy result and evidence links, not merely the dispatch machinery. Observability records behavior without becoming dispatch authority.
15. Return the result using the output contract and name any unresolved residue.
</process>

<dependency-semantics>
- `sequential`: the target waits for the source result.
- `zig-zag`: the target waits for the source to open the exchange; bounded returns follow the declared loop cap.
- `feedback`: advisory return edge that never makes a group unready.
- no connections: groups are independent and may start together after registration.

Keep scopes distinct: layers belong to groups, edge loop caps belong to zig-zag or feedback edges, and the global maximum loop count belongs to the whole dispatch.
</dependency-semantics>

<observability>
A meaningful execution is any trigger decision, proposed strategy, tension-gate attempt, registered run, or closeout that produces a user-facing decision or artifact.

Emit or preserve:

- profile identifier and dispatch type,
- trigger decision and matching triggers,
- group, agent, role, angle, and dependency counts,
- preflight status and its concrete design consequence,
- tension-check results and revision count,
- confirmation and freeze state,
- registration and close event identifiers,
- agent lifecycle counts and partial failures,
- final approver and approval status,
- result artifacts and validation,
- Quality Bar status, Anti-Pattern hits, workflow gaps, output-contract drift, and reflection trigger.

Use `templates/usage-telemetry.md`. Reflect after five meaningful executions, ten generated artifacts, three related workflow gaps, or one severe gap. Missing confirmation, unregistered execution, unpaired ledger events, unsafe scope expansion, private evidence leakage, or unclosed agents are severe gaps.
</observability>

<quality-bar>
A successful execution must:

- decide and explain whether a dispatch trigger holds before fan-out,
- keep a bounded one-helper case outside the dispatch lifecycle,
- resolve a live type owner and valid runtime profile before registration,
- expose the full strategy and artifact destination to the human,
- define real anti-bias tension for every multi-agent group,
- receive two independent PASS results before confirmation,
- require explicit confirmation and freeze the confirmed sheet,
- register before spawning working groups,
- honor blocking and non-blocking dependency semantics,
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
- treating silence or continued discussion as confirmation,
- editing the frozen sheet without rerunning the tension gate,
- spawning working agents before deterministic registration,
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
- Groups / lanes: <purpose, role, anti-bias axis, parallel or dependent>
- Subagents: <names or handles, roles, angles, expected outputs>
- Dependency flow: <sequential, zig-zag, feedback, final approval>
- Tension gate: <PASS/PASS | revision required | unavailable | not applicable>
- Human gate: <awaiting confirmation | confirmed/frozen | not applicable>
- Registration: <unregistered | registered with evidence | blocked | not applicable>
- Execution: <not started | completed | partial | failed | not applicable>
- Agent closeout: <open/joined/failed/closed counts and residue>
- Ledger closeout: <paired | pending | blocked | not applicable>
- Result artifacts: <paths or inline>
- Validation: <checks and status>
- Reflection trigger: none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap
- Next human action: <confirm, revise, decline, inspect, or none>
```
</output-contract>
