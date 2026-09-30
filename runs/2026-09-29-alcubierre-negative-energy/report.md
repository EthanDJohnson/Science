# Negative-energy options for a superluminal Alcubierre-type drive: report
*Run 2026-09-29-alcubierre-negative-energy · 2026-09-29 · depth quick · question: "Considering Alcubierre drives, what are viable engineering options for the negative energy required to travel at superluminal effective speeds?"*

## Bottom line
- **There is no viable engineering option, and none is buildable by 2100.** Credence in the null (C1) is 0.85.
- **Every superluminal warp metric needs energy-condition-violating matter.** This rests on theorems: Olum 1998 and Santiago–Schuster–Visser 2022.
- **None of the proposed sources survives its own decisive test:**
  - Casimir plates, squeezed light and "negative effective mass" media fail.
  - Van Den Broeck's pocket fails.
  - The positive-energy solitons of Lentz and Fell–Heisenberg fail.
- **The single biggest reason is scale.** Even with the quantum-inequality (QI) limit set aside, the smallest known budget at the reference case is:
  - about 1e28–1e30 kg of negative energy (0.006–0.56 M_sun) at R = 100 m and v = 10c;
  - roughly 24–26 orders of magnitude more than a year of world primary energy;
  - about 60 orders more than any demonstrated Casimir energy.
- **Horizons add a separate obstacle.** They stop the ship from creating or steering the bubble.
- **One qualification.** Established physics does not strictly prove the drive impossible:
  - The quantum inequalities that force Planck-thin walls are proven only for free fields, and interacting fields are known to evade them.
  - What would close the door completely is a conjecture, the self-consistent achronal averaged null energy condition (ANEC).
- **The answerable nearby goal is sub-light travel.** A relativistic rocket needs no negative energy and is about 23 orders of magnitude closer to feasible.

## Ranked answers
Credences are independent (candidates.md: not mutually exclusive). For options, the credence is for "viable in principle under established physics". For reframes, it is for "correct as stated", with the narrowed form in brackets. Energies are in kg (SI) at R = 100 m and v = 10c unless noted.

| # | Candidate | In principle | In practice (horizon) | Key obstacle | Gap (orders of magnitude) | Credence |
|---|---|---|---|---|---|---|
| 1 | **C1 Null:** no option supplies or avoids the negative energy; none buildable by 2100 | The need is theorem-backed. Excluding every supply rests on the free-field QI plus a conjecture (self-consistent achronal ANEC) | Holds: TRL ≤ 1, not by 2100 | Energy scale, QIs, horizons | 60.6–94.9 above the Bressi Casimir energy; 25.6–59.8 above one world-year | **0.85** |
| 2 | **C8 Reframe:** drop "superluminal" (relativistic rocket; Fuchs shell) | Rocket: yes. Fuchs shell: positive-energy only while coasting | Rocket: not by 2100 at 1e5 kg payload | Antimatter supply | Photon rocket 10^2.8 world-years; antimatter 10^17.1 × all ever made | 0.6 (0.9) |
| 3 | **C7 Reframe:** total Eulerian energy is the wrong figure of merit | Holds for lapse, irrotational and flattened variants | n/a | n/a | n/a | 0.5 (0.85) |
| 4 | **C6 Reframe:** the obstacle is causal, so a pre-laid track is needed | Horizon facts hold. "Not quantitative" and "round trips only" fail | Track: TRL ≤ 1 | Supply, as for C1 | Same as C1 | 0.25 (0.85) |
| 5 | **C2** Thick-wall or flattened bubble on a pre-laid track, with a source the free-field QI does not govern | Only if such a source exists (not excluded; none known) | No, TRL 1 | Supply; horizons; growth of the renormalized stress-energy (RSET, 2D models) | Spherical floor 10^26.2 world-years and 10^61.3 Bressi; flattened about 2 lower (ours); free-field QI exceeded by ≥ 4e67 | 0.10 |
| 6 | **C3** Van Den Broeck pocket, femtometre neck, "QI satisfied" | Refuted: QI violated by 2.0e33 | No | QI; curvature near Planck scale | Density 10^107.3 above ideal 20 nm Casimir; energy 10^61.4–10^63.4 above Bressi | 0.02 |
| 7 | **C4** Positive-energy solitons (Lentz; Fell–Heisenberg) | Refuted: kink-plane energy cancels Lentz's total; SSV NEC theorem; Fell–Heisenberg "superluminal" is only an ergoregion | No, TRL 0–1 | Theorems; self-gravity (2GM/c² ≈ 1.1e3 R) | Positive density 10^7.4 above quark–gluon plasma | 0.02 |
| 8 | **C5** Scale up lab negative energy (Casimir, squeezed light, negative effective mass) | Refuted: Casimir cells net positive by ≥ 3.5e3; squeezed light limited by the proven EM QI; negative effective mass has T_00 > 0 | No, TRL about 1 | Plate mass; proven QI | Squeezed light 10^67.3 short at a 1 m, 10c wall; graphene Casimir 33.5 short in density | 0.01 |

