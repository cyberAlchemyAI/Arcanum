# INV-HANDOFF-BLOCK-001

## Scenario

Request a new session/thread handoff without a source session reference.

## User Request

Open a new research thread for the cross-project direction we just discussed.

## Inputs

- Mode: `handoff`
- Source session reference: missing
- New session prompt: present
- Handoff type: `research-direction`
- Context Builder selection: cannot run without source session reference

## Expected Result

- Phase status: `block`
- Missing input: source session reference
- Context Builder coverage: `block`
- Expected next route: deferred

## Expected Output

[INV-HANDOFF-BLOCK-001.expected.md](INV-HANDOFF-BLOCK-001.expected.md)
