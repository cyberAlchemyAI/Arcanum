---
module: inventory-attachment-hook
runId: 20260621T162713Z-runtime-integration
stage: s3-refine-review
status: pass
updatedAt: 2026-06-21
docType: refine-review
---

# Review: Runtime Definition

## Verdict

`pass` with named implementation residue.

## Review Questions

| Question | Result |
| --- | --- |
| Does the definition make Codex the universal runtime contract? | No. Codex is a lane projection. |
| Does it include Claude Code and generic runtimes? | Yes. Both are required lanes. |
| Does it preserve chat invocation as the proof surface? | Yes. Editor UI is explicitly deferred. |
| Does it confuse Inventory candidate evidence with promotion? | No. Candidate-only authority is explicit. |
| Does it hide the direct skill observability gap? | No. The gap is named as future implementation residue. |

## Required Guardrails

1. Runtime integration must start from the shared closeout lifecycle, then map
   into hosts.
2. Direct `$skill` invocation must be designed as the first proof path.
3. Legacy `/command` support is prior evidence only, not compatibility work for
   this route.
4. Host UI behavior is a separate projection and must not enter this design as
   a hidden acceptance criterion.
5. Inventory Attachment cannot attach Inventory-created hook operation rows.

## Remaining Ambiguities

No blocker ambiguities remain for the design pass.
