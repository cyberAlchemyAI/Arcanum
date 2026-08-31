# INV-DEFINE-GLOSSARY-001

## Scenario

A candidate definition contains a new local term that must not be silently
promoted.

## User Request

Define an experiment session notebook for Mars geology analysis. The notebook introduces a local term, "sol-thread", for observations grouped by Martian day and analyst discussion.

## Inputs

- Mode: `define`
- Core goal: present
- Scope hints: present
- Existing artifacts: absent
- Template inventory: present
- Candidate-template permission: not needed
- Necronomicon concept sources: available
- New candidate definition term: sol-thread

## Expected Result

- Phase status: `pass`
- Template selection: `invoke.generic-definitions-baseline.v3`
- Outputs: spec artifact, `DEFINITIONS.json`, `DEFINITIONS.md`, `GLOSSARY.md`, and define transport report
- Definition status: `sol-thread` remains candidate with exact source evidence and a promotion boundary
- Implementation layering: seed emitted or gap recorded
- Expected next route: `deferred`

## Expected Output

[INV-DEFINE-GLOSSARY-001.expected.md](INV-DEFINE-GLOSSARY-001.expected.md)
