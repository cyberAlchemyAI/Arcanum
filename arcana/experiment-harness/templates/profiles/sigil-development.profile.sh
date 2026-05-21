PROFILE_ID="sigil-development"
PROFILE_ARTIFACT_TYPE="sigil"
PROFILE_LIFECYCLE_OWNER="sigil-development"
PROFILE_SCENARIO_PACK="sigil-development-lifecycle"
PROFILE_REQUIRED_MODES="new, update, observe, reflect, harness-validation"
PROFILE_PROMPT_SET="sigil-new-low, sigil-update-medium, sigil-observe-medium, sigil-reflect-complex, sigil-harness-validation-complex"
PROFILE_REGIME_SET="LIVE-SIGIL-NEW-001, LIVE-SIGIL-UPDATE-001, LIVE-SIGIL-OBSERVE-001, LIVE-SIGIL-REFLECT-001, LIVE-SIGIL-HARNESS-VALIDATION-001"
PROFILE_VALIDATION_FOCUS="Sigil Development output contract is represented; target sigil contract remains authoritative; observer inference is separated from applied edits; reflection triggers are named; lifecycle recommendation is explicit"
PROFILE_OBSERVABILITY_FOCUS="lifecycle owner judgment; observer evidence; reflection trigger; promotion or revision recommendation"
PROFILE_PROMOTION_GATE="lifecycle owner review"

PROFILE_PROMPT_IDS=("sigil-new-low" "sigil-update-medium" "sigil-observe-medium" "sigil-reflect-complex" "sigil-harness-validation-complex")
PROFILE_REGIME_IDS=("LIVE-SIGIL-NEW-001" "LIVE-SIGIL-UPDATE-001" "LIVE-SIGIL-OBSERVE-001" "LIVE-SIGIL-REFLECT-001" "LIVE-SIGIL-HARNESS-VALIDATION-001")
PROFILE_PROMPT_REQUESTS=(
	"Use Sigil Development to review whether the target sigil can accept a small new capability change."
	"Use Sigil Development to plan or review a medium update to the target sigil without rewriting its contract silently."
	"Use Sigil Development to inspect observability evidence for the target sigil and separate inference from applied edits."
	"Use Sigil Development to reflect on a complex lifecycle signal and return a promotion, hold, or revision recommendation."
	"Use Sigil Development to validate the target sigil's experiment harness and report whether the evidence is usable."
)
PROFILE_REGIME_GOALS=(
	"Validate Sigil Development new-sigil lifecycle reasoning."
	"Validate Sigil Development update lifecycle reasoning."
	"Validate Sigil Development observability review behavior."
	"Validate Sigil Development reflection behavior."
	"Validate Sigil Development experiment-harness review behavior."
)
