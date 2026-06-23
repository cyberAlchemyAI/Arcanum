# UX Pattern — `<pattern_id>`

> The reusable distillate of one or more lessons. Pattern-card shape + two consumer-intake blocks.
> Anti-overbuild guard: a `consumer_intake` entry may only assert a check if it names the exact consumer field it feeds.

```yaml
pattern_id:                # kebab id, e.g. detail-beside-the-subject
name:
intent:
problem:
solution:
when_to_use:
anti_pattern:
forces: []
evidence_link:             # lesson_id(s) + evidence refs
status:                    # seed | calibrated | promoted
residue:
consumer_intake:
  validator:
    - claim_class:         # hard_gate | soft_flag | screenshot_review | human_study | not_automatable
      mode:                # ux-evidence-validator mode entered, e.g. spec
      feeds_field:         # the exact validator field/claim this feeds
  studio:
    intent:                # reposition | reword | restructure | ...
    comment_event_template:
      target: { odId: , selector: , elementLabel: }
      severity:            # minor | major | critical
      note:
    mutation_task:
      odId:
      changeType:          # layout-reposition | reword | restructure | ...
```

## Promotion checklist
- [ ] backed by ≥1 `lesson` (no invented patterns)
- [ ] `status` matches evidence (`seed` until cross-session signal)
- [ ] anecdote-only evidence ⇒ no `hard_gate` claim_class
- [ ] every `consumer_intake` entry names a real consumer field
- [ ] stored as a `ux`-tagged architecture-pattern-inventory card (no new store)
