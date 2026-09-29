# Lens catalog and selection rules

Each lens is an independent Opus analyst with its own method, defined in `.claude/agents/lens-<name>.md`. Lenses never see each other's work. The philosopher label is only a mnemonic: the method instructions do the work. Whether the persona wording adds anything is an open question; the eval plan in `docs/conundrum-skill-plan.md` §5.8 tests it.

| Lens (agent) | Label | Must produce | Best for |
|---|---|---|---|
| `decomposer` | Descartes | Sub-question tree; **assumption ledger** (measured / derived / assumed / unknown); the one assumption whose failure would dissolve the question | Always |
| `constraints` | Kant | Energy conditions, conservation, thermodynamic, causal and quantum-inequality limits, dimensional analysis and magnitudes, **computed in Python**; validity domain of each model | Always for physics |
| `examiner` | Socrates | Challenges the framing: is the question well posed, is the premise true, does "viable" or "superluminal" mean what it seems? Gives the 5–10 hardest questions no current answer handles | Always |
| `engineer` | Archimedes | Requirement vs. best demonstrated capability as an **orders-of-magnitude gap**, scaling laws, power and energy budgets, materials and control limits, TRL, next milestone experiment | Feasibility and design questions |
| `mechanist` | Aristotle | A causal chain for each candidate mechanism or option; what kind of phenomenon each relies on | Questions asking "how" or "which options" |
| `idealizer` | Plato | The simplest idealized or toy model that captures the question, **solved**, plus where reality departs from it | Theory-heavy questions |
| `empiricist` | Hume | What has actually been observed or measured vs. inferred; base rates (how often do claims like this survive?); analogous cases | Anomalies; claims resting on experiments |
| `dialectician` | Hegel | For two well-supported but conflicting bodies of evidence: the regime or condition under which both hold | When the dossier's "Contested" section has a real contradiction |
| `statistician` | Bayes | For each claimed signal: local and **global** significance (look-elsewhere effect), systematics, the Bayes-factor bound and the prior the claim needs, the failure modes that apply, and the data that would settle it, **computed with `stats_tools.py`** | Anomalies; any claim resting on a marginal measurement |

## Choosing lenses

The main session picks lenses at the dossier checkpoint, after reading the brief's type and the dossier.

| Question type | Standard set | Add when |
|---|---|---|
| **feasibility** ("can X be done / what are the options for X") | decomposer, constraints, examiner, engineer, mechanist | idealizer if theory-heavy; dialectician if the dossier has a live contradiction |
| **design** ("how would we build X to spec") | decomposer, constraints, engineer, mechanist, examiner | idealizer for a sizing model |
| **mechanism** ("how does X work / why does theory predict Y") | mechanist, idealizer, constraints, examiner, empiricist | dialectician |
| **anomaly** ("why do we observe Y") | statistician, empiricist, mechanist, constraints, examiner | decomposer; dialectician |

How many lenses to run at each depth:
- **quick:** 3 lenses, always `constraints` and `examiner` plus the most type-specific one (`engineer`, `mechanist` or `statistician`).
- **standard:** the 5 in the row.
- **deep:** the 5 plus every "add when" lens that applies, up to 7.

**Worked example.** "Considering Alcubierre drives, what are viable engineering options for the negative energy required to travel at superluminal effective speeds?"
- **Type:** feasibility.
- **Standard lenses:** decomposer, constraints, examiner, engineer, mechanist.
- **Deep:** add idealizer, for a thin-wall bubble model solved in closed form. Also add dialectician if the dossier pits positive-energy warp-shell papers against energy-condition theorems.
