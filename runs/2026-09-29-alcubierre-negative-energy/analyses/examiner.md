# Analysis: examiner (examine the question before answering it)

## Method applied
Define the loaded terms of the question ("superluminal effective speed", "negative energy", "required", "viable", "engineering option"), test each hidden premise (brief's seven plus ones found here) for support, falsifier and what the question becomes if it fails, look for a better-posed nearby question, and list the hardest checkable questions any answer must survive. Units: geometric (G = c = 1) unless marked SI.

## Findings
1. **The free-field quantum inequality (QI) caps wall thickness from above, not below.** So the brief's own reference wall (Δ = 1 m) is not available to any source that the proven QIs govern. Pfenning–Ford, verbatim: "∆ ≤ 10² vb LPlanck … Thus, unless vb is extremely large, the wall thickness cannot be much above the Planck scale" [new: Pfenning & Ford 1997, arXiv gr-qc/9702026, full-text, "the wall thickness cannot be much above the Planck scale"] [D-13, D-55].
   - The reason: demand grows as |ρ| ~ v²/Δ², while the QI bound, with sampling time αΔ/v, grows as v⁴/(α⁴Δ⁴). The ratio of demand to allowed density is therefore (Δ/Δ_max)².
   - At v = 10c and Δ = 1 m that ratio is 10^63.6. At Δ = 1 fm it is still 10^33.6 [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-examiner_premises.py].
   - Consequence: the Δ = 1 m figure of −7.5e31 kg (38 M_sun) [D-17] and the thick-wall floor of −1.1e30 kg [D-19] describe classical exotic matter. That lies outside established physics. They do not describe Casimir or squeezed-vacuum sources, for which the QI-consistent figure is −4.6e63 kg (2.3e33 M_sun) [D-18].
   - "Supply" options (quantum sources) and "shrink" options (thick walls, White) therefore pull in opposite directions and cannot simply be combined.
   - Caveat: the QI is proven for free fields in flat space only [D-54, U-09].
2. **At v > c, most of the negative energy must sit where nothing can ride along with the bubble.**
   - A worldline x = x0 + vt is timelike only where f > 1 − 1/v. The surface f = 1 − 1/v is also the ship's forward horizon.
   - Fraction of the Eulerian negative energy lying at f < 1 − 1/v, at v = 10c:
     - tanh profile: 97%;
     - linear ramp: 90%;
     - Bobrick–Martire optimal f = min(r0/r, 1): 90%.
   - At v = 2c the fraction is 50% for every profile, and at v ≤ 1 it is 0 [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-examiner_premises.py].
   - So a superluminal source cannot be a material shell carried by the ship. It has to be a *pattern* written into matter or fields that are already in place along the route. This restates Everett–Roman's control problem [D-58] as a statement about sourcing. The premise that the negative energy is something the ship brings with it fails.
3. **The QI-limited wall approaches Planck density.** At v = 10c and R = 100 m, a wall of Δ_max = 1.6e-32 m has a volume of 2.0e-27 m³. Holding 4.6e63 kg there gives a mean |ρ| of 2.3e90 kg/m³, which is 4.4e-7 of the Planck density, 5.2e96 kg/m³ (SI) [calc: same]. A semiclassical treatment is marginal there, which is the same reason the Van Den Broeck neck is doubtful [D-25].
4. **Casimir negative energy comes with far more positive mass (ideal plates, T = 0).**
   - Two graphene monolayers weigh 3.2e11 times the gap's |E|/c² at a 1 nm gap, and 3.2e17 times at 100 nm.
   - Two 50 nm gold films weigh 4.0e14 times at 1 nm.
   - These ratios use assumed plate areal masses (graphene 7.6e-7 kg/m² per sheet; gold 19,300 kg/m³). The ideal-conductor formula is the most favourable case [calc: same].
   - The system as a whole always has net positive energy, so "separating" the negative part is the real engineering problem [D-08, D-35]. The brief's smoke-test ratio of 7.7e9 is not reproduced by these assumptions; it is lower than mine by 1.6 to 4.7 orders of magnitude.
5. **"Total negative energy" is not an invariant budget.** For unit-lapse, flat-slice drives (the Natário class [D-51]), the spatial metric is exactly δ_ij, so the ADM mass is identically zero, while ∫ρ_Eulerian < 0 [D-02]. The Eulerian integral depends on the slicing, not on anything an outside observer could weigh. The binding quantities are local: ρ_u for every u, the stresses [D-06], and QI-sampled density [D-54]. This supports hidden premise 2 of the brief: Eulerian E is not the right budget. (This is our own inference from the definition of ADM mass; no source was opened for it.)
6. **A bubble the traveller makes after leaving cannot shorten the one-way trip.** Krasnikov, verbatim: "It is argued that under some reasonable assumptions in globally hyperbolic spacetimes the traveller cannot hasten reaching the destination" [new: Krasnikov 1998, Phys. Rev. D 57, 4760, abstract, "under some reasonable assumptions in globally hyperbolic spacetimes the traveller cannot hasten reaching the destination"] [D-59].
   - Findings 2 and 6, together with [D-58] and [D-62], all say the same thing: the bubble can only be superluminal if its stress-energy is laid out in advance along the route by agents who got there earlier at subluminal speed.
   - So "a ship-borne drive" is a hidden premise that fails.
   - The question that survives is about pre-laid infrastructure. It helps only after the first trip, and it shortens only round trips as timed on Earth [D-59].
7. **"Required" holds at every speed, so it is not tied to v > c.**
   - For Natário-class metrics the NEC fails at any v > 0 [D-03, D-52]. Under their own assumptions, the WEC fails for superluminal travel [D-50, D-51].
   - No positive-energy superluminal claim has survived critique:
     - Lentz: disputed; the corrected version still violates the WEC, but that rebuttal is a preprint [D-40].
     - Fell–Heisenberg: WEC and NEC not shown for all observers [D-41].
     - Bobrick–Martire's positive-energy solutions are subluminal only [D-07].
   - Premise 1 (a superluminal drive must violate some energy condition) survives. Its falsifier would be an explicit superluminal metric that passes an observer-robust test such as Le 2026's matrix-inequality test [D-69] for the NEC and WEC. None exists in the dossier.
   - Where it fails, it fails only by leaving established physics: Einstein–Cartan torsion or modified gravity [U-11], both [speculative].
8. **"Negative effective mass" in condensed matter is not negative energy density.** A Physical Review Letters paper on "Negative-Mass Hydrodynamics in a Spin-Orbit–coupled Bose-Einstein Condensate" exists [new: Khamehchi et al. 2017, PRL 118, 155301, search-summary, SUMMARY "Crossref title/venue only; abstract not printed"].
   - Our reading, not taken from the paper: in such systems the effective mass is the inverse curvature of the dispersion, m* = ħ²/(d²E/dk²). The atoms have positive rest mass, so T_00 > 0 throughout.
   - Premise 7 (that exotic-matter candidates supply negative energy in the GR sense) fails for this class of candidate.
   - [D-10, D-38] Squeezed vacuum does give ρ < 0 in the GR sense, but only as transient pulses bounded by the QIs [D-46, D-56]. No absolute energy density in J/m³ has been recorded [D-10].
9. **The reductions that are published do not compare like with like (brief premise 3).**
   - Van Den Broeck: quoted at v ≈ 1, for Eulerian observers only, and disputed [D-20–D-25, U-05].
   - Fell–Heisenberg: the length unit is unknown [U-07].
   - White 102: rests on brane-world physics [U-02].
   - Loup: the gain is measured in the ship frame only [U-03].
   - Rodal: the figures are peak measures, not totals [U-10].
   - Bobrick–Martire: the ~1e2 reduction comes from flattening, which pushes the along-track wall to the Planck scale [U-04].
   - Only Bobrick–Martire's ~3× profile gain and the thick-wall floor [D-19] have been stated in the same convention as Alcubierre, and the thick-wall floor is not open to QI-bound sources (finding 1).

## Lens-specific outputs

### A. Loaded terms and whether each definition survives
| Term | Brief's definition | Test | Verdict and repair |
|---|---|---|---|
| "Superluminal effective speed" | Measured in the asymptotically flat exterior: the trip between two points at rest there takes less time than light needs through empty space | (i) Superluminality is gauge- or paradigm-dependent when two different spacetimes are compared [D-43]. (ii) The Alcubierre metric describes an *eternal* bubble; a trip has to include creation and stopping, and Krasnikov argues a traveller cannot hasten arrival in globally hyperbolic spacetimes (finding 6). (iii) The endpoints can be at rest only if the bubble exists along the whole route. | **Strained.** It survives for an eternal, given bubble. For "travel" it must be redefined in terms of events, including creation from flat space, as Olum [D-50] and Krasnikov do. Under that redefinition, a ship-launched bubble is not superluminal. |
| "Negative energy" | ρ_u = T_μν u^μ u^ν < 0 for some observer u; the budget is the Eulerian integral | The integral is not invariant: the ADM mass is 0 for flat-slice drives even though ∫ρ < 0 (finding 5). The QIs bound sampled density along worldlines, not totals [D-54]. | **Survives as a local criterion, fails as a budget.** Replace "amount required" with three things: the minimum over observers u of ρ_u, the NEC contraction, and the QI-sampled density at the wall, together with the stresses [D-06]. |
| "Required" | The WEC or NEC fails for some observer | NEC fails at every v [D-03, D-52]; WEC fails for superluminal travel under Olum's assumptions [D-50] and for the Natário class [D-51]. No positive-energy superluminal claim has survived critique [D-40, D-41, D-07]. | **Survives** within established physics. Fails only by leaving it [U-11]. |
| "Viable in principle" | Consistent with GR and semiclassical QFT, including the proven QIs | The QIs are proven only for free fields in 4D Minkowski [D-54, U-09], so for interacting or plasma sources [U-06] no theorem decides the question. | **Strained:** it is two-valued. Split it into "excluded by a theorem" and "excluded under the free-field QI extrapolation". Most options land in the second group. |
| "Engineering option" | A concrete source with the right T_μν, place, size and duration, or a geometry change; the whole package must work | At v > c, 90–97% of the negative energy lies where no comoving timelike source can sit (finding 2). The ship cannot create or steer the bubble [D-58], and no solution self-accelerates [D-62]. | **Strained.** A ship-carried source is excluded at v > c. The only coherent meaning left is route infrastructure laid down in advance. |
| Reference wall Δ = 1 m | A reference case for comparing options | This wall is 10^63.6 above the free-field QI in density at v = 10c (finding 1). | **Ill-posed for quantum sources.** Keep it only as a "classical exotic matter [speculative]" case. The QFT-consistent reference is Δ ≈ 1.6e-32 m, giving 4.6e63 kg [D-18]. |
| "TRL by 2100" | Demonstrated capability plus extrapolation | No source has ever produced negative energy that gravitates and can be isolated [D-09, D-10]. | TRL 1 at most, for "basic principle observed" (the Casimir force). This scale cannot resolve a gap of more than 30 orders of magnitude, so report orders of magnitude instead. |

### B. Premise ledger
| # | Premise | Support | What would falsify it | If false, the question becomes | Status |
|---|---|---|---|---|---|
| P1 | Superluminal drives must violate an energy condition | Olum [D-50]; Santiago et al. [D-51]; Lobo–Visser [D-52]; Bobrick–Martire's own statement [D-07] | A superluminal metric passing an observer-robust NEC/WEC test [D-69], e.g. a corrected Lentz metric | "Find a positive-energy source (plasma) of ~tens of M_sun" [U-06]; the causal problems (P6, P8) remain | **Survives** (established physics) |
| P2 | The total Eulerian energy is the right budget | Standard practice [D-02] | — | Local density, stresses and QI-sampled density bind instead (findings 1, 5) | **Fails** |
| P3 | Published reductions compare like with like | — | — | Every reduction must be recomputed at R = 100 m, v = 10c, with a stated Δ convention and all observers | **Fails** for most (finding 9) |
| P4 | Lab negative energy can be scaled, concentrated and separated | Casimir ρ < 0 is real in principle [D-08] | A demonstration of net-negative local energy with its source mass off-site | Nothing is left to engineer at lab scale | **Fails**: plate mass exceeds the deficit by ≥ 3e11 at 1 nm (finding 4); quantum interest [D-56]; no concentration source [D-09] |
| P5 | Geometry tricks leave a usable ship | Van Den Broeck keeps a 100 m pocket [D-05] | — | Tides and Planck-scale structure become the binding constraint | **Strained**: Van Den Broeck curvature ~10 L_P [D-25]; thick walls shrink the interior; unchecked tides [D-72] scale as v², which at v = 10c gives ~4 g/m near the centre (prior-note value 0.04 g/m × 100, unchecked arithmetic) |
| P6 | The ship can create, steer and stop the bubble | — | A self-accelerating solution [D-62] | Only a route pre-laid by earlier subluminal agents is possible | **Fails** [D-58, D-62, finding 6] |
| P7 | Exotic-matter candidates are GR-negative energy | — | A measured T_00 < 0 in bulk matter | Only quantum-vacuum sources remain | **Fails** for condensed-matter "negative mass" (finding 8) |
| P8 (new) | The negative-energy source travels with the bubble | Implicit in "drive" | Timelike comoving worldlines where f < 1 − 1/v; there are none | "Who writes the stress-energy pattern along the route, and when?" | **Fails**: 97% of E at v = 10c (tanh) (finding 2) |
| P9 (new) | Supply options and shrink options can be combined | Implicit in the brief's option list | A QI for the actual source field that permits Δ ≫ 100 v L_P | Choose one: a QFT source with a Planck-thin wall and ~1e63 kg, or a thick wall with classical exotic matter [speculative] | **Fails** under free-field QIs (finding 1); open for interacting fields [U-09] |
| P10 (new) | Semiclassical gravity is valid at the needed densities | Brief's admissible physics | — | Quantum gravity decides; nothing is established | **Strained**: the QI wall is 4e-7 of Planck density (finding 3); Van Den Broeck is ~10 L_P [D-25] |
| P11 (new) | A 0.44 yr trip is shorter than the time any instability needs to grow | — | A 4D stable superluminal semiclassical solution | Only brief bursts at v > c [D-45] | **Strained**: the stress-energy grows exponentially within ~1/κ [D-39, D-61] (2D models only) |

### C. Reframes
- **R1: pre-laid route (the best-posed nearby question).** "Can agents who travel at subluminal speed lay a route (warp track or Krasnikov tube) whose QI-obeying sources are switched as the pattern passes, giving faster-than-light round trips later?"
  - This matches findings 2 and 6 and [D-59]. It has a clear partial answer: it helps only round trips timed on Earth; it still needs "unphysically thin layers" [D-59], with thin walls of QI-class energy; and two tubes make a time machine [D-59, D-60].
- **R2: density-gap framing.** "At the QI-consistent wall, how far is the required local negative energy density from the best demonstrated density?"
  - This is well posed and gives a clear number: ~10^99 at v = 1c versus an ideal 1 nm Casimir gap [D-33].
  - The total-energy framing is not well posed (finding 5).
- **R3: subluminal positive-energy warp shells.** "What is the least exotic warp geometry at v < c?"
  - Answer: shells that meet all the energy conditions, of about Jupiter mass (4.49e27 kg at 0.04c) [U-08], with no self-acceleration [D-62].
  - This is well posed and answerable, but it abandons the goal of travelling faster than light.

### D. Hardest questions any answer must survive
1. **Observers.** Which observer field and which slicing does the energy figure use? Does the option pass the NEC and WEC for *all* timelike and null vectors, for example by the matrix-inequality test [D-69], or only for Eulerian observers [D-06]?
2. **Wall thickness against the QI.** Is the wall thickness Δ consistent with the QI for the actual source field? If Δ > 1e2 v L_P (1.6e-32 m at 10c), name the physics that escapes the free-field QI, give its status, and give the resulting density excess (10^63.6 at Δ = 1 m) [finding 1].
3. **Causal placement of the source.** At v = 10c, what timelike worldlines carry the source into the region f < 1 − 1/v, which holds ≥ 90% of E? Who placed it there, and was that event in the causal past of departure (finding 2, [D-58])?
4. **Net local energy.** At the wall location, is the *net* local energy density, including the plates, cavity or compensating pulse, below zero? Is it at the required ~1e42 J/m³ (v = 1c, Δ = 1 m) or ~5e107 J/m³ (QI wall) [D-33, finding 4]?
5. **Like-with-like conversion.** Has the reduction been converted to R = 100 m (ship region), v = 10c and PF Δ, with the measure named, and with "(ours)" marking the conversion (finding 9)?
6. **Creation and stopping.** How is the bubble created from flat space, accelerated to 10c and stopped, given no self-acceleration [D-62], the horizon [D-58] and the growth of the renormalized stress-energy within ~1/κ [D-61]?
7. **Semiclassical validity.** Does any curvature radius or wall thickness fall within ~1e3 Planck lengths (Van Den Broeck ~10 L_P; QI wall ~1e3 L_P at 10c), where semiclassical gravity is not established (finding 3, [D-25])?
8. **Tides on the crew.** Using the tidal tensor, not raw Riemann components, is the tidal acceleration across a 2 m body below ~1 g at v = 10c? The unchecked prior note gives 0.04 g/m at the centre at v = c, scaling as v² [D-72].
9. **Causality.** If bubbles can be launched from two frames, what excludes closed timelike curves without invoking the chronology-protection conjecture [D-60]?

## Calculations
- `runs/2026-09-29-alcubierre-negative-energy/calc/lens-examiner_premises.py` (geometric units for part 1, SI for parts 2–4).
  1. Fraction of Eulerian negative energy at f < 1 − 1/v, where no bubble-comoving timelike source can sit. At v = 10c: tanh (σR = 200) 0.9724; thin-wall tanh 0.972; linear ramp 0.90; Bobrick–Martire optimal profile 0.90. At v = 2c it is 0.50 for every profile; at v = 1.01c it is 0.0003 to 0.01; at v = 100c it is ≥ 0.99.
  2. Free-field QI density excess, (Δ/Δ_max)² with Δ_max = 1e2 v L_P. At v = 10c: 10^63.6 for Δ = 1 m, 10^57.6 for 1 mm, 10^33.6 for 1 fm. At v = 1c: 10^65.6 for Δ = 1 m.
  3. QI wall at 10c: shell volume 2.0e-27 m³; mean |ρ| = 2.3e90 kg/m³, which is 4.4e-7 of the Planck density (5.15e96 kg/m³).
  4. Casimir, ideal plates: |E|/A = 0.433 J/m² (4.8e-18 kg/m²) at 1 nm. Plate-mass to deficit ratio: two graphene layers 3.2e11 at 1 nm, 3.2e17 at 100 nm; two 50 nm gold films 4.0e14 at 1 nm. Plate areal masses are assumed inputs.

## Candidate answers (at least 3; the null and a reframe count)
Not mutually exclusive: EXAMINER-A is the null, B and C are reframes, and D to F are option-type.

- [EXAMINER-A] **Null.** No viable engineering option exists within established physics.
  - The supply routes are only quantum-vacuum sources, bound by free-field QIs to Planck-thin walls: ~4.6e63 kg (2.3e33 M_sun) at 10c [D-18], and a density gap of ~10^99 [D-33].
  - Every classical "exotic matter" route is [speculative] (findings 1, 7, 8).
  - In principle, no theorem excludes interacting-field sources [U-09], so the in-principle verdict is "excluded under extrapolation", not "by theorem". The in-practice verdict is TRL ≤ 1.
  - | status: surviving | why: every premise that would open an option (P4, P6, P8, P9) fails, and P1 survives.
  - | test: a QI or QEI for a realistic interacting source that permits Δ ≫ 100 v L_P, or an observer-robust positive-energy superluminal metric; either would move this to strained.
  - | confidence: high
- [EXAMINER-B] **The premise is wrong: the binding obstacle is causal, not quantity.**
  - At v > c, 90–97% of the required negative energy (v = 10c) lies where nothing comoving with the bubble can exist, and the ship cannot create or steer the bubble. Any source must therefore be written along the route in advance by agents who travelled more slowly than light.
  - The well-posed question is R1, pre-laid infrastructure. That gives at best faster round trips as timed on Earth, after a subluminal first trip, and it still needs QI-thin walls and risks closed timelike curves [D-59, D-60].
  - | status: surviving | why: finding 2 is a direct metric calculation that holds for every profile tested; it agrees with [D-58] and Krasnikov (finding 6).
  - | test: this is the only candidate that predicts a v-threshold. The comoving-source fraction is 0 for v ≤ 1 and 1 − 1/v or more above it. Any sub-luminal demonstration leaves it untouched, and any claimed superluminal source must show its worldlines in f < 1 − 1/v.
  - | confidence: medium-high
- [EXAMINER-C] **Reframe: energy totals are the wrong metric, and the brief's Δ = 1 m reference is internally inconsistent for QFT sources.**
  - The Eulerian total is slicing-dependent (the ADM mass is 0), so the binding measure is local QI-sampled density.
  - With that measure, the "38 M_sun at Δ = 1 m" and the "0.56 M_sun thick-wall floor" apply only to [speculative] classical exotic matter. The only QFT-consistent Alcubierre number is ~1e63 kg. Thick-wall reductions (White 101) and QI-bound supplies are mutually exclusive.
  - | status: surviving | why: the PF quote and the calculation give (Δ/Δ_max)² = 10^63.6.
  - | test: a proven QEI for the proposed source field, such as Lentz's plasma [U-06] or the electromagnetic field in dielectrics. If it permits metre-scale walls at ~1e44 J/m³ (v = 10c), this reframe collapses back into the brief's total-energy framing.
  - | confidence: medium (the QI's reach beyond free fields is open [U-09])
- [EXAMINER-D] **Option: a Van Den Broeck pocket plus a QI-obeying quantum source**, about solar mass at v ≈ 1 [D-20–D-24].
  - | status: strained | why:
    - curvature ~10 L_P [D-25];
    - Bobrick–Martire's equivalence dispute [U-05];
    - QI checked for Eulerian observers only [D-24];
    - not rescaled to 10c;
    - the causal-placement problem (P8) applies unchanged to its outer wall;
    - its density gap versus Casimir is 10^102 [D-34].
  - | test: recompute region-II energy with the B(0)²v² term Bobrick–Martire claim is missing, at v = 10c, with all observers. A rise by a factor of about α² would eliminate it.
  - | confidence: medium
- [EXAMINER-E] **Option: positive-energy superluminal solitons remove the need for negative energy** (Lentz, Fell–Heisenberg).
  - | status: eliminated (as "no negative energy needed") | why:
    - P1 survives [D-50, D-51];
    - the corrected Lentz metric still violates the WEC (preprint) [D-40];
    - Fell–Heisenberg is Eulerian-only [D-41];
    - even if positive, Lentz needs ~tens of M_sun at 10c [U-06], with its source beyond the horizon (finding 2).
  - | test: an observer-robust NEC/WEC test [D-69] on the Lentz and Fell–Heisenberg metrics. Passing it would revive this as a positive-energy but still causally uncontrollable option.
  - | confidence: medium
- [EXAMINER-F] **Reframe R3: subluminal positive-energy warp shells are the viable nearby target.** These are Jupiter-mass shells at v < c (4.49e27 kg at 0.04c [U-08]) that meet all the energy conditions but cannot self-accelerate [D-62].
  - | status: surviving as a reframe, but it does not answer the superluminal question | why: it is well posed and consistent with established physics.
  - | test: a solved acceleration phase for a Fuchs-type shell using positive energy only. Without one it is not a drive at all.
  - | confidence: medium

## What would change my mind
- A proven quantum energy inequality for a realistic interacting source, such as a plasma, dielectric electromagnetism or a non-minimally coupled scalar, that allows metre-scale walls at the required density. That would revive the thick-wall and Δ = 1 m options, and weaken EXAMINER-A and C.
- An explicit superluminal metric that passes the NEC and WEC for all observers under an observer-robust test [D-69].
- A self-consistent solution in which the source for the region f < 1 − 1/v is supplied by worldlines that start inside the ship's causal past, which I believe is impossible by construction. That would defeat EXAMINER-B.
- A laboratory measurement of net-negative local energy density with its positive-mass source removed.

## Assumptions I relied on
- **Metric.** The Alcubierre/Natário-class metric with the shift along x. The comoving criterion f > 1 − 1/v is exact for that metric; for lapse-modified drives (Loup [U-03], Lentz) the threshold moves but does not vanish. This is not computed.
- **Energy weighting.** The Eulerian energy weight is f′(r)² with the same angular factor at every r. This is exact for Alcubierre [D-02]. For Natário the density involves f″ as well [D-04], so the fractions could differ by O(10%).
- **Pfenning–Ford's scaling.** I use their scaling Δ_max = 1e2 v L_P (α = 1/10). The factor-of-2 convention dispute [D-47] does not affect the orders of magnitude.
- **Plate masses.** The Casimir plate areal masses are assumed, not sourced. The ideal-conductor formula overstates real-metal Casimir energy at gaps below the plasma wavelength, which is qualitative general knowledge not opened here, so the mass ratios are lower bounds.
- **ADM-mass argument.** The ADM-mass-zero statement is my own inference from flat spatial slices.
- **Tides at 10c.** The ~4 g/m figure at 10c is unchecked prior-note arithmetic [D-72].
