'use strict';

const { createHash } = require('crypto');

const SHA256_RE = /^[0-9a-f]{64}$/;
const TIMESTAMP_RE =
  /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})$/;
const REASON_CODE_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const EVIDENCE_STATES = new Set(['observed', 'partial', 'unavailable', 'not-reached']);
const STATUS_VALUES = new Set([
  'dry-run-ready',
  'applied',
  'identical-no-op',
  'invalid-request',
  'id-conflict',
  'tooling-unavailable',
  'baseline-blocked',
  'candidate-blocked',
  'write-failed',
  'postwrite-digest-mismatch',
]);

const BODY_FIELDS = [
  'schema_version', 'operation', 'mode', 'status', 'reason_code',
  'timestamp_input', 'inventory_root', 'runtime', 'inputs', 'baseline',
  'candidate', 'warning_delta', 'write', 'authority_boundary', 'residue',
];
const RECEIPT_FIELDS = [
  'schema_version', 'operation', 'mode', 'status', 'reason_code',
  'operation_fingerprint', 'timestamp_input', 'inventory_root', 'runtime',
  'inputs', 'baseline', 'candidate', 'warning_delta', 'write',
  'authority_boundary', 'residue', 'receipt_sha256',
];
const OPERATION_INPUT_FIELDS = [
  'operation', 'mode', 'timestamp_input', 'inventory_root', 'runtime', 'inputs',
];
const INPUT_DIGEST_FIELDS = [
  'baseline_index_sha256', 'baseline_human_index_sha256',
  'record_sha256', 'normalized_record_sha256',
];
const CANDIDATE_FIELDS = [
  'evidence_state', 'disposition', 'index_sha256', 'human_index_sha256',
  'report_sha256', 'lookup_readiness',
];

