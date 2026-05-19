# Invoke Define Transport: Sigilcraft Session Process

## Observer Envelope

- run_id: arcanum-invoke-define-20260519T120954Z
- capability.id: invoke
- capability.kind: spell
- capability.tier: spell
- capability.mode: define
- target_artifact: arcana/sigil-development/development/SIGILCRAFT-SESSION-HANDOFF.md
- request summary: create a development session for the idea that sigil and spell craft are resumable lifecycle processes from idea refinement to execution, with a proposed rename from `sigil-development` to `sigilcraft`.
- expected outputs: sigilcraft session handoff, glossary, implementation-layering seed, define transport report.

## Bounded Define Context

The request is a lifecycle-authoring change, not an immediate runtime rename. The idea is that craft capabilities should behave as processes with continuity: a session can refine an idea, produce governed artifacts, validate them, observe use, reflect on evidence, and hand off bounded execution.

The core distinction is:

- `invoke` is a governed authoring spell that prepares define/design/plan artifacts and handoff context.
- `sigil-development`, proposed as `sigilcraft`, owns sigil lifecycle development.
- `spellcraft` owns spell lifecycle development.
- `task-session` owns bounded execution once the craft process has produced a ready task.

## Template Selection Evidence

- Selected template family: invoke.sigil
- Template path: spells/invoke/templates/sigil/sigil.md
- Eligibility: the target artifact is a sigil lifecycle revision with identity, modes, inputs, outputs, observability, validation expectations, and sigil-development handoff needs.
- Tie cases: the generic template was not selected because this is not an untyped artifact; the spell template was not selected because the primary target is the sigil lifecycle authority, even though Spellcraft should later receive parallel session-language review.
- Candidate status: the sigil template family is invoke-local candidate coverage; lifecycle execution remains with sigil-development until a rename is approved.

## Decisions

- Mode selected: `define`, because the request is an early lifecycle design idea rather than an implementation task.
- Target artifact type: sigil lifecycle revision.
- Current target owner: `sigil-development`.
- Proposed user-facing name: Sigilcraft.
- Proposed canonical id: `sigilcraft`, pending explicit approval.
- Rename policy: no filesystem, registry, adapter, or invoke-contract rename during define.
- Compatibility policy: keep `sigil-development` as an alias or compatibility route if the rename proceeds.
- Process model: craft sessions should expose stage, artifact ledger, decision ledger, open gaps, and next route.
- Boundary decision: `invoke` can prepare handoffs but should not absorb sigilcraft or spellcraft lifecycle execution.
- Spellcraft parity: likely needed, but should be handled through Spellcraft's own lifecycle route after the sigilcraft model is approved.

## Outputs

- Sigilcraft session handoff: arcana/sigil-development/development/SIGILCRAFT-SESSION-HANDOFF.md
- Glossary: arcana/sigil-development/development/SIGILCRAFT-GLOSSARY.md
- Implementation layering seed: arcana/sigil-development/development/SIGILCRAFT-IMPLEMENTATION-LAYERING-SEED.md
- Define transport report: arcana/sigil-development/development/SIGILCRAFT-DEFINE-TRANSPORT.md

## Glossary Linking

- linked: Sigil Development, Spellcraft, Invoke, Task Session, canonical id.
- partial: Sigilcraft, stage, lifecycle authority, artifact ledger, decision ledger, compatibility alias, user-facing name, handoff packet.
- no-match: craft session, session state, rename migration.

Candidate glossary promotion is not automatic and was not performed.

## Governance

- No upstream registry mutation was performed.
- No command adapter mutation was performed.
- No filesystem rename was performed.
- No invoke contract references were changed from `sigil-development` to `sigilcraft`.
- No Spellcraft mutation was performed.
- Sigil-development owns lifecycle execution until the rename decision is approved.

## Unresolved Gaps

- Blocker before implementation: explicit approval is needed to make `sigilcraft` canonical rather than a user-facing alias.
- Non-blocking: exact session stage names may be refined during sigil-development design.
- Non-blocking: Spellcraft should receive parallel session-state language after this model is validated.
- Non-blocking: observability field names for session stage, artifact ledger, and next route need design before runtime adapter work.
- Non-blocking: compatibility policy needs validation with `tools/arcanum --resolve` once adapters are updated.

## Recommended Next Route

sigil-development

Use sigil-development to turn this define pack into a targeted lifecycle update. If the rename is approved, do the migration in layers: contract language first, compatibility surface second, examples third, observability fourth, registry promotion last.
