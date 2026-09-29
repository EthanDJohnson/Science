# Analysis: constraints (Kant — conditions any valid answer must satisfy)

## Method applied
Audit of every constraint a position on the problem of time must satisfy (energy conditions and the theorems that use them, quantum inequalities, conservation and thermodynamics, causality/chronology and global time, stability, plus the problem-specific no-go results K-01 to K-09), with a calculation of what each candidate position requires against each constraint, and a statement of the assumptions under which each constraint actually binds. Classification per candidate: violates / strained / consistent.

## Findings
1. **Energy conditions and quantum inequalities do not bind any position directly.** As the dossier notes, no classical energy condition or quantum energy inequality enters K-01 to K-09 ([D-§4 header]). None of the positions needs negative energy, so the Ford–Roman bounds (free fields on a fixed background, sampling time short compared with the curvature radius) have nothing to bound. They are **not violated, and not applicable**. Energy conditions do enter *indirectly*, through facet 4 (global time). The Friedmann/Raychaudhuri equations give dH/dt = -4π(ρ+p) + k/a² = -(4π/3)(ρ+3p) - H² (G = c = 1). So York/CMC time K = -3H is strictly monotonic whenever the SEC holds (any k), or the NEC holds and k ≤ 0. When the SEC fails in a closed (k = +1) universe it can have turning points. gr_tensors reproduces the Hamiltonian constraint ρ = 3(ȧ²+k)/(8πa²) and the pressure equation to 4e-16 and 7e-16 relative error [calc: runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-constraints_global_time.py, Part A]. This is the classical statement of facet 1: the ρ equation is a constraint, first order in time, not an evolution equation [D-01].
2. **Which internal clocks are monotonic (facet 4, classical minisuperspace)** [calc: …/lens-constraints_global_time.py, Part B]. Turning points were counted over t = 0–60 L (geometric units, arbitrary length scale L), with RK4 at n = 60000 and 1.5n = 90000 steps giving identical counts and a constraint residual ≤ 3e-6.
   - (i) Closed universe, massless scalar: the volume turns once (recollapse). φ, York time and the unimodular 4-volume T4 = ∫a³dt are monotonic. The SEC holds (Type I). The DEC is exactly saturated (ρ = p for a stiff fluid); the 5 of 40 points flagged are round-off at saturation.
   - (ii) Flat universe, massive scalar (m = 1/L): φ has 17 turning points. Volume, H and T4 are monotonic. The SEC is violated at 18 of 40 sampled points and the NEC at none.
   - (iii) Closed universe, massive scalar: φ has 17 turning points and H has **35**, so York time fails. Volume and T4 are monotonic over the window, and the SEC is violated at 18 of 40 points.
   - Only the unimodular 4-volume, and dust proper time along non-crossing worldlines, are monotonic by construction. Every matter or geometric clock tested fails in some admissible model. This supports facet 4 as a real constraint on "internal clock" positions [D-02, D-03].
