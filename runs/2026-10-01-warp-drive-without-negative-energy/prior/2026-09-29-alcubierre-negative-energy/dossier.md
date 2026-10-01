# Dossier: Negative-energy options for a superluminal Alcubierre-type drive
slug: 2026-09-29-alcubierre-negative-energy | depth: quick | compiled 2026-09-29

**Read this first.** This is a quick run: three facets (theory RT, quantitative RQ, critiques RC) and **no source-check files**. Every claim below is therefore **unchecked**; no check has verified it. Status labels such as "peer-reviewed" are the researchers' own, and ACCESS labels are carried through unchanged. The engineering (E) and frontier (F) facets were not run.

**Units.** Geometric units (G = c = 1) unless a line says SI. Masses are in kg, with M_sun = 1.989e30 kg and M_J = 1.898e27 kg (brief convention). Unless stated, v is in units of c.

**Conventions.** "Eulerian" means observers normal to the t = const slices. Wall thickness Δ uses the Pfenning–Ford (PF) convention unless stated; σ is Alcubierre's steepness, roughly 2/Δ. "(ours)" marks arithmetic by a researcher of this run, not a figure from the source.

## 1. Established
All items are unchecked (quick run). Where a paper is the only source, the item states the claim that paper makes.

- [D-01] **Alcubierre metric and energy conditions.** Alcubierre's metric is ds² = −dt² + (dx − v_s f(r_s) dt)² + dy² + dz², where f is a top-hat of radius R and steepness σ. The Eulerian energy density is nowhere positive, so the weak and dominant energy conditions (WEC, DEC) fail; Alcubierre states that the strong energy condition (SEC) fails too. His conclusion: "one needs exotic matter to travel faster than the speed of light". (refs: RT-01) peer-reviewed, full-text
- [D-02] **Energy density and its scaling.** The Eulerian energy density is −(v²/32π)[(∂f/∂x)² + (∂f/∂y)²] < 0, arranged as a torus around the axis of travel. For spherically symmetric f, the total is E = −(1/12) v² ∫ r² (df/dr)² dr (PF form). Lobo–Visser estimate M_warp ≈ −v²R²σ for the tanh profile. The requirement scales "quadratically with bubble velocity, quadratically with bubble size, and inversely as the thickness of the bubble wall", i.e. |E| ∝ v²R²/Δ. The O(1) coefficient depends on the profile and on the Δ convention: 1/18 for tanh and 1/12 for a linear ramp in the brief's convention. Lobo–Visser's ≈ v²R²σ is an order-of-magnitude estimate. (refs: RT-02, RQ-05) peer-reviewed, full-text
- [D-03] **Null energy condition (NEC) at any speed.** The Alcubierre spacetime violates the NEC "for all v". In the weak-field limit, G_tt + Σ G_ii = −2 Tr(K²) < 0 with K = O(v), so "localized NEC violations are ubiquitous and persist to arbitrarily low warp bubble velocities". The same holds for Natário's drive. Needing negative energy is therefore **not** a threshold effect at v = c. (refs: RT-03, RQ-17, RC-16) peer-reviewed, full-text
- [D-04] **Natário zero-expansion drive.**
  - The expansion is "but a marginal consequence" of Alcubierre's choice of shift. With θ = ∇·X = 0, the Eulerian density is ρ = −K_ij K^ij/(16π) ≤ 0, zero only if K_ij ≡ 0.
  - Natário's spherical example: ρ = −(v_s²/8π)[3(f′)² cos²θ + (f′ + r f″/2)² sin²θ].
  - Lobo–Visser: the WEC is violated everywhere, with M_warp = −(1/16π) ∫ Tr(K²) d³x, the same v²R²σ scaling as Alcubierre.
  - Santiago et al.: ρ + p̄ = −(1/8π) tr(K²) ≤ 0, so the NEC is violated too.
  - **Zero expansion redistributes the negative energy; it does not remove or reduce its scale.** (refs: RT-13, RQ-16, RC-03) peer-reviewed, full-text
- [D-05] **Van Den Broeck geometry.** A ship pocket of about 100 m internal size (inner diameter 200 m per RQ-03) sits inside a femtometre-scale outer bubble, using a large spatial expansion factor.
  - Parameters: α = 1e17, Δ̃ = 1e-15 m, R̃ = 1e-15 m, R = 3e-15 m.
  - This cuts the total negative mass to "a few solar masses, accompanied by a comparable amount of positive energy", at v_s ≈ 1 and for Eulerian observers.
  - Cost: curvature radii of about ten Planck lengths. The paper concedes that "the geometry still has structure with sizes only a few orders of magnitude above the Planck scale; this seems to be generic for spacetimes allowing superluminal travel", and that generating the negative energy remains unsolved. Numbers are in section 2. (refs: RT-14, RQ-03, RQ-04, RQ-15, RC-12) peer-reviewed, full-text
- [D-06] **Eulerian positivity does not establish the WEC.** The WEC needs every timelike observer to see ρ ≥ 0.
  - Counterexample (Santiago et al.): a stress-energy with rest-frame density ρ₀ > 0 is seen as ρ₀γ²(1 − Γ²v²), which is negative for a subluminal observer with |v| > 1/Γ.
  - For zero-vorticity (Hawking–Ellis type I) drives, Eulerian ρ ≥ 0 **plus** the NEC implies the WEC, so the NEC must be checked separately.
  - All three 2021 positive-energy papers work with the Eulerian density ρ = (1/16π)(K² − tr K²). Bobrick–Martire compute only that quantity. Santiago et al. call Fell–Heisenberg's "hidden geometric structure" (K² − tr K² = 2 tr cof K) "less useful than one might hope", and say all three should compute the stresses T_ij. (refs: RC-01, RC-02, RC-04, RQ-08, RT-15) peer-reviewed, full-text
