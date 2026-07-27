'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const test = require('node:test');

const { runAppendApply } = require('../lib/inventory-update.cjs');

const inventorySource = path.resolve(__dirname, '..');
const fixtureSource = path.join(__dirname, 'fixtures', 'append-dry-run');
const applyFixtureSource = path.join(__dirname, 'fixtures', 'append-apply');
const timestamp = '2026-07-24T18:19:00Z';

function makeInstalledFixture() {
  const repository = fs.mkdtempSync(path.join(os.tmpdir(), 'inventory-apply-'));
  const inventoryRoot = path.join(repository, '.arcanum', 'inventory');
  fs.mkdirSync(inventoryRoot, { recursive: true });
  for (const member of ['bin', 'lib', 'schemas', 'scripts']) {
    fs.cpSync(path.join(inventorySource, member), path.join(inventoryRoot, member), {
      recursive: true,
    });
  }
  fs.cpSync(fixtureSource, inventoryRoot, { recursive: true });
  fs.cpSync(applyFixtureSource, inventoryRoot, { recursive: true });
  const unrelated = path.join(repository, 'unrelated');
  fs.mkdirSync(unrelated);
  return {
    repository,
    inventoryRoot,
    unrelated,
    recordPath: path.join(inventoryRoot, 'requests', 'apply.json'),
    indexPath: path.join(inventoryRoot, 'index.json'),
    humanPath: path.join(inventoryRoot, 'index.md'),
  };
}

function withFixture(callback) {
  const fixture = makeInstalledFixture();
  try {
    callback(fixture);
  } finally {
    fs.rmSync(fixture.repository, { recursive: true, force: true });
  }
}

function baselineBytes(fixture) {
  return {
    index: fs.readFileSync(fixture.indexPath),
    human: fs.readFileSync(fixture.humanPath),
  };
}

test('CLI apply observes exact candidate digests and commits both projections', () => {
  withFixture((fixture) => {
    const cli = path.join(fixture.inventoryRoot, 'bin', 'inventory');
    const result = spawnSync(process.execPath, [
      cli,
      'append',
      '--record',
      fixture.recordPath,
      '--timestamp',
      timestamp,
      '--apply',
      '--json',
    ], {
      cwd: fixture.unrelated,
      encoding: 'utf8',
    });
    assert.equal(result.status, 0, result.stderr);
    const receipt = JSON.parse(result.stdout);
    assert.equal(receipt.status, 'applied');
    assert.equal(receipt.write.attempted, true);
    assert.equal(receipt.write.committed, true);
    assert.deepEqual(
      receipt.write.expected_postwrite_digests,
      receipt.write.actual_postwrite_digests,
    );
    const index = JSON.parse(fs.readFileSync(fixture.indexPath, 'utf8'));
    assert.equal(index.indexes.by_id['apply-record'], 'wiki/apply.md');
  });
});

test('baseline drift immediately before write blocks without runtime writes', () => {
  withFixture((fixture) => {
    const before = baselineBytes(fixture);
    const result = runAppendApply({
      inventoryRoot: fixture.inventoryRoot,
      recordPath: fixture.recordPath,
      timestampInput: timestamp,
      hooks: {
        beforeWrite() {
          fs.appendFileSync(fixture.indexPath, ' ');
        },
      },
    });
    assert.equal(result.receipt.status, 'baseline-blocked');
    assert.equal(result.receipt.reason_code, 'baseline-drift-before-write');
    assert.equal(result.receipt.write.attempted, false);
    assert.deepEqual(fs.readFileSync(fixture.humanPath), before.human);
    assert.equal(fs.readFileSync(fixture.indexPath).length, before.index.length + 1);
  });
});

test('first-write failure is distinct and observes no changed projection', () => {
  withFixture((fixture) => {
    const before = baselineBytes(fixture);
    const result = runAppendApply({
      inventoryRoot: fixture.inventoryRoot,
      recordPath: fixture.recordPath,
      timestampInput: timestamp,
      hooks: { failBeforePath: 'index.json' },
    });
    assert.equal(result.receipt.status, 'write-failed');
    assert.equal(result.receipt.reason_code, 'index-json-write-failed');
    assert.equal(result.receipt.write.committed, false);
    assert.deepEqual(result.receipt.write.observed_changed_paths, []);
    assert.equal(result.receipt.write.possible_partial_mutation, true);
    assert.equal(result.receipt.write.repair_required, true);
    assert.deepEqual(fs.readFileSync(fixture.indexPath), before.index);
    assert.deepEqual(fs.readFileSync(fixture.humanPath), before.human);
  });
});

test('second-write failure exposes the exact partial mutation', () => {
  withFixture((fixture) => {
    const before = baselineBytes(fixture);
    const result = runAppendApply({
      inventoryRoot: fixture.inventoryRoot,
      recordPath: fixture.recordPath,
      timestampInput: timestamp,
      hooks: { failBeforePath: 'index.md' },
    });
    assert.equal(result.receipt.status, 'write-failed');
    assert.equal(result.receipt.reason_code, 'index-md-write-failed');
    assert.deepEqual(result.receipt.write.observed_changed_paths, ['index.json']);
    assert.notDeepEqual(fs.readFileSync(fixture.indexPath), before.index);
    assert.deepEqual(fs.readFileSync(fixture.humanPath), before.human);
    assert.match(result.receipt.residue.join('\n'), /restore-both-projections/);
  });
});

test('postwrite alteration yields digest mismatch and repair residue', () => {
  withFixture((fixture) => {
    const result = runAppendApply({
      inventoryRoot: fixture.inventoryRoot,
      recordPath: fixture.recordPath,
      timestampInput: timestamp,
      hooks: {
        afterWrites() {
          fs.appendFileSync(fixture.humanPath, 'altered-after-write\n');
        },
      },
    });
    assert.equal(result.receipt.status, 'postwrite-digest-mismatch');
    assert.equal(result.receipt.write.committed, false);
    assert.equal(result.receipt.write.possible_partial_mutation, true);
    assert.equal(result.receipt.write.repair_required, true);
    assert.notEqual(
      result.receipt.write.expected_postwrite_digests['index.md'],
      result.receipt.write.actual_postwrite_digests['index.md'],
    );
  });
});
