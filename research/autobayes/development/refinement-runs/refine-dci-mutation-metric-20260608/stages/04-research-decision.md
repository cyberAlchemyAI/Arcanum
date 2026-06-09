---
stage: 4
name: Research Decision
capability: refine
mode: research-if-gap-appears
decision: no-research
status: pass
dispatch_id: refine-dci-mutation-metric-20260608
---

# Research Decision

**Decision: no-research.** The differential and its power analysis are standard two-proportion
change-detection on local telemetry; the methods (two-proportion z-test / Fisher exact, power for
proportions) are well-known and need no external pass. The `observer_version` lever was found
locally. If the power-analysis reviewer finds a settled rare-event sequential-change-detection
method is genuinely needed, that re-triggers this decision with operator confirmation.
