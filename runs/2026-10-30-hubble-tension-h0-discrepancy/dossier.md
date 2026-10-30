# Dossier: The Hubble tension, local (~73) versus early-universe (~67–68) H0
status: final

Units: H0 in km s⁻¹ Mpc⁻¹ (written km/s/Mpc); distances in Mpc or h⁻¹ Mpc; magnitudes in mag; ages in Gyr; neutrino masses in eV; angles dimensionless. Uncertainties are 68% unless a source says otherwise, and they are quoted as each source gives them (stat, sys and σ_SN kept separate; asymmetric errors kept). Refs: RT = theory, RQ = quantitative, RC = critiques, RE = engineering, RF = frontier. "Not source-checked" means the facet had a check file but the checker did not list that claim. ACCESS labels are carried over from the research files without change.

## 1. Established

- [D-01] The CMB measures the acoustic angular scale almost independently of the model: 100θ_* = 1.0411 ± 0.0003 (0.03%), Planck 2018 TT,TE,EE+lowE. H0 is a model-dependent late-Universe parameter inferred under base ΛCDM. The "geometric degeneracy" (Ω_K or w0 changes H0 at fixed θ_*) is broken mainly by adding BAO. So "the CMB measures H0" is false in the strict sense (premise 3). (refs: RT-16, RQ-05) peer-reviewed, full-text.
- [D-02] Three CMB experiments with largely independent instruments (Planck, ACT DR6, SPT-3G D1) each give a low H0 under flat ΛCDM, between 66.5 and 67.6 km/s/Mpc alone; their combination CMB-SPA gives 67.19 ± 0.38 km/s/Mpc. Values are in §2 (D-41 to D-45). Note: the statement that this rules out a Planck-only systematic (foregrounds, A_L) is the researcher's inference, not the SPT paper's (RC-15 check note). (refs: RQ-01, RQ-02, RQ-05, RQ-06, RC-15) peer-reviewed, full-text.
- [D-03] BAO measure H(z)·r_d and D(z)/r_d, and uncalibrated SNe fix the shape of D(z). Together they constrain the product r_d·H0: β_BAO ≡ c/(r_s^drag H0) = 29.54 ± 0.406 (BOSS BAO + Pantheon, 2019 data, 5-point spline H(z), zero curvature). A local H0 of about 73 therefore implies a small r_d. The Cepheid-calibrated empirical r_s is about 7% below the Planck-ΛCDM r_s (2.6σ in Bernal et al., as cited by Knox & Millea), robust to the choice of CMB dataset (Aylor et al., as cited). (refs: RT-01, RT-02) peer-reviewed, full-text.
- [D-04] Within ΛCDM the r_s-shrinking routes fail. (a) ω_b would have to nearly double for a 7% reduction of r_s, which BBN abundances contradict. (b) Raising ω_m gives δr_s/r_s ≃ −¼ δω_m/ω_m, but shifts the equality multipole by 3 δr_s/r_s (about 21% for 7%), which the CMB spectra rule out. It also gives a *lower* H0 today unless D_A is separately reduced. (c) Pure ΔN_eff: r_s ∝ (1+R_ν)^−1/2 with R_ν = (7/8)(4/11)^(4/3) N_eff needs N_eff ≈ 4.2 for 7%. (refs: RT-03, RT-04, RT-05, RT-17) peer-reviewed, full-text.
- [D-05] Recombination changes big enough to cut r_s by 7% are expected to "wreak havoc" on the damping tail. Knox & Millea state this as an expectation, not a proof. The CMB limit they cite on a varying α is δα/α = (0.7 ± 2.5)×10⁻³ (older data). The least-unlikely solutions raise the expansion rate in the decade of scale factor just before recombination, and these are "tightly constrained" by photon diffusion and acoustic driving. (refs: RT-06, RC-40 [not source-checked]) peer-reviewed.
- [D-06] SH0ES does not measure H0 directly. It measures the SN Ia peak absolute magnitude M_B, calibrated via Cepheids to geometric anchors, and converts it to H0 through the Pantheon(+) magnitude–redshift relation at 0.023 < z < 0.15. A late-time H(z) "solution" must therefore be tested against the SN magnitude–redshift relation and BAO, not imposed through an H0 prior. A sudden phantom ("hockey-stick") transition at z < 0.1 cannot reconcile the ladder M_B with the M_B needed to fit SN+BAO+CMB. In magnitudes the SH0ES R22 gap is 0.176 ± 0.035 mag in 5 log H0 against Planck+ΛCDM 67.4 ± 0.5 (5.0σ). (refs: RT-08, RC-43, RE-09) peer-reviewed.
- [D-07] The inverse distance ladder (BAO r_d plus uncalibrated SNe Ia) gives H0 ≈ 67 km/s/Mpc without assuming flat ΛCDM at late times. Its r_d is calibrated from the CMB (ω_b-based), so it is not independent of early-universe physics (anchor D-48). The SN-cosmology systematics considered by Popovic et al. move the inverse-ladder H0 by < 0.1 km/s/Mpc. A −0.3 mag shift recovers only H0 = 70.96 km/s/Mpc (checker note). (refs: RQ-07, RQ-08) peer-reviewed, full-text.
- [D-08] BAO+BBN, with no CMB anisotropies, gives H0 = 68.50 ± 0.58 km/s/Mpc (DESI DR2, ΛCDM). This is an early-universe-type value that does not use the CMB power spectra. (refs: RQ-03, RE-01) preprint (DESI DR2), full-text.
- [D-09] SH0ES JWST NIRCam photometry of more than 1000 Cepheids in NGC 4258 and 5 SN hosts agrees with HST: mean distance difference −0.01 ± 0.03 mag. Unrecognised crowding that grows with distance is rejected at 8.2σ. Across JWST Cycles 1–2 (19 hosts, 24 SNe Ia) no HST bias is seen. These are SH0ES-team analyses of SH0ES-selected data. They test photometry only, not Cepheid physics, SN standardisation or anchors. (refs: RC-01, RC-02, RE-11, RF-06) Riess 2024 peer-reviewed (journal ref not checked); Riess 2025 peer-review status unconfirmed (see §7).
- [D-10] Cosmic variance of local H0 in ΛCDM N-body simulations is σ(H0^loc) = 0.31 km/s/Mpc for an SH0ES-2016-like SN selection at 0.023 < z < 0.15. That is a "nearly negligible fraction" of the ~6 km/s/Mpc gap. A void explanation needs a ~20σ deviation, i.e. δ ≈ −0.8 on 120 h⁻¹ Mpc, which is incompatible with ΛCDM large-scale structure. (refs: RT-10, RT-11, RC-42) Wu & Huterer 2017 peer-reviewed; Huterer & Wu 2023 preprint chapter.
- [D-11] The SN luminosity distance–redshift relation (1295 SNe Ia, Pantheon+Foundation+CSP) is inconsistent at 4–5σ with LTB voids of |δ| > 20%. The 5σ bound is δ < 27% on scales larger than 69 h⁻¹ Mpc (sharp-edged LTB void, 2019 SN sample). (refs: RC-20 [not source-checked]) peer-reviewed, abstract.
- [D-12] The DESI DR2 evolving-dark-energy (w0wa) fits move the CMB+BAO(+SN) H0 *down*, away from 73 (anchor D-51). DESI DR2 favours dark energy crossing from phantom at high z to quintessence-like at low z, which "implies a lower value of the Hubble constant". (refs: RQ-04, RT-22) DESI preprint; Pang et al. peer-reviewed.
- [D-13] ACT DR6 extended-model fits find no evidence for self-interacting dark radiation, early-universe variation of constants, EDE, primordial magnetic fields or modified recombination. "Models introduced to increase the Hubble constant ... are not favored by our data." Fitted without a SH0ES prior, these models reach only 69.1–69.9 km/s/Mpc (anchor D-52). (refs: RC-34, RC-35 [not source-checked], RQ-11) ACT DR6 paper (JCAP per INSPIRE; published version not verified).
- [D-14] EDE theory: a scalar field obeying φ̈ + 3Hφ̇ + dV/dφ = 0, frozen until H falls below its effective mass near z_c, then diluting faster than matter. It is parametrised by f_EDE(z_c), log10 z_c and θ_i. Its potential needs fine-tuned cancellations, and it has a "why then" coincidence with matter–radiation equality. Without a SH0ES prior, EDE was not favoured in the pre-ACT-DR6 data (Planck + BAO + Pantheon). It gives only an upper limit (best fit f = 0.088, h = 0.706). With the SH0ES prior it gives f_EDE = 0.109 +0.030/−0.024 and h = 0.715 ± 0.009, which is "at face value in tension" with the no-SH0ES result. (refs: RT-13, RT-14, RC-22 [not source-checked]) review.
- [D-15] SH0ES R22 dust and colour variants are small levers. Host-specific R from Hahn et al. raises H0 by 0.8 km/s/Mpc. Discarding Cepheid colour raises it by 2%. The full Cepheid-reddening correction is ~0.03 mag (~1.5%). R22's own fit numbering is internally inconsistent (p.43 vs p.50). (refs: RE-10) peer-reviewed, full-text.
- [D-16] Mass-sheet degeneracy (MSD) dominates the time-delay error budget. Marginalising it with a kinematics-constrained λ_int raised the uncertainty from 2% to 8% for the same 7 lenses: 74.2 ± 1.6 km/s/Mpc with assumed profiles versus 74.5 +5.6/−6.1 km/s/Mpc with the MSD free. (refs: RE-08) stated in a 2026 preprint (TDCOSMO), full-text.
- [D-17] H0 Olympics (Schöneberg et al. 2022). This is a historical ranking on pre-2022 data (Planck 2018, BOSS, Pantheon, SH0ES 2021).
  - Criteria: (1) high H0 or M_B without a ladder prior; (2) a good combined fit; (3) ΔAIC improvement with SH0ES included.
  - Medals: varying m_e (flat or with curvature) won the only gold, reducing the tension to ≲ 2σ with curvature. EDE, NEDE, EMG and Majoron won silver; PMF and SIDR won bronze.
  - Late-time dark energy and decaying dark matter "cannot resolve the Hubble tension".
  - Adding RSD, cosmic chronometers and Lyα BAO makes PMF fail every criterion and puts m_e+Ω_k under "significant additional pressure".
  (refs: RT-21, RC-27 [not source-checked], RC-29 [not source-checked], RC-30 [not source-checked]) peer-reviewed.