3. **Closed ΛCDM: York time has a turning point** at a* = 3Ω_m/(2|Ω_k|), where H reaches a minimum just below H0·√Ω_Λ and then rises. With Ω_m = 0.315 and H0 = 67.4 km/s/Mpc: for Ω_k = -0.001, a* = 472.5 and t* = 120.5 Gyr; for -0.01, a* = 47.3 and t* = 79.9 Gyr; for -0.05, a* = 9.45 and t* = 51.2 Gyr. Integration with n = 20000 and 30000 agrees to 0.01 Gyr [calc: …/lens-constraints_global_time.py, Part D]. So CMC/York time (shape dynamics, the York-time deparametrization) is a global clock for our epoch but not for all time if k = +1. The failure lies in the far future and has no observable consequence now.
4. **Chronology: energy conditions do not guarantee a global time.** The Gödel metric (a_G = 1 L) requires a source that satisfies NEC, WEC, SEC and DEC (Hawking–Ellis type I) at all 25 scanned radii, r = 0.1–2.5. Yet g_φφ = 4a²(sinh²r − sinh⁴r) < 0 for r > asinh(1) = 0.8814, so closed timelike curves pass through every event (the space is homogeneous) and no global time function exists [calc: …/lens-constraints_global_time.py, Part C]. Any position that needs a foliation (unimodular time, preferred-foliation theories, collapse dynamics, dust or scalar deparametrization, Bohmian mechanics) must *assume* stable causality or global hyperbolicity. Canonical GR already does this through M = R × Σ [D-01]. This restricts the domain; it is not a violation, and it is consistent with observation. Relational and histories positions do not need a foliation.
5. **The Unruh–Wald/Pauli no-go is evaded only by unsharp clocks, at a quantified price** [calc: runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-constraints_clocks.py, A]. The test clocks are finite and equally spaced (bounded spectrum, ω = 1 rad/s, ħ = 1). Their time states are orthogonal only at lattice times, where |⟨t|t+τ⟩|/d ≤ 7e-17. Between lattice points they overlap: 0.90 at a quarter-step and 0.64 at a half-step, for d = 4, 16 and 64. The covariant POVM still resolves the identity over one period (defect ≤ 3e-15). The Mandelstam–Tamm resolution π/(2ΔE) is 1.41 s, 0.34 s and 0.085 s for d = 4, 16 and 64. So a monotonic clock variable exists only as a POVM, as K-02's escape clause requires. **Relational positions therefore pay with finite time resolution (δt ≳ πħ/(2ΔE_clock)). K-02 does not falsify them**, because its sharp-PVM assumption is dropped, not violated.
6. **Kuchař's two-time objection holds for the naive rule and fails for the memory rule, inside the model** [calc: …/lens-constraints_clocks.py, B]. Setup: a qubit with H = 0.5σx and d = 8. The naive projector conditional probability gives P(1 at t2 | 0 at t1) = 0 exactly for three pairs t1 ≠ t2, and 1 for equal times, which is K-03's reductio. The Giovannetti–Lloyd–Maccone memory construction gives 0.500000, 0.853553 and 1.000000, equal to the Born values |⟨1|U(t2−t1)|0⟩|² to 1e-6. The objection therefore constrains the *interpretation rule*, not the relational framework. The escape costs an extra memory record in the constraint, consistent with the HSL reply [D-19, K-03]. This is a finite-dimensional, uncoupled-clock result only.
7. **Interacting clocks: the gravitational (Smith–Ahmadi) coupling is unitary and negligible; generic couplings remove exact physical states** [calc: …/lens-constraints_clocks.py, C].
   - With λ = ħG/(c⁴x), the Sr-transition clock (ω_S = 2π × 429 THz) has a fractional shift λω_S = 2.35e-60 at x = 1 mm and 2.35e-63 at 1 m. Reaching the 1e-18 level of current clocks would need E_S/x ≥ 1.2e26 J/m, a mass-energy of 1.3e9 kg per metre of separation.
   - In the finite model (λ = 0.05) the effective generator is Hermitian to 1.7e-16, with eigenvalues [0, 1.052632] = H_S/(1−λH_S). The coupling acts as a time dilation, not a non-unitarity.
   - A generic random Hermitian coupling (g = 0.05 or 0.2, dimension 6 × 3) leaves **no** exact null vector of J. A coupled finite constraint has solutions only when fine-tuned, or with a clock large enough to absorb the shift.
   - The interacting-clock facet is therefore a real constraint on *which* clock–system splits admit PW dynamics. For gravity at laboratory scales the effect is about 1e-60, so no experiment can separate "ideal" from "gravitationally coupled" relational clocks.
8. **Thermal time recovers mechanical time only for KMS (Gibbs) states** [calc: …/lens-constraints_clocks.py, D]. For a 4-level H at β = 0.7, the modular Hamiltonian satisfies K = βH + c to 1e-16. Mixing in a random non-Gibbs admixture ε = 0.01, 0.1 or 0.5 gives ‖[K,H]‖/(‖K‖‖H‖) = 3.4e-3, 3.3e-2 and 0.16, and the best proportional fit leaves residuals of 1.3%, 14% and 75%. The thermal-time flow is not the Hamiltonian flow outside equilibrium. So the position needs the state to be KMS with respect to *some* H before it can reproduce laboratory dynamics. This is the calculable form of the circularity worry [D-24]: consistent, but the recovery of NRQM time (the "right limits" condition) is strained for non-equilibrium states.
9. **Thermal time reproduces the measured redshift gradient in equilibrium** [calc: runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-constraints_scales.py, §3].
   - Tolman–Ehrenfest (T√(−g_tt) = const) with gr_tensors Schwarzschild at Earth's surface gives T(R+1 mm)/T(R) − 1 = −1.0927e-19 in 50-digit arithmetic. float64 returns exactly 0, a precision trap caught by the check. This equals the redshift prediction (−1.09e-19 per mm) and is consistent with the measured Sr gradient, −9.8(2.3)e-20 per mm [D-14, Q-06]. So "temperature as the speed of time" does not conflict with the one precision test of gravitational time on mm scales.
   - Unruh temperature at a = g: 3.98e-20 K. For that state the modular parameter maps to proper time as dτ/ds = 2πc/a = 1.92e8 s.
   - `horizons_1p1` on the Painlevé–Gullstrand river u = −√(2M/r) for 1 M_sun finds the horizon at 2953.25 m with κ = 1.6930e-4 1/m = 1/(4M), so T_H = 6.17e-8 K.
