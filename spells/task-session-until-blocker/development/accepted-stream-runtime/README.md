# Accepted Stream Runtime Validation

Generic fixtures only. The direct validation surface is:

```text
python3 scripts/validate_accepted_stream_transition.py --validate-swu SWU-MVLR-007
python3 scripts/validate_accepted_stream_completion.py --validate-swu SWU-MVLR-008
python3 scripts/rehearse_accepted_stream.py --validate-swu SWU-MVLR-009
```

The rehearsal executes the real deterministic driver twice over fourteen generic units with no effects and zero retries.
