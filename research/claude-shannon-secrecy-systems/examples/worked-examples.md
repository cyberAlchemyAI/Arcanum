# Worked Examples

Status: pass

## Example 1: Prior And Posterior

Source kind: operator-reading

Suppose an observer thinks three messages are possible before seeing a
cryptogram:

```text
P(M1) = 1/2
P(M2) = 1/4
P(M3) = 1/4
```

In a perfectly secret system, after the observer sees the cryptogram, the
message probabilities stay the same:

```text
P_E(M1) = 1/2
P_E(M2) = 1/4
P_E(M3) = 1/4
```

Local lesson: the artifact was visible, but it did not update the observer's
belief about which message was sent.

## Example 2: Redundancy And Unicity Distance

Source kind: local-inference

Shannon's random-cipher approximation says the unicity distance is roughly
key uncertainty divided by language redundancy.

```text
larger H(K) -> more intercepted material needed
larger D -> less intercepted material needed
```

Local lesson: if a source is highly structured, observations carry leverage.
If the key uncertainty is small, that leverage catches up sooner.

## Example 3: Confusion Versus Diffusion

Source kind: operator-reading

Diffusion asks: if the source leaks structure, can the system spread that
structure so small observations are less useful?

Confusion asks: if the observer can compute statistics, can the system make the
path from those statistics back to key coordinates difficult to use?

Local lesson: both concepts require an observer model. Without one, they
become empty complexity words.