10. **Semiclassical (WKB) time: the corrections are below every achievable precision** [calc: …/lens-constraints_scales.py, §1].
    - (E/m_P)², with m_P = 2.650e19 GeV (Kiefer convention, Q-17): 4.5e-57 (Sr transition), 2.6e-55 (hydrogen), 2.8e-31 (LHC) [matches Q-18], 1.4e-13 (H = 1e13 GeV) and 1.4e-11 (H = 1e14 GeV).
    - The cosmic variance of C_ℓ is 0.63, 0.31 and 0.18 at ℓ = 2, 10 and 30, so even at the tensor-mode bound the correction is ≥ 1e10 below cosmic variance.
    - The best clock resolves 7.6e-21 [Q-05], 1e36 above the Sr-scale correction.
    - No observation within 20 years can test the semiclassical-time corrections: they are consistent and empirically idle. Their consistency constraint is theoretical: the full theory must be anomaly-free [K-04].
11. **Unimodular time passes the uncertainty and conservation audit.**
    - From S_Λ = −(c³/8πG)Λ·V4 (V4 the four-volume in m⁴), the pair (V4, −c³Λ/8πG) is canonical. So ΔΛ·ΔV4 ≥ 4πħG/c³ = 4π l_P² = 3.28e-69 m² (my derivation, SI).
    - Resolving cosmic time to 1 s over a Hubble volume costs ΔΛ ≥ 1.0e-156 m⁻² = 9e-105 Λ_obs (Λ_obs = 1.09e-52 m⁻²). At 1e-15 s the cost is 9e-90 Λ_obs [calc: …/lens-constraints_scales.py, §2].
    - The Unruh–Wald no-go (K-02) does not bind, because its assumption "H bounded below" fails: Λ's spectrum is the whole real line.
    - The binding constraint is structural. It is Kuchař's own: [new: Kuchař 1991, Phys. Rev. D 43, 3332, abstract (via INSPIRE API, fetch_text), "the cosmological time labels only equivalence classes formed by hypersurfaces separated by a zero four-volume, while individual spacelike hypersurfaces within an equivalence class are physically irrelevant. As a result, unless complemented by a hypertime variable, cosmological time does not uniquely set the conditions for measuring geometric variables either in the classical or in the quantum theory."] This closes the dossier's gap "no critique of unimodular time was collected" [D-§6], and it leaves facet 5/7 (local, many-fingered time) open.
12. **Realistic-clock decoherence (GPP) is consistent and unobservable** [calc: …/lens-constraints_scales.py, §4].
    - δT(1 s) = 1.43e-29 s and δT(92 h) = 9.9e-28 s, against the Sr clock's 92 h timing uncertainty of about 7.6e-21 × 92 h = 2.5e-15 s, a gap of 2.5e12.
    - The decoherence exponent for the Sr transition is 2.2e-27 (1 s), 2.2e-22 (1 yr) and 1.3e-15 (13.8 Gyr), reproducing Q-15.
    - A 1% loss of coherence in 1 s needs a level splitting of ħω = 3.8e12 eV (5.7e27 rad/s). No coherent superposition is remotely near this.
    - GPP is therefore empirically equivalent to the ideal-clock relational position at every foreseeable scale [D-20].
13. **Clock-in-superposition tests are shared predictions, not discriminators** [calc: …/lens-constraints_scales.py, §5].
    - An Sr clock with interferometer arms Δh = 0.01, 0.1 and 0.5 m apart for 1 s accumulates Δτ = 1.1e-18, 1.1e-17 and 5.5e-17 s, giving visibilities 1.00000, 0.99989 and 0.99730. This is Zych's witness, from QM plus GR on a fixed background; closed light-pulse interferometers see it only with internal-state transitions [F-09].
    - Pikovski τ_dec is 1.04e-3 s (gram scale, reproduces Q-08). For a 25 kDa molecule with about 6000 modes at 500 K and an assumed 0.1 µm vertical split it is 2.6e7 s. For a vertical QGEM diamond at 1 K it is 3.2e2 s.
    - Every position that recovers QM on a classical background predicts the same numbers. They test hidden premise 1 (QM already copes with relativistic time), not the rivals.
