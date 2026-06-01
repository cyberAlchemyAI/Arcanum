# Stage 05: Distill

## Status

pass

## coherent-unit

`unit:lane-model-plus-layered-html-renderer`

## Selected Unit

The smallest coherent `x-ray` capability is:

> A dispatch-spec lane model that extracts multiple visions of a target and renders them as selectable layers in a local HTML explanation page.

## Rejected Expansions

- Full 3D engine as baseline: too expensive and not necessary for explanation quality.
- Generic diagramming workbench: loses the sigil's purpose.
- Code analysis engine as baseline: codebase mode can begin with file/module evidence and deepen later.
- Live web diagram API dependency: inappropriate for private local artifacts as the default path.

## Minimum Component Catalog

- target resolver,
- mode selector,
- evidence and inference ledger,
- lane dispatcher,
- lane handles,
- renderer model,
- static HTML/SVG template,
- optional Mermaid adapter,
- validation checks,
- observability signal.

