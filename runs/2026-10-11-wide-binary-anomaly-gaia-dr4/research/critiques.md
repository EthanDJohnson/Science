# Research: critiques
status: final
Mandate: estimator and systematics critiques on both sides of the wide-binary gravity test, with replies and re-analyses.
Access: lit_search INSPIRE ok (no record for arXiv ids 2603.11015, 2608.24556), arXiv partly ok (one HTTP 400); fetch_text on arxiv.org pdf/abs ok; WebFetch not used

## Claims
- [RC-01] CLAIM: Chae & Yoon (arXiv:2607.14450, 16 July 2026, preprint, no journal ref) attribute all "no anomaly" results (Banik et al. 2024, Pittordis et al. 2025, Cookson et al. 2026, Makarov 2026) to three causes: bypassed calibration of the multiple-star fraction on Newtonian-regime data, bias introduced by data-quality cuts, and insufficient low-acceleration statistics. They claim >5 sigma confirmation of the anomaly after applying ruwe<1.2 to three samples (Chae 2023, Banik 2024, Pittordis 2025) and calibrating f_trip at high acceleration.
  SOURCE: Chae & Yoon 2026, "Revisiting Data Quality Control and Multiple-star Modeling in Wide Binary Gravity Tests", arXiv:2607.14450, https://arxiv.org/pdf/2607.14450
  QUOTE: "We find that studies claiming no evidence for the low-acceleration gravitational anomaly are consequences of bypassed calibration of the fraction of multiple-star systems using the Newtonian-regime data, bias- introduction in data quality control that is not taken into account in gravity tests, or insufficient statistics in the low-acceleration regime."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RC-02] CLAIM: Chae & Yoon say the Pittordis et al. (2025) sample (PSS), after their own re-calibration with ruwe<1.2, needs only f_trip = 0.10 +- 0.03 (Chae 2023 sample with ruwe<1.2: 13602 binaries, 69% of the sample; excluded 31% has far more hierarchical systems); this is a large drop from f_multi = 0.43 +- 0.05 for the no-ruwe-cut sample (Chae 2024b). They state Pittordis et al.'s preference for Newton over a control MOND model was "significantly affected" by lack of Newtonian-regime triple-fraction calibration. This is Chae's side of the conflict; it is a preprint claim of the party whose result is being criticised.
  SOURCE: Chae & Yoon 2026, arXiv:2607.14450, https://arxiv.org/pdf/2607.14450
  QUOTE: "The fitted value of f trip = 0.10 +- 0.03 with the limit ruwe <1.2 is dramatically reduced from f multi = 0.43 +- 0.05 (see Appendix A of K.-H. Chae (2024b)) for the sample without the ruwe cut" [fetch_text printed "0.10±0.03" and "0.43±0.05"]
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium
- [RC-03] CLAIM: Chae & Yoon criticise Cookson et al. (2026): their "<2 sigma" no-evidence-for-MOND claim is called "largely a consequence of low number statistics" (61 wide binaries in the MOND regime) plus the Banik et al. 2024 "biased" v~-error cut, a "biased" CMD cut, and "incorrect masses for a large portion of the stars". They say a sample with 8 times as many MOND-regime binaries confirms the anomaly at >3 sigma. They also say Banik et al.'s sample (r_p>2 kau only) cannot calibrate on Newtonian-regime pairs and has a higher fraction of unbound pairs.
  SOURCE: Chae & Yoon 2026, arXiv:2607.14450, https://arxiv.org/pdf/2607.14450
  QUOTE: "The <2 sigma claim of 'no evidence for MOND' by S. A. Cookson et al. (2026) was largely a consequence of low number statistics (their sample includes only 61 wide binaries in the MOND regime) along with other factors such as the I. Banik et al. (2024) biased cut, a biased CMD cut, and incorrect masses for a large portion of the stars."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RC-04] CLAIM: Saad & Ting (OJAp 9, 2026; arXiv:2603.11015) reanalyse the same 36-binary Chae et al. 2026 dataset with a hierarchical Bayesian forward model fitting 3D orbital elements and a global gamma: they get gamma = 1.00 +0.24 -0.19 versus Chae et al.'s gamma ~ 1.60 +0.17 -0.14, and say the inferred anomaly depends on the modelling framework (orbital parameterisation).
  SOURCE: Saad, Ting et al. 2026, "No Gravitational Anomaly in Wide Binaries from Forward Modeling of 3D Orbits", Open J. Astrophys. 9, arXiv:2603.11015 (v2), https://arxiv.org/pdf/2603.11015
  QUOTE: "Our model yields gamma = 1.00 +0.24 -0.19, consistent with Newtonian gravity (gamma = 1)." / "The fact that Chae et al. (2026) infers gamma >1 from overlapping data underscores that the inferred anomaly depends on the modeling framework, consistent with the sensitivity to orbital parameteriza- tion that we identify in this work." [the two Greek letters are rendered as 'γ' in the source; ASCII here]
  ACCESS: full-text
  STATUS: peer-reviewed (Open Journal of Astrophysics per INSPIRE/arXiv listing)
  CONFIDENCE: high
