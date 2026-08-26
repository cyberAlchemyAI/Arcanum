# Evidence-Grounded Diagrams Validation Report

- Timestamp: 20260825T225154Z
- Profile ID: sigil-development
- Lifecycle owner: sigil-development
- Artifact type: sigil
- Contract path: transmutations/evidence-grounded-diagrams/SKILL.md
- Canonical byte-set SHA-256: 3d06382f17c29b33f2b26e93cd9de383756aab2ac6fc18ba434fc4fb9e62fff3
- Canonical bytes stable during run: true
- Status: pass
- Quality Bar status: pass
- Anti-Pattern hits: []
- Workflow gaps: []
- Runtime forward evidence: four fresh-agent outputs plus durable normalized fixtures

## Profile Fields

PROFILE_ID=sigil-development
LIFECYCLE_OWNER=sigil-development
ARTIFACT_TYPE=sigil
CONTRACT_PATH=transmutations/evidence-grounded-diagrams/SKILL.md
PROMPT_SET=sigil-new-low, sigil-update-medium, sigil-observe-medium, sigil-reflect-complex, sigil-harness-validation-complex
REGIME_SET=LIVE-SIGIL-NEW-001, LIVE-SIGIL-UPDATE-001, LIVE-SIGIL-OBSERVE-001, LIVE-SIGIL-REFLECT-001, LIVE-SIGIL-HARNESS-VALIDATION-001
PROFILE_VALIDATION=pass

## Failures

- none

## Command Evidence

### runtime preflight

```text
RUNTIME_PREFLIGHT=pass
PYTHON=3.12.2
PyYAML=6.0.1
jsonschema=4.21.1
```
### package closure

```text
SKILL_PACKAGE_VALIDATION=pass
PACKAGE=C:\Users\victo\Arcanum\transmutations\evidence-grounded-diagrams
```
### bundle contract

```text
BUNDLE_CONTRACT_TEST=pass
PROBES=package,valid-draft,duplicate-revision,invalid-tag,broken-reference,stale-digest,false-ready
```
### bundle lifecycle

```text
BUNDLE_LIFECYCLE_TESTS=pass
CASES=valid-draft,index-resolution,lineage,immutable-prior,draft-does-not-supersede,no-overwrite,receipt-consistency,tamper-exclusion,coverage,path-traversal
```
### security contract

```text
SECURITY_CONTRACT_TESTS=pass
CASES=inline-review-request,receipt-exact-coverage,manual-pass-forgery,review-bundle-binding,external-attestation-advisory,evidence-set-binding,index-failure-rollback,crash-orphan-recovery,unmarked-invisible-idempotent-finalize,committed-revision-no-reuse,concurrent-index,concurrent-telemetry
```
### review contract

```text
REVIEW_CONTRACT_TESTS=pass
CASES=request-target-discrimination,revise-bundle-authorization,major-only-fix,conditional-first-blocker,source-digest-binding,bundle-identity-path-binding,exact-member-coverage,unique-roles,manifest-member-digest-binding
```
### persistence boundary

```text
PERSISTENCE_BOUNDARY_TESTS=pass
CONFINEMENT_PROBE=pass (Windows junction)
CASES=promotion-evidence-schema,initial-promotion-rejection,index-rollback,post-rename-quarantine,reparse-confinement
```
### resolver lifecycle security

```text
RESOLVER_LIFECYCLE_SECURITY_TESTS=pass
CASES=draft-does-not-supersede,validated-plus-draft,draft-fallback,validated-requires-pass,member-alias,memberless-discovery,promotion-evidence-verification,forged-published-discovery
```
### inline review receipt

```text
REVIEW_RECEIPT_VALIDATION=pass
RECEIPT=C:\Users\victo\Arcanum\transmutations\evidence-grounded-diagrams\development\fixtures\forward-review-target.receipt.yml
```
### fresh-agent review receipt

```text
REVIEW_RECEIPT_VALIDATION=pass
RECEIPT=C:\Users\victo\Arcanum\transmutations\evidence-grounded-diagrams\development\example-outputs\postfix-review.receipt.yml
```
### inline review stdin

```text
REVIEW_RECEIPT_VALIDATION=pass
RECEIPT=C:\Users\victo\Arcanum\transmutations\evidence-grounded-diagrams\development\fixtures\forward-review-target.receipt.yml
```

## Fresh-Agent Evidence Digests

- `postfix-create.md` `62a4357f2929dbfc08b7d37e7e4df640d137adaf216cc8d80edb5b4d0e37077e` -> `postfix-create.output.md` `ca219f37147920496967882859360a2042d0f75df56ee1686fb53e40b1fa0bb5`
- `postfix-needs-evidence.md` `6b70e3befedffc27c517eb11e42635dd0d36e8e4c0a550531c7f2c112a56287a` -> `postfix-needs-evidence.output.md` `10463857cf86b8c801ed361d802bf8132fae4376bc35039241e359739a087f1d`
- `postfix-review.md` `43ff1588528069de9e367243dc66c1c07991511722df69409804c9c21ca1ba86` -> `postfix-review.output.md` `4633f479a7fcc991dab62d996235f8544da139a65e08c0796bd2de6f3bc6ffa3`
- `postfix-revise.md` `26fe5cb7adeb468cb238f12d2b090f31758da4748f990d30d1bea3cb8d1a30f4` -> `postfix-revise.output.md` `74c5b9b053627b150f1f1c099106a964b2f1a331f8af71d597359573b21f9a84`

Fresh-agent outputs are immutable behavioral snapshots bound to their preserved invocations. The deterministic bundle contract and lifecycle tests reconstruct create/revise persistence in temporary roots on every harness run; ignored live bundle trees are not required for replay.
