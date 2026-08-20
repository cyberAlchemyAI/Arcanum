# Decision Gate: OVS-GATE-004 Default Output Declaration

Status: pass
Date: 2026-08-20
Resolved: 2026-08-20T00:48:17Z
Target scope: `ontology-vault` `<default-output>` — whether a machine-readable JSON
artifact becomes the declared default creation pattern.

## Blocked Work

`<default-output>` in `arcana/ontology-vault/SKILL.md` names four markdown fallbacks and
no machine-readable artifact. The sigil nevertheless already emits a JSON validation record;
version 0.3.0 added `<emission-contract>` documenting that record but did not make it the
declared default. Changing `<default-output>` and `<output-contract>` was blocked pending
this gate.

## Evidence

- `arcana/ontology-vault/SKILL.md` `<default-output>`, `<output-contract>`, `<emission-contract>`
- `OVS-GATE-001-promotion-boundary.md` — Still disallowed: "promoting canonical Ontology Vault
  templates"; "treating the JSON Schema candidate as final canonical schema"
- `OVS-GATE-002-promotion-record-companion-boundary.md`
- `../GOVERNED-CANDIDATE-BUNDLE.md#remaining-gates` — Template promotion gate `pending`;
  Label governance gate `deferred`
- `../schema/branch-aware-ontology-candidate.schema.yml` — `$defs.branch_context.properties.primary.enum`
  = `[meaning, system, operational, bridge]`
- Repository census (16 ontology directories, 1518 JSON records): 1067 record-per-file
  documents against 5 carrier documents; `schema_version` present in 971 (64%) with values
  split across slash and dot type identities plus 188 bare semvers; `authority_effect` present
  in 366 (24%) and constant `none` in 353 of those (96%)
- Three-agent tournament `2026-08-20-ontology-vault-dialect-convergence` (tension gate: checker
  PASS, reviewer PASS), receipts held on the private side

## Blocker Decision

Question:

```text
What should ontology-vault's <default-output> declare?
```

## Admissibility

One candidate was excluded before presentation rather than offered and rejected:

**Excluded — "JSON primary plus the candidate schema shipped as canonical."**
`OVS-GATE-001` lists "treating the JSON Schema candidate as final canonical schema" under
*Still disallowed*. The candidate schema's `branch_context.primary` enum also contains
`meaning`, whose governance is `deferred` by the Label governance gate. Adopting it would
import a label under deferred governance and would require reopening two gates. Structurally
inadmissible at this gate; not put to the operator.

Verified discriminator: the sigil's own branch vocabulary is `business | system | bridge`
(`SKILL.md` argument-hint). `meaning` appears in `SKILL.md` only as ordinary English
("domain meaning", "business meaning"), never as a label value. Declaring the sigil's own
record format therefore does not touch the deferred label; adopting the candidate schema does.

## Options Presented

### Option A: Leave markdown as the sole default

```text
leave-markdown-default
```

- Benefit: zero governance risk; respects every open gate.
- Cost: the sigil's primary artifact stays unvalidatable prose; the operator's request is unaddressed.
- Choose when: the Template promotion and Label governance gates should clear first.
- Downstream: revisit after those gates.

### Option B: JSON primary for sigil-written artifacts, markdown derived

```text
json-primary-sigil-written-only
```

- Benefit: a validatable primary artifact; imports no deferred label; promotes no template;
  imposes nothing on the sixteen existing ontologies. Matches the point three independently
  angled agents converged on: *the contract governs what the sigil writes, never what owners write.*
- Cost: narrow. Governs the sigil's own output rather than a rich graph format. No canonical
  schema ships, so validation remains per-repository.
- Choose when: progress is wanted without reopening deferred governance.
- Downstream: Template promotion and Label governance remain untouched; a richer graph format
  stays a later decision.

### Option D: Scope the default by ontology type

```text
scope-default-by-ontology-type
```

- Benefit: matches evidence — `business-system-bridge` and `architecture-property` generate
  typed edges and properties by construction, and one consuming repository already runs
  `architecture-property` in JSON. Explicitly protects the small-repository case the sigil's
  own anti-patterns defend.
- Cost: two output modes to maintain; the general case stays unresolved.
- Choose when: the small-map case needs explicit protection now.
- Downstream: partial resolution; a later gate still needed for the general case.

## Selected Option

Selected:

```text
json-primary-sigil-written-only
```

Source of decision:

```text
Operator selection through decision-gate on 2026-08-20.
```

Rationale:

- It is the narrowest change that answers the request.
- It touches neither gate that is still open: no template is promoted, and the deferred
  `meaning` label is not imported because it is absent from the sigil's own vocabulary.
- It matches the one conclusion three opposed tournament angles reached independently.
- It is reversible: revert the contract block and bump the version.

## Allowed Next Work

- Rewrite `<default-output>` so a machine-readable JSON artifact is the declared primary
  output for artifacts the sigil writes, with markdown as a derived view.
- Update `<output-contract>` consistently.
- Bump the package version and regenerate the generated runtime mirrors from canonical.

## Still Disallowed By This Gate

- Promoting canonical Ontology Vault templates (OVS-GATE-001, unchanged).
- Treating the branch-aware candidate schema as final canonical schema (OVS-GATE-001, unchanged).
- Importing `meaning` or any other label under deferred governance.
- Requiring any consuming repository to emit, adopt, or migrate to these keys.
- Rewriting records held by owners.

## Deferred Decisions

- Whether the emitted record's dot-grammar identity is normalized to the package's slash
  grammar. Recorded in `<emission-contract>` as owner-routed; renaming would orphan records
  already held by a consuming repository.
- Whether the sixteen ontologies ever converge on one record contract. Costed at 616 records
  requiring per-record owner authorship (~255 distinct decisions); no owner route exists for
  cross-project ontology migration.
- Whether a richer graph format becomes a default for any ontology type (Option D remains
  available at a later gate).
- Template promotion gate and Label governance gate remain `pending` and `deferred`.

## Assumptions Recorded

- Version 0.3.0's `<emission-contract>` addition was not itself gated: it documented behaviour
  that was already occurring and appears nowhere in OVS-GATE-001's disallowed list.
- The census denominators used as evidence are scope-bound (16 directories, 1518 records,
  excluding `development/` and staged replicas). Agent counts over other scopes agree on
  proportions but not absolutes.

## Gate Result

Result:

```text
PASS
```

No blocker remains for rewriting `<default-output>` within the bounds above.
