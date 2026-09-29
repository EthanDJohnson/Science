// Offline tests for the two conundrum workflows. A mock runtime stands in for the
// Workflow tool: agent() calls are recorded and answered by a per-test handler.
// Run from the project root:  node --test .claude/skills/conundrum/scripts/tests/
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../../..')
const WORKFLOWS = path.join(ROOT, '.claude/workflows')
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor

function load(name) {
  const src = readFileSync(path.join(WORKFLOWS, `${name}.js`), 'utf8')
  const metaText = src.match(/export const meta = (\{[\s\S]*?\n\})\n/)[1]
  const meta = new Function(`return (${metaText})`)()
  const body = src.replace(/^export const meta\s*=/m, 'const meta =')
  const fn = new AsyncFunction('agent', 'parallel', 'pipeline', 'phase', 'log', 'args', 'budget', 'workflow', body)
  return { meta, fn, src }
}

async function run(name, args, handler) {
  const { meta, fn } = load(name)
  const calls = []
  const logs = []
  const phases = []
  let current = null
  const agent = async (prompt, opts = {}) => {
    const call = { prompt, opts, phase: opts.phase || current }
    calls.push(call)
    return handler(call)
  }
  const parallel = thunks => Promise.all(thunks.map(t => Promise.resolve().then(t).catch(() => null)))
  const pipeline = (items, ...stages) => Promise.all(items.map(async (item, i) => {
    let prev = item
    for (const stage of stages) {
      try { prev = await stage(prev, item, i) } catch { return null }
    }
    return prev
  }))
  const phase = t => { current = t; phases.push(t) }
  const log = m => logs.push(m)
  const result = await fn(agent, parallel, pipeline, phase, log, args, { total: null }, async () => null)
  return { meta, result, calls, logs, phases }
}

const byType = (calls, type) => calls.filter(c => c.opts.agentType === type)
const typeOf = c => c.opts.agentType

// ---------------------------------------------------------------- research workflow
test('research, quick: three facets, no source checks, one compiler', async () => {
  const { result, calls } = await run('conundrum-research', { slug: 's', depth: 'quick' }, () => 'ok')
  assert.deepEqual(byType(calls, 'researcher').map(c => c.opts.label),
    ['research:theory', 'research:quantitative', 'research:critiques'])
  assert.equal(byType(calls, 'source-checker').length, 0)
  assert.equal(byType(calls, 'dossier-compiler').length, 1)
  assert.equal(result.ok, true)
  assert.deepEqual(result.unchecked, ['theory', 'quantitative', 'critiques'])
  assert.match(byType(calls, 'dossier-compiler')[0].prompt, /no source check: theory, quantitative, critiques/)
})

test('research, standard: a failed researcher skips its checker and is reported missing', async () => {
  const handler = c => (c.opts.label === 'research:engineering' ? null : 'ok')
  const { result, calls, logs } = await run('conundrum-research', { slug: 's', depth: 'standard' }, handler)
  assert.equal(byType(calls, 'researcher').length, 4)
  assert.deepEqual(byType(calls, 'source-checker').map(c => c.opts.label).sort(),
    ['check:critiques', 'check:quantitative', 'check:theory'])
  assert.deepEqual(result.missing, ['engineering'])
  assert.deepEqual(result.unchecked, [])
  assert.match(byType(calls, 'dossier-compiler')[0].prompt, /failed and have no notes: engineering/)
  assert.ok(logs.some(l => l.includes('engineering')))
})

test('research, deep: five facets and phases match meta', async () => {
  const { result, calls, meta } = await run('conundrum-research', { slug: 's', depth: 'deep' }, () => 'ok')
  assert.equal(byType(calls, 'researcher').length, 5)
  assert.equal(byType(calls, 'source-checker').length, 5)
  assert.equal(result.ok, true)
  const titles = new Set(meta.phases.map(p => p.title))
  for (const c of calls) assert.ok(titles.has(c.phase), `phase ${c.phase} missing from meta`)
})

test('research: every researcher failing returns ok:false without compiling', async () => {
  const { result, calls } = await run('conundrum-research', { slug: 's' }, c =>
    (typeOf(c) === 'researcher' ? null : 'ok'))
  assert.equal(result.ok, false)
  assert.equal(byType(calls, 'dossier-compiler').length, 0)
})

