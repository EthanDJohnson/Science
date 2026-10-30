# Research: engineering
status: final
Mandate: local H0 measurements method by method (anchors, Cepheid/TRGB/JAGB/Mira ladders, SN samples, non-SN ladders, one-step methods, community combination) with quoted stat/sys uncertainties, largest systematics, blinding, supersession and shared data; plus running and planned local programmes.
Access: lit_search INSPIRE ok, arXiv endpoint timed out repeatedly (papers read through fetch_text on arxiv.org PDFs and abs pages); WebFetch/fetch_text domains that worked: arxiv.org, cosmos.esa.int, observing.docs.ligo.org

## Claims
- [RE-01] CLAIM: The community "Local Distance Network" (H0DN, ISSI workshop; A&A 708, A166, 2026) gives baseline H0 = 73.50 ± 0.81 km/s/Mpc (1.09%), a covariance-weighted combination of SNe Ia (Pantheon+), SBF and Hubble-flow masers as tracers, calibrated by Cepheids (all three anchors) and TRGB (NGC 4258 only), and differs by 7.1 sigma from Planck+SPT+ACT flat-LCDM (67.24 ± 0.35) and by 5.0 sigma from DESI DR2 BBN+BAO (68.51 ± 0.58). It is a combination of existing data, not an independent new measurement: it shares the SH0ES Cepheid/HST/JWST data and the Pantheon+ SNe with the SH0ES result and the CCHP TRGB data with CCHP.
  SOURCE: Casertano et al. 2025/2026, "The Local Distance Network: A community consensus report on the measurement of the Hubble constant at ~1% precision", A&A 708 A166, arXiv:2510.23823 (arXiv PDF text)
  QUOTE: "The baseline result isH 0=73.50±0.81 km s−1 Mpc−1. Compared to early Universe+ΛCDM results, our result differs by 7.1σfrom the CMB anisotropies within flat ΛCDM, 67.24±0.35 km s −1 Mpc−1 from Planck+SPT+ACT (Eq. (54) of E. Camphuis et al. 2025) and 5.0σfrom BBN+BAO within flat ΛCDM from DESI DR2 (68.51±0.58 km s −1 Mpc−1"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  ARTIFACT: code (IDL, with config files for every variant; repository referred to near the end of the paper, URL not captured)
  CONFIDENCE: high
- [RE-02] CLAIM: H0DN fixed its baseline by anonymous votes taken before any H0 was derived (a form of procedural blinding to the answer, not data blinding): a method entered the baseline if it got more than half the votes. Baseline calibrators: Cepheids, detached eclipsing binaries, TRGB, NGC 4258, Gaia parallaxes; JAGB and Miras went to variants only (the vote-count columns are garbled in the PDF extraction, so counts are not given). Secondary indicators: SNe Ia, SBF and Hubble-flow masers in the baseline; SNe II, DESI fundamental plane and Tully-Fisher as variants.
  SOURCE: Casertano et al., arXiv:2510.23823, Section 2 (Tables 2 and 3)
  QUOTE: "Methods were included in the baseline if they garnered more than half the total votes, including abstentions, as indicated by the horizontal lines in Tables 2 and 3. All votes were taken prior to deriving a value ofH 0, and their outcomes were considered binding."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: medium (vote-table columns are garbled in the PDF extraction; the rule itself is verbatim)
- [RE-03] CLAIM: H0DN leave-one-out and alternative-treatment variants (all in km/s/Mpc, 1-sigma as tabulated, all with a common H0DN pipeline): no Cepheids (V08) 72.509 ± 1.296 (custom baseline with the same SN calibrators V08B 72.873 ± 0.874); no TRGB/SBF (V09) 73.526 ± 0.878; no Gaia MW parallaxes 73.609 ± 0.929; no NGC 4258 73.084 ± 0.920; no SNe Ia (V13) 73.434 ± 1.795; no HST data 73.754 ± 1.325; exclude JWST data (V17) 73.002 ± 0.856; SNe Ia with CSP, all 55 calibrators (V22) 73.350 ± 0.963; no Cepheid metallicity correction (V28) 73.080 ± 0.801; Hubble-flow SNe at z > 0.06 (V20) 73.190 ± 0.862; SNe in 0.03-0.10 (V21) 72.667 ± 0.862; add Tully-Fisher (V06) 73.957 ± 0.787 with reduced chi2 = 1.47. 'Everything' (V99) 73.994 ± 0.697; 'everything except Tully-Fisher' (V99a) 73.656 ± 0.713. The dispersion of the variant central values is 0.400 km/s/Mpc.
  SOURCE: Casertano et al., arXiv:2510.23823, Table 4 and Sect. 5.2
  QUOTE: "V08 72.509 1.296 65.8536 69 0.95440 Baseline without Cepheids V08B 72.873 0.874 95.6518 98 0.97604 Custom baseline for V08 ... V17 73.002 0.856 81.5863 85 0.95984 Exclude JWST data ... V13 73.434 1.795 11.1578 23 0.48512 Baseline without SNe Ia ... the dispersion of central values is 0.400 km s−1 Mpc−1, or 50% of the baseline’s 1σuncertainty."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high
