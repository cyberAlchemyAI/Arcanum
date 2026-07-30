# Experiment Profile — Work Pack Readiness Audit

## Artifact

- Type: spell
- Canonical ID: `work-pack-readiness-audit`
- Lifecycle owner: `spellcraft`
- Experiment owner: `experiment-harness`
- Validation posture: deterministic synthetic frontier plus adversarial variants

## Question

Can one captured work-pack frontier be audited without executing target commands
while fail-closing graph ambiguity, unsafe command/path contracts, write-scope
drift, current runtime admission gaps, fail-open receipts, attempt lifecycle
gaps, snapshot drift, and refresh authority escalation?

## Independent Variables

- dependency/successor graph;
- task class and requested Task Session execution mode;
- material/output/allowed write sets;
- command cwd, argv, runtime identity, and risk;
- attempt and teardown completeness;
- receipt-schema strength;
- start/end snapshot identity;
- refresh pack authority fields.

## Controlled Variables

- Python standard runtime and installed `jsonschema`;
- repository-relative fixture layout;
- exact SHA-256 and byte-size references;
- audit-only execution policy;
- no network and no target command execution.

## Success Criteria

- the passing read-only frontier returns `pass`, one ready root,
  `selected_unit: null`, and `mutation_ready: false`;
- every acceptance-critical adversary returns a named blocker;
- plan-contract and runtime-admission verdicts remain separate;
- generated report and refresh pack validate against their schemas;
- refresh schema rejects apply authority, mutation readiness, and promotion;
- repeated fixture runs are deterministic.

## Claim Ceiling

Passing fixtures establish deterministic contract behavior for the tested
formats. They do not prove an arbitrary project work pack is ready, do not
select a unit, and do not validate target implementation behavior.
