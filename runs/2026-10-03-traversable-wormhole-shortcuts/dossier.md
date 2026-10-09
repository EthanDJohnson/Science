# Dossier: Traversable wormholes: shortcuts, negative energy, and what holds them open
status: final

Compiled 2026-10-08 from `research/{theory,quantitative,critiques,engineering,frontier}.md` and their `.check.md` files, after the relaunch that brought in the 2026-10-01 warp-drive run. Replaces `superseded/dossier.v1.md`, which was compiled without the warp-run material.

Conventions:
- Signature (−,+,+,+). Units are stated per item: SI, or geometric with G = c = 1, or natural with ħ = c = 1.
- Ref IDs are the researchers' claim IDs: RT theory, RQ quantitative, RC critiques, RE engineering, RF frontier.
- A tag `[warp-run, re-verified]` marks a claim carried from 2026-10-01-warp-drive-without-negative-energy (it has a PRIOR line in its research note) whose words were found again in the source during this run.
- "check: verified / unverifiable / unchecked" is the source-checker's verdict. Every facet had a check file. A few claims were skipped by the checker: they are labelled "unchecked".
- Claims marked `ACCESS: search-summary` are labelled **[search-summary]** and are never quoted.

## 1. Established

Peer-reviewed or textbook results whose sources were checked. Theorems and bounds, with their assumptions, are in section 4.

**Two-sided (AdS / 2D) constructions**
- [D-01] **Gao–Jafferis–Wall (GJW).** Setting: the eternal BTZ black hole (AdS₃, 2+1D bulk).
  - A double-trace coupling between the two boundary CFTs gives a one-loop quantum stress tensor with negative averaged null energy. Its back-reaction makes the Einstein–Rosen bridge traversable.
  - It is two-sided, with no shared ambient space, and the authors state "it cannot be used to violate causality".
  - In the decoupled system no signal can pass through the bulk. At linear order the averaged null energy vanishes for the TFD state. So traversability exists only through the boundary coupling, which is the non-gravitational channel the brief says to compare against.
  - ANEC violation is a prerequisite for traversability.
  - The authors note "presumably there is some limit on how much information can get through" but do not derive it.
  - Refs: RT-04, RT-05, RC-15, RQ-24. Peer-reviewed (JHEP 12 (2017) 151). Check: verified (RC-15 itself unverifiable, not re-fetched; its content duplicates RT-04/05, which are verified).