- [RE-04] CLAIM: H0DN notes that 55 SN Ia calibrators are in its baseline, of which only 35 have a non-Cepheid (TRGB) host distance, so removing Cepheids also removes 20 calibrators; and TRGB is anchored to NGC 4258 only, because Milky Way and LMC TRGB calibrations "do not meet our data requirements (notably photometric homogeneity across anchors and hosts in HST/JWST passbands)". The Cepheid-free solution therefore rests on one geometric anchor, with 1-sigma 0.87 km/s/Mpc against 1.30 when the calibrator set is not matched.
  SOURCE: Casertano et al., arXiv:2510.23823, Sect. 2 and 5.1
  QUOTE: "when Cepheid measurements are excluded, only 35 of the 55 SNe Ia calibrators in the baseline can be included, since the other 20 only have determinations of the host distances through Cepheids." and "TRGB distances are only anchored to NGC 4258, since TRGB calibrations from the Milky Way and LMC do not meet our data requirements (notably photometric homogeneity across anchors and hosts in HST/JWST passbands)."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high
- [RE-05] CLAIM: CCHP (Freedman et al. 2025, ApJ 985, 203) best estimate is H0 = 70.39 ± 1.22 (stat) ± 1.33 (sys) ± 0.70 (sigma_SN) km/s/Mpc from the TRGB alone with 24 SN Ia calibrators (HST + JWST) tied into the CSP B-band SN sample; JWST-only values are 68.81 ± 1.79 (stat) ± 1.32 (sys) for TRGB (11 calibrators) and 67.80 ± 2.17 (stat) ± 1.64 (sys) for JAGB (8 calibrators; JAGB uncertainty inflated by a factor 1.45). Eleven of the 24 SNe are common to the HST+JWST and JWST-only TRGB samples. This is the 'status report' that supersedes the CCHP 2019 TRGB value (69.8, HST) as the CCHP current number; it shares NGC 4258 as the only geometric anchor and the CSP SNe with the CSP sample.
  SOURCE: Freedman et al. 2025, "Status Report on the Chicago-Carnegie Hubble Program (CCHP)", ApJ 985, 203, arXiv:2408.06153
  QUOTE: "Our current best (highest precision) estimate is H0 = 70.39± 1.22 (stat)± 1.33 (sys)± 0.70 (σSN ), based on the TRGB method alone, with a total of 24 SN Ia calibrators from both HST and JWST data. Based on our new JWST data only, and tying into SNe Ia, we find values of H0 = 68.81± 1.79 (stat) ± 1.32 (sys) for the TRGB, and H0 = 67.80± 2.17 (stat)± 1.64 (sys) km s−1 Mpc−1 for the JAGB method."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high
- [RE-06] CLAIM: With CCHP's TRGB zero points applied to the SH0ES covariance machinery (Pantheon+ B band), CCHP finds H0 = 69.29 (TRGB, 11 calibrators) and 68.80 (JAGB, 8 calibrators), against R22's 72.51 ± 1.54 for the NGC 4258 anchor alone; and CCHP's own CSP-based number moves with the Hubble-flow redshift cut (69.81 +1.32/-1.29 for z > 0.025 to 70.73 +1.21/-1.18 when SN 1981D is omitted). So the SN sample/standardisation and the calibrator subset matter at the 1-2 km/s/Mpc level inside CCHP's own tables.
  SOURCE: Freedman et al. 2025, arXiv:2408.06153, Table 5
  QUOTE: "Pantheon SNe Ia sample 69.29 ... TRGB + Pantheon+ B band ; 11 SN calibrators SHoESd 68.80 ... JAGB + Pantheon+ B band ; 8 SN calibrators SHoESd ... R22 find H0 = 72.51± 1.54 for NGC 4258, but do not list the statistical and systematic uncertainties separately."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: medium
