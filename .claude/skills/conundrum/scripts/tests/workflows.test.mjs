// Offline tests for the two conundrum workflows. A mock runtime stands in for the
// Workflow tool: agent() calls are recorded and answered by a per-test handler.
// Run from the project root:  node --test .claude/skills/conundrum/scripts/tests/workflows.test.mjs
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
// What a file-writing agent returns once its file is written (the WROTE schema).
const wroteOk = c => ({ ok: true, path: `runs/s/${c.opts.label}.md`, summary: `${c.opts.label} done` })
const WROTE_FIELDS = ['ok', 'path', 'summary']

// ---------------------------------------------------------------- research workflow
test('research, quick: three facets, no source checks, one compiler', async () => {
  const { result, calls } = await run('conundrum-research', { slug: 's', depth: 'quick' }, wroteOk)
  assert.deepEqual(byType(calls, 'researcher').map(c => c.opts.label),
    ['research:theory', 'research:quantitative', 'research:critiques'])
  assert.equal(byType(calls, 'source-checker').length, 0)
  assert.equal(byType(calls, 'dossier-compiler').length, 1)
  assert.equal(result.ok, true)
  assert.deepEqual(result.unchecked, ['theory', 'quantitative', 'critiques'])
  assert.match(byType(calls, 'dossier-compiler')[0].prompt, /no source check: theory, quantitative, critiques/)
})

test('research, standard: a failed researcher skips its checker and is reported missing', async () => {
  const handler = c => (c.opts.label === 'research:engineering' ? null : wroteOk(c))
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
  const { result, calls, meta } = await run('conundrum-research', { slug: 's', depth: 'deep' }, wroteOk)
  assert.equal(byType(calls, 'researcher').length, 5)
  assert.equal(byType(calls, 'source-checker').length, 5)
  assert.equal(result.ok, true)
  const titles = new Set(meta.phases.map(p => p.title))
  for (const c of calls) assert.ok(titles.has(c.phase), `phase ${c.phase} missing from meta`)
})

test('research: every researcher failing returns ok:false without compiling', async () => {
  const { result, calls } = await run('conundrum-research', { slug: 's' }, c =>
    (typeOf(c) === 'researcher' ? null : wroteOk(c)))
  assert.equal(result.ok, false)
  assert.equal(byType(calls, 'dossier-compiler').length, 0)
})

test('research: ok:false and unstructured returns count as failures, not silent gaps', async () => {
  const handler = c => {
    if (c.opts.label === 'research:theory') return { ok: false, path: '', summary: 'could not write' }
    if (c.opts.label === 'research:quantitative') return 'I ran out of turns'
    if (c.opts.label === 'check:critiques') return { ok: false, path: '', summary: 'no file' }
    return wroteOk(c)
  }
  const { result, calls } = await run('conundrum-research', { slug: 's', depth: 'standard' }, handler)
  assert.deepEqual(result.missing, ['theory', 'quantitative'])
  assert.deepEqual(result.unchecked, ['critiques'])
  assert.deepEqual(byType(calls, 'source-checker').map(c => c.opts.label).sort(), ['check:critiques', 'check:engineering'])
  const compile = byType(calls, 'dossier-compiler')[0].prompt
  assert.match(compile, /failed and have no notes: theory, quantitative/)
  assert.match(compile, /no source check: critiques/)
  assert.equal(result.ok, true)
})

test('research: summaries flow into the result; a failed compiler returns ok:false', async () => {
  const { result } = await run('conundrum-research', { slug: 's', depth: 'quick' }, wroteOk)
  assert.equal(result.researchSummaries.theory, 'research:theory done')
  assert.equal(result.dossierSummary, 'dossier done')
  const failed = await run('conundrum-research', { slug: 's', depth: 'quick' }, c =>
    (typeOf(c) === 'dossier-compiler' ? { ok: false, path: '', summary: '' } : wroteOk(c)))
  assert.equal(failed.result.ok, false)
  assert.equal(failed.result.reason, 'dossier compiler failed')
})

test('research: every agent is asked for the {ok, path, summary} shape', async () => {
  const { calls } = await run('conundrum-research', { slug: 's', depth: 'deep' }, wroteOk)
  for (const c of calls) assert.deepEqual(c.opts.schema?.required, WROTE_FIELDS, c.opts.label)
})

