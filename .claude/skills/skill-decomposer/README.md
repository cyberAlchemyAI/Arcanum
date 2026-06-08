# Skill Decomposer

Skill Decomposer is an Arcana sigil for extracting one reusable capability from a larger skill, prompt, workflow, command set, or mixed document.

It maps the source, identifies candidate capabilities, separates reusable behavior from local machinery, makes boundary decisions, and prepares a handoff package for [skill-transcriptor](../skill-transcriptor/) when a candidate is ready to become a sigil.

## Problem It Solves

Some sources are too broad to convert directly. They may contain several workflows, private routing rules, local assumptions, embedded validation logic, and useful fragments tangled together.

Skill Decomposer prevents over-conversion. It isolates the reusable part before authoring starts, so Arcanum gains focused sigils instead of oversized copies of source systems.

## Use When

- a source contains multiple possible sigils,
- the user points to one section inside a larger source,
- the reusable behavior is present but mixed with local mechanics,
- conversion should wait until a boundary is explicit,
- candidate capabilities need scoring before selection.

## Do Not Use When

- the source is already one coherent capability,
- the user only needs a direct package conversion,
- the fragment has too little context to judge safely,
- there is no reusable behavior beyond a local implementation detail.

Use [skill-transcriptor](../skill-transcriptor/) when the source is coherent enough for direct conversion.

## Outputs

Skill Decomposer can produce:

- source map,
- capability candidate list,
- boundary decision,
- coupling-risk review,
- decomposition report,
- handoff package for Skill Transcriptor.

## Relationship To Sigil Development

Skill Decomposer is an authoring helper, not a replacement for [sigil-development](../sigil-development/).

Use Skill Decomposer to define what should become a sigil. Use Skill Transcriptor to convert a coherent candidate. Use Sigil Development to govern lifecycle, telemetry, reflection, and later iteration.

## Why This Is Arcana

The sigil coordinates ambiguity, candidate discovery, boundary decisions, coupling risk, human gates, and handoff into conversion. It must stop safely when the reusable capability cannot be isolated.
