# Iteration And Stop

Run stages sequentially:

1. Execute `002`; verify and write its result.
2. Execute `003`; verify and write its result.
3. Execute `004`; verify and write its result.
4. Check prerequisite result files for `002`, `003`, and `004`.
5. Execute `005` only if the prerequisite result files exist.

Stop with `BLOCK` if:

- any stage cannot be verified from local evidence;
- a required stage result file cannot be produced;
- write scope must expand to continue;
- live experiments would be required;
- `005` prerequisites are absent after attempting `002-004`.

If a stage blocks, report the exact blocker and do not continue to later stages
that depend on it.
