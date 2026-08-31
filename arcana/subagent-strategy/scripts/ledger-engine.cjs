#!/usr/bin/env node
'use strict';

/*
 * Shared append-only registrar mechanics for Subagent Strategy runtime profiles.
 *
 * Profile adapters validate their own forms and render their own ledger rows.
 * This module alone owns governed path resolution, locking, structural history
 * checks, exact-content idempotence, durable append, paired close ordering, and
 * temporary-envelope consumption.
 */

const fs = require('fs');
const path = require('path');

class RegistrationError extends Error {
  constructor(message, code = 2) {
    super(message);
    this.code = code;
  }
}

function isWithin(root, target) {
  const relative = path.relative(root, target);
  return relative === '' || (
    relative !== '..' &&
    !relative.startsWith('..' + path.sep) &&
    !path.isAbsolute(relative)
  );
}

function nearestExisting(candidate) {
  let current = path.resolve(candidate);
  while (!fs.existsSync(current)) {
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }
  return current;
}

function decodeScalar(raw, lineNumber, ledgerPath) {
  try {
    return JSON.parse(raw);
  } catch (_) {
    throw new RegistrationError(
      `ledger structural check failed at ${ledgerPath}:${lineNumber}: value is not valid JSON`,
      1,
    );
  }
}

function parseLedger(text, ledgerPath) {
  const dispatchRows = new Map();
  const closeRows = new Map();
  const rows = [];
  const sourceLines = text.split('\n');
  let sawTop = false;
  let current = null;

  const fail = (lineNumber, message) => {
    throw new RegistrationError(
      `ledger structural check failed at ${ledgerPath}:${lineNumber}: ${message}`,
      1,
    );
  };

  for (let index = 0; index < sourceLines.length; index += 1) {
    const line = sourceLines[index].replace(/\r$/, '');
    if (line === '' || line.startsWith('#')) continue;
    if (line === 'dispatches:') {
      if (sawTop) fail(index + 1, 'duplicate "dispatches:" key');
      sawTop = true;
      continue;
    }
    const match = /^(  - |    )([A-Za-z_][A-Za-z0-9_]*):(?: (.*))?$/.exec(line);
    if (!match) fail(index + 1, 'unrecognized line shape');
    if (!sawTop) fail(index + 1, 'row content before the "dispatches:" key');

    let value;
    if (match[3] === undefined || match[3] === '') {
      const block = [];
      let next = index + 1;
      while (next < sourceLines.length) {
        const continuation = sourceLines[next].replace(/\r$/, '');
        if (continuation === '') {
          next += 1;
          continue;
        }
        if (/^\s*/.exec(continuation)[0].length <= 4) break;
        block.push(continuation.trim());
        next += 1;
      }
      if (block.length === 0) fail(index + 1, `value of "${match[2]}" is empty`);
      value = decodeScalar(
        block.join('\n').replace(/,\s*([}\]])/g, '$1'),
        index + 1,
        ledgerPath,
      );
      index = next - 1;
    } else {
      value = decodeScalar(match[3], index + 1, ledgerPath);
    }

    if (match[1] === '  - ') {
      current = { [match[2]]: value, __line: index + 1, __index: rows.length };
      rows.push(current);
      if (match[2] === 'dispatch_id') {
        if (dispatchRows.has(value)) fail(index + 1, `duplicate dispatch_id ${JSON.stringify(value)}`);
        dispatchRows.set(value, current);
      } else if (match[2] === 'close_of') {
        if (closeRows.has(value)) fail(index + 1, `duplicate close_of ${JSON.stringify(value)}`);
        closeRows.set(value, current);
      } else {
        fail(index + 1, `row must start with dispatch_id or close_of, got "${match[2]}"`);
      }
    } else {
      if (!current) fail(index + 1, 'continuation field appears before a row');
      if (Object.prototype.hasOwnProperty.call(current, match[2])) {
        fail(index + 1, `duplicate row field "${match[2]}"`);
      }
      current[match[2]] = value;
    }
  }

  if (!sawTop) fail(1, 'missing "dispatches:" key');
  for (const [dispatchId, closeRow] of closeRows.entries()) {
    const dispatchRow = dispatchRows.get(dispatchId);
    if (!dispatchRow) fail(closeRow.__line, `close_of ${JSON.stringify(dispatchId)} has no dispatch row`);
    if (closeRow.__index <= dispatchRow.__index) {
      fail(closeRow.__line, `close_of ${JSON.stringify(dispatchId)} precedes its dispatch row`);
    }
  }
  return { dispatchRows, closeRows, rows };
}

function assertGovernedPaths({ projectDir, ledgerPath, tempRoot, sourcePath, consume }) {
  const realProject = fs.realpathSync(projectDir);
  const ledgerParent = path.dirname(ledgerPath);
  const existingParent = fs.realpathSync(nearestExisting(ledgerParent));
  if (!isWithin(realProject, existingParent)) {
    throw new RegistrationError('ledger path escapes the real project root through a symlink or junction');
  }
  fs.mkdirSync(ledgerParent, { recursive: true });
  if (!isWithin(realProject, fs.realpathSync(ledgerParent))) {
    throw new RegistrationError('ledger directory resolves outside the real project root');
  }

  if (!consume) return;
  if (!sourcePath || !tempRoot) {
    throw new RegistrationError('temporary-envelope consumption requires sourcePath and tempRoot');
  }
  fs.mkdirSync(tempRoot, { recursive: true });
  const realSource = fs.realpathSync(sourcePath);
  if (!isWithin(fs.realpathSync(tempRoot), realSource)) {
    throw new RegistrationError('temporary record resolves outside its governed runtime root');
  }
  if (!sourcePath.endsWith('.tmp.json')) {
    throw new RegistrationError('temporary record must use the .tmp.json suffix');
  }
}

