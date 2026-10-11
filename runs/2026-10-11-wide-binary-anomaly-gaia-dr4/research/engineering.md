# Research: engineering
status: final
Mandate: Gaia DR3 astrometric/RV/RUWE facts, El-Badry+2021 catalogue construction, each group's cuts and N, what DR4 adds (baseline, precision, epoch data, NSS/acceleration), DR4 wide-binary counts, Boufourou's pre-registered DR4 protocol.
Access: lit_search INSPIRE ok (often returns nothing for multi-word queries), arXiv ok; fetch_text worked for cosmos.esa.int, arxiv.org PDFs, zenodo.org (records and API); github.com returned 403; WebFetch worked for cosmos.esa.int.

## Claims
- [RE-01] CLAIM: Gaia DR4 is released 2 December 2026 and is based on 66 months of data (25 July 2014 to 20 January 2020, the complete nominal mission), against 34 months for DR3.
  SOURCE: ESA Gaia, "Gaia DR4 content" page and "Gaia release" page, https://www.cosmos.esa.int/web/gaia/dr4 ; https://www.cosmos.esa.int/web/gaia/release
  QUOTE: "Gaia DR4 data is based on data collected between 25 July 2014 (10:30 UTC) and 20 January 2020 (22:00 UTC) spanning a period of 66 months of data collection that includes the complete nominal mission. As a comparison, Gaia DR3 was based on 34 months of data" ; release page: "Gaia DR4 (based on 66 months of data) 2 December 2026"
  ACCESS: full-text
  STATUS: textbook-or-review (official ESA documentation)
  CONFIDENCE: high

- [RE-02] CLAIM: DR4 publishes data for all ~2.8 billion processed sources (about 2 billion in a high-quality gaia_source subset), with a "best-suited model" per source (e.g. a binary-star model instead of the DR3 single-star default). Total volume ~400 TB (DR3: 10 TB), mostly epoch products.
  SOURCE: ESA Gaia DR4 content page, https://www.cosmos.esa.int/web/gaia/dr4
  QUOTE: "In contrast to previous releases, data will be published for all processed sources, which amount to about 2.8 billion sources in total. The gaia_source table in Gaia DR4 contains a high-quality subset of about 2 billion of these sources that are considered to have both high-quality astrometry and photometry. ... the best-suited model has been applied for a given source (e.g., a binary-star model instead of the default single-star model as was the case in Gaia DR3)."
  ACCESS: full-text
  STATUS: textbook-or-review (official ESA documentation)
  CONFIDENCE: high

