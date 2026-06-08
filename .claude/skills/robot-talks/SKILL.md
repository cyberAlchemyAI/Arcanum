---
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcana/robot-talks/SKILL.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
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
