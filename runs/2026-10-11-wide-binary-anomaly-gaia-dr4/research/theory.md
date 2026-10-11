# Research: theory
status: final
Mandate: Governing theory for wide-binary gravity tests: Newtonian ṽ distribution (eccentricity, projection, time-averaged separation), inner-binary effects, MOND with Galactic EFE (Banik & Zhao 2018), AQUAL vs QUMOND, interpolating functions, γ(g_N) parametrisation.
Access: lit_search INSPIRE ok, arXiv ok (some queries returned 0 for multi-name queries), Semantic Scholar rate-limited once; fetch_text.py on arxiv.org PDFs worked; no WebSearch needed

## Claims
- [RT-01] CLAIM: Banik & Zhao 2018 (MNRAS 480, 2660; arXiv:1805.12273) advance wide binaries in QUMOND, treating each as a point mass M plus test particle in a uniform Galactic external field g_ext. QUMOND computes the true field from the Newtonian field g_N via ∇·g = ∇·[ν(|g_N|/a0) g_N]; g_N includes the external Newtonian field g_N,ext (what the EF would be without MOND), so the EFE enters through g_N = -GM r̂/r² + g_N,ext. The simple interpolating function is ν(y) = 1/2 + sqrt(1/4 + 1/y).
  SOURCE: Banik & Zhao 2018, Testing gravity with wide binary stars like alpha Centauri, MNRAS 480, 2660 (arXiv preprint v9), https://arxiv.org/pdf/1805.12273
  QUOTE: "We begin by describing how we advance WB systems using the quasilinear formulation of MOND (QUMOND, Milgrom 2010). Each system is treated as a single point mass M plus a test particle embedded in a uniform EF gext. QUMOND uses the Newtonian gravitational field gN to determine the true gravitational field g by first finding its divergence."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-02] CLAIM: In the EF-dominated limit (separation well beyond the MOND radius, g_N,ext >> self-gravity), the QUMOND radial force on a wide-binary component is g_r = g_N,r ν_ext (1 + K0 sin²θ /2), with θ the angle between the separation and the external field, K0 = (y/ν) dν/dy at the external field. The boost is maximal for θ = 0 or π and minimal at θ = π/2, so it is anisotropic; the angle-averaged boost of Newtonian gravity is η = ν_ext (1 + K0/3). (Force boost; the velocity boost is roughly sqrt of this.)
  SOURCE: Banik & Zhao 2018, MNRAS 480, 2660, eqs 14-16, https://arxiv.org/pdf/1805.12273
  QUOTE: "In very widely separated systems, the total acceleration is dominated by the EF rather than self-gravity g. In this limit, we can obtain gr analytically (Banik & Zhao 2018a, equation 37). gr = gN,r νext (1 + K0/2 sin²θ) (15) Substituting this into Equation 14 yields η = νext (1 + K0/3) (16)" [equation typesetting garbled by PDF extraction; wording above is as printed apart from equation layout]
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-03] CLAIM: Banik & Zhao 2018 Table 3 (EF-dominated limit, Solar neighbourhood) gives the expected MOND boost to gravity (force, angle-averaged) for three interpolating functions: standard (Kent 1987) ν_ext = 1.1462, η = 1.0726 (QUMOND) / 1.0661 (AQUAL); simple (Famaey & Binney 2005) ν_ext = 1.5602, η = 1.4228 (QUMOND) / 1.4056 (AQUAL); MLS (McGaugh et al. 2016 eq 4) ν_ext = 1.5081, η = 1.3692 / 1.3508. Different functions require different g_N,ext to match the same true g_ext from the LSR motion. So for the simple function the asymptotic gravity boost is γ ≈ 1.41-1.42 (velocity boost ≈ 19-20%), for MLS ≈ 1.35-1.37, for the standard function only ≈ 1.07.
  SOURCE: Banik & Zhao 2018, Table 3, https://arxiv.org/pdf/1805.12273
  QUOTE: "Interpolating νext η in QUMOND η in AQUALfunction Standard 1.1462 1.0726 1.0661 Simple 1.5602 1.4228 1.4056 MLS 1.5081 1.3692 1.3508 Table 3. The expected MOND boost to gravity in the Solar neighbourhood for the standard (Kent 1987, section 6) and simple (Famaey & Binney 2005) interpolating functions as well as the one labelled..."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-04] CLAIM: AQUAL and QUMOND relate g and g_N in opposite directions in spherical symmetry (x μ(x) = y for AQUAL; y ν(y) = x for QUMOND, x = g/a0, y = g_N/a0). In the EF-dominated regime both give the same maximum boost, but the angle-averaged AQUAL boost differs slightly (1/η = tan^-1(√L0)/(μ_ext √L0)); AQUAL boost is maximised at θ = 0 or π as in QUMOND. The AQUAL-QUMOND difference for the simple function is ~1.2% in η (1.4056 vs 1.4228).
  SOURCE: Banik & Zhao 2018, section 7.2, https://arxiv.org/pdf/1805.12273
  QUOTE: "In spherical symmetry, AQUAL and QUMOND take opposite approaches to relate g and gN. xµ(x) = y (AQUAL) yν(y) = x (QUMOND) x ≡ g/a0 and y ≡ gN/a0 (31)"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-05] CLAIM: The MOND radius for a 1 Msun system is only ~7 kAU (r_M = sqrt(GM/a0)); the boost from MOND saturates at separations beyond ~r_M because the EF then dominates (r_M ≈ 11 kAU for 2.4 Msun). Hence beyond ~10-20 kAU the boost does not grow, and the expected velocity excess is ~20% for the simple function.
  SOURCE: Banik & Zhao 2018, https://arxiv.org/pdf/1805.12273
  QUOTE: "In fact, the MOND radius rM is only 7000 astronomical units (7 kAU) for a system with M = M⊙." ; "the MOND boost to gravity does not increase much for systems more widely separated than their MOND radius (Equation 1). As this is only 11 kAU for the heaviest systems we consider (2.4M⊙)"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-06] CLAIM: Chae 2023 (ApJ 952, 128) models wide binaries with g_N < ~1e-9 m/s² and ≥ ~5 kau as "pseudo-Newtonian" with G -> G' under the Galactic EF. Using g_ext ≈ 2.26e-10 m/s² (≈1.9 a0, a0 = 1.2e-10 m/s²; g0 = V²/R0 ≈ 2.14e-10 m/s² from V = 232.8 km/s, R0 = 8.20 kpc, plus vertical g0/3) he takes G' ≈ 1.37 G from Chae & Milgrom (2022) AQUAL numerical solutions for circular orbits. Reported: g_obs/g_pred = 1.43 ± 0.06 at g_N = 10^-10.15 m/s². The AQUAL treatment uses circular orbits only ("AQUAL numerical solutions for general elliptical orbits are not available").
  SOURCE: Chae 2023, Breakdown of the Newton-Einstein standard gravity at low acceleration in internal dynamics of wide binary stars, ApJ 952, 128, https://arxiv.org/pdf/2305.04613
  QUOTE: "Assuming a vertical gravity of g0/3, the total external acceleration is estimated to be gext ≈ 2.26×10−10 m s−2 or gext ≈ 1.9a0 for the MOND critical acceleration a0 = 1.2×10−10 m s−2. For this external field, we estimate G′ ≈ 1.37G using the Chae & Milgrom (2022) numerical solutions of AQUAL."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-07] CLAIM: Chae 2023 states the Newtonian-vs-pseudo-Newtonian logic: when the internal acceleration is in the deep-MOND regime but the system is in a significant external field, MOND "dynamics becomes pseudo-Newtonian with Newton's gravitational constant modified: G -> G'", for separations > ~5 kau. Chae explicitly says the goal is a generic trend, not a rigorous test of a specific model, and that the AQUAL comparison uses circular-orbit boost.
  SOURCE: Chae 2023, ApJ 952, 128, https://arxiv.org/pdf/2305.04613
  QUOTE: "modified gravity theories (Bekenstein & Milgrom 1984; Milgrom 2010) of MOND predict that dynamics becomes pseudo-Newtonian with Newton's gravitational constant modified: G → G′. This is the situation for wide binaries separated more than ≈ 5 kau"; "our present goal is not to rigorously test a specific model of modified gravity but a generic trend."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-08] CLAIM: Hwang, Ting & Zakamska (2022; arXiv:2111.01789, MNRAS 512, 3383 per arXiv/DOI 10.1093/mnras/stac675) infer eccentricity from the Gaia EDR3 v-r angle for ~1e6 wide binaries, fitting f(e) ∝ e^α. Result: roughly uniform (α≈0) at ~1e2 au, thermal (α=1) at ~10^2.7 au, superthermal (α>1) at > 1e3 au. A thermal distribution f(e)=2e corresponds to an isotropic phase-space distribution depending only on energy, and gives a flat observed v-r angle distribution. Eccentricities e<0.3 suppressed and e>0.9 enhanced at wide separations.
  SOURCE: Hwang, Ting & Zakamska 2022, The eccentricity distribution of wide binaries and their individual measurements, arXiv:2111.01789 (published MNRAS, doi:10.1093/mnras/stac675)
  QUOTE: "Our results show that the eccentricity distribution of wide binaries at 10 2 AU is close to uniform and becomes superthermal at > 103 AU, suggesting two formation mechanisms dominating at different separation regimes." ; "Therefore, Fig. 6 shows that the eccentricity distribution evolves from uniform to thermal, and then super thermal with increasing binary separations."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-09] CLAIM: Chae's parametrised AQUAL boost (the "γ_g(g_N)" used in Chae 2024b, ApJ 972, 186) is the Chae & Milgrom (2022) fitting function for circular-orbit AQUAL under an external field: g/g_N = ν(y_β) [1 + (tanh(β g_N,ext/g_N))^γ ν̂(y_β)/3], with y_β = sqrt((g_N/a0)² + (β g_N,ext/a0)²), ν̂ = dlnν/dlny, simple ν (Famaey & Binney 2005), β = 1.1, γ = 1.2 (for external-field inclination 60° to orbital axis), Newtonian external field from x²/(1+x) = g_N,ext/a0 with x = g_ext/a0 = 1.90 ± 0.19, a0 = 1.2e-10 m/s². It is applied as G_eff = γ_g(g_N) G with g_N ≈ a0 (1.2 s/r_M)^-2, and ṽ ≈ sqrt(g/g_N) at r ≈ 1.2 s. This becomes Newtonian as s/r_M -> 0 and pseudo-Newtonian with G_eff ≈ 1.37 G for s/r_M ≳ 1; the transition 0.1 ≲ s/r_M ≲ 0.7 is "less accurate and should be taken with a grain of salt". (This is the Chae-camp function for γ(g_N); it uses circular orbits and an averaged inclination, not elliptical-orbit AQUAL.)
  SOURCE: Chae 2024, Measurements of the low-acceleration gravitational anomaly from the normalized velocity profile of Gaia wide binary stars, ApJ 972, 186 (arXiv:2402.05720), https://arxiv.org/pdf/2402.05720
  QUOTE: "The effective Newton's constant depends on s/rM through Geff = γg(gN)G with gN ≈ a0(1.2s/rM)−2 (see Equation (23)), where the function γg(gN) represents the right-hand side of Equation (22). This model becomes Newtonian as s/rM → 0 and pseudo-Newtonian with Geff = 1.37 for s/rM ≳ 1. In the transition range 0.1 ≲ s/rM ≲ 0.7, this model is less accurate and should be taken with a grain of salt."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-10] CLAIM: Chae & Milgrom (2022) AQUAL solutions are for circular orbits of a test particle; Chae notes that "numerical solutions for the elliptical motions of binaries under the external field of the Milky Way are not available", so the elliptical-orbit MOND prediction in the Chae camp is a pseudo-Newtonian (G -> G_eff) Kepler approximation. The same approximation is the brief's labelled "Keplerian with G_eff = γ(g_N) G".
  SOURCE: Chae 2024, ApJ 972, 186, https://arxiv.org/pdf/2402.05720
  QUOTE: "For the AQUAL model, numerical solutions for the elliptical motions of binaries under the external field of the Milky Way are not available at present."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-11] CLAIM: Definition of the normalized velocity used by Chae 2024b (and Banik & Zhao 2018, Pittordis & Sutherland 2018): ṽ = v_p / v_c(s), with v_p the observed sky-projected relative velocity, v_c(s) = sqrt(G M_tot / s) the Newtonian circular velocity at the sky-projected separation s, and M_tot the total mass including any hidden companion(s). v_p = 4.7404e-3 km/s × Δμ[mas/yr]... × d[pc] (Δμ in mas/yr, d in pc). Chae also states that the fitted f_multi depends on the selection, with an intrinsic degeneracy between f_multi and the inferred gravity, so Newtonian-regime binaries are needed to fix f_multi.
  SOURCE: Chae 2024, ApJ 972, 186, https://arxiv.org/pdf/2402.05720
  QUOTE: "the normalized velocity on the sky plane is defined (Pittordis & Sutherland 2018; Banik & Zhao 2018) by ṽ ≡ vp/vc(s), (1) where vp is the observed sky-projected relative velocity between the pair and vc(s) is the theoretical Newtonian circular velocity at the sky-projected separation s." ; "The value of fmulti depends on the selection criteria used to select binaries, and there is an intrinsic degeneracy between fmulti and the inferred gravity."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-12] CLAIM: Banik et al. 2024 (MNRAS 527, 4573; arXiv:2311.03436) parametrise the gravity law with α_grav: the Newtonian simulated (r_sky, ṽ) distribution is transformed into the Milgromian one and the transformation coefficients are interpolated, so α_grav = 0 is Newton, α_grav = 1 is their MOND (QUMOND, simple function, EFE) template, α_grav < 0 means sub-Newtonian normalisation, α_grav > 1 means above-MOND; allowed range (-2, 3.6). The MOND velocity excess at asymptotically large separation is ≈20% (their abstract) i.e. γ_MOND ≈ η ≈ 1.4 in force. They fit WBs with orbit eccentricity exponent (their "γ", f(e) ∝ e^γ_e) free and a 1.5-dex Öpik-law population of unresolved close binaries (CBs); inferred γ_e ≈ 2, more superthermal than Hwang et al. 2022 (1.32 ± 0.09 for that exponent), which they attribute partly to undetected CBs flattening the v-r angle distribution towards uniform (hence thermal).
  SOURCE: Banik et al. 2024, Strong constraints on the gravitational law from Gaia DR3 wide binaries, MNRAS 527, 4573, https://arxiv.org/pdf/2311.03436
  QUOTE: "we allow α grav to lie in the range (−2,3.6). Negative values imply that the gravity in the asymptotic regime has a lower than Newtonian normalization, while α grav > 1 implies a normalization higher than expected in MOND. To set up a parametrized gravity law, we obtain the simulated (r sky, ṽ) distribution in both gravity theories for each (M,a,γ), with different orbital eccentricities marginalized over for the adopted γ using the eccentricity distribution it defines"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-13] CLAIM: Banik et al. 2024 state that the gravity law is mostly sensitive to the main-peak region of the ṽ distribution, so the extended tail at ṽ ≳ 2 (which carries CB/LOS contamination) need not be modelled very accurately, and that eccentricity-distribution differences matter less to the overall ṽ distribution than Newton vs MOND (BZ18 fig. 3). They also compute the median ṽ for a grid of Keplerian orbits, all orbital phases and viewing angles, as a function of the eccentricity exponent; the Newtonian median depends on the assumed eccentricity distribution, and "agreement with MOND is possible at very high γ" (very superthermal), but they argue a rapidly rising γ_e(a) trend is implausible. They also report a Newton-vs-MOND preference of 19σ.
  SOURCE: Banik et al. 2024, MNRAS 527, 4573, https://arxiv.org/pdf/2311.03436
  QUOTE: "An important reason for the similar results is that the gravity law is mostly sensitive to the main peak region of the ev distribution, so it is not necessary to have a very accurate model for the extended tail at ev ≳ 2." ; "The median of the resulting ev distribution depends on the assumed γ, as shown by the solid red line on Figure 15. ... While agreement with MOND is possible at very high γ, we must bear ..." [ev here = ṽ; their γ is the eccentricity exponent, not G_eff/G]
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-14] CLAIM: The empirical "fat tail" of the ṽ distribution of Gaia wide-binary candidates at ṽ ≈ 1.5-6 (in units of the circular velocity) cannot be bound Newtonian pure binaries (ṽ ≤ √2); at ṽ ≳ 2.5 the systems are too fast to be explained by modified gravity without overshooting galaxy rotation curves. The proposed explanation (Clarke 2020) is higher-order multiples: one component an unresolved close binary, or a third star at resolvable separation too faint for Gaia, whose closer orbit boosts the apparent velocity difference of the wide pair. Pittordis & Sutherland fitted binary + triple + flyby populations; GR preferred over MOND if their crude triple model is right.
  SOURCE: Manchanda, Sutherland & Pittordis 2023, Wide binaries as a modified gravity test: prospects for detecting triple-system contamination, arXiv:2210.07781
  QUOTE: "the main obstacle at present is the observed “fat tail” of candidate wide-binary systems with velocity differences at ∼ 1.5 − 6× circular velocity; this tail population cannot be bound pure binary systems, but a possible explanation of the tail is triple or quadruple systems with unresolved or undetected additional star(s)."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RT-15] CLAIM: Milgrom's QUMOND (MNRAS 403, 886, 2010): the MOND potential φ solves a Poisson equation with modified source density ρ* = -(1/4πG) ∇·g, g = ν(|g_N|/a0) g_N, g_N the Newtonian field of ρ. Bekenstein & Milgrom 1984 (ApJ 286, 7) is the AQUAL nonrelativistic Lagrangian theory with a modified Poisson equation. Milgrom 1983 (ApJ 270, 365/371/384) is the original MOND and predicted the external-field effect (the strong equivalence principle fails; Chae 2023 cites Milgrom 1983a for the EFE).
  SOURCE: Milgrom 2010, Quasi-linear formulation of MOND, MNRAS 403, 886 (arXiv:0911.5464); Bekenstein & Milgrom 1984, ApJ 286, 7
  QUOTE: "A new formulation of MOND as a modified-potential theory of gravity is propounded. In effect, the theory dictates that the MOND potential phi produced by a mass distribution rho is a solution of the Poisson equation for the modified source density rho*=-(1/4 pi G)divergence(g), where g=nu(|gN|/a0)gN, and gN is the Newtonian acceleration field of rho."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-16] CLAIM: Hwang, Ting & Zakamska 2022 Table 1 (Gaia EDR3, d<200 pc, power-law f(e) ∝ e^α by true separation): α = 0.08 (+0.15/-0.13) at 1.5-2.0 log au (N=686); 0.59 (+0.09/-0.10) at 2.0-2.25; 0.82 (+0.05/-0.04) at 2.25-2.5; 0.94 (+0.04/-0.04) at 2.5-2.75; 1.20 (+0.05/-0.05) at 2.75-3.0 (N=14884); 1.30 (+0.05/-0.06) at 3.0-3.5 (N=18496); 1.32 (+0.09/-0.08) at 3.5-4.0 (N=7570); 1.17 (+0.14/-0.15) at 4.0-4.5 (N=2301). The authors' own test says α=1.3 at >10^3.5 au "may be slightly overestimated from a true value of ∼1.2" because of the proper-motion S/N criterion. So the brief's "α ≈ 1.2-1.3 at 1-10 kau" is confirmed; at the MOND-relevant 3-30 kau it is ≈1.2-1.3 (superthermal), not thermal. Banik et al. 2024 argue undetected close binaries bias this toward thermal and prefer an even more superthermal exponent (≈2 in their parametrisation).
  SOURCE: Hwang, Ting & Zakamska 2022, arXiv:2111.01789 (MNRAS 512, 3383; doi:10.1093/mnras/stac675)
  QUOTE: "Separation (log AU) Number of binaries α [2.75, 3.00] 14884 1.20+0.05−0.05 [3.00, 3.50] 18496 1.30+0.05−0.06 [3.50, 4.00] 7570 1.32+0.09−0.08 [4.00, 4.50] 2301 1.17+0.14−0.15" ; "At > 103.5 AU, the measured α = 1.3 may be slightly overestimated from a true value of ∼ 1.2"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-17] CLAIM: Newtonian ṽ distribution, my own Monte Carlo (Kepler orbits, random mean anomaly, isotropic orientation, selection in a narrow projected-separation bin s0 ± 10% for a population dN/da ∝ a^-1.6; ṽ = v_p/sqrt(GM/s)). Checks: <r>/a = 1+e²/2 reproduced (e=0.7: 1.2436 numeric vs 1.2450; e=0.95: 1.4507 vs 1.4512); <sin θ> = 0.7846 vs π/4 = 0.7854; max ṽ = 1.4019 (thermal), 1.4114 (α=4) vs bound √2 = 1.4142 (ṽ² = v_p² s/GM <= v² r/GM... <= 2 for bound orbits since v² <= 2GM/r and s <= r). Median ṽ (Newton, no noise, no contamination): circular 0.6925; e=0.5 0.6159; uniform 0.5896; thermal 0.5269; α=1.3 0.5134; α=2 0.4880; α=4 0.4486. P(ṽ>1) ≈ 4.7% for thermal.
  SOURCE: [calc: runs/2026-10-11-wide-binary-anomaly-gaia-dr4/calc/theory_newton_mond.py]
  QUOTE: "max v~ (thermal) = 1.4019  (bound: sqrt2 = 1.4142)" ; "f(e)=thermal   N_sel= 201014 median v~=0.5269  frac(v~>1)=0.047" (script log)
  ACCESS: full-text
  STATUS: preliminary
  CONFIDENCE: medium
