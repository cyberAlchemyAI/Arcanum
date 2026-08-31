## Source Fields In Schema Order

The top-level object rejects unknown properties and requires every field below.

| Field | Required value or decision |
| --- | --- |
| `schema_version` | fixed `invoke.define-source.v2` |
| `source_id` | 3-128 characters; starts alphanumeric; remaining characters alphanumeric, `.`, `_`, or `-` |
| `target` | `{id, objective}` as non-empty strings |
| `discovery` | either `{kind:"artifact", ref:<exact ref>}` or `{kind:"waiver", waiver_reason:<8+ chars>}` |
| `template_selection` | profile and selected are fixed `invoke.generic-definitions-baseline.v2`; `eligible` is a non-empty unique string array containing the selected profile; `tie` is fixed `false` |
| `spec_declarations` | non-empty array of `{id,title,statement}` non-empty strings |
| `definition_registry` | registry metadata plus one or more complete candidate definitions |
| `layering` | seed `{kind:"seed",decision,minimum_unit}` or gap `{kind:"gap",rationale:<8+ chars>}` |
| `dispatch_trace` | `{techniques:[...]}` with at least one unique non-empty technique id |
| `distill` | required/pass `{classification:"required",verdict:"pass",evidence}` or not-required `{classification:"not-required",rationale:<8+ chars>}` |
| `identity_denominator` | required `{classification:"required",request_ref,result_ref}` or not applicable `{classification:"not-applicable",rationale:<8+ chars>}`; a required result must contain `verdict:"pass"` |
| `output_contracts` | the fixed filenames listed below, with layering chosen to match the layering branch |
| `transport_policy` | fixed `{append_existing_only:true,upstream_mutation:false,targets:[]}` |
| `next_route` | `design`, `spellcraft`, `sigil-development`, or `deferred` |

The output contract is exact:

```json
{
  "spec": "SPEC.md",
  "definitions": "DEFINITIONS.json",
  "definitions_view": "DEFINITIONS.md",
  "glossary": "GLOSSARY.md",
  "layering": "LAYERING-GAP.md",
  "template_selection": "TEMPLATE-SELECTION-RECEIPT.json",
  "dispatch_trace": "DISPATCH-TRACE.json",
  "distill": "DISTILL-RECEIPT.json",
  "identity_denominator": "IDENTITY-DENOMINATOR-RECEIPT.json",
  "transport": "DEFINE-TRANSPORT-REPORT.json",
  "stage_receipt": "INVOKE-DEFINE-STAGE-RECEIPT.json"
}
```

Use `IMPLEMENTATION-LAYERING.md` instead of `LAYERING-GAP.md` when
`layering.kind` is `seed`. The successful directory contains these eleven
files; the stage receipt describes the other ten outputs rather than listing
itself.

The registry requires `registry_id`, `title`, `owner_route`,
`authority_scope`, `visibility`, and `definitions`. A registry id starts with a
letter and then uses letters, digits, `.`, `_`, or `-`. Authority scope is
`{kind,ref}` where kind is `repository`, `project`, `feature`, or `artifact`.
Visibility is `public` or `private`. For a public registry, every definition
source must resolve inside the public Arcanum repository root.
