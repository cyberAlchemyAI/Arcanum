# Stage 08: Distill Repair

Status: `pass`

## Repairs

- Add mapping limits as required Translate output.
- Add target-domain definition as required Translate output.
- Keep User ledger writes outside Translate.
- Keep Guide subagent/research dispatch outside Translate.
- Defer `/guide this architecture` full route until Translate contract exists.

## Repaired Ordering

```text
1. User ledger contract
2. Translate sigil candidate
3. Translate fixtures
4. Guide orchestration design
5. Guide spell candidates
```

## Why User Still Comes First

Translate needs vocabulary preferences and known domain anchors. Those come from User. But User does not need to be fully implemented before Translate can be designed; Translate can use fixture handles.

So the practical route is:

```text
define minimal User fixture handles
  -> develop Translate contract
  -> validate translation fixtures
  -> design Guide orchestration around Translate
```