- [RE-07] CLAIM: TDCOSMO-2026 (blind; 11 lensed quasars; nine with spatially resolved kinematics, six with JWST-NIRSpec) gives H0 = 71.1 +2.4/-2.3 km/s/Mpc (3.3%) in flat LCDM with a DES-Dovekie Omega_m prior, and 3.0% precision when SLACS and SL2S non-time-delay lenses are added. It is a preprint (arXiv:2610.14781, Oct 2026), unblinded on 23 September 2026 after internal review by five reviewers. It supersedes TDCOSMO-2025 (8 lenses, blind baseline 71.6 +3.9/-3.3, with SLACS+SL2S 74.3 +3.1/-3.7) and TDC4/Birrer 2020 (7 lenses; 74.5 +5.6/-6.1 alone, 67.4 +4.1/-3.2 with the 33 SLACS lenses, whose SDSS velocity dispersions were later found to have underestimated uncertainties). It shares the time-delay lenses of H0LiCOW (Wong et al. 2020).
  SOURCE: Birrer et al. 2026, "TDCOSMO 2026: A 3% measurement of the Hubble constant from strong lensing and stellar kinematics", arXiv:2610.14781
  QUOTE: "In the flatΛ cold dark matter (ΛCDM) cosmology, we find 𝐻0=71.1+2.4 −2.3 km s−1 Mpc−1, a 3.3% uncertainty that accounts for the mass-sheet degeneracy. The SLACS and SL2S samples are in excellent agreement with the TDCOSMO-2026 sample, improving the precision on𝐻0 in flatΛCDMto 3.0%." / "Unblinding of the hierarchical analysis took place on September 23, 2026, after completion of the internal review, and the results were published without modification."
  ACCESS: full-text
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: high
- [RE-08] CLAIM: The dominant systematic of time-delay cosmography is the mass-sheet degeneracy (MSD); the TDCOSMO approach marginalises it with a free internal parameter lambda_int constrained by stellar kinematics (raising the uncertainty from 2% to 8% for the same 7 lenses relative to power-law/composite profile assumptions, which gave H0 = 74.2 ± 1.6), and the result is therefore sensitive to the kinematic data quality and to the choice of mass-profile family.
  SOURCE: Birrer et al. 2026, arXiv:2610.14781, Introduction
  QUOTE: "Shajib et al.[38], Wong et al.[52], Millon et al.[57] broke it by assuming functional forms for the mass density profiles of the deflectors that go to zero at large radii, obtaining𝐻0 =74.2±1.6 km s −1 Mpc−1, in agreement with the H0DN value and a 2% uncertainty." / "For the same sample of 7 lensed quasars analyzed by Millon et al.[57], the uncertainty increased from 2% to 8% as a result, yielding𝐻0=74.5+5.6 −6.1 km s−1 Mpc−1."
  ACCESS: full-text
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: high
- [RE-09] CLAIM: SH0ES R22 (ApJL 934, L7) baseline: H0 = 73.04 ± 1.04 km/s/Mpc including systematics from analysis variants (73.04 ± 1.01 from the fit alone), from 42 Cepheid-hosted SNe Ia (37 hosts) and 277 Hubble-flow SNe Ia at 0.0233 < z < 0.15 from Pantheon+, with three anchors (MW Gaia EDR3, LMC DEBs, NGC 4258 maser) and M_B^0 = -19.253 ± 0.027 mag; metallicity term Z_W = -0.217 ± 0.046 mag/dex; 67 analysis variants; Cepheid + TRGB combined 72.53 ± 0.99. The difference from Planck+LCDM (67.4 ± 0.5) is 0.176 ± 0.035 mag in 5 log H0, 5.0 sigma. The analysis was not blinded in the conventional sense (R22 only offers to supply artificial-Cepheid images for others to test their photometry blindly).
  SOURCE: Riess et al. 2022, "A Comprehensive Measurement of the Local Value of the Hubble Constant with 1 km/s/Mpc Uncertainty from the Hubble Space Telescope and the SH0ES Team", ApJL 934, L7, arXiv:2112.04510
  QUOTE: "Our baseline result from the Cepheid–SN Ia sample is H 0 = 73.04± 1.04 km s −1 Mpc−1, which includes systematic uncertainties and lies near the median of all analysis variants. We demonstrate consistency with measures from HST of the TRGB between SN Ia hosts and NGC 4258, and include them simultaneously to yield 72.53± 0.99 km s−1 Mpc−1." / "The full difference from the Planck+ΛCDM prediction of H 0 = 67.4± 0.5 ... in units of ∆5 log H0 is 0.176± 0.035 mag (errors in quadrature), a difference of 5.0 σ"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high
- [RE-10] CLAIM: SH0ES R22 variants for dust: using empirical host-specific R_V from the Hahn et al. attenuation framework raises H0 by 0.8 km/s/Mpc; dropping Cepheid colour altogether (Fit 23) raises H0 by 2%; the net E(V-I) difference between anchor Cepheids (weighted mean 0.43 mag) and SN-host Cepheids (mean 0.35 mag) is 0.08 mag, so the full effect of correcting Cepheid reddening is about 0.03 mag (~1.5%). The R22 text gives the dust treatment as a small lever, not a candidate for the 0.17 mag gap.
  SOURCE: Riess et al. 2022, arXiv:2112.04510, Sect. 6.3
  QUOTE: "Fit 22 uses these modeled values of R from Hahn et al. (2021) and results in an increase in H 0 of 0.8 km s−1 Mpc−1." / "the full impact on H0 of correcting for Cepheid reddening is 0.03 mag or ∼ 1.5%" / "In Fit 23 we discard the use of color altogether ... and find that H 0 goes up by 2%."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high