14. **Diósi–Penrose makes a sharp, near-term-relevant prediction for QGEM** [calc: …/lens-constraints_scales.py, §6].
    - For m = 1e-14 kg diamond (R = 0.88 µm) split by 250 µm [Q-09], the bulk E_G = (1 to 2) × Gm²(6/(5R) − 1/Δx) = 0.9–1.8e-32 J, so τ_DP = ħ/E_G = 6–12 ms. The factor-2 spread is a convention ambiguity I did not resolve.
    - The granular (per-nucleus, R0 = 0.54e-10 m) term is 3e-40 J, negligible. So the prediction does not depend on the free R0 that survives K-07.
    - QGEM needs about 1 s of coherence. Free-R0 DP therefore predicts **no** gravity-mediated entanglement, and a successful QGEM run would eliminate it. This is my arithmetic, not a quoted result.
    - Conservation audit: the DP heating formula quoted in Q-04 evaluates to 2.0e-3 K/s at R0 = 1e-15 m, not the "~1e-4 K/s" stated there, a factor-20 inconsistency to flag for the math check. At the R0 bound (0.54e-10 m) it gives 1.3e-17 K/s, far below detectability. The energy non-conservation is real but bounded.
15. **Fundamentally semiclassical gravity (Møller–Rosenfeld/Schrödinger–Newton) fails a causality constraint unless collapse is added.**
    - [new: Bahrami et al. 2014, "The Schrödinger-Newton equation and its foundations", New J. Phys. 16, 115007, arXiv:1407.4370 abstract (fetch_text), "Together with the standard collapse postulate, fundamentally semi-classical gravity gives rise to superluminal signalling. A consistent fundamentally semi-classical theory of gravity can therefore only be achieved together with a suitable prescription of the wave-function collapse."]
    - The simplest version is also experimentally disfavoured: [new: Page & Geilker 1981, Phys. Rev. Lett. 47, 979, abstract (lit_search), "An experiment gave results inconsistent with the simplest alternative to quantum gravity, the semiclassical Einstein equations. This evidence supports (but does not prove) the hypothesis that a consistent theory of gravity coupled to quantized matter should also have the gravitational field quantized."]
    - Status: *violates* (causality or observation) in its simplest form; it survives only as a collapse-augmented theory, which reduces it to D/F-type positions.
16. **Postquantum classical gravity: the delta-kernel version is excluded by a factor of 1e17** (D2 ≥ 1e-24 needed against ≤ 1e-41 kg² s m⁻³ allowed) [K-06, Q-20, Q-21; calc §7]. Other kernels are not excluded by this argument. Its time is the classical spacetime's, so it *removes* facets 1–3 by fiat rather than solving them [F-05], at the price of the fundamental stochasticity and irreversibility in K-05.
17. **Preferred-foliation theories (Hořava–Lifshitz; khronometric) need a coupling tuned to 1e-15.** [new: Gümrükçüoğlu et al. 2018, "Hořava gravity after GW170817", Phys. Rev. D 97, 024032, arXiv:1711.08845 full text (fetch_text), "GW170817 with coincident gamma ray emission [6] yields − 3× 10−15≤cT− 1≤ 7× 10−16, (13) … which implies that |β| ≲ 10−15."] A preferred foliation (global time) is compatible with observation only if its gravitational-sector Lorentz violation is suppressed to about 1e-15 in β. The theory is *strained*, not violated.

## Lens-specific outputs

### Constraint ledger: what binds, and under which assumptions

