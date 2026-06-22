# Verification

## Required Checks

Run these checks after creating the candidate contract:

```bash
bash tools/check_markdown_links.sh arcanum/spells/reading-learning-package/README.md
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py arcanum/spells/reading-learning-package/development/reading-learning-package.dispatch.json
git -C arcanum diff --check -- spells/reading-learning-package
```

## Review Evidence

The final report must confirm that `arcanum/spells/reading-learning-package/README.md` contains:

- spell identity and candidate lifecycle status,
- purpose and trigger conditions,
- modes and required inputs,
- outputs and shared state,
- phase contract,
- gates,
- observability signals,
- validation examples,
- registry readiness,
- Spellcraft handoff notes,
- explicit boundaries against runtime implementation, source-authority promotion, and copied sigil bodies.

## Expected Verification Result

- Markdown links: pass.
- Dispatch source validation: `VALIDATION=pass`.
- Diff whitespace: clean.
- Review evidence: all required contract sections present.

If any check fails, repair within the write scope or stop with `BLOCK`.
