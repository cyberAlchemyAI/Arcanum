# Distill: Coherent Unit Selection

Status: pass
Mode: standard
Capability: `distill`

## Proposal Tracks

| Track | Claim | Verdict |
| --- | --- | --- |
| New Arcana IntegrationSpec | One named package can coordinate ports, adapters, policies, mappings, standards, and evidence. | useful but too heavy as first move |
| Integration Boundary Discipline | A discipline can define the recurring boundary practice and route to template/validator owners. | selected |
| DomainSpec Integration Aspect | A template aspect can document integration details close to feature specs. | promotion candidate, but not enough alone |
| Formula Validator | A deterministic contract can enforce completeness. | promotion candidate, but cannot select trade-offs alone |
| Standards Crosswalk Only | Existing standards plus guidance may be enough. | insufficient for application-layer evidence envelope |

## Smallest Coherent Unit

Selected unit: **Integration Boundary Discipline**.

Responsibility:

Define the public-safe rules and minimum component catalog for integration boundaries, then route concrete authoring into DomainSpec template extensions and validation into a formula-level contract.

## Why This Unit

It is small enough to avoid premature arcana package weight, but large enough to preserve the core insight: integrations need a governed boundary envelope, not only API shape files.

## Recomposition Proof

The discipline can recompose upward into a future `integration-spec` arcana package if repeated evidence shows that authoring, validation, research, and execution handoff need a single autonomous lifecycle owner.

It can recompose sideways into:

- DomainSpec `integrations.md` template;
- `formulae/integration-contract`;
- Task Session evidence handoff guidance;
- definitions-governance promotion candidates if local terms stabilize.

## Rejected Alternatives

- Immediate new arcana package: useful, but premature without a minimal proof and likely to duplicate standards.
- DomainSpec aspect only: too narrow for provider/resource selection, cache handling, and execution evidence.
- Formula validator only: enforces structure but cannot choose architecture trade-offs.
- Standards crosswalk only: does not capture application-layer authority and evidence.

## Residue

The name `integration-spec` remains useful as the development target and possible future package name. The selected first unit is discipline-first hardening, not immediate sigil creation.
