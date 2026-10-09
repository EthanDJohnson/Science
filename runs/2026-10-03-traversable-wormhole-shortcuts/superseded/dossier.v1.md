# Dossier: Traversable wormholes: shortcuts, negative energy, and what holds them open

Compiled 2026-10-04 from `research/{theory,quantitative,critiques,engineering,frontier}.md` and their five `.check.md` files. All five facets were source-checked.

**Units.** Where the source does, formulas use geometric units (G = c = 1) or natural units (hbar = c = 1, l_p = sqrt(G_4)). Numbers stated in SI are marked. "Status" gives the publication status, with the checker's verdict in brackets where it matters.

**Access labels.** Every item carries the ACCESS label of its weakest load-bearing source claim:
- **FT:** full-text;
- **AB:** abstract;
- **SS:** search-summary.

A claim the checker could not confirm is marked **[unverified]**.

---

## 1. Established

### 1a. General results on energy conditions

- [D-01] Essentially every quantum field theory violates all the pointwise energy conditions (NEC, WEC, SEC, DEC). Of the standard conditions, the achronal ANEC (AANEC) "comes closest to being generally valid". Whether AANEC holds in curved spacetime is listed as an open question. (refs: RT-24) textbook-or-review, FT.
- [D-02] Quantum fields violate plain (non-achronal) ANEC: a quantum scalar in Minkowski space compactified in one direction does, and so does one around a Schwarzschild black hole. In both cases the violating null geodesics are chronal, not achronal. Kontou (2024) sorts all known ANEC violations into three kinds:
  1. on chronal null geodesics;
  2. in backgrounds that are not self-consistent;
  3. at the Planck scale.

  (refs: RT-01, RC-02, RQ-09) peer-reviewed / review, FT.
- [D-03] In a static wormhole, NEC violation does not by itself make the wormhole traversable. Kain's static Einstein–Dirac–Maxwell (EDM) solutions violate the NEC but are not traversable once evolved in time (see D-17). (refs: RT-18, RC-06) peer-reviewed, FT.

### 1b. Two-sided holographic constructions (AdS, JT gravity)

- [D-04] **Gao–Jafferis–Wall (GJW).**
  - Setting: an eternal BTZ black hole (AdS3, so a 2+1D bulk). A double-trace interaction couples the two boundary CFTs.
  - What holds it open: a one-loop quantum matter stress tensor with negative averaged null energy, whose back-reaction makes the Einstein–Rosen bridge traversable.
  - ANEC violation is a prerequisite for traversability.
  - With the boundaries decoupled, "no signal can be transmitted between the boundaries through the bulk". At linear order the averaged null energy is i·ε⟨[∫dU T_UU, A]⟩, which vanishes for the thermofield-double (TFD) state.
  - Shortcut: the authors state it "cannot be used to violate causality". It is two-sided, with no shared ambient space, so the comparison channel is the boundary coupling itself.

  (refs: RT-04, RT-05, RC-15) peer-reviewed (JHEP 12 (2017) 151), FT.
- [D-05] **Maldacena–Stanford–Yang (MSY 2017), nearly-AdS2.**
  - "We cannot send a signal through the wormhole faster than we can send it through the outside" is how they state the general-relativity prohibition.
  - Back-reaction ensures "we cannot send more information through the wormhole than the information we have to send in order to set up the interaction". The channel depends on g only through exp(−i g⟨V⟩), with 0 ≤ g⟨V⟩ < 2π, so only "a few bits" can pass.
  - Checker's note: Sec. 2.5 calls these bounds "parametric" only, so this is not a sharp cap.

  (refs: RT-26, RC-16) peer-reviewed (Fortsch. Phys. 65, 1700034), FT.
- [D-06] **Freivogel, Galante, Nikolakopoulou & Rotundo 2020 (BTZ, probe regime).**
  - The GJW wormhole is open for a proper time shorter than the Planck time, yet signal transmission "can sometimes remain within the semiclassical regime".
  - For horizons of order the AdS radius, information "cannot be reliably sent". Large black holes (horizon ≫ AdS radius) allow more.
  - Kontou's 2024 restatement of the Planck-time point (RQ-18) cites an unidentified ref. [78]. This dossier relies on the primary paper.

  (refs: RT-29, RQ-18) peer-reviewed (JHEP 01 (2020) 050), FT.
- [D-07] **Maldacena–Qi 2018, eternal traversable wormhole.**
  - Setting: nearly-AdS2 (JT gravity), or two coupled SYK systems.
  - What holds it open: negative null energy from quantum fields under an external coupling between the two boundaries. A large number N of fields is needed for control.
  - Integrated null energy: ∫dX⁺ T_{X⁺X⁺} = −2φ_r < 0, forced because the dilaton grows towards both boundaries. This is the 2D special case of topological censorship. A finite amount of negative energy suffices.
  - Two-sided.

  (refs: RT-08) arXiv preprint confirmed; journal reference unverified; FT.

### 1c. Four-dimensional constructions held open by quantum fields

- [D-08] **Maldacena–Milekhin–Popov (MMP), "Traversable wormholes in four dimensions".**
  - Setting: 4D Einstein–Maxwell plus charged massless fermions. Two oppositely magnetically charged, near-extremal black holes are joined by a long wormhole.
  - What holds it open: a negative, Casimir-like null–null stress from the fermions' lowest Landau level along the magnetic field lines.
  - ANEC is violated along null lines that wrap the field-line circle. "Of course, these null lines are not achronal."
  - Shortcut: no. It is "a long wormhole that does not lead to causality violations in the ambient space". The authors define "long" as taking longer through the wormhole than through the ambient space, and say short wormholes "are not allowed by the Einstein equations combined with the achronal average null energy condition".
  - Traveller's proper time is of order r_E ~ q, against π·ℓ ∝ q² seen from outside.
  - Standard Model embedding: possible only if the overall size is small compared with the electroweak scale ("say 1/TeV", about 2e-19 m, SI). Standard Model fermions then act like N_f = 54 charge-one flavours.
  - Energy budget (natural units): E = r_e³/(G_N l²) − q/(8l). This is minimised at l = 16 r_e³/(G_N q), giving E_min = −G_N q²/(256 r_e³). The checker confirmed these values by hand. The research file's "quote" of them is a paraphrase, so cite them as equations 5.30–5.31, not as a quote.

  (refs: RT-06, RT-07, RC-17, RE-16, RF-20) peer-reviewed (CQG 40, 155016, per RT-06), FT.
