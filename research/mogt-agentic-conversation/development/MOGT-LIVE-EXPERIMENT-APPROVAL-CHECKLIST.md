---
name: MOGT Live Experiment Approval Checklist
description: Approval checklist for moving from dry-run rehearsal to claim-bearing MOGT experiment execution.
created: 2026-06-08
status: repair-needed
approval_verdict: not_approved
last_approval_gate: MOGT-LIVE-EVIDENCE-APPROVAL
---

# MOGT Live Experiment Approval Checklist

## Verdict

Current verdict: REPAIR-NEEDED.

Live experiments are not approved yet.

Latest approval-gate result: `MOGT-LIVE-EVIDENCE-APPROVAL` confirmed that
approval can be decided from local evidence and remains `repair-needed`.

## Approval Gates

| Gate | Requirement | Current Evidence | Decision |
| --- | --- | --- | --- |
| G1 protocol measurability | Each E1-E4 protocol has measurable criteria, definitions, context, and schema mapping. | Protocols exist but hard gates remain pending. | repair-needed |
| G2 source validation | Required sources are validated, pinned, and publication-safe. | Several novelty/source-normalization gaps remain. | research-gap |
| G3 inventory/readiness | Required inventory and reviewer artifacts are ready. | Reviewer rubric is finalized as scoring gate; E3 coverage incomplete. | repair-needed |
| G4 data integrity | Data integrity path exists for real runs. | Fixture validation exists; no live/raw run integrity report. | repair-needed |
| Reviewer rubric | Score anchors, blinding, calibration, agreement, and adjudication are approved. | Rubric is finalized as scoring gate; calibration still required. | repair-needed |
| Live execution authorization | Models, scenario counts, sampling, cost, and operator limits are approved. | Required parameter categories are listed, but concrete values are not specified. | repair-needed |
| Evidence mutation policy | Claim-impact update process is approved. | Evidence status remains insufficient; mutation policy not approved. | repair-needed |

## Experiment-Specific Approval

| Experiment | Current State | Live Approval Decision | Required Repair |
| --- | --- | --- | --- |
| E1 | Protocol draft; fixture summary exists. | not approved | Close G1-G3, calibrate traceability/acceptance rubric. |
| E2 | Protocol draft; fixture summary and Pareto metrics exist. | not approved | Close G1-G3, normalize/source-check Pareto and weighted-sum authorities. |
| E3 | Protocol draft; no dedicated fixture summary. | second-wave by default | Create E3 dry-run package or explicitly approve first-wave inclusion; normalize negotiation/game-theory authorities. |
| E4 | Protocol draft; fixture summary exists. | not approved | Close G1-G3, calibrate overhead and reviewer-burden thresholds. |

## Required Live-Run Parameters

Before approval, define:

- model IDs and versions;
- model temperature;
- scenario set and count per experiment;
- policy regimes to compare;
- reviewer count: at least two independent reviewers per scored run;
- blinding method;
- scoring rubric version: `MOGT-REVIEWER-RUBRIC-DRAFT.md` finalized scoring gate;
- calibration set: 3-5 examples scored by all reviewers before production;
- data output paths;
- max token/cost budget;
- latency and overhead stop conditions;
- evidence-status mutation owner;
- paper rewrite owner.

## Stop Conditions

Live execution must stop or block if:

- model/tool access is unavailable or unapproved;
- reviewer rubric is not calibrated with 3-5 examples;
- protocol gates remain pending;
- data schema validation fails;
- cost or latency exceeds approved budget;
- reviewers cannot be blinded as required;
- evidence-status mutation would occur before claim adjudication.

## Next Route Decision

Decision: repair-needed.

Recommended next actions:

1. Build and record the 3-5 example calibration set.
2. Close protocol hard gates G1-G3 for E1, E2, and E4.
3. Keep E3 second-wave by default unless explicitly approved for first-wave inclusion.
4. Run bounded novelty/source-normalization refresh for publication framing.
5. Return for live approval only after the above repairs are complete.

## Latest Local Approval Check

| Check | Decision | Evidence |
| --- | --- | --- |
| Rubric finalized as scoring gate | pass | `MOGT-REVIEWER-RUBRIC-DRAFT.md` status is `finalized_for_approval_gate`. |
| Calibration examples | repair-needed | No calibration-set artifact exists; 3-5 examples are required. |
| E1 protocol gates G1-G3 | repair-needed | E1 protocol hard gates remain `pending`. |
| E2 protocol gates G1-G3 | repair-needed | E2 protocol hard gates remain `pending`. |
| E4 protocol gates G1-G3 | repair-needed | E4 protocol hard gates remain `pending`. |
| E3 first-wave inclusion | pass as deferred | E3 is second-wave by default. |
| Live model/run parameters | repair-needed | Parameter categories exist, concrete values are not approved. |
| Evidence mutation policy | repair-needed | Evidence status remains insufficient and mutation owner is not approved. |

## Evidence Boundary

This checklist does not approve live experiments.

Do not update:

- `results/MOGT-EVIDENCE-STATUS.md`;
- paper result sections;
- publication claims.
