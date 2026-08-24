# Governance Defect Receipt

## Classification

- Candidate: `20260820-impeccable-method-adoption`.
- Defect class: governance-only packaging/link projection.
- Product or semantic behavior disputed: no.
- Canonical targets changed during failed apply: no.
- Promotion/publication/generated package changed: no.
- Original exact acceptance consumed as canonical apply authority: no; the apply
  stopped at acceptance-critical preflight.

## Root Cause

The accepted candidate README used two relative links shaped for the candidate's
nested development directory:

- `../../UX-PLAYWRIGHT-EVIDENCE-RESEARCH-STRATEGY.md`
- `../../ux-playwright-evidence-research.dispatch.json`

Preflight projected the candidate README to its canonical target
`arcanum/arcana/ux-evidence-validator/README.md`. From that target location the
links resolve outside the sigil's `development/` directory and do not identify
the existing canonical research strategy/dispatch. Candidate-local validation
had checked the staged package shape without exercising link resolution from
the actual target location.

## Affected Invariant

Acceptance-critical validation must exercise the exact staged bytes at their
declared canonical target paths, including relative Markdown links. A passing
candidate-local check is insufficient when promotion changes a file's directory
depth.

## Minimal Repair

Change only the two README link destinations to:

- `development/UX-PLAYWRIGHT-EVIDENCE-RESEARCH-STRATEGY.md`
- `development/ux-playwright-evidence-research.dispatch.json`

No prose, product rule, evidence model, source card, fixture contract, Work Pack,
or other target content changes.

## Changed-Byte Inventory

| Target | Prior accepted candidate | Repaired candidate | Bytes | Delta |
| --- | --- | --- | --- | --- |
| `README.md` | `a971917eb6d511a74d4475c02f0b8a281cf686236751f019366e84b913603263`, 6630 | `73b04ebcb11147419919e99cf9192c5e23e1783276a225e985cce7cb1bb025bf`, 6642 | +12 | two link destinations only |

The other six acceptance-bound target files remain byte-identical to the prior
candidate. Canonical input digests remain unchanged.

## Required Revalidation

1. regenerate the seven-target digest/byte inventory;
2. compare every live canonical target to its recorded input digest;
3. parse candidate JSON and reference-card YAML;
4. recheck source-card IDs/counts and external provenance boundary;
5. resolve every candidate Markdown link from its projected canonical target,
   using candidate target bytes as an overlay and unchanged canonical files for
   non-target dependencies;
6. verify exact candidate package file inventory, sidecar hashes, whitespace and
   placeholder scans;
7. obtain one independent read-only observer verdict over the repaired bytes and
   target-overlay result;
8. request renewed owner acceptance bound to the repaired README and current
   manifest; never stretch the older exact acceptance over repaired bytes.

## Renewed Owner Acceptance

Required: yes. README is acceptance-bound and its digest/bytes changed, even
though the repair is mechanically obvious and governance-only. The prior phrase
`accept exact UEV candidate` bound the previous README digest and cannot authorize
the repaired target.

## Regression Fix

`validate-target-overlay.py` is added as a candidate-local, repeatable regression
check. It validates exact inventory/digests and resolves Markdown links from
projected canonical target locations. The next acceptance request must cite its
passing result. Promoting this check into a shared Sigil Development workflow is
a separate lifecycle decision; this repair does not mutate canonical workflow
code without authority.

## Authority Ceiling

This receipt authorizes no canonical apply, generated-package sync, promotion,
publication, commit, push, or product work. It records the governance defect,
repair, required validation, and renewed acceptance boundary only.
