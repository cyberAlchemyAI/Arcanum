# Invoke Define v3 Authoring Guide

This is the execution guide for agents and operators authoring Define v3
inputs. For a version-neutral introduction to what Define does and why, start
with the [human overview](./define/README.md).

## The Job In One Sentence

Define v3 turns an independently checked semantic context into one exact,
candidate-only definition bundle, then admits that bundle only when a clean
compiler replay proves that its meaning, authority, topology, and projections
are still current.

The author is responsible for meaning. The semantic assessor is responsible
for closure. The compiler is responsible for deterministic construction. The
admission validator is responsible for point-in-time replay and drift
classification. None of them may silently assume another role.

```text
intent and repository evidence
             |
             v
 DEFINE-SEMANTIC-CONTEXT.json        authored semantic surface
             |
             v
 independent semantic closure       assessed dispositions and topology
             |
             v
 DEFINE-SOURCE.json                  authored v3 applications
             |
             v
 compiler -> 13-file bundle          deterministic candidate
             |
             v
 bundle admission receipt            independent current-state proof
             |
             v
 capability resolution               stage + admission, or BLOCK
```

The normative shape authorities are:

- [semantic context v1](./schemas/define-semantic-context-v1.schema.json),
  retained for historical declared-probe evidence
- [semantic context v2](./schemas/define-semantic-context-v2.schema.json),
  required for new intent-coverage claims
- [semantic closure receipt v1](./schemas/define-semantic-closure-receipt-v1.schema.json)
- [semantic closure receipt v2](./schemas/define-semantic-closure-receipt-v2.schema.json)
- [Define source v3](./schemas/define-source-v3.schema.json)
- [Definitions v2 artifact](./schemas/definitions-v2.schema.json)
- [Define stage receipt v3](./schemas/define-result-v3.schema.json)
- [bundle admission receipt v1](./schemas/define-bundle-admission-receipt-v1.schema.json)
- [bundle admission receipt v2](./schemas/define-bundle-admission-receipt-v2.schema.json)

If this guide and a schema disagree, the schema wins. Compiler checks add
cross-field semantic invariants that JSON Schema cannot express.

## Use The Stateless CLI

The CLI does not write JSON from prose. Give it one complete authoring-request
document whose `document` contains the meaning-bearing values and whose
`evidence_paths` map JSON Pointers to repository-relative whole files. The CLI
rehashes those files, inserts fixed contract fields, derives the top-level
artifact ID, validates the resulting source, and exclusively creates one
absent output.

The request schemas are
[semantic-context authoring](./schemas/define-semantic-context-authoring-request-v1.schema.json)
and [Define-source authoring](./schemas/define-source-v3-authoring-request-v1.schema.json).
Do not put `$schema`, `schema_version`, `context_id`, `source_id`, profile
constants, `authority_effect`, SHA-256 values, byte sizes, producer fields, or
receipt fields inside `document`; those values are fixed, derived, or
forbidden. An evidence binding has this authoring-only shape:

```json
{"pointer":"/upstream_bindings/semantic_context_ref","path":"path/to/DEFINE-SEMANTIC-CONTEXT.json"}
```

Inspect and validate before writing:

```sh
tools/arcanum invoke define describe semantic-context
tools/arcanum invoke define check semantic-context \
  --request path/to/context-authoring-request.json \
  --repo-root .

tools/arcanum invoke define author semantic-context \
  --request path/to/context-authoring-request.json \
  --repo-root . \
  --output path/to/absent/DEFINE-SEMANTIC-CONTEXT.json
```

Use the same `check` then `author` sequence for the `source` stage. Authoring
does not replace the independent semantic-closure or admission stages.

## The Eight-Step Authoring Path

1. Inventory semantic intent before choosing probes: assess the subject,
   parts, relationships, evidence states, validation and gates, execution
   handoff, and authority boundary. Bind every obligation to exact evidence.
2. Author the semantic context: bound the target, authority surface,
   registry roots, consumer roots, evidence sources, obligations, and concept
   probes. Every probe must name the obligations it serves.
3. Obtain independent semantic closure: the assessor must be different from
   the context author and must inspect the configured roots completely.
4. Resolve every concept disposition: each probe must be exactly
   `reuse-existing`, `new-scoped-term`, or `specialize-existing`; a conflict or
   canonical-change proposal stops Define.
5. Author the v3 source: apply every closure result exactly once through a
   candidate definition, an authority binding, or both.
6. Compile into an absent output directory: the producer either publishes all
   thirteen files atomically or leaves the requested directory absent.
