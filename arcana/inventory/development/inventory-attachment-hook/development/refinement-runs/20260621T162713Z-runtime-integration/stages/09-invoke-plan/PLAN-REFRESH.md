---
module: inventory-attachment-hook
runId: 20260621T162713Z-runtime-integration
stage: s9-invoke-plan
status: pass
updatedAt: 2026-06-21
docType: plan-refresh
---

# Plan Refresh: Runtime Integration

## Plan Status

`pass` for planning; `flag` for runtime proof.

The design is ready to route to bounded implementation, but runtime readiness
must not be claimed until fixtures prove chat skill closeout.

## Recommended SWUs

| SWU | Goal | Write Scope | Validation |
| --- | --- | --- | --- |
| SWU-IAH-RUNTIME-001 | Add skill-aware Codex observation bridge for explicit `$skill-name` invocation. | observability/OIL canonical docs, Codex hook fixture, targeted generated mirrors after canonical edits | `$skill-name` fixture opens envelope from `.agents/skills/<skill>/SKILL.md`; no `/command` compatibility requirement; `bash -n` hooks; `jq` hook config |
| SWU-IAH-RUNTIME-002 | Add no-native-hook fallback receipt schema and fixture. | observability/OIL docs, generic runtime fixture, optional `.arcanum/runtime` adapter schema notes | dry-run fixture emits fallback receipt and explicit observer status |
| SWU-IAH-RUNTIME-003 | Add Claude Code native receipt acceptance gates. | OIL docs, Claude generated mirror regeneration after canonical edits, stage-worker validation notes | `validate-claude-skills.sh`; receipt transforms into shared closeout |
| SWU-IAH-RUNTIME-004 | Update existing work-pack generated mirror acceptance to include Claude surfaces. | `WORK-PACK.md` through a separate approved edit route | work-pack names `.agents/skills`, `.claude/skills`, and `.claude/agents` acceptance |

## Validation Bundle

Future implementation should include:

```bash
jq empty .codex/hooks.json .arcanum/runtime/config.json
bash -n .codex/hooks/arcanum-user-prompt-submit.sh
bash -n .codex/hooks/arcanum-post-tool-use.sh
bash -n .codex/hooks/arcanum-stop.sh
bash -n arcanum/tools/bootstrap_arcanum.sh
bash arcanum/tools/validate-claude-skills.sh .claude/skills
git -C arcanum diff --check -- arcana/inventory/development/inventory-attachment-hook arcanum/framework/observability arcanum/spells/observed-invocation-loop
```

Fixture cases:

- no policy: skip attachment;
- enabled policy with durable public-safe output: handoff produced;
- private/unsafe output: rejected;
- duplicate idempotency key: deduped;
- Inventory failure: warn by default, block only when required/block policy;
- attachment operation output: recursion guard skips;
- EvidenceSet references evidence-card IDs only;
- generated mirrors refreshed from canonical source.

## Next Route

`task-session` for `SWU-IAH-RUNTIME-001` is the best next move.

Do not start with editor UI. Do not start with broad generated mirror sync. The
first proof is explicit chat `$skill-name` observation.
