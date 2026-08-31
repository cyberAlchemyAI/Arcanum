#!/usr/bin/env node
'use strict';

// Composite, non-mutating confirmation-readiness gate for Arcanum strategy
// sheets. Registration delegates here; this file never writes the ledger.
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const src = process.argv[2] ? path.resolve(process.argv[2]) : null;
if (!src || process.argv.length !== 3) {
  console.error('usage: node validate-readiness.cjs <record.tmp.json>');
  process.exit(2);
}

let bytes, rec;
try {
  bytes = fs.readFileSync(src);
  rec = JSON.parse(bytes.toString('utf8').replace(/^\uFEFF/, ''));
} catch (error) {
  console.error('cannot read/parse readiness record:', error.message);
  process.exit(2);
}

const repoRoot = path.resolve(__dirname, '..', '..', '..');
const projectRoot = path.resolve(
  process.env.ARCANUM_PROJECT_DIR || process.env.CODEX_PROJECT_DIR ||
  process.env.CLAUDE_PROJECT_DIR || rec.project_dir || process.cwd()
);
const profilePath = path.join(repoRoot, 'arcana', 'subagent-strategy', 'profiles', 'arcanum.yaml');
const poolPath = path.join(repoRoot, 'telemetry', 'agents', 'agent-pool.yaml');
const appender = path.join(__dirname, 'append-dispatch.cjs');
const errs = [];

const schema = spawnSync(process.execPath, [appender, '--schema-check', src], {
  cwd: projectRoot,
  env: Object.assign({}, process.env, { ARCANUM_PROJECT_DIR: projectRoot }),
  encoding: 'utf8',
});
if (schema.status !== 0) {
  process.stderr.write(schema.stderr || schema.stdout || 'strategy sheet schema validation failed\n');
  process.exit(schema.status || 2);
}

function parseProfile(text) {
  const dispatchTypes = new Map();
  let inTypes = false;
  let current = null;
  for (const line of text.split(/\r?\n/)) {
    if (line === 'dispatch_types:') { inTypes = true; current = null; continue; }
    if (inTypes && /^\S/.test(line) && line !== 'dispatch_types:') { inTypes = false; current = null; }
    const type = inTypes ? /^  ([a-z_]+):\s*$/.exec(line) : null;
    if (type) { current = { status: null, owner_capability: null }; dispatchTypes.set(type[1], current); continue; }
    if (current) {
      const field = /^    (status|owner_capability):\s*(.*?)\s*$/.exec(line);
      if (field) current[field[1]] = field[2] === 'null' ? null : field[2];
    }
  }
  const modelsLine = /^\s*allowed_models:\s*\[(.*?)\]\s*$/m.exec(text);
  const allowedModels = modelsLine ? modelsLine[1].split(',').map((x) => x.trim()).filter(Boolean) : [];
  return { dispatchTypes, allowedModels };
}

function parseAgentPool(text) {
  const pool = new Map();
  let currentName = null;
  for (const line of text.split(/\r?\n/)) {
    const named = /^\s*- name:\s*("(?:[^"\\]|\\.)*")\s*$/.exec(line);
    if (named) {
      try { currentName = JSON.parse(named[1]); } catch (_) { currentName = null; }
      continue;
    }
    const roles = currentName ? /^\s*role_fit:\s*\[(.*?)\]\s*$/.exec(line) : null;
    if (roles) {
      pool.set(currentName, new Set(roles[1].split(',').map((x) => x.trim()).filter(Boolean)));
      currentName = null;
    }
  }
  return pool;
}

let profile, pool;
try {
  profile = parseProfile(fs.readFileSync(profilePath, 'utf8'));
  pool = parseAgentPool(fs.readFileSync(poolPath, 'utf8'));
} catch (error) {
  console.error('cannot load readiness authorities:', error.message);
  process.exit(2);
}

const type = profile.dispatchTypes.get(rec.dispatch_type);
if (!type || type.status !== 'live' || !type.owner_capability) {
  errs.push(`dispatch_type ${JSON.stringify(rec.dispatch_type)} has no live owner in ${path.relative(repoRoot, profilePath)}`);
} else if (!fs.existsSync(path.join(repoRoot, type.owner_capability))) {
  errs.push(`live owner capability does not exist: ${type.owner_capability}`);
}

