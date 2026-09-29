export const meta = {
  name: 'conundrum-analyze',
  description: 'Conundrum stage 2: independent lenses, candidate slate, falsification, crux round, adjudication, audit',
  whenToUse: 'Run by the /conundrum skill after the dossier checkpoint; args {slug, depth, type, lenses?}',
  phases: [
    { title: 'Lenses', detail: 'independent analyses of the dossier' },
    { title: 'Math', detail: "standard and deep runs: each lens's mathematics re-derived independently" },
    { title: 'Slate', detail: 'competing candidate answers' },
    { title: 'Falsify', detail: 'refuters per candidate' },
    { title: 'Crux', detail: 'deep runs: survivors answer their verdicts' },
    { title: 'Judge', detail: 'neutral adjudication' },
    { title: 'Audit', detail: 'trace every report claim' },
  ],
}

const LENSES = ['decomposer', 'constraints', 'examiner', 'engineer', 'mechanist', 'idealizer', 'empiricist', 'dialectician', 'statistician']
const DEFAULT_LENSES = {
  feasibility: ['decomposer', 'constraints', 'examiner', 'engineer', 'mechanist'],
  design: ['decomposer', 'constraints', 'engineer', 'mechanist', 'examiner'],
  mechanism: ['mechanist', 'idealizer', 'constraints', 'examiner', 'empiricist'],
  anomaly: ['statistician', 'empiricist', 'mechanist', 'constraints', 'examiner'],
  foundations: ['examiner', 'decomposer', 'dialectician', 'idealizer', 'constraints'],
}
const QUICK_THIRD = { feasibility: 'engineer', design: 'engineer', mechanism: 'mechanist', anomaly: 'statistician',
  foundations: 'idealizer' }
// Deep runs give each refuter a different angle. Engineering scale means nothing to a position on a
// foundations question, so those runs attack its consistency and its cost instead.
const ANGLES_BY_TYPE = { foundations: ['consistency', 'evidence', 'cost'] }
const DEFAULT_ANGLES = ['physics', 'evidence', 'scale']
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
          type: { type: 'string', enum: ['mechanism', 'option', 'explanation', 'position', 'null', 'reframe'] },
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
// The judge returns the report as text: Claude Code refuses a subagent's write to a file named
// report*.md ("Subagents should return findings as text, not write report files"), so the main
// session saves it (SKILL.md step 5).
const REPORT = {
  type: 'object',
  required: ['ok', 'report', 'summary'],
  properties: {
    ok: { type: 'boolean' },
    report: { type: 'string' },
    summary: { type: 'string' },
  },
}
// A math checker reports its claim counts as well.
const MATH = {
  type: 'object',
  required: ['ok', 'path', 'summary', 'verified', 'refuted', 'unverified'],
  properties: {
    ok: { type: 'boolean' },
    path: { type: 'string' },
    summary: { type: 'string' },
    verified: { type: 'integer' },
    refuted: { type: 'integer' },
    unverified: { type: 'integer' },
  },
}

if (!args || !args.slug) throw new Error('conundrum-analyze needs args.slug (the run directory under runs/)')
const dir = `runs/${args.slug}`
const depth = ['quick', 'standard', 'deep'].includes(args.depth) ? args.depth : 'standard'
const type = DEFAULT_LENSES[args.type] ? args.type : 'feasibility'
let requested = args.lenses && args.lenses.length ? args.lenses : DEFAULT_LENSES[type]
if (depth === 'quick' && !(args.lenses && args.lenses.length)) requested = ['constraints', 'examiner', QUICK_THIRD[type]]
const unknownLenses = requested.filter(l => !LENSES.includes(l))
if (unknownLenses.length) log(`ignoring unknown lenses: ${unknownLenses.join(', ')}`)
const chosen = [...new Set(requested.filter(l => LENSES.includes(l)))]
// A relaunch after a failure replays the failed agent and every agent that started after it, even
// completed ones. Start the calculation-heavy lenses last: they are the likeliest to run long or fail.
const HEAVY = ['idealizer', 'engineer', 'constraints']
const lenses = [...chosen.filter(l => !HEAVY.includes(l)), ...HEAVY.filter(l => chosen.includes(l))]
const refuters = depth === 'deep' ? 3 : 1
const ANGLES = ANGLES_BY_TYPE[type] || DEFAULT_ANGLES
log(`depth ${depth}; type ${type}; lenses: ${lenses.join(', ')}; refuters per candidate: ${refuters}`)

// ----- Lenses: independent and isolated. In standard and deep runs, each lens's mathematics goes to
// an independent math checker as soon as that lens finishes (no barrier). The slate needs every lens
// and its check, so the wait after this stage is intentional.
phase('Lenses')
const checkingMath = depth !== 'quick'
const lensResults = await pipeline(lenses,
  l => agent(
    `Run directory: ${dir}. Read ${dir}/brief.md and ${dir}/dossier.md, then write ${dir}/analyses/${l}.md. ` +
    `Put any calculation scripts in ${dir}/calc/.`,
    { agentType: `lens-${l}`, label: l, phase: 'Lenses', schema: WROTE }).then(wrote),
  (analysis, l) => (analysis == null || !checkingMath) ? { analysis, math: null } : agent(
    `Run directory: ${dir}. Lens: ${l}. Check the load-bearing mathematics in ${dir}/analyses/${l}.md ` +
    `and write ${dir}/math/${l}.md, with your check scripts in ${dir}/math/${l}/.`,
    { agentType: 'math-checker', label: `math:${l}`, phase: 'Math', schema: MATH })
    .then(m => ({ analysis, math: m && m.ok ? m : null })))
