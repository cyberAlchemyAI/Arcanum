# Stage 09: Invoke Plan

Status: `pass`

## Non-Executed Plan

### Phase 1: Define Package

Create development artifacts only:

- `development/user-guide/USER-GUIDE-DEFINE.md`
- `development/user-guide/USER-LEDGER-SCHEMA.yml`
- `development/user-guide/GUIDE-RECEIPT-SCHEMA.yml`
- `development/user-guide/USER-GUIDE-GLOSSARY.md`
- `development/user-guide/VALIDATION-FIXTURES.md`

### Phase 2: Validate Fixtures

Use a fixture corpus before any runtime:

| Fixture | Expected Result |
| --- | --- |
| Sales to architecture | Valid bridge receipt with mapping limits. |
| Software to science | Valid bridge receipt plus target definition. |
| Music to construction | Valid bridge receipt plus mismatch warning. |
| Clarified but not mastered | Concept state becomes `clarified`. |
| Teach-back and transfer | Concept state may become `mastered`. |
| Failed analogy | Residue row and preference update proposal. |

### Phase 3: Candidate Sigil Development

Run `sigil-development` only after Phase 1 and 2 are reviewed:

- `user-ledger`
- `guide-section-receipt`
- `guide-bridge-selector`
- `guide-concept-ladder`
- `user-mastery-glossary`

### Phase 4: Candidate Spellcraft

Run `spellcraft` only after candidate sigils have stable contracts:

- `cyberalchemy-install-game`
- `guide-clarify-blocker`
- `guide-domain-bridge`
- `guide-master-definition`
- `guide-generalize`

### Phase 5: Runtime Prototype

Implement only the smallest local prototype:

```text
one concept library seed
one install-game transcript fixture
one user ledger fixture
one guide receipt fixture
one validation report
```

## Stop Conditions

- Stop if user data would be stored without explicit visibility rules.
- Stop if canonical registries would be mutated before candidate validation.
- Stop if Guide starts claiming mastery without active evidence.
- Stop if concept libraries become universal authority rather than local teaching aids.
