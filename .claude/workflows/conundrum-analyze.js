export const meta = {
  name: 'conundrum-analyze',
  description: 'Conundrum stage 2: independent lenses, candidate slate, falsification, crux round, adjudication, audit',
  whenToUse: "Run by the /conundrum skill after the dossier checkpoint; args {slug, depth, type, lenses?, stopAfter?: 'slate', slateNote?}",
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
// foundations question, so those runs attack its consistency and its cost instead. An anomaly candidate
// names the dominant cause of a discrepancy, so its refuters check the size of the shift it produces,
// the evidence, and the independent bounds it must satisfy. Angle names are single words.
const ANGLES_BY_TYPE = {
  foundations: ['consistency', 'evidence', 'cost'],
  anomaly: ['magnitude', 'evidence', 'bounds'],
}
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
if (depth === 'deep' && lenses.length < 6) log(`warning: a deep run with only ${lenses.length} lenses; lenses.md adds 1–2 more at deep`)

// ----- Lenses, then an independent math check of each (standard and deep runs).
// A resume replays saved agents only for the unchanged prefix of agent() calls, in call order, so the
// calls must come in the same order on every run. Every lens starts at once, in a fixed order. Each
// lens's math check starts once that lens and every lens before it have finished: checks still overlap
// the slower lenses, but their order no longer depends on which lens happens to finish first. (Started
// in finishing order, a resume after a container restart re-ran checks that had already finished.)
phase('Lenses')
const checkingMath = depth !== 'quick'
const settle = p => Promise.resolve(p).then(r => r, () => null)
const lensRuns = lenses.map(l => settle(agent(
  `Run directory: ${dir}. Read ${dir}/brief.md and ${dir}/dossier.md, then write ${dir}/analyses/${l}.md. ` +
  `Put any calculation scripts in ${dir}/calc/.`,
  { agentType: `lens-${l}`, label: l, phase: 'Lenses', schema: WROTE })))
const analyses = []
const mathRuns = []
for (const [i, l] of lenses.entries()) {
  const analysis = wrote(await lensRuns[i])
  analyses.push(analysis)
  mathRuns.push(analysis == null || !checkingMath ? null : settle(agent(
    `Run directory: ${dir}. Lens: ${l}. Check the load-bearing mathematics in ${dir}/analyses/${l}.md ` +
    `and write ${dir}/math/${l}.md, with your check scripts in ${dir}/math/${l}/.`,
    { agentType: 'math-checker', label: `math:${l}`, phase: 'Math', schema: MATH })))
}
const mathResults = (await Promise.all(mathRuns)).map(m => (m && m.ok ? m : null))
const lensesDone = lenses.filter((_, i) => analyses[i] != null)
const lensesFailed = lenses.filter((_, i) => analyses[i] == null)
if (lensesFailed.length) log(`lenses that failed: ${lensesFailed.join(', ')}`)
if (lensesDone.length < 2) {
  return { ok: false, reason: 'fewer than two lens analyses completed', dir, lensesDone, lensesFailed }
}
const math = {}
lenses.forEach((l, i) => {
  const m = mathResults[i]
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
// A slateNote (the user's correction after a stopAfter: 'slate' checkpoint) changes only this prompt, so
// a relaunch replays the lenses and math checks and rebuilds the slate.
const slateNote = typeof args.slateNote === 'string' && args.slateNote.trim() ? args.slateNote.trim() : ''
const slate = await agent(
  `Run directory: ${dir}. Question type: ${type}. Build the candidate slate from ${dir}/analyses/ ` +
  `(completed lenses: ${lensesDone.join(', ')}) and write ${dir}/candidates.md.` +
  (mathNote ? mathNote + ' A candidate may not rest on a claim they refuted.' : '') +
  (slateNote ? ` The user reviewed an earlier slate and asks: ${slateNote} Rewrite ${dir}/candidates.md accordingly.` : ''),
  { agentType: 'candidate-builder', schema: SLATE, label: 'slate', phase: 'Slate' })
if (!slate || !slate.candidates || !slate.candidates.length) {
  return { ok: false, reason: 'candidate slate was not produced', dir, lensesDone }
}
const seenIds = new Set()
const unique = slate.candidates.filter(c => !seenIds.has(c.id) && seenIds.add(c.id))
if (unique.length < slate.candidates.length) {
  log(`slate repeated candidate IDs; kept the first of each: ${slate.candidates.length - unique.length} dropped`)
}
// Never drop the null or reframe candidates when trimming an oversized slate.
const pinned = unique.filter(c => c.type === 'null' || c.type === 'reframe')
const room = Math.max(0, MAX_CANDIDATES - pinned.length)
const others = unique.filter(c => !(c.type === 'null' || c.type === 'reframe'))
const kept = new Set([...pinned, ...others.slice(0, room)].map(c => c.id))
const candidates = unique.filter(c => kept.has(c.id))
const trimmed = unique.filter(c => !kept.has(c.id)).map(c => c.id)
if (trimmed.length) log(`slate had ${unique.length} candidates; not falsified (over the ${MAX_CANDIDATES} cap): ${trimmed.join(', ')}`)
if (!candidates.some(c => c.type === 'null')) log('warning: the slate has no null candidate')

// The user can stop here to review a slate before the costly half (falsification, crux, judge). A relaunch
// with the same args minus stopAfter, and resumeFromRunId, replays every agent so far.
if (args.stopAfter === 'slate') {
  return { ok: true, stoppedAfter: 'slate', dir, candidates, trimmed, lenses: lensesDone, lensesFailed, math, mathFailed,
    slatePath: `${dir}/candidates.md` }
}

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
  }))))
