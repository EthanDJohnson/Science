# Candidate answers
Exclusivity: **not mutually exclusive** (foundations positions address different facets). C1 (reframe) is compatible with every other candidate. C2 (relational) and C3 (emergent semiclassical) are complementary: C3 is C2's heavy-gravitational-clock limit. C4 (added-structure time) is compatible with C2 as its ideal-clock case. C5 (thermal time) coincides with C2 for KMS/Gibbs states and is a rival only outside them. C6 (fundamental clock decoherence) excludes C2's claim that relational evolution is *exactly* unitary. C7 (modify QM, classical or collapsing geometry) excludes C2–C6 as fundamental accounts, because it denies lasting superpositions of geometry. C8 (null) is compatible with C2–C6 treated as *partial* resolutions and excludes any claim of *complete* resolution.

Units: SI unless stated. Toy models (Page–Wootters M1, minisuperspace M2) use ħ = 1, with energies in rad/s and times in s, or dimensionless model units where marked. FRW and Gödel calculations use geometric units G = c = 1 with an arbitrary length scale L. Where a result comes from a lens, its math-check ID (M-...) is given.

Facets (brief): 1 frozen formalism, 2 multiple choice, 3 Hilbert space/inner product, 4 global time, 5 functional evolution, 6 observables, 7 spacetime reconstruction.

---

## C1: The question misplaces the conflict. QM already runs on GR's proper times on any fixed classical spacetime, and GR's time is already relational. The genuine problem of time arises only when the geometry itself is quantum (superposed), and its first observable form is a superposition of proper times, which is the gravity-mediated-entanglement phase.
type: reframe
from: EXAMINER-A, DECOMPOSER-A, DIALECTICIAN-C, IDEALIZER-C, CONSTRAINTS-R
argument:
- **"Universal, absolute" time belongs to NRQM only.** Relativistic QFT and QFTCS already run on any Cauchy foliation of a Lorentzian background, with proper times along worldlines (brief premise 1).
- **Quantum clocks read GR proper time, and this is measured.** The Sr lattice clock resolves the 1 mm redshift, -9.8(2.3)e-20 per mm measured against -1.09e-19 per mm predicted, at a fractional uncertainty of 7.6e-21 (dimensionless) [D-14, Q-05, Q-06; M-DECOMPOSER-01 verified]. The question conflates QM's evolution *parameter* (which cannot be a proper time) with QM *clocks* (which read proper time) (EXAMINER F6).
- **"Curvature" is the wrong word.** Laboratory time dilation is a potential (g_00) effect. Over 1 mm the tidal term is 1.57e-10 of the uniform-field term, and Rindler (flat) spacetime gives dilation with Riemann = 0 [calc: runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-examiner_premises.py; M-EXAMINER-01 verified].
- **GR time dilation fits inside a timeless quantum constraint as a unitary relational redshift.** With the Smith–Ahmadi mass-energy coupling, H_eff = H_S(1 − λH_S)^-1 with λ = ħG/(c⁴x) = 8.71e-76 s at x = 1 mm (SI) [calc: lens-idealizer_pw_model.py; M-EXAMINER-05, M-IDEALIZER-03, M-DIALECTICIAN-07, M-CONSTRAINTS-07 verified].
- **The frozen formalism depends on topology and quantization scheme.** For asymptotically flat spacetimes "the Hamiltonian does not vanish but its value is given rather by a nonzero surface integral" [new: Regge & Teitelboim 1974, Annals Phys. 88, 286, ACCESS abstract].
- **Facet 5 is not new to gravity.** Torre–Varadarajan non-unitarity already occurs for a free field on flat R × T^n [K-01]. A "generalized notion of unitarity does hold" [new: Agullo & Ashtekar 2015, PRD 91 124010, ACCESS abstract], and an embedding-dependent Fock Dirac quantization "super-cede[s] the no-go implications of the TV results" [new: Varadarajan 2007, PRD 75 044018, ACCESS abstract].
- **What is new to quantum gravity is a superposed geometry.** Christodoulou–Rovelli: "the relevant effect turns out to be a quantum superposition of proper times" [new: Christodoulou & Rovelli 2019, PLB 792, 64, ACCESS abstract (fetch_text)]. As a Compton-clock reading, the QGEM phase is Δτ = ħΔφ/(mc²) = 2.70e-38 s for 0.23 rad and m = 1e-14 kg (SI) [M-EXAMINER-02 verified]. An optical clock would need a superposed source of 1.8e8 kg (200/450 µm) to accumulate 1 rad in 1 s [M-IDEALIZER-12 verified].
- **Gives up:** nothing physical. It gives up the question's framing ("absolute vs relative", "curvature", "flow") and the claim that the conflict exists on classical backgrounds.
predictions:
- **If true:**
  - Every fixed-background test agrees with QM plus GR proper time, whichever quantum-gravity position is right. A two-level clock in a superposition of heights shows exactly V = |cos(ωΔτ/2)| with Δτ = gΔhT/c². The first zero is at T·Δh = 10.7 m·s for Sr (429 THz) and 4.98e5 m·s for Cs (9.19 GHz) [M-EXAMINER-04 verified], and V = 0.98921 at Δh = 1 m, T = 1 s [M-DECOMPOSER-08 verified].
  - New physics can appear only when the *source* of the geometry is superposed.
  - Clock-rate signatures of a superposed source lie 10–18 orders of magnitude below the 7.6e-21 clock resolution: 9.2e-39 (QGEM, 1e-14 kg) and 7.4e-31 (1 g displaced 1 µm at 1 mm), both dimensionless. The only accessible handle is an interferometric phase of about 0.18–0.44 rad for 1e-14 kg over 1–2.5 s [M-IDEALIZER-12].