7. Run bundle admission: an independent validator replays the exact source and
   closure, compares every byte, validates every consumer, and classifies all
   discovered drift.
8. Submit both receipts: a new intent-covered artifact requires the matching
   v3 stage receipt and a current v2 admission PASS. A v1 closure or admission
   remains historical declared-probe evidence and cannot establish intent
   coverage.

That order is mandatory. A plausible source is not a substitute for closure;
a successful compile is not a substitute for admission; admission is not
promotion or runtime authority.

## Know Who Owns Every Value

| Class | What to do | Examples |
| --- | --- | --- |
| Authored | Make one evidence-backed semantic judgment. | target intent, declarations, voices, boundaries, relations, applications, rationale |
| Observed | Read current repository bytes; never guess. | path, SHA-256, byte size, selector, registry and consumer membership |
| Fixed | Copy the active v3 contract exactly. | schema/profile IDs, output filenames, candidate status, `authority_effect: none` |
| Derived | Omit and let the producer or validator calculate it. | `DEFINITIONS.json`, Markdown views, producer hash, inventories, receipt IDs/digests, drift summary |
| Forbidden | Never claim it in authoring input. | active/canonical status for a candidate, promotion, release, runtime readiness, semantic equivalence from counts or paths |

An exact hash proves byte identity only. It does not prove equivalent meaning
after a change. A changed meaning-bearing field, authority binding, topology,
schema, or identity denominator must take its declared reassessment route.

## Author Semantic Context Before Definitions

The context is the machine-readable answer to: “What existing meaning must
this work respect, and which semantic obligations did we decide must be
represented?” A v2 context declares:

- one bounded `target` with objective, authority scope, and visibility;
- one discovery artifact or an honest discovery waiver;
- an `intent_coverage` denominator whose exact evidence sources, seven facet
  assessments, and typed concept, relationship, and boundary obligations
  define the bounded completeness claim;
- separate `semantic_disposition` and `authority_disposition` values for every
  evidence source;
- a `discovery_contract` with independent `registry_roots` and
  `consumer_roots`; consumer enumeration comes from configured globs, not from
  searching only for already-selected probe labels;
- ordered `concept_probes` with exact evidence, requested terms and aliases,
  intended scope, proposed disposition, obligation IDs, and any claimed
  canonical match;
- the canonical `authority_boundary`, including source, index, resolution
  evidence, owner, and scope;
- every adjacent registry and current consumer in the configured roots;
- exact, evidenced exclusions when a discovered file is not a live consumer;
- different `authored_by` and `assessed_by` owners; and
- fixed `authority_effect: none`.

Its v2 top-level field set is `$schema`, `schema_version`, `context_id`,
`authored_by`, `assessed_by`, `target`, `discovery`, `discovery_contract`,
`intent_coverage`, `concept_probes`, `authority_boundary`, `adjacent_registries`,
`consumer_boundary`, `exclusions`, and `authority_effect`. Unknown fields are
rejected.

### Inventory intent before probes

For each target, assess these facets exactly once: `subject`, `parts`,
`relationships`, `evidence-state`, `validation-gates`, `execution-handoff`,
and `authority-boundary`. A facet is either `represented`, with one or more
obligation IDs, or `not-applicable`, with exact evidence and rationale.
`unassessed` is a schema-valid fail-closed state for authoring and test
fixtures; semantic closure blocks it.

Every semantic obligation is a `concept`, `relationship`, or `boundary`.
Covered obligations map to one or more probes. Relationship obligations name
the subject probe, relation type, and object probe. Boundary obligations name
the probe, boundary field, and required text. Out-of-scope obligations require
evidence and rationale. An uncovered obligation or an orphan probe blocks
closure.

### Apply a semantic quotient before selecting probes

An intent inventory is not a glossary dump. Before selecting probes, reduce
the observed vocabulary to the smallest set of independently testable domain
meanings that still covers every assessed facet. This reduction is a semantic
quotient: it removes duplicate and implementation-level labels without merging
meanings that have different relations, boundaries, validation behavior, or
consumers.

Use these tests in order:

1. **Removal test:** if removing a candidate meaning would leave no way to
   state a required facet, relation, boundary, or gate, retain it.
2. **Independence test:** if two labels always share the same evidence,
   relations, boundary, and validation behavior, model one meaning and retain
   the other as an alias or explanatory detail. If any of those differ, keep
   them separate.
3. **Part test:** keep a named part first-class when it participates in its own
   containment, ordering, ownership, validation, or handoff relation. Do not
   collapse several independently governed parts into one umbrella term.
