export type UiPrototypingStudioErrorCode =
  | "UPS_AUTH_REQUIRED"
  | "UPS_AUTH_FORBIDDEN"
  | "VARIANT_COUNT_OUT_OF_RANGE"
  | "SESSION_NOT_FOUND"
  | "PROMPT_REQUIRED"
  | "PROMPT_NOT_SET"
  | "VARIANT_GENERATION_COUNT_MISMATCH"
  | "BASELINE_SELECTION_REQUIRED"
  | "BASELINE_LABEL_INVALID"
  | "BASELINE_GATE_UNSATISFIED"
  | "COMMENT_SCHEMA_INVALID"
  | "COMMENT_SET_EMPTY"
  | "SOURCE_REVISION_INVALID"
  | "DRAFT_BATCH_NOT_FOUND"
  | "BATCH_NOT_FOUND"
  | "BATCH_NOT_DRAFT"
  | "APPROVAL_METADATA_REQUIRED"
  | "APPROVAL_STALE"
  | "AUTO_APPLY_FORBIDDEN"
  | "BATCH_APPROVAL_REQUIRED"
  | "BATCH_STALE_FOR_HEAD"
  | "HANDOFF_REVISION_REQUIRED"
  | "HANDOFF_REFERENCE_INCOMPLETE"
  | "HANDOFF_BUNDLE_NOT_READY"
  | "CANDIDATE_HASH_MISMATCH"
  | "NO_STAGED_CANDIDATE"
  | "OD_ID_MISSING"
  | "ARTIFACT_CONTENT_PORT_UNAVAILABLE"
  | "CURRENT_HTML_UNRESOLVABLE"
  | "SCOPE_EMPTY"
  | "NO_REVISION_TO_REVERT"
  | "REVISION_NOT_FOUND"
  | "HANDOFF_CONFIRMATION_REQUIRED"
  | "AUTO_OBJECTIVE_REQUIRED"
  | "CYCLE_CANDIDATES_REQUIRED"
  | "CYCLE_SCORE_INVALID"
  | "CYCLE_CEILING_REACHED";

export type UiPrototypingStudioError = Error & {
  code: UiPrototypingStudioErrorCode;
  details: Record<string, unknown>;
};

export function createUiPrototypingStudioError(
  code: UiPrototypingStudioErrorCode,
  message: string,
  details: Record<string, unknown> = {},
): UiPrototypingStudioError {
  const error = new Error(message) as UiPrototypingStudioError;
  error.name = "UiPrototypingStudioError";
  error.code = code;
  error.details = details;
  return error;
}

export function isUiPrototypingStudioError(
  error: unknown,
): error is UiPrototypingStudioError {
  if (!error || typeof error !== "object") {
    return false;
  }

  const candidate = error as Partial<UiPrototypingStudioError>;
  return (
    typeof candidate.message === "string" &&
    typeof candidate.name === "string" &&
    typeof candidate.code === "string" &&
    typeof candidate.details === "object"
  );
}
