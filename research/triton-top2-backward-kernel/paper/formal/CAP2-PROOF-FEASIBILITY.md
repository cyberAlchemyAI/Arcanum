# CAP2 Fixed-Load Derivative Feasibility Report

Status: `scoped-deferred`

## Target

The planned theorem was one narrow CAP2 fixed-load derivative piece, such as a
fixed-load penalty component or normalized membership factor.

## Feasibility Result

This proof should not be added as a theorem in the current task session. The
current formal package can state CAP2 boundary classifications and router
linear-map identities, but it does not yet contain a canonical formal
definition of the CAP2 relaxation itself.

The missing formal choices are:

- the exact CAP2-v0 mathematical definition to freeze as canonical;
- whether loads are represented as fixed data, normalized probabilities, or
  differentiable functions of logits;
- which scalar penalty term corresponds to the implementation and paper text;
- how to connect a local derivative piece to the already proved fixed-mask and
  router-adjoint identities without implying global routing optimality;
- how to avoid suggesting a novelty proof.

## Exact Blocker

The blocker is definition selection, not proof tooling. A derivative theorem
for CAP2 should not be written until the paper package selects a canonical
formal CAP2 definition with the same contract as the implementation evidence.

## Next Smallest Theorem

The next safe theorem should formalize one scalar fixed-load penalty component
after the CAP2 definition is frozen:

```text
fixedLoadPenalty load assignment
```

with load treated as fixed data, then prove the derivative contribution with
respect to router logits is absent unless the selected CAP2 definition makes
load differentiable.

## Claim Boundary

This report is feasibility evidence only. It does not prove CAP2 calculus,
CAP2 novelty, global routing optimality, or gradients through dynamic
load-balancing decisions.
