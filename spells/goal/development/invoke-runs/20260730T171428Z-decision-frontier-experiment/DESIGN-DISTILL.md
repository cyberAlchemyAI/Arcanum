# Design Distill

## Smallest Coherent Architecture

The core is one pure pipeline:

```text
versioned map -> validate -> derive reasons/frontier -> canonical receipt
```

Claims and reconciliation are later layers because they add state transition
and concurrency semantics. HITL, Way Clear, and execution non-collapse are
separate acceptance boundaries. Cross-capability adapters are deferred because
current contracts do not carry the candidate shape.

## Removed Alternatives

| Alternative | Disposition |
| --- | --- |
| new canonical fourth capability | rejected until fixture and workflow evidence exists |
| issue tracker as source authority | rejected; conflicts with Craft ownership |
| direct Goal runtime modification | deferred; fixture host first |
| cross-capability adapter implementation | deferred; current contracts lack the candidate shape |
| unified decision/task node | rejected; destroys execution boundary |
| daemon or network lock service | deferred; unjustified by fixture scope |
| automatic HITL fallback | rejected; violates human route |

## Residue

- expiry and crash recovery remain unresolved beyond single-process fixtures;
- a later Design refresh must decide how accepted claims and fog are
  represented canonically;
- real workflow benefit needs paired evidence after behavior exists.

## Verdict

The architecture is coherent only as a development experiment. Its essential
extensions are persistence/concurrency, integration/versioning, state/event
semantics, and validation contracts.
