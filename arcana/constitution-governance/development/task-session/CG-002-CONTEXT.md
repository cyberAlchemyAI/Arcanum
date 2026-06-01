# Task Session Context: CG-002

## Task

CG-002: Add focused validation fixture for chart line-break rule.

## Controlling Sources

- `arcana/constitution-governance/development/WORK-PACK.md`
- `framework/ARTIFACT-CONSTITUTION.md`
- `tools/validate-artifact-constitution.sh`

## Scope

Allowed:

- update `tools/validate-artifact-constitution.sh`,
- update Artifact Constitution validation instructions,
- synchronize `CG-002` status in the Constitution Governance work-pack,
- write task-session evidence under `arcana/constitution-governance/development/task-session/`.

Out of scope:

- split Artifact Constitution,
- create a separate visual-artifact constitution,
- broaden validator checks beyond chart line-break fixture coverage,
- mutate unrelated validators.

## Gate Check

Proceed with a local validator self-test because the failing fixture cannot be committed as a normal source artifact without making the repository validator fail. The self-test creates temporary passing/failing fixtures and removes them after execution.

## Validation Surface

```bash
bash -n tools/validate-artifact-constitution.sh
tools/validate-artifact-constitution.sh --self-test
tools/validate-artifact-constitution.sh
```
