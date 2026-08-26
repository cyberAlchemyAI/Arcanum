---
artifact_id: resolution-router.review.post-promotion.2026-08-25
artifact_type: validation-report
intent: Record the independent post-promotion review of the lens and resolution routing slice.
owner: resolution-router
lifecycle_status: reviewed
constitution_selectors:
  - framework.artifact-metadata
  - framework.sigil-development
validation_profile:
  - adversarial-review
  - routing-skill
evidence_role: durable-evidence
---

# Post-Promotion Review — Lens and Resolution Routing

Date: 2026-08-25  
Dispatch: `routing-post-promotion-review-20260825`  
Run: `routing-review-20260825-001`  
Verdict: **FIX**

Five `MAJOR` findings survived independent verification. No `CRITICAL` or
`MINOR` finding survived. The routing architecture itself remained coherent
under attack: lens selection, resolution selection, low-tier writing, direct
entry, unavailable medium/high stopping, dependency closure, generated-package
fidelity, and repository adapters showed no verified ownership or route defect.
The release claim is not yet adequately governed or evidenced, however.

## Coverage

| role | adversarial lens | resolved coverage | result |
|---|---|---|---|
| governance attacker | lifecycle fidelity, promotion authority, ownership, abuse resistance | 36 target files across the three routing packages, promotion surfaces, validators, installer, registry, workflow/template, and three adapters | 3 candidates |
| operability attacker | executable correctness, installation closure, validators, redirects, availability, evidence reproducibility | same corpus; two isolated selective installs plus semantic and adversarial checks | 3 candidates |
| independent skeptic | literal refutation, severity calibration, coverage and zero-finding audit | all six candidates and the same resolved target corpus | 5 survived; 1 refuted |

The review workspace was read as dispatch authority but excluded from the target
corpus by `review.dispatch.json:276-278`. Both attackers supplied concrete
zero-finding defenses. The skeptic accepted coverage for both lenses.

## Findings

### F1 — Forward-test evidence does not bind the current contracts (`MAJOR`)

Locators:

- `transmutations/resolution-router/development/validation/FORWARD-TESTS-2026-08-25.md:27-36`
- `transmutations/lens-router/SKILL.md`
- `transmutations/resolution-router/SKILL.md`
- `transmutations/low-resolution-explanation/SKILL.md`
- the three `SKILL.md.artifact.yml:6` sidecars

Evidence: the report binds its behavioral results to `24EAFD…`, `3F6BC2…`, and
`3DCE85…`. Current SHA-256 values are:

- `lens-router`: `3331FB648050DEBA1295944C2DFDF0E77E7F7DF97BB222539A2160C52A3DF0AD`;
- `resolution-router`: `365994C2F08F646AD43A8211C2D3314AD38D667E41E0C17C6B66498F7E18CBD4`;
- `low-resolution-explanation`: `979E2F2EA11AB9C30549B3D5263F4A2F30512FCDE25EA9ED2A322CB844BE288B`.

The report also claims canonical sidecars, while all three current sidecars are
`reviewed`. Consequently, the durable forward-test record cannot substantiate
the present contracts' routing behavior.

Change request: rerun the complete final forward-test matrix against the exact
current trio and replace the report's digests and lifecycle claim with evidence
from that tested package.

### F2 — Required raw forward-test evidence is absent (`MAJOR`)

Locators:

- `transmutations/resolution-router/references/validation.md:55-58`
- `transmutations/resolution-router/development/validation/FORWARD-TESTS-2026-08-25.md:20-40`
- `transmutations/resolution-router/development/validation/FORWARD-TESTS-2026-08-25.md:74-83`
- `transmutations/resolution-router/development/validation/`

Evidence: the validation contract requires commands, results, raw artifacts,
and user-like prompts under `development/validation/` before registry
promotion. The durable directory contains the two narrative reports and the
post-review governance files, but no test prompts, packets, plans, writer
outputs, guarantee audits, validator outputs, commands, or agent receipts.

Consequence: redirect-once termination, exactly-one-writer execution, finding
preservation, and no-fallback behavior cannot be independently replayed or
falsified from governed evidence.

Change request: persist one compact evidence bundle per final forward-test
scenario containing the exact prompt, packet, plan, result or audit, validator
output, and content digests.

### F3 — Promotion accepts a non-canonical lifecycle state (`MAJOR`)

Locators:

- the three `SKILL.md.artifact.yml:6` sidecars;
- `transmutations/resolution-router/development/validation/FORWARD-TESTS-2026-08-25.md:27-28`;
- `transmutations/resolution-router/development/validation/VALIDATION.md:47` and `:84-90`;
- `tools/validate-artifact-metadata.py:35-42` and `:290-292`;
- `tools/bootstrap_arcanum.sh:892-907`.