- [D-07] **Bobrick–Martire's positive-energy drives are subluminal only.**
  - Their positive-energy, spherically symmetric solutions "are always subluminal, satisfy the energy conditions". They state that "negative energy densities are a general property of any superluminal drive (Olum 1998, Visser et al. 2000)".
  - Any warp drive "is realised through a shell of ordinary or exotic negative energy density material", moving inertially. "There are no self-consistent warp drive solutions proposed in the literature which can self-accelerate at all from zero velocities."
  - They claim a reduction of about two orders of magnitude in the Alcubierre negative-energy requirement. Its R, Δ and v were not extracted. (refs: RQ-09, RC-17) peer-reviewed, full-text
- [D-08] **Casimir source: the textbook ideal-plate result.**
  - u = −π²ħc/(720 a⁴) and energy per area −π²ħc/(720 a³), for perfect conductors at T = 0. Values are in section 2.
  - Olum's worked example gives the stress tensor between plates: T_ab = (π²/720 d⁴) diag(−1, 1, 1, −3). It can make a normal null ray converge less (R_ab K^a K^b = −2π³/(45 d⁴)), so Casimir negative energy is real and gravitationally relevant in principle.
  - The tensor is anisotropic with large pressures, unlike the Alcubierre stress-energy. (refs: RQ-12 [search-summary, own calc], RC-08 [full-text]) textbook / peer-reviewed
- [D-09] **Demonstrated Casimir experiments measured forces, not usable energy.**
  - Lamoreaux 1997: 0.6–6 µm.
  - Mohideen & Roy 1998: 0.1–0.9 µm, sphere–plate.
  - Bressi et al. 2002: parallel metallic plates, gap not read.
  - None extracted or concentrated negative energy. (refs: RQ-13) peer-reviewed; ACCESS abstract/title only
- [D-10] **Squeezed light.** The best demonstrated squeezing is 15 dB below the shot-noise variance (Vahlbruch et al. 2016; title seen only). The facet found no absolute negative energy density in J/m³ and no duration. (refs: RQ-14) ACCESS: title for Vahlbruch; full-text for Maclay–Davis
- [D-11] **White et al. 2021 (EPJC 81, 677) is a qualitative shape match, not a source.**
  - Method: worldline numerics, massless scalar, Dirichlet boundaries, a 1 µm sphere in a 4 µm cylinder. It "cannot assess any frequency dependence of materials" and ignores temperature.
  - It gives no metric, no stresses other than the density, and no total-energy or length-scale match to a ship bubble.
  - The "real, albeit humble, warp bubble" is a stated conjecture for chip-scale experiments. (refs: RC-20) peer-reviewed, full-text
- [D-12] **Matter the bubble meets (test particles, no backreaction).** In a superluminal Alcubierre bubble, some particles are captured at the front and never reach the ship, and others are ejected. Particles catching up from behind arrive with blueshift 0 < b ≤ 1, head-on ones with b ≥ 1. (refs: RC-21) peer-reviewed, full-text, medium

## 2. Quantitative anchors
The reference case is R = 100 m, v = 10c (4.37 ly in about 0.44 yr, per the brief), with Δ = 1 m or Δ at the QI limit. "Ours" means arithmetic by an RQ researcher in `[calc: runs/2026-09-29-alcubierre-negative-energy/calc/quantitative_reference.py]`. That file was read by the compiler but not re-run.

