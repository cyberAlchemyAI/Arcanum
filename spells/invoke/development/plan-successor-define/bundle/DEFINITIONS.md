# Invoke Plan Successor Candidate Definitions

Status: candidate
Owner route: definitions-governance
Scope: feature:invoke-plan-successor
Authority effect: none

## Candidate Definitions

### PLAN-D1: Plan authoring source

Aliases: Plan source document
Status: candidate

#### Normative voice

The Plan authoring source is the sole machine-readable document whose authored fields state the proposed Work Pack, requested effect, route contracts, and readiness configuration for one Plan candidate.

#### Plain-language voice

The one JSON file where we write what the Plan is supposed to contain before tools generate the rest.

#### Domain context

In Invoke Plan, this replaces scattered author-controlled fields across generated Work Pack files and receipts while retaining the current plan-execution-source v1 as migration evidence.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Authoring Source`; sha256 `807eaf92f5450150bfdb6bee23d76772170072fba9a02592e3977b506cf5966c`)
- evidence: `arcanum/spells/invoke/schemas/plan-execution-source-v1.schema.json` (json-pointer `/properties`; sha256 `c401f799453a662f4bb5a1fb18538c8fdef8265d727afa4c19c421d927cdbc2a`)
- evidence: `arcanum/spells/invoke/scripts/compile_plan_execution_source.py` (symbol `compile_source`; sha256 `d3e06c232d3ce2060b7846b9c8dabdae8955cab64b6ef4dec5ac350ee2107f82`)
- evidence: `arcanum/spells/invoke/design.md` (heading `Activation Gate`; sha256 `5651f9e5d0fe5fe66af4c1fced08ebabe8fd18f714824163f352ba9d27fe68f6`)

### PLAN-D2: Plan candidate bundle

Aliases: generated Plan bundle
Status: candidate

#### Normative voice

A Plan candidate bundle is the complete ordered set of files deterministically generated from one exact Plan authoring source and its bound predecessor evidence.

#### Plain-language voice

All Plan files produced together from one source, held for checking before anyone treats them as accepted.

#### Domain context

The bundle contains the Work Pack and its supporting planning, layering, trace, and producer evidence; it is not the execution of that Work Pack.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Candidate Bundle`; sha256 `807eaf92f5450150bfdb6bee23d76772170072fba9a02592e3977b506cf5966c`)
- evidence: `arcanum/spells/invoke/PLAN-ARTIFACT-BOUNDARIES.md` (heading `Artifact Boundary Summary`; sha256 `7f8aa4d74af790e9afed0501944596c2d21cdc9ae26cb18b1fe6c098a513b1a7`)
- evidence: `arcanum/spells/invoke/plan.md` (heading `Mode Output Contract`; sha256 `b447d50d0cb023965c85a28f468faec360d261505e73c20a8bb48b3f3f577c5c`)

### PLAN-D3: Plan bundle admission

Aliases: Plan admission result
Status: candidate

#### Normative voice

Plan bundle admission is an independent point-in-time result that replays one exact Plan authoring source, compares every required bundle member, and runs the declared structural and consumer checks for that exact candidate.

#### Plain-language voice

A second checker proves that this exact generated Plan still matches its source and works with the checks that depend on it.

#### Domain context

Plan admission sits after deterministic generation and before capability status. Work Pack Readiness Audit and Implementation Readiness remain separate later proofs.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Bundle Admission`; sha256 `807eaf92f5450150bfdb6bee23d76772170072fba9a02592e3977b506cf5966c`)
- evidence: `arcanum/spells/invoke/scripts/prepare_plan_implementation_readiness.py` (symbol `main`; sha256 `e83d0d264df0f606be993f6dfd8372af9c23cdeab7eb0c07b906ae078546893c`)
- evidence: `arcanum/spells/work-pack-readiness-audit/README.md` (heading `Purpose`; sha256 `7942d0e7d80b74bc9a400773244ad071b79fe93c54ba204ab6ab3a31f3359401`)
- evidence: `arcanum/spells/implementation-readiness/README.md` (heading `Work-Pack Execution Outer Loop`; sha256 `1556cee05fc11bcc553ba4760f4c85edfa0136927961d43bd967537d54b34bca`)

### PLAN-D4: Plan evidence state

Aliases: Plan proof state
Status: candidate

#### Normative voice

A Plan evidence state is the typed statement of the highest Plan claim established by exact current receipts, while preserving all later unproved or unauthorized states as separate fields.

#### Plain-language voice

A precise answer to what we have proved about the Plan so far, without turning 'written' into 'ready' or 'approved.'

#### Domain context

Invoke uses this state to hand a Plan successor into later readiness and execution workflows without collapsing artifact PASS into permission to mutate a product.

#### Evidence

- evidence: `arcanum/spells/invoke/development/plan-successor-define/DISCOVERY.md` (heading `Plan Evidence State`; sha256 `807eaf92f5450150bfdb6bee23d76772170072fba9a02592e3977b506cf5966c`)
- evidence: `arcanum/spells/invoke/README.md` (heading `Evidence Capability Contract`; sha256 `489c0208cec0cceb9f7af8b98debfafe7aeabd36dea395007fd4bd8df3dcdcba`)
- evidence: `arcanum/spells/invoke/scripts/capability_status_resolver.py` (symbol `resolve_capability_status`; sha256 `4bf4de651f6c747c54c9c76eddb558fa2a7635cd7d71ce1f0857a52074ad277f`)

## Semantic Applications

| Probe | Disposition | Candidate definitions | Authority bindings |
| --- | --- | --- | --- |
| probe:plan-authoring-source | new-scoped-term | PLAN-D1 | none |
| probe:plan-candidate-bundle | new-scoped-term | PLAN-D2 | none |
| probe:plan-bundle-admission | new-scoped-term | PLAN-D3 | none |
| probe:plan-evidence-state | new-scoped-term | PLAN-D4 | none |
