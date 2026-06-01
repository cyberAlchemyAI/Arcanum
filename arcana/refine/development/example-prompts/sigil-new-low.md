# Experiment Prompt: sigil-new-low

Run the target sigil through the sigil-development experiment profile.

## Target Artifact

arcana/refine

## Contract

arcana/refine/SKILL.md

## Lifecycle Owner

sigil-development

## User Request

Use Refine to run the refinement loop defined in `arcana/refine/REFINEMENT-LOOP.md` for a new Arcana sigil development seed for `x-ray`, then validate `REFINE-DISPATCH.json` through dispatch-spec and continue through deterministic `tools/arcanum` stage dispatch far enough to return the final refinement result or a blocked result with exact stage evidence.

`x-ray` should accept any context supplied by the user and create an HTML page with a user-driven explanation of what that context is about. The intent is to create a dynamic, structured view of a component, plan, architecture, process, or system. It should guide the user step by step so they understand what they are asking `x-ray` to analyze. The experience should be UX-driven, using constructed visual explanations or diagram-like images where useful. It should explain data flow, transformations, process steps, actors, and relationships.

Do not create the finished `x-ray` sigil. The final output for this experiment is the refinement result produced from the canonical Refine loop, not merely the proposed route.

The result must include:

- the `Refine Seed Proposal` used as the execution seed,
- a materialized target-local refinement run folder under `arcana/x-ray/development/refinement-runs/<run-id>/`,
- `Run manifest`, `Evidence index`, `Dispatch route`, `Runtime handoff`, and `Result artifact` paths,
- a `Refinement Loop Evidence` section that cites `arcana/refine/REFINEMENT-LOOP.md`,
- evidence for every selected loop stage from the refinement loop:
  - Context Builder evidence baseline,
  - Invoke Define,
  - Interrogation refine-review,
  - Research decision,
  - Distill,
  - Invoke Redefine / Design,
  - Interrogation refine-design-review,
  - Distill Repair,
  - Invoke Plan,
  - Final Interrogation and Synthesis,
- for every loop stage: command, resolved command file, mode/config, artifact path, observation envelope or invocation summary, pass/flag/block verdict, or explicit blocked reason,
- the dispatch route validation status,
- the runtime execution status,
- the final refinement output for `x-ray`,
- the research mode, preset, loop count, planned and executed stages,
- runtime eligibility,
- evidence that `tools/arcanum` remained the command dispatch surface,
- and any blocked fields if final execution could not complete.

If the run can only produce a proposal and cannot execute the refinement loop stages through the installed skills, return `Status: flag` or `Status: block` and explain which loop-stage evidence is missing. A proposal-only output is not refine experiment evidence.

When blocked, still write the run manifest and evidence index. Each selected stage must have either an existing artifact path produced by the owning skill or an explicit blocked reason.

Return the full user-facing result body. Do not summarize that you saved an output file.

## Required Capture

Save only the final artifact result body to `development/example-outputs/sigil-new-low.output.md`.
