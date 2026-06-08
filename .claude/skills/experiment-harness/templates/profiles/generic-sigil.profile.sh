PROFILE_ID="generic-sigil"
PROFILE_ARTIFACT_TYPE="sigil"
PROFILE_LIFECYCLE_OWNER="experiment-harness"
PROFILE_SCENARIO_PACK="generic-sigil-lifecycle"
PROFILE_REQUIRED_MODES="low run, medium update/review, complex lifecycle validation"
PROFILE_PROMPT_SET="sigil-low, sigil-medium, sigil-complex"
PROFILE_REGIME_SET="LIVE-SIGIL-LOW-001, LIVE-SIGIL-MEDIUM-001, LIVE-SIGIL-COMPLEX-001"
PROFILE_VALIDATION_FOCUS="target SKILL.md exists; output uses target sigil output contract; Quality Bar and Anti-Patterns are observable; output is not a save summary"
PROFILE_OBSERVABILITY_FOCUS="quality bar status; anti-pattern hits; workflow gaps; reflection trigger recommendation"
PROFILE_PROMOTION_GATE="lifecycle owner review"

PROFILE_PROMPT_IDS=("sigil-low" "sigil-medium" "sigil-complex")
PROFILE_REGIME_IDS=("LIVE-SIGIL-LOW-001" "LIVE-SIGIL-MEDIUM-001" "LIVE-SIGIL-COMPLEX-001")
PROFILE_PROMPT_REQUESTS=(
	"Run the target sigil on a small focused request and return the full user-facing result body."
	"Run the target sigil on a medium update or review request and expose decisions, validation, and follow-up."
	"Run the target sigil on a complex lifecycle validation request and return risks, gates, and next action."
)
PROFILE_REGIME_GOALS=(
	"Validate low-complexity target sigil execution against its contract."
	"Validate medium target sigil update or review behavior against its contract."
	"Validate complex target sigil lifecycle behavior against its contract."
)
