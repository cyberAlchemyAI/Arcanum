# Invoke Define v2 Authoring Guide

## What You Author And What Invoke Generates

Invoke Define turns bounded intent plus exact repository evidence into one
candidate definition bundle. You author one `invoke.define-source.v2` JSON
document. The compiler validates it and generates the bundle.

```text
intent + exact repository evidence
                |
                v
       DEFINE-SOURCE-v2.json      <- author this
                |
                v
     Invoke Define v2 compiler
                |
                +--> DEFINITIONS.json            <- machine artifact
                +--> DEFINITIONS.md / GLOSSARY.md <- derived views
                +--> SPEC.md + evidence files
                `--> stage receipt                <- production evidence
```

Do not author `DEFINITIONS.json` or the stage receipt. The generated
`DEFINITIONS.json` is the machine definition artifact. The Markdown files are
deterministic views. The receipt proves only that this producer completed the
declared transformation. Every new registry and definition remains
`candidate`, with `authority_effect: none`; compilation grants no acceptance,
promotion, mutation, publication, deployment, or production authority.

## Five Kinds Of Responsibility

Treat every value according to who owns it.

| Class | What to do | Examples |
| --- | --- | --- |
| Authored | Make a semantic judgment supported by the case evidence. | objective, declarations, terms, five voices, boundaries, consumers, relations |
| Computed | Observe current repository bytes with tools. Never guess or preserve stale values. | repository-relative path, SHA-256, byte size, line bounds, selector |
| Fixed | Copy the active producer contract exactly. | schema/profile ids, candidate status, output names, no-effect transport policy |
| Derived | Omit from the source and let the compiler create it. | `DEFINITIONS.json`, Markdown views, output hashes, producer identity, receipt id/digest, `authority_effect` |
| Prohibited | Never assert it in a new source. | active status, non-empty supersession state, authored receipt metadata, authority effects |

The practical rule is: exercise judgment over meaning, use tools for evidence,
copy constants from the contract, and never impersonate the producer. A JSON
string that looks plausible is still wrong when it should have been computed.

## One Bounded Authoring Pass

1. Read the complete case task and its evidence files.
2. Choose one repository-relative source path for the output JSON.
3. Record target, declaration, registry, and definition semantics from the
   task. Do not add definitions or authority not requested by the evidence.
4. Compute exact discovery, definition-source, structural-schema, and identity
   references from current bytes.
5. Fill the fixed v2 profile, output, candidate-state, and no-effect transport
   constants.
6. Check that every relation target exists in the same source and no term or
   alias collides after case-folding and whitespace normalization.
7. Validate and compile into an output directory that does not already exist.
8. Inspect generated `DEFINITIONS.json` first, the two Markdown views second,
   and the stage receipt last.

For a first-attempt benchmark, stop after authoring the requested source. The
benchmark owner runs compilation exactly once; do not use compiler feedback to
repair the source.

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

## Write One Definition Completely

Every definition rejects unknown properties and requires all of these fields,
including nullable and empty-array fields:

| Field | Rule for a new Define v2 source |
| --- | --- |
| `id` | stable id beginning with a letter; remaining characters letters, digits, `.`, `_`, or `-` |
| `term` | non-blank string; unique across all terms and aliases after Unicode case-folding and whitespace normalization |
| `aliases` | unique string array; may be empty; must not collide with any term or alias |
| `status` | fixed `candidate` |
| `status_detail` | non-empty string or `null` |
| `deferred_as` | fixed `null` |
| `supersedes` | fixed empty array for a new candidate |
| `superseded_by` | fixed `null` |
| `source_kinds` | non-empty unique array from `operator-reading`, `local-inference`, `synthesis`, `method-vocabulary`, `domain-vocabulary`, `historical` |
| `voices` | all five keys: non-blank `normative`, `plain_language`, and `domain_context`; `formal` and `operational` are non-blank strings or `null` |
| `notation` | array of `{symbol,meaning}`; may be empty |
| `boundary` | `{includes,excludes,conditions}` unique string arrays; at least one of the three arrays is non-empty |
| `source_refs` | non-empty exact source-reference array; at least one item has role `normative`, `provenance`, or `evidence` |
| `primary_consumers` | non-empty unique string array |
| `relations` | array of `{id,type}` where the id is another definition in this same source and type is `references`, `depends-on`, or `contrasts-with`; no self or unresolved relation |
| `use_carefully` | non-empty string or `null` |
| `misuse_warning` | non-empty string or `null` |
| `challenge_contract` | complete object described below or `null` |
| `promotion_boundary` | non-empty string or `null`; do not imply that compilation promotes |
| `drift_route` | non-empty string naming the repair owner or route |
| `definition_version` | 1-64 characters; starts alphanumeric; remaining characters alphanumeric, `.`, `_`, `+`, or `-` |
| `structural_schema` | complete object described below or `null` |

The five voices preserve one meaning under different responsibilities:

- `normative`: what the term means;
- `formal`: a stable precise representation, or `null` when unsupported;
- `operational`: how a consumer recognizes or uses it, or `null` when no
  responsible test exists;
- `plain_language`: the same meaning without specialist machinery;
- `domain_context`: where that meaning applies in this case.

If one voice changes the object, status boundary, or permission, repair the
semantic disagreement before compilation.

A challenge contract requires unique `modes` from `contradiction`, `scope`,
`evidence`, and `authority`, plus non-empty `claim_or_edge`, `owner_route`,
`gate`, `blocking_question`, and `residue_route`.

A structural schema is `{handle,status,ref}`. The handle begins alphanumeric
and ends in `-SCHEMA` or `-SCHEMA-<positive integer>`. Status is `documentary`
or `machine-checkable`. A machine-checkable schema requires a non-null
repository-relative `ref`, and that file must parse as a valid Draft 2020-12
JSON Schema.

## Exact Evidence Cookbook

Run evidence commands from the repository root. Record paths relative to that
root, never absolute paths, URLs, or paths containing a `..` segment.

```sh
sha256sum path/to/file
wc -c < path/to/file
nl -ba path/to/file
```

Discovery artifact refs and required identity refs are exactly:

```json
{"path":"path/to/file","sha256":"<64 lowercase hex>","size":123}
```

Definition `source_refs` add semantic location fields:

```json
{
  "role": "evidence",
  "path": "path/to/file",
  "visibility": "public",
  "selector_type": "heading",
  "selector": "Exact Heading",
  "start_line": null,
  "end_line": null,
  "sha256": "<64 lowercase hex>",
  "size": 123
}
```

Roles are `normative`, `provenance`, `evidence`, or `example`. A normative,
provenance, or evidence ref requires current SHA-256 and size. An example ref
may use `null` for those two fields, but exact bindings are preferable.

Selector rules:

| `selector_type` | `selector` | line fields |
| --- | --- | --- |
| `heading` | exact Markdown heading text or slug-equivalent text | both `null` |
| `anchor` | Markdown heading slug, with or without leading `#` | both `null` |
| `line-span` | descriptive non-empty label | integer `start_line <= end_line`, within file |
| `json-pointer` | RFC 6901 pointer beginning `/`, such as `/concept/meaning` | both `null` |
| `yaml-path` | dotted path with optional zero-based indexes, such as `groups[0].id` | both `null` |
| `symbol` | exact text that occurs in the file | both `null` |

