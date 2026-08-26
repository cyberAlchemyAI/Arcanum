# Cross-Skill Validation Matrix

Use this shared evidence fixture for routing scenarios unless a row overrides it:

- object: the three routing skills in this repository;
- consumer: an Arcanum skill maintainer;
- purpose: understand why lenses and explanation resolution have separate
  ownership and how they exchange evidence;
- evidence boundary: the three canonical `SKILL.md` files and their normative
  references, represented with structured whole-resource or bounded line-range
  scopes;
- known terms: skill, router;
- reserved terms: evidence, authority, resolution, lens.

## Behavioral scenarios

| scenario | user-like prompt or mutation | exact assertions |
|---|---|---|
| ordinary explanation | “Explain this routing architecture so a new maintainer understands why it exists.” | `resolution-router` is entry; a valid packet precedes final routing; selected tier is justified; exactly one writer executes |
| direct low invocation | “Use $low-resolution-explanation to explain the architecture.” | writer redirects once with `requested_resolution: low`; router obtains packet; completed writer input does not redirect again |
| supplied valid packet | run `python transmutations/lens-router/scripts/validate_lens_packet.py --emit-valid-fixture > packet.json` from the repository root, then provide `packet.json` | semantic validator passes; lenses are not rerun |
| malformed packet | duplicate rationale, remove one selected-lens finding, or add dangling composition ID | semantic validator returns nonzero at the first or accumulated named violations; no resolution plan is produced |
| out-of-scope evidence | declare `artifact.md` lines 1-10 and cite `artifact.md:999` | packet validator returns nonzero for evidence outside `evidence_boundary`; no plan is produced |
| one lens | “Determine what the evidence licenses us to claim about this candidate.” | only epistemic is selected; one rationale exists; `composed_findings` is empty |
| two lenses | “Explain how evidence authority constrains the next system transition.” | epistemic and systemic views finish independently; composition references both; unmatched material findings receive a disposition |
| three lenses | “Audit evidence, dynamics, and preservation across this cross-layer transformation.” | all three have rationales and findings; every composition record joins different lenses |
| promotion | start with `requested_resolution: low` and a purpose requiring operational comparison | first activating `M*` guarantee is recorded; target becomes medium; because medium is unavailable, no fallback explanation is emitted |
| explicit high | set `requested_resolution: high` for implementation validation | selected tier is never lower than high; unavailable route is reported exactly |
| forged plan | use fake guarantee ID, downgraded tier, or arbitrary writer path | semantic plan validator returns nonzero; writer does not execute |
| replayed or mismatched pair | pair a valid plan with a changed packet, another consumer or purpose, a different boundary, different selected lenses, or incomplete finding allocations | joint handoff validator returns nonzero; writer does not execute |
| manifest drift | copy `routes.md`, mark a missing target available in the copy, then run `validate_resolution_plan.py plan.json --routes <copy>` | validator reports the exact missing path and does not search broadly |
| low writer audit | execute low with a valid packet and plan | every `L01`–`L10` entry has pass/fail plus an explanation locator or excerpt; every material finding ID is included or deferred |
| low review mode | “Review this existing low-resolution explanation and identify its first structural failure.” | returns first excessive-resolution passage, first unearned concept, first failed `L*` guarantee, and smallest repair; does not silently rewrite |

## Required local checks

Run every command from the Arcanum repository root.

1. Run `quick_validate.py` on every skill folder.
2. Parse every JSON schema as Draft 2020-12.
3. Verify `jsonschema` is available, or confirm that both validators return the
   actionable command from their copied `requirements.txt` files.
4. Run:
   - `python transmutations/lens-router/scripts/validate_lens_packet.py --self-test`;
   - `python transmutations/resolution-router/scripts/validate_resolution_plan.py --self-test`;
   - `python transmutations/resolution-router/scripts/validate_routing_handoff.py --self-test`;
   - `python tools/validate-sigil-dependencies.py --selection resolution-router`.
5. Resolve every manifest path and verify that filesystem state matches its
   declared availability.
6. Run strict Arcanum artifact metadata validation over the three canonical
   `SKILL.md` files and their sidecars. Run advisory directory validation over
   the complete packages and require a nonzero checked-file count.
7. Validate a selective install of `resolution-router` and
   `low-resolution-explanation`; each must close over all three routing skills.
8. Record commands and results under `development/validation/`.

Require fresh-agent forward tests with raw artifacts and the user-like prompts
above before registry promotion. Keep medium and high unavailable until their
own writers pass structural, semantic, behavioral, and forward tests.