| ID | Quantity | Value (units) | Conditions | Source refs | Access |
|---|---|---|---|---|---|
| D-13 | Alcubierre wall thickness allowed by QI | Δ ≤ 1e2 v L_P (L_P = 1.6e-35 m, so about 1.6e-33 m at v = 1c and 1.6e-32 m at v = 10c) | PF 1997; flat-space Ford–Roman QI, free massless scalar, sampling parameter α = 1/10, linear-ramp Δ convention | RT-04, RQ-01, RC-10 | full-text |
| D-14 | Alcubierre total negative energy at the QI wall | E ≤ −6.2e65 v g = −6.2e62 v kg ≈ −3e20 v M_galaxy (M_galaxy = 1e12 M_sun) | R = 100 m, PF Eq. 29/31; Eulerian | RT-04, RQ-01, RQ-02, RC-10 | full-text |
| D-15 | Scaling at the QI wall | E ∝ v R² (one decade in E per decade in v) | Δ ∝ v at the QI limit | RQ-02, RC-11 | full-text |
| D-16 | Reference: Alcubierre, Δ = 1 m, v = 1c | E = −6.7e46 J = −7.5e29 kg = −0.38 M_sun = −394 M_J | tanh, E = −v²R²/(18Δ)·c⁴/G (SI, c⁴/G = 1.21e44 N), R = 100 m | RQ-11 (ours) | search-summary (own calc) |
| D-17 | Reference: Alcubierre, Δ = 1 m, **v = 10c** | E = −6.7e48 J = **−7.5e31 kg = −38 M_sun** | as D-16; ∝ v² | RQ-11 (ours) | search-summary (own calc) |
| D-18 | Reference: Alcubierre at the QI wall | −4.6e62 kg (tanh) and −6.9e62 kg (linear ramp) at v = 1c; **−4.6e63 kg = 2.3e33 M_sun at v = 10c** | Δ = 100 v L_P; linear ramp is within 11% of PF's 6.2e62 kg | RQ-11 (ours) | search-summary (own calc) |
| D-19 | Thick-wall floor | E → −(v²R/12)·c⁴/G = −1.0e45 J = −1.1e28 kg = −5.9 M_J (v = 1c); −1.1e30 kg = −0.56 M_sun (v = 10c) | Δ → ∞, R = 100 m; linear in R, quadratic in v. The formula E_min = −(v²/12)R(R + D)/D comes from an earlier repository note and was **not re-derived** | RQ-11; brief (prior run wall_thickness.py) | search-summary (own calc) |
| D-20 | Van Den Broeck region II negative energy | E_II,− = −1.4e30 kg (0.70 M_sun, 738 M_J, 1.26e47 J, ours) | v_s ≈ 1, Eulerian; α = 1e17, R = 3e-15 m, Δ̃ = R̃ = 1e-15 m | RQ-03, RQ-15, RT-14 | full-text |
| D-21 | Van Den Broeck region II positive energy | E_II,+ = +4.9e30 kg (≈ 2.5 M_sun, ours) | region w > 0.981 | RQ-03, RC-12 | full-text |
| D-22 | Van Den Broeck outer (Alcubierre-like) region | E_IV ≈ −6.3e29 v_s kg | outer bubble R = 3e-15 m | RQ-03 | full-text |
| D-23 | Van Den Broeck reduction factor | ≈ 1e32 (6.2e62 / 1.4e30 = 4.4e32, ours) | against PF at R = 100 m, v ≈ 1 | RQ-03 | full-text + own arithmetic |
| D-24 | Van Den Broeck QI check | peak LHS ≈ −6.6e93 kg/m³ vs bound ≈ −9.2e94 kg/m³ ("amply satisfied") | Eulerian observers only; free massless scalar; τ₀ = 0.1 × minimum curvature radius | RQ-04 | full-text |
| D-25 | Van Den Broeck curvature scale | curvature radius about 10 L_P; neck 3e-15 m ≈ 2e20 L_P (ours) | as D-20 | RQ-04, RQ-15, RC-12 | full-text |
| D-26 | Fell–Heisenberg example | ρ_max ≈ 3.2e26 kg/m³; E_total ≈ 9.25e43 J = 1.0e27 kg = 0.54 M_J = 5.2e-4 M_sun (ours); central shift 1.26c | their Fig. 2 configuration; Eulerian energy only; length scale not stated in the passages read; authors: SEC violated, "more than likely" forms a black hole | RQ-07, RC-18 | full-text |
| D-27 | Bobrick–Martire optimisation | about 1e2 (two orders of magnitude) less negative energy than Alcubierre | parameters not extracted | RQ-09 | full-text (abstract phrase) |
| D-28 | Rodal 2026 irrotational drive | peak proper-energy deficit about 38× below Alcubierre and 2.6e3× below Natário; peak NEC violation more than 60× below Natário | "identical profile parameters" per the paper; not reproduced | RC-07 | full-text |
| D-29 | Ideal Casimir energy density | −4.3e8 J/m³ (−4.8e-9 kg/m³) at a = 1 nm; −4.3 J/m³ at 100 nm; −4.3e-4 J/m³ at 1 µm | perfect conductors, T = 0, SI | RQ-12 (ours) | search-summary (own calc) |
| D-30 | Ideal Casimir energy, 1 cm² plates at 1 nm | E = −4.3e-5 J = −4.8e-22 kg | as D-29 | RQ-12 (ours) | search-summary (own calc) |
| D-31 | Casimir pressure at 100 nm | ≈ 13 Pa (= 3\|u\|) | ideal plates | RQ-13 (ours) | own arithmetic |
| D-32 | Measured Casimir gap ranges | 0.6–6 µm (Lamoreaux 1997); 0.1–0.9 µm (Mohideen & Roy 1998) | force measurements | RQ-13 | abstract/title |
| D-33 | Energy-density gap, Alcubierre wall vs 1 nm Casimir | peak about 1.2e42 J/m³, i.e. 10^33.4 × (Δ = 1 m, v = 1c); about 4.6e107 J/m³, i.e. 10^99 × (Δ = 1.6e-33 m) | order of magnitude only, with f′ ≈ 1/Δ; SI | RQ-12 (ours) | search-summary (own calc) |
| D-34 | Energy-density gap, Van Den Broeck vs 1 nm Casimir | 6.6e93 kg/m³ ≈ 5.9e110 J/m³, i.e. 10^102 × | SI | RQ-12, RQ-15 (ours) | own calc |
| D-35 | Total-energy gap vs Casimir plates | about 1e51 cm² of ideal 1 nm plates for 7.5e29 kg (D-16); Van Den Broeck 1.26e47 J / 4.3e-5 J ≈ 2.9e51 (per cm² of plates) | ignores plate mass, geometry and the wrong stress tensor | RQ-12, RQ-15 (ours) | search-summary (own calc) |
| D-36 | Ford–Roman QI | ρ̂ ≥ −3/(32π² t₀⁴) (ħ = c = 1); in SI, magnitude 3ħc/(32π²(c t₀)⁴); electromagnetic bound 2× more negative | free fields, 4D Minkowski, inertial observer, Lorentzian sampling of width t₀ | RT-06 | full-text |
| D-37 | Lobo–Visser weak-field ship bound | v²R²σ ≲ M_ship (geometric) | linearized; volume-integrated WEC required ≥ 0 | RQ-06, RT-03 | full-text (medium) |
| D-38 | Best squeezing | 15 dB below shot noise | optical; no absolute J/m³ found | RQ-14 | title only |
| D-39 | Finazzi et al. backreaction timescale | ≈ 1/κ after the white horizon forms; Hawking temperature T_H = κ/2π | 2D model, superluminal, dynamical formation | RC-15 | full-text |