The selector resolves inside the whole referenced file; SHA-256 and size also
describe the whole file, not only the selected passage. Recompute both whenever
the file changes.

## Complete Compilable Example

This example binds the public file
`arcanum/spells/invoke/development/define-v2-documentation/tournament/shared/example-evidence.md`.
Its current SHA-256 is `5660f590b332ca0450b64cd1bbadd6f826f0c64cfa37223571087773ac39b63b` and its size is
`253` bytes.

```json
{
  "schema_version": "invoke.define-source.v2",
  "source_id": "DOC-GUIDE-EXAMPLE-001",
  "target": {
    "id": "Candidate Artifact Vocabulary",
    "objective": "Define one exact-source-bound candidate artifact term."
  },
  "discovery": {
    "kind": "artifact",
    "ref": {
      "path": "arcanum/spells/invoke/development/define-v2-documentation/tournament/shared/example-evidence.md",
      "sha256": "5660f590b332ca0450b64cd1bbadd6f826f0c64cfa37223571087773ac39b63b",
      "size": 253
    }
  },
  "template_selection": {
    "profile_id": "invoke.generic-definitions-baseline.v2",
    "selected": "invoke.generic-definitions-baseline.v2",
    "eligible": ["invoke.generic-definitions-baseline.v2"],
    "tie": false
  },
  "spec_declarations": [
    {
      "id": "EX-D1",
      "title": "Candidate Boundary",
      "statement": "The generated definition remains candidate-only."
    }
  ],
  "definition_registry": {
    "registry_id": "invoke.guide.example",
    "title": "Guide Example Candidate Definition",
    "owner_route": "definitions-governance",
    "authority_scope": {"kind": "artifact", "ref": "guide-example"},
    "visibility": "public",
    "definitions": [
      {
        "id": "DOC-EX1",
        "term": "bounded candidate artifact",
        "aliases": ["candidate artifact"],
        "status": "candidate",
        "status_detail": null,
        "deferred_as": null,
        "supersedes": [],
        "superseded_by": null,
        "source_kinds": ["domain-vocabulary"],
        "voices": {
          "normative": "A bounded candidate artifact records proposed meaning for review without active authority.",
          "formal": "status = candidate",
          "operational": "Permit inspection while blocking active-policy consumption.",
          "plain_language": "A proposed artifact that can be reviewed but is not active.",
          "domain_context": "Used by the Invoke guide as an exact-source-bound public example."
        },
        "notation": [],
        "boundary": {
          "includes": ["Proposed meaning available for review."],
          "excludes": ["Active policy or promotion authority."],
          "conditions": []
        },
        "source_refs": [
          {
            "role": "normative",
            "path": "arcanum/spells/invoke/development/define-v2-documentation/tournament/shared/example-evidence.md",
            "visibility": "public",
            "selector_type": "heading",
            "selector": "Candidate Artifact",
            "start_line": null,
            "end_line": null,
            "sha256": "5660f590b332ca0450b64cd1bbadd6f826f0c64cfa37223571087773ac39b63b",
            "size": 253
          }
        ],
        "primary_consumers": ["DEFINITIONS.md", "GLOSSARY.md"],
        "relations": [],
        "use_carefully": null,
        "misuse_warning": null,
        "challenge_contract": null,
        "promotion_boundary": "Candidate only; definitions-governance owns promotion.",
        "drift_route": "definitions-governance",
        "definition_version": "1",
        "structural_schema": null
      }
    ]
  },
  "layering": {
    "kind": "gap",
    "rationale": "Downstream planning owns implementation layering for this example."
  },
  "dispatch_trace": {
    "techniques": ["sequence", "owner_boundary_check", "concrete_path_evidence"]
  },
  "distill": {
    "classification": "not-required",
    "rationale": "The example contains one bounded definition unit."
  },
  "identity_denominator": {
    "classification": "not-applicable",
    "rationale": "No separate canonical identity denominator is asserted."
  },
  "output_contracts": {
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
  },
  "transport_policy": {
    "append_existing_only": true,
    "upstream_mutation": false,
    "targets": []
  },
  "next_route": "deferred"
}
```

