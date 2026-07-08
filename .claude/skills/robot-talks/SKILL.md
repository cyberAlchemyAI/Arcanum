---
name: robot-talks
description: Run a multi-agent parallel investigation that maps cross-layer tensions before any fix — decompose by concern, explore in parallel, synthesize contradictions, gate on a human.
---

# robot-talks — multi-agent cross-layer investigation

**What this is.** An auditing tool. You spawn parallel agents, each on one bounded concern, and
synthesize their findings into **tensions** — places where one layer's assumption contradicts
another layer's reality. It maps misalignment; it does **not** implement fixes.

**What you produce.** A session document holding the scope, every agent report verbatim, the
synthesized tensions, and the human-gate decision.

**The procedure.** Setup → Explore → Synthesize → Human gate → Preserve.

## When to run it

Run only if **every** box is YES:

- [ ] Problem spans 2+ distinct layers (not a single-file bug or local refactor)
- [ ] A single investigator would trade depth for breadth
- [ ] You need to identify contradictions **before** acting (audit, not implementation)
- [ ] Cost of misunderstanding exceeds the cost of a ~90 min investigation

If any box is empty, route elsewhere:

| Instead you have | Use |
|---|---|
| Single-file bug | the `systematic-debugging` skill |
| "How does X work?" | the `gitnexus-exploring` skill |
| Refactor in one module | the `gitnexus-impact-analysis` skill |
| Well-specified feature | implement directly |

## 1. Setup (~15 min)

Scope has two stages with distinct ownership. **Agents do not spawn until the user approves.**

**Stage A — user defines the problem.** Do NOT proceed until the user has stated both. Ask if missing:

1. **Central question** — what misalignment are we investigating?
2. **Assumptions to challenge** — what we think is true but might be wrong.

**Stage B — you propose the strategy.** Based on the user's input:

3. **Agent roles** — each with a concern, a central question, and explicit exclusions.
4. **Strategy check** — state one alternative decomposition you considered and why you rejected it.
   Present both the chosen strategy and the alternative to the user.

**Decompose by concern, not by files.** File-based cuts overlap; concern-based cuts don't.

- WRONG: "Agent 1 reads `frontend/*`, Agent 2 reads `backend/*`" — file-based, likely overlapping questions.
- RIGHT: "Agent 1: API contract assumptions. Agent 2: backend mutation implementation. Agent 3:
  frontend error handling. Agent 4: concurrency semantics" — concern-based, non-overlapping
  questions, may read the same files.

Two tests before spawning:

- **Concern overlap** — if two agents could produce contradictory answers to *the same question*,
  their scopes overlap; redefine. Answering *different* questions off the *same* evidence is fine —
  tension discovery often needs shared evidence.
- **Coverage** — list the system's major assumptions; assign each to exactly one agent. Any
  unassigned assumption is a blind spot.

If the scope can't be written in clear prose, the robot-talk can't proceed.

**Scope template:**

```markdown
## Investigation Scope

**Central Question:** [what tension or gap are we investigating?]
**Why Now:** [what triggered this?]

**Agent Roles:**

| Agent | Concern | Central Question | Out of Scope |
|-------|---------|-----------------|--------------|
| Agent 1 | [layer/concern] | [what should it answer?] | [what NOT to investigate] |
| Agent 2 | [different concern] | [what should it answer?] | [what NOT to investigate] |
| Agent 3 | [different concern] | [what should it answer?] | [what NOT to investigate] |

**Assumptions to Challenge:**
- [Layer A assumes X — is it true?]
- [Layer B guarantees Y — does it actually?]

**Success Criteria:** [investigation complete when…]
```

## 2. Explore (~15 min per agent, parallel)

Spawn the agents in parallel; each investigates independently within its bounds. Every agent
reports in this mandatory format:

