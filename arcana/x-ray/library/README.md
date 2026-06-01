# x-ray Visual Library

This library is a starter catalog for composing `x-ray` HTML/SVG explanations. The canonical reusable records are YAML files; the Markdown files are human-readable companion docs.

It is not a renderer engine or design system. A valid `x-ray` can use plain semantic HTML and inline SVG while borrowing these components and patterns.

## Families

| Family | Use |
| --- | --- |
| Shapes | Bounded visual objects such as a node, boundary, layer panel, or risk marker. |
| Connectors | Relationships such as an arrow, branch, or feedback loop. |
| Charts | Compact summaries such as a timeline strip or risk matrix. |
| Patterns | Reusable compositions such as process branch, dependency boundary, lifecycle stack, or evidence/inference split. |

## Baseline Rule

Every visual element should answer three questions:

1. Which `x-ray` lane does this serve?
2. What source evidence or explicit inference does it represent?
3. What would become misleading if this visual were drawn differently?

If those answers are unclear, prefer text or a simpler visual.

## User Extension Nudge

Add your own shape, chart, or pattern when the target has a domain-specific form that the starter library cannot represent honestly. Custom additions should follow [user-shapes-template.md](user-shapes-template.md) and preserve the evidence/inference boundary.

## Source Of Truth

- [components.yml](components.yml): canonical starter shapes, connectors, and tiny charts.
- [patterns.yml](patterns.yml): canonical starter visual composition patterns.
- [user-shapes-template.yml](user-shapes-template.yml): canonical template for user-proposed shapes, charts, and patterns.

Each YAML record declares the lane it serves and the evidence/inference rule it carries. Markdown companions may explain the catalog, but YAML is the source of truth for validation and future renderers.

## Companion Docs

- [components.md](components.md): readable summary of `components.yml`.
- [patterns.md](patterns.md): readable summary of `patterns.yml`.
- [user-shapes-template.md](user-shapes-template.md): readable guide for `user-shapes-template.yml`.
