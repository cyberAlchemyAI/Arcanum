#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { inspectHistory } = require('./ledger-engine.cjs');

const PROFILE_SCHEMA_VERSION = 'arcanum.subagent-strategy-runtime-profile.v1';
const PROFILE_KEYS = new Set([
  'schema_version',
  'profile_id',
  'profile_version',
  'row_schemas',
  'confirmation',
  'source_lifecycle',
  'ledger',
  'runtime_temp_root',
  'adapter_module',
  'adapter_base',
  'adapter_operations',
  'required_admission_receipt_kind',
  'dispatch_types',
]);
const PORTABLE_PATH = /^(?!\/)(?![A-Za-z]:)(?!.*(?:^|\/)\.\.(?:\/|$))(?!.*\\).+$/;
const IDENTIFIER = /^[a-z0-9.-]+$/;
const SEMVER = /^[0-9]+\.[0-9]+\.[0-9]+$/;

function requireProfile(condition, message) {
  if (!condition) throw new Error(`invalid runtime profile: ${message}`);
}

function validateRuntimeProfile(profile) {
  requireProfile(profile && typeof profile === 'object' && !Array.isArray(profile), 'root must be an object');
  requireProfile(
    Object.keys(profile).length === PROFILE_KEYS.size &&
      Object.keys(profile).every((key) => PROFILE_KEYS.has(key)),
    'unknown or missing root fields',
  );
  requireProfile(profile.schema_version === PROFILE_SCHEMA_VERSION, 'schema_version mismatch');
  requireProfile(typeof profile.profile_id === 'string' && IDENTIFIER.test(profile.profile_id), 'profile_id is invalid');
  requireProfile(typeof profile.profile_version === 'string' && SEMVER.test(profile.profile_version), 'profile_version is invalid');
  const rows = profile.row_schemas;
  requireProfile(rows && typeof rows === 'object' && !Array.isArray(rows), 'row_schemas must be an object');
  requireProfile(
    Object.keys(rows).length === 2 &&
      typeof rows.current === 'string' && rows.current.length > 0 &&
      Array.isArray(rows.historical_validate_only) &&
      rows.historical_validate_only.every((item) => typeof item === 'string' && item.length > 0) &&
      new Set(rows.historical_validate_only).size === rows.historical_validate_only.length,
    'row_schemas is invalid',
  );
  const confirmation = profile.confirmation;
  requireProfile(
    confirmation && typeof confirmation === 'object' && !Array.isArray(confirmation) &&
      Object.keys(confirmation).length === 3,
    'confirmation is invalid',
  );
  requireProfile(['exact_sheet', 'material_projection'].includes(confirmation.mode), 'confirmation.mode is invalid');
  if (confirmation.mode === 'exact_sheet') {
    requireProfile(
      confirmation.binding_digest === 'source_sheet' && confirmation.equivalence_receipt_kind === null,
      'exact_sheet confirmation must bind the source sheet without equivalence',
    );
  } else {
    requireProfile(
      confirmation.binding_digest === 'material_projection' &&
        typeof confirmation.equivalence_receipt_kind === 'string' &&
        confirmation.equivalence_receipt_kind.length > 0,
      'material_projection confirmation must bind material equivalence',
    );
  }
  requireProfile(['temporary_consumed', 'durable'].includes(profile.source_lifecycle), 'source_lifecycle is invalid');
  for (const field of ['ledger', 'runtime_temp_root', 'adapter_module']) {
    requireProfile(typeof profile[field] === 'string' && PORTABLE_PATH.test(profile[field]), `${field} is not portable`);
  }
  requireProfile(['arcanum_root', 'project_root'].includes(profile.adapter_base), 'adapter_base is invalid');
  const operations = profile.adapter_operations;
  requireProfile(
    operations && typeof operations === 'object' && !Array.isArray(operations) &&
      Object.keys(operations).length === 3 &&
      Object.keys(operations).every((key) => ['readiness', 'register', 'close'].includes(key)) &&
      Object.values(operations).every((value) => typeof value === 'string' && /^--[a-z][a-z-]*$/.test(value)),
    'adapter_operations is invalid',
  );
  requireProfile(
    profile.required_admission_receipt_kind === null ||
      (typeof profile.required_admission_receipt_kind === 'string' && profile.required_admission_receipt_kind.length > 0),
    'required_admission_receipt_kind is invalid',
  );
  const types = profile.dispatch_types;
  requireProfile(types && typeof types === 'object' && !Array.isArray(types) && Object.keys(types).length > 0, 'dispatch_types is invalid');
  for (const [type, owner] of Object.entries(types)) {
    requireProfile(IDENTIFIER.test(type), `dispatch type ${JSON.stringify(type)} is invalid`);
    requireProfile(
      owner && typeof owner === 'object' && !Array.isArray(owner) && Object.keys(owner).length === 2,
      `dispatch type ${type} has invalid fields`,
    );
    requireProfile(['live', 'reserved'].includes(owner.status), `dispatch type ${type} has invalid status`);
    if (owner.status === 'live') {
      requireProfile(
        typeof owner.owner_capability === 'string' && PORTABLE_PATH.test(owner.owner_capability),
        `live dispatch type ${type} has no portable owner capability`,
      );
    } else {
      requireProfile(owner.owner_capability === null, `reserved dispatch type ${type} must not name an owner`);
    }
  }
}

