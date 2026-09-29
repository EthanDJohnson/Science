# Candidate answers
Exclusivity: NOT mutually exclusive. C2–C5 are engineering options that can coexist or combine. C1 (null) excludes any of C2–C5 being viable in principle under established physics at the reference scale. C6–C8 are reframes, compatible with C1 and with one another.

Conventions: SI unless a value is marked "(geometric)", which means G = c = 1 with lengths in m (1 m of mass = 1.3466e27 kg). Masses are in kg, with M_sun = 1.989e30 kg and M_J = 1.898e27 kg; v is in units of c. Reference case: flat ship region R = 100 m, v = 10c, wall Δ in the Pfenning–Ford (PF) convention, either Δ = 1 m or at the free-field QI limit (Δ_QI = 97.7 v L_P = 1.58e-32 m at 10c). This is a quick run: every [D-..] and [U-..] item is unchecked, and the lens calculations are in-run and unreviewed. "(ours)" and "(lens inference)" mark lens reasoning that is not in a source. ACCESS labels are carried from the lens citations.

## C1: No option supplies or avoids the negative energy for a superluminal Alcubierre-type drive within established physics (GR + semiclassical QFT) at the reference scale, and none is buildable by 2100 (TRL ≤ 1 for every key component).
type: null
from: EXAMINER-A, ENGINEER-A, CONSTRAINTS-A
argument:
- **Negative energy is required at every speed.**
  - Natário-class metrics violate the NEC at every v > 0 [D-03, D-52].
  - Olum's theorem requires the WEC to fail for superluminal travel, under his definition [D-50].
  - Santiago–Schuster–Visser: all physically reasonable Natário-class drives violate the WEC, SEC and DEC [D-51].
  - Lens scans, Alcubierre wall: the NEC fails at 108/108 points at 0.1c and 1c, and at 100/108 points at 10c. The stress is mostly Hawking–Ellis type IV, which no classical source produces, and Casimir stress is type I [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_alcubierre.py].
  - The irrotational and lapse variants fail the NEC at every sampled point [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_irrot_ec.py] [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_lapse.py].
- **The only demonstrated sources are free fields, and the proven quantum inequality (QI) binds them.**
  - Ford–Roman [D-54] forces Δ ≤ 97.7 v L_P (α = 0.1), which is 1.58e-32 m at 10c.
  - That wall needs E = −4.7e63 kg (2.4e33 M_sun), about 5e10 times the mass inside the Hubble radius (9.2e52 kg, ours) [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_alcubierre.py] [D-18].
  - For any design, meeting the free-field QI forces curvature radii ≤ 98 L_P (Alcubierre) or 24–42 L_P (Natário) (constraints finding 19, our derivation).
- **In practice.**
  - Every geometry at the reference case needs |E_−| between 1e29 and 1e63 kg.
  - That is 60.6–94.9 orders above the largest demonstrated Casimir energy (5.0e-15 J, ideal plates, Bressi geometry) and 25.6–59.8 orders above one year of world primary energy (5.92e20 J) [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_gaps.py].
  - Densities are 39–107 orders above demonstrated negative densities.
  - The best parameter changes (v → 1c, R → 1 m, thick wall) recover at most 5.5 orders.
- **The rest of the package fails even if supply were solved.**
  - Horizons at f = 1 − 1/v block creating or steering the bubble [D-58].
  - No known solution self-accelerates [D-62].
  - The renormalized stress-energy (RSET) grows by at least 1.5e13 e-folds per 0.437 yr cruise, for any wall up to 1 km thick. This takes the 2D growth rate κ over to 4D [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_horizons_tides_sources.py].
- **Status of the verdict.** The in-principle verdict rests on theorems for the need and on the free-field QI extrapolation for the supply, not on a single theorem, because QIs are proven only for free fields in flat space [D-54, U-09]. The brief excludes [speculative] routes (negative-mass matter, torsion, brane-world, modified gravity) from this verdict; see C2.
predictions:
- **If true:**
  - An observer-robust energy-condition test (Le 2026 matrix inequalities [D-69]) finds NEC violation somewhere in every published superluminal metric.
  - Any quantum energy inequality (QEI) derived for a realistic interacting source caps sustained negative density at Planck-adjacent wall scales.
  - No lab system shows net-negative energy in a volume that includes its own source.