- [RC-05] CLAIM: Boufourou (arXiv:2608.24556, single author, preprint) claims a full-median estimator self-calibrated on the Newtonian regime, even with a perfect eccentricity correction, returns gamma = 1.08-1.13 from purely Newtonian synthetic universes with 20-30% residual triples, while tail-truncated and mixture-likelihood estimators return gamma <= 1.04 (truncated) and mixture ~1; all three recover >= 1.26 on injected MOND-EFE truth (gamma = 1.4 above 2 kau). Single-seed grid, jitter ~ +-0.02. Not independently reproduced as of this file; no peer review.
  SOURCE: Boufourou 2026, "Estimator forensics for the wide-binary gravity test...", arXiv:2608.24556v1, https://arxiv.org/pdf/2608.24556
  QUOTE: "A full-median estimator self-calibrated on the Newtonian regime, even with a perfect eccentricity correction, recovers gamma = 1.08-1.13 from purely Newtonian universes containing 20-30% residual triples -- half-way to the claimed anomaly" [Greek letter rendered ASCII] ; and "On MOND truth all three recover >=1.26. Single-seed grid; statistical jitter ~ +-0.02."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RC-06] CLAIM: Saad & Ting locate the Newtonian-vs-MOND flip on the 36-pair sample in the deprojection model: replacing a free semi-major-axis parameter (broken power-law prior, break at 5 kau, slope -1.6 above, Hwang et al. 2022 s-dependent eccentricity) by a geometric deprojection of the observed projected separation (the Chae et al. approach) moves gamma from 1.00 [0.81, 1.24] (P(gamma<1)=0.50) to 1.56 [1.38, 1.77] (P(gamma<1)=0.00) on the same data. Sampler (NUTS vs emcee), hierarchical vs per-system pooling, and treating r_perp as exact are shown to be subdominant. A caveat on the critique itself: the result is prior-dependent in both directions; the independent-a model builds in a population prior on a that Chae would call an assumption.
  SOURCE: Saad & Ting 2026, arXiv:2603.11015, https://arxiv.org/pdf/2603.11015
  QUOTE: "This test yields gamma = 1.56 +0.21 -0.18, closely matching the result of Chae et al. (2026). This shows that if the three- dimensional orbital separation is forward modelled using an independent semi-major axis parameter and then projected into the space of the observables, the relative velocities of wide binaries are consistent with Newtonian gravity." ; table: "Broken power-law prior 1.00 [0.81, 1.24] 0.50 / Geometric r true 1.56 [1.38, 1.77] 0.00" ; "The dominant source of the discrepancy between our baseline result and Chae et al. (2026) is the semi-major axis parameterization, not the handling of r_perp."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RC-07] CLAIM: Boufourou's own real-data mixture fit does not return exactly gamma=1: gamma = 1.05 [1.04, 1.07] with f_trip = 0.15 (cf. Pittordis et al. 2025 f_trip = 0.17), and Delta lnL(gamma=1) = 4.8 (about 3.1 sigma, statistical), against Delta lnL = 129 (about 16 sigma) for gamma = 1.4, on 41,760 pairs (RUWE<1.4, R_chance<0.01, sigma_vtilde<0.10); the full eccentricity-model systematic band is [0.957, 1.068]. The deep bin (g_N/a0 in [0.03, 0.3]) is perspective-sensitive: gamma moves from 0.97 to 1.11 +- 0.07 after the angular correction, full bracket ~[0.97, 1.19], excluding 1.35-1.40 only at about 3 sigma. The 16 sigma is statistical only and relies on a single-author generative model.
  SOURCE: Boufourou 2026, arXiv:2608.24556v1, https://arxiv.org/pdf/2608.24556
  QUOTE: "the mixture likelihood on the real test zone gives gamma = 1.05 [1.04,1.07] with ftrip = 0.15, in striking external agreement with the independent PS25 value of 0.17; gamma = 1.4 is rejected at Delta lnL = 129 (~16 sigma, statistical)... Delta lnL(gamma = 1) = 4.8 (~3.1 sigma, statistical) lies within that same..." ; "The full deep-bin bracket [~0.97,1.19] is consistent with Newton and excludes 1.35-1.40 at ~3 sigma"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RC-08] CLAIM: Boufourou self-declares three caveats: (i) per-pair eccentricities of Chae (2024) are prior-dependent and define the upper edge of his systematic band; (ii) the deep bin couples perspective correction, RV availability and small numbers; (iii) his triple model has a 10-14% P90 excess of the high-v tail over Pittordis et al. 2025, so the quoted +0.08-0.13 full-median bias is an "upper edge" and would shrink by roughly that fraction if the PS25 tail were matched. He also states: "we have not audited individual published pipelines" (i.e. the claim that Chae's pipeline contains this bias is inferred from a synthetic map, not demonstrated on Chae's code).
  SOURCE: Boufourou 2026, arXiv:2608.24556v1, https://arxiv.org/pdf/2608.24556
  QUOTE: "we have not audited individual published pipelines, and the injection-recovery framework is the neutral ground on which any implementation can be tested." ; "the 10-14% P90 excess of our triple model implies the quoted +0.08-0.13 is an upper edge; matching the PS25 tail exactly would shrink it by roughly that fraction"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RC-09] CLAIM: Cookson, Banik, El-Badry et al. (MNRAS 547, stag342, 2026; arXiv:2602.24035) criticise Chae 2023/2024 on four named grounds: (a) no v~ quality cut, so wide-binary samples with large v~ uncertainty inflate the median v~ in the MOND-regime bins; Banik et al. 2024 (their sec. 5.3) showed that a v~-uncertainty cut removing just 20% of pairs "completely eliminates" the apparent rising trend in median v~ with r_sky/r_M in the Chae 2023 setup; (b) no spherical (perspective) projection correction (Chae 2024c eq. 6), which they say matters when crossing the MOND radius and can fake a MOND signal; (c) inadequate removal of flybys and historical encounters (Banik et al. 2024 fig. 11: modest contamination can skew the result); (d) no HRD/CMD cut against unresolved close companions. Their own result is the "No Evidence for MOND" of the title. They list Chae 2023/2024a/c as scoring 8-11 on their quality checklist against 14 for Banik et al. 2024 and 10 for Cookson 2024 (checklist is the authors' own, so partly self-referential).
  SOURCE: Cookson et al. 2026, "A Quality Framework for Testing Gravity with Wide Binaries: No Evidence for MOND", MNRAS 547, stag342, arXiv:2602.24035, https://arxiv.org/pdf/2602.24035
  QUOTE: "the most important being the lack of any ~v quality cut." ; "those authors showed that an appropriate cut on the ~v uncertainty that removes just 20% of the WBs completely eliminates the apparent rising trend in median ~v with respect to r sky/r M." ; "The most compelling and most recent such study (Chae 2024c) overlooks spherical projection and does not include an HRD cut, casting doubt on its preference for MOND." [whitespace restored where the PDF extraction dropped spaces; wording unchanged]
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RC-10] CLAIM: Chae & Yoon reply on perspective and cuts: the perspective effect "is overall very minor and matters only at the last bin of 0.3<log10(rp/rM)<0.6 (15 <~ r_p <~ 30 kau)"; an RV subsample with perspective correction gives results "very similar" to the uncorrected one; the anomaly is already clear at 7 <~ r_p <~ 15 kau; the ipd_frac_multi_peak = 0 requirement also has negligible effect, "contrary to the concerns raised by S. A. Cookson et al. (2026)". Independent data point on the same question: Boufourou finds the angular correction moves the deepest bin (g_N/a0 in [0.03, 0.3]) from gamma = 0.97 to 1.11 +- 0.07 in his pipeline, i.e. the correction raises rather than lowers gamma there, in the opposite direction to the Cookson concern.
  SOURCE: Chae & Yoon 2026, arXiv:2607.14450, https://arxiv.org/pdf/2607.14450; Boufourou 2026, arXiv:2608.24556
  QUOTE: "the correction of the perspective effect or the requirement of ipd frac multi peak = 0 has negligible effects on the low-acceleration gravita- tional anomaly, contrary to the concerns raised by S. A. Cookson et al. (2026)."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium
- [RC-11] CLAIM: Pasquini et al. (arXiv:2602.04661, 4+3 pages, preprint) with VLT-ESPRESSO spectra of 26 wide binaries at projected separation >13,000 AU: 14 of the 26 were discarded (12 for RV variability indicating unresolved close companions, 1 with a faint Gaia companion, 1 too young); of the remaining 12, 9 fit a bound Newtonian orbit and 3 have velocity differences too large for any bound orbit. They conclude such pairs may be disrupted/unbound and that "utmost caution must be applied when studying wide binaries as isolated systems". Scope: 26 pairs from an archival ESPRESSO selection, not a random or complete wide-binary sample; 12/26 = 46% hidden-close-companion rate is an upper-end evidence point against a low f_multi at large separation, but selection of the archive is unknown.
  SOURCE: Pasquini, Saglia, Patat et al. 2026, "Wide binaries without viable bound Newtonian orbits", arXiv:2602.04661, https://arxiv.org/pdf/2602.04661
  QUOTE: "Of the 26 initial systems, 14 were discarded: 12 due to radial-velocity variability indicating unresolved close binaries, 1 that hosts a faint Gaia companion, and 1 that is too young. Of the remaining 12, 9 can be fitted with a bound orbital solution, while the velocity differences of the other 3 are..."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RC-12] CLAIM: Hernandez, Chae & Aguayo-Ortiz (arXiv:2312.03162, "A critical review of recent GAIA wide binary gravity tests", preprint v3; MNRAS status not checked) critique Pittordis & Sutherland 2023 and Banik et al. 2024 on three grounds: (a) they use only a narrow low-acceleration range (s2D > 5 kau in PS23, > 2 kau in B24) and exclude the Newtonian regime, so the hidden-tertiary fraction f_multi cannot be calibrated: with an excessive f_multi = 0.65 the Newtonian-regime medians of v~ come out "clearly lower than the Newtonian predictions" (chi^2_nu = 7.5 for the Newtonian model in their numerical experiment), whereas re-adjusting to f_multi ~ 0.4 makes AQUAL fit and rules Newton out; "working with excessively large hidden binary fractions will necessarily result in reduced effective gravity inferences"; (b) B24 bins v~ in narrow 0.08-wide bins although more than half of its pairs have sigma_v~ between 0.04 and 0.1, and the sigma_v~ play "no role in the gravity inference procedure" other than the sample cut (e.g. 37.5% chance of wrong bin for a pair with sigma_v~ = 0.04); (c) B24 uses a "higher than present f_multi" (65.7% hidden tertiaries in their fig. 10). The numerical experiment is the authors' own (Chae is a co-author), so it carries the same calibration premise it tests.
  SOURCE: Hernandez, Chae & Aguayo-Ortiz 2023, "A critical review of recent GAIA wide binary gravity tests", arXiv:2312.03162, https://arxiv.org/pdf/2312.03162
  QUOTE: "With f multi = 0. 65, at high accelerations, the Newtonian data is now inconsi stent with the Newtonian prediction as a consequence of the artiﬁcially high value of f multi." ; "As we have shown explicitly, working within ex- cessively large hidden binary fractions will necessarily r esult in reduced eﬀective gravity inferences."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
