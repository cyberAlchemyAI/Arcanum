---
name: close-session
description: Close a session and create a governed session node under sessions/.
---

# Close Session Workflow

This repository-local package is adapted from
`cyberalchemy-orchestrator/.codex/skills/close-session`. Its frontmatter guide is
packaged at [references/frontmatter.md](references/frontmatter.md) so the skill
does not depend on another runtime tree.

## Step 0 — Triage

**Create a node if any is true:** repository documentation changed, domain code
changed, an architectural decision was made, verification artifacts changed, or
a contradiction was found or resolved.

**Skip if:** no documentation or code changed and the exchange was purely Q&A
with no decisions. Say *“Q&A-only session. No session node created.”* and stop.

---

## Step 1 — Write the summary and forward registers

The closing agent authors the node itself. First read
`references/frontmatter.md` completely, then choose concrete topical tags,
exactly one primary `layer`, and meaningful typed Connections. Do not delegate
these judgments.

Write up to **10 sentences** covering what the session set out to do, what was
decided and why, and what was done. Use no subheadings or per-file detail in the
summary. A reader should grasp the arc without access to the conversation. Draft
the forward registers in Step 2 yourself.

---

## Step 2 — Assemble the node

File: `sessions/YYYY-MM-DD-HHMM-{short-slug}.md`

Every new node emitted by this workflow has `artifact_kind: session`.

```markdown
---
tags: [{tag1}, {tag2}]
artifact_kind: session
layer: {project | domain | capability | feature | task | others}
version: 0.1.0
created_at: YYYY-MM-DDTHH:MM:SS±HH:MM
updated_at: YYYY-MM-DDTHH:MM:SS±HH:MM
expires: {calendar date of created_at + 60 days}
decisions_made: true | false
contradictions_found: true | false
specs_updated: [paths or []]
promoted_candidates: [nodes or []]
expected_importance: {0-10}
importance_rationale: "{sentence}"
---

# {Title}

## Summary

{Maximum 10 sentences from Step 1.}

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [real context or artifact](path) | `is-part-of` | Why this session belongs structurally to that context. |

## Open questions

{Undecided claim or conjecture. Omit if none.}

## Next steps

{Decided action, method known — imperative and priority-ordered. Omit if the arc is closed.}

## Recommendation

{The keystone among the items above and how to attack it. Omit on routine sessions; never use a placeholder.}

## Files touched

{Flat bullet list of paths. No table and no descriptions.}

## Extra section

{Include only when the user asked to register something specific from this session.}
```

`## Connections` is mandatory. Use the three-column table only for supported
relationships with real targets. If no real relationship is known, replace the
table with:

```text
No real connection was identified in this session.
```

A session may use `is-part-of` toward its actual enclosing project, domain,
capability, feature, or task context. It may use `validates`, `contradicts`,
`contextualizes`, `derives-from`, or `other` only when evidence supports that
relationship. `contains` is the inverse of `is-part-of`; add the inverse to a
governed target only when that target is in scope for the same change. Do not
infer Connections from directory placement or from files merely read,
mentioned, or touched.

Contradictions belong in `## Connections` when a typed target relationship
exists. Add separate contradiction prose only when it contributes useful
narrative that is not duplicated by the edge row.

`## Files touched` is an operational record only and never generates
Connections.

### Forward registers

- The three registers are distinct. **Open questions** are undecided and become
  resolved, not “done”; **Next steps** are decided labor; **Recommendation**
  ranks across them and asserts nothing new. If a line seems to fit two, ask
  whether it can be done or claims a truth, then move it to the matching
  register.
- **Open questions** name an epistemic gap the session opened but did not close.
  If the method is already known and only labor remains, use **Next steps**. A
  question may remain here even when it mentions an existing artifact.
  File-path existence does not establish an edge; add a Connection only when a
  real typed relationship can be asserted.
- **Next steps defer to the backlog.** This repository has no `backlog/` yet, so
  keep them body-only with `promoted_candidates: []` until one exists.
- **Recommendation obeys the subset rule.** Recommend a direction, never assert
  the outcome; name the licensing fact or self-label a hunch. Reference only
  items in the sections above.
- Omit, do not pad. No open business means omitting the empty forward sections.
  Absence is the signal.

> **Hard cap:** The body below frontmatter must not exceed **200 lines**. The
> forward sections count toward the cap and have the lowest priority: trim them
> first, then omit them.

---

## Step 3 — Final checks

Before finishing, the creating agent checks directly that:

1. the frontmatter is valid and follows `references/frontmatter.md`;
2. `artifact_kind` is `session`, tags are topical, and exactly one layer is
   selected;
3. `## Connections` has supported typed edges with real targets or the explicit
   no-connection statement;
4. files touched have not been converted mechanically into edges;
5. the forward registers obey their distinct roles; and
6. the body stays within the 200-line cap.

There is no automatic review in this workflow for now. Any future review must
use the repository's governed subagent workflow.
