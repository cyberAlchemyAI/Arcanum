# Review — Unified Skill Model research artifacts

## Coverage

| attacker | lens | targets checked | findings raised | zero-findings defense |
|---|---|---|---:|---|
| definition skeptic | fidelity/governance and definitional correctness | `research.md` and `findings.md`, in full | 4 | Attacked output shape, role separation, raw-return fidelity, RQ coverage, terminology, candidate verdicts, and evidence boundaries. Runtime-type, compatibility, RQ status discipline, and candidates 1/2/4/5 survived. |
| operability skeptic | mechanics/operability and ownership/reference integrity | `research.md` and `findings.md`, in full | 4 | Checked private paths, link resolution, locators, headings, reproducibility, current path-bound consumers, and source-state boundaries. No private path survives in either target; internal cross-links and the current path-bound claims resolve. |

## Findings

| # | artifact and locator | evidence | severity | consequence | proposed fix |
|---|---|---|---|---|---|
| 1 | `findings.md:97` | The artifact says the dispatch “used the stale `.agents/skills/research` adapter and combined synthesis with writing.” The current owner separates a non-persisting synthesizer, a post-convergence writer, and a downstream auditor (`arcana/research/SKILL.md:23-31,35-50,111-114`). | CRITICAL | The report may be honest evidence, but it cannot be represented as a canonically executed and approved research dispatch. | Preserve the drift disclosure and do not mark the dispatch canonically resolved. Treat this review and the user-authorized findings rewrite as corrective artifacts, not retroactive proof that the original topology complied. |
| 2 | `research.md:241-249,266,289,312,381,396`; `findings.md:31,33,69-70,73,84` | The locator prefix `installed-native-skill-creator/` does not exist in the repository. The inspected sources are the installed native files under `$CODEX_HOME/skills/.system/skill-creator/`. | MAJOR | Load-bearing claims about native skill shape and validation cannot be independently retrieved from the published locator as written. | In `findings.md`, use the portable `$CODEX_HOME` locator and record SHA-256 digests. Preserve the raw report but explicitly disclose that its locator was mechanically normalized and is unresolved without that mapping. |
| 3 | `findings.md:9,33,84` | “Several distinct structural schemas” and the broad KILL of “one authoritative skill schema” are supported by representations, parsers, and validators with different scopes. `definitions/DEFINITIONS.md:77-119` defines a schema as an explicit structural representation, while `framework/SCHEMA-CONSTITUTION.md:20-26` excludes implementation code from schema artifacts. | MAJOR | Fragmented enforcement does not prove that no authoritative schema exists; candidate 3 is stronger than its evidence. | Describe the witnessed surfaces as structural representations and validators. Keep the broad schema question unresolved; narrow candidate 3 to the witnessed absence of one composing executable validation/precedence surface. |
| 4 | `research.md:1`; `findings.md:3-13` | The current `arcana/research/SKILL.md:96-114` requires an `Objective` preamble and `Objective → Results → Context`, but the writing contracts it delegates to require no `research.md` preamble and `Goal → TL;DR → Context` (`.claude/skills/custom/domainspec-research-writing.md:16-28`; `.claude/skills/custom/domainspec-findings-writing.md:18-30`). | MAJOR | The same governing route contains incompatible shape requirements, so deterministic format compliance is impossible. | Preserve the writing-contract shape for this artifact and disclose the authority conflict. The `arcana/research` owner must reconcile the contracts before a later run claims canonical format compliance. |
| 5 | `research.md:152,427,461` | One locator is inverted (`24-22`) and two use the unbounded suffix “onward.” | MINOR | These raw-return citations are not precisely reproducible. | Do not silently rewrite the raw return. Identify the imprecision in the findings evidence boundary and avoid relying on those locators for final claims. |

## Artifact verdicts

| artifact | KEEP or FIX | rationale |
|---|---|---|
| `research.md` | FIX | Its evidentiary content remains useful, but native-source aliases and three imprecise locators prevent a clean audit, and prior normalization means it is not literally verbatim. |
| `findings.md` | FIX | It needs portable source locators, a narrower schema conclusion, and explicit process/format boundaries. |

## Change requests

1. Preserve the original dispatch drift and do not claim canonical resolution.
2. Replace unresolved native-source aliases in `findings.md` with portable locators plus source digests.
3. Recast the schema conclusion and candidate verdict at the strength actually supported.
4. Record the conflict between the canonical research owner and its delegated writing contracts.
5. Keep broken or fuzzy raw-return locators non-load-bearing rather than silently rewriting the transcript.

## Evidence boundary

This review covered only `research.md` and `findings.md`, read in full, and consulted named governing artifacts solely to verify literal contradictions and locator resolution. It did not reopen candidate research or claim an exhaustive downstream inventory. The deleted evidence-grounded-diagrams validator remains visible only as historical raw-return evidence; `findings.md` already excludes it from current load-bearing support. No machine-specific private path occurs in either reviewed target.