- [RE-03] CLAIM: DR4 includes, for the first time, epoch astrometry for all sources treated in the main astrometric processing (table epoch_astrometry, 129,625,750,708 rows, 62 TB, DL2), in addition to the source-level tables. Epoch RVS parameters are published only as astrophysical-parameter epoch tables for RR Lyrae and Cepheids (ap_rvs_epoch, 363,457 rows) in the listing seen; the all_source_rvs table (mean RVS results) has 312,247,580 rows (DR3 gaia_source had RVs for ~33.8 million; that DR3 number is not from this page and is unverified here).
  SOURCE: ESA Gaia DR4 content page, https://www.cosmos.esa.int/web/gaia/dr4
  QUOTE: "epoch_astrometry Time series of astrometric data, i.e. individual astrometric measurements for all sources treated in the main astrometric processing. Epoch NEW DL2 Astrometry DataLink 129,625,750,708 62 TB" ; "all_source_rvs Parameters such as radial velocities, spectral line broadening, and Grvs magnitudes, derived from the Radial Velocity Spectrometer (RVS). Main NEW DL3 Spectroscopy TAP 312,247,580 28 GB"
  ACCESS: full-text
  STATUS: textbook-or-review (official ESA documentation)
  CONFIDENCE: high for the table facts; low for the "epoch RV for all sources" question (I did not find an all-source epoch RV table in the greps; verify on the page before the brief's "epoch RVs" premise is relied on)

- [RE-04] CLAIM: DR4 contains non-single-star (NSS) tables directly relevant to wide-binary tests: nss_acceleration_astro (3,365,947 rows, sources with non-linear proper motion compatible with an acceleration solution), nss_two_body_orbit (5,901,111 rows), nss_multiple_orbits (16,681), and NEW tables nss_resolved_pair (22,829,105 rows; "resolved pairs of sources being physically bound") and nss_multiplicity (229,083,823 rows; sources in more than one resolved pair).
  SOURCE: ESA Gaia DR4 content page, https://www.cosmos.esa.int/web/gaia/dr4
  QUOTE: "nss_acceleration_astro Non-single-star (NSS) astrometric solution models for sources having a non-linear proper motion which is compatible with an acceleration solution. Non-single stars DL3 Astrometry TAP 3,365,947" ; "nss_resolved_pair Non-single-star astrometric models for resolved pairs of sources being physically bound (in contrast with chance alignment pairs). Non-single stars NEW DL3 Astrometry TAP 22,829,105" ; "nss_multiplicity Source may be involved in more than one resolved pair. This table list all pairs involving a given source."
  ACCESS: full-text
  STATUS: textbook-or-review (official ESA documentation)
  CONFIDENCE: high

- [RE-05] CLAIM: ESA's predicted DR4 parallax standard errors (sky-averaged) are 10 uas at G=13, 14 at G=14, 22 at G=15, 35 at G=16, 59 at G=17, 107 at G=18, 211 at G=19, 462 at G=20; modelled as sigma_plx[uas] = T_factor (40 + 800 z + 30 z^2)^(1/2) with T_factor = 0.749 for DR4 and 0.527 for DR5. Proper-motion errors scale as sigma_mu = 0.96 sigma_plx (EDR3), 0.54 sigma_plx (DR4), 0.27 sigma_plx (DR5) (per-axis: mu_alpha* 1.03/0.58/0.29, mu_delta 0.89/0.50/0.25). ESA states published errors are typically ~10% larger than formal ones. Hence at a given G the DR4 proper-motion error is smaller than the EDR3 one by a factor 0.54*0.749/0.96 ~ 0.42 (my arithmetic, using the EDR3 parallax model without a T-factor, assuming the same z-model applies to EDR3; this EDR3 normalization is not on the page), i.e. roughly 2.4x, NOT the 2.7x of the brief's (66/34)^1.5 estimate.
  SOURCE: ESA Gaia science performance page, https://www.cosmos.esa.int/web/gaia/science-performance
  QUOTE: "σ μ 0.96 · σ ϖ 0.54 · σ ϖ 0.27 · σ ϖ" ; "σ ϖ [μas] = T factor · (40 + 800 · z + 30 · z 2 ) 1/2 , where T factor = 0.749 for Gaia DR4 and 0.527 for Gaia DR5 represents the temporal improvement factor in the parallax uncercainty allowed by adding more data that span a longer time interval" ; table row "G = 15 mag 22 μas 16 μas"
  ACCESS: full-text
  STATUS: textbook-or-review (official ESA prediction, pre-release; DR4 not yet public)
  CONFIDENCE: high for the table and scaling; medium for the 2.4x ratio (my derived number; the EDR3 sigma_plx normalisation must be checked against El-Badry+2021 / Lindegren+2021)

- [RE-06] CLAIM: Boufourou 2026 (single-author, independent researcher, preprint, not refereed; LLMs used as computational assistants, per his own declaration) uses the public Chae (2024) sample of 81,088 pairs within 200 pc drawn from El-Badry+2021, and gets, with fiducial cuts RUWE<1.4 (both), R_chance<0.01, sigma_vtilde<0.10 (41,760 pairs retained): E2 (tail-truncated at vtilde<sqrt2, templates re-truncated and noise-matched) gamma_test(2-30 kau) = 1.045 [1.025, 1.068] (68% bootstrap; empirical per-zone f(e)); f(e) systematic band 0.96-1.05 (thermal 0.958, superthermal 0.957); E3 mixture gamma = 1.05 [1.04, 1.07] with f_trip = 0.15; gamma=1.4 rejected at Delta lnL = 129 (~16 sigma, statistical). Deep bin (g_N/a0 in [0.03,0.3], N=341): gamma(E2) = 0.97 without and 1.11 +/- 0.07 with the angular perspective correction; full bracket ~[0.97, 1.19].
  SOURCE: Boufourou 2026, "Estimator forensics for the wide-binary gravity test...", arXiv:2608.24556v1, https://arxiv.org/pdf/2608.24556
  QUOTE: "we measureγtest = 1.045 [1.025,1.068](2–30 kau;f(e)systematic band 0.96–1.05) and, from a joint(γ,f trip)mixture fit,γ= 1.05 [1.04,1.07]withf trip = 0.15 ... γ= 1.4is rejected at∆ lnL= 129(≈16σ)." ; "Fiducial cuts: RUWE<1.4(both components), Rchance <0.01,σ ˜v<0.10(41,760 pairs)"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high (that the paper says this); medium for the physics (unrefereed, LLM-assisted, generator tuned to Pittordis+2025 oracles)

- [RE-07] CLAIM: Boufourou's estimator definitions and the sample-vs-estimator test: E1 = full-median (squared ratio of full medians test/validation corrected by expected Newtonian ratio); E2 = medians truncated at vtilde<sqrt2 with identical truncation of zone-matched noisy templates inverted on a gamma grid; E3 = Poisson mixture likelihood (1-f)*binaries_gamma + f*triple template, (gamma,f) free. On Newtonian truth with 20-30% residual triples E1 returns 1.08-1.13 (identical in all three f(e) panels), E2 <=1.04, E3 1.00; on MOND truth (gamma=1.4 above 2 kau) all three return >=1.26 (E2 1.31-1.36). Single-seed grid, statistical jitter ~+/-0.02. A Rice-type noise bias: before zone-matched noisy templates even E2 returned 1.18 on pure Newtonian truth. He states the E1 bias is an upper edge because his triple model's P90 is 10-14% above Pittordis+2025.
  SOURCE: arXiv:2608.24556v1, https://arxiv.org/pdf/2608.24556
  QUOTE: "On Newtonian truth, E1 manufacturesγ= 1.08–1.13atf trip = 0.2–0.3, identically in all threef(e)panels ... E2 stays≤1.04and E3 at1.00. On MOND truth all three recover≥1.26(E2: 1.31–1.36" ; "before zone-matched noisy templates even E2 returned 1.18 on pure Newtonian truth" ; "Single-seed grid; statistical jitter≈±0.02."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high (as reported); the bias map is what the run's mechanist must reproduce

- [RE-08] CLAIM: Boufourou's DR4 protocol: sample/cuts, three zones (validation 0.2-2 kau; test 2-30 kau; deep bin g_N/a0 in [0.03,0.3]), estimators E2 (primary) and E3 (secondary) with measured biases, a mandatory f(e) band, noise- and selection-matched templates, four pre-written decision criteria including STOP-and-publish if the validation-zone control fails (median within 2% of Newtonian template; he measures +1.4% on DR3) and a grey zone if E2 and E3 disagree beyond combined intervals. The paper expects DR4 to "multiply proper-motion precision by 2-4 and the usable sample by 3-5", with sigma_stat(gamma)<~0.005. The paper says the protocol v1.0 was frozen on 15 July 2026, but the Zenodo record (published 24 Aug 2026, Version v1.0 = code package) says the pre-registered protocol inside is "draft v0.95" and "Le protocole gelé (v1.0) fera l'objet d'une release ultérieure avant le 2026-12-02". Internal inconsistency in dating.
  SOURCE: arXiv:2608.24556v1 Sect. 6; Zenodo record https://zenodo.org/records/22073431 (doi:10.5281/zenodo.22073431)
  QUOTE: "We therefore freeze, before the release, a complete protocol ... and four decision criteria written in advance, including a STOP-and-publish rule if the validation-zone control fails and an explicit grey-zone outcome. E2 is primary and E3 secondary" ; "the frozen protocol (v1.0, 15 July 2026)" ; Zenodo: "protocole/ : protocole pré-enregistré Gaia DR4 (draft v0.95) ... Le protocole gelé (v1.0) fera l'objet d'une release ultérieure avant le 2026-12-02."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high
  NOTE: the Zenodo page said "There is a newer version of the record available" (checked 2026-10-11); see next claim.

- [RE-09] CLAIM: The Zenodo concept record of Boufourou's package (concept DOI 10.5281/zenodo.22073430) has two versions as of 2026-10-11: v1.0 (published 2026-08-24, doi 10.5281/zenodo.22073431) and v2.0 (published 2026-08-26, doi 10.5281/zenodo.22114321; "threshold scan, MNRAS version"; paper submitted to MNRAS as manuscript MN-26-2659-P). Both describe the pre-registered DR4 protocol as "draft v0.95" with the frozen v1.0 (dated 2026-07-15 in the v2.0 text) to be released "avant le 2026-12-02". I found no separate Zenodo record of a frozen protocol v1.0 as of 2026-10-11, so the protocol is not yet independently time-stamped; the DR4 protocol cannot yet be treated as frozen. GitHub (403) could not be read.
  SOURCE: Zenodo API https://zenodo.org/api/records/22073431/versions ; https://zenodo.org/records/22114321
  QUOTE: "protocole/ : protocole pré-enregistré Gaia DR4 (draft v0.95 ; version gelée v1.0 du 2026-07-15, release avant le 2026-12-02)" ; "(soumis à MNRAS, manuscript MN-26-2659-P)" ; versions list "total": 2
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high for the record state on 2026-10-11; the state may change before 2 Dec

- [RE-10] CLAIM: Banik et al. 2024 compared a sample of 8611 wide binaries with a forward model for the WB population, undetected close binaries and line-of-sight contamination; result alpha_grav = -0.021 (+0.065, -0.045), "excluding MOND at 16 sigma" (as summarised by Cookson+2026; the Banik paper itself is the primary source; Boufourou's intro cites "19 sigma for Newton"). Banik's d limit is 250 pc, vs Cookson+2026's 130 pc (150 pc variant).
  SOURCE: Cookson et al. 2026 (A Quality Framework for Testing Gravity with Wide Binaries: No Evidence for MOND), MNRAS 547, stag342, arXiv:2602.24035, Sect. 6.10, https://arxiv.org/pdf/2602.24035
  QUOTE: "This study compared a large sample of 8611 WBs with a forward modelfortheWBpopulation,undetectedCBs,andlineofsightcontamination ... αgrav =−0.021 +0.065 −0.045, excluding MOND at16σconfidence but well within1σof the Newtonian expectation."
  ACCESS: full-text
  STATUS: peer-reviewed (Cookson 2026, MNRAS) quoting Banik+2024 (MNRAS 527, 4573); secondary for the Banik numbers
  CONFIDENCE: medium-high (primary Banik+2024 text to be opened by the quantitative facet)

- [RE-11] CLAIM: Cookson et al. 2026's sample cuts (their "quality framework") are: heliocentric distance d_h < 130 pc (also shown to 150 pc; Banik+2024 went to 250 pc), RUWE < 1.25 (they note the optimal single-source DR3 cutoff varies 1.15-1.37 across the sky, average ~1.25), ipd_frac_multi_peak = 0 for both stars (particularly important beyond ~130 pc), a colour-magnitude-diagram parallelogram, and kinematic cuts such as vtilde < 2.5 (removing ~50 of ~900 pairs in their Fig. 3 panel) plus a spherical (perspective) projection correction. They note a RUWE cut "will only filter out CBs with periods of months to years" and is insensitive to shorter and longer periods.
  SOURCE: Cookson et al. 2026, MNRAS 547, stag342, arXiv:2602.24035, Sect. 3, https://arxiv.org/pdf/2602.24035
  QUOTE: "We therefore require RUWE<1.25, though a moreconservativecutoffat1.15mightalsobereasonable." ; "It is important to note that a RUWE cut will only filter out CBs with periods of months to years, but will be insensitive to CBs with bothshorterandlongerperiods" ; "Requiringipd_frac_multi_peak= 0for both stars in a WB provides an additional layer of quality control" ; "Cookson(2024)imposedanupperlimitof130pc,whichweadopt here."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-12] CLAIM: Chae & Yoon 2026 (preprint, 49 pp) argue the sample difference is itself the issue: Banik+2024 and Chae 2023 vtilde distributions (no RUWE limit) are similar, but the Pittordis-Sutherland-Shepherd (PSS) sample, which satisfies RUWE<1.2 plus a narrow CMD band, has a significantly lower median vtilde because the RUWE cut removed a large fraction of hierarchical systems; PSS has all pairs at r_p > 2 kau, so no high-acceleration (g_N >~ 10^-8.5 m/s^2) pairs for f_multi calibration, and a larger unbound fraction. They also say the Cookson+2026 quality framework (distance limit, RUWE cut, perspective correction, CMD cut, ipd_frac_multi_peak=0, Banik vtilde-error cut) does not remove the anomaly. This is Chae's claim, not established.
  SOURCE: Chae & Yoon 2026, "Revisiting Data Quality Control and Multiple-star Modeling in Wide Binary Gravity Tests", arXiv:2607.14450, https://arxiv.org/pdf/2607.14450
  QUOTE: "The PSS sample satisfiesruwe<1.2 and a narrow band in the color-magnitude diagram (CMD), and thus it includes a significantly lower fraction of hierarchical systems ... The median ˜vin the fiducial bin decreases in the or- der of the K.-H. Chae (2023) sample, the I. Banik et al. (2024) sample, and the PSS sample." ; "all pairs haver p >2 kau and thus do not include systems with high internal acceleration (≳10−8.5 m s−2) that can be useful for calibration purposes"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high (as reported)

- [RE-13] CLAIM: El-Badry, Rix & Heintz 2021 (MNRAS 506, 2269) catalogue: Gaia eDR3, within 1 kpc, projected separations from a few au to 1 pc, 1.3 million (1.1 million) binaries with >90% (>99%) probability of being bound, including 16,000 WD+MS and 1,400 WD+WD. Selection: parallaxes consistent within 3 sigma (6 sigma for theta<4 arcsec), and proper-motion difference consistent with a Keplerian orbit, Delta_mu <= Delta_mu_orbit + 2 sigma_Delta_mu, where Delta_mu_orbit corresponds to a circular orbit of total mass 5 Msun: Delta_V_orb = 2.1 km/s (s/1000 au)^(-1/2). This hard cut is the source of the velocity truncation in the sample (Boufourou quotes vtilde <= 2.23/sqrt(M_tot) with M_tot in Msun) and removes "a significant fraction of unresolved hierarchical triples". Chance-alignment probabilities R are estimated empirically from (i) the Gaia eDR3 mock catalogue and (ii) the same catalogue with every star shifted 0.5 deg in position.
  SOURCE: El-Badry, Rix & Heintz 2021, "A million binaries from Gaia eDR3: sample selection and validation of Gaia parallax uncertainties", arXiv:2101.05282, doi:10.1093/mnras/stab323, https://arxiv.org/pdf/2101.05282
  QUOTE: "We require Δμ ≤ Δμorbit + 2σΔμ ... Δμorbit= 0.44 mas yr−1 (ϖ/mas)^(3/2)(θ/arcsec)^(−1/2) which is the maximum proper motion difference expected for a circular orbit of total mass 5M ; it corresponds to a projected physical velocity difference ΔVorb= 2.1 km s−1 (s/1000 au)^(−1/2)" (symbols reconstructed from extraction; wording of the text exact) ; "the cut on proper motion difference removes from the sample a significant fraction of unresolved hierarchical triples and higher-order multiples" ; "artificially shift it from its true position by ∼0.5 degrees"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-14] CLAIM: El-Badry+2021 found Gaia eDR3 formal parallax uncertainties underestimated: "generally ~30% for isolated sources with well-behaved astrometry" brighter than G~18, up to 80% for apparently well-behaved sources with a companion within ~4 arcsec, "much larger" for poor astrometric fits; reliable for faint stars (G >~ 18). They supply an empirical inflation function for isolated sources. Consequence for this run: every DR3 sigma_vtilde (Chae, Banik, Boufourou use catalogue errors) depends on this, and a DR4 analogue calibration is needed.
  SOURCE: El-Badry, Rix & Heintz 2021, arXiv:2101.05282 abstract
  QUOTE: "We show that these uncertainties are generally reliable for faint stars (G ≳ 18), but are underestimated significantly for brighter stars. The underestimates are generally ∼30% for isolated sources with well-behaved astrometry, but are larger (up to ∼80%) for apparently well-behaved sources with a companion within . 4 arcsec, and much larger for sources with poor astrometric fits."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-15] CLAIM: Chae 2023 (ApJ 952, 128) sample: main sample of 26,615 wide binaries within 200 pc (gN~10^-10.15 gives g_obs/g_pred = 1.43 +/- 0.06 per his abstract; value belongs to the quantitative facet); calibration/statistical sample within 80 pc, selected by: both stars main sequence (El-Badry 'MSMS'), chance-alignment probability R<0.01, |d_A - d_B| < 3 sqrt(sigma_dA^2 + sigma_dB^2), and relative errors of all PM components smaller than 0.01 (or 0.005). Median RUWE of the selected stars is 1.03; there is no RUWE limit. 80 pc distance limit chosen so s>200 au is resolved at >2.5 arcsec and extinction is negligible; El-Badry excluded systems with resolved additional components, so the d<80 pc sample is free of resolved companions down to M_G~16.5. Chae 2023 considers ruwe<1.2 and PM error <0.003 only in a robustness check.
  SOURCE: Chae 2023, "Breakdown of the Newton-Einstein Standard Gravity at Low Acceleration in Internal Dynamics of Wide Binary Stars", ApJ 952, 128, arXiv:2305.04613, https://arxiv.org/pdf/2305.04613
  QUOTE: "from the main sample of 26,615 wide binaries within 200 pc" ; "Relative errors of PM components for each binary are all smaller than 0.01 (or 0.005 as an alternative choice). Median ruwe value for the selected stars is 1.03." ; "R< 0.01 whereR is the chance alignment probability defined by El-Badry, Rix & Heintz (2021)."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-16] CLAIM: Gaia (E)DR3 astrometry facts: median uncertainty in parallax and annual proper motion is 0.02-0.03 mas (mas/yr for PM) at G = 9 to 14 and about 0.5 mas at G = 20; 5-parameter solutions available for 93% of sources brighter than G=17. ESA's DR4 prediction at G=13-14 is sigma_plx = 10-14 uas, i.e. sigma_mu ~ 5.4-7.6 uas/yr using the 0.54 factor (RE-05), so DR4 proper-motion errors are smaller than the quoted DR3 medians by ~3-5x at G~13-14 (my arithmetic: 20-30 uas/yr over 5.4-7.6 uas/yr) and by ~2.4x on the pure model-ratio basis in RE-05. The brief's (66/34)^1.5 ~ 2.7x lies inside this range; Boufourou's "2-4" is also consistent. DR3 angular covariance of astrometric errors on small scales is characterised by Lindegren+2021 (Fig. 15, quasar sample), which matters for pairs a few arcmin apart whose PM differences are used (common-mode errors cancel, as Boufourou notes; not measured here).
  SOURCE: Lindegren et al. 2021, "Gaia Early Data Release 3: The astrometric solution", A&A 649, A2, arXiv:2012.03380, https://arxiv.org/pdf/2012.03380
  QUOTE: "The median uncertainty in parallax and annual proper motion is 0.02–0.03 mas at magnitudeG = 9 to 14, and around 0.5 mas atG = 20."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high for the DR3 quote; medium for the DR4/DR3 ratios (derived)

