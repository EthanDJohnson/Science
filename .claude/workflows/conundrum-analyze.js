export const meta = {
  name: 'conundrum-analyze',
  description: 'Conundrum stage 2: independent lenses, candidate slate, falsification, crux round, adjudication, audit',
  whenToUse: 'Run by the /conundrum skill after the dossier checkpoint; args {slug, depth, type, lenses?}',
  phases: [
    { title: 'Lenses', detail: 'independent analyses of the dossier' },
    { title: 'Slate', detail: 'competing candidate answers' },
    { title: 'Falsify', detail: 'refuters per candidate' },
    { title: 'Crux', detail: 'deep runs: survivors answer their verdicts' },
    { title: 'Judge', detail: 'neutral adjudication' },
    { title: 'Audit', detail: 'trace every report claim' },
  ],
}

const LENSES = ['decomposer', 'constraints', 'examiner', 'engineer', 'mechanist', 'idealizer', 'empiricist', 'dialectician']
const DEFAULT_LENSES = {
  feasibility: ['decomposer', 'constraints', 'examiner', 'engineer', 'mechanist'],
  design: ['decomposer', 'constraints', 'engineer', 'mechanist', 'examiner'],
  mechanism: ['mechanist', 'idealizer', 'constraints', 'examiner', 'empiricist'],
  anomaly: ['decomposer', 'mechanist', 'empiricist', 'constraints', 'examiner'],
}
const QUICK_THIRD = { feasibility: 'engineer', design: 'engineer', mechanism: 'mechanist', anomaly: 'empiricist' }
const ANGLES = ['physics', 'evidence', 'scale']
const MAX_CANDIDATES = 8

const SLATE = {
  type: 'object',
  required: ['candidates'],
  properties: {
    candidates: {
      type: 'array',
      items: {
        type: 'object',
        required: ['id', 'claim', 'type'],
        properties: {
          id: { type: 'string' },
          claim: { type: 'string' },
          type: { type: 'string', enum: ['mechanism', 'option', 'explanation', 'null', 'reframe'] },
        },
      },
    },
  },
}
const VERDICT = {
  type: 'object',
  required: ['verdict', 'basis'],
  properties: {
    verdict: { type: 'string', enum: ['refuted', 'weakened', 'survives'] },
    basis: { type: 'string', enum: ['calculation', 'cited-evidence', 'internal-inconsistency', 'none'] },
  },
}

// Every file-writing agent reports back in this shape. An agent cut off by its turn
// limit can't produce it, so a missing file shows up as a failure, not a silent gap.
const WROTE = {
  type: 'object',
  required: ['ok', 'path', 'summary'],
  properties: {
    ok: { type: 'boolean' },
    path: { type: 'string' },
    summary: { type: 'string' },
  },
}
const wrote = r => (r && r.ok ? r : null)

if (!args || !args.slug) throw new Error('conundrum-analyze needs args.slug (the run directory under runs/)')
const dir = `runs/${args.slug}`
const depth = ['quick', 'standard', 'deep'].includes(args.depth) ? args.depth : 'standard'
const type = DEFAULT_LENSES[args.type] ? args.type : 'feasibility'
let requested = args.lenses && args.lenses.length ? args.lenses : DEFAULT_LENSES[type]
if (depth === 'quick' && !(args.lenses && args.lenses.length)) requested = ['constraints', 'examiner', QUICK_THIRD[type]]
const unknownLenses = requested.filter(l => !LENSES.includes(l))
if (unknownLenses.length) log(`ignoring unknown lenses: ${unknownLenses.join(', ')}`)
const lenses = [...new Set(requested.filter(l => LENSES.includes(l)))]
const refuters = depth === 'deep' ? 3 : 1
log(`depth ${depth}; type ${type}; lenses: ${lenses.join(', ')}; refuters per candidate: ${refuters}`)

// ----- Lenses: independent and isolated; the slate needs all of them, so this barrier is intentional.
phase('Lenses')
const analyses = await parallel(lenses.map(l => () => agent(
  `Run directory: ${dir}. Read ${dir}/brief.md and ${dir}/dossier.md, then write ${dir}/analyses/${l}.md. ` +
  `Put any calculation scripts in ${dir}/calc/.`,
  { agentType: `lens-${l}`, label: l, phase: 'Lenses', schema: WROTE }).then(wrote)))
const lensesDone = lenses.filter((_, i) => analyses[i] != null)
const lensesFailed = lenses.filter((_, i) => analyses[i] == null)
if (lensesFailed.length) log(`lenses that failed: ${lensesFailed.join(', ')}`)
if (lensesDone.length < 2) {
  return { ok: false, reason: 'fewer than two lens analyses completed', dir, lensesDone, lensesFailed }
}

// ----- Slate
phase('Slate')
const slate = await agent(
  `Run directory: ${dir}. Build the candidate slate from ${dir}/analyses/ ` +
  `(completed lenses: ${lensesDone.join(', ')}) and write ${dir}/candidates.md.`,
  { agentType: 'candidate-builder', schema: SLATE, label: 'slate', phase: 'Slate' })
