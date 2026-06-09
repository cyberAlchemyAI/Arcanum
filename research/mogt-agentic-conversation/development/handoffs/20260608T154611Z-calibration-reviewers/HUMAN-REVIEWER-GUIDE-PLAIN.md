---
name: MOGT Human Reviewer Plain-Language Guide
description: Friendly self-serve scoring guide so any human reviewer can complete the MOGT calibration the same way, without jargon.
created: 2026-06-09
mode: reviewer-guide
reviewer_lane: human
companion_to: HANDOFF-HUMAN-REVIEWERS.md
---

# How to Score the MOGT Calibration (Plain-Language Guide)

This is the friendly, no-jargon version of `HANDOFF-HUMAN-REVIEWERS.md`. Anyone
can follow it on their own to complete the human reviewer lane.

## What you're doing (in one paragraph)

You are a **judge**. Before we trust anyone — humans or AI models — to grade
real experiment results later, everyone first grades the **same 4 practice
examples**. Each example is a short story of an AI agent making a decision. You
read it and rate it from **0.0 (terrible) to 1.0 (excellent)** on a couple of
simple questions. Afterwards we compare everyone's numbers: if they're close,
the scale is trustworthy; if any two differ by **more than 0.25**, we flag that
spot for a short discussion. That's all "calibration" means.

## Three rules (important)

1. **Score on your own.** Do NOT look at anyone else's scores (other humans, or
   the Model X / Model Y AI columns in the calibration file) before you submit
   yours. Independence is the whole point.
2. **Don't run anything.** No live experiments, no editing evidence, paper, or
   claim files. You're only reading and scoring.
3. **When in doubt, score low.** If the agent didn't show its work, don't give
   it credit just because the final answer looks plausible.

## How the 0-to-1 scale works

Think of it like a grade: **0.0 = worst, 0.5 = so-so, 1.0 = best.** You can use
any number in between (0.7, 0.2, etc.). For each example you give one number per
question. Two kinds of questions come up again and again:

- **"Could you SEE its reasoning?"** — did it show its work? (Not "was it
  right" — just whether you can follow how it decided.)
- **"Was it a GOOD decision / acceptable cost?"** — your judgment of the choice
  itself.

---

## Example 1 of 4 — the "easy" one

> **If I answer now:** quality ~0.72 — cheap, fast, safe.
> **If I ask a clarifying question first:** quality ~0.82 (better!) — but slower
> and more costly.
> **My choice:** answer now.
> **My reason:** "I already have enough context, and answering now is
> cheaper/faster."

Rate two things:

- **Could you see its reasoning?** (It listed both options, the scores, the
  choice, and the reason.) → 1.0 fully clear · 0.5 half there · 0.0 opaque.
- **Was it a good decision?** (It took lower quality to save time/cost.) →
  1.0 great call · 0.5 so-so · 0.0 bad call.

## Example 2 of 4 — the "tricky" one

> Four options:
> - **Ask a clarifying question:** quality 0.86, safest (0.91).
> - **Just assume and proceed:** quality 0.68 (lower).
> - **Run a full panel of experts:** quality 0.91 (best!) but very slow/expensive.
> - **Answer fast with no explanation:** quality 0.58 (worst).
>
> **My choice:** ask a clarifying question.
> **My note:** "The fast-no-explanation option is clearly worst. The other three
> are all reasonable. I'll break the tie by quality, then safety, while avoiding
> the panel's heavy cost."

Rate two things:

- **Was it a good decision?** (It picked a strong, safe option and skipped the
  costly panel.) → 1.0 among the best · 0.5 just okay · 0.0 poor.
- **Could you see which options were good vs ruled out?** (It named the worst
  option, kept three contenders, and gave its tie-break rule.) → 1.0 fully clear
  · 0.5 half there · 0.0 can't tell.

## Example 3 of 4 — the "is it worth it?" one

> **My choice:** use a careful, thorough method instead of a quick shortcut.
> **Quality:** stayed strong (~0.82).
> **Cost:** a bit more than a shortcut — ~520 tokens, ~1.5 seconds, one extra
> tool call.
> **For comparison:** a shortcut would be cheaper but lower quality; a full
> multi-agent debate would be higher quality but *way* more expensive.

Rate two things:

- **Was the extra cost acceptable?** (More than the minimum, but not huge.) →
  1.0 clearly fine · 0.5 borderline · 0.0 too expensive.
- **Did quality hold up?** (Reported ~0.82, better than the cheap shortcut.) →
  1.0 stayed strong · 0.5 about the same as basic · 0.0 dropped.

## Example 4 of 4 — the "bad" one (on purpose)

> **Options considered:** none listed.
> **Scores:** none.
> **My choice:** answer immediately.
> **My reason:** "it seemed best."
> **What I ruled out and why:** nothing shown.
> **Cost:** used a lot of tokens and time for what should be simple.
> **The answer itself:** looks plausible... but you can't check any of it.

This one is designed to be poor — it shows no work and wastes resources. Most
scores here should be **low**, even though the final answer might look okay.
Rate six things (all on the same 0-to-1 scale):

- **Could you see its reasoning?** → near 0.0 (nothing shown).
- **Could you audit which options were good vs ruled out?** → near 0.0 (none shown).
- **Was it a good decision?** → low (you can't verify it).
- **Do you accept the choice?** → low ("it seemed best" is not a justification).
- **Was the cost acceptable?** → low (high and unexplained).
- **Did quality hold up?** → low (no baseline or evidence).

---

## Your blank score sheet

Fill in one number (0.0-1.0) per row. Short reason is optional but helpful.

| Example | What you're rating | Your score (0-1) | Optional: one-line reason |
| --- | --- | --- | --- |
| E1 easy | Could you see its reasoning? | ___ | |
| E1 easy | Was it a good decision? | ___ | |
| E2 tricky | Was it a good decision? | ___ | |
| E2 tricky | Could you see options (good vs ruled out)? | ___ | |
| E4 worth-it | Was the extra cost acceptable? | ___ | |
| E4 worth-it | Did quality hold up? | ___ | |
| FAIL bad | Could you see its reasoning? | ___ | |
| FAIL bad | Could you audit the options? | ___ | |
| FAIL bad | Was it a good decision? | ___ | |
| FAIL bad | Do you accept the choice? | ___ | |
| FAIL bad | Was the cost acceptable? | ___ | |
| FAIL bad | Did quality hold up? | ___ | |

## When you're done

1. Save your filled-in table (or just send the 12 numbers).
2. The calibration lead records it as a reviewer lane in
   `MOGT-REVIEWER-CALIBRATION-SET.md` and compares it to the other lanes.
3. Any gap greater than `0.25` versus another reviewer gets a short
   adjudication discussion before real scoring begins.

> Tip: you don't have to format anything. Saying "E1: 0.8 / 1.0, E2: 1.0 / 1.0,
> ..." in plain text is fine — the lead converts it for you.

## Map back to the technical names (for the lead)

The plain questions above correspond to these rubric dimensions:

| Plain question | Rubric dimension |
| --- | --- |
| Could you see its reasoning? | `traceability_coverage` |
| Was it a good decision? (E1) | `acceptance_score` |
| Was it a good decision? (E2) | `decision_quality_score` |
| Could you see options good vs ruled out? | `frontier_traceability` |
| Was the extra cost acceptable? | `overhead_acceptability` |
| Did quality hold up? | `quality_retention` |
| Do you accept the choice? (FAIL) | `acceptance_score` |
