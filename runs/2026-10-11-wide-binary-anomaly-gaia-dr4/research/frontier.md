# Research: frontier
status: final
Mandate: 2025-2026 preprints and talks on the wide-binary gravity test, newest first, each labelled with evidential status; responses to Boufourou; DR4-readiness; each camp's DR4 expectations.
Access: lit_search INSPIRE ok (arXiv-ID lookups of 2608.24556 and 2602.24035 returned NOT FOUND), arXiv ok; WebFetch domains that worked: none used; fetch_text worked on arxiv.org, zenodo.org, cosmos.esa.int

## Claims
- [RF-01] CLAIM: Boufourou (arXiv:2608.24556v1, 25 Aug 2026, single independent author, preprint, not refereed, no journal ref) reports on synthetic Newtonian catalogues that a full-median estimator, self-calibrated on the Newtonian regime with a perfect eccentricity correction, returns gamma = 1.08-1.13 for 20-30% residual triples, while a tail-truncated estimator returns gamma <= 1.04 and a mixture likelihood gamma = 1.00; an injected boost gamma = 1.4 above 2 kau is recovered at gamma >= 1.26 by all three. The generative model was validated against Pittordis et al. 2025 published statistics, not against independent data.
  SOURCE: Boufourou 2026, Estimator forensics for the wide-binary gravity test, arXiv preprint, https://arxiv.org/pdf/2608.24556
  QUOTE: "A full-median estimator self-calibrated on the Newtonian regime, even with a perfect eccentricity correction, recoversγ= 1.08–1.13from purely Newtonian universes containing 20–30% residual triples — half-way to the claimed anomaly — while a tail-truncated estimator and a mixture likelihood recoverγ≤1.04and γ= 1.00. An injected MOND-like boost (γ= 1.4above 2 kau) is recovered atγ≥1.26by all three"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high (that this is what it says); medium (that it is correct, single author, unrefereed)
- [RF-02] CLAIM: Boufourou applies his calibrated estimators to the 81,088-pair Chae (2024) sample: gamma_test = 1.045 [1.025, 1.068] (2-30 kau; f(e) systematic band 0.96-1.05); joint (gamma, f_trip) mixture fit gives gamma = 1.05 [1.04, 1.07] with f_trip = 0.15 (Pittordis et al. 2025 independent: 0.17); gamma = 1.4 rejected at Delta lnL = 129 (about 16 sigma, statistical). Deep bin (g_N < 0.3 a0) is perspective-sensitive: gamma moves from 0.97 to 1.11 +/- 0.07 after the angular correction, full bracket about [0.97, 1.19], excludes 1.35-1.40 at about 3 sigma. Reading his map backwards, a full-median analysis of the same sample with empirical-e correction would report gamma about 1.12 (global) to 1.20 (deep).
  SOURCE: Boufourou 2026, arXiv:2608.24556, https://arxiv.org/pdf/2608.24556
  QUOTE: "The full deep-bin bracket[≈0.97,1.19]is consistent with Newton and excludes 1.35–1.40 at≈3σ; the global test zone excludes it at∼16σ(statistical), with systematics bounded by the published band (Fig. 3). Reading the map of Fig. 1 backwards, a full-median analysis of this same sample with empirical-ecorrection would reportγ≈1.12(global) to1.20(deep)"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high (as reported); medium (correctness)
