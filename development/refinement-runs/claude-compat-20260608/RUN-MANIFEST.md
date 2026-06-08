# Run Manifest — claude-compat-20260608

- target: `arcanum/` Claude skill surface + installer
- preset: full | research: research-if-gap-appears (no external research)
- subagents: recommended → granted; Claude `Agent` workers (native Arcanum capabilities `blocked`, substituted with claude-agent)
- status: pass (non-executed plan delivered)

## Canonical 10-stage loop

| # | Stage | Surface | Artifact | Status |
|---|-------|---------|----------|--------|
| 1 | Context Builder | claude-agent (Explore) | stages/01-context-builder.md | pass |
| 2 | Invoke Define | main-loop | REFINE-SEED-PROPOSAL.md | pass |
| 3 | Interrogation (refine-review) | folded into stage 7 | stages/03-interrogation-distill.md | pass |
| 4 | Research decision | refine | (no-research) | pass |
| 5 | Distill | folded into stage 7 | stages/03-interrogation-distill.md | pass |
| 6 | Invoke Design (A/B tournament) | claude-agent (Plan ×2) | stages/02-design-tournament.md | pass |
| 7 | Interrogation (refine-design-review) | claude-agent | stages/03-interrogation-distill.md | pass |
| 8 | Distill Repair | claude-agent | stages/03-interrogation-distill.md | pass |
| 9 | Invoke Plan | main-loop | RESULT.md | pass |
| 10 | Final Interrogation + Synthesis | main-loop | RESULT.md | pass |

## Owner boundaries
- Refine: seed, research decision, dispatch, runtime handoff, manifest/index, synthesis.
- Dispatch Spec: route-shape (hand-validated; native skill blocked).
- Stage capabilities: native artifacts (substituted by claude-agent receipts).

## Blocked / substitutions
- Native Arcanum capability skills (context-builder, invoke, interrogation, distill, dispatch-spec) are not installed as Claude skills → all runtime-backed stages recorded `native_capability=blocked, substituted_with=claude-agent`. This is itself the motivating problem the plan fixes (dogfooding, Step 7).
