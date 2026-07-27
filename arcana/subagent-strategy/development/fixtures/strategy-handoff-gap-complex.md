# Fixture: strategy-handoff-gap-complex

## Request

Continue a confirmed and registered dispatch whose producer group has returned
its required artifact. The downstream consumer depends on that artifact through
a sequential edge. The dispatch type owner requires two source-local selectors
in the handoff, but both are unresolved placeholders.

The frozen sheet already declares a producer feedback edge with one loop
remaining. A separate consumer-to-auditor revision is reserved for improving
the completed consumer output.

## Inputs

- Producer artifact: exists, with two unresolved selector placeholders.
- Type-owner handoff verdict: blocked with two typed evidence gaps.
- Producer feedback edge: declared with one loop remaining.
- Consumer group: not started.
- Auditor revision capacity: unused.
- Final approver: receives the gap if producer feedback cannot repair it.
