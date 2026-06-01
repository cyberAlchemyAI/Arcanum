# Fixture: Architecture Boundary Guide

## Input

```text
/guide this architecture decision: keep the workflow engine isolated from direct database writes. The engine emits commands through an interface; repositories own persistence.
```

User handles:

- `UDA-SALES-001`
- `UVP-CONCRETE-FIRST-001`
- `UCS-SCHEMA-001`

## Expected Route

| Phase | Expected Output |
| --- | --- |
| Frame | The decision protects workflow policy from persistence details. |
| Inspect | Boundary: workflow engine vs repositories; dependency: engine depends on interface; failure: direct writes bypass validation. |
| Translate | Sales qualification analogy may be used, with machine-enforcement limit preserved. |
| Explain | Concrete frame, target definition, mapping limit, system abstraction. |
| Validate | Ask user what should not cross the boundary. |
| Receipt | Propose clarified architecture-boundary concept state only after user response. |

## Expected Guide Output Summary

The workflow engine is like a sales stage that should not directly close a deal without qualification rules. The useful part of the analogy is that the next stage is protected by a gate. The limit is that software boundaries are enforced by interfaces and code behavior, not by negotiation.

Target-domain definition:

An architecture boundary is a designed separation between system parts, with explicit contracts for allowed dependencies, data, behavior, and failure handling.

Active evidence prompt:

In your own words, explain what the workflow engine should not do directly and why the repository interface exists.

## Expected Verdict

`pass`

## Validation Notes

- Translate is called by contract, not inlined as a sigil definition.
- User-ledger update is a proposal.
- No live research or subagent dispatch is needed.
