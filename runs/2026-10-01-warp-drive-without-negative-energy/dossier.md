# Dossier: Can any warp drive move a payload without negative energy?
status: final

Inputs compiled: research/theory.md (RT-01..14), research/quantitative.md (RQ-01..20), research/critiques.md (RC-01..15), research/engineering.md (RE-01..22), research/frontier.md (RF-01..24), and the five matching `*.check.md` files. All five facets named in the brief are present and were source-checked. Unit systems: SI unless marked "geometric" (G = c = 1, lengths and energies in metres; E[J] = E_geo × c⁴/G, c⁴/G = 1.21e44 N). "Eulerian" means the density seen by normal observers on a t = const slice. It is **not** a WEC test for all observers. "(ours)" marks arithmetic by this run's researchers in `calc/`, not a published number.

## 1. Established
Peer-reviewed or textbook claims that the checker verified. Theorems are in §4.

- [D-01] Natário's framework writes every unit-lapse, flat-slice warp spacetime as ds² = −dt² + Σ(dxⁱ − Xⁱdt)² (geometric units; shift β = −X). Its quantities are K_ij = ½(∂_iX_j + ∂_jX_i), expansion θ = ∇·X, and Eulerian density ρ = (1/16π)(θ² − K_ijK^ij). Eulerian observers are geodesic. (refs: RT-01) peer-reviewed.
- [D-02] Natário's zero-expansion drive has θ ≡ 0. Its Eulerian density is ρ = −(1/16π)K_ijK^ij = −(v_s²/8π)[3(f′)²cos²θ + (f′ + r f″/2)² sin²θ] ≤ 0, which is negative wherever the wall curves the slice. The Alcubierre Eulerian density is ρ = −(1/32π)v_s²[f′(r_s)]²(y²+z²)/r_s² (Natário's restatement), equivalently E_Alc = −(1/32π)((∂_xN_z)² + (∂_yN_z)²) (Lentz's restatement). It is negative everywhere in the wall: "the renowned toroid of negative energy density". (refs: RT-02, RQ-13; corroborated by the preprint theorem RF-17) peer-reviewed. Natário himself claims only that the SEC need not fail in the expansion sense (RT-02).
- [D-03] Alcubierre and Natário zero-expansion drives have identically zero ADM mass. The zero-vorticity drive can, but need not, have nonzero ADM mass. (refs: RT-05) peer-reviewed.
- [D-04] The three 2020–21 "positive-energy" papers (Lentz; Bobrick–Martire; Fell–Heisenberg) checked only the comoving Eulerian observers. The WEC requires all timelike observers. Santiago, Schuster & Visser call these claims "at best incomplete". Warp Factory (Helmerich et al. 2024) says the same of Lentz and Fell: positive Eulerian density, but "it has been argued that these still both violate the weak energy condition, as shown generally by [14] and by Fell himself". (refs: RC-01, RC-02, RT-04, RT-12, RQ-18) peer-reviewed.
- [D-05] **Fell–Heisenberg 2021 concede an all-observer WEC failure.** Their metric is ds² = −dt² + Σ(dxⁱ + (∂_iφ + ω_i)dt)² (N = 1, flat slices, shift sign "+"). Their Eulerian density is ρ ≥ 0, but for the type-I stress tensor "ρ + p_i < 0 for some i ∈ {1,2,3} in compact regions". The example also violates the SEC. Their "superluminal" means a central shift magnitude of 1.26 (in units of c) exceeding the lapse, not a travel-time advance. They say horizons form while the configuration is pushed from subluminal to superluminal, which prevents transport of an inertial observer across the light barrier. (refs: RT-09, RQ-12) peer-reviewed.
- [D-06] **Lentz 2021 construction.**
  - Form: N = 1, with a shift N_i = ∂_iφ from a scalar potential obeying ∂_x²φ + ∂_y²φ − (2/v_h²)∂_z²φ = ρ, and rhomboid source lobes.
  - Energy conditions as claimed: the "WEC" claim rests on the Eulerian density. The DEC holds only while N_iN^i < 1, and horizons form between the soliton and the exterior at higher speed.
  - Source: the source check is on the trace equation and the momentum/energy conditions. No full solution of the coupled Maxwell-plasma-fluid system is exhibited.
  - Scope: Santiago et al. name this metric explicitly as inside the class their theorem covers (§4, D-41).
  (refs: RT-08, RC-01) peer-reviewed. Whether the positive Eulerian density holds is contested: §3, D-30.
- [D-07] **Bobrick–Martire 2021.**
  - Classes: they define Classes I–IV by whether the comoving-frame vector ξ is timelike, null or spacelike. Spherically symmetric positive-energy drives "all belong to Class I … always subluminal".
  - Mechanism and propulsion: any warp drive "is a shell of regular or exotic material moving inertially … Therefore, any warp drive requires propulsion".
  - Superluminal matter: Classes II/III need "superluminal matter", which for a perfect fluid violates the DEC.
  - Time inside: positive-energy spherical drives "must slow down the time compared to the comoving observer"; making interior time run faster requires negative energy.
  - Their own superluminal solutions carry negative energy. Their conclusions "do not support the recent claim in (Lentz 2020)".
  - Van Den Broeck's solution "is equivalent to the Alcubierre solution" by a coordinate transformation.
  (refs: RT-10, RQ-07, RQ-09) peer-reviewed.
- [D-08] **Fuchs et al. 2024 "warp shell", as published.**
  - Construction: a TOV-type static spherical matter shell (R₁ = 10 m, R₂ = 20 m, M = 4.49e27 kg = 2.365 M_J, positive ADM mass) plus a shift vector. The lapse is not unity and the slices are not flat.
  - Speed and energy conditions: constant velocity v_warp = 0.04 c (subluminal). It is reported to satisfy "all of the energy conditions", tested numerically with Warp Factory by sampling observers. This is not an exact type-I eigenvalue test.
  - Limits stated by the authors: mass is capped by R_shell > 2GM_shell/c², and the shift adds momentum flux, so its magnitude has an upper limit. Their three key ingredients are positive ADM mass, Eulerian energy density much larger than pressure and momentum flux, and subluminal speed.
  - Acceleration is not solved. Moving the centre while growing the shift "requires a negative energy density throughout space". The alternative named is mass shedding. Whether "spinning up" moves the structure "without the need for any energy ejection" is left open, with 4-momentum conservation as the likely constraint.
  - Passengers follow geodesics, so they feel no local acceleration (ignoring passenger mass).
  - Parameters were found "by trial and error", with moving-average smoothing.
  (refs: RT-11, RQ-01, RQ-03, RQ-05) peer-reviewed. Validity is contested: §3, D-31.
- [D-09] The gauge-invariant observable Fuchs et al. offer is a light round-trip time difference at v_warp = 0.04 c: warp shell δt = 7.6 ns against 0 ns for the same matter shell without shift. On that basis they argue the shift "cannot be reduced to a coordinate transformation" and call the effect a Lense-Thirring-like linear frame dragging. (refs: RT-11, RQ-04) peer-reviewed. The source's own sign-convention tension is §3, D-33.
- [D-10] Warp Factory (Helmerich et al. 2024) is a numerical finite-difference toolkit. It computes G_μν on a grid from the 3+1 metric, reports T_μν in the Eulerian tetrad, and tests the NEC, WEC, SEC and DEC by contracting with a sampled observer field. It concludes that the earlier proposals "have been unphysical, requiring energy condition violations and large energy requirements". (refs: RT-12, RQ-18) peer-reviewed. Sampling caveat: brief premise 8.
- [D-11] **Rodal 2026 (GRG 58, 1).** An irrotational unit-lapse flat-slice drive that is globally Hawking–Ellis Type I.
  - Peak proper-energy deficit: about 38× smaller than Alcubierre and about 2.6e3× smaller than Natário.
  - Peak NEC violation: more than 60× smaller than Natário.
  - Net slice-integrated proper energy: "consistent with zero" (0.04% residual after a far-field extrapolation, which is the author's own reading).
  - Negative energy and NEC violation are reduced, not removed. The figures and tables are for v = c only; superluminal behaviour is asserted to be "analogous" but not computed.
  (refs: RC-09, RF-04, RF-16) peer-reviewed.
- [D-12] Rodal 2024 (IJTP 63, 168) finds Natário's spacetime is Petrov type I, with curvature-invariant amplitudes 35× Alcubierre's at identical bubble parameters. (refs: RF-22) peer-reviewed (abstract checked).
- [D-13] Two control and semiclassical objections apply to superluminal bubbles only:
  - Everett & Roman 1997: an observer at the centre of an Alcubierre bubble is causally separated from the outer wall, so they can neither create nor control it (RC-12).
  - Finazzi, Liberati & Barceló 2009: the renormalized stress-energy tensor grows exponentially at the front wall of a superluminal bubble, and an observer at the centre sees a generically thermal Hawking flux (RC-13).
  (refs: RC-12, RC-13) peer-reviewed; the restriction to v > c is the researcher's reading.
- [D-14] Clough, Dietrich & Khan 2024 (Open J. Astrophys. 7) numerically evolve a warp-drive "containment failure" with a stiff-fluid equation of state and compute the gravitational-wave signal. They acknowledge "a requirement for negative energy". (refs: RC-14, RF-09) peer-reviewed.
- [D-15] Buchert & Frackowiak 2026 (Universe 12, 132) give dynamical equations for the Natário class with one-component coordinate velocity. They find "an expected generic instability of the warp field" in their second example, and claim no start/stop solution that satisfies the energy conditions. (refs: RF-12) peer-reviewed.
- [D-16] **Laboratory "negative energy" in hand: sub-vacuum noise, not gravitating negative mass.**
  - Squeezed light: 15 dB directly observed (Vahlbruch et al. 2016, PRL 117, 110801; cite the DOI as primary), and 6.03 ± 0.02 dB in GEO 600.
  - Dynamical Casimir effect: observed in a SQUID-modulated transmission line at about 11 GHz, with the electrical length changed at "a few percent of the speed of light".
  - Quantum energy teleportation: demonstrated on IBM superconducting hardware.
  None of these produces a sustained or macroscopic negative energy density. (refs: RE-05, RE-07, RE-08) peer-reviewed. The 16 mW pump, the "all GW observatories since 2019" remark and the exact 0.05c figure are unchecked.
- [D-17] **Past exotic-propulsion lab claims: no positive result survives.**
  - EmDrive: Tajmar et al. 2021 find no thrust above the force equivalent of classical radiation, ruling out earlier positives "by at least two orders of magnitude" (abstract).
  - White–Juday interferometer: Lee & Cleaver 2016 show it cannot resolve the effect of a 1e6 V/m field, assumed by them because the field is not specified (field energy density 4.4 J/m³, Schwarzschild radius 1.92e-23 m).
  (refs: RE-09, RE-10) peer-reviewed.
- [D-18] Weak-field gravitomagnetism (frame dragging) is measured. Gravity Probe B reaches about 19%; LAGEOS/LARES reaches a claimed about 2% (§2). This tests only the linear Lense-Thirring term, not a strong-field shift. (refs: RE-01, RE-02) peer-reviewed.
- [D-19] Archimedes plans to weigh Casimir-type vacuum energy in layered high-Tc superconductors (design signal in §2). Only a room-temperature prototype balance has been reported, and there is no vacuum-weight result. (refs: RE-04 peer-reviewed; RE-19 status statement **unverified**, abstract not re-opened.)
- [D-20] Analogue gravity: spontaneous Hawking radiation has been observed from an analogue black hole in a BEC (Steinhauer 2016). No analogue warp-bubble experiment was found. (refs: RE-22; partly verified) peer-reviewed.

## 2. Quantitative anchors
All values are current unless marked. "Ours" means computed in `calc/quantitative_numbers.py` or `calc/engineering_gaps.py` from the cited inputs.

| ID | Quantity | Value ± stat ± sys (units), as quoted | Conditions; current or preliminary; supersedes <ref> if any | Source refs | Access |
|---|---|---|---|---|---|
| D-21 | 2024 warp-shell parameters | R₁ = 10 m, R₂ = 20 m, M = 4.49e27 kg (2.365 M_J; 2.26e-3 M_sun ours), v_warp = 0.04 c | The only published parameter set; found "by trial and error"; constant velocity; current (peer-reviewed) | RT-11, RQ-01 | full-text |
| D-22 | 2024 shell: mean density, compactness, pressure scale (ours) | Mean density M/V = 1.53e23 kg/m³ = 1.38e40 J/m³ (V = 2.932e4 m³); 2GM/c² = 6.67 m; 2GM/(c²R₂) = 0.333; 2GM/(c²R₁) = 0.667; Newtonian pressure scale GMρ/R₂ = 2.3e39 Pa (0.17 ρc²); ρc² = 1.4e40 Pa (upper-bound stress scale) | Our arithmetic on D-21. Fig. 4 axes read by eye as peaks of order 1e40 J/m³ (density) and 1e39 Pa (pressure); axis-read, low confidence. 6.7e5× nuclear saturation density (2.3e17 kg/m³ is unsourced). Buchdahl 8/9 is only a scale, because this is a shell | RQ-02, RE build table | full-text (inputs) |
| D-23 | 2024 shell energies (ours) | Mc² = 4.04e44 J; boost KE ½Mv² at 0.04 c = 3.2e41 J (8e-4 Mc²); 1e5 kg payload KE at 0.04 c = 7.2e18 J; ratio 4.5e22 | Newtonian KE of the shell treated as ordinary matter; Mc² = 6.8e23 world-years at 592.2 EJ/yr (6.5e23 at 620 EJ/yr) | RQ-02, RQ-07, RE-12 | full-text (inputs) |
| D-24 | 2024 shell scaled to a 100 m payload (ours) | R₁ = 100 m, R₂ = 200 m: M = 4.49e28 kg = 23.7 M_J = 2.26e-2 M_sun; mean density 1.5e21 kg/m³; Mc² = 4.04e45 J | Our self-similar scaling: M ∝ R at fixed compactness and v/c; assumes the matter solution rescales; no published scaling law in R, Δ or v | RQ-06 | full-text (inputs) |
| D-25 | Gauge-invariant time delay, Fuchs et al. Table 1 | Warp Shell 7.6 ns; Matter Shell 0 ns; Alcubierre (R = 15 m) 8.0 ns; Van Den Broeck (R₁ = 10 m, R₂ = 15 m, α = 0.1) 9.1 ns; Modified Time (R = 15 m, A = 2) 6.7 ns | v_warp = 0.04 c; Sagnac-like two-arm set-up; 7.6 ns ≈ 2.3 m of light path (ours). Sign convention unresolved: the text calls the Alcubierre case an "advance" while the table lists +8.0 ns (D-33) | RT-11, RQ-04 | full-text |
| D-26 | Observer-robust EC test of a *regularized* Fuchs shell (Le, arXiv:2602.18023v6) | Fuchs rows: Hawking–Ellis Type I in 100% of wall cells, min(ρ + p_i) = 0.021 (table a) and 0.022 (table b, v_s = 0.02), "in R_c² units" as recorded. Alcubierre: 100% Type IV in table (a), v_s not stated in the extracted text; 99.4% Type IV and 0.6% Type I in table (b) at v_s = 0.5. Rodal −2.7e-4; Garattini–Zatrimaylov −3.5e-4 | Preprint, v6 of 24 Sep 2026 (current; six versions since Feb 2026, not compared). Applies to a covariantly modified, C²-regularized shell at fixed smoothing widths, not the published one. Pointwise G_ab/8π tests; source consistency and ANEC are not settled. **Corrected:** the research note's "Alcubierre Type IV 100% at v_s = 0.02" is unsupported (checker) | RC-08, RF-03 | full-text |
| D-27 | Compactness bound, static spherical matter | sup 2m/r ≤ ((1+2Ω)² − 1)/(1+2Ω)²: 8/9 for Ω = 1 (Buchdahl); 48/49 ≈ 0.98 for Ω = 3 (any p ≥ 0 matter obeying the DEC; our arithmetic) | Static, spherically symmetric, ρ ≥ 0, p ≥ 0, p + 2p_T ≤ Ωρ, no shift; sharp | RT-13 | full-text |
| D-28 | Alcubierre Eulerian energy, reference case (ours) | tanh wall (Δ = 2/σ), R = 100 m, Δ = 1 m: v = 1 c → −6.72e46 J = −7.48e29 kg = −0.376 M_sun = −394 M_J; v = 10 c → −6.72e48 J = −7.48e31 kg = −37.6 M_sun. Linear-ramp wall, v = 10 c → −1.12e32 kg = −56 M_sun. Thick-wall floor (linear ramp, Δ ≫ R), v = 10 c → 1.12e30 kg = 0.56 M_sun | Closed form E_geo = −v²R²/(18Δ) (tanh), −(v²/12)R²/Δ (linear ramp; factor 1.5 between the conventions); quadrature matches; Eulerian only. With Bobrick–Martire's factor-3 shape, v = 10 c → −12.5 M_sun (ours) | RQ-13, RQ-08 | secondary (ours) |
| D-29 | Quantum-inequality-limited Alcubierre wall | Δ ≤ 10² v_b L_Planck (α = 1/10); E ≤ −6.2e62 v_b kg for R = 100 m (printed 6.2e65 v_b g). Ours: Δ = 1.6e-33 m (v = 1 c), 1.6e-32 m (v = 10 c); linear-ramp |E| = 6.9e62 kg = 3.5e32 M_sun (v = 1 c) and 6.9e63 kg = 3.5e33 M_sun (v = 10 c), 11% above the published value | Pfenning & Ford 1997: free massless scalar, flat-space QI sampled over times short against the curvature radius. Lentz 2021 cites the Alcubierre baseline as −6e62 v_s/c kg, reduced by later work to −1e30 v_s/c kg (Lentz writes v_s and v_s/c in different places) | RQ-14, RQ-11 | full-text |
| D-30a | Lentz soliton energy scaling | E_tot ~ C v_s² R²/w, C "of order unity"; R = 100 m, w = 1 m → "(few)×10⁻¹ M_sun v_s²", the "same magnitude" as an Alcubierre bubble of the same size. Ours at v = 10 c, few = 2–5: 20–50 M_sun = 4e31–1e32 kg | Eulerian density integral (Lentz's convention, w = average source thickness along z); positivity disputed (D-30). The 2021 CQG text prints "(few)×10⁻¹ M⊙ v_s"; the 2022 proceedings print v_s² | RQ-10, RT-08 | full-text |
| D-34 | Natário zero-expansion Eulerian energy | Ours: R = 100 m, Δ = 1 m, v = 1 c → −5.38e50 J = −6.0e33 kg = −3.0e3 M_sun (8.0e3× Alcubierre at the same R, Δ); v = 10 c → −3.0e5 M_sun. Fit E_geo = −0.0445 v²R⁴/Δ³ (converged to 7 digits on grid halving; ratio to Alcubierre ≈ 0.8 (R/Δ)²; ratio 22 at Δ = 20 m). Preprint bound: E ≥ (1/60) v²R⁴/Δ³ [(1 + Δ/2R)(1 + Δ/R)²]⁻¹; thin-wall sharp minimum E_min ~ v²R⁴/(4Δ³) | Unit lapse, flat slice, Lobo–Visser Eulerian volume integral, geometric units in the bound; the wall conventions differ, so the prefactors differ while the scaling agrees. Bound: Bolívar, Vasilev & Abellán, arXiv:2609.36211 (preprint, 28 Sep 2026). Our fit was not re-run by the checker | RQ-15, RC-10, RF-01 | full-text (bound), secondary (ours) |
| D-35 | Fell–Heisenberg example | ρ_max ≈ 3.2e26 kg/m³ (Eulerian); E_total ≈ 9.25e43 J = 1.03e27 kg = 0.542 M_J = 5.2e-4 M_sun (ours); central shift magnitude 1.26; parameters (Π, r, V, σ) = (1/4, 6, 10, 1) | Eulerian. The paper says "four orders of magnitude" below E_sun = 1.78e47 J; the actual ratio is 5.2e-4, 3.3 orders (corrected). A length unit of 1 m is our inference (low confidence), giving 2GM/c² = 1.53 m and 2GM/(c²·6 m) = 0.26; the authors say "more than likely" it forms a black hole | RT-09, RQ-12 | full-text |
| D-36 | Rodal irrotational drive | Peak proper-energy deficit ≈ 38× below Alcubierre and ≈ 2.6e3× below Natário; peak NEC violation > 60× below Natário; |E₊ − E₋|/(E₊ + E₋) = 0.04%, with E₋ = E₊ = 1.33e44 J per the checker's reading | v = c only (D-11); two-point 1/R tail extrapolation; peer-reviewed | RC-09, RF-04, RF-16 | full-text |
| D-37 | Earth-mass shell time slowing | "a small fraction of 4·10⁻⁴" for an Earth-mass shell with R = 10 m (ours: GM/(c²R) = 4.4e-4) | Bobrick–Martire; non-exotic shells slow interior time; the 2024 shell at 2GM/(c²R₂) = 0.33 slows it far more (magnitude not computed) | RQ-07 | full-text |
| D-38 | Radiative-steering mass cost (Le, arXiv:2606.22531v4) | m_f/m_i = e^(−3L), L = exterior velocity-space path length | Burns joined at static spheres; photon-rocket (Kinnersley) exterior; strict surface DEC; preprint, v4 of 13 Sep 2026, substantially revised and retitled from earlier versions | RQ-05, RF-02, RF-15 | abstract + full-text |
| D-39 | Trip reference, 1e5 kg to α Cen, 4.37 ly (ours, rocket_tools.py) | 1 g photon rocket, accelerate to the midpoint then brake: 3.58 yr ship time, 6.00 yr Earth time, peak β = 0.952, mass ratio 40.4, initial mass 4.04e6 kg, propellant energy 3.5e23 J. Coast at 0.04 c: 109 yr; at 0.1 c: 43.7 yr (photon-rocket start-and-stop mass ratio 1.22). Alcubierre R = 10 m, Δ = 1 m, v = 4.37 c: |E| = 1.4e29 kg = 0.072 M_sun (R = 100 m: 7.2 M_sun). Shell Mc² / rocket propellant energy = 1.1e21; shell mass / payload = 4.5e22 | Ideal photon rocket; flat-space coast times; warp start-up ignored | RQ-16 | secondary (ours) |
| D-40 | Atmospheric signature of a zero-ADM-mass bubble | Luminosity > 1 TW for an aircraft-scale bubble at relativistic speed | Fell & Loeb 2026 preprint (RQ-19 names "Fell et al."; RF-08 names Fell & Loeb, same arXiv:2608.10800). Zero ADM mass only (Alcubierre, VdB, Lentz); not computed for non-zero-ADM-mass shells; assumes the bubble exists | RQ-19, RF-08, RF-19 | abstract + full-text |
| D-42a | Gravity Probe B | Frame dragging −37.2 ± 7.2 mas/yr (GR −39.2); geodetic −6,601.8 ± 18.3 mas/yr (GR −6,606.1) | 642 km polar orbit, Aug 2004–Aug 2005; about 19% (1σ/value); final result | RE-01 | full-text |
| D-42b | LAGEOS/LAGEOS 2/LARES frame dragging | (0.9910 ± 0.0006 stat) ± 0.02 to ± 0.04 sys, relative to GR | 7 yr LARES + 26 yr LAGEOS; systematic from the Earth gravity field; current published | RE-02 | full-text |
| D-42c | LARES 2 target | ≈ 0.2% Lense-Thirring test, claimed "in the near future" | Launched 13 Jul 2022 (date phrase not re-grepped); Ciufolini's claim as reported by Iorio 2025, who disputes it; preliminary/contested | RE-03 | full-text |
| D-43 | Archimedes design signal | Force modulation 5e-16 N; integration 4e6 s (about 2 months); torque ASD 7e-13 N/√Hz | Samples 3 mm thick, 0.15 m radius, modulated at about 10 mHz; design expectation; Casimir fraction of the condensation energy "still under evaluation"; no result | RE-04 | full-text |
| D-44 | Static pressure / strength records | > 1 TPa static (double-stage DAC); nanodiamond yield ≈ 460 GPa at ≈ 70 GPa confinement; graphene intrinsic strength 130 GPa; CNT bundles 80 GPa true (43 GPa engineering) **search-summary only, unverifiable** | Sample about 3 µm × 1 µm. Shell stress scale ρc² ≈ 1.4e40 Pa is 28.1 orders above 1 TPa and 28.5 orders above 460 GPa (ours) | RE-14 | full-text / abstract / search-summary (CNT) |
| D-45 | Fastest human-made object | Parker Solar Probe 430,000 mph = 192.2 km/s = 6.41e-4 c (ours) on 24 Dec 2024 | About 600 kg probe; 0.04 c is about 62× faster | RE-11 | full-text |
| D-46 | World primary energy | 592.2 EJ (5.922e20 J) in 2024 = 6.6e3 kg/yr mass-energy (ours) | Energy Institute Statistical Review 2025 via IEEJ; current. **Supersedes** the 620 EJ (2023) figure (RQ-20, Statistical Review 2024, search summary only, unverifiable). The 2025 edition implies 2023 = 592.2 − 11.9 = 580.3 EJ (our arithmetic); the cause of the difference is not established | RE-12 (current), RQ-20 (superseded) | full-text / search-summary |
| D-47 | Largest controlled fusion yield | 8.6 MJ from 2.08 MJ of laser energy (gain > 4), NIF, 7 Apr 2025 = 9.6e-11 kg mass-energy (ours) | Transient ICF | RE-13 | full-text |
| D-48 | DART momentum demonstration | Dimorphos period change −33.0 ± 1.0 (3σ) min | Only the period change is sourced; the post-impact period, 4.7× enhancement and mass/Δv remarks are unchecked or unsourced and dropped | RE-15 | full-text |
| D-49 | Antimatter production | 1e7 antiprotons per bunch at 100 keV every 2 min, May–November (AD/ELENA). **Corrected (ours):** 1.67e-20 kg per bunch; ≈ 1.5e5 bunches per run ≈ 2.6e-15 kg per run; 2mc² ≈ 4.6e2 J; ≈ 20 orders (3.8e19×) below 1e5 kg | Preprint arXiv:2503.22471. The research note's "1e-8 kg/yr" and "1e18" are wrong and dropped | RE-16 | full-text |
| D-50 | Smallest lab gravity source | Two gold spheres of about 1 mm radius, 90 mg | Westphal et al. 2021. The mass is confirmed in the arXiv abstract; "smallest source mass to date" is **search-summary only**; the mass ratio to Jupiter is about 31 orders (checker) | RE-17 | search-summary |
| D-51 | HF-GW sensitivity need | √S_n ≈ 3e-24 Hz⁻¹ᐟ² for post-merger NS emission at 1–5 kHz at 40 Mpc | Living Review; no instrument can test a warp-bubble GW burst | RE-18 | full-text |
| D-52 | Lab "spacetime distortion" claim (fringe) | Claimed fringe movement ≈ 140–160 nm with a spark gap; ours: GR estimate h ≈ 2.1e-40, path change ≈ 1.5e-40 m over 0.725 m, about 33 orders below | Glenn 2025; **unverified** (abstract not re-opened); our estimate assumes 1 GJ/m³ over 1 mm (illustrative); fringe | RE-20 | abstract |
| D-53 | Reference constants | M_J = 1.898e27 kg; M_sun = 1.989e30 kg; L_Planck = 1.616e-35 m; c⁴/G = 1.21e44 N; M_sun c² = 1.79e47 J; M_J c² = 1.71e44 J | Brief values / computed from ħ, G, c | RQ-20, brief | — |

## 3. Contested or conflicting
- [D-30] **Does Lentz's soliton have non-negative energy density?**
  - Yes, for Eulerian observers: Lentz 2021 claims everywhere-positive Eulerian density (RT-08). His 2022 Marcel Grossmann reply argues that the Santiago et al. divergence-theorem argument fails because his density is only C⁰ at x = 0 and y = 0, and that the no-go proofs assume a limit his soliton "cannot undergo … without being destroyed" (RC-06). He says Santiago et al. "did not adequately analyze" his paper (RC-07).
  - No:
    - Santiago, Schuster & Visser 2022: the class theorem violates the NEC, and they name Lentz explicitly (RT-04, RC-01).
    - Celmaster & Rubin 2025 (preprint): direct Eulerian computation finds negative-energy regions; there are "several derivation errors"; a modified Lentz geometry still violates the WEC even for Eulerian observers; the WEC has no "singular-line exclusion" at the delta-function planes (RC-03, RC-04).
    - Bobrick–Martire's conclusions "do not support" Lentz (RQ-09).
    - Warp Factory reports the WEC-violation argument (RT-12).
    - Barzegar et al. (preprint) say the claims were "refuted correctly (fully or partially) by Santiago et al." (RF-18).
  - No reply by Lentz to Celmaster & Rubin was found. The weight of evidence is against Lentz, but the only direct recomputation is a preprint. That Celmaster & Rubin answer the reply's C⁰ premise is the researcher's inference; the checker did not confirm it against their text.
- [D-31] **Is the Fuchs et al. 2024 shell a valid solution that satisfies the energy conditions?**
  - For:
    - The peer-reviewed paper reports all four energy conditions satisfied by sampled-observer numerics (D-08).
    - Le's observer-robust preprint test of a *covariantly modified, C²-regularized* Fuchs shell finds Type I in 100% of wall cells with min(ρ + p_i) > 0 (D-26). The same preprint's abstract may say otherwise (D-84).
    - Bolívar, Abellán & Vasilev (preprint) show that freeing the lapse admits static hollow shells with flat cavities, Schwarzschild exteriors and NEC/WEC/SEC/DEC on an explicit compactness interval (RC-11, RF-13). The checker did not see the lapse-release sentence in the excerpt read.
  - Against: Barzegar, Buchert & Vigneron 2026 (preprint).
    - Error 18: "not a solution to Einstein's equations", because the TOV equations are not actually solved (their App. B, which says Bobrick–Martire made the same mistake).
    - Error 13: "constant velocity" has no meaning without distinguishing uⁱ and u_i.
    - The asymptotic flatness of the construction is vague.
    - Dropping time derivatives after a Galilean transformation is a mistake.
    (RC-05, RF-18). Error 13 and the asymptotic-flatness point were not individually checked.
  - Le notes his pointwise tests "do not resolve that source-consistency question" (RC-08).
  - No reply from the Fuchs/Helmerich/Martire group was found as of 1 Oct 2026.
- [D-32] **Does vanishing ADM mass explain the energy-condition violation?**
  - Linked: Schuster, Santiago & Visser 2023 formalize ADM mass, giving zero for Alcubierre and Natário and nonzero possible for zero-vorticity drives (RT-05). Fuchs et al. list positive ADM mass as a key ingredient (RQ-03).
  - Not linked: Barzegar et al. (preprint) say "there is no direct relation between the violation of the WEC and the vanishing of the ADM mass" (Error 8; RC-15). Yet their own Thm IV.19 plus the DEC positive-energy theorem gives "zero ADM energy ⇒ DEC fails or flat" for their R-Warp class (RQ-17).
  - These are two groups in conflict, and it is unsettled. Which named metrics fall in the R-Warp class was not checked.
- [D-33] **Sign of the Fuchs et al. time delay.**
  - Table 1 lists +8.0 ns for Alcubierre and positive δt for every model.
  - The p. 27 text says that for Alcubierre "an advance is perceived".
  - The source is internally inconsistent, and the table cannot be used as a travel-time (advance) test until the convention is fixed (RQ-04, quantitative.check).
- [D-54] **Do the 2021 Bobrick–Martire positive-energy shells satisfy the energy conditions?**
  - B-M: Class I spherical positive-energy solutions "satisfy the energy conditions" (RT-10, RQ-08).
  - Santiago et al.: B-M's "model warp drives" also violate the NEC "for slightly different reasons" (RT-04).
  - Barzegar et al. (preprint): B-M share the unsolved-TOV error (RC-05 checker note).
  - Scope matters. The B-M Class I shells have a non-unit lapse, outside the generic Natário class, and which B-M models Santiago et al. mean was not extracted.
- [D-55] **Quantum inequalities against squeezed-light data.** Maclay & Davis 2019 report that a Marecki-type QI "is violated by most of the experimental data", while all data fit an OPA model (RE-06). It is a single group, about a quantum-optics-adapted QI, not the Fewster–Eveson free-field bound. No rebuttal was located; treat it as a minority result.
- [D-84] **Does Le's preprint find the regularized Fuchs shell NEC-clean or NEC-violating?**
  - Clean: the body tables give Type I in 100% of wall cells with min(ρ + p_i) = 0.021–0.022 for the Fuchs rows (RC-08, low confidence on the cell reading).
  - Violating: the v6 abstract says global bounds "establish null-energy violation in all four bubble walls" among "four warp geometries", and the tables have four rows (Fuchs, Alcubierre, Rodal, Garattini–Zatrimaylov) (RF-03).
  - The two readings may refer to different parameter sets or geometries; this was not settled by the researchers or checkers. Read the v6 PDF before using either reading as the energy-condition verdict on the shell.
- [D-56] **Can LARES 2 reach 0.2%?** Ciufolini et al. claim so; Iorio 2025 disputes the systematic budget and proposes POLARES (RE-03). The POLARES detail is unchecked.

## 4. Constraints: theorems, bounds, no-go results
- [D-41] **Santiago–Schuster–Visser NEC theorem (2022).**
  - Statement: every "generic Natário" warp drive violates the NEC, and hence the WEC, SEC and DEC, if the warp field is sufficiently localized.
  - Assumptions: unit lapse N = 1; flat slices h_ij = δ_ij; localized shift; classical GR. It uses monotonicity along Eulerian trajectories and needs neither zero ADM mass nor integration by parts.
  - Domain: it explicitly covers Alcubierre, Natário zero-expansion and Lentz/Fell–Heisenberg zero-vorticity drives. It does **not** cover N ≠ 1 or curved slices, which the authors call "beyond the generic Natário framework". That is the class of the 2024 shell.
  (refs: RT-04, RC-01, RC-02) peer-reviewed.
- [D-57] **Schuster–Santiago–Visser 2023, massive (Schwarzschild-based, Painlevé–Gullstrand) warp drives.** The flow falls off as vⁱ = v₀ⁱ(t) + √(2M/r) r̂ⁱ + O(r^−3/2). For a Schwarzschild-based drive, and for a bubble with payload on a Schwarzschild base, p̄ < 0 over an entire hemisphere at large r, so the NEC (and the SEC, WEC and DEC) fail there. Assumption: unit lapse, flat slices (Natário class). (refs: RT-05) peer-reviewed.
- [D-58] **Natário 2002 Theorem 1.7.** Any non-flat unit-lapse flat-slice warp spacetime violates either the WEC or the SEC. The WEC argument uses Eulerian observers; the SEC argument uses Raychaudhuri. (refs: RT-01) peer-reviewed. Preprint strengthenings by Barzegar et al.:
  - Thm IV.32: the Natário zero-expansion drive violates the WEC (Hamiltonian constraint with K = 0).
  - Thm IV.33: a non-vacuum spacetime with a vanishing-mean-curvature foliation and R < 2Λ + |K|² violates the WEC.
  - Error 26: the Alcubierre WEC violation is independent of v.
  (RF-17).
- [D-59] **Olum 1998.**
  - Statement: superluminal travel requires WEC violation.
  - Definition of superluminal: a path reaching a destination surface earlier than any neighbouring path, the travel-time sense.
  - Assumptions: classical GR; the generic condition on the path (it holds wherever there is normal matter or transverse tidal force); no singularities.
  - Domain: it does not constrain coordinate speeds or flat spacetime in odd coordinates.
  (refs: RT-03) peer-reviewed.
- [D-60] **Gao–Wald 2000, Theorem 1.**
  - Statement: in a null-geodesically complete spacetime satisfying the NEC and the null generic condition, for any compact K there is a compact K′ such that "fastest" causal curves between points outside K′ cannot enter K.
  - The authors' own caveat: K′ may be far larger than K, so this is a weak argument against a finite-region time advance.
  - It does not apply where the NEC fails. It is a key step of the Penrose–Sorkin–Woolgar positive-mass argument.
  (refs: RT-06) peer-reviewed.
- [D-61] **Visser–Bassett–Liberati 2000.** In linearized gravity about Minkowski space, the NEC narrows light cones, so Shapiro delay is always a delay. Effective FTL by tipped light cones therefore needs NEC violation. This is a perturbative argument from conference proceedings. (refs: RT-07) peer-reviewed.
- [D-62] **Positive-mass theorems.**
  - Penrose–Sorkin–Woolgar 1993: a causal-structure proof that positive energy density focuses and retards null geodesics, while negative total mass would advance them (RT-14; abstract; preprint status).
  - Schoen–Yau/Witten: asymptotically flat data obeying the DEC have ADM mass ≥ 0. Treated as textbook, **not quoted from a primary source this run**.
  - Barzegar Thm IV.19 (preprint): R-Warp models have E_ADM = 0, so under the DEC they are Minkowski (RQ-17).
- [D-63] **Andréasson 2008 compactness bound.** See D-27.
  - Assumptions: static, spherically symmetric, ρ ≥ 0, p ≥ 0, p + 2p_T ≤ Ωρ.
  - Bounds: Buchdahl's 8/9 for Ω = 1; 48/49 for DEC matter with p ≥ 0 (Ω = 3).
  - It caps a plain matter shell's mass. It does **not** cap the shift added to it. Fuchs et al. state only qualitatively that the shift's momentum flux adds a further upper limit (RQ-03).
  (refs: RT-13) peer-reviewed.
- [D-64] **Fuchs et al. horizon and shift caps.** The cap is R_shell > 2GM_shell/c², and the shift magnitude is bounded because it adds momentum flux. No closed-form cap on the shift at given compactness was found. (refs: RT-11, RQ-03) peer-reviewed.
- [D-65] **Bobrick–Martire superluminal-matter result.**
  - Statement: Class II/III (superluminal) drives require matter at rest in a spacelike frame; for a perfect fluid this violates the DEC. Spherically symmetric positive-energy drives are Class I, always subluminal.
  - Assumption for the class statement: spherical symmetry.
  (refs: RT-10) peer-reviewed.
- [D-66] **Bolívar–Abellán–Vasilev static boundary obstruction (preprint).**
  - Statement: in the unit-lapse, flat-slice radial Painlevé–Gullstrand class, an empty flat cavity inside a regular nonnegative-density wall has p_r = −ρ and p_⊥ = −ρ − rρ′/2. A density rising out of the cavity therefore violates the transverse NEC and WEC.
  - Scope: "a static boundary theorem and construction, not … a transport result".
  (refs: RC-11, RF-13) preprint.
- [D-67] **Pfenning–Ford 1997 quantum-inequality wall bound.**
  - Bound: Δ ≤ 10² v_b L_Planck for α = 1/10 (D-29).
  - Assumptions: free massless scalar field; flat-space QI applied over sampling times short against the local curvature radius.
  - It applies to negative-energy (Alcubierre-type) walls only.
  (refs: RQ-14) peer-reviewed.
- [D-68] **Bolívar–Vasilev–Abellán Natário minimum (preprint).**
  - Bound: E ≥ (1/60) v²R⁴/Δ³[(1 + Δ/2R)(1 + Δ/R)²]⁻¹, with sharp thin-wall E_min ~ v²R⁴/(4Δ³).
  - Assumptions: unit lapse; flat slice; flat interior radius R; exact matching to a uniform exterior stream at R + Δ; Lobo–Visser Eulerian integral (not ADM mass); geometric units.
  (refs: RQ-15, RC-10, RF-01) preprint.
- [D-69] **Momentum accounting for start and stop.**
  - Bobrick–Martire: "any warp drive requires propulsion" (D-07).
  - Le's radiative steering (preprint): the Bondi four-momentum balance holds. Zero matter flux leaves the total Bondi momentum fixed. Steering comes from anisotropic photon emission with mass cost e^(−3L), and the Bondi news vanishes, so there is no GW flux (RF-15, D-38). The rocket-equation lemma was not grepped. The researcher's inference that it cannot beat a photon rocket in momentum accounting is consistent with the text.
  - A primary-source theorem on whether an isolated warp spacetime can change its own ADM momentum was **not found** (§6).
- [D-70] **Rodal 2025 metamaterial-coupling no-go (preprint, unverified).** A prescribed κ(x) in G^μν = κ(x)T^μν contradicts the contracted Bianchi identity. A dynamical κ is a scalar-tensor theory excluded by |γ − 1| ≲ 1e-5 (Solar System, pulsar timing). (refs: RF-21) The checker did not open it.
- [D-71] **Horizons and control for superluminal bubbles.** See D-13 (Everett–Roman; Finazzi–Liberati–Barceló). A subluminal shell without a horizon is outside both. Coutant et al. 2012 report the instability persists with UV Lorentz-violating dispersion (abstract only, unchecked).

## 5. Frontier and speculative (labelled; not established)
- [D-72] [frontier, preprint] Le, "Radiative steering of warp shells", arXiv:2606.22531v4. The construction:
  - exact junctions between a flat cavity and a Kinnersley photon-rocket exterior;
  - strict surface DEC;
  - subluminal steering under nonnegative radiation, with m_f/m_i = e^(−3L);
  - freely falling interior observers are inertial, but "an observer needs a force to follow the accelerating cavity center".
  It is a start-stop-steer construction powered by emitted radiation: a photon rocket with a warp-style cavity, **not self-propelled**. Self-gravitating settling after a turn is open, and the abstract also reports growing normal modes in self-similar shells (checker). (refs: RQ-05, RF-02, RF-15)
- [D-73] [frontier, preprint] Le, "Observer-robust energy condition verification", arXiv:2602.18023v6. The method uses S-lemma LMI tests with interval-arithmetic certificates (the Warpax toolkit), with no Hawking–Ellis classification or rapidity cutoff needed. Results:
  - "At the reference parameters, the global bounds establish null-energy violation in all four bubble walls", Rodal's irrotational profile included. Which four geometries these are was not recorded. The body tables list Fuchs, Alcubierre, Rodal and Garattini–Zatrimaylov rows, yet D-26 reports a positive min(ρ + p_i) for the regularized Fuchs shell. This apparent tension within one preprint is unresolved; see D-84.
  - For Rodal's profile, the Eulerian reading misses about 73% of the sampled wall WEC violations.
  - The type labels and fractions are samples, not interval bounds.
  (refs: RF-03, RC-08)
- [D-74] [frontier, preprint] Le, "Relativistic elastic shells", arXiv:2605.25417v3. Nonnegative isotropic pressure cannot support a static spherical shell of positive-density matter with two free vacuum faces. Tangential elastic stress admits equilibria that, in sufficiently weak gravity, obey the DEC with subluminal sound speeds. The cavities are locally flat, with redshifted clocks. Nonspherical and rotating stability are open. This bears on the matter model for any positive-energy shell (premise 6). Note: the brief's "Le 2026, arXiv:2605.25417, on the 2024 shell's boundary" is this paper, not a critique of the 2024 shell; the versions (v1–v3) were not compared. (refs: RF-05, RC gaps)
- [D-75] [frontier, preprint] Garattini & Zatrimaylov, arXiv:2502.13153v4. An Alcubierre-type bubble in de Sitter space, moving at the expansion speed, can have non-negative energy density, with the WEC and NEC holding only "up to a total divergence term that averages to zero". The background is not asymptotically flat and the conditions hold in an averaged sense, so it fails the brief's pointwise WEC. (refs: RF-06)
- [D-76] [frontier, preprint] Jusufi & Lobo, arXiv:2609.05554. A T-duality-inspired Alcubierre profile with closed-form Eulerian E = −(15π/1024) v_s² l (geometric units; the formula was not displayed in the checker's grep). "Exotic matter remains necessary." (refs: RF-07)
- [D-77] [frontier, preprint] Lentz & Felton 2024, arXiv:2405.19381. A technosignature programme to search for emissions from warp travel. It assumes positive-energy bubbles exist and gives no number. (refs: RF-10, RQ-19)
- [D-78] [frontier, preprint, unverified primary] Fell & Loeb cite Sellers et al. as showing that present GW detectors are sensitive to rapidly or massively accelerating objects, "which would include non-zero ADM mass accelerating warp drive spacetimes". The primary paper was not located. (refs: RF-20)
- [D-79] [frontier, peer-reviewed, abstracts only] Abellán et al. 2024 (CQG 41, 105011): a non-uniform lapse accommodates a fluid with heat flow. Bolívar et al. 2025 (Ann. Phys. 481, 170147): a piecewise analytic Painlevé–Gullstrand-type shell leads to an anisotropic T_μν. Both are paywalled and **unverified** (checker could not open them). (refs: RF-24)
- [D-80] [frontier, peer-reviewed, unverified] Chowdhury 2025 (EPJC 85, 112) extends the Alcubierre–Natário class via Martel–Poisson charts (Minkowski, AdS and dS backgrounds; non-flat slices). NEC violations remain. The checker did not open it. (refs: RF-14)
- [D-81] [speculative: negative active mass] Shirokov, arXiv:2608.24577. A positive-mass plus phantom-scalar "Bondi dipole" in 3+1 numerical relativity self-accelerates to 0.056 c by t = 400 (geometric units), with total signed momentum zero to ≲ 1%. Not a warp metric; it never counts toward established physics. (refs: RF-23)
- [D-82] [fringe] Glenn 2025: a spark-gap interferometer "spacetime distortion" claim, with no replication (D-52; unverified). Astrum Drive (G. Martire, a co-author of the 2021 and 2024 papers) holds an NSF SBIR Phase I "to test our warp-drive framework in a lab" and claims a "recipe" using counter-rotating EM fields. No measurement has been reported, and the EM-field claim is unchecked. (refs: RE-20, RE-21)
- [D-83] [frontier, secondary] Analogue warp metrics by transformation optics were seen only in model-written summaries; a 0.25c cap is asserted but unverified. Barcelo et al. 2022 on chronology protection in analogue gravity: the title was confirmed, the content was not. (refs: RE-22)

## 6. Unknowns and gaps
- **No all-observer energy-condition calculation from this run exists yet.** Every energy in §2 is an Eulerian integral or a published claim. The NEC/WEC/SEC/DEC table with Hawking–Ellis types belongs to the constraints lens; the brief's tools `tools/numeric_stress_energy.py` and `tools/warp_shell.py` exist but produced no evidence used here.
- **The travel-time test is not done.** No source computes whether any of these metrics yields arrival before light between exterior rest points; this is the examiner's calculation. Fuchs Table 1 cannot serve until its sign convention is fixed (D-33).
- **The 2024 shell has no published E₋, E₊ or Eulerian integral,** no peak density or pressure numbers beyond the axis read, no scaling law in R, Δ or v, and no closed-form cap on the shift at given compactness (§2 D-22, D-24; D-64).
- **Whether the 2024 shell solves Einstein's equations** (Barzegar Error 18) has no reply. Its matter model (isotropic against tangential stress: D-74) is unresolved, and Le's regularized test covers a modified shell (D-26).
- **No accelerating positive-energy warp solution with solved dynamics exists.** No primary-source theorem on an isolated warp spacetime changing its own ADM momentum was found. The Schoen–Yau/Witten positive-mass theorem was not quoted from a primary source.
- **Lentz's soliton is unresolved.** Its plasma source is not exhibited as a full solution. Celmaster & Rubin are unrefereed. No Lentz reply after 2022 was found.
- Le 2026 version histories (2602.18023 v1–v6, 2605.25417 v1–v3, 2606.22531 v1–v4) were not compared; their numbers are moving.
- **Not opened this run:** Alcubierre 1994; Lobo & Visser 2004; Everett 1996; Shoshany & Snodgrass 2023 (closed timelike curves); Santiago et al. App. C on Fell–Heisenberg; Rodal 2025 metamaterial paper; Mach-effect thruster tests (Kossling et al. 2019; Neunzig et al. 2022); NSF award abstract; ISS mass; Starship payloads.
- **Unknown parameters:**
  - Fell–Heisenberg's length unit (1 m is an inference).
  - The parameters behind Bobrick–Martire's "two orders of magnitude".
  - Nuclear saturation density (2.3e17 kg/m³) is used but unsourced.
- **Experiments:**
  - No experiment was found that tests a premise specific to a positive-energy shell, such as a strong-field gravitomagnetic shift sourced by moving matter. GP-B and LARES test only the weak-field linear term. No peer-reviewed lab gravitomagnetism measurement was found.
  - The quantum-inequality gap for squeezed light was not computed.
  - Archimedes has no cryogenic-run date or prototype sensitivity number.
  - No atmospheric or GW signature has been computed for non-zero-ADM-mass shells (D-40, D-78).
- **PAPER TO REQUEST:**
  - 10.1007/s12567-021-00385-1 | High-accuracy thrust measurements of the EMDrive and elimination of false-positive effects | the balance sensitivity (µN) and the exact quoted limit.
  - 10.1142/S0217751X24430280 | Weighing the vacuum with the Archimedes experiment | the timeline and current balance sensitivity.
  - 10.1088/1361-6382/ad3ed9 | Spherical warp-based bubble with non-trivial lapse function and its consequences on matter content | whether lapse freedom gives DEC-satisfying warp matter, and with what sources.
  - 10.1016/j.aop.2025.170147 | Warp bubble geometries with anisotropic fluids: a piecewise analytical approach | whether its piecewise shells meet the NEC, WEC and DEC for all observers.

## 7. Source-quality notes
- **Claims compiled:** 95 (theory 14, quantitative 20, critiques 15, engineering 22, frontier 24). Checker verdicts:
  - theory: 14 verified;
  - quantitative: 19 verified, 1 unverifiable;
  - critiques: 14 verified, 1 misattributed;
  - engineering: 18 verified or partly verified, 3 unverifiable, 1 contradicted as written;
  - frontier: 20 verified, 3 unverifiable.
  No claim was status-wrong.
- **Superseded values:**
  - World primary energy: 620 EJ (2023; RQ-20, Statistical Review 2024, search summary) is superseded by 592.2 EJ (2024; RE-12, Statistical Review 2025), whose implied 2023 value is 580.3 EJ (ours). The cause of the difference is not established.
  - Le's preprints are cited at their latest versions (2602.18023v6, 2605.25417v3, 2606.22531v4); earlier versions were not compared.
  - No erratum or re-analysis of the Pfenning–Ford, Lentz, Fell–Heisenberg or Fuchs numbers was found.
- **Dropped or corrected:**
  - RE-16 (antimatter): the "≈1e-8 kg/yr" and "≈1e18 below" figures are contradicted and dropped; the corrected values are ≈ 2.6e-15 kg per run and ≈ 4.6e2 J (D-49).
  - RC-08 (misattributed): the "Alcubierre Type IV 100% at v_s = 0.02" cell is replaced with the table (a)/(b) values (D-26).
  - RT-09/RQ-12 (Fell–Heisenberg): the "roughly 1e-4 M_sun / four orders" figure is corrected to 5.2e-4 M_sun, 3.3 orders.
  - RE-15: the unsourced remarks on Dimorphos's mass and Δv dropped.
  - RE-17: "25+ orders" noted as conservative (≈ 31 orders by mass).
- **Errors in the brief's leads:** the brief's arXiv:2605.25417 "on the 2024 shell's boundary" is the elastic-shells paper (D-74). The shell critique is Barzegar et al., and the observer-robust test of a regularized shell is Le 2602.18023. Fell et al. 2026 (RQ-19) and Fell & Loeb 2026 (RF-08) are the same arXiv paper.
- **Unverifiable claims kept, marked unverified:** RQ-20 (superseded), RE-19, RE-20, RF-14, RF-21, RF-24.
- **Search-summary share:** 2 of 95 claims (≈ 2%) rest only on search summaries (RQ-20, RE-17). Two sub-figures inside other claims are also summary-only: the CNT 80 GPa (RE-14) and the analogue 0.25c cap (RE-22). Many frontier claims rest on abstracts only (ACCESS: abstract); that is labelled throughout.
- **Preprint dependence:** several items are unrefereed preprints, many from 2026 and some only days old (Bolívar et al. 2609.36211, 28 Sep 2026). These include:
  - every critique of the 2024 shell (Barzegar et al.);
  - the only direct recomputation against Lentz (Celmaster & Rubin);
  - the Natário sharp bound;
  - all start-and-stop constructions (Le).
- **Fringe excluded from evidence:** Glenn 2025 and the Astrum Drive claims appear only in §5 as fringe.
- **Missing facets:** none. All five brief facets and their checks are present.
- **Carried from earlier runs:** 0 claims carry a PRIOR line. The two prior runs (2026-09-29-alcubierre-negative-energy and 2026-09-29-warp-bubble-shapes) were used as leads only. The quantitative facet states that every claim was re-found in its source this run. Engineering cites the shell mass as an "earlier-run lead", but the theory and quantitative facets verified it independently (RT-11, RQ-01). Carried and re-verified: 0 of 0.
