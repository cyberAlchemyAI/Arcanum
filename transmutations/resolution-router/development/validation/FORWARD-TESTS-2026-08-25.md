---
artifact_id: resolution-router.validation.forward-tests.2026-08-25
artifact_type: validation-report
intent: Record fresh-agent behavioral evidence for the routing-skill trio before promotion.
owner: resolution-router
lifecycle_status: reviewed
constitution_selectors:
  - framework.artifact-metadata
  - framework.sigil-development
validation_profile:
  - artifact-metadata
  - routing-forward-tests
evidence_role: durable-evidence
---

# Forward Tests — Routing Skills

Date: 2026-08-25

## Evidence package

Behaviorally tested installed package:
`C:\tmp\arcanum-routing-install-20260825-v4-calibrated\.agents\skills`.

The post-promotion package was regenerated at
`C:\tmp\arcanum-routing-install-20260825-v5-promoted\.agents\skills`. Its three
generated `SKILL.md` contracts were unchanged; the copied artifact sidecars
advanced from `candidate` to `canonical` after the behavioral gates passed.

Canonical skill-contract SHA-256 values:

- `lens-router`: `24EAFD91A0C997392D04C9ADE91EBD30106E9968CC3B0268EDB69166C0A59372`;
- `resolution-router`: `3F6BC222B7A6515FAD4CA4CF0808D0177DA8C44FBC36781C57054D323B857F6F`;
- `low-resolution-explanation`: `3DCE85BB6C1E1C89D5DD134ABB476CCEFA518320B6DE934B11B9F2AD1B48C50A`.

Every agent received `fork_turns: none`, one user-like prompt, the installed
skill path, and the installed files as its evidence boundary. Agents were not
given expected results, earlier findings, or proposed fixes.

## Results

| ID | scenario | observed behavior | verdict |
|---|---|---|---|
| FT-01 | ordinary explanation, first attempt | selected `medium` because the source mentioned architecture and handoffs; returned unavailable | FAIL; exposed excessive promotion |
| FT-01R | ordinary explanation after calibration repair | selected `low`, one categorical lens, executed the low writer, and returned all `L01`–`L10` audits | PASS |
| FT-02 | direct low writer invocation on final package | redirected through the router, obtained a valid packet and plan, executed low exactly once, and returned finding disposition plus all low audits | PASS |
| FT-03 | explicit high | selected `high`, validated packet and plan, returned exact unavailable target, executed zero writers, and emitted no fallback prose | PASS |
| FT-04 | evidence-only claim question | selected only `epistemic`, left composition empty, validated the packet, and preserved the claim ceiling | PASS |
| FT-05 | evidence authority constraining a state transition | selected `epistemic` and `systemic`, completed independent findings, composed cross-lens relations, and validated the packet | PASS |
| FT-06 | requested low but operational comparison required | promoted to `medium` with `M01-operational-model`, returned the unavailable writer, and did not downgrade | PASS |
| FT-07 | review an over-detailed low explanation | identified the first excessive passage, first unearned concept, first failed guarantee `L01`, and the smallest repair without rewriting | PASS |

## Failure, repair, and retry

FT-01 initially reported:

> A new maintainer needs an operational model ... This requires
> `M01-operational-model` and `M02-boundaries-assumptions`; low resolution is
> insufficient.

The prompt asked only why lens selection and explanation resolution are
separate. The routing contract was repaired to classify the action the reader
must perform rather than the complexity nouns in the source. The guarantee
reference now states that low may name central roles, one essential handoff,
and a load-bearing branch for orientation. FT-01R then selected low and stated:

> The maintainer needs rationale, two central roles, and one essential
> handoff—not an operational or implementation model.

No other forward-test failure required a contract change.

## Key acceptance evidence

- Direct entry terminates: the final direct-low result redirected once and
  returned a complete explanation plus audit; it did not redirect a complete
  handoff.
- Lens cardinality is selective: the evidence-only question selected one lens,
  the transition question selected two, and the direct-low architecture request
  selected all three.
- Composition augments individual findings: the two-lens packet retained every
  `E*` and `S*` finding and composed only cross-lens IDs.
- Tier semantics are cumulative and non-fallback: promotion selected medium;
  explicit high selected high; both unavailable targets stopped without prose
  from the low writer.
- Review mode is read-only: it proposed one bounded repair and explicitly left
  later defects for subsequent revision.

## Verdict

`PASS` for the final installed low-resolution routing slice. Medium and high
remain reserved and unavailable; this report does not validate their writers.
