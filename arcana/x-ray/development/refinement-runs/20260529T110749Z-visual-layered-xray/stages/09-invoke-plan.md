# Stage 09: Invoke Plan

## Status

pass

## Non-Executed Implementation Plan

### SWU-XRAY-VISUAL-001: Contract Update

Update `arcana/x-ray/SKILL.md` and `README.md` to define:

- modes,
- canonical lanes,
- lane output handles,
- renderer ladder,
- HTML page model,
- evidence/inference boundary,
- anti-patterns for decorative-only visuals and premature 3D.

### SWU-XRAY-VISUAL-002: Example Artifact

Add one example x-ray package:

- source target: a small architecture or artifact description,
- generated lane model JSON or Markdown,
- static HTML output with inline SVG layer stack.

### SWU-XRAY-VISUAL-003: Validation Harness

Add validation checks for:

- required lane ids,
- each lane having evidence or an explicit inference marker,
- HTML parse success,
- presence of layer controls,
- internal and external dependency sections,
- no required network dependency for L0.

### SWU-XRAY-VISUAL-004: Visual Adapter Backlog

Create deferred notes for:

- Mermaid conservative templates,
- Mermaid architecture-beta guarded use,
- CSS 3D layer stack,
- optional Three.js layer toggles,
- optional Kroki SVG export when policy permits.

## Recommended Route

`/sigil-development arcana/x-ray --mode revise --from arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/RESULT.md`

Then use Task Session for SWU execution after the sigil-development review approves the revision.

