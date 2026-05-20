# Generalized Experiment Profile Contract

Status: design contract for profile-aware harness initialization.

## Purpose

An experiment profile is the boundary object between Experiment Harness mechanics and a lifecycle authority such as Spellcraft or Sigil Development.

Experiment Harness owns:

- file layout,
- prompt and regime generation,
- loop execution,
- validation mechanics,
- report and observability mechanics.

The lifecycle authority owns:

- what the artifact must prove,
- which lifecycle modes are meaningful,
- which Quality Bar, Anti-Patterns, and output contract define success,
- whether the evidence supports promotion, hold, or revision.

## Command Surface

Backward-compatible form:

```bash
arcana/experiment-harness/scripts/init-harness.sh <artifact-path> --type spell|sigil
```

Profile-aware form:

```bash
arcana/experiment-harness/scripts/init-harness.sh <artifact-path> --type spell|sigil --profile <profile-id>
```

Inference rules:

| Input | Inferred Profile |
| --- | --- |
| `--type spell` | `generic-spell` |
| `--type sigil` | `generic-sigil` |
| `--type spell --profile spellcraft` | `spellcraft` |
| `--type sigil --profile sigil-development` | `sigil-development` |

Blocking rules:

- unknown profile id blocks initialization,
- `--profile spellcraft` with `--type sigil` blocks,
- `--profile sigil-development` with `--type spell` blocks,
- missing or unreadable target artifact path blocks unless creation is explicitly allowed by the caller,
- existing files are preserved unless an explicit future overwrite mode is added.

## Generated Profile Artifact

Every profile-aware initialization writes:

```text
development/EXPERIMENT-PROFILE.md
```

Minimum shape:

```markdown
# Experiment Profile

- Profile ID: <profile-id>
- Artifact type: spell | sigil
- Lifecycle owner: experiment-harness | spellcraft | sigil-development
- Artifact path: <artifact path>
- Contract path: <artifact path>/SKILL.md or <artifact path>/README.md
- Scenario pack: <scenario-pack-id>
- Required modes: <comma-separated mode ids>
- Prompt set: <comma-separated prompt ids>
- Regime set: <comma-separated regime ids>
- Validation focus: <short list>
- Observability focus: <short list>
- Promotion gate: <human approval | mock loop pass | live loop pass | lifecycle owner review>

## Ownership Boundary

Experiment Harness owns experiment mechanics. The lifecycle owner owns artifact meaning and promotion judgment.
```

## Profile Definitions

### `generic-sigil`

Use when a sigil needs a reusable harness but no lifecycle-specific Sigil Development proof is requested.

Required modes:

- low run,
- medium update/review,
- complex lifecycle validation.

Prompt set:

- `sigil-low`,
- `sigil-medium`,
- `sigil-complex`.

Regime set:

- `LIVE-SIGIL-LOW-001`,
- `LIVE-SIGIL-MEDIUM-001`,
- `LIVE-SIGIL-COMPLEX-001`.

Validation focus:

- target `SKILL.md` exists,
- output uses the target sigil's output contract,
- Quality Bar and Anti-Patterns are observable,
- generated output is not a save summary.

### `sigil-development`

Use when Sigil Development is explicitly testing or maintaining a sigil lifecycle pack.

Required modes:

- new,
- update,
- observe,
- reflect,
- harness-validation.

Prompt set:

- `sigil-new-low`,
- `sigil-update-medium`,
- `sigil-observe-medium`,
- `sigil-reflect-complex`,
- `sigil-harness-validation-complex`.

Regime set:

- `LIVE-SIGIL-NEW-001`,
- `LIVE-SIGIL-UPDATE-001`,
- `LIVE-SIGIL-OBSERVE-001`,
- `LIVE-SIGIL-REFLECT-001`,
- `LIVE-SIGIL-HARNESS-VALIDATION-001`.

Validation focus:

- Sigil Development output contract is represented,
- target sigil contract remains authoritative,
- observer inference is separated from applied edits,
- reflection triggers are named,
- lifecycle recommendation is explicit.

### `generic-spell`

Use when a spell needs a reusable harness but no lifecycle-specific Spellcraft proof is requested.

Required modes:

- low spell design,
- medium spell composition,
- complex lifecycle validation.

Prompt set:

- `spell-low`,
- `spell-medium`,
- `spell-complex`.

Regime set:

- `LIVE-SPELL-LOW-001`,
- `LIVE-SPELL-MEDIUM-001`,
- `LIVE-SPELL-COMPLEX-001`.

Validation focus:

- spell contract exists,
- phase inputs, outputs, gates, and failure policy are visible,
- referenced sigils are named without copying full sigil contracts,
- observability and handoff artifacts are named.

### `spellcraft`

Use when Spellcraft is explicitly testing or maintaining a spell lifecycle pack.

Required modes:

- design,
- install/adapt,
- validate,
- observe/reflect.

Prompt set:

- `spellcraft-design-low`,
- `spellcraft-install-medium`,
- `spellcraft-validate-complex`,
- `spellcraft-reflect-complex`.

Regime set:

- `LIVE-SPELLCRAFT-DESIGN-001`,
- `LIVE-SPELLCRAFT-INSTALL-001`,
- `LIVE-SPELLCRAFT-VALIDATE-001`,
- `LIVE-SPELLCRAFT-REFLECT-001`.

Validation focus:

- Spellcraft output contract is represented,
- aliases resolve to stable canonical ids,
- referenced sigils remain references, not copied processes,
- local adaptation does not rewrite upstream contracts,
- validation produces a clear next action.

## Profile Validation Rules

`validate-harness.sh` should treat profile validation as a structural check before output validation.

Block when:

- `development/EXPERIMENT-PROFILE.md` is missing for a profile-aware harness,
- profile id is unknown,
- artifact type and profile are incompatible,
- lifecycle owner is missing,
- contract path is missing or unreadable,
- prompt set listed in the profile has no matching prompt files,
- regime set listed in the profile has no matching regime files,
- a regime references a missing prompt.

Flag when:

- profile exists but generated prompts do not mention lifecycle owner,
- profile exists but generated regimes do not mention Quality Bar or Anti-Patterns,
- profile exists but no report records profile id or lifecycle owner,
- profile exists but validation is deterministic-only and live evidence is expected for promotion.

Pass when:

- profile metadata is complete,
- prompt and regime sets match generated files,
- regime validation passes,
- target contract can be inspected,
- ownership boundary is explicit,
- reports can carry profile id and lifecycle owner.

## Report Fields

Generalized reports should include:

```text
PROFILE_ID=<profile-id>
LIFECYCLE_OWNER=<owner>
ARTIFACT_TYPE=<spell|sigil>
CONTRACT_PATH=<path>
PROMPT_SET=<ids>
REGIME_SET=<ids>
PROFILE_VALIDATION=pass|flag|block
```

These fields let observability distinguish harness mechanics from lifecycle judgment.

## First Proof Boundary

The first proof should use a sandbox copy of `arcana/concept-layer-optimizer` with the `sigil-development` profile.

Only after the sandbox report is reviewable should the real target be touched, and only with explicit write-scope approval or a clean target worktree.
