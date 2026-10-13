# Brief: Do gravitational waves decay into photon pairs in vacuum?
slug: 2026-10-13-gravitational-wave-decay-photon-pairs | depth: deep | type: mechanism | date: 2026-10-13

## Question as asked
"Do gravitational waves decay into photon pairs in vacuum, as Blas & Oller claim in 'Gravitational waves decay in vacuum' (arXiv:2607.24930)? Test their central result, the coherent-state graviton-fusion rate for g g → γγ, dP/dt = 3G²N²ω_s³σ_ω²/(25π) (their eq. 8): is it computed correctly, and is it the physically right quantity for a gravitational wave emitted by a real source such as a compact-binary inspiral or merger? Then test the consequences they draw from it: the photon luminosity of binaries (their Fig. 2), the depletion of a stochastic GW background (eq. 14), the constraints from CMB spectral distortions, extragalactic backgrounds and light-nuclei photofission, and the analogous decay into ultralight dark matter (eqs. 16–18)."

## Question made precise

Abbreviation: B&O = Blas & Oller, arXiv:2607.24930 (cite the version read, v1 or v2, and the equation and page). Units: natural (ħ = c = 1, Heaviside–Lorentz) for amplitudes and rates; SI for astrophysical numbers. Always state which.

Five sub-questions:
- **Q1 Computation.** Within B&O's own model (their coherent state, eq. 5–7, the tree-level amplitudes of eq. 6, the S6 integral and the 2πδ(0) → T step), is eq. 8 algebraically right? Check separately:
  - the tree-level g g → γγ helicity amplitudes (eq. 6), magnitudes and phases, and g g → φφ (S10);
  - how eq. 7 combines them into an "unpolarized" coherent amplitude;
  - the phase-space integral to the coefficient 3/(25π), and 7/(450π) for scalars;
  - eqs. 9–10 (photon number, reaction time τ) and the ħ counting (eqs. 11–12).
- **Q2 Right quantity.** Is eq. 8 the physically right quantity for a GW emitted by a real source? In particular:
  - Does B&O's state describe an outgoing wave (retarded field of a source) or something else? Where in space and time is the probability generated?
  - Is turning a total probability into a rate by 2πδ(0) → T legitimate here; does it give a sustained rate, a peak rate, or neither?
  - Does a freely propagating wave in vacuum keep producing pairs (a decay with lifetime and depletion), or only near its source while the source radiates?
  - Does the answer depend on polarisation pattern and packet profile, and by how much?
  - Is the "N² coherent enhancement" a quantum effect or classical field nonlinearity (the classical Einstein–Maxwell field equations at second order)?
