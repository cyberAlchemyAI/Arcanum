# Fixture: strategy-close-complex

## Request

Close a confirmed and registered dispatch with a dependency graph. Two parallel
explorers feed a synthesizer through sequential edges. The synthesizer and a
skeptic have one zig-zag loop; the skeptic has a non-blocking feedback edge to
the parent. One explorer failed after returning partial evidence. The parent is
the final approver.

## Inputs

- Frozen sheet: confirmed.
- Dispatch event: appended once.
- Partial explorer evidence: available.
- All agents: joined and closed.
- Parent verdict: flag because the failure limits confidence.
- Close event: appended once with a typed exit reason.