- [RT-18] CLAIM: Sensitivity of a median-ṽ estimator to the assumed eccentricity distribution (premise 5), from the same Monte Carlo: if the template assumes thermal but the truth is α=1.3, the equivalent spurious γ = (median ratio)² = 0.950; truth uniform vs thermal template 1.252; truth e=0.5 1.366; truth circular 1.727; truth α=2 0.858; α=4 0.725. Against an α=1.3 template: truth thermal gives 1.053, truth uniform 1.319. So an eccentricity mismatch of Δα≈0.3 near the Hwang value moves a median-based γ by ≈5%; a gross mismatch (uniform vs superthermal) by ≈25-30%, and the sign is: assuming too few eccentric orbits (too circular a template) lowers the Newtonian median and so makes γ biased LOW; assuming too eccentric a template biases γ HIGH. The effect is scale-free (identical in every s bin) unless f(e) itself changes with s; an anomaly-like rise in γ with decreasing g_N therefore requires a separation-dependent eccentricity or contamination mismatch, not a constant offset. (Caveat: unit conventions here: median ṽ, no noise/contamination; the effect on tail-truncated and mixture estimators differs.)
  SOURCE: [calc: runs/2026-10-11-wide-binary-anomaly-gaia-dr4/calc/theory_newton_mond.py]
  QUOTE: "equivalent gamma if a thermal template is used for truth f(e)=alpha1.3: (med/med_thermal)^2 = 0.950" ; "... truth f(e)=uniform: (med/med_thermal)^2 = 1.252" (script log)
  ACCESS: full-text
  STATUS: preliminary
  CONFIDENCE: medium