4. **Control-vocabulary test:** schema fields, status labels, filenames,
   validators, routes, techniques, and downstream lifecycle actors are not
   automatically domain concepts. Put them in evidence, facets, boundaries,
   or consumer topology unless the target objective treats them as an
   independently testable meaning.
5. **Target-label test:** the target name is not automatically a definition.
   Define it only when downstream semantics require the subject itself, rather
   than merely its parts and invariants.
6. **Authority-reference test:** an authority binding is for an externally
   owned semantic input. A target-owned evidence limit, fairness rule, stop
   condition, or authority-preservation invariant remains a local obligation;
   it does not become external merely because it constrains authority.
7. **Domain-role test:** a retained concept should be the required subject, a
   named structural part with its own relationship, a cross-cutting validity
   invariant that distinguishes pass from block, or an execution or authority
   boundary. Evidence inputs, presentation modes, output fields, return
   mechanics, and control states support those meanings; they are not separate
   concepts unless the target gives them an independent domain role.

After quotienting, every retained concept or binding has exactly one probe,
every probe maps at least one independently enumerated obligation, and every
relationship or boundary obligation names retained endpoints. A smaller model
that merges independently testable meanings is incomplete; a larger model of
incidental vocabulary creates orphan probes and is also incomplete.

Historical evidence is not one discard decision. Use
`semantic_disposition: retain-and-reassess` when its domain concepts remain
relevant even though its old executable form is obsolete. Set
`authority_disposition` independently to `historical-only` or `none`. Exclude
historical meaning only with an exact source-backed rationale. This prevents
discarding an obsolete Plan format from silently discarding Work Pack, layer,
wave, task, SWU, validation, gate, or execution-entry concepts embodied by it.

Do not author a closure receipt. Run the independent closure validator. A
ready receipt must say `outcome: ready-for-define` and `next_route: define-v3`,
bind the installed validator and both schemas, contain no blockers, and equal a
fresh replay byte for byte.

### The three dispositions

| Closure disposition | v3 source shape | Meaning |
| --- | --- | --- |
| `reuse-existing` | no candidate definition; exactly one `reuse` authority binding | Refer to canonical authority without copying or redefining it. |
| `new-scoped-term` | exactly one candidate definition; no authority binding | Introduce one new meaning inside the target scope. |
| `specialize-existing` | exactly one candidate definition plus one `specialization-basis` binding | Narrow an existing canonical meaning; never broaden or replace it. |

Every probe appears once in `semantic_applications`, in source order. Its
`disposition` and `rationale` must equal the closure result exactly. Every
candidate definition and authority binding is owned by exactly one
application. Each application contains only `probe_id`, `disposition`,
`definition_ids`, `authority_binding_ids`, and `rationale`.

## Fill The v3 Source

The top-level source rejects unknown fields and requires all of these:

| Field | Authoring rule |
| --- | --- |
| `$schema` | fixed `https://arcanum.dev/schemas/invoke/define-source/v3` |
| `schema_version` | fixed `invoke.define-source.v3` |
| `source_id` | stable 3-128 character identifier |
| `profile_id` | fixed `invoke.generic-definitions-baseline.v3` |
| `upstream_bindings` | exact `semantic_context_ref` and `semantic_closure_receipt_ref` |
| `template_selection` | `profile_id` and `selected` fixed to v3; `eligible` contains v3; `tie` is `false` |
| `spec_declarations` | one or more `{id,title,statement}` durable rules |
| `definition_registry` | target-owned candidate definitions plus canonical authority bindings |
| `semantic_applications` | total, ordered projection of every closure disposition |
| `layering` | `seed` with `decision` and `minimum_unit`, or `gap` with rationale |
| `dispatch_trace` | one or more unique technique IDs actually used |
| `distill` | required passing evidence, or `not-required` with rationale |
| `identity_denominator` | required exact request/result refs, or `not-applicable` with rationale |
| `output_contracts` | all thirteen fixed filenames; layering filename follows its branch |
| `transport_policy` | fixed append-existing-only, no upstream mutation, no targets |
| `next_route` | `design`, `spellcraft`, `sigil-development`, or `deferred` |
| `authority_effect` | fixed `none` |

The registry requires `registry_id`, `title`, `owner_route`,
`authority_scope`, `visibility`, `definitions`, and `authority_bindings`. At
least one of the final two arrays is non-empty. `visibility` is `public` or
`private`; a public registry may consume only public definition and authority
sources.

### Candidate definitions

