---
description: How to write a subagents-research document — one file per dispatch, verbatim explorer returns assembled under per-explorer headers.
---
# Subagents Research Writing

## Purpose

A `subagents-research` document records the **verbatim returns of every explorer in a single domainspec-subagents-strategy dispatch**, assembled into **one file per dispatch** under stable per-explorer headers (`## Agent N — <one-line brief>`). It is appended **mechanically by the strategist** (the parent that owns the dispatch) — only the explorer returns are transcribed; synthesizer and reviewer output is not (it survives digested, and cited, in `findings.md`).

One dispatch → one `research.md` file → multiple `## Agent N — ...` sections.

If you find yourself reconciling claims across explorers, summarizing an explorer's output, or producing one file per explorer — stop. The first two are findings work; the third produces a malformed artifact.

---

## Mandatory Document Structure

There is no template and no preamble. The file is **only** the appended verbatim returns of the explorers — one section per explorer, nothing else. No Context, no Goal, no synthesis: that framing lives in `findings.md`.

### `## Agent N — <one-line brief>` (one per explorer, in dispatch order)

One section per explorer the strategist dispatched. Header format is exact: `## Agent N — <brief>` so that the slug `agent-n--brief` is a stable anchor for `findings.md` citations.

The body of each section is the **explorer's return verbatim**:

- Do **not** edit, summarize, paraphrase, reformat, or "tidy up."
- If the explorer returned its own structured subsections (Findings, Gaps, Limits, etc.), preserve them as-is.
- If the explorer returned messy prose, that messy prose is the artifact. Fidelity beats neatness.

Each explorer's return stands alone in its own section. Cross-explorer synthesis lives in `findings.md`.

---

## Anti-Patterns (malformed artifacts)

Each of the following produces a malformed artifact:

- **One file per explorer.** Forbidden. The dispatch produces exactly one `research.md` containing N `## Agent N — ...` sections.
- **Adding Context, Goal, or any framing.** Forbidden. Research is pure appends; the Context/Goal framing lives in `findings.md`.
- **Editing, summarizing, or reformatting explorer output.** Forbidden. This is transcription, not curation. Summarization destroys the audit trail that findings citations depend on.
- **Cross-explorer synthesis in this file** ("Agent A said X but Agent B said Y", reconciliation, tensions, implications). Forbidden here. That work belongs in `findings.md`.
- **Transcribing non-explorer output.** Forbidden. Only the explorer returns go here; the synthesizer's reconciliation and the reviewers' attacks live — digested and cited — in `findings.md`.
- **An agent writing this file directly.** Forbidden. Agents return text; the **strategist** persists this file by following this skill.

---

## Edges the generated `research.md` must carry

In its `## Connections` block, the research artifact must declare:

- `derives` → the `findings.md` that derives from it (`./findings.md`) — the inverse of the `derives-from` edge the findings file declares back toward it.

---

## Quality Checks Before Finishing

- [ ] Exactly one file produced for the dispatch — no per-explorer files.
- [ ] File path is `<working_folder>/research.md` (the root of the working folder).
- [ ] No Context, Goal, or any preamble — the file opens straight into `## Agent N` sections.
- [ ] One `## Agent N — <brief>` section per explorer the strategist dispatched, in dispatch order, with exact header format.
- [ ] Each agent section contains the explorer's return verbatim — no edits, no summary, no reformatting.
- [ ] No synthesizer/reviewer output, no cross-explorer reconciliation, no tensions, no implications, no Dispatch record in this file.
- [ ] The `## Connections` block declares `derives` → the findings file.

---