## Why, candidate by candidate

**C1 (null): weakened, survives in narrower form** (verdicts/C1-0.md).
- **For.**
  - Energy-condition violation is required by Olum's WEC theorem [D-50] and by Santiago–Schuster–Visser for the Natário class [D-51]. The NEC also fails at every speed [D-03, D-52].
  - The falsifier reproduced C1's key numbers: QI wall 1.58e-32 m, giving 4.74e63 kg (2.38e33 M_sun); thick-wall floor 1.12e30 kg, which is 10^26.2 world-years.
- **Against.**
  - Olum & Graham 2003 (full text) show the QIs "are simply not correct in the case of interacting fields", and that Casimir systems violate them too.
  - The ANEC is violated on fixed curved backgrounds (Urban & Olum 2010, abstract only). So complete in-principle exclusion rests on the self-consistent achronal ANEC, which is a conjecture.
  - Bostelmann–Fewster expect no state-independent bounds for general interacting theories (cited in verdicts/C2-0.md).
- **Net.** "Impossible in practice" is robust by 24 or more orders of magnitude. "Impossible in principle under established physics" holds only if that conjecture is true.
- **Decisive test.** Prove or disprove that a superluminal bubble must contain a complete achronal null geodesic with a negative ANEC integral in a self-consistent semiclassical spacetime.

**C8 (sub-light reframe): weakened, but its narrow form is strong** (verdicts/C8-0.md).
- **For.** The rocket figures reproduce with `rocket_tools`: 3.58 yr ship time, 6.00 yr Earth time, mass ratio 40.4, and 3.54e23 J for a 1e5 kg payload. That is 22.8 orders below the cheapest established-physics warp against world energy, and 43.6 orders on a like-for-like basis (antimatter against Casimir).
- **Against.**
  - Fuchs et al.'s own §5.3 says naive acceleration "requires a negative energy density throughout space", and the positive-energy alternative is "rocket-like". The shell is therefore positive-energy only at constant velocity.
  - Le 2026, a single-author preprint, reports violations at the shell boundary; a later version drops that statement.
  - "Cheapest superluminal warp" must exclude White's [speculative] brane-world claim of 1e3 kg.
  - For a pion rocket with v_e = 0.33c the margin shrinks to 19.5 orders.
- **Decisive test.** Solve a positive-energy acceleration phase for a Fuchs-type shell.

**C7 (figure of merit): weakened** (verdicts/C7-0.md).
- **For.**
  - For the Loup lapse from A₀ = 1 to 10, the Eulerian total falls 98× while the worst-null NEC integral rises 1.37× (−4.10 to −5.60 m, geometric units).
  - The irrotational shift has E_tot = 0 yet fails every energy condition.
  - Flattening moves stress into K_xx, which ρ_Eul leaves out (checked analytically).
  - Under the free-field QI, thick walls and QI-bound supply are mutually exclusive (a mismatch of 10^63.6).
- **Against.**
  - The "~8e3× worse" Natário penalty belongs to Natário's compact published profile. A zero-expansion shift with a dipole exterior restores the Alcubierre v²R²/Δ scaling, at about 2–13× the Alcubierre energy.
  - Nobody claimed Natário's drive as a reduction [U-10].
  - Rodal 2026 reports a real 38× reduction in a local peak measure [D-28, not reproduced].
