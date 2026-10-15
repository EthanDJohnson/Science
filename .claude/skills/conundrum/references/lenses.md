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
| `simulator` | Galileo | A verified executable model, each candidate **run in closed loop**, and the failure boundary: the actuator limit, model error, noise, delay and disturbance at which it stops working. Must produce a verification table before any result counts | Only when the system can actually be simulated: see below |

## Choosing lenses

The main session picks lenses at the dossier checkpoint, after reading the brief's type and the dossier.

| Question type | Standard set | Add when |
|---|---|---|
| **feasibility** ("can X be done / what are the options for X") | decomposer, constraints, examiner, engineer, mechanist | idealizer if theory-heavy; dialectician if the dossier has a live contradiction; **simulator** when the system can be run |
| **design** ("how would we build X to spec") | decomposer, constraints, engineer, mechanist, examiner | idealizer for a sizing model; **simulator** when the design can be run |
| **mechanism** ("how does X work / why does theory predict Y") | mechanist, idealizer, constraints, examiner, empiricist | dialectician; **simulator** when the mechanism can be run |
| **anomaly** ("why do we observe Y") | statistician, empiricist, mechanist, constraints, examiner | decomposer; dialectician; **simulator** when a candidate cause can be modelled and its predicted shift computed |
| **foundations** ("how is the problem of time resolved", "which interpretation of quantum mechanics holds up") | examiner, decomposer, dialectician, idealizer, constraints | empiricist, when a position makes a testable prediction; mechanist |

**When to add the simulator lens.** It is the only lens that settles anything by experiment, which makes it the strongest evidence in a run when its model is verified and a waste of the run's most expensive slot when it is not. Add it when all four hold:

1. **The system has equations you can write down and integrate** from parameters the dossier gives: a robot, a vehicle, a circuit, a control loop, a reactor, a mechanism, a population model. Not a system whose governing equations are themselves the question.
2. **The parameters are measured, not guessed.** A simulation of invented parameters produces numbers with no evidential value, and they are harder to discount later than no numbers at all.
3. **It can be verified** against a conserved quantity, a known limit, a published result or a second implementation. Without a verification table its output is a demo, and the rubric weighs it as one.
4. **A run fits the budget**: seconds to minutes of wall clock per case, so the lens can also sweep the failure boundary rather than showing one nominal success.

Questions in established GR and QFT usually fail (1) or (3): a warp bubble has no closed-loop behaviour to integrate and no conserved quantity to check an integrator against, and `constraints` with `gr_tensors.py` already computes what matters there. Control, robotics, vehicle, mechanism and circuit questions usually pass all four, and for them the simulator lens is where the answer comes from. **In a standard run it displaces `mechanist`** (the causal chain is implicit in a model you can run); at deep it is added without displacing anything.

When the simulator lens produces an analysis, the refuters' `physics` angle becomes `simulation`: the strongest attack on a candidate is then to run it and find where it breaks, using the scripts the lens left in `calc/`. That substitution is automatic in the analyze workflow.

**Foundations questions** are about consistency and interpretation, not about building or explaining something. Their candidate answers are positions: each resolves the problem, dissolves it, or modifies the theory. Positions are often empirically equivalent, so they are judged on internal consistency (the math checks matter most here), on what each gives up, and on whether any observation could tell them apart. The idealizer's toy model, for example a finite-dimensional Page–Wootters clock, is often the sharpest test.

How many lenses to run at each depth:
- **quick:** 3 lenses, always `constraints` and `examiner` plus the most type-specific one (`engineer`, `mechanist`, `statistician` or, for foundations, `idealizer`).
- **standard:** the 5 in the row.
- **deep:** the 5 plus every "add when" lens that applies, up to 7.

**Worked example.** "Considering Alcubierre drives, what are viable engineering options for the negative energy required to travel at superluminal effective speeds?"
- **Type:** feasibility.
- **Standard lenses:** decomposer, constraints, examiner, engineer, mechanist.
- **Deep:** add idealizer, for a thin-wall bubble model solved in closed form. Also add dialectician if the dossier pits positive-energy warp-shell papers against energy-condition theorems.
