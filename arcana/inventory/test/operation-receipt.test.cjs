'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const {
  computeOperationFingerprint,
  computeReceiptSha256,
  createOperationReceipt,
  normalizeBody,
  validateOperationReceipt,
} = require('../lib/operation-receipt.cjs');

const digest = (character) => character.repeat(64);

function noWriteEvidence() {
  return {
    evidence_state: 'observed',
    attempted: false,
    committed: false,
    observed_changed_paths: [],
    expected_postwrite_digests: {
      'index.json': digest('1'),
      'index.md': digest('2'),
    },
    actual_postwrite_digests: {
      'index.json': digest('1'),
      'index.md': digest('2'),
    },
    possible_partial_mutation: false,
    repair_required: false,
  };
}

function notReachedBaseline() {
  return {
    evidence_state: 'not-reached',
    report_sha256: null,
    lookup_readiness: null,
    failure_count: null,
    warning_count: null,
  };
}

function notReachedCandidate() {
  return {
    evidence_state: 'not-reached',
    disposition: null,
    index_sha256: null,
    human_index_sha256: null,
    report_sha256: null,
    lookup_readiness: null,
  };
}

function notReachedWarnings() {
  return {
    evidence_state: 'not-reached',
    introduced: [],
    resolved: [],
    inherited_count: null,
    inherited_set_sha256: null,
  };
}

function normativeBody() {
  return {
    schema_version: 'inventory.operation-receipt.v1',
    operation: 'append',
    mode: 'dry-run',
    status: 'dry-run-ready',
    reason_code: null,
    timestamp_input: '2026-07-24T18:19:00Z',
    inventory_root: '.arcanum/inventory',
    runtime: {
      evidence_state: 'observed',
      bundle_sha256: digest('a'),
      helpers: [
        {
          path: 'scripts/validate_projection_conformance.py',
          evidence_state: 'observed',
          sha256: digest('d'),
        },
        {
          path: 'lib/inventory-update.cjs',
          evidence_state: 'observed',
          sha256: digest('b'),
        },
        {
          path: 'scripts/validate-index-json.sh',
          evidence_state: 'observed',
          sha256: digest('c'),
        },
      ],
    },
    inputs: {
      evidence_state: 'observed',
      baseline_index_sha256: digest('1'),
      baseline_human_index_sha256: digest('2'),
      record_sha256: digest('3'),
      normalized_record_sha256: digest('4'),
    },
    baseline: {
      evidence_state: 'observed',
      report_sha256: digest('5'),
      lookup_readiness: 'ready',
      failure_count: 0,
      warning_count: 72,
    },
    candidate: {
      evidence_state: 'observed',
      disposition: 'added',
      index_sha256: digest('6'),
      human_index_sha256: digest('7'),
      report_sha256: digest('8'),
      lookup_readiness: 'ready',
    },
    warning_delta: {
      evidence_state: 'observed',
      introduced: ['warning-z', 'warning-a'],
      resolved: ['warning-old-z', 'warning-old-a'],
      inherited_count: 72,
      inherited_set_sha256: digest('9'),
    },
    write: noWriteEvidence(),
    authority_boundary: 'inventory-read-model-only',
    residue: ['z-residue', 'a-residue'],
  };
}

function toolingUnavailableBody() {
  const body = normativeBody();
  body.status = 'tooling-unavailable';
  body.reason_code = 'missing-runtime-helper';
  body.runtime = {
    evidence_state: 'partial',
    bundle_sha256: null,
    helpers: [
      {
        path: 'lib/inventory-update.cjs',
        evidence_state: 'observed',
        sha256: digest('b'),
      },
      {
        path: 'scripts/validate_projection_conformance.py',
        evidence_state: 'unavailable',
        sha256: null,
      },
    ],
  };
  body.inputs = {
    evidence_state: 'not-reached',
    baseline_index_sha256: null,
    baseline_human_index_sha256: null,
    record_sha256: null,
    normalized_record_sha256: null,
  };
  body.baseline = notReachedBaseline();
  body.candidate = notReachedCandidate();
  body.warning_delta = notReachedWarnings();
  body.write = {
    evidence_state: 'not-reached',
    attempted: false,
    committed: false,
    observed_changed_paths: [],
    expected_postwrite_digests: {},
    actual_postwrite_digests: {},
    possible_partial_mutation: false,
    repair_required: false,
  };
  return body;
}

test('complete observed receipt validates and emits canonical UTF-8 JSON', () => {
  const result = createOperationReceipt(normativeBody());
  assert.equal(result.validation.valid, true);
  assert.equal(result.bytes.endsWith('\n'), true);
  assert.equal(result.bytes.endsWith('\n\n'), false);
  assert.deepEqual(JSON.parse(result.bytes), result.receipt);
});

test('identical semantic inputs remain byte-identical', () => {
  const first = createOperationReceipt(normativeBody());
  const reordered = normativeBody();
  reordered.runtime.helpers.reverse();
  reordered.warning_delta.introduced.reverse();
  reordered.residue.reverse();
  const second = createOperationReceipt(reordered);
  assert.equal(first.bytes, second.bytes);
  assert.equal(first.operation_fingerprint, second.operation_fingerprint);
  assert.equal(first.receipt_sha256, second.receipt_sha256);
});