const args = process.argv.slice(2);
const profileFlag = args.indexOf('--profile');
let profileInput = null;
if (profileFlag !== -1) {
  profileInput = args[profileFlag + 1];
  if (!profileInput) {
    console.error('--profile requires a JSON path');
    process.exit(2);
  }
  args.splice(profileFlag, 2);
}
const mode = args.shift();
if (!['readiness', 'register', 'close', 'check-history'].includes(mode)) {
  console.error('usage: node strategy-runtime.cjs <readiness|register|close|check-history> [record.tmp.json] [--profile profile.json]');
  process.exit(2);
}
const record = args.shift();
if (args.length > 0 || (mode !== 'check-history' && !record) || (mode === 'check-history' && record)) {
  console.error('invalid arguments for strategy runtime mode ' + mode);
  process.exit(2);
}

const arcanumRoot = path.resolve(__dirname, '..', '..', '..');
const projectRoot = path.resolve(
  process.env.ARCANUM_PROJECT_DIR ||
  process.env.CODEX_PROJECT_DIR ||
  process.env.CLAUDE_PROJECT_DIR ||
  process.cwd(),
);
const profilePath = path.resolve(
  profileInput || path.join(arcanumRoot, 'arcana/subagent-strategy/profiles/arcanum.json'),
);

let profile;
try {
  profile = JSON.parse(fs.readFileSync(profilePath, 'utf8'));
  validateRuntimeProfile(profile);
} catch (error) {
  console.error('cannot read runtime profile:', error.message);
  process.exit(2);
}

if (mode === 'check-history') {
  try {
    const header = 'dispatches:\n';
    const history = inspectHistory({
      projectDir: projectRoot,
      ledgerRelative: profile.ledger,
      header,
    });
    const openDispatches = [...history.dispatchRows.keys()].filter(
      (dispatchId) => !history.closeRows.has(dispatchId),
    );
    console.log(JSON.stringify({
      schema_version: 'arcanum.subagent-strategy-runtime-receipt.v1',
      status: 'pass',
      mode,
      profile_id: profile.profile_id,
      ledger: profile.ledger,
      dispatch_row_count: history.dispatchRows.size,
      close_row_count: history.closeRows.size,
      open_dispatch_ids: openDispatches,
    }));
    process.exit(0);
  } catch (error) {
    console.error(error.message || String(error));
    process.exit(Number.isInteger(error.code) ? error.code : 1);
  }
}

const adapterBase = profile.adapter_base === 'project_root' ? projectRoot : arcanumRoot;
const adapter = path.resolve(adapterBase, profile.adapter_module);
const adapterMode = profile.adapter_operations[mode];
const completed = spawnSync(process.execPath, [adapter, adapterMode, path.resolve(record)], {
  cwd: projectRoot,
  env: Object.assign({}, process.env, { ARCANUM_PROJECT_DIR: projectRoot }),
  encoding: 'utf8',
});
if (completed.stdout) process.stdout.write(completed.stdout);
if (completed.stderr) process.stderr.write(completed.stderr);
if (completed.status !== 0) process.exit(completed.status || 2);

let adapterReceipt = null;
if (mode !== 'readiness') {
  const receiptLine = (completed.stdout || '')
    .split(/\r?\n/)
    .reverse()
    .find((line) => line.startsWith('RUNTIME_RECEIPT='));
  try {
    adapterReceipt = receiptLine ? JSON.parse(receiptLine.slice('RUNTIME_RECEIPT='.length)) : null;
  } catch (_) {
    adapterReceipt = null;
  }
  if (
    !adapterReceipt ||
    adapterReceipt.schema_version !== 'arcanum.subagent-strategy-runtime-receipt.v1' ||
    adapterReceipt.status !== 'pass' ||
    adapterReceipt.mode !== mode
  ) {
    console.error('profile adapter did not return a valid normalized runtime receipt');
    process.exit(2);
  }
}

console.log(JSON.stringify({
  schema_version: 'arcanum.subagent-strategy-runtime-receipt.v1',
  status: 'pass',
  mode,
  profile_id: profile.profile_id,
  confirmation_mode: profile.confirmation.mode,
  source_lifecycle: profile.source_lifecycle,
  ledger: profile.ledger,
  append_status: adapterReceipt ? adapterReceipt.append_status : null,
  identity: adapterReceipt ? adapterReceipt.identity : null,
  content_digest: adapterReceipt ? adapterReceipt.content_digest : null,
  temporary_envelope_consumed: adapterReceipt
    ? adapterReceipt.temporary_envelope_consumed === true
    : false,
  registration_envelope_consumed: mode === 'register'
    ? adapterReceipt.temporary_envelope_consumed === true
    : false,
  temporary_close_consumed: mode === 'close'
    ? adapterReceipt.temporary_envelope_consumed === true
    : false,
}));