- [RE-11] CLAIM: SH0ES JWST Cycle 1 (Riess et al. 2024, ApJL 962, L17): JWST NIRCam photometry of >1000 Cepheids in NGC 4258 and five SN Ia hosts (eight SNe Ia) gives a mean JWST-minus-HST Cepheid distance difference of -0.01 ± 0.03 mag; unrecognised crowding that grows with distance and could explain the tension is rejected at 8.2 sigma; P-L dispersion reduced by a factor 2.5. A later Cycle 2 paper (Riess et al. 2025, ApJL 992, L34, 'Perfect Host' NGC 3447/3447A) adds >100 Cepheids, finds no component offset (sigma < 0.03 mag), and across Cycles 1-2 covers 19 SH0ES hosts (24 of 42 SNe Ia) with no HST bias; JWST Cepheids (19 hosts, 24 SNe Ia) combined with HST (37 hosts, 42 SNe Ia) give H0 = 73.49 ± 0.93, and adding 35 TRGB calibrations (55 SNe Ia) gives 73.18 ± 0.88 km/s/Mpc. Both are SH0ES-team analyses of SH0ES-selected data (not independent of R22's anchors and SN sample); they test photometry, not the other rungs.
  SOURCE: Riess et al. 2024, arXiv:2401.04773; Riess et al. 2025, arXiv:2509.01667
  QUOTE: "We find no significant difference in the mean distance measurements determined from HST and JWST, with a formal difference of -0.01±0.03 mag." / "Combining JWST Cepheid measurements in 19 hosts (24 SNe Ia) with HST data (37 hosts, 42 SNe Ia) yields H 0 = 73.49± 0.93 km s−1 Mpc−1. Including 35 TRGB-based calibrations (from HST and JWST) totals 55 SNe Ia and gives H 0 = 73.18± 0.88 km s−1 Mpc−1"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high
- [RE-12] CLAIM: SH0ES (Riess et al. 2024, arXiv:2408.11770, "JWST Validates HST Distance Measurements: Selection of Supernova Subsample Explains Differences in JWST Estimates of Local H0") finds the CCHP-JWST versus SH0ES-HST difference (delta H0 ~ 2.5 km/s/Mpc) is consistent with SN-calibrator sample selection: on the JWST-observed SN subsets, HST Cepheids predict 71.2 (CCHP-selected, 11 SNe Ia), 73.6-73.9 (SH0ES-selected, 9-11 SNe Ia), while the matching JWST Cepheid values are 72.0 ± 2.4 and 74.2 ± 2.3; for the 16 unique SNe at D <= 25 Mpc JWST Cepheids/JAGB/TRGB give 73.4 ± 2.1, 72.2 ± 2.2, 72.1 ± 2.2 and the three-method JWST result is 72.6 ± 2.0 (HST Cepheids in the same galaxies: 72.8); the HST full set (42 SNe Ia, 4 anchors) is 73.17 ± 0.86 (73.2 ± 0.9). SH0ES also states that a distance-dependent (non-linear) HST bias of 0.07 mag per mag is excluded at ~7 sigma. Competing reading: CCHP regards its own selection and its TRGB/JAGB calibration as the more reliable route (see RE-05); the two teams have not converged on a common SN subsample.
  SOURCE: Riess et al. 2024, arXiv:2408.11770, abstract and Table 4
  QUOTE: "We show that ∆H 0∼2.5 km s−1 Mpc−1 between the CCHP JWST program and the full HST sample is entirely consistent with differences in sample selection. We combine all JWST samples into a new distance-limited set of 16 SNe Ia at D≤ 25 Mpc. Using JWST Cepheids, JAGB, and TRGB, we find 73.4± 2.1, 72.2± 2.2, and 72.1± 2.2 km s−1 Mpc−1, respectively. Explicitly accounting for common SNe, the three-method JWST result is H 0 = 72.6± 2.0"
  ACCESS: full-text
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: high
- [RE-13] CLAIM: Megamaser Cosmology Project (Pesce et al. 2020, ApJL 891, L1): H0 = 73.9 ± 3.0 km/s/Mpc (4.1%) from six maser galaxies (UGC 3789, NGC 6264, NGC 6323, NGC 5765b, CGCG 074-064, NGC 4258), no peculiar-velocity correction, a fixed 250 km/s peculiar-velocity uncertainty; alternative peculiar-velocity treatments span 71.8-76.9 km/s/Mpc. The primary systematic is the unknown peculiar motion of the maser galaxies (distances 7.6-150 Mpc, recession velocities ~679-10,200 km/s). The NGC 4258 distance is shared with the SH0ES, CCHP and H0DN anchors, so the MCP value is not independent of the ladders at that one galaxy.
  SOURCE: Pesce et al. 2020, "The Megamaser Cosmology Project. XIII. Combined Hubble constant constraints", ApJL 891, L1, arXiv:2001.09213
  QUOTE: "we constrain the Hubble constant to beH0 = 73.9±3.0 km s−1 Mpc−1 independent of distance ladders and the cosmic microwave background. This best value relies solely on maser-based distance and velocity measurements, and it does not use any peculiar velocity corrections. Diﬀerent approaches for correcting peculiar velocities do not modify H0 by more than±1σ, with the full range of best-ﬁt Hubble constant values spanning 71.8–76.9 km s−1 Mpc−1."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high
- [RE-14] CLAIM: A 2026 preprint re-analysis of the MCP data (Stiskalek et al., arXiv:2609.17684) from maser spot catalogues, five of the six galaxies (NGC 4258 excluded and treated separately), with a non-linear (Manticore-Local) peculiar-velocity reconstruction finds H0 = 71.6 ± 3.7 km/s/Mpc (statistical error only); relative to ignoring peculiar velocities, linear and non-linear reconstructions lower H0 by 0.8-1.4 and 1.6-2.1 km/s/Mpc; NGC 4258 distance 7.558 ± 0.073 (stat.) Mpc, within 0.13 sigma of the published maser distance. An earlier reanalysis with the 2M++ field (Boruah et al. 2021) gave 70.1 ± 2.9. So the maser H0 depends at the 2-4 km/s/Mpc level on peculiar-velocity modelling, and Pesce 2020 is superseded as the preferred maser value only if this preprint is accepted.
  SOURCE: Stiskalek et al. 2026, "A reanalysis of the megamaser Hubble constant: from spot catalogues to peculiar velocities", arXiv:2609.17684
  QUOTE: "Accounting for peculiar velocities with the non-linear Manticore-Localreconstruction, we inferH 0 = 71.6±3.7 km s −1 Mpc−1, where the uncertainty is statistical. Relative to ignoring peculiar velocities, the linear and non-linear reconstructions lowerH 0 by 0.8–1.4 and 1.6–2.1 km s−1 Mpc−1, respectively"
  ACCESS: full-text
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: high
- [RE-15] CLAIM: LVK GWTC-4.0 (ApJL 1007, L17, 2026): using 142 of 218 GW sources (141 dark sirens, FAR < 0.25/yr, through O4a, with the GLADE+ catalogue, plus GW170817 as the single bright siren) and the fiducial source-frame mass model, H0 = 75.4 +12.8/-9.1 (68.3%) [+24.5/-13.3 at 90%] km/s/Mpc. Its H0 is dominated by population/mass-feature information and the GW170817 counterpart; it is not independent of the GW170817 value (Abbott et al. 2017, 70 +12/-8). GWTC-5.0 (preprint arXiv:2605.27227, 236 sources, DES-Y6 galaxy catalogue, v2 4 Aug 2026) supersedes it: H0 = 71.7 +9.4/-7.5 km/s/Mpc (median, 68% symmetric credible interval), 22% smaller H0 uncertainty than GWTC-4.0. Sirens are therefore consistent with both 67 and 73 at ~10-13% precision.
  SOURCE: Abac et al. (LVK) 2026, ApJL 1007, L17, arXiv:2509.04348 (abstract via arXiv page); LVK 2026, GWTC-5.0, arXiv:2605.27227 (abstract via arXiv page)
  QUOTE: "we estimate $H_0 = 75.4^{+12.8}_{-9.1} (75.4^{+24.5}_{-13.3})$ km s$^{-1}$ Mpc$^{-1}$. This value is reported as a median with 68.3% (90%) symmetric credible interval, and includes combination with the $H_0$ measurement from GW170817 and its electromagnetic counterpart." / "We estimate $H_0 = {71.7}_{-7.5}^{+9.4}\,{\text{km}\,\text{s}^{-1}\,\text{Mpc}^{-1}}$ (median with $68\%$ symmetric credible interval)."
  ACCESS: abstract
  STATUS: peer-reviewed (GWTC-4.0); preprint (GWTC-5.0)
  SETTING: analysis
  CONFIDENCE: high
- [RE-16] CLAIM: SUPERSESSION/ERRATUM-type update to the SN input of every Pantheon+-based ladder: a revised host-mass correction to Pantheon+ changes 114 of 1701 apparent-magnitude rows (none of the calibrator SNe, 52 of the 277 Hubble-flow rows). Applying the corrections to the H0DN fit moves the H0DN baseline from 73.499 ± 0.809 to 73.264 ± 0.806 km/s/Mpc (6.85 sigma against CMB 67.24 ± 0.35); replacing the whole Hubble-flow treatment with corrected Pantheon+ gives 73.139 ± 0.791 (6.82 sigma); DES-DOVEKIE (220 SNe, 0.025 <= z_HD <= 0.151, offset held fixed) gives 73.267 ± 0.828 (6.70 sigma). The author's conclusion is that neither update resolves the tension. This is a single-author ApJL analysis, not an H0DN-collaboration or SH0ES product; the SH0ES R22 and CCHP values were not recomputed by it. The corrected Pantheon+ is therefore the current Hubble-flow input for re-running any Pantheon+ ladder (SH0ES R22/2025, H0DN), shifting H0 by about -0.2 to -0.4 km/s/Mpc.
  SOURCE: Roy Choudhury 2026, "Updated 1.1% Precision Values of the Hubble Constant with Corrected Pantheon+ and DES-DOVEKIE Type Ia Supernovae", ApJL 1008, L50, arXiv:2607.24443 (v2, 15 Sep 2026)
  QUOTE: "A revised host-mass correction applied to the older Pantheon+ changes 114 of the total 1701 apparent-magnitude rows. The calibrator supernovae are not affected, but 52 of the 277 Hubble-flow rows are. Applying only these magnitude corrections, with the H0DN covariance, redshifts, and velocities unchanged, gives $H_0=73.264\pm0.806$ km s$^{-1}$ Mpc$^{-1}$ and a $6.85\sigma$ Hubble tension."
  ACCESS: abstract
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: medium (single-author recomputation from the H0DN public inputs; the Pantheon+ revision itself was not located)
- [RE-17] CLAIM: Local H0 depends on the assumed low-z background cosmology: if local distances are analysed with the w0wa models preferred by DESI instead of LCDM, H0 can be as much as 2.5 km/s/Mpc smaller; when the w0wa models are further constrained by CMB and SN data the downward shift is 1.1 ± 0.38 km/s/Mpc (DESI+CMB) and 0.5 ± 0.1 km/s/Mpc (DESI+CMB+SNIa). The H0DN pipeline's only direct cosmology dependence is a fixed q0 = -0.55, j0 = +1 (changing q0 to -0.50 lowers H0DN by under 0.1 km/s/Mpc).
  SOURCE: Turner & Huterer 2026, "The DESI results impact the local determination of H0", arXiv:2606.05358 (preprint); Casertano et al. arXiv:2510.23823 App. B
  QUOTE: "the downward shift is $1.1 \pm 0.38\,\mathrm{km\,s^{-1}Mpc^{-1}}$ (DESI + CMB) and $0.5 \pm 0.1\,\mathrm{km\,s^{-1}Mpc^{-1}}$ (DESI + CMB + SNIa)."
  ACCESS: full-text (abstract page text)
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RE-18] CLAIM: Surface-brightness-fluctuation (SBF) ladder, an SN-light-curve-independent route to the Hubble flow only for the SBF rung (it still uses SNe Ia in the Hubble flow in the Garnavich variant): Blakeslee et al. 2021 gave H0 = 73.3 ± 0.7 (stat) ± 2.4 (sys) km/s/Mpc with HST SBF calibrated to Cepheids and then TRGB; the TRGB-SBF Project III (Jensen et al. 2025, ApJ) recalibrated the HST SBF zero point with JWST TRGB distances anchored on the NGC 4258 maser, giving H0 = 73.8 ± 0.7 (stat) ± 2.3 (sys) km/s/Mpc, 'virtually identical' to Blakeslee 2021 and independent of Cepheids and SN Ia. The systematic term is dominated by the small number of calibrator galaxies (seven earlier). Garnavich et al. 2023 (SBF as intermediate step to SNe Ia) 74.6 ± 0.9 ± 2.7, which became 73.3 ± 1.0 ± 2.7 once SN fits were corrected for fast decliners. Jensen 2025 supersedes Blakeslee 2021 as the SBF H0; its TRGB calibration uses JWST TRGB tied to NGC 4258 (shared anchor with SH0ES/CCHP).
  SOURCE: Jensen et al. 2025, "The TRGB-SBF Project. III. Refining the HST SBF Distance Scale Calibration with JWST", arXiv:2502.15935
  QUOTE: "This new calibration, along with improved optical color measurements from PanSTARRS and DECam, gives an updated value ofH0 = 73.8 ± 0.7 (statistical) ±2.3 (systematic) km s−1 Mpc−1 that is virtually identical to the SBF Hubble constant measured by Blakeslee et al. (2021)."
  ACCESS: full-text
  STATUS: preprint (accepted for ApJ per INSPIRE DOI 10.3847/1538-4357/addfd6)
  SETTING: analysis
  CONFIDENCE: high