- [RF-03] CLAIM: Boufourou's DR4 pre-registration: expects DR4 to multiply proper-motion precision by 2-4 and usable sample by 3-5, sigma_stat(gamma) < 0.005. Protocol uses two estimators only (E2 primary, E3 secondary; the paper does not include a full-median estimator in the protocol), zones validation 0.2-2 kau, test 2-30 kau, deep bin g_N/a0 in [0.03, 0.3]; fiducial cuts RUWE < 1.4, R_chance < 0.01, sigma_vtilde < 0.10 (41,760 pairs on DR3); Newton and anomaly verdicts both require E2 and E3 to agree, otherwise a pre-declared grey zone. The paper says protocol v1.0 was frozen on 15 July 2026 (the brief says v0.95 with v1.0 promised, so the brief's note is out of date or the Zenodo record differs: check Zenodo). The protocol predicts no gamma value for DR4 itself.
  SOURCE: Boufourou 2026, arXiv:2608.24556, Sect. 6 and Sect. 2, https://arxiv.org/pdf/2608.24556
  QUOTE: "DR4 (2026) will multiply proper-motion precision by 2–4 and the usable sample by 3–5, driving σstat(γ)below 0.005: estimator systematics will fully dominate ... One version note: the frozen protocol (v1.0, 15 July 2026) quotes calibration-standard values from the pipeline state of that date"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-04] CLAIM: Chae & Yoon (arXiv:2607.14450, draft 17 July 2026, preprint, not refereed, written before Boufourou 2026 and does not respond to it) state that Gaia-DR3 wide binaries with separations beyond several kau show a MOND-type boost gamma ~ 1.3-1.6 and that proper data quality control or reasonable variation in multiple-star modelling cannot remove it; they attribute null results to (i) bypassed calibration of the multiple-star fraction on Newtonian-regime data, (ii) bias-introducing quality cuts, (iii) insufficient low-acceleration statistics. Methods: acceleration-plane test, vtilde-distribution test, median-vtilde-profile test, on 2D sky-projected velocities.
  SOURCE: Chae & Yoon 2026, Revisiting Data Quality Control and Multiple-star Modeling in Wide Binary Gravity Tests, arXiv preprint, https://arxiv.org/pdf/2607.14450
  QUOTE: "We find that studies claiming no evidence for the low-acceleration gravitational anomaly are consequences of bypassed calibration of the fraction of multiple-star systems using the Newtonian-regime data, bias- introduction in data quality control that is not taken into account in gravity tests, or insufficient statistics in the low-acceleration regime."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-05] CLAIM: Chae & Yoon specifically dispute Cookson et al. 2026: they say its "<2 sigma, no evidence for MOND" result rests on only 61 wide binaries in the MOND regime plus the Banik et al. 2024 vtilde-error cut, a biased CMD cut and incorrect masses; they claim a sample 8x larger in the MOND regime with "a correct data quality framework" gives >3 sigma confirmation. They also say the preference for Newton over a control MOND model in Pittordis et al. 2025 was significantly affected by its cuts/f_multi treatment, and that the anomaly agrees with the numerical QUMOND wide-binary orbit solution of Pflamm-Altenburg (2025). They dismiss Makarov (2026) for not modelling multiples.
  SOURCE: Chae & Yoon 2026, arXiv:2607.14450, https://arxiv.org/pdf/2607.14450
  QUOTE: "The<2σclaim of ‘no evi- dence for MOND’ by S. A. Cookson et al. (2026) was largely a consequence of low number statistics (their sample includes only 61 wide binaries in the MOND regime) along with other factors such as the I. Banik et al. (2024) biased cut, a biased CMD cut, and incor- rect masses for a large portion of the stars. A much larger sample including 8 times as many wide binaries as their sample in the MOND regime with a correct data quality framework confirms the low-acceleration gravi- tational anomaly with>3σsignificance."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-06] CLAIM: Saad & Ting (arXiv:2603.11015; v1 11 Mar 2026, v2 9 Sep 2026; published Open J. Astrophys. 9 (2026), refereed) reanalyse the 36-binary Chae et al. 2026 sample (Bayesian 3D, Chae reported gamma ~ 1.60 +0.17/-0.14 at low acceleration) with a hierarchical Bayesian model that fits an independent semi-major axis: gamma = 1.00 +0.24/-0.19. Replacing the semi-major axis by a geometric de-projection of projected separation (Chae-like) returns gamma = 1.56 +0.21/-0.18. Family: Bayesian 3D orbit fits; the spread within this family on the SAME 36 pairs is 1.00 vs 1.56 and is set by the deprojection/prior treatment, not by the data. Statistical error about +/-0.2 on 36 systems.
  SOURCE: Saad & Ting 2026, No Gravitational Anomaly in Wide Binaries from Forward Modeling of 3D Orbits, Open J. Astrophys. 9, arXiv:2603.11015, https://arxiv.org/abs/2603.11015
  QUOTE: "Our model yields $\gamma = 1.00^{+0.24}_{-0.19}$, consistent with Newtonian gravity ($\gamma = 1$). To identify the source of the discrepancy, we perform a test using an approach similar to Chae et al. (2026), replacing the semi-major axis with a geometric de-projection of the observed projected separation. This test yields $\gamma = 1.56^{+0.21}_{-0.18}$, closely matching the result of Chae et al. (2026)."
  ACCESS: full-text (arXiv abstract page)
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-07] CLAIM: Saad & Ting (arXiv:2512.19652; v1 22 Dec 2025, v3 6 Oct 2026; Open J. Astrophys. 9 (2026), refereed) measure differential RVs for 85 C3PO wide binaries (precision ~8-15 m/s per pair, ~10-100x better than Gaia DR3, median ~24x), retain 57 bound systems, and fit a hierarchical Bayesian model for the MOND scale a0 rather than gamma: for the simple interpolating function (b=1) the canonical a0 is excluded at 2.5 sigma, for the standard function (b=2) at 1.5 sigma; they flag EFE treatment in the transition regime as a systematic. This is an RV-based Bayesian 3D result, not a gamma-in-a-bin number, and uses no DR4 data.
  SOURCE: Saad & Ting 2026, High-Precision Differential Radial Velocities of C3PO Wide Binaries, Open J. Astrophys. 9, arXiv:2512.19652, https://arxiv.org/abs/2512.19652
  QUOTE: "Our results indicate tension with MOND at the presently accepted $a_0$ value: for $b=1$, the canonical value is excluded at $2.5\sigma$, while for $b=2$, the exclusion is at $1.5\sigma$."
  ACCESS: full-text (arXiv abstract page)
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-08] CLAIM: Pasquini et al. (arXiv:2602.04661, 4 Feb 2026, preprint, 4 pages + appendix): VLT-ESPRESSO archival spectra of 26 wide binaries with s > 13,000 AU. 14 of 26 discarded (12 for RV variability indicating unresolved close binaries, 1 faint Gaia companion, 1 young). Of the remaining 12, nine admit bound Newtonian orbits and three have velocity differences too large for any bound orbit; they exclude unresolved triples as the cause, with one possible exception, and suggest perturbed or unbound pairs. Implication for DR4: ~54% (12/26) of this RV-monitored wide sample hosted close companions detectable by RV; small-N and not a gamma measurement.
  SOURCE: Pasquini et al. 2026, Wide binaries without viable bound Newtonian orbits, arXiv:2602.04661, https://arxiv.org/abs/2602.04661
  QUOTE: "Fourteen of the 26 initial systems were discarded: 12 due to radial velocity variability indicating unresolved close binaries, one hosting a faint Gaia companion, and one too young. Of the remaining 12, nine can be fitted with bound orbital solution, while three show velocity differences too large to be reconciled with any bound Newtonian orbit."
  ACCESS: full-text (arXiv abstract page)
  STATUS: preprint
  CONFIDENCE: high