**Scaling summary**, taken from the rows above:

| Option | Scaling of \|E\| | Reference-case value (R = 100 m) | Demonstrated | Gap |
|---|---|---|---|---|
| Alcubierre, fixed Δ | v²R²/Δ | 7.5e31 kg at 10c, Δ = 1 m | 4.8e-22 kg per cm² of ideal 1 nm Casimir plates | total energy about 1e51 cm² of plates at v = 1c, Δ = 1 m (D-35); no facet computed it at 10c; density 10^33.4 (v = 1c) |
| Alcubierre, QI wall | vR² | 4.6e63 kg at 10c | same | about 10^99 in density at v = 1c |
| Thick-wall floor | v²R | 1.1e30 kg at 10c (prior-note formula) | same | not computed |
| Natário | same v²R²σ scaling as Alcubierre, O(1) coefficient | not computed | same | not computed |
| Van Den Broeck | E_IV ∝ v_s; v-scaling of E_II not extracted | 1.4e30 kg (−) and 4.9e30 kg (+) at v ≈ 1 | same | about 10^51.5 in total energy; 10^102 in density |

Blank "not computed" cells are gaps (section 6); the compiler added no numbers.

## 3. Contested or conflicting
- [D-40] **Lentz 2021: superluminal solitons with positive energy, sourced by Einstein–Maxwell plasma.**
  - For: Lentz 2021 claims no negative-energy source is needed (RQ-10, abstract only; no total-mass figure found). His 2022/23 reply says Santiago et al.'s divergence-theorem argument "does not hold" for his soliton, because his Eulerian density is non-smooth at the source boundaries x = 0 and y = 0 (RC-05). He himself lists the DEC, horizons and a creation mechanism as open problems.
  - Against: Santiago, Schuster & Visser 2022 say the claim is incomplete, because only Eulerian observers were checked (RC-01, RC-02, RC-04). Celmaster & Rubin 2025 find regions of **negative Eulerian** energy density in Lentz's own drive, several derivation errors, and WEC violation even in a corrected version (RC-06, **preprint**).
  - Status: claimed superluminal; disputed; no peer-reviewed confirmation of the claim, and the strongest specific rebuttal is a preprint.
- [D-41] **Fell–Heisenberg 2021: Eulerian ρ ≥ 0 within "a certain subclass", example total 9.25e43 J (D-26).**
  - For: the paper (RQ-07, RC-18).
  - Against: Santiago et al. (RC-01 to RC-04). Eulerian positivity alone does not give the WEC or NEC, and zero-vorticity drives of this type must violate the SEC or the WEC.
  - The authors themselves state that their configurations violate the SEC. RQ-07 also says they concede DEC violation, but that part is not in the quoted text.
  - Status: claimed superluminal (central shift 1.26c); WEC and NEC for all observers not demonstrated; no published reply found.
- [D-42] **Bobrick–Martire's superluminal solutions.** They claim these "satisfy quantum inequalities" (RC-17) and concede they still need negative energy (RQ-09). The facets found no independent check of the QI claim beyond Santiago et al.'s general critique.
- [D-43] **Superluminal censorship.**
  - Visser, Bassett & Liberati 2000: in linearized gravity, the NEC narrows light cones, so no effective faster-than-light travel without NEC violation (RT-12, RC-09).
  - Gao & Wald 2000: the comparison is gauge dependent. This is known only through Barceló et al.'s account; the original was not opened.
  - Barceló et al. 2023/24 argue both are correct in different paradigms (RT-12).
- [D-44] **Reach of Olum's theorem.** Olum 1998 proves WEC violation under his definition of superluminal travel (RT-05, RC-08). Baird 1999 argues hyper-fast travel without exotic matter for one-way information delivery under restricted set-ups (RC-22: **preprint, abstract only, low confidence, no adopters found**).
- [D-45] **Semiclassical divergence: static versus dynamical.**
  - Hiscock 1997: ⟨T_μν⟩ diverges for v > c in a 2D reduction (RT-10, RC-14).
  - Finazzi et al. 2009: a dynamical formation from flat space gives thermal Hawking flux and exponential growth of the renormalized stress-energy tensor (RSET) at the front wall (RT-11, RC-15).
  - Both conclude instability. The facets disagree on which paper uses a "Boulware-like" vacuum: RT-11 attributes it to Finazzi, RC-14 to Hiscock (with Finazzi arguing dynamical formation selects otherwise). Neither is quoted on this, so it is unresolved.
  - RC-15 also records that Finazzi et al. say the Cauchy-horizon divergence would be avoided if superluminal operation lasts only a finite time.