1. **Key findings** — 3–5 bullets, each with evidence (file, line number, doc reference).
2. **Gaps or inconsistencies** — what is missing, undocumented, or contradictory within scope.
3. **Local tensions** — conflicts inside this scope (docs vs. code, etc.).
4. **Questions for synthesis** — what should synthesis focus on from this report?

A finding without evidence is speculation, not data.

## 3. Synthesize (~15 min)

Identify **tensions** — contradictions between layers — not summaries. A tension is one of:

- Agent A says X, Agent B says NOT-X.
- A finding contradicts a documented contract.
- Frontend assumes Y, backend implements NOT-Y.

Tensions are **found, not created**: if synthesis can't point to which finding contradicts which
other finding or contract, there is no tension. A synthesis without explicit tensions is a summary.

**Tension template:**

```markdown
## Tension: [Descriptive Name]

**Held by [Layer A]:** [the assumption or expectation]
**Reality in [Layer B]:** [what the code/system actually does]
**Impact:** [severity] — [what breaks, who is affected]
**Evidence:**
- Agent 1: [specific finding]
- Agent 2: [specific finding that contradicts]
```

Single pass is the default. **Iterate at most once**, and only if the human gate asks for clarity
on a specific tension or a contradiction surfaces only after the first pass. To iterate: author one
targeted follow-up question (narrow, single concern), re-assign it to the original agent(s), run a
second synthesis pass, and return to the gate. Do NOT iterate to "get more findings" or because
synthesis raised many questions — that is scope creep, and it's a signal to fix scope design next
time. Each iteration costs ~20 min; more than one round needs explicit human approval.

## 4. Human gate

No action without human validation. Present the tensions; for each, the human decides:

| Verdict | Next step |
|---|---|
| Real + actionable | Author an implementation plan (separate session) |
| Real + deferred | Create a backlog item with justification |
| Misinterpretation | Close with explanation; document if others might hit the same confusion |
| Uncertain | Targeted follow-up (the single iteration above) |

To separate a real tension from a misinterpretation, ask: Is the contradiction unintentional (not
legacy compatibility, migration, or a documented exception)? Does it cause observable problems
(bugs, friction, missed requirements)? Does it violate a documented expectation? "Yes" on these
points to a real tension; "no" points to an accepted design choice.

## 5. Preserve the session

Write `claude/current_conversations/YYYY-MM-DD-HHMM-UNIQUEID-<topic>.md` with
`node_type: agent-dialogue`, containing:

- **Investigation scope** — from step 1.
- **Agent reports** — each verbatim, with findings and evidence.
- **Synthesis** — all identified tensions with evidence.
- **Human gate notes** — validation, decisions, authorization.
- **Follow-up actions** — links to resulting plans, backlog items, or doc updates.

Purpose is provenance: when someone later asks "why did we change X?", the answer traces back here.

## Standing rules

1. **Audit, not implementation** — robot-talks map how a thing is misaligned; they never "fix this thing."
2. **Bounded scope** — if you can't state what an agent is *not* investigating, you don't have a robot-talk.
3. **Concerns don't overlap; evidence may** — no two agents answer the same question; sharing an artifact is fine.
4. **Full traceability** — every synthesis statement traces to a finding, every finding to code, docs, or observable behavior. No assertion without evidence.
5. **Human validation before action** — mandatory, every time.
6. **Initial and final positions both preserved** — when a robot-talk feeds a downstream synthesizer (e.g. a `review` or research dispatch that runs it), record each agent's *initial* finding and its *final* position after any iteration, so premature convergence (collapse) stays detectable; never overwrite an agent's first report with its revision.

## Timeline

| Phase | Typical duration |
|---|---|
| Scope definition | ~10 min |
| Parallel exploration | 15–20 min per agent |
| Synthesis | 15–20 min |
| Human gate | 15–30 min |

**Agent count:** 3–5. Fewer than 3 and a single agent is cheaper; more than 5 and synthesis becomes
unwieldy. **Heartbeat:** if no agent completes within 30 min, force synthesis with partial findings
tagged `partial_synthesis`.