- [RC-13] CLAIM: Banik et al. (MNRAS 527, 4573, 2024; arXiv:2311.03436) criticise Chae 2023 directly: Chae infers 3D separation and relative velocity from projected data "instead of modelling into the space of the observables", neglects the systemic RV and sets v_sky = d * mu_rel (no spherical-projection correction), and the nominal sample's mass-dependent eccentricity cutoff may matter (Appendix E). They also note that Chae & Milgrom 2022's eq. 15 for the AQUAL EFE boost "has the wrong asymptotic limit" when the EFE dominates, and show that the QUMOND and AQUAL boosts are almost identical for r <~ 0.5 r_M, so the test is "not sensitive to which formulation" is used. These are claims by the criticised parties' main opponent; Chae & Yoon's reply is in RC-01/RC-03/RC-10.
  SOURCE: Banik, Pittordis, Sutherland et al. 2024, "Strong constraints on the gravitational law from Gaia DR3 wide binaries", MNRAS 527, 4573, arXiv:2311.03436, https://arxiv.org/pdf/2311.03436
  QUOTE: "The WB analysis of Chae (2023) uses the WB sample of El-Badry et al. (2021), but it attempts to infer the 3D separation and relative velocity from the available projected information instead of modelling into the space of the ob- servables." ; "We see that when r <~ 0.5 r M , the AQUAL and QUMOND results are almost identical. Therefore, results for the WBT are not sensitive to which formulatio..." [truncated by the extraction]
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RC-14] CLAIM: Hernandez (MNRAS 2025, 537, 2925; arXiv:2410.17178) re-analysis of Cookson (2024): says Cookson's Newtonian comparison curve used a mean total binary mass of 2.0 Msun while the data's mean is 1.56 Msun, and after correcting this the same published binned 1D RMS data are inconsistent with Newton at 3.3 sigma in slope. A direct example of a mass-normalisation error flipping a verdict (mass-scale sensitivity, gamma scales as 1/M).
  SOURCE: Hernandez et al. 2025, "A recent confirmation of the wide binary gravitational anomaly", MNRAS 537, 2925, arXiv:2410.17178, https://arxiv.org/pdf/2410.17178
  QUOTE: "the Newtonian predictions used refer to wide binaries with mean total ma sses of 2.0 Msun. This is larger than the 1.56 Msun value which applies to the data used in said paper." ; "with the overall slope of the velocity-separation scaling being inconsistent with Newtonian expec tations at a 3.3 sigma level."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RC-15] CLAIM: Makarov (AJ 171, 79, 2026; arXiv:2512.25002) uses a different observable (projected orbital momentum) on 103,169 resolved Gaia DR3 binaries and reports no MOND manifestation above ~7 kau. Chae & Yoon dismiss it without analysis because it "does not take into account multiples". It is therefore an unmatched null on the same catalogue, not rebutted on substance.
  SOURCE: Makarov 2025/2026, "Distributions of wide binary stars in theory and in Gaia data: III. Orbital momenta, masses, and manifestations of MOND", arXiv:2512.25002, https://arxiv.org/pdf/2512.25002
  QUOTE: "The anticipated manifestation of MOND is computed in the investigated parameter space {separation, momentum}. This effect is absent in the given data." ; "there is no evidence of any excessive momenta for orbital separations above ~7 KAU where the MOND effects are expected to be manifest for solar-type binaries."
  ACCESS: full-text
  STATUS: preprint (published AJ 171, 79 per Boufourou's reference list; not independently checked)
  CONFIDENCE: medium

- [RC-16] CLAIM: Banik et al. 2024 headline numbers (the target of the Hernandez/Chae/Chae-Yoon critiques): alpha_grav = -0.021 +0.065 -0.045 (MCMC; 0 = Newton, 1 = their MOND template), MOND excluded at 16 sigma, Newton preferred over MOND at 19 sigma in the direct best-model comparison, 8611 wide binaries within 250 pc, s = 2-30 kau. Their fitted undetected-close-binary fraction is f_CB = 69.9% (Newton) / 65.7% (MOND), i.e. much higher than the f_trip ~ 0.10-0.17 used by Chae & Yoon / Pittordis-Shepherd (differently defined populations: f_CB counts any close companion, not only those that perturb the velocity; the two numbers are not directly comparable). The paper itself states its test needs a "Newtonian anchor" but its sample has r_p > 2 kau and relies on the predicted MOND effects differing at low and high r_sky.
  SOURCE: Banik et al. 2024, MNRAS 527, 4573, arXiv:2311.03436, https://arxiv.org/abs/2311.03436 and https://arxiv.org/pdf/2311.03436 (Table 2)
  QUOTE: "Directly comparing the best Newtonian and Milgromian models reveals that Newtonian dynamics is preferred at 19 sigma confidence. Using a complementary Markov Chain Monte Carlo analysis, we find that alpha_grav = -0.021 +0.065 -0.045, which is fully consistent with Newtonian gravity but excludes MOND at 16 sigma confidence." [abstract; Greek letters rendered ASCII]
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RC-17] CLAIM: Pittordis, Sutherland & Shepherd (2025, Open J. Astrophys.; arXiv:2504.07569) themselves weaken their own verdict: Newtonian models fit "significantly better" than MOND, "though improved understanding of the triple population is necessary to make this fully decisive"; they name triples as "perhaps the dominant source of uncertainty" in the contradictory published results, and cite Manchanda et al. (2023) that ~85-95% of unseen triples can be flagged by follow-up including future Gaia (non-single-star) data. Their f_trip = 0.17 (cited by Boufourou) vs 0.185 used by Chae & Yoon as a fixed value.
  SOURCE: Pittordis, Sutherland & Shepherd 2025, arXiv:2504.07569v2, https://arxiv.org/pdf/2504.07569
  QUOTE: "We find as before that Newtonian models provide a significantly better fit than MOND, though improved understanding of the triple population is necessary to make this fully decisive." ; "with the triple systems perhaps the dominant source of uncer- tainty."
  ACCESS: full-text
  STATUS: peer-reviewed (accepted by OJAp 2025 July 29)
  CONFIDENCE: high
