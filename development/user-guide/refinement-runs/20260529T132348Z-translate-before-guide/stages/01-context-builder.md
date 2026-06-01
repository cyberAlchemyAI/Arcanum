# Stage 01: Context Builder Evidence Baseline

Status: `pass`

## Inputs

- Prior result: `development/user-guide/refinement-runs/20260529T131319Z-user-guide-ledger/RESULT.md`
- Prior manifest: `development/user-guide/refinement-runs/20260529T131319Z-user-guide-ledger/RUN-MANIFEST.md`
- New operator intent: split `Translate` out before `Guide`.

## Baseline

The prior result treated bridging as part of Guide candidates:

- `guide-bridge-selector`
- `guide-domain-bridge`
- `guide-concept-ladder`

The new intent reveals a cleaner architecture:

```text
User = durable learning/preferences ledger
Translate = vocabulary/domain/concept bridge
Guide = orchestration, walkthrough, research, subagent dispatch, explanation flow
```

## Context Finding

If Guide owns translation internals, it becomes too large. If Translate owns translation as a separate sigil, Guide can remain a higher-level spell/capability that dispatches Translate, research, x-ray, inventory, or subagents depending on the request.
