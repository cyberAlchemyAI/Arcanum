# Decision Gate: OVS-GATE-001 Promotion Boundary

Status: pass
Date: 2026-05-31
Resolved: 2026-06-01T07:43:33Z
Target scope: branch-aware ontology development schema, JSON Schema, record-kind profiles, and templates

## Previously Blocked Work

The development validation surface is passing, but canonical mutation was blocked until the promotion boundary became explicit.

Previously blocked downstream work:

- canonical Ontology Vault template mutation,
- canonical branch convention update,
- treating the development JSON Schema as governed schema,
- requiring Inventory or structured-action-schema to emit/adopt ontology fields,
- promoting `record_kind` profiles into authoring templates.

The gate now resolves what may proceed: the validated development surface can move forward as a governed candidate bundle only. Final canonical templates and external-system obligations remain out of scope.

## Evidence

- `../VALIDATION-REPORT.md`
- `../WORK-PACK.md`
- `../../BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md`
- `../schema/branch-aware-ontology-candidate.schema.yml`
- `../tests/validate_branch_schema.py`
- `../tests/validate_branch_json_schema.py`

Development validation currently passes:

- deterministic fixture validator,
- development JSON Schema validator,
- Artifact Constitution validation with existing unrelated generated-artifact warnings.

## Blocker Decision

Question:

```text
What is allowed to move from development-only ontology schema work toward canonical Ontology Vault conventions/templates now?
```

## Options

### Option A: Promote Nothing Yet

Selection value:

```text
promote-nothing
```

Benefit:

- Safest governance boundary.
- Keeps the whole model exploratory.
- Avoids freezing `meaning`, `record_kind`, profile rules, or lifecycle fields too early.

Cost or risk:

- No canonical consumer can rely on the schema yet.
- Future sessions must keep carrying development context.

Choose when:

- We want more pressure from DomainSpec, real future-system examples, or mutation primitive catalog work before promotion.

Downstream impact:

- Next route should be a development continuation, likely mutation primitive catalog or DomainSpec handoff.

### Option B: Promote Minimal Vocabulary Only

Selection value:

```text
promote-minimal-vocabulary
```

Benefit:

- Canonicalizes only the safest conceptual split:
  - `branch_context.primary`
  - `meaning | system | operational | bridge`
  - Inventory non-authority boundary
  - development/canonical separation
- Lets other artifacts reference the branch vocabulary without adopting the full schema.

Cost or risk:

- `record_kind`, lifecycle statuses, JSON Schema, and templates remain development-only.
- Requires a narrow convention note or template advisory.

Choose when:

- We trust the branch discriminator but do not want to lock the whole schema.

Downstream impact:

- Create a small canonical convention candidate while keeping schema/profile validation in development.

### Option C: Promote Vocabulary Plus Record-Kind Profiles As Candidate Templates

Selection value:

```text
promote-vocabulary-and-profile-templates
```

Benefit:

- Makes the validated record families available for authoring:
  - `ontology_entry`
  - `promotion_record`
  - `evidence_input`
  - `bridge_validation`
- Gives future ontology entries a reusable shape.

Cost or risk:

- Higher chance of freezing profile boundaries before DomainSpec and future-system evidence mature.
- PromotionRecord companion-template questions may return quickly.

Choose when:

- We want practical authoring templates now and accept that they are candidate templates, not final templates.

Downstream impact:

- Build Ontology Vault candidate templates from the validated development schema and keep them gated.

### Option D: Promote Development JSON Schema As Canonical Candidate Schema

Selection value:

```text
promote-json-schema-candidate
```

Benefit:

- Makes validation executable for canonical-ish ontology entries.
- Reduces ambiguity for future agents.

Cost or risk:

- Highest lock-in.
- May overfit current fixtures.
- Requires a strong statement that `.schema.yml` is candidate-governed, not final truth.

Choose when:

- We believe the fixture suite is sufficient for a first governed candidate schema.

Downstream impact:

- Move or copy the development schema into the appropriate canonical/candidate schema location and add template validation.

### Option E: Promote Governed Candidate Bundle

Selection value:

```text
promote-governed-candidate-bundle
```

Benefit:

- Carries the whole validated development bundle forward without pretending every layer has final authority:
  - branch vocabulary,
  - schema axes,
  - record-kind profiles,
  - development JSON Schema candidate,
  - fixture validator,
  - validation report.
- Preserves the useful parts of "promote everything" while keeping canonical templates, Inventory, structured-action-schema, DomainSpec ownership, and future-system obligations out of scope.
- Gives future sessions one coherent candidate package to test instead of scattering the schema across development notes.

Cost or risk:

- Requires strict wording that the bundle is a governed candidate, not a final canonical schema.
- Consumers may still confuse candidate validation with required adoption unless the boundary is repeated in the package index and templates remain unmutated.
- PromotionRecord companion templates and DomainSpec-owned packages remain unresolved.

Choose when:

- We trust the current validation pass enough to keep the full bundle together, but not enough to require all ontology authors or external systems to adopt it.

Downstream impact:

- Create or refresh a candidate-bundle index that points to the existing development schema, JSON Schema, fixtures, validators, and report.
- Do not mutate canonical Ontology Vault templates yet.
- Do not require Inventory, structured-action-schema, DomainSpec, CyberAlchemy, or future systems to emit the fields.

## Recommended Option

Recommended:

```text
promote-governed-candidate-bundle
```

Rationale:

- The branch discriminator and Inventory non-authority boundary are stable enough to reference.
- The record-kind/profile layer and JSON Schema are validated enough to keep as one coherent candidate package.
- They are not yet mature enough to become final canonical templates or required external-system obligations.
- This answers the "why not everything?" concern by allowing everything to travel together as candidate evidence, while refusing only the unsafe part: final authority over templates and adopters.

## Selected Option

Selected:

```text
promote-governed-candidate-bundle
```

Decision source:

```text
User selected "option E" through decision-gate on 2026-06-01.
```

Decision rationale:

- Promote the whole validated development surface as one coherent candidate package.
- Preserve the distinction between candidate validation and canonical authoring authority.
- Keep canonical Ontology Vault templates unmutated until a later template-specific gate.
- Keep Inventory and structured-action-schema as evidence or handoff surfaces, not emitters or ontology authorities.
- Keep DomainSpec, CyberAlchemy, and future-system adoption as separate owner-scoped work.

Allowed next work:

- Create or refresh a governed candidate-bundle index.
- Reference the development schema, JSON Schema candidate, fixtures, validators, and validation report as candidate evidence.
- Plan follow-up gates for templates, PromotionRecord companion work, and DomainSpec handoff.

Still disallowed by this gate:

- promoting canonical Ontology Vault templates,
- requiring Inventory to emit ontology fields,
- mutating structured-action-schema,
- treating the JSON Schema candidate as final canonical schema,
- mutating DomainSpec or CyberAlchemy source packages,
- requiring future systems to adopt the fields.

## Deferred Decisions

- Whether `promotion_record` needs a companion schema/template.
- Whether DomainSpec should receive a separate ontology package.
- Whether the mutation primitive catalog should become part of ontology core or a bridge/profile extension.
- Whether `meaning` becomes canonical as the long-term first branch label.

## Gate Result

Result:

```text
PASS
```

No blocker remains for creating a governed candidate-bundle index. Canonical template mutation remains blocked behind a later, narrower gate.