test('research: requested calculators are built alongside the research, into the run folder', async () => {
  const tools = [{ name: 'rocket_trip', purpose: 'relativistic trip times' }, { name: 'casimir', purpose: 'plate energies' }]
  const handler = c => (c.opts.label === 'tool:casimir' ? { ok: false, path: '', summary: 'gave up' } : wroteOk(c))
  const { result, calls, logs } = await run('conundrum-research', { slug: 's', depth: 'quick', tools }, handler)
  const smiths = byType(calls, 'toolsmith')
  assert.deepEqual(smiths.map(c => c.opts.label), ['tool:rocket_trip', 'tool:casimir'])
  assert.ok(smiths.every(c => c.opts.phase === 'Tools' && c.opts.schema.required.includes('ok')))
  assert.match(smiths[0].prompt, /Write runs\/s\/tools\/rocket_trip\.py/)
  assert.deepEqual(result.tools.map(t => [t.name, t.ok]), [['rocket_trip', true], ['casimir', false]])
  assert.ok(logs.some(l => l.includes('calculators not built: casimir')))
  assert.equal(result.ok, true)                        // a failed calculator never blocks the dossier
  assert.equal(byType(calls, 'researcher').length, 3)
})

test('research: bad calculator requests are ignored loudly; tools still report when research fails', async () => {
  const tools = [{ name: '../../etc/passwd', purpose: 'x' }, { name: 'Bad Name', purpose: 'y' }, { name: 'ok_tool' }, { name: 'units_ext', purpose: 'more units' }]
  const { calls, logs } = await run('conundrum-research', { slug: 's', depth: 'quick', tools }, wroteOk)
  assert.deepEqual(byType(calls, 'toolsmith').map(c => c.opts.label), ['tool:units_ext'])
  assert.ok(logs.some(l => l.includes('ignoring 3 tool request(s)')))
  const failed = await run('conundrum-research', { slug: 's', tools: [{ name: 'units_ext', purpose: 'p' }] },
    c => (typeOf(c) === 'researcher' ? null : wroteOk(c)))
  assert.equal(failed.result.ok, false)
  assert.deepEqual(failed.result.tools.map(t => t.name), ['units_ext'])
})

test('research: approved earlier runs reach the researchers, and only them', async () => {
  const prior = [{ slug: '2026-03-01-alcubierre-energy', mode: 'update' }, { slug: '2026-09-29-warp-bubble-shapes', mode: 'leads' }]
  const { result, calls, logs } = await run('conundrum-research', { slug: 's', depth: 'standard', prior }, wroteOk)
  for (const c of byType(calls, 'researcher')) {
    assert.match(c.prompt, /runs\/s\/prior\/2026-03-01-alcubierre-energy\/ \(update\), runs\/s\/prior\/2026-09-29-warp-bubble-shapes\/ \(leads\)/)
    assert.match(c.prompt, /PROVENANCE\.md/)
  }
  for (const c of byType(calls, 'source-checker')) assert.doesNotMatch(c.prompt, /prior/)
  assert.match(byType(calls, 'dossier-compiler')[0].prompt, /PRIOR line/)
  assert.deepEqual(result.prior, prior.map(p => p.slug))
  assert.ok(logs.some(l => l.includes('building on earlier runs')))
})

test('research: bad earlier-run entries are ignored loudly; without any, prompts are unchanged', async () => {
  const prior = [{ slug: '../../etc', mode: 'update' }, { slug: '2026-01-01-x', mode: 'ignore' }, { slug: '2026-01-02-y' }]
  const { result, calls, logs } = await run('conundrum-research', { slug: 's', depth: 'quick', prior }, wroteOk)
  assert.ok(logs.some(l => l.includes('ignoring 3 earlier-run entries')))
  assert.deepEqual(result.prior, [])
  for (const c of calls) assert.doesNotMatch(c.prompt, /prior|PRIOR/, c.opts.label)
})

