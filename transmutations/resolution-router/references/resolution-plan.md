# Resolution Plan Contract

`resolution_plan` records the router's decision. It travels to the writer beside
the complete `lens_packet`; it never replaces or embeds that packet.

The writer input is exactly:

```text
{
  lens_packet,
  resolution_plan
}
```

## Required fields

- `plan_version`: `2.0`.
- `packet_digest`: exact copy of the validated `lens_packet.packet_digest`.
- `requested_resolution`: `low`, `medium`, `high`, or `null`.
- `selected_resolution`: `low`, `medium`, or `high`.
- `reason`: why this is the lowest sufficient tier.
- `guarantee_ids`: every guarantee inherited by the selected tier.
- `promotion`: `null` or a record containing `from`, `to`,
  `activating_guarantee_id`, and `reason`.
- `lens_specific_allocation`: exactly one record per selected packet lens,
  containing `lens`, `emphasis`, every individual `finding_id` owned by that
  lens, and the guarantee IDs activated by that allocation.
- `composed_finding_ids`: every composed finding ID in the packet, or an empty
  list when the packet has no compositions.
- `target_writer`: record containing `skill_id`, `path`, and `status`.

## Validity rules

- `guarantee_ids` must exactly cover the selected tier's cumulative guarantees.
- Every activating guarantee ID must occur in `guarantee_ids`.
- Allocation may change emphasis but may not hide a material packet finding.
- `packet_digest` must match the supplied packet. This binds consumer, purpose,
  selected lenses, evidence boundary, vocabulary constraints, findings,
  composition, audit, and uncertainty without duplicating them in the plan.
- Allocation lenses must exactly equal the packet's selected lenses. Each
  individual finding must occur once, in the allocation for its own lens, and
  `composed_finding_ids` must exactly cover packet composition IDs.
- A requested resolution may be promoted but never silently downgraded.
- `promotion` must be `null` when no requested baseline exists or when selected
  equals requested. Otherwise `from` equals the requested tier, `to` equals the
  selected tier, and the activating guarantee belongs to the selected tier's
  additions (`M*` for medium or `H*` for high).
- Target ID, path, and status must match `routes.md`.
- An unavailable target forbids writer execution and fallback generation.
- The writer must receive the unchanged valid `lens_packet` with this plan.

`resolution-plan.schema.json` validates structure only. It cannot enforce exact
guarantee sets, tier ordering, promotion consistency, packet identity,
allocation membership, composition coverage, or manifest identity by itself.

Run `../scripts/validate_resolution_plan.py` for every plan exchanged with a
writer. A plan is valid only when both structural and semantic validation pass.
Before writer execution, also run
`../scripts/validate_routing_handoff.py <packet.json> <plan.json>`. This joint
gate is mandatory: separate packet and plan passes do not prove that the pair
belongs together. A plan copied beside a changed or different valid packet is
invalid, even when consumer-facing strings happen to match.