- [RE-19] CLAIM: Geometric anchors in the SH0ES ladder: adding the SMC (15 late-type detached eclipsing binaries, HST Cycle 30 GO-17097 Cepheids) as a fourth anchor gives H0 = 73.17 ± 0.86 km/s/Mpc (SMC alone 74.1 ± 2.1), a 5.8 sigma tension with CMB+LCDM, and a Cepheid metallicity term gamma = -0.234 ± 0.052 mag/dex. This 73.17 is the SH0ES 4-anchor value that supersedes R22's 73.04 ± 1.04 as the SH0ES headline (it uses the same 42 SNe Ia and Pantheon+); Riess 2025 (RE-11) updates it again with JWST Cepheids to 73.49 ± 0.93. The H0DN fit with the SMC added (V07) gives 73.314 ± 0.789.
  SOURCE: Breuval et al. 2024, "Small Magellanic Cloud Cepheids Observed with the Hubble Space Telescope Provide a New Anchor for the SH0ES Distance Ladder", arXiv:2404.08038 (journal reference not checked)
  QUOTE: "With the SMC as the only anchor, we find H 0 =74.1 ± 2.1 km s−1 Mpc−1. Combining these four geometric distances with our HST photometry of SMC Cepheids, we obtain H0 = 73.17 ± 0.86 km s−1 Mpc−1. ... we find γ = −0.234 ± 0.052 mag dex−1."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high