- **If false:** either a proven QEI permits metre-scale walls at about 1e23–1e27 kg/m³, held for months, or an observer-robust positive-energy superluminal metric appears with 2GM/c² < R.
evidence for:
- Dossier: [D-03] [D-18] [D-50] [D-51] [D-52] [D-54] [D-55] [D-58] [D-61] [D-62].
- Calculations: [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_alcubierre.py] [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_gaps.py] [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_horizons_tides_sources.py] [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_qi_natario_floor.py].
- The ANEC is proven for general QFT in Minkowski space [new: Faulkner, Leigh, Parrikar & Wang 2016, arXiv 1605.08072, ACCESS: abstract, "prove the averaged null energy condition in Minkowski space-time"].
- The achronal-ANEC conjecture "is sufficient to rule out wormholes and closed timelike curves" [new: Graham & Olum 2007, arXiv 0705.3193, ACCESS: abstract]. That it also excludes self-consistent superluminal bubbles is lens inference, and the ANEC here is a conjecture.
evidence against:
- The QI is proven only for free fields, in 4D Minkowski, along inertial worldlines [D-54]. PF's ~1e62 kg is therefore a free-field estimate, not a theorem about all matter [U-09].
- Krasnikov 2003 (abstract only) argues the QI "does not (always) imply large energy densities" [U-09].
- Lentz argues the QI wall limit does not apply to a plasma source [U-06].
- The Lentz dispute is unresolved, and its strongest specific rebuttal is a preprint [D-40].
- At the QI limit the sampling time is τ₀ ≈ 2–10 L_P, so transferring the QI to the wall is itself at the edge of validity (constraints finding 19).
- The semiclassical instability results come from 2D models only [D-61].
- All dossier items are unchecked.
decisive test: Apply the Le 2026 observer-robust NEC/WEC test [D-69] to the full Lentz and Fell–Heisenberg metrics via gr_tensors `Spacetime.from_adm`, including Lentz's kink planes. A clean pass by a superluminal metric with 2GM/c² < R breaks the null. For the supply half, a QEI for Einstein–Maxwell plasma or dielectric electromagnetism, evaluated at metre-scale sampling times, decides.

## C2: A thick-walled, energy-optimal (optionally Bobrick–Martire-flattened) Alcubierre bubble on a pre-laid track, needing at least 1.12e30 kg (0.56 M_sun) of Eulerian negative energy at R = 100 m and v = 10c, is viable in principle only if its wall can be sourced by matter that the free-field quantum inequality does not govern.
type: option
from: CONSTRAINTS-B, ENGINEER-B (thick-wall and Bobrick–Martire parts), ENGINEER-G, CONSTRAINTS-I (the [speculative] source routes are folded in as branch b)
argument:
- **The floor.**
  - Take f falling from 1 at r = R to 0 at r = R + D. Cauchy–Schwarz gives ∫f′²r²dr ≥ R(R + D)/D, with equality for f′ ∝ 1/r², so E_min = −(v²/12)R(R + D)/D (geometric).
  - The constraints lens verified this to 5 digits [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_qi_natario_floor.py] and the engineer lens to 6 digits [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_natario_vs_alcubierre.py]. This confirms [D-19].
  - Values at 10c:

    | Wall thickness D | E_min |
    |---|---|
    | 1 m | 57 M_sun |
    | 10 m | 6.2 M_sun |
    | 100 m | 1.13 M_sun |
    | D → ∞ | −v²R/12 = 1.12e30 kg (0.56 M_sun) |

  - The floor scales as v²R.
  - White's thick wall ("Warp Field Mechanics 101") belongs to this family [U-01]. Bobrick–Martire's optimal profile f = min(r₀/r, 1) is its D → ∞ member [U-04].
- **Flattening.** Flattening along the direction of travel by α_X = 1 + v² = 101 [U-04] gives:
  - 2.5e29 kg (0.12 M_sun), starting from the optimal profile at Δ = 1 m (engineer, ours);
  - 7.4e29 kg (0.37 M_sun), starting from the tanh Δ = 1 m case (constraints, ours).
  - Either way, the along-track wall is pushed toward the Planck scale. Per Bobrick–Martire it then meets the QIs but not the ANEC [U-04].
- **Source.**
  - (a) Established-physics branch: an interacting QFT or an Einstein–Maxwell plasma. No QI theorem exists for these [U-09, U-06].
  - (b) [speculative] branch: classical negative-mass or exotic matter, Einstein–Cartan torsion [U-11], or brane-world coupling.
  - White's oscillating variant ("Warp Field Mechanics 102") claims ~1e3 kg for a 10 m, 10c bubble [U-02]. That is 25 orders below the GR floor for R = 5 m, 5.6e28 kg (constraints, ours), so any saving below the floor is wholly non-GR.