Each candidate definition includes every field below, including explicit nulls
and empty arrays:

| Field | Allowed value or decision |
| --- | --- |
| `id` | stable candidate ID, unique in this registry |
| `term` | non-blank label matching its concept probe |
| `aliases` | unique labels matching the probe; no normalized collision |
| `status` | fixed `candidate` |
| `status_detail` | non-empty detail or `null` |
| `deferred_as` | fixed `null` |
| `supersedes` | fixed empty array |
| `superseded_by` | fixed `null` |
| `source_kinds` | one or more of `operator-reading`, `local-inference`, `synthesis`, `method-vocabulary`, `domain-vocabulary`, `historical` |
| `voices` | aligned `normative`, `formal`, `operational`, `plain_language`, and `domain_context` voices |
| `notation` | zero or more `{symbol,meaning}` entries |
| `boundary` | `includes`, `excludes`, and `conditions`; at least one is non-empty |
| `source_refs` | exact context-probe evidence projected without adding undeclared ranges |
| `primary_consumers` | one or more named real consumers |
| `relations` | local candidate IDs with `references`, `depends-on`, or `contrasts-with` |
| `use_carefully` | guidance or `null` |
| `misuse_warning` | warning or `null` |
| `challenge_contract` | complete challenge object or `null` |
| `promotion_boundary` | later promotion owner or `null`; never imply automatic promotion |
| `drift_route` | responsible repair owner or route |
| `definition_version` | stable candidate version |
| `structural_schema` | `{handle,status,ref}` or `null` |

The five voices explain one meaning from different positions. `normative` says
what the term means. `formal` gives a justified precise representation or is
`null`. `operational` says how a consumer recognizes the meaning or is
`null`. `plain_language` makes the same meaning easy to retell.
`domain_context` says where it applies. A disagreement about object, boundary,
status, permission, or owner is semantic drift, not stylistic variation.

A `challenge_contract` names one or more modes from `contradiction`, `scope`,
`evidence`, and `authority`, plus `claim_or_edge`, `owner_route`, `gate`,
`blocking_question`, and `residue_route`.

A `structural_schema` may be `documentary` or `machine-checkable`. The latter
must use a valid `*-SCHEMA` handle and a repository-relative `ref` to valid
Draft 2020-12 JSON Schema. Admission exact-binds those schema bytes.
A later valid schema change still requires semantic reassessment; validity does
not prove equivalent structure.

### Authority bindings are references, not copied definitions

An authority binding contains `binding_id`, `probe_id`, `role`, canonical
`definition_id`, `term`, `authority_scope`, `authority_status`, and an exact
`authority_ref`. Its ID, term, scope, selector, and source bytes must equal the
single canonical match in the closure.

Never put copied canonical normative prose into a candidate to make reuse look
self-contained. The generated view points readers back to the authority source.

## Bind Exact Evidence

Run evidence commands from the repository root:

```sh
sha256sum path/to/file
wc -c < path/to/file
nl -ba path/to/file
```

An exact reference is:

```json
{"path":"path/to/file","sha256":"<64 lowercase hex>","size":123}
```

Semantic source refs additionally carry `format`, `selector_type`, `selector`,
and `visibility`. Candidate definition refs carry `role`, `selector_type`,
`selector`, optional line bounds, and visibility. Available selector types are
`heading`, `anchor`, `line-span`, `json-pointer`, `yaml-path`, and `symbol`.
Roles are `normative`, `provenance`, `evidence`, or `example`.

The digest and size always describe the whole file. The selector identifies
the relevant material inside it. Recompute the whole-file binding after any
byte change; never repair a stale ref by changing only its hash while ignoring
the semantic change.

## Compile And Admit

From the repository root, the committed mixed example runs as follows:

```sh
define_v3_run="$(mktemp -d arcanum/spells/invoke/development/.define-v3-guide.XXXXXX)"

tools/arcanum invoke define produce semantic-closure \
  --context arcanum/spells/invoke/examples/define-v3/DEFINE-SEMANTIC-CONTEXT.json \
  --repo-root . \
  --discovery-root arcanum/spells/invoke/examples/define-v3 \
  --public-root arcanum \
  --output "$define_v3_run/closure.json"

cmp "$define_v3_run/closure.json" \
  arcanum/spells/invoke/examples/define-v3/DEFINE-SEMANTIC-CLOSURE-RECEIPT.json

tools/arcanum invoke define produce bundle \
  --source arcanum/spells/invoke/examples/define-v3/DEFINE-SOURCE.json \
  --repo-root . \
  --discovery-root arcanum/spells/invoke/examples/define-v3 \
  --public-root arcanum \
  --output "$define_v3_run/bundle"

tools/arcanum invoke define admit admission \
  --repo-root . \
  --bundle "$define_v3_run/bundle" \
  --output "$define_v3_run/admission.json"
```

