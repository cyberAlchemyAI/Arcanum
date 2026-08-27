#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const guard = path.resolve(__dirname, '..', 'scripts', 'enforce-append-only-dispatch.cjs');
const handoff = path.resolve(__dirname, '..', 'scripts', 'validate-stage-handoff.cjs');
let failures = 0;
function check(name, condition, detail) {
  if (condition) console.log('PASS ' + name);
  else { failures++; console.error('FAIL ' + name + (detail ? ': ' + detail : '')); }
}
function hook(payload) {
  return spawnSync(process.execPath, [guard], { input: JSON.stringify(payload), encoding: 'utf8' });
}
const denied = hook({ tool_name: 'Write', tool_input: { file_path: 'C:\\repo\\.arcanum\\observability\\subagents-strategy\\subagents-dispatch.yaml' } });
check('direct cross-platform ledger write is denied', /"permissionDecision":"deny"/.test(denied.stdout), denied.stdout);
const read = hook({ tool_name: 'PowerShell', tool_input: { command: 'Get-Content .arcanum/observability/subagents-strategy/subagents-dispatch.yaml' } });
check('read-only ledger command is allowed', read.status === 0 && read.stdout === '', read.stdout);
const shellWrite = hook({ tool_name: 'Bash', tool_input: { command: 'echo x >> .arcanum/observability/subagents-strategy/subagents-dispatch.yaml' } });
check('shell redirection to ledger is denied', /"permissionDecision":"deny"/.test(shellWrite.stdout), shellWrite.stdout);

const root = fs.mkdtempSync(path.join(os.tmpdir(), 'arcanum-handoff-'));
try {
  const validPath = path.join(root, 'valid.json');
  fs.writeFileSync(validPath, JSON.stringify({ schema_version: 'arcanum.stage-handoff.v0.1', dispatch_id: 'd', dispatch_type: 'review', from_group: 'attackers', to_group: 'writer', verdict: 'ready', evidence_refs: ['review/input.md'] }));
  const valid = spawnSync(process.execPath, [handoff, validPath], { encoding: 'utf8' });
  check('valid stage handoff passes', valid.status === 0, valid.stderr);
  const invalidPath = path.join(root, 'invalid.json');
  fs.writeFileSync(invalidPath, JSON.stringify({ schema_version: 'arcanum.stage-handoff.v0.1', dispatch_id: 'd', dispatch_type: 'review', from_group: 'writer', to_group: 'attackers', verdict: 'needs_feedback', evidence_refs: [] }));
  const invalid = spawnSync(process.execPath, [handoff, invalidPath], { encoding: 'utf8' });
  check('unbound feedback handoff is blocked', invalid.status === 2 && /typed_defect/.test(invalid.stderr), invalid.stderr);
} finally { fs.rmSync(root, { recursive: true, force: true }); }
if (failures) process.exit(1);
