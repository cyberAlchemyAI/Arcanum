## Validate, Compile, And Read The Result

From the repository root, choose an output directory that does not exist:

```sh
python3 arcanum/spells/invoke/scripts/compile_define_source_v2.py \
  path/to/DEFINE-SOURCE-v2.json \
  --output-dir path/to/absent-output \
  --repo-root .
```

A successful run exits zero, creates exactly eleven files, and emits a v2
stage receipt whose `result` is `pass` and `authority_effect` is `none`. Inspect
`DEFINITIONS.json` and verify the registry and every definition remain
`candidate`. Then inspect `DEFINITIONS.md` and `GLOSSARY.md` as derived views.
Read `INVOKE-DEFINE-STAGE-RECEIPT.json` last as production evidence.

The pass proves that the installed producer accepted the exact source and
created a schema-valid, semantically checked, internally consistent candidate
bundle. It does not prove that a definition is true, accepted, active,
promoted, published, deployed, or ready for runtime mutation. Any of those
claims belongs to another explicit owner and gate.
