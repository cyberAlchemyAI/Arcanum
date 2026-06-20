# Definition Card: Perfect Secrecy

Status: local-research-only

## Source Meaning

Observing a cryptogram does not change the probabilities assigned to the
possible messages.

Source kind: primary-source

Evidence: `tracks/paper-claim-ledger.md` C6-C7.

## Formal Or Structural Shape

```text
For every cryptogram E and message M:
P_E(M) = P(M)

Equivalent condition in the paper:
P_M(E) = P(E)
```

## Notation

| Symbol | Meaning | Shared notation link |
| --- | --- | --- |
| `M` | message | n/a |
| `E` | cryptogram | n/a |
| `P(M)` | prior message probability | n/a |
| `P_E(M)` | posterior message probability after observing E | n/a |
| `P_M(E)` | probability of E given M | n/a |

## Operator Reading

A visible artifact can exist without teaching the observer anything new about
the protected state, but only under strict conditions.

## Use Carefully

- Use only when prior and posterior are explicitly modeled.
- Keep the key-supply requirement visible.

## Misuse Warning

- Do not use this phrase to mean "very private," "encrypted," "secure enough,"
  or "hard to attack."

## Promotion Boundary

blocked

