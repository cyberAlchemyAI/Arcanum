# Three-Voice Definition Audit Report

Date: 2026-06-19

## Scope

- Canonical source: [../../../../definitions/DEFINITIONS.md](../../../../definitions/DEFINITIONS.md)
- Lookup index: [../../../../definitions/DEFINITIONS-INDEX.md](../../../../definitions/DEFINITIONS-INDEX.md)
- Drift audit: [../../../../definitions/DEFINITION-DRIFT-AUDIT.md](../../../../definitions/DEFINITION-DRIFT-AUDIT.md)
- Controlling contract: [../../SKILL.md](../../SKILL.md)

## Result

| Check | Result | Evidence |
| --- | --- | --- |
| Definitions audited | pass | 11 indexed definitions checked. |
| Scientific/formal voice | pass | All indexed definitions include `Scientific/Formal Voice`. |
| Plain-language voice | pass | All indexed definitions include `Plain-Language Voice`. |
| Domain-context voice | pass | All indexed definitions include `Domain Context`. |
| Stable IDs and anchors | pass | Definition heading IDs remained unchanged. |
| Index synced | pass | Governance notes mention the three-voice requirement. |
| Downstream drift remediation | deferred | Existing downstream remediation targets remain outside L0. |

## Definitions Covered

- `DEF-ARC-CONTRACT`
- `DEF-ARC-SCHEMA`
- `DS-D1`
- `DS-D2`
- `DS-D3`
- `DS-D7`
- `DS-D8`
- `DS-D10`
- `DS-P1`
- `DS-P2`
- `DS-P3`

## Domain Context Surface

The Arcanum-local domain-context voice is grounded in:

- `development/user-guide/README.md` for reader-facing explanation and guide boundaries,
- `definitions/TAXONOMY.md` for DomainSpec meta-type examples,
- `definitions/RELATIONSHIPS.md` for DomainSpec relationship examples,
- existing definitions-governance authority boundaries for non-promoted local vocabulary.

## Validation Evidence

| Command | Result |
| --- | --- |
| `perl ... arcanum/definitions/DEFINITIONS.md` voice-completeness check | pass: `PASS definitions=11 voices=3` |
| `bash tools/check_markdown_links.sh definitions/DEFINITIONS.md --check-anchors` | pass |
| `bash tools/check_markdown_links.sh definitions/DEFINITIONS-INDEX.md --check-anchors` | pass |
| `git -C arcanum diff --check` | pass |

## Follow-Up

- L1 should review downstream consumer artifacts listed in
  `definitions/DEFINITION-DRIFT-AUDIT.md` for references to the canonical
  definitions.
- L2 can add a small reusable structure check if this audit pattern repeats.