- **Placement.** At v > c the source must be laid down in advance (see C6).
predictions:
- **If true:**
  - A QEI for the actual source field permits a Lorentzian-sampled |ρ| ≈ 1.3e23 kg/m³ (peak density at D = 100 m, 10c) over sampling times of order D/(v c).
  - No observer-robust NEC failure appears that the source cannot supply.
- **If false:** every QEI for realistic fields caps the wall near 1e2 v L_P. The thick wall then exceeds the bound by (D/Δ_QI)² ≥ 4e67 at D = 100 m.
evidence for:
- Dossier: [D-19] [U-01] [U-04] [U-06] [U-09].
- Calculations: [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_qi_natario_floor.py] [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_natario_vs_alcubierre.py].
evidence against:
- **Quantum inequality.**
  - The free-field QI is exceeded by at least 4e67 at D = 100 m (constraints candidate table).
  - The ratio of demand to allowed density is (Δ/Δ_max)² = 10^63.6 at Δ = 1 m and 10c [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-examiner_premises.py].
  - Pfenning–Ford: "the wall thickness cannot be much above the Planck scale" [new: Pfenning & Ford 1997, arXiv gr-qc/9702026, ACCESS: full-text].
  - Examiner finding 1: thick-wall budgets describe classical exotic matter, so QI-bound supply and thick walls are mutually exclusive.
- **Scale.** The total energy is 10^61.3 above the Bressi Casimir energy, and at least 10^25.6 above a year of world energy [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_gaps.py].
- **Formation.** Forming the bubble requires radiating at least 1e47 J of positive energy to infinity (constraints K9, ours).
- **Stability.** The RSET grows by at least 1.5e13 e-folds per cruise even for D = 1 km (2D model) [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_horizons_tides_sources.py].
- **Flattening.** It moves stress into K_xx, which the Eulerian budget ignores, and it violates the ANEC [U-04].
- **Interacting fields.** The achronal-ANEC conjecture plausibly excludes this bubble even for interacting fields (lens inference, conjecture) [new: Graham & Olum 2007, arXiv 0705.3193, ACCESS: abstract].
- **Control.** Horizons, and no self-acceleration [D-58, D-62].
decisive test: Derive or locate a QEI for the proposed interacting source, for example Einstein–Maxwell plasma [U-06] or dielectric electromagnetism. Evaluate it at sampling time τ₀ = α r_c, with r_c ≈ D/v, for D = 100 m and v = 10c. If it permits a sustained |ρ| ≥ 1.3e23 kg/m³, C2 stays alive in principle; a bound near the free-field value eliminates it.

## C3: A Van Den Broeck pocket (expansion factor α = 1e17 inside a femtometre-scale outer bubble) cuts the negative energy for a 100 m ship region to a few solar masses (≈ 5.7e30 kg, 2.9 M_sun, at 10c) while satisfying the free-field quantum inequality.
type: option
from: EXAMINER-D, ENGINEER-B (Van Den Broeck part), CONSTRAINTS-E
argument:
- The geometry and its claimed savings are in [D-05].
- Region II, reproduced with Van Den Broeck's own n = 80 profile: E_II,− = −1.38e30 kg and E_II,+ = +4.87e30 kg [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_vdb.py].
- E_II does not depend on v, because region II is ultrastatic in comoving coordinates (K_ij = 0).
- The QI-limited outer wall (tanh) gives E_IV = −4.3e30 kg at 10c. The total negative energy is therefore about −5.7e30 kg.
- The published QI check is "amply satisfied" [D-24]. The reduction factor against PF is about 1e32 [D-23].
predictions:
- **If true:**
  - The largest orthonormal-frame Riemann component in region II is about 1e68 m⁻² (geometric), i.e. a curvature radius of ~10 L_P, as Van Den Broeck states.
  - The QI holds for all observers, not only Eulerian ones.
  - Region II's energy stays independent of v at 10c.
- **If false:**
  - The largest orthonormal curvature is about 1.88e33 m⁻² (geometric), giving an invariant curvature radius r_c = 2.3e-17 m ≈ 1.4e18 L_P.
  - The Ford–Roman bound is then −1.2e26 kg/m³ against a required peak |ρ| of 2.4e59 kg/m³, so the QI is violated by about 2e33.
  - Or region II acquires the B(0)²v² factor that Bobrick–Martire say is missing [U-05].