| # | Constraint | Assumptions under which it binds | Binds here? | Evidence |
|---|---|---|---|---|
| K1 | Energy conditions (NEC/WEC/SEC/DEC) | Classical T_ab; used by singularity and focusing theorems | Only indirectly: SEC (or NEC with k ≤ 0) makes York time monotonic; they do not guarantee a global time function (Gödel) | F1–F4 |
| K2 | Ford–Roman quantum inequalities | Free QFT on a fixed background, sampling time ≪ curvature radius, negative energy present | **No.** No position needs negative energy | F1 |
| K3 | Hamiltonian constraint / frozen formalism | Spatially closed universe; Dirac quantization | Yes, for canonical positions. Not for asymptotically flat spacetimes (ADM energy survives) or reduced/deparametrized quantizations | [D-01], F1 |
| K4 | Pauli / Unruh–Wald no monotonic clock | H bounded below; sharp PVM clock | Evaded by POVM clocks (at the cost of δt ≳ πħ/2ΔE) and by unbounded "clock Hamiltonians" (unimodular Λ, ideal clocks) | [K-02], F5, F11 |
| K5 | Kuchař two-time reductio | Naive projectors applied twice to the physical state | Binds the naive rule only; the memory rule gives the Born values | [K-03], F6 |
| K6 | Clock dependence (multiple choice) | Different deparametrizations; unitarity per clock | Yes: an open cost for all internal-time positions | [D-02], [D-03] |
| K7 | Global time: no monotonic internal clock | Generic matter content, closed universes | Yes: φ, volume and York time each fail in some model; only unimodular 4-volume and dust (before caustics) are monotonic by construction | F2, F3 |
| K8 | Torre–Varadarajan functional evolution | Free field, Fock representation, dim > 2, arbitrary Cauchy surfaces | Yes for many-fingered-time (Tomonaga–Schwinger) evolution, even on a flat background. Avoided by evolving along one fixed foliation or one clock | [K-01] |
| K9 | Giulini–Kiefer anomaly condition | WKB/Born–Oppenheimer expansion | Conditional: semiclassical time is consistent only if the full theory is anomaly-free | [K-04] |
| K10 | Chronology (stable causality) | Any position needing a global foliation | Restricts the domain to globally hyperbolic spacetimes; consistent with observation | F4 |
| K11 | Energy conservation / thermodynamics | Unitary, time-translation-invariant dynamics | Violated by DP (heating 1.3e-17 K/s at the R0 bound) and by PQCG (diffusion); both are bounded, not excluded. GPP decoherence is in the energy basis | F14, F16, [K-05] |
| K12 | No superluminal signalling | Nonlinear or state-dependent dynamics plus collapse | **Violated** by fundamentally semiclassical (Møller–Rosenfeld/Schrödinger–Newton) gravity with standard collapse | F15 |
| K13 | Lorentz invariance of gravitational waves | Preferred-foliation theories | |c_T − 1| ≤ 7e-16 requires |β| ≲ 1e-15 | F17 |
| K14 | Collapse bounds | DP smeared-mass model | R0 > 0.54e-10 m, which kills parameter-free Penrose; free R0 survives, but QGEM would test the bulk E_G | [K-07], F14 |
| K15 | Classical-gravity squeeze | PQCG, delta kernel, Markovian | Delta kernel excluded by 1e17; other kernels open | [K-06], F16 |
| K16 | Stability | — | No instability computed here. The Hořava–Lifshitz extra scalar mode and the stability of the PQCG diffusion are not audited (gap) | — |

### Candidate × constraint matrix
Key: C = consistent, S = strained, V = violates, n/a = the constraint's assumptions do not hold.

| Position | K3 frozen | K4 clock no-go | K5 two-time | K6 multiple choice | K7 global time | K8 functional evol. | K11 conservation | K12 causality | Observational bound | Overall |
|---|---|---|---|---|---|---|---|---|---|---|
| Relational PW/trinity (POVM clocks) | C (reinterpreted) | C (POVM) | C (memory rule) | S (open) | S (no monotonic clock in general) | C per clock | C | C | none; equivalent to QM+GR | **consistent, facets 2/4 open** |
| Semiclassical WKB time | C (emergent) | n/a | n/a | S (routes differ [D-21]) | S (fails at turning points) | S (K-04) | S (tiny non-unitarity [D-09]) | C | corrections ≤ 1e-11 | **consistent as an effective theory** |
| Unimodular time | C | n/a (unbounded Λ) | C | C (one time) | C (4-volume monotonic) | **S** (Kuchař 1991: needs hypertime) | C (ΔΛ ~ 1e-105 Λ_obs) | C in globally hyperbolic spacetimes | none | **strained** |
| Dust / scalar deparametrization | C | C | C | S | S (caustics; φ turns) | C along the dust frame | C | C | none | **strained** |
| CMC/York, shape dynamics, Hořava | C | C | C | C (one preferred slicing) | S (York turns if SEC fails, k = +1) | C along the foliation | C | C | |β| ≲ 1e-15 (Hořava) | **strained** |
| Thermal time | C | n/a | n/a | S (state-dependent flow) | S | n/a | C | C | Tolman = redshift −1.09e-19/mm ✓ | **consistent in equilibrium, strained outside it** |
| Histories (Hartle) | C | n/a | C | S (measure from classical limit) | C (no foliation needed) | C | C | C | none | **consistent; interpretation-dependent** |
| DP collapse (free R0) | n/a (needs external time) | n/a | n/a | n/a | assumes foliation | n/a | S (heating) | C (collapse models avoid signalling [F15 quote]) | R0 > 0.54e-10 m; QGEM would decide | **surviving, testable** |
| Semiclassical MR/SN gravity | n/a | n/a | n/a | n/a | assumes foliation | n/a | C | **V** (with collapse) | Page–Geilker | **eliminated in simplest form** |
| Postquantum classical gravity | removed by fiat | n/a | n/a | n/a | classical time | n/a | S (diffusion) | C | delta kernel excluded ×1e17 | **strained** |
| GPP realistic-clock decoherence | C | C | C | S | S | C | C | C | 1% needs 3.8e12 eV splitting | **consistent, empirically idle** |

