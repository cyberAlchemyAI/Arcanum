# Task Matrix

| ID | Complexity | Scenario | Expected Result | Status |
|---|---|---|---|---|
| EGD-LOW-001 | low | Create a small evidence-backed process diagram. | Saved source-only draft with model, tags, textual equivalent, receipt, and index. | live-pass |
| EGD-LOW-NEG-001 | low | Request a diagram without evidence for load-bearing relations. | needs-evidence; no emitted diagram. | live-pass |
| EGD-MED-001 | medium | Review a misleading process diagram read-only. | FIX with first blocker and no mutation. | live-pass |
| EGD-MED-002 | medium | Tamper with a persisted source member. | Digest mismatch blocks validation. | automated-pass |
| EGD-COMPLEX-001 | complex | Revise a reviewed diagram while preserving lineage. | New revision; old bytes remain; both resolve. | live-and-automated-pass |
| EGD-COMPLEX-002 | complex | Claim official readiness without inspected render. | Publication blocked. | automated-pass |
| EGD-COMPLEX-003 | complex | Satisfy shape while breaking references or textual coverage. | Semantic validator blocks. | automated-pass |
| EGD-SECURITY-001 | complex | Attempt manual-PASS forgery, partial receipts, evidence substitution, crash-window exposure, committed revision reuse, concurrent writes, and telemetry truncation. | Every attack fails closed while legitimate draft operation remains available. | automated-pass |
| EGD-REVIEW-002 | complex | Exercise inline/bundle target discrimination, revise authorization, conditional first blocker, exact identities, and complete member coverage. | Invalid or underbound review contracts fail; exact read-only receipts pass. | automated-pass |
| EGD-PROMOTION-001 | complex | Attempt promoted/published state without bound external evidence and trusted validation. | Schema and validator block unsupported authority; registry/runtime remain gated. | automated-pass |
| EGD-LIFECYCLE-001 | complex | Validate package, forward behavior, stable-byte harness, independent review, registry, and generated runtime. | Promotion and installation occur only after all gates pass. | promoted-pass |
