# Decision Gate: OVS-GATE-002 PromotionRecord Companion Boundary

Status: pass
Date: 2026-06-01
Target scope: PromotionRecord companion template/schema boundary for the branch-aware ontology governed candidate bundle

Resolved: 2026-06-03
Selected option: `promotion-record-canonical-record-kind`

## Blocked Work

The governed candidate bundle is published, and `record_kind: promotion_record` validates as a record-kind profile. The next consequential decision was whether PromotionRecord remains only a profile, receives a candidate authoring template, begins separate schema work, or becomes canonical at a narrower ontology-governance boundary.

Previously blocked downstream work:

- drafting a PromotionRecord companion authoring template,
- creating a separate PromotionRecord schema,
- treating PromotionRecord as a reusable authoring surface beyond the current JSON Schema profile,
- template-level promotion for record-kind profiles,
- DomainSpec or CyberAlchemy handoffs that assume PromotionRecord template authority.

This gate resolves only the record-kind authority boundary. It does not authorize canonical companion templates, separate governed schemas, or external-system adoption obligations.

## Evidence

- `../GOVERNED-CANDIDATE-BUNDLE.md`
- `../VALIDATION-REPORT.md`
- `../WORK-PACK.md`
- `OVS-GATE-001-promotion-boundary.md`
- `../refinement-runs/20260529T160631Z-promotion-record-companion-boundary/RESULT.md`
- `../fixtures/valid/cyberalchemy-caol-promotion-record.json`
- `../schema/branch-aware-ontology-candidate.schema.yml`
- `../tests/validate_branch_schema.py`
- `../tests/validate_branch_json_schema.py`

Current evidence:

- `promotion_record` is valid as a record-kind profile.
- The CyberAlchemy pressure fixture validates as `record_kind: promotion_record`.
- The development JSON Schema candidate validates the fixture corpus.
- OVS-GATE-001 allows the whole validation surface to travel as a governed candidate bundle.
- OVS-GATE-001 does not authorize canonical template mutation or external-system adoption obligations.
- GoldenQuill now provides a canonical applied reference for grant-writing promotion governance that preserves the split between local domain objects and PromotionRecord-compatible owner decisions.

## Blocker Decision

Question:

```text
What companion boundary should PromotionRecord have in the published candidate bundle?
```

## Options

### Option A: Keep Profile Only

Selection value:

```text
promotion-record-profile-only
```

Benefit:

- Safest boundary.
- Keeps PromotionRecord inside the existing base schema plus record-kind profile model.
- Avoids creating template authority before more real PromotionRecord examples exist.
- Preserves CyberAlchemy and DomainSpec owner boundaries.

Cost or risk:

- Future authors do not get a dedicated PromotionRecord authoring shape.
- Repeated PromotionRecord entries may drift in field usage unless validators remain the main guide.

Choose when:

- We want more examples before designing any companion authoring surface.

Downstream impact:

- Update the candidate bundle to say PromotionRecord is profile-only for now.
- Proceed to OVS-GATE-003 or gather more PromotionRecord fixtures.

### Option B: Create Candidate Companion Template Only

Selection value:

```text
promotion-record-candidate-template
```

Benefit:

- Gives authors a reusable candidate template for PromotionRecord entries without making it canonical.
- Uses the existing profile rules and CyberAlchemy pressure fixture as source evidence.
- Helps future PromotionRecord examples stay consistent.

Cost or risk:

- Template language may look more authoritative than intended.
- The template could prematurely freeze authoring ergonomics before DomainSpec and future-system examples mature.

Choose when:

- We want practical authoring support now, but can clearly mark it as candidate-only and non-canonical.

Downstream impact:

- Create a development-only candidate template under the schema-validation package or an Ontology Vault development templates folder.
- Do not mutate canonical Ontology Vault templates.
- Add a validation note tying the template back to the existing `promotion_record` profile.

### Option C: Create Separate Candidate Schema

Selection value:

```text
promotion-record-candidate-schema
```

Benefit:

- Makes PromotionRecord-specific validation more explicit.
- May help if PromotionRecord becomes complex enough to need independent lifecycle, target, rollback, and contradiction rules.

Cost or risk:

- Higher split cost.
- Risks duplicating or drifting from the base ontology entry schema.
- Earlier refine evidence explicitly warned that separate governed schemas were premature.

Choose when:

- We already know PromotionRecord needs independent validation beyond what `record_kind` profiles can express.

Downstream impact:

- Draft a separate candidate schema that composes or references the base schema.
- Add fixtures proving the separate schema catches failures the existing profile cannot.
- Keep it candidate-only.

