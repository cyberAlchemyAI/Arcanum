# Expected Output: INV-QUALITY-ANTI-PATTERN-001

## Invoke Validation Fixture Result

- Fixture: INV-QUALITY-ANTI-PATTERN-001
- Status: pass
- User request: validate Quality Bar and Anti-Pattern evidence in the invoke experiment loop
- Mode contract: arcanum/spells/invoke/define.md and arcanum/spells/invoke/design.md
- Next route: experiment-harness observe

## Expected Classifications

```text
QUALITY_BAR_STATUS=pass
QUALITY_BAR_STATUS=partial
QUALITY_BAR_STATUS=fail
ANTI_PATTERN_HITS_JSON=["save-summary output instead of artifact body","candidate definition promoted by Define","generated glossary treated as authority","design proceeds without approved define outputs","deferred plan/full behavior emitted from design"]
WORKFLOW_GAPS_JSON=[{"category":"quality-bar","severity":"medium","summary":"usable output has unresolved non-blocker gaps","evidence":"fixture"},{"category":"anti-pattern","severity":"severe","summary":"design treats missing contracts as approved","evidence":"fixture"}]
```

## Telemetry Expectations

- Observer telemetry includes `quality_bar_status`.
- Observer telemetry includes `anti_pattern_hits`.
- Observer telemetry includes `workflow_gaps`.
- Observer telemetry includes `reflection_trigger`.