- [RE-20] CLAIM: JAGB: the CCHP/Lee et al. JWST JAGB result is 67.80 ± 2.17 (stat) ± 1.64 (sys) (8 calibrators, RE-05), whereas an independent SH0ES-side JAGB 2.0 analysis (Li et al. 2025, ApJ 988, 97; three JWST programs, six more hosts, nine SNe Ia) finds H0 = 73.3 ± 1.4 (stat) ± 2.0 (sys) km/s/Mpc, with the systematic dominated by differences across NGC 4258 calibrating fields or their measures, and a ~4 km/s/Mpc swing depending on how the JAGB reference magnitude is measured (mode, mean, median, etc.). Separately, a ground-based JAGB test (Anand 2025) finds a sizable discrepancy between JAGB and space-based TRGB distances to nearby galaxies, contradicting the CCHP 1% agreement claim for that sample. The JAGB rung is thus method-dependent at the level of the entire CCHP-SH0ES gap.
  SOURCE: Li et al. 2025, "JAGB 2.0", arXiv:2502.05259; Anand 2025, "A Sizable Discrepancy in Ground-Based JAGB Distances to Nearby Galaxies", arXiv:2502.07882
  QUOTE: "Using the middle result of all JAGB measures to calibrate SNe Ia yields a Hubble constant ofH0 = 73.3 ± 1.4 (stat)±2.0 (sys) km/s/Mpc with the systematic dominated by apparent differences across NGC 4258 calibrating fields or their measures." / "Differences in the method used to measure the JAGB reference magnitude change the value of H0 by ∼ 4 km/s/Mpc."
  ACCESS: full-text
  STATUS: peer-reviewed (Li 2025); preprint (Anand 2025)
  SETTING: analysis
  CONFIDENCE: high
- [RE-21] CLAIM: Tully-Fisher (Cosmicflows-4, Boubel et al. 2024, MNRAS 533, 1550): H0 = 73.3 ± 2.1 (stat) ± 3.5 (sys) km/s/Mpc using all absolute-distance calibrators; the large systematic reflects inconsistencies between the Cepheid, TRGB, and other zero-point calibrations used to calibrate the TF relation, and the statistical term is limited by the small number of calibrators. In H0DN the TF data have excess dispersion (reduced chi2 = 1.47 when added), which is why TF is a variant only. Because TF is calibrated through the same Cepheid/TRGB hosts, it is not independent of the primary-indicator rungs.
  SOURCE: Boubel et al. 2024, "An improved Tully-Fisher estimate of H0", arXiv:2408.03660; H0DN arXiv:2510.23823 (Table 4)
  QUOTE: "Using all available absolute distance calibrators, we obtain𝐻0= 73.3±2.1(stat)±3.5(sys)kms −1Mpc−1, where the statistical uncertainty is dominated by the small number of galaxies with absolute distance estimates."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high
