---
profile: autobayes-research
name: TASK-AB-LEARN-001 Codex Goal Profile
description: Native Codex goal profile for closing the remaining AutoBayes learning research.
type: codex-goal-profile
task_id: TASK-AB-LEARN-001
swu_id: SWU-AB-LEARN-001
status: ready
last_updated: 2026-06-07
---

# Codex Goal Profile Result

- Source work-pack: `research/autobayes/work-pack/WORK-PACK.md`
- Selected unit: `SWU-AB-LEARN-001`
- Readiness: `pass`

## Native Goal

```text
/goal Implement SWU-AB-LEARN-001 from research/autobayes/work-pack/WORK-PACK.md: close the remaining AutoBayes learning research into a final source-backed Arcanum operator pack.

Outcome:
Produce or update the local research artifacts needed to close the AutoBayes tower:
- research/autobayes/tracks/paper-claim-ledger.md
- research/autobayes/tracks/bayesian-lens-definition-card.md
- research/autobayes/tracks/parameter-exposure-card.md
- research/autobayes/tracks/cups-caps-boundary-shift-card.md
- research/autobayes/tracks/two-step-symbolic-loss-calculation.md
- research/autobayes/tracks/implementation-residue-note.md
- research/autobayes/FINAL-LEARNING-PACK.md when the synthesis is coherent
- final updates to research/autobayes/GLOSSARY.md, DEFINITIONS.md, DISTILLED-KNOWLEDGE.md, NEXT.md, and residue/open-residue.md

The final result must let the Arcanum developer understand AutoBayes through source-first language and Arcanum-shaped mental models without treating local research as canonical Arcanum vocabulary.

Verification surface:
Read the handoff pack first:
- research/autobayes/work-pack/context/TASK-AB-LEARN-001-CONTEXT.md
- research/autobayes/work-pack/context/TASK-AB-LEARN-001-CONTEXT.json

Then validate:
- formulae/dispatch-spec/scripts/validate-dispatch.py research/autobayes/development/refinement-runs/20260607T070805Z-research-closure-plan/REFINE-DISPATCH.json --json
- rg -n "source kind|promotion_scope|Status:|closed-|open-question|Arcanum reading|Misuse|Do not promote" research/autobayes

If subagents are spawned, report the subagent lifecycle ledger and block success unless every spawned lane is joined, closed, blocked with residue, timed out with residue and reroute, or handed off with reroute.

Constraints:
- Pack-first execution only. Start from the context Markdown and JSON index.
- Write only under research/autobayes/ and its work-pack/refinement-run folders.
- Do not mutate canonical Arcanum source, registries, ontology, inventory, sigils, spells, runtime contracts, generated global skill surfaces, or memory promotion surfaces.
- Source terms first; Arcanum translation second.
- Every closed claim must name its source kind: AutoBayes paper, related paper, derived reading, Arcanum analogy, candidate bridge, or open question.
- Related papers may be used only for named gaps from the handoff pack.
- Extra sources must be reported with the gap they addressed and whether they changed the result.
- No canonical promotion from local glossary, definitions, distills, or bridge decisions.
- Hidden open subagents block success.

Boundaries:
- Source work-pack: research/autobayes/work-pack/WORK-PACK.md
- Selected task: research/autobayes/work-pack/tasks/TASK-AB-LEARN-001-research-closure.md
- Handoff Markdown: research/autobayes/work-pack/context/TASK-AB-LEARN-001-CONTEXT.md
- Handoff JSON/index: research/autobayes/work-pack/context/TASK-AB-LEARN-001-CONTEXT.json
- Existing tower: research/autobayes/README.md, TOWER.md, NEXT.md, gates/closure-gates.md, levels/L2-closure-plan.md, residue/open-residue.md
- Existing receipts: research/autobayes/sessions/full-mode-source-receipts.md and research/autobayes/sessions/task-session-autobayes-all-possible-subagents-result.md
- Primary paper record: https://arxiv.org/abs/2503.18608

Iteration policy:
Work in closure layers. First validate the dispatch and read the handoff pack. Then close the paper claim ledger, then definition cards, then worked examples/loss calculation, then bridge/final distill. After each layer, update residue/open-residue.md and do a read-back check against the closure gates. Use subagents only if approved and useful; every spawned subagent must return lifecycle closeout before parent synthesis.

Blocked stop condition:
Stop and report BLOCK if the handoff Markdown or JSON index is missing, if the dispatch route does not validate, if source meaning cannot be separated from Arcanum analogy, if a required claim cannot be supported by the paper or named related-paper evidence, if the work would require canonical Arcanum mutation, if external research expands beyond named gaps, if any spawned subagent remains hidden/open/pending, or if final artifacts cannot pass the source/promotion/residue read-back check.
```

## Verification Surface

- `formulae/dispatch-spec/scripts/validate-dispatch.py research/autobayes/development/refinement-runs/20260607T070805Z-research-closure-plan/REFINE-DISPATCH.json --json`
- `rg -n "source kind|promotion_scope|Status:|closed-|open-question|Arcanum reading|Misuse|Do not promote" research/autobayes`

## Boundaries

- Write scope: `research/autobayes/`
- Source context: AutoBayes tower artifacts plus the strict handoff pack.
- Excluded scope: canonical Arcanum source and promotion surfaces.

## Handoff Pack

- Markdown: `research/autobayes/work-pack/context/TASK-AB-LEARN-001-CONTEXT.md`
- JSON/index: `research/autobayes/work-pack/context/TASK-AB-LEARN-001-CONTEXT.json`

## Strict Coverage

`pass`

## Fallback Exploration

`named gaps only`

## Extra-Source Reporting

`required`

## Stop Condition

Report `BLOCK` with exact missing source, unsupported claim, unsafe mutation, validation failure, or subagent closeout failure.

## Validation

Profile generated from the ready SWU and strict context handoff pack. Dispatch validation is required before runtime execution.
