---
template_id: invoke.session-handoff
template_type: session-handoff
applies_to:
  - handoff
required_inputs:
  - source_session_reference
  - new_session_prompt
  - handoff_type
  - context_builder_selection
optional_inputs:
  - target_project
  - target_lifecycle_owner
  - destination_thread_label
  - constraints
output_files:
  - SESSION-HANDOFF.md
status: candidate
authority_level: invoke-local
promotion_evidence: []
promotion_decision: pending
validation_rules:
  - source session reference present
  - new session prompt present
  - handoff type selected
  - context builder coverage reported
validation_examples:
  - examples/passing.md
  - examples/missing-input.md
created_at: 2026-05-25
updated_at: 2026-05-25
---

# Session Handoff: {handoff-title}

## Identity

- Source session reference: `{source-session-reference}`
- Destination label: `{destination-thread-label-or-none}`
- Handoff type: `{workflow-reflection | new-lifecycle-thread | research-direction | execution-continuation | generic-continuation}`
- Target project or lifecycle: `{target-project-or-lifecycle}`
- Created for: `{new-session-purpose}`

## New Session Prompt

```text
{prompt-to-start-the-new-session}
```

## Route Rationale

- Recommended next route: `{route}`
- Rationale: `{why-this-route-fits}`
- Lifecycle owner: `{invoke | workflow-reflect | spellcraft | sigil-development | task-session | external-project | deferred}`

## Context Builder Selection

| Obligation | Coverage | Selected Source | Why It Matters |
| --- | --- | --- | --- |
| `{obligation-id}` | `covered | resolved | block` | `{session-ref#selector}` | `{reason}` |

Strict coverage: `{pass | flag | block}`

## Selected Session Context

- `{session-ref#selector}`
  - Obligation refs: `{ids}`
  - Context summary: `{short selected excerpt or summary}`

## Excluded Context

| Candidate | Reason Excluded |
| --- | --- |
| `{session-ref#selector}` | `{not obligation-relevant | stale | superseded | too broad}` |

## Target Boundary

- In scope for the new thread: `{scope}`
- Out of scope for the new thread: `{non-goals}`
- Prior decisions to preserve: `{decisions-or-none}`

## Gaps And Blockers

| Gap | Owner | Status | Next Action |
| --- | --- | --- | --- |
| `{gap}` | `{owner}` | `open | deferred | blocked | resolved` | `{action}` |

## Next-Session Start Prompt

```text
{copy-ready-start-prompt-with-selected-context-summary-and-route}
```

## Provenance

- Source refs: `{paths-or-session-selectors}`
- Context Builder mode: `{lean | standard | deep}`
- Evidence date: `{yyyy-mm-dd}`
- Output path: `{path}`

## Gate Result

- Status: `{pass | flag | block}`
- Reason: `{gate-result-summary}`