if (!slate || !slate.candidates || !slate.candidates.length) {
  return { ok: false, reason: 'candidate slate was not produced', dir, lensesDone }
}
const seenIds = new Set()
const unique = slate.candidates.filter(c => !seenIds.has(c.id) && seenIds.add(c.id))
// Never drop the null or reframe candidates when trimming an oversized slate.
const pinned = unique.filter(c => c.type === 'null' || c.type === 'reframe')
const room = Math.max(0, MAX_CANDIDATES - pinned.length)
const others = unique.filter(c => !(c.type === 'null' || c.type === 'reframe'))
const kept = new Set([...pinned, ...others.slice(0, room)].map(c => c.id))
const candidates = unique.filter(c => kept.has(c.id))
const trimmed = unique.filter(c => !kept.has(c.id)).map(c => c.id)
if (trimmed.length) log(`slate had ${unique.length} candidates; not falsified (over the ${MAX_CANDIDATES} cap): ${trimmed.join(', ')}`)
if (!candidates.some(c => c.type === 'null')) log('warning: the slate has no null candidate')

// ----- Falsify: independent refuters; deep mode gives each a different angle.
phase('Falsify')
const verdicts = (await parallel(candidates.flatMap(c =>
  Array.from({ length: refuters }, (_, i) => () => {
    const angle = refuters === 1 ? 'strongest available (physics, evidence or scale; say which)' : ANGLES[i % ANGLES.length]
    return agent(
      `Run directory: ${dir}. Candidate ${c.id} (${c.type}): "${c.claim}". You are refuter ${i}; angle: ${angle}. ` +
      `Write ${dir}/verdicts/${c.id}-${i}.md.`,
      { agentType: 'falsifier', schema: VERDICT, label: `${c.id}#${i}`, phase: 'Falsify' })
      .then(v => (v == null ? null : { id: c.id, refuter: i, angle, verdict: v.verdict, basis: v.basis }))
  })))).filter(Boolean)

const votes = {}
for (const v of verdicts) (votes[v.id] = votes[v.id] || []).push(v.verdict)
const refutedByMajority = id => {
  const vs = votes[id] || []
  return vs.length > 0 && vs.filter(x => x === 'refuted').length * 2 > vs.length
}
const unexamined = candidates.filter(c => !votes[c.id]).map(c => c.id)
const alive = candidates.filter(c => !refutedByMajority(c.id)).map(c => c.id)
const eliminated = candidates.filter(c => refutedByMajority(c.id)).map(c => c.id)
const tally = candidates.map(c => `${c.id}: ${(votes[c.id] || ['no verdict']).join('/')}`).join('; ')
log(`votes: ${tally}`)
if (unexamined.length) log(`no verdict returned for ${unexamined.join(', ')}; kept alive and flagged to the judge`)

// ----- Crux (deep only): each survivor answers its own verdicts without seeing the others'.
// Evidence on multi-agent debate says extra rounds add little over independent votes, so
// standard runs rely on the decisive tests already in candidates.md instead.
const cruxed = []
if (depth === 'deep' && alive.length >= 2) {
  phase('Crux')
  const answers = await parallel(alive.map(id => () => agent(
    `Run directory: ${dir}. Your candidate: ${id}. Rivals: ${alive.filter(x => x !== id).join(', ')}. ` +
    `Answer the verdicts in ${dir}/verdicts/${id}-*.md and write ${dir}/cruxes/${id}.md.`,
    { agentType: 'crux-advocate', label: `crux:${id}`, phase: 'Crux', schema: WROTE }).then(wrote)))
  alive.forEach((id, i) => { if (answers[i] != null) cruxed.push(id) })
}

// ----- Judge: Fable at high by default; quick runs use Opus, deep runs raise effort to max.
phase('Judge')
const judgeOpts = { agentType: 'adjudicator', label: 'judge', phase: 'Judge', schema: WROTE }
if (depth === 'quick') Object.assign(judgeOpts, { model: 'opus', effort: 'high' })
if (depth === 'deep') judgeOpts.effort = 'max'
const judged = wrote(await agent(
  `Run directory: ${dir}. Adjudicate from ${dir}/brief.md, ${dir}/dossier.md, ${dir}/candidates.md and ${dir}/verdicts/` +
  (cruxed.length ? ` and ${dir}/cruxes/` : '') + `. Refuter votes: ${tally}.` +
  (unexamined.length ? ` Unexamined (refuters failed): ${unexamined.join(', ')}.` : '') +
  (trimmed.length ? ` Not falsified (over the slate cap): ${trimmed.join(', ')}.` : '') +
  ` Write ${dir}/report.md.`,
  judgeOpts))
const bottomLine = judged ? judged.summary : null
if (bottomLine == null) {
  return { ok: false, reason: 'adjudicator failed', dir, candidates, alive, eliminated, unexamined }
}

// ----- Audit
phase('Audit')
const audited = wrote(await agent(
  `Run directory: ${dir}. Audit ${dir}/report.md against the run's evidence and write ${dir}/audit.md.`,
  { agentType: 'report-auditor', label: 'audit', phase: 'Audit', schema: WROTE }))
const auditSummary = audited ? audited.summary : null

return {
  ok: true,
  dir,
  report: `${dir}/report.md`,
  audit: auditSummary == null ? null : `${dir}/audit.md`,
  bottomLine,
  auditSummary,
  lenses: lensesDone,
  lensesFailed,
  candidates,
  trimmed,
  alive,
  eliminated,
  unexamined,
  cruxed,
}