const sleepCell = new Int32Array(new SharedArrayBuffer(4));

function processAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return error.code === 'EPERM';
  }
}

function acquireLock(lockPath) {
  const deadline = Date.now() + 15000;
  while (Date.now() < deadline) {
    try {
      const descriptor = fs.openSync(lockPath, 'wx');
      fs.writeFileSync(
        descriptor,
        JSON.stringify({ pid: process.pid, created_at: new Date().toISOString() }),
      );
      fs.closeSync(descriptor);
      return;
    } catch (error) {
      if (error.code !== 'EEXIST') throw error;
      try {
        const stat = fs.statSync(lockPath);
        const lock = JSON.parse(fs.readFileSync(lockPath, 'utf8'));
        if (Date.now() - stat.mtimeMs > 30000 && !processAlive(lock.pid)) {
          fs.unlinkSync(lockPath);
          continue;
        }
      } catch (_) {
        // Another registrar may be replacing a stale lock.
      }
      Atomics.wait(sleepCell, 0, 0, 25);
    }
  }
  throw new RegistrationError(`timed out acquiring ledger lock ${lockPath}`, 1);
}

function appendDurably(ledgerPath, text) {
  const descriptor = fs.openSync(ledgerPath, 'a');
  try {
    fs.writeSync(descriptor, text, null, 'utf8');
    fs.fsyncSync(descriptor);
  } finally {
    fs.closeSync(descriptor);
  }
}

function inspectHistory({ projectDir, ledgerRelative, header }) {
  const root = path.resolve(projectDir);
  const ledgerPath = path.resolve(root, ledgerRelative);
  assertGovernedPaths({ projectDir: root, ledgerPath, consume: false });
  const text = fs.existsSync(ledgerPath) ? fs.readFileSync(ledgerPath, 'utf8') : header;
  const history = parseLedger(text, ledgerPath);
  return { ledgerPath, text, ...history };
}

function mutateRegistration(options) {
  const {
    projectDir: projectInput,
    ledgerRelative,
    tempRootRelative,
    sourcePath: sourceInput,
    consume = false,
    header,
    rowKind,
    identity,
    contentDigest,
    digestField,
    conflictDescription = 'content',
    renderRow,
    beforeAppend,
    receipt = {},
  } = options;
  if (!['dispatch', 'close'].includes(rowKind)) {
    throw new RegistrationError('rowKind must be dispatch or close');
  }
  const projectDir = path.resolve(projectInput);
  const ledgerPath = path.resolve(projectDir, ledgerRelative);
  const tempRoot = path.resolve(projectDir, tempRootRelative);
  const sourcePath = sourceInput ? path.resolve(sourceInput) : null;
  assertGovernedPaths({ projectDir, ledgerPath, tempRoot, sourcePath, consume });

  const lockPath = ledgerPath + '.lock';
  let lockOwned = false;
  try {
    acquireLock(lockPath);
    lockOwned = true;
    try {
      fs.writeFileSync(ledgerPath, header, { flag: 'wx' });
    } catch (error) {
      if (error.code !== 'EEXIST') throw error;
    }
    const existing = fs.readFileSync(ledgerPath, 'utf8');
    const state = parseLedger(existing, ledgerPath);
    const rows = rowKind === 'close' ? state.closeRows : state.dispatchRows;
    const prior = rows.get(identity);
    let appendStatus = 'appended';

    if (prior) {
      if (prior[digestField] !== contentDigest) {
        throw new RegistrationError(
          `${rowKind === 'close' ? 'close_of' : 'dispatch_id'} ${JSON.stringify(identity)} already exists with different ${conflictDescription}; temporary record preserved`,
        );
      }
      appendStatus = 'already_present_identical';
    } else {
      if (rowKind === 'close' && !state.dispatchRows.has(identity)) {
        throw new RegistrationError(`close_of ${JSON.stringify(identity)} has no matching dispatch row`);
      }
      if (beforeAppend) beforeAppend(state);
      const lines = renderRow(new Date().toISOString());
      if (!Array.isArray(lines) || lines.length === 0) {
        throw new RegistrationError('profile adapter rendered no ledger row');
      }
      const newline = existing.length > 0 && !existing.endsWith('\n') ? '\n' : '';
      appendDurably(ledgerPath, newline + lines.join('\n') + '\n');
    }

    let consumed = false;
    if (consume) {
      fs.unlinkSync(sourcePath);
      consumed = true;
    }
    return {
      schema_version: 'arcanum.subagent-strategy-runtime-receipt.v1',
      status: 'pass',
      mode: rowKind === 'close' ? 'close' : 'register',
      append_status: appendStatus,
      identity,
      content_digest: contentDigest,
      ledger: ledgerRelative.split(path.sep).join('/'),
      temporary_envelope_consumed: consumed,
      ...receipt,
    };
  } finally {
    if (lockOwned) {
      try {
        fs.unlinkSync(lockPath);
      } catch (_) {
        // Preserve the primary result if an external actor already removed it.
      }
    }
  }
}

module.exports = {
  RegistrationError,
  inspectHistory,
  mutateRegistration,
  parseLedger,
};
