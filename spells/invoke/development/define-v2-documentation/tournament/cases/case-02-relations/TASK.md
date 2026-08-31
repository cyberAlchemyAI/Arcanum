# Case 02: Two Related Definitions

Author `case-02.json` as an `invoke.define-source.v2` document.

Use source id `DOC-TOURNAMENT-C02`, target id `Definition Bundle Validation`,
and objective `Define the gate and bundle relationship for an atomic candidate output.`
Bind discovery to this case's `evidence.md`.

Create public project registry `invoke.tournament.bundle-validation`, titled
`Bundle Validation Candidate Definitions`, owned by `invoke`, with authority
scope `project:invoke-documentation-tournament`.

Create definition `DOC-T2-GATE`:

- term `definition validation gate`, alias `validation gate`;
- source kind `method-vocabulary`;
- normative voice `A definition validation gate is a bounded check that must pass before a candidate definition bundle can proceed.`;
- formal voice `gate(source) = pass`;
- operational voice `Run the declared source and artifact checks before handing the generated bundle forward.`;
- plain voice `A required check before the bundle can move on.`;
- domain voice `Used by Invoke Define before its candidate bundle is handed to another route.`;
- boundary includes `Source and generated-artifact validation.`;
- excludes `Acceptance or promotion decisions.`;
- condition `The gate evaluates one exact source and its generated bundle.`;
- one normative public heading reference to `Validation Gate` in `evidence.md`;
- consumers `invoke` and `definitions-governance`;
- no relations, warnings, challenge contract, notation, or structural schema;
- candidate promotion boundary owned by `definitions-governance`, drift route
  `invoke`, version `1`.

Create definition `DOC-T2-BUNDLE`:

- term `candidate definition bundle`, alias `definition bundle`;
- source kind `synthesis`;
- normative voice `A candidate definition bundle is the complete atomic output generated from one valid Define source.`;
- formal voice `bundle = compile(valid_source)`;
- operational voice `Inspect DEFINITIONS.json first, derived views second, and the stage receipt last.`;
- plain voice `All files produced together from one valid definition source.`;
- domain voice `Used by Invoke Define as its candidate-only handoff package.`;
- boundary includes `The complete eleven-file atomic output directory.`;
- excludes `Active registry state or downstream execution authority.`;
- condition `Every file comes from the same successful compiler run.`;
- one evidence public heading reference to `Candidate Bundle` in `evidence.md`;
- consumers `invoke` and `task-session`;
- one `depends-on` relation to `DOC-T2-GATE`;
- misuse warning `Do not treat the stage receipt as the definition artifact.`;
- no use-carefully text, challenge contract, notation, or structural schema;
- candidate promotion boundary owned by `definitions-governance`, drift route
  `invoke`, version `1`.

Use one spec declaration `C02-D1`, title `Atomic Bundle`, stating `The bundle is
published only after every declared validation passes.` Use a layering seed
whose decision is `Preserve one atomic source-to-bundle producer boundary.` and
minimum unit is `One source, one compiler run, and one complete bundle.`
Classify Distill as required/pass with evidence `Two related terms are retained
as the smallest coherent semantic graph.` Identity denominator is not
applicable with a defensible rationale. Trace `sequence`, `validation_loop`,
and `owner_boundary_check`. Set the next route to `design`.
