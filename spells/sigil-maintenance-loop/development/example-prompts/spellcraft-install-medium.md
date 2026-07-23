# Experiment Prompt: spellcraft-install-medium

Run the target spell through the spellcraft experiment profile.

## Target Artifact

arcanum/spells/sigil-maintenance-loop

## Contract

arcanum/spells/sigil-maintenance-loop/README.md

## Lifecycle Owner

spellcraft

## User Request

Use Spellcraft to assess a local adaptation of `sigil-maintenance-loop` in two
repository states: no Inventory package, and an Inventory with `index.md` but no
parseable `index.json`. The result must attempt lookup automatically, continue
with explicit residue, and must not ask to install, query, ingest, backfill, or
sync Inventory. Preserve the canonical public spell and return the full
Spellcraft result body.

## Required Capture

Save only the final artifact result body to `development/example-outputs/spellcraft-install-medium.output.md`.
