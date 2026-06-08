# Iteration And Stop Policy

Work in small iterations:

1. inspect existing tool/script conventions;
2. create schema;
3. create validator;
4. create passing and failing fixtures;
5. run validation;
6. record result and update work-pack status only for this SWU.

Stop with `BLOCK` if:

- required fields cannot be decided from the context pack and local evidence;
- a validator dependency is unavailable and no lightweight fallback is practical;
- completing validation requires live experiment execution;
- write scope must expand beyond the declared boundaries;
- the schema would need to copy MARS project-specific fields unchanged.

Do not continue into `SWU-MOGT-HARNESS-002` unless explicitly asked after this
unit is verified.