- [D-02] **Maldacena–Stanford–Yang (MSY) 2017.** Setting: nearly-AdS₂.
  - They state that GR forbids traversable wormholes "in the sense that we cannot send a signal through the wormhole faster than we can send it through the outside". GJW evades this only through the boundary coupling.
  - Back-reaction of the signals limits what passes: roughly, the number of quanta is less than a constant times the number of bits exchanged to set up the coupling, so "we can't send more than a few bits". Section 2.5 of the paper calls these bounds "parametric", not sharp (check note on RC-16).
  - A 1 kg payload lies far outside this perturbative treatment (researcher's scope note).
  - Refs: RT-26, RQ-23, RC-16. Peer-reviewed (Fortsch. Phys. 65, 1700034).
- [D-03] **Freivogel, Galante, Nikolakopoulou & Rotundo 2020** (BTZ, probe regime).
  - The GJW wormhole is open for a proper time shorter than the Planck time, yet a signal can sometimes stay semiclassical.
  - For horizons of order the AdS radius, information cannot be reliably sent. For horizons much larger than the AdS radius, the number of quanta that can pass is of order the horizon area in AdS units. More light fields allow more.
  - Kontou's 2024 review restates the "shorter than the Planck time" result (RQ-18). Its reference [78] was not identified; low confidence on that restatement alone.
  - Refs: RT-29, RC-27, RQ-18. Peer-reviewed (JHEP 01 (2020) 050).
- [D-04] **Maldacena–Qi 2018.** Setting: nearly-AdS₂ (JT); also two coupled SYK systems.
  - An eternal traversable wormhole supported by negative null energy of quantum fields under an external coupling between the two boundaries. Large N is needed for control.
  - The ANEC requirement is the 2D special case of topological censorship: ∫dX⁺ T₊₊ = −2φ_r < 0. A finite amount of negative energy suffices. Two-sided.
  - Refs: RT-08. Status: arXiv preprint as confirmed; journal ref not confirmed. Check: verified.
- [D-05] **Fu–Grado-White–Marolf (FGM) 2018: self-supporting quotients.**
  - Z₂-quotient wormholes become traversable through first-order back-reaction of linear quantum fields with (anti)periodic boundary conditions, in Hartle–Hawking-type states, with no boundary interaction. Works with few fields.
  - In the rotating KKZBO example the wormhole is traversable only "until a time t_f", which grows toward extremality. The authors only "suggest" that a non-perturbative treatment would find an eternal self-supporting wormhole. They call the link between the near-extremal divergence and known extremal-black-hole instabilities an open question.
  - The key quantity ∫dU⟨T_kk⟩ along non-contractible cycles is negative (Casimir-like), so the construction needs quotient topology.
  - Refs: RT-09, RC-28, RQ-25. Journal ref: CQG 36, 045006 per INSPIRE (RQ-25); RT-09 and RC-28 left it unverified. Check: verified.

**Four-dimensional quantum-supported constructions (one ambient space)**
- [D-06] **Maldacena–Milekhin–Popov (MMP) 2018.**
  - Setting: 4D Einstein–Maxwell with charged massless fermions. Two oppositely magnetically charged near-extremal black holes are joined by a long wormhole.
  - Support: the negative Casimir-like energy of fermions in the lowest Landau level along the magnetic field lines. "Ordinary matter" here does not mean "no negative energy".
  - ANEC is violated along null lines wrapping the field-line circle, but these null lines are not achronal (the authors' own statement).
  - It is a long wormhole, chosen so as not to violate the achronal ANEC. The authors state that short wormholes "are not allowed by the Einstein equations combined with the achronal average null energy condition".
  - Traversal: proper time of order r_E ∼ q, much shorter than the time seen from outside, πℓ ∝ q². Not a shortcut.
  - Standard Model embedding: possible only if the overall size is small compared with the electroweak scale ("say 1/TeV", about 2×10⁻¹⁹ m), with SM fermions acting like N_f = 54 charge-one flavours.
  - In the covering space the wormhole would join different universes and be short, which "should be forbidden by causality". The solution depends on the actual topology.
  - Refs: RT-06, RT-07, RC-17, RQ-26, RE-16, RF-20. Peer-reviewed (CQG 40, 155016). Check: verified. The πℓ/d → 1 limit for d ≪ d₀ in RC-17 is unchecked.
- [D-07] **FGM 2019: asymptotically flat, short transit.**
  - Setting: 4D, Λ = 0. A pair of oppositely charged black holes, held apart by a cosmic string, with perturbative back-reaction of bulk quantum fields in Hartle–Hawking states.
  - At finite temperature the wormhole becomes traversable for appropriately timed signals, with minimum transit time t_min = d + logs (c = 1). This is more than a factor 2 shorter than for MMP, but it is not shorter than d.
  - The paper ties d + logs to the prohibition on wormholes providing the fastest causal curves between distant points. The paper calls this prohibition "general arguments (and in particular the generalized second law)", not a proven theorem (check note, RT-11). Per the check note on RF-08, the "no shortcut" reading holds as "approaches the minimum, at least in higher dimensions".
  - Traversability is exponentially fragile, destroyed by exponentially small perturbations. An arbitrarily small back-reaction can open the wormhole "at least for some period of time". The background is unstable: the black holes merge on a timescale ∼ d^{3/2} (G = c = 1).
  - Refs: RT-10, RT-11, RQ-15, RC-09, RC-21, RF-08. Peer-reviewed (CQG 36, 245018). RC-21 unverifiable (not re-checked; the abstract supports transience and fragility); its content duplicates verified claims.
- [D-08] **Maldacena–Milekhin (MM) 2020, "humanly traversable".**
  - Needs a speculative sector: Randall–Sundrum II and a dark U(1). The authors themselves call this "science fiction".
  - The pure 4D free-fermion version fails: it needs N_f > 10⁵², against N_f < M_pl²/TeV² ∼ 10³².
  - Not a shortcut: πℓ > d for any mouth separation. The traveller's proper time is ∼ πr_e: "less than a second" for galactic distances, against "tens of thousands of years for somebody looking from the outside".
  - From outside, the mouths resemble intermediate-mass charged black holes.
  - Practical obstructions stated by the authors:
    - a CMB photon falling in is boosted by γ and seen by the traveller with γ², so the system must sit "inside a refrigerator";
    - the dark sector must be colder than 1/ℓ ∼ 10⁻²⁶ eV;
    - matter that falls in and loses energy accumulates and "would eventually make the wormhole collapse into a black hole";
    - "We have not given any plausible mechanism for their formation."
  - Refs: RT-12, RT-13, RT-14, RQ-01 to RQ-06, RC-18, RC-19, RE-14, RF-05, RF-06. Peer-reviewed (PRD 103, 066007). RC-19 unverifiable (not re-fetched); RE-14 independently verified the "much colder than the present universe", refrigerator and formation quotes. The 10⁻²⁶ eV figure and the collapse sentence rest on RC-19 alone.

**Einstein–Dirac–Maxwell (EDM) "no exotic matter" wormholes**
- [D-09] **Blázquez-Salcedo–Knoll–Radu (BKR) 2021.**
  - Asymptotically flat, spherically symmetric traversable wormholes in 4D EDM, with two gauged massive fermions in a singlet state.
  - The Dirac matter is "a quantum wave function rather than a quantum field" (semiclassical). The authors claim this works "without needing any form of exotic matter".
  - All their solutions have Q_e/M > 1 and q/μ < 1 (Planck units). The family is scale-invariant with a one-particle condition, so the physical size is set by the fermion mass in Planck units (the researcher's inference).
  - Refs: RT-16, RQ-13, RE-17. Peer-reviewed (PRL 126, 101102). Check: verified. The closed-form mass M = 2Q_e²r₀/(Q_e² + r₀²) (RQ-13) was not seen by the checker.
- [D-10] **Critiques of the symmetric BKR construction.**
  - (a) Bolokhov, Bronnikov, Krasnikov & Skvortsova 2021: by the standard definition (exotic = NEC-violating), exotic matter is unavoidable at any throat. So "no exotic matter" is misleading: the Dirac fields become exotic matter.
  - (b) Danielson, Satishchandran, Wald & Weinbaum 2021: the reflection-glued BKR wormholes violate the Dirac matching conditions. They contain shells of charged matter and spurious distributional Dirac sources at r = 0, so they "are not solutions to the EDM equations". This paper also argues non-smoothness (metric not C³ at the throat), so it overlaps Konoplya–Zhidenko's point (correction from check).
  - (c) Konoplya & Zhidenko 2022:
    - mirror symmetry forces non-smooth fields;
    - it also forces a sign flip of the fermion charge density at the throat, with particles and antiparticles coexisting without annihilation, and a matter membrane at the throat;
    - they built asymmetric smooth EDM wormholes instead;
    - they also state that wormholes "have never been observed" and that formation scenarios are "highly disputable".
  - Per the check note on RQ-14, BKR's negative ADM mass applies to solutions near the critical line, not to smooth solutions in general.
  - Refs: RT-19, RC-22, RC-04, RQ-14, RE-18, RF-03, RT-20. Peer-reviewed. RT-20 (the comment arXiv:2206.12250 on the N′(0) = 0 condition) is unverifiable: not load-bearing.
- [D-11] **Kain 2023 (PRD 108, 044019): evolution of the asymmetric EDM wormholes.**
  - Parameters: μ̄ = 0.2, ē/√(4π) = 0.03, spherical symmetry.
  - In every case black holes form, connected by the wormhole. Null geodesics that cross the throat are trapped inside a black hole: "Einstein-Dirac-Maxwell wormholes are not traversable".
  - The static solutions are regular, but they violate the NEC (T^r_r − T^t_t < 0 with radial null vectors). Their throat radii are 75.28 to 498.4 Planck lengths (Table I).
  - Kain: "violation of the null energy condition is an insufficient condition for determining if a static wormhole solution is traversable".
  - Caveat from Kain: another asymmetric EDM solution may behave differently.
  - Refs: RT-17 [search-summary lead], RT-18, RC-05, RC-06, RF-01, RF-02. Peer-reviewed per RC-05/RF-01; RT-18 lists the journal ref as unverified. Check: verified.
- [D-12] **Weinbaum 2026: static obstruction in Einstein–Dirac theory.**
  - Classical positive-frequency Dirac fields on certain fixed wormhole geometries can violate ANEC.
  - But a numerical search for static, spherically symmetric, asymptotically flat solutions with definite frequency, angular momentum and parity finds only "partial-wormhole solutions". These cannot be continued to a second asymptotically flat end. The reflection-symmetric conditions "cannot be satisfied".
  - Conclusion: the results "strongly support" that the Einstein–Dirac system admits no traversable wormhole sourced by a physically meaningful Dirac field. This is numerical evidence on a restricted ansatz, not a theorem.
  - Weinbaum says the earlier works mishandled single-particle electromagnetic self-interaction and used negative-frequency modes. Per the check note on RC-23, this undercuts Konoplya–Zhidenko and Kain 2023 as well as BKR.
  - Status: peer-reviewed per INSPIRE (PRD 114, 084004, doi:10.1103/g89c-gqyf). The text was read from the arXiv version. The frontier checker could not see the journal ref, so treat it as "preprint at least".
  - Refs: RT-38, RC-23, RC-24, RF-22. Check: verified (quotes).

**Classical wormholes: dynamics and stability**
- [D-13] **Ghost-scalar (Ellis–Bronnikov-type) wormholes are unstable.**
  - Every static member of the family has exactly one unstable radial mode. Nonlinear evolution makes the wormhole either expand or collapse to a Schwarzschild black hole, depending on the sign of the perturbation. Charged ghost-scalar wormholes are also unstable (González, Guzmán & Sarbach 2009; abstracts only).
  - Kain 2026 (CQG 43, 045014): the Ellis–Bronnikov and the semiclassical "quantum-corrected Schwarzschild" wormholes evolve "remarkably similar[ly]". A weak regular-scalar pulse (A = 0.002 in the paper's units) makes the static wormhole collapse: positive-energy infall closes the throat.
  - Scope: spherical symmetry, numerical.
  - Refs: RC-14 (abstract), RC-26. Peer-reviewed (Kain 2026 journal ref per INSPIRE).
- [D-14] **Thin-shell (Visser) wormholes, Poisson & Visser 1995.**
  - The shell's surface energy density σ₀ is negative, so the shell is already "exotic matter".
  - Linearised stability requires "somewhat perverse" restrictions on the speed of sound (β₀² = dp/dσ). The sign of the stability inequality flips at a₀ = 3M. Large wormholes (a₀ > 3M) are stable only for β₀² < 0.
  - Refs: RT-41, RQ-20 (method). Peer-reviewed. The PRD 52, 7318 ref and equation numbers were not checked.
- [D-15] **Morris–Thorne/Ellis throat energy conditions (this run's calculation).**
  - At the Ellis–Bronnikov throat (Φ = 0, b = b₀²/r): ρ = p_l = −1/(8πb₀²) and p_t = +1/(8πb₀²), so ρ + p_l = −1/(4πb₀²) < 0 (geometric units).
  - NEC, WEC, SEC and DEC are all violated pointwise.
  - The ANEC integral along the radial null geodesic is finite and negative, I = −E/(8b₀) per unit conserved energy E.
  - The general Morris–Thorne form at the throat, ρ + p_r = (b′ − b/r)/(8πr²) < 0 under flare-out, is a standard result. No source was opened for it [search-summary] (RT-32, unverifiable).
  - Refs: RQ-19 [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/quantitative_wormhole_tools.py], RT-32. Calculation; the checker re-did the arithmetic but did not re-derive the ANEC integral.

**The 2022 quantum-processor experiment and related experiments**
- [D-16] **Jafferis et al. 2022 (Nature 612, 51).**
  - A teleportation protocol on Google Sycamore. A learned, sparsified SYK-like Hamiltonian was realised "with 164 two-qubit gates on a nine-qubit circuit".
  - The paper claims five properties of traversable-wormhole physics: perfect size winding, coupling consistent with a negative-energy shockwave, Shapiro delay, causal time order, and scrambling/thermalisation.
  - The authors frame it as "a step towards a program for studying quantum gravity in the laboratory". No spacetime was created; neither side of the dispute claims one was (researcher's inference, consistent with both).
  - The Nature page lists an Author Correction (4 Apr 2025) and a Matters Arising (23 Jul 2025).
  - Refs: RE-01, RE-02, RF-13, RQ-12. Peer-reviewed; abstract page only (body paywalled).
- [D-17] **Wormhole-inspired teleportation on other hardware (Brown et al., "Quantum Gravity in the Lab").**
  - Holographic teleportation protocols "readily executed in table-top experiments", mimicking GJW/MSY in non-gravitational entangled systems (PRX Quantum 4, 010320). RE-08 is unverifiable: not fetched in the check.
  - Data from 7 qubits (IBM) and 6 qubits (Quantinuum). Corrected after check: the unmitigated fidelity of about 80% of ideal is the Quantinuum run only. The IBM run was about 20%, about 35% with mitigation (per the checker).
  - The authors do not claim the quantum-gravitational regime.
  - Refs: RE-08, RQ-12.
- [D-18] **Ikeda 2023: quantum energy teleportation on IBM hardware.**
  - Results are "consistent with the exact solution" after error mitigation. QET "requires only local operations and classical communication".
  - It creates no sustained negative energy density and is not a wormhole (researcher's remark).
  - Refs: RE-28 [warp-run, re-verified]. Peer-reviewed (PRApplied 20, 024051, ref unchecked).

**Laboratory negative energy and vacuum effects**
- [D-19] **Casimir force measurements** (ordinary-quantum-field negative energy is real and measurable at sub-micrometre gaps). Nothing has been measured at a throat-relevant scale or geometry.
  - Bressi et al. 2002: parallel plates, 0.5 to 3.0 µm, force coefficient at 15%.
  - Decca et al. 2003: Cu–Au, 0.2 to 2 µm, noise 6 fN/√Hz. Corrected after check: agreement with theory better than 1% applies to the 0.2 to 0.5 µm sub-range only.
  - Roy, Lin & Mohideen (PRD 60, 111101, published 1999; the claim's "2000" is a minor discrepancy): improved sphere–plate precision.
  - The Mohideen & Roy 1998 percent-level figures are [search-summary].
  - Refs: RE-23, RE-29.
- [D-20] **Squeezed light** (the one sub-vacuum state in routine use). These are noise-variance statements, not energy densities in J/m³; no source gives a squeezed-light negative energy density in SI units.
  - Vahlbruch et al. 2016 (PRL 117, 110801): up to 15 dB below vacuum noise, at 3 to 8 MHz and 1064 nm, with 16 mW of pump power. RE-25 corrects RE-22's [search-summary] "about −15 dB over three decades" phrase, which is not in the paper.
  - Lough et al. 2021 (PRL 126, 041102): GEO 600 achieved 6.03 ± 0.02 dB at 6 kHz, the first km-scale 6 dB result.
  - Refs: RE-25 [warp-run, re-verified], RE-26 [warp-run, re-verified], RE-22.
- [D-21] **Dynamical Casimir effect** (Wilson et al. 2011, Nature 479, 376).
  - A superconducting transmission line whose electrical length is changed "at a few percent of the speed of light" by a SQUID modulated at about 11 GHz. Real photons and two-mode squeezing were observed.
  - It demonstrates moving-boundary vacuum radiation, not a bulk negative energy density.
  - Refs: RE-27 [warp-run, re-verified; the earlier "0.05c" value is not in the source and was dropped].

**Astronomical searches** (all null; each assumes a classical Ellis/negative-mass lens or a horizon-replacement model)
- [D-22] **Lensing searches.**
  - Takahashi & Asada 2013 (SDSS Quasar Lens Search, 50,836 quasars in the statistical sample): no multiple images from negative-mass objects or Ellis wormholes. Bounds are in section 2.
  - Abe 2010: Ellis-wormhole microlensing light curves show about 4% "gutters" outside Einstein-ring crossing, with magnification generally below Schwarzschild's.
  - Galactic microlensing could probe throat radii of 100 to 10⁷ km. Sources of about 10⁶ km smear smaller lenses.
  - These searches do not constrain MMP/MM mouths, which look like positive-mass extremal charged black holes (researchers' scope note).
  - Refs: RQ-16, RE-10, RE-11. Peer-reviewed.
- [D-23] **Orbital-perturbation test** (Dai & Stojkovic 2019). If Sgr A* were a wormhole, a star on the far side would perturb S2.
  - Needs about 10⁻⁶ m/s² acceleration precision. Achieved: 4×10⁻⁴ m/s² (2 yr); projected 2×10⁻⁵ m/s² (20 yr).
  - Assumes a classical picture in which gravity propagates through the mouth.
  - Simonetti et al. (preprint): a triple system improves the limit by about 4 orders of magnitude; a pulsar in an S2-like orbit by about 10.
  - Refs: RE-12 (peer-reviewed), RE-13 (preprint).
- [D-24] **Gravitational-wave echoes and black-hole shadows.**
  - LVK O3 echo searches find p-values consistent with noise. Earlier O1 echo claims are disputed; the "2.5σ" figure is unconfirmed.
  - EHT Sgr A*: image size within about 10% of Kerr predictions.
  - Neither test probes MM-type extremal mouths.
  - Refs: RE-20 (preprint, journal ref unchecked), RE-21 (peer-reviewed). The 47 to 50 µas shadow values and the "Ellis–Bronnikov not excluded by size alone" point are unverified / [search-summary].
- [D-25] **Magnetic monopoles.**
  - MoEDAL's Schwinger-mechanism search (Pb–Pb at 5.02 TeV per nucleon, 0.235 nb⁻¹) excluded monopoles with 1 to 3 g_D up to 75 GeV/c². No magnetic charge has been detected at any scale.
  - Later limits up to about 3.9 TeV are [search-summary], unconfirmed.
  - Refs: RE-19. Peer-reviewed (Nature 602, 63).

**Reviews framing the field**
- [D-26] **Kontou & Sanders 2020** (review).
  - All pointwise energy conditions are violated by essentially any QFT.
  - The achronal ANEC "comes closest to being generally valid". Its validity in curved spacetime is open.
  - Refs: RT-24. Textbook-or-review.
- [D-27] **Kontou 2024** (Universe 10, 291, review).
  - The achronal ANEC "is free of counterexamples in semiclassical gravity" and suffices to rule out causality violations in asymptotically flat spacetimes. It "seems to prohibit" shortcut wormholes.
  - "Long" wormholes escape it because no complete achronal null geodesic passes through them. Null QEIs, SNEC and DSNEC then apply. Kontou applies SNEC and DSNEC to MMP; the DSNEC constraint is a new result.
  - Known ANEC violations fall into three kinds: on chronal geodesics; in non-self-consistent backgrounds; at Planck scale without transverse averaging.
  - A Planck-size throat "would not be traversable".
  - Refs: RF-11, RF-12, RQ-09, RQ-08. Peer-reviewed review.

## 2. Quantitative anchors

All values are current unless marked. "Calc" = this run's own calculation, cited to its script.

| ID | Quantity | Value ± stat ± sys (units), as quoted | Conditions; current or preliminary; supersedes <ref> if any | Source refs | Access |
|---|---|---|---|---|---|
| Q-01 | MM tidal minimum throat radius | r_e > 1.5×10⁷ m (∼0.05 light-s) (SI) | a ∼ size·c²/r_e² < 20 g (g = 9.8 m/s²), size 0.5 m, short durations; MM's own criterion; current | RQ-01, RT-14, RF-05, RE-14; reproduced 1.51×10⁷ m in RQ-17 [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/quantitative_scales.py] | full-text |
| Q-02 | MM worked RS II parameters (eq. 3.27) | r_e ∼ 0.05 s; c₂ ∼ 7×10⁷²; ℓ ∼ 3×10³ ly; γ = ℓ/r_e ∼ 2×10¹²; E_bin ∼ −5×10⁹ kg (≈ −4.5×10²⁶ J, SI) | Minimal r_e, largest allowed RS length R₅ = 50 µm; speculative sector; current | RQ-02 | full-text |
| Q-03 | MM species count, free-fermion 4D version | N_f > 10⁵² required, against N_f < M_pl²/TeV² ∼ 10³² allowed | 10³ kg ship, \|E_bin\| > 10³ kg, r_e > 10⁷ m, g²N_f < 1; the bound assumes a TeV UV cutoff (Bekenstein-like); current | RT-13, RQ-04, RC-18, RF-05 | full-text |
| Q-04 | MM mouth mass | M_e = r_e c²/G ≈ 2.0×10³⁴ kg ≈ 1.0×10⁴ M_☉ per mouth (SI) | Extremal relation M_e = r_e/G₄ with r_e = 1.5×10⁷ m; researcher's arithmetic; current | RQ-06, RQ-17, RE-15, RF-21 [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/engineering_mm_scale.py] | full-text (input) + calc |
| Q-05 | MM binding energy relative to mouth mass | \|E_bin\|/M_e ≈ 2.5×10⁻²⁵ (dimensionless) | Q-02 E_bin over Q-04 M_e; calc; current | RQ-17 [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/quantitative_scales.py] | calc |
| Q-06 | MM traversal times | External πℓ/c ≈ 9.4×10³ yr; traveller proper time πr_e/c ≈ 0.157 s (SI) | From Q-02. The paper says "tens of thousands of years"; the checker calls this loose rounding. T_thru/T_ext = πℓ/d ≥ π for d ≤ ℓ (researcher's reading; the paper states πℓ > d for any d); current | RQ-03, RQ-17, RC-18, RF-06 | full-text + calc |
| Q-07 | MM dark-sector temperature requirement | T < 1/ℓ ∼ 10⁻²⁶ eV (natural units) | RS II construction in cold flat ambient space; current | RC-19 (unverifiable, not re-fetched; RE-14 verifies the "much colder than the present universe" wording) | full-text |
| Q-08 | MM magnetic field at r_e | B ≈ 2.3×10¹¹ T (SI) | Assumes extremal Reissner–Nordström in SI electromagnetism; researcher's assumption; current | RE-15 [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/engineering_mm_scale.py] | calc |
| Q-09 | MM magnetic charge | Two incompatible estimates: 1.6×10⁴¹ Dirac charges per mouth (RE-15, extremal RN in SI EM) vs q ∼ 3×10⁸¹ to 3×10⁸³ (RQ-17, from r_e = √(πq) l_p/g₄ with g₄ = 0.1 to 1, "illustrative") | Different charge conventions (dark U(1) with unspecified g₄ vs SI Maxwell); unresolved, see D-C7; current | RE-15, RQ-17 | calc |
| Q-10 | MMP energy and throat length | E = r_e³/(G_N l²) − q/(8l); minimised at l = 16 r_e³/(G_N q); E_min = −G_N q²/(256 r_e³) (ħ = c = 1) | Energy relative to two extremal BHs; eqs 5.30–5.31. The checker read the equations correctly and found the low-confidence flag unnecessary; current | RT-07 | full-text |
| Q-11 | MMP Standard Model embedding scale | size ≪ electroweak scale, "say 1/TeV" ≈ 2×10⁻¹⁹ m (SI); N_f = 54 effective charge-one flavours | SM-only realisation; current | RE-16, RC-17 | full-text |
| Q-12 | MMP traversal times | Proper time ∼ r_E ∼ q; external πℓ ∝ q² (units set by magnetic charge q) | Long wormhole; FGM 2019 quote t_transit/d > 2 for MMP; current | RQ-26, RC-09, RC-17 | full-text |
| Q-13 | FGM 2019 minimum transit time | t_min = d + logs (c = 1; d = mouth separation) | 4D asymptotically flat; perturbative; > 2× shorter than MMP; merger time ∼ d^{3/2} (G = c = 1); current | RT-10, RQ-15, RF-08, RC-09 | full-text |
| Q-14 | FGM 2018 shortest boundary-to-boundary transit (BTZ) | t* = −(ℓ²/r₊) ln(\|ΔV\|/(2ℓ)) (boundary time; boundary metric −dt² + ℓ²dφ²) | ΔV < 0 horizon shift from the quantum stress tensor, perturbative; large and logarithmic for small \|ΔV\|; current | RQ-25 | full-text |
| Q-15 | GJW traversability window | Particle must be sent Δt ≈ R ln(R/(h L_planck)) before the coupling is switched on; eikonal approximation fails beyond (3/2)Δt | AdS₃/BTZ, coupling h; for h ∼ 1, of order the scrambling time. Integrated ANEC value not reproduced numerically; current | RQ-24 | full-text |
| Q-16 | GJW open time | Shorter than the Planck time (proper time) | BTZ, probe regime (Freivogel et al. 2020); current | RT-29, RC-27, RQ-18 | full-text |
| Q-17 | MSY coupling range / information | 0 ≤ g⟨V⟩ < 2π; "can't send more than a few bits"; quanta ≲ const × bits exchanged | Nearly-AdS₂, probe, at or slightly before scrambling time; parametric bound; current | RT-26, RQ-23, RC-16 | full-text |
| Q-18 | Kain static EDM throat radius | R₀/l_P = 75.28 to 498.4 (dimensionless; l_P = 1.616×10⁻³⁵ m) | μ̄ = 0.2, ē/√(4π) = 0.03; Table I values only; current | RF-02, RC-05 | full-text |
| Q-19 | BKR charge-to-mass | Q_e/M > 1; q/μ < 1 (Planck units); closed form M = 2Q_e²r₀/(Q_e² + r₀²), Q_e < r₀ (massless case) | All BKR solutions found; closed form not seen by the checker; current | RQ-13, RE-17 | full-text |
| Q-20 | Ford–Roman single-scale throat bound | r₀ ≲ l_P/f² or l_P/(2f²); for f ∼ 0.01: r₀ ≲ 10⁴ l_P ∼ 10⁻³¹ m (researcher: 5.0×10³ l_P = 8.1×10⁻³² m) (SI) | Massless minimally coupled scalar; flat-space QI at sampling times ≪ curvature radius; f unfixed; the two formulas (eqs 51, 91) rest on different assumptions and were not re-grepped; current | RQ-08, RQ-17 | full-text |
| Q-21 | Ford–Roman thin-band width | a₀ ≲ (r₀/(8f⁴l_P))^{1/3} l_P with f ∼ 0.01: r₀ = 1 m gives a₀ ≲ 10¹⁴ l_P ≈ 10⁻²¹ m (researcher 9.2×10¹³ l_P = 1.5×10⁻²¹ m); r₀ = 1 ly gives ≲ 2×10¹⁹ l_P ≈ 0.2 fm (researcher 3.1×10⁻¹⁶ m); r₀ = 10⁵ ly gives ≲ 10²¹ l_P ≈ 10⁻¹⁴ m (researcher 1.5×10⁻¹⁴ m) (SI) | Same assumptions as Q-20; order of magnitude; current | RQ-08 [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/quantitative_wormhole_tools.py], RC-12 | full-text |
| Q-22 | Pfenning–Ford wall thickness | Δ ≤ 10² v_b L_Planck (α = 1/10); ≈ 1.6×10⁻³³ m at v_b = 1 (SI) | Alcubierre wall, free massless scalar, flat-space QI over sampling short against curvature; bears on throats only through the shared QI; current | RQ-22 [warp-run, re-verified] | full-text |
| Q-23 | Fewster–Eveson Lorentzian QEI | ρ ≥ −27/(2048π²τ⁴) (ħ = c = 1) = 9/64 of the Ford–Roman −3/(32π²τ⁴); SI: −5.2×10⁻²⁷ J/m³ at τ = 1 ns, −5.2×10⁻³ J/m³ at τ = 1 fs | 4D massless free scalar, Minkowski, inertial worldline, Lorentzian sampling; SI restoration by researcher, checked; current | RQ-21 [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/quantitative_wormhole_tools.py] | full-text |
| Q-24 | Ellis throat stress (b₀ = 1 m / 1 km) | ρ = p_l = −4.82×10⁴² Pa / −4.82×10³⁶ Pa; ρ + p_l = −1/(4πb₀²) (geometric) (SI via c⁴/G = 1.2103×10⁴⁴ N) | Φ = 0 Ellis–Bronnikov; calc; current | RQ-19 [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/quantitative_wormhole_tools.py] | calc |
| Q-25 | Ellis radial ANEC integral | I = −E/(8b₀) (geometric, 1/m); −1.51×10⁴³ J/m² per unit E (b₀ = 1 m), −1.51×10⁴⁰ J/m² (b₀ = 1 km) | Radial null geodesic, k^t = E at infinity; direct integral and integration by parts agree; not independently re-derived by the checker; current | RQ-19 | calc |
| Q-26 | Ellis volume integrals | Ω = 2∫(ρ + p_r)4πr²dr = −2b₀ = −2.69×10²⁷ kg (≈ −1.4 M_Jup) for b₀ = 1 m; ∫ρ dV (both sheets) = −b₀ = −1.35×10²⁷ kg (SI) | Visser–Kar–Dadhich coordinate-volume measure r²dr; not the ADM mass (zero for Ellis); current | RQ-19 | calc |
| Q-27 | Morris–Thorne throat radial tension | τ₀ = c⁴/(8πG r₀²) ≈ 5×10⁴¹ dyn/cm² (10 m/r₀)² = 4.8×10⁴⁰ Pa at r₀ = 10 m; 4.8×10⁴² Pa at 1 m; 4.8×10³⁶ Pa at 1 km (SI) | Equals the central pressure of a massive neutron star at r₀ = 3 km (Kuhfittig, preprint survey); current | RQ-19, RE-30 | full-text (Kuhfittig) + calc |
| Q-28 | Morris–Thorne effective mass scale, 1 m throat | b₀c²/(2G) = 6.7×10²⁶ kg = 0.355 M_Jup (6.1×10⁴³ J) (SI); 6.7×10²⁹ kg for 1 km | Order-of-magnitude reading of the mass function, not the exotic-matter amount (shape-dependent). Checks the "about a Jupiter mass for a 1 m throat" lead as an order of magnitude only; the lead itself was not found in any source; current | RE-30 [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/engineering_casimir_anchors.py] | calc |
| Q-29 | Schwarzschild thin-shell wormhole, M = 1 M_☉ (1476.6 m geometric) | σ = −√(1 − 2M/a)/(2πa). a = 3M (4430 m): σ = −2.51×10³⁹ J/m², P = +2.51×10³⁹ N/m, m_s = −6.89×10³⁰ kg (−3.5 M_☉). a = 4M: σ = −2.31×10³⁹ J/m², m_s = −1.12×10³¹ kg. a = 10 km: σ = −1.62×10³⁹ J/m², m_s = −2.26×10³¹ kg (−11 M_☉); shell ANEC = −1.93×10³⁹ J/m² per unit E (SI) | Static shell, Poisson–Visser junction formulae via wormhole_tools; surface NEC just satisfied at a = 3M, violated at 4M; stability ranges not reproduced; current | RQ-20 [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/quantitative_wormhole_tools.py] | calc (abstract for method) |
| Q-30 | Thin-shell stability sign flip | at a₀ = 3M; for a₀ > 3M stable only if β₀² < 0 | Poisson–Visser linearised, radial; current | RT-41 | full-text |
| Q-31 | Ideal Casimir pressure / energy density | P = π²ħc/(240d⁴): 1.30×10⁵ Pa (10 nm), 0.81 Pa (0.2 µm, scaled), 0.0208 Pa (500 nm), 1.30×10⁻³ Pa (1 µm); u = −π²ħc/(720d⁴): −4.3×10⁴ J/m³ (10 nm), −4.3×10⁻⁴ J/m³ (1 µm) (SI) | Perfect conductors, T = 0; textbook formulas, not sourced; real metals give tens of percent less at 0.5 µm; current | RE-30 [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/engineering_casimir_anchors.py] | calc |
| Q-32 | Gap: MT throat tension vs Casimir pressure | 3.7×10³⁷ (b₀ = 1 m vs ideal 10 nm); 3.7×10³¹ (b₀ = 1 km vs 10 nm); ≈ 6×10⁴² (b₀ = 1 m vs 0.81 Pa at the smallest measured gap, 0.2 µm) (dimensionless) | Corrected after check: the 3.7×10³⁷ ratio belongs to 4.8×10⁴² Pa (b₀ = 1 m), not to the 10 m figure placed next to it in RE-30's prose; the script is right. Casimir energy equal to Q-28 at 1 µm would need a cavity volume of 1.4×10⁴⁷ m³ (side 5.2×10¹⁵ m ≈ 35,000 AU); current | RE-30 | calc |
| Q-33 | Measured Casimir force ranges | Bressi: 0.5 to 3.0 µm, coefficient at 15%. Decca: 0.2 to 2 µm, noise 6 fN/√Hz, agreement < 1% in 0.2 to 0.5 µm only (SI) | Parallel plates (Bressi); MEMS torsional oscillator + sphere (Decca); current | RE-29 | full-text (Bressi); abstract (Decca) |
| Q-34 | Strongest directly observed squeezing | 15 dB below vacuum noise (factor 0.032 in noise power) | 3 to 8 MHz, 1064 nm, 16 mW SH pump; noise variance, not J/m³; current; replaces RE-22's [search-summary] "three decades" wording | RE-25 [warp-run, re-verified] | full-text |
| Q-35 | Squeezing in a km-scale GW detector | 6.03 ± 0.02 dB at 6 kHz | GEO 600, medians averaged over 6.3 to 6.5 kHz over two months; equivalent to ×4 circulating power; current | RE-26 [warp-run, re-verified] | full-text |
| Q-36 | Dynamical Casimir boundary speed | "a few percent of the speed of light"; SQUID at ∼11 GHz | Superconducting transmission line; the "0.05c" of the warp run was not in the source and is dropped; current | RE-27 [warp-run, re-verified] | full-text |
| Q-37 | Sycamore experiment scale | 164 two-qubit gates on a nine-qubit circuit; learned Hamiltonian = 7 Majorana fermions, 5 fully commuting terms | Jafferis et al. 2022 abstract; Kobrin et al. description; N = 7 / 5 terms also in Weinstein (secondary). The 9 qubits were chosen as the least noisy of 72; measured fidelity already below ½ of noiseless (secondary preprint arXiv:2301.03522, unknown authors); current | RE-01, RE-03, RQ-12, RF-13, RE-07 | full-text (abstract) |
| Q-38 | Brown et al. WIT hardware fidelity | Quantinuum (6 qubits): about 80% of ideal, unmitigated; IBM (7 qubits): about 20%, about 35% mitigated | Corrected after check: RQ-12 gave "about 80%" for both; current | RQ-12 | full-text |
| Q-39 | Byun et al. 2026 chaotic-SYK hardware run | N = 8, q = 4, J = √2, β = 3, \|μ\| = 12; mutual information I_PT of order 0.01 (plotted up to ∼0.025) | IBM processor; preprint; the 10,000-shot figure is confirmed only for the noiseless emulation; preliminary (preprint) | RE-06, RE-09, RF-15 | full-text |
| Q-40 | SDSS lens-search abundance bounds | Negative mass: n < 10⁻⁸ (10⁻⁴) h³ Mpc⁻³ for \|M\| > 10¹⁵ (10¹²) M_☉, i.e. \|Ω\| < 10⁻⁴. Ellis: n < 10⁻⁴ h³ Mpc⁻³ for throat a = 10 to 10⁴ pc | 50,836 quasars; classical zero-ADM-mass Ellis / negative-mass lens; Ellis number now full-text verified; current | RQ-16, RE-10 | full-text |
| Q-41 | GRB femtolensing bound | n ≲ 10⁻⁹ AU⁻³ for throat a ∼ 1 cm | Yoo et al. 2013, as cited in Takahashi & Asada; not opened; current | RQ-16, RE-11 | full-text (citing paper) |
| Q-42 | Ellis microlensing features | "Gutters" of about 4% just outside Einstein-ring crossing; Galactic microlensing sensitive for throat 100 to 10⁷ km; source radius ≈ 10⁶ km smears smaller lenses | Weak-field Ellis lens; current | RE-11 | full-text |
| Q-43 | S2-orbit wormhole test | Needed 10⁻⁶ m/s²; achieved 4×10⁻⁴ m/s² (2 yr); projected 2×10⁻⁵ m/s² (20 yr); S2 acceleration 1.5 m/s² (SI) | 10⁻⁶ m/s² only if velocity uncertainty reaches 2 km/s; classical through-mouth gravity; current | RE-12 | full-text |
| Q-44 | Triple-system / pulsar improvement | ∼4 orders of magnitude better perturber-mass limit than S2; pulsar ∼10 orders more sensitive | Simonetti et al.; preprint; current | RE-13 | full-text |
| Q-45 | EHT Sgr A* consistency | Image size within ∼10% of Kerr | Mass-to-distance prior; current. 47 to 50 µas shadow diameters unverified | RE-21 | full-text |
| Q-46 | MoEDAL monopole exclusion | 1 g_D ≤ g ≤ 3 g_D, masses up to 75 GeV/c² | Pb–Pb 5.02 TeV per nucleon, 0.235 nb⁻¹, Schwinger production; current. "Up to ∼3.9 TeV for 1 to 10 g_D" is [search-summary], unconfirmed | RE-19 | full-text / search-summary |
| Q-47 | Fastest human-made object | 430,000 mph = 192.2 km/s = 6.41×10⁻⁴ c (SI) | Parker Solar Probe, 24 Dec 2024. The "roughly 600 kg" mass is unsourced and dropped; current | RE-32 [warp-run, re-verified] | full-text |
| Q-48 | Archimedes design signal | Force modulation 5×10⁻¹⁶ N; ∼4×10⁶ s integration; torque ASD 7×10⁻¹³ N/√Hz | **Not re-verified** (carried numbers; source blocked). Status (construction/R&D, no result; room-temperature 50 cm prototype) re-verified at abstract level; preliminary | RE-31 [warp-run; numbers not re-verified] | abstract |
| Q-49 | Andréasson compactness bound | sup 2m/r ≤ ((1+2Ω)² − 1)/(1+2Ω)²: Ω = 1 gives 8/9 (Buchdahl); Ω = 3 (DEC, p ≥ 0) gives 48/49 | ρ ≥ 0, p ≥ 0, p + 2p_T ≤ Ωρ, static spherical; sharp (thin shell); does not apply to negative-σ thin-shell wormholes; current | RT-37 [warp-run, re-verified] | full-text |
| Q-50 | MMP throat tortoise length | J ∼ πL_wh/2 ∼ 2.2×10³⁵ in r_* (abstract: barrier separation 2D ≃ πL_wh ∼ 10³⁵); barriers O(10²) wide (problem's own units, not SI) | Mondal et al. test fields; preprint; preliminary | RF-26 | full-text |
| Q-51 | MMP late-time scalar transmission | Accumulated cross-section → ½ of BH absorption cross-section; short-time σ_r ∼ A(ωr_e)² (scaling unchecked); charged massless fermions ≈ unit transmission at low energy | Freivogel et al. 2026, low frequency, test fields; preprint; preliminary | RC-25, RF-23 | full-text |
| Q-52 | MT tidal criterion vs MM | MT: ≲ 1 g over a 2 m body [search-summary]; naive scaling with 0.5 m and 1 g gives r ≳ 6.8×10⁷ m (SI), vs MM's 20 g → 1.5×10⁷ m | MT 1988 not opened; the scaling treats the criteria as the same estimate, not a derivation from the MT equations; unverified | RT-31, RQ-27, RT-14 | search-summary |

## 3. Contested or conflicting

- [D-C1] **Is the Sycamore experiment gravitational?**
  - Side A (Jafferis et al. 2022; reply arXiv:2303.15423, preprint): the comment agrees on key points (size winding is the mechanism; the system thermalises and scrambles at teleportation time). The objections concern "counterfactual scenarios". All fermions show size winding at 2 ≲ t ≲ 5. A non-commuting perturbation preserves wormhole teleportation.
  - Side B (Kobrin, Schuster & Yao: preprint 2023, published as Nature Matters Arising 643, E17–E19, 23 Jul 2025): the learned Hamiltonian does not thermalise; the signal resembles SYK only for the training operators; perfect size winding appears only because the Hamiltonian is fully commuting.
  - Byun et al. 2026 (preprint) treat the sparsification concern as live and ran a chaotic N = 8 instance.
  - Not resolved. Whether a published reply accompanies the Matters Arising is unknown.
  - Refs: RE-03, RE-04, RE-05, RC-07, RC-08 (unchecked), RF-13, RF-14, RQ-12, RE-06, RF-15.
- [D-C2] **Can Einstein–Dirac(–Maxwell) fields hold a throat open "without exotic matter"?**
  - For: BKR 2021 (D-09); Konoplya–Zhidenko's asymmetric smooth solutions. Dzhunushaliev et al. 2026 (EPJC 86, 240, abstract only) build asymmetric EDM wormholes with identical asymptotics.
  - Against:
    - Bolokhov et al.: definitional; the fields are exotic by the NEC definition.
    - Danielson et al.: the symmetric version is not a solution.
    - Kain 2023: the asymmetric version collapses to black holes, and the static solutions violate the NEC.
    - Weinbaum 2026: no full two-ended solution for positive-frequency Dirac sources; he also says the KZ and Kain solutions used negative-frequency modes.
  - Unreconciled tension, flagged by the critiques researcher: Weinbaum finds Dirac fields can violate ANEC on fixed backgrounds but finds no self-consistent solution; Kain finds NEC-violating static solutions that collapse; neither addresses Dzhunushaliev et al.
  - No reply by BKR or KZ to Kain or Weinbaum was found. The BKR reply to Danielson et al. (EPJC, arXiv:2108.12187) was seen only as an abstract line.
  - Refs: RT-16 to RT-20, RT-38, RC-04 to RC-06, RC-22 to RC-24, RF-01 to RF-03, RF-22, RQ-13, RQ-14, RE-17, RE-18.
- [D-C3] **Self-consistent achronal ANEC: conjecture vs established.**
  - For general validity:
    - Graham & Olum 2007 conjecture it; no known violations.
    - Wall 2010 derives ANEC on null lines from the GSL under auxiliary assumptions.
    - Wald–Yurtsever proofs (2D; 4D with a bifurcate Killing horizon, free scalars).
    - Flat-space proofs (Faulkner et al. 2016; Hartman–Kundu–Tajdini 2017).
    - Kontou 2024: "free of counterexamples in semiclassical gravity".
  - Against or limiting:
    - Urban & Olum 2010 (check: unchecked): a conformally coupled scalar in a conformally flat 3+1D spacetime violates ANEC and achronal ANEC for test fields, "as large as desired". This does not refute the self-consistent version.
    - Wall's theorems fail once linearised gravitons are quantised.
    - Kontou–Sanders list curved-spacetime validity as open.
    - No source proves the self-consistent version in general.
  - Refs: RT-01, RT-02, RT-21 to RT-24, RC-01 to RC-03, RF-10, RF-12, RQ-09.
- [D-C4] **Chronology protection: how strong is the support?**
  - Kay, Radzikowski & Wald 1997 prove that a linear-field QFT breaks down at base points of a compactly generated Cauchy horizon. They present this as "support" for Hawking's conjecture, not proof.
  - Krasnikov 1999 disputes the force of the F-locality assumption. Only a truncated abstract was read: low confidence on his conclusion.
  - Hawking 1992 itself was not retrieved.
  - Refs: RT-27, RC-13 (unchecked).
- [D-C5] **Is MMP traversable for a given signal?**
  - MMP present an eternal traversable wormhole (D-06).
  - Freivogel et al. 2026 (preprint): low-frequency scalars are mostly reflected or trapped on light-crossing timescales, with resonant perfect transmission at some frequencies; charged massless fermions pass with essentially unit probability. So traversability depends on probe and timescale.
  - MMP's own interior is "unstable to large fluctuations in energy" per Bilotta's review.
  - Sadhukhan 2026 (preprints) finds the throat equations consistent only if the fermions respond, including the anomaly trace part "that MMP discard". He finds no growing mode for l ≥ 2 in one sector within an O(α) truncation.
  - Refs: RC-25, RF-23, RF-20, RF-24.
- [D-C6] **Do quantum inequalities hold for squeezed light?**
  - Maclay & Davis 2019 (Found. Phys. 49, 797; single group, unreplicated): a quantum-optics-adapted QI "is violated by most of the experimental data", while the data fit an OPA model.
  - The other side is the standard Ford–Roman / Fewster–Eveson QEIs, which are theorems for free fields (section 4). The adapted inequality is not the Fewster–Eveson bound.
  - No rebuttal or replication was found. No laboratory test of a QEI of the type used in wormhole arguments was found.
  - Refs: RE-33 [warp-run, re-verified], RE-22.
- [D-C7] **Magnetic charge of an MM mouth (internal calculation discrepancy).**
  - RE-15 gives about 1.6×10⁴¹ Dirac charges per mouth (extremal RN in SI electromagnetism).
  - RQ-17 gives q ∼ 10⁸²: integer charge of the dark U(1) from r_e = √(πq) l_p/g₄ with g₄ = 0.1 to 1, flagged "illustrative".
  - These answer different questions (SI Maxwell charge vs dark-sector flux number with an unspecified coupling). Neither is a source figure. A lens that needs the charge must recompute it with the convention stated.
  - Refs: RE-15, RQ-17.
- [D-C8] **Tidal criterion for "humanly traversable".**
  - Morris–Thorne 1988: about 1 g over a 2 m body [search-summary].
  - Maldacena–Milekhin: 20 g for short durations over 0.5 m.
  - The naive scaling (Q-52) gives a throat about 4.5 times larger under the MT-like criterion. This is a choice of criterion, not a factual conflict, but it changes the size anchor.
  - Refs: RT-31, RQ-27, RT-14, RQ-01.
- [D-C9] **"Integrated" NEC violation: what is being integrated.**
  - Visser–Kar–Dadhich 2003: volume-integrated violation can be arbitrarily small.
  - Chakrabarti 2026 (preprint, 4 pages): the volume-integrated null energy "can even be positive".
  - These are volume integrals, not the ANEC line integral along the throat geodesic. They do not conflict with Hochberg–Visser or topological censorship (the frontier researcher's reading). Listed here so later agents keep the two quantities apart (hidden premise 2).
  - Refs: RT-28, RQ-07, RF-29.

## 4. Constraints: theorems, bounds, no-go results, each with its assumptions

**Throat and topology theorems (classical GR)**
- [K-01] **Topological censorship** (Friedman, Schleich & Witt 1993). PROVED.
  - Assumptions: asymptotically flat; globally hyperbolic; ANEC on all inextendible null geodesics; 4D classical GR.
  - Result: every causal curve from J⁻ to J⁺ is deformable to one near infinity. So a traversable wormhole in that class requires ANEC violation along some inextendible null geodesic.
  - Renormalised free-field stress tensors violate ANEC in generic spacetimes (Wald–Yurtsever). The open question is the weaker achronal version.
  - Refs: RT-25.
- [K-02] **Generic throat NEC violation** (Hochberg & Visser). PROVED.
  - Static case (PRD 56, 4745, 1997): minimal-area 2-surface plus flare-out. The NEC is violated at some points on or near the throat, and a weighted throat integral of the NEC must be negative. High-genus throats also violate WEC and DEC.
  - Dynamic case (PRL 81, 746, 1998; gr-qc/9802048): completely non-symmetric, time-dependent throats. Local geometry only, with no asymptotic-flatness assumption.
  - Frame caveat: Brans–Dicke-type splits can hide the violation in the scalar sector, but the total is frame-independent (caveat not checked).
  - Extension: unimodular gravity also needs NEC violation (Pastén et al. 2026, CQG 43, 115014 per INSPIRE; Cataldo et al. 2026, abstract). This adds robustness against that modification only, and says nothing about achronal ANEC.
  - Superseded reference: an earlier version of RT-03 attributed the PRL to gr-qc/9710001 (a conference proceedings paper); corrected after source check.
  - Refs: RT-03, RC-11 (unverifiable: not re-fetched; content matches RT-03), RT-39, RC-29.
- [K-03] **Gao–Wald time-delay theorem** (2000). PROVED.
  - Assumptions: null geodesically complete spacetime; pointwise NEC; null generic condition; any dimension.
  - Result: for any compact K there is a compact K′ such that fastest null geodesics between points outside K′ cannot enter K.
  - Caveats: no control over the size of K′. The authors say a strong "no time advance" interpretation is hard to argue. It does not apply to throats, which violate the NEC; its quantum/ANEC extension is what Graham–Olum and FGM invoke.
  - Gao–Wald Theorem 1 "expresses a key aspect" of the Penrose–Sorkin–Woolgar argument (K-04).
  - Refs: RT-15 [warp-run, re-verified; earlier non-verbatim quote corrected], RC-10.
- [K-04] **Penrose–Sorkin–Woolgar positive-mass theorem** (1993).
  - Based on causal structure: positive energy density focuses and retards null geodesics, while negative total mass would advance them. Uses O(1/r) retardation near infinity and does not look behind horizons.
  - Assumes NEC-type focusing, so it is not a no-wormhole theorem.
  - Transfer to wormholes (researcher's reading): a time advance between asymptotic regions would be in tension with positive ADM mass unless NEC/ANEC fails along the relevant geodesics.
  - Status: arXiv preprint (no journal ref on INSPIRE). The Schoen–Yau/Witten proof was not re-opened and is not carried.
  - Refs: RT-36 [warp-run, re-verified].
- [K-05] **Olum 1998: superluminal travel requires negative energy.** PROVED.
  - Definition: a path that reaches a destination surface earlier than any neighbouring path.
  - Assumptions: classical GR; the generic condition on P (holds if there is any normal matter or transverse tidal force on P); no singularities.
  - Result: WEC is violated somewhere on P.
  - Transfer (researcher's reading; Olum does not mention wormholes): a wormhole shortcut beats paths in another homotopy class, and a throat already violates the NEC, so the theorem does not by itself exclude a wormhole shortcut.
  - Olum also says the Tipler/Hawking theorems (no CTCs from a compact region without WEC violation or a singularity on the boundary) are separate results. Extending his theorem to CTC regions is "not easily accomplished".
  - Refs: RT-33, RT-34 [warp-run, re-verified].
- [K-06] **Visser–Bassett–Liberati 2000, "superluminal censorship"** (conference proceedings, "we argue").
  - In linearised gravity about Minkowski space, the NEC makes the Shapiro effect always a delay, never an advance.
  - They state that wormhole effective FTL "necessarily involves NEC violations", citing rigorous theorems (K-01, K-02).
  - Caveat: lensing voids can give an advance relative to an FRW background without NEC violation.
  - Refs: RT-35 [warp-run, re-verified].

**Energy conditions in quantum field theory**
- [K-07] **Achronal ANEC family.** The crux.
  - (a) Self-consistent achronal ANEC (Graham–Olum 2007): a CONJECTURE. It is claimed sufficient to rule out CTCs and wormholes connecting different asymptotically flat regions. Semiclassical regime only.
  - (b) Wald–Yurtsever: PROVED for minimally coupled free scalars in curved 2D, or in 4D with a bifurcate Killing horizon.
  - (c) Wall 2010: PROVED that ANEC on null lines follows from the GSL for causal horizons, for quantum fields minimally coupled to semiclassical Einstein gravity. Auxiliary assumptions: CPT; a renormalisation scheme for generalised entropy; extra-strong cosmic censorship; horizons persisting under perturbation (the assumptions beyond the first two were not checked). Fails once linearised gravitons are quantised.
  - (d) Flat-space ANEC:
    - Faulkner–Leigh–Parrikar–Wang 2016: general argument from relative-entropy monotonicity, assuming a well-defined continuum limit; Minkowski space and static bifurcate Killing horizons.
    - Hartman–Kundu–Tajdini 2017: from causality, for unitary Lorentz-invariant QFTs with an interacting UV fixed point; Minkowski only.
  - (e) Test-field counterexample: Urban–Olum 2010 (see D-C3).
  - (f) Long wormholes have no complete achronal null geodesic through them, so (a) does not constrain them (Kontou 2024; MMP's ANEC-violating null lines are chronal).
  - Refs: RT-01, RT-02, RT-21, RT-22, RT-23, RT-24, RC-01 to RC-03, RF-11, RF-12, RQ-09.
- [K-08] **Ford–Roman 1996 QI constraint on wormholes.**
  - Assumptions: massless minimally coupled free scalar in 4D; flat-space Lorentzian-sampled QI applied on scales much smaller than the local curvature radius and the distance to boundaries; sampling ratio f ∼ 0.01, unfixed; static spherically symmetric Morris–Thorne geometry.
  - Result: either the throat is barely above the Planck length, or negative energy sits in a band many orders thinner than the throat (Q-20, Q-21). The authors call macroscopic wormholes "very improbable".
  - Other fields are argued, not derived. Loopholes the authors name: fields with large coefficients in a tiny region; superposed effects.
  - Refs: RQ-08, RC-12, RT-30 (unverifiable as a separate claim; covered by RQ-08).
- [K-09] **Fewster–Eveson 1998 QEI.** PROVED.
  - Assumptions: free real scalar of mass m ≥ 0 in d-dimensional Minkowski space; any smooth, even, non-negative sampling function; inertial observer.
  - Bounds how negative and for how long (Q-23). It does not bound ANEC.
  - Using it in curved space needs sampling times short against curvature radii.
  - Refs: RQ-21.
- [K-10] **Pfenning–Ford 1997 thickness bound.** Same scalar-field flat-space QI, with sampling short against both curvature and the time over which bubble velocity changes; α = 1/10 (Q-22). Warp-specific energy figures are not carried. Refs: RQ-22 [warp-run, re-verified].
- [K-11] **Kontou–Sanders: all pointwise conditions fail in QFT.** Essentially any QFT violates every pointwise energy condition, so pointwise NEC violation at a throat is not by itself exotic in the QFT sense. Refs: RT-24.

**Chronology**
- [K-12] **Chronology protection.**
  - Hawking 1992: CONJECTURE (not retrieved).
  - Kay–Radzikowski–Wald 1997: PROVED. Assumptions: linear (scalar) QFT; a spacetime with a compactly generated Cauchy horizon; the F-locality / Hadamard criterion. Result: no extension of the field algebra satisfies F-locality at base points of the horizon. Interpreted as support only. Manufacturing a time machine would require at least entering a regime where quantum gravity dominates.
  - Time-machine models (Kim–Thorne, Gott, Grant) contain self-intersecting null geodesics.
  - Morris–Thorne–Yurtsever 1988, Kim–Thorne 1991 and Frolov–Novikov 1990 were not retrieved.
  - Refs: RT-27, RC-13.
- [K-13] **Everett–Roman 1997** (Krasnikov tubes; transfer to wormholes is the researcher's inference).
  - A single tube has no CTCs; two non-overlapping tubes make a time machine.
  - Tubes, warp bubbles and traversable wormholes all need unphysically thin layers of negative energy and large total negative energy.
  - The warp-only control objection does not apply to a throat.
  - Refs: RC-31 [warp-run, re-verified].
- [K-14] **Finazzi–Liberati–Barceló 2009** (semiclassical instability).
  - For dynamical superluminal warp metrics with horizons, the renormalised stress tensor grows exponentially at the front wall.
  - It bears on a wormhole shortcut only if that shortcut creates an effective horizon or chronology boundary, which is not shown. MMP and MM are designed as non-shortcuts and are outside the result.
  - Refs: RC-32 [warp-run, re-verified; transfer medium confidence].

**Payload and information bounds**
- [K-15] **MSY information bound.** Nearly-AdS₂ (JT) with a boundary double-trace coupling, probe regime, parametric: quanta passed ≲ const × bits exchanged to set up the coupling (Q-17). Refs: RT-26, RQ-23, RC-16.
- [K-16] **Freivogel et al. 2020.** BTZ, probe regime, quantum metric fluctuations deferred: no reliable transfer for horizons ∼ the AdS radius; for large horizons, quanta of order the horizon area in AdS units. Refs: RT-29, RC-27.
- [K-17] **Andréasson compactness bound** (Q-49).
  - Assumptions: static, spherically symmetric; ρ ≥ 0, p ≥ 0, p + 2p_T ≤ Ωρ.
  - Does NOT apply to Visser thin-shell wormholes, whose σ₀ < 0 (D-14). It bears only on positive-energy shells added near a throat (a payload) and on horizon formation when positive mass piles up there (researcher's reading, checked as following from the hypotheses).
  - Refs: RT-37 [warp-run, re-verified], RT-41.

**No-go results for specific supports**
- [K-18] **Kanai, Maeda & Yoshida 2025/26** (PRD 113, 064026 per INSPIRE; status corrected from "preprint" to peer-reviewed per the check note).
  - Traversable wormholes cannot arise perturbatively from near-extremal Reissner–Nordström (4D) or equal-angular-momenta Myers–Perry (5D) black holes through higher-derivative EFT corrections, whatever the correction terms, because enhanced near-horizon symmetry constrains the effective stress tensor.
  - Escapes: Casimir energy (as in MMP) or reduced symmetry.
  - Scope: perturbations of those near-horizon geometries; EFT corrections only.
  - Refs: RC-20, RF-25.
- [K-19] **Weinbaum 2026 numerical obstruction** (D-12). Einstein–Dirac; static, spherical, asymptotically flat; definite frequency, angular momentum and parity; positive-frequency single-particle Dirac sources. Numerical, not a theorem. Refs: RT-38, RC-23, RF-22.
- [K-20] **Jiang et al. 2026** (PRD 114, 025001 per INSPIRE).
  - Fixed zero-tidal wormhole background; non-minimally coupled massive scalar; Hadamard renormalisation; not self-consistent.
  - Two intervals of scalar mass m₀ cannot satisfy the Morris–Thorne conditions for any coupling ξ. Three disconnected regions of (m₀, ξ) can.
  - Abstract-level reading.
  - Refs: RC-30.
- [K-21] **Visser–Kar–Dadhich 2003.**
  - Static spherical examples: the volume-integrated NEC-violating stress can be made arbitrarily small.
  - This does not remove the need for ANEC violation, and says nothing about cost, tidal limits or achronality.
  - The authors liken topological censorship to the area-increase theorem rather than the positive-mass theorem.
  - Refs: RT-28, RQ-07.
- [K-22] **MM UV-cutoff species bound.** N_f < M_pl²/TeV² ∼ 10³². This is a Bekenstein-like expectation for a local field theory with a TeV cutoff, not a theorem. It excludes the free-fermion humanly traversable version (Q-03). Refs: RT-13, RQ-04.

**Not retrieved, but named in the brief:** the topology-change theorems (Geroch 1967; Tipler 1977), Kontou–Olum 2015, and the Ford–Roman thin-band derivations beyond what RQ-08 quotes. See section 6.

## 5. Frontier and speculative (labelled; not established)

Newest first where dated.
- [F-01] **Sadhukhan 2026: MMP linear stability** (arXiv:2609.33511, Sep; arXiv:2610.09847, v1 7 Oct 2026, the only item found dated after 2026-10-01). Single-author preprints. PRELIMINARY.
  - The throat equations are consistent only if the fermions respond, through the full 2D anomaly stress tensor with an induced Hall current.
  - In the axial-metric/polar-gauge sector the response is the Schwinger current, giving the electric field a screening mass. "Within the O(α) truncation the sector has no growing mode for l ≥ 2."
  - Assumptions: q ≫ 1, l ≪ √q, lowest Landau level only.
  - The full perturbation problem is not complete in what was read.
  - Refs: RF-24, RE-34.
- [F-02] **Chakrabarti 2026** (preprint, 4 pages): the volume-integrated null energy can be positive despite throat NEC violation. Not the ANEC line integral (D-C9). Refs: RF-29.
- [F-03] **Junior et al. 2026** (preprint, abstract only): "black bounce" regular black holes and wormholes with ordinary bulk matter and "the necessary exoticity confined to an infinitesimally thin defect". The NEC violation is concentrated in a shell, not removed. Blázquez-Salcedo et al. 2026 (preprint, abstract only): nonradial QNMs of phantom-supported charged Ellis–Bronnikov wormholes. Refs: RF-30.
- [F-04] **Freivogel et al. 2026, "How traversable is a traversable wormhole?"** (preprint): see D-C5 and Q-51. Refs: RC-25, RF-23.
- [F-05] **Byun, Kim & Lee 2026** (preprint): first hardware run of the wormhole-teleportation protocol with an explicitly chaotic Hamiltonian (Q-39). In their convention μ < 0 "corresponds to ANEC violation and hence to traversability" in the holographic reading. A PRA publication was suggested by a search result but not opened. Refs: RE-06, RE-09, RF-15, RF-16.
- [F-06] **Djogama et al. 2026** (preprint, abstract only): fermionic double-trace traversable wormhole in two-sided near-horizon near-extremal Kerr (Kerr/CFT). With Bilotta 2023 (preprint; bosonic, nNHEK), these are the two Kerr-based constructions. Both are perturbative and two-sided, and neither addresses a 4D asymptotically flat non-perturbative solution. Refs: RF-28 (unverifiable), RF-10.
- [F-07] **Lu, Yang & Zheng 2026** (preprint): the GJW protocol in AdS₂ as a quantum channel. Its capacity is governed by the time derivative of an OTOC and bounded by the Einstein-gravity (chaos-bound) limit, "a natural benchmark for quantum simulations". The rough bound |p₊|Δp₊ ≲ |a₊|/G_N ∼ g and "one-shot" were not checked. Refs: RF-27.
- [F-08] **Altunkaynak & Tuncer 2025** (preprint, low confidence): throat-area monotonicity for NEC-obeying signal matter after a GJW-type window, and a proposed Q_max ≤ A_min/(4G_N) qubits. The paper says the area statement follows from the standard Raychaudhuri equation. Not compared with MSY or Freivogel et al. If right, a payload of ordinary matter cannot widen a throat. Refs: RT-40.
- [F-09] **Mondal et al. 2025** (preprint): MMP echoes. The throat is enormously long in tortoise coordinate (Q-50), so echo delays are set by that length, not by the mouth's light-crossing time. The numerical delay and amplitude were not read. Refs: RF-26.
- [F-10] **Liu & Miao 2025; Ahn et al. 2024**: further AdS double-trace wormholes. [search-summary] Refs: RF-18.
- [F-11] **Speculative classical solution-generating work**: Avalos et al. 2025 (hyperbolic Casimir-like wormhole, EPJC 85, 793) and Garattini et al. 2024 (wormhole–warp correspondence, JCAP). Both assume a stress tensor of the required sign. SPECULATIVE; abstracts only, unverifiable. Refs: RF-19.
- [F-12] **Le 2026** (preprint, several large revisions): the S-lemma writes NEC, WEC and SEC as 4×4 linear matrix inequalities, "observer-robust". It could certify NEC violation at a throat for all null directions, but it has been applied to warp bubbles only; this run has not applied it to a wormhole. Refs: RF-31 [warp-run, re-verified; warp-specific results not carried].
- [F-13] **Kontou 2024: Casimir-plate stabilisation and spontaneous tunnelling production.** Mentioned as speculative, without details (original source not identified). Refs: RF-11.
- [F-14] **EDM observational predictions** (Churilova et al., JCAP 2021; Stuchlik et al., EPJ Plus 2021): QNMs, echoes, shadows and QPO frequencies for "wormholes without exotic matter". These are model predictions for hypothetical objects whose premise is now doubtful (D-11, D-12). Abstract only, unverifiable. Refs: RF-04.
- [F-15] **Emparan, Grado-White, Marolf & Tomasevic 2021** (JHEP 05, 032; peer-reviewed but frontier): multi-mouth quantum-supported 4D wormholes (fundamental group F₂ for three mouths). Asymptotically flat "up to ... magnetic fluxes or cosmic strings". No creation mechanism or payload analysis. Refs: RF-09.
- [F-16] **MM's "secret signals or qubits" use** for a small wormhole with mouths in one system. A speculative remark bearing on hidden premise 4, not a calculation. Refs: RF-07.
- [F-17] **Archimedes** (INFN, Sos Enattos): planned weighing of vacuum energy in layered superconductors. Construction/R&D stage, no result. It would test whether a condensed-matter Casimir term gravitates, an input to Q2. Design numbers are not re-verified (Q-48). Refs: RE-31 [warp-run, numbers not re-verified].
- [F-18] **Shapoval et al. 2023** (Quantum 7, 1138) and **Weinstein 2023**: pointers on quantum-processor gravity tests; abstract snippets only. Refs: RF-17.
- [F-19] **Technology-readiness estimates (researcher's judgement, [search-summary], low confidence):**
  - Quantum-processor wormhole-inspired teleportation: TRL about 3–4 as a lab simulation, TRL 1 as a quantum-gravity test.
  - Astronomical searches: instruments at TRL 6–9, but null, and sensitive only to classical Ellis/negative-mass or horizon-replacement models.
  - Creating or widening any wormhole: TRL 0–1.
  - RE-24's "largest engineered mass ∼10⁵ kg" anchor is unsourced and was corrected by the researcher: the MM mouth mass is at least about 26 orders above any engineered object (10⁸ kg is the unsourced upper end).
  - Refs: RE-24.

## 6. Unknowns and gaps, with the papers to request

**Papers to request (deduplicated)**
- doi:10.1119/1.15620 | Morris & Thorne 1988, "Wormholes in space-time and their use for interstellar travel" (Am. J. Phys. 56, 395) | The 1 g tidal criterion, the throat-size and tension figures, and whether the "about a Jupiter mass for a 1 m throat" figure appears in it (D-C8, Q-28, Q-52).
- doi:10.1038/s41586-022-05424-3 | Jafferis et al. 2022, "Traversable wormhole dynamics on a quantum processor" | Fidelity, the magnitude of the sign-dependent asymmetry, and the Shapiro-delay numbers of the Sycamore run (D-16, D-C1). The OSTI copy returned HTTP 429.
- doi:10.1103/PhysRevD.46.603 | Hawking 1992, "Chronology protection conjecture" | Hawking's exact argument (divergent stress tensor at the chronology horizon) and its assumptions (K-12, D-C4).
- doi:10.3390/physics2010001 | "Progress in a Vacuum Weight Search Experiment" (Archimedes, 2020) | Re-verify the 5×10⁻¹⁶ N design force and 4×10⁶ s integration (Q-48).
- doi:10.1051/epjconf/202531909003 | "Exploring Vacuum-Gravity Interaction through the Archimedes Experiment: Recent Results and Future Prospects" | Current Archimedes sensitivity and schedule (F-17).

**Missing quantities and unread sources**
- **ANEC values for the perturbative constructions.** GJW, Maldacena–Qi, MMP and FGM 2018 ANEC integrals were not reproduced numerically. Only structural statements and the Ellis and thin-shell values were computed (Q-24, Q-25, Q-29). The constraints lens owns this.
- **Classical papers not retrieved:**
  - Morris–Thorne–Yurtsever 1988, Kim–Thorne 1991, Frolov–Novikov 1990 (time-machine conversion: the mechanist lens has no sourced mouth-motion numbers);
  - Visser 1989 and Visser's 1995 book;
  - Geroch 1967 and Tipler 1977 (topology change);
  - Hawking 1992.
  - Thin-shell negative σ is sourced only for the Schwarzschild case (Poisson–Visser).
- **Not fetched:** Kontou–Olum 2015; the Ford–Roman thin-band derivations beyond the quoted results; Urban–Olum's violation magnitude.
- **Unconfirmed journal refs:** Maldacena–Qi, FGM 2018 (CQG 36, 045006 per INSPIRE only), Kain 2023 (RT-18 vs RC-05), Weinbaum 2026, Pastén 2026, Kanai 2026, Kain 2026, Simonetti et al., the LVK O3 echo paper (arXiv:2309.01894).
- **EDM debate:**
  - the BKR reply to Danielson et al. (arXiv:2108.12187) and Dzhunushaliev et al. 2026 (arXiv:2510.03656) were not opened;
  - whether Weinbaum's static no-go covers the Maxwell-coupled and asymmetric branches was not read;
  - no BKR or KZ reply to Kain or Weinbaum was found;
  - the physical throat size of EDM wormholes for electron-like fermions was not computed.
- **Payload energy:** no source gives the energy needed to pass a 1 kg or 70 kg payload through a given throat. Payload back-reaction is sourced only qualitatively: positive-energy infall closes the throat (D-13; RC-19; Kain 2026).
- **Creation routes:**
  - Garfinkle–Strominger pair creation of magnetic black holes: no rate retrieved;
  - no formation mechanism for MM wormholes in any source (the authors say so);
  - no sensitivities retrieved for magnetic-black-hole searches (Parker bound, MACRO, IceCube).
- **Tests:**
  - no dedicated survey search for Ellis-wormhole microlensing events (OGLE/MOA/EROS) was found;
  - the Cramer et al. 1995 predictions were not located;
  - the Abedi et al. echo claim is [search-summary] only;
  - no experiment targets MM-type extremal magnetic mouths;
  - no squeezed-light negative energy density in J/m³ or its extent is available, so the only computed lab gap is the Casimir one (Q-32);
  - no laboratory QEI/QNEC/ANEC test beyond Maclay–Davis;
  - the reply to the 2025 Matters Arising and the peer-reviewed status of the Su et al. IBM/Quantinuum experiment are unknown;
  - Brown et al. "Quantum Gravity in the Lab II" (arXiv:2102.01064) was abstract only.
- **Frontier:**
  - Freivogel et al. 2026 and Sadhukhan 2026 are unrefereed;
  - the stability verdict of Sadhukhan's first paper (abstract text after "With both effects included") was not read;
  - no 2023–2026 proof or refutation of the self-consistent achronal ANEC in 4D gravity;
  - no update to the MSY/Freivogel information bounds;
  - arXiv rate limits left the 2024–2026 hep-th sweep incomplete.
- **Method gap (theory facet):** no paper applies Olum 1998 to wormholes between mouths in different homotopy classes (K-05 transfer is the researcher's reading).
- **What transfers from AdS and 2D to 4D asymptotically flat spacetime** (hidden premise 11) is addressed only by the constructions' own scope statements. No source treats it directly.

## 7. Source-quality notes

**Inputs and coverage**
- All five facets in the brief are present, each with a check file: theory, quantitative, critiques, engineering, frontier. No facet is missing.
- Raw claims: 164 (RT 41, RQ 25 (no RQ-10 or RQ-11), RC 33, RE 34, RF 31). After merging duplicates across facets they map to 27 established items, 52 anchors, 9 contested items, 22 constraints and 19 frontier items.

**Superseded values and what replaced them**
- Kobrin–Schuster–Yao critique: the arXiv preprint (2302.07897, 2023) is now published as Nature Matters Arising 643, E17–E19 (23 Jul 2025, RE-05). The published version is the anchor for that side of D-C1. The preprint's wording is retained only where the published abstract is silent. This is the same critique, so it is not counted twice.
- Squeezing: RE-22's [search-summary] "about −15 dB over three decades" is replaced by Vahlbruch et al.'s 15 dB at 3–8 MHz (RE-25, Q-34).
- Dynamical Casimir: the warp run's "∼0.05c" is replaced by the source's "a few percent of the speed of light" (RE-27, Q-36).
- GEO 600: the warp run's "all GW observatories since 2019" remark was dropped as not re-verified (RE-26).
- Maclay–Davis: RE-33 [warp-run] supersedes RE-22's low-confidence label for the QI statement only.
- Hochberg–Visser journal ref: corrected from gr-qc/9710001 (proceedings) to PRL 81, 746 / gr-qc/9802048 (RT-03).
- Gao–Wald: an earlier non-verbatim "K′ far larger" quote was replaced by the verbatim p. 5 and p. 10 sentences (RT-15).
- First dossier: `superseded/dossier.v1.md` is replaced by this file. It lacked the warp-run carry-overs and the relaunch additions (RC-22 to RC-33, RE-25 to RE-34, RF-22 to RF-31, RQ-19 to RQ-27, RT-33 to RT-41).
- No measurement in this dossier is a re-analysis of the same data as another. Distinct results on related apparatus:
  - Byun et al. 2026 (IBM) and Brown et al. (IBM/Quantinuum) are independent hardware runs of the same protocol family as Sycamore, so the statistician should treat them as related but not the same data.
  - Kain 2023 and Kain 2026 share an author and numerical method on different wormhole families.

**Dropped (contradicted)**
- No claim was contradicted by any checker, so none was dropped on that ground.
- Removed as unsourced or not in the source:
  - the Parker probe "roughly 600 kg" mass (RE-32);
  - the "∼0.05c" DCE figure (RE-27);
  - the "largest engineered mass ∼10⁵ kg" anchor (RE-24, corrected by its own researcher).

**Corrected (misattributed / scope / status)**
- RQ-12: the about 80% WIT fidelity is Quantinuum only; IBM is about 20% (about 35% mitigated).
- RQ-14: BKR's negative ADM mass applies near the critical line, not to smooth solutions generally.
- RC-20: STATUS inconsistency (text said preprint) resolved to peer-reviewed per INSPIRE (PRD 113, 064026).
- RC-22: Danielson et al. also argue non-smoothness, so they overlap Konoplya–Zhidenko rather than being wholly different.
- RC-23/RC-24: Weinbaum's critique also covers the KZ and Kain 2023 solutions (negative-frequency modes).
- RE-29: Decca's < 1% agreement applies to 0.2–0.5 µm only.
- RE-30: the 3.7×10³⁷ ratio belongs to b₀ = 1 m, not the 10 m tension in the same sentence.
- RE-23: the PRD 60, 111101 year is 1999, not 2000.
- RT-07: the low-confidence flag was lifted; the checker read eqs 5.30–5.31 correctly.
- RT-11 / RF-08: the "prohibition" on fastest causal curves is "general arguments (GSL)", not a theorem; "no shortcut" holds as "approaches the minimum".
- RC-16: the MSY bound is parametric.
- RF-22 / RT-38 / RC-23: Weinbaum's "peer-reviewed" status rests on INSPIRE and was not seen by the frontier checker.

**Unverifiable or unchecked, kept with labels**
- Unverifiable: RT-20, RT-30, RT-31, RT-32, RQ-27, RC-11, RC-15, RC-19, RC-21, RE-08, RE-09, RE-19 (part), RE-22, RE-23 (part), RE-24, RE-31, RE-34, RF-04, RF-17, RF-18, RF-19, RF-28, RF-29 (Pastén half), RF-30.
- Not checked by the critiques checker: RC-02, RC-03, RC-08, RC-13. These are full-text claims marked "unchecked" where cited. RC-03 (Urban–Olum) is load-bearing for D-C3 and should be confirmed before heavy use.

**Share resting only on search summaries**
- 6 of 164 raw claims (3.7%) rest entirely on search summaries: RT-17, RT-31, RT-32, RQ-27, RE-24, RF-18.
- 5 more (RE-09, RE-19, RE-21, RE-22, RE-23) have one component that is search-summary only. Including those, 11 of 164 (6.7%).
- No load-bearing quantitative anchor rests only on a search summary, except Q-52 (the MT tidal criterion), which is labelled.

**Fringe and speculative**
- No fringe source was used as evidence.
- The Maclay–Davis QI-violation claim is peer-reviewed but single-group and unreplicated, so it is kept as contested (D-C6), not established.
- Speculative ingredients are labelled where they occur: RS II, the dark U(1), 10⁵² species, phantom fields, and modified-gravity Casimir-like solutions.

**Claims carried from earlier runs**
- All carried claims come from one run: 2026-10-01-warp-drive-without-negative-energy. There are 18 claims with a PRIOR line:
  - theory 6: RT-15, RT-33, RT-34, RT-35, RT-36, RT-37;
  - quantitative 1: RQ-22;
  - critiques 3: RC-31, RC-32, RC-33;
  - engineering 7: RE-25, RE-26, RE-27, RE-28, RE-31, RE-32, RE-33;
  - frontier 1: RF-31.
- Re-verified: 17 of 18.
  - RT-34's PRIOR line records "new quote this run" rather than the word "re-verified", but the checker verified its quotes.
  - RE-31 is re-verified only at abstract level for its status. Its design numbers (Q-48) are not re-verified and are weighted accordingly.
- RE-29 and RE-30 carry "PRIOR: new this pass" lines: they are new, not carried, and are not counted.
- RQ-08 and RQ-21 re-found the Ford–Roman and Fewster–Eveson material in the primary sources without PRIOR lines, so they count as this run's claims.
- How the warp-run evidence entered: following the toolkit rules, this compiler did not read `prior/` directly. Warp-run evidence enters only through the researchers' re-verified carry-overs above, as the brief's relaunch facet scopes direct. Warp-only material was deliberately not carried by the researchers: Natário and Santiago–Schuster–Visser theorems (except RC-33's method point), warp-bubble energy budgets, and Lentz/Fuchs shells.
