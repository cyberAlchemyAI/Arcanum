'use strict';

const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const test = require('node:test');

const canonicalRoot = path.resolve(__dirname, '..');
const fixtureRoot = path.join(__dirname, 'fixtures');
const syncScript = path.join(canonicalRoot, 'scripts', 'sync-runtime.sh');
const timestamp = '2026-07-24T18:19:00Z';

function digest(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function sync(target, mode) {
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

function makeConsumer({ applyOverlay = false } = {}) {
  const repository = fs.mkdtempSync(path.join(os.tmpdir(), 'inventory-consumer-proof-'));
  const inventoryRoot = path.join(repository, '.arcanum', 'inventory');
  fs.mkdirSync(inventoryRoot, { recursive: true });
  fs.cpSync(path.join(fixtureRoot, 'append-dry-run'), inventoryRoot, { recursive: true });
  if (applyOverlay) {
    fs.cpSync(path.join(fixtureRoot, 'append-apply'), inventoryRoot, { recursive: true });
  }
  const installed = sync(inventoryRoot, 'apply');
  assert.equal(installed.status, 0, installed.stderr);
  const unrelated = path.join(repository, 'work', 'unrelated');
  fs.mkdirSync(unrelated, { recursive: true });
  return { repository, inventoryRoot, unrelated };
}

function withConsumer(options, callback) {
  const consumer = makeConsumer(options);
  try {
    callback(consumer);
  } finally {
    fs.rmSync(consumer.repository, { recursive: true, force: true });
  }
}

function runCli(consumer, request, mode = 'dry-run') {
  const result = spawnSync(process.execPath, [
    path.join(consumer.inventoryRoot, 'bin', 'inventory'),
    'append',
    '--record',
    path.join(consumer.inventoryRoot, 'requests', request),
    '--timestamp',
    timestamp,
    mode === 'apply' ? '--apply' : '--dry-run',
    '--json',
  ], {
    cwd: consumer.unrelated,
    encoding: 'utf8',
  });
  return {
    ...result,
    receipt: result.stdout ? JSON.parse(result.stdout) : null,
  };
}

function projectionBytes(consumer) {
  return {
    index: fs.readFileSync(path.join(consumer.inventoryRoot, 'index.json')),
    human: fs.readFileSync(path.join(consumer.inventoryRoot, 'index.md')),
  };
}

function installedLibrary(consumer) {
  const modulePath = path.join(consumer.inventoryRoot, 'lib', 'inventory-update.cjs');
  delete require.cache[require.resolve(modulePath)];
  return require(modulePath);
}

test('manifest installs a clean package that runs from unrelated CWD', () => {
  withConsumer({}, (consumer) => {
    const checked = sync(consumer.inventoryRoot, 'check');
    assert.equal(checked.status, 0, checked.stderr);
    assert.equal(checked.report.status, 'clean');
    const result = runCli(consumer, 'add.json');
    assert.equal(result.status, 0, result.stderr);
    assert.equal(result.receipt.status, 'dry-run-ready');
    assert.doesNotMatch(result.stdout, new RegExp(consumer.repository.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
  });
});

test('installed dry runs are deterministic, attributable, and mutation-free', () => {
  withConsumer({}, (consumer) => {
    const before = projectionBytes(consumer);
    const first = runCli(consumer, 'add.json');
    const second = runCli(consumer, 'add.json');
    const warning = runCli(consumer, 'warning.json');
    assert.equal(first.stdout, second.stdout);
    assert.equal(warning.receipt.warning_delta.introduced.length, 1);
    assert.match(warning.receipt.warning_delta.introduced[0], /new-warning/);
    assert.deepEqual(projectionBytes(consumer), before);
  });
});

test('installed no-op and conflict remain distinct', () => {
  withConsumer({}, (consumer) => {
    const before = projectionBytes(consumer);
    const noOp = runCli(consumer, 'identical.json');
    const conflict = runCli(consumer, 'conflict.json');
    assert.equal(noOp.receipt.status, 'identical-no-op');
    assert.equal(conflict.receipt.status, 'id-conflict');
    assert.equal(noOp.status, 0);
    assert.equal(conflict.status, 1);
    assert.deepEqual(projectionBytes(consumer), before);
  });
});

test('installed apply succeeds and injected second-write failure exposes partial state', () => {
  withConsumer({ applyOverlay: true }, (successConsumer) => {
    const applied = runCli(successConsumer, 'apply.json', 'apply');
    assert.equal(applied.status, 0, applied.stderr);
    assert.equal(applied.receipt.status, 'applied');
    assert.equal(applied.receipt.write.committed, true);
  });

  withConsumer({ applyOverlay: true }, (failureConsumer) => {
    const library = installedLibrary(failureConsumer);
    const failed = library.runAppendApply({
      inventoryRoot: failureConsumer.inventoryRoot,
      recordPath: path.join(failureConsumer.inventoryRoot, 'requests', 'apply.json'),
      timestampInput: timestamp,
      hooks: { failBeforePath: 'index.md' },
    });
    assert.equal(failed.receipt.status, 'write-failed');
    assert.deepEqual(failed.receipt.write.observed_changed_paths, ['index.json']);
    assert.equal(failed.receipt.write.possible_partial_mutation, true);
    assert.equal(failed.receipt.write.repair_required, true);
  });
});

test('installed library admits facets and installed validator proves mixed maps', () => {
  withConsumer({}, (consumer) => {
    const facetRoot = path.join(consumer.repository, 'facet-inventory');
    fs.cpSync(path.join(fixtureRoot, 'facet-projection'), facetRoot, { recursive: true });
    const validator = path.join(
      consumer.inventoryRoot,
      'scripts',
      'validate_projection_conformance.py',
    );
    const validation = spawnSync('python3', [
      validator,
      path.join(facetRoot, 'index.json'),
      '--json',
    ], { encoding: 'utf8', cwd: consumer.unrelated });
    assert.equal(validation.status, 0, validation.stderr);
    const report = JSON.parse(validation.stdout);
    assert.equal(report.checks.facet_admission.status, 'pass');
    assert.equal(report.checks.derived_maps.status, 'pass');

    const library = installedLibrary(consumer);
    const record = JSON.parse(
      fs.readFileSync(path.join(fixtureRoot, 'facet-admission', 'valid.json'), 'utf8'),
    );
    const normalized = library.normalizeEntry(record, timestamp, {
      namespaces: ['example-space'],
      recordClasses: library.DEFAULT_RECORD_CLASSES,
    });
    assert.deepEqual(normalized.concepts, ['append-runtime', 'test-generation']);
  });
});

test('runtime drift repair preserves all consumer-owned negative fixtures', () => {
  withConsumer({}, (consumer) => {
    const protectedPaths = [
      'index.json', 'index.md', 'schema.md', 'tags.md', 'log.md',
      'entries/existing.md',
    ];
    for (const relative of ['schema.md', 'log.md']) {
      fs.writeFileSync(path.join(consumer.inventoryRoot, relative), `consumer ${relative}\n`);
    }
    const before = Object.fromEntries(protectedPaths.map((relative) => [
      relative,
      digest(fs.readFileSync(path.join(consumer.inventoryRoot, relative))),
    ]));
    fs.writeFileSync(
      path.join(consumer.inventoryRoot, 'lib', 'inventory-update.cjs'),
      'drift\n',
    );
    assert.equal(sync(consumer.inventoryRoot, 'check').status, 1);
    assert.equal(sync(consumer.inventoryRoot, 'apply').status, 0);
    assert.equal(sync(consumer.inventoryRoot, 'check').status, 0);
    const after = Object.fromEntries(protectedPaths.map((relative) => [
      relative,
      digest(fs.readFileSync(path.join(consumer.inventoryRoot, relative))),
    ]));
    assert.deepEqual(after, before);
  });
});

test('public runtime and lifecycle artifacts contain no private bindings', () => {
  const scanRoots = [
    'bin',
    'lib',
    'schemas',
    'runtime-manifest.json',
    'scripts/validate-index-json.sh',
    'scripts/validate_projection_conformance.py',
    'scripts/sync-runtime.sh',
    'SKILL.md',
    'README.md',
    'templates/package-readme.md',
    'development/runtime-faceted-layout',
  ];
  const forbidden = /\/home\/|ops\/development|domainspec-core|cyberAlchemy/;
  const hits = [];
  function scan(candidate) {
    const stat = fs.statSync(candidate);
    if (stat.isDirectory()) {
      for (const name of fs.readdirSync(candidate)) scan(path.join(candidate, name));
      return;
    }
    const extension = path.extname(candidate);
    if (!['', '.cjs', '.json', '.md', '.py', '.sh'].includes(extension)) return;
    const text = fs.readFileSync(candidate, 'utf8');
    if (forbidden.test(text)) hits.push(path.relative(canonicalRoot, candidate));
  }
  for (const relative of scanRoots) {
    const candidate = path.join(canonicalRoot, relative);
    if (fs.existsSync(candidate)) scan(candidate);
  }
  assert.deepEqual(hits, []);
});
