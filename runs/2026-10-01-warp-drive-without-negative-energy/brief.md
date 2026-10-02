# Brief: Can any warp drive move a payload without negative energy?
slug: 2026-10-01-warp-drive-without-negative-energy | depth: deep | type: feasibility | date: 2026-10-01

## Question as asked
"Can any warp-drive spacetime move a payload faster than light, or at all, without negative energy? Weigh the Alcubierre and Natário metrics against the positive-energy and subluminal solutions proposed since 2020 (Lentz, Fell–Heisenberg, Bobrick–Martire, and the 2024 constant-velocity "physical warp drive"), checking each one's energy conditions by calculation. For whatever survives, what would it take to build in mass, energy and technology, and what is the nearest experiment that could test any part of it?"

## Question made precise

**The metrics in scope.**
- Alcubierre 1994 (CQG 11 L73; arXiv:gr-qc/0009013).
- Natário 2002, the zero-expansion drive (CQG 19 1157; arXiv:gr-qc/0110086).
- Lentz 2021, "Breaking the warp barrier: hyper-fast solitons in Einstein–Maxwell-plasma theory" (CQG 38 075015; arXiv:2006.07125), with his later proceedings and replies.
- Fell & Heisenberg 2021, "Positive energy warp drive from hidden geometric structures" (CQG 38 155020; arXiv:2104.06488).
- Bobrick & Martire 2021, "Introducing physical warp drives" (CQG 38 105009; arXiv:2102.06824): their general shell framework, and any explicit positive-energy example they give.
- Fuchs, Helmerich, Bobrick, Sellers, Melcher & Martire 2024, "Constant velocity physical warp drive solution" (CQG 41 095013; arXiv:2405.02709). This is the question's "2024 constant-velocity physical warp drive". Its numerical method is in Helmerich et al. 2024, "Analyzing warp drive spacetimes with Warp Factory" (CQG 41 095009; arXiv:2404.03095).
- Any later construction (2024–2026) that research finds claiming to need no negative energy, or claiming to accelerate.
- Van Den Broeck's and White's variants enter only as comparators. Wormholes and Krasnikov tubes are out of scope, except as a reframe.

**Definitions.**
- **Warp-drive spacetime.** A solution of Einstein's equations in 3+1 form, ds² = −N²c²dt² + h_ij (dx^i + β^i dt)(dx^j + β^j dt). Papers differ in the sign of β; state which convention you use. A payload region moves relative to the exterior because of a localized region where the shift β, the lapse N or the spatial metric h_ij differs from the exterior's, not because the payload is pushed by its own reaction mass. The exterior is asymptotically flat; it may be Schwarzschild-like, with nonzero ADM mass.
- **Payload region.** A region of radius at least 10 m that encloses a payload on a timelike worldline, with tidal accelerations below 1 g over 10 m. That is a crewed standard; an uncrewed relaxation is allowed if labelled. Compute tides with the tidal tensor, not raw Riemann components.
- **"Move a payload."** Grade each construction at three levels:
  - **Coast:** a stationary solution in which the payload region moves at constant speed v relative to the exterior's asymptotic rest frame.
  - **Start and stop:** a solution, or at least a worked construction, that takes the payload from rest relative to the exterior to v and back, with the energy conditions holding throughout. External propulsion (reaction mass, radiation) is allowed but must be counted in mass and energy.
  - **Self-propelled:** the same with no momentum supplied from outside, and none emitted beyond what the solution itself radiates, such as gravitational waves. Say whether conservation of ADM momentum permits it.
  A construction that only coasts is a vehicle shape, not a drive. Say so where it applies.
- **"Faster than light."** Measured in the asymptotically flat exterior: the payload travels between two points at rest there and arrives before a light signal sent between them through the undisturbed exterior would, so v > c in that frame. Keep two things apart:
  - a genuine time advance of that kind: the sense of Olum 1998, of Visser, Bassett & Liberati 2000, and of the Gao–Wald 2000 time-delay theorem;
  - a local shift exceeding the lapse (|β| > N somewhere, which makes an ergoregion or horizon), or a coordinate speed above c. Neither one by itself means earlier arrival.
  Report which sense each paper's "superluminal" claim meets.