evidence for:
- Dossier: [D-05] [D-20] [D-21] [D-22] [D-23] [D-24].
- The energies are reproduced in [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_vdb.py].
evidence against:
- **Curvature and the QI.**
  - Invariant curvature radius: r_c = 2.3e-17 m. The toolkit's `curvature_at` agrees, and `precision_check` gives a relative error of 2e-14 [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_vdb_curvature.py].
  - A coordinate (Cartesian, all-lower) component gives 7.8 L_P, which reproduces Van Den Broeck's "about ten Planck lengths". Van Den Broeck: "The minimum curvature radius is determined by the largest component of the Riemann tensor" [new: Van Den Broeck 1999, arXiv gr-qc/9905084, ACCESS: full-text].
  - That he used the coordinate component is lens inference.
  - The radial NEC is violated at the neck: 3R_r̂r̂ = −3.8e33 m⁻² (geometric).
- **Unresolved density discrepancy.** [D-24] gives a peak of 6.6e93 kg/m³, while the lens's orthonormal peak is 2.4e59 kg/m³.
- **Disputed energy.** Bobrick–Martire's equivalence dispute, and Van Den Broeck's own follow-up calling superluminal bubbles "unlikey" [U-05].
- **Limited checks.** The QI was checked for Eulerian observers only [D-24].
- **Scale.** The outer wall is still about 98 v L_P thick (constraints), and the 3e-15 m neck is nuclear-sized (engineer).
- **Gaps.** The peak density is 10^107.3 above ideal 20 nm Casimir, and the total energy is 10^61.4–10^63.4 above the Bressi Casimir energy [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_gaps.py].
- **Placement.** The causal-placement problem applies unchanged to the outer wall (examiner P8).
decisive test: Compute region II's largest orthonormal-frame Riemann component with gr_tensors `curvature_at` (n = 80, α = 1e17, R̃ = Δ̃ = 1e-15 m).
- About 1.9e33 m⁻² (geometric) eliminates the QI pass.
- About 1e68 m⁻² restores the pass, but puts the curvature at ~10 L_P, outside semiclassical validity.
- A secondary test: recompute E_II at v = 10c including Bobrick–Martire's B(0)²v² term.

## C4: Positive-energy superluminal solitons — Lentz's Einstein–Maxwell plasma soliton and Fell–Heisenberg's Eulerian-positive subclass — remove the need for negative energy altogether.
type: option
from: EXAMINER-E, ENGINEER-D, CONSTRAINTS-F
argument:
- **Lentz.**
  - He claims Eulerian ρ ≥ 0, sourced by a plasma.
  - His budget is E_tot ~ C v²R²/w, which gives (few) × 0.1 M_sun at R = 100 m and w = 1 m (printed with a factor v_s), and so tens of M_sun of positive energy at 10c [U-06] (the 10c conversion is ours).
  - His reply to critics: the divergence-theorem argument "does not hold" because his Eulerian density is non-smooth at x = 0 and y = 0 [D-40].
- **Fell–Heisenberg.**
  - Eulerian ρ ≥ 0, with an example total E ≈ 1.0e27 kg and a central shift of 1.26c [D-26, D-41].
  - Their exterior is Schwarzschild-like [U-07].
predictions:
- **If true:** the Le matrix-inequality test passes the NEC and WEC at every point, including the distributional surface stresses on Lentz's kink planes, and 2GM/c² < R.
- **If false:** one of the following appears:
  - a null direction with T_μν k^μ k^ν < 0, as at all 6 Eulerian-positive points of the lens's irrotational drive;
  - negative surface tension on the kink planes;
  - a positive mass lying inside its own Schwarzschild radius.
