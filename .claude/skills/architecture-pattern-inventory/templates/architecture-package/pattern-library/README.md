# Pattern Library

Use this library as a selective context source during implementation.

- Load only the concept files required for the current task.
- Pair concept files with relationship cards from `../ARCHITECTURE-PATTERN-LIBRARY.md`.
- Keep examples aligned with architecture foundations, dependency rules, testing alignment, and observability alignment.

## Architecture References

- [architecture-foundations](ARCHITECTURE-FOUNDATIONS.md)
- [dependency-rules](DEPENDENCY-RULES.md)
- [testing-alignment](TESTING-ALIGNMENT.md)
- [observability-alignment](OBSERVABILITY-ALIGNMENT.md)

## Inventories

- [concepts](concepts/README.md)
- [relationships](relationships/README.md)
- [inventory](inventory/README.md)

## Selection Recipe

1. Start from the task intent.
2. Open only the concept files needed by that intent.
3. Open only the relationship cards connecting those concepts.
4. Apply dependency, testing, and observability obligations from the relevant alignment documents.