- **If false:** a fixed-background proper-time experiment shows extra decoherence or a redshift deviation from g·Δh/c².
evidence for:
- Measured: [D-14], [Q-05], [Q-06].
- Background-free structure: [K-01] with the generalized-unitarity replies above.
- Verified calculations: [calc: lens-examiner_premises.py], [calc: lens-decomposer_subquestions.py Part 3], [calc: lens-idealizer_superposed_time.py], [calc: lens-constraints_scales.py §5].
- Constraints lens: all fixed-background predictions (Zych visibility 0.99730 at 0.5 m for 1 s; Pikovski τ_dec = 1.04e-3 s) are shared by every position [M-CONSTRAINTS-13 verified].
- The operational framework for time with gravitating quantum clocks when "the metric is ... indefinite" [new: Castro-Ruiz et al. 2020, Nat. Commun. 11, 2672, ACCESS abstract].
evidence against:
- **Math refutation (corrected here).** DECOMPOSER F4's "20–30 orders of magnitude below clock resolution" is refuted (M-DECOMPOSER-10). The correct gap is 10–18 orders: 17.9 for QGEM (17.6–18.1 with exact distances) and 10.0 for 1 g. The conclusion that clock rates cannot reach it is unchanged.
- **Math refutation (corrected here).** IDEALIZER F12's claim that the dossier's 0.23/0.57 rad [Q-10] comes from Gm²t/(ħd) with d = 450 µm is refuted (M-IDEALIZER-15). That formula gives 0.141/0.352 rad. The dossier values come from near-minus-far separations of 200 µm and 700 µm. The candidate uses only the order of magnitude, which holds.
- **The bulk constraint is local.** 𝓗 ≈ 0 holds at every point whatever the global topology, so a boundary Hamiltonian rescues time only for isolated subsystems seen from infinity, not for cosmology (DECOMPOSER F5, F7).
- **Spatial closure is observationally open:** Ω_K = -0.0054 ± 0.0055 [new: Vagnozzi et al. 2021, ApJ 908, 84, ACCESS full-text (abstract page)].
- **The quantum-geometry reading of QGEM is contested.** Whether the entanglement phase shows quantum geometry is disputed [D-23] (Anastopoulos–Hu, preprint, arXiv version withdrawn).
- **Scope.** The reframe says where the problem is. It does not solve the residual problem.
decisive test:
- **Cheapest refuting experiment:** put an internal-state optical clock in a superposition of heights (Δh ~ 0.25–1 m, T ~ 1 s) and compare the visibility with |cos(ωgΔhT/(2c²))| (predicted 0.99932 at 0.25 m and 0.98921 at 1 m). Any excess loss on a *classical* background refutes C1.
- **Positive discriminating step:** a QGEM-type witness of the superposed-proper-time phase.

---

## C2: Relational time dissolves the frozen formalism exactly and answers Kuchař's two-time objection. Here dynamics is correlation between a clock subsystem and the rest inside a constraint-satisfying state (Page–Wootters, relational Dirac observables and quantum deparametrization, one "trinity"), with covariant-POVM clocks and record-conditioned multi-time probabilities. GR time dilation appears as a unitary relational redshift. The position gives up a global time, a unique clock, and flow as a property of the global state.
type: position
from: IDEALIZER-A, DIALECTICIAN-A, CONSTRAINTS-A, DECOMPOSER-B (relational part), EXAMINER-C (relational part); DIALECTICIAN-B (the "unitarity is clock-relative" synthesis)
argument:
- **Facet 1 (single time).** For any clock uncoupled from the system, the conditional state ψ(t) = (⟨t|⊗1)Ψ of a physical state (H_C⊗1 + 1⊗H_S)Ψ = 0 obeys iψ' = H_Sψ exactly. This holds for equally or unequally spaced and degenerate clock spectra [U-01; M-EXAMINER-05 analytic proof; M-IDEALIZER-01 and M-DECOMPOSER-04 verified to ~1e-16].
- **Facet 1 (two-time; Kuchař).**
  - The naive projector rule gives P(b at t2 | a at t1) = 0 for every pair at distinct lattice times. Off the lattice it equals the clock overlap kernel times no system evolution. In a d = 8 clock with qubit H_S = σx/2 rad/s, ħ = 1 [M-DECOMPOSER-02, M-IDEALIZER-02, M-DIALECTICIAN-01, M-CONSTRAINTS-06, M-EXAMINER-06 verified].
  - A memory (record) subsystem, the GLM construction, restores the Born values 0.146447, 0.500000, 0.853553 (and 1.000000), equal to |⟨b|U(t2−t1)|a⟩|² to about 1e-15 [M-DECOMPOSER-03, M-DIALECTICIAN-02 verified].
  - Kuchař and HSL compute different quantities (DIALECTICIAN synthesis I), consistent with HSL [D-06, D-19] and Moreva 2017 [D-08].
