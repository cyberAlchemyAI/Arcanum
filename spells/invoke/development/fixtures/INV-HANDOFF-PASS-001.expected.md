## Invoke Validation Fixture Result

- Fixture: INV-HANDOFF-PASS-001
- User request: Create a new handoff thread to reflect on a gap I feel while using invoke: the plan handoffs feel too execution-heavy, and I want a workflow reflection that can improve invoke without losing the useful context from this session.
- Mode: handoff
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: arcanum/spells/invoke/handoff.md
- Outputs: artifacts/invoke-plan-reflection/SESSION-HANDOFF.md, artifacts/invoke-plan-reflection/context-builder-pack.md
- Handoff type: workflow-reflection
- Source session: .arcanum/necronomicon/sessions/demo-invoke-plan-thread/
- Context Builder coverage: pass
- Template/profile selection: session-handoff family
- Decisions: preserve the user's felt gap as reflection evidence; select only session context tied to invoke plan handoff heaviness; exclude unrelated implementation details
- Unresolved gaps: workflow-reflect must decide whether the gap belongs to invoke templates, plan contract gates, or downstream task-session expectations
- Next-session prompt: Reflect on invoke plan handoffs feeling too execution-heavy using the selected session evidence and propose improvements without mutating invoke directly.
- Next route: workflow-reflect