- [D-46] **Squeezed light versus a proposed QI.** Maclay & Davis 2019 meta-analysis: measured squeezed-light data violate a proposed squeezed-light QI "by much or all of the data" for all physically reasonable sampling choices, while matching an ideal optical parametric amplifier (OPA) model. They read this as an unresolved inconsistency, **not** as a demonstration of large negative energy (RQ-14; status labelled preprint by RQ, though a Found. Phys. venue is given).
- [D-47] **QI-limited wall value.**
  - PF: Δ ≤ 1e2 v L_P, giving 4.6e62 kg (tanh) or 6.9e62 kg (ramp) at v = 1c (D-13, D-18).
  - The earlier repository smoke test (brief): about 51 L_P, giving about −9.0e62 kg.
  - The difference is about a factor of 2, which the facets attribute to the Δ convention and α choice; not rechecked (RT gaps).
- [D-48] **Do superluminal warp drives necessarily allow closed timelike curves (CTCs)?**
  - A summary line in RT-16 (Kontou–Sanders) says the Alcubierre bubble "necessarily" involves causality violation, but that wording is not in the quoted text.
  - Everett 1996 (abstract only) and Shoshany–Snodgrass 2024 give **constructions** that produce closed causal loops, not proofs that every drive must have them (RT-09, RC-19).
  - Chronology protection is a conjecture.

## 4. Constraints: theorems, bounds, no-go results, each with its assumptions
- [D-50] **Olum 1998 (theorem, classical GR).** Superluminal travel requires **WEC** violation. The proof uses the Raychaudhuri equation along a null geodesic, so what fails is in effect R_ab K^a K^b ≥ 0.
  - Assumptions: Olum's definition of superluminal (the path reaches the destination surface before any neighbouring path, with no conjugate points), the generic condition (which holds if there is any normal matter or transverse tidal force on the path), and no singularities.
  - Coverage: any spacetime class meeting the definition. A metric that is flat space in odd coordinates does not qualify. (RT-05, RC-08)
- [D-51] **Santiago, Schuster & Visser 2022 (classical GR).**
  - Class: Natário-class metrics (unit lapse, flat spatial slices, Minkowski exterior), including Alcubierre, Natário, and Lentz and Fell–Heisenberg zero-vorticity drives.
  - Result: within this class, all physically reasonable warp drives violate the **WEC, SEC and DEC**, and the **NEC** "under plausible subsidiary conditions" (conditional, not unconditional). Natário's theorem 1.7: a generic drive in this class violates the SEC or the WEC.
  - Not a proof for Bobrick–Martire shells with non-flat slicing. (RT-15, RC-01, RC-03)
- [D-52] **Lobo & Visser 2004 (classical GR).** For the Alcubierre and Natário metrics (flat slices, unit lapse), the **NEC** is violated at every v, including v ≪ c (weak-field). A volume-integrated WEC ≥ 0 requires v²R²σ ≲ M_ship, so the negative field energy must be comparable to the ship's own mass. (RT-03, RQ-06, RC-16)
- [D-53] **Visser, Bassett & Liberati 2000 (perturbative).** In linearized gravity about Minkowski, the **NEC** implies Shapiro delay, never advance, so no effective superluminality. Its gauge status is contested (D-43). (RT-12, RC-09)
- [D-54] **Ford–Roman quantum inequality (proven).** ρ̂ ≥ −3/(32π² t₀⁴) with Lorentzian sampling.
  - Proven for **free** massless or massive scalar fields (EM bound 2× more negative), in **4D Minkowski**, along an **inertial** worldline.
  - Applied to curved spacetime only when the sampling time is short compared with the local curvature radius. Not a theorem for interacting fields or general curved backgrounds.
  - Fewster's general quantum energy inequalities (QEIs) were not opened. (RT-06)
- [D-55] **Pfenning–Ford 1997 (application of D-54).**
  - Result: Alcubierre wall Δ ≤ 1e2 v L_P for α = 1/10, which forces E ≈ −6.2e62 v kg at R = 100 m.
  - Assumptions: the wall is treated as locally flat; free massless scalar; sampling-time choice α; Eulerian energy; linear-ramp Δ. (RT-04, RQ-01, RC-10, RC-11)
- [D-56] **Quantum interest.** A negative-energy pulse must be followed by a compensating positive pulse, with separation inversely proportional to amplitude.
  - The overcompensation ("interest") is **proven only for δ-function pulses of massless scalars in 2D and 4D Minkowski**; elsewhere it is a conjecture.
  - Implication: no sustained steady-state negative energy from generic QFT states. (RT-07)
- [D-57] **Averaged null energy condition (ANEC).** Proven (Wald–Yurtsever) for Hadamard states of a massless scalar in globally hyperbolic **2D** spacetimes along complete **achronal** null geodesics, with results for 4D Minkowski. It is argued not to hold for all states in all 4D spacetimes. (RT-16)
- [D-58] **Horizon and control (Everett–Roman 1997).** At v > c, the ship at the centre is causally cut off from the front wall, so it "can neither create a warp bubble on demand nor control one". Fell–Heisenberg likewise cite horizons as making the Alcubierre soliton uncontrollable. (RT-08, RC-13, RC-18)
- [D-59] **Krasnikov tube as pre-laid infrastructure (out of scope except as a reframe).**
  - It removes the control problem, but the one-way trip cannot be shortened; only the round trip as timed by Earth clocks can.
  - It still needs "unphysically thin layers of negative energy density", and two non-overlapping tubes make a time machine.
  - Krasnikov 1998: under reasonable assumptions in globally hyperbolic spacetimes, the traveller cannot reach the destination sooner. (RT-08, RC-13)
