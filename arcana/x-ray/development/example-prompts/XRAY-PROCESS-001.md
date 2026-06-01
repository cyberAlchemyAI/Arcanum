# Experiment Prompt: XRAY-PROCESS-001

Use `x-ray` in `process` mode.

Target context:

```text
Refund approval process:

A customer support agent receives a refund request. The agent checks whether the order is within the refund window, whether the item was delivered, and whether the customer has prior refund abuse flags. If the request passes policy checks, the agent sends it to the payments queue. If the request fails policy checks, the agent sends a denial explanation to the customer. If evidence is unclear, the agent escalates to a supervisor. Supervisors review escalations daily and may update policy notes.
```

Expected evidence:

- mode: `process`
- actors, steps, decisions, branches, transformations, and handoffs
- internal and external dependencies
- `pattern.process-branch` or similar library pattern where appropriate
- L0 HTML/SVG output or a complete HTML page model
