# SWU-RCNS-008 Final Active Readiness Audit

## Status

- SWU: `SWU-RCNS-008`
- Date: 2026-06-08
- Result: `pass-with-known-flag`
- Known flag: existing `sigil-new-low.output.md` remains historical blocked example output and does not yet prove a non-blocked native receipt run.

## Completed SWUs

| SWU | Result | Evidence |
| --- | --- | --- |
| `SWU-RCNS-001` | flag | `SWU-RCNS-001-ACTIVE-SURFACE-INVENTORY.md` classified active command-interface dependencies; delegated Noether receipt timed out and was closed. |
| `SWU-RCNS-002` | pass | Refine `SKILL.md`, `README.md`, `REFINEMENT-LOOP.md`, and templates now use native capability/receipt vocabulary. |
| `SWU-RCNS-003` | pass | Refine dispatch template and generator use `g03-native-capability-receipts`; generated dispatch validates. |
| `SWU-RCNS-004` | flag | Refine validation no longer blocks on command resolution; current historical example output still flags as missing native receipt proof. |
| `SWU-RCNS-005` | pass | Invoke active authoring contract no longer uses deprecated command files as readiness evidence; plan SWU result shape includes native receipt fields. |
| `SWU-RCNS-006` | pass | Dispatch schema/validator now enforce native receipt fields, role alignment, stricter subagent strategy, and command-interface proof blocking. |
| `SWU-RCNS-007` | pass | Bootstrap staged installs in `/tmp` do not generate `.codex/commands` by default; generated package text points to native receipts and explicit compatibility boundaries. |

## Active Surface Audit

Remaining active grep hits are classified:

- Refine canonical docs/templates: deprecation boundary text only; no active command-interface success gate.
- Refine validation script/doc: validator patterns intentionally detect and classify stale command-interface wording.
- Invoke canonical docs: native authoring boundary text only.
- Invoke validation doc: command bridges classified as explicit legacy example-runner compatibility.
- Dispatch Spec validator: active command-interface proof is blocked unless route class is explicitly `legacy-compatibility`.
- Bootstrap: deprecated command generation remains behind `--legacy-codex-commands`; default staged installs did not create `.codex/commands`.

## Validation Evidence

Commands used or to be rerun by the parent task-session:

```bash
python3 -m json.tool arcana/refine/templates/refine-dispatch.json
python3 -m json.tool arcana/refine/templates/evidence-index.json
python3 -m json.tool formulae/dispatch-spec/dispatch.schema.json
python3 -m py_compile formulae/dispatch-spec/scripts/validate-dispatch.py
python3 -m py_compile arcana/refine/scripts/generate-refine-dispatch.py
python3 arcana/refine/scripts/generate-refine-dispatch.py --seed arcana/refine/development/fixtures/refine-dispatch-seed.json --output /tmp/refine-commandless-dispatch.json --validate
formulae/dispatch-spec/scripts/validate-dispatch.py /tmp/refine-commandless-dispatch.json
formulae/dispatch-spec/scripts/validate-dispatch.py arcana/refine/development/REFINE-COMMANDLESS-NATIVE-SCHEMA-DISPATCH.json
formulae/dispatch-spec/development/run-validation-fixtures.sh
arcana/refine/development/run-validation-fixtures.sh
bash -n tools/bootstrap_arcanum.sh
```

## Staged Install Evidence

- Repo staged install: `/tmp/rcns-repo-install`
- Personal staged install: `/tmp/rcns-personal-home2`
- Default command surface check: `.codex/commands` absent without `--legacy-codex-commands`.
- Generated skill grep: `refine`, `invoke`, and `orchestrate` packages name native receipts/capabilities and classify command helpers as deprecated compatibility or handoff preparation.

## Remaining Follow-Up

1. Run or refresh a non-blocked Refine live/example output that produces native receipt evidence for every canonical stage.
2. Optionally refresh live installed packages under `$CODEX_HOME` after explicit approval and backup.
3. Preserve historical command-interface evidence as migration history; do not rewrite prior run outputs.