- [RE-22] CLAIM: Gaia is the anchor-side programme with a dated milestone: ESA lists Gaia DR4 (66 months of data) for 2 December 2026 and Gaia DR5 'not before the end of 2030' (10.5 yr). The Milky Way Cepheid anchor currently uses EDR3 parallaxes with a zero-point correction; a 2026 review notes that the bright Cepheids still show a residual parallax offset of roughly -14 ± 6 microarcsec (about 0.9% in distance) after the official correction, and that a conservative residual-parallax treatment in a broader prior reassessment (Hogas & Mortsell 2026) gives a lower combined H0 of about 70.6 ± 1.0 km/s/Mpc; DR4 is the planned cleaner test. H0DN without MW parallaxes (V10): 73.609 ± 0.929, so the MW anchor does not drive the H0DN baseline.
  SOURCE: ESA Gaia release schedule, https://www.cosmos.esa.int/web/gaia/release (WebFetch summary; page text fetched but the date line was not within the grep window); Chen & Wang 2026, arXiv:2606.26831 (review)
  SUMMARY: "Gaia DR4 is scheduled for 2 December 2026 ... Gaia DR5 ... 'not before the end of 2030' and will cover the complete 10.5 years of extended mission data." (WebFetch summary of the ESA page). The review: "a cleaner external test of this systematic requires the brighter-star astrometry and revised zero-point calibration expected from Gaia DR4."
  ACCESS: search-summary (date); full-text (review sentence)
  STATUS: secondary (date); preprint (review)
  CONFIDENCE: medium
