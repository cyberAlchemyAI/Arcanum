# Stage 01 — Context Builder evidence baseline

## Context Pack Summary

- Task: separate reusable plan readiness from selected-unit material admission
- Mode: `standard`
- Files selected: 10
- Selector groups: 13
- Obligation coverage: 100%
- Handoff pack: runtime
- Strict coverage: `pass`
- Blockers: 0

## Obligations

| ID | Obligation | Status | Evidence |
| --- | --- | --- | --- |
| O1 | Prove why a second audit is currently required. | covered | audit runner `runtime_checks` and verdict construction |
| O2 | Preserve immutable plan, graph, command, write, receipt, closeout, and snapshot checks. | covered | audit README phases 1–3 and 5–7 |
| O3 | Preserve live material admission immediately before mutation. | covered | Task Session Step 5A and `verify-mutation-readiness.py` |
| O4 | Detect semantic plan drift without treating lifecycle bookkeeping as plan drift. | covered | v2 semantic-component structure, proposed selector-value digests, and separate status/lifecycle receipts |
| O5 | Keep explicit selection and zero mutation authority. | covered | audit `selected_unit=null`, `mutation_ready=false`; Task Session live-selection rules |
| O6 | Preserve existing consumers. | covered | additive schema/profile requirement; current `1.0.0` semantics remain strict |
| O7 | Eliminate Invoke Refresh for the no-defect/missing-material case only. | covered | route distinction between plan defect and expected runtime-pending state |
| O8 | Define falsifiable fixtures. | covered | Anime.js five-unit blocked report and named stale/wrong-unit counterexamples |

## Included Context

- `arcanum/spells/work-pack-readiness-audit/README.md` — purpose, phase ownership, output contract, and v1/v2 ceilings — O1, O2, O5, O6
- `arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py:583` — material absence becomes runtime blocker — O1
- `arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py:970` — runtime block lowers the global verdict — O1
- `arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py:991` — report always routes to Invoke Refresh — O1, O7
- `arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py:1156` — v2 also requires the complete material tuple — O6
- `arcanum/spells/work-pack-readiness-audit/schemas/audit-config.schema.json:288` — v1 permits null material but assigns no admission timing — O1, O6
- `arcanum/spells/work-pack-readiness-audit/schemas/audit-report.schema.json:29` — no runtime-pending state and hardcoded next owner — O1, O7
- `arcanum/arcana/task-session/SKILL.md:216` — live admission immediately before the first write — O3, O5
- `arcanum/arcana/task-session/scripts/verify-mutation-readiness.py:322` — exact material, receipt, controls, dependencies, writes, validation, and ownership are re-read — O3, O4
- `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/readiness/results-r2/work-pack-readiness-report.json` — plan and receipt pass while five absent material packages force refresh — O1, O8

## Evidence versus inference

- Evidence: both audit versions require material artifacts before a passing readiness verdict; v1 hardcodes the repair owner; Task Session independently revalidates current material immediately before mutation.
- Inference selected for design: material availability is execution-epoch evidence, not plan-authoring evidence. It can move to the selected Task Session boundary only if the readiness artifact binds selector-level semantic plan values rather than whole mutable Work Pack files.

## Excluded Candidates

- Invoke Refresh internals: excluded because no plan artifact needs mutation in the target success path.
- Anime.js ontology/research evidence: excluded because it cannot change the generic gate boundary.
- External workflow standards: excluded because the local contracts expose the complete tension.

## Authority precedence

Canonical Arcanum sources outrank generated skill mirrors and project run evidence. Project evidence demonstrates the failure mode but does not define public spell behavior.
