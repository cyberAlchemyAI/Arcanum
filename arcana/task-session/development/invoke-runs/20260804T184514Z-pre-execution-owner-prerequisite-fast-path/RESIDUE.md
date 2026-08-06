# Residue and Blindspots

## Open but non-blocking for package authoring

1. **Zero-extra-prompt policy.** Current authority rules do not let a bare Task Session invocation authorize `invoke:refresh:apply-approved`. The implementation should support exact carried authorization from the caller or outer composition. Making that implicit requires a separate, explicit authority decision.
2. **Plan-once adoption default.** The route is implemented and validated but remains opt-in. This package recommends it for new just-in-time-material plans; making it the global default needs compatibility evidence.
3. **Multiple prerequisites.** More than one dependent owner hop belongs to an outer-loop spell. The fast path intentionally supports only one hop.
4. **No-op semantics.** An Invoke no-op satisfies a prerequisite only when the declared satisfaction predicate proves the required state already exists.
5. **Same-attempt resume.** The implementation must distinguish returning control to a suspended phase from recursively invoking a new Task Session.
6. **Observability cost.** Minimal route evidence must be emitted, but full observability enrichment belongs after classification so it does not recreate the delay.
7. **Dirty canonical surfaces.** Task Session, Invoke, and readiness sources already contain pending work. Lifecycle execution must bind baselines and coordinate or stop on overlap.
8. **Wall-clock variability.** A five-second local SLO is useful telemetry but not a portable correctness gate.

## Blockers before implementation dispatch

- exact user authorization for the proposed cross-capability dispatch;
- current target inventory/baselines for each selected SWU;
- lifecycle-owner acceptance of the carried-authorization representation for `SWU-PEP-004` and `SWU-PEP-005`.
