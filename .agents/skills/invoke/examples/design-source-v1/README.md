# Design Source v1 Executable Example

The current success example is executable rather than a static copied JSON
bundle. `development/test_compile_design_candidate.py` creates a real Define v2
PASS bundle, compiles the normal W1 five-file family, authors a digest-current
`DESIGN-SOURCE.json`, and compiles the atomic W2 candidate.

A checked-in static PASS source would contain run-specific paths, sizes, and
SHA-256 bindings and would become false evidence as soon as any upstream byte
changed. Use the fixture builder in that test as the canonical example and run
it through the real compiler. The same suite includes governed failure cases
and proves that their success directories remain absent.

This example proves only the W2 candidate boundary described in
`design-source-authoring-guide.md`; it is not a final Design stage receipt or a
Plan handoff.