- [RE-23] CLAIM: Projected sample-supply gains for the distance ladder (a review's own forecast, not a collaboration commitment): Rubin/LSST could move the Cepheid-hosted SN Ia calibrator set from the current 37 hosts (42 SNe Ia, ~2150 Cepheids in R22) toward 60-80 systems, with ~10^4 usable Cepheids, shrinking the finite-Cepheid statistical term by a factor ~2.2 and the SN calibrator statistical term from 0.020 mag to 0.015 mag (0.7% in H0) for 80 SNe Ia, before shared systematics; Roman would put the enlarged stellar samples on a homogeneous near-infrared system; Gaia DR4/DR5 plus the LMC DEB distance would test Cepheid/RR Lyrae/Mira/TRGB/JAGB zero points to ~0.5%, the level needed for a 1% network.
  SOURCE: Chen & Wang 2026, "Distance-ladder Measurements of the Hubble Constant: Recent Progress, Systematics, and Prospects", Res. Astron. Astrophys. 26, 084003, arXiv:2606.26831
  QUOTE: "This can move the calibrator set from the current 37 SN Ia host galaxies with Cepheids toward a plausible 60–80 systems and, as a longer-term target, order 100; it could also increase the usable Cepheid sample toward nearly10 4 stars."
  ACCESS: full-text
  STATUS: peer-reviewed (review; forecasts are the authors' own scaling)
  SETTING: analysis
  CONFIDENCE: medium
- [RE-24] CLAIM: Time-delay cosmography forecast and error-budget targets (Treu 2026 review): with data quality comparable to the current JWST programme, about 40 time-delay lenses should suffice for 1% precision on H0 in flat LCDM (Birrer & Treu 2021); the review's per-lens error-budget table gives current random errors of 1-6% (time delay), 3% (galaxy lens model), 3-5% (kinematics/dynamics), 3% (line of sight, galaxies), with per-lens bias goals of <0.3% each. Rubin/LSST is expected to discover ~40 lensed SNe Ia and ~80 lensed SNe II per year, and Roman's High Latitude Time-Domain Survey ~10 lensed SNe per year; Euclid, Rubin and Roman are expected to raise known lensed-quasar samples by orders of magnitude. The 11-lens TDCOSMO-2026 sample (RE-07) is at 3.0-3.3%, so the 1% target needs roughly 4x more precise lenses than today's per-lens yield allows; quote 'in the next decade', not a date.
  SOURCE: Treu 2026, "Cosmology with strong gravitational lenses", arXiv:2610.19598 (preprint review)
  QUOTE: "In flat ΛCDM breaking the 1% precision barrier is within reach. If data quality comparable to that achieved with the current JWST program can be achieved, samples comprising∼40 time delay lenses should be sufficient (Birrer and Treu, 2021)." / "the Legacy Survey of Space and Time (LSST) with Rubin is ex- pected to discover∼40 SNe Ia and∼80 Type II SNe ... per year ... Ap- proximately 10 SN/year are expected to be discovered by the Roman Space Telescope High Latitude Time-Domain Survey"
  ACCESS: full-text
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RE-25] CLAIM: LVK schedule (observing plan page, 15 October 2026 update): the detectors are in upgrade/commissioning; a six-month intermediate run IR1 is planned to start mid-January 2027 (two LIGO detectors, Virgo joining, KAGRA later); the long O5 run's 'plans and timeline ... are in discussion'. O4 ended in November 2025 (WebSearch summary), and GWTC-5.0 (236 sources) is the latest published cosmology analysis (RE-15). The siren H0 uncertainty is currently ~10-13% (RE-15); no LVK-stated H0 precision target or date for O5 was found.
  SOURCE: LIGO-Virgo-KAGRA observing plans page, https://observing.docs.ligo.org/plan/ (15 October 2026 update)
  QUOTE: "We are currently planning a six-month observing run, designated as IR1 (Intermediate Run 1), targeting a mid-January 2027 start. ... Plans and timeline for the fifth observing run (O5) are in discussion."
  ACCESS: full-text
  STATUS: secondary (collaboration web page)
  CONFIDENCE: high
- [RE-26] CLAIM: Roman Space Telescope launch was set by NASA for 30 August 2026 on Falcon Heavy, with a five-year primary mission (commitment: flight no later than May 2027). One news source reports the launch occurred on 30 August 2026; I could not confirm liftoff from a primary NASA page. Roman's relevance to H0 is the High Latitude Time-Domain Survey (SNe Ia and lensed SNe, ~10 lensed SN/year) and homogeneous near-infrared Cepheid/Mira/TRGB photometry in SN hosts; no collaboration-published target precision for an H0 programme was found.
  SOURCE: spacepolicyonline.com, "NASA Sets Launch Date for Roman Space Telescope"; sci.news launch report (found via WebSearch, not opened)
  SUMMARY: "NASA set an August 30, 2026 launch date for the Nancy Grace Roman Space Telescope, eight months earlier than originally planned ... NASA's commitment was flight no later than May 2027." (WebSearch summary)
  ACCESS: search-summary
  STATUS: secondary
  CONFIDENCE: low
- [RE-27] CLAIM: Sharing map (what is independent of what), assembled from the sources above. (i) Shared SN input: SH0ES R22/2024/2025, H0DN, Riess JWST papers and CCHP's Pantheon+ comparison all use Pantheon+ SN Ia photometry for the Hubble flow; CCHP's headline uses CSP B-band SNe (24 calibrators); H0DN's V22 (CSP, all 55 calibrators) gives 73.350 ± 0.963. (ii) Shared geometric anchor: NGC 4258 (Reid et al. 2019; H0DN quotes D = 7.58 ± 0.11 Mpc) enters SH0ES, CCHP (sole anchor), H0DN TRGB, JAGB, SBF-JWST (Jensen 2025) and MCP (Pesce 2020); the SBF, CCHP-TRGB, Li-JAGB and Mira routes are NOT independent of one another through this anchor. (iii) Shared data: H0DN is a combination of SH0ES, CCHP-type TRGB and other published data; SH0ES JWST papers re-observe the same SN hosts as CCHP in places (11 and 9 SNe in the matched subsets, RE-12). (iv) Independent of the SN rung: time delays (TDCOSMO, with a SN Omega_m prior only), masers (geometric), sirens. (v) TDCOSMO-2026 supersedes TDCOSMO-2025 and TDC4, and contains the H0LiCOW lenses.
  SOURCE: Synthesis of Casertano et al. arXiv:2510.23823 (Sect. 2, Fig. 18), Freedman et al. arXiv:2408.06153, Jensen et al. arXiv:2502.15935, Pesce et al. arXiv:2001.09213, Birrer et al. arXiv:2610.14781
  QUOTE: "Besides the M. J. Reid et al. (2019) measure atD= 7.58±0.11 Mpc (shown as grey band) we also tried increasing or decreasing the distance by±5% and 10% (black crosses). The result its a large internal inconsistency in the distance network (due to other geometric anchors) which is highly significant." (Casertano et al., Fig. 18 caption)
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: medium (synthesis; the quote supports only the NGC 4258 distance and its role in H0DN)

## Gaps
- Searched but not opened: Type II SN ladder (de Jaeger et al. 2022, Vogl et al. 2025), Mira variables (Huang et al. 2024), EDD TRGB (Anand et al. 2022), the Hogas & Mortsell 2026 reassessment (70.6 ± 1.0 is a secondhand figure from the Chen & Wang review, not verified at the source), the Scolnic et al. 2025 Coma/DESI fundamental plane (abstract seen only), and the Riess 2025 'perfect host' systematic error budget table. Their values appear in H0DN variants (RE-03) but were not quoted separately.
- No source found stating a numerical error budget for R22 in the form 'largest items' (anchor, Cepheid zero point, SN calibrators, crowding). The R22 text gives the Cepheid Wesenheit zero point M_H,1^W = -5.894 ± 0.017 mag (~0.8% in distance; via the Chen & Wang review quoting R22), a ~20% uncertainty on the JWST crowding correction (Riess 2025), and 0.176 ± 0.035 mag for the tension; the dominant remaining terms (NGC 4258 ~1.5% distance, SN calibrator statistics 0.13/sqrt(42) = 0.020 mag) come from the review's arithmetic and not from the R22 table.
- Blinding: only TDCOSMO (blind, with formal unblinding 23 Sept 2026) and H0DN (votes before computing H0) have documented procedures that I could quote. I found no blinding statement for SH0ES R22 or CCHP; R22 only offers artificial-Cepheid images for blind tests by others. Not claimed as absent in the experiments, only as absent from the text I searched.
- Not found: a primary, collaboration-stated target precision and date for (a) a CCHP or SH0ES JWST Cycle 4/5 H0 programme, (b) the ELT time-delay follow-up, (c) Roman H0 forecasts, (d) LSST lensed-quasar/lensed-SN H0 timeline. The numbers in RE-23, RE-24 are review-level projections. No JWST cycle proposal pages were opened.
- Superseded values identified: SH0ES R22 73.04 ± 1.04 by Breuval 2024 73.17 ± 0.86 (4 anchors) and Riess 2025 73.49 ± 0.93 (JWST+HST Cepheids) / 73.18 ± 0.88 (with TRGB); Freedman 2019 TRGB 69.8 (HST) by the 2025 70.39; Blakeslee 2021 SBF by Jensen 2025; TDC4 and TDCOSMO-2025 by TDCOSMO-2026; GWTC-4.0 by GWTC-5.0; Pesce 2020 only provisionally by Stiskalek 2026 (preprint); H0DN 73.50 by the Roy Choudhury corrected-Pantheon+ update (73.264 ± 0.806 or 73.139 ± 0.791) as a third-party recomputation.
- Access: lit_search INSPIRE worked; arXiv endpoint timed out repeatedly; fetch_text worked on arXiv PDFs and abs pages. Facets on early-universe H0 values (Planck, SPT, ACT, DESI) are left to quantitative, so the 67.24 ± 0.35 and 68.51 ± 0.58 figures here are quoted only as H0DN used them.
