export const meta = {
  name: 'conundrum-research',
  description: 'Conundrum stage 1: partitioned literature research, source checks, and a compiled dossier',
  whenToUse: 'Run by the /conundrum skill after the user confirms the brief; args {slug, depth, type?, facets?, tools?, prior?}',
  phases: [
    { title: 'Tools', detail: 'toolsmiths build requested calculators alongside the research' },
    { title: 'Research', detail: 'one researcher per facet' },
    { title: 'Check', detail: 'a source checker behind each researcher' },
    { title: 'Dossier', detail: 'compile the checked claims' },
  ],
}

const FACETS = {
  theory: 'governing theory and established results: equations, theorems, what is proven vs. conjectured, and the standard references',
  quantitative: 'numbers: requirements, bounds, and measured or computed magnitudes, each with units, conditions and source; ' +
    'for measurements, the statistical and systematic uncertainties exactly as quoted, and any value a re-analysis or erratum superseded',
  critiques: 'objections, no-go theorems, instabilities, failed or debunked proposals, and conflicting results',
  engineering: 'experimental and engineering state of the art: what has been built or measured, at what scale, and its technology readiness; ' +
    'and the planned or running experiments that will improve on it: who, the target precision and when results are expected',
  frontier: 'recent (roughly the last five years) results, preprints, conference talks and proposals, newest first, each labelled with its evidential status',
}
// An anomaly turns on each experiment's error budget, which no generic facet asks for, and not on
// technology readiness. The facet keys stay the same, so labels and file names don't change.
const FACETS_BY_TYPE = {
  anomaly: {
    engineering: 'the measurements themselves, method by method: every result bearing on the anomaly with its statistical and ' +
      'systematic uncertainties exactly as quoted, the largest items of each systematic budget, blinding, the in-situ tests each ' +
      'experiment ran, which results supersede or re-analyse others, and which share an apparatus; and the planned or running ' +
      'experiments that will improve on them: who, the target precision and when results are expected',
  },
}
const DEFAULT_FACETS = {
  quick: ['theory', 'quantitative', 'critiques'],
  standard: ['theory', 'quantitative', 'critiques', 'engineering'],
  deep: ['theory', 'quantitative', 'critiques', 'engineering', 'frontier'],
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

if (!args || !args.slug) throw new Error('conundrum-research needs args.slug (the run directory under runs/)')
const dir = `runs/${args.slug}`
const depth = DEFAULT_FACETS[args.depth] ? args.depth : 'standard'
const requested = args.facets && args.facets.length ? args.facets : DEFAULT_FACETS[depth]
const unknown = requested.filter(f => !FACETS[f])
if (unknown.length) log(`ignoring unknown facets: ${unknown.join(', ')}`)
const facets = requested.filter(f => FACETS[f])
if (!facets.length) throw new Error('no valid facets to research')
const checking = depth !== 'quick'
const type = typeof args.type === 'string' ? args.type : ''
const mandate = f => ((FACETS_BY_TYPE[type] || {})[f]) || FACETS[f]
log(`depth ${depth}; ${type ? `type ${type}; ` : ''}facets: ${facets.join(', ')}; source checks ${checking ? 'on' : 'off'}`)

// Calculators agreed at framing (SKILL.md step 1). Toolsmiths start alongside the researchers and
// write only into the run folder; the main session promotes a calculator into the shared toolkit.
const TOOL_NAME = /^[a-z][a-z0-9_]{2,40}$/
const requestedTools = Array.isArray(args.tools) ? args.tools : []
const tools = requestedTools.filter(t => t && TOOL_NAME.test(t.name || '') && typeof t.purpose === 'string' && t.purpose)
if (tools.length < requestedTools.length) {
  log(`ignoring ${requestedTools.length - tools.length} tool request(s) without a snake_case name and a purpose`)
}
const toolRuns = parallel(tools.map(t => () => agent(
  `Run directory: ${dir}. Build the calculator "${t.name}": ${t.purpose}. ` +
  `Write ${dir}/tools/${t.name}.py in the tool format and run its selftest.`,
  { agentType: 'toolsmith', label: `tool:${t.name}`, phase: 'Tools', schema: WROTE })
  .then(r => ({ name: t.name, ...(wrote(r) || { ok: false, path: `${dir}/tools/${t.name}.py`, summary: 'toolsmith failed' }) }))))

// Earlier runs the user approved at framing (SKILL.md step 1), as [{slug, mode}]. The main session
// has copied each into ${dir}/prior/<slug>/, whose PROVENANCE.md says how its notes may be used.
// Conclusions never come across, so only researchers are told about them.
const RUN_NAME = /^[A-Za-z0-9][A-Za-z0-9._-]*$/
const requestedPrior = Array.isArray(args.prior) ? args.prior : []
const prior = requestedPrior.filter(p => p && RUN_NAME.test(p.slug || '') && ['leads', 'update'].includes(p.mode))
if (prior.length < requestedPrior.length) {
  log(`ignoring ${requestedPrior.length - prior.length} earlier-run entries without a run name and a mode of leads or update`)
}
if (prior.length) log(`building on earlier runs: ${prior.map(p => `${p.slug} (${p.mode})`).join(', ')}`)
const priorNote = prior.length
  ? ` Earlier runs to build on: ${prior.map(p => `${dir}/prior/${p.slug}/ (${p.mode})`).join(', ')}. ` +
    `Read each one's PROVENANCE.md before searching; it says how its notes may be used.`
  : ''

// A resume replays saved agents only for the unchanged prefix of agent() calls, in call order, so the
// calls must come in the same order on every run. Every researcher starts at once, in a fixed order;
// each facet's source check starts once that facet's research and every earlier facet's have finished.
// Checks still overlap slower researchers, but their order no longer depends on who finishes first.
const settle = p => Promise.resolve(p).then(r => r, () => null)
const researchRuns = facets.map(f => settle(agent(
  `Run directory: ${dir}. Your facet: ${f}. Mandate: ${mandate(f)}. ` +
  `Read ${dir}/brief.md (its Research facets section scopes this mandate), then write ${dir}/research/${f}.md.` + priorNote,
  { agentType: 'researcher', label: `research:${f}`, phase: 'Research', schema: WROTE })))
const results = []
const checkRuns = []
for (const [i, f] of facets.entries()) {
  const r = wrote(await researchRuns[i])
  results.push(r ? { facet: f, research: r.summary, check: null } : null)
  checkRuns.push(r == null || !checking ? null : settle(agent(
    `Run directory: ${dir}. Check the load-bearing claims in ${dir}/research/${f}.md ` +
    `and write ${dir}/research/${f}.check.md.`,
    { agentType: 'source-checker', label: `check:${f}`, phase: 'Check', schema: WROTE })))
}
const checks = await Promise.all(checkRuns)
results.forEach((r, i) => { if (r) r.check = wrote(checks[i]) ? checks[i].summary : null })

const done = results.filter(Boolean)
const missing = facets.filter(f => !done.some(r => r.facet === f))
const unchecked = done.filter(r => r.check == null).map(r => r.facet)
if (!done.length) {
  log('every researcher failed; no dossier compiled')
  return { ok: false, reason: 'all researchers failed', dir, missing, tools: (await toolRuns).filter(Boolean) }
}
if (missing.length) log(`facets with no research notes: ${missing.join(', ')}`)
if (checking && unchecked.length) log(`facets whose source check failed: ${unchecked.join(', ')}`)

phase('Dossier')
const dossier = wrote(await agent(
  `Run directory: ${dir}. Compile ${dir}/research/ into ${dir}/dossier.md.` +
  (missing.length ? ` These facets failed and have no notes: ${missing.join(', ')}.` : '') +
  (unchecked.length ? ` These facets have no source check: ${unchecked.join(', ')}.` : '') +
  (prior.length ? ' Claims with a PRIOR line were carried from earlier runs: keep the line, and count them in your summary.' : ''),
  { agentType: 'dossier-compiler', label: 'dossier', schema: WROTE }))
const dossierSummary = dossier ? dossier.summary : null
const builtTools = (await toolRuns).filter(Boolean)
const failedTools = builtTools.filter(t => !t.ok).map(t => t.name)
if (failedTools.length) log(`calculators not built: ${failedTools.join(', ')}`)

return {
  ok: dossierSummary != null,
  reason: dossierSummary == null ? 'dossier compiler failed' : undefined,
  dir,
  dossier: `${dir}/dossier.md`,
  facets: done.map(r => r.facet),
  prior: prior.map(p => p.slug),
  missing,
  unchecked,
  researchSummaries: Object.fromEntries(done.map(r => [r.facet, r.research])),
  dossierSummary,
  tools: builtTools,
}