- **"Without negative energy."** The stress-energy the metric requires, T_μν = (c⁴/8πG) G_μν, satisfies the weak energy condition (WEC) everywhere, for every observer: T_μν u^μ u^ν ≥ 0 for all timelike u. This includes the null energy condition (NEC): T_μν k^μ k^ν ≥ 0 for all null k. We compute T_μν from the metric ourselves rather than taking it from the paper. A positive energy density seen only by Eulerian (normal) observers does not qualify.
  - **Also report the strong and dominant energy conditions (SEC, DEC).** A metric that meets the WEC but fails the DEC needs no negative energy, but needs matter whose energy flows faster than light. Call that failure "unphysical source", not "negative energy".
  - **Report averaged conditions and quantum inequalities** wherever violations remain: the ANEC on complete null geodesics, and the free-field quantum inequalities. They decide whether semiclassical QFT could supply the violation.
  - **Classify each point by Hawking–Ellis type.** For type I, test exactly with the rest-frame density and principal pressures (ρ + p_i ≥ 0, ρ ≥ 0, and so on). Otherwise sample observers and null directions, and say so.
  - **A source is also required.** Name a known matter model that can produce the T_μν consistently with its own equations of motion: a perfect or anisotropic fluid, an elastic solid, or an electromagnetic field with plasma. Report whether each paper supplies one.
- **Energy and mass budgets.** Report:
  - the ADM mass;
  - the integral of the Eulerian energy density over a t = const slice, split into negative and positive parts (E₋, E₊);
  - the rest mass of the matter.
  Convert with M = E/c², and give kg, Jupiter masses (1.898e27 kg) and solar masses (1.989e30 kg). Wall-thickness conventions differ between papers, so every number names its convention.

**Reference cases, so numbers compare like with like.** Give each paper's own parameters first, then:
- **Superluminal:** payload radius R = 100 m, v = 10c and wall Δ = 1 m, the same case as the earlier warp run. Where negative energy remains, also give Δ at the free-field quantum-inequality limit.
- **Subluminal:** the 2024 shell at its published parameters. Where a scaling law exists, also scale it to payload radii of 10 m and 100 m, marking the conversion as ours.
- **Trip:** a 1e5 kg payload to Alpha Centauri (4.37 ly), compared with a relativistic rocket (`rocket_tools.py`).

**Admissible physics.**
- **Established:** classical GR, QFT on curved spacetime, and semiclassical gravity (G_μν = 8πG⟨T_μν⟩/c⁴), with the proven quantum inequalities and the ANEC where their assumptions hold.
- **Conjectures** may be used when labelled: quantum interest, chronology protection, the self-consistent achronal ANEC.
- **Speculative extensions** are allowed only when labelled [speculative]: modified gravity, extra dimensions and brane worlds, Einstein–Cartan torsion, negative-mass matter. They never count toward "possible in principle under established physics".

**Horizon for "viable".** Two verdicts for each construction:
- **In principle:** consistent with established physics, stating which assumptions that needs.
- **In practice:** buildable by 2100, from demonstrated capability plus credible extrapolation. Give a technology readiness level (TRL) and the gap in orders of magnitude.

**"Nearest experiment."** A laboratory test, space mission or astronomical observation, not a calculation, whose outcome could change the credence of a surviving answer because it tests a premise that answer rests on.
- Rank candidate experiments by the gap, in orders of magnitude, between the effect the premise predicts and the experiment's demonstrated sensitivity.
- Name the decisive calculation separately, if it would settle more than any experiment.

## Hidden premises to test
1. **That "positive energy" in the 2021 papers means the energy conditions hold.**
   - Lentz, Fell–Heisenberg and Bobrick–Martire mostly evaluate the Eulerian energy density.
   - Santiago, Schuster & Visser (2022) argue that this misses other observers.
   - Test each metric for all observers, including distributional (sheet) contributions wherever a profile has a kink. Lentz's own reply to his critics concerns non-smoothness at his source boundaries.
2. **That each "superluminal" claim is superluminal in the travel-time sense** defined above, and not an ergoregion or a coordinate speed.
3. **That the no-go theorems apply, and which assumption a positive-energy faster-than-light metric would have to break.**
   - The theorems: Olum 1998; Visser, Bassett & Liberati 2000; Gao & Wald 2000; Santiago, Schuster & Visser 2022, which covers unit lapse and flat slices; and the positive-mass theorem (with the DEC, a non-flat asymptotically flat spacetime has positive ADM mass).
   - Check each theorem's assumptions against each metric: asymptotic flatness, the generic condition, the slicing, and what "superluminal" means.