const identities = new Set();
for (let gi = 0; gi < rec.groups.length; gi++) {
  const group = rec.groups[gi];
  const agents = group.agents;
  for (let ai = 0; ai < agents.length; ai++) {
    const agent = agents[ai];
    if (profile.allowedModels.length > 0 && !profile.allowedModels.includes(agent.model)) {
      errs.push(`groups[${gi}].agents[${ai}].model is not admitted by the runtime profile`);
    }
    if (agent.agent_name != null) {
      if (identities.has(agent.agent_name)) errs.push(`agent identity is duplicated: ${JSON.stringify(agent.agent_name)}`);
      identities.add(agent.agent_name);
      const fits = pool.get(agent.agent_name);
      if (!fits) errs.push(`agent identity is not present in the configured pool: ${JSON.stringify(agent.agent_name)}`);
      else if (!fits.has(agent.role)) errs.push(`agent ${JSON.stringify(agent.agent_name)} does not declare role ${JSON.stringify(agent.role)}`);
    }
  }

  if (agents.length >= 2) {
    const expected = new Set();
    for (let a = 0; a < agents.length; a++) for (let b = a + 1; b < agents.length; b++) expected.add(`${a}:${b}`);
    const seen = new Set();
    const records = group.predicted_disagreements;
    if (Array.isArray(records)) {
      for (let pi = 0; pi < records.length; pi++) {
        const item = records[pi];
        if (!item || typeof item !== 'object' || Array.isArray(item)) {
          errs.push(`groups[${gi}].predicted_disagreements[${pi}] must be an object`); continue;
        }
        const keys = Object.keys(item).sort().join(',');
        if (keys !== 'between,question') errs.push(`groups[${gi}].predicted_disagreements[${pi}] must contain exactly between and question`);
        if (!Array.isArray(item.between) || item.between.length !== 2 ||
            !item.between.every(Number.isInteger) || item.between[0] >= item.between[1] ||
            item.between[0] < 0 || item.between[1] >= agents.length) {
          errs.push(`groups[${gi}].predicted_disagreements[${pi}].between must be ordered agent indexes`); continue;
        }
        const pair = `${item.between[0]}:${item.between[1]}`;
        if (seen.has(pair)) errs.push(`groups[${gi}] repeats predicted disagreement pair ${pair}`);
        seen.add(pair);
        if (typeof item.question !== 'string' || item.question.trim() === '') errs.push(`groups[${gi}].predicted_disagreements[${pi}].question must be non-empty`);
      }
    }
    for (const pair of expected) if (!seen.has(pair)) errs.push(`groups[${gi}] is missing predicted disagreement pair ${pair}`);
    for (const pair of seen) if (!expected.has(pair)) errs.push(`groups[${gi}] declares invalid predicted disagreement pair ${pair}`);
  }
}

if (rec.final_approver !== 'parent') {
  const matches = [];
  for (const group of rec.groups) for (const agent of group.agents) {
    if (agent.agent_name === rec.final_approver) matches.push({ group, agent });
  }
  if (matches.length !== 1 || matches[0].agent.role !== 'auditor' || matches[0].group.agents.length !== 1) {
    errs.push('final_approver must be parent or one named auditor in a dedicated one-agent group');
  }
}

if (rec.execution_projection_sha256 !== undefined && !/^[a-f0-9]{64}$/.test(rec.execution_projection_sha256)) {
  errs.push('execution_projection_sha256 must be a lowercase SHA-256');
}

const tempRoot = path.join(projectRoot, '.arcanum', 'runtime', 'subagents-strategy');
const relative = path.relative(path.resolve(tempRoot), src);
if (relative === '..' || relative.startsWith('..' + path.sep) || path.isAbsolute(relative) || !src.endsWith('.tmp.json')) {
  errs.push(`strategy sheet must be a *.tmp.json file below ${tempRoot}`);
}

if (errs.length > 0) {
  console.error('confirmation readiness blocked:');
  for (const err of errs) console.error('  - ' + err);
  process.exit(2);
}

console.log(JSON.stringify({
  status: 'pass',
  mode: 'confirmation-readiness',
  schema_version: rec.schema_version,
  sheet_sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
  execution_projection_sha256: rec.execution_projection_sha256 || null,
  obligations: [
    'form-and-version', 'live-type-owner-prerequisites',
    'agent-eligibility-and-identity-uniqueness', 'final-approver-admission',
    'digest-owned-tension-evidence', 'publication-boundary'
  ],
}));