- **Q3 Kinematics in vacuum.** Independently of B&O: are there general no-go arguments (collinear kinematics of massless plane waves, the known stability of plane gravitational waves, Gibbons 1975 on plane waves not producing particles, Deser's results) that forbid decay of a single plane wave, and what exactly does a wave packet (non-collinear momenta) evade? Distinguish 1 → 2 decay (forbidden for massless on-shell gravitons) from 2 → 2 fusion within one coherent state.
- **Q4 Consequences.** Re-derive or test, each with its own verdict:
  - photon luminosity of compact binaries (Fig. 2) and the footnote-4 flux at a sphere of radius τ;
  - the depletion time τ_h and any depletion of a GW signal over its path;
  - eq. 14 (8πG²ρ²_GW/15 per volume) for a stochastic background, the ~1e-110 m⁻³ s⁻¹ emissivity, and eq. 15/S9;
  - the CMB-stimulated factor (1 + 2f_γ) and the constraints from CMB spectral distortions (μ, y), extragalactic background light, and light-nuclei photofission (BBN); the cosmological integration of eq. 19/S12;
  - the ULDM channel: S10/S11, 7/(450π), τ_φ = (54/7)τ, eqs. 16–17 (Bose-enhanced, resonant coefficient 1/16), and eq. 18 (W_φ ~ 1e14 W).
- **Q5 Observable.** Is there any regime, source or observation where GW → γγ (or → φφ) could ever be detected or constrain anything, once the right quantity is used?

### Definitions
- **"Decay in vacuum":** a freely propagating GW, far from its source (r ≫ λ and outside any matter or plasma), loses energy to photon pairs at a rate that persists as it propagates, so that its energy decreases along the path. Contrast with **near-source production**: pairs made where the source's field is strong or non-radiative (r ≲ λ/2π) while it radiates, which is a property of the source, not of the wave. Report each separately.
- **Coherent state:** a displaced Fock vacuum S|0⟩ of the graviton field whose expectation value is the classical field. Say whether it is used as an in-state, an out-state, or the Heisenberg state of a retarded source; these carry different classical fields (incoming, outgoing, or time-symmetric/Pauli–Jordan).
- **Rate vs total:** "rate" = pairs per unit time; "total" = pairs over the whole history. "Pairs" vs "photons": photons = 2 × pairs. B&O's eq. 8 is a pair rate.
- **In-out vs in-in:** the S-matrix probability for a pair final state vs the expectation value of the out number operator. State which, and whether they agree at the order used.
- **Physical helicity vs spin projection on a common axis:** state which labels each amplitude uses.
- **"Computed correctly":** algebra and integrals reproduce within the stated model. **"Physically right":** the model's initial state, field, and limits describe a wave from a real source.
- **Real source:** the reference sources are (a) a GW150914-like binary black hole merger (~65 M☉ total, peak luminosity ~3.6e49 W, f ~ 150–250 Hz); (b) a long-lived inspiral (a double neutron star, or a galactic white-dwarf binary in the LISA band); (c) the stochastic background at the ρ_GW allowed by ΔN_eff and by pulsar-timing amplitudes. Use B&O's Fig. 2 inputs where they are stated.

### Admissible physics
- **Established:** GR as an effective field theory of gravitons coupled to Maxwell and to a free scalar, at tree level (O(G²) in rates); classical GR and Einstein–Maxwell at second order; QFT in flat and FRW backgrounds; standard cosmology (ΛCDM, CMB spectral-distortion theory, BBN photodisintegration).
- **Allowed if labelled:** ultralight dark matter models (axion-like or scalar, m ~ 1e-22 to 1e-10 eV); loop corrections; plasma effects on photon production (the photon is not massless in the intergalactic or early-universe plasma; say when this matters).
- **Not admissible as established:** modified gravity, extra dimensions, massive gravitons.

### Horizon
In principle (is the process real at all, and is eq. 8 the right quantity), and in practice (is any consequence detectable or constraining with existing or planned observations, within about 20 years).

## Hidden premises to test
1. That the coherent state B&O use, S_source|0⟩ taken as an *in*-state, carries the outgoing field a real source emits, rather than an incoming-and-re-expanding (time-symmetric) one.
2. That eq. 6's amplitudes can be added as real positive numbers in eq. 7 (that a phase convention exists making them all real), and that the "unpolarized" coherent state is physically realisable.
3. That 2πδ(0) → T, with T ~ 1/σ_ω, turns a finite total into a sustained rate valid along the propagation path.
4. That the rate depends only on N, ω_s and σ_ω, not on the packet's profile shape or polarisation pattern.
5. That a wave far from its source keeps fusing: that the non-collinearity needed for g g → γγ survives at r ≫ λ, where a spherical wave becomes locally plane.
6. That splitting a chirp into fractional-bandwidth bins gives a lower bound ("as any residual coherence between bins is neglected").
7. That each GW event radiates W_γ for its whole propagation time to redshift z (eq. 19/S12).
8. That CMB stimulation enters as (1 + 2f_γ(ω_s)) "in the average sense" and that photons with ω ~ 1e-13 eV propagate as vacuum photons in the cosmic plasma (plasma frequency ~1e-14 eV today, far higher earlier).
9. That ULDM occupation numbers and a resonance with coefficient 1/16 apply over the GW signal's duration (eqs. 16–18), given the dark matter velocity spread and the time a band needs to fill.
10. That the N² enhancement signals quantum "decay" rather than classical nonlinearity whose ħ-free content could be computed classically.

## What counts as an answer
- A verdict for each of Q1–Q5, and for each numbered B&O claim tested: **confirmed** (right arithmetic, right quantity), **right arithmetic, wrong quantity**, **refuted** (wrong), or **undetermined**, each with the script that prints its number.
- If eq. 8 is the wrong quantity: what the right quantity is (a total near the source, a rate falling with r, zero), its formula or scaling, and its size for the reference sources against B&O's numbers.
- A ranked set of answers to the headline question (e.g. "GWs decay in vacuum as claimed", "they produce pairs only near the source, and B&O's numbers are of the right order for that", "B&O's numbers are too large by X", "the effect is zero for a freely propagating wave"), with credences.
- For each consequence (Fig. 2, eq. 14, CMB, EBL, photofission, ULDM): does it stand, fall, or change size, and does any constraint B&O derive survive.
- The decisive calculations, so a reader can re-run them.

## Research facets
- **theory:** the formal underpinnings: graviton-photon scattering amplitudes (KLT/double-copy, Skobelev, Bjerrum-Bohr, Holstein, Boccaletti), photon/scalar production by classical GWs and plane-wave no-go results (Gibbons 1975, Deser, Garriga–Verdaguer), coherent states and classical limits (KMOC, Cristofoli et al.), in-in vs in-out, the 2πδ(0) → T prescription and wave-packet formalism. Leaves numbers to quantitative and objections to critiques.
- **quantitative:** the numbers B&O use and the inputs a re-computation needs: GW150914 and other merger parameters (peak luminosity, frequency, duration), compact-binary populations, ρ_GW bounds (ΔN_eff, PTA amplitude, LVK upper limits), CMB μ/y bounds (COBE/FIRAS and forecasts), EBL and radio background data, BBN photodisintegration thresholds and limits, ULDM density and velocity dispersion, plasma frequencies today and at early times. Leaves the B&O paper's own derivation to theory and frontier.
- **critiques:** published objections, comments and replies to B&O, and to earlier claims of GW → photon conversion or graviton-to-photon decay in vacuum (Gertsenshtein effect needs a background field; it is not vacuum decay); arguments that coherent-state "decay" is classical nonlinearity or vanishes for outgoing waves. Owns any rebuttal or erratum.
- **engineering:** the observational side: which instruments could see the claimed photons (radio arrays at the GW frequency are impossible below the ionospheric/plasma cutoff; say so with numbers), CMB spectral-distortion missions (PIXIE, etc.), EBL and radio-background measurements (ARCADE-2, etc.), and what each could actually constrain. Leaves cosmological theory to theory.
- **frontier:** B&O itself (both versions, SM sections S1–S12), the 2025–2026 literature citing or citing back to it (INSPIRE citations), related recent work on graviton coherent states, gravitational-wave "memory" of particle production, and dark-matter production by GWs. Newest first.

## Worked calculations
- **Reproduce eq. 8 within B&O's model** (coefficient 3/(25π) and scalar 7/(450π)): owner **idealizer**.
- **Helicity amplitudes, phases and the physical coherent-state coefficient** for realistic polarisation patterns (linear quadrupole, circular binary, pure circular): owner **mechanist**.
- **Space-time structure of the coherent state** (which field it carries; where and when the probability is generated; the yield beyond radius r for an outgoing wave): owner **examiner**.
- **The 2πδ(0) → T step and the binning claim** (peak vs average rate, profile dependence, chirp bins): owner **dialectician** (it is the hinge between B&O's "rate" and a finite total).
- **Consequences: Fig. 2 luminosity, eq. 14, eq. 19/S12 integration, CMB μ/y, EBL, photofission, plasma cutoff**: owner **constraints**.
- **ULDM channel, eqs. 16–18** and whether any observation is in reach: owner **empiricist**.

The toolkit's `qft_second_order.py` gives tree-level g g → γγ and g g → φφ amplitudes, cross sections and two-beam rates; use it, and cross-check every load-bearing output by an independent route.

## Known constraints, prior attempts, and user-supplied data
- A massless on-shell particle cannot decay 1 → 2 into massless particles except collinearly, where the amplitude for gravitons to photons vanishes; any process must be 2 → 2 within the wave.
- Gibbons (1975): an exact plane gravitational wave produces no particles of a massless field (all the S-matrix's Bogoliubov β vanish); check its exact assumptions.
- The Gertsenshtein effect (GW → photon in a background magnetic field) is a different process and not vacuum decay.
- **Out of bounds for every agent:** `checks/` in the repository root. Agents must not read it, or any file it contains; this run is an independent re-check (see Prior runs).

## Prior runs
- checks/2026-10-11-blas-oller-gw-decay (2026-10-11, not a /conundrum run): **ignore** proposed. An earlier independent check of this paper, with strong conclusions of its own; ignoring it makes this run an independent test of those conclusions, and the main session compares the two after the judge reports. It was not source-checked by the pipeline, and its value is in its calculations, which the toolkit's calculators already encode without naming B&O.
- runs listed by prior_runs.py (wormholes, problem of time, neutron lifetime, warp drives): unrelated; none.
