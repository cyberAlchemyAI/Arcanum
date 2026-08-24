---
name: intent-route-resolver
description: Resolve a normalized intent against one digest-bound finite route catalog and return a non-authorizing candidate, ambiguity, no-match, or invalid disposition.
argument-hint: "<intent-route.request@1 JSON plus catalog>"
tier: arcana
domain: intent-routing
version: 0.1.0
allowed-tools: Read, Bash
---

# Intent Route Resolver

<objective>
Expose one small deterministic relation before inference and execution:

`intent-route.request@1 + digest-bound catalog -> candidate | ambiguous | no-match | invalid`

The result is advice about possible routing only. It never grants permission,
opens work, binds a workflow, schedules execution, or records effects.
</objective>

<inputs>

- one normalized `intent-route.request@1` value;
- one finite `intent-route.catalog@1` value whose content digest equals the
  request binding;
- an adapter-provided capability token for the local JSON port.
</inputs>

<process>

1. Reject unsupported protocol, core, manifest, or content-digest bindings.
2. Validate request and catalog as closed values.
3. Preserve every discriminator posture: `declared`, `inferred`, or
   `unresolved`; never fill an unresolved value.
4. Evaluate exclusions before requirements.
5. Use only catalog-declared dominance to remove eligible alternatives.
6. Return `ambiguous` when missing information can change eligibility,
   `candidate` only for one non-dominated eligible route, `no-match` without
   fallback, or `invalid` for admitted semantic input failures.
7. Emit one canonical `intent-route.runtime-port@1` response with a complete
   route trace and `authority_effect: none`.
</process>

<authority-boundary>

The resolver has no discovery, repair, ranking, registration, approval,
authorization, persistence, dispatch, scheduling, execution, host-spawn,
network, filesystem-write, or effect authority. A consumer may display the
result, ask the exact clarification, collect a replacement request, or stop.
Any later binding or execution remains owned by the consumer's existing
governed workflow.
</authority-boundary>

<quality-bar>

- all protocol and digest bindings are explicit and fail closed;
- catalog order cannot change canonical response bytes;
- removing evidence cannot improve a disposition;
- every evaluated route appears in the trace;
- transport rejection is never presented as a trusted disposition;
- candidate source and generated closures contain no product-specific imports;
- the manifest declares zero permissions, zero side effects, and no authority.
</quality-bar>

<anti-patterns>

- inferring missing discriminators;
- semantic retry, compatibility fallback, or model escalation;
- treating one candidate as approval;
- creating a route registry or a second decision lifecycle;
- importing a consumer runtime, product model, or private implementation;
- claiming product acceptance from Node or browser portability evidence.
</anti-patterns>

<output-contract>

Return exactly one canonical JSON document matching either
`intent-route.runtime-port@1` or `intent-route.error@1`, with the documented
numeric exit code and zero stderr bytes.
</output-contract>