4. **That the 2024 shell is a drive, not a massive shell coasting at constant velocity in clever coordinates.**
   - Its authors say the shift "cannot be reduced to a coordinate transformation".
   - Find a gauge-invariant observable that separates it from the same matter shell simply boosted to v.
   - Say whether that difference does anything for a payload.
5. **That a positive-energy warp configuration can be started and stopped.**
   - The 2024 paper solves only constant velocity.
   - Test whether acceleration keeps the energy conditions, and what momentum must be supplied or ejected. ADM momentum is conserved for an isolated system.
6. **That meeting the energy conditions makes a construction physical.** It also needs:
   - a matter model obeying its own equations of motion;
   - the DEC, so that sound travels no faster than light;
   - stability;
   - densities and stresses that some matter can bear.
   For Lentz, check whether Einstein–Maxwell-plasma theory actually sources the soliton.
7. **That positive matter can make the "warp effect" large.** At a given mass and size, these may cap how large an interior shift or speed difference positive matter can produce:
   - compactness bounds (Buchdahl-type bounds for spheres and shells);
   - horizon formation;
   - the DEC.
   Find the cap.
8. **That numerical checks establish "everywhere, for all observers".**
   - Grid sampling, finite differences, observer sampling and smoothing can miss violations or create them, for example at shell boundaries.
   - Use exact type-I tests where possible, check convergence, and say what was sampled.
9. **That Natário's zero-expansion drive needs negative energy as Alcubierre's does.** Check it, rather than assume it either way.
10. **That "move a payload at all" is a meaningful bar.**
    - An ordinary rocket moves a payload with positive energy.
    - The real question for any subluminal survivor is whether the warp geometry gives something a rocket can't: no acceleration felt by the passengers, a shorter proper time, or a lower energy cost.

## What counts as an answer
1. **An energy-condition table, one row per metric:** the six named, plus any later construction research finds. Columns:
   - speed class, and in which sense superluminal;
   - the sign of the Eulerian energy density;
   - NEC, WEC, SEC and DEC for all observers, computed by us with code in `calc/`, at the paper's parameters and at the reference case;
   - Hawking–Ellis type where it matters;
   - the paper's own claim;
   - whether the claim survived published critique;
   - ADM mass, E₋ and E₊;
   - whether acceleration is solved;
   - the matter model.
2. **A verdict on each headline question:**
   - **(A) Faster than light without negative energy:** possible in principle under established physics, or not? Name the theorem that decides it, its assumptions, and the loophole that would have to hold.
   - **(B) Any motion of a payload without negative energy:** which constructions qualify, at which level (coast, start and stop, self-propelled), and whether any of them beats a rocket at anything.
3. **For whatever survives, what building it takes:**
   - mass;
   - energy, both the rest-mass energy and the energy to reach v and stop;
   - peak density and stresses, against the strongest materials and nuclear matter;
   - compactness, against horizon formation;
   - the acceleration method;
   - TRL, and the gap in orders of magnitude against demonstrated capability;
   - the same trip by rocket, for comparison.
4. **The nearest experiment for each survivor:**
   - the premise it tests;
   - the predicted effect against the demonstrated sensitivity, with the gap in orders of magnitude;
   - who could do it, and when;
   - separately, the decisive calculation.
5. **The null and a reframe, ranked alongside the options.** The null is that no warp spacetime moves a payload faster than light without negative energy, and that the positive-energy subluminal ones do nothing an ordinary massive vehicle cannot.

## Research facets
- **theory:** the metrics in computable form, and the theorems with their assumptions.
  - **Metrics:** Alcubierre; Natário; Lentz 2021 and his later proceedings; Fell–Heisenberg; Bobrick–Martire's classification and shell construction; Fuchs et al. 2024, with the Warp Factory method of Helmerich et al. 2024. For each, record:
    - the lapse, shift, spatial metric, profile functions and parameter values;
    - the claimed speed class;
    - which energy conditions the authors checked, for which observers.
  - **Theorems:** Olum 1998; Visser, Bassett & Liberati 2000; Gao & Wald 2000; Santiago, Schuster & Visser 2022; Schuster, Santiago & Visser on ADM mass in warp spacetimes; the positive-mass theorem; Buchdahl-type compactness bounds for spheres and shells; results on whether a warp spacetime can change its own ADM momentum.
  - **Leaves to others:** energies and masses to quantitative, published critiques to critiques, and constructions after mid-2024 to frontier.