- **Decisive test.** Compute the observer-robust NEC integral for the dipole-exterior Natário and Rodal drives.

**C6 (causal reframe): weakened** (verdicts/C6-0.md).
- **For.** The shares reproduce: at 10c, 97.2% (tanh) and 90% (linear ramp and Bobrick–Martire optimal) of E_− lies at f < 1 − 1/v. The front wall is outside the ship's causal future [D-58].
- **Against.**
  - Everett & Roman (full text) say a *pre-laid* Alcubierre track gives passengers *one-way* superluminal trips. The round-trip-only limit belongs to Krasnikov tubes.
  - E_− is continuous across v = 1: the ratio between 1.01c and 0.99c is 1.041. The quantitative obstacle binds at every speed, and the causal one comes on top of it.
  - The rear half of that energy (48.6%) lies in the ship's causal future.
- **Decisive test.** Compute the comoving-source fraction for Natário and Loup-lapse metrics.

**C2 (thick or flattened wall with a non-free-field source): weakened** (verdicts/C2-0.md).
- **For.** The "only if" logic holds. The free-field QI is exceeded by at least 4e67 at D = 100 m, and the literature does leave loopholes for interacting fields.
- **Against.**
  - "At least 1.12e30 kg" holds only for spherical, unflattened profiles:
    - C2's own flattening rule gives 1.11e28 kg.
    - A transverse "pancake" profile goes logarithmically toward 0 in Eulerian energy (7.3e29 kg at 1 km transverse extent).
  - Both savings shift stress into non-Eulerian components, and nobody computed the pancake's stresses.
  - Horizons, the lack of self-acceleration [D-62] and RSET growth (2D models) remain.
- **Decisive test.** Derive a QEI for the proposed interacting or plasma source at τ₀ ~ D/(vc). A net-negative density of at least 1.3e23 kg/m³ sustained over metre scales would keep C2 alive.

