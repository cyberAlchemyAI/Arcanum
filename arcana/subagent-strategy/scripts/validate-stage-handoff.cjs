#!/usr/bin/env node
'use strict';

const fs = require('fs');
const source = process.argv[2];
if (!source || process.argv.length !== 3) {
  console.error('usage: node validate-stage-handoff.cjs <handoff.json>');
  process.exit(2);
}
let value;
try { value = JSON.parse(fs.readFileSync(source, 'utf8').replace(/^\uFEFF/, '')); }
catch (error) { console.error('cannot read/parse stage handoff:', error.message); process.exit(2); }
const errors = [];
const isText = (item) => typeof item === 'string' && item.trim() !== '';
if (!value || typeof value !== 'object' || Array.isArray(value)) errors.push('handoff must be an object');
else {
  const allowed = new Set(['schema_version', 'dispatch_id', 'dispatch_type', 'from_group', 'to_group', 'verdict', 'evidence_refs', 'typed_defect', 'repair_owner_group', 'edge', 'remaining_loops', 'reason']);
  for (const key of Object.keys(value)) if (!allowed.has(key)) errors.push(`unknown handoff key ${JSON.stringify(key)}`);
  if (value.schema_version !== 'arcanum.stage-handoff.v0.1') errors.push('schema_version must be arcanum.stage-handoff.v0.1');
  for (const key of ['dispatch_id', 'dispatch_type', 'from_group', 'to_group']) if (!isText(value[key])) errors.push(`${key} must be a non-empty string`);
  if (!['ready', 'needs_feedback', 'blocked', 'not_applicable'].includes(value.verdict)) errors.push('verdict must be ready, needs_feedback, blocked, or not_applicable');
  if (!Array.isArray(value.evidence_refs) || value.evidence_refs.some((item) => !isText(item))) errors.push('evidence_refs must be an array of non-empty strings');
  if (value.verdict === 'needs_feedback') {
    for (const key of ['typed_defect', 'repair_owner_group', 'edge']) if (!isText(value[key])) errors.push(`${key} is required for needs_feedback`);
    if (!Number.isInteger(value.remaining_loops) || value.remaining_loops < 1) errors.push('remaining_loops must be a positive integer for needs_feedback');
  }
  if (value.verdict === 'not_applicable' && !isText(value.reason)) errors.push('reason is required for not_applicable');
}
if (errors.length) {
  console.error('stage handoff blocked:');
  for (const error of errors) console.error('  - ' + error);
  process.exit(2);
}
console.log(JSON.stringify({ status: 'pass', schema_version: value.schema_version, dispatch_id: value.dispatch_id, verdict: value.verdict }));
