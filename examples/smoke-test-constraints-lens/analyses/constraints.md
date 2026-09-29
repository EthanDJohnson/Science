# Analysis: constraints (Kant)

## Method applied
I audited the conditions any answer must meet (energy conditions, Ford–Roman quantum inequalities, conservation and thermodynamics, causality and chronology, stability), with the assumptions each needs. I computed what every candidate in the brief and dossier requires, plus five I added, using `gr_tensors.py`: Einstein-tensor T_ab, Eulerian ρ, an all-observer NEC/WEC/SEC/DEC check with the Hawking–Ellis type, and slice energies checked at n and 1.5n. A Riemann-based curvature radius sets where the flat-space QI may be applied. Each candidate is then classified as violates, strained or consistent. Units: geometric (G = c = 1, lengths in m, so ρ is in m⁻² and E in m) unless marked SI.

## Findings

1. **What each condition protects, and its assumptions.**
   - **NEC** (T_ab k^a k^b ≥ 0 for all null k). [D-02] shows generic Natário-class warp drives violate it. Background results that also rely on the NEC (no source opened in this run): the Penrose singularity and area theorems, Hawking's chronology protection for compactly generated horizons, and topological censorship (averaged form).
   - **WEC** (T_ab u^a u^b ≥ 0 for all timelike u). Olum's theorem: superluminal travel requires its violation [new: K. D. Olum, Phys. Rev. Lett. 81, 3567 (1998), https://link.aps.org/doi/10.1103/PhysRevLett.81.3567, "proves that superluminal travel requires weak-energy-condition violation"]. The theorem's definition of "superluminal" and its technical assumptions were not visible in the snippet.
   - **SEC.** It drives timelike focusing in the singularity theorems [new: E. Curiel, "A Primer on Energy Conditions", arXiv:1405.0403, https://arxiv.org/abs/1405.0403, "The strong energy condition plays a central role in the Hawking-Penrose singularity theorems, as it guarantees the focusing of timelike geodesic congruences through the Raychaudhuri equation"]. It is not protective here, because warp drives already need the stronger NEC violation.
   - **DEC** (WEC plus causal energy flux). The positive-mass and Hawking–Ellis conservation theorems rely on it (background, no source opened).
   - **Ford–Roman QI** [D-04]. It assumes a free massless scalar, flat spacetime, an inertial observer, Lorentzian sampling and no boundaries. In curved spacetime it is trusted only for sampling times τ0 ≪ the local curvature radius r_c, which is the method behind [D-05]. I use τ0 = α r_c with α = 0.01–0.5 and N = 1–100 scalar-equivalent fields.
   - **Conservation**, ∇_a T^ab = 0. It holds identically for any metric (Bianchi identity), so it constrains the matter model, not the geometry.

2. **The Alcubierre T_ab fails all four point-wise conditions at every speed tested, subluminal included.**
   - gr_tensors reproduces the ρ of [D-01] to 7.5e-9 relative.
   - At wall points for v = 0.1, 1, 2 and 10 (units of c), NEC, WEC, SEC and DEC all fail.
   - T^a_b is Hawking–Ellis type IV (complex eigenvalues, flux-dominated) at most wall points. It is type I on the equator for v ≥ 1, with rest-frame ρ0 = −0.149 m⁻² (v = 1, R = 1 m, σ = 8 m⁻¹).
   - The Eulerian momentum density is |J|/|ρ| = 0.5 at v = 1 and 5 at v = 0.1 on the equator.
   - The toolkit scan agrees: ρ = −0.637 m⁻² and min T(k,k) = −2.84 m⁻² (v = 2) [calc: runs/smoke-constraints/calc/lens-constraints_alcubierre_ec.py].
   - So negative energy is needed at every v > 0, not only above c.

3. **In the whole Natário class (unit lapse, flat slices), negative Eulerian energy is unavoidable.**
   - I derived and checked E_Eul = ∫ρ d³x = −(1/32π)∫|∇×β|² d³x ≤ 0. For a generic shift (curl and divergence both nonzero) both sides are −0.0964954 m at n = 72 and 108. For Alcubierre both are −0.2553803 m.
   - An irrotational bubble has total 5e-9 m (zero), but its negative part is −1.821 m, cancelled by an equal positive part.
   - The NEC fails at 587 of 660 sampled wall points of that bubble (min T(k,k) = −7.2 m⁻²), although it holds at its ρ-minimum [calc: runs/smoke-constraints/calc/lens-constraints_natario_class.py].
   - Corollary: a Natário-class metric with ρ_Eul ≥ 0 everywhere must have ρ_Eul ≡ 0.
   - This reproduces [D-02] computationally and answers the brief's hidden premise 1 at class level.

4. **Positive-energy warp solutions.**
   - Lentz's superluminal positive-energy claim is disputed [D-06]. A 2025 preprint reports that direct calculation gives negative Eulerian energy density [new: B. Celmaster & S. Rubin, arXiv:2511.18251 (preprint), https://arxiv.org/abs/2511.18251, "there are spacetime regions where the energy density is negative"].
   - If Lentz's metric has unit lapse and flat slices (not verified here), finding 3 already forbids ρ_Eul ≥ 0 unless ρ_Eul ≡ 0.
   - With Olum's WEC theorem (finding 1) and [D-02], a positive-energy superluminal soliton contradicts established results under their assumptions.
   - Subluminal positive-energy shells [D-06] use a non-unit lapse or curved slices. They fall outside finding 3 and violate no condition audited here, but they do not reach v > c.

5. **Requirement for a ship-scale bubble, R = 100 m** (thin-wall formula derived here: E = −v²σR²/36 − v²(π²−6)/(432σ); wall Δ := 2/σ).

   | v (c) | E at Δ = 1 m (SI) | E at Δ = 1 mm (SI) | peak \|ρ\| at Δ = 1 m (SI) |
   |---|---|---|---|
   | 0.1 | −7.5e27 kg (−3.8e-3 M_sun) | −7.5e30 kg | 1.2e40 J/m³ |
   | 1 | −7.5e29 kg (−0.38 M_sun) | −7.5e32 kg (−376 M_sun) | 1.2e42 J/m³ |
   | 2 | −3.0e30 kg (−1.5 M_sun) | −3.0e33 kg | 4.8e42 J/m³ |
   | 10 | −7.5e31 kg (−38 M_sun) | −7.5e34 kg | 1.2e44 J/m³ |

   The formula was validated three ways [calc: runs/smoke-constraints/calc/lens-constraints_alcubierre_ec.py]:
   - At σR = 8 (n = 96 and 144), the 3D slice integral, the 1D radial integral and the formula agree to 1e-12. They agree exactly at σR = 50 and 200.
   - E ∝ v² holds: E(v=3)/E(v=1) = 9.000000.
   - The peak equatorial ρ = −v²σ²/(128π) matches to 7 digits.

6. **The QI [D-04] forces Planck-scale walls, costing |E| ≈ 1e60–1e66 kg (SI) for R = 100 m and v = 1–10.**
   - The curvature radius on the equatorial wall is r_c = 2.309/(vσ). My Riemann tensor's Ricci contraction matches `ricci()` to 1e-14.
   - I imposed the QI at τ0 = α r_c, using the Lorentzian average along the geodesic Eulerian worldline (factor 0.83–1.02 at α ≤ 0.1). The maximum wall thickness is 51 L_P (v = 1), 93 L_P (v = 2) and 110 L_P (v = 10) at α = 0.1, N = 1. The most generous setting (α = 0.01, N = 100) gives 4.7e4 L_P = 7.6e-31 m (v = 1).
   - This is the same order as [D-05] and [new: M. J. Pfenning & L. H. Ford, Class. Quantum Grav. 14, 1743 (1997), https://arxiv.org/abs/gr-qc/9702026v1, "the bubble wall thickness is on the order of only a few hundred Planck lengths"].
   - E(R = 100 m) = −9.0e62 kg = −4.5e32 M_sun at v = 1, α = 0.1, N = 1. The range over v = 1–10, α = 0.01–0.5 and N = 1–100 is −9.8e59 to −1.6e66 kg.
   - The peak |ρ| is 1.8e108 J/m³ = 3.8e-6 of the Planck density, and r_c ≈ 59 L_P.
   - For v ≲ 1 the maximum thickness scales ∝ v: 6.6 L_P at v = 0.1 and 0.67 L_P at v = 0.01. Slow bubbles therefore leave the semiclassical domain.
   - Only one worldline per v was tested, and the QI must hold for every inertial observer, so the true maxima are at most these values [calc: runs/smoke-constraints/calc/lens-constraints_qi_wall.py].

7. **New here: subluminal walls violate the QI for free-field sources at any thickness.**
   - Observers at rest in the bubble frame, near the front axis in the outer tail, see a static ρ_c that is negative and first order in f. For the tanh profile, ρ_c/f = −0.004 to −0.010 (v = 0.1), −0.14 to −0.32 (v = 0.5) and −1.8 to −3.8 (v = 0.9).
   - The curvature there is also first order, so C_c = |ρ_c| r_c⁴ σ² ≈ (0.002–0.1)/f, which diverges as f → 0.
   - Their acceleration is small, a·(0.1 r_c) ≤ 4e-2, so the inertial QI applies. It fails wherever f ≲ C_c f · 32π²α⁴/(3N(L_P σ)²), a non-empty zone for every σ [calc: runs/smoke-constraints/calc/lens-constraints_qi_wall.py §6].
   - This does not apply for v > 1, where observers cannot co-move in the outer tail (v(1−f) > 1).
   - Checked for the tanh profile only.

8. **Casimir cavities [D-03] are consistent as physics but fail as a wall source.**
   - Ideal plates give ρ = −4.33e8, −4.33e4, −4.33 and −4.33e-4 J/m³ (SI) at a = 1 nm, 10 nm, 100 nm and 1 µm.
   - Stresses: p_z = 3ρ (checked numerically from −d(E/A)/da) and p_x = −ρ (tracelessness assumed). The NEC fails normal to the plates (ρ + p_z = 4ρ), and the SEC gives ρ + Σp = 2ρ < 0.
   - The plates carry far more positive energy than the Casimir deficit. Two plates of only m_p/(0.3 nm)² = 1.9e-8 kg/m² hold 7.7e9 (a = 1 nm) to 7.7e18 (a = 1 µm) times more rest energy. A net-negative cavity would need plate areal mass < 4.8e-18 kg/m² at 1 nm, so the cavity's net T_00 is positive.
   - The density gap to a 1-m-wall bubble at v = 1 is 33.4 orders (1 nm), 41.4 (100 nm) and 45.4 (1 µm).
   - The boundary-free QI does not apply here. A static −4.3e-4 J/m³ would exceed its τ0 = 1 s bound (3.7e-62 J/m³) by 58 orders, which only shows that the boundary assumption fails, not that anything is violated [calc: runs/smoke-constraints/calc/lens-constraints_sources.py].

9. **Squeezed and other free-field states are QI-capped** [D-04].
   - Per field, the QI allows 3.7e-2 J/m³ at τ0 = 1 fs and 3.7e-26 J/m³ at 1 ns. Each packet carries about 3ħ/(32π²τ0) = 1e-21 J at 1 fs.
   - In a 1-m wall at v = 1 the trusted τ0 = 3.9e-10 s allows 1.7e-24 J/m³ against 1.2e42 J/m³ required, a violation by 10^65.9 [calc: runs/smoke-constraints/calc/lens-constraints_sources.py].
   - Sub-vacuum field noise has been observed [new: C. Riek et al., Nature 541, 376 (2017), https://www.nature.com/articles/nature21024, "they found subcycle intervals with noise levels that are substantially less than the amplitude of the vacuum field"]. No measured negative energy density magnitude appears in the dossier or the snippets, so dossier gap 6 stays open.

10. **Labelled speculative: a non-minimally coupled classical scalar lies outside the free-field QI's assumptions.**
    - It can violate the energy conditions classically [new: C. Barceló & M. Visser, "Scalar fields, energy conditions, and traversable wormholes", Class. Quantum Grav. 17 (2000), https://arxiv.org/pdf/gr-qc/0003025, "A non-minimally coupled scalar field with a positive curvature coupling ξ > 0 can easily violate all the standard energy conditions, up to and including the averaged null energy condition (ANEC)"].
    - An order-of-magnitude match gives 8πGξφ² ≈ v²/4, i.e. φ ≈ (v/2)φ_c with φ_c = E_P/√(8πξ) = 5.97e18 GeV (ξ = 1/6), independent of wall thickness.
    - At v ≥ 2 the field reaches φ_c, where G_eff = G/(1 − 8πGξφ²) diverges and changes sign [calc: runs/smoke-constraints/calc/lens-constraints_sources.py §4; a scaling estimate, not a solution].

11. **Van Den Broeck [D-09] shrinks the outer-wall cost, but its expansion (B) region needs its own exotic matter.**
    - Toy model: v = 1, R_out = 1.2 m, B_max = 4. Where f = 1, K_ij = 0 and ρ = (1/8π)[|∇B|²/B⁴ − 2∇²B/B³]; gr_tensors matches this there.
    - The B-region total is positive, E_B = ½∫B'²B⁻¹r²dr = +0.753 m, but it contains −1.336 m of negative energy. NEC and WEC fail in both the B region and the outer wall.
    - Slice totals (n = 128 and 192) are +0.43117 and +0.43119 m, with a negative part of −1.658 m. The outer wall alone would need −0.321 m.
    - At physical scale, with R_out = 1e-15 m and QI-limited walls, the outer wall costs −9.0e28 kg (v = 1) to −4.2e30 kg (v = 10), i.e. 0.05–2.1 M_sun. That is consistent in order with [D-09].
    - Co-moving geodesic observers see a static ρ in the B region. In the deep part (B ≫ 1) the QI requires the proper scale B/s_B ≤ 98 L_P (α = 0.1, N = 1).
    - At the outer edge, ρ and curvature are both first order in (B − 1), and C·s_B²·(B − 1) → 0.020. The QI therefore fails near the edge of every smooth tanh-type transition.
    - Enforcing only the deep-part limit already costs E_B ≳ L_pocket²/(6 l_max), where l_max is the maximum allowed proper scale. For a 100 m pocket that is 1.4e63 kg (α = 0.1, N = 1) to 1.4e60 kg (α = 0.01, N = 100), no saving over plain Alcubierre (finding 6).
    - Untested: B profiles whose outer edge keeps ρ ≥ 0. Float64 evaluation of the unsimplified ρ is wrong for B_max ≳ 1e6 (checked against 50-digit values), so the numerics use B_max ≤ 1e4 [calc: runs/smoke-constraints/calc/lens-constraints_vdb.py].

12. **Causality and control (hidden premise 3).**
    - For v < 1 there is no horizon. For v > 1 a horizon sphere sits at f(r_h) = 1 − 1/v, with surface gravity κ = v|f'(r_h)| = 2σ(1 − 1/v); this thin-wall closed form matches numerics to ≤ 2e-6.
    - At every point of the plane ξ = r_h (bubble frame), dξ/dt ≤ 0 for all causal directions. The half-space ahead of it is therefore unreachable from the ship, and any stress-energy there must be placed in advance along the route, consistent with [D-07].
    - That half-space holds a small but nonzero share of the wall's negative energy: 3.0e-6 (v = 2) and 2.9e-5 (v = 10) for R = 100 m and Δ = 1 m, scaling as (Δ/R)² [calc: runs/smoke-constraints/calc/lens-constraints_horizon_ctc.py].

13. **Chronology.**
    - Two superluminal legs close a causal loop once the second launch frame moves at w > 2u/(1+u²) relative to the first: 0.80c for u = 2, 0.198c for u = 10 and 0.020c for u = 100. A numeric round trip at 1% above threshold returns before departure [calc: runs/smoke-constraints/calc/lens-constraints_horizon_ctc.py].
    - This matches [new: A. E. Everett, Phys. Rev. D 53, 7365 (1996), https://link.aps.org/doi/10.1103/PhysRevD.53.7365, "Everett verified this conjecture by exhibiting a simple modification of Alcubierre's model in which causal loops are possible"].
    - It assumes bubbles can be launched at speed u from any inertial frame.

14. **Thermodynamics and stability.**
    - The horizon temperature T = ħcκ/(2πk_B) is 7.3e-4 K for Δ = 1 m (v = 2). For the QI-limited wall it is 4.8e29 K, i.e. 3.4e-3 of the Planck temperature.
    - The natural time scale 1/(cκ) is 1.7e-9 s and 2.5e-42 s respectively. I use it as my own dimensional estimate for the exponential stress-energy (RSET) growth at the front horizon [D-08]; the dossier gives no rate [calc: runs/smoke-constraints/calc/lens-constraints_horizon_ctc.py].
    - Semiclassical gravity is least reliable exactly where energy is negative [new: C.-I. Kuo & L. H. Ford, Phys. Rev. D 47, 4510 (1993), https://link.aps.org/doi/10.1103/PhysRevD.47.4510, "The energy density fluctuations are large whenever the local energy density is negative"].
    - No classical stability analysis of any wall matter model is in the dossier (gap).

15. **Classification.** A bound whose assumptions fail is not counted as violated.

    | Candidate | Class | Decisive constraint (finding) | Holds under |
    |---|---|---|---|
    | Casimir cavities as wall source [D-03] | violates | net cavity energy positive by ≥ 7.7e9; density gap 33–45 orders (8) | material plates ≥ m_p/(0.3 nm)²; ideal-plate upper bound |
    | Free-field states (squeezed, moving mirrors), wall ≥ mm | violates | QI exceeded by 10^66 at Δ = 1 m (9) | free fields, τ0 = 0.1 r_c |
    | Free-field states, QI-limited wall, v > 1 [D-05] | strained | E ≈ 1e60–1e66 kg for R = 100 m; r_c ≈ 13–60 L_P (6) | stated α and N ranges |
    | Any subluminal Alcubierre bubble from free fields | violates | tail QI failure at any σ (7); sub-Planck wall for v ≲ 0.03 (6) | tanh profile; nearly inertial static observers |
    | Natário-class drive with any source [D-02] | negative energy required | E_Eul ≤ 0; NEC fails (3) | unit lapse, flat slices, decaying shift |
    | Van Den Broeck geometry with free fields [D-09] | strained; violates for tanh-type B | B-edge QI failure; E_B ≳ 1e60–1e63 kg (11) | B profiles with ρ ≥ 0 at the edge untested |
    | Positive-energy superluminal soliton [D-06] | violates | Olum WEC theorem, [D-02], Celmaster–Rubin (4) | theorem assumptions not verified here |
    | Positive-energy subluminal shells [D-06] | consistent (but v < c) | none violated (4) | outside the Natário class |
    | Non-minimal classical scalar (speculative) | strained | φ ≈ (v/2)φ_c ~ 1e18 GeV; G_eff pole at v ≥ 2 (10) | scaling estimate |
    | Bubble controlled from inside, v > 1 [D-07] | violates | unreachable half-space ahead of ξ = r_h (12) | stationary bubble |
    | Sustained v > 1 bubble [D-08] | strained | front-horizon RSET growth, scale 1/(cκ) (14) | test-field result |

16. **Validity domains.**

    | Model | Domain | Is the question's regime inside? |
    |---|---|---|
    | Classical GR with prescribed T_ab | r_c ≫ L_P | Macroscopic walls: yes. QI-limited walls: marginal (r_c ≈ 13–60 L_P at α = 0.1). Slow bubbles: no (wall < L_P) (6) |
    | Semiclassical gravity, G = 8π⟨T⟩ | stress fluctuations ≪ mean | No, for every negative-energy source (Kuo–Ford, 14) |
    | Flat-space QI [D-04], as used in [D-05] | free fields, no boundaries, τ0 ≪ r_c | Wall application: yes by construction (α ≤ 0.1). Casimir and classical non-minimal scalars: outside (8, 10) |
    | Ideal Casimir formula [D-03] | perfect conductors, T = 0, a ≫ atomic spacing | a = 1 nm is at the edge; the formula is an upper bound on \|ρ\| |
    | Finazzi et al. [D-08] | test field on a fixed background | Valid only until the RSET rivals the source, which its own result undermines. The direction of the effect is robust; its rate is not |
    | Horizon temperature | stationary bubble frame | Constant v only; not during acceleration |
    | Thin-wall energy formula | σR ≫ 1 | Verified at σR = 8, 50 and 200 (5) |

## Calculations
All files are in runs/smoke-constraints/calc/ and run from the project root.
- `lens-constraints_alcubierre_ec.py` (~40 s): checks ρ against [D-01]; all-observer NEC/WEC/SEC/DEC and Hawking–Ellis types at 6 points × 4 speeds; slice energy at n and 1.5n with 1D and asymptotic cross-checks; SI table. Result: E(R = 100 m, Δ = 1 m, v = 1) = −6.7e46 J = −7.5e29 kg (SI), with peak |ρ| = 1.2e42 J/m³.
- `lens-constraints_qi_wall.py` (~25 s): Riemann tensor and frame curvature radius; Lorentzian worldline averages; QI → maximum wall thickness and E; §6 static observers in the tail. Result: maximum thickness 51 L_P = 8.3e-34 m at v = 1 (α = 0.1, N = 1); E = −9.0e62 kg (SI) for R = 100 m; subluminal tail violation.
- `lens-constraints_horizon_ctc.py` (~2 s): horizon radius, κ, unreachable-region share, temperatures, antitelephone. Results: κ = 2σ(1 − 1/v); share 3.0e-6 (v = 2, R = 100 m, Δ = 1 m); w_crit = 0.80c at u = 2.
- `lens-constraints_natario_class.py` (~3 min): Hamiltonian-constraint identity for three shifts; negative part; NEC search. Results: E_Eul = −(1/32π)∫|∇×β|², verified to 7 digits; the irrotational bubble has total 0 and negative part −1.82 m; NEC fails at 587/660 points.
- `lens-constraints_sources.py` (<1 s): Casimir stresses and plate penalty; free-field QI budget; gaps; non-minimal scalar scaling. Results: 7.7e9 plate penalty at a = 1 nm; 33.4-order density gap; φ_c = 5.97e18 GeV.
- `lens-constraints_vdb.py` (~3 min): VdB toy ρ, scans and slice energy (n = 128 and 192); 1D B-region split; B-region QI scaling; float64 precision check. Results: E_total = +0.4312 m with negative part −1.658 m (toy); B-edge QI failure; E_B ≳ 1.4e60–1.4e63 kg (SI) for a 100 m pocket.

## Candidate answers (at least 3)
- [CONSTRAINTS-A] (null) No admissible negative-energy source can support a controllable superluminal Alcubierre, Natário or Van Den Broeck bubble at ship scale. Free-field sources are QI-capped to walls of about 10²–10⁵ L_P, costing |E| ≈ 1e60–1e66 kg (SI) for R = 100 m. Casimir cavities carry net positive energy (≥ 7.7e9 times the Casimir deficit). Every v > c bubble has an unreachable leading region, allows CTC-capable networks and has a front-horizon instability. | why: findings 5–9 and 11–14 | prediction (calculable): repeating the QI audit with any other smooth wall profile or field content gives a maximum wall thickness within about one order of 50–110 L_P at v = 1–10, and |E(R = 100 m)| ≥ 1e59 kg. Prediction (observable): no free-field state will show a Lorentzian-averaged energy density below −3ħ/(32π²c³τ⁴) per field, e.g. −0.04 J/m³ at τ = 1 fs | confidence: high
- [CONSTRAINTS-B] (reframe of hidden premise 1) Negative energy is unavoidable for every Natário-class drive at any speed (E_Eul = −(1/32π)∫|∇×β|² ≤ 0, with the NEC failing) and for superluminal travel generally (Olum). For subluminal Alcubierre walls, free-field sources fail the QI at any thickness. The only energy-condition-consistent warp geometries on record are subluminal positive-energy shells with non-trivial lapse or spatial metric [D-06], and they do not deliver v > c. | why: findings 2–4 and 7 | prediction (calculable): an all-observer NEC/WEC/SEC/DEC and Hawking–Ellis audit (the method of lens-constraints_alcubierre_ec.py) of the published positive-energy shells passes for v < 1 and fails once v > 1; Lentz's soliton shows ρ_Eul < 0 somewhere | confidence: medium-high
- [CONSTRAINTS-C] (option, strained) The only construction not excluded outright here combines four elements: a route prepared in advance; a microscopic outer bubble (VdB type) with QI-limited Planck-thin walls fed by free-field negative energy; a B profile engineered so its outer edge keeps ρ ≥ 0; and acceptance of Planck-proximate curvature. It costs −9e28 kg (v = 1) to −4e30 kg (v = 10) for R_out = 1e-15 m, plus a B region that costs ≳ 1e60 kg if tanh-shaped. Its walls have r_c ~ 10–100 L_P, and for v > 1 its horizons sit at T ~ 1e29 K with instability times ~1e-42 s. | why: findings 6, 11, 12 and 14 | prediction (calculable): find a B(r) whose negative-ρ region satisfies the QI (proper scale ≤ ~10² L_P, no first-order negative edge) and compute E_B. If E_B ≲ 1e31 kg for a 100 m pocket the option survives; otherwise it collapses into A. A semiclassical backreaction run at the front horizon should show growth on a ~1/(cκ) time scale | confidence: low
- [CONSTRAINTS-D] (option, labelled speculative, strained) Classical non-minimally coupled scalar fields evade the free-field QIs. A v ≈ 1 wall needs φ ≈ 0.5φ_c ≈ 3e18 GeV (ξ = 1/6), and at v ≥ 2 the field reaches φ_c, where G_eff diverges and changes sign. | why: finding 10 | prediction (calculable): solving Einstein + ξRφ² for a thick-wall bubble should require 8πGξφ² ≈ v²/4 in the wall; a solution with 8πGξφ² ≪ 1 at v ≥ 1 would upgrade this option | confidence: low

## What would change my mind
- A free-field or interacting quantum state shown to sustain negative energy density beyond the flat-space QI in a boundary-free region would reopen macroscopic walls and weaken A and finding 7.
- A DEC-satisfying, asymptotically flat solution with v > 1 that passes an all-observer audit would overturn the superluminal half of B, which would also require Olum's assumptions to fail.
- A B(r) profile with QI-compliant negative-energy regions and E_B ≲ 1e31 kg for a 100 m pocket would strengthen C.
- A backreaction calculation in which the front-horizon growth saturates would also strengthen C.
- A static-observer audit of a compactly supported wall profile in which ρ_c stays non-negative in the tail would weaken finding 7.
- Curved-space QIs much weaker than the flat form at τ0 ~ 0.1 r_c would raise the maximum wall thickness. Even a 1e6 relaxation still leaves |E| ≳ 1e54 kg (SI) for R = 100 m, so A would hold.

## Assumptions I relied on
- **Geometry and scale.** Alcubierre's tanh profile throughout; R = 100 m as the ship-scale bubble; wall thickness Δ := 2/σ. The equatorial curvature radius is computed, not assumed.
- **QI application.** τ0 = α r_c with α ∈ [0.01, 0.5]; N ∈ [1, 100] scalar-equivalent fields; only one Eulerian worldline per v.
- **Finding 7.** The static-observer result was computed for the tanh profile only. That it extends to compactly supported profiles is argued, not computed.
- **Casimir.** Ideal plates; tracelessness for the lateral stress; plate areal mass ≥ m_p/(0.3 nm)².
- **Chronology.** The antitelephone assumes bubbles can be launched at speed u from any inertial frame (asymptotic Lorentz invariance).
- **Horizon physics.** The horizon temperature uses the stationary 1+1 formula. The instability time 1/(cκ) is my dimensional estimate, not a number from [D-08].
- **Non-minimal scalar.** The numbers are order-of-magnitude matching, not a solution.
- **VdB.** Tanh-type B profiles, with B_max ≤ 1e4 in the numerics (float64 limit). The physical-scale inputs (R_out = 1e-15 m, B_max = 1e17, 100 m pocket) are my illustrative choices, not values from [D-09].
- **Constants.** CODATA 2018 (in gr_tensors), m_p from CODATA 2018, M_sun from the IAU 2015 nominal GM_sun, and exact SI k_B and eV.
- **Sources.** Every [new] quote is WebSearch summary text. The tool returns synthesized summaries rather than raw snippets, and WebFetch to journals and preprint servers is blocked here, so no quote was checked verbatim against its source. The dossier is a hand-written fixture.
