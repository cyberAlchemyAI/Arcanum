# Stages

Command-backed stage artifacts were not created because the run blocked before stage execution.

Blocked reason:

- `tools/arcanum --resolve dispatch-spec` fails.
- `tools/arcanum --resolve runtime-handoff` fails.

The canonical Refine loop requires dispatch validation and runtime handoff readiness before command-backed stage execution.