## Diagnose The First Real Failure

| Failure | Repair owner |
| --- | --- |
| source schema invalid | repair the authored shape, fixed constant, missing nullable field, or enum |
| exact ref is stale | recompute SHA-256 and byte size from the intended current file |
| selector does not resolve | choose a selector type and value that resolves in the referenced bytes |
| public source is outside public root | use public evidence inside Arcanum or make the registry private when the contract permits it |
| term or alias collision | choose non-colliding semantic identities after normalization |
| unresolved or self relation | point only to another definition id in the same source |
| layering output mismatch | pair `seed` with `IMPLEMENTATION-LAYERING.md` and `gap` with `LAYERING-GAP.md` |
| identity result is not pass | stop; the required identity denominator is not satisfied |
| structural schema invalid | repair the referenced Draft 2020-12 schema or classify the structural schema honestly |
| generated view drift | discard the output directory and rerun the compiler from the source; never hand-edit a generated view |

The compiler publishes atomically: schema, evidence, selector, semantic graph,
identity, or late view failures leave the requested output directory absent.
Do not reinterpret an absent bundle or a `BLOCK` message as a partial pass.

## Validate, Compile, And Read The Result

From the repository root, choose an output directory that does not exist:

```sh
python3 arcanum/spells/invoke/scripts/compile_define_source_v2.py \
  path/to/DEFINE-SOURCE-v2.json \
  --output-dir path/to/absent-output \
  --repo-root .
```

A successful run exits zero, creates exactly eleven files, and emits a v2
stage receipt whose `result` is `pass` and `authority_effect` is `none`. Inspect
`DEFINITIONS.json` and verify the registry and every definition remain
`candidate`. Then inspect `DEFINITIONS.md` and `GLOSSARY.md` as derived views.
Read `INVOKE-DEFINE-STAGE-RECEIPT.json` last as production evidence.

The pass proves that the installed producer accepted the exact source and
created a schema-valid, semantically checked, internally consistent candidate
bundle. It does not prove that a definition is true, accepted, active,
promoted, published, deployed, or ready for runtime mutation. Any of those
claims belongs to another explicit owner and gate.