- [D-18] Independent comparisons of sound-horizon-reduction models (Jedamzik, Pogosian & Zhao 2021) find that a model which only reduces r_* "can never fully resolve" the tension. Lower Ω_m h² conflicts with BAO, and higher Ω_m h² conflicts with weak lensing (bound in §4, D-73). (refs: RC-28) peer-reviewed, abstract.

## 2. Quantitative anchors

Values marked "same data" must not be combined with each other as independent measurements.

### Local (distance ladder and one-step)

| ID | Quantity | Value ± stat ± sys (units), as quoted | Conditions; current or preliminary; supersedes | Source refs | Access |
|---|---|---|---|---|---|
| D-20 | H0, SH0ES Cepheid–SN Ia (HST+JWST) | 73.49 ± 0.93 km/s/Mpc; with 35 TRGB calibrations added (55 SNe Ia): 73.18 ± 0.88 km/s/Mpc (same data, not independent) | JWST Cepheids in 19 hosts (24 SNe) + HST (37 hosts, 42 SNe Ia); Pantheon+ Hubble flow; "~6σ above ΛCDM+CMB". **Current**, but publication status unconfirmed (arXiv: "ApJ, submitted"; researchers cite ApJL 992 L34). **Supersedes** R22 73.04 ± 1.04 (3 anchors: MW Gaia EDR3, LMC DEBs, NGC 4258; 42 SNe; 277 Hubble-flow SNe 0.0233<z<0.15; R22 Cepheid+TRGB 72.53 ± 0.99), and Breuval 2024 73.17 ± 0.86 (SMC added as 4th anchor; SMC alone 74.1 ± 2.1; 5.8σ not seen by checker) = Riess 2024 HST full set 73.2 ± 0.9. SH0ES-team analysis. A corrected Pantheon+ (D-22) would shift Pantheon+ ladders by about −0.2 to −0.4 km/s/Mpc (researcher's inference, not recomputed for SH0ES). | RC-02, RE-11, RF-06, RE-09, RE-19, RE-12 | abstract (RC-02, RF-06); full-text (RE-11, RE-09, RE-19) |
| D-21 | SN Ia absolute magnitude M_B, ladder vs inverse ladder | Ladder (R22): M_B^0 = −19.253 ± 0.027 mag. Inverse ladder (DES-SN5YR + DESI DR1 BAO): −19.375 +0.018/−0.017 mag (4th-order cosmography); −19.394 +0.017/−0.016 mag (flat ΛCDM) | R22 Cepheid metallicity term Z_W = −0.217 ± 0.046 mag/dex (not individually checked); Breuval 2024 γ = −0.234 ± 0.052 mag/dex. Inverse-ladder r_d from CMB. These compilations use different SN systems; the difference is not computed here (statistician). | RE-09, RE-19, RQ-07 | full-text |
| D-22 | H0, Local Distance Network (H0DN) community combination | **Current:** 73.264 ± 0.806 km/s/Mpc (corrected Pantheon+ magnitudes; 6.85σ vs 67.24 ± 0.35); with full corrected Pantheon+ Hubble-flow treatment 73.139 ± 0.791 (6.82σ); DES-DOVEKIE Hubble flow 73.267 ± 0.828 (6.70σ; not checked) | Roy Choudhury 2026 (single author, ApJL 1008 L50 per researcher; status not checked): revised host-mass correction changes 114 of 1701 Pantheon+ rows, none of the calibrators, 52 of 277 Hubble-flow SNe; the Pantheon+ revision itself was not located. "Neither update resolves the Hubble tension." **Supersedes** H0DN baseline 73.50 ± 0.81 (1.09%; 7.1σ vs Planck+SPT+ACT 67.24 ± 0.35; 5.0σ vs DESI DR2 BBN+BAO 68.51 ± 0.58; A&A 708 A166). Baseline fixed by anonymous binding votes before H0 was computed. Calibrators: Cepheids (3 anchors) and TRGB (NGC 4258 only); tracers SNe Ia, SBF, Hubble-flow masers. **Not independent** of D-20, D-24, D-29, D-30: it combines SH0ES, CCHP-type TRGB, SBF and maser data. The Chen et al. 2026 seven-route covariance summary 73.30 ± 0.92 (5.6σ above Planck) uses the same data. | RE-16, RF-03, RE-01, RE-02, RF-02, RC-11, RF-24 | abstract (RE-16, RF-03, RC-11, RF-24); full-text (RE-01, RE-02, RF-02) |
| D-23 | H0DN leave-one-out variants (original Pantheon+, before the D-22 correction) | No Cepheids 72.509 ± 1.296 (matched-calibrator custom 72.873 ± 0.874); no TRGB/SBF 73.526 ± 0.878; no MW parallaxes 73.609 ± 0.929; no NGC 4258 73.084 ± 0.920; no SNe Ia 73.434 ± 1.795; no HST 73.754 ± 1.325; no JWST 73.002 ± 0.856; CSP SNe, all 55 calibrators 73.350 ± 0.963; no Cepheid metallicity correction 73.080 ± 0.801; Hubble-flow cut labelled "z > 0.06" 73.190 ± 0.862; 0.03–0.10 72.667 ± 0.862; +Tully–Fisher 73.957 ± 0.787 (χ²_ν = 1.47); everything 73.994 ± 0.697; SMC added 73.314 ± 0.789. Dispersion of variant centres 0.400 (all km/s/Mpc) | Variants of one dataset. Without Cepheids only 35 of 55 calibrators remain and TRGB rests on NGC 4258 alone. The V20 label is internally inconsistent in the paper (table "z>0.06", text "0.023≤z≤0.06"). The no-HST, no-MW and SMC variants were not individually checked. Replacing SNe Ia with galaxy-based indicators changes H0 by < 0.1 km/s/Mpc and doubles the error. | RE-03, RE-04, RE-19, RC-11, RF-02 | full-text |
| D-24 | H0, CCHP TRGB (HST+JWST) | 70.39 ± 1.22 (stat) ± 1.33 (sys) ± 0.70 (σ_SN) km/s/Mpc | 24 SN Ia calibrators, CSP B-band SNe, NGC 4258 sole anchor; CCHP says consistent with ΛCDM. **Current CCHP headline**; replaces CCHP 2019 HST TRGB 69.8 (supersession not checked). Internal variants: Pantheon+ B-band through SH0ES machinery 69.29 (11 cal.); CSP z > 0.025 69.81 +1.32/−1.29; 70.73 +1.21/−1.18 omitting SN 1981D (with 23 calibrators, z > 0.01, so it differs in two respects). | RC-06, RE-05, RE-06 | abstract (RC-06); full-text (RE-05, RE-06) |
| D-25 | H0, CCHP JWST-only TRGB | 68.81 ± 1.79 (stat) ± 1.32 (sys) km/s/Mpc (Table 5: ± 1.80) | 11 calibrators. Hoyt et al. 2026 (CCHP, JWST F115W, 10 hosts / 11 SNe): 68.4 < H0 < 69.6 across four SN photometry sets; extending to 24 SNe raises CSP-II by +0.8 (1.4σ) and Pantheon+ by +2 km/s/Mpc (3.1σ). Hoyt likely re-uses these JWST data; whether it supersedes 68.81 is not established. | RE-05, RC-09 | full-text / abstract |
| D-26 | H0, JAGB (overlapping data, two analyses) | CCHP JWST JAGB: 67.80 ± 2.17 (stat) ± 1.64 (sys) km/s/Mpc (8 cal.; error inflated ×1.45; Pantheon+ variant 68.80). SH0ES-side JAGB 2.0 (Li 2025): 73.3 ± 1.4 (stat) ± 2.0 (sys) km/s/Mpc (15 galaxies, 18 SNe Ia, all JWST JAGB programmes) | **Same data in part; do not combine.** Li 2025: JAGB–HST Cepheid −0.03 ± 0.02 (stat) ± 0.05 (sys) mag; NGC 4258 two-field JAGB mode difference 0.11 ± 0.02 mag; ~4 km/s/Mpc swing with the reference-magnitude measure (not seen by checker). Li 2025 status: researchers cite ApJ 988, 97; arXiv says "submitted". Dispute in D-81. | RE-05, RC-10, RE-20, RF-16 | full-text / abstract |
| D-27 | H0, all HST/JWST TRGB SN calibrations (SH0ES-side) | 72.1–73.3 ± 1.8 km/s/Mpc depending on methodology | Li et al. 2026: 35 hosts with Pantheon+; the 11 hosts not in CCHP's 24 alone give 74.1 (2σ above the selected sample); +0.6 km/s/Mpc from a peculiar-velocity correction. Overlaps D-24/D-25 data. ApJ 997, 115 not confirmed (arXiv: submitted). | RC-08 | abstract |
| D-28 | H0, JWST distance-limited sample (SH0ES, D ≤ 25 Mpc, 16 SNe) | Cepheids 73.4 ± 2.1; JAGB 72.2 ± 2.2; TRGB 72.1 ± 2.2; three-method 72.6 ± 2.0 km/s/Mpc (HST Cepheids, same galaxies: 72.8) | SH0ES says ΔH0 ≈ 2.5 km/s/Mpc between CCHP-JWST and full HST is "entirely consistent with differences in sample selection". HST predicts 71.2 for the CCHP-selected subset and 73.6–73.9 for the SH0ES-selected one (not individually checked). Linearity of HST distances 0.994 ± 0.010 (distance-dependent bias excluded ~7σ). Shares data with D-20, D-24–D-26. | RC-07, RE-12 | abstract / full-text |
| D-29 | H0, SBF ladder | 73.8 ± 0.7 (stat) ± 2.3 (sys) km/s/Mpc | Jensen et al. 2025: HST SBF zero point recalibrated with JWST TRGB on NGC 4258; independent of Cepheids and SNe Ia; sys dominated by the few calibrators. **Current**; **supersedes** Blakeslee 2021 73.3 ± 0.7 ± 2.4. Garnavich 2023 (SBF→SN) 74.6 ± 0.9 ± 2.7 (73.3 ± 1.0 ± 2.7 after fast-decliner correction; not seen by checker). Shares the NGC 4258 anchor. | RE-18 | full-text |
| D-30 | H0, Tully–Fisher (Cosmicflows-4) | 73.3 ± 2.1 (stat) ± 3.5 (sys) km/s/Mpc | Boubel 2024; sys from inconsistent Cepheid/TRGB zero points; calibrated through the same hosts, so not independent of the primary rungs; excess dispersion in H0DN. | RE-21 | full-text |
| D-31 | H0, strong-lensing time delays (TDCOSMO-2026) | 71.1 +2.4/−2.3 km/s/Mpc (3.3%, includes MSD); 3.0% with SLACS+SL2S | 11 lensed quasars, 9 with resolved kinematics (6 JWST-NIRSpec); blind, unblinded 23 Sep 2026; flat ΛCDM with DES-Dovekie Ω_m prior (DESI-BAO prior consistent); robust across oΛCDM, wCDM, w0waCDM. **Preprint (submitted to PRD).** **Supersedes** TDCOSMO-2025 (8 lenses, 71.6 +3.9/−3.3; with SLACS+SL2S 74.3 +3.1/−3.7) and TDC4/Birrer 2020 (74.5 +5.6/−6.1; 67.4 +4.1/−3.2 with SLACS). Contains the H0LiCOW lenses. The researcher's σ-distances (1.7σ from H0DN, 1.5σ from CMB) were contradicted by the checker; the statistician must recompute them. | RE-07, RF-01, RE-08 | full-text / abstract |
| D-32 | H0, megamasers | 71.6 ± 3.7 km/s/Mpc (statistical only) | **Preliminary** (preprint). Stiskalek et al. 2026 reanalysis of the MCP data from spot catalogues: 5 galaxies (NGC 4258 treated separately) with non-linear Manticore-Local peculiar velocities. PV corrections lower H0 by 0.8–1.4 (linear) or 1.6–2.1 (non-linear) km/s/Mpc; NGC 4258 distance 7.558 ± 0.073 (stat) Mpc. **Supersedes as a reanalysis** Pesce 2020 73.9 ± 3.0 (6 galaxies, no PV correction, fixed 250 km/s PV error; range 71.8–76.9) and the earlier Boruah 2021 reanalysis 70.1 ± 2.9. Shares NGC 4258 with every ladder. | RE-14, RE-13 | full-text |
| D-33 | H0, gravitational-wave sirens | 71.7 +9.4/−7.5 km/s/Mpc (median, 68%) | GWTC-5.0, 236 sources, includes GW170817 bright siren and galaxy-catalogue information; uncertainty 22.0% smaller than GWTC-4.0. **Preprint.** **Supersedes** GWTC-4.0 75.4 +12.8/−9.1 (68.3%) [+24.5/−13.3 at 90%] (142 of 218 sources), which itself contains GW170817 (70 +12/−8). | RE-15, RF-13 | abstract |
| D-34 | H0, TRGB two-rung (EDD, ~400 hosts, LMC + NGC 4258) | 68.4 ± 5.9 (equal weighting) or 72.3 ± 2.6 (evidence weighting) km/s/Mpc; field-to-field scatter 5.2 km/s/Mpc | **Preliminary** (Stiskalek et al. 2026 preprint). The limit is peculiar-velocity reconstruction variance (80 Manticore-Local realisations): "cannot yet arbitrate". | RF-21 | abstract |
| D-35 | H0, SN-standardisation reanalyses of the SH0ES/Pantheon+ data | Wojtak & Hjorth 2025 (two SN populations): 70.59 ± 1.15 (differing reddening allowed); 71.45 ± 1.03 ("most conservative") km/s/Mpc; discrepancy reduced 30–50% (3.5–2.2σ) | **Same data as D-20**; a contested alternative standardisation, not an independent measurement. The same group's 2024 extinction model gave 70.5 ± 1 (5.2σ → 2.8σ; ΔBIC = −11). Their 2022 colour-slope analysis: R_B ~ 4.6 ± 0.4 in calibrators recovers SH0ES at c = 0 and Planck at c ~ −0.13 (not source-checked). | RC-05, RC-04, RC-03 | abstract |
| D-36 | Local-ladder corrections from flows and background | Laniakea flow model: ΔH0 ≈ +0.6 (SN Ia), +1.4 (SBF) km/s/Mpc (raises local H0). Analysing the ladder in DESI w0wa backgrounds: up to −2.5; constrained −1.1 ± 0.38 (DESI+CMB), −0.5 ± 0.1 (DESI+CMB+SNIa) km/s/Mpc. H0DN q0 −0.55 → −0.50 changes H0 by < 0.1 (not checked) | Giani 2024 (with erratum), effective ellipsoid, Pantheon+ and 63 SBF galaxies; Turner & Huterer 2026 preprint. | RC-38, RE-17, RF-04 | abstract |
| D-37 | Local cosmic variance of H0 | σ(H0^loc) = 0.31 km/s/Mpc (ΛCDM N-body, R16 SN geometry); most underdense sub-volume δ = −0.16 at 120 h⁻¹ Mpc gives ΔH0 = 0.65 ± 0.13. Empirical σ_H0 = 0.60% (local structure) vs ~0.42% predicted (Kenworthy 2019) | The R16 SN selection, not the 2022 sample. Derived: the linear-theory void contrast needed for an 8.3% shift is δ ≈ −0.47 (f = 0.525, top-hat; rough); the SH0ES−Planck gap of 5.6 km/s/Mpc is ≈ 18σ of 0.31 [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/theory_rs_scaling.py]. | RT-10, RC-42, RC-20, RT-19 | full-text / abstract |

### Early universe, inverse ladder and related parameters

| ID | Quantity | Value ± stat ± sys (units), as quoted | Conditions; current or preliminary; supersedes | Source refs | Access |
|---|---|---|---|---|---|
| D-40 | Acoustic scale | 100θ_* = 1.0411 ± 0.0003 (0.03%) | Planck 2018 TT,TE,EE+lowE; weakly model-dependent. | RT-16, RQ-05 | full-text |
| D-41 | H0, Planck alone, ΛCDM | **Current:** PR4 HiLLiPoP+LoLLiPoP TTTEEE 67.64 ± 0.52 km/s/Mpc (σ8 = 0.8070 ± 0.0065; S8 = 0.819 ± 0.014; Ω_m = 0.3092 ± 0.0070; τ = 0.058 ± 0.006). Per spectrum: TT 67.89 ± 1.11, TE 68.49 ± 0.76, EE 68.49 ± 1.91 | **Supersedes** PR3 (Planck 2018, TT,TE,EE+lowE+lensing) 67.36 ± 0.54 (abstract 67.4 ± 0.5; Ω_m = 0.315 ± 0.007; σ8 = 0.811 ± 0.006), still the standard reference. PR3 with N_eff free: 66.3 ± 1.4. Planck in SPT Table I (with lensing, PR4 τ prior): 67.41 ± 0.49. Likelihood choice (Plik vs CamSpec-NPIPE) moves P-ACT from 67.62 ± 0.51 to 67.86 ± 0.48 (Jense 2026; not checked). | RQ-05, RQ-06, RQ-01 | full-text |
| D-42 | H0, ACT DR6, ΛCDM | ACT alone (with lensing, PR4 τ prior): 66.51 ± 0.64; P-ACT (ACT+Planck): 67.62 ± 0.50; P-ACT-LB (+CMB lensing + DESI DR1 BAO): 68.22 ± 0.36; with DESI DR2: 68.43 ± 0.27 km/s/Mpc | P-ACT agrees with DESI DR2 at 1.6σ. The BAO-included values are not CMB-only. | RQ-02, RQ-01 | full-text |
| D-43 | H0, SPT-3G D1, ΛCDM | SPT-3G alone 66.66 ± 0.60 (6.2σ from SH0ES); SPT+ACT 66.59 ± 0.46; SPT+Planck 67.07 ± 0.38 km/s/Mpc | 2019+2020 data, 4% of sky, TT/TE/EE + lensing, PR4 τ prior. PRD 113 083504 per INSPIRE (not re-checked). | RQ-01, RC-15 | full-text |
| D-44 | H0, CMB-SPA (SPT+ACT+Planck), ΛCDM | 67.19 ± 0.38 km/s/Mpc (6.4σ from SH0ES); Ω_m = 0.3175 ± 0.0055; r_d = 147.00 ± 0.24 Mpc; σ8 = 0.8137 ± 0.0037; n_s = 0.9679 ± 0.0033; age 13.805 ± 0.014 Gyr (age not re-opened by checker) | Tightest CMB constraint; **correlated** with D-41–D-43. H0DN quotes "67.24 ± 0.35 from Planck+SPT+ACT (Eq. 54 of Camphuis et al.)". The two numbers are not reconciled in the inputs: probably a different combination, but unverified. CMB vs DESI DR2 in ΛCDM: 2.8σ in the Ω_m–h r_d plane. | RQ-01, RC-15, RE-01 | full-text |
| D-45 | DESI DR2 BAO, ΛCDM | Ω_m = 0.2975 ± 0.0086; h r_d = 101.54 ± 0.73 Mpc (correlation −0.92); DESI+BBN H0 = 68.50 ± 0.58 (Table V 68.51 ± 0.58); DESI+BBN+θ_* 68.45 ± 0.47; DESI+CMB 68.17 ± 0.28 km/s/Mpc | **Preprint.** BAO–CMB discrepancy 2.3σ (1.9σ in DR1), along Ω_m h³ = const. DESI is consistent with θ_*, so the discrepancy is in Ω_m, not r_s. Supersedes DR1 values. | RQ-03, RQ-15, RE-01 | full-text |
| D-46 | BBN baryon density | (D/H)_P = 2.527 ± 0.030 × 10⁻⁵; η10 = 5.931 ± 0.051 | Cooke, Pettini & Steidel 2018; within 2σ of Planck. The claim that newer d(p,γ)³He rates shift ω_b by ~1σ (Pitrou et al. 2021) rests on an INSPIRE title only: unverified. | RQ-10 | full-text |
| D-47 | Sum of neutrino masses | DESI DR2+CMB < 0.064 eV (ΛCDM), < 0.16 eV (w0wa) (95%); ACT DR6 paper: < 0.089 eV (95%, P-ACT-LB = Planck+ACT+lensing+DESI DR1, Eq. 33; corrected from "ACT alone") and < 0.082 eV (95%, abstract; combination not stated in the inputs); DES Y6 joint < 0.14 eV (95%) | RQ-15 misattribution corrected. The 0.082 vs 0.089 difference is unresolved (likely different combinations). | RQ-15, RQ-11, RC-34, RQ-09 | full-text / abstract |
| D-48 | H0, inverse distance ladder | 67.19 +0.66/−0.64 km/s/Mpc (4th-order cosmography); 67.67 +0.69/−0.68 (flat ΛCDM; Ω_m = 0.322 ± 0.012) | DES-SN5YR + DESI DR1 BAO; r_d from the CMB. Earlier values (Aubourg 2015 67.3 ± 1.1; Macaulay 2019 67.8 ± 1.3) are older data, not checked. Popovic 2026: SN systematics < 0.1 km/s/Mpc. A drift of ~0.2 mag in dμ/dz (implying flat-ΛCDM Ω_M = 0.23, "10σ") would be needed for 74; the drift and Ω_M figures were not confirmed (garbled abstract). | RQ-07, RQ-08 | full-text |
| D-49 | H0 without the sound horizon (DESI DR1) | Zaborowski et al. 2026 (uncalibrated post-reconstruction BAO + θ_*): 69.2 +1.3/−1.4 (CMB lensing×unWISE), 70.3 +1.4/−1.2 (DES Y3 6x2pt), 69.6 +1.3/−1.8 (CMB lensing + DES Y5 SNe) km/s/Mpc. arXiv:2411.16677 (lensing + uncalibrated SNe + Lyα + BBN ω_b prior): 66.7 +1.7/−1.9 (DESY5), 67.9 +1.9/−2.1 (Pantheon+), 67.8 +2.0/−2.2 (Union3); 2.2–3.0σ from SH0ES; 18 of 25 mock 68% intervals covered the truth | Both use DESI DR1, so they are **correlated**. Zaborowski reports "somewhat higher values ... relative to our previous work". Whether 2411.16677 is that previous work is not established in the inputs (author list unverified), so the older set is not declared superseded. Earlier ACT lensing + unWISE + Pantheon+: 64.3 +2.1/−2.4. Reeves 2026 multiprobe: 70.0 ± 4.4 (not source-checked). | RC-44, RF-07, RQ-13, RC-16 | abstract / full-text |
| D-50 | H0 from the equality scale (BOSS DR12) | 65.1 +3.0/−5.4 (Pantheon Ω_m prior); 65.6 +3.4/−5.5 (uncalibrated-BAO Ω_m); 70.6 +3.7/−5.0 with BAO-lensing equality results (km/s/Mpc) | Philcox et al. 2021; pre-DESI. Only the first value differs from SH0ES at 95%. | RQ-12 | full-text |
| D-51 | DESI DR2 evolving dark energy | DESI+CMB: w0 = −0.42 ± 0.21, wa = −1.75 ± 0.58, 3.1σ; with SNe 2.8σ (Pantheon+), 3.8σ (Union3), 4.2σ (DESY5). w0waCDM H0: 63.6 +1.6/−2.1 (DESI+CMB); 67.51 ± 0.59; 65.91 ± 0.84; 66.74 ± 0.56 km/s/Mpc. wCDM: DESI+CMB 69.51 ± 0.92 (w = −1.055 ± 0.036); with SNe 67.97 ± 0.57, 68.01 ± 0.68, 67.34 ± 0.54 | **Preprint.** SNe Unite (Pantheon+ + DES-SN5YR, 2884 SNe; preprint): with CMB+DES+DESI BAO, (Ω_m, w0, wa) = (0.305 ± 0.004, −0.861 +0.044/−0.042, −0.60 +0.17/−0.19); 3.3σ (MAP) / 3.1σ (max-likelihood) but "only weak preference" in Bayesian evidence (Ω_m values not checked). | RQ-04, RF-22 | full-text / abstract |
| D-52 | ACT DR6 extended models (no SH0ES prior) | EDE (axion-like n=3): P-ACT f_EDE < 0.12 (95%), H0 = 69.3 +0.9/−1.5; P-ACT-LB f_EDE < 0.12, H0 = 69.9 +0.8/−1.5 (vs ΛCDM 68.2 ± 0.4); ACT alone f_EDE < 0.088, H0 = 67.5 +0.9/−1.7. PMF 69.1 ± 0.5; modified recombination 69.6 ± 1.0 (P-ACT-LB). N_eff = 2.86 ± 0.13 (2.89 ± 0.11 with He and D); N_idr < 0.134 | BOSS instead of DESI BAO lowers these H0 by 1–1.5 km/s/Mpc. MAP Δχ² for EDE = 4.3 (1.2σ, P-ACT) and 6.6 (1.7σ, P-ACT-LB) (not checked). | RQ-11, RC-34 | full-text |
| D-53 | EDE bounds and fits, other data | Planck NPIPE: f_EDE < 0.061 (95%, z ∈ [10³, 10⁴]), 66.9 < H0 < 69.5 (95%), 3.7σ residual vs SH0ES, robust to prior volume. SPT-3G alone f_EDE < 0.12 (95%), 2.3σ; SPT+ACT+Planck f_EDE < 0.070 (95%), 3.6σ; +DESI DR2 f_EDE = 0.055 +0.024/−0.047, 2.6σ (not individually checked); SPT+DESI 0.081 +0.037/−0.052, 1.5σ. Poulin et al. 2026 (Planck ℓ<1000 + ACT DR6 + lensing + Pantheon+ + DESI DR2, profile likelihood, no SH0ES): f_EDE = 0.09 ± 0.03, H0 = 71.0 ± 1.1, ~2σ residual; Δχ² = −35.4 with SH0ES | Axion-like EDE throughout. The Khalife (SPT) authors attribute the DESI-induced shift to the DESI–CMB discrepancy in ΛCDM. Multiprobe (Reeves 2026): EDE 70.5 ± 1.2 at 2.3σ (not source-checked). Dispute in D-83. | RC-12, RC-14, RF-11, RC-13, RF-10, RC-16 | abstract |
| D-54 | S8 and weak lensing | KiDS-Legacy S8 = 0.815 +0.016/−0.021 (0.73σ from Planck; not re-fetched). DES Y6 3x2pt S8 = 0.789 ± 0.012, Ω_m = 0.333 +0.023/−0.028; 1.8σ full-space and 2.6σ in S8 from Planck+ACT+SPT (3x2pt-alone numbers verified via RQ-09, not RF-23). DES Y6 + CMB + DESI DR2 + DES SNe + SPT clusters: S8 = 0.806 +0.006/−0.007, Ω_m = 0.302 ± 0.003, h = 0.683 +0.003/−0.002 | DES Y6 is a preprint; the joint h is a ΛCDM fit to all data, not a one-side measurement. The S8 tension is now ~1–3σ depending on survey. | RQ-09, RF-23 | full-text / abstract |
| D-55 | Age of the Universe from globular clusters | t_U = 13.81 ± 0.25 (stat) ± 0.23 (sys) Gyr (Part IV, multiple populations, after a conservative formation delay); metal-poor GC mean age 13.61 ± 0.25 ± 0.23 (not checked) | **Preprint** (first author and title unverified). **Supersedes** Part III t_U = 13.57 +0.16/−0.14 (stat) ± 0.23 (sys) Gyr. In ΛCDM t_U ≈ 13.857 Gyr × (68/H0). H0 = 73 gives a Universe ~1 Gyr (7%) younger, 2σ below the GC age ("two sigma does not a tension make"). | RQ-14 | full-text |
| D-56 | Required r_d / r_s reduction (derived) | Fixed H0·r_d: 7.67%, 7.72%, 8.30% for local H0 = 73.0, 73.04, 73.5 vs 67.4 km/s/Mpc. Pure-N_eff equivalent: 4.21 (7.0%), 4.34 (7.7%), 4.59 (9.0%). ω_m route: δω_m/ω_m ≈ 28–31%, ℓ_EQ shift ≈ 21–23% | Arithmetic on Knox–Millea scalings, verified by the checker; 67.4 is a Planck-2018 placeholder (CMB-SPA 67.19 would raise these slightly; not computed here) [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/theory_rs_scaling.py]. | RT-18, RT-05 | full-text (calc) |
| D-57 | Tension significances as quoted by sources (not recomputed) | SH0ES R22 vs Planck 67.4 ± 0.5: 5.0σ. SPT-3G alone vs SH0ES: 6.2σ; CMB-SPA vs SH0ES: 6.4σ. H0DN vs Planck+SPT+ACT: 7.1σ; vs DESI DR2 BBN+BAO: 5.0σ. Corrected H0DN: 6.85σ. Riess 2025: "~6σ". Chen et al.: 5.6σ vs Planck. TDCOSMO companion (preprint): a no-SN late-universe combination is 3.7σ from Planck, and 2.7σ after excluding the local distance ladder entirely | Each source picks its own pair of values; the statistician owns the recomputation with correlations. | RE-09, RQ-01, RE-01, RE-16, RF-06, RF-24, RF-18 | full-text / abstract |

## 3. Contested or conflicting

- [D-80] **SH0ES vs CCHP: what makes the ~2.5–3 km/s/Mpc difference.**
  - CCHP: TRGB-only 70.39 (D-24) and JWST-only 67.8–68.8 (D-25, D-26), "consistent with ΛCDM" (RC-06, RE-05).
  - SH0ES side: the difference is calibrator *sample selection* (RC-07, RE-12). The 11 hosts left out of CCHP's 24 alone give 74.1, and a peculiar-velocity correction adds 0.6 (RC-08, D-27). JWST Cepheid, JAGB and TRGB on a distance-limited 16-SN set give 72.6 ± 2.0 (D-28).
  - CCHP's own Hoyt et al.: the result also depends on the SN photometry compilation. Pantheon+ shifts up by +2 km/s/Mpc (3.1σ) when the sample is extended, against +0.8 for CSP-II. They call for "independent analyses of low-redshift SNe" (RC-09).
  - H0DN treats the split as a sample/method choice inside a covariance network: removing Cepheids or TRGB "has minimal effect" (RC-11, D-23).
  - No CCHP reply to Li 2026, Riess 2024/2025 or H0DN was found (RF-25, search-summary; RC Gaps).
- [D-81] **JAGB.**
  - CCHP JWST JAGB 67.80 ± 2.17 ± 1.64 against SH0ES-side JAGB 2.0 at 73.3 ± 1.4 ± 2.0, on overlapping data (D-26).
  - Li 2025 finds a 0.11 ± 0.02 mag field-to-field JAGB difference within NGC 4258 (RC-10, RE-20, RF-16).
  - Anand 2025 (preprint) finds ground-based JAGB distances offset from HST TRGB by Δμ = 0.17 ± 0.04 (stat) ± 0.06 (sys) mag (9% in distance, HST TRGB further). This challenges the CCHP claim of 1% TRGB–JAGB agreement for that local sample (RF-15, RE-20). No CCHP rebuttal was found.
- [D-82] **SN standardisation between calibrators and the Hubble flow.**
  - Wojtak & Hjorth argue for different colour/extinction or two-population behaviour, giving 70.5–71.5 (D-35; RC-03, RC-04, RC-05). They note "no obvious physical basis" for the 2022 colour-slope difference.
  - Against: Brout & Riess 2023 (SH0ES-side review, preprint) say H0 is "robust" to dust-model uncertainties. It predates the 2025 two-population model (RC-37, not source-checked).
  - Against: Huang et al. 2025 report a 5σ intercept tension between second- and third-rung Pantheon+ SNe. Removing it gives 73.4 ± 1.0 from the first two rungs, which "rules out third-rung SN systematics" (RC-32). **Unverifiable**: the checker could not confirm the numbers in the abstract.
  - Dong et al. 2026 (preprint): host peculiar-velocity corrections move a forward Pantheon+ H0 from 74.30 +1.18/−1.20 to 71.37 +1.23/−1.18 km/s/Mpc, and cut the "cosmological intercept" tension from 6.8σ to 3.9σ (backward: 60.83 → 63.25, 7.3σ → 4.3σ) (RF-20). This sits against the ~6.7–6.9σ H0DN/Roy Choudhury result (D-22), which uses a different method.
- [D-83] **Is EDE still open after ACT DR6, SPT-3G and DESI DR2?**
  - Closed side: Planck NPIPE f_EDE < 0.061, 3.7σ residual, robust to prior volume (RC-12). SPT+ACT+Planck f_EDE < 0.070, 3.6σ (RC-14). ACT DR6 "not favored" (RC-34, RC-35). ACT+SPT close the electron-density-fluctuation variant, giving 69.3 ± 0.5 (RF-08).
  - Open side: Poulin et al. 2026 find f_EDE = 0.09 ± 0.03 and H0 = 71.0 ± 1.1 (profile likelihood) with a ~2σ residual. This uses Planck only at ℓ < 1000 and no SPT, and Bayesian analyses show strong prior-volume effects (RC-13, RF-10). eROSITA clusters + external data give f_EDE = 0.10 +0.04/−0.03 (~3.2σ) and H0 = 71.4 ± 1.4 (RF-09; accepted by A&A).
  - Mediating reading: the SPT authors say the DESI-driven EDE preference is "a manifestation of the discrepancy ... between DESI and CMB experiments" (RC-14). Reeves 2026 find that EDE (70.5 ± 1.2) and w0wa cannot resolve both the H0 and the BAO–CMB issues at once (RC-16, not source-checked). RC-45 is the critiques researcher's own synthesis (secondary).
  - Even the pro-EDE values (69.9–71.4) stay below SH0ES/H0DN fitted without a SH0ES prior (D-52, D-53).
- [D-84] **Local void.**
  - Against: Kenworthy 2019 excludes |δ| > 20% at 4–5σ (RC-20). Wu & Huterer and Huterer & Wu need δ ≈ −0.8 (~20σ) (RT-10, RT-11, RC-42). Camarena et al. 2022: ΛLTB is favoured only for SNe in 0.023 < z < 0.15, and the full sample removes the preference (RT-12). The Cai et al. 2026 decade review says a void "has long been ruled out" (RC-21; that quote was not checked).
  - For: Banik et al. 2026 (preprint, minority) keep the KBC void, linking it to a low-z BAO α_iso < 1 anomaly and predicting rapid convergence to CMB-consistent expansion for z ≳ 0.2 (RC-21).
- [D-85] **Evolving dark energy and SN samples.** Efstathiou 2025 finds a ~0.04 mag low-/high-z offset between SNe common to DES5Y and Pantheon+, and evolving-DE evidence ranging from ~3.9σ (DES5Y) to ~2.5σ (Pantheon+). Vincenzi et al. 2025 attribute 43% of the offset to scatter/host modelling and 38% to selection functions; the DES evidence falls only to 3.3σ, and they "confirm the validity" of DES-SN5YR (RC-39). This is unresolved, and neither paper is about H0 directly.
- [D-86] **Anchors.** Mörtsell et al. (pre-2022 data, individual extinction laws): per-anchor H0 ranges from 68.1 ± 3.5 to 76.7 ± 2.0. The Milky Way anchor is in 2.1–3.1σ tension with NGC 4258 and the LMC. Wesenheit H0 = 73.2 ± 1.3; individual-law H0 = 73.9 ± 1.8 (RC-36, not source-checked; journal reference from memory). Efstathiou 2020: a 0.1–0.15 mag Cepheid P–L intercept bias would resolve the tension, the anchor tension and SH0ES-vs-TRGB (RC-41, not source-checked). That is superseded in detail by the SMC anchor and the JWST tests (D-09, D-20). A 2026 review reports a residual MW Cepheid parallax offset of about −14 ± 6 µas (~0.9% in distance) after the official correction. It also gives Högås & Mörtsell 2026 a combined H0 ≈ 70.6 ± 1.0, a second-hand figure not verified at source (RE-22). Against: H0DN without MW parallaxes is 73.609 ± 0.929 (D-23).
- [D-87] **DESI–CMB Ω_m discrepancy, size by test.** DESI: 2.3σ (BAO vs CMB, ΛCDM). SPT: 2.8σ (CMB-SPA vs DESI DR2 in the Ω_m–h r_d plane). ACT: 1.6σ (P-ACT vs DESI DR2 parameters). It lies along Ω_m h³ = const and does not by itself pull H0 toward 73 (RQ-03, RQ-02, RQ-01, RQ-15). A 2026 preprint (Zaldarriaga) argues that the leading BAO+SN distance mode measures Ω_m h², and that most of the tension in ΛCDM extensions sits there (RT-23; frontier).
- [D-88] **Cepheid selection effects.** Percival 2026 (preprint) finds 1.3–2.3σ evidence for residual Cepheid selection in SN host galaxies. Its corrections are −1.4 (Cepheid cut-off), −0.2 (SN selection) and −1.0 km/s/Mpc (equal-volume distance prior); "together, these effects substantially reduce the inferred tension". The effects need not add (RF-19). No SH0ES reply was found.

## 4. Constraints: theorems, bounds, no-go results, each with its assumptions

- [D-70] **Inverse-ladder / M_B no-go for late-time solutions.**
  - Statement: BAO + uncalibrated SNe fix r_d·H0 (β_BAO = 29.54 ± 0.406). With the standard r_d, any late-time H(z) gives H0 ≈ 67. A late-time change cannot raise H0 to the ladder value without breaking the SN magnitude–redshift relation. The real conflict is in M_B.
  - Assumptions: standard pre-recombination physics (r_d from CMB or BBN ω_b); SN Ia standardisation that does not evolve with z; flat geometry (Knox–Millea spline; Efstathiou dynamics-free); FRW homogeneity; BAO measured with a fiducial cosmology.
  - Data vintage: 2019–2021 (Pantheon, BOSS/eBOSS) for Knox–Millea and Efstathiou 2021; DES-SN5YR + DESI DR1 for Camilleri 2025; current SN systematics for Popovic 2026.
  - Efstathiou 2026 (preprint) says the DESI w0wa hint "does not alter this conclusion".
  - Escapes: a change in M_B or G_eff itself (D-92), or a non-standard r_d.
  (refs: RT-02, RT-08, RC-43, RQ-07, RQ-08, RC-17, RF-05)
- [D-71] **Cosmic-chronometer / PAge late-time no-go** (Cai et al. 2022a,b). Both early- and late-time scenarios are "largely ruled out". Late-time new physics is "strongly disfavored" once growth data are added (S8, S12).
  - Assumptions: PAge cosmic-age parametrisation; cosmic-chronometer calibration with no sound-horizon prior; 2021-vintage data.
  - It does not address changes of M_B or G at low z.
  (refs: RC-19, RC-23 [not source-checked])
- [D-72] **Sound-horizon scalings in ΛCDM** (Knox & Millea). Reaching a 7% r_s cut needs:
  - ω_b × ~2, excluded by BBN;
  - δω_m/ω_m ≈ 28%, which shifts ℓ_EQ by 3δr_s/r_s and is excluded by the CMB spectra;
  - N_eff ≈ 4.2.
  Assumptions: ΛCDM pre-recombination physics, fixed θ_s, simple scaling arguments (not full Boltzmann fits). For the run's targets see D-56. (refs: RT-03, RT-04, RT-05, RT-18)
- [D-73] **Sound-horizon-only no-go** (Jedamzik, Pogosian & Zhao 2021): "any model which only reduces r_⋆ can never fully resolve the Hubble tension while remaining consistent with other cosmological datasets".
  - Assumptions: the model changes only pre-recombination physics (EDE, extra radiation, neutrino-sector changes, PMF, varying constants as r_* reducers); BAO and galaxy weak-lensing data of 2020–21.
  - It does not apply to models that also change post-recombination physics.
  - Later partial-resolution results (D-52, D-53) are consistent with it.
  (refs: RC-28)
- [D-74] **N_eff and dark-radiation bounds.** ACT DR6 gives N_eff = 2.86 ± 0.13 (2.89 ± 0.11 with primordial He and D) and N_idr < 0.134. Assumptions: free-streaming N_eff in ΛCDM+N_eff; ACT DR6 + Planck + lensing + DESI DR1 BAO. Planck PR3 with N_eff free gives H0 = 66.3 ± 1.4, so freeing N_eff does not raise H0 in Planck-only fits. An LBT helium measurement (2026 preprint) "precludes most but not all" self-interacting-light-relic and varying-constant models via BBN; which models survive is not extracted. (refs: RQ-11, RC-34, RQ-05, RC-25)
- [D-75] **EDE bounds (axion-like, 95% CL, no SH0ES).**
  - Planck NPIPE: f_EDE < 0.061 for z_c ∈ [10³, 10⁴], giving 66.9 < H0 < 69.5.
  - SPT+ACT+Planck: f_EDE < 0.070.
  - SPT alone and P-ACT(-LB): < 0.12. ACT alone: < 0.088.
  - Assumptions: the axion-like potential (n = 3 for ACT); Bayesian posteriors are prior-volume sensitive (profile likelihoods are wider: D-53, Poulin).
  - Collateral objections: the S8 tension (now weaker, D-54), the BOSS EFT full-shape analysis (not opened), and the "why then" coincidence.
  (refs: RC-12, RC-14, RQ-11, RT-13, RC-22)
- [D-76] **Varying m_e / modified recombination.**
  - Perturbative m_e(z) modifications "fully resolve" the tension with Planck + ACT DR6 (+lensing). They cannot once DESI DR2 BAO is added, because raising H0 this way "generically lowers Ω_m" (Lee et al. 2026, preprint).
  - Sekiguchi & Takahashi 2021 give general necessary conditions and a time-varying m_e model that also fits BAO and SNe. The checker notes they report 72.3 +2.7/−2.8 in Ω_kΛCDM with no local prior.
  - The varying-α limit δα/α = (0.7 ± 2.5)×10⁻³ comes from older data.
  - ACT DR6 finds no evidence for early varying constants; its modified-recombination H0 = 69.6 ± 1.0 (P-ACT-LB).
  (refs: RC-24, RT-20, RT-06, RQ-11)
- [D-77] **Local-void bounds.**
  - ΛCDM cosmic variance σ = 0.31 km/s/Mpc. Assumptions: N-body halo catalogues; SH0ES R16 SN geometry and weights.
  - The needed void is δ ≈ −0.8 on 120 h⁻¹ Mpc, about 20σ.
  - SN Hubble diagram excludes |δ| > 20% at 4–5σ (δ < 27% at 5σ on > 69 h⁻¹ Mpc). Assumptions: LTB void with a sharp edge, 1295 SNe (2019).
  - ΛLTB loses its preference over ΛCDM with the full SN sample. Assumption: the observer is at the centre (non-Copernican).
  (refs: RT-10, RT-11, RC-20, RT-12, RC-42)
- [D-78] **Cepheid photometry bound** (SH0ES JWST). HST−JWST = −0.01 ± 0.03 mag; distance-growing crowding is rejected at 8.2σ; the NGC 3447/3447A component offset is σ < 0.03 mag; HST distance linearity is 0.994 ± 0.010 (~7σ against a 0.07 mag/mag bias).
  - Assumptions: SH0ES photometry pipelines and host selection; the bound covers photometric bias only.
  - Compare with the 0.1–0.15 mag P–L intercept bias that Efstathiou 2020 said would be needed (D-86).
  (refs: RC-01, RC-02, RC-07, RE-11, RE-12, RC-41)
- [D-79] **Stellar-age bound.** t_U(GC) = 13.81 ± 0.25 ± 0.23 Gyr. In ΛCDM at fixed Ω_m, H0 = 73 gives an age ~7% younger, 2σ below the GC age.
  - Assumptions: ΛCDM; a model-dependent formation delay; GC isochrone systematics (0.23 Gyr).
  - It is a weak (2σ) preference for low H0.
  (refs: RQ-14)
- [D-79a] **Planck A_L / lensing anomaly.** The PR3 preference for A_L > 1 and for non-GR Σ_0, γ_0 (~2.5σ) is "significantly reduced or disappear[s]" in PR4. Within 1σ of GR for HiLLiPoP/LoLLiPoP; within 1.5σ (Σ_0) and 2σ (γ_0) for CamSpec. PR4 H0 stays low (D-41). Assumption: MG parametrisation (Σ_0, γ_0). (refs: RC-31 [not source-checked])
- [D-79b] **Required sizes for ladder systematics.** Cepheid P–L intercept bias needed: 0.1–0.15 mag (Efstathiou 2020, 2020 data; RC-41, not source-checked). Total ladder–CMB gap: 0.176 ± 0.035 mag in 5 log H0 (R22 vs Planck 67.4 ± 0.5; RE-09). Published small levers: dust/colour 0.03 mag (~1.5%) (RE-10); metallicity term dropped → H0DN 73.080 (D-23). The mechanist owns the full comparison.

## 5. Frontier and speculative (labelled; not established)

- [D-90] **TDCOSMO 2026 companion** (preprint, submitted to PRL). The tension with Planck is robust to dropping any one of the SN-, Cepheid- or TRGB-based methods. A no-SN late-universe combination is 3.7σ from Planck, and "Even after completely excluding the LDL ... the tension with Planck persists at the 2.7σ level". The comparison is with Planck alone. (RF-18)
- [D-91] **Sirens + time delays via the distance sum rule** (Xiong et al. 2026, preprint): 83.78 +12.53/−10.23 km/s/Mpc (TDCOSMO-2025 hierarchical MSD) vs 75.42 +3.74/−4.66 (H0LiCOW method). The lens-modelling choice moves H0 by ~8 km/s/Mpc at fixed data. It shares data with D-31 (TDCOSMO-2025) and D-33 (GWTC-4). (RF-14)
- [D-92] **Speculative late-time M_B/G_eff transition** (Marra & Perivolaropoulos 2021, peer-reviewed proposal). μ_G = G_eff/G_N = 1 for z ≲ 0.01 and ≈ 0.9 above. That raises the Chandrasekhar mass and lowers SN M_B at z ≳ 0.01 by ≈ 0.2 mag. Δμ_G ≈ −0.12 and the "9%, > 4σ" wording are not checked. It is claimed to help growth (S8) too. It is the kind of model that escapes D-70 by changing M_B rather than H(z). Huang et al. (RC-32, unverifiable) claim to rule out a late-time M_B transition. (RT-09)
- [D-93] **Combined early+late model** (Wang et al. 2025, preprint). w0waCDM+EDE fitted to Planck+ACT+SPT+DESI+Pantheon+**+SH0ES** allows a quintessence-like w0+wa ≥ −1 at 1σ, with Δχ² ≲ −14 against w0waCDM without EDE. The SH0ES prior is included. Related: Pang et al. 2025 report that in w0waCDM+EDE fits with the SH0ES prior, the dynamical-DE preference falls to 1.5σ/1.4σ/2.4σ for Pantheon+/Union3/DESY5. **Corrected scope:** these numbers are for w0waCDM+EDE, not for CMB+DESI+SNe with only a SH0ES prior. (RF-12, RT-22)
- [D-94] **eROSITA eRASS1 cluster-count EDE detection** (Strunk et al. 2026, accepted by A&A per arXiv comment; status corrected from "preprint"). 5259 clusters (0.1 < z < 0.45 subsample used). Counts alone give f_EDE < 0.3. With primary CMB + BAO + lensing + external data (no ladder): f_EDE = 0.10 +0.04/−0.03 (~3.2σ), H0 = 71.4 ± 1.4 km/s/Mpc. (RF-09)
- [D-95] **Small-scale electron-density fluctuations** (Lynch et al. 2026, preprint). With Planck + a ladder prior: H0 = 71.1 ± 0.7, preferred over ΛCDM. With ACT DR6 + SPT-3G D1 and the same prior: 69.3 ± 0.5, with no preference. Variance of the density contrast < 0.21 (95%; not checked). The TE damping tail drives the closure. (RF-08)
- [D-96] **Primordial magnetic fields** (Jedamzik & Pogosian 2020, peer-reviewed; Jedamzik et al. 2023 chapter, preprint). Baryon clumping speeds up recombination and shrinks r_s. The required field is "of the right order" for galactic, cluster and void fields. The fits used a local-H0 dataset. ACT DR6 gives H0 = 69.1 ± 0.5 (D-52), and PMF fails all H0-Olympics criteria once more data are added (D-17). (RT-15, RC-33)
- [D-97] **Local void revival** (Banik et al. 2026, preprint; minority): see D-84. **ΛLTB** (Camarena et al. 2022): explains the tension only if the observer sits near the centre of a non-Copernican inhomogeneity, and it is disfavoured by the full SN sample. Inhomogeneous/backreaction (timescape) cosmologies were not covered by any facet. (RC-21, RT-12)
- [D-98] **Distance-mode reframing** (Zaldarriaga 2026, preprint). The leading SVD mode of DESI BAO + SN distances is "to high accuracy, a measurement of Ω_m h²". BAO constrain it more tightly than the CMB does, and most of the extended-model tension lies in it. w0wa opens a second mode with no significant tension, and curvature is the only other extension that opens a new direction. This bears on premise 8. (RT-23)
- [D-99] **Ladder systematics under active development.**
  - Percival 2026: Cepheid selection (D-88).
  - Dong et al. 2026: intercept tension with peculiar velocities (D-82).
  - Stiskalek et al. 2026: maser reanalysis (D-32) and TRGB two-rung ladder (D-34).
  - Roy Choudhury 2026: corrected Pantheon+ (D-22; peer-reviewed per researcher, status not checked).
  - Turner & Huterer 2026: background dependence (D-36).
  - All 2026 preprints except Roy Choudhury; none is yet answered by SH0ES in the literature found.
- [D-99a] **Varying m_e under DESI DR2** (Lee et al. 2026, preprint): see D-76. **LBT helium** (Loverde et al. 2026, preprint): see D-74.

## 6. Unknowns and gaps, with the papers to request

**Papers to request:** none. No researcher flagged a `PAPER TO REQUEST`; all relevant papers had free arXiv copies.

Gaps that matter for the answer:
- **Replies not found:** no CCHP reply to Li 2026, Riess 2024/2025 or H0DN; no SH0ES reply to Wojtak & Hjorth 2025, Percival 2026 or Dong 2026. Would settle whether the SH0ES–CCHP gap is selection, SN photometry or method (D-80, D-82, D-88).
- **Independent low-z SN calibration:** the Pantheon+ vs CSP calibration shift that Hoyt flags (D-25) has no independent analysis in the inputs. The Pantheon+ host-mass revision behind Roy Choudhury (D-22) was not located at source.
- **SH0ES error budget:** no R22 table of the "largest items". Only the review's arithmetic is available (NGC 4258 ~1.5% in distance; SN calibrator statistics 0.020 mag; Cepheid zero point M_H,1^W = −5.894 ± 0.017 mag second-hand) (RE Gaps).
- **Blinding:** documented only for TDCOSMO and H0DN (procedural). No statement was found for SH0ES R22 or CCHP.
- **Not covered by any facet:**
  - Type II SN ladder (de Jaeger 2022, Vogl 2025);
  - Miras (Huang 2024);
  - EDD TRGB (Anand 2022), beyond the Stiskalek preprint;
  - DESI fundamental plane;
  - SN host-mass/environment step (Rigault 2015/2020; Dixon 2025, arXiv:2408.01001);
  - Gaia parallax zero-point critique of the MW anchor at source;
  - Högås & Mörtsell 2026 (70.6 ± 1.0, second-hand only);
  - SH0ES metallicity-term bounds;
  - cosmic chronometer H0 values;
  - timescape/backreaction cosmologies;
  - interacting dark energy;
  - modified-gravity G_eff / screened Cepheid models;
  - formal SIDR models and the N_eff phase-shift argument;
  - BOSS EFT full-shape EDE bounds (Ivanov, Hill, D'Amico 2020);
  - Poulin 2019, Hill 2020, Bernal 2016, Aylor 2019 and Lemos 2019 at source.
- **Early-side items not retrieved:**
  - a post-2024 BAO+BBN H0 with updated d(p,γ)³He rates; the Pitrou 2021 claim is unverified (D-46);
  - a DESI DR2 full-shape / equality-scale H0;
  - Simons Observatory σ(H0) and σ(N_eff) forecasts;
  - a primary source for the CMB-S4 cancellation (search-summary only);
  - SPT-3G Ext-10k and ACT final-release dates;
  - a DESI DR3 date (absence, search-summary);
  - the PR4 CamSpec primary H0;
  - the reconciliation of CMB-SPA 67.19 ± 0.38 with H0DN's quoted 67.24 ± 0.35 (D-44);
  - the ACT Σm_ν 0.082 vs 0.089 eV combinations (D-47);
  - whether arXiv:2411.16677 is the "previous work" that Zaborowski 2026 updates (D-49).
- **Schedules:**
  - Gaia DR4 on 2 Dec 2026 (verified; ESA). DR5 "not before end of 2030" (wording not seen by checker).
  - LVK IR1 planned for mid-January 2027; the O5 timeline is "in discussion".
  - Roman launch on 30 Aug 2026 (search-summary only; unverified).
  - LiteBIRD launch at the end of JFY2032 (Q1 2033).
  - Euclid DR1: first tranche Nov 2026, full release mid-2027, no cosmology before mid-2027 (blog source).
  - DESI: data to end-2028, DESI-II 2029–2035 (search-summary).
  - No collaboration-stated H0 target precision or date was found for the SH0ES/CCHP JWST programmes, ELT time-delay follow-up, Roman H0, LSST lensed SNe or LVK O5.
  - Review-level forecasts only: ~40 time-delay lenses for 1% (Treu 2026); 37 → 60–80 Cepheid calibrator hosts with Rubin (Chen & Wang 2026); Rubin ~40 lensed SNe Ia and ~80 lensed SNe II per year, Roman ~10 per year (counts not seen by checker). (RQ-16, RE-22–RE-26, RF-17, RF-25)
- **Not computed in the inputs:**
  - the proper correlated combination of local results and of early results, and every tension significance (statistician; D-57 lists only source-quoted values);
  - r_d reductions against the CMB-SPA 67.19 rather than 67.4 (D-56).

## 7. Source-quality notes

**Superseded values (each with what replaced it):**
- SH0ES: R22 73.04 ± 1.04 → Breuval 2024 73.17 ± 0.86 (= Riess 2024 HST full set 73.2 ± 0.9) → Riess 2025 73.49 ± 0.93 (Cepheids, HST+JWST) / 73.18 ± 0.88 (with TRGB) (D-20).
- H0DN baseline 73.50 ± 0.81 → corrected-Pantheon+ recomputation 73.264 ± 0.806. This is a third-party, single-author recomputation; the Pantheon+ revision itself was not located (D-22).
- CCHP 2019 HST TRGB 69.8 → CCHP 2025 70.39 ± 1.22 ± 1.33 ± 0.70 (D-24).
- SBF: Blakeslee 2021 73.3 ± 0.7 ± 2.4 → Jensen 2025 73.8 ± 0.7 ± 2.3 (D-29).
- Time delays: TDC4/Birrer 2020 and TDCOSMO-2025 → TDCOSMO-2026 71.1 +2.4/−2.3 (preprint) (D-31).
- Masers: Pesce 2020 73.9 ± 3.0 (and Boruah 2021 70.1 ± 2.9) → Stiskalek 2026 71.6 ± 3.7 (stat only; preprint). This is a reanalysis of the same data, so it is the anchor, but it is preliminary (D-32).
- Sirens: GWTC-4.0 75.4 +12.8/−9.1 → GWTC-5.0 71.7 +9.4/−7.5 (preprint; includes GW170817) (D-33).
- Planck: PR3 67.36 ± 0.54 → PR4 67.64 ± 0.52 (D-41).
- DESI DR1 → DR2 BAO (D-45).
- GC ages: Part III 13.57 → Part IV 13.81 ± 0.25 ± 0.23 Gyr (D-55).
- Wojtak & Hjorth 2024 70.5 ± 1 → 2025 70.59 ± 1.15 / 71.45 ± 1.03. This is the same group's newer SN model; both are alternative analyses of the SH0ES data (D-35).
- Pre-ACT-DR6 EDE numbers (2023 review, Murgia 2021 [RC-26, not source-checked], H0 Olympics) are superseded as current bounds by D-52, D-53 and D-75.

**Dropped (contradicted):** the RF-01 statement that TDCOSMO-2026 lies "about 1.7σ below H0DN and about 1.5σ above Planck+SPT+ACT". The checker recomputed ≈ 0.95σ and ≈ 1.66σ (naive, uncorrelated). The value 71.1 +2.4/−2.3 is kept; the σ-distances are left to the statistician.

**Corrected (misattributed or status-wrong):**
- RQ-15: Σm_ν < 0.089 eV is P-ACT-LB, not "ACT DR6 alone" (D-47).
- RT-22: the 1.5σ/1.4σ/2.4σ reductions apply to w0waCDM+EDE fits with the SH0ES prior (D-93).
- RF-09: eROSITA EDE is accepted by A&A, not an unrefereed preprint (D-94).
- Unconfirmed peer-review labels: Riess 2025 "Perfect Host" (arXiv: "ApJ, submitted"; cited as ApJL 992 L34; RC-02, RE-11, RF-06); Li 2025 JAGB 2.0 (arXiv: submitted; cited as ApJ 988, 97); Li 2026 TRGB (arXiv: submitted; cited as ApJ 997, 115); ACT DR6 papers (JCAP per INSPIRE, not verified); Roy Choudhury ApJL 1008 L50 (not checked).
- Internal inconsistencies in sources: H0DN V20 label (D-23); R22 Fit 22/23 numbering (D-15); the CCHP 69.81 vs 70.73 variants differ in two respects, not one (D-24).
- RC-15's "Planck-only systematic cannot account for the gap" is the researcher's inference (D-02).
- RE-15's "22% smaller" could not be found by the engineering checker but was verified by the frontier checker ("reduction by 22.0%").

**Kept but unverifiable:**
- RC-32 (Huang 2025: 5σ intercept tension, 73.4 ± 1.0; numbers not found in abstract) (D-82).
- RE-26 (Roman launch; search-summary).
- RE-27 (sharing map; a synthesis whose components were checked, Reid 2019 7.58 ± 0.11 Mpc not seen).
- RF-25 (absence of a CCHP 2026 update and of DESI DR3; search-summary).
- RQ-10 Pitrou clause; RQ-08 dμ/dz and Ω_M = 0.23 details; RQ-16(c) CMB-S4 cancellation and (e) DESI timeline.

**Not source-checked** (critiques facet; claims kept, flagged where used): RC-03, RC-16, RC-18, RC-20, RC-22, RC-23, RC-26, RC-27, RC-29, RC-30, RC-31, RC-33, RC-35, RC-36, RC-37, RC-40, RC-41, RC-42, RC-44, RC-45 (20 of 45). RC-42 and RC-44 duplicate verified claims (RT-10, RF-07). RC-45 is a researcher synthesis (STATUS secondary) and is not used as evidence.

**Access shares:**
- Total claims in the inputs: 136 (RT 23, RQ 16, RC 45, RE 27, RF 25).
- Resting only on search summaries: 2 (RE-26, RF-25), ≈ 1.5%.
- Partly on search summaries: 2 more (RE-22 Gaia date, later verified by RF-17; RQ-16 parts c and e), ≈ 3% in total.
- Abstract-only: large. Most critiques claims (all but RC-29, RC-30, RC-34) and most frontier claims (all but RF-02 and RF-17). Quotes from these are abstract wording, not full text.
- RT-18, RT-19 and part of D-37/D-56 rest on this run's calculation [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/theory_rs_scaling.py], arithmetic verified by the checker.

**Correlations to respect (for the statistician):**
- NGC 4258 is a shared anchor of SH0ES, CCHP, H0DN-TRGB, JAGB, SBF-JWST and the masers.
- Pantheon+ is shared by SH0ES, H0DN and the CCHP Pantheon+ variants.
- H0DN and the Chen et al. summary combine the same data.
- The SH0ES JWST papers re-observe CCHP hosts.
- CMB-SPA contains Planck, ACT and SPT. ACT and SPT Table I columns share the PR4 τ prior.
- DESI DR1 enters D-48 and both D-49 sets.
- TDCOSMO-2026 contains the H0LiCOW lenses.
- GWTC-5.0 contains GW170817.

**Fringe excluded:** none labelled fringe. The Banik void revival is kept as a labelled minority preprint.

**Facets:** all five (theory, quantitative, critiques, engineering, frontier) present, each with a check file. None missing.

**Earlier runs:** none. The brief lists no relevant prior run, and no `prior/` material exists, so 0 claims were carried and 0 re-verified.