- [RF-09] CLAIM: Makarov (arXiv:2512.25002, 31 Dec 2025, accepted by Astron. J. per arXiv comment) uses a censored catalogue of 103,169 resolved Gaia DR3 binaries and a projected-orbital-momentum observable (total mass, a, e, inclination), and finds the anticipated MOND manifestation absent in the data. Does not model hidden multiples (per Chae & Yoon's objection). Estimator family: none of the four exactly (distribution-matching of an orbital-momentum observable); closest to full-distribution forward comparison.
  SOURCE: Makarov 2025, Distributions of wide binary stars in theory and in Gaia data: III, arXiv:2512.25002, https://arxiv.org/abs/2512.25002
  QUOTE: "The anticipated manifestation of MOND is computed in the investigated parameter space \{separation, momentum\}. This effect is absent in the given data."
  ACCESS: full-text (arXiv abstract page)
  STATUS: preprint (accepted AJ)
  CONFIDENCE: medium
- [RF-10] CLAIM: Chae & Yoon say they expect Gaia DR4 (December 2026) to give "dramatically larger samples with significantly improved data qualities" and that gravity tests on large numbers of 2D velocities remain promising; they say further refined hierarchical-system modelling than Pittordis et al. 2025 is likely to be important. They do not state a predicted gamma for DR4 nor any pre-registration. (Chae camp DR4 statement.)
  SOURCE: Chae & Yoon 2026, arXiv:2607.14450, p. 48, https://arxiv.org/pdf/2607.14450
  QUOTE: "gravity tests based on a large number of 2D velocities are also promising with the upcoming release of Gaia DR4 in December 2026, which will provide dramatically larger samples with significantly improved data qualities."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-11] CLAIM: Pittordis, Sutherland & Shepherd (arXiv:2504.07569, accepted Open J. Astrophys. 29 July 2025, refereed) say DR4 (2026) will give dramatically improved proper-motion precision, allowing the sample to expand to G ~ 18 and distance ~ 400 pc, and full-epoch astrometry will allow fitting accelerations from long-period inner orbits, but "the full power of this test will need to wait for the 10-year Gaia DR5 around 2030"; they conclude prospects for a decisive test are excellent when DR4/DR5 are combined with follow-up to detect triples. (Null camp DR4 statement, mixture-likelihood family.)
  SOURCE: Pittordis, Sutherland & Shepherd 2025, Wide Binaries from Gaia DR3: testing GR vs MOND with realistic triple modelling, Open J. Astrophys., arXiv:2504.07569, https://arxiv.org/pdf/2504.07569
  QUOTE: "the upcoming Gaia DR4 release in 2026 will provide dra- matically improved proper-motion precision, allowing ex- panding the sample to G∼ 18 and distance∼ 400 pc for improved statistics. The full-epoch astrometric data will also allow fitting for accelerations from long-period inner orbits, though the full power of this test will need to wait for the 10-year Gaia DR5 around 2030"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-12] CLAIM: Pittordis, Sutherland & Shepherd 2025 fit histograms of observed vs Newtonian velocity differences to a mixture of binary + triple populations with realistic eccentricity distributions plus unbound flyby and random-chance populations, and find Newtonian models fit significantly better than MOND, but say "improved understanding of the triple population is necessary to make this fully decisive". Family: mixture-likelihood. Independent triple fraction 0.17 (as quoted by Boufourou, RF-02).
  SOURCE: Pittordis, Sutherland & Shepherd 2025, arXiv:2504.07569, https://arxiv.org/pdf/2504.07569
  QUOTE: "We fit histograms of observed vs Newtonian velocity differences to a flexible mixture of binary + triple populations with realistic eccentricity distributions, plus unbound flyby and random-chance populations. We find as before that Newtonian models provide a significantly better fit than MOND, though improved understanding of the triple population is necessary to make this fully decisive."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-13] CLAIM: Cookson et al. (arXiv:2602.24035, MNRAS 547(2), stag342, 2026, refereed) note astrometric time series for hidden-companion acceleration searches are expected only in Gaia DR4, which will give Keplerian orbital solutions for a large binary sample, so hidden companions are currently handled by RUWE and photometric cuts that "will miss others". Their DR3 result: the scaled relative-velocity distribution of a high-purity sample within 130 pc, s = 1-30 kAU, shows no 20% MOND enhancement; a chi-square analysis finds Newton ~1500x more likely than MOND in the median vtilde vs r_sky/r_M trend; Chae & Yoon (RF-05) dispute the sample size (61 MOND-regime pairs) and cuts.
  SOURCE: Cookson et al. 2026, A Quality Framework for Testing Gravity with Wide Binaries: No Evidence for MOND, MNRAS 547, stag342, arXiv:2602.24035, https://arxiv.org/pdf/2602.24035
  QUOTE: "It is not presently possible to search for this acceleration directly because astrometric time series are expected to be available only forGaiaData Release 4 (DR4), which will provide Keplerian orbital solutions for a large sample of binaries (El-Badry et al. 2024)."  ... "A standardχ 2 analysis indicates that Newtonian dynamics is some 1500×more likely than MOND given the observed flat trend in the median~v"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-14] CLAIM: Chae et al. (arXiv:2601.21728, preprint, 2026): 36 highest-quality Gaia DR3 wide binaries with accurate 3D (HARPS/other RV) velocities, Bayesian 3D orbit fits: Gamma = log10 sqrt(gamma) = 0.102 +0.028/-0.021 for g_N < 10^-9.1 m/s^2 (0.132 +0.035/-0.027 for g_N < 10^-9.5 m/s^2), giving gamma = 1.60 +0.24/-0.14 (abstract); the paper notes the anomaly is dominated by two systems (HD 189739/HD 189760 and TYC 259-236-1/TYC 259-906-1) with 3D relative velocities exceeding estimated Newtonian escape velocities. Family: Bayesian 3D orbit fits. Saad & Ting (RF-06) reanalyse the same 36 pairs and get gamma = 1.00 +0.24/-0.19. The two systems may be the kind of unbound/perturbed pairs Pasquini et al. (RF-08) discuss.
  SOURCE: Chae et al. 2026, Detection of Gravitational Anomaly at Low Acceleration from a Highest-quality Sample of 36 Wide Binaries with Accurate 3D Velocities, arXiv:2601.21728, https://arxiv.org/pdf/2601.21728
  QUOTE: "we find Γ = 0 .102+0.028 −0.021 for < 10−9.1 m s−2 (0.132+0.035 −0.027 for < 10−9.5 m s−2) giving a gravity boost factor of γ = 1 .60+0.24 −0.14, which rules out Newton and is higher than relevant MOND predictions. This strong anomaly is dominated by two systems (the pairs of HD 189739, HD 189760, and TYC 259-236-1, TYC 259-906-1) that have 3D relative velocities exceeding their estimated Newtonian escape velocities"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-15] CLAIM: Chae et al. 2026 adopt as the MOND prediction a QUMOND numerical curve from Pflamm-Altenburg (2025), which gives a lower boost in 10^-9 > g_N > 10^-10.5 m/s^2 but a limiting gamma ~ 1.5 at lower accelerations (g_N ~ 10^-11 m/s^2), versus the simpler EFE estimate G/G_N ~ 1.4 for g_N <~ 10^-10 m/s^2 (Banik & Zhao 2018; Chae & Milgrom 2022) with external field ~1.8 a0. The MOND target for 'consistent with MOND' therefore differs between the camps (1.4 vs up to 1.5; Chae also finds gamma 1.6 'higher than relevant MOND predictions').
  SOURCE: Chae et al. 2026, arXiv:2601.21728, p. 3-4, https://arxiv.org/pdf/2601.21728
  QUOTE: "the external field due to the Galaxy is ≈ 1.8a0, which is so strong in the context of MOND that the gravity boost factor is expected to be about G/GN ≈ 1.4 for a test particle ... Complete numerical solutions for a two-body dynamics under an external field (due to a third body) find a lower boost ... factor in the range 10−9 ≳ gN ≳ 10−10.5 m s−2 but a similar boost factor at lower accelerations with a some- what larger limiting value of γ ≈ 1.5."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RF-16] CLAIM: Boufourou's Zenodo record (concept DOI 10.5281/zenodo.22073430) has two public versions as of 2026-10-11: v1.0 (24 Aug 2026, doi:10.5281/zenodo.22073431) and v2.0 (26 Aug 2026, doi:10.5281/zenodo.22114321, adds a threshold scan T in [1.2, 1.8] and an MNRAS-format manuscript, submitted to MNRAS as MN-26-2659-P). In both, the deposited protocol file is "draft v0.95"; the frozen protocol "v1.0 of 2026-07-15" is described as to be released "before 2026-12-02" and was NOT yet a public deposit in the versions list I could see. The arXiv text calls the protocol "frozen (v1.0, 15 July 2026)" but the Zenodo package contains v0.95 only, so a public time-stamp of the frozen protocol does not yet exist. Zenodo lists only E1/E2/E3 estimators (E1 = full median, per the 'three estimator families').
  SOURCE: Zenodo records 22073431 and 22114321 (HBoufourou/paperI-wide-binaries), https://zenodo.org/records/22073431 and https://zenodo.org/api/records/22073431/versions
  QUOTE: "protocole/ : protocole pré-enregistré Gaia DR4 (draft v0.95). ... Le protocole gelé (v1.0) fera l'objet d'une release ultérieure avant le 2026-12-02." (v1.0 record) ; "protocole/ : protocole pré-enregistré Gaia DR4 (draft v0.95 ; version gelée v1.0 du 2026-07-15, release avant le 2026-12-02)" (v2.0 record)
  ACCESS: full-text
  STATUS: preprint (software deposit, not refereed)
  CONFIDENCE: high
