'use strict';

const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const test = require('node:test');

const inventoryRoot = path.resolve(__dirname, '..');
const syncScript = path.join(inventoryRoot, 'scripts', 'sync-runtime.sh');
const consumerFixture = path.join(__dirname, 'fixtures', 'runtime-sync', 'consumer-state');
const consumerPaths = [
  'index.json', 'index.md', 'schema.md', 'tags.md', 'log.md',
  'entries/owned.md', 'queries/owned.md', 'raw/owned.txt', 'receipts/owned.json',
];

function digest(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function snapshot(root, relativePaths = null) {
  const paths = relativePaths || fs.readdirSync(root, { recursive: true })
    .filter((relative) => fs.statSync(path.join(root, relative)).isFile());
  const output = {};
  for (const relative of paths) {
    output[relative] = digest(fs.readFileSync(path.join(root, relative)));
  }
  return output;
}

function runSync(target, mode) {
  const result = spawnSync('bash', [
    syncScript,
    mode === 'check' ? '--check' : '--apply',
    '--target',
    target,
    '--json',
  ], { encoding: 'utf8' });
  return {
    ...result,
    report: result.stdout ? JSON.parse(result.stdout) : null,
  };
}

function withTarget(callback) {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'inventory-sync-'));
  const target = path.join(temporary, '.arcanum', 'inventory');
  fs.mkdirSync(target, { recursive: true });
  fs.cpSync(consumerFixture, target, { recursive: true });
  try {
    callback(target);
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }
}

test('check reports exact missing members and writes nothing', () => {
  withTarget((target) => {
    const before = snapshot(target);
    const result = runSync(target, 'check');
    assert.equal(result.status, 1);
    assert.equal(result.report.status, 'drift');
    assert.deepEqual(result.report.before.drifted, []);
    assert.deepEqual(result.report.before.extra_managed, []);
    assert.equal(result.report.before.missing.includes('runtime-manifest.json'), true);
    assert.equal(result.report.before.missing.includes('bin/inventory'), true);
    assert.deepEqual(snapshot(target), before);
    assert.deepEqual(result.report.changed_paths, []);
  });
});

test('apply installs only managed members and reaches clean check state', () => {
  withTarget((target) => {
    const consumerBefore = snapshot(target, consumerPaths);
    const applied = runSync(target, 'apply');
    assert.equal(applied.status, 0, applied.stderr);
    assert.equal(applied.report.status, 'applied');
    assert.deepEqual(applied.report.after, {
      missing: [],
      drifted: [],
      extra_managed: [],
    });
    assert.deepEqual(snapshot(target, consumerPaths), consumerBefore);

    const checked = runSync(target, 'check');
    assert.equal(checked.status, 0, checked.stderr);
    assert.equal(checked.report.status, 'clean');
    assert.deepEqual(checked.report.changed_paths, []);
  });
});

test('check distinguishes missing, drifted, and extra-managed paths', () => {
  withTarget((target) => {
    assert.equal(runSync(target, 'apply').status, 0);
    fs.rmSync(path.join(target, 'schemas', 'inventory.operation-receipt.v1.schema.json'));
    fs.writeFileSync(path.join(target, 'lib', 'inventory-update.cjs'), 'drift\n');
    fs.writeFileSync(path.join(target, 'lib', 'extra-managed.cjs'), 'extra\n');

    const checked = runSync(target, 'check');
    assert.equal(checked.status, 1);
    assert.deepEqual(checked.report.before.missing, [
      'schemas/inventory.operation-receipt.v1.schema.json',
    ]);
    assert.deepEqual(checked.report.before.drifted, [
      'lib/inventory-update.cjs',
    ]);
    assert.deepEqual(checked.report.before.extra_managed, [
      'lib/extra-managed.cjs',
    ]);
  });
});

test('apply repairs drift and removes only extra files in managed roots', () => {
  withTarget((target) => {
    assert.equal(runSync(target, 'apply').status, 0);
    const consumerBefore = snapshot(target, consumerPaths);
    fs.writeFileSync(path.join(target, 'lib', 'inventory-update.cjs'), 'drift\n');
    fs.writeFileSync(path.join(target, 'lib', 'extra-managed.cjs'), 'extra\n');

    const applied = runSync(target, 'apply');
    assert.equal(applied.status, 0, applied.stderr);
    assert.equal(applied.report.changed_paths.includes('lib/inventory-update.cjs'), true);
    assert.equal(applied.report.changed_paths.includes('lib/extra-managed.cjs'), true);
    assert.equal(fs.existsSync(path.join(target, 'lib', 'extra-managed.cjs')), false);
    assert.deepEqual(snapshot(target, consumerPaths), consumerBefore);
    assert.equal(runSync(target, 'check').status, 0);
  });
});

test('canonical manifest excludes every consumer-owned root', () => {
  const manifest = JSON.parse(
    fs.readFileSync(path.join(inventoryRoot, 'runtime-manifest.json'), 'utf8'),
  );
  const paths = [
    ...manifest.members.map((member) => member.path),
    ...manifest.managed_files,
    ...manifest.managed_roots,
  ];
  for (const forbidden of [
    'entries', 'queries', 'raw', 'receipts',
    'index.json', 'index.md', 'schema.md', 'tags.md', 'log.md',
  ]) {
    assert.equal(
      paths.some((value) => value === forbidden || value.startsWith(`${forbidden}/`)),
      false,
      `${forbidden} must stay consumer-owned`,
    );
  }
});