- [RT-19] CLAIM: Reproduction of Banik & Zhao 2018 Table 3 from the formula η = ν_ext(1+K0/3): with g_ext = 1.785 a0 (2.14e-10 m/s² for a0 = 1.2e-10 m/s²), simple function gives ν_ext = 1.5602, K0 = -0.2642, η = 1.4228; standard function gives ν_ext = 1.1462, η = 1.0725 (table: 1.0726). K0 < 0, so in the EF-dominated regime the radial boost ranges from ν_ext (separation parallel to g_ext) to ν_ext(1+K0/2) (perpendicular): 1.560 to 1.354 for the simple function (force), i.e. ṽ boost 1.249 to 1.164 (velocity), versus the angle-average η = 1.4228. The EFE boost is thus anisotropic by ≈15% in force at fixed separation for the simple function, and scalar "γ in a bin" is the angle/orbit-average.
  SOURCE: [calc: runs/2026-10-11-wide-binary-anomaly-gaia-dr4/calc/theory_newton_mond.py], compared with Banik & Zhao 2018 Table 3
  QUOTE: "simple: x=g_ext/a0=1.785 (g_ext=2.142e-10 m/s^2 for a0=1.2e-10) y_ext=1.1441 nu_ext=1.5602 K0=-0.2642 eta=1.4228" ; "standard: ... nu_ext=1.1462 K0=-0.1928 eta=1.0725" (script log)
  ACCESS: full-text
  STATUS: preliminary
  CONFIDENCE: high
