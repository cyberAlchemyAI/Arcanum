---
run_id: 20260607T204404Z-mars-import-absorption
status: accepted
---

# Refine Seed Proposal

## Target

Use MARS as a source of research-orchestration assets for MOGT and Arcanum.

## Problem

MOGT S0 follow-through found that Arcanum's current Experiment Harness is useful for lifecycle evidence but does not yet provide the research-project mechanics needed for MOGT dry-run fixtures: JSONL run schemas, objective-vector validation, Pareto/frontier scoring, reviewer-rubric integration, and result-summary generation.

MARS already contains project-agnostic research contracts, templates, and dry-run patterns that match much of this missing surface. The risk is importing too broadly and accidentally making MARS-specific project evidence or Copilot runtime scaffolding canonical Arcanum material.

## Refinement Question

What can MOGT use from MARS immediately, what should Arcanum absorb after proof, and what must remain MARS-owned reference material?

## Constraints

- Do not run live MOGT experiments.
- Do not mutate canonical Arcanum harness, dispatch, invoke, refine, or Whisper contracts during this mapping.
- Preserve MARS ownership boundaries: `implementation/mars` is reusable framework source; `research/projects/mars` is project execution state.
- Prefer MOGT-local imports before Arcanum-wide absorption.
