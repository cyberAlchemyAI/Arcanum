# Validation Experiment — Work Pack Readiness Audit

## Command

```bash
bash development/run-validation-fixtures.sh
```

Run from `arcanum/spells/work-pack-readiness-audit`.

## Expected Result

- nine tests pass;
- no network access occurs;
- no configured target command executes;
- all writes remain inside temporary fixture directories;
- the public spell contains no consuming-project vocabulary or path.

## Additional Static Checks

```bash
python3 -m json.tool schemas/audit-config.schema.json >/dev/null
python3 -m json.tool schemas/audit-report.schema.json >/dev/null
python3 -m json.tool schemas/refresh-signal-pack.schema.json >/dev/null
python3 -m py_compile scripts/audit_work_pack.py development/test_work_pack_readiness.py
git diff --check -- spells/work-pack-readiness-audit registry/SPELLS.md
```

Public/private leakage is checked with a caller-supplied denylist before
registry admission. Generated runtime mirrors must be reproduced from the
canonical README and compared byte-for-byte below their generated frontmatter.
