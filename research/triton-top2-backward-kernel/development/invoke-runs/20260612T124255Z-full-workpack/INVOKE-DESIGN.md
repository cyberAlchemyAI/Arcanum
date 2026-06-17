# Invoke Design - Full Work Pack To Completion

Run id: `20260612T124255Z-full-workpack`

Status: `pass`

## Design

Use gated waves:

```text
W0 environment and dependency gate
W1 V0 reference parity with PyTorch
W2 prior-art baselines
W3 CAP2-v0 candidate design-or-kill
W4 formal math validation
W5 Triton fixed-mask baseline
W6 Triton selected relaxation
W7 zero-allocation / FP16 / performance
W8 final comparison and novelty report
```

## Gate Model

| Gate | Blocks |
| --- | --- |
| No PyTorch | W1+ autograd/gradcheck; W0 must resolve. |
| No Triton/GPU | W5-W7 only. |
| CAP2 killed | W6 uses selected prior-art relaxation or stops novelty track. |
| CAP2 undefined | W3 cannot pass. |
| V0 reference fails | All Triton implementation blocked. |
| Prior-art baselines missing | Novelty report blocked. |

## Evidence Model

Each SWU must produce:

- local result artifact;
- validation command/output;
- updated status row in `WORK-PACK.md`;
- follow-up residue if flagged.
