PROFILE_ID="invoke-live"
PROFILE_ARTIFACT_TYPE="spell"
PROFILE_LIFECYCLE_OWNER="invoke"
PROFILE_SCENARIO_PACK="invoke-live-promotion"
PROFILE_REQUIRED_MODES="define, design, define-design, observability"
PROFILE_PROMPT_SET="invoke-define-live-pass, invoke-design-live-pass, invoke-define-design-live-pass, invoke-define-live-pass"
PROFILE_REGIME_SET="LIVE-DEFINE-001, LIVE-DESIGN-001, LIVE-DEFINE-DESIGN-001, LIVE-OBSERVABILITY-001"
PROFILE_VALIDATION_FOCUS="invoke output contract; define/design handoff evidence; live loop pass; observability telemetry"
PROFILE_OBSERVABILITY_FOCUS="live loop report; quality bar status; anti-pattern hits; workflow gaps; reflection trigger"
PROFILE_PROMOTION_GATE="live loop pass plus observed report"

PROFILE_PROMPT_IDS=("invoke-define-live-pass" "invoke-design-live-pass" "invoke-define-design-live-pass" "invoke-define-live-pass")
PROFILE_REGIME_IDS=("LIVE-DEFINE-001" "LIVE-DESIGN-001" "LIVE-DEFINE-DESIGN-001" "LIVE-OBSERVABILITY-001")
PROFILE_PROMPT_REQUESTS=(
	"Run invoke define and return a real define artifact body."
	"Run invoke design and return a governed six-view design artifact body."
	"Run invoke define-to-design and return inspectable handoff evidence."
	"Observe a completed invoke experiment loop report and return telemetry evidence."
)
PROFILE_REGIME_GOALS=(
	"Validate live invoke define execution against the invoke contract."
	"Validate live invoke design execution against the invoke contract."
	"Validate live invoke define-to-design execution and authority handoff."
	"Validate experiment-loop observability from completed live invoke evidence."
)