- **quantitative:** the required quantities, each with its convention.
  - **Per paper:** published energies and masses (ADM mass, Eulerian total, negative and positive parts); densities and pressures; wall thicknesses and speeds; scaling laws in R, Δ and v; Bobrick–Martire's reduction factors.
  - **The 2024 shell:** R₁, R₂, M, peak density and pressure, compactness and speed.
  - **Lentz:** his energy scaling.
  - **Fell–Heisenberg:** the example's parameters and length unit.
  - **Reference constants:** M_J, M_sun, the Planck length, world primary energy per year.
  - **Leaves to others:** demonstrated capability and experimental sensitivity to engineering.
- **critiques:** published critiques of each named metric and each positive-energy claim, and the authors' replies, whatever their date. This facet owns the question "did it survive critique?". Cover:
  - Santiago, Schuster & Visser and related papers by the Visser group;
  - Celmaster & Rubin 2025 on Lentz;
  - Le 2026 on the 2024 shell, comparing its versions;
  - Warp Factory's re-analysis of the earlier metrics;
  - Rodal's analyses;
  - Lentz's replies;
  - any critique arguing the 2024 shell is a coordinate artefact or just a heavy shell;
  - horizons and control (Everett & Roman 1997), semiclassical instability (Finazzi, Liberati & Barceló 2009), and closed timelike curves.
- **engineering:** what building a survivor would take, and the experiments.
  - **Demonstrated capability:** the strongest materials' tensile and compressive strengths; the highest densities and pressures sustained or produced; the largest masses assembled or moved in space; world energy production; propulsion records (highest Δv, fastest spacecraft); antimatter production.
  - **Experiments that could test a load-bearing premise:**
    - frame dragging and gravitomagnetism: Gravity Probe B, LAGEOS and LARES 2, and laboratory proposals;
    - whether Casimir or vacuum energy gravitates: the Archimedes experiment;
    - negative energy density in the laboratory: squeezed light, the dynamical Casimir effect, quantum-energy-teleportation demonstrations;
    - analogue-gravity horizon or warp experiments;
    - past "warp" lab claims and their null results: the White–Juday interferometer and Eagleworks, and tests of EmDrive and Mach-effect thrusters;
    - high-frequency gravitational-wave detectors.
  - **For each experiment:** method, sensitivity, who runs it, status and timeline.
  - **Leaves to others:** the metrics' required numbers to quantitative.
- **frontier:** 2023–2026 work, newest first, each item labelled preprint or preliminary where it applies:
  - new constructions, such as accelerating or superluminal positive-energy proposals made since the 2024 shell, and Rodal's irrotational drive;
  - numerical-relativity simulations of warp spacetimes, such as Clough, Dietrich & Khan 2024 on gravitational waves from a collapsing bubble;
  - Warp Factory follow-ups;
  - conference talks;
  - responses to critiques that are new constructions.
  It leaves critiques of the named 2021–2024 metrics to critiques.

## Worked calculations
Lenses run at the same time and can't read each other's work. Each item below has one owner, and the owner's result is the reference the slate builder, the refuters and the judge use. Another lens that needs the number computes its own and says so.
- **constraints: the energy-condition table** (answer item 1).
  - For every metric, compute T_μν from the metric through Einstein's equations.
  - Test the NEC, WEC, SEC and DEC for all observers, with the Hawking–Ellis type, and show the Eulerian density alongside.
  - Do this at each paper's parameters and at the reference case, with grid-convergence checks.
- **examiner: the travel-time test** (premise 2). For each metric claimed superluminal:
  - does a payload or signal through it arrive before light sent through the undisturbed exterior?
  - does the shift exceed the lapse anywhere?
- **idealizer: an analytic thin-shell model of a positive-energy warp shell** (premises 4 and 7). For a shell of mass M and radius R carrying an interior shift, compute:
  - from the Israel junction conditions, the surface energy, momentum and stresses the shift requires, and their energy conditions;
  - the largest shift positive matter allows at a given compactness;
  - a gauge-invariant difference from a plain boosted shell.
- **mechanist: the acceleration phase** (premise 5).
  - Find the extra stress-energy a time-dependent shift requires, and whether the energy conditions survive it.
  - Find the momentum and energy that must be supplied or ejected to reach v and stop.