- [RE-17] CLAIM: Gaia DR3 radial velocities exist for 33,812,183 stars to G_RVS=14, median formal precision 1.3 km/s at G_RVS=12 and 6.4 km/s at G_RVS=14, zero-point trend reaching ~400 m/s at G_RVS=14 (correction supplied). These errors are comparable to or larger than typical wide-binary orbital speeds (~0.1-0.5 km/s at 2-30 kau; Boufourou cites ~0.5 km/s orbital signal), so DR3 RVs are useful for the systemic-velocity perspective correction but not for relative line-of-sight velocity. Katz+2023 state the plan to publish RVs of all sources to G_RVS~16 in DR4. Boufourou reports RV availability for the Chae-2024 sample as 83.0% (validation zone 0.2-2 kau), 95.7% (test zone) and 99.4% (deep bin), and warns that individual-distance perspective corrections and missing-RV sentinels (-10,000 / -20,000 km/s) inject noise.
  SOURCE: Katz et al. 2023, "Gaia Data Release 3: Properties and validation of the radial velocities", A&A 674, A5, arXiv:2206.05902, https://arxiv.org/pdf/2206.05902 ; Boufourou arXiv:2608.24556
  QUOTE: "The median formal precision of the velocities is of 1.3 km s −1 at GRVS = 12 and 6.4 km s−1 at GRVS = 14 mag. The velocity zero point exhibits a small systematic trend with magnitude starting around GRVS = 11 mag and reaching about 400 m s−1at GRVS = 14 mag." ; "It is planned to publish the radial velocities of all sources down to the RVS limiting magnitude ofGRVS∼ 16 mag, in the Fourth Gaia Data Release"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RE-18] CLAIM: Both camps say DR4 will matter, with different emphasis. Chae & Yoon 2026 (preprint): "gravity tests based on a large number of 2D velocities are also promising with the upcoming release of Gaia DR4 in December 2026, which will provide dramatically larger samples with significantly improved data qualities", and they expect orbit modelling with 3D velocities to play a larger role. Cookson+2026 (MNRAS): astrometric acceleration of a contaminating companion cannot yet be searched for directly because "astrometric time series are expected to be available only for Gaia Data Release 4 (DR4), which will provide Keplerian orbital solutions for a large sample of binaries (El-Badry et al. 2024)"; for now they use RUWE as proxy. Neither paper gives a numerical DR4 target precision.
  SOURCE: Chae & Yoon 2026, arXiv:2607.14450 (Conclusions); Cookson et al. 2026, MNRAS 547, stag342, arXiv:2602.24035, Sect. 3
  QUOTE: see CLAIM (both passages verbatim from fetch_text: "gravity tests based on a large number of 2D velocities are also promising with the upcoming release of Gaia DR4 in December 2026, which will provide dramatically larger samples with significantly improved data qualities" ; "astrometric time series are expected to be available only forGaiaData Release 4 (DR4), which will provide Keplerian orbital solutions for a large sample of binaries")
  ACCESS: full-text
  STATUS: preprint (Chae & Yoon); peer-reviewed (Cookson)
  CONFIDENCE: high

