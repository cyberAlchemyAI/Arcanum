# Stage 09: Invoke Plan

Status: pass.

## Executed Plan

| Unit | Output | Validation |
| --- | --- | --- |
| U1 HTML guide | `development/user-guide/arcanum-development-loop.html` | HTML parser check. |
| U2 fixture substrate | `idea-substrate.yml` | YAML parse and fixture validator. |
| U3 candidate routes | `candidate-routes.yml` | YAML parse and selected/rejected candidate checks. |
| U4 composition parts | `composition-parts.yml` | YAML parse and part responsibility checks. |
| U5 toy probe | `toy-nonwriting-probe.yml`, `validate-fixture.py` | Missing-core negative probe. |
| U6 evidence sync | run manifest, runtime handoff, evidence index, task-session report | JSON parse and dispatch validation. |

## Follow-Up Plan

1. Browser-review the HTML guide through localhost when a Playwright/browser runtime is available.
2. Optionally add a small interactive form for filling idea resonance, relevance, and trajectory.
3. Route any external UX/cognition claims through a separate `dispatch-spec` research route.
