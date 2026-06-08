# Skill Transcriptor

Skill Transcriptor is an Arcana sigil for converting a complete, coherent skill, prompt, command, or workflow into an Arcanum-compliant sigil package.

It preserves reusable behavior while translating the source into Arcanum's tier model, folder structure, quality bar, anti-patterns, output contract, observability guidance, and registry expectations.

## Problem It Solves

Useful skills often exist outside Arcanum in a shape that cannot be reused directly. They may have different frontmatter, private vocabulary, implicit gates, local tool assumptions, or missing validation.

Skill Transcriptor converts those sources into sigils without importing the source environment as-is. It checks whether the source is one coherent capability, classifies the target tier, rewrites language neutrally, drafts the package plan, and defines validation before registration.

## Use When

- an existing skill or workflow is already one coherent reusable capability,
- a prompt or command should become a formal Arcanum sigil,
- a draft sigil needs package normalization,
- the source behavior is clear but the Arcanum tier, folder, and registry contract are not yet defined.

## Do Not Use When

- the source contains several separable capabilities,
- the user only points to one fragment inside a larger workflow,
- the reusable behavior is not yet clear,
- source vocabulary or routing mechanics are too tangled to convert safely.

Use [skill-decomposer](../skill-decomposer/) first when the source boundary is unclear.

## Outputs

Skill Transcriptor can produce:

- conversion assessment,
- tier classification,
- sigil package plan,
- neutral vocabulary check,
- draft `README.md` and `SKILL.md` guidance,
- template recommendations,
- registry update plan,
- conversion report.

## Relationship To Sigil Development

Skill Transcriptor is an authoring helper, not a replacement for [sigil-development](../sigil-development/).

Use Skill Transcriptor to convert a coherent source into a package. Use Sigil Development to govern lifecycle, observability, reflection, and later iteration.

## Why This Is Arcana

The sigil coordinates source analysis, tier judgment, neutral rewriting, package planning, conversion gating, validation, and observability. It must stop safely when the source is not coherent enough for direct conversion.
