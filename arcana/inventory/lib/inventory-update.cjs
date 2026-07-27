'use strict';

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const {
  BODY_FIELDS,
  canonicalSerialize,
  createOperationReceipt,
  sha256Hex,
} = require('./operation-receipt.cjs');

const ENTRY_FIELDS = [
  'id', 'path', 'kind', 'type', 'title', 'summary', 'tags', 'sources',
  'updated', 'status', 'confidence', 'selectors', 'evidence_card_ids',
  'evidence_set_ids', 'namespace', 'record_class', 'concepts', 'residue',
];
const DEFAULT_RECORD_CLASSES = [
  'research', 'review', 'invoke', 'task-session', 'maintenance', 'runtime',
  'decision', 'evidence', 'synthesis',
];
const FACET_TOKEN_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const SUPPORTED_KINDS = new Set([
  'page', 'entry', 'query', 'lint', 'raw-manifest',
  'evidence-card-bundle', 'evidence-set-bundle',
]);
const ARRAY_MAP_SOURCES = [
  ['by_type', (entry) => [entry.type]],
  ['by_status', (entry) => [entry.status]],
  ['by_tag', (entry) => entry.tags],
  ['by_source', (entry) => entry.sources],
  ['by_evidence_card', (entry) => entry.evidence_card_ids],
  ['by_evidence_set', (entry) => entry.evidence_set_ids],
  ['by_namespace', (entry) => entry.namespace ? [entry.namespace] : []],
  ['by_record_class', (entry) => entry.record_class ? [entry.record_class] : []],
  ['by_concept', (entry) => entry.concepts || []],
];
const REQUIRED_RUNTIME_MEMBERS = [
  'lib/inventory-update.cjs',
  'lib/operation-receipt.cjs',
  'schemas/inventory.operation-receipt.v1.schema.json',
  'scripts/validate-index-json.sh',
  'scripts/validate_projection_conformance.py',
];
const MD_TABLES = [
  { prefix: 'entries/', header: '## Entries' },
  { prefix: 'wiki/', header: '## Wiki Pages' },
  { prefix: 'queries/', header: '## Query Files' },
  { prefix: 'lint/', header: '## Lint Files' },
];