- **engineer: build requirements and experiment gaps** (answer items 3 and 4).
  - The build requirements for whatever survives, including the rocket comparison with `rocket_tools.py`.
  - The predicted effect against the demonstrated sensitivity for each candidate experiment.
- **decomposer: the theorem-applicability ledger** (premise 3): each theorem's assumptions checked against each metric.

## Known constraints, prior attempts, and user-supplied data
**Toolkit.**
- **`gr_tensors.py`.**
  - Alcubierre and Van Den Broeck are built in. Natário, and smoothed versions of Lentz and Fell–Heisenberg, go in through `Spacetime.from_adm`.
  - `energy_conditions` and `scan_energy_conditions` give the NEC, WEC, SEC and DEC for all observers, with the Hawking–Ellis type. Type I is tested exactly; other types sample boosts up to 0.99c and null directions.
  - It is symbolic, so a metric known only numerically, such as the 2024 shell's TOV solution, can't go in directly.
- **Proposed calculators.** If approved at framing, they are built in `runs/2026-10-01-warp-drive-without-negative-energy/tools/` during research:
  - `numeric_stress_energy`: energy conditions for numerical metrics;
  - `warp_shell`: the 2024 shell itself.
  If they are not built, each lens builds what it needs in `calc/`.
- **Other tools.** `rocket_tools.py` covers the rocket comparison, and `unit_tools.py` has `Msun` and `Mjup`.

**Leads, unverified.** These come from the earlier warp runs, whose sources were never checked, and from framing. None is evidence until a researcher finds the source and quotes it.
- **Critiques and replies:**
  - Celmaster & Rubin 2025 (preprint, on Lentz);
  - Le 2026 (preprint, arXiv:2605.25417, on the 2024 shell's boundary; its versions reportedly differ);
  - Lentz's Marcel Grossmann reply;
  - Rodal 2024 (IJTP 63, 168), Rodal 2025 (arXiv:2507.09724) and Rodal 2026 (an irrotational drive).
- **Theorems:**
  - Olum 1998 (PRL 81, 3567);
  - Visser, Bassett & Liberati 2000;
  - Gao & Wald 2000 (CQG 17, 4999);
  - Santiago, Schuster & Visser 2022 (PRD 105, 064038; arXiv:2105.03079);
  - Schuster, Santiago & Visser on ADM mass in warp-drive spacetimes;
  - Lobo & Visser 2004 (arXiv:gr-qc/0406083).
- **Horizons, stability and causality:**
  - Everett & Roman 1997 (arXiv:gr-qc/9702049);
  - Finazzi, Liberati & Barceló 2009;
  - Everett 1996;
  - Shoshany & Snodgrass 2023.
- **Simulations:** Clough, Dietrich & Khan 2024, gravitational waveforms from a collapsing warp bubble.
- **Experiments to check:**
  - the Archimedes experiment (weighing vacuum energy);
  - LARES 2 and Gravity Probe B (frame dragging);
  - squeezed-light negative energy (Vahlbruch et al. 2016, 15 dB squeezing);
  - quantum-energy-teleportation demonstrations (2023);
  - the dynamical Casimir effect (Wilson et al. 2011);
  - the White–Juday warp-field interferometer;
  - the Dresden SpaceDrive tests of EmDrive and Mach-effect thrusters.
- **Earlier run's notes on the 2024 shell, unverified:** R₁ = 10 m, R₂ = 20 m, M = 4.49e27 kg (2.365 M_J), v = 0.04c. Its own §5.3 reportedly discusses acceleration.

**Access.** At framing, the arXiv API timed out once while INSPIRE answered. If arXiv is slow, try INSPIRE for the abstract, then `find_fulltext.py`.

## Prior runs
- 2026-09-29-alcubierre-negative-energy (2026-09-29): leads. A complete quick run on negative-energy supply for superluminal drives. It overlaps on the positive-energy claims and the theorems, but its sources were never checked. This brief reuses and extends its definitions.
- 2026-09-29-warp-bubble-shapes (2026-09-29): leads. A partial single-researcher run on energy-reducing shapes, never source-checked. Its notes flag values read off a plot by eye, and a claim that rests on a search summary.
- 2026-09-29-problem-of-time-quantum-gravity (2026-09-29): ignore. Unrelated.
- 2026-09-30-neutron-lifetime-beam-bottle (2026-09-30): ignore. Unrelated.
