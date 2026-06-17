# Receipt 07 - Route Validation

Step id: `route-validation`

Status: `pass`

Capability: `dispatch-spec`

## Command

```bash
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py research/triton-top2-backward-kernel/top2-backward-research.dispatch.json
```

## Result

```text
VALIDATION=pass
DISPATCH=research/triton-top2-backward-kernel/top2-backward-research.dispatch.json
```

## Verdict

`pass`: the dispatch route validates after the relaxation-candidates update.