Evidence: each current sidecar says `lifecycle_status: reviewed`, while the
evidence says the sidecars advanced to canonical and registry promotion is
complete. Strict metadata validation passes with `checked: 3` because it only
requires a recognized state, not the canonical state claimed by promotion.
Fresh selective installs faithfully reproduce the `reviewed` sidecars.

Consequence: registry exposure and validation prose can declare canonical
completion without the governed artifacts proving the transition.

Change request: add one blocking promotion-state check requiring every selected
source sidecar to be `canonical`, then reconcile the trio's sidecars and
validation claims through an authorized promotion decision.

### F4 — The documented PowerShell fixture path is not executable (`MAJOR`)

Locators:

- `transmutations/resolution-router/references/validation.md:21`;
- `transmutations/lens-router/scripts/validate_lens_packet.py:392-395`.

Evidence: on the repository's Windows PowerShell host, the documented `>`
redirection emitted UTF-16LE bytes beginning `FF FE 7B 00 0D 00 0A 00`.
`validate_lens_packet.py` reads the file only as UTF-8 and does not catch
`UnicodeDecodeError`; both the attacker and skeptic reproduced the resulting
traceback.

Consequence: the supplied-valid-packet scenario fails on the active host and
returns an unbounded traceback instead of a controlled validation result.

Change request: provide an encoding-stable UTF-8 fixture-emission path in the
validator and documented command, and classify decode failures as bounded input
errors.

### F5 — The authoring and promotion surfaces do not enforce ownership and entry inputs (`MAJOR`)

Locators:

- `framework/SIGIL-DEVELOPMENT-WORKFLOW.md:63-78`, `:83-95`, and `:200-211`;
- `framework/templates/sigil-template.md:14-54`;
- `registry/SIGILS.md:123-133`.

Evidence: Intent Design names objective, ownership, inputs, and output contract,
but the mandatory Behavior Contract list omits ownership and inputs. The
template has no ownership, authority, inputs, or entry-contract section, and
the Promotion and registry-entry lists do not restore them. The current routing
trio compensates manually, but the normal authoring path does not require that
compensation.

Consequence: a future router can satisfy the documented template and promotion
surface while leaving selection, redirection, approval, or input authority
ambiguous.

Change request: add ownership/authority and inputs-or-entry-contract sections
to the template and require those sections in the Behavior Contract and
Promotion checks.

## Refuted candidate

The skeptic refuted `GOV-003`, which alleged ambiguity over whether the review
workspace belonged to the target corpus. The dispatch explicitly excludes that
workspace from reviewed targets. Its readability as dispatch authority does not
make it a target, and neither attacker demonstrated divergent coverage.

## Artifact verdicts

| surface | verdict | basis |
|---|---|---|
| lens-router / resolution-router / low writer contracts | **FIX before canonical claim** | semantic ownership and routing survived, but current contracts lack binding behavioral evidence |
| route manifest, cumulative guarantees, dependency closure | **KEEP** | low is available; medium/high are absent and stop as unavailable; no substitute or smuggled guarantee survived |
| generated installed packages and repository adapters | **KEEP** | two isolated installs closed over the trio; bodies/support files matched; adapters resolved without redefining behavior |
| validation evidence and lifecycle promotion | **FIX** | F1, F2, and F3 |
| fixture validator/documentation | **FIX** | F4 |
| sigil workflow, template, and registry admission surface | **FIX** | F5 |

## Verified non-findings

- Lens work belongs to `lens-router`; tier choice and writer dispatch belong to
  `resolution-router`; reader-facing low representation belongs to the low
  writer. No double ownership survived.
- Direct-entry transition rules terminate on complete handoffs, and unavailable
  medium/high routes forbid fallback. The semantic validators reject fake
  targets and higher-tier guarantees smuggled into low plans.
- Dependency closures, Draft 2020-12 schema checks, semantic self-tests,
  metadata/dependency self-tests, Markdown links, and adapter targets passed.
- No attacker, skeptic, or parent modified the reviewed target during review.

## Evidence boundary

This verdict applies to the observed working-tree bytes, which were already
modified or untracked before the review and are not bound to a commit. Medium
and high writers were out of scope except for their explicit unavailability
semantics. Prior temporary installed packages were available, but they do not
replace the missing governed raw forward-test artifacts. Review lifecycle
evidence is under `.arcanum/runtime/routing-post-promotion-review/`; isolated
install trees and the retained PowerShell fixture remain there as recorded
runtime residue.

No reviewed-target fix was applied during this review. The next admissible step
is a bounded repair pass over F1-F5 followed by deterministic validation and a
fresh independent post-fix review.