The output directory must be absent before compilation. The admission output
must also be absent and must sit outside the submitted bundle. For comparison
with an earlier point in time, add `--prior-admission
path/to/prior-admission.json`.

A successful compile creates exactly thirteen regular files: semantic context,
semantic closure, spec, `DEFINITIONS.json`, two deterministic Markdown views,
layering seed or gap, template selection, dispatch trace, Distill result,
identity-denominator result, transport report, and the v3 stage receipt.

A successful admission exits zero and records:

- `result: pass` and `authority_effect: none`;
- exact agreement with the v3 producer receipt and all thirteen files;
- the submitted bundle digest and the fixed thirteen-check admission inventory;
- a byte-identical clean replay;
- current semantic context and closure;
- valid `DEFINITIONS.json`, views, structural schemas, and semantic outcome;
- live structural-schema bytes equal to their compile-time stage bindings;
- `evidence_state: current`;
- unchanged semantic, authority, topology, and projection states; and
- `overall: current` with no blockers or differences.

An evaluated inadmissible bundle exits one and still writes its typed BLOCK
receipt with every reachable blocker. An invocation failure exits two and
writes no receipt.

## Understand Drift Before Repairing It

Semantic drift is a change, or unresolved uncertainty, that affects meaning,
ownership, authority scope, applicability, relationships, structural contract,
identity denominator, registry/consumer topology, or consumer obligations.

| Observation | Classification | Required route |
| --- | --- | --- |
| submitted and clean bytes equal | current for that exact material | continue |
| only a deterministic view differs while `DEFINITIONS.json` is unchanged | projection drift | recompile |
| source bytes changed without a stored machine projection | semantic review required | rerun semantic closure |
| label, voice, boundary, relation, or application changed | semantic change | reauthor source after reassessment |
| authority owner, kind, scope, source, or index changed | authority change | Definitions Governance |
| registry or consumer membership changed | topology change | rerun closure and reassess semantics |
| structural schema changed but remains valid | structural semantic review | reauthor or reaffirm source |
| identity-denominator material changed | identity review | identity-denominator validator |
| file added, removed, or substituted | bundle inventory drift | recompile or stop |

Stable counts, filenames, or prose assertions never prove semantic equivalence.
Any non-current semantic, authority, or topology state blocks admission.

## Use The Mixed Example As Shape Evidence

The committed example deliberately exercises all three dispositions:

- [semantic context](./examples/define-v3/DEFINE-SEMANTIC-CONTEXT.json)
- [independent closure](./examples/define-v3/DEFINE-SEMANTIC-CLOSURE-RECEIPT.json)
- [v3 source](./examples/define-v3/DEFINE-SOURCE.json)
- [discovery evidence](./examples/define-v3/discovery.md)
- [canonical example authority](./examples/define-v3/definitions/DEFINITIONS.md)
- [consumer](./examples/define-v3/consumer/SPEC.md)

Copy fixed contract shape only. Do not copy its target semantics, paths,
digests, sizes, selectors, owner claims, or dispositions into another project.

## Retell-Chain Check

Before submitting a source, a reader should be able to retell the chain without
opening the schemas:

1. “The context inventories the bounded semantic obligations and every current
   registry and consumer.”
2. “Historical evidence separates retained meaning from discarded authority.”
3. “A different owner assessed every facet, obligation, and concept.”
4. “The source applies each resolution exactly once without stealing canonical
   authority.”
5. “The compiler materialized every covered concept, relationship, and
   boundary into a complete candidate bundle from those exact bytes.”
6. “Admission replayed the work and found no semantic, authority, topology, or
   projection drift.”

If any sentence is false or uncertain, stop at that boundary. Do not compress
the uncertainty into a generic PASS.

## Claim Ceiling

A v3 stage receipt proves deterministic production of one candidate bundle. A
current v2 admission PASS additionally proves that every independently
enumerated semantic obligation was mapped and materialized at one exact point
in time. It does not prove that an open-ended human intent had no omitted
obligation. Together they may open only the `artifact_authored` axis.

They do not make a definition true, canonical, active, accepted, released,
published, deployed, or mutation-runtime ready. Later consumers must bind the
admission receipt and independently rehash the live material they intend to
use.
