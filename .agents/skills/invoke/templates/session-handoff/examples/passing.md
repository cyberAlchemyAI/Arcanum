# Passing Example: Workflow Reflection Handoff

## Input

- Source session reference: `.arcanum/necronomicon/sessions/20260525-invoke-thread/`
- New session prompt: "Reflect on why invoke plan handoffs keep feeling too execution-heavy and propose improvements."
- Handoff type: `workflow-reflection`
- User-stated gap: "The handoff feels like it drags too much implementation detail into reflection."
- Context Builder selection: pass

## Expected Output

- Phase status: `pass`
- Handoff type: `workflow-reflection`
- Context Builder coverage: `pass`
- Selected context includes the user's felt gap, the current invoke plan contract, and prior handoff examples.
- Excluded context records unrelated implementation details.
- Next route: `workflow-reflect`
