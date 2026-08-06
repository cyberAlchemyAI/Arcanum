# Execution Pack

## Choreography

```text
Wave 0: contract
  SWU-001
     |
Wave 1: plan projection
  SWU-002
     |
Wave 2: owner routing
  SWU-003 -> SWU-004
     |
Wave 3: execution entry
  SWU-005 -> SWU-006
     |
Wave 4: proof and packaging
  SWU-007 -> SWU-008
```

The route is serial because each later layer consumes the exact contract and
receipt from the earlier layer. Independent fixture implementation inside an
SWU may be parallelized only if write scopes do not overlap and a validated
dispatch is explicitly authorized at that later time.

## Wave gates

| Wave | Entry evidence | Exit gate |
| --- | --- | --- |
| 0 | approved Work Pack and selected SWU-001 | schemas and negative fixtures pass |
| 1 | L0 receipt | Plan cannot emit a contradictory entry state/next route |
| 2 | Plan projection receipt | bound route runs without per-hop authorization; outer loop joins it |
| 3 | routing receipts | fast guard and fresh-session resumption pass |
| 4 | L0-L2 receipts | end-to-end and stop-class fixtures pass; generated parity passes |

## Owner routing

- Spellcraft owns changes to `implementation-readiness`, Invoke, Work Pack
  Readiness Audit, and Task Session Until Blocker spell contracts.
- Sigil Development owns Continuation Router and Task Session lifecycle changes.
- Task Session executes one selected implementation SWU at a time after the
  relevant lifecycle owner admits it.
- Dispatch Spec validates the cross-capability execution route.

## No per-hop authorization rule

Once the user starts the selected Work Pack, calls to these lifecycle owners,
validators, local tools, and bounded Task Sessions are route mechanics. The
outer loop does not interrupt for another authorization unless a stop class is
encountered.

