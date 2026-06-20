# Definition Card: Unicity Distance

Status: local-research-only

## Source Meaning

Unicity distance is the approximate intercepted length at which a unique
solution emerges for a random cipher in Shannon's analysis.

Source kind: primary-source

Evidence: `tracks/paper-claim-ledger.md` C9.

## Formal Or Structural Shape

```text
approximate unicity distance = H(K) / D
```

## Notation

| Symbol | Meaning | Shared notation link |
| --- | --- | --- |
| `H(K)` | key uncertainty | n/a |
| `D` | redundancy per letter/symbol | n/a |
| `N` | intercepted length | n/a |

## Operator Reading

Ambiguity can collapse after enough evidence accumulates. More hidden
uncertainty delays collapse; more source redundancy accelerates it.

## Use Carefully

- Treat the formula as source-model-specific.
- Use the concept qualitatively unless the assumptions have been rebuilt.

## Misuse Warning

- Do not turn this into a generic countdown for any system or process.

## Promotion Boundary

analogy-only

