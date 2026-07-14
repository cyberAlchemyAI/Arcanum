---
name: create-skill
description: Author or evolve an invocable Claude Code skill (SKILL.md) through a guided interview — gate whether it should be a skill, draft the routing description, set naming and frontmatter, write a dense body, self-check and verify it fires. Use when asked to create, scaffold, write, design, or edit a skill or slash-command.
argument-hint: "[skill-name] [one-line purpose...]"
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
---

# create-skill

Authors or evolves ONE invocable skill: a `<skills-dir>/<name>/SKILL.md`, triggered as `/<name>`.
Guided — ASK at each gate; do not assume.

## 0 — Gate: should this even be a skill? (ask, then branch)
Ask the user for the one purpose in a sentence. Then route:
- a standing behavior the model should ALWAYS do → a project rule (CLAUDE.md / AGENTS.md), not a skill; stop, tell the user.
- a tool-restricted worker or persona → an agent; stop, tell the user.
- passive lookup material → a plain reference doc; stop, tell the user.
- a user-invocable verb-action → continue.
Glob the skills dir for an existing skill with the same name. Exists → go to "Editing" below. Else → new.

## The bar — what an excellent skill is
The smallest artifact that fires at the right moment, makes the model act without hesitating, and
blocks its task's typical error:
1. **Discoverable** — routes on the `description` ALONE (body unseen at selection). Weak description = dead skill.
2. **Coherent scope** — one purpose; may do several *related* things, never unrelated ones.
3. **Dense** — ideally self-contained inline. Pointing to another **skill** is fine when this one *routes* to it
   (a dispatcher) or reuses its owned procedure; the smell is pointing to a passive doc to dodge condensing
   your own steps.
4. **Imperative, ordered where it matters, right altitude** (pin the what + guardrails, don't micro-manage),
   **failure-mode aware**.

The steps below apply this bar; §4 verifies against it.

## 1 — Description (the gate that decides life)
Draft the `description` first: third person, packing what + when + trigger words a user types.
Grep existing skill descriptions for those triggers — if another claims them, narrow yours.
Show it to the user and get a yes. Weak description → stop; the skill is dead on arrival.
- BAD: `Helps with tests`
- GOOD: `Audit test coverage for uncommitted changes — finds missing, incomplete, fragile tests. Use before committing.`

## 2 — Name + frontmatter
Name: lowercase-hyphen, ≤64 chars (platform limit), unique; directory name equals `name`.
Required: `name`, `description`. Earned only: `argument-hint`, `allowed-tools` (least privilege),
`agent`. Add nothing else — a project's doc-frontmatter convention (if any) does NOT apply to a
SKILL.md; that is the most common mistake.

## 3 — Body
Inline your own steps. The only legitimate exits are The bar's two — router-dispatch (name the
skills you route to) or bulky-reference (link a sibling `reference.md`/script/template, loaded only
when referenced). Never link out your own steps to dodge condensing them.

## 4 — Write, self-check, verify it fires
Write the file, then check mechanics: frontmatter opens line 1 and closes; `name` == directory,
≤64 chars; only the five allowed fields; `allowed-tools` matches the tools the body uses; the body
meets **The bar**. If this harness keeps a separate skills dir for subagents, mirror the file there
when subagents must invoke it. Then verify: in a fresh session, a prompt using the trigger words
should surface `/<name>`; if not, the description is too weak — fix it.

## Editing an existing skill
The risk is the routing trigger, not a blank page. If you change what the skill DOES, update its
`description` to match — routing is description-only, so a stale description silently breaks
selection. Never broaden a description without re-grepping siblings for new overlap. Re-run §4.
