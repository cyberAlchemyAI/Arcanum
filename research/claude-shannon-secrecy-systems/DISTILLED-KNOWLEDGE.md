# Distilled Knowledge

Status: pass

Promotion scope: local-research-only

## One-Sentence Model

Secrecy is the managed gap between what an interceptor can observe and what
they can infer, formalized through prior probabilities, key-selected
transformations, posterior probabilities, and remaining uncertainty.

## Compositional Spine

```text
message source -> message M
key source -> key K -> transformation T_i
T_i(M) -> cryptogram E
interceptor sees E -> posterior over M and K
secrecy measure -> how much uncertainty remains
```

## What To Borrow Carefully

- Model the observer explicitly: what do they know before seeing the artifact?
- Treat visible artifacts as posterior-update triggers, not as neutral objects.
- Separate theoretical secrecy from practical labor or cost.
- Ask whether redundancy in a source is leaking structure.
- Use key uncertainty as a limited resource, not a magic label.

## What To Keep Analogy-Only

- `unicity distance` as a threshold metaphor for ambiguity collapse.
- `confusion` and `diffusion` as governance/design metaphors.
- `perfect secrecy` as an ideal of non-updating observation outside formal
  cryptography.

## What To Block

- Promoting Shannon terms into canonical Arcanum vocabulary without a separate
  decision.
- Using the paper to claim modern protocol security.
- Treating "the enemy knows the system" as a complete threat model.
- Applying `H(K) / D` to arbitrary systems.

## Operator Model

The useful local move is not "encrypt things like Shannon." It is:

```text
Name the hidden state.
Name the observer.
Name what the observer sees.
Name the prior.
Name how the visible artifact changes the posterior.
Then decide whether uncertainty was preserved, collapsed, or merely made costly
to collapse.
```