## Eliminated, and what eliminated them
- **C3, Van Den Broeck** (verdicts/C3-0.md; basis: calculation plus a check of the paper's arXiv versions).
  - The paper's "QI amply satisfied" figures come from its v1–v4 Planck-scale parameters (α = 1e34). They were never redone for the published femtometre neck (α = 1e17).
  - At the stated parameters the recomputation gives r_c = 2.3e-17 m and a QI violation of 2.0e33. The lens's independent `curvature_at` calculation agrees.
  - Passing the QI needs r_c < 32 L_P, which is outside semiclassical validity.
  - The region-II energies (−1.38e30 kg and +4.87e30 kg) do reproduce.
- **C4, positive-energy solitons** (verdicts/C4-0.md; basis: calculation plus a peer-reviewed theorem).
  - For Lentz's l1-norm gradient shift, δ-function sheets on the x = 0 and y = 0 planes cancel the smooth Eulerian energy exactly (the sum is zero to 1e-5 relative). Positive smooth energy therefore forces negative energy on the sheets.
  - SSV prove NEC violation for any localized Natário-form drive "without any need to assume zero ADM mass".
  - Fell–Heisenberg's "superluminal" means N·N > 1, i.e. an ergoregion. The authors expect their own example to form a black hole.
- **C5, lab negative energy** (verdicts/C5-0.md; basis: calculation).
  - Casimir: a scale-free bound (Lifshitz formula plus the f-sum rule) makes the plates outweigh their deficit by at least 3.5e3 at any gap; for graphene the factor is 5.9e9.
  - Squeezed vacuum: the proven free-field EM QI holds in this regime and leaves it 10^67.3 short.
  - "Negative effective mass" BEC: T_00 ≈ +1.3e12 J/m³ (SI).

## Assumptions every surviving answer shares
- Semiclassical GR is the right framework at wall scales. If walls must be near-Planckian, it is not.
- The [speculative] routes are excluded from "established physics": negative-mass matter, Einstein–Cartan torsion, brane worlds (White's "Warp Field Mechanics 102"), modified gravity. Admitting them would change C1's in-principle verdict, not its in-practice one.
- The Eulerian energy is an adequate *lower* proxy for the exotic stress. C7 argues it understates it.
- The semiclassical instability results (Hiscock; Finazzi et al.) carry over from 2D models to 4D.

## What would change this verdict
1. **A QEI, or a proof that none exists, for a realistic interacting source** (plasma or dielectric electromagnetism) that allows net-negative, metre-thick walls held for months. This would lift C2 toward 0.3 and cut C1 toward 0.6.
2. **A proof that the self-consistent achronal ANEC holds and applies to superluminal bubbles.** This would push C1 above 0.95 in principle and C2 below 0.03.
3. **A superluminal metric with 2GM/c² < R that passes an observer-robust NEC/WEC test** (the Le-type matrix test [D-69] on the full Lentz and Fell–Heisenberg metrics). This would revive C4 and roughly halve C1.

## Key numbers
| Quantity | Value (units) | Source or calc |
|---|---|---|
| Alcubierre, tanh, Δ = 1 m, 10c | −7.5e31 kg (−38 M_sun) | [D-17]; calc/falsifier-C6-0_causal_vs_quant.py (−7.48e31 kg) |
| Free-field QI wall at 10c | 1.58e-32 m | calc/falsifier-C1-0_checks.py |
| Alcubierre at the QI wall, 10c | −4.74e63 kg (2.38e33 M_sun), 5.1e10 × the Hubble-radius mass | calc/falsifier-C1-0_checks.py |
| Spherical thick-wall floor, v²R/12 (geometric) | −1.12e30 kg (0.56 M_sun) = 1.01e47 J; 10^26.2 world-years; 10^61.3 × Bressi | calc/falsifier-C1-0_checks.py |
| Flattened floor (α_X = 101) | −1.11e28 kg (5.6e-3 M_sun) | calc/falsifier-C2-0_pancake_floor.py |
| Pancake profile, 1 km transverse extent | −7.3e29 kg | calc/falsifier-C2-0_pancake_floor.py |
| Natário (quintic wall) vs Alcubierre, reference case | compact −4.91e36 kg; dipole −2.16e33 kg; Alcubierre −1.62e32 kg | calc/falsifier-C7-0_natario_noncompact.py |
| Van Den Broeck region II | −1.38e30 kg / +4.87e30 kg; QI violated by 2.0e33 at α = 1e17 | calc/falsifier-C3-0_vdb_qi.py |
| Casimir plate-to-deficit ratio | ≥ 3.5e3 (any gap); 5.9e9 (graphene, 0.335 nm gap) | calc/falsifier-C5-0_mirror_cost.py; calc/falsifier-C5-0_lab_sources.py |
| Ideal gap for the wall's peak density of 1.2e44 J/m³ | 1.38e-18 m | calc/falsifier-C5-0_lab_sources.py |
| Squeezed-light QI shortfall, 1 m wall at 10c | 10^67.3 | calc/falsifier-C5-0_lab_sources.py |
| Largest demonstrated Casimir energy | 5.0e-15 J (ideal-plate formula, Bressi geometry) | calc/lens-engineer_gaps.py |
| Share of E_− beyond the horizon at 10c | 97.2% (tanh); 90% (linear ramp and Bobrick–Martire optimal) | calc/falsifier-C6-0_causal_vs_quant.py |
| Loup lapse, A₀ = 1 → 10 | E_Eul falls 98×; worst-null NEC integral rises 1.37× | calc/falsifier-C7-0_nec_integral.out |
| Photon rocket, 1 g to 4.37 ly, 1e5 kg payload | 3.58 yr ship time; 3.54e23 J (10^2.78 world-years) | calc/falsifier-C8-0_reframe_gaps.py |
| Fuchs shell, accelerate and brake to 0.04c | ≥ 6.5e41 J (10^21.0 world-years) | calc/falsifier-C8-0_reframe_gaps.py |
| RSET growth per 0.44 yr cruise (2D models) | ≥ 1.5e13 e-folds (lens); about 4e13 (falsifier) | calc/lens-constraints_horizons_tides_sources.py; calc/falsifier-C1-0_checks.py |

**What would move a headline number by 2×:**
- The QI-wall energy moves 2× with the Δ convention and the choice of sampling parameter α [D-47].
- The floor moves 2× with a 2× change in R, or a √2 change in v.
- The Casimir ratio moves 2× with the plates' areal mass.
- The null credence of 0.85: a proof of item 2 above would roughly halve its remaining doubt, taking it to about 0.92; item 1 would lower it to about 0.4–0.6.

## Caveats
- **Quick run, no source check.** Every dossier item is unchecked, and the lens and falsifier calculations were run inside this run and are unreviewed. The ranking relies mostly on falsifier calculations with visible code; I spot-checked the C1 and C3 calculations.
- **Abstract-only or search-summary evidence:**
  - Graham–Olum 2007, Urban–Olum 2010, Krasnikov 1998 and 2003, and Fewster–Hollands were read as abstracts only.
  - The antimatter production figure (about 16 ng) comes from a search summary. It affects only C8's like-for-like margin.
  - The downgrade of C1's in-principle half rests on Olum & Graham 2003 (full text) plus those abstracts. That is why C1 sits at 0.85 rather than above 0.95.
- **Preprints.** Celmaster–Rubin 2025 could not be retrieved and was not used. Le 2026 is a single-author preprint whose later version has changed.
- **Not computed:**
  - full stresses for the pancake and dipole-exterior Natário profiles;
  - an observer-robust (Le-type) test on any metric;
  - tidal forces, for which no literature was found [D-63];
  - 4D semiclassical stability.
- **Unresolved:** the factor-of-2 discrepancy in the QI wall thickness [D-47].
- **Speculative physics:** White's oscillating (brane-world) variant and the torsion and extra-dimension routes were labelled and excluded, not evaluated.

## Sources
- Pfenning & Ford 1997: https://arxiv.org/abs/gr-qc/9702026
- Van Den Broeck 1999, CQG 16 3973 (v1–v5): https://arxiv.org/abs/gr-qc/9905084
- Santiago, Schuster & Visser 2022, PRD 105 064038: https://arxiv.org/abs/2105.03079
- Lentz 2021, CQG 38 075015: https://arxiv.org/abs/2006.07125
- Fell & Heisenberg 2021, CQG 38 155020: https://arxiv.org/abs/2104.06488
- Lobo & Visser 2004: https://arxiv.org/abs/gr-qc/0406083
- Natário 2002: https://arxiv.org/abs/gr-qc/0110086
- Olum & Graham 2003, PLB 554 175: https://arxiv.org/abs/gr-qc/0205134
- Graham & Olum 2007, PRD 76 064001: https://arxiv.org/abs/0705.3193
- Urban & Olum 2010, PRD 81 024039: https://arxiv.org/abs/0910.5925
- Bostelmann & Fewster 2009, CMP 292 761: https://arxiv.org/abs/0812.4760
- Fewster & Hollands 2005: https://arxiv.org/abs/math-ph/0412028
- Faulkner, Leigh, Parrikar & Wang 2016: https://arxiv.org/abs/1605.08072
- Graham & Olum 2005, PRD 72 025013: https://arxiv.org/abs/hep-th/0506136
- Everett & Roman 1997: https://arxiv.org/abs/gr-qc/9702049
- Bressi et al. 2002, PRL 88 041804: https://arxiv.org/abs/quant-ph/0203002
- Khamehchi et al. 2017, PRL 118 155301: https://arxiv.org/abs/1612.04055
- Fuchs et al. 2024, CQG 41 095013: https://arxiv.org/abs/2405.02709
- Le 2026 (preprint): https://arxiv.org/abs/2605.25417
- Loup, Waite & Halerewicz 2001: https://arxiv.org/abs/gr-qc/0107097
- Antimatter production (search summary): https://www.symmetrymagazine.org/article/april-2015/ten-things-you-might-not-know-about-antimatter
- URLs not recorded in the run files: Olum 1998 [D-50]; Bobrick & Martire 2021, CQG 38 105009 [D-07, U-04]; Krasnikov 1998, PRD 57 4760; Rodal 2026 [D-28].