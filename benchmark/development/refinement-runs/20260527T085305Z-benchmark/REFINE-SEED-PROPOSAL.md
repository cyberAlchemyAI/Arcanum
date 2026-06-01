# Refine Seed Proposal

## Target

`benchmark`

## Source Request

target=benchmark; preset=standard; research=research-if-gap-appears; refine the idea of using refine/distill/invoke to validate our tool against the completed benchmark smoke tests; do not mutate benchmark source or recompute benchmark scores

## Runtime Configuration

- Preset: `standard`
- Research: `research-if-gap-appears`

## Validation Surface

- command resolution through `tools/arcanum --resolve`
- command-backed stage output artifacts under `stages/`
- final `RUN-MANIFEST.md`, `evidence-index.json`, and `RESULT.md`
