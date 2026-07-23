# Experiment Prompt: spellcraft-validate-complex

Run the target spell through the spellcraft experiment profile.

## Target Artifact

arcanum/spells/sigil-maintenance-loop

## Contract

arcanum/spells/sigil-maintenance-loop/README.md

## Lifecycle Owner

spellcraft

## User Request

Use Spellcraft to validate the full `sigil-maintenance-loop` contract and its
experiment pack. Check referenced sigils, required Spellcraft sections, and six
runtime boundaries: relevant `index.json` match, no match, `index.md` fallback,
no Inventory package, insufficient reflection signal, and rejected mutation
approval. Separate structural validity from live reusable-behavior evidence and
return a concrete next action in the full result body.

## Required Capture

Save only the final artifact result body to `development/example-outputs/spellcraft-validate-complex.output.md`.