- **Unruh–Wald/Pauli escape.** A monotonic clock exists as a covariant POVM, which resolves the identity with a defect of about 3e-15. The price is resolution δt ≳ πħ/(2ΔE): 1.405, 0.3408 and 0.0850 s for d = 4, 16 and 64 at 1 rad/s spacing [M-CONSTRAINTS-05 verified]. The ideal clock is the d → ∞ limit, with t_half·d → 3.79 [M-IDEALIZER-05 verified].
- **Gravitational coupling.** The Smith–Ahmadi coupling −λH_C⊗H_S gives the Hermitian generator H_S(1 − λH_S)^-1, a redshift and not a breakdown. It amounts to 2.35e-60 at 1 mm for an optical transition (dimensionless) [M-IDEALIZER-03, M-DIALECTICIAN-07, M-EXAMINER-07 verified].
- **Unitarity is relative to the clock variable.** A sharp reading gives fidelity 1. Conditioning on a Gaussian-blurred reading with error σ gives exactly exp(−σ²Δ²/2) dephasing [M-DIALECTICIAN-03 verified]. Tracing out a product-coupled clock gives Gaussian dephasing with time scale 1/(λω_SΔE_C) [M-IDEALIZER-14 verified; cf. Castro-Ruiz et al. 2017, PNAS 114, E2303, ACCESS abstract].
- **Multiple choice as covariance.** Facet 2 is recast as quantum-reference-frame covariance: "for any event we can find a reference frame where local quantum operations take their standard unitary dilation form" [new: Castro-Ruiz et al. 2020, ACCESS abstract]. Weak-field, Newtonian order only.
- **Facets:** 1 dissolved; 3 resolved for linear constraints and per frequency sector for Klein–Gordon [D-07]; 6 resolved for clock–system splits; 2, 4, 7 open; 5 untested (single-constraint models).
- **Gives up:** a global time; a unique clock (facet 2); flow as a property of the global state (flow is carried by records); exact unitarity once the clock couples generically; positivity of the inner product across frequency sectors.
predictions:
- **If true:**
  - Empirically equivalent to QM plus GR at all accessible scales. Differences from C3–C5 are at most (E/m_P)² or λE ~ 1e-60 (lab).
  - Record-conditioned two-time correlations show a Leggett–Garg violation that falls as K3,max = 1.5·exp(−Ω²σ²) and vanishes at Ωσ = 0.637 (dimensionless) [M-DIALECTICIAN-06 verified].
  - The record-free (naive) statistic reproduces the clock overlap kernel.
  - If gravity is quantized, gravity-mediated entanglement is present (shared with C3–C5).
- **If false:** the HSL two-time conditioning fails gauge invariance for interacting or non-covariant clocks, or the memory record cannot be embedded in the null state of a coupled constraint.
evidence for:
- Dossier and model support: [D-05], [D-06], [D-07], [D-08], [D-19] (reply side), [U-01].
- Calculations: [calc: lens-idealizer_pw_model.py], [calc: lens-dialectician_two_time.py], [calc: lens-dialectician_clock_dephasing.py], [calc: lens-dialectician_lg_resolution.py], [calc: lens-constraints_clocks.py], [calc: lens-decomposer_subquestions.py Part 1]. All the numbers cited above are verified by math checks.
evidence against:
- **Generic coupling breaks exact relational unitarity.**
  - A generic (non-gravitational) clock–system coupling makes the conditional generator non-Hermitian, linearly in the coupling g. The slope is verified; the coefficient is realization-specific, 0.34–0.93 across seeds against IDEALIZER's 0.45 (M-IDEALIZER-04).
  - The specific numbers in DECOMPOSER Part 2 (0.19–0.30 rad/s, 2.0 rad/s, norm 0.971–1.029) are **unverified** (M-DECOMPOSER-06). An independent model gives 0.24–0.31 rad/s, 1.16 rad/s and norm 0.981–1.000 at g = 0.3 rad/s. Only the qualitative result stands.
  - EXAMINER's 0.971 / 1.1e-3 are **unverified** (M-EXAMINER-08).
  - A generic coupling leaves no exact null vector at all in 40 random trials [M-CONSTRAINTS-07].
  - Gravity couples every clock to energy, so the realistic clock is the coupled one [K-09].
- **Clock dependence (facet 2) is demonstrated, not an artefact.** In a finite 3-part universe, one clock gives unitary and another non-unitary dynamics (DECOMPOSER F3, qualitative verified M-DECOMPOSER-05). Different clocks give "different and inequivalent notions of unitarity" in FLRW [D-03]. The algebraic construction "depends on which observer is employed" [new: De Vuyst et al. 2025, JHEP 07 146, ACCESS abstract].
- **The two-time answer is not independently confirmed.** HSL's own caveat that two-time gauge invariance is "not established" by Theorems 3–4 is unverifiable, and no independent assessment of HSL exists [D-19].
- **The memory construction is not a coupled-constraint null state.** It is a lattice history state with an impulsive record, not the null state of a coupled constraint (EXAMINER F9 caveat).
- **The models have one global constraint.** Facet 5 and UV issues are absent by construction (IDEALIZER ledger).
- **The inner-product problem returns.** The Klein–Gordon inner product is indefinite across sectors [D-07], and in the heavy-clock limit a Schrödinger-norm drift appears at O(E_S/(M e)) [M-IDEALIZER-08 verified; the exactly conserved quantity is the Wronskian].
decisive test:
- **Calculation (settles it):** build relational (trinity/QRF) dynamics for a constraint with local degrees of freedom and a gravitationally coupled, non-monotonic clock. Check whether evolution is unitary and clock-covariant through the clock's turning point with a positive inner product. As a smaller step, embed the GLM memory in the null state of a *coupled* constraint and test gauge invariance of the two-time probability.
- **Cheapest experiment (tests internal consistency only, not gravity):** a Moreva-type photonic Page–Wootters setup with calibrated clock-reading noise, checking the Leggett–Garg threshold Ωσ = 0.637.

