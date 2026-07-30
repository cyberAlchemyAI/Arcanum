# Validation Experiment

- Artifact: arcanum/formulae/html-preview-server
- Artifact type: sigil
- Runtime: Codex CLI
- Harness owner: experiment-harness

## Goal

Validate that HTML Preview Server remains a deterministic Formulae sigil across:

- a low-complexity direct open of one standalone HTML file;
- medium lifecycle behavior covering reuse, status, explicit-root/port conflicts,
  relative assets, sanitized recent/online/offline listing, and cleanup;
- complex containment, concurrency, encoded-path, stale-state, observability, and
  proof-boundary review, including capped offline history and malformed-record
  isolation.

## Evidence Required

- Fixture inputs and expected outputs.
- Real example prompts.
- Deterministic lifecycle-helper output from
  `development/test-html-preview-server.mjs`.
- One browser-navigation receipt through an available shared runtime.
- Real native skill outputs after generated runtime installation.
- Timestamped validation reports under `development/runs/`.

## Promotion Gate

This artifact is not promotion-ready until deterministic validation passes,
expected outputs are inspectable, the generated runtime mirror matches canonical
source, at least one browser-navigation receipt exists, and repeated meaningful
executions produce observability evidence. A single local pass establishes
candidate usability, not broad runtime portability.