- [RT-20] CLAIM: γ_MOND(g_N) with the Chae 2024 (eq 22) circular-orbit AQUAL fit, simple ν, g_ext/a0 = 1.90 [values for 1.71 and 2.09 in brackets, i.e. ±10%]: log10 g_N [m/s²] = -8.0: 1.012 [1.012, 1.012]; -9.0: 1.103 [1.104, 1.102]; -9.5: 1.236 [1.245, 1.226]; -10.0: 1.333 [1.366, 1.305]; -10.15: 1.346 [1.382, 1.315]; -10.5: 1.362 [1.403, 1.328]; -11.0: 1.367 [1.410, 1.331]. Deep limit ≈ 1.37 (matches Chae's G_eff = 1.37G); BZ18 EF-dominated angle-average for the same simple function is 1.4228 (QUMOND) or 1.4056 (AQUAL), MLS 1.37/1.35, standard 1.07. So a "MOND value" in the scoring bin (g_N range wholly below 10^-9.5 m/s² containing 10^-10) is ≈ 1.33 (Chae function at the bin centre log g_N = -10.0), and the asymptote is 1.35-1.42 for simple/MLS functions; ≈1.07 if the standard function were the true one. Note γ(10^-9.5) = 1.24 is only just below the P(γ>1.25) threshold.
  SOURCE: [calc: runs/2026-10-11-wide-binary-anomaly-gaia-dr4/calc/theory_newton_mond.py]; formula from Chae 2024, ApJ 972, 186 eq 22
  QUOTE: "log10 g_N=-10.00: gamma_g=1.333  (g_ext/a0=1.90) | 1.71: 1.366 | 2.09: 1.305" ; "log10 g_N= -9.50: gamma_g=1.236  (g_ext/a0=1.90) | 1.71: 1.245 | 2.09: 1.226" (script log)
  ACCESS: full-text
  STATUS: preliminary
  CONFIDENCE: medium
- [RT-21] CLAIM: Mapping g_N to separation (my calc, G M_tot/r², r = true 3D separation): for M_tot = 1.5 Msun, g_N = 10^-9.5 m/s² corresponds to r = 5,304 au and g_N = 1e-10 m/s² to r = 9,432 au (Chae's s ≈ r/1.2 gives s = 4,420 and 7,860 au); for 1.0 Msun, r = 4,331 and 7,702 au; for 2.0 Msun, 6,125 and 10,892 au. MOND radius r_M = sqrt(GM/a0) = 7,031 au (1 Msun), 8,611 au (1.5), 9,943 au (2.0) for a0 = 1.2e-10 m/s². Hence the scoring bin "wholly below 10^-9.5 and containing 10^-10 m/s²" corresponds to s ≳ 4-5 kau and r up to the 20-30 kau sample limit (g_N ~ 1e-11 m/s² at r ≈ 30 kau).
  SOURCE: [calc: runs/2026-10-11-wide-binary-anomaly-gaia-dr4/calc/theory_newton_mond.py]
  QUOTE: "M=1.5 Msun, log g_N=-9.5: r=5,304 au, s=r/1.2=4,420 au; r_M=sqrt(GM/a0)=8,611 au" ; "M=1.5 Msun, log g_N=-10.0: r=9,432 au, s=r/1.2=7,860 au" (script log)
  ACCESS: full-text
  STATUS: preliminary
  CONFIDENCE: high
- [RT-22] CLAIM: Inner-binary (hidden companion) velocity scale (my calc, M_wide = 1.5 Msun, inner pair 0.8 Msun with q = 0.5, luminosity ratio ∝ q^4 for illustration): the reflex orbital speed of the observed star about the inner centre of mass is 8.9 km/s at a_in = 1 au (P = 1.1 yr), 2.8 km/s at 10 au (P = 35 yr), 0.89 km/s at 100 au, 0.51 km/s at 300 au, compared with the wide-orbit v_c(s) = 0.666 km/s at s = 3,000 au and 0.365 km/s at 10,000 au. The photocentre factor |q/(1+q) - ℓ/(1+ℓ)| ≈ 0.27 reduces this to ≈ 0.27 of the relative orbital speed. So even a=100-300 au inner binaries (P > 1000 yr, undetectable by RUWE/RVs) contribute a velocity perturbation of order 0.6-2 v_c(s) at 3-10 kau, i.e. comparable to the wide orbit itself, and move systems into the ṽ>1 tail. Crude MC (thermal wide orbits, inner a_in log-uniform 3-300 au, instantaneous velocity, NO Gaia averaging so an upper bound): median ṽ rises by (med/med0)² = 1.145, 1.338, 1.612 at f_triple = 0.1, 0.2, 0.3, with 7%, 14%, 21% of pairs at ṽ > √2. The Gaia astrometric window (34 months in DR3) averages out inner motion only for P ≲ baseline, and hierarchical-stability limits and detection by RUWE were not modelled.
  SOURCE: [calc: runs/2026-10-11-wide-binary-anomaly-gaia-dr4/calc/theory_newton_mond.py]
  QUOTE: "a_in=   100 au P= 1118.03 yr: reflex v_A=  0.888 km/s =   1.33 v_c(s); photocentre factor 0.27 ->   1.10 v_c(s)" ; "f_triple=0.2: median v~=0.6107; (med/med0)^2 = 1.338; frac(v~>1.5)=0.135" (script log)
  ACCESS: full-text
  STATUS: preliminary
  CONFIDENCE: low
- [RT-23] CLAIM: Clarke (2019/2020, MNRAS Lett.; arXiv:1910.10256) argued that the high-velocity tail of apparently unbound Gaia DR2 wide binaries, which could be read as non-Newtonian gravity, is explicable by hidden triples (one component itself an unresolved binary).
  SOURCE: Clarke, The distribution of relative proper motions of wide binaries in GAIA DR2: MOND or multiplicity?, arXiv:1910.10256 (doi:10.1093/mnrasl/slz161)
  QUOTE: "We argue that this tail is instead explicable in terms of a population of hidden triples, i.e. cases where one of t"  [abstract as truncated by lit_search]
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium
- [RT-24] CLAIM: Belokurov et al. 2020 (MNRAS; arXiv:2003.05467): for stars with unresolved companions the centre of light and the centre of mass move differently, so a single-source astrometric model fits poorly; RUWE can be converted into the amplitude of the image-centroid wobble. This is the observable that links photocentre wobble to the RUWE flag used as a binarity cut by wide-binary analyses (instrument facts left to the engineering facet).
  SOURCE: Belokurov et al. 2020, Unresolved stellar companions with Gaia DR2 astrometry, arXiv:2003.05467 (doi:10.1093/mnras/staa1522)
  QUOTE: "For stars with unresolved companions, motions of the centre of light and that of mass decouple, causing a single-source astrometric model to perform poorly. We show that such stars can be easily detected with the reduced chi2 statistic, or RUWE, provided as part of Gaia DR2. We convert RUWE into the amplitude of the image centroid wobble"
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-25] CLAIM: Boufourou (2026 preprint, arXiv:2608.24556) reports that in his DR3 re-measurement of the Chae 2024 sample the choice of eccentricity template alone moves the tail-truncated estimator's γ over a band [0.957, 1.068]: empirical per-zone f(e) gives 1.045, thermal 0.958, superthermal 0.957. Theory cross-check: in my Monte Carlo (RT-18) a thermal-vs-superthermal (α=1.3) template mismatch moves a pure median by only ≈ 5% in the sense superthermal truth <-> thermal template gives γ 0.95; his thermal and superthermal results being almost equal (0.958 vs 0.957) is not the pattern expected from a pure-median estimator, but his estimator is tail-truncated, not a pure median, so no inconsistency is claimed here (flag for the mechanist/critiques).
  SOURCE: Boufourou 2026, Estimator forensics for the wide-binary gravity test, arXiv:2608.24556, https://arxiv.org/pdf/2608.24556
  QUOTE: "f(e)systematic band {empirical 1.045; thermal 0.958; superthermal 0.957} — the empirical-eccentricity correction alone pushes the es-"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium
## Gaps
- No published AQUAL or QUMOND N-body solution for ELLIPTICAL wide-binary orbits in the Galactic EF was found; Chae (RT-10) says none exists, and the "G_eff = γ(g_N) G Kepler" model used by the Chae camp and by the brief's calculator is therefore an approximation, as is any scalar γ(g_N) (EFE boost is anisotropic by ~15% in force at fixed separation for the simple function, RT-19). Banik & Zhao 2018 do run QUMOND orbits with inclination marginalisation, but their Table 3 values are EF-dominated asymptotes only.
- The ṽ ≤ √2 bound (RT-17) was checked numerically and by the energy argument but not located as a stated theorem in a paper; the brief states it too.
- Analytic closed-form ṽ distribution for circular orbits was not sourced; my Monte Carlo gives numbers only (RT-17, RT-18). Two quantities the mechanist should recompute: the s-bin weighting assumption dN/da ∝ a^-1.6 and its effect on the Newtonian median.
- Not covered in this facet by mandate: measured values (quantitative), multiple fractions (Moe & Di Stefano; quantitative), Gaia astrometric error model and DR4 content (engineering).
- Pittordis & Sutherland 2018/2023 EFE formulation was not opened (only cited through Banik & Zhao Fig. 1 caption); Chae & Milgrom 2022 (the AQUAL circular-orbit fit) was read only via Chae 2024's quotation of it; Milgrom 1983/1986 and Bekenstein & Milgrom 1984 were seen only as Crossref/INSPIRE listings and abstracts.
- No source found that gives the γ(g_N) for interpolating functions other than simple/standard/MLS in the EF-dominated limit (e.g. the n=2 family); constraints facet computes extra functions.
- PAPER TO REQUEST: none essential (all key papers are open on arXiv).
