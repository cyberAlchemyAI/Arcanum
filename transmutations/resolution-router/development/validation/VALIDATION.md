---
artifact_id: resolution-router.validation.current
artifact_type: validation-report
intent: Record deterministic, installation, and behavioral validation for the routing-skill trio.
owner: resolution-router
lifecycle_status: reviewed
constitution_selectors:
  - framework.artifact-metadata
  - framework.sigil-development
validation_profile:
  - artifact-metadata
  - codex-skill
  - routing-skill
evidence_role: durable-evidence
---

# Validation Record — Routing Skills

Date: 2026-08-25

Scope:

- `transmutations/lens-router/`;
- `transmutations/resolution-router/`;
- `transmutations/low-resolution-explanation/`;
- directly implicated registry, bootstrap, metadata-validator, and sigil-workflow files.

## Deterministic checks

| check | result |
|---|---|
| official `quick_validate.py` on the three canonical skills | PASS |
| official `quick_validate.py` on all three generated Codex packages | PASS |
| `validate-artifact-metadata.py --self-test` | PASS |
| strict artifact metadata validation on the three canonical `SKILL.md` files and sidecars | PASS; `checked: 3` |
| advisory directory metadata validation on the complete trio | PASS; `checked: 23` |
| `validate-sigil-dependencies.py --self-test` | PASS |
| dependency closure for `resolution-router` | PASS: `resolution-router,lens-router,low-resolution-explanation` |
| dependency closure for `low-resolution-explanation` | PASS: `low-resolution-explanation,lens-router,resolution-router` |
| `validate_lens_packet.py --self-test` | PASS, including adversarial mutations |
| `validate_resolution_plan.py --self-test` | PASS, including adversarial mutations |
| both JSON Schemas checked as Draft 2020-12 | PASS |
| missing-`jsonschema` behavior under `python -S` | PASS: exit `3` plus exact `pip install -r` instruction |
| `bash -n tools/bootstrap_arcanum.sh` using Git for Windows Bash | PASS |
| Markdown-link checks on changed governance, registry, skill, and validation documents | PASS |
| public registry metadata extraction from `SKILL.md.artifact.yml` | PASS for all three skills |
| post-promotion selective install with canonical sidecars | PASS |
| repository `.agents/skills` link-stub resolution for all three IDs | PASS |

The earlier package-level metadata PASS was vacuous because directories were
silently skipped. The validator now expands directories, rejects missing or
empty requested paths, reports the checked-file count, and has self-tests for
that behavior. This record supersedes the earlier claim.

## Selective installation

Real bootstrap runs were executed into isolated targets under `C:\tmp`:

- `--sigils resolution-router --profiles repo-codex --spells none`;
- `--sigils low-resolution-explanation --profiles repo-codex --spells none`.

Both runs auto-added the dependency closure, copied both `requirements.txt`
files, generated all three skill packages, and produced packages accepted by
the official Codex skill validator. Generated provenance is now nested under
the allowed `metadata` key instead of invalid top-level frontmatter fields.

## Behavioral validation

See [FORWARD-TESTS-2026-08-25.md](FORWARD-TESTS-2026-08-25.md).

Seven final behavioral scenarios passed with fresh-context agents. The first
ordinary-explanation attempt exposed an excessive low-to-medium promotion. The
routing contract was calibrated by reader action, reinstalled, and retested;
the final attempt selected low and executed the low writer. Direct entry,
one/two/three lenses, promotion, explicit high, unavailable-route stopping, and
low review mode all passed on the final package.

## Environment note

`C:\Windows\System32\bash.exe` still routes to the broken WSL installation.
All Bash syntax, link, and live bootstrap checks used
`C:\Program Files (x86)\Git\bin\bash.exe` successfully.

## Promotion state

- low route: validated and available;
- medium route: unavailable; writer not authored;
- high route: unavailable; writer not authored;
- registry promotion: complete in `registry/SIGILS.md`;
- repository skill surface: complete in `.agents/skills`;
- post-promotion independent review: required; its verdict is external to this
  self-authored validation record.