---

## C3: QM's parameter time is emergent and approximate. It is the WKB/Born–Oppenheimer time carried by the heavy gravitational degrees of freedom of a Wheeler–DeWitt state (covariantly, the classical-spacetime limit of Hartle's generalized sum-over-histories QM). It is valid wherever spacetime is nearly classical, with quantum-gravitational corrections of relative size (E/m_P)², and it gives up exact unitarity, a unique time and any time at all where geometry is not classical.
type: position
from: IDEALIZER-B, CONSTRAINTS-B, CONSTRAINTS-I, EXAMINER-C (semiclassical part), DECOMPOSER-B (semiclassical part)
argument:
- **Emergence from Wheeler–DeWitt.** Expanding the Wheeler–DeWitt equation in powers of G gives a Schrödinger equation for matter on a classical background. In the adiabatic case the only surviving correction contains H_S², plus "smaller terms which describe a gravitationally induced violation of unitarity" [D-09] (peer-reviewed, abstract).
- **Toy model M2** (one heavy variable of mass M standing for m_P², ħ = 1, model units):
  - With WKB time t = x/v, the conditional state obeys i∂_tχ = [H_S + H_S²/(2Mv²)]χ. The order-0 infidelity falls as M^-2: 1.89e-4, 1.88e-6, 1.88e-8, 1.88e-10 for M = 10 to 1e4 at t = 10. The corrected equation brings 1 − F to 1.3e-9 at M = 10 [calc: runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-idealizer_bo_minisuperspace.py; M-IDEALIZER-07 verified at 40 digits].
  - This is the conditional-state construction of C2 with the heavy variable as the clock (IDEALIZER-B, CONSTRAINTS header).
- **Covariant form (Hartle).** Hamiltonian QM is "an approximation ... appropriate for those epochs and those scales when the universe ... does exhibit a classical spacetime geometry" [D-13] (review, full-text). No foliation is needed at the fundamental level, so this form is untouched by the global-time and chronology constraints (CONSTRAINTS-I).
- **Facets:** 1 dissolved approximately; 7 resolved at leading order (classical background plus local proper times); 2, 3, 4 reappear at O(1/M); 5 conditional on anomaly freedom [K-04].
- **Gives up:** exact unitarity beyond leading order; a unique time (routes differ); time near turning points and the big bang; interpretation-independence (a WKB branch is selected by hand, and the histories form needs a consistent-histories interpretation).
predictions:
- **If true:** the corrections have relative size (E/m_P)², with m_P = 2.65e19 GeV (Kiefer convention [Q-17]):
  - 4.5e-57 for the Sr transition, 2.8e-31 at 14 TeV, 1.4e-11 at H = 1e14 GeV [M-CONSTRAINTS-10, M-IDEALIZER-13 verified].
  - With the standard Planck energy 1.22e19 GeV each value is 4.7× larger (M-DECOMPOSER-12, M-IDEALIZER-13). The conclusion is unchanged.
  - The CMB low-ℓ correction is at least 1e10 below cosmic variance (0.18 at ℓ = 30) [M-CONSTRAINTS-10 verified].
  - The global-time breakdown window near a turning point shrinks as ℓ = (2M²g)^(-1/3) ∝ M^(-2/3), and the time window as Δt ∝ M^(-1/3) [M-IDEALIZER-09 verified for the scalings].
- **If false:** the O(1/M) corrections have no clock-invariant part, or the full theory cannot be anomaly-free (K-04), so the semiclassical time is inconsistent beyond leading order.
evidence for: [D-09], [D-13], [Q-17], [Q-18], [calc: lens-idealizer_bo_minisuperspace.py], [calc: lens-constraints_scales.py §1]. It explains why QM's external t works everywhere we have looked (CONSTRAINTS-B).
evidence against:
- **Semiclassical time is not unique.** Three routes (Kiefer–Singh, Maniccia–Montani reference fluid, extended phase space) give "different" equations and corrections at O(1/M) [D-21].
- **Clock dependence enters at the same order as the first correction.** Coefficients are 5.0e-5 vs 1.67e-4, a relative phase of 7.3e-3 rad (model units) (IDEALIZER F10). The arithmetic is verified, but it rests on the unproven modelling assumption that the chosen clock absorbs all of E_S (M-IDEALIZER-10).
- **Anomalies.** Giulini–Kiefer: central charges "spoil the consistency of the semiclassical approximation unless the full quantum theory of gravity and matter is anomaly-free" [K-04].
- **Foundations and data.** The Wheeler–DeWitt theory itself is unproven [D-09]. The CMB estimate [Q-19] is a preprint essay, and its size and sign are disputed by later papers seen only by title [D-21].
- **Unverified sub-numbers.** The WKB-vs-Airy error numbers are unverified (M-IDEALIZER-09) and not load-bearing.
- **Empirically idle for decades.** No observation within 20 years can test the corrections (CONSTRAINTS F10).
decisive test:
- **Calculation:** in a two-heavy-variable minisuperspace model, do a full Born–Oppenheimer expansion (not the single-clock formula) and determine whether the O(1/M) correction is the same, up to a field or clock redefinition, for different heavy-variable clocks and for the three published routes [D-21]. A clock-invariant correction would make C3 predictive; a strictly clock-dependent one reduces it to C2 plus an arbitrary choice.
- **Observation:** none within 20 years.