- [RE-19] CLAIM (shared apparatus and supersession map, engineering view): Every DR3 result in the dispute uses the same Gaia (E)DR3 astrometry (34 months) and, except where noted, the El-Badry+2021 catalogue as parent; they are therefore not independent measurements of the sky. Boufourou's 2026 DR3 numbers re-analyse the same 81,088-pair Chae-2024 sample (so they share data with, and do not add data to, Chae 2024). Chae 2023 (26,615 pairs, <200 pc; superseded as the headline sample by later Chae papers) and Banik+2024 (8,611 pairs, d<250 pc) draw on the same catalogue with different distance and quality cuts (Chae: no RUWE cut, R<0.01, PM relative errors <0.01; Cookson: d<130 pc, RUWE<1.25, ipd_frac_multi_peak=0; Boufourou: RUWE<1.4 both, R<0.01, sigma_vtilde<0.10, 41,760 pairs). Chae+2026 (36 isolated wide binaries with accurate 3D velocities) adds ground-based radial velocities and is a different data subset I did not open this run. Makarov 2026 (AJ 171, 79) uses 103,169 Gaia DR3 wide binaries and the projected orbital momentum, as reported by Boufourou; not opened here.
  SOURCE: synthesis of RE-06, RE-10, RE-11, RE-12, RE-15; Chae et al. 2026 abstract (arXiv:2601.21728, via lit_search), Makarov via Boufourou arXiv:2608.24556
  SUMMARY: synthesis claim; component sources quoted above. Chae+2026 abstract (lit_search): "We set out to accurately measure gravity in the low-acceleration range (10^-11,10^-9) m s^-2 from 3D motions of isolated wide binary stars."
  ACCESS: abstract (Chae+2026); full-text (others)
  STATUS: preprint / peer-reviewed mixed
  CONFIDENCE: medium

