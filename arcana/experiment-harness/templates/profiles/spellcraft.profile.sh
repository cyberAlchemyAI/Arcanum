PROFILE_ID="spellcraft"
PROFILE_ARTIFACT_TYPE="spell"
PROFILE_LIFECYCLE_OWNER="spellcraft"
PROFILE_SCENARIO_PACK="spellcraft-lifecycle"
PROFILE_REQUIRED_MODES="design, install/adapt, validate, observe/reflect"
PROFILE_PROMPT_SET="spellcraft-design-low, spellcraft-install-medium, spellcraft-validate-complex, spellcraft-reflect-complex"
PROFILE_REGIME_SET="LIVE-SPELLCRAFT-DESIGN-001, LIVE-SPELLCRAFT-INSTALL-001, LIVE-SPELLCRAFT-VALIDATE-001, LIVE-SPELLCRAFT-REFLECT-001"
PROFILE_VALIDATION_FOCUS="Spellcraft output contract is represented; aliases resolve to stable canonical ids; referenced sigils remain references; local adaptation does not rewrite upstream contracts; validation produces a clear next action"
PROFILE_OBSERVABILITY_FOCUS="spell lifecycle evidence; install/adapt boundary; validation status; reflection recommendation"
PROFILE_PROMOTION_GATE="lifecycle owner review"

PROFILE_PROMPT_IDS=("spellcraft-design-low" "spellcraft-install-medium" "spellcraft-validate-complex" "spellcraft-reflect-complex")
PROFILE_REGIME_IDS=("LIVE-SPELLCRAFT-DESIGN-001" "LIVE-SPELLCRAFT-INSTALL-001" "LIVE-SPELLCRAFT-VALIDATE-001" "LIVE-SPELLCRAFT-REFLECT-001")
PROFILE_PROMPT_REQUESTS=(
	"Use Spellcraft to design a small spell lifecycle change and return the full user-facing result body."
	"Use Spellcraft to review a medium install/adapt scenario and preserve canonical references."
	"Use Spellcraft to validate a complex spell lifecycle pack and report concrete next action."
	"Use Spellcraft to observe or reflect on complex spell evidence and return promote, hold, or revise guidance."
)
PROFILE_REGIME_GOALS=(
	"Validate Spellcraft design behavior."
	"Validate Spellcraft install/adapt behavior."
	"Validate Spellcraft validation behavior."
	"Validate Spellcraft observe/reflect behavior."
)