test('research: unknown facets are ignored loudly; missing slug throws', async () => {
  const { calls, logs } = await run('conundrum-research', { slug: 's', facets: ['theory', 'astrology'] }, () => 'ok')
  assert.equal(byType(calls, 'researcher').length, 1)
  assert.ok(logs.some(l => l.includes('astrology')))
  await assert.rejects(run('conundrum-research', {}, () => 'ok'), /args.slug/)
})

// ---------------------------------------------------------------- analyze workflow
const SLATE5 = {
  candidates: [
    { id: 'C1', claim: 'Casimir cavities supply the energy', type: 'option' },
    { id: 'C2', claim: 'Squeezed vacuum states', type: 'option' },
    { id: 'C3', claim: 'Positive-energy warp shells avoid the need', type: 'reframe' },
    { id: 'C4', claim: 'Exotic scalar fields', type: 'mechanism' },
    { id: 'C5', claim: 'No viable option within admissible physics', type: 'null' },
  ],
}

function analyzeHandler({ slate = SLATE5, verdict = () => ({ verdict: 'survives', basis: 'calculation' }), fail = () => false } = {}) {
  return c => {
    if (fail(c)) return null
    switch (typeOf(c)) {
      case 'candidate-builder': return slate
      case 'falsifier': return verdict(c)
      default: return 'ok'
    }
  }
}

test('analyze, standard: default feasibility lenses, one refuter each, no crux, Fable judge untouched', async () => {
  const verdict = c => (c.opts.label.startsWith('C1#') ? { verdict: 'refuted', basis: 'calculation' }
    : { verdict: 'survives', basis: 'cited-evidence' })
  const { result, calls } = await run('conundrum-analyze', { slug: 's', depth: 'standard', type: 'feasibility' },
    analyzeHandler({ verdict }))
  assert.deepEqual(calls.filter(c => typeOf(c).startsWith('lens-')).map(typeOf),
    ['lens-decomposer', 'lens-constraints', 'lens-examiner', 'lens-engineer', 'lens-mechanist'])
  assert.equal(byType(calls, 'falsifier').length, 5)
  assert.deepEqual(result.eliminated, ['C1'])
  assert.deepEqual(result.alive, ['C2', 'C3', 'C4', 'C5'])
  assert.equal(byType(calls, 'crux-advocate').length, 0)
  const judge = byType(calls, 'adjudicator')[0]
  assert.equal(judge.opts.model, undefined)
  assert.equal(judge.opts.effort, undefined)
  assert.doesNotMatch(judge.prompt, /cruxes/)
  assert.match(judge.prompt, /C1: refuted/)
  assert.equal(byType(calls, 'report-auditor').length, 1)
  assert.equal(result.ok, true)
  // 5 lenses + slate + 5 refuters + judge + audit
  assert.equal(calls.length, 13)
})

test('analyze, deep: three refuters with distinct angles, majority vote, judge at max effort', async () => {
  const plan = { C1: ['refuted', 'refuted', 'survives'], C2: ['refuted', 'survives', 'weakened'] }
  const verdict = c => {
    const [id, i] = c.opts.label.split('#')
    const v = (plan[id] || [])[Number(i)] || 'survives'
    return { verdict: v, basis: 'calculation' }
  }
  const lenses = ['decomposer', 'constraints', 'examiner', 'engineer', 'mechanist', 'idealizer', 'dialectician']
  const { result, calls } = await run('conundrum-analyze', { slug: 's', depth: 'deep', type: 'feasibility', lenses },
    analyzeHandler({ verdict }))
  assert.equal(calls.filter(c => typeOf(c).startsWith('lens-')).length, 7)
  const c1 = byType(calls, 'falsifier').filter(c => c.opts.label.startsWith('C1#'))
  assert.deepEqual(c1.map(c => c.prompt.match(/angle: (\w+)/)[1]), ['physics', 'evidence', 'scale'])
  assert.deepEqual(result.eliminated, ['C1'])
  assert.ok(result.alive.includes('C2'))
  assert.deepEqual(byType(calls, 'crux-advocate').map(c => c.opts.label), ['crux:C2', 'crux:C3', 'crux:C4', 'crux:C5'])
  assert.match(byType(calls, 'crux-advocate')[0].prompt, /Rivals: C3, C4, C5/)
  const judge = byType(calls, 'adjudicator')[0]
  assert.equal(judge.opts.effort, 'max')
  assert.match(judge.prompt, /cruxes/)
})

