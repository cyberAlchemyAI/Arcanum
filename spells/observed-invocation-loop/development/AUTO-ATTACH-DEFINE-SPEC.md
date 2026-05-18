# Define Spec: OIL Automatic Runtime Attachment

## Identity

- Capability: Observed Invocation Loop automatic runtime attachment
- Parent spell: `observed-invocation-loop`
- Capability kind: spell extension
- Date: 2026-05-18
- Status: defined

## User Need

Arcanum should not depend on an agent remembering to emit telemetry after a sigil, spell, or skill is invoked. When an Arcanum capability is installed into a runtime command surface, its adapter should automatically include the Observed Invocation Loop closeout path.

The user specifically wants this to work for any sigil and asked whether Codex commands should be added and attached to every command. The answer is: Codex commands are one runtime target, but the attachment source of truth should be the Arcanum runtime installer and adapter templates. Each runtime command surface should receive generated observed closeout from the same contract.

## Problem Statement

OIL currently has a generic observer, reflection runner, and pilot evidence for one skill, one sigil, and one spell. That proves the pipeline. It does not yet guarantee that every generated adapter gets the same hook-first closeout.

The remaining gap is adapter propagation:

- existing generated adapters still vary in how observability is described,
- new runtime adapters can be created without the OIL closeout block,
- Codex command adapters are planned by `sigil-runtime-installer`, but this repo does not currently have generated `.codex/commands/` files,
- manual updates across every adapter are brittle and will drift.

## Goals

1. Make OIL attachment automatic for generated Arcanum runtime adapters.
2. Support all capability kinds: `skill`, `sigil`, and `spell`.
3. Support runtime targets through the installer contract: GitHub Copilot first, Codex and Claude through command adapter plans or generated commands when conventions are confirmed.
4. Provide an idempotent refresh path that can update all installed adapters without clobbering unrelated local edits.
5. Validate that every managed adapter either contains or points to the observed invocation closeout contract.
6. Preserve the primary capability result and make telemetry closeout deterministic.

## Non-Goals

- Do not make Codex-specific command files the canonical source of OIL behavior.
- Do not edit every external consumer repository in this wave.
- Do not claim native agent hooks outside Arcanum-managed adapter surfaces.
- Do not make reflection mutate sigils or spells automatically.
- Do not replace `experiment-harness`; it remains a producer that delegates to generic observation.

## Required Inputs

| Input | Required | Source |
| --- | --- | --- |
| runtime target | yes | `sigil-runtime-installer` invocation |
| capability id | yes | registry or selected command |
| capability kind | yes | registry classification |
| adapter path | yes | runtime target convention |
| observability dir | yes when strict | `.arcanum/observability` |
| OIL contract ref | yes | `.arcanum/runtimes/<runtime>/OBSERVED-INVOCATION.md` or generated block |

## Required Outputs

| Output | Description |
| --- | --- |
| observed adapter template | reusable closeout section for generated adapters |
| attachment manifest | inventory of generated adapters and OIL status |
| adapter refresh command | idempotent install or refresh operation |
| validation report | pass, flag, or block for every adapter |
| Codex command plan | generated or planned `.codex/commands/` bridge strategy |

## Acceptance Criteria

| Criterion | Status Rule |
| --- | --- |
| Every new generated adapter has OIL closeout. | pass when installer template emits it by default |
| Existing adapters can be refreshed safely. | pass when refresh is idempotent and detects local conflicts |
| Sigil coverage is complete for installed sigil adapters. | pass when every `arcanum-sigil-*` adapter is listed in the attachment manifest |
| Codex commands have a defined path. | pass when `.arcanum/runtimes/codex/commands/` and `.codex/commands/` are generated or explicitly planned with validation |
| Telemetry remains hook-first. | pass when generated adapters call or point to `observe-invocation.sh` closeout, not a manual reminder |

## Invoke Result

- Mode: define
- Spell: invoke
- Phase status: pass
- Canonical parent: `observed-invocation-loop`
- Complexity: medium
- Next route: design