- [D-60] **Causality.** Everett 1996 (abstract) and Shoshany–Snodgrass 2024 construct warp-drive spacetimes with closed causal loops. Hawking's chronology protection is a **conjecture**. Whether CTCs arise depends on being able to produce bubbles at will. (RT-09, RC-19)
- [D-61] **Semiclassical instability (superluminal only).**
  - Hiscock 1997: in 2D, with a free conformal scalar, ⟨T_μν⟩ is regular for v < c and diverges for v > c.
  - Finazzi, Liberati & Barceló 2009: for a dynamical superluminal bubble, thermal Hawking flux at the centre ("extremely high" if the exotic matter obeys QIs), and exponential growth of the RSET at the front wall within a time of order 1/κ.
  - Both are 2D, single-field models, not full 4D self-consistent solutions. (RT-10, RT-11, RC-14, RC-15)
- [D-62] **No self-acceleration (Bobrick–Martire).** No proposed self-consistent warp solution accelerates from rest, so a warp shell needs external propulsion. (RC-17)
- [D-63] **Tidal forces.** No literature source was found by any facet. Only the earlier repository calculation quoted in the brief exists (see D-72).

## 5. Frontier and speculative (labelled; not established)
- [D-64] [frontier, peer-reviewed single paper, not reproduced] **Rodal 2026 (Gen. Relativ. Gravit. 58).** An explicit irrotational, unit-lapse, flat-slice drive that is globally Hawking–Ellis type I, with "predominantly positive" invariant energy density. It **reduces but does not eliminate** NEC/WEC violation (factors in D-28). This is consistent with D-51, not a counterexample. Whether it is superluminal was not recorded. (RC-07)
- [D-65] [frontier, contested] **Lentz positive-energy hyper-fast solitons in Einstein–Maxwell plasma.** See D-40. (RQ-10, RC-05, RC-06)
- [D-66] [frontier, contested] **Fell–Heisenberg Eulerian-positive superluminal subclass.** See D-41. (RQ-07, RC-18)
- [D-67] [frontier] **Bobrick–Martire superluminal QI-satisfying solutions**, which still need negative energy. (RC-17, RQ-09)
- [D-68] [speculative] **White et al. 2021 chip-scale "humble warp bubble".** A qualitative Casimir-density pattern, with no metric or energy match. No replication or independent critique was found, and it is not known whether the experiment was performed. (RC-20)
- [D-69] [frontier, preprint] **Le 2026.** An observer-robust test of energy conditions: the NEC, WEC and SEC as 4×4 linear matrix inequalities via the S-lemma, and two tests for the DEC. It answers the "Eulerian-only" objection methodologically; no results were read. (RC-23)
- [D-70] [speculative, preprint, low] **Baird 1999.** Exotic-matter-free hyper-fast delivery in restricted one-way set-ups. (RC-22)
- [D-71] [not researched] **Speculative extensions allowed by the brief:** extra dimensions or brane worlds, Einstein–Cartan torsion, modified gravity, non-minimal or phantom fields, negative-mass matter. No facet covered them, so there are no claims.

## 6. Unknowns and gaps
- [D-72] **Tidal forces on ship and crew.** No literature. The brief quotes an earlier repository calculation (`runs/2026-09-29-warp-bubble-shapes/calc/interior_tides.py`), which is **not literature and was not rechecked** here:
  - Case: R = 50 m, v = c, 10 m wall.
  - Stretch: 0.04 g/m near the centre, 36 g/m at 10 m, 2,000 g/m at 15 m; tides scale as v².
  - Outside the bubble, above 100 g/m out to 170 km.
- **White's thick-wall and oscillating variants** ("Warp Field Mechanics" 101 and 102), plus Loup et al. and Fuchs et al. No facet extracted their energy claims or critiques, although the brief lists them as in scope. The earlier run `runs/2026-09-29-warp-bubble-shapes/research/shapes.md` covers them but was not an input to this compilation.
- **Missing energy numbers:**
  - Lentz: no total-energy figure found.
  - Bobrick–Martire: parameters for the 1e2 reduction, and subluminal shell masses.
  - Fell–Heisenberg: length scale of the 9.25e43 J example, and its R, Δ, v dependence; whether the 1.26c shift is measured in the asymptotic frame.
  - Natário: reference-case energy.
  - Van Den Broeck: rescaled to v = 10c; only E_IV ∝ v_s was recorded.
- **Squeezed vacuum:** no absolute negative energy density (J/m³) or pulse duration. No orders-of-magnitude gap can be stated for it.
- **Exotic matter:** no claimed measurement of GR-sense negative energy density was found. The hidden premise about condensed-matter "negative effective mass" was not researched.
- **Separability:** the facets found no source on scaling Casimir negative energy, concentrating it into a wall, or separating it from the plates' positive mass. The brief's smoke-test figure (plates at least 7.7e9 times their energy deficit) was not re-sourced.
- **QI limits:**
  - Not opened: Fewster QEIs, curved-space and interacting-field QIs, the exact PF Eq. 22 coefficient, and the meaning of α.
  - The factor-2 discrepancy in the QI wall (D-47) is unresolved.
  - The QI check for Van Den Broeck covers Eulerian observers only.
- **Semiclassical results** exist only in 2D models; no 4D result.
- **Horizons and causality:**
  - Unread: Everett 1996 (full text), a primary source for Hawking's chronology protection, and Gao & Wald 2000 (original).
  - McMonigal et al.'s effects on the surroundings (front-wall pile-up, energy release on stopping) were not confirmed.
