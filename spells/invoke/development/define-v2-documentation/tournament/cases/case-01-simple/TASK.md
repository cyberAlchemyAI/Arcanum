# Case 01: One Public Definition

Author `case-01.json` as an `invoke.define-source.v2` document.

Use source id `DOC-TOURNAMENT-C01`, target id `Invoice Review Vocabulary`, and
objective `Define one reviewable candidate term for the invoice-review feature.`
Bind discovery to this case's `evidence.md`.

Create registry `invoke.tournament.invoice-review`, titled `Invoice Review
Candidate Definitions`, owned by `definitions-governance`, with public
visibility and authority scope `feature:invoice-review`.

Create exactly one definition:

- id `DOC-T1`;
- term `reviewable definition draft`;
- alias `definition draft`;
- source kind `domain-vocabulary`;
- five voices:
  - normative: `A reviewable definition draft is proposed meaning bound to exact evidence and available for review without active authority.`
  - formal: `status = candidate`;
  - operational: `Render and inspect the draft, but do not consume it as an active registry definition.`
  - plain language: `A proposed meaning that can be reviewed but is not active.`
  - domain context: `Used by the invoice-review feature while its vocabulary is still being evaluated.`
- no notation;
- boundary includes `Exact-source-bound candidate meaning.`;
- boundary excludes `Promotion, runtime, publication, or deployment authority.`;
- no boundary conditions;
- one normative public source reference to heading `Definition Boundary` in
  `evidence.md`;
- primary consumers `DEFINITIONS.md` and `GLOSSARY.md`;
- no relations;
- no special use warning, misuse warning, or challenge contract;
- promotion boundary `Candidate only; definitions-governance owns promotion.`;
- drift route `definitions-governance`;
- definition version `1`;
- no structural schema.

Use one spec declaration `C01-D1`, title `Candidate Boundary`, stating
`The generated registry remains candidate-only and authority-free.` Use a
layering gap, Distill not required, and identity denominator not applicable,
with defensible rationales. Trace `sequence`, `owner_boundary_check`, and
`concrete_path_evidence`. Set the next route to `deferred`.
