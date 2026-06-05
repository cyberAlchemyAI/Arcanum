# Arcanum Sigil: robot talks

<!-- arcanum:capability-id robot-talks -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command arcanum-sigil-robot-talks -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-sigil-robot-talks-<UTC timestamp>`.
- `capability.id`: `robot-talks`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `robot-talks` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `robot-talks`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/robot-talks/README.md

````markdown
# Robot-Talks

Robot-Talks is an Arcana sigil for coordinated cross-layer investigation.

It sends multiple investigators after distinct concerns, then synthesizes their evidence into tensions that a human can validate before any implementation work begins.

## Problem It Solves

Complex systems can fail because different layers believe different things. Documentation may describe one behavior while implementation does another. A frontend may assume one contract while a backend exposes another. Operational practice may depend on an unstated rule that no artifact owns.

A single investigator can miss these contradictions because broad coverage competes with depth. Robot-Talks solves that by splitting the inquiry by concern, collecting independent evidence, and synthesizing contradictions rather than summaries.

## Use When

- the problem spans two or more layers,
- contradictions must be identified before acting,
- independent perspectives are likely to reveal better evidence,
- the cost of misunderstanding is higher than the cost of a structured investigation,
- a human decision gate is needed before follow-up work begins.

## Do Not Use When

- the issue is a single-file bug,
- the user only needs a quick explanation of one component,
- the requested work is already well specified,
- implementation should begin immediately without an audit phase.

## Investigation Model

Robot-Talks has four phases:

1. Setup: define the central question, assumptions to challenge, agent roles, and decomposition strategy.
2. Exploration: each investigator reports findings, gaps, local tensions, and synthesis questions.
3. Synthesis: the orchestrator identifies contradictions across layers.
4. Human gate: the user decides whether each tension is actionable, deferred, invalid, or uncertain.

## Output

The primary output is a preserved investigation record containing:

- the scope definition,
- investigator roles,
- independent findings with evidence,
- synthesized tensions,
- human gate decisions,
- follow-up action links or notes.

## Why This Is Arcana

The sigil coordinates multiple reasoning threads, preserves state across phases, and requires human validation before action. Its value is not a single transformed artifact; it is governed inquiry that produces a responsible next move.
````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/robot-talks/SKILL.md

````markdown
---
name: robot-talks
description: Run a multi-agent parallel investigation to identify cross-layer tensions
tier: arcana
domain: multi-agent-governance
version: 0.1.0
origin: generalized from recurring cross-layer investigation practice
---

# Robot-Talks: Multi-Agent Investigation Skill

Auditing tool for cross-layer tension discovery. Does NOT implement fixes.

<logic-type>
Arcana: recursive, multi-agent investigation with synthesis, human gating, and session preservation.
</logic-type>

Use this sigil when misunderstanding the system shape is more expensive than a short, structured investigation.

## Invocation Checklist (All must be YES)

- [ ] Problem spans 2+ distinct layers (not a single-file bug or local refactor)
- [ ] A single investigator would trade depth for breadth
- [ ] You need to identify contradictions before acting (audit, not implementation)
- [ ] Cost of misunderstanding exceeds cost of ~90 min investigation

**If any box is empty:**

- Single-file bug -> use a local debugging workflow
- "How does X work?" -> use focused code or documentation exploration
- Refactor in one module -> use local impact analysis
- Well-specified feature -> implement directly

## Phase 1: Setup (~15 min)

**Step 1 - User defines the problem.** The user must provide:

1. **Central question** - what misalignment are we investigating?
2. **Assumptions to challenge** - what we think is true but might be wrong

Do NOT proceed until the user has stated both. Ask if missing.

**Step 2 - Orchestrator proposes strategy.** Based on the user's input:

3. **Agent roles** - each with: concern, central question, explicit exclusions
4. **Strategy check** - state one alternative decomposition considered and why it was rejected. Present both the chosen strategy and the alternative to the user.

Agents do NOT spawn until the user evaluates and approves the approach.

Rules: decompose by **concerns**, not files. No two agents investigate the same question. Evidence overlap is fine.

## Phase 2: Exploration (~15 min per agent, parallel)

Each agent reports independently using this mandatory format:

1. **Key Findings** - 3-5 bullets, each with evidence (file, line number, doc reference)
2. **Gaps or Inconsistencies** - missing, undocumented, or contradictory within scope
3. **Local Tensions** - conflicts within this scope (docs vs code, etc.)
4. **Questions for Synthesis** - what should synthesis focus on?

A finding without evidence is speculation, not data.

## Phase 3: Synthesis (~15 min)

Identify **tensions** (contradictions between layers), not summaries. A tension is:

- Agent A says X, Agent B says NOT-X
- Finding contradicts documented contract
- Frontend assumes Y, backend implements NOT-Y

Each tension needs: what Layer A holds, what Layer B actually does, impact severity, and evidence from specific agent findings.

## Phase 4: Human Gate

No action without human validation. Present tensions, human decides:

- Real + actionable -> implementation plan (separate session)
- Real + deferred -> backlog item
- Misinterpretation -> close with explanation
- Uncertain -> targeted follow-up

## Session Preservation

Create `claude/current_conversations/YYYY-MM-DD-HHMM-UNIQUEID-<topic>.md` (`node_type: agent-dialogue`) containing: scope definition, all agent reports, synthesis with tensions, human gate notes, follow-up action links.

Recommended agent count: 3-5. Heartbeat timeout: 30 min per agent.

````
