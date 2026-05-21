PROFILE_ID="generic-spell"
PROFILE_ARTIFACT_TYPE="spell"
PROFILE_LIFECYCLE_OWNER="experiment-harness"
PROFILE_SCENARIO_PACK="generic-spell-lifecycle"
PROFILE_REQUIRED_MODES="low spell design, medium spell composition, complex lifecycle validation"
PROFILE_PROMPT_SET="spell-low, spell-medium, spell-complex"
PROFILE_REGIME_SET="LIVE-SPELL-LOW-001, LIVE-SPELL-MEDIUM-001, LIVE-SPELL-COMPLEX-001"
PROFILE_VALIDATION_FOCUS="spell contract exists; phase inputs, outputs, gates, and failure policy are visible; referenced sigils are named without copied contracts; observability and handoff artifacts are named"
PROFILE_OBSERVABILITY_FOCUS="phase evidence; gate status; workflow gaps; handoff clarity"
PROFILE_PROMOTION_GATE="lifecycle owner review"

PROFILE_PROMPT_IDS=("spell-low" "spell-medium" "spell-complex")
PROFILE_REGIME_IDS=("LIVE-SPELL-LOW-001" "LIVE-SPELL-MEDIUM-001" "LIVE-SPELL-COMPLEX-001")
PROFILE_PROMPT_REQUESTS=(
	"Run the target spell on a small spell-design request and return the full user-facing result body."
	"Run the target spell on a medium composition request and show phase inputs, outputs, gates, and next action."
	"Run the target spell on a complex lifecycle validation request and return risks, gates, observability, and handoff evidence."
)
PROFILE_REGIME_GOALS=(
	"Validate low-complexity target spell behavior against its contract."
	"Validate medium target spell composition behavior against its contract."
	"Validate complex target spell lifecycle behavior against its contract."
)
