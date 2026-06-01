# Component Catalog

Canonical component records live in [components.yml](components.yml). This Markdown file is companion prose for quick review.

## Components

| ID | Family | Lane |
| --- | --- | --- |
| `shape.node` | shape | `components` |
| `shape.boundary` | shape | `internal_dependencies`, `external_dependencies` |
| `shape.layer-panel` | shape | `visual_composition` |
| `shape.risk-marker` | shape | `risk_questions` |
| `connector.arrow` | connector | `flow`, `internal_dependencies`, `external_dependencies` |
| `connector.branch` | connector | `flow` |
| `connector.feedback-loop` | connector | `lifecycle`, `flow` |
| `chart.timeline-strip` | chart | `lifecycle` |
| `chart.risk-matrix` | chart | `risk_questions` |

Use the YAML source of truth for inputs, sketches, evidence rules, and when-not-to-use guidance.
