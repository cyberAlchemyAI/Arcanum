# research.md — collected explorer returns

> Dispatch `2026-06-16-arcanum-manual-question-types`. Read-only research; verbatim/faithful
> returns from the three explorer lanes. Synthesis lives in `findings.md`.

## Explorer A — "Ariely, Dan" (prompt-archaeology, empirical, corpus = user's actual prompts)

Typed intents, each anchored to a numbered user prompt (P1–P6):
- **T1 Compose a multi-capability pipeline** (P2: "start a craft space … then create a /dispatch-spec … input to /whisper … create a manual") → craft→dispatch-spec→whisper.
- **T2 Distill a large body of knowledge into an explainer** (P2: "distilling knowledge, explaing usage … so the user can understand") → whisper + distill; x-ray as intake.
- **T3 Inspect/expose the framework surface as base** (P2: "use /x-ray and @…/user-guide/ as base and final artifact") → x-ray.
- **T4 Execute by spawning subagents** (P3: "run scope spawning sub agents"; P4: "add a sub agents") → subagents-strategy.
- **T5 Validate/design the dispatch route before running** (P1+P2: invoked /dispatch-spec, then "create a /dispatch-spec … research strategy") → dispatch-spec.
- **T6 Build a research strategy that mines the user's own prompts** (P4: "create a research and look for my promots, so we can improve the tutorial") → research dispatch.
- **T7 Explain how to USE the tools, grounded in the user's own use** (P4: "explain how can i user use the tools based in my use, how refine helps, how you can construct dispatch specs") → refine + dispatch-spec + whisper. A *teaching* intent.
- **T8 Explain governance concepts + their rationale** (P4: "what is a constitution governances, why it matters") → constitution-governance.
- **T9 Generate more questions of this kind** (P4: "add a sub agents just to get more type of questions like this") → subagents-strategy (meta/self-amplifying).
- **T10 Retry / re-run a stalled attempt** (P5: "retry") → orchestration control.

Three highest-frequency: **T1 compose-a-pipeline** (strongest signature), **T4/T9 execute-by-subagents** (stated twice), **T7 explain-tool-use-from-my-own-usage**. Cross-cutting: the user always couples *do* + *explain*; every pipeline ends in an explainer; execution is delegated. No standalone "just run one tool" intent observed.

## Explorer B — "Simon, Herbert" (affordance-map, formal, corpus = tool contracts)

- **Tool-use-by-user-pattern:** the user's "propose → permission → execute → synthesize" pipeline habit is exactly refine's model; refine does NOT auto-execute (shows a Run Strategy Proposal first). Source: `arcanum/arcana/refine/SKILL.md`.
- **How refine helps:** runs a fixed **ten-stage** discovery/design loop (context baseline → invoke-define → interrogation review → research decision → distill → invoke-design → design review → distill-repair → invoke-plan → final synthesis); presets tune depth not stages. Reach for refine when the idea is still broad; invoke when you already have approval for durable artifacts; task-session only after a bounded SWU exists. Refine makes discovery *mandatory* before design. Source: `arcanum/arcana/refine/SKILL.md`.
- **How to construct a dispatch-spec:** required fields `dispatch_id, intent, mode, steps, gates, observability`; each step has `step_id, name, capability_ref, pattern (route|sequential|fanout|dialectic|tournament|distill|xray|decision|validation|toy_game|synthesis|handoff), inputs[], outputs[]`; parallel steps need `join_policy`; validation steps need `evidence_artifact`; techniques cited from the catalog only when used; gates (policy/quality/promotion_guardrail/validation/human_approval) prevent unsafe continuation. Source: `.claude/skills/dispatch-spec/SKILL.md` + `arcanum/formulae/dispatch-spec/dispatch.schema.yml`. Newcomer misread: dispatch-spec validates *shape*, it does not execute.
- **What constitution-governance is:** a modular, scoped ruleset governing artifact structure/form; composed narrowest-scope-first (task → artifact-type → domain → framework → repo); each rule declares a validation mode (deterministic/review/hybrid/none-yet); it is a *selector*, not a 200-rule catch-all. Source: `arcanum/arcana/constitution-governance/SKILL.md`. Why it matters: lets you validate without context bloat and promote only when rules are met.

## Explorer C — "Alexander, Christopher" (latent-demand, generative, corpus = personas + distill notes)

Latent (no current witness) question-types the user is likely to ask NEXT, by persona:
1. **"How do I see what just happened in a run I dispatched?"** (Reviewer) → signal-observer + `.arcanum/observability/` + workflow-reflect. *Most likely next ask.*
2. **"refine vs invoke vs task-session — when each?"** (Consumer) → lifecycle boundary.
3. **"How do I validate a dispatch-spec before running it?"** (Researcher) → dispatch-spec validate-mode + check-tension gates.
4. **"Tension between subagents-strategy and running inline?"** (Cross-functional/Author) → subagents-strategy P1 trigger + human gate.
5. **"When does my pipeline graduate into a reusable spell?"** (Author) → 12-stage lifecycle + evidence-gated promotion.
6. **"How do I install this setup for someone else / another repo?"** (Maintainer) → arcanum-bootstrap, sigil-runtime-installer, FRIEND-INSTALL-TUTORIAL.
7. **"Which constitution applies to THIS artifact, and how do I compose one?"** (Reviewer) → constitution-governance select/compose/validate.
8. **"How do I make a run reflect on itself and improve next time?"** (Author/Reviewer) → observe→reflect→iterate, reflection thresholds.
9. **"How do I explain a pipeline to a non-Arcanum collaborator?"** (Cross-functional) → guide-architecture + User/Translate/Guide + whisper-for-explanation.

Coverage: 6 of 7 personas; Newcomer correctly untouched (user is past it). Densest gap cluster: observe/reflect (#1, #8) — the largest afforded-but-unused surface in the user's trajectory.