- **Creation mechanism:** none identified in any source (Lentz lists it as open; Bobrick–Martire say no solution self-accelerates).
- **Responses to recent critiques:** it is not known whether Lentz or others have responded to Celmaster–Rubin 2025 or Rodal 2026.

## 7. Source-quality notes
- **Checks.** None of the three facets (theory, quantitative, critiques) had a `.check.md` file, so all 57 claims (RT 17, RQ 17, RC 23) are **unchecked**. Their status and ACCESS labels are the researchers' own and are carried through unchanged.
- **Missing facets:** engineering (E) and frontier (F) were not run at quick depth. Lab values come from RQ only; frontier items come from RC.
- **Dropped:** none. No claim was contradicted by a check, and no fringe source was excluded.
- **Corrections made by the compiler** (internal inconsistencies between facets, not source checks):
  1. RC-18 converts "four orders of magnitude smaller than the solar mass" to about 2e26 kg. That is superseded by the paper's own E_total ≈ 9.25e43 J = 1.0e27 kg (RQ-07, D-26). The ratio to the Sun's rest energy (1.78e47 J) is 5.2e-4.
  2. RQ-15 calls 1.4e30 kg Van Den Broeck's "total" negative energy. It is only the region-II figure: RQ-03 also records E_IV ≈ −6.3e29 v_s kg, so D-20 and D-22 are kept separate.
  3. RT-16's "Alcubierre bubble necessarily involves causality violations" is not supported by its quote. It is downgraded to "constructions exist" (D-48, D-60).
  4. Van Den Broeck title: RT-14 prints "…with reasonable total energy requirements", while RQ-03 and RC-12 print "…with **more** reasonable…". Same arXiv ID (gr-qc/9905084); the majority form is used.
  5. RQ-07's "(and the full dominant energy condition)" for Fell–Heisenberg is not in the quoted text and is kept as unquoted.
  6. RQ-13's "energy in the gap is bounded by the gap volume (µm³ to mm³ at most)" is a researcher inference, not sourced.
  7. The facets conflict on which paper used a Boulware-like vacuum (D-45). Left unresolved.
- **Status cautions** (labels kept, flagged):
  - RQ-14 labels Maclay & Davis 2019 a preprint while giving a Found. Phys. venue.
  - RC-05 (Lentz reply) is a Marcel Grossmann proceedings paper labelled peer-reviewed.
  - RT-17 is a synthesis of RT-03, RT-05 and RT-15, labelled full-text and peer-reviewed; it is not an independent source and is not used as one.
  - RQ-09's "two orders of magnitude" figure was read from the abstract (RQ gaps), although it is labelled full-text.
  - RQ-11 and RQ-12 are labelled search-summary but are in-run calculations (the calc file was read; the numbers match its formulas; it was not re-run).
- **Share of claims resting only on search summaries:** 2 of 57 (3.5%): RQ-11 and RQ-12, both in-run calculations rather than web summaries.
  - Abstract or title only: RT-09, RQ-10, RQ-13, RC-22, and the Everett half of RC-19. That is 5 of 57 (9%), plus the Vahlbruch title in RQ-14.
  - Preprints: RC-06 (Celmaster–Rubin), RC-22 (Baird), RC-23 (Le), and RQ-14 as labelled.
- **Coverage bias.** The positive-energy claims were read mostly through their critics (Santiago et al.). Lentz's own paper was seen only as an abstract.

## User-supplied
Added at the dossier checkpoint with the user's approval. Each item condenses claims from an earlier single-researcher run in this repository, `runs/2026-09-29-warp-bubble-shapes/research/shapes.md` (IDs RS-xx). Read that file for the verbatim quotes. That run had **no separate source check**, so treat these items like the unchecked claims above. Status and ACCESS labels are that researcher's, and "(ours)" marks arithmetic added here, not in any source.

- [U-01] [user] **White's thick-wall variant.**
  - Sources: "Warp Field Mechanics 101", an NTRS 20110015936 conference paper (2011). A JBIS version exists (66, 242–247, 2013), confirmed by search summary only; its text was not read.
  - Claim: for the Alcubierre tanh metric at fixed v and R, a thicker wall "drastically" cuts the peak energy density, and the integrated energy is "orders of magnitude" lower. The cost is a smaller flat interior.
  - Missing: no closed-form scaling, no SI total, and no quantum-inequality discussion. The plotted case is v = 10c with a 10 m diameter.
  - This agrees with |E| ∝ v²R²/Δ; the thick-wall floor is D-19.
  - No published rebuttal aimed at White was found.
  - (RS-01, RS-02, RS-03, RS-06; full-text NTRS)
- [U-02] [user] [speculative] **White's oscillating variant.**
  - Source: "Warp Field Mechanics 102: Energy Optimization", NTRS 20130011213 (2013), an unrefereed slide deck.
  - Slide 16 plots "exotic mass" for a 10 m diameter bubble at v = 10c against shell-thickness fraction, with one curve per "bulk velocity" dU/dt.
  - Read by eye: the thin-shell curve with no oscillation sits near 1e28 kg (Jupiter class). The thickest-shell curve with the fastest oscillation sits near 1e3 kg (Voyager class).
  - The dU/dt dependence comes from a Chung–Freese brane-world relation ("we need to engage higher dimensional models"), not from GR. The part of the reduction beyond the thick-wall effect is therefore outside the brief's established physics.
  - (RS-04, RS-05; fringe status; values read by eye from a scanned plot)
