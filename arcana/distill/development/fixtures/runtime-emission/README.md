# Distill Runtime-Emission Fixtures

The producer compatibility suite intentionally consumes the accepted event
fixtures under:

`arcanum/spells/invoke/development/fixtures/distill-evidence/`

This avoids copying the consumer-owned event grammar into Distill. The focused
runner invokes the Distill emitter for every event, then resolves the resulting
ledger through the existing Invoke consumer.
