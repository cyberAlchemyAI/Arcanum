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
