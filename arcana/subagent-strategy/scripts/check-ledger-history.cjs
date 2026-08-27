#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const root = path.resolve(process.env.ARCANUM_PROJECT_DIR || process.cwd());
const ledger = '.arcanum/observability/subagents-strategy/subagents-dispatch.yaml';
const base = process.argv[2] || process.env.ARCANUM_LEDGER_BASE;
if (!base || /^0+$/.test(base)) { console.log('append-only history check skipped: no base revision'); process.exit(0); }
const prior = spawnSync('git', ['show', `${base}:${ledger}`], { cwd: root, encoding: null });
if (prior.status !== 0) { console.log('append-only history check: ledger is new at this revision'); process.exit(0); }
const currentPath = path.join(root, ...ledger.split('/'));
if (!fs.existsSync(currentPath)) { console.error('append-only ledger was deleted'); process.exit(2); }
const current = fs.readFileSync(currentPath);
if (current.length < prior.stdout.length || !current.subarray(0, prior.stdout.length).equals(prior.stdout)) {
  console.error('append-only ledger history was edited or truncated; only byte-for-byte suffix appends are allowed');
  process.exit(2);
}
console.log('append-only ledger history preserved');