---

## C4: A physical time variable added to the theory removes the frozen formalism and the global-time problem by supplying an ideal clock whose constraint is linear in its momentum. The candidates are unimodular 4-volume time conjugate to Λ, a Brown–Kuchař dust frame, or a preferred CMC/York or Hořava foliation. The price is nondynamical background structure, extra matter or a preferred frame, and clock uniqueness is postulated rather than derived.
type: position
from: EXAMINER-E, DECOMPOSER-C, IDEALIZER-E, CONSTRAINTS-C
argument:
- **Unimodular time.** Quantum unimodular gravity "has a normal 'Schrödinger' form of time development" [D-11] (abstract).
- **Dust clocks.** Brown–Kuchař dust gives a functional Schrödinger equation [D-10] (full-text).
- **It is the ideal-clock limit of C2.** In M1 the d → ∞ equally spaced clock, with spectrum R, is exactly the ideal clock (IDEALIZER F5; M-IDEALIZER-05).
- **It escapes Unruh–Wald.** Λ's spectrum is unbounded, so the "H bounded below" assumption of [K-02] fails.
- **The unimodular uncertainty cost is negligible.** ΔΛ·ΔV4 ≥ 4πħG/c³ = 4π l_P² = 3.28e-69 m², so resolving 1 s over a Hubble volume costs ΔΛ ≥ 1.0e-156 m⁻², i.e. 9e-105 Λ_obs (SI). Verified under the lens's assumed canonical pairing and ħ/2 normalization (M-CONSTRAINTS-11).
- **Monotonicity.** The unimodular 4-volume T4 is monotonic in all three FRW + scalar models, while φ, volume or York time each turn in some model (G = c = 1; M-CONSTRAINTS-02 verified qualitatively; the exact turning-point counts depend on unstated initial data).
- **A single global clock avoids the Torre–Varadarajan UV obstruction** by construction (DIALECTICIAN synthesis III(b)).
- **Facets:** 1 and 4 resolved while the clock stays monotonic; 3 resolved if the linear constraint survives quantization; 2 removed by postulate; 5 and 7 partial.
- **Gives up:** a nondynamical background volume element (unimodular: "one must introduce a nondynamic background spacetime volume element" [D-11]); extra matter and a privileged frame (dust); a preferred foliation and Lorentz invariance in the gravity sector (Hořava); global hyperbolicity or chronology as an assumption.
predictions:
- **If true:**
  - No laboratory signature beyond GR with Λ as an integration constant.
  - For Hořava, gravitational-wave speed |c_T − 1| ≤ 7e-16 requires |β| ≲ 1e-15 [new: Gümrükçüoğlu et al. 2018, PRD 97, 024032, ACCESS full-text].
  - For CMC/York time in a closed ΛCDM universe (Ω_m = 0.315, H0 = 67.4 km/s/Mpc), a turning point at t* = 120.5, 79.9 and 51.2 Gyr for Ω_k = −0.001, −0.01 and −0.05 [M-CONSTRAINTS-03 verified]. It is a global clock for our epoch but not for all time if k = +1.
  - Many-fingered field clocks such as dust may meet a Torre–Varadarajan-type UV obstruction unless they use surface-dependent representations. This is an analogy, not found in the literature; low confidence (DIALECTICIAN).
- **If false:** the added clock cannot fix the conditions for measuring geometry without a further "hypertime", or its quantization is ambiguous or non-unitary.
evidence for: [D-10], [D-11], [F-01], [F-02], [calc: lens-constraints_global_time.py], [calc: lens-constraints_scales.py §2], [calc: lens-idealizer_pw_model.py (F5)].
evidence against:
- **Kuchař's critique of unimodular time.** "the cosmological time labels only equivalence classes formed by hypersurfaces separated by a zero four-volume ... unless complemented by a hypertime variable, cosmological time does not uniquely set the conditions for measuring geometric variables either in the classical or in the quantum theory" [new: Kuchař 1991, PRD 43, 3332, ACCESS abstract]. This leaves facets 5 and 7 open.
- **Dust.** Its factor-ordering ambiguity is an "overwhelming if", vacuum problems are unresolved, and it is one clock among many [D-10, F-02].
- **York time** fails (H turns) in closed universes with SEC violation (CONSTRAINTS F2, F3).
- **Chronology must be assumed.** The Gödel metric satisfies NEC, WEC, SEC and DEC yet has CTCs for r > asinh(1) = 0.8814 (G = c = 1) [M-CONSTRAINTS-04 verified]. Energy conditions therefore do not supply a global time; it must be assumed.
- **Hořava needs tuning to about 1e-15.**
- **Empirically equivalent** to C2 and C3 at accessible scales.
decisive test:
- **Calculation:** check whether a Dirac quantization of unimodular gravity *with* Kuchař's hypertime, or of Brown–Kuchař dust, gives unitary, foliation-independent functional evolution on one matter Hilbert space. This is a Torre–Varadarajan-type test of its matter sector.
- **Observation (Hořava branch only):** tighter gravitational-wave speed and preferred-frame bounds.

