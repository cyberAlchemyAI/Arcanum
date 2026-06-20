# Definition Card: Equivocation

Status: local-research-only

## Source Meaning

Equivocation is conditional uncertainty about the transmitted message or key
after the cryptogram is known.

Source kind: primary-source

Evidence: `tracks/paper-claim-ledger.md` C8.

## Formal Or Structural Shape

```text
H_E(M): uncertainty about message M after observing cryptogram E
H_E(K): uncertainty about key K after observing cryptogram E
```

## Notation

| Symbol | Meaning | Shared notation link |
| --- | --- | --- |
| `H_E(M)` | message equivocation | n/a |
| `H_E(K)` | key equivocation | n/a |
| `N` | amount of intercepted material | n/a |

## Operator Reading

Equivocation is residue after evidence. The useful question is not "is there
uncertainty?" but "how much uncertainty remains after this observation?"

## Use Carefully

- Name the evidence event.
- Name the candidate set.
- Distinguish message equivocation from key equivocation.

## Misuse Warning

- Do not use it as a decorative synonym for ambiguity or vagueness.

## Promotion Boundary

promotion-candidate

