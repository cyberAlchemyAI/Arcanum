# Experiment Prompt: XRAY-BLOCK-001

Use `x-ray` with the smallest safe mode.

Target context:

```text
Explain the system. It has some services and maybe a queue. The important part is hidden.
```

Expected evidence:

- result should be `block` or `flag`
- no invented component graph
- asks for missing target boundary, source context, and user intent
- explains why the target is too broad or underspecified