evidence for: [D-26] [D-40] (Lentz's reply) [D-41] [U-06] [U-07].
evidence against:
- **Theorems.** Olum [D-50] and Santiago–Schuster–Visser [D-51]; Eulerian positivity is not the WEC [D-06].
- **Curl identity (ours).**
  - A smooth, compactly supported, zero-vorticity, flat-slice shift has E_tot = 0 exactly, so Eulerian ρ ≥ 0 forces ρ ≡ 0 [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_natario_energy.py].
  - Lentz's escape needs kinks in ∇β, which carry δ-function stresses (lens inference).
- **Explicit counterexample.** The irrotational drive fails the NEC, WEC, SEC and DEC at 11/11 points, including all 6 points where Eulerian ρ is positive [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_irrot_ec.py].
- **Lentz critique.** Celmaster–Rubin 2025 (preprint) find negative Eulerian regions in Lentz's drive, and WEC violation even in a corrected version [D-40].
- **Fell–Heisenberg.**
  - Their positive total is the boundary flux (an ADM-type mass) of a non-Minkowski exterior (constraints finding 4c, ours).
  - The authors say the SEC is violated [D-26].
  - A central shift of 1.26c implies a surface with |β| = 1, i.e. a horizon (constraints table).
- **Self-gravity.**
  - +7.5e31 kg of positive energy at R = 100 m has a Schwarzschild radius of 1.1e5 m, which is 1.1e3 R.
  - The shell density, 5.4e43 J/m³, is 10^7.4 above LHC quark–gluon plasma, and must be sustained [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_gaps.py]. This assumes C ≈ 1/18.
  - Quark–gluon plasma density ~14 GeV/fm³ [new: arXiv:1304.1452 and Braun-Munzinger & Stachel review via WebSearch, ACCESS: search-summary].
- **Placement.** The source lies beyond the ship's horizon (examiner finding 2).
decisive test: Compute the distributional stress-energy on Lentz's kink planes (x = 0, y = 0), then run the Le 2026 NEC/WEC matrix-inequality test [D-69] over the full Lentz and Fell–Heisenberg metrics. Any NEC-violating null direction eliminates the "no negative energy" claim.

## C5: Demonstrated laboratory negative-energy phenomena — Casimir cavities, squeezed vacuum, or condensed-matter "negative effective mass" — can be scaled, concentrated and separated from their positive-energy sources into the supply for a warp wall.
type: option
from: ENGINEER-E, CONSTRAINTS-H (examiner findings 4 and 8 and premises P4 and P7 supply its main tests)
argument:
- **Casimir.** The negative energy is real and, in principle, gravitationally relevant [D-08]. Forces have been measured [D-09]:
  - Bressi et al., 1.2 × 1.2 mm² plates at 0.5–3.0 µm [new: Bressi et al. 2002, PRL 88 041804, arXiv:quant-ph/0203002, ACCESS: full-text, "form a capacitor with an area of 1.2 × 1.2 mm 2."];
  - Ederth, gaps of 20–100 nm [new: Ederth 2000, Phys. Rev. A 62 062104, ACCESS: title only (lit_search/Crossref)].
- **Squeezed vacuum.**
  - Sub-vacuum noise has been observed in subcycle intervals [new: Riek et al. 2017, Nature 541, 376, ACCESS: abstract, "Subcycle intervals with noise level significantly below the pure quantum vacuum are found."].
  - Squeezing reaches 15 dB [D-38]. Maclay–Davis report a tension between measured data and a proposed squeezed-light QI [D-46].
- **Demonstrated anchors** (ideal-plate formulas): 5.0e-15 J for the Bressi plates at 0.5 µm, and 2.7e3 J/m³ at a 20 nm gap [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_gaps.py].
predictions:
- **If true:**
  - A macroscopic volume that includes the plates (or other source) shows net negative energy.
  - Measured squeezed-light negative density exceeds the electromagnetic Ford–Roman bound for its sampling time.
  - An Archimedes-type weighing shows vacuum energy gravitates as predicted.
- **If false:**
  - Every cell that includes its plates is net positive, by roughly 1e10 or more.
  - Squeezed-light negative density stays within the electromagnetic QI (≤ 0.074 J/m³ at τ₀ = 1 fs).
  - "Negative effective mass" media have T_00 > 0.
evidence for: [D-08] [D-09] [D-38] [D-46]; Riek et al. 2017 (abstract).
evidence against:
- **Gap size.** An ideal Casimir gap reaches the 1.2e44 J/m³ wall peak (Δ = 1 m, 10c) only at a = 1.4e-18 m. At the QI wall it would need a = 1.7e-34 m [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_horizons_tides_sources.py].
- **The plates outweigh the deficit.** Stacks are therefore net positive, at +5e19 to +9e20 J/m³ (engineer).

  | Lens | Plate mass ÷ energy deficit | Conditions | Source |
  |---|---|---|---|
  | constraints | 8.5e9 to 3e11 | 0.3 nm to 1 nm gap, graphene-like plates | constraints finding 11 |
  | examiner | 3.2e11 to 4.0e14 | assumed plate masses | [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-examiner_premises.py] |
  | engineer | 10^11.1 to 10^23.3 | per cell | [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_gaps.py] |

- **Wrong stress type.** Casimir stress is type I, diag(−1, 1, 1, −3) [D-08]. The wall needs mostly type IV [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_alcubierre.py].
- **Quantum inequality.**
  - The electromagnetic Ford–Roman bound allows −1.2e44 J/m³ only for τ₀ ≤ 5e-27 s. At τ₀ = 1 fs it allows at most 0.074 J/m³, 45 orders short.
  - The cruise needs 1.4e7 s, which is 22.2 orders longer than femtosecond windows.
  - Quantum interest [D-56].
- **Total energy.** The gap is at least 10^60.6 above the Bressi Casimir energy, for every geometry [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_gaps.py].
- **Gravitation untested.** Nobody has yet weighed engineered vacuum energy [new: Avino et al. 2020, MDPI Physics 2, 1, ACCESS: abstract] [new: Calloni et al. 2024, EPJ Plus, ACCESS: search-summary].
- **Negative effective mass.** In a spin-orbit-coupled BEC this is the inverse curvature of the dispersion; the atoms have positive rest mass, so T_00 > 0. This is examiner reading, not the paper [new: Khamehchi et al. 2017, PRL 118, 155301, ACCESS: search-summary (title/venue only)].
decisive test:
- **Cheapest calculation:** the per-cell energy balance (plate rest energy plus ideal Casimir deficit) for the thinnest physical plate (one atom, ~0.3 nm). Any net-negative cell reopens the Casimir branch; the lenses predict at least 8.5e9 times net positive.
- **Cheapest measurement:** an absolute calibration (J/m³ and duration) of Riek-type sub-vacuum intervals, compared with the electromagnetic Ford–Roman bound.

## C6: The binding obstacle is causal, not quantitative: at v = 10c, 90–97% of the Eulerian negative energy must sit where no bubble-comoving timelike source can exist and the ship cannot create, steer or stop the bubble, so the only coherent "option" is route infrastructure pre-laid by earlier subluminal agents, which shortens only Earth-timed round trips.
type: reframe
from: EXAMINER-B (also the constraints ledger rows K10 and K14 and its Krasnikov-tube row, which carry no candidate ID)
argument:
- **Where a comoving source can sit.**
  - A worldline x = x₀ + vt is timelike only where f > 1 − 1/v, and that surface is also the ship's forward horizon.
  - For Δ = 1 m at 10c the horizons sit 0.55 m inside the wall centre [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_horizons_tides_sources.py].
- **Share of the negative energy out of reach** (at f < 1 − 1/v) [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-examiner_premises.py]:

  | Speed | Share of Eulerian negative energy |
  |---|---|
  | v ≤ 1c | 0 |
  | 2c | 50%, for every profile |
  | 10c | 97% (tanh), 90% (linear ramp), 90% (Bobrick–Martire optimal) |

- **Control.** Everett–Roman: the ship can neither create nor control the bubble [D-58]. No known solution self-accelerates [D-62].
- **Krasnikov.** "under some reasonable assumptions in globally hyperbolic spacetimes the traveller cannot hasten reaching the destination" [new: Krasnikov 1998, Phys. Rev. D 57, 4760, ACCESS: abstract].
- **Krasnikov tube** [D-59]:
  - it shortens only round trips timed on Earth;
  - it still needs "unphysically thin layers" of negative energy;
  - two tubes make a time machine.
- **Chronology.** Any frame boosted by β > 1/v (0.10c at 10c) sees the trip run backward in time, so bubbles launched on demand in two frames close a causal loop (constraints finding 12) [D-60].
predictions:
- **If true:**
  - The comoving-source fraction is 0 for v ≤ 1, and rises to 50% at 2c, ≥ 90% at 10c and ≥ 99% at 100c, for every profile. That includes Natário and lapse-modified drives, where the threshold may move but not vanish.
  - No self-consistent superluminal solution specifies source worldlines inside the ship's causal past.
- **If false:** either a solution whose source in the f < 1 − 1/v region is supplied by worldlines from the causal past of departure, or a self-accelerating superluminal solution.
evidence for:
- Dossier: [D-58] [D-59] [D-60] [D-62].
- Calculations: [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-examiner_premises.py] [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_horizons_tides_sources.py].
evidence against:
- **Coverage.** The fractions were computed for Alcubierre-family profiles only. Natário's f″ weighting could shift them by O(10%), and lapse-modified drives (Loup, Lentz) were not computed (examiner assumptions).
- **Gauge.** Whether a trip counts as superluminal is gauge- or paradigm-dependent [D-43].
- **Supply problem remains.** A pre-laid route still needs QI-thin walls [D-59].
- **Finite duration.** Finazzi et al. note that a finite-duration superluminal phase may avoid the Cauchy-horizon divergence [D-45].
decisive test: Recompute the comoving-source fraction at v = 10c for Natário's zero-expansion shift and for a Loup-lapse metric, via `Spacetime.from_adm`. A fraction near 0 for any superluminal design refutes the reframe; ≥ 50% at 2c and ≥ 90% at 10c for all designs confirms it.

## C7: Total Eulerian negative energy is the wrong figure of merit: published "reductions" (Natário zero expansion, Loup lapse, irrotational shifts, Bobrick–Martire flattening) relocate or relabel the exotic stress without removing it (Natário's is ~8e3 times worse at the reference case), so the binding quantities are local — worst-null-direction NEC stress and QI-sampled wall density — under which QI-bound supply and thick-wall shrinking are mutually exclusive.
type: reframe
from: EXAMINER-C, CONSTRAINTS-C, ENGINEER-C, CONSTRAINTS-G
argument:
- **The total is not invariant.**
  - For unit-lapse, flat-slice drives the ADM mass is 0, while ∫ρ_Eul < 0 (examiner finding 5; own inference, unsourced).
  - Slice identity: E_Eul = −(1/32π)∫|∇×X|² d³x + boundary flux (constraints, ours) [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_natario_energy.py].
- **Irrotational shift** X = v∇((x − vt)f):
  - E_tot = 0.0000 m (geometric), with E_± = ±2.858 m, yet the NEC, WEC, SEC and DEC fail at 11/11 points [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_irrot_ec.py].
  - This matches Rodal 2026's net ≈ 0 (0.04%) [U-10] and his "reduces but does not eliminate" [D-64].
- **Loup lapse.**
  - E_Eul ∝ A₀⁻²: −0.22334, −0.02516 and −0.00228 m (geometric) at A₀ = 1, 3 and 10.
  - Yet the lapse hill alone fails every energy condition at 17/17 points. Its worst NEC value, −0.314 m⁻² (geometric), exceeds the wall's own peak |ρ| of 0.159 m⁻² [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_lapse.py].
- **Flattening.** Alcubierre's ρ_Eul contains only transverse gradients [D-02], so flattening moves stress into K_xx, which the Eulerian budget ignores (constraints, ours). It also violates the ANEC [U-04].
- **Natário, thin wall.**
  - Two lenses independently find |E_Nat| ≈ v²R⁴/(22.5Δ³) (constraints) and ≈ 0.0056 v²R⁴σ³ (engineer).
  - The ratio to Alcubierre is ≈ 0.8(R/Δ)², i.e. ≈ (σR)²/5: 14.7× at R = 1 m and σ = 8 m⁻¹.
  - At R = 100 m, Δ = 1 m and 10c this gives 6.0e35 kg (3.0e5 M_sun), 8.0e3 times the Alcubierre value [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_natario_vs_alcubierre.py] [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_horizons_tides_sources.py].
  - The mechanism: a compact divergence-free shift must return the interior flux through the wall, so the wall carries a backflow ≈ vR/(2Δ), which is 500c here.
  - Lobo–Visser's "same scaling" rests on assuming that "gradients of β in the bubble walls are of order vσ" [new: Lobo & Visser 2004, arXiv gr-qc/0406083, ACCESS: full-text].
- **Natário at the QI limit.** E_Nat ≈ −(2–10)e81 kg at 10c (estimate) [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-constraints_natario_qi_est.py].
- **Supply and shrink are mutually exclusive.**
  - Under the free-field QI the demand/allowed ratio is (Δ/Δ_max)² = 10^63.6 at Δ = 1 m and 10c [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-examiner_premises.py].
  - So the 38 M_sun (Δ = 1 m) and 0.56 M_sun (thick-wall floor) figures apply only to [speculative] classical exotic matter.
  - The QFT-consistent Alcubierre figure is ~4.6e63 kg [D-18].
predictions:
- **If true:**
  - For each reduction, the worst-null-direction NEC integral ∫min_k T_μν k^μ k^ν d³x does not fall in proportion to E_Eul.
  - An independent `from_adm` reproduction gives E_Nat = −3.288, −23.64 and −183.8 m (geometric) at R = 1 m, σ = 8, 16 and 32 m⁻¹, and v = 1.
  - Any compact divergence-free drive shows a wall backflow ≈ vR/(2Δ).
- **If false:** one of the following holds:
  - Natário's thin-wall energy scales as v²R²σ, like Alcubierre [D-04];
  - the NEC integral falls with E_Eul in the lapse, flattened or irrotational variants;
  - a QEI for a real source permits metre-scale walls, which would restore totals as the budget.
evidence for:
- Dossier: [D-02] [D-06] [D-18] [D-51] [D-64] [U-04].
- [U-10]: Rodal 2024 finds Natário's curvature invariants 35 times Alcubierre's.
- The calculations cited above.
evidence against:
- [D-04]: Lobo–Visser give Natário the same v²R²σ scaling, and the dossier lists this as established.
- The brief sets the Eulerian energy as the default budget.
- The ADM-mass argument is unsourced lens inference.
- Loup's published 1/A⁴ was not reproduced; their measure may differ [U-03].
- The Natário figure at the QI limit is an estimate with cubic sensitivity to r_c, and the toolkit's thinner-wall points had not finished (constraints finding 18).
decisive test: Using gr_tensors `Spacetime.from_adm`, independently recompute two things.
- The Natário/Alcubierre Eulerian-energy ratio at R = 1 m and σ = 8, 16, 32 m⁻¹. The prediction is ≈ 14.7 at σ = 8, growing as (σR)²/5.
- The worst-null-direction NEC integral for the Loup-lapse (A₀ = 10) and irrotational variants, against plain Alcubierre.

A ratio near 1, or an NEC integral that falls with E_Eul, refutes the reframe.

## C8: The answerable nearby question drops "superluminal": subluminal positive-energy warp shells (Fuchs et al.: 4.49e27 kg, 2.4 M_J, at 0.04c) and sub-light relativistic rockets (a 1 g photon rocket reaches 4.37 ly in 3.58 yr ship time) need no negative energy, and the rocket's energy need is more than 20 orders of magnitude closer to demonstrated supply than the cheapest superluminal warp's.
type: reframe
from: EXAMINER-F, ENGINEER-F, CONSTRAINTS-D
argument:
- **Fuchs shell.** It meets all the energy conditions, with R₁ = 10 m, R₂ = 20 m, M = 4.49e27 kg and v = 0.04c [U-08].
- **Theory.** Bobrick–Martire's positive-energy solutions are always subluminal [D-07], and Olum's theorem applies only to superluminal travel [D-50].
- **Photon rocket at 1 g** to 4.37 ly (engineer finding 18, via `python3 .claude/skills/conundrum/scripts/rocket_tools.py trip --distance "4.37 ly" --accel "1 g0" --ve c`):
  - ship time 3.58 yr; Earth time 6.00 yr;
  - peak speed 0.952c; mass ratio 40.4;
  - 3.5e18 J per kg of payload.
- **Energy for a 1e5 kg ship:** 3.5e23 J, about 600 world-years (10^2.8), against at least 10^25.6 world-years for the cheapest warp [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_gaps.py].
- **Discrepancy to check.** The engineer's text says the rocket is "roughly 25 orders closer", but its own figures (10^25.6 against 10^2.8 world-years) give about 23 orders. The claim above uses the conservative "more than 20".
predictions:
- **If true** (as the better-posed target):
  - An energy-condition-satisfying shell can be given a solved acceleration phase using positive energy only, but cannot be boosted through v = c without violating the NEC (as Olum and Bobrick–Martire predict).
  - Rocket requirements stay within a few orders of world energy supply.
- **If false:** either no energy-condition-satisfying shell admits any positive-energy acceleration phase, in which case it is not a drive at all, or a positive-energy shell crosses v = c, which would also weaken C1.
evidence for: [D-07] [D-50] [U-08]; the rocket_tools calculation; [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_gaps.py].
evidence against:
- No acceleration phase has been solved for the Fuchs shell [U-08], and no known solution self-accelerates [D-62].
- The Fuchs shell has 2GM/(c²R₂) = 0.33 and a mean density of 1.4e40 J/m³, 10^3.8 above quark–gluon plasma, held static [calc: runs/2026-09-29-alcubierre-negative-energy/calc/lens-engineer_gaps.py].
- Neither route meets the brief's definition of superluminal effective speed.
- The engineer notes that a 100 t rocket is still beyond 2100 at that mass.
decisive test: Solve an acceleration phase for a Fuchs-type shell, checking the energy conditions for all observers with the Le 2026 matrix-inequality test [D-69]. Success makes it a subluminal drive; failure leaves the rocket as the only positive-energy route.