test('research: unknown facets are ignored loudly; missing slug throws', async () => {
  const { calls, logs } = await run('conundrum-research', { slug: 's', facets: ['theory', 'astrology'] }, wroteOk)
  assert.equal(byType(calls, 'researcher').length, 1)
  assert.ok(logs.some(l => l.includes('astrology')))
  await assert.rejects(run('conundrum-research', {}, wroteOk), /args.slug/)
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

const mathOk = c => ({ ...wroteOk(c), verified: 3, refuted: 0, unverified: 1 })

function analyzeHandler({ slate = SLATE5, verdict = () => ({ verdict: 'survives', basis: 'calculation' }), fail = () => false,
  math = mathOk } = {}) {
  return c => {
    if (fail(c)) return null
    switch (typeOf(c)) {
      case 'candidate-builder': return slate
      case 'falsifier': return verdict(c)
      case 'math-checker': return math(c)
      default: return wroteOk(c)
    }
  }
}

test('analyze, standard: default feasibility lenses, one refuter each, no crux, Fable judge untouched', async () => {
  const verdict = c => (c.opts.label.startsWith('C1#') ? { verdict: 'refuted', basis: 'calculation' }
    : { verdict: 'survives', basis: 'cited-evidence' })
  const { result, calls } = await run('conundrum-analyze', { slug: 's', depth: 'standard', type: 'feasibility' },
    analyzeHandler({ verdict }))
  assert.deepEqual(calls.filter(c => typeOf(c).startsWith('lens-')).map(typeOf),
    ['lens-decomposer', 'lens-examiner', 'lens-mechanist', 'lens-engineer', 'lens-constraints'])
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
  // 5 lenses + 5 math checks + slate + 5 refuters + judge + audit
  assert.equal(calls.length, 18)
})

test('analyze, standard: each lens goes to its own math checker, and every later stage hears the results', async () => {
  const math = c => (c.opts.label === 'math:constraints' ? { ...mathOk(c), refuted: 2 } : mathOk(c))
  const { result, calls, logs } = await run('conundrum-analyze', { slug: 's', depth: 'standard' }, analyzeHandler({ math }))
  const checkers = byType(calls, 'math-checker')
  assert.deepEqual(checkers.map(c => c.opts.label),
    ['math:decomposer', 'math:examiner', 'math:mechanist', 'math:engineer', 'math:constraints'])
  for (const c of checkers) {
    assert.equal(c.opts.phase, 'Math')
    assert.deepEqual(c.opts.schema.required, ['ok', 'path', 'summary', 'verified', 'refuted', 'unverified'])
    assert.match(c.prompt, new RegExp(`runs/s/analyses/${c.opts.label.slice(5)}\\.md`))
  }
  assert.deepEqual(result.math.constraints, { verified: 3, refuted: 2, unverified: 1 })
  assert.deepEqual(result.mathFailed, [])
  const slate = byType(calls, 'candidate-builder')[0].prompt
  assert.match(slate, /constraints: 3 verified, 2 refuted, 1 unverified/)
  assert.match(slate, /may not rest on a claim they refuted/)
  for (const c of byType(calls, 'falsifier')) assert.match(c.prompt, /runs\/s\/math\//)
  assert.match(byType(calls, 'adjudicator')[0].prompt, /Math checks of the lenses/)
  assert.match(byType(calls, 'report-auditor')[0].prompt, /math checks in runs\/s\/math\//)
  assert.ok(logs.some(l => l.startsWith('math checks:')))
})

test('analyze: a failed lens gets no math check; a failed math check is reported and never blocks the slate', async () => {
  const fail = c => c.opts.label === 'engineer' || c.opts.label === 'math:mechanist'
  const { result, calls, logs } = await run('conundrum-analyze', { slug: 's', depth: 'standard' }, analyzeHandler({ fail }))
  assert.ok(!byType(calls, 'math-checker').some(c => c.opts.label === 'math:engineer'))
  assert.deepEqual(result.mathFailed, ['mechanist'])
  assert.ok(logs.some(l => l.includes('math checks that failed: mechanist')))
  assert.match(byType(calls, 'candidate-builder')[0].prompt, /The math of mechanist went unchecked/)
  assert.equal(result.ok, true)
})

test('analyze, quick: no math checks, and no stage is told about them', async () => {
  const { result, calls } = await run('conundrum-analyze', { slug: 's', depth: 'quick' }, analyzeHandler())
  assert.equal(byType(calls, 'math-checker').length, 0)
  for (const c of calls) assert.doesNotMatch(c.prompt, /math/i, c.opts.label)
  assert.deepEqual(result.math, {})
  assert.deepEqual(result.mathFailed, [])
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
    ['lens-examiner', 'lens-statistician', 'lens-constraints'])
  assert.equal(byType(calls, 'crux-advocate').length, 0)
  const judge = byType(calls, 'adjudicator')[0]
  assert.equal(judge.opts.model, 'opus')
  assert.equal(judge.opts.effort, 'high')
  assert.equal(result.alive.length, 5)
})

test('analyze, standard anomaly: the statistician replaces the decomposer', async () => {
  const { calls } = await run('conundrum-analyze', { slug: 's', depth: 'standard', type: 'anomaly' }, analyzeHandler())
  assert.deepEqual(calls.filter(c => typeOf(c).startsWith('lens-')).map(typeOf),
    ['lens-statistician', 'lens-empiricist', 'lens-mechanist', 'lens-examiner', 'lens-constraints'])
})

test('analyze: fewer than two lenses completing stops before the slate', async () => {
  const fail = c => typeOf(c).startsWith('lens-') && typeOf(c) !== 'lens-constraints'
  const { result, calls } = await run('conundrum-analyze', { slug: 's' }, analyzeHandler({ fail }))
  assert.equal(result.ok, false)
  assert.equal(byType(calls, 'candidate-builder').length, 0)
})

test('analyze: calculation-heavy lenses start last, so a relaunch replays as little as possible', async () => {
  const lenses = ['constraints', 'engineer', 'decomposer', 'idealizer', 'examiner']
  const { calls } = await run('conundrum-analyze', { slug: 's', lenses }, analyzeHandler())
  assert.deepEqual(calls.filter(c => typeOf(c).startsWith('lens-')).map(typeOf),
    ['lens-decomposer', 'lens-examiner', 'lens-idealizer', 'lens-engineer', 'lens-constraints'])
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

test('analyze: a lens returning ok:false is reported failed and left out of the slate prompt', async () => {
  const handler = analyzeHandler()
  const { result, calls } = await run('conundrum-analyze', { slug: 's', type: 'feasibility' }, c =>
    (typeOf(c) === 'lens-engineer' ? { ok: false, path: '', summary: 'cut off' } : handler(c)))
  assert.deepEqual(result.lensesFailed, ['engineer'])
  assert.match(byType(calls, 'candidate-builder')[0].prompt, /completed lenses: decomposer, examiner, mechanist, constraints\)/)
  assert.equal(result.ok, true)
})

test('analyze: a failed judge returns ok:false and skips the audit', async () => {
  const fail = c => typeOf(c) === 'adjudicator'
  const { result, calls } = await run('conundrum-analyze', { slug: 's' }, analyzeHandler({ fail }))
  assert.equal(result.ok, false)
  assert.equal(result.reason, 'adjudicator failed')
  assert.equal(byType(calls, 'report-auditor').length, 0)
})

test('analyze: a failed audit still returns the report, with audit: null', async () => {
  const fail = c => typeOf(c) === 'report-auditor'
  const { result } = await run('conundrum-analyze', { slug: 's' }, analyzeHandler({ fail }))
  assert.equal(result.ok, true)
  assert.equal(result.audit, null)
  assert.equal(result.bottomLine, 'judge done')
})

test('analyze, deep: a crux advocate that fails is left out of cruxed', async () => {
  const handler = analyzeHandler()
  const { result } = await run('conundrum-analyze', { slug: 's', depth: 'deep' }, c =>
    (c.opts.label === 'crux:C2' ? { ok: false, path: '', summary: '' } : handler(c)))
  assert.deepEqual(result.cruxed, ['C1', 'C3', 'C4', 'C5'])
})

test('analyze: file-writing agents get the {ok, path, summary} shape; slate and verdicts keep theirs', async () => {
  const { calls } = await run('conundrum-analyze', { slug: 's', depth: 'deep' }, analyzeHandler())
  for (const c of calls) {
    const required = c.opts.schema?.required
    if (typeOf(c) === 'candidate-builder') assert.deepEqual(required, ['candidates'])
    else if (typeOf(c) === 'falsifier') assert.deepEqual(required, ['verdict', 'basis'])
    else if (typeOf(c) === 'math-checker') assert.deepEqual(required, [...WROTE_FIELDS, 'verified', 'refuted', 'unverified'])
    else assert.deepEqual(required, WROTE_FIELDS, c.opts.label)
  }
})

test('workflow scripts avoid APIs the runtime forbids', () => {
  for (const name of ['conundrum-research', 'conundrum-analyze']) {
    const { src } = load(name)
    assert.doesNotMatch(src, /Date\.now\(|Math\.random\(|new Date\(\)|import\(|require\(/, name)
  }
})