test('analyze, quick: three lenses, no crux, Opus judge', async () => {
  const { result, calls } = await run('conundrum-analyze', { slug: 's', depth: 'quick', type: 'anomaly' }, analyzeHandler())
  assert.deepEqual(calls.filter(c => typeOf(c).startsWith('lens-')).map(typeOf),
    ['lens-constraints', 'lens-examiner', 'lens-empiricist'])
  assert.equal(byType(calls, 'crux-advocate').length, 0)
  const judge = byType(calls, 'adjudicator')[0]
  assert.equal(judge.opts.model, 'opus')
  assert.equal(judge.opts.effort, 'high')
  assert.equal(result.alive.length, 5)
})

test('analyze: fewer than two lenses completing stops before the slate', async () => {
  const fail = c => typeOf(c).startsWith('lens-') && typeOf(c) !== 'lens-constraints'
  const { result, calls } = await run('conundrum-analyze', { slug: 's' }, analyzeHandler({ fail }))
  assert.equal(result.ok, false)
  assert.equal(byType(calls, 'candidate-builder').length, 0)
})

test('analyze: a missing slate stops before falsification', async () => {
  const { result, calls } = await run('conundrum-analyze', { slug: 's' }, analyzeHandler({ slate: null }))
  assert.equal(result.ok, false)
  assert.equal(byType(calls, 'falsifier').length, 0)
})

test('analyze: oversized slate keeps null and reframe candidates and logs what it trimmed', async () => {
  const many = { candidates: [
    ...Array.from({ length: 9 }, (_, i) => ({ id: `C${i + 1}`, claim: `option ${i + 1}`, type: 'option' })),
    { id: 'C10', claim: 'reframe', type: 'reframe' },
    { id: 'C11', claim: 'none viable', type: 'null' },
  ] }
  const { result, calls, logs } = await run('conundrum-analyze', { slug: 's' }, analyzeHandler({ slate: many }))
  const falsified = new Set(byType(calls, 'falsifier').map(c => c.opts.label.split('#')[0]))
  assert.equal(falsified.size, 8)
  assert.ok(falsified.has('C10') && falsified.has('C11'))
  assert.deepEqual(result.trimmed, ['C7', 'C8', 'C9'])
  assert.ok(logs.some(l => l.includes('C7, C8, C9')))
  assert.match(byType(calls, 'adjudicator')[0].prompt, /Not falsified/)
})

test('analyze: a candidate whose refuter fails is kept alive and flagged to the judge', async () => {
  const fail = c => typeOf(c) === 'falsifier' && c.opts.label.startsWith('C4#')
  const { result, calls } = await run('conundrum-analyze', { slug: 's' }, analyzeHandler({ fail }))
  assert.deepEqual(result.unexamined, ['C4'])
  assert.ok(result.alive.includes('C4'))
  assert.match(byType(calls, 'adjudicator')[0].prompt, /Unexamined \(refuters failed\): C4/)
})

test('analyze: everything refuted means no crux round, but the judge still reports', async () => {
  const verdict = () => ({ verdict: 'refuted', basis: 'calculation' })
  const { result, calls } = await run('conundrum-analyze', { slug: 's' }, analyzeHandler({ verdict }))
  assert.deepEqual(result.alive, [])
  assert.equal(byType(calls, 'crux-advocate').length, 0)
  assert.equal(byType(calls, 'adjudicator').length, 1)
})

test('analyze: unknown lenses are ignored loudly; phases match meta', async () => {
  const { calls, logs, meta } = await run('conundrum-analyze',
    { slug: 's', lenses: ['constraints', 'examiner', 'numerology'] }, analyzeHandler())
  assert.equal(calls.filter(c => typeOf(c).startsWith('lens-')).length, 2)
  assert.ok(logs.some(l => l.includes('numerology')))
  const titles = new Set(meta.phases.map(p => p.title))
  for (const c of calls) assert.ok(titles.has(c.phase), `phase ${c.phase} missing from meta`)
})

test('workflow scripts avoid APIs the runtime forbids', () => {
  for (const name of ['conundrum-research', 'conundrum-analyze']) {
    const { src } = load(name)
    assert.doesNotMatch(src, /Date\.now\(|Math\.random\(|new Date\(\)|import\(|require\(/, name)
  }
})
