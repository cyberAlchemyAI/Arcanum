# Experiment Prompt: sigil-new-low

Run the target sigil through the sigil-development experiment profile.

## Target Artifact

arcana/refine

## Contract

arcana/refine/SKILL.md

## Lifecycle Owner

sigil-development

## User Request

Use Refine to prepare a new Arcana sigil development seed for `x-ray`, then continue through the approved Task Session/Codex Goal execution path far enough to return the final refinement result.

`x-ray` should accept any context supplied by the user and create an HTML page with a user-driven explanation of what that context is about. The intent is to create a dynamic, structured view of a component, plan, architecture, process, or system. It should guide the user step by step so they understand what they are asking `x-ray` to analyze. The experience should be UX-driven, using constructed visual explanations or diagram-like images where useful. It should explain data flow, transformations, process steps, actors, and relationships.

Do not create the finished `x-ray` sigil. The final output for this experiment is the refinement result produced from the proposed Task Session execution path, not merely the proposed route.

The result must include:

- the `Refine Seed Proposal` used as the execution seed,
- the Task Session/Codex Goal execution status,
- the final refinement output for `x-ray`,
- the research mode, preset, loop count, planned and executed stages,
- Codex Goal eligibility,
- evidence that Task Session remained execution owner,
- and any blocked fields if final execution could not complete.

If the run can only produce a proposal and cannot execute the proposed Task Session path, return `Status: flag` or `Status: block` and explain that the output is preflight-only and not promotion evidence.

Return the full user-facing result body. Do not summarize that you saved an output file.

## Required Capture

Save only the final artifact result body to `development/example-outputs/sigil-new-low.output.md`.