test('tooling-unavailable receipt records partial evidence without sentinel hashes', () => {
  const result = createOperationReceipt(toolingUnavailableBody());
  assert.equal(result.validation.valid, true);
  assert.equal(result.receipt.runtime.bundle_sha256, null);
  assert.equal(result.receipt.runtime.helpers[1].sha256, null);
  assert.equal(result.receipt.inputs.normalized_record_sha256, null);
});

test('baseline block may stop before candidate and request evidence', () => {
  const body = toolingUnavailableBody();
  body.status = 'baseline-blocked';
  body.reason_code = 'baseline-not-ready';
  body.runtime = normativeBody().runtime;
  body.baseline = {
    evidence_state: 'observed',
    report_sha256: digest('5'),
    lookup_readiness: 'blocked',
    failure_count: 1,
    warning_count: 0,
  };
  const result = createOperationReceipt(body);
  assert.equal(result.validation.valid, true);
  assert.equal(result.receipt.candidate.evidence_state, 'not-reached');
});

test('invalid request supports partial raw input evidence', () => {
  const body = normativeBody();
  body.status = 'invalid-request';
  body.reason_code = 'record-json-invalid';
  body.inputs = {
    evidence_state: 'partial',
    baseline_index_sha256: digest('1'),
    baseline_human_index_sha256: digest('2'),
    record_sha256: digest('3'),
    normalized_record_sha256: null,
  };
  body.candidate = notReachedCandidate();
  body.warning_delta = notReachedWarnings();
  const result = createOperationReceipt(body);
  assert.equal(result.validation.valid, true);
  assert.equal(result.receipt.inputs.normalized_record_sha256, null);
});

test('evidence-state contradictions fail closed', () => {
  const missingObserved = normativeBody();
  missingObserved.inputs.normalized_record_sha256 = null;
  assert.throws(() => createOperationReceipt(missingObserved), /required when observed/);

  const inventedUnavailable = toolingUnavailableBody();
  inventedUnavailable.runtime.helpers[1].sha256 = digest('f');
  assert.throws(() => createOperationReceipt(inventedUnavailable), /must be null when not observed/);

  const notReachedWrite = toolingUnavailableBody();
  notReachedWrite.write.attempted = true;
  assert.throws(() => createOperationReceipt(notReachedWrite), /empty no-attempt witness/);
});

test('missing, unknown, invalid digest, timestamp, and path fail closed', () => {
  const missing = normativeBody();
  delete missing.inputs.record_sha256;
  assert.throws(() => createOperationReceipt(missing), /inputs\.record_sha256 is required/);

  const unknown = normativeBody();
  unknown.runtime.checkout_path = '/private/checkout';
  assert.throws(() => createOperationReceipt(unknown), /runtime\.checkout_path is unknown/);

  const invalidDigest = normativeBody();
  invalidDigest.inputs.record_sha256 = 'ABC';
  assert.throws(() => createOperationReceipt(invalidDigest), /lowercase SHA-256/);

  const implicitTimestamp = normativeBody();
  implicitTimestamp.timestamp_input = '';
  assert.throws(() => createOperationReceipt(implicitTimestamp), /explicit ISO-8601/);

  const absolutePath = normativeBody();
  absolutePath.runtime.helpers[0].path = '/private/helper';
  assert.throws(() => createOperationReceipt(absolutePath), /Inventory-root-relative/);
});

test('fingerprints and receipt digests reproduce and tampering fails validation', () => {
  const result = createOperationReceipt(normativeBody());
  const normalized = normalizeBody(normativeBody());
  assert.equal(result.operation_fingerprint, computeOperationFingerprint(normalized));
  assert.equal(
    result.receipt_sha256,
    computeReceiptSha256(normalized, result.operation_fingerprint),
  );
  const tampered = { ...result.receipt, receipt_sha256: digest('f') };
  assert.equal(validateOperationReceipt(tampered).valid, false);
  assert.match(validateOperationReceipt(tampered).errors.join('\n'), /does not reproduce/);
});

test('normative schema is strict and kernel remains clock/filesystem independent', () => {
  const schemaPath = path.join(
    __dirname, '..', 'schemas', 'inventory.operation-receipt.v1.schema.json',
  );
  const libraryPath = path.join(__dirname, '..', 'lib', 'operation-receipt.cjs');
  const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
  const source = fs.readFileSync(libraryPath, 'utf8');
  assert.equal(schema.additionalProperties, false);
  assert.equal(schema.$defs.evidenceState.enum.includes('not-reached'), true);
  assert.equal(schema.required.includes('receipt_sha256'), true);
  assert.doesNotMatch(source, /require\(['"](?:node:)?fs['"]\)/);
  assert.doesNotMatch(source, /\bDate(?:\.|\()/);
  assert.doesNotMatch(source, /process\.cwd/);
});
