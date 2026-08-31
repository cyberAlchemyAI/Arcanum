PROFILE_ID="invoke-live"
PROFILE_ARTIFACT_TYPE="spell"
PROFILE_LIFECYCLE_OWNER="invoke"
PROFILE_SCENARIO_PACK="invoke-live-promotion"
PROFILE_REQUIRED_MODES="define, design, plan, define-design, define-design-plan, semantic-intent-low, semantic-intent-medium, semantic-intent-complex, observability"
PROFILE_PROMPT_SET="invoke-define-live-pass, invoke-design-live-pass, invoke-plan-live-pass, invoke-define-design-live-pass, invoke-define-design-plan-live-pass, invoke-semantic-intent-low, invoke-semantic-intent-medium, invoke-semantic-intent-complex, invoke-observability-live-pass"
PROFILE_REGIME_SET="LIVE-DEFINE-001, LIVE-DESIGN-001, LIVE-PLAN-001, LIVE-DEFINE-DESIGN-001, LIVE-DEFINE-DESIGN-PLAN-001, LIVE-SEMANTIC-INTENT-LOW-001, LIVE-SEMANTIC-INTENT-MEDIUM-001, LIVE-SEMANTIC-INTENT-COMPLEX-001, LIVE-OBSERVABILITY-001"
PROFILE_VALIDATION_FOCUS="invoke output contract; define/design/plan handoff evidence; parsed semantic-intent coverage; live pass; observability telemetry"
PROFILE_OBSERVABILITY_FOCUS="semantic receipt; quality bar status; anti-pattern hits; workflow gaps; reflection trigger"
PROFILE_PROMOTION_GATE="two consecutive semantic-validator passes at low, medium, and complex plus lifecycle-owner review"
PROFILE_SEMANTIC_VALIDATOR="spells/invoke/development/fixtures/define-intent-coverage/validate_semantic_intent.py"
PROFILE_SEMANTIC_ORACLE="spells/invoke/development/fixtures/define-intent-coverage/fixture-matrix.json"
PROFILE_SEMANTIC_EVIDENCE_GLOB="spells/invoke/development/live-intent-evidence/*/artifact.json"
PROFILE_SEMANTIC_REQUIRED_PASS_COUNT=6

PROFILE_PROMPT_IDS=("invoke-define-live-pass" "invoke-design-live-pass" "invoke-plan-live-pass" "invoke-define-design-live-pass" "invoke-define-design-plan-live-pass" "invoke-semantic-intent-low" "invoke-semantic-intent-medium" "invoke-semantic-intent-complex" "invoke-observability-live-pass")
PROFILE_REGIME_IDS=("LIVE-DEFINE-001" "LIVE-DESIGN-001" "LIVE-PLAN-001" "LIVE-DEFINE-DESIGN-001" "LIVE-DEFINE-DESIGN-PLAN-001" "LIVE-SEMANTIC-INTENT-LOW-001" "LIVE-SEMANTIC-INTENT-MEDIUM-001" "LIVE-SEMANTIC-INTENT-COMPLEX-001" "LIVE-OBSERVABILITY-001")
PROFILE_PROMPT_REQUESTS=(
	"Run invoke define and return a real define artifact body."
	"Run invoke design and return a governed six-view design artifact body."
	"Run invoke plan and return an implementation-ready planning artifact body."
	"Run invoke define-to-design and return inspectable handoff evidence."
	"Run invoke define-to-design-to-plan and preserve every handoff boundary."
	"Author a low-complexity parsed semantic-intent artifact from source evidence."
	"Author a medium-complexity parsed semantic-intent artifact from source evidence."
	"Author a complex parsed semantic-intent artifact from source and historical evidence."
	"Observe a completed invoke experiment loop report and return telemetry evidence."
)
PROFILE_REGIME_GOALS=(
	"Validate live invoke define execution against the invoke contract."
	"Validate live invoke design execution against the invoke contract."
	"Validate live invoke plan execution against the invoke contract."
	"Validate live invoke define-to-design execution and authority handoff."
	"Validate live invoke define-to-design-to-plan execution and authority handoffs."
	"Validate low semantic intent completeness with the repository-owned parser."
	"Validate medium semantic intent completeness with the repository-owned parser."
	"Validate complex semantic intent completeness with the repository-owned parser."
	"Validate experiment-loop observability from completed live invoke evidence."
)
