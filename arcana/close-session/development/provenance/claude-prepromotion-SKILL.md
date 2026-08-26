---
name: close-session
description: Close a session and create a vault conversation node
---

# Close Session Workflow

> **Classification source of truth:** `docs/vault/ontology-conventions.md`.

---

## Step 0 — Triage

**Create a node if any is true:** vault doc changed/created/deleted, domain code changed, architectural decision made, tests added/modified, contradiction found/resolved.

**Skip if:** no vault/code changes AND purely Q&A with no decisions. Say *"Q&A-only session. No vault node created."* and stop.

**Scratchpad:** Check `claude/current_conversations/` for a session file. If found, use it as primary input and delete it after saving the node.

---

## Step 1 — Write Summary (do this yourself)

Write up to **10 sentences**: what the session set out to do, what was decided (and why), what was done. No sub-headings, no per-file detail. A reader should grasp the arc without access to the conversation. Also draft the **Forward** lines yourself (Step 3). The discriminating test is a judgment — never delegated to Sonnet.

---

## Step 2 — Delegate classification to Sonnet

Spawn an Agent (model: sonnet) with your summary + list of files touched. It returns:

1. **node_type** (first match wins): constitution → premise → conceptual → test → discovery → implementation-plan → audit → spec (fallback).
2. **tags, layer, nature** per `ontology-conventions.md`.
3. **expected_importance** (0–10) + **importance_rationale** (one sentence).
4. **Contradictions** — only if a vault node was validated, contradicted, or questioned. One bullet per edge. Omit section if none.
5. **Files touched** — flat list of paths, no descriptions. Git has the detail.

Sonnet returns the above only — it never writes the `## Forward` block (that block is yours, Step 1).

---

## Step 3 — Assemble the node

File: `docs/vault/conversations/YYYY-MM-DD-HHMM-{short-slug}.md`

```markdown
---
tags: [{tag1}, {tag2}]
node_type: {type}
is_session: true
layer: {layer}
nature: {nature}
status: active
created: YYYY-MM-DD
timestamp: YYYY-MM-DDTHH:MM:SS±HH:MM
expires: {created + 60 days}
conversation_id: {id}
decisions_made: true | false
contradictions_found: true | false
specs_updated: [paths or []]
promoted_candidates: [nodes or []]
expected_importance: {0-10}
importance_rationale: "{sentence}"
---

# {Title}

## Summary

{max 10 sentences from Step 1}

## Contradictions

{Omit if none. One bullet per edge: "validates/contradicts/questions {node} — reason."}

## Open questions

{A claim the session did NOT decide — a question or conjecture, never a task. Node-less only: a question naming a vault/spec node is a `questions {node}` Contradictions edge, not an Open question. Omit if nothing is genuinely undecided.}

## Next steps

{A decided action, method known — only labor remains. Imperative, priority-ordered, what+where. A step worth standing tracking is promoted to the backlog and linked via `promoted_candidates`; the line here is then a pointer. Omit if the arc is closed.}

## Recommendation

{Your call: of the items above, the keystone and how the next session should attack it. Recommend a direction, never assert the outcome; name the licensing fact — a validated node, a landed test, a resolved contradiction — or self-label a hunch. References only items above. Omit on routine sessions; never a placeholder.}

## Files touched

{Flat bullet list of paths. No table, no descriptions.}
```

### Forward registers

Apply these while drafting (Step 1) and assembling (Step 3) the three forward sections.

- Three distinct registers, written by you. **Open questions** are undecided (resolved, never "done"); **Next steps** are decided labor; **Recommendation** ranks across them and asserts nothing new. If a line fits two, apply the discriminating test — can it be done? does it claim a truth? — and move it.
- **Open questions are node-less only.** A question naming a vault/spec node is a `questions {node}` edge → `## Contradictions`, not Open questions (else the two double-record). Mechanical test: if the target can be written as an existing file path, it is a Contradictions edge; otherwise an Open question.
- **Next steps defer to the backlog.** A step worth standing tracking is promoted to the backlog and linked via `promoted_candidates`; the Next-steps line is then only a pointer. To promote: append it to `docs/vault/backlog/{topic}.md` per `.claude/skills/custom/backlog-pattern.md`, then list that path. Not promoting? Keep it body-only and leave `promoted_candidates: []`.
- **Recommendation obeys the subset rule.** Recommend a direction, never assert the outcome; name the licensing fact (validated node, landed test, resolved contradiction) or self-label a hunch. It references only items in the sections above.
- Omit, don't pad. No open business → omit the empty sections entirely. Absence is the signal.

> **Hard cap:** The body (below frontmatter) must not exceed **200 lines**. If it does, you are writing too much — cut. The three forward sections count inside the 200 and are the lowest-priority — if over cap, trim them first, then omit them.

---

## Step 4 — Review (two Sonnet agents)

Before the node is final, spawn **two Agents (model: sonnet)** in parallel, each given the assembled node + the list of files touched. They review independently:

1. **Classification & frontmatter** — node_type, tags, layer, nature, importance, and any edges match `ontology-conventions.md`; frontmatter is well-formed; the body is within the 200-line cap.
2. **Body discipline** — the three forward registers obey the discriminating test and subset rule; Open questions are node-less; Next steps defer to the backlog; Recommendation references only items above and names a license or self-labels a hunch; no narration.

Each returns **PASS** or a list of concrete problems. **If either returns problems, send the node back to the writing agent (the one that wrote it, Steps 1/3) to fix, then re-review.** Only a clean PASS from both finalizes the node.
