# Refine Strategy Result: HTML Guide And Whisper-Core Fixture

Status: pass with command-surface caveat.

## Summary

The guide residue became two linked artifacts:

1. A non-technical HTML guide that makes the Arcanum development loop approachable and visual: `development/user-guide/arcanum-development-loop.html`.
2. A complete Whisper-based fixture that demonstrates one idea-to-MVP run from raw intent through cores, candidates, gates, parts, work-pack, task-session evidence, validators, and residue: `development/user-guide/fixtures/whisper-idea-to-mvp/`.

The central design insight is to reuse Whisper's core model as a general idea-exploration grammar:

- `resonance_core` becomes idea promise: the felt value, trust, energy, or meaning the tool should create.
- `relevance_core` becomes audience and domain fit: who it is for, why it matters now, and what objections or constraints shape it.
- `trajectory_core` becomes transformation path: how the user moves from first prompt to validated MVP evidence.

## Selected Route

Executed the `parallel spine` route:

- Define a shared core model first.
- Use that model to design the HTML guide.
- Use the same model to build the Whisper fixture.
- Let the HTML guide teach from the fixture rather than merely describing abstractions.

## Why Whisper Is The Right Example

The Whisper run is useful because it already shows the whole pattern in miniature:

- raw creative intent becomes a substrate,
- the substrate is decomposed into cores,
- candidate routes are compared across resonance, relevance, and trajectory,
- hard gates prevent attractive but unsafe candidates from winning,
- `composition_parts` turn the selected candidate into local responsibilities,
- validators turn important rules into executable checks,
- task-session receipts show bounded execution and evidence,
- residue names what remains unresolved.

This is exactly what the Arcanum development guide wants users to understand: ambitious ideas can be explored as living structures, not flattened into one prompt or one task list.

## Outputs

- `development/user-guide/arcanum-development-loop.html`
- `development/user-guide/fixtures/whisper-idea-to-mvp/README.md`
- `development/user-guide/fixtures/whisper-idea-to-mvp/idea-substrate.yml`
- `development/user-guide/fixtures/whisper-idea-to-mvp/candidate-routes.yml`
- `development/user-guide/fixtures/whisper-idea-to-mvp/composition-parts.yml`
- `development/user-guide/fixtures/whisper-idea-to-mvp/toy-nonwriting-probe.yml`
- `development/user-guide/fixtures/whisper-idea-to-mvp/validate-fixture.py`
- `development/user-guide/fixtures/whisper-idea-to-mvp/WORK-PACK.md`
- `development/user-guide/fixtures/whisper-idea-to-mvp/EVIDENCE-LEDGER.md`
- `development/user-guide/fixtures/whisper-idea-to-mvp/PLAYBOOK.md`

## Validation

- Dispatch validation: pass.
- HTML parser validation: pass.
- Fixture YAML parse: pass.
- Fixture negative probe: pass.
- Whisper draft validation: pass.

## Caveat

This is complete local task-session evidence. It is not full adapter-backed Refine promotion evidence because several stage owner commands do not resolve through the local `tools/arcanum` command surface.
