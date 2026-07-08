---
description: How to write a subagents-findings document — synthesis of the single subagents-research file from one dispatch.
---
# Subagents Findings Writing

## Purpose

A `subagents-findings` document is the **synthesis of one full dispatch**, authored by the **writer** (pipeline stage 4): it reconciles the explorer returns transcribed in the single `research.md` — together with the synthesizer's reconciliation and the reviewers' attacks — and turns them into claims the rest of the vault can build on.

One dispatch → one findings file. If you are pulling from research across multiple dispatches, you are writing a discovery, not findings.

If you are simply rewriting a single explorer's output in nicer prose, you are writing nothing — go back and synthesize.

There is **no template** to fill. Read the research and write the synthesis in whatever form serves it best.

---

## Document Structure

Fixed at the top and bottom; free in between.

**Opening, in this order:**

1. **Goal** — what the dispatch set out to achieve. One to two sentences.
2. **TL;DR** — the synthesis answer in a few sentences: what the research adds up to. No build-up — the conclusion first.
3. **Context** — where the need for the dispatch arose and what made a single inline investigation insufficient.

**Closing — mandatory, the last section:**

- **Open Questions** — the investigation residue: coverage gaps and sub-questions this dispatch could not resolve. One entry per question, each with a recommendation and a **named owner**; numbering need not be contiguous — never renumber; flag blockers inline.

  ```
  - **OQ-N** — <question>. Recommendation: <rec>. Owner: <named owner>.
  - **OQ-N (BLOCKER)** — <blocker question>. Recommendation: <rec>. Owner: <named owner>.
  ```

**Everything between the opening and Open Questions is the writer's call.** Choose the sections that best convey *this* synthesis and drop what the material doesn't need. Useful candidates — not a required set:

- **Agreements** — claims that multiple explorers' research independently supports (cite ≥2 explorers; qualify as `strong` / `majority` / `partial`).
- **Disagreements** — where explorers diverge: the opposing positions with citations, and a recommendation (which side, escalate as `contradicts`, or re-dispatch).

You may propose a structure you think fits the dispatch better.

---

## Edges the generated `findings.md` must carry

In its `## Connections` block, the findings artifact must declare:

- `derives-from` → the `research.md` it synthesizes (`./research.md`). This is the reciprocal of the `derives` edge the research file declares back toward it.

---

## Quality Checks Before Finishing

- [ ] Goal, TL;DR, and Context open the document, in that order
- [ ] Open Questions closes the document — each with a recommendation and a named owner
- [ ] File path is `<working_folder>/findings.md` (the root of the working folder), not under `vault/`
- [ ] The `## Connections` block declares `derives-from` → the research file
- [ ] Every `## Agent N` section of the research file is accounted for — nothing dropped silently
- [ ] Claims are grounded in the research, not introduced from nowhere
- [ ] Where explorers disagree, the synthesis says what to do about it
- [ ] The document synthesizes — it does not just paraphrase one explorer

---

## Navigation

- Frontmatter cheatsheet: `.claude/skills/custom/frontmatter.md`
- Edge catalog: `.claude/skills/custom/edges.md`
- How to write the upstream research file: `.claude/skills/custom/domainspec-research-writing.md`
- Node-type semantics: `.claude/skills/custom/frontmatter-semantics.md`