- [RC-18] CLAIM: Saad & Ting's C3PO differential-RV sample (arXiv:2512.19652, OJAp 9, 2026): 57 bound wide binaries with 3D orbits, gamma = 1.17 +0.37 -0.23 for the 18 systems above 3000 AU projected separation and 1.05 +0.11 -0.08 for the 39 below, both consistent with gamma = 1; the authors say the sample is mostly in the MOND transition regime so it is "less informative" than their direct a0 inference. They estimate a hidden-triple contamination ceiling of <~ 5% consistent with the velocity-separation trend and argue triples bias velocities upward, opposite to the MOND sign. Contrast with Pasquini (RC-11) where 46% of the ESPRESSO sample is RV-variable; the two samples are selected differently (chemically-matched co-natal pairs vs archival ESPRESSO pairs).
  SOURCE: Saad & Ting 2026, arXiv:2512.19652v3, https://arxiv.org/pdf/2512.19652
  QUOTE: "we also inferred an effective gravity boost factor gamma for the C3PO systems that are bound in three dimensions, split at a projected separation of 3000 AU, finding gamma = 1.17 +0.37 -0.23 for the 18 systems above and 1.05 +0.11 -0.08 for the 39 below, both consistent with Newtonian gravity (gamma = 1)." [Greek letter rendered ASCII]
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RC-19] CLAIM: Estimator-dependence is now documented within a single camp's data: the same 36-binary sample gives gamma 1.00 [0.81,1.24] or 1.56 [1.38,1.77] depending only on the semi-major-axis/deprojection parameterisation (RC-06), and Boufourou's synthetic map shows a full-median estimator moving by +0.08-0.13 on Newtonian truth (RC-05, upper edge per RC-08). Both of these are single-comparison results; the first (Saad & Ting) is peer-reviewed, the second (Boufourou) is an unreplicated preprint. Neither shows that Chae's actual pipeline is biased by that amount; Chae & Yoon (written before Boufourou) say their approach calibrates f_trip on Newtonian-regime data, which is the correction Boufourou also applies ("self-calibrated on the Newtonian regime"), so Boufourou's residual bias comes from the triple tail shape, not from skipping calibration.
  SOURCE: derived from RC-05, RC-06, RC-08, RC-01
  SUMMARY: "Synthesis of the cited papers; no new number."
  ACCESS: search-summary
  STATUS: secondary
  CONFIDENCE: medium

