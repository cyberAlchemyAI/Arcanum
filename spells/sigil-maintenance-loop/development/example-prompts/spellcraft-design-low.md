# Experiment Prompt: spellcraft-design-low

Run the target spell through the spellcraft experiment profile.

## Target Artifact

arcanum/spells/sigil-maintenance-loop

## Contract

arcanum/spells/sigil-maintenance-loop/README.md

## Lifecycle Owner

spellcraft

## User Request

Use Spellcraft to review the existing `sigil-maintenance-loop` after a user asks
for automatic Inventory exploration on every maintenance run. Decide whether to
create a new spell or revise the canonical one. Require read-only `inventory
lookup` before reflection, machine-index-first behavior, a named lookup packet,
and no extra user prompt for lookup. Preserve explicit approval before mutation.
Return the full Spellcraft result body; do not merely report that a file was
saved.

## Required Capture

Save only the final artifact result body to `development/example-outputs/spellcraft-design-low.output.md`.