## Gaps
- Not found: any independent group's DR4-specific wide-binary forecast with numbers (target sigma_stat, expected N). Only Boufourou's unsupported "usable sample x3-5, sigma_stat(gamma) <~ 0.005" and Chae & Yoon's qualitative "dramatically larger samples". My arithmetic from the ESA tables suggests DR4 proper-motion errors ~2.4-5x smaller than DR3 at fixed G; the number of DR4 pairs is not derived. The new DR4 table nss_resolved_pair (22.8 million rows, "physically bound" resolved pairs, all separations) is a ready-made parent catalogue; how many have 2-30 kau, d<250 pc and the quality cuts used here is unknown until release (2 Dec 2026).
- Not verified: whether DR4 provides epoch radial velocities for all RVS sources (the greps found only all_source_rvs, 312,247,580 rows, and ap_rvs_epoch for RR Lyrae/Cepheids); the brief's "epoch RVs" premise is unconfirmed beyond mean RVs to G_RVS~16.
- Not verified: ESA science-performance page predates DR4 and is labelled predictions; actual DR4 errors are not public until 2 Dec 2026. The page also says published errors are typically ~10% larger than formal.
- Zenodo: frozen Boufourou protocol v1.0 is not a separate record yet (only code packages v1.0 and v2.0 exist as of 2026-10-11). GitHub returned 403, so the protocol text itself (decision criteria numerically) was not read; the protocol PDF inside the Zenodo zip (26.7 MB) was not opened. Boufourou's code was not read (brief says method only).
- Not done: Banik+2024 primary text (cuts, RUWE, d<250 pc, 2-30 kau, vtilde-error cut); Hernandez et al. 2024 sample and cuts; Pittordis, Sutherland & Shepherd 2025 sample (RUWE<1.2, r_p>2 kau per Chae & Yoon; N not captured); Pasquini+2026 and Saad & Ting 2026 (critiques facet); Chae's 81,088-pair sample definition (Chae 2024 ApJ 960, 114 / 972, 186). The systematic budgets of each analysis (largest items) were therefore not collected beyond what Boufourou and Chae & Yoon describe; the quantitative and critiques facets own the quoted gamma errors.
- No blinding: none of the DR3 analyses read described a blinded analysis; Boufourou's pre-registration is the only declared pre-commitment (and it was written after DR3 results were known, with DR3 as the calibration standard).
- PAPER TO REQUEST: none (all sources reachable).
