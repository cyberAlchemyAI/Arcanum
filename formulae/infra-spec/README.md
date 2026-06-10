# Infra-Spec (CANDIDATE formulae package)

> **Status: CANDIDATE.** Not authoritative; not promotion authority; not yet wired into any pipeline.
> Created by `invoke define` on 2026-06-10 from the validated refine artifacts. See `development/PROVENANCE.md`.

## What this is

`infra-spec` is a governed **infrastructure contract** — an *evidence substrate* that binds a project's operational contract (services, environments, boundaries, secrets, gates) to its runtime evidence (receipts, signals, drift), governing promotion through typed status and typed residue. Runtime evidence never self-promotes.

It is **distinct** from deployment tooling and runtime installers: the package validates infrastructure intent and evidence obligations, but it does not provision resources.

## Why an evidence substrate (not "deployment docs with nicer names")

The package ships the **operational-contract spine** first and keeps runtime evidence additive. Concrete provider bindings and realized infrastructure instances remain outside this candidate.

## Package contents

| File | Role |
| --- | --- |
| `infra-spec.schema.json` / `.yml` | The candidate schema (operational-contract spine). Self-contained Draft 2020-12. |
| `scripts/validate-infra-spec.py` | Two-layer validator: JSON Schema (shape) + 5 governance rules. Output/exit parity with `validate-dispatch.py`. |
| `fixtures/` | 1 `spine-pass` + 9 violation fixtures + `fixtures/README.md` expectation table. |
| `SPEC.md` | The capability define doc (fields, discipline, reuse map, non-negotiables). |
| `development/PROVENANCE.md` | Where this came from + the next-route handoff (invoke → sigil-development). |

## The spine (MVP fields)

`runtime_profile` → `environments[]` → `services[]` (owner, deployment, dependencies, reversal) → `boundaries[]` (kind ∈ network/secret/data_store/tenant/policy/environment) → `state_namespaces[]` + fail-closed `gates[]` + 7-state `promotion_status` + typed `residue[]`. Reuses dispatch-spec `$def` *shapes*; `boundary.kind` redefined for infra; `gate_action` inlined.

## Governance rules (in the validator)

1. **fail-closed gates** — promotion_guardrail gates and secret/data_store boundaries must `block`.
2. **status floor** — `deployed`+ needs a receipt; `validated`+ needs observability/SLO evidence (evidence justifies, never grants).
3. **reversal obligations** — `promoted`/production needs `reversal.rollback`; every data_store needs `reversal.backup`; every `migration.forward` needs a `reverse`.
4. **unowned state** — every data_store maps to a single-owner state_namespace.
5. **analogy labelling** — borrowed-register vocabulary in obligations needs an `analogy_labels` entry (flag).
- (tooling errors surface as `VALIDATION=blocked`, distinct from governance `block`.)

## How to iterate

```bash
# validate a candidate instance
python3 formulae/infra-spec/scripts/validate-infra-spec.py <instance.json>

# run the full fixture matrix (spine-pass -> exit 0, every v-* -> exit 1)
for f in formulae/infra-spec/fixtures/*.json; do
  python3 formulae/infra-spec/scripts/validate-infra-spec.py "$f" >/dev/null 2>&1
  echo "$(basename "$f") exit=$?"
done
```

Iterate by adding fields or axes with a pass-and-violation fixture pair, sharpening governance rules, then piloting against a representative public example. Promotion beyond candidate status requires an explicit Arcanum owner gate.
