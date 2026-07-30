# Implementation Plan

The canonical executable plan is [WORK-PACK.md](WORK-PACK.md). Layer governance is
owned by [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md), cross-task order
by [EXECUTION-PACK.md](EXECUTION-PACK.md), and exact Task Session closeout controls
by [work-pack/shared/EXECUTION-CONTROL.md](work-pack/shared/EXECUTION-CONTROL.md).

The plan deliberately separates the pure evaluator, runner contracts, state machine,
reconciliation/application, owner hooks, and operations. A single “do everything”
script would be shorter to describe but would duplicate authority and be difficult
to validate or resume safely.