function compareStrings(left, right) {
  if (left < right) return -1;
  if (left > right) return 1;
  return 0;
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function isNonEmptyString(value) {
  return typeof value === 'string' && value.length > 0;
}

function asArray(value) {
  if (value === undefined || value === null) return [];
  if (!Array.isArray(value)) throw new TypeError('expected an array');
  return [...value];
}

function orderedEntry(source) {
  const output = {};
  for (const field of ENTRY_FIELDS) {
    if (source[field] !== undefined) output[field] = source[field];
  }
  return output;
}

function normalizeFacetToken(value, label) {
  if (typeof value !== 'string') throw new TypeError(`${label} must be a string`);
  const normalized = value.trim().toLowerCase().replace(/\s+/g, '-');
  if (!FACET_TOKEN_RE.test(normalized)) {
    throw new TypeError(`${label} must normalize to a path-safe token`);
  }
  return normalized;
}

function facetPolicyFromIndex(indexObject) {
  const configured = (
    indexObject && indexObject.validation && indexObject.validation.facets
  ) || {};
  return {
    namespaces: Array.isArray(configured.namespaces) ? configured.namespaces : [],
    recordClasses: Array.isArray(configured.record_classes)
      ? configured.record_classes
      : DEFAULT_RECORD_CLASSES,
  };
}

function normalizeFacets(record, policy) {
  const fields = ['namespace', 'record_class', 'concepts'];
  const present = fields.filter((field) =>
    Object.prototype.hasOwnProperty.call(record, field));
  if (present.length === 0) return {};
  if (present.length !== fields.length) {
    throw new TypeError('namespace, record_class, and concepts must be provided together');
  }
  const namespace = normalizeFacetToken(record.namespace, 'record.namespace');
  const recordClass = normalizeFacetToken(record.record_class, 'record.record_class');
  const stableId = normalizeFacetToken(record.id, 'record.id');
  if (stableId !== record.id) {
    throw new TypeError('faceted record.id must already be a normalized path-safe token');
  }
  const allowedNamespaces = new Set((policy.namespaces || []).map((value) =>
    normalizeFacetToken(value, 'facet policy namespace')));
  const allowedClasses = new Set((policy.recordClasses || DEFAULT_RECORD_CLASSES).map((value) =>
    normalizeFacetToken(value, 'facet policy record class')));
  if (!allowedNamespaces.has(namespace)) {
    throw new TypeError(`record.namespace is not configured: ${namespace}`);
  }
  if (!allowedClasses.has(recordClass)) {
    throw new TypeError(`record.record_class is not controlled: ${recordClass}`);
  }
  if (!Array.isArray(record.concepts) || record.concepts.length === 0) {
    throw new TypeError('record.concepts must be a non-empty array');
  }
  const concepts = record.concepts.map((value, index) =>
    normalizeFacetToken(value, `record.concepts[${index}]`));
  if (new Set(concepts).size !== concepts.length) {
    throw new TypeError('record.concepts contains normalized duplicates');
  }
  concepts.sort(compareStrings);
  const expectedPath = `entries/${namespace}/${recordClass}/${stableId}.md`;
  if (record.path !== expectedPath) {
    throw new TypeError(`faceted record.path must equal ${expectedPath}`);
  }
  return { namespace, record_class: recordClass, concepts };
}

function normalizeEntry(record, timestampInput, facetPolicy = {}) {
  if (!record || typeof record !== 'object' || Array.isArray(record)) {
    throw new TypeError('record must be an object');
  }
  for (const field of ['id', 'path', 'kind', 'type']) {
    if (!isNonEmptyString(record[field])) throw new TypeError(`record.${field} is required`);
  }
  if (!SUPPORTED_KINDS.has(record.kind)) {
    throw new TypeError(`record.kind is unsupported: ${record.kind}`);
  }
  if (
    record.path.startsWith('/') || record.path.includes('\\') ||
    record.path.split('/').includes('..')
  ) {
    throw new TypeError('record.path must be Inventory-root-relative');
  }
  const facets = normalizeFacets(record, facetPolicy);
  return orderedEntry({
    id: record.id,
    path: record.path,
    kind: record.kind,
    type: record.type,
    title: isNonEmptyString(record.title) ? record.title : record.path,
    summary: typeof record.summary === 'string' ? record.summary : '',
    tags: asArray(record.tags),
    sources: asArray(record.sources),
    updated: isNonEmptyString(record.updated) ? record.updated : timestampInput.slice(0, 10),
    status: isNonEmptyString(record.status) ? record.status : 'candidate',
    confidence: isNonEmptyString(record.confidence) ? record.confidence : 'unknown',
    selectors: asArray(record.selectors),
    evidence_card_ids: asArray(record.evidence_card_ids),
    evidence_set_ids: asArray(record.evidence_set_ids),
    ...facets,
    residue: asArray(record.residue),
  });
}

function ensureMaps(index) {
  index.entries = Array.isArray(index.entries) ? index.entries : [];
  index.indexes = index.indexes && typeof index.indexes === 'object' ? index.indexes : {};
  for (const name of ['by_id', ...ARRAY_MAP_SOURCES.map(([mapName]) => mapName)]) {
    if (!index.indexes[name] || typeof index.indexes[name] !== 'object') {
      index.indexes[name] = {};
    }
  }
}

function appendToArrayMap(map, key, id) {
  if (!Object.prototype.hasOwnProperty.call(map, key)) map[key] = [];
  if (!map[key].includes(id)) map[key].push(id);
}

function entriesEqual(left, right) {
  return canonicalSerialize(orderedEntry(left)) === canonicalSerialize(orderedEntry(right));
}

function updateIndex(indexObject, normalizedEntry, timestampInput) {
  const output = clone(indexObject);
  ensureMaps(output);
  const existing = output.entries.find((entry) => entry.id === normalizedEntry.id);
  if (existing) {
    return {
      index: output,
      entry: normalizedEntry,
      disposition: entriesEqual(existing, normalizedEntry)
        ? 'identical-no-op'
        : 'id-conflict',
      changed: false,
    };
  }
  output.entries.push(normalizedEntry);
  output.indexes.by_id[normalizedEntry.id] = normalizedEntry.path;
  for (const [mapName, select] of ARRAY_MAP_SOURCES) {
    for (const key of select(normalizedEntry)) {
      appendToArrayMap(output.indexes[mapName], key, normalizedEntry.id);
    }
  }
  output.generated_at = timestampInput;
  return {
    index: output,
    entry: normalizedEntry,
    disposition: 'added',
    changed: true,
  };
}

function serializeIndex(indexObject) {
  return `${JSON.stringify(indexObject, null, 2)}\n`;
}

function mdCell(value) {
  return String(value === undefined || value === null ? '' : value)
    .replace(/\r?\n/g, ' ')
    .replace(/\|/g, '\\|')
    .trim();
}

function mdRowFor(entry) {
  const tags = entry.tags.map((tag) => `\`${mdCell(tag)}\``).join(', ');
  return `| [${entry.path}](${entry.path}) | ${mdCell(entry.type)} | ${tags} | ${mdCell(entry.summary)} |`;
}

function updateHumanIndex(markdown, entry) {
  const table = MD_TABLES.find(({ prefix }) => entry.path.startsWith(prefix));
  if (!table) return { markdown, changed: false, reason: 'no-table-for-path' };
  const lines = markdown.split('\n');
  const headingIndex = lines.findIndex((line) => line.trim() === table.header);
  if (headingIndex === -1) return { markdown, changed: false, reason: 'table-header-not-found' };
  let separatorIndex = -1;
  for (let index = headingIndex + 1; index < lines.length; index += 1) {
    if (/^\|\s*-+/.test(lines[index])) {
      separatorIndex = index;
      break;
    }
    if (/^## /.test(lines[index])) break;
  }
  if (separatorIndex === -1) {
    return { markdown, changed: false, reason: 'table-separator-not-found' };
  }
  let lastRow = separatorIndex;
  for (let index = separatorIndex + 1; index < lines.length; index += 1) {
    if (lines[index].startsWith('|')) lastRow = index;
    else break;
  }
  const link = `[${entry.path}](${entry.path})`;
  if (lines.slice(separatorIndex + 1, lastRow + 1).some((line) => line.includes(link))) {
    return { markdown, changed: false, reason: 'row-already-present' };
  }
  lines.splice(lastRow + 1, 0, mdRowFor(entry));
  return {
    markdown: lines.join('\n'),
    changed: true,
    reason: 'row-added',
  };
}

function digestFile(filePath) {
  return sha256Hex(fs.readFileSync(filePath));
}

function inspectRuntime(inventoryRoot) {
  const helpers = REQUIRED_RUNTIME_MEMBERS.map((relativePath) => {
    const memberPath = path.join(inventoryRoot, ...relativePath.split('/'));
    if (!fs.existsSync(memberPath) || !fs.statSync(memberPath).isFile()) {
      return {
        path: relativePath,
        evidence_state: 'unavailable',
        sha256: null,
      };
    }
    return {
      path: relativePath,
      evidence_state: 'observed',
      sha256: digestFile(memberPath),
    };
  });
  const complete = helpers.every((helper) => helper.evidence_state === 'observed');
  return {
    evidence_state: complete ? 'observed' : 'partial',
    bundle_sha256: complete ? sha256Hex(canonicalSerialize(helpers)) : null,
    helpers,
  };
}

function deepCanonical(value) {
  if (Array.isArray(value)) return value.map(deepCanonical);
  if (!value || typeof value !== 'object') return value;
  const output = {};
  for (const key of Object.keys(value).sort(compareStrings)) {
    let child = value[key];
    if ((key === 'errors' || key === 'warnings') && Array.isArray(child)) {
      child = [...child].sort(compareStrings);
    }
    output[key] = deepCanonical(child);
  }
  return output;
}

function stableValidatorReport(report) {
  const normalized = clone(report);
  normalized.index = '.arcanum/inventory/index.json';
  return deepCanonical(normalized);
}

function validatorFailureReport() {
  return {
    schema_version: 'inventory.projection-conformance.report.v1',
    overall: 'fail',
    lookup_readiness: 'blocked',
    index: '.arcanum/inventory/index.json',
    checks: {
      validator_execution: {
        status: 'fail',
        errors: ['validator-execution-failed'],
        warnings: [],
      },
    },
    failure_count: 1,
    warning_count: 0,
  };
}

function runValidator(inventoryRoot, indexPath) {
  const validator = path.join(inventoryRoot, 'scripts', 'validate_projection_conformance.py');
  const result = spawnSync('python3', [validator, indexPath, '--json'], {
    encoding: 'utf8',
    cwd: inventoryRoot,
  });
  let report;
  try {
    report = JSON.parse(result.stdout);
  } catch (_error) {
    report = validatorFailureReport();
  }
  return stableValidatorReport(report);
}

function reportDigest(report) {
  return sha256Hex(canonicalSerialize(report));
}

function warningIdentities(report) {
  const warnings = [];
  for (const [checkName, check] of Object.entries(report.checks || {})) {
    for (const warning of check.warnings || []) warnings.push(`${checkName}:${warning}`);
  }
  return [...new Set(warnings)].sort(compareStrings);
}

function warningDelta(baselineReport, candidateReport) {
  const baseline = warningIdentities(baselineReport);
  const candidate = warningIdentities(candidateReport);
  const baselineSet = new Set(baseline);
  const candidateSet = new Set(candidate);
  const inherited = candidate.filter((warning) => baselineSet.has(warning));
  return {
    evidence_state: 'observed',
    introduced: candidate.filter((warning) => !baselineSet.has(warning)),
    resolved: baseline.filter((warning) => !candidateSet.has(warning)),
    inherited_count: inherited.length,
    inherited_set_sha256: sha256Hex(canonicalSerialize(inherited)),
  };
}

function notReachedInputs() {
  return {
    evidence_state: 'not-reached',
    baseline_index_sha256: null,
    baseline_human_index_sha256: null,
    record_sha256: null,
    normalized_record_sha256: null,
  };
}

function notReachedBaseline() {
  return {
    evidence_state: 'not-reached',
    report_sha256: null,
    lookup_readiness: null,
    failure_count: null,
    warning_count: null,
  };
}

function notReachedCandidate() {
  return {
    evidence_state: 'not-reached',
    disposition: null,
    index_sha256: null,
    human_index_sha256: null,
    report_sha256: null,
    lookup_readiness: null,
  };
}

function notReachedWarnings() {
  return {
    evidence_state: 'not-reached',
    introduced: [],
    resolved: [],
    inherited_count: null,
    inherited_set_sha256: null,
  };
}

function notReachedWrite() {
  return {
    evidence_state: 'not-reached',
    attempted: false,
    committed: false,
    observed_changed_paths: [],
    expected_postwrite_digests: {},
    actual_postwrite_digests: {},
    possible_partial_mutation: false,
    repair_required: false,
  };
}

function noWriteObservation(expectedDigests, actualDigests) {
  return {
    evidence_state: 'observed',
    attempted: false,
    committed: false,
    observed_changed_paths: [],
    expected_postwrite_digests: expectedDigests,
    actual_postwrite_digests: actualDigests,
    possible_partial_mutation: false,
    repair_required: false,
  };
}

function baseBody(timestampInput, runtime) {
  return {
    schema_version: 'inventory.operation-receipt.v1',
    operation: 'append',
    mode: 'dry-run',
    status: 'tooling-unavailable',
    reason_code: 'runtime-member-unavailable',
    timestamp_input: timestampInput,
    inventory_root: '.arcanum/inventory',
    runtime,
    inputs: notReachedInputs(),
    baseline: notReachedBaseline(),
    candidate: notReachedCandidate(),
    warning_delta: notReachedWarnings(),
    write: notReachedWrite(),
    authority_boundary: 'inventory-read-model-only',
    residue: ['no-currentness-or-promotion-claim'],
  };
}

function emit(body) {
  const result = createOperationReceipt(body);
  const success = ['dry-run-ready', 'applied', 'identical-no-op'].includes(body.status);
  return { ...result, exitCode: success ? 0 : 1 };
}

function readBaseline(inventoryRoot) {
  const indexPath = path.join(inventoryRoot, 'index.json');
  const humanPath = path.join(inventoryRoot, 'index.md');
  return {
    indexPath,
    humanPath,
    indexBytes: fs.readFileSync(indexPath),
    humanBytes: fs.readFileSync(humanPath),
  };
}

function currentDigests(baseline) {
  return {
    'index.json': digestFile(baseline.indexPath),
    'index.md': digestFile(baseline.humanPath),
  };
}

function stageCandidate(inventoryRoot, indexBytes, humanBytes) {
  const temporaryRepository = fs.mkdtempSync(path.join(os.tmpdir(), 'inventory-dry-run-'));
  const stagedRoot = path.join(temporaryRepository, '.arcanum', 'inventory');
  fs.mkdirSync(path.dirname(stagedRoot), { recursive: true });
  fs.cpSync(inventoryRoot, stagedRoot, { recursive: true });
  fs.writeFileSync(path.join(stagedRoot, 'index.json'), indexBytes);
  fs.writeFileSync(path.join(stagedRoot, 'index.md'), humanBytes);
  return { temporaryRepository, stagedRoot };
}

function runAppendDryRun({ inventoryRoot, recordPath, timestampInput }) {
  const runtime = inspectRuntime(inventoryRoot);
  const body = baseBody(timestampInput, runtime);
  if (runtime.evidence_state !== 'observed') return emit(body);

  let baseline;
  try {
    baseline = readBaseline(inventoryRoot);
  } catch (_error) {
    body.runtime = {
      ...runtime,
      evidence_state: 'partial',
      bundle_sha256: null,
    };
    body.reason_code = 'inventory-state-unavailable';
    return emit(body);
  }

  const baselineDigests = {
    'index.json': sha256Hex(baseline.indexBytes),
    'index.md': sha256Hex(baseline.humanBytes),
  };
  const baselineReport = runValidator(inventoryRoot, baseline.indexPath);
  body.inputs = {
    evidence_state: 'partial',
    baseline_index_sha256: baselineDigests['index.json'],
    baseline_human_index_sha256: baselineDigests['index.md'],
    record_sha256: null,
    normalized_record_sha256: null,
  };
  body.baseline = {
    evidence_state: 'observed',
    report_sha256: reportDigest(baselineReport),
    lookup_readiness: baselineReport.lookup_readiness,
    failure_count: baselineReport.failure_count,
    warning_count: baselineReport.warning_count,
  };
  body.write = noWriteObservation(baselineDigests, currentDigests(baseline));
  if (baselineReport.lookup_readiness !== 'ready') {
    body.status = 'baseline-blocked';
    body.reason_code = 'baseline-not-ready';
    return emit(body);
  }

  let recordBytes = null;
  let normalizedEntry;
  try {
    recordBytes = fs.readFileSync(recordPath);
    const record = JSON.parse(recordBytes);
    const indexObject = JSON.parse(baseline.indexBytes);
    normalizedEntry = normalizeEntry(record, timestampInput, facetPolicyFromIndex(indexObject));
  } catch (_error) {
    body.status = 'invalid-request';
    body.reason_code = recordBytes ? 'record-json-invalid' : 'record-unavailable';
    body.inputs.record_sha256 = recordBytes ? sha256Hex(recordBytes) : null;
    return emit(body);
  }

  const normalizedBytes = canonicalSerialize(normalizedEntry);
  body.inputs = {
    evidence_state: 'observed',
    baseline_index_sha256: baselineDigests['index.json'],
    baseline_human_index_sha256: baselineDigests['index.md'],
    record_sha256: sha256Hex(recordBytes),
    normalized_record_sha256: sha256Hex(normalizedBytes),
  };
  const indexObject = JSON.parse(baseline.indexBytes);
  const transition = updateIndex(indexObject, normalizedEntry, timestampInput);

  if (transition.disposition !== 'added') {
    body.status = transition.disposition;
    body.reason_code = transition.disposition === 'id-conflict'
      ? 'existing-id-differs'
      : null;
    body.candidate = {
      evidence_state: 'observed',
      disposition: transition.disposition,
      index_sha256: baselineDigests['index.json'],
      human_index_sha256: baselineDigests['index.md'],
      report_sha256: reportDigest(baselineReport),
      lookup_readiness: baselineReport.lookup_readiness,
    };
    body.warning_delta = warningDelta(baselineReport, baselineReport);
    body.write = noWriteObservation(baselineDigests, currentDigests(baseline));
    return emit(body);
  }

  const humanTransition = updateHumanIndex(
    baseline.humanBytes.toString('utf8'),
    normalizedEntry,
  );
  const candidateIndexBytes = Buffer.from(serializeIndex(transition.index));
  const candidateHumanBytes = Buffer.from(humanTransition.markdown);
  const staged = stageCandidate(inventoryRoot, candidateIndexBytes, candidateHumanBytes);
  try {
    const candidateReport = runValidator(
      staged.stagedRoot,
      path.join(staged.stagedRoot, 'index.json'),
    );
    body.candidate = {
      evidence_state: 'observed',
      disposition: 'added',
      index_sha256: sha256Hex(candidateIndexBytes),
      human_index_sha256: sha256Hex(candidateHumanBytes),
      report_sha256: reportDigest(candidateReport),
      lookup_readiness: candidateReport.lookup_readiness,
    };
    body.warning_delta = warningDelta(baselineReport, candidateReport);
    body.write = noWriteObservation(baselineDigests, currentDigests(baseline));
    if (candidateReport.lookup_readiness !== 'ready') {
      body.status = 'candidate-blocked';
      body.reason_code = 'candidate-not-ready';
      body.residue.push('candidate-validation-blocked');
    } else {
      body.status = 'dry-run-ready';
      body.reason_code = null;
    }
    return emit(body);
  } finally {
    fs.rmSync(staged.temporaryRepository, { recursive: true, force: true });
  }
}

function bodyFromReceipt(receipt) {
  const body = {};
  for (const field of BODY_FIELDS) body[field] = clone(receipt[field]);
  return body;
}

function applyCandidateBytes(baseline, recordPath, timestampInput) {
  const record = JSON.parse(fs.readFileSync(recordPath));
  const indexObject = JSON.parse(baseline.indexBytes);
  const normalizedEntry = normalizeEntry(
    record,
    timestampInput,
    facetPolicyFromIndex(indexObject),
  );
  const transition = updateIndex(
    indexObject,
    normalizedEntry,
    timestampInput,
  );
  if (transition.disposition !== 'added') {
    throw new Error(`apply candidate disposition changed: ${transition.disposition}`);
  }
  const humanTransition = updateHumanIndex(
    baseline.humanBytes.toString('utf8'),
    normalizedEntry,
  );
  return {
    indexBytes: Buffer.from(serializeIndex(transition.index)),
    humanBytes: Buffer.from(humanTransition.markdown),
  };
}

function runAppendApply({
  inventoryRoot,
  recordPath,
  timestampInput,
  hooks = {},
}) {
  const dryRun = runAppendDryRun({ inventoryRoot, recordPath, timestampInput });
  const body = bodyFromReceipt(dryRun.receipt);
  body.mode = 'apply';
  if (body.status !== 'dry-run-ready') return emit(body);

  const baseline = readBaseline(inventoryRoot);
  const baselineDigests = {
    'index.json': sha256Hex(baseline.indexBytes),
    'index.md': sha256Hex(baseline.humanBytes),
  };
  const candidate = applyCandidateBytes(baseline, recordPath, timestampInput);
  const candidateDigests = {
    'index.json': sha256Hex(candidate.indexBytes),
    'index.md': sha256Hex(candidate.humanBytes),
  };
  if (
    candidateDigests['index.json'] !== body.candidate.index_sha256 ||
    candidateDigests['index.md'] !== body.candidate.human_index_sha256
  ) {
    throw new Error('candidate bytes do not reproduce the validated dry-run digests');
  }

  if (typeof hooks.beforeWrite === 'function') hooks.beforeWrite({ baseline });
  const immediateDigests = currentDigests(baseline);
  if (
    immediateDigests['index.json'] !== baselineDigests['index.json'] ||
    immediateDigests['index.md'] !== baselineDigests['index.md']
  ) {
    const driftReport = {
      schema_version: 'inventory.baseline-drift-report.v1',
      expected: baselineDigests,
      actual: immediateDigests,
    };
    body.status = 'baseline-blocked';
    body.reason_code = 'baseline-drift-before-write';
    body.baseline = {
      evidence_state: 'observed',
      report_sha256: reportDigest(deepCanonical(driftReport)),
      lookup_readiness: 'blocked',
      failure_count: 1,
      warning_count: 0,
    };
    body.candidate = notReachedCandidate();
    body.warning_delta = notReachedWarnings();
    body.write = noWriteObservation(baselineDigests, immediateDigests);
    body.residue.push('baseline-drift-observed-before-write');
    return emit(body);
  }

  let failedPath = null;
  let writeError = null;
  try {
    failedPath = 'index.json';
    if (hooks.failBeforePath === failedPath) throw new Error('injected index.json write failure');
    fs.writeFileSync(baseline.indexPath, candidate.indexBytes);

    failedPath = 'index.md';
    if (hooks.failBeforePath === failedPath) throw new Error('injected index.md write failure');
    fs.writeFileSync(baseline.humanPath, candidate.humanBytes);
    failedPath = null;

    if (typeof hooks.afterWrites === 'function') hooks.afterWrites({ baseline, candidate });
  } catch (error) {
    writeError = error;
  }

  const actualDigests = currentDigests(baseline);
  const observedChangedPaths = Object.keys(actualDigests)
    .filter((relativePath) => actualDigests[relativePath] !== baselineDigests[relativePath])
    .sort(compareStrings);
  const committed =
    actualDigests['index.json'] === candidateDigests['index.json'] &&
    actualDigests['index.md'] === candidateDigests['index.md'];

  body.write = {
    evidence_state: 'observed',
    attempted: true,
    committed,
    observed_changed_paths: observedChangedPaths,
    expected_postwrite_digests: candidateDigests,
    actual_postwrite_digests: actualDigests,
    possible_partial_mutation: !committed,
    repair_required: !committed,
  };
  if (committed) {
    body.status = 'applied';
    body.reason_code = null;
  } else if (writeError) {
    body.status = 'write-failed';
    body.reason_code = failedPath === 'index.json'
      ? 'index-json-write-failed'
      : 'index-md-write-failed';
    body.residue.push('repair-route-restore-both-projections-from-validated-candidate');
  } else {
    body.status = 'postwrite-digest-mismatch';
    body.reason_code = 'postwrite-digest-mismatch';
    body.residue.push('repair-route-restore-both-projections-from-validated-candidate');
  }
  return emit(body);
}

module.exports = {
  ENTRY_FIELDS,
  DEFAULT_RECORD_CLASSES,
  REQUIRED_RUNTIME_MEMBERS,
  facetPolicyFromIndex,
  inspectRuntime,
  normalizeEntry,
  runAppendApply,
  runAppendDryRun,
  runValidator,
  serializeIndex,
  updateHumanIndex,
  updateIndex,
  warningDelta,
};