- [U-03] [user] **Loup, Waite & Halerewicz 2001: a lapse function A** (arXiv:gr-qc/0107097, preprint, not refereed).
  - Claim: the ship-frame energy density falls as 1/A⁴, reducing the requirement "arbitrarily". Their QI analysis gives Δ ≤ 10² v L_P A₀, and they divide Pfenning's "−0.068 solar mass" figure by A₀⁴.
  - They concede the WEC is still violated in other frames. No published critique was found.
  - (RS-12)
- [U-04] [user] **Bobrick–Martire's optimizations of the Alcubierre drive** (CQG 38, 105009, 2021). These fill the D-27 parameter gap.
  - Flattening the bubble along the direction of travel by a factor α_X gives E → E/α_X. Choosing α_X = 1 + v² removes the asymptotic v-dependence.
  - The energy-optimal radial profile, f = min(r₀/r_s, 1), lowers |E| by about 3× relative to tanh.
  - The abstract's "two orders of magnitude" probably corresponds to α_X ~ 100. That is the researcher's inference, not verified.
  - Extreme flattening pushes the along-track wall to near the Planck scale. Per the paper, this meets the QIs but not the averaged null energy condition.
  - (RS-13, RS-14)
- [U-05] [user] **Bobrick–Martire on Van Den Broeck** (disputed; a derivation in their appendix). This bears on D-20 to D-25.
  - They argue Van Den Broeck's solution "is equivalent to the Alcubierre solution" in the inner observer's coordinates.
  - They say the small region-II energy comes from an expression missing the expected B(0)² v² dependence.
  - They note the outer wall is still about 100 v Planck lengths thick.
  - No reply from Van Den Broeck was found. His own follow-up preprint (gr-qc/9906050) says superluminal bubbles "seem an unlikey [sic] possibility", while subluminal ones "may still be possible".
  - (RS-10, RS-11)
- [U-06] [user] **Lentz's energy scaling** (CQG 38, 075015, 2021; full-text). This fills the D-40 energy gap.
  - E_tot ~ C v² R²/w, with C of order 1. For R = 100 m and w = 1 m he gives E_tot ~ (few)×10⁻¹ M_sun (printed with a factor v_s), "of the same magnitude" as Pfenning–Ford's estimate for an Alcubierre bubble of the same size.
  - So the claim is positive energy density, not a smaller budget. With the v² law, the reference case (v = 10c) needs of order tens of M_sun of positive energy (ours), comparable to D-17.
  - Lentz argues the QI wall limit does not apply to a plasma source. He suggests Van Den Broeck-, White- and Loup-type optimizations "may provide significant savings", but has not applied them.
  - (RS-17)
- [U-07] [user] **More on Fell–Heisenberg** (CQG 38, 155020, 2021). This adds to D-26 and D-41.
  - The exterior is Schwarzschild-like, not Minkowski, so the ADM mass is nonzero.
  - Horizons and the transition from sub- to superluminal speed are not analysed.
  - The length unit of the example (parameters Π, r, V, σ = 1/4, 6, 10, 1) was not identified, so it cannot be compared like for like with R = 100 m.
  - (RS-19)
- [U-08] [user] **Fuchs et al. 2024** (CQG 41, 095013). A constant-velocity **subluminal** warp shell that satisfies all the energy conditions.
  - It is a stable matter shell with R₁ = 10 m, R₂ = 20 m and M = 4.49e27 kg (2.365 M_J), moving at v = 0.04c.
  - No acceleration phase is solved, and it has no superluminal capability. It trades negative energy for a Jupiter-scale positive mass.
  - (RS-20)
- [U-09] [user] **How far the QI wall bound reaches.** Pfenning–Ford applied a free massless scalar QI to a spacetime not produced by such a field, so the ~1e62 kg figure is a free-field semiclassical estimate, not a theorem about all matter.
  - Krasnikov 2003 (PRD 67, 104013; abstract only) argues the relevant QI "does not (always) imply large energy densities", and that large E_tot "does not necessarily exclude shortcuts".
  - (RS-08; bears on D-54, D-55)
- [U-10] [user] **Natário's drive is not lower-energy.** This adds to D-04, D-28 and D-64.
  - No energy-reduction claim was found for it.
  - Rodal (2024, IJTP 63, 168) finds its curvature invariants are 35× larger than Alcubierre's for identical bubble parameters.
  - Rodal's 2026 irrotational drive reports a slice-integrated net proper energy consistent with zero (|E₊ − E₋|/(E₊ + E₋) = 0.04%). Its reported reductions are local peak measures, not totals.
  - (RS-15, RS-16)
- [U-11] [user] [speculative] **Other routes.** These partly fill D-71.
  - Obousy–Cleaver 2008 (JBIS 61, 364): tune the radius of a compact extra dimension to drive the bubble. Only the abstract was read, so there are no energy numbers.
  - DeBenedictis–Ilijic 2018 (CQG 35, 215001): in Einstein–Cartan gravity, torsion from spin allows warp drives that respect the energy conditions. This changes the gravity theory.
  - Rodal 2025 (preprint, arXiv:2507.09724): argues that "low-energy" routes via an engineered, spatially varying gravitational coupling either conflict with the contracted Bianchi identity or are excluded by the |γ − 1| ≲ 1e-5 solar-system bound.
  - (RS-21, RS-22, RS-23)
