#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

const appender = path.resolve(__dirname, '..', 'scripts', 'append-dispatch.cjs');
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'arcanum-ledger-lock-'));
const tempRoot = path.join(root, '.arcanum', 'runtime', 'subagents-strategy');
fs.mkdirSync(tempRoot, { recursive: true });
const record = {
  dispatch_id: 'concurrent-identical-dispatch', schema_version: '0.6.1', dispatch_type: 'review',
  goal: 'Prove cross-process ledger serialization.', context: 'Eight concurrent registrars submit identical confirmed bytes.',
  max_loops: 1, final_approver: 'parent', output_mode: 'inline',
  groups: [{ group_id: 'worker', agents: [{ agent_name: null, role: 'writer', model: 'gpt-5.6-sol', token_budget: 100, initial_prompt: 'Write one receipt.' }] }],
  connections: [], invoked_by: 'concurrency@example.invalid'
};
const bytes = JSON.stringify(record);
const sources = Array.from({ length: 8 }, (_, index) => {
  const source = path.join(tempRoot, `concurrent-${index}.tmp.json`);
  fs.writeFileSync(source, bytes);
  return source;
});
function run(source) {
  return new Promise((resolve) => {
    const child = spawn(process.execPath, [appender, '--consume', source], {
      env: Object.assign({}, process.env, { ARCANUM_PROJECT_DIR: root }), stdio: ['ignore', 'pipe', 'pipe']
    });
    let stdout = '', stderr = '';
    child.stdout.on('data', (chunk) => { stdout += chunk; });
    child.stderr.on('data', (chunk) => { stderr += chunk; });
    child.on('close', (status) => resolve({ status, stdout, stderr }));
  });
}
(async () => {
  try {
    const results = await Promise.all(sources.map(run));
    const failed = results.filter((result) => result.status !== 0);
    const ledger = fs.readFileSync(path.join(root, '.arcanum', 'observability', 'subagents-strategy', 'subagents-dispatch.yaml'), 'utf8');
    const rows = (ledger.match(/^  - dispatch_id: "concurrent-identical-dispatch"$/gm) || []).length;
    const leftovers = sources.filter((source) => fs.existsSync(source));
    if (failed.length || rows !== 1 || leftovers.length) {
      console.error(JSON.stringify({ failed, rows, leftovers }, null, 2));
      process.exitCode = 1;
    } else console.log('concurrency lock: 8 callers, one exact row, all temporary files consumed');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
})();