---

## C5: The physical flow of time is the Tomita–Takesaki modular flow of the statistical state on the observable algebra (Connes–Rovelli thermal time), with observer-dressed de Sitter or closed-universe algebras as its modern form. It gives up a state-independent time, and it coincides with clock (relational) time only for KMS/Gibbs states.
type: position
from: IDEALIZER-G, CONSTRAINTS-H; supporting findings EXAMINER F12 and DECOMPOSER F6 (observer-dressed algebras)
argument:
- **The hypothesis.** "the physical time-flow is not a universal property of the mechanical theory, but rather it is determined by the thermodynamical state" [D-12] (full-text). The Tomita–Takesaki theorem is a theorem; the physical identification is a hypothesis.
- **For a Gibbs state it reduces to Hamiltonian time:** K = βH + ln Z exactly [M-CONSTRAINTS-08 verified].
- **Equilibrium reproduces the measured redshift.** Tolman–Ehrenfest (T√(−g_tt) = const) in Schwarzschild at Earth's surface gives T(R+1 mm)/T(R) − 1 = −1.0927e-19 (SI, 50-digit arithmetic), matching the measured −9.8(2.3)e-20 per mm [M-CONSTRAINTS-09 verified; D-14].
- **Modern form: observer algebras.** The de Sitter static-patch algebra uses "operators gravitationally dressed to the worldline of an observer" [new: Chandrasekaran et al. 2023, JHEP 02, 082, ACCESS abstract]. The observer supplies a clock and the modular structure supplies the flow. That this makes C5 converge on C2 is the lens's inference, not the abstract's.
- **Facets:** 1 dissolved (flow from the state); 3 resolved algebraically; 6 resolved (dressed observables); 2 recast as a choice of state or observer; 4 and 7 open.
- **Gives up:** a state-independent time; agreement with clock time outside equilibrium.
predictions:
- **If true:** modular time coincides with relational clock time only for Gibbs weights (a single β). For a 3-level system with E = 0, 1, 3 rad/s and non-Gibbs weights (0.5, 0.2, 0.3), the modular/energy ratios are 0.916 and 0.170 rad⁻¹·s instead of one common β, so modular "time" differs from any clock reading [M-IDEALIZER-06 verified]. For a qubit every diagonal state is Gibbs, so a difference needs at least 3 levels.
- **If false:** physical clocks in non-equilibrium states track Hamiltonian time and not the modular flow.
evidence for: [D-12], [F-07], [calc: lens-constraints_scales.py §3], [calc: lens-idealizer_pw_model.py (F6)], [calc: lens-constraints_clocks.py D].
evidence against:
- **Circularity.** "the thermal time hypothesis requires dynamics – and hence time – to get off the ground" [D-24] (Chua 2024, preprint; no reply collected).
- **Non-KMS mismatch.** Outside KMS states the modular flow departs from the Hamiltonian flow and the misalignment grows with the non-Gibbs admixture. The "1–75%" residuals quoted by CONSTRAINTS are instance-dependent and only illustrative (M-CONSTRAINTS-08 partial).
- **Observer dependence.** The algebraic construction "depends on which observer is employed" [new: De Vuyst et al. 2025, ACCESS abstract], so facet 2 persists.
- **No experiment identified.**
decisive test:
- **Calculation:** show whether the states relevant to gravity (the de Sitter static patch with an observer, or a closed universe with a clock) are KMS with respect to the observer's physical clock Hamiltonian. Then compute, for a non-equilibrium state in such an algebra, whether the modular parameter tracks the observer's clock reading. Disagreement strains C5; agreement lifts the circularity worry.

---