- [RF-17] CLAIM: Gaia DR4 timing per ESA: the Gaia ESA Archive goes down on Wednesday 25 November 2026 12:00 CET and re-opens on Wednesday 2 December 2026 12:00 CET with DR4 (ESA Gaia news item dated 2026-10-08). Search-summary: DR4 is the first principal release since DR3, covers 5.5 years, delivers full-mission epoch astrometry/photometry/spectroscopy, and non-single-star orbit catalogues including multi-body models; a DR4 pre-release in June 2026 contained astrometric time series for 12 sources including three non-single stars with previously published Gaia Keplerian orbits. Acceleration-solution specifics not confirmed in this search.
  SOURCE: ESA Gaia news 2026, https://www.cosmos.esa.int/web/gaia/news-2026 ; DR4 prerelease page https://www.cosmos.esa.int/en/web/gaia/dr4-prerelease
  QUOTE: "In preparation of Gaia DR4, the ​​​​​​​Gaia ESA Archive will be down as of Wednesday 25 November 2026 12:00 CET. The archive will re-open on Wednesday 2 December 2026 at 12:00 CET, featuring the new Gaia DR4 release."
  ACCESS: full-text (date); search-summary (DR4 content statements)
  STATUS: institutional
  CONFIDENCE: high (date); medium (content)
