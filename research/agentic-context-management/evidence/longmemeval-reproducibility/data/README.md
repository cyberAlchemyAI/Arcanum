# Append-Only Live Run Data

Status: `empty; live execution not authorized`

## Rules

- One JSONL file owns exactly one run.
- File names must be immutable run IDs: `<run-id>.jsonl`.
- Append records only in protocol order: manifest, question results, summary.
- Never edit or truncate a run after its first row is written.
- Write raw retrieval, answer, and judge artifacts to an immutable sibling
  artifact store and record their references and SHA-256 values in JSONL.
- Never place credentials, secrets, private customer data, or mutable URLs here.
- Synthetic fixtures belong in `../fixtures/`, not this directory.
- A validator pass is integrity evidence, not claim adjudication.

No live or dry-run provider data has been written.