## C6: Relational time with physically realizable clocks makes quantum evolution fundamentally non-unitary (Gambini–Porto–Pullin). A universal Planck-scale limit on clock accuracy, δT ~ t_P^(2/3) T^(1/3), produces decoherence with exponent (3/2) t_P^(4/3) T^(2/3) ω12², so the position gives up exact unitarity.
type: position
from: DECOMPOSER-F, CONSTRAINTS-G, DIALECTICIAN-B (fundamental reading)
argument:
- **The claim.** With realistic clocks "quantum mechanics ceases to be unitary and a fundamental mechanism of decoherence of quantum states arises" [D-20] (full-text).
- **Clock accuracy.** δT ~ t_P(T_max/t_P)^(1/3), from a clock whose lifetime is bounded by black-hole formation [Q-14, K-08]. δT(1 s) = 1.427e-29 s (SI) [M-DIALECTICIAN-04 verified].
- **Decoherence size.** The exponent at ω12 = 2π × 429 THz is 2.22e-27 (1 s), 2.22e-22 (1 yr) and 1.28e-15 (13.8 Gyr) (dimensionless) [M-DECOMPOSER-13, M-CONSTRAINTS-12 verified].
- **Facets:** as C2, plus a claimed fundamental resolution limit.
- **Gives up:** exact unitarity of quantum evolution; the black-hole information problem is claimed to be removed as a consequence [D-20].
predictions:
- **If true:** the decoherence exponent scales as T^(2/3)·ω12², a log-log time slope of 2/3. Markovian collapse and classical-gravity diffusion give slope 1, and Pikovski time-dilation decoherence gives slope 2 in its Gaussian regime [M-DIALECTICIAN-05 verified].
- **Size:** a 1% coherence loss in 1 s needs a level splitting ħω = 3.8e12 eV [M-CONSTRAINTS-12 verified]. The residue persists even when conditioning on a better clock.
- **If false:** conditioning on a more accurate clock removes the dephasing entirely.
evidence for: [D-20], [Q-14], [Q-15], [K-08], [F-04], [calc: lens-dialectician_clock_dephasing.py], [calc: lens-constraints_scales.py §4].
evidence against:
- **GPP's exponent is exactly Gaussian clock-reading dephasing.** It equals σ²ω²/2 with σ = √3·δT_GPP [M-DIALECTICIAN-04 verified]. A sharp reading of a covariant clock gives fidelity 1 [M-DIALECTICIAN-03]. So the "fundamental" non-unitarity is exactly as strong as the claim that no clock can beat δT.
- **Math-check caveat, which cuts both ways.** The identity is a pure rewriting (any aω² exponent equals σ²ω²/2 for some σ). Whether GPP's mechanism physically *is* clock-reading error was not confirmed from their derivation.
- **The bound is heuristic.** K-08 is a gedanken-clock argument, not a theorem of a fixed theory, and the authors call their black-hole model "very crude" [D-20].
- **Empirically idle.** The effect is 2.5e12 below the Sr clock's 92 h timing uncertainty [M-CONSTRAINTS-12], and GPP themselves say it is "too small to be observed in the lab" [Q-15].
decisive test:
- **Calculation:** derive the δT bound as a theorem of a definite theory and show it binds *every* clock, including one that conditions on a different, better clock. Equivalently, show that some decoherence residue survives conditioning on a more accurate clock. Without this, C6 reduces to C2.
- **Observation:** none within 20 years.

---

## C7: Time stays a fundamental external parameter because geometry never stays in superposition. Either gravity is classical (postquantum classical gravity) or superposed geometries collapse (Diósi–Penrose with a free R0). The problem of time is avoided rather than solved, at the price of fundamentally stochastic, non-unitary quantum dynamics and a presupposed foliation.
type: position
from: EXAMINER-D, DECOMPOSER-D, DIALECTICIAN-E, IDEALIZER-F, CONSTRAINTS-D, CONSTRAINTS-E, CONSTRAINTS-F
argument:
- **One spacetime supplies the time parameter,** so ĤΨ = 0 never arises and facets 1–5 are removed by assumption [F-05, F-06].
- **The cost is proved for hybrid dynamics.** Hybrid classical–quantum dynamics "necessarily results in decoherence of the quantum system", and classical GR "necessarily modifies the dynamical laws of quantum mechanics – the theory must be fundamentally stochastic" [K-05] (peer-reviewed).
- **The simplest variant is eliminated.** Fundamentally semiclassical gravity (Møller–Rosenfeld/Schrödinger–Newton) with standard collapse "gives rise to superluminal signalling" [new: Bahrami et al. 2014, NJP 16, 115007, ACCESS abstract]. Page–Geilker's result is "inconsistent with ... the semiclassical Einstein equations" [new: Page & Geilker 1981, PRL 47, 979, ACCESS abstract]. So only collapse-augmented or stochastic versions survive (CONSTRAINTS-E: eliminated in simplest form).
- **Surviving variants.**
  - Diósi–Penrose with free R0 > 0.54e-10 m (probability 0.95) [K-07, Q-01].
  - Postquantum classical gravity with kernels other than the delta kernel [K-06].
- **Gives up:** unitarity and determinism of QM; energy conservation (bounded: DP heating 1.28e-17 K/s at R0 = 0.54e-10 m [M-CONSTRAINTS-14 verified]); foliation independence (it assumes a foliation and chronology); the quantum nature of gravity.
predictions:
- **If true:**
  - **No gravity-mediated entanglement** in a QGEM-type test. The quantum-geometry positions predict a phase of about 0.18/0.44 rad (1e-14 kg, 200/450 µm, 1 s/2.5 s [M-IDEALIZER-12]) or 0.23/0.57 rad (dossier 200/700 µm convention, per M-IDEALIZER-15).
  - **For DP:** the bulk self-energy difference for a 1e-14 kg diamond (R = 0.879 µm) split by 250 µm is E_G = 0.91–1.82e-32 J, so τ_DP = ħ/E_G = 5.8–11.6 ms (SI), independent of the free R0 (the granular term, 3e-40 J, is negligible) [M-CONSTRAINTS-14 verified; factor-2 convention ambiguity unresolved]. QGEM with about 1 s of coherence would then see no entanglement.
  - **For postquantum classical gravity:** a diffusion–decoherence trade-off, with D2 inside the window between the torsion-balance and interferometry bounds for surviving kernels [Q-20, Q-21].
  - The decoherence exponent is linear in time (Markovian slope 1) [M-DIALECTICIAN-05].