- [RF-18] CLAIM: Pflamm-Altenburg (A&A 703, A68, 2025; arXiv:2509.01493, refereed) solves the complete two-body QUMOND problem numerically: in the non-linear transition regime the effective one-body treatment (total mass 2 Msun) gives acceleration up to a factor 1.44 above Newtonian, whereas the full two-body solution gives only a factor 1.2-1.3 for the simple transition function. This lowers the MOND target below the Banik & Zhao value in the transition regime; Chae et al. 2026 adopt this curve. (Whether it includes the Galactic EFE is not stated in the abstract: verify.)
  SOURCE: Pflamm-Altenburg 2025, Numerical solutions of the complete two-body system in QUMOND, A&A 703, A68, https://arxiv.org/abs/2509.01493
  QUOTE: "In the non-linear transition regime the kinematical acceleration of the effective one-body system with a total mass of 2 Msun is up to a factor of 1.44 higher than the Newtonian acceleration, whereas the acceleration is only boosted by a factor of 1.2--1.3 in the two-body system in the case of the simple transition function."
  ACCESS: full-text (arXiv abstract page)
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-19] CLAIM: Yoon, Tian & Chae (ApJ 992, 102, 2025; arXiv:2507.13177, refereed; Chae-camp, Gaia DR3, includes perspective effects, extended to 50 kau) report gamma_g = g_obs/g_N = 1.61 +0.37/-0.29 at g_N = 10^-11.0 m/s^2, 1.26 +0.12/-0.10 at g_N = 10^-10.3 m/s^2, and 1.32 +0.12/-0.11 for all binaries with g_N <~ 10^-10 m/s^2. Note gamma_g here is defined as g_obs/g_N (log10 gamma_g / sqrt2 = delta), a different convention from Chae's Gamma = log10 sqrt(gamma): check conversion before scoring. This is the most recent Chae-camp 2D vp result with a g_N < 10^-10 bin and full errors.
  SOURCE: Yoon, Tian & Chae 2025, Probing the nature of gravity in the low-acceleration limit, ApJ 992, 102, arXiv:2507.13177, https://arxiv.org/abs/2507.13177
  QUOTE: "At Newtonian accelerations $g_{\mathrm N} = 10^{-10.3}$ m\,s$^{-2}$, we find $\gamma_g=1.26^{+0.12}_{-0.10}$ ($\delta_{\rm obs-newt}=0.072\pm0.027$). For all binaries with $g_{\rm N}\lesssim10^{-10}$ m\,$s^{-2}$ from our sample, we find $\gamma_g=1.32^{+0.12}_{-0.11}$ ($\delta_{\rm obs-newt}=0.085\pm0.027$)."
  ACCESS: full-text (arXiv abstract page)
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-20] CLAIM: Estimator-family mapping evidence for Cookson et al. 2026 (refereed): the headline statistic is a chi-square on the binned MEDIAN vtilde against separation (Newtonian normalisation fitted freely, 5 d.o.f. for 6 bins), after a hard cut vtilde < 2.5 (justified as the largest vtilde any MOND/TeVeS/emergent-gravity case needs). It is therefore a tail-truncated, median-based estimator, not the mixture likelihood the brief suggests; the mixture-likelihood family on DR3 is then represented by Pittordis et al. 2025 (RF-12) and Banik et al. 2024 (not re-read here). The family mapping affects the DR4 scoring rule.
  SOURCE: Cookson et al. 2026, MNRAS 547, stag342, arXiv:2602.24035, https://arxiv.org/pdf/2602.24035
  QUOTE: "we would not lose any non-Newtonian signal by imposing a cut of~v <2.5." ... "we freely vary the median~vin the Newtonian limit (the Newtonian normalization) to get the best overall fit. This means that although we have 6 binned data points, theχ2 values in Table 3 correspondtoonly5degreesoffreedom."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium (mapping is my inference from the method text)