function sha256Hex(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function canonicalSerialize(value) {
  return JSON.stringify(value, null, 2) + '\n';
}

function isPlainObject(value) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

function orderedObject(source, fields) {
  const output = {};
  for (const field of fields) output[field] = source[field];
  return output;
}

function compareStrings(left, right) {
  if (left < right) return -1;
  if (left > right) return 1;
  return 0;
}

function sortedUniqueStrings(values) {
  return [...new Set(values)].sort(compareStrings);
}

function sortedDigestMap(value) {
  const output = {};
  for (const key of Object.keys(value).sort(compareStrings)) output[key] = value[key];
  return output;
}

function normalizeBody(body) {
  return orderedObject({
    schema_version: body.schema_version,
    operation: body.operation,
    mode: body.mode,
    status: body.status,
    reason_code: body.reason_code,
    timestamp_input: body.timestamp_input,
    inventory_root: body.inventory_root,
    runtime: {
      evidence_state: body.runtime.evidence_state,
      bundle_sha256: body.runtime.bundle_sha256,
      helpers: [...body.runtime.helpers]
        .map((helper) => ({
          path: helper.path,
          evidence_state: helper.evidence_state,
          sha256: helper.sha256,
        }))
        .sort((left, right) =>
          compareStrings(left.path, right.path) ||
          compareStrings(left.evidence_state, right.evidence_state) ||
          compareStrings(left.sha256 || '', right.sha256 || '')),
    },
    inputs: orderedObject(body.inputs, ['evidence_state', ...INPUT_DIGEST_FIELDS]),
    baseline: orderedObject(body.baseline, [
      'evidence_state', 'report_sha256', 'lookup_readiness',
      'failure_count', 'warning_count',
    ]),
    candidate: orderedObject(body.candidate, CANDIDATE_FIELDS),
    warning_delta: {
      evidence_state: body.warning_delta.evidence_state,
      introduced: sortedUniqueStrings(body.warning_delta.introduced),
      resolved: sortedUniqueStrings(body.warning_delta.resolved),
      inherited_count: body.warning_delta.inherited_count,
      inherited_set_sha256: body.warning_delta.inherited_set_sha256,
    },
    write: {
      evidence_state: body.write.evidence_state,
      attempted: body.write.attempted,
      committed: body.write.committed,
      observed_changed_paths: sortedUniqueStrings(body.write.observed_changed_paths),
      expected_postwrite_digests: sortedDigestMap(body.write.expected_postwrite_digests),
      actual_postwrite_digests: sortedDigestMap(body.write.actual_postwrite_digests),
      possible_partial_mutation: body.write.possible_partial_mutation,
      repair_required: body.write.repair_required,
    },
    authority_boundary: body.authority_boundary,
    residue: sortedUniqueStrings(body.residue),
  }, BODY_FIELDS);
}

function operationInputs(normalizedBody) {
  return orderedObject(normalizedBody, OPERATION_INPUT_FIELDS);
}

function computeOperationFingerprint(normalizedBody) {
  return sha256Hex(canonicalSerialize(operationInputs(normalizedBody)));
}

function receiptWithoutDigest(normalizedBody, operationFingerprint) {
  return orderedObject({
    ...normalizedBody,
    operation_fingerprint: operationFingerprint,
  }, RECEIPT_FIELDS.filter((field) => field !== 'receipt_sha256'));
}

function computeReceiptSha256(normalizedBody, operationFingerprint) {
  return sha256Hex(canonicalSerialize(
    receiptWithoutDigest(normalizedBody, operationFingerprint),
  ));
}

function ownKeysExact(value, fields, label, errors) {
  if (!isPlainObject(value)) {
    errors.push(`${label} must be an object`);
    return false;
  }
  const expected = new Set(fields);
  for (const field of fields) {
    if (!Object.prototype.hasOwnProperty.call(value, field)) {
      errors.push(`${label}.${field} is required`);
    }
  }
  for (const field of Object.keys(value)) {
    if (!expected.has(field)) errors.push(`${label}.${field} is unknown`);
  }
  return true;
}

function expectEvidenceState(value, label, errors) {
  if (!EVIDENCE_STATES.has(value)) errors.push(`${label} is not a valid evidence state`);
}

function expectDigest(value, label, errors, nullable = false) {
  if (nullable && value === null) return;
  if (typeof value !== 'string' || !SHA256_RE.test(value)) {
    errors.push(`${label} must be ${nullable ? 'null or ' : ''}a lowercase SHA-256 digest`);
  }
}

function expectInteger(value, label, errors, nullable = false) {
  if (nullable && value === null) return;
  if (!Number.isInteger(value) || value < 0) {
    errors.push(`${label} must be ${nullable ? 'null or ' : ''}a non-negative integer`);
  }
}

function expectBoolean(value, label, errors) {
  if (typeof value !== 'boolean') errors.push(`${label} must be boolean`);
}

function expectRelativePath(value, label, errors) {
  if (
    typeof value !== 'string' || value.length === 0 || value.startsWith('/') ||
    value.includes('\\') || value.split('/').includes('..')
  ) {
    errors.push(`${label} must be an Inventory-root-relative POSIX path`);
  }
}

function expectStringSet(value, label, errors, pathValues = false) {
  if (!Array.isArray(value)) {
    errors.push(`${label} must be an array`);
    return;
  }
  const seen = new Set();
  value.forEach((item, index) => {
    if (typeof item !== 'string' || item.length === 0) {
      errors.push(`${label}[${index}] must be a non-empty string`);
    } else if (seen.has(item)) {
      errors.push(`${label} must not contain duplicates`);
    } else {
      seen.add(item);
    }
    if (pathValues) expectRelativePath(item, `${label}[${index}]`, errors);
  });
}

function validateDigestMap(value, label, errors) {
  if (!isPlainObject(value)) {
    errors.push(`${label} must be an object`);
    return;
  }
  for (const [relativePath, digest] of Object.entries(value)) {
    expectRelativePath(relativePath, `${label} key`, errors);
    expectDigest(digest, `${label}.${relativePath}`, errors);
  }
}

function requireNulls(section, fields, label, errors) {
  for (const field of fields) {
    if (section[field] !== null) errors.push(`${label}.${field} must be null when not reached`);
  }
}

function validateRuntime(runtime, errors) {
  if (!ownKeysExact(runtime, ['evidence_state', 'bundle_sha256', 'helpers'], 'runtime', errors)) return;
  expectEvidenceState(runtime.evidence_state, 'runtime.evidence_state', errors);
  expectDigest(runtime.bundle_sha256, 'runtime.bundle_sha256', errors, true);
  if (!Array.isArray(runtime.helpers)) {
    errors.push('runtime.helpers must be an array');
    return;
  }
  const paths = new Set();
  runtime.helpers.forEach((helper, index) => {
    const label = `runtime.helpers[${index}]`;
    if (!ownKeysExact(helper, ['path', 'evidence_state', 'sha256'], label, errors)) return;
    expectRelativePath(helper.path, `${label}.path`, errors);
    expectEvidenceState(helper.evidence_state, `${label}.evidence_state`, errors);
    expectDigest(helper.sha256, `${label}.sha256`, errors, true);
    if (helper.evidence_state === 'observed' && helper.sha256 === null) {
      errors.push(`${label}.sha256 is required when observed`);
    }
    if (helper.evidence_state !== 'observed' && helper.sha256 !== null) {
      errors.push(`${label}.sha256 must be null when not observed`);
    }
    if (paths.has(helper.path)) errors.push(`runtime.helpers contains duplicate path ${helper.path}`);
    paths.add(helper.path);
  });
  if (runtime.evidence_state === 'observed') {
    if (runtime.bundle_sha256 === null) errors.push('runtime.bundle_sha256 is required when observed');
    if (runtime.helpers.length === 0) errors.push('runtime.helpers must be non-empty when observed');
    if (runtime.helpers.some((helper) => helper.evidence_state !== 'observed')) {
      errors.push('runtime.helpers must all be observed when runtime evidence is observed');
    }
  } else if (runtime.evidence_state === 'not-reached' && runtime.bundle_sha256 !== null) {
    errors.push('runtime.bundle_sha256 must be null when not reached');
  }
}

function validateInputs(inputs, errors) {
  if (!ownKeysExact(inputs, ['evidence_state', ...INPUT_DIGEST_FIELDS], 'inputs', errors)) return;
  expectEvidenceState(inputs.evidence_state, 'inputs.evidence_state', errors);
  INPUT_DIGEST_FIELDS.forEach((field) => expectDigest(inputs[field], `inputs.${field}`, errors, true));
  if (inputs.evidence_state === 'observed') {
    INPUT_DIGEST_FIELDS.forEach((field) => {
      if (inputs[field] === null) errors.push(`inputs.${field} is required when observed`);
    });
  } else if (inputs.evidence_state === 'not-reached') {
    requireNulls(inputs, INPUT_DIGEST_FIELDS, 'inputs', errors);
  }
}

function validateBaseline(baseline, errors) {
  const fields = ['evidence_state', 'report_sha256', 'lookup_readiness', 'failure_count', 'warning_count'];
  if (!ownKeysExact(baseline, fields, 'baseline', errors)) return;
  expectEvidenceState(baseline.evidence_state, 'baseline.evidence_state', errors);
  expectDigest(baseline.report_sha256, 'baseline.report_sha256', errors, true);
  if (![null, 'ready', 'blocked'].includes(baseline.lookup_readiness)) {
    errors.push('baseline.lookup_readiness must be null, ready, or blocked');
  }
  expectInteger(baseline.failure_count, 'baseline.failure_count', errors, true);
  expectInteger(baseline.warning_count, 'baseline.warning_count', errors, true);
  const values = ['report_sha256', 'lookup_readiness', 'failure_count', 'warning_count'];
  if (baseline.evidence_state === 'observed') {
    values.forEach((field) => {
      if (baseline[field] === null) errors.push(`baseline.${field} is required when observed`);
    });
  } else if (baseline.evidence_state === 'not-reached') {
    requireNulls(baseline, values, 'baseline', errors);
  }
}

function validateCandidate(candidate, errors) {
  if (!ownKeysExact(candidate, CANDIDATE_FIELDS, 'candidate', errors)) return;
  expectEvidenceState(candidate.evidence_state, 'candidate.evidence_state', errors);
  if (![null, 'added', 'identical-no-op', 'id-conflict'].includes(candidate.disposition)) {
    errors.push('candidate.disposition is not supported');
  }
  ['index_sha256', 'human_index_sha256', 'report_sha256'].forEach((field) =>
    expectDigest(candidate[field], `candidate.${field}`, errors, true));
  if (![null, 'ready', 'blocked'].includes(candidate.lookup_readiness)) {
    errors.push('candidate.lookup_readiness must be null, ready, or blocked');
  }
  const values = ['disposition', 'index_sha256', 'human_index_sha256', 'report_sha256', 'lookup_readiness'];
  if (candidate.evidence_state === 'observed') {
    values.forEach((field) => {
      if (candidate[field] === null) errors.push(`candidate.${field} is required when observed`);
    });
  } else if (candidate.evidence_state === 'not-reached') {
    requireNulls(candidate, values, 'candidate', errors);
  }
}

function validateWarningDelta(warningDelta, errors) {
  const fields = ['evidence_state', 'introduced', 'resolved', 'inherited_count', 'inherited_set_sha256'];
  if (!ownKeysExact(warningDelta, fields, 'warning_delta', errors)) return;
  expectEvidenceState(warningDelta.evidence_state, 'warning_delta.evidence_state', errors);
  expectStringSet(warningDelta.introduced, 'warning_delta.introduced', errors);
  expectStringSet(warningDelta.resolved, 'warning_delta.resolved', errors);
  expectInteger(warningDelta.inherited_count, 'warning_delta.inherited_count', errors, true);
  expectDigest(warningDelta.inherited_set_sha256, 'warning_delta.inherited_set_sha256', errors, true);
  if (warningDelta.evidence_state === 'observed') {
    if (warningDelta.inherited_count === null) errors.push('warning_delta.inherited_count is required when observed');
    if (warningDelta.inherited_set_sha256 === null) {
      errors.push('warning_delta.inherited_set_sha256 is required when observed');
    }
  } else if (warningDelta.evidence_state === 'not-reached') {
    if (warningDelta.introduced.length !== 0 || warningDelta.resolved.length !== 0) {
      errors.push('warning_delta sets must be empty when not reached');
    }
    requireNulls(warningDelta, ['inherited_count', 'inherited_set_sha256'], 'warning_delta', errors);
  }
}

function validateWrite(write, errors) {
  const fields = [
    'evidence_state', 'attempted', 'committed', 'observed_changed_paths',
    'expected_postwrite_digests', 'actual_postwrite_digests',
    'possible_partial_mutation', 'repair_required',
  ];
  if (!ownKeysExact(write, fields, 'write', errors)) return;
  expectEvidenceState(write.evidence_state, 'write.evidence_state', errors);
  expectBoolean(write.attempted, 'write.attempted', errors);
  expectBoolean(write.committed, 'write.committed', errors);
  expectStringSet(write.observed_changed_paths, 'write.observed_changed_paths', errors, true);
  validateDigestMap(write.expected_postwrite_digests, 'write.expected_postwrite_digests', errors);
  validateDigestMap(write.actual_postwrite_digests, 'write.actual_postwrite_digests', errors);
  expectBoolean(write.possible_partial_mutation, 'write.possible_partial_mutation', errors);
  expectBoolean(write.repair_required, 'write.repair_required', errors);
  if (write.committed === true && write.attempted !== true) {
    errors.push('write.committed=true requires write.attempted=true');
  }
  if (write.evidence_state === 'not-reached') {
    if (
      write.attempted || write.committed || write.observed_changed_paths.length ||
      Object.keys(write.expected_postwrite_digests).length ||
      Object.keys(write.actual_postwrite_digests).length ||
      write.possible_partial_mutation || write.repair_required
    ) {
      errors.push('write must contain the empty no-attempt witness when not reached');
    }
  }
}

function validateStatusSemantics(body, errors) {
  if (body.status === 'tooling-unavailable' && !['partial', 'unavailable'].includes(body.runtime.evidence_state)) {
    errors.push('tooling-unavailable requires partial or unavailable runtime evidence');
  }
  if (body.status === 'baseline-blocked') {
    if (body.baseline.evidence_state !== 'observed' || body.baseline.lookup_readiness !== 'blocked') {
      errors.push('baseline-blocked requires an observed blocked baseline');
    }
    if (body.candidate.evidence_state !== 'not-reached') {
      errors.push('baseline-blocked requires candidate evidence to be not-reached');
    }
  }
  if (body.status === 'invalid-request' && body.inputs.evidence_state === 'observed') {
    errors.push('invalid-request requires partial or unavailable input evidence');
  }
  if (body.status === 'dry-run-ready') {
    if (body.mode !== 'dry-run') errors.push('dry-run-ready requires dry-run mode');
    for (const section of ['runtime', 'inputs', 'baseline', 'candidate', 'warning_delta']) {
      if (body[section].evidence_state !== 'observed') {
        errors.push(`dry-run-ready requires observed ${section} evidence`);
      }
    }
    if (body.write.evidence_state !== 'observed' || body.write.attempted) {
      errors.push('dry-run-ready requires an observed no-attempt write witness');
    }
    if (
      canonicalSerialize(sortedDigestMap(body.write.expected_postwrite_digests)) !==
      canonicalSerialize(sortedDigestMap(body.write.actual_postwrite_digests))
    ) {
      errors.push('dry-run-ready requires equal expected and actual no-write digests');
    }
  }
}

function validateNonDerivedBody(body) {
  const errors = [];
  if (!ownKeysExact(body, BODY_FIELDS, 'receipt_body', errors)) return errors;
  if (body.schema_version !== 'inventory.operation-receipt.v1') {
    errors.push('receipt_body.schema_version must equal inventory.operation-receipt.v1');
  }
  if (body.operation !== 'append') errors.push('receipt_body.operation must equal append');
  if (!['dry-run', 'apply'].includes(body.mode)) errors.push('receipt_body.mode must be dry-run or apply');
  if (!STATUS_VALUES.has(body.status)) errors.push('receipt_body.status is not supported');
  if (
    body.reason_code !== null &&
    (typeof body.reason_code !== 'string' || !REASON_CODE_RE.test(body.reason_code))
  ) {
    errors.push('receipt_body.reason_code must be null or a kebab-case code');
  }
  if (typeof body.timestamp_input !== 'string' || !TIMESTAMP_RE.test(body.timestamp_input)) {
    errors.push('receipt_body.timestamp_input must be an explicit ISO-8601 timestamp');
  }
  if (body.inventory_root !== '.arcanum/inventory') {
    errors.push('receipt_body.inventory_root must equal .arcanum/inventory');
  }
  if (body.authority_boundary !== 'inventory-read-model-only') {
    errors.push('receipt_body.authority_boundary must equal inventory-read-model-only');
  }
  validateRuntime(body.runtime, errors);
  validateInputs(body.inputs, errors);
  validateBaseline(body.baseline, errors);
  validateCandidate(body.candidate, errors);
  validateWarningDelta(body.warning_delta, errors);
  validateWrite(body.write, errors);
  expectStringSet(body.residue, 'residue', errors);
  if (errors.length === 0) validateStatusSemantics(body, errors);
  return errors;
}

function createOperationReceipt(body) {
  const errors = validateNonDerivedBody(body);
  if (errors.length > 0) {
    throw new TypeError(`invalid operation receipt body:\n- ${errors.join('\n- ')}`);
  }
  const normalizedBody = normalizeBody(body);
  const operationFingerprint = computeOperationFingerprint(normalizedBody);
  const receiptSha256 = computeReceiptSha256(normalizedBody, operationFingerprint);
  const receipt = orderedObject({
    ...normalizedBody,
    operation_fingerprint: operationFingerprint,
    receipt_sha256: receiptSha256,
  }, RECEIPT_FIELDS);
  const validation = validateOperationReceipt(receipt);
  if (!validation.valid) {
    throw new TypeError(`constructed operation receipt is invalid:\n- ${validation.errors.join('\n- ')}`);
  }
  return {
    receipt,
    bytes: canonicalSerialize(receipt),
    operation_fingerprint: operationFingerprint,
    receipt_sha256: receiptSha256,
    validation,
  };
}

function validateOperationReceipt(receipt) {
  const errors = [];
  if (!ownKeysExact(receipt, RECEIPT_FIELDS, 'receipt', errors)) {
    return { valid: false, errors };
  }
  const body = {};
  for (const field of BODY_FIELDS) body[field] = receipt[field];
  errors.push(...validateNonDerivedBody(body));
  expectDigest(receipt.operation_fingerprint, 'receipt.operation_fingerprint', errors);
  expectDigest(receipt.receipt_sha256, 'receipt.receipt_sha256', errors);
  if (errors.length > 0) return { valid: false, errors };
  const normalizedBody = normalizeBody(body);
  const expectedFingerprint = computeOperationFingerprint(normalizedBody);
  if (receipt.operation_fingerprint !== expectedFingerprint) {
    errors.push('receipt.operation_fingerprint does not reproduce');
  }
  const expectedReceiptSha256 = computeReceiptSha256(normalizedBody, expectedFingerprint);
  if (receipt.receipt_sha256 !== expectedReceiptSha256) {
    errors.push('receipt.receipt_sha256 does not reproduce');
  }
  return { valid: errors.length === 0, errors };
}

module.exports = {
  BODY_FIELDS,
  RECEIPT_FIELDS,
  canonicalSerialize,
  computeOperationFingerprint,
  computeReceiptSha256,
  createOperationReceipt,
  normalizeBody,
  sha256Hex,
  validateOperationReceipt,
};
