# Analysis: dialectician (resolve real contradictions)

## Method applied
Pick the three contradictions in the dossier that carry the most weight; state thesis and antithesis with evidence; find the regime or definition in which both hold (or show which yields); derive from each synthesis a prediction neither side made alone; test the syntheses in the finite-dimensional Page–Wootters toolkit where possible.

## Findings

1. **Kuchař's naive two-time probability is exactly zero at distinct lattice times, and it is also "frozen" off the lattice.** In a d = 8 ideal clock with a resonant qubit (H_S = σx/2, Ω = 1 rad/s, ħ = 1), the naive P(b = 1 at t2 | a = 0 at t1) = 0 at every distinct lattice pair (step 0.785 s). Off the lattice, the naive total Σ_b P equals the clock self-overlap |⟨t1|t2⟩|²/d² to all printed digits (e.g. τ = 0.2 s: 0.8067477 both), and the normalised system part is exactly 0 for a spin flip. So the naive formula gives (clock resolution kernel) × (no system evolution). The textbook P(1|0) would be 0.00997 at τ = 0.2 s and 0.366 at τ = 1.3 s. This supports the objection side of [D-19]/[K-03] in its own terms. [calc: runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-dialectician_two_time.py]
2. **The record (Giovannetti–Lloyd–Maccone memory) version reproduces the textbook propagator exactly.** The same model with a memory written at t1 gives P(1|0) = 0.146447, 0.500000 and 1.000000 at τ = 1, 2 and 4 lattice steps, identical to |⟨1|U(τ)|0⟩|². This supports the reply side of [D-19] (HSL's criticism (3) resolved) and matches the Moreva 2017 demonstration [D-08]. [calc: same file]
3. **Uncoupled relational evolution is exactly unitary for a sharp clock reading, and conditioning on a Gaussian-blurred reading dephases in the system energy basis exactly as exp(−σ²Δ²/2).** For d = 64, Δ = 3 rad/s: at σ = 0.2 s, |ρ01| = 0.417635 against 0.417635 predicted; at σ = 0.8 s, 0.028067 against 0.028067. The sharp conditional fidelities are 1.000000000. This confirms the U-01 statement [U-01] in an independent script. [calc: runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-dialectician_clock_dephasing.py]
4. **The Gambini–Porto–Pullin decoherence exponent is algebraically identical to Gaussian clock-reading dephasing with σ(T) = √3·δT_GPP(T).** Here δT_GPP = t_P (T/t_P)^(1/3) is their own clock-accuracy bound. With GPP's exponent (3/2) t_P^(4/3) T^(2/3) ω12² [Q-15] and δT [Q-14], σ²ω12²/2 = (3/2) t_P^(4/3) T^(2/3) ω12² identically. Numerically, at ω12 = 2π × 429 THz, T = 1 s: δT = 1.427e-29 s and exponent 2.219e-27 by both routes; T = 13.8 Gyr: 1.275e-15 by both routes. This is an identity, not independent evidence. It shows that GPP's "fundamental decoherence" and HSL's "exact unitarity" are the same relational dynamics seen through a sharp versus a bounded-accuracy clock [D-20], [K-08]. [calc: same file]
5. **The rival decoherence mechanisms scale differently with time.** The log-log slope of the decoherence exponent against elapsed time is 2/3 for GPP realistic clocks, 2 for Pikovski time-dilation decoherence (Gaussian in t/τ_dec [Q-07]), and 1 for any Markovian (Lindblad) collapse or classical-gravity diffusion ([K-05], [F-06]). The GPP exponent also scales as ω12² (it quadruples when the splitting doubles). [calc: same file]
6. **The premise "relativistic QFT accepts any Cauchy foliation" (brief, Tomonaga–Schwinger) conflicts with Torre–Varadarajan [K-01].** Agullo & Ashtekar show that the conflict dissolves in a generalized sense. [new: Agullo & Ashtekar 2015, arXiv:1503.03407, PRD 91 124010, abstract (fetch_text), "on time dependent space-times ---including the simplest cosmological models--- dynamics of quantum fields is not unitary in the standard sense. This issue is first explained with an explicit example and it is then shown that a generalized notion of unitarity does hold. The generalized notion allows one to correctly pass to the Schrödinger picture starting from the Heisenberg picture used in the textbook treatments."] Torre–Varadarajan themselves found the 1+1 case unitary. [new: Torre & Varadarajan 1998, PRD 58 064007, abstract (lit_search), "dynamical evolution along arbitrary spacelike foliations is unitarily implemented on the same Fock space as that associated with inertial foliations. It follows that the Schrodinger picture exists for arbitrary foliations as a unitary image of the Heisenber…"]

7. **Recorded two-time correlations lose their Leggett–Garg violation when the clock reading is blurred, at a sharp threshold.** For a qubit precessing at Ω with equally spaced readings, K3 = e^(−Ω²σ²)(2cos Ωτ − cos 2Ωτ), where each clock reading has an independent Gaussian error σ. So K3,max = 1.5 e^(−Ω²σ²), and the violation (K3 > 1) disappears at Ωσ = √(ln 1.5) = 0.637 (dimensionless). A Monte Carlo over clock errors agrees to within 3e-4 (Ωσ = 0.4: 1.2782 exact, 1.2784 MC). For an optical qubit (Ω = 2π × 429 THz) read by a clock at the GPP accuracy after T = 1 s, Ωσ = 3.8e-14, far below threshold. [calc: runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-dialectician_lg_resolution.py]
8. **Dirac quantization with embedding-dependent Fock spaces evades the Torre–Varadarajan obstruction in parametrized field theory, including in higher dimensions but only for finite gauge transformations.** [new: Varadarajan 2007, arXiv:gr-qc/0607068, PRD 75 044018, abstract (fetch_text), "We construct a Dirac quantization of PFT,unitarily equivalent to the standard Fock quantization, using techniques from Loop Quantum Gravity (LQG) which are powerful enough to super-cede the no- go implications of the TV results. The key features of our quantization include an LQG type representation for the embedding variables, embedding dependent Fock spaces for the scalar field, an anomaly free representation of (a generalization of) the finite transformations generated by the constraints and group averaging techniques. The difference between 2 and higher dimensions is that in the latter, only finite gauge transformations are defined in ..."] The same abstract states that the formal functional Schrödinger picture is equivalent to Fock quantization only "if scalar field evolution along arbitrary foliations is unitarily implemented on the Fock space", which TV showed fails for d > 2. The obstruction therefore sits in the infinitesimal functional Schrödinger (Tomonaga–Schwinger) equation on a single Hilbert space, not in foliation independence as such.
9. **A gravitationally coupled Page–Wootters clock stays unitary; only coarse-graining or tracing makes it decohere.** Smith–Ahmadi's exactly solvable Newtonian clock–system coupling gives H_eff = H_S(1 − λH_S)^(-1), a Hermitian (unitary) redshifted generator. At 1 mm with E = ħ·2π × 429 THz, λ = 8.714e-76 s and the fractional correction λE = 2.35e-60 (dimensionless). A generic non-gravitational coupling (0.2 X_C ⊗ σz, d = 6) gives a non-Hermitian effective generator of about 1e-3 rad/s. So the U-01 taxonomy [U-01] sorts the mechanisms: GPP is readability, Pikovski is coupling plus a trace over internal clock degrees of freedom, and Smith–Ahmadi is coupling with unitary time dilation. [calc: toolkit `page_wootters.py gravity --energy "2*pi*429 THz" --distance "1 mm"` and `interact --d 6 --g 0.2`, run in this session; output quoted from terminal]

## Lens-specific outputs

### Contradiction I: does time flow in a timeless (constraint-satisfying) state? (facet 1; [D-19], [K-03])
- **Thesis (Kuchař).** Conditional probabilities computed on a physical state Ψ with JΨ = 0 cannot produce flow: the two-time probability built from clock projectors on Ψ vanishes unless T′ = T″ [K-03], [D-19]. Finding 1 confirms this exactly, and more strongly than stated: off the lattice the naive quantity is the clock self-overlap times *no* system evolution.
- **Antithesis (Page–Wootters, HSL, GLM).** Relational conditional probabilities reproduce the textbook propagator "without approximations" [D-19], [D-06]. Relativistic sectors add per-sector validity [D-07], and a photonic experiment shows the correct two-time correlations [D-08]. Finding 2 reproduces the propagator exactly.
- **Where both hold.** They compute different quantities.
  - Kuchař's expression is the joint probability that a single timeless state shows clock reading t1 *and* t2 with no physical record in between. For an ideal clock that is correctly zero, and for a finite clock it is the clock's resolution kernel (Finding 1).
  - The HSL/GLM expression conditions on a *record*: a memory subsystem whose coupling is inside the constraint. It yields |⟨b|U(t2 − t1)|a⟩|² (Finding 2).
  - Kuchař's valid residue is that a measurement cannot be modelled as a projector applied to the physical state; it must be a constraint-respecting interaction. HSL's criticism (2) says the same from the other side [D-19].
  - What yields: the claim "Page–Wootters cannot give multi-time statistics", and the idea that flow is a property of the global state rather than of recorded correlations.
- **Prediction neither side made alone.** Flow is carried by records, and its visibility is bounded by the clock's resolution. The Leggett–Garg violation of relational two-time correlations falls as K3,max = 1.5 e^(−Ω²σ²) and vanishes at Ωσ = 0.637 (Finding 7). The record-free (naive) two-time statistic is not meaningless: it measures the clock overlap |⟨t1|t2⟩|²/d². Both can be tested in a Moreva-type photonic setup by injecting calibrated clock-reading noise [D-08].
- **Scope limit.** Nothing here is gravitational. It establishes internal consistency and empirical equivalence of relational QM with standard QM for ideal clocks. It does not touch facets 2, 4 or 7.

### Contradiction II: exact relational unitarity vs fundamental decoherence from realistic clocks (facets 3–4; [D-20], with [D-03], [D-21])
- **Thesis (HSL).** For ideal or covariant-POVM clocks that do not interact with the system, relational evolution is exactly unitary [D-06], [K-09].
- **Antithesis (Gambini–Porto–Pullin).** With realistic clocks, "quantum mechanics ceases to be unitary and a fundamental mechanism of decoherence of quantum states arises" [D-20], with exponent (3/2) t_P^(4/3) T^(2/3) ω12² [Q-15].
- **Where both hold.** Unitarity is a property relative to the clock variable one conditions on.
  - With a sharp reading of a covariant clock the evolution is unitary (Finding 3: fidelity 1.000000000).
  - Conditioning on a reading with Gaussian error σ gives exactly exp(−σ²Δ²/2) dephasing in the system energy basis (Finding 3).
  - GPP's exponent is identically this dephasing with σ = √3·δT_GPP(T) (Finding 4). So the two papers describe one dynamics seen through two clocks.
  - The dispute relocates entirely to [K-08]: is there a *fundamental* lower bound δT ≥ t_P^(2/3) T^(1/3) on every clock? That bound comes from a heuristic black-hole gedanken clock, not a theorem. "Fundamental decoherence" is therefore only as strong as K-08.
- **Extension (same structure, [D-03] vs [D-09]/[D-21]).**
  - Different clocks give "different and inequivalent notions of unitarity" [D-03].
  - Yet all semiclassical routes give the same Schrödinger equation at leading order, with different O(1/M) corrections [D-21].
  - Both hold. Clock choices agree where each clock is monotonic and semiclassical, and disagree at O(1/M) and near clock turning points or singularities. In D-03 the scalar-field clock gives recollapse and the fluid clock resolves the singularity.
  - So the multiple-choice facet (2) is the global-time facet (4) seen from the other side. It is not a separate contradiction that a synthesis can remove.
- **Predictions neither side made alone.**
  - (a) Any decoherence that comes from clock limitations has an exponent scaling as T^(2/3)·ω12². Markovian collapse and classical-gravity diffusion scale as T^1, and Pikovski time-dilation decoherence as T² (Finding 5). The time-scaling exponent identifies the mechanism.
  - (b) Clock-limitation decoherence is conditional. It disappears for an observer who conditions on a more accurate clock, so to count as fundamental it must be shown to be clock-independent. That is a checkable theoretical criterion for GPP.
  - (c) At lab scale the GPP exponent is 2.2e-27 at T = 1 s (Finding 4), so HSL and GPP are empirically equivalent now.
  - (d) Quantum-gravity corrections to the Schrödinger equation are observables only in their clock-invariant part. A CMB claim such as [Q-19] has to name its clock before its sign can be compared.

### Contradiction III: does QFT already reconcile relativistic time? (hidden premise 1 vs facet 5; [K-01], [K-04])
- **Thesis (the reframe premise).** Relativistic QFT and QFTCS already give up absolute time: any inertial frame or Cauchy foliation (Tomonaga–Schwinger) works, so the conflict is confined to dynamical or quantum geometry (brief, premise 1).
- **Antithesis (Torre–Varadarajan).** Even on flat spacetime with d > 2, evolution from a flat to a generic Cauchy surface "cannot, in general, be unitarily implemented on the Fock space" [K-01]. Giulini–Kiefer find that integrability "prevent[s] the existence of Tomonaga-Schwinger time functions on the space of three-metrics" [K-04]. Facet 5 thus exists without quantum gravity.
- **Where both hold.** The thesis is true in the Heisenberg or algebraic picture; the antithesis is true of the Schrödinger picture on a single Fock space.
  - Dynamics as an automorphism of the field algebra is foliation-independent.
  - Unitary implementability on one Fock space fails. Agullo–Ashtekar show that "a generalized notion of unitarity does hold", and that it recovers the Schrödinger picture from the Heisenberg one (Finding 6).
  - Varadarajan's Dirac quantization, with embedding-dependent Fock spaces and finite gauge transformations, "super-cede[s] the no-go implications of the TV results" (Finding 8).
  - What yields: the demand that functional (many-fingered) evolution be an infinitesimal unitary Schrödinger flow on one Hilbert space. Neither side's core claim yields.
- **Predictions neither side made alone.**
  - (a) Proposals that fix a *field* clock with local, many-fingered time and write an infinitesimal functional Schrödinger equation on one matter Hilbert space should meet a Torre–Varadarajan-type UV obstruction in their matter sector unless they adopt surface-dependent representations. This covers Brown–Kuchař dust [D-10] and local semiclassical Tomonaga–Schwinger time [K-04].
  - (b) Proposals with a single global clock parameter avoid it by construction: unimodular 4-volume time [D-11], a homogeneous scalar or fluid clock [D-03], and one Page–Wootters clock [D-06].
  - (c) The part of the problem of time that is new to gravity is therefore not "absolute vs relative time" and not foliation dependence. It is superposition of the geometry itself (proper times in superposition). The experiments that probe that are the Zych proper-time visibility witness and gravity-mediated entanglement [F-09], [D-23], not clock redshift on a classical background [D-14].
- **Caveat.** Prediction (a) is an inference by analogy. I found no paper applying Torre–Varadarajan to dust-clock quantizations.

### Synthesis table
| # | Thesis | Antithesis | Regime where both hold | What yields | New prediction |
|---|---|---|---|---|---|
| I | Naive two-time P = 0: no flow (Kuchař) | Relational P gives textbook propagator (HSL, GLM, Moreva) | Different quantities: record-free joint projection vs record-conditioned probability | "PW cannot do multi-time"; flow as a property of the global state | LG violation ∝ e^(−Ω²σ²), lost at Ωσ = 0.637; naive statistic = clock overlap kernel |
| II | Exact relational unitarity (HSL) | Fundamental decoherence (GPP) | Unitarity is relative to the clock variable: sharp → unitary, bounded-accuracy → dephasing, GPP ≡ σ = √3 δT | "Fundamental" unless K-08 is a theorem | Exponent ∝ T^(2/3) ω² (vs T¹ collapse, T² Pikovski); clock-invariant part alone is observable |
| III | QFT already relativizes time | TV: no unitary evolution between generic surfaces, even in flat space | Algebraic/generalized unitarity vs single-Fock Schrödinger picture | Infinitesimal functional Schrödinger evolution on one Hilbert space | Local field clocks meet UV obstruction; single global clocks evade it; the gravity-specific residue is superposed geometry |

### Facet map from the syntheses
| Facet | Status after syntheses I–III |
|---|---|
| 1 frozen formalism | Dissolved for ideal and covariant clocks (I). Flow = record-conditioned correlation |
| 2 multiple choice | Not dissolved. Located where clocks cease to be monotonic or semiclassical (II ext.) |
| 3 Hilbert space | Sector-wise for KG-type clocks [D-07]. Not addressed further here |
| 4 global time | Open. Tied to facet 2 (II ext.) |
| 5 functional evolution | Dissolved as a gravity-specific problem (III). A generalized-unitarity reformulation exists for free fields |
| 6 observables | Relational Dirac observables for clock–system splits [D-06]. Open for full GR |
| 7 spacetime reconstruction | Not touched by any synthesis. Open |

## Calculations
- `runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-dialectician_two_time.py`: Kuchař's naive two-time probability against the GLM memory construction and the textbook propagator. Model: d = 8 equally spaced clock (1 rad/s spacing) and a qubit with Ω = 1 rad/s, ħ = 1. Results:
  - Naive P(1|0) = 0 at all distinct lattice times.
  - GLM = textbook = 0.146447, 0.500000 and 1.000000 at τ = 0.785, 1.571 and 3.142 s.
  - Off the lattice, naive total = |⟨t1|t2⟩|²/d² (e.g. 0.8067477 at τ = 0.2 s) and naive normalised P(1|0) = 0.
- `runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-dialectician_clock_dephasing.py`:
  - (A) Gaussian clock-reading dephasing in a d = 64 Page–Wootters state (Δ = 3 rad/s): |ρ01| = 0.5 exp(−σ²Δ²/2) to 6 digits for σ = 0.05–0.8 s.
  - (B) GPP exponent = σ²ω²/2 with σ = √3 δT_GPP. Ratio 1.000000 at T = 1 s, 1 yr and 13.8 Gyr; δT = 1.427e-29 s at 1 s; exponent 2.219e-27 at 1 s and 1.275e-15 at 13.8 Gyr for ω12 = 2π × 429 THz (SI).
  - (C) Log-log time slopes of the decoherence exponent: 0.6667 (GPP), 2.0000 (Pikovski), 1.0000 (Markovian).
- `runs/2026-09-29-problem-of-time-quantum-gravity/calc/lens-dialectician_lg_resolution.py`: Leggett–Garg K3 against the clock-reading error, exact against Monte Carlo (2e5 samples). K3,max = 1.5 e^(−Ω²σ²); threshold Ωσ = 0.6368 (dimensionless); GPP-accuracy clock at 1 s gives Ωσ = 3.8e-14 for an optical qubit.
- Toolkit runs (not saved as scripts): `page_wootters.py gravity` (λ = 8.714e-76 s, λE = 2.35e-60 at 1 mm) and `page_wootters.py interact --d 6 --g 0.2` (non-Hermiticity of the effective generator up to 1.1e-3 rad/s).

## Candidate answers (at least 3; the null and a reframe count)
Header: not mutually exclusive. A, B and C are complementary syntheses on different facets; D and E are the null and a modification.

- [DIALECTICIAN-A] **Relational time resolves the frozen formalism (facet 1), and Kuchař's two-time objection and its rebuttal are both correct about different quantities.** Time's flow is the record-conditioned correlation between a clock subsystem and memories inside the constraint; the record-free joint projection correctly shows no flow. It gives up: flow as a property of the global state, and a fundamental external time.
  - Status: **surviving.**
  - Why: exact in the toy model (Findings 1–2), and consistent with HSL [D-06], [D-19], the relativistic per-sector extension [D-07] and the photonic demonstration [D-08].
  - From synthesis I.
  - Prediction/test: relational two-time correlations lose their Leggett–Garg violation as K3,max = 1.5 e^(−Ω²σ²), vanishing at Ωσ = 0.637. The record-free statistic reproduces the clock overlap kernel. Both can be tested in a Moreva-type photonic experiment with calibrated clock noise. This is empirically equivalent to standard QM for ideal clocks.
  - Confidence: medium. The one independent assessment of HSL is missing [D-19], and interacting clocks lie outside the theorem [K-09].
- [DIALECTICIAN-B] **"Exact relational unitarity" (HSL) and "fundamental clock decoherence" (Gambini–Porto–Pullin) are one dynamics seen through a sharp versus a bounded-accuracy clock.** Unitarity, like the choice of time, is clock-relative. The same structure explains why different clocks give inequivalent unitary theories [D-03] and different O(1/M) semiclassical corrections [D-21]: clocks agree where they are monotonic and semiclassical and disagree near turning points.
  - Status: **surviving** as a synthesis. The *fundamental* (QM-modifying) reading of GPP is **strained**, because it rests wholly on the heuristic clock-accuracy bound [K-08].
  - From synthesis II.
  - Prediction/test:
    - Clock-limited decoherence scales as T^(2/3) ω12², against T¹ for Markovian collapse or classical-gravity diffusion and T² for Pikovski time-dilation decoherence.
    - Its size is 2.2e-27 at T = 1 s for an optical transition, so it is unobservable now.
    - The theoretical test is whether any clock-independent residue survives conditioning on a better clock.
    - Semiclassical quantum-gravity corrections (e.g. CMB [Q-19]) are observable only in their clock-invariant part.
  - Confidence: medium. The identity is exact; its interpretation depends on K-08.
- [DIALECTICIAN-C] **Reframe: the question misplaces the conflict.** "Absolute vs relative time" is already solved by relativistic QFT and QFTCS. Foliation dependence (facet 5) is not specific to gravity: Torre–Varadarajan non-unitarity already occurs in flat spacetime, and it is resolved by generalized or algebraic unitarity [K-01], (Findings 6, 8). What is new to quantum gravity is (i) a superposed geometry, meaning proper times in superposition, and (ii) the clock non-uniqueness of facets 2 and 4 in a closed universe. It gives up: the demand for an infinitesimal unitary Schrödinger flow on one Hilbert space for arbitrary hypersurfaces.
  - Status: **surviving.**
  - From synthesis III.
  - Prediction/test:
    - Field-clock (many-fingered) deparametrizations such as Brown–Kuchař dust [D-10] should meet a TV-type UV obstruction unless they use surface-dependent representations. Single-global-clock schemes (unimodular [D-11], homogeneous clocks [D-03], one PW clock) evade it.
    - The empirically decisive experiments are proper time in superposition and gravity-mediated entanglement [F-09], [D-23], not redshift on a classical background [D-14].
  - Confidence: medium-high for the reframe, low for prediction (a), which is an analogy not found in the literature.
- [DIALECTICIAN-D] **Null: no position resolves the problem of time within admissible physics.**
  - Status: **strained** in its strong form ("every facet is unresolved or every position pays an unacceptable cost"): syntheses I and III dissolve facets 1 and 5 at no cost beyond giving up global flow and single-Hilbert-space functional evolution. **Surviving** in a weak form: facets 2 and 4 (multiple choice, global time) have no synthesis, because they are a genuine non-uniqueness rather than a contradiction between two claims [D-03], [D-21]; facet 7 (spacetime reconstruction) has no source and no synthesis. This is Kuchař's verdict [D-04], narrowed to those facets.
  - Prediction/test: any proposed resolution must produce a clock-invariant prediction that differs between the scalar-field and fluid clocks of the D-03 model (recollapse against singularity resolution). If none can be constructed, the weak null stands.
  - Confidence: medium.
- [DIALECTICIAN-E] **Modify QM so that time stays external: gravity-related collapse (Diósi–Penrose), classical or postquantum gravity, or GPP as fundamental.**
  - Status: **strained.**
  - Why:
    - Synthesis III removes the foliation problem as a motive for keeping an external time.
    - Synthesis II shows that GPP's non-unitarity is a clock artefact unless K-08 is fundamental.
    - DP survives only with a free R0 > 0.54e-10 m [K-07], and the delta-kernel postquantum model is excluded [K-06].
    - Not eliminated, since the free-R0 DP and finite-range classical-gravity kernels survive.
  - From synthesis II (scaling) and III (motive).
  - Prediction/test: the decoherence exponent scales linearly in time (Markovian) and there is no gravity-mediated entanglement (for classical gravity [F-05]). Both are distinguishable from B's T^(2/3) and from Pikovski's T².
  - Confidence: medium.

## What would change my mind
- An independent analysis showing that HSL's two-time conditional probabilities fail gauge invariance for interacting or non-covariant clocks. The unconfirmed HSL sentence in [D-19] would then weaken A.
- A derivation of the GPP clock-accuracy bound [K-08] as a theorem of a definite theory, independent of which clock is used. That would turn B's "strained fundamental reading" into "surviving", and E would gain.
- A paper showing that Brown–Kuchař dust or other field-clock quantizations are free of TV-type obstructions on a single Fock space, which would falsify C's prediction (a). Or one showing that single-global-clock schemes fail for an analogous reason.
- A clock-invariant, observable difference between clock choices in a minisuperspace model, which would weaken the weak null D and sharpen B.

## Assumptions I relied on
- The finite-dimensional Page–Wootters model ([U-01], toolkit `page_wootters.py`) represents the logical structure of Kuchař's objection. Real quantum gravity has continuous, unbounded-spectrum and possibly non-separable constraints.
- GPP's decoherence is modelled as Gaussian clock-reading error. The identity in Finding 4 holds for their published exponent, but I did not open their derivation to confirm that they model it the same way.
- The Pikovski T² and Markovian T¹ scalings are taken from their functional forms ([Q-07], Lindblad structure of [K-05]). Non-Markovian collapse variants would change the T¹ slope.
- Agullo–Ashtekar and Varadarajan are read from abstracts only. The higher-dimensional PFT result covers finite gauge transformations, as the abstract says, and was not checked for interacting fields.
- No `math/` check of this lens existed when I wrote it. All numbers come from this lens's scripts or the toolkit.