const analyses = lensResults.map(r => (r ? r.analysis : null))
const lensesDone = lenses.filter((_, i) => analyses[i] != null)
const lensesFailed = lenses.filter((_, i) => analyses[i] == null)
if (lensesFailed.length) log(`lenses that failed: ${lensesFailed.join(', ')}`)
if (lensesDone.length < 2) {
  return { ok: false, reason: 'fewer than two lens analyses completed', dir, lensesDone, lensesFailed }
}
const math = {}
lenses.forEach((l, i) => {
  const m = lensResults[i] && lensResults[i].math
  if (m) math[l] = { verified: m.verified || 0, refuted: m.refuted || 0, unverified: m.unverified || 0 }
})
const mathChecked = Object.keys(math)
const mathFailed = checkingMath ? lensesDone.filter(l => !math[l]) : []
if (mathFailed.length) log(`math checks that failed: ${mathFailed.join(', ')}`)
const mathTally = mathChecked.map(l => `${l}: ${math[l].verified} verified, ${math[l].refuted} refuted, ` +
  `${math[l].unverified} unverified`).join('; ')
if (mathChecked.length) log(`math checks: ${mathTally}`)
const mathNote = mathChecked.length
  ? ` Math checks of the lenses are in ${dir}/math/ (${mathTally}).` +
    (mathFailed.length ? ` The math of ${mathFailed.join(', ')} went unchecked.` : '')
  : ''

// ----- Slate
phase('Slate')
const slate = await agent(
  `Run directory: ${dir}. Question type: ${type}. Build the candidate slate from ${dir}/analyses/ ` +
  `(completed lenses: ${lensesDone.join(', ')}) and write ${dir}/candidates.md.` +
  (mathNote ? mathNote + ' A candidate may not rest on a claim they refuted.' : ''),
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
    const angle = refuters === 1 ? `strongest available (${ANGLES.join(', ')}; say which)` : ANGLES[i % ANGLES.length]
    return agent(
      `Run directory: ${dir}. Candidate ${c.id} (${c.type}): "${c.claim}". You are refuter ${i}; angle: ${angle}. ` +
      `Write ${dir}/verdicts/${c.id}-${i}.md.` +
      (mathChecked.length ? ` The math checks in ${dir}/math/ count as calculations: a claim they refuted is grounds for a verdict.` : ''),
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
const judgeOpts = { agentType: 'adjudicator', label: 'judge', phase: 'Judge', schema: REPORT }
if (depth === 'quick') Object.assign(judgeOpts, { model: 'opus', effort: 'high' })
if (depth === 'deep') judgeOpts.effort = 'max'
const judged = (await agent(
  `Run directory: ${dir}. Question type: ${type}. Adjudicate from ${dir}/brief.md, ${dir}/dossier.md, ${dir}/candidates.md and ${dir}/verdicts/` +
  (cruxed.length ? ` and ${dir}/cruxes/` : '') + `. Refuter votes: ${tally}.` +
  (unexamined.length ? ` Unexamined (refuters failed): ${unexamined.join(', ')}.` : '') +
  (trimmed.length ? ` Not falsified (over the slate cap): ${trimmed.join(', ')}.` : '') +
  mathNote +
  ` Return the whole report as \`report\` in your final output; don't write it to a file.`,
  judgeOpts))
// Keep a report the judge returned even if it flagged it incomplete: losing a finished report to a
// false ok is worse than presenting it with a warning.
const report = judged && typeof judged.report === 'string' && judged.report.trim() ? judged.report : null
if (report == null) {
  return { ok: false, reason: 'adjudicator failed: no report returned', dir, candidates, alive, eliminated, unexamined }
}
const reportIncomplete = !judged.ok
if (reportIncomplete) log('the judge returned its report but did not mark it complete')
const bottomLine = judged.summary || null

// ----- Audit
phase('Audit')
const audited = wrote(await agent(
  `Run directory: ${dir}. Audit the judge's report below against the run's evidence and write ${dir}/audit.md. ` +
  `The main session saves the report as ${dir}/report.md after this workflow, so read it here.` +
  (mathChecked.length ? ` Trace the report's mathematical claims to the math checks in ${dir}/math/.` : '') +
  `\n<report>\n${report}\n</report>`,
  { agentType: 'report-auditor', label: 'audit', phase: 'Audit', schema: WROTE }))
const auditSummary = audited ? audited.summary : null

return {
  ok: true,
  dir,
  // The main session must save this text verbatim as reportPath before anything else.
  report,
  reportPath: `${dir}/report.md`,
  reportIncomplete,
  audit: auditSummary == null ? null : `${dir}/audit.md`,
  bottomLine,
  auditSummary,
  lenses: lensesDone,
  lensesFailed,
  math,
  mathFailed,
  candidates,
  trimmed,
  alive,
  eliminated,
  unexamined,
  cruxed,
}