- [RF-21] CLAIM: Cookson et al. conclude that "apparent MOND signals diminish as methodological rigour improves" (meta-analysis) and constrain gravity modifications between a0/10 and 200 a0, with Newton up to 1500x more likely than MOND for the cleanest sample; they state the wide-binary test is based on sky-projected velocities "and will remain so for the foreseeable future". Banik-camp DR4 statement: hidden-companion acceleration searches become possible with DR4 time series, no gamma prediction for DR4.
  SOURCE: Cookson et al. 2026, arXiv:2602.24035, https://arxiv.org/pdf/2602.24035
  QUOTE: "Across this range of internal accelerations, Newtonian gravity is up to1500×more likely than MOND for our cleanest sample."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-22] CLAIM: Hernandez & Kroupa (MNRAS 537, 2925, 2025; arXiv:2410.17178 v2 31 Jan 2025, refereed) reanalyse Cookson (2024) after correcting the assumed mean total mass (2.0 vs 1.56 Msun) and find the velocity-separation slope inconsistent with Newton at 3.3 sigma. This is a reply to Cookson (2024), pre-dating Cookson et al. 2026; the Hernandez camp has posted no DR4 statement that I could find. It illustrates the mass-estimate sensitivity: a 2.0 vs 1.56 Msun mass choice flips the verdict on the same binned data.
  SOURCE: Hernandez & Kroupa 2025, A recent confirmation of the wide binary gravitational anomaly, MNRAS 537, 2925, arXiv:2410.17178, https://arxiv.org/abs/2410.17178
  QUOTE: "the data presented there actually show a clear anomaly in the low acceleration gravitational regime, with the overall slope of the velocity-separation scaling being inconsistent with Newtonian expectations at a 3.3$\sigma$ level."
  ACCESS: full-text (arXiv abstract page)
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RF-23] CLAIM: A Zenodo preprint by J. Pedinielli (4 June 2026, 'Binary Emergent Gravity applied to wide binary stars', not on arXiv, not refereed) predicts a constant boost gamma_g ~ 1.077 at ALL separations (including g_N > a0) and says the discriminating test (Gamma at g_N > 10 a0 with sigma_Gamma < 0.005) needs ~600 pairs with 3D velocities accessible to Gaia DR4. It is the only explicit numerical DR4-era prediction of a gamma I found other than the MOND ~1.4-1.5 and the Newtonian 1.0; it would not be scored in the low-acceleration bin as distinct from Newton at the Boufourou-like 1.05 level.
  SOURCE: Pedinielli 2026, Binary Emergent Gravity Applied to Wide Binary Stars: Predictions for Gaia DR3/DR4 and the Gravitational Boost, Zenodo, https://zenodo.org/records/20544019
  QUOTE: "BEG predicts a gravitational boost γ _g = G_eff/G_N ≈ 1.077, constant across all separations — a signature qualitatively distinct from MOND ... The discriminating test — Γ at g_N > 10 a₀ with σ _ Γ < 0.005 — requires ~600 pairs with 3D velocities, accessible to Gaia DR4."
  ACCESS: full-text
  STATUS: fringe
  CONFIDENCE: high (that it says this); low (physics)