### Validity domains of the models the dossier relies on
- **FRW minisuperspace** (F2, F3, [D-03]): homogeneity truncation. Clock-monotonicity results are exact for the model. Inhomogeneous modes can only add further failures of monotonicity.
- **Finite-dimensional Page–Wootters** (F5–F7, [D-17], [U-01]): non-relativistic, finite dimension, uncoupled or Newtonian-coupled (λE ≪ 1). Relativistic Klein–Gordon constraints hold only per frequency sector [D-07], and the Klein–Gordon inner product is indefinite across sectors. Positive- and negative-frequency components enter the norm with opposite signs (standard; not computed here).
- **Semiclassical gravity (Møller–Rosenfeld)**: valid only when quantum fluctuations of T_ab are small compared with its mean. It fails for macroscopic mass superpositions (Page–Geilker, F15). The question's regime (quantum geometry) lies outside it.
- **WKB/Born–Oppenheimer** (F10, [D-09]): E ≪ m_P, away from classical turning points and the big bang. It lies inside its domain everywhere we can observe, which is exactly why it cannot be tested there.
- **Smith–Ahmadi coupling, DP, PQCG**: weak-field, Newtonian, non-relativistic. The DP collapse time (F14) is a Newtonian estimate.
- **Thermal time** (F8, F9): von Neumann algebra with a faithful state. The flow is geometric only for KMS or Bisognano–Wichmann states.
- **Tolman–Ehrenfest/redshift** (F9): static spacetimes, equilibrium.
- **Overall:** the problem of time proper (closed universe, quantum geometry, Planck-scale Hamiltonian constraint) lies outside the validity domain of *every* established model here. "Consistent" in this audit means internally consistent and not contradicted by data, not verified in the regime.

## Calculations
- `runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-constraints_global_time.py` (gr_tensors; runs in about 8 s):
  - FRW Hamiltonian constraint and pressure: relative error 4e-16 and 7e-16.
  - Turning-point audit of internal clocks in three minisuperspace models, stable under n → 1.5n (constraint residual ≤ 3e-6), with gr_tensors energy-condition scans.
  - Gödel: all energy conditions hold (25 radii) while CTCs appear for r > 0.8814.
  - Closed ΛCDM York-time turning point: t* = 120.5, 79.9 and 51.2 Gyr for Ω_k = −0.001, −0.01 and −0.05 (n versus 1.5n agree).
- `runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-constraints_clocks.py` (page_wootters toolkit, ħ = 1):
  - POVM sharpness: overlaps 0.90 and 0.64 off-lattice; Mandelstam–Tamm bounds 1.41, 0.34 and 0.085 s.
  - Kuchař naive two-time probability = 0, against GLM = Born (0.5, 0.853553, 1.0).
  - Smith–Ahmadi shift: 2.35e-60 at 1 mm. H_eff is Hermitian (1.7e-16). A generic coupling leaves no null space.
  - Modular versus Hamiltonian flow: misalignment 3.4e-3 to 0.16.
- `runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-constraints_scales.py` (SI):
  - (E/m_P)²: 4.5e-57 to 1.4e-11.
  - Unimodular: ΔΛΔV4 ≥ 3.28e-69 m², so ΔΛ/Λ_obs ≥ 9e-105 at 1 s.
  - Tolman ratio −1.0927e-19 per mm (50 digits; float64 gives 0).
  - T_U(g) = 3.98e-20 K; T_H(M_sun) = 6.17e-8 K via horizons_1p1.
  - GPP gap 2.5e12; 1% decoherence needs 3.8e12 eV.
  - Pikovski τ_dec: 1.04e-3 s, 2.6e7 s and 3.2e2 s.
  - Zych visibility 0.99730 (0.5 m, 1 s).
  - DP: τ = 6–12 ms for QGEM; heating 1.3e-17 K/s at the bound, and 2.0e-3 K/s at 1e-15 m (the Q-04 value is inconsistent with its own formula).
  - PQCG gap 1e17.

## Candidate answers (at least 3; the null and a reframe count)
Header: the candidates are **not** mutually exclusive. A (relational), B (semiclassical) and H (thermal) are complementary: semiclassical time can be read as a relational clock in a WKB state, and thermal time coincides with it for KMS states. D, E and F exclude A–C as *fundamental* accounts.