// parallel() keeps call order, so a failed refuter (null) is identified by its position.
const slots = candidates.flatMap(c => Array.from({ length: refuters }, (_, i) => `${c.id}#${i}`))
const refutersFailed = slots.filter((_, k) => verdicts[k] == null)
const verdictsIn = verdicts.filter(Boolean)
if (refutersFailed.length) log(`refuters that failed: ${refutersFailed.join(', ')}`)

const votes = {}
const shown = {}
for (const v of verdictsIn) {
  (votes[v.id] = votes[v.id] || []).push(v.verdict);
  (shown[v.id] = shown[v.id] || []).push(refuters > 1 ? `${v.verdict} (${v.angle}, ${v.basis})` : `${v.verdict} (${v.basis})`)
}
const refutedByMajority = id => {
  const vs = votes[id] || []
  return vs.length > 0 && vs.filter(x => x === 'refuted').length * 2 > vs.length
}
const unexamined = candidates.filter(c => !votes[c.id]).map(c => c.id)
const alive = candidates.filter(c => !refutedByMajority(c.id)).map(c => c.id)
const eliminated = candidates.filter(c => refutedByMajority(c.id)).map(c => c.id)
const tally = candidates.map(c => `${c.id}: ${(shown[c.id] || ['no verdict']).join(' / ')}`).join('; ')
log(`votes: ${tally}`)
if (unexamined.length) log(`no verdict returned for ${unexamined.join(', ')}; kept alive and flagged to the judge`)
// Candidates judged on fewer verdicts than planned: a single 'refuted' can eliminate one of them.
const thin = candidates.filter(c => votes[c.id] && votes[c.id].length < refuters).map(c => c.id)

// ----- Crux (deep only): each survivor answers its own verdicts without seeing the others'.
// Evidence on multi-agent debate says extra rounds add little over independent votes, so
// standard runs rely on the decisive tests already in candidates.md instead.
// A candidate with no verdicts has nothing to answer, so it gets no advocate.
const cruxed = []
const cruxFailed = []
const answerable = alive.filter(id => !unexamined.includes(id))
if (depth === 'deep' && answerable.length >= 2) {
  phase('Crux')
  const answers = await parallel(answerable.map(id => () => agent(
    `Run directory: ${dir}. Your candidate: ${id}. Rivals: ${answerable.filter(x => x !== id).join(', ')}. ` +
    `Answer the verdicts in ${dir}/verdicts/${id}-*.md and write ${dir}/cruxes/${id}.md.`,
    { agentType: 'crux-advocate', label: `crux:${id}`, phase: 'Crux', schema: WROTE }).then(wrote)))
  answerable.forEach((id, i) => { (answers[i] != null ? cruxed : cruxFailed).push(id) })
  if (cruxFailed.length) log(`crux advocates that failed: ${cruxFailed.join(', ')}`)
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
  (thin.length ? ` Fewer verdicts than refuters (some failed): ${thin.join(', ')}.` : '') +
  (cruxFailed.length ? ` Survivors with no crux file (the advocate failed, not a concession): ${cruxFailed.join(', ')}.` : '') +
  (trimmed.length ? ` Not falsified (over the slate cap): ${trimmed.join(', ')}.` : '') +
  mathNote +
  (depth === 'deep' ? ` There are ${verdictsIn.length} verdict files${cruxed.length ? `, ${cruxed.length} crux files` : ''}` +
    `${mathChecked.length ? ` and ${mathChecked.length} math files` : ''}: read them several per step, in parallel.` : '') +
  ` Return the whole report as \`report\` in your final output; don't write it to a file.`,
  judgeOpts))
// Keep a report the judge returned even if it flagged it incomplete: losing a finished report to a
// false ok is worse than presenting it with a warning.
const report = judged && typeof judged.report === 'string' && judged.report.trim() ? judged.report : null
if (report == null) {
  return { ok: false, reason: 'adjudicator failed: no report returned', dir, candidates, alive, eliminated, unexamined,
    refutersFailed, cruxFailed }
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
  refutersFailed,
  cruxed,
  cruxFailed,
}