- [RF-24] CLAIM: Responses to Boufourou: none found. INSPIRE does not index arXiv:2608.24556 (NOT FOUND), arXiv search returns no citing paper, and the Zenodo record shows 57 views / 25 downloads (v1.0) as of 2026-10-11. It is submitted to MNRAS (MN-26-2659-P). Chae & Yoon (written 17 July 2026) pre-date it, so no Chae-camp reply exists; Saad & Ting v2 (9 Sep 2026) and v3 of the C3PO paper (6 Oct 2026) do not cite it in the abstract.
  SOURCE: INSPIRE refersto query (NOT FOUND), arXiv search, Zenodo record 22073431/22114321
  SUMMARY: "INSPIRE has no record for arxiv:2608.24556"; Zenodo v2.0 description: "soumis à MNRAS, manuscript MN-26-2659-P"
  ACCESS: full-text (Zenodo metadata); search-summary (absence of citations, search-based)
  STATUS: preprint
  CONFIDENCE: medium
- [RF-25] CLAIM: DR4 statements by each camp: (a) Chae & Yoon: tests "promising" with larger samples (RF-10), no gamma forecast, no pre-registration. (b) Pittordis et al. / Banik-Cookson camp: DR4 allows G ~ 18 and ~400 pc, acceleration fits for long-period inner orbits, full power at DR5 ~2030 (RF-11, RF-13). (c) Boufourou: sigma_stat(gamma) < 0.005, systematics dominate, pre-registered E2/E3 protocol (RF-03). (d) Saad & Ting: no DR4 mention in the two 2026 papers (grep 'DR4' no match in arXiv:2603.11015). Neither main camp has stated an expected DR4 gamma; the only pre-committed DR4 test with decision criteria is Boufourou's.
  SOURCE: as cited in RF-03, RF-10, RF-11, RF-13; fetch_text grep of 2603.11015 and 2601.21728 for 'DR4' returned NO MATCH
  QUOTE: "NO MATCH for 'DR4'. Try fewer or different words." (fetch_text.py on arXiv:2603.11015 and arXiv:2601.21728)
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium
## Gaps
- No talks/slides (EAS, AAS, MOND workshops, Gaia DR4 science meetings) with new wide-binary results were found by WebSearch; none confirmed as preliminary. 
- No published response or independent replication of Boufourou's estimator-forensics result (RF-24); no reanalysis by Banik, Chae or Hernandez of the 81,088-pair sample at his estimators.
- Banik et al. 2024 (MNRAS 527, 4573), Chae 2023/2024 and Chae 2025 (ApJ 985, 210) were not re-read here (owned by quantitative); only newer papers were covered.
- Boufourou's frozen v1.0 protocol (15 July 2026) is not publicly deposited as of 2026-10-11 (RF-16); Zenodo contains draft v0.95 only. Re-check before 2026-11-25.
- Whether Pflamm-Altenburg 2025 includes the Galactic EFE in the full two-body solution and the exact bin values (theory facet) not checked beyond the abstract.
- ESA DR4 content page (acceleration solutions, epoch RVs) text not extracted: only the date and a search-summary of content (RF-17).
- PAPER TO REQUEST: none strictly required; Boufourou's frozen protocol v1.0 (not yet public) would settle which estimator families and bin the pre-registered test scores.
