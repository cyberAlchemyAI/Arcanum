#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const root = path.resolve(__dirname, '..', '..', '..');
const profilePath = path.join(root, 'arcana/subagent-strategy/profiles/arcanum.json');
const runtime = path.join(root, 'arcana/subagent-strategy/scripts/strategy-runtime.cjs');
const profile = JSON.parse(fs.readFileSync(profilePath, 'utf8'));

function requireCondition(condition, message) {
  if (!condition) throw new Error(message);
}

requireCondition(
  profile.schema_version === 'arcanum.subagent-strategy-runtime-profile.v1',
  'profile schema mismatch',
);
requireCondition(profile.confirmation.mode === 'exact_sheet', 'public confirmation must bind exact sheet bytes');
requireCondition(profile.confirmation.binding_digest === 'source_sheet', 'public confirmation binding must be source_sheet');
requireCondition(profile.source_lifecycle === 'temporary_consumed', 'public source must be temporary');
requireCondition(profile.required_admission_receipt_kind === null, 'public profile must not require a private admission receipt');
requireCondition(profile.dispatch_types.experiment.status === 'reserved', 'public experiment must remain reserved');

const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'strategy-runtime-profile-'));
const result = spawnSync(process.execPath, [runtime, 'check-history', '--profile', profilePath], {
  cwd: temp,
  env: Object.assign({}, process.env, { ARCANUM_PROJECT_DIR: temp }),
  encoding: 'utf8',
});
requireCondition(result.status === 0, result.stderr || result.stdout);
const receipt = JSON.parse(result.stdout.trim());
requireCondition(receipt.status === 'pass', 'history receipt must pass');
requireCondition(receipt.profile_id === profile.profile_id, 'history receipt profile mismatch');
requireCondition(receipt.dispatch_row_count === 0 && receipt.close_row_count === 0, 'new history must be empty');

const runtimeTemp = path.join(temp, '.arcanum', 'runtime', 'subagents-strategy');
fs.mkdirSync(runtimeTemp, { recursive: true });
const dispatchPath = path.join(runtimeTemp, 'profile-runtime.tmp.json');
const dispatch = {
  dispatch_id: '2026-08-27-public-profile-runtime',
  schema_version: '0.6.1',
  dispatch_type: 'research',
  goal: 'Exercise every public shared-runtime operation.',
  context: 'Temporary fixture; no repository product bytes are touched.',
  max_loops: 1,
  final_approver: 'parent',
  working_folder: 'research/public-profile-runtime/',
  groups: [{
    group_id: 'writer',
    agents: [{ role: 'writer', model: 'claude-opus-4-8', token_budget: 100, initial_prompt: 'Write the bounded fixture.' }],
  }],
  connections: [],
};
fs.writeFileSync(dispatchPath, `${JSON.stringify(dispatch, null, 2)}\n`);
const runtimeEnv = Object.assign({}, process.env, { ARCANUM_PROJECT_DIR: temp });
const runMode = (mode, recordPath) => spawnSync(
  process.execPath,
  [runtime, mode, recordPath, '--profile', profilePath],
  { cwd: temp, env: runtimeEnv, encoding: 'utf8' },
);
const readiness = runMode('readiness', dispatchPath);
requireCondition(
  readiness.status === 0 && /"mode":"confirmation-readiness"/.test(readiness.stdout) &&
    /"mode":"readiness"/.test(readiness.stdout),
  readiness.stderr || readiness.stdout,
);
requireCondition(fs.existsSync(dispatchPath), 'readiness must not consume its input');
const registered = runMode('register', dispatchPath);
requireCondition(
  registered.status === 0 && /"mode":"register"/.test(registered.stdout) &&
    /"registration_envelope_consumed":true/.test(registered.stdout),
  registered.stderr || registered.stdout,
);
requireCondition(!fs.existsSync(dispatchPath), 'register must consume its temporary source');

const closePath = path.join(runtimeTemp, 'profile-runtime.close.tmp.json');
fs.writeFileSync(closePath, `${JSON.stringify({
  close_of: dispatch.dispatch_id,
  exit_reason: 'resolved',
  agents_spawned: { total: 1, tree: { writer: 1 }, loops_used: 0 },
}, null, 2)}\n`);
const closed = runMode('close', closePath);
requireCondition(
  closed.status === 0 && /"mode":"close"/.test(closed.stdout) &&
    /"temporary_close_consumed":true/.test(closed.stdout),
  closed.stderr || closed.stdout,
);
requireCondition(!fs.existsSync(closePath), 'close must consume its temporary record');
const finalHistory = spawnSync(process.execPath, [runtime, 'check-history', '--profile', profilePath], {
  cwd: temp,
  env: runtimeEnv,
  encoding: 'utf8',
});
requireCondition(finalHistory.status === 0, finalHistory.stderr || finalHistory.stdout);
const finalReceipt = JSON.parse(finalHistory.stdout.trim());
requireCondition(
  finalReceipt.dispatch_row_count === 1 && finalReceipt.close_row_count === 1 &&
    finalReceipt.open_dispatch_ids.length === 0,
  'public runtime history must contain one paired register/close row',
);
const invalidProfilePath = path.join(temp, 'invalid-profile.json');
const invalidProfile = JSON.parse(JSON.stringify(profile));
invalidProfile.confirmation.binding_digest = 'material_projection';
fs.writeFileSync(invalidProfilePath, `${JSON.stringify(invalidProfile, null, 2)}\n`);
const invalidResult = spawnSync(
  process.execPath,
  [runtime, 'check-history', '--profile', invalidProfilePath],
  {
    cwd: temp,
    env: Object.assign({}, process.env, { ARCANUM_PROJECT_DIR: temp }),
    encoding: 'utf8',
  },
);
requireCondition(
  invalidResult.status === 2 && /exact_sheet confirmation/.test(invalidResult.stderr),
  'runtime must reject profile contracts that violate schema-level confirmation invariants',
);
fs.rmSync(temp, { recursive: true, force: true });
console.log('runtime profile tests: pass');