## Gaps
- No reply by Chae (or Hernandez) to Saad & Ting 2026 (arXiv:2603.11015) or to Boufourou (arXiv:2608.24556) was found; INSPIRE listed no citing papers for either (INSPIRE has no record of either id; refersto returned NOT FOUND). Chae & Yoon (July 2026) predates Boufourou and does not discuss Saad & Ting's semi-major-axis result (grep for Saad returned nothing in Chae et al. 2026). Left to the frontier facet to monitor.
- No published independent reproduction of Boufourou's injection-recovery map was found; the run's mechanist owns this.
- Clarke / Loeb perspective-effect papers: a targeted search returned nothing relevant; the perspective critique is documented here only through Cookson et al. 2026, Chae & Yoon 2026 and El-Badry (2019)/Shaya & Olling (2011) as cited by them. Not read directly.
- Pflamm-Altenburg (2025) realistic QUMOND wide-binary orbits (cited by Chae & Yoon as agreeing with the data): not found in INSPIRE/arXiv search; not read. Theory facet's territory.
- Chae & Yoon's three-point claim on "insufficient statistics" and Cookson's 61 MOND-regime pairs: the sigma values in Cookson were not extracted (the PDF text lost spaces). Quantitative facet should supply them.
- Banik et al. 2024 sec. 5.3 (their rebuttal of Chae 2023's median trend) quoted via Cookson's summary of it (RC-09), not from Banik's own text.
- PAPER TO REQUEST: none; all cited papers had free arXiv copies.
