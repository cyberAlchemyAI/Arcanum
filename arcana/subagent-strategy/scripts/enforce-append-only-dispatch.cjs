#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const LEDGER_SUFFIX = '.arcanum/observability/subagents-strategy/subagents-dispatch.yaml';
const REASON = `${LEDGER_SUFFIX} is append-only; use append-dispatch.cjs for dispatch and close rows.`;
const canon = (value) => path.posix.normalize(String(value).trim().split('\\').join('/').toLowerCase());

function targetsLedger(input) {
  const target = input.file_path || input.notebook_path;
  return target != null && canon(target).endsWith(LEDGER_SUFFIX);
}
function isReadOnly(command) {
  if (/[<>]/.test(command) || /\|\s*(tee|set-content|add-content|out-file)\b/i.test(command)) return false;
  if (/\b(tee|sed|awk|perl|rm|mv|cp|del|truncate|set-content|add-content|out-file|clear-content|remove-item|move-item|copy-item|new-item)\b/i.test(command)) return false;
  const words = command.trim().split(/\s+/);
  const first = (words[0] || '').toLowerCase().replace(/\.exe$/, '');
  if (['cat', 'get-content', 'gc', 'rg', 'grep', 'head', 'tail', 'ls', 'dir', 'get-childitem', 'gci', 'stat', 'wc', 'less', 'more', 'select-string', 'sls', 'jq', 'yq', 'file', 'type'].includes(first)) return true;
  if (first === 'git') return ['diff', 'show', 'log', 'status', 'add', 'blame', 'cat-file'].includes((words[1] || '').toLowerCase());
  return false;
}
try {
  const payload = JSON.parse(fs.readFileSync(0, 'utf8'));
  const name = payload.tool_name || '';
  const input = payload.tool_input || {};
  let deny = ['Edit', 'MultiEdit', 'Write', 'NotebookEdit'].includes(name) && targetsLedger(input);
  if (['Bash', 'PowerShell'].includes(name) && canon(input.command || '').includes('subagents-dispatch.yaml')) deny = !isReadOnly(String(input.command || ''));
  if (deny) process.stdout.write(JSON.stringify({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'deny', permissionDecisionReason: REASON } }));
} catch (_) { /* fail open for unrelated work */ }
process.exit(0);
