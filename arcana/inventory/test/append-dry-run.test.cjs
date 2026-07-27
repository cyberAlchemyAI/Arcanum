'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const test = require('node:test');

const inventorySource = path.resolve(__dirname, '..');
const fixtureSource = path.join(__dirname, 'fixtures', 'append-dry-run');
const timestamp = '2026-07-24T18:19:00Z';

function makeInstalledFixture() {
  const repository = fs.mkdtempSync(path.join(os.tmpdir(), 'inventory-installed-'));
  const inventoryRoot = path.join(repository, '.arcanum', 'inventory');
  fs.mkdirSync(inventoryRoot, { recursive: true });
  for (const member of ['bin', 'lib', 'schemas', 'scripts']) {
    fs.cpSync(path.join(inventorySource, member), path.join(inventoryRoot, member), {
      recursive: true,
    });
  }
  fs.cpSync(fixtureSource, inventoryRoot, { recursive: true });
  const unrelated = path.join(repository, 'unrelated', 'working-directory');
  fs.mkdirSync(unrelated, { recursive: true });
  return { repository, inventoryRoot, unrelated };
}

function runAppend(fixture, requestName) {
  const cli = path.join(fixture.inventoryRoot, 'bin', 'inventory');
  const record = path.join(fixture.inventoryRoot, 'requests', requestName);
  const result = spawnSync(process.execPath, [
    cli,
    'append',
    '--record',
    record,
    '--timestamp',
    timestamp,
    '--dry-run',
    '--json',
  ], {
    cwd: fixture.unrelated,
    encoding: 'utf8',
  });
  return {
    ...result,
    receipt: result.stdout ? JSON.parse(result.stdout) : null,
  };
}

function boundBytes(fixture) {
  return {
    index: fs.readFileSync(path.join(fixture.inventoryRoot, 'index.json')),
    human: fs.readFileSync(path.join(fixture.inventoryRoot, 'index.md')),
  };
}

function assertUnchanged(fixture, before) {
  assert.deepEqual(fs.readFileSync(path.join(fixture.inventoryRoot, 'index.json')), before.index);
  assert.deepEqual(fs.readFileSync(path.join(fixture.inventoryRoot, 'index.md')), before.human);
}

function withFixture(callback) {
  const fixture = makeInstalledFixture();
  try {
    callback(fixture);
  } finally {
    fs.rmSync(fixture.repository, { recursive: true, force: true });
  }
}

test('package-relative dry run succeeds from unrelated working directory', () => {
  withFixture((fixture) => {
    const before = boundBytes(fixture);
    const result = runAppend(fixture, 'add.json');
    assert.equal(result.status, 0, result.stderr);
    assert.equal(result.receipt.status, 'dry-run-ready');
    assert.equal(result.receipt.runtime.evidence_state, 'observed');
    assert.equal(result.receipt.write.attempted, false);
    assert.deepEqual(
      result.receipt.write.expected_postwrite_digests,
      result.receipt.write.actual_postwrite_digests,
    );
    assertUnchanged(fixture, before);
  });
});

test('repeated dry runs are byte-identical and mutation-free', () => {
  withFixture((fixture) => {
    const before = boundBytes(fixture);
    const first = runAppend(fixture, 'add.json');
    const second = runAppend(fixture, 'add.json');
    assert.equal(first.stdout, second.stdout);
    assertUnchanged(fixture, before);
  });
});

test('warning delta attributes exactly one introduced warning', () => {
  withFixture((fixture) => {
    const before = boundBytes(fixture);
    const result = runAppend(fixture, 'warning.json');
    assert.equal(result.status, 0, result.stderr);
    assert.equal(result.receipt.warning_delta.introduced.length, 1);
    assert.match(result.receipt.warning_delta.introduced[0], /new-warning/);
    assert.equal(result.receipt.warning_delta.resolved.length, 0);
    assert.equal(result.receipt.warning_delta.inherited_count, 0);
    assertUnchanged(fixture, before);
  });
});

test('identical no-op and ID conflict are distinct deterministic receipts', () => {
  withFixture((fixture) => {
    const before = boundBytes(fixture);
    const identical = runAppend(fixture, 'identical.json');
    const conflict = runAppend(fixture, 'conflict.json');
    assert.equal(identical.status, 0);
    assert.equal(identical.receipt.status, 'identical-no-op');
    assert.equal(conflict.status, 1);
    assert.equal(conflict.receipt.status, 'id-conflict');
    assert.notEqual(identical.stdout, conflict.stdout);
    assertUnchanged(fixture, before);
  });
});

test('invalid request and candidate block emit receipts without mutation', () => {
  withFixture((fixture) => {
    const before = boundBytes(fixture);
    const invalid = runAppend(fixture, 'invalid.json');
    const blocked = runAppend(fixture, 'missing-path.json');
    assert.equal(invalid.status, 1);
    assert.equal(invalid.receipt.status, 'invalid-request');
    assert.equal(invalid.receipt.inputs.evidence_state, 'partial');
    assert.equal(blocked.status, 1);
    assert.equal(blocked.receipt.status, 'candidate-blocked');
    assertUnchanged(fixture, before);
  });
});

test('baseline block precedes request processing and preserves targets', () => {
  withFixture((fixture) => {
    const indexPath = path.join(fixture.inventoryRoot, 'index.json');
    const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
    index.indexes.by_id.existing = 'entries/wrong.md';
    fs.writeFileSync(indexPath, `${JSON.stringify(index, null, 2)}\n`);
    const before = boundBytes(fixture);
    const result = runAppend(fixture, 'invalid.json');
    assert.equal(result.status, 1);
    assert.equal(result.receipt.status, 'baseline-blocked');
    assert.equal(result.receipt.inputs.record_sha256, null);
    assert.equal(result.receipt.candidate.evidence_state, 'not-reached');
    assertUnchanged(fixture, before);
  });
});

test('missing runtime helper yields a phase-accurate tooling receipt', () => {
  withFixture((fixture) => {
    const validator = path.join(
      fixture.inventoryRoot,
      'scripts',
      'validate_projection_conformance.py',
    );
    fs.rmSync(validator);
    const before = boundBytes(fixture);
    const first = runAppend(fixture, 'add.json');
    const second = runAppend(fixture, 'add.json');
    assert.equal(first.status, 1);
    assert.equal(first.receipt.status, 'tooling-unavailable');
    assert.equal(first.receipt.runtime.evidence_state, 'partial');
    assert.equal(first.receipt.runtime.bundle_sha256, null);
    assert.equal(first.stdout, second.stdout);
    assertUnchanged(fixture, before);
  });
});

test('stdout is exactly one receipt and diagnostics do not depend on caller CWD', () => {
  withFixture((fixture) => {
    const result = runAppend(fixture, 'add.json');
    assert.equal(result.stderr, '');
    assert.equal(result.stdout.endsWith('\n'), true);
    assert.equal(result.stdout.endsWith('\n\n'), false);
    assert.doesNotMatch(result.stdout, new RegExp(fixture.repository.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
    assert.equal(result.receipt.authority_boundary, 'inventory-read-model-only');
  });
});
