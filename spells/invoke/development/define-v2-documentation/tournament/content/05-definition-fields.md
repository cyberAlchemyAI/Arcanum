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
