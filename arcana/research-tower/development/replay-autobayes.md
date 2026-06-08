# AutoBayes Replay Report

Status: recognition pass with promotion blockers

Target: `research/autobayes/`

Date checked: 2026-06-07

## Purpose

Check whether the draft Research Tower sigil can recognize the completed
AutoBayes research run as a valid tower shape instead of duplicating work.

## Required Artifact Recognition

| Contract item | AutoBayes artifact | Status |
| --- | --- | --- |
| Tower orientation | `research/autobayes/README.md` | pass |
| Tower model | `research/autobayes/TOWER.md` | pass |
| Notation bridge | `research/autobayes/NOTATION.md` | pass |
| Local glossary | `research/autobayes/GLOSSARY.md` | pass |
| Governed definitions | `research/autobayes/DEFINITIONS.md` | pass |
| Distilled knowledge | `research/autobayes/DISTILLED-KNOWLEDGE.md` | pass |
| Claim ledger | `research/autobayes/tracks/paper-claim-ledger.md` | pass |
| Related work | `research/autobayes/tracks/related-framework-crosswalk.md` | pass |
| Bridge decision | `research/autobayes/tracks/arcanum-bridge-decision.md` | pass |
| Final learning pack | `research/autobayes/FINAL-LEARNING-PACK.md` | pass |
| Open residue | `research/autobayes/residue/open-residue.md` | pass |

## Hardening Recognition

| Gate | Evidence | Status |
| --- | --- | --- |
| Promotion boundary | `promotion_scope: local-research-only` in notation and final pack; bridge decision has `promotion_guardrail: local-research-only`. | pass |
| Notation first | Final pack points readers to `NOTATION.md`, which links to shared notation. | pass |
| Borrow/block split | Final pack contains borrow carefully, analogy-only, block, and honest cutoff sections. | pass |
| Subagent closeout | AutoBayes work-pack and task-session results contain explicit subagent closeout rules and reports. | pass |
| Hidden open lanes blocked | AutoBayes hardening task records that hidden open subagents block success. | pass |

## Replay Decision

The AutoBayes tower should be treated as a completed exemplar for the Research
Tower sigil. A replay run should inspect and report the existing artifacts; it
should not create duplicates unless a required artifact is missing or stale.

## Promotion Blockers

Research Tower is still a draft candidate until:

- a compact-mode smoke test proves the sigil can avoid overbuilding;
- a notation-heavy non-AutoBayes paper proves notation behavior is general;
- an experiment harness records low, medium, and complex prompts;
- observability or telemetry shape is defined for meaningful executions;
- registry promotion is explicitly approved.

## Validation Commands Used

```bash
for f in research/autobayes/README.md research/autobayes/TOWER.md research/autobayes/NOTATION.md research/autobayes/GLOSSARY.md research/autobayes/DEFINITIONS.md research/autobayes/DISTILLED-KNOWLEDGE.md research/autobayes/tracks/paper-claim-ledger.md research/autobayes/tracks/related-framework-crosswalk.md research/autobayes/tracks/arcanum-bridge-decision.md research/autobayes/FINAL-LEARNING-PACK.md research/autobayes/residue/open-residue.md; do test -f "$f"; done
rg -n "promotion_scope|local-research-only|Notation Reading|What To Borrow Carefully|What To Keep Analogy-Only|What To Block|Remaining Honest Cutoff" research/autobayes/FINAL-LEARNING-PACK.md research/autobayes/NOTATION.md research/autobayes/tracks/arcanum-bridge-decision.md
rg -n "task-session|subagent|Subagent|closed|integrated|all possible" research/autobayes/sessions research/autobayes/work-pack -S
```