- [D-09] **Fu–Grado-White–Marolf 2018.**
  - Setting: Z2 quotients (globally hyperbolic quotients of spacetimes with bifurcate Killing horizons).
  - These become traversable through first-order back-reaction of quantum fields in Hartle–Hawking-type states, "even when sourced by only a single scalar quantum field" (checker).
  - The traversal window grows towards extremality, which "suggests" a self-supporting eternal wormhole.
  - The negative ∫dU⟨T_kk⟩ runs along non-contractible cycles, so the construction needs quotient topology.

  (refs: RT-09) journal reference unverified; FT.
- [D-10] **Fu–Grado-White–Marolf 2019.**
  - Setting: 4D, asymptotically flat (Λ = 0). Oppositely charged black holes held apart by a cosmic string, with quantum fields in Hartle–Hawking states and perturbative back-reaction.
  - Transit time: the minimum is t_min = d + logs (c = 1, d the mouth separation). This is shorter than for MMP by more than a factor of 2, and "approaches the value that, at least in higher dimensions, would be the theoretical minimum".
  - Shortcut: no. t_min/d → 1; it approaches the exterior light time and does not beat it.
  - Stability:
    - traversability is "exponentially fragile";
    - an arbitrarily small back-reaction can open the wormhole "at least for some period of time", so it is transient;
    - the background is unstable, with the black holes falling together on a time of order d^{3/2} (G = c = 1).

  (refs: RT-10, RT-11, RQ-15, RC-09, RC-21, RF-08) peer-reviewed (CQG 36, 245018), FT.
- [D-11] **Emparan, Grado-White, Marolf & Tomasevic 2021.** Extends D-10 to multi-mouth wormholes; the three-mouth case has fundamental group F_2. The solutions are asymptotically flat "up to the presence of possible magnetic fluxes or cosmic strings that extend to infinity". (refs: RF-09) peer-reviewed (JHEP 05 (2021) 032), FT.
- [D-12] **Maldacena–Milekhin 2020, "Humanly traversable wormholes".**
  - Ingredients: a Randall–Sundrum II braneworld and a dark sector (a 4D CFT with a gauged U(1)). The physics is speculative beyond the Standard Model, and the authors call it "science fiction".
  - From outside the mouths "resemble intermediate mass charged black holes". Both mouths sit in one shared ambient space.
  - Shortcut: no. "The time through the wormhole is always longer than through the outside, π·ℓ > d".
  - The traveller's proper time is of order π·r_e: "less than a second" across the galaxy, against "tens of thousands of years" for an outside observer.

  (refs: RT-12, RQ-03, RC-18, RF-06, RE-14) peer-reviewed (PRD 103, 066007), FT.
- [D-13] **Maldacena–Milekhin free-fermion (MMP-type 4D) version.** For a ship of about 1e3 kg (SI) it needs |E_bin| > 1e3 kg with r_e > 1e7 m, which gives N_f > 1e52 fermion species. A TeV-scale UV cutoff requires N_f ≲ M_pl²/TeV² ~ 1e32. So the simple free-fermion model cannot be humanly traversable, which is why the authors move to RS II. The 1e52 figure is an estimate for a 1e3 kg spaceship, not a general requirement. (refs: RT-13, RQ-04, RC-18, RF-05) peer-reviewed, FT.
- [D-14] **Maldacena–Milekhin practical obstructions** (stated by the authors):
  - the infall boost is γ ~ ℓ/r_e;
  - a CMB photon falling in is boosted by γ and seen by the traveller boosted by γ², so the hole must sit "inside a refrigerator";
  - the dark sector must be colder than 1/ℓ ~ 1e-26 eV;
  - matter that scatters inside accumulates positive energy that "would eventually make the wormhole collapse into a black hole";
  - the ambient space must be cold and flat, "much colder than the present universe";
  - "We have not given any plausible mechanism for their formation."

  (refs: RQ-05, RC-19 [unverified by its checker; the same content is verified under RE-14], RE-14) peer-reviewed, FT.

### 1d. Einstein–Dirac–Maxwell (EDM) wormholes held open by classical fields