- [CONSTRAINTS-A] **Relational time (Page–Wootters, relational Dirac observables, trinity) with unsharp (covariant-POVM) clocks resolves facets 1, 5 and 6 without modifying QM or GR, and leaves facets 2 and 4 open.**
  - Status: surviving.
  - Why: the only no-go that bites (K4) assumes sharp clocks and is escaped at the price δt ≳ πħ/(2ΔE) (F5). Kuchař's reductio binds only the naive rule, and the memory rule gives the Born values (F6). Gravitational clock coupling is unitary and about 1e-60 (F7).
  - Facet 7 (spacetime reconstruction) is not addressed by this model.
  - Cost: clock dependence [D-03] and no monotonic clock in general (F2).
  - Prediction: empirically equivalent to QM plus GR on a background at all accessible scales. The calculable signature is finite resolution, with two-time statistics requiring a record system. No experiment separates it from B, G or H.
  - Confidence: medium.
- [CONSTRAINTS-B] **Semiclassical (Born–Oppenheimer/WKB) emergent time explains why QM's external t works wherever we look, as an approximation, not a fundamental resolution.**
  - Status: surviving as an effective account.
  - Why: the corrections are 1e-57 to 1e-11 (F10), consistent with every bound but untestable. Consistency requires the full theory to be anomaly-free [K-04], and different routes give different corrections [D-21].
  - Prediction: CMB low-ℓ suppression of about (H/m_P)² ≤ 1.4e-11, 1e10 below cosmic variance. This prediction is calculable but not observable.
  - Confidence: medium-high that it is correct as a limit; low that it resolves facets 2–3.
- [CONSTRAINTS-C] **A fundamental global time (unimodular 4-volume, dust frame, CMC/York or a Hořava preferred foliation) removes the frozen formalism and the multiple-choice problem at the price of extra background or matter structure.**
  - Status: strained.
  - Why:
    - Unimodular time passes the uncertainty audit (ΔΛ/Λ ~ 1e-105) and escapes Unruh–Wald (Λ unbounded). But it labels only equivalence classes of hypersurfaces and needs a hypertime (Kuchař 1991, F11), and it needs a nondynamical volume element [D-11].
    - York time turns around in closed universes with SEC violation (F2, F3).
    - Hořava needs |β| ≲ 1e-15 (F17).
    - Dust needs factor-ordering luck [D-10].
    - All of them presuppose chronology (F4).
  - Prediction: a preferred-frame signal in gravitational-wave propagation (|c_T − 1|) or in a Lorentz-violating sector for Hořava. Unimodular time predicts nothing beyond GR with Λ as an integration constant.
  - Confidence: medium.
- [CONSTRAINTS-D] **Diósi–Penrose collapse (free R0): the conflict is resolved by making QM's evolution non-unitary at the scale where geometries differ.**
  - Status: surviving but testable.
  - Why: R0 > 0.54e-10 m kills only the parameter-free version [K-07]. Heating at the bound is 1.3e-17 K/s (F14). It needs an external time and foliation, so it does not solve facets 1–7 of canonical QG; it replaces them.
  - Prediction: a 1e-14 kg diamond in a 250 µm superposition collapses in τ = 6–12 ms (bulk E_G, independent of R0), so QGEM with about 1 s of coherence would see **no** entanglement. A successful QGEM would eliminate it.
  - Confidence: medium on the arithmetic (factor 2 in the E_G convention), low on the timescale for realization [Q-12, F-10].
- [CONSTRAINTS-E] **Fundamentally semiclassical gravity (Møller–Rosenfeld/Schrödinger–Newton), keeping QM's external time and treating geometry as classical.**
  - Status: eliminated in its simplest form.
  - Why: with standard collapse it gives superluminal signalling (Bahrami et al. 2014, F15), and the Page–Geilker experiment is inconsistent with it. It survives only by adding a collapse prescription, which turns it into D or F.
  - Prediction: Schrödinger–Newton self-gravity dynamics of mesoscopic wavepackets.
  - Confidence: medium-high.
- [CONSTRAINTS-F] **Postquantum classical gravity: time stays GR's classical time, with QM made stochastic.**
  - Status: strained.
  - Why: the delta kernel is excluded by a factor of 1e17 [K-06, F16]. Other kernels are open. It dissolves facets 1–3 by keeping gravity classical, and pays with fundamental irreversibility [K-05].
  - Prediction: a decoherence–diffusion trade-off with no gravity-mediated entanglement. Torsion-balance acceleration noise and interferometric decoherence squeeze it from both sides.
  - Confidence: medium.
- [CONSTRAINTS-G] **Realistic-clock (Gambini–Porto–Pullin) fundamental decoherence.**
  - Status: surviving but empirically idle.
  - Why: the exponent is 2.2e-27 for the Sr transition over 1 s, and a 1% effect in 1 s needs a 3.8e12 eV splitting (F12). It is empirically equivalent to A.
  - Confidence: medium.
