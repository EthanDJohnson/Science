# Dossier: The problem of time: reconciling quantum-mechanical and general-relativistic time

Compiled from `research/theory.md`, `research/quantitative.md`, `research/critiques.md` and `research/engineering.md`, with their `.check.md` files. Every facet was source-checked. No `math/` checks existed when this was compiled, so no finding here has been re-derived independently apart from the source checker re-running the calc scripts.

Units: SI unless a row says otherwise. Where a source uses natural units (hbar = c = 1) or Planck-mass GeV conventions, the row says so. Dimensionless ratios are marked "(dimensionless)".

Labels: **[peer-reviewed]**, **[review]** (textbook or review), **[preprint]**, **[calc]** (this run's own script output, re-run by the checker), **[search-summary]** (rests only on a search-engine summary, so it is not a quote). The label **(unchecked-part)** marks the part of a claim that the checker could not confirm.

---

## 1. Established

- [D-01] **Frozen formalism (facet 1).** In canonical GR for a spatially closed universe, every observable commutes with the constraints, so it is a constant of motion along the foliation for any choice of lapse N and shift N^i. In the Dirac-quantized theory the state is annihilated by the Hamiltonian constraint and physical matrix elements do not depend on time. Isham: this "seems to imply that nothing happens in a quantum theory of gravity". The frozen formalism is established as a property of Dirac quantization of closed-universe GR. Whether it is a defect or a feature depends on the position taken. (refs: RT-01) [review, full-text, verified]
- [D-02] **Multiple-choice and Hilbert-space problems (facets 2, 3).** Isham: "Generically, there is no geometrically natural choice for the internal spacetime coordinates and, classically, all have an equal standing", and at the quantum level "there is no reason to suppose that the theories corresponding to" different choices are equivalent. On Rovelli's evolving-constants scheme, Isham says it "seems most unlikely that a single Hilbert space can be used for all possible choices of an internal time function T", but calls these difficulties "no worse than those that arise in any of the other approaches". (refs: RT-02, RC-04) [review, full-text, verified]
- [D-03] **Clock dependence exhibited in a model (facet 2).** In a flat FLRW minisuperspace model with a massless scalar and a perfect fluid, quantized relationally, the paper compares three clocks: fluid time, volume time and the scalar field. Demanding unitarity in fluid time gives a boundary condition at the singularity and generic singularity resolution. In volume time, semiclassical states follow the classical singular trajectories. With the scalar field as clock, the boundary condition sits at infinity, and the universe undergoes a "quantum recollapse ... at large volume". The authors: "When different notions of time exist, there will be corresponding different and inequivalent notions of unitarity"; "Dirac quantisation would not resolve the issue." Scope: one model; not a general theorem. (refs: RT-10 [clock names corrected per check], RC-05) [peer-reviewed, full-text, verified]
- [D-04] **Kuchař's survey verdict.** Kuchař's review "critically examine[s] ten major attempts to circumvent this problem and discuss[es] their shortcomings". As quoted by Dolby, Kuchař concluded: "none of us has so far succeeded in proposing an interpretation of quantum gravity that would either solve or circumvent the problems of time". Bibliographic note from the check: INSPIRE lists it as a 1991-05 conference paper, and the IJMPD 20 (2011) 3 reprint was not seen independently. (refs: RT-03, RC-02) [peer-reviewed/conference review, abstract; verdict quote via Dolby preprint, full-text]
- [D-05] **Page–Wootters mechanism.** Page and Wootters argue that because the Schrödinger time parameter is unobservable, energy obeys a superselection rule, so observables are stationary and a closed system such as the Universe may be taken to be in a stationary state. Observed dynamics is then "described entirely in terms of stationary observables as a dependence upon internal clock readings". The researcher's gloss that non-ideal clocks give only approximately unitary evolution is not in the abstract (check note). (refs: RT-11) [peer-reviewed, abstract, verified]
- [D-06] **Trinity theorem (relational dynamics).** Höhn, Smith and Lock prove that three approaches are "three faces of the same dynamics" for a Dirac-quantized system with a clock that is "well-behaved" and "does not couple to the evolving degrees of freedom": (1) relational Dirac observables in the clock-neutral picture; (2) the Page–Wootters relational Schrödinger picture; (3) the relational Heisenberg picture obtained by quantum deparametrization. The proof covers group-covariant clock POVMs with a constraint linear in the clock Hamiltonian. It is a mathematical equivalence, not a resolution of the interacting-clock case. (refs: RT-04, RC-07) [peer-reviewed, full-text, verified]
- [D-07] **Trinity in relativistic settings.** For constraints quadratic in the clock momentum (Klein–Gordon type), "this 'trinity' of relational quantum dynamics holds in relativistic settings per frequency superselection sector". The abstract also says Kuchař's criticism is resolved in that setting. The researcher's inference that global-time and inner-product issues therefore survive sector by sector is not in the abstract. (refs: RT-06, RC-09) [peer-reviewed, abstract, verified]
- [D-08] **Laboratory illustrations of Page–Wootters.**
  - Moreva et al. 2014: two polarization-entangled photons (702 nm filters, FWHM 1 nm). One photon is the clock, its polarization rotated in birefringent quartz. An "internal" observer correlated with the clock sees the other photon evolve, while an "external" observer measuring global properties "can prove it is static". This is a d = 2 clock with no gravity and no dynamical constraint. (refs: RQ-10, RE-02) [peer-reviewed, full-text, verified]
  - Moreva et al. 2017 (arXiv:1710.00707): a single photon's position serves as a continuous clock. Two-time correlations seen by the internal observer violate a Leggett–Garg inequality. The authors state that the paper's main result is "to experimentally prove that the mechanism can indeed provide [the correct two-time correlations]". Scope: an ideal, non-interacting clock. (refs: RE-10) [preprint, full-text, verified]
- [D-09] **Semiclassical (Born–Oppenheimer/WKB) time from Wheeler–DeWitt.** Expanding the full functional Wheeler–DeWitt equation in powers of G yields a Schrödinger equation for matter on a classical background, plus two classes of corrections: (i) breakdown of the classical-background picture, and (ii) quantum-gravitational corrections to the matter fields. Class (ii) is independent of the factor ordering of the gravitational kinetic term. In the adiabatic case the only surviving correction contains the square of the matter Hamiltonian. "In the general case there are also smaller terms which describe a gravitationally induced violation of unitarity. The corrections are numerically extremely tiny except near the big bang and the final stages of a black hole." Time here is emergent and approximate. The expansion is definite within Wheeler–DeWitt theory, which is itself unproven. (refs: RT-12, RC-10; RC-10 was marked unverifiable because the abstract was not re-fetched, but the RT-12 check confirmed the same abstract, including the unitarity-violation sentence) [peer-reviewed, abstract]
- [D-10] **Brown–Kuchař dust clock.** Coupling GR to incoherent dust "introduces into spacetime a privileged dynamical reference frame and time foliation". Dust proper time and comoving coordinates become canonical variables. The Hamiltonian constraint can be solved for the momentum conjugate to dust time, which gives a functional Schrödinger equation. Caveat: "Due to factor-ordering ambiguities, the quantum theories constructed from H↑(x) and H↑0(x) do not necessarily coincide." Correction from the check: the paper presents this as a "satisfactory phenomenological approach". It calls a commuting factor ordering an "overwhelming if" and leaves vacuum problems unresolved. The researcher's "solves facets 1 and 3" overstates it. (refs: RT-14) [peer-reviewed, full-text, verified with correction]
- [D-11] **Unimodular time (Unruh 1989).**
  - Λ becomes an integration constant, and the Hamiltonian constraint is replaced by a secondary constraint. The quantum version "has a normal 'Schrödinger' form of time development, and the wave function does not obey the usual 'Wheeler-DeWitt' equation".
  - Unruh names the key weakness: "one must introduce a nondynamic background spacetime volume element".
  - Classically the theory is GR with Λ as an integration constant. As quantum gravity it is speculative (see F-01).
  - (refs: RT-09, RT-15) [peer-reviewed, abstract, verified]
- [D-12] **Thermal-time hypothesis, stated.** Connes and Rovelli propose that "in a generally covariant quantum theory the physical time-flow is not a universal property of the mechanical theory, but rather it is determined by the thermodynamical state". The time flow is the Tomita–Takesaki modular group of the state on the von Neumann observable algebra. For a non-covariant system in a Gibbs state "this postulate reduces to the Hamiltonian equations". The Tomita–Takesaki theorem is a theorem; the physical identification is a hypothesis. (refs: RT-07) [peer-reviewed, full-text, verified]
- [D-13] **Histories formulation (Hartle).** Generalized sum-over-histories quantum mechanics for closed systems needs no preferred time. Hamiltonian quantum mechanics is "an approximation ... appropriate for those epochs and those scales when the universe ... does exhibit a classical spacetime geometry". "For closed cosmological spacetimes there is no preferred notion of time, therefore no preferred notion of energy, therefore no covariant notion of Hamiltonian". The approach depends on a consistent-histories interpretation. (refs: RT-16; the first quote was not separately grepped by the checker) [review, full-text, verified]
- [D-14] **Gravitational redshift resolved across 1 mm (fixed classical background).** JILA's Sr lattice clock uses about 1e5 87Sr atoms at about 100 nK.
  - Synchronous two-region comparison: fractional frequency uncertainty 7.6e-21 (dimensionless) after 92 h, with instability 4.4e-18/sqrt(tau) (tau in s).
  - Measured gradient: -9.8(2.3)e-20 per mm, against a predicted -1.09e-19 per mm; -1.28(27)e-19 per mm after systematics.
  - This tests GR time dilation on a classical background, not a superposition of proper times.
  - (refs: RQ-03, RE-01) [peer-reviewed, full-text, verified]
- [D-15] **Table-top gravity from small sources.**
  - Westphal et al. 2021 measured gravitational coupling between 1 mm-radius gold spheres (source 92.1 mg, test 90.7 mg, 40 mm separation, torsion pendulum).
  - Fuchs et al. 2024 measured the gravity of a 2.4 kg source on a levitated sub-milligram test mass: coupling 10–30 aN, force noise 0.5 fN/sqrt(Hz).
  - Check correction: Westphal's sources are about 0.09 g, not "~0.1 g".
  - (refs: RE-08) [peer-reviewed, full-text, verified]
- [D-16] **Largest reported mechanical cat state (resonator).** Bild et al. 2023 prepared a mechanical resonator of effective mass 16.2 micrograms (1.62e-8 kg) in Schrödinger cat states of motion. Correction from the check: the paper gives the superposition size of that mode as 2.1e-18 m, about 1e14 times smaller than the 250 micrometre QGEM requirement. The research file said this size was "not quantified". The phrase "largest effective mass in a cat state" does not appear in the source and is unverified. (refs: RQ-13 [misattributed, corrected]) [peer-reviewed, full-text]
- [D-17] **Finite-dimensional Page–Wootters toy model (own computation).** Setup: a d-level clock with H_C = -eps diag(0..d-1) and a qubit with H_S = diag(0, omega) (hbar = 1, dimensionless), with physical states in the null space of H_C⊗1 + 1⊗H_S.
  - For omega = j·eps with integer j ≤ d-1, the conditional states reproduce exp(-i H_S t_n) with fidelity 1.000000 at every tick t_n = 2πn/(d·eps), for d = 4, 8, 16 and 32.
  - For non-integer omega/eps there is no exact physical state. The residual of the best approximate state is |eta|·eps/sqrt(2), and the minimum fidelity falls. Numbers are in Q-25 to Q-27.
  - Increasing d refines the time resolution T/d but does not fix a spectral mismatch.
  - Not tested: the Kuchař two-time objection and interacting clocks.
  - (refs: RQ-11) [calc: runs/2026-09-29-problem-of-time-quantum-gravity/calc/quantitative_pw_clock.py; re-run by checker, verified]
- [D-18] **Measurement-theory arguments for quantizing gravity are inconclusive.** Albers, Kiefer and Reginatto 2008 re-examine Eppley–Hannah/DeWitt-type arguments. The check found their abstract's verdict, "one cannot conclude from the existing gedanken experiments that gravity has to be quantized", which upgrades the research file, where the verdict was listed as unknown. (refs: RC-14, critiques.check) [peer-reviewed, abstract]

## 2. Quantitative anchors

| ID | Quantity | Value (units) | Conditions | Source refs | Access |
|---|---|---|---|---|---|
| Q-01 | Lower bound on the Diósi–Penrose smearing radius R0 | R0 > 0.54e-10 m (probability 0.95) | Gran Sasso underground Ge detector; spontaneous-radiation channel; photon band 10 keV to ~1e5 keV; DP model "in the present formulation" | RQ-01, RC-12, RE-05 | full-text |
| Q-02 | Penrose's parameter-free R0 for Ge | 0.05e-10 m | Debye–Waller estimate, Ge at liquid-nitrogen temperature; excluded by Q-01 (about 11x below) | RQ-01, RE-05 | full-text |
| Q-03 | Earlier DP bounds on R0 | GW detectors: R0 ≥ 40.1e-15 m; neutron stars: R0 ≳ 1e-13 m | Q-01 is "about three orders of magnitude stronger" | RE-05, RC-12 | full-text |
| Q-04 | DP heating rate at R0 ~ 1e-15 m | dT/dt = 4 sqrt(pi) m0 G hbar/(3 kB R0^3) ~ 1e-4 K/s | Non-interacting gas, m0 = nucleon mass, no dissipation; contradicted by experiment | RQ-02 | full-text |
| Q-05 | Sr clock two-region fractional frequency uncertainty | 7.6e-21 (dimensionless) | 92 h of data; instability 4.4e-18/sqrt(tau), tau in s; ~1e5 atoms, ~100 nK | RQ-03, RE-01 | full-text |
| Q-06 | Measured redshift gradient | -9.8(2.3)e-20 per mm; -1.28(27)e-19 per mm after systematics | Predicted -1.09e-19 per mm (g·Δh/c², Earth surface; also reproduced by calc/quantitative_scales.py) | RE-01, RQ-03 | full-text |
| Q-07 | Pikovski time-dilation decoherence time | tau_dec = sqrt(2/N)·hbar c²/(kB T g Δx); V(t) ~ exp[-(t/tau_dec)²] | N internal oscillators at temperature T; height separation Δx; lowest order in c^-2; no environment | RQ-04, RE-03 | full-text |
| Q-08 | Pikovski example value | tau_dec ≈ 1e-3 s (calc: 1.04e-3 s) | N ~ 1e23 (gram scale), room temperature, Δx = 1e-6 m; prediction, not observed, disputed (C-02) | RQ-04, RE-03 | full-text |
| Q-09 | QGEM (Bose et al.) test-mass parameters | m ~ 1e-14 kg (radius ~1 µm); Δx ~ 250 µm; gradient ~1e6 T/m for ~500 ms; closest approach ~200 µm; tau ~ 1 s; Casimir–Polder ~0.1 of gravity | Proposal, not realized | RQ-05, RE-04 | full-text |
| Q-10 | QGEM gravitational energy and phase spread | G m²/d = 1.5e-35 J; phase spread 0.23 rad (tau = 1 s), 0.57 rad (tau = 2.5 s) | m = 1e-14 kg, d = 450 µm, Δx = 250 µm; researcher's arithmetic | RQ-13 | calc: calc/quantitative_scales.py |
| Q-11 | Heaviest demonstrated mechanical cat state | 16.2 µg = 1.62e-8 kg effective mass; superposition size 2.1e-18 m | Resonator oscillation-phase superposition, not centre-of-mass delocalization | RQ-13 (corrected) | full-text |
| Q-12 | Heaviest matter-wave interference | > 25,000 Da (≈ 4.2e-23 kg), up to ~2000 atoms; 2 m Talbot–Lau | Gap to 1e-14 kg is about 2.4e8 (≈ 8.4 orders of magnitude), corrected from "~9" | RE-11 | search-summary |
| Q-13 | Gravity-sensing source masses | 92.1 mg source / 90.7 mg test at 40 mm; 2.4 kg source with coupling 10–30 aN and noise 0.5 fN/sqrt(Hz) | Torsion pendulum; levitated sub-mg test mass | RE-08 | full-text |
| Q-14 | Gambini–Porto–Pullin clock accuracy | δT ~ t_P (T_max/t_P)^(1/3); δT = 1.4e-29 s at T = 1 s | t_P = 5.39e-44 s; black-hole-lifetime clock argument | RQ-06 | full-text + calc/quantitative_scales.py |
| Q-15 | GPP decoherence exponent | ln(rho12(T)/rho12(0)) = -(3/2) t_P^(4/3) T^(2/3) omega12² (natural units in source) | Evaluated for omega12 = 2π × 429 THz: 2.2e-27 (T = 1 s), 2.2e-22 (1 yr), 1.3e-15 (13.8 Gyr). Authors: "too small to be observed in the lab" | RQ-06 | full-text + calc |
| Q-16 | Salecker–Wigner minimum clock mass | M ≥ hbar T/(c² δt²); T = 1 s, δt = 1e-18 s gives 1.2e-15 kg; δt = t_P gives ~4e35 kg | Formula as recalled by researcher; primary paper not opened | RQ-07 | search-summary (unverifiable) |
| Q-17 | Planck mass in Kiefer's convention | m_P = sqrt(3π hbar c/(2G)) ≈ 2.65e19 GeV | Semiclassical corrections suppressed by (E/m_P)² | RQ-08 | full-text |
| Q-18 | Semiclassical correction at LHC energy | (1.4e4/2.65e19)² ≈ 3e-31 (dimensionless) | Researcher's arithmetic on Q-17 | RQ-08 | calc/arithmetic |
| Q-19 | Inflationary Hubble bound from WDW-correction CMB estimate | H ≲ 1.4e-2 m_P ≈ 4e17 GeV; weaker than the tensor-to-scalar bound H ≲ 1e-5 m_P ~ 1e14 GeV | Kiefer–Kramer; Born–Oppenheimer ansatz; model-dependent | RQ-08 | full-text (preprint essay) |
| Q-20 | Postquantum classical gravity: upper bound on diffusion D2 | D2 ≤ 1e-41 kg² s m^-3 | Torsion-balance acceleration noise; local continuous model; Vb ~ 1e15 m³ | RQ-09 | full-text |
| Q-21 | Postquantum classical gravity: lower bound on D2 | D2 ≥ 1e-24 kg² s m^-3 | Fullerene interferometry, M_λ ~ 1e-24 kg, V_λ ~ 1e-25 m³, λ ~ 10 s^-1; delta-function kernel ("already ruled out") | RQ-09 | full-text |
| Q-22 | Moreva 2014 photon wavelength | 702 nm (FWHM 1 nm) | d = 2 polarization clock | RQ-10 | full-text |
| Q-23 | MAGIS-100 baseline | ~100 m vertical; 10 m prototypes | Proposed freely falling atom-interferometer clock | RE-07 | full-text (preprint) |
| Q-24 | PW toy model, integer omega/eps | min conditional-state fidelity 1.000000 | d = 4, 8, 16, 32; omega = j·eps, j ≤ d-1; hbar = 1 | RQ-11 | calc: calc/quantitative_pw_clock.py |
| Q-25 | PW toy model, omega/eps = 1.25 | residual 0.1768 eps; min fidelity 0.691342 (d = 4), 0.524534 (d = 32) | Best approximate constraint solution | RQ-11 | calc |
| Q-26 | PW toy model, omega/eps = 1.5 | residual 0.3536 eps; min fidelity 0.146447 (d = 4), 0.002408 (d = 32) | as above | RQ-11 | calc |
| Q-27 | PW toy model, representable range | frequency mismatch ≤ eps/2 = π/T; max frequency (d-1)·eps; resolution T/d | T = 2π/eps is the clock period | RQ-11 | calc |

## 3. Contested or conflicting

- [D-19] **Kuchař's objections to Page–Wootters and the replies.**
  - *Objection side:*
    - Kuchař's "reductio ad absurdum": the naive two-time conditional probability built from projectors on the physical state vanishes unless T′ = T″ and Q′ = Q″, so the interpretation "prohibits the time to flow" (RC-01).
    - HSL paraphrase Kuchař's three criticisms: (1) wrong for Klein–Gordon systems; (2) the conditioning violates the constraint; (3) it gives wrong propagators (RC-09, RT-20).
    - Page's own reply was that only single-instant quantities are accessible. Dolby does "not intend to defend this response" (RC-01).
  - *Reply side:*
    - Dolby 2004 [preprint] offers a refined conditional-probability interpretation that answers multi-time questions for a discrete E = 0 spectrum (RC-01).
    - HSL 2021 [peer-reviewed] state that criticism (2) "is incorrect" and resolve (3) "without approximations, ideal clocks or ancilla systems", using conditional probabilities of relational observables (RT-05, RT-20, RC-07). The relativistic follow-up addresses (1) per superselection sector (D-07).
    - Moreva 2017 [preprint] demonstrates correct two-time correlations with an ideal photonic clock (D-08).
  - *Open:*
    - HSL themselves say gauge-invariance of the two-time conditioning is "not established" by their Theorems 3–4 and is recovered through the algebra-homomorphism property. The checker could not re-find this sentence (unverifiable item within RC-07).
    - No independent (non-HSL) assessment of the resolution was found (RC-07, critiques Gaps).
  - (refs: RC-01, RC-07, RC-09, RT-05, RT-20, RE-10)
- [D-20] **Realistic clocks: exact relational unitarity vs fundamental decoherence.**
  - Gambini–Porto–Pullin: with realistic clocks, "quantum mechanics ceases to be unitary and a fundamental mechanism of decoherence of quantum states arises", fast enough, they estimate, to remove the black-hole information puzzle. They also call their black-hole model "very crude" (RT-17, check note). Their lab-scale rate is negligible (Q-15).
  - HSL: exactly unitary relational evolution for ideal or covariant-POVM clocks that do not interact with the system (D-06, RT-19).
  - These concern different clock idealizations. The research states no direct published confrontation, and the "disputed elsewhere" remark in RT-17 is unsourced.
  - (refs: RT-17, RQ-06, RT-04, RT-19)
- [D-21] **Semiclassical time is not unique.**
  - Ayala Oña, Kamenshchik et al. 2023 compare three routes to time: Kiefer–Singh; the Maniccia–Montani Kuchař–Torre reference-fluid approach; and an extended-phase-space approach with the Schrödinger equation fundamental and time from an observer's frame. Each gives at O(1/M) a temporal Schrödinger equation with quantum-gravitational corrections, "However, equations and corrections are different". The research file's "Banks-type/Brout-type" label was wrong and is corrected here per the check.
  - Non-unitarity of the corrections: Kiefer–Singh report "a gravitationally induced violation of unitarity" in the general case (D-09). Di Gioia et al. 2021 is known only by title.
  - Size and sign of the CMB effect (Q-19): later papers (Brizuela–Kiefer–Kramer; Bini et al.) reportedly dispute it; only their titles were seen.
  - (refs: RT-13 [misattributed, corrected], RT-12, RC-10, RQ-08)
- [D-22] **Is gravitational time-dilation decoherence real at the predicted size?** Pikovski et al. predict tau_dec ≈ 1e-3 s for a gram-scale body (Q-07, Q-08). Bonder, Okon and Sudarsky present "a series of arguments against the results" (Comment, Nature Phys. 12, 2 (2016)). The research file's author list was corrected per the check. The arguments were not detailed in the research. (refs: RQ-04, RE-03, RQ-15)
- [D-23] **Does gravity-mediated entanglement prove that gravity is quantum?** Bose et al. (and Marletto–Vedral, not opened) argue that an entanglement witness shows the mediator is non-classical, in the LOCC sense (RQ-05, RE-04). Anastopoulos and Hu counter that "gravity-induced entanglement by Newtonian forces is agnostic to the quantum or classical nature of the gravitational true degrees of freedom" (RQ-14). That comment is a preprint whose arXiv version has been withdrawn for copyright reasons, so its availability is weak. Related: measurement-theory arguments for quantizing gravity are inconclusive (D-18). (refs: RQ-05, RQ-14, RE-04, RC-14)
- [D-24] **Is thermal time circular?** Connes–Rovelli derive a time flow from a thermal state (D-12). Chua 2024 [preprint] argues that "the thermal time hypothesis requires dynamics – and hence time – to get off the ground, thereby running into worries of circularity". This is a conceptual objection, not a theorem. No reply was collected. (refs: RT-07, RC-13)

## 4. Constraints: theorems, bounds, no-go results

No classical energy condition or quantum energy inequality enters any constraint below. The assumptions that matter are the spacetime class, the quantization scheme and the clock model, and each entry states them.

- [K-01] **Torre–Varadarajan functional-evolution no-go (facet 5).**
  - *Result:* for a free Klein–Gordon field on flat R × T^n with n > 1 (spacetime dimension > 2), the canonical transformation from a flat Cauchy surface to a generic final Cauchy surface "cannot, in general, be unitarily implemented on the Fock space". Evolution between isometry-related surfaces is unitary, and n = 1 (1+1 D) is unitary. The failure is an ultraviolet (Hilbert–Schmidt) effect, not caused by curvature of the surface as such.
  - *Assumptions:* free field; standard Fock (Poincaré-invariant) representation; toroidal spatial sections. On Minkowski space the authors only "expect" the same result. Exotic CCR representations are not excluded.
  - *Consequence:* even on a fixed flat background, Tomonaga–Schwinger evolution between arbitrary hypersurfaces is not unitary. This bears on hidden premise 1.
  - (refs: RT-08, RC-03) [peer-reviewed, full-text, verified]
- [K-02] **Unruh–Wald no-go on dynamical clocks (facet 4, quantum form).**
  - *Result:* "in ordinary Schrödinger quantum mechanics for a system with a Hamiltonian bounded from below, no dynamical variable can correlate monotonically with the Schrödinger time parameter t", so t cannot be replaced by a dynamical variable. They also argue that adding observers does not ease the interpretive problems of quantum gravity.
  - *Assumptions:* Hamiltonian bounded below; sharp (projection-valued) clock observables.
  - *Escapes:* unsharp POVM clocks, or idealized clocks with unbounded spectrum. A secondary preprint (arXiv:2607.01296) describes POVMs as the usual escape, and HSL claim their covariant POVMs resolve the non-monotonicity issue (RT-19).
  - *Provenance:* the theorem wording rests on the INSPIRE abstract and that secondary preprint, not the paper. Pauli's theorem (no self-adjoint time conjugate to a semibounded H) appears only through HSL's remark that time operator and clock Hamiltonian form a Heisenberg pair "only in the case of the ideal clock, in accordance with Pauli's remark". Pauli's text was not fetched.
  - (refs: RC-06 [verified partly], RC-07, RT-19)
- [K-03] **Kuchař's two-time conditional-probability objection.** In the naive conditional-probability interpretation, the two-time probability built from projectors on a constraint-satisfying state is non-zero only when T′ = T″ and Q′ = Q″. *Assumptions:* sharp clock projectors applied twice to the physical state. It does not apply to the relational-observable two-time conditional probabilities of HSL, subject to the caveat in D-19. (refs: RC-01, RT-20) [preprint report of Kuchař, full-text]
- [K-04] **Giulini–Kiefer consistency of semiclassical time.**
  - *Result:* "integrability conditions prevent the existence of Tomonaga-Schwinger time functions on the space of three-metrics but admit them on superspace", and "central charges in the matter sector spoil the consistency of the semiclassical approximation unless the full quantum theory of gravity and matter is anomaly-free".
  - *Assumptions:* WKB/Born–Oppenheimer approximation to canonical quantum gravity.
  - (refs: RC-11) [peer-reviewed, full-text, verified]
- [K-05] **Classical–quantum coupling must decohere and diffuse (the postquantum price).**
  - Oppenheim et al.: "any such hybrid dynamics necessarily results in decoherence of the quantum system, and a breakdown in predictability in the classical phase space". There is a trade-off in which "long coherence times require strong diffusion in phase-space relative to the strength of the coupling".
  - Galley, Giacomini and Selby: any consistent coupling of classical gravity to quantum matter is "fundamentally irreversible".
  - Oppenheim 2023: assuming GR is classical "necessarily modifies the dynamical laws of quantum mechanics – the theory must be fundamentally stochastic".
  - *Assumptions:* hybrid dynamics linear in the density matrix, completely positive, trace-preserving; Markovian with bounded generators (Eq. 4 of 2203.01982). The time parameter is that of the classical spacetime.
  - (refs: RT-18, RC-08, RE-09) [peer-reviewed; abstract/full-text, verified]
- [K-06] **Experimental squeeze on postquantum classical gravity.** For the delta-function kernel, the torsion-balance upper bound D2 ≤ 1e-41 kg² s m^-3 lies below the fullerene-decoherence lower bound D2 ≥ 1e-24 kg² s m^-3 (Q-20, Q-21). The authors conclude that this kernel "is already ruled out by experiment" and that classical theories are "squeezed by experiments from both ways". *Assumptions:* the specific kernel; order-of-magnitude "extremely conservative" estimates. Finite-range and other kernels are not excluded by this argument. (refs: RQ-09) [peer-reviewed, full-text, verified]
- [K-07] **Diósi–Penrose collapse bound.** R0 > 0.54e-10 m at probability 0.95 excludes the parameter-free Penrose version, R0 = 0.05e-10 m for Ge (Q-01, Q-02). *Assumptions:* the DP model with smeared nuclear mass density; the spontaneous-radiation-emission calculation, which is model-dependent; no dissipative extension. DP with a free, larger R0 survives. (refs: RQ-01, RC-12, RE-05) [peer-reviewed, full-text, verified]
- [K-08] **Clock-resolution limits.**
  - Gambini–Porto–Pullin: best accuracy δT ~ t_P (T_max/t_P)^(1/3) (Q-14), from a clock whose lifetime is bounded by black-hole formation and evaporation.
  - Salecker–Wigner: M ≥ hbar T/(c² δt²) (Q-16). Search-summary only; the formula is not verified against the paper.
  - *Assumptions:* heuristic gedanken-clock arguments, not theorems of a fixed theory.
  - (refs: RQ-06, RQ-07)
- [K-09] **Scope limits of the trinity theorem, stated by its authors.**
  - Time operator and clock Hamiltonian form a Heisenberg pair only for an ideal clock with Spec(H_C) = R.
  - Equivalence of reduced-phase-space and Dirac quantization needs a condition (their Eq. 57) that fails in general. Not checked by the checker.
  - The formalism shows clock-dependent temporal nonlocality under a change of clock.
  - The theorem assumes a clock–system split with no interaction.
  - Relativistic extension holds per frequency superselection sector (D-07).
  - (refs: RC-07, RT-04, RT-06)

## 5. Frontier and speculative (labelled; not established)

- [F-01] **SPECULATIVE: unimodular gravity as quantum gravity with a fundamental 4-volume time** conjugate to Λ. The price is a nondynamical background volume element (D-11). No critique of unimodular time was collected. (refs: RT-09, RT-15)
- [F-02] **SPECULATIVE: matter-clock deparametrization (Brown–Kuchař dust) as a resolution.** It adds a privileged frame and extra matter, and factor-ordering ambiguity remains (D-10). Facet 2 persists, since dust is one clock among many. The researcher also states that facet 4 holds only while dust worldlines do not cross; this is an inference, not quoted. (refs: RT-14)
- [F-03] **SPECULATIVE: semiclassical Wheeler–DeWitt time with observable corrections.** Corrections scale as (E/m_P)² (Q-17, Q-18). The Kiefer–Kramer CMB large-scale power suppression gives only H ≲ 4e17 GeV (Q-19). The estimate is a preprint essay, and later papers dispute size and sign (titles only). (refs: RQ-08, RT-12, RT-13)
- [F-04] **SPECULATIVE: realistic-clock fundamental decoherence (Gambini–Porto–Pullin),** a modification of effective QM. By the authors' own statement it is unobservable in the lab without large level splittings (Q-15). (refs: RT-17, RQ-06)
- [F-05] **SPECULATIVE: postquantum classical gravity (Oppenheim).** Time is the classical spacetime's time with stochastic fluctuations, which removes the frozen formalism rather than solving it. The delta kernel is already excluded (K-06). Its distinctive signatures are metric noise and decoherence, and no gravity-mediated entanglement. (refs: RT-18, RQ-09, RC-08, RE-09)
- [F-06] **SPECULATIVE: gravity-related collapse (Diósi–Penrose).** Collapse dynamics presupposes an external time parameter (researcher's framing, RQ-01, RE-05). Only the free-R0 version survives K-07. (refs: RQ-01, RE-05)
- [F-07] **SPECULATIVE (as quantum gravity): thermal time.** It is contested on circularity grounds (D-24). No research claim covers extensions to de Sitter or closed-universe observer algebras. (refs: RT-07, RC-13)
- [F-08] **SPECULATIVE (as quantum gravity): Hartle's generalized quantum mechanics of spacetime.** The decoherence functional, measure and identification of physical time are supplied by the classical limit (D-13). (refs: RT-16)
- [F-09] **PROPOSED EXPERIMENTS (not realized):**
  - Zych et al. 2011: the proper-time visibility witness. Visibility drops "to the extent to which the path information becomes available from reading out the proper time", which would be "the first test of the genuine general relativistic notion of proper time in quantum mechanics" (RQ-12).
  - Pikovski time-dilation decoherence (Q-07).
  - Loriani et al. 2019 quantum-clock twin-paradox interferometer: closed light-pulse interferometers without clock transitions "are not sensitive to gravitational time dilation in a linear potential" (RE-06; confirmed at full text per the update and check).
  - The MAGIS-100 freely falling atom-clock time-dilation measurement [preprint] (RE-07).
  - QGEM spin-entanglement witness (Q-09, Q-10).
  - None discriminates between relational, semiclassical, thermal and unimodular positions. They test proper time in superposition, or whether gravity is quantum.
- [F-10] **[search-summary] Readiness of levitated-particle platforms.**
  - Levitated nanoparticles have reached motional ground-state cooling with picometre-scale delocalization, far from the ~100 µm needed.
  - The TRL 2–3 estimate for QGEM, and TRL 3–4 for MAGIS time dilation, are the researcher's judgement.
  - Treat these as background, not evidence.
  - (refs: RE-12, RE-07)

## 6. Unknowns and gaps

- **No discriminating observation among the "conservative" positions.** No number was found that separates Page–Wootters/relational, semiclassical WDW, thermal or unimodular time. All recover GR proper time at leading order, and the only bounded positions are collapse, classical gravity and clock decoherence (quantitative Gaps; RE-13 [search-summary negative synthesis]).
- **No experiment on quantum time.** None has put a clock in a superposition of gravitational potentials, tested a Wheeler–DeWitt-type constraint, or seen gravity-mediated entanglement (RE-13, search-summary; absence of evidence).
- **Kuchař and Unruh–Wald primary texts not opened.** Kuchař's objections come via Dolby and HSL. The Unruh–Wald theorem wording comes from an abstract and a secondary preprint, whose own workaround claim was not evaluated.
- **No independent assessment of the HSL replies.** None was found. Rijavec 2023 (PRD 108, PW robustness), finite, degenerate and interacting-clock analyses, and Smith–Ahmadi 2019 and Giovannetti–Lloyd–Maccone 2015 were not opened.
- **Missing primary sources.**
  - Pauli's theorem.
  - The ADM/Dirac constraint algebra and ADM energy for asymptotically flat spacetimes (brief premise 4). No research claim covers them.
  - Rovelli 1991 and Dittrich partial/complete observables.
  - Banks 1985 and Brout–Venturi.
  - Penrose 1996 (HTTP 403) and Diósi 1987.
  - Page–Geilker 1981 (Crossref only).
  - Marletto–Vedral 2017.
  - Henneaux–Teitelboim unimodular gravity.
  - Salecker–Wigner 1958.
- **Positions with no collected claims:** shape dynamics/CMC (York) time, Hořava–Lifshitz, causal sets, spin foams, holographic/boundary time, Barbour's timeless view, Everett/Bohm dependence (brief premise 8), and observer-dressed algebras in de Sitter.
- **Missing critiques and bounds:**
  - Critiques of unimodular time, dust clocks, Hořava–Lifshitz and shape dynamics.
  - Schrödinger–Newton and CSL bounds.
  - The Bonder–Okon–Sudarsky arguments themselves.
  - Later CMB-correction estimates.
  - Di Gioia et al. 2021.
- **Toy model not yet built for the hard cases.** The Kuchař two-time objection and interacting or degenerate clocks are not tested in the finite-dimensional Page–Wootters model. There is no minisuperspace Born–Oppenheimer toy model. These are assigned to the idealizer and math checks.
- **Facet 7 (spacetime reconstruction) has no dedicated source.**

## 7. Source-quality notes

- **Inputs.**
  - Four research facets (theory 20 claims, quantitative 15, critiques 14, engineering 13; 62 in total), each with a check file.
  - No frontier facet was run: the brief assigns four facets, and frontier items here come from the other facets.
  - No facet was missing a check file, so no claims are marked unchecked.
  - No `math/` checks existed at compile time.
- **Dropped (contradicted):** none. No checker returned "contradicted" or "status-wrong".
- **Corrected (misattributed):**
  - RT-13: the three semiclassical approaches are Kiefer–Singh, the Maniccia–Montani reference fluid and extended phase space, not "Banks-type/Brout-type" (D-21).
  - RQ-13: the Bild et al. superposition size is given in the paper (2.1e-18 m), and "largest effective mass" is unsourced (D-16, Q-11).
- **Other corrections from the checks:**
  - RT-10: clock names are fluid, volume and scalar.
  - RT-14: overstated "solves facets 1 and 3" (D-10).
  - RT-03: INSPIRE dates it as a 1991 conference paper.
  - RQ-02: "four orders" is about 3.7 orders; the source's own figure is "about three orders" over GW bounds.
  - RQ-15: authors are Bonder, Okon and Sudarsky.
  - RE-08: "~0.1 g" should be ~0.09 g.
  - RE-11: the mass gap is about 8.4 orders of magnitude, not ~9.
  - RC-14: the verdict was upgraded from the abstract, as found by the checker.
  - RT-06 and RT-11: glosses flagged as researcher inference.
- **Unverifiable claims kept, with labels:**
  - RQ-07 (search-summary).
  - RE-11 (search-summary).
  - RE-12 (search-summary; background only).
  - RE-13 (negative synthesis).
  - RC-10 (abstract not re-fetched; the same abstract was verified under RT-12).
  - Within RC-07, the "two-time gauge-invariance not established" sentence.
  - RC-06 (partly verified; theorem wording secondhand).
- **Share of claims resting only on search summaries:** 4 of 62 research claims (6.5%): RQ-07, RE-11, RE-12, RE-13. RE-06 was upgraded to full text by the researcher's later fetch, confirmed by the checker. Two quantitative anchors (Q-12, Q-16) and one frontier item (F-10) rest only on search summaries.
- **Preprints relied on:**
  - Dolby 2004 (RC-01).
  - Kiefer–Kramer 2012 essay (RQ-08).
  - Chua 2024 (RC-13).
  - Anastopoulos–Hu 2018 (RQ-14; arXiv version withdrawn).
  - Moreva 2017 (RE-10).
  - Roura et al. 2024 (RE-07).
- **Fringe excluded:** none identified.
- **Own-computation claims:**
  - RQ-11 (Page–Wootters toy model).
  - The arithmetic in RQ-06, RQ-07, RQ-08 and RQ-13.
  - All come from `calc/quantitative_pw_clock.py` and `calc/quantitative_scales.py`, and the checker re-ran them.
- **Earlier runs:** none. There is no `prior/` folder; the brief lists the warp-bubble run as "ignore". So 0 claims were carried from earlier runs and 0 were re-verified.

## User-supplied

- [U-01] [user] **How to read the toy-model fidelities in D-17 and Q-25 to Q-27.** Proposed by the main session at the dossier checkpoint and approved by the user. When omega/eps is not an integer, the fidelities in Q-25 and Q-26 come from the *best approximate* solution of the constraint: the system energy omega is missing from the clock's spectrum, so no exact physical state carries it. They measure this spectral mismatch (coverage). They are not evidence that conditional evolution breaks down.
  - For any exact physical state of an uncoupled constraint J = H_C⊗1 + 1⊗H_S, the conditional state psi_S(t) = (<t|⊗1)|Psi>> obeys i d/dt psi_S = H_S psi_S exactly, for every t and any clock spectrum (equally spaced or not, degenerate or not). The reason is that d<t|/dt = i<t|H_C when |t> = sum_k e^{-i E_k t}|E_k>.
  - Non-ideal uncoupled clocks fail in other ways:
    - *coverage:* only system energies e with -e in spec(H_C) survive;
    - *readability:* time states are orthogonal only for an equally spaced spectrum at lattice times, and a Gaussian reading error sigma dephases the energy basis by exp(-sigma^2 Delta^2/2);
    - *degeneracy:* the map from physical states to psi_S is not injective.
  - Only a coupling between clock and system makes the conditional evolution non-unitary or time-nonlocal; the Smith–Ahmadi gravitational coupling is an exactly solvable case.
  - (refs: D-17, Q-25 to Q-27) [calc: runs/2026-09-29-problem-of-time-quantum-gravity/tools/page_wootters.py selftest, promoted as .claude/skills/conundrum/scripts/page_wootters.py; checks "unequally spaced clock: fidelity 1 at arbitrary t" and the docstring's "Key identity"]
