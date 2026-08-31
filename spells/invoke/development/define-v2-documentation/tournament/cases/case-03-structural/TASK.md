# Case 03: Structural And Identity Evidence

Author `case-03.json` as an `invoke.define-source.v2` document.

Use source id `DOC-TOURNAMENT-C03`, target id `Exact Definition Source
Binding`, and objective `Define a machine-checkable source binding with an
explicit identity denominator.` Bind discovery to this case's `evidence.json`.

Create public artifact registry `invoke.tournament.source-binding`, titled
`Source Binding Candidate Definition`, owned by `invoke`, with authority scope
`artifact:define-source-v2`.

Create exactly one definition:

- id `DOC-T3`, term `definition source binding`, alias `source binding`;
- source kinds `method-vocabulary` and `local-inference`;
- normative voice `A definition source binding is an exact link from a semantic claim to repository bytes and a selector that resolves within those bytes.`;
- formal voice `binding = (path, sha256, size, selector_type, selector)`;
- operational voice `Recompute the digest and size, then prove the selector resolves before accepting the source.`;
- plain voice `A precise pointer from a definition to the evidence it relies on.`;
- domain voice `Used by Invoke Define to make candidate definitions reproducible from public repository evidence.`;
- notation symbol `binding`, meaning `The exact path, digest, size, and selector tuple.`;
- boundary includes `Repository-relative path, exact digest and size, and a resolving selector.`;
- excludes `Remote URLs, guessed evidence values, and promotion authority.`;
- condition `The referenced bytes remain unchanged.`;
- one evidence public JSON-pointer source reference to `/concept/meaning` in
  `evidence.json`;
- one provenance public JSON-pointer source reference to `/title` in
  `concept.schema.json`;
- consumers `invoke` and `validate_definitions_artifact`;
- no relations or use-carefully text;
- misuse warning `A path without current byte evidence is not an exact source binding.`;
- challenge contract modes `evidence` and `scope`, claim or edge `DOC-T3 source evidence`, owner route `invoke`, gate `source_ref_validation`, blocking question `Do the recorded bytes and selector still resolve exactly?`, residue route `invoke:refresh`;
- promotion boundary `Candidate only; validation does not promote the definition.`;
- drift route `invoke:refresh`, version `1`;
- structural schema handle `DOC-T3-SCHEMA`, status `machine-checkable`, ref to
  this case's `concept.schema.json`.

Use declaration `C03-D1`, title `Exact Evidence`, statement `Every normative or
evidence source is bound to current repository bytes.` Use a layering gap and
Distill not required with defensible rationales. Trace `concrete_path_evidence`,
`owner_boundary_check`, and `validation_loop`. Classify identity denominator as
required and bind exact refs to this case's `identity-request.json` and
`identity-result.json`. Set the next route to `sigil-development`.