- [CONSTRAINTS-H] **Thermal time (Connes–Rovelli): time flow is the modular flow of the state.**
  - Status: strained.
  - Why: it reproduces the measured redshift gradient via Tolman–Ehrenfest (−1.0927e-19 per mm against −9.8(2.3)e-20 per mm measured, F9). Outside KMS states the modular flow departs from the Hamiltonian flow by 1–75% (F8), so recovering mechanical time presupposes an equilibrium state for a known H [D-24].
  - Prediction: local temperature ∝ 1/√(−g_tt) in equilibrium. This is shared with standard physics.
  - Confidence: medium.
- [CONSTRAINTS-I] **Histories (Hartle generalized QM): no preferred time is needed.**
  - Status: surviving.
  - Why: no foliation is needed, so it is untouched by K7, K8 and K10. Its costs are interpretational (consistent histories) and a measure fixed by the classical limit [D-13].
  - Prediction: none that differs from A or B at accessible scales.
  - Confidence: low-medium.
- [CONSTRAINTS-N] (null) **No position satisfies every constraint while resolving all seven facets within admissible physics.**
  - Status: surviving; strongly supported by this audit.
  - Why: every consistent position leaves at least one facet open or pays a cost:
    - A: facets 2 and 4 open.
    - B: approximate only.
    - C: background structure.
    - D and F: non-unitarity or stochasticity.
    - H: needs KMS.
    - I: interpretation-dependent.
  - Only E is outright violated, and the others fail on completeness, not on consistency.
  - Prediction: no experiment within 20 years separates A, B, G, H and I (the calculated effects are ≤ 1e-11). Only D, E and F carry near-term bounds.
  - Confidence: high.
- [CONSTRAINTS-R] (reframe) **The QM-versus-GR "absolute versus relative time" framing misplaces the conflict.**
  - Status: surviving.
  - Why:
    - QM on a fixed curved background already handles relative time: the Tolman/redshift gradient −1.09e-19 per mm is measured [Q-06]. Relational clocks with gravitational coupling reproduce time dilation unitarily (H_eff = H_S/(1 − λH_S), F7). A clock in an interferometer shows proper-time which-path loss (visibility 0.99730 for 0.5 m over 1 s, F13).
    - The genuine conflict is narrower. It arises (i) for superpositions of geometries, (ii) from the Hamiltonian constraint of closed universes (asymptotically flat spacetimes keep an ADM energy), and (iii) from functional evolution, which is non-unitary between arbitrary hypersurfaces even on flat space [K-01].
  - Prediction: every test on a classical background (clock redshift, Zych visibility, Pikovski dephasing) agrees with standard QM plus GR whichever position is true. The first discriminating data would come from a superposed-geometry test (QGEM or DP collapse).
  - Confidence: high.

## What would change my mind
- **Entanglement witnessed in a QGEM-type experiment** (m ~ 1e-14 kg, Δx ~ 250 µm, ~1 s): eliminates bulk DP (D) and PQCG (F), and weakens E further.
- **Excess heating or noise at the DP-predicted level:** revives D over A–C.
- **A published independent derivation** showing the DP E_G for QGEM is much smaller than 1e-32 J (the factor-2 convention cannot do this; a different collapse functional could): moves D from testable to idle.
- **A proof that a deparametrization is clock-independent** (unitary equivalence across clocks) in an inhomogeneous model: would close facet 2 for A and C.
- **A demonstration that CMC foliations exist and stay monotonic in realistic closed Λ cosmologies** by a non-homogeneous slicing: my F3 turning point is for homogeneous slices only.
- **A stability failure** in Hořava or PQCG, or a signalling result for DP: would move C or D from strained to violated.

## Assumptions I relied on
- Dossier items D-01 to D-24, K-01 to K-09, Q-01 to Q-27 as stated. The DP heating number in Q-04 is flagged as inconsistent with its own formula (F14).
- Geometric units G = c = 1 in the minisuperspace and Gödel calculations, with an arbitrary length scale L. SI elsewhere, with CODATA values from the toolkit.
- The FRW + scalar models stand in for "generic matter". Turning-point counts depend on initial data, but the existence of turning points in (ii) and (iii) is generic for a massive scalar.
- Closed-ΛCDM parameters (Ω_m = 0.315, H0 = 67.4 km/s/Mpc) are illustrative. Whether k = +1 is not settled by anything in the dossier.
- The unimodular uncertainty relation is my derivation from the action normalization. The DP E_G uses a homogeneous-sphere estimate with a factor-2 convention ambiguity. The Pikovski molecule and QGEM-vertical inputs are assumed, not sourced.
- The page_wootters toolkit (promoted from this run, self-tested [U-01]) is taken as correct. No math check (`math/constraints.md`) exists yet for any of the above.