### Option D: Create Candidate Template Plus Schema

Selection value:

```text
promotion-record-candidate-template-and-schema
```

Benefit:

- Most complete authoring and validation surface.
- Gives both human and machine consumers a dedicated PromotionRecord package.

Cost or risk:

- Highest lock-in.
- Most likely to overfit one CyberAlchemy pressure fixture.
- May create the appearance of canonical PromotionRecord authority before there is enough cross-system evidence.

Choose when:

- We accept that PromotionRecord needs its own candidate package now and are willing to carry the governance overhead.

Downstream impact:

- Create template and schema as candidate-only artifacts.
- Add extra fixtures and validator coverage.
- Open a later promotion gate before any canonical adoption.

### Option E: Promote Canonical Record Kind Only

Selection value:

```text
promotion-record-canonical-record-kind
```

Benefit:

- Promotes the stable ontology-governance concept without over-promoting authoring templates or separate schemas.
- Treats `promotion_record` as the canonical record family for owner-routed promotion decisions.
- Lets GoldenQuill act as the canonical applied reference while preserving local domain model ownership.
- Keeps Inventory, structured-action-schema, DomainSpec, CyberAlchemy, and future systems behind owner-scoped adoption routes.

Cost or risk:

- Authors still need candidate templates or examples before ergonomics are fully stable.
- Implementations must distinguish canonical record-kind semantics from non-canonical template/schema surfaces.
- GoldenQuill fixture pressure is still needed before broader external adoption claims.

Choose when:

- We want PromotionRecord to become the canonical ontology decision shape, but do not want to freeze a companion template or separate schema yet.

Downstream impact:

- Update the candidate bundle to state that `promotion_record` is canonical as a record-kind / governance decision shape.
- Keep the development JSON Schema and authoring templates candidate-only.
- Route GoldenQuill L0 fixtures and future external implementations through PromotionRecord-compatible projection checks.
- Proceed to OVS-GATE-003 or GoldenQuill fixture validation rather than template mutation.

## Recommended Option

Previous recommendation:

```text
promotion-record-candidate-template
```

Rationale:

- PromotionRecord is already profile-backed and fixture-backed enough for authoring support.
- A candidate template gives future sessions a stable shape without splitting schema ownership too early.
- A separate schema is premature because the current profile validates successfully and only one real external pressure family exists.
- The template can remain development-only, candidate-only, and explicitly subordinate to the governed candidate bundle.

Updated recommendation:

```text
promotion-record-canonical-record-kind
```

Rationale:

- The validated profile evidence already proved the core record-kind boundary.
- GoldenQuill adds a concrete applied model showing how local domain candidates can project into PromotionRecord-compatible owner decisions.
- Canonical record-kind promotion captures the real governance primitive without prematurely promoting authoring templates, separate schemas, or external adoption requirements.
- This is a narrower and safer canonical step than making the entire schema or template family canonical.

## Selected Decision

Selected:

```text
promotion-record-canonical-record-kind
```

Source of decision:

- user instruction on 2026-06-03 to refresh the ontology from the GoldenQuill canonical applied strategy;
- GoldenQuill canonical promotion-record refinement at `projects/goldenquill/docs/strategy/goldenquill_canonical_promotion_record_refine_2026-06-03.md`;
- existing Ontology Vault validation evidence for `record_kind: promotion_record`.

Decision effect:

- `promotion_record` is canonical as an Ontology Vault record-kind / governance decision shape.
- Companion templates remain candidate-only until a later template promotion gate.
- Separate PromotionRecord schemas remain deferred until fixture evidence proves independent schema ownership is needed.
- External systems may adapt or project to PromotionRecord, but adoption remains owner-scoped.

## Deferred Decisions

- Whether PromotionRecord ever becomes a canonical Ontology Vault authoring template.
- Whether PromotionRecord ever needs a separate governed companion schema.
- Whether DomainSpec should define its own PromotionRecord-like concept in a DomainSpec-owned package.
- Whether CyberAlchemy source ontology should adopt or map to this profile.
- Whether GoldenQuill L0 fixtures are sufficient to support broader external adoption guidance.

## Required User Decision

Resolved. Historical options were:

```text
A: promotion-record-profile-only
B: promotion-record-candidate-template
C: promotion-record-candidate-schema
D: promotion-record-candidate-template-and-schema
E: promotion-record-canonical-record-kind
```

PromotionRecord companion template/schema work still should not proceed until a later template or schema-specific gate authorizes it.