- **If false:** gravity-mediated entanglement is observed with coherence of order 1 s, modulo [D-23].
evidence for: [K-05], [K-06], [K-07], [D-18] (arguments that gravity must be quantized are inconclusive), [calc: lens-constraints_scales.py §6–7].
evidence against:
- **Excluded versions.** The delta-kernel postquantum model is excluded by a factor of 1e17 (D2 ≥ 1e-24 needed against ≤ 1e-41 kg² s m⁻³ allowed) [K-06; M-CONSTRAINTS-15]. Parameter-free Penrose (R0 = 0.05e-10 m for Ge) is excluded by the 0.54e-10 m bound [K-07].
- **Page–Geilker supports (but does not prove) quantized gravity** [new: Page & Geilker 1981].
- **A foliation and chronology must be assumed** (Gödel example, M-CONSTRAINTS-04).
- **It replaces facets 1–7 rather than solving them.**
- **Dossier error flagged.** The Q-04 DP heating value (~1e-4 K/s) is inconsistent with its own formula, which gives 2.0e-3 K/s at R0 = 1e-15 m (M-CONSTRAINTS-14, arithmetic confirmed). It is not load-bearing here.
- **The decisive experiment is far off.** Matter-wave interferometry reaches about 4.2e-23 kg, 8.4 orders below 1e-14 kg [Q-12] (search-summary). The heaviest cat state's superposition size is 2.1e-18 m, about 1e14 below the requirement [D-16, Q-11].
- **Entanglement may not decide it.** Whether entanglement would refute a classical mediator is itself contested [D-23].
decisive test:
- **Settles it:** a QGEM-type spin-entanglement witness (m ~ 1e-14 kg, Δx ~ 250 µm, coherence ~1 s) [Q-09]. Entanglement eliminates DP and postquantum classical gravity; a clean null at the required sensitivity promotes C7.
- **Cheaper partial test of DP alone:** show that a 1e-14 kg superposition over 250 µm stays coherent longer than about 12 ms.

---

## C8: No position resolves the problem of time within admissible physics. Every consistent position either leaves the multiple-choice, global-time and spacetime-reconstruction facets (2, 4, 7) open in strongly quantum, gravitationally coupled geometry (plus functional evolution, facet 5, once constraints are local), or removes them by modifying QM or adding background structure.
type: null
from: EXAMINER-B, DECOMPOSER-E, DIALECTICIAN-D, IDEALIZER-D, CONSTRAINTS-N
argument:
- **Kuchař's verdict is not overturned for the full-gravity case.** "none of us has so far succeeded in proposing an interpretation of quantum gravity that would either solve or circumvent the problems of time" [D-04].
- **The other positions all fall short** (C2–C7 above):
  - C2 is exact only for uncoupled or product-coupled clocks, and facets 2 and 4 stay open [D-03, K-09].
  - In M2, dissolving facet 1 brings back clock dependence, norm drift and turning-point failure at O(E/K_heavy), the same order as the first quantum-gravity correction (IDEALIZER-D).
  - C3 is approximate and non-unique [D-21, K-04].
  - C4 adds structure and needs a hypertime (Kuchař 1991).
  - C5 needs KMS states.
  - C6 rests on a heuristic bound.
  - C7 modifies QM and is squeezed [K-06, K-07].
- **Every model has a single global constraint,** so facet 5 in the local theory is untested (IDEALIZER ledger).
- **Facets 2 and 4 are a genuine non-uniqueness, not a contradiction a synthesis can remove,** and facet 7 has no dedicated source (DIALECTICIAN-D weak form).
- **Weak vs strong form.** The null holds in its *weak* form (facets 2, 4, 7 open). The *strong* form, "every facet unresolved", is strained: facet 1 is dissolved for ideal and covariant clocks (C2), and facet 5 is dissolved as a gravity-specific problem by generalized unitarity (C1).
predictions:
- **If true:**
  - No experiment within 20 years separates C2, C3, C4, C5 and C6. Their calculated differences are at most 1e-11 fractional, from (E/m_P)² at H = 1e14 GeV, and about 1e-60 in the lab [M-CONSTRAINTS-10, M-EXAMINER-07].
  - Only C7 (and the C1 fork, quantum vs classical geometry) carries near-term bounds.
  - No construction appears that gives clock-covariant unitary relational dynamics for local gravitational constraints.
- **If false:** such a construction exists and recovers GR proper times.
evidence for: [D-04], [D-03], [D-21], [K-04], [K-09], dossier §6 ("No discriminating observation among the 'conservative' positions"), [calc: lens-idealizer_bo_minisuperspace.py], [calc: lens-constraints_global_time.py], and the constraint × candidate matrix (CONSTRAINTS lens).
evidence against:
- **Several facets are already dissolved at no cost beyond a global flow:** facet 1 including two-time questions (C2), and facet 5 via generalized unitarity (C1) (DIALECTICIAN synthesis).
- **Weak-field QRF covariance** claims a local unitary frame always exists [new: Castro-Ruiz et al. 2020, ACCESS abstract].
- **The demand may be ill-posed.** If C1 is right, "resolve all seven facets" misstates what is needed, because facets 1 and 5 are scheme- and QFT-level artefacts.
decisive test:
- **Calculation (would refute C8):** in a model with local degrees of freedom and a clock that turns around, exhibit relational dynamics that is clock-covariant and unitary with a positive inner product, has anomaly-free functional evolution, and recovers GR proper times.
- **Smaller calculation:** in the flat FLRW + scalar + fluid model [D-03], construct a clock-invariant prediction that decides between scalar-clock recollapse and fluid-clock singularity resolution. If none can be constructed, the weak null stands.
