# INV-HANDOFF-PASS-001

## Scenario

Create a new session/thread handoff from a referenced session.

## User Request

Create a new handoff thread to reflect on a gap I feel while using invoke: the plan handoffs feel too execution-heavy, and I want a workflow reflection that can improve invoke without losing the useful context from this session.

## Inputs

- Mode: `handoff`
- Source session reference: `.arcanum/necronomicon/sessions/demo-invoke-plan-thread/`
- New session prompt: present
- Handoff type: `workflow-reflection`
- Context Builder selection: whole referenced session scanned; selected context maps to obligations
- Target lifecycle owner: invoke development cycle, with `workflow-reflect` first

## Expected Result

- Phase status: `pass`
- Template/profile selection: session-handoff family
- Handoff type: `workflow-reflection`
- Context Builder coverage: `pass`
- Output artifact: `artifacts/invoke-plan-reflection/SESSION-HANDOFF.md`
- Expected next route: `workflow-reflect`

## Expected Output

[INV-HANDOFF-PASS-001.expected.md](INV-HANDOFF-PASS-001.expected.md)