- [D-15] **Blázquez-Salcedo, Knoll & Radu 2021 (BKR).**
  - Setting: 4D, asymptotically flat, spherically symmetric, singularity-free traversable wormholes in Einstein–Dirac–Maxwell theory. Two gauged massive fermions sit in a singlet state, with a one-particle condition on each spinor.
  - The Dirac matter is "a quantum wave function rather than a quantum field": semiclassical, with no Casimir term.
  - The abstract says "without needing any form of exotic matter".
  - All solutions constructed so far have Q_e/M > 1 and q/μ < 1 (Planck units).
  - Some solutions near the critical line have negative ADM mass. The checker narrowed this scope: it applies to solutions near the critical line, not to "some smooth-geometry solutions" in general.
  - Generic solutions carry a thin shell at the throat, with ε_T = −4ν'(0)/√f(0). It disappears only when ν'(0) = 0.
  - The family is scale-invariant, so physical size is set by the fermion mass in Planck units (the researcher's labelled inference).
  - The closed form M = 2Q_e² r_0/(Q_e² + r_0²) was not found by the checker **[unverified]**.

  (refs: RT-16, RQ-13, RQ-14, RE-17) peer-reviewed (PRL 126, 101102), FT.
- [D-16] **Critiques of BKR.**
  - *Bolokhov, Bronnikov, Krasnikov & Skvortsova 2021.* "Without needing any form of exotic matter" looks misleading: by the standard definition exotic matter is NEC-violating matter, and some is necessary at a throat. "It would be better to say that Dirac spinor fields become exotic matter." They also cite Danielson et al. (arXiv:2108.13361), who argue that the BKR solution fails the junction conditions for the Maxwell and Dirac fields; that is a secondary citation, not opened.
  - *Konoplya & Zhidenko 2022.* Mirror symmetry about the throat forces non-smooth fields there. The fermionic charge density must change sign at the throat, so particles and antiparticles coexist without annihilating, and a "membrane of matter" sits at the throat. "Apparently this kind of configuration could not exist in nature." They then build asymmetric, smooth EDM wormholes.

  (refs: RT-19, RQ-14, RC-04, RF-03, RE-18, RT-20 [unverified comment arXiv:2206.12250]) peer-reviewed (Grav. Cosmol. 27, 401; PRL 128, 091104), FT.
- [D-17] **Kain 2023, time evolution of the asymmetric EDM wormholes** (spherical symmetry; μ̄ = 0.2, ē/√(4π) = 0.03).
  - "In all cases considered", black holes form connected by the wormhole. Null geodesics that cross the throat are trapped inside a black hole. "We conclude that Einstein-Dirac-Maxwell wormholes are not traversable."
  - Kain does not rule out other asymmetric EDM solutions.
  - The static solutions are regular and asymptotically flat, but they violate the NEC (T^r_r − T^t_t < 0).
  - Their throat radius R0 is 75–498 Planck lengths.

  (refs: RT-17, RT-18, RC-05, RC-06, RF-01, RF-02) Status: RC-05 and RF-01 give PRD 108, 044019; RT-18 lists it as a preprint, and no checker confirmed the journal. FT.

### 1e. Classical support by a ghost scalar

- [D-18] **Ellis–Bronnikov-type wormholes held open by a ghost scalar** (massless, minimally coupled, spherical symmetry) are linearly unstable, with exactly one unstable mode. Under nonlinear evolution they either expand or collapse to a Schwarzschild black hole, depending on the sign of the perturbation. Charged versions are also unstable. (refs: RC-14) peer-reviewed (CQG 26, 015010 and 015011; PRD 80, 024023), AB.

### 1f. Laboratory and observation

- [D-19] **Jafferis et al. 2022 (Nature 612, 51).**
  - Ran a learned, sparsified SYK model on Google Sycamore "with 164 two-qubit gates on a nine-qubit circuit".
  - Claims five properties of traversable-wormhole physics:
    - perfect size winding;
    - coupling on either side consistent with a negative-energy shockwave;
    - a Shapiro delay;
    - causal time-ordering of the signals;
    - scrambling and thermalisation.
  - Its own description is "a step towards a program for studying quantum gravity in the laboratory".
  - That no spacetime region was created is the researcher's inference. Neither side of the debate (D-29) claims a spacetime wormhole was made.

  (refs: RE-01, RE-02, RF-13) peer-reviewed, FT (abstract page; body paywalled).
- [D-20] **Kobrin, Schuster & Yao.**
  - The learned Hamiltonian has seven Majorana fermions and five fully commuting terms.
  - Their findings: (i) it does not thermalise; (ii) the teleportation signal resembles SYK only for the operators used in training; (iii) perfect size winding is generic to small fully commuting models.
  - Published as a Nature Matters Arising: Nature 643, E17–E19 (23 Jul 2025).
  - Status correction: RF-13 and RC-07 call the critique an unrefereed preprint. It was later peer-reviewed and published (RE-05, verified).

  (refs: RC-07, RE-03, RE-05, RF-13, RQ-12) peer-reviewed (Matters Arising), FT.
- [D-21] **Takahashi & Asada 2013, SDSS Quasar Lens Search** (N_Q = 50,836 quasars). No multiple images from exotic lenses were found. The bounds, assuming the classical Ellis or negative-mass lens model with zero ADM mass for Ellis, are:
  - negative-mass compact objects: n < 1e-8 (1e-4) h³ Mpc⁻³ for |M| > 1e15 (1e12) M_sun, i.e. |Ω| < 1e-4;
  - Ellis wormholes: n < 1e-4 h³ Mpc⁻³ for throat radius a = 10–1e4 pc.

  (refs: RQ-16, RE-10) peer-reviewed (ApJL 768, L16), FT.
- [D-22] **Abe 2010, Ellis-wormhole microlensing.**
  - Light curves show "gutters" of about 4% just outside Einstein-ring crossing, and magnification below Schwarzschild's.
  - Takahashi & Asada's introduction says Galactic microlensing could probe throats of a = 100–1e7 km (SI).
  - Lenses with Einstein radius below the stellar radius (about 1e6 km) are smeared out by finite-source effects; this point was not re-checked.
  - Yoo et al. 2013 (GRB femtolensing) give n ≲ 1e-9 AU⁻³ for a ~ 1 cm. This is a secondary citation via Takahashi & Asada; the original was not opened.

  (refs: RE-11, RQ-16) peer-reviewed, FT.
- [D-23] **Dai & Stojkovic 2019.** If Sgr A* were a traversable wormhole, a star on the far side would perturb S2's orbit. A few-solar-mass star at a few gravitational radii would be detectable at 1e-6 m/s² acceleration precision (SI). For comparison:
  - S2's acceleration is 1.5 m/s²;
  - precision achieved is 4e-4 m/s² (2 yr of data);
  - projected precision is 2e-5 m/s² (20 yr);
  - 1e-6 m/s² needs about 2 km/s velocity uncertainty.

  (refs: RE-12) peer-reviewed (PRD 100, 083513), FT.
- [D-24] **EHT Sgr A*.** The image size is "within ~10% of the Kerr predictions". The 47–50 µas shadow figures and the claim that Ellis–Bronnikov shadows are not excluded are **[unverified / SS]**. (refs: RE-21) peer-reviewed, FT for the quote.
- [D-25] **MoEDAL Schwinger-mechanism search** (Pb–Pb at 5.02 TeV per nucleon, 0.235 nb⁻¹). It excluded monopoles with 1–3 g_D and masses up to 75 GeV/c². No magnetic charge has been detected at any scale. The later limit of about 3.9 TeV is **[SS, unconfirmed]**. (refs: RE-19) peer-reviewed (Nature 602, 63), FT for 75 GeV.
- [D-26] **Casimir force.** Measured by atomic force microscope between an Al-coated sphere and a plate (Roy, Lin & Mohideen, PRD 60, 111101, published 1999; RE-23 dates it "2000"). So negative energy from ordinary quantum fields is real and measurable at sub-micron separations. The earlier figures of 1.6 pN rms and ~1% (Mohideen & Roy 1998) are SS. That no laboratory analogue of a wormhole throat's Casimir support exists is the researcher's inference. (refs: RE-23) peer-reviewed, FT.

### Construction index
This index only cross-references D-items; it adds no new facts. "AF" means asymptotically flat.

| Construction | One- or two-sided | What holds it open | Throat ANEC | Throat geodesic achronal? | Shortcut? | Key items |
|---|---|---|---|---|---|---|
| Morris–Thorne / Ellis–Bronnikov | not specified in sources | exotic matter or ghost scalar | NEC violated at the throat (D-39; formula at D-44); ANEC violated on some geodesic (D-38) | not computed | not established in sources | D-18, D-38, D-39, D-43, D-44 |
| Visser thin-shell / polyhedral | not covered | not covered | not covered | not covered | not covered | gap (Section 6) |
| GJW (+ MSY, Freivogel) | two-sided, AdS3 | one-loop quantum fields plus boundary coupling | negative | n/a (two-sided) | no: nothing passes without the coupling; a few bits at most | D-04, D-05, D-06 |
| Maldacena–Qi | two-sided, AdS2/JT | quantum fields plus external coupling | −2φ_r < 0 | n/a | compared with the coupling channel | D-07 |
| MMP | one-sided, 4D AF | Casimir-like energy of massless charged fermions | violated on non-achronal wrapped lines | no (authors) | no: long, t/d > 2 | D-08 |
| FGM 2018 | Z2 quotient | quantum fields, Hartle–Hawking state | negative along non-contractible cycles | not stated | not stated | D-09 |
| FGM 2019 | one-sided, 4D AF (with cosmic string) | perturbative quantum back-reaction | negative (exponentially small) | not stated | no: d + logs, approaching d | D-10 |
| Maldacena–Milekhin 2020 | one-sided (two mouths in one space) | RS II dark-sector CFT (speculative) | violated (via MMP mechanism) | not stated | no: π·ℓ > d; proper time short | D-12 to D-14 |
| BKR EDM, with KZ and Kain | two-sided AF, Z2-symmetric (BKR) or asymmetric (KZ) | classical Dirac wave functions plus Maxwell | NEC violated (Kain); no ANEC integral reported | not stated | not reported; dynamically forms black holes | D-15 to D-17 |

---

## 2. Quantitative anchors

| ID | Quantity | Value (units) | Conditions | Source refs | Access |
|---|---|---|---|---|---|
| D-Q01 | Maldacena–Milekhin minimum throat (extremal) radius r_e | > 1.5e7 m (about 0.05 light-seconds), SI | tidal acceleration a ~ size·c²/r_e² < 20 g, g = 9.8 m/s², size 0.5 m, short duration | RQ-01, RT-14, RF-05, RE-14; recomputed as 1.51e7 m [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/quantitative_scales.py] | FT |
| D-Q02 | Tidal criterion used | 20 g (MM) against about 1 g, Earth gravity, between parts of a 2 m body (Morris–Thorne 1988) | MT criterion from a search summary only; MT PDF extraction failed | RT-14, RT-31 | FT (MM) / SS (MT) |
| D-Q03 | MM worked parameters, eq. 3.27 | r_e ~ 0.05 s; c_2 ~ 7e72 (2D central charge); ℓ ~ 3e3 ly; γ = ℓ/r_e ~ 2e12; E_bin ~ −5e9 kg (≈ −4.5e26 J, SI) | RS II with R_5 = 50 µm (largest allowed), minimal r_e | RQ-02, RQ-17 | FT |
| D-Q04 | MM exterior vs. proper transit time | π·ℓ/c ≈ 9.4e3 yr (paper: "tens of thousands of years"); π·r_e/c ≈ 0.157 s | eq. 3.27 parameters; T_thru/T_ext = π·ℓ/d ≥ π for d ≤ ℓ | RQ-03, RQ-17 [calc: quantitative_scales.py] | FT + calc |
| D-Q05 | MM mouth mass, if each mouth is extremal Reissner–Nordström | M = r_e c²/G ≈ 2.0e34 kg ≈ 1.0e4 M_sun per mouth (SI) | extremal-RN mapping is the researcher's assumption; the paper says "up to a small correction" | RQ-06, RQ-17, RE-15, RF-21 [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/engineering_mm_scale.py] | FT + calc |
| D-Q06 | Two-mouth rest energy | ≈ 3.6e51 J (SI) | as D-Q05 | RE-15 [calc: engineering_mm_scale.py] | calc |
| D-Q07 | |E_bin| / M_e | ≈ 2.5e-25 (dimensionless) | eq. 3.27 E_bin against D-Q05 | RQ-17 | calc |
| D-Q08 | MM magnetic charge per mouth | ≈ 1.6e41 Dirac charges (extremal-RN SI estimate); a separate illustrative estimate q ~ 3e81–3e83 flux quanta for g_4 = 0.1–1 | the two conventions differ (Gaussian-type Dirac charge vs. the paper's q with unspecified g_4); both are illustrative, not printed in the paper | RE-15, RQ-17 | calc |
| D-Q09 | MM surface magnetic field | ≈ 2.3e11 T at r_e (SI) | extremal-RN assumption | RE-15 | calc |
| D-Q10 | Free-fermion species requirement vs. bound | N_f > 1e52 required; N_f ≲ M_pl²/TeV² ~ 1e32 allowed | ship of about 1e3 kg, r_e > 1e7 m, g²N_f < 1 | RT-13, RQ-04, RF-05 | FT |
| D-Q11 | MM dark-sector temperature requirement | < 1/ℓ ~ 1e-26 eV | RS II construction | RC-19 [unverified by its checker] | FT |
| D-Q12 | MMP Standard Model embedding size | ≲ 1/TeV ≈ 2e-19 m (SI); N_f = 54 effective charge-one flavours | Standard Model fermions | RE-16 | FT |
| D-Q13 | MMP energy minimum | l = 16 r_e³/(G_N q); E_min = −G_N q²/(256 r_e³) (natural units) | eqs. 5.30–5.31 | RT-07 | FT (equations, not a verbatim quote) |
| D-Q14 | MMP transit-time ratio | t_transit/d > 2 | eternal MMP | RC-09, RT-10 | FT |
| D-Q15 | FGM 2019 minimum transit time | t_min = d + logs (c = 1); t_min/d → 1 | 4D AF, perturbative, Hartle–Hawking state | RT-10, RQ-15, RF-08 | FT |
| D-Q16 | FGM 2019 instability time | ~ d^{3/2} (G = c = 1) | black holes fall together | RQ-15, RF-08 | FT |
| D-Q17 | GJW open time | proper time < Planck time | BTZ, probe regime | RT-29 | FT |
| D-Q18 | MSY information cap | "a few bits"; 0 ≤ g⟨V⟩ < 2π | nearly-AdS2, probe approximation; parametric only | RT-26, RC-16 | FT |
| D-Q19 | Kain EDM static throat radius | R0 = 75.28 to 498.4 l_P (Planck lengths) | μ̄ = 0.2, ē/√(4π) = 0.03, Table I | RF-02, RC-05 | FT |
| D-Q20 | BKR charge-to-mass ratio | Q_e/M > 1; q/μ < 1 (Planck units) | all solutions found | RQ-13, RE-17 | FT |
| D-Q21 | Ford–Roman: thin-band width | negative energy in a band thinner than the throat by about (l_P/r0)^n, n ≲ 1 (as stated in RC-12) | massless minimally coupled scalar QI, static throat | RC-12 | FT |
| D-Q22 | Planck length | 1.616e-35 m (SI); 1e4 l_P = 1.6e-31 m | reference value | RQ-17 | calc |
| D-Q23 | Sycamore experiment size | 9 qubits (chosen from a 72-qubit chip), 164 two-qubit gates; learned Hamiltonian of 7 Majorana fermions, 5 commuting terms | Jafferis 2022 | RE-01, RE-03, RE-07, RC-07 | FT |
| D-Q24 | Sycamore circuit fidelity | measured fidelity "already below 1/2 of the noiseless fidelity" | secondary paper arXiv:2301.03522; author unknown, low weight | RE-07 | FT |
| D-Q25 | Byun 2026 IBM run | N = 8 binary sparse SYK, q = 4, J = √2, β = 3, |μ| = 12; mutual information up to about 0.025 | IBM superconducting, preprint | RE-06, RE-09, RF-15 | FT |
| D-Q26 | SDSS lens bounds | see D-21 | Ellis/negative-mass model | RQ-16, RE-10 | FT |
| D-Q27 | Microlensing-sensitive throat range | a = 100–1e7 km (SI) | Galactic microlensing (Takahashi–Asada introduction) | RE-11 | FT |
| D-Q28 | Femtolensing bound | n ≲ 1e-9 AU⁻³ for a ~ 1 cm | Yoo et al. 2013, via Takahashi–Asada | RQ-16, RE-11 | FT (secondary citation) |
| D-Q29 | S2-orbit test sensitivity | need 1e-6 m/s²; have 4e-4 m/s² (2 yr); projected 2e-5 m/s² (20 yr); S2 acceleration 1.5 m/s² | far-side star of a few M_sun at a few r_g | RE-12 | FT |
| D-Q30 | Triple-system wormhole test | mass limit about 4 orders of magnitude better than from S2; a pulsar about 10 orders better | Simonetti et al., preprint | RE-13 | FT |
| D-Q31 | EHT Sgr A* consistency | image size within ~10% of Kerr | mass-to-distance prior | RE-21 | FT |
| D-Q32 | MoEDAL monopole exclusion | 1–3 g_D, mass ≤ 75 GeV/c² | Pb–Pb, 0.235 nb⁻¹ | RE-19 | FT |
| D-Q33 | MM mass versus largest engineered mass | gap ~1e29 (RE-24) | **corrected**: the "1e5 kg largest engineered object" input is unsourced and questionable (structures exceed 1e8 kg), so the gap is uncertain by several orders; the qualitative conclusion stands | RE-24 | SS (researcher's judgement) |
| D-Q34 | Squeezed-light squeezing | about −15 dB | negative energy density "too small to be directly measurable" | RE-22 | SS |

---

## 3. Contested or conflicting

- [D-27] **Do EDM wormholes need "exotic matter"?**
  - *No:* BKR say they are built "without needing any form of exotic matter" (RT-16, RE-17).
  - *Yes, by definition:* exotic matter means NEC violation, and the Dirac fields become exotic matter (Bolokhov et al., RT-19). Kain shows the static solutions violate the NEC (RC-06).
  - *Resolution in the sources:* "no exotic matter" means no phantom or ghost field put in by hand. It does not mean the NEC holds.
- [D-28] **Are EDM wormholes physical and traversable?**
  - *Hopeful:* Konoplya & Zhidenko's asymmetric smooth solutions give "hope that such kind of wormholes could exist in nature" (RF-03).
  - *Not traversable:* Kain's evolutions form black holes and trap the throat-crossing null geodesics (RF-01, RT-18). The symmetric BKR solutions also face the non-smoothness and membrane objections (RC-04) and Danielson et al.'s junction-condition objection (second-hand via RT-19).
  - No rebuttal of Kain was found (frontier gaps).
- [D-29] **Did the 2022 Sycamore experiment show gravitational (wormhole) dynamics?**
  - *Jafferis et al.:* five wormhole properties preserved (RE-02). Their 2023 reply says Kobrin et al. agree that size winding is the mechanism and that the system thermalises and scrambles at the teleportation time, and that the objections concern "counterfactual scenarios" (RE-04, RC-08, RF-14; preprint).
  - *Kobrin, Schuster & Yao:* there is no thermalisation, the signal resembles SYK only for the training operators, and size winding is generic to commuting models (RE-03, RE-05, now a peer-reviewed Matters Arising).
  - Neither side claims a spacetime wormhole was created.
  - Byun et al. 2026 (preprint) say the concern about sparsification at small N remains "live" (RE-06, RF-15).
  - Whether a published reply accompanies the 2025 Matters Arising is unknown.
- [D-30] **Does chronology protection have a proof?**
  - *Support:* Kay, Radzikowski & Wald prove that QFT breaks down at the base points of a compactly generated Cauchy horizon, which they read as "support" for Hawking's conjecture (RT-27, RC-13).
  - *Objection:* Krasnikov (1999) disputes the force of the F-locality assumption. Only a truncated abstract was seen (RC-13, AB, low confidence).
- [D-31] **Is the achronal ANEC true?**
  - *For:*
    - no known counterexample in self-consistent semiclassical gravity (RF-12, Kontou 2024);
    - proofs in flat-space QFT (RT-23);
    - Wall's derivation from the generalised second law (RT-21).
  - *Against, or limiting:*
    - for test fields, Urban & Olum (2010) found ANEC and achronal ANEC violated by a conformally coupled scalar in a conformally flat 3+1D spacetime, "as large as desired" (RC-03; unverified by checker, FT);
    - Wall's theorem fails once the linearised graviton is quantised (RT-21);
    - Kontou & Sanders list curved-spacetime validity as open (RT-24).
  - The self-consistent version (Graham–Olum) is untouched by Urban–Olum, because their background is not self-consistent.
- [D-32] **How much exotic matter is required?**
  - *Very little, by one measure:* Visser–Kar–Dadhich show the volume integrals of the NEC-violating stresses can be made arbitrarily small, though ANEC violation is still required (RT-28, RQ-07).
  - *Strong limits, by another:* Ford–Roman quantum inequalities imply either a throat only a little larger than the Planck size or negative energy confined to a band many orders of magnitude thinner than the throat, making macroscopic wormholes "very improbable" (RC-12).
  - The two use different measures (volume integral vs. QI-bounded energy density), so they do not directly contradict.
  - Kontou: a Planck-scale throat "would not be traversable" (RQ-08). This is a statement about generic Planck-scale throats, not specifically about the [90] solution.
- [D-33] **Is the FGM 2019 bound on transit time a theorem?**
  - *RT-11 and RF-08* call it a "prohibition", with t_min approaching the minimum allowed by the achronal ANEC.
  - *The checker* notes the paper rests it on "general arguments (and in particular the generalized second law)", with the minimum "at least in higher dimensions". It is not a proven theorem in 4D (RT-11 check, RF-08 check).
  - RC-09's reading that D ≥ 5 saturates was not re-grepped.
- [D-34] **Which tidal criterion?** Maldacena–Milekhin use 20 g for short durations on a 0.5 m traveller (RT-14). Morris–Thorne's is about 1 g between parts of a 2 m body (RT-31, SS only). No source computes the minimum r_e under the 1 g, 2 m criterion; this is left to the analysis stage.
- [D-35] **Gravitational-wave echoes.** Abedi–Dykaar–Afshordi claimed O1/O2 echoes, about 2.5σ according to a search summary (unconfirmed). LVK O3 searches find p-values consistent with noise (RE-20, preprint arXiv:2309.01894).
- [D-36] **Squeezed light and quantum inequalities.** Maclay & Davis (Found. Phys. 2019) claim a meta-analysis of squeezed-light data conflicts with a quantum inequality. This is contested, low-confidence, and from authors outside the mainstream QEI community. No mainstream response was found (RE-22).
- [D-37] **The MM exterior time.** The abstract says "tens of thousands of years". π·ℓ with ℓ ~ 3e3 ly gives about 9.4e3 yr, which the checker attributes to the paper's loose rounding (RQ-03, RQ-17). The order of magnitude is consistent.

---

## 4. Constraints: theorems, bounds and no-go results, each with its assumptions

- [D-38] **Topological censorship** (Friedman, Schleich & Witt 1993). *Proved theorem.*
  - Assumptions: asymptotically flat, globally hyperbolic spacetime; ANEC on all inextendible null geodesics.
  - Conclusion: every causal curve from J⁻ to J⁺ deforms to one in a simply connected neighbourhood of infinity, so there is no traversable wormhole.
  - Contrapositive: a traversable wormhole in that class requires ANEC violation along some (not all) null geodesics.
  - Free renormalised fields violate plain ANEC in generic spacetimes (Wald–Yurtsever).

  (refs: RT-25, RT-03) FT.
- [D-39] **Hochberg & Visser: the generic static throat.**
  - Assumptions: static spacetime; a minimal-area 2-surface that flares out; no spherical symmetry needed; classical GR.
  - Conclusions: the NEC is violated at some points on or near the throat, and a suitably weighted throat integral of the NEC must be negative. Throats of high genus violate the WEC and DEC somewhere.
  - The extension to dynamic wormholes is claimed in RT-03. Brans–Dicke-type frames can hide the violation in the scalar sector, though the total violation is frame-independent; this caveat was not checked.

  (refs: RC-11 [PRD 56, 4745; unverified by checker], RT-03 [**status corrected**: arXiv gr-qc/9710001 is the Haifa proceedings "Generic wormhole throats", not PRL 81, 746; the quotes themselves are verified]) FT.
- [D-40] **Gao–Wald time-delay theorem (2000).** *Proved theorem.*
  - Assumptions: null-geodesically complete spacetime; pointwise NEC; null generic condition; any dimension.
  - Conclusion: for every compact K there is a compact K′ such that "fastest" null geodesics between points outside K′ do not enter K.
  - The authors say the "no time advance" reading is suggestive only, because "the theorem gives little control over the size of the region K′".
  - Wormholes violate the NEC, so it does not apply to them directly. Its ANEC and GSL extensions are what Graham–Olum and FGM invoke.

  (refs: RT-15 [the quote in RT-15 is a paraphrase; use RC-10's verbatim wording], RC-10) FT.
- [D-41] **Self-consistent achronal ANEC** (Graham & Olum 2007). *Conjecture.*
  - Statement: no self-consistent semiclassical solution violates ANEC on a complete achronal null geodesic.
  - Scope: semiclassical regimes well below Planck curvature.
  - Claimed consequence: if true, it rules out closed timelike curves and wormholes connecting different asymptotically flat regions, i.e. it rules out shortcuts.
  - Evidence: a "tube of flat space" argument for a minimally coupled scalar. "Such a proof will have to await future work."
  - It leaves open "long" wormholes, through which no complete achronal null geodesic passes (Kontou 2024; MMP).
  - Bilotta 2023 restates it as "proven … in the absence of gravity … conjectured … in gravity" (RF-10, preprint).

  (refs: RT-01, RT-02, RC-01, RF-11, RF-12, RF-10) FT.
- [D-42] **Achronal ANEC: partial proofs.** Each holds only under its own assumptions.
  - *Wald–Yurtsever:* minimally coupled free scalars, on a curved 2D spacetime or in 4D with a bifurcate Killing horizon (RT-22, RC-02).
  - *Wall 2010:* proved for quantum fields minimally coupled to semiclassical Einstein gravity, assuming the generalised second law for causal horizons, CPT, a suitable renormalisation scheme for generalised entropy, extra-strong cosmic censorship and horizons that persist under perturbation. The last three assumptions were not checked. It fails once the linearised graviton is quantised (RT-21).
  - *Faulkner–Leigh–Parrikar–Wang 2016:* flat-space ANEC from monotonicity of relative entropy, in Minkowski space and static bifurcate Killing horizons. Not fully rigorous for all QFTs (RT-23; scope wording not re-grepped).
  - *Hartman–Kundu–Tajdini 2017:* ANEC from causality, for unitary Lorentz-invariant QFTs with an interacting UV fixed point, in Minkowski space only (RT-23).
  - Kontou–Sanders: proved for all massive fields in 2D Minkowski; partial results in higher dimensions; open in curved spacetime (RT-24).
- [D-43] **Quantum energy inequalities applied to wormholes** (Ford & Roman 1996).
  - Assumptions: massless, minimally coupled scalar; a quantum inequality derived in Minkowski space applied over short scales; static Morris–Thorne geometry. The authors expect similar bounds for other fields.
  - Conclusion: either the throat is only slightly larger than the Planck length, or there are large scale discrepancies (the negative energy sits in a thin band).
  - Loopholes the authors note: a field that makes the coefficients large only in a tiny region; superposition of effects.
  - Kontou 2024 applies the smeared null energy condition (SNEC) and the double smeared one (DSNEC) to MMP "long" wormholes, with the DSNEC result new. The DSNEC is said to hold only in Minkowski space or below the curvature scale; that scope claim was not checked.

  (refs: RC-12, RT-30 [unverified], RQ-08 [unverified, partly SS], RF-11) FT.
- [D-44] **Morris–Thorne flare-out NEC violation.**
  - Metric: ds² = −e^{2Φ}dt² + dr²/(1 − b/r) + r²dΩ² (G = c = 1).
  - Energy density: ρ = b′/(8πr²).
  - Radial NEC at the throat: ρ + p_r = (b′ − b/r)/(8πr²) < 0 at r0, given b(r0) = r0 and the flare-out condition b′(r0) < 1.
  - The research presents this as a standard result **[unverified / SS]**; no calc file in the research reports its numerical output. The brief notes that ρ = b′/(8πr²) is already checked in `gr_tensors.py`.

  (refs: RT-32, RT-31)
- [D-45] **Kay–Radzikowski–Wald 1997, chronology.** *Proved theorem.*
  - Assumptions: linear (free) scalar QFT on a spacetime with a compactly generated Cauchy horizon; F-locality / Hadamard criterion.
  - Conclusion: no extension of the field algebra satisfies F-locality at the base points (past terminal accumulation points) of the horizon, so the theory breaks down there.
  - It supports Hawking's 1992 chronology protection *conjecture* but does not prove it. To build a time machine one must "enter a regime where quantum effects of gravity itself will be dominant" (this quote was not re-grepped).

  (refs: RT-27, RC-13) FT. Hawking 1992, Kim–Thorne 1991 and Morris–Thorne–Yurtsever 1988 were not retrieved (Section 6).
- [D-46] **Information bounds for two-sided wormholes.**
  - MSY: back-reaction stops more information passing than was spent setting up the coupling (nearly-AdS2; parametric).
  - Freivogel et al.: open for less than the Planck time, and no reliable transfer for horizons of order the AdS radius (BTZ).
  - GJW: the decoupled system transmits nothing.

  (refs: RT-05, RT-26, RC-16, RT-29)
- [D-47] **Kanai–Maeda–Yoshida 2025 no-go.**
  - Assumptions: effective-field-theory (higher-derivative) corrections to Einstein–Maxwell; perturbation of near-extremal Reissner–Nordström (4D) or equal-angular-momenta Myers–Perry (5D) black holes.
  - Conclusion: traversable wormholes cannot arise perturbatively, whatever the correction terms. Escaping requires new ingredients such as Casimir energy (as in MMP) or black holes with reduced symmetry.
  - Status: PRD 113, 064026 per INSPIRE. RC-20's claim text calls it a preprint while its STATUS line says peer-reviewed; peer-reviewed is supported. The order-of-perturbation scope is the researcher's gloss.

  (refs: RC-20) FT.
- [D-48] **Bound on species in the MM construction.** N_f ≲ M_pl²/TeV² ~ 1e32 if the UV cutoff of the local field theory is above the TeV scale (Bekenstein-like) (RT-13, RQ-04).
- [D-49] **Two-sided comparison channel.** In GJW, Maldacena–Qi and the SYK/teleportation constructions, traversability exists only with the boundary coupling: an ANEC-violating negative-energy shockwave opens the channel. The meaningful "shortcut" comparison is therefore with that coupling, and nothing arrives without it. (refs: RT-05, RC-15, RF-16 [unverified, preprint], D-46)

---

## 5. Frontier and speculative (labelled; not established)

- [D-50] **Bilotta 2023, Kerr** (preprint, SPECULATIVE/PERTURBATIVE). A double-trace deformation of the near-horizon, near-extremal Kerr region gives negative average null energy and a traversable wormhole. The state off-axis is irregular because of superradiance, and a non-perturbative 4D asymptotically flat version is only commented on. That this is the first move towards astrophysical rotating black holes is the research file's gloss, not the paper's. (refs: RF-10) FT.
- [D-51] **Byun, Kim & Lee 2026** (preprint). Reports "the first quantum-hardware realization of the TW protocol driven by an explicitly chaotic Hamiltonian": an N = 8 binary sparse SYK model on an IBM superconducting processor. The mutual information shows a sign-dependent asymmetry near the teleportation time; μ < 0 corresponds to ANEC violation in the holographic reading. (refs: RE-06, RE-09, RF-15, RF-16) FT. A separate IBM/Quantinuum "wormhole-inspired" run by Su et al. is known only from a Quanta search summary (RE-09, SS).
- [D-52] **"Quantum gravity in the lab"** (Brown et al., PRX Quantum 4, 010320). Holographic teleportation protocols "readily executed in table-top experiments" that mimic GJW and MSY. **[unverified by checker]** (refs: RE-08) FT. Shapoval et al. (Quantum 7, 1138) and Weinstein 2023 are pointers only (RF-17, AB).
- [D-53] **Maldacena–Milekhin: a small wormhole for "very secret signals or qubits".** A speculative remark, not a computed result. It bears on whether a non-shortcut is useless (brief, hidden premise 4). (refs: RF-07) FT.
- [D-54] **Observational modelling of EDM and RS II "wormholes without exotic matter"**: quasinormal modes, echoes and shadows (Churilova et al., JCAP 10 (2021) 010), and epicyclic and quasi-periodic-oscillation frequencies (Stuchlik et al., EPJ Plus 136, 1127). These are predictions for hypothetical objects whose premise is undermined by D-17. (refs: RF-04 [unverified], AB.)
- [D-55] **Further double-trace AdS wormholes** (Ahn et al. 2024; Liu & Miao 2025). AdS only. (refs: RF-18) SS.
- [D-56] **Classical "Casimir-like" and wormhole–warp-drive solutions** (Avalos et al. 2025; Garattini et al. 2024). SPECULATIVE: they assume a source with the required sign, and the portion read does not engage the achronal ANEC or QEIs. (refs: RF-19 [unverified]) AB.
- [D-57] **Proposals for observational wormhole tests**, null so far:
  - S2 orbit perturbation (D-23);
  - a triple system or pulsar, about 4 to 10 orders of magnitude more sensitive than S2 (Simonetti et al., preprint) (RE-13).

  These assume a classical wormhole through which gravity propagates.
- [D-58] **Technology readiness (TRL), the researcher's own judgement, not sourced** (RE-24, SS).
  - Quantum-processor teleportation: TRL ~3–4 as a simulation, ~1 as a test of quantum gravity.
  - Astronomical searches: TRL 6–9 as instruments, but null results and sensitive only to classical Ellis or negative-mass models.
  - Creating or widening any wormhole: TRL 0–1. No mechanism appears in any source, and Konoplya & Zhidenko call formation scenarios "highly disputable" (RE-18).
- [D-59] **Kontou 2024** mentions an old proposal to stabilise wormholes with Casimir plates, and spontaneous production by tunnelling, as speculative without details. The original source was not identified (RF-11).
- [D-60] **Large-squeezing, quantum-inequality-violation claims** (Maclay & Davis). Contested; see D-36.

---

## 6. Unknowns and gaps

- **No calculation in the research for any construction** of:
  - the ANEC integral along the throat-crossing geodesic;
  - the achronality of that geodesic;
  - T_thru against T_ext.

  Only published statements are reproduced (MMP non-achronal; MM π·ℓ > d; FGM d + logs). `runs/<slug>/tools/wormhole_tools.py` exists, but no research claim reports its self-test or output. The Morris–Thorne NEC formula (D-44) is unverified. The published ANEC values for GJW, Maldacena–Qi, MMP and FGM 2018 were not reproduced.
- **Visser thin-shell and polyhedral wormholes** (Visser 1989; Poisson–Visser 1995 stability; *Lorentzian Wormholes* 1995): no claims at all. A whole row of the brief's table is missing.
- **Primary classical sources not retrieved:**
  - Morris & Thorne 1988 (the tidal criterion is SS only; the "8.64 Earth radii" figure is unverified);
  - Morris, Thorne & Yurtsever 1988 (mouth motion turning a wormhole into a time machine);
  - Hawking 1992;
  - Kim & Thorne 1991;
  - Frolov & Novikov 1990;
  - Geroch 1967 and Tipler 1977 (topology change).

  Whether a long, non-shortcut wormhole can be made into a time machine by moving its mouths is not addressed by any retrieved source.
- **The "Jupiter mass of exotic matter for a 1 m throat" figure** was not found in any source. No source gives the energy needed to pass a 1 kg or 70 kg payload through a given throat, apart from MM's |E_bin| > ship-mass condition.
- **Creation routes:** no rates or pathways. Garfinkle–Strominger pair creation of magnetic black holes is SS only; no rate was retrieved.
- **Searches for magnetic black holes and monopoles:** no Parker bound, MACRO or IceCube sensitivities retrieved, and no observation targeting MM or MMP-type extremal magnetic mouths.
- **The physical size of BKR/EDM wormholes for electron-like fermions** was not computed.
- **Maldacena–Qi and FGM 2018:** journal references unverified. The Kain PRD reference was not independently checked.
- **Kontou–Olum 2015** was not fetched. The DSNEC bound values for MMP were not extracted. Krasnikov's critique of KRW was seen only as a truncated abstract. Danielson et al. (arXiv:2108.13361) was not opened.
- **Sycamore:** fidelity values, the size of the asymmetry and the Shapiro-delay numbers were not quoted (body paywalled). The "N = 10 SYK with 210 terms" comparison is unverified. Whether the authors replied to the 2025 Matters Arising is unknown.
- **No dedicated microlensing-survey search** (OGLE, MOA, EROS) for Ellis-wormhole events was located. Cramer et al. 1995 was not located. The Cardoso–Franzin–Pani journal reference was not verified.
- **No laboratory test of a quantum energy inequality** was found, and no mainstream response to Maclay & Davis.
- **No 2023–2026 paper proving or refuting the self-consistent achronal ANEC in 4D gravity** was found. The frontier sweep was incomplete because arXiv rate-limited the searches (HTTP 429).
- **Hidden premise 11** (whether AdS and 2D results transfer to 4D asymptotically flat spacetime) is addressed only indirectly: by MMP, FGM 2019 and Emparan et al. (4D asymptotically flat, up to cosmic strings or fluxes) and by Bilotta (Kerr, perturbative).

---

## 7. Source-quality notes

- **Contradicted claims dropped:** none. No checker returned "contradicted".
- **Status and attribution corrections applied:**
  - **RT-03** (status-wrong): arXiv gr-qc/9710001 is the Haifa proceedings "Generic wormhole throats", not PRL 81, 746. Its content is kept and paired with RC-11 (PRD 56, 4745, static only), which is unverified.
  - **RT-15:** the quoted wording is a paraphrase. D-40 uses RC-10's verbatim wording instead.
  - **RT-07:** values verified, but the "quote" is a paraphrase, so the equations are cited, not quoted. The low-confidence flag was lifted (checker).
  - **RT-11 / RF-08:** FGM's "prohibition" is presented as a general argument from the GSL, valid "at least in higher dimensions", not as a 4D theorem (D-33).
  - **RQ-08:** it blended two Kontou passages. "Would not be traversable" applies to generic Planck-scale throats. The Ford–Roman Planck-size statement now rests on RC-12 (FT, verified), not on RQ-08's search summary.
  - **RQ-12:** the Sycamore "N = 7, 5 terms" detail is re-sourced to Kobrin et al. (verified: seven Majoranas, five commuting terms). The "N = 10, 210 terms" detail is dropped as unverified.
  - **RQ-13:** the closed-form BKR mass formula is marked unverified.
  - **RQ-14:** the negative-ADM-mass scope is narrowed to solutions near the critical line.
  - **RQ-18:** "open less than the Planck time" is re-based on the primary Freivogel et al. paper (RT-29). Kontou's ref. [78] remains unidentified.
  - **RC-13 / RF-13:** the Kobrin et al. critique was presented as an unrefereed preprint. It was published as a Nature Matters Arising in 2025 (RE-05).
  - **RC-16:** the MSY bound is marked as parametric.
  - **RC-18:** N_f > 1e52 is scoped to the 1e3 kg free-fermion estimate.
  - **RC-20:** the internal preprint/peer-reviewed inconsistency is resolved to peer-reviewed (INSPIRE).
  - **RE-23:** the publication year is corrected to 1999.
  - **RE-24:** the "~1e29 mass gap" is flagged because its 1e5 kg denominator is unsourced and questionable.
  - **RF-21:** read with the caveat that 2e34 kg is the extremal black-hole mass, while the binding energy is only about 5e9 kg.
- **Unverifiable claims kept, labelled [unverified]:** RT-20, RT-30, RT-31, RT-32, RQ-08, RQ-12 (in part), RC-11, RC-15, RC-19, RC-21, RE-08, RE-09 (Su et al.), RE-19 (3.9 TeV), RE-22, RE-23 (1998 figures), RE-24, RF-04, RF-16 to RF-19. Most are duplicated by a verified claim from another facet: RC-15 by RT-04/RT-05, RC-19 by RE-14, RC-21 by RT-10, RT-30 by RC-12.
- **The checkers left these claims unchecked:** RC-02, RC-03, RC-04, RC-08, RC-13, RC-15, RC-19. Except for RC-03 and RC-13, each is duplicated by a verified claim (RT-01, RF-03, RE-04, RT-27), and RC-03 (Urban–Olum) is treated as full-text but unchecked.
- **Share of claims resting only on search summaries:**
  - research claims whose only access is SS: 5 of 114 (about 4%): RT-17, RT-31, RT-32, RE-24 and RF-18. RT-17 is superseded by the full-text RT-18;
  - claims with at least one SS-only component: about 12 of 114 (about 11%), adding RQ-08, RQ-12, RE-09, RE-19, RE-21, RE-22 and RE-23;
  - in this dossier, items resting on SS alone are: the Morris–Thorne 1 g criterion (D-34), the Morris–Thorne NEC formula (D-44), the TRL judgements (D-58), D-55, the Su et al. run, the 3.9 TeV MoEDAL limit, −15 dB squeezing, the 1998 Casimir figures and the Ellis shadow point.
- **Fringe and speculative material:**
  - nothing was excluded as fringe;
  - Maclay & Davis are retained as contested and low-confidence;
  - classical Casimir-like and warp-drive solutions are confined to Section 5;
  - Maldacena–Milekhin's RS II dark sector is peer-reviewed but uses speculative physics, as the authors themselves say.
- **Missing facets:** none. All five (theory, quantitative, critiques, engineering, frontier) have research and check files. The missing *topics* inside them are listed in Section 6, most importantly thin-shell wormholes, the classical time-machine and chronology-protection primaries, and the explicit ANEC, achronality and T_thru/T_ext calculations the brief requested.
