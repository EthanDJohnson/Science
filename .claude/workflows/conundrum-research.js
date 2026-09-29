export const meta = {
  name: 'conundrum-research',
  description: 'Conundrum stage 1: partitioned literature research, source checks, and a compiled dossier',
  whenToUse: 'Run by the /conundrum skill after the user confirms the brief; args {slug, depth, facets?}',
  phases: [
    { title: 'Research', detail: 'one researcher per facet' },
    { title: 'Check', detail: 'a source checker behind each researcher' },
    { title: 'Dossier', detail: 'compile the checked claims' },
  ],
}

const FACETS = {
  theory: 'governing theory and established results: equations, theorems, what is proven vs. conjectured, and the standard references',
  quantitative: 'numbers: requirements, bounds, and measured or computed magnitudes, each with units, conditions and source',
  critiques: 'objections, no-go theorems, instabilities, failed or debunked proposals, and conflicting results',
  engineering: 'experimental and engineering state of the art: what has been built or measured, at what scale, and its technology readiness',
  frontier: 'recent (roughly the last five years) preprints and speculative proposals, each labelled with its evidential status',
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
log(`depth ${depth}; facets: ${facets.join(', ')}; source checks ${checking ? 'on' : 'off'}`)

// Each facet's check starts as soon as its own research finishes (no barrier).
const results = await pipeline(facets,
  f => agent(
    `Run directory: ${dir}. Your facet: ${f}. Mandate: ${FACETS[f]}. ` +
    `Read ${dir}/brief.md, then write ${dir}/research/${f}.md.`,
    { agentType: 'researcher', label: `research:${f}`, phase: 'Research', schema: WROTE })
    .then(r => (wrote(r) ? { facet: f, research: r.summary, check: null } : null)),
  (prev, f) => (prev == null || !checking) ? prev : agent(
    `Run directory: ${dir}. Check the load-bearing claims in ${dir}/research/${f}.md ` +
    `and write ${dir}/research/${f}.check.md.`,
    { agentType: 'source-checker', label: `check:${f}`, phase: 'Check', schema: WROTE })
    .then(r => ({ ...prev, check: wrote(r) ? r.summary : null })))

const done = results.filter(Boolean)
const missing = facets.filter(f => !done.some(r => r.facet === f))
const unchecked = done.filter(r => r.check == null).map(r => r.facet)
if (!done.length) {
  log('every researcher failed; no dossier compiled')
  return { ok: false, reason: 'all researchers failed', dir, missing }
}
if (missing.length) log(`facets with no research notes: ${missing.join(', ')}`)
if (checking && unchecked.length) log(`facets whose source check failed: ${unchecked.join(', ')}`)

phase('Dossier')
const dossier = wrote(await agent(
  `Run directory: ${dir}. Compile ${dir}/research/ into ${dir}/dossier.md.` +
  (missing.length ? ` These facets failed and have no notes: ${missing.join(', ')}.` : '') +
  (unchecked.length ? ` These facets have no source check: ${unchecked.join(', ')}.` : ''),
  { agentType: 'dossier-compiler', label: 'dossier', schema: WROTE }))
const dossierSummary = dossier ? dossier.summary : null

return {
  ok: dossierSummary != null,
  reason: dossierSummary == null ? 'dossier compiler failed' : undefined,
  dir,
  dossier: `${dir}/dossier.md`,
  facets: done.map(r => r.facet),
  missing,
  unchecked,
  researchSummaries: Object.fromEntries(done.map(r => [r.facet, r.research])),
  dossierSummary,
}
