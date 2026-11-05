# Research: frontier
status: final
Mandate: newest material (2025-2026) on either side of the Hubble tension, newest first, each with evidential status.
Access: lit_search INSPIRE ok, arXiv API timed out (blocked intermittently); fetch_text on arxiv.org/abs and arxiv.org/pdf worked; WebSearch used for Gaia DR4 date, CCHP and DESI DR3 absence checks

## Claims
- [RF-01] CLAIM: TDCOSMO 2026 (submitted 10 Oct 2026 to PRD, not yet refereed): 11 lensed quasars, blind analysis, flat LCDM with a DES-Dovekie SN Omega_m prior gives H0 = 71.1 +2.4 -2.3 km/s/Mpc (3.3%, includes mass-sheet degeneracy); adding SLACS+SL2S gives 3.0%; DESI-DR2 BAO prior in place of Dovekie gives consistent results; robust across open LCDM, wCDM, w0waCDM, w_phi CDM. Spatially resolved kinematics for 9 systems (6 with JWST-NIRSpec) vs 1 in the 2025 analysis. Lensing sits between the two sides (about 1.7 sigma below H0DN 73.50 using the quoted errors naively; about 1.5 sigma above Planck+SPT+ACT 67.24 +- 0.35, my arithmetic, statistician to confirm). Supersedes the TDCOSMO 2025 sample result for the headline lensing H0 (same collaboration, enlarged sample, improved methods).
  SOURCE: TDCOSMO Collaboration (Birrer et al.), 2026, "TDCOSMO 2026: A 3% measurement of the Hubble constant from strong lensing and stellar kinematics", arXiv:2610.14781 (submitted to PRD), https://arxiv.org/abs/2610.14781
  QUOTE: "In the flat $\Lambda$ cold dark matter ($\Lambda$CDM) cosmology, we find $H_0=71.1^{+2.4}_{-2.3}$ km.s$^{-1}$.Mpc$^{-1}$, a 3.3% uncertainty that accounts for the mass-sheet degeneracy. The SLACS and SL2S samples are in excellent agreement with the TDCOSMO-2026 sample, improving the precision on $H_0$ in flat $\Lambda$CDM to 3.0%."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  ARTIFACT: dataset "data and likelihoods will be made publicly available upon acceptance" (not yet released)
  CONFIDENCE: medium
- [RF-02] CLAIM: The Local Distance Network (H0DN) community consensus, A&A 708, A166 (2026), arXiv Oct 2025: covariance-weighted baseline H0 = 73.50 +- 0.81 km/s/Mpc (1.09%; 0.9% with all estimators); differs by 7.1 sigma from flat LCDM CMB (Planck+SPT+ACT, 67.24 +- 0.35 km/s/Mpc, Eq. 54 of Camphuis et al. 2025) and by 5.0 sigma from BBN+BAO (DESI DR2, 68.51 +- 0.58 km/s/Mpc). Baseline includes SNe Ia, SBF and masers as tracers; removing Cepheids gives 72.51 +- 1.30 (V08), baseline without TRGB and SBF gives 73.53 +- 0.88 (V09); replacing SNe Ia with galaxy-based indicators shifts H0 by <0.1 km/s/Mpc but doubles the uncertainty. With SN subsets: CSP-in-U24 / TRGB calibration only (27 SNe) gives 71.61 +- 1.53 (Pantheon+), i.e. the TRGB-only CSP route is lower. Over 100 authors including both Riess and Freedman-adjacent community members (CCHP team itself is not an author list member in the quoted abstract; verify).
  SOURCE: H0DN Collaboration (Casertano et al.), 2026, "The Local Distance Network: a community consensus report on the measurement of the Hubble constant at 1% precision", A&A 708, A166, arXiv:2510.23823, https://arxiv.org/pdf/2510.23823
  QUOTE: "The baseline result isH 0=73.50±0.81 km s−1 Mpc−1. Compared to early Universe+ΛCDM results, our result differs by 7.1σfrom the CMB anisotropies within flat ΛCDM, 67.24±0.35 km s −1 Mpc−1 from Planck+SPT+ACT (Eq. (54) of E. Camphuis et al. 2025) and 5.0σfrom BBN+BAO within flat ΛCDM from DESI DR2 (68.51±0.58 km s −1 Mpc−1"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  ARTIFACT: code and data products released ("We provide open-source software and data products")
  CONFIDENCE: high
- [RF-03] CLAIM: Roy Choudhury (ApJL 1008, L50, 2026; arXiv:2607.24443 v2, 15 Sep 2026) updates H0DN with corrected Pantheon+ (a revised host-mass correction changes 114 of 1701 rows; calibrator SNe unaffected, 52 of 277 Hubble-flow rows affected): H0 = 73.264 +- 0.806 km/s/Mpc (6.85 sigma vs CMB LCDM 67.24 +- 0.35) from magnitude corrections alone; 73.139 +- 0.791 (6.82 sigma) with the full corrected Pantheon+ Hubble-flow treatment; 73.267 +- 0.828 (6.70 sigma) using DES-DOVEKIE (220 SNe, 0.025<=z_HD<=0.151) on the H0DN scale. H0DN baseline was 73.499 +- 0.809. The author concludes "Neither update resolves the Hubble tension."
  SOURCE: Roy Choudhury, S., 2026, "Updated 1.1% Precision Values of the Hubble Constant with Corrected Pantheon+ and DES-DOVEKIE Type Ia Supernovae", ApJL 1008 L50, arXiv:2607.24443, https://arxiv.org/abs/2607.24443
  QUOTE: "Applying only these magnitude corrections, with the H0DN covariance, redshifts, and velocities unchanged, gives $H_0=73.264\pm0.806$ km s$^{-1}$ Mpc$^{-1}$ and a $6.85\sigma$ Hubble tension. This is our main baseline result and the update for the astrophysics community."
  ACCESS: abstract
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high
- [RF-04] CLAIM: Turner and Huterer (3 Jun 2026) show a local-distance-ladder H0 depends on the assumed low-z background: analysed with DESI-preferred w0wa models the ladder H0 can be up to 2.5 km/s/Mpc lower than with LCDM; after constraining those models with CMB and SNe the downward shift is 1.1 +- 0.38 km/s/Mpc (DESI+CMB) and 0.5 +- 0.1 km/s/Mpc (DESI+CMB+SNIa). This reduces the gap by well under 1 sigma-equivalent of the 0.8 km/s/Mpc H0DN error only in the DESI+CMB+SNIa case (0.5 km/s/Mpc against a ~6 km/s/Mpc gap).
  SOURCE: Turner & Huterer, 2026, "The DESI results impact the local determination of H0", arXiv:2606.05358, https://arxiv.org/abs/2606.05358
  QUOTE: "the downward shift is $1.1 \pm 0.38\,\mathrm{km\,s^{-1}Mpc^{-1}}$ (DESI + CMB) and $0.5 \pm 0.1\,\mathrm{km\,s^{-1}Mpc^{-1}}$ (DESI + CMB + SNIa)."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RF-05] CLAIM: Efstathiou (31 Jul 2026, 7 pp) argues the CMB-distance-ladder tension is a tension in SN Ia M_B, insensitive to the late-time expansion history, and that the DESI evolving-dark-energy hint does not alter this. Supports reframing premise 8 (M_B rather than H0) and disfavours late-time solutions.
  SOURCE: Efstathiou, G., 2026, "Late Time Dynamical Dark Energy and the CMB-Distance Ladder Tension", arXiv:2607.29562, https://arxiv.org/abs/2607.29562
  QUOTE: "This CMB-distance ladder tension is insensitive to the actual late time expansion history of the Universe. ... The tentative claim by the Dark Energy Spectroscopic Instrument collaboration for late time evolution of the dark energy equation of state does not alter this conclusion."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium

- [RF-06] CLAIM: SH0ES "Perfect Host" paper (Riess et al., ApJL 992, L34, 2025; arXiv Sep 2025): JWST Cycle 1-2 Cepheids in 19 SH0ES hosts (24 SNe Ia, >50% of the sample) show no bias relative to HST photometry; in the background-free companion NGC 3447A vs the spiral NGC 3447 there is no component-to-component offset (sigma<0.03 mag) and scatter falls to ~0.12 mag. Combined JWST (19 hosts, 24 SNe) + HST (37 hosts, 42 SNe) Cepheid H0 = 73.49 +/- 0.93 km/s/Mpc; adding 35 TRGB-based calibrations (HST and JWST; 55 SNe Ia total) gives H0 = 73.18 +/- 0.88 km/s/Mpc, "~6 sigma above the LambdaCDM+CMB expectation". This is SH0ES's own analysis (the authors are the Cepheid team), not an independent one.
  SOURCE: Riess et al., 2025, "The Perfect Host: JWST Cepheid Observations in a Background-free Type Ia Supernova Host Confirm No Bias in Hubble-constant Measurements", ApJL 992 L34, arXiv:2509.01667, https://arxiv.org/abs/2509.01667
  QUOTE: "Combining JWST Cepheid measurements in 19 hosts (24 SNe Ia) with HST data (37 hosts, 42 SNe Ia) yields H0 = 73.49 +/- 0.93 km/s/Mpc. Including 35 TRGB-based calibrations (from HST and JWST) totals 55 SNe Ia and gives H0 = 73.18 +/- 0.88 km/s/Mpc, ~6 sigma above the LambdaCDM+CMB expectation."
  ACCESS: abstract
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high
- [RF-07] CLAIM: Zaborowski et al. (DESI collaboration members, JCAP 04 (2026) 004; arXiv:2510.19149) measure H0 independent of the sound horizon r_s and (optionally) of SNe, from DESI DR1 BAO with the CMB acoustic scale theta_* as high-z anchor: H0 = 69.2 +1.3 -1.4, 70.3 +1.4 -1.2 and 69.6 +1.3 -1.8 km/s/Mpc (i: Planck/ACT CMB lensing x unWISE; ii: DES Y3 6x2pt; iii: CMB lensing + DES Y5 SNe), "better than 2% precision", higher than their earlier r_s-free values. This relaxes the "anything using r_s vs anything not" partition (premise 2): an r_s-free route sits between 69 and 70 with ~1.3-1.4 km/s/Mpc errors, consistent with both H0DN (73.5) at ~2-2.5 sigma and Planck (67.2) at ~1.5 sigma. Assumes LCDM-like late expansion in the rescaling heuristic is not required but pre-recombination physics enters via theta_* only.
  SOURCE: Zaborowski et al., 2026, "H0 Without the Sound Horizon (or Supernovae): A 2% Measurement in DESI DR1", JCAP 04 (2026) 004, arXiv:2510.19149, https://arxiv.org/abs/2510.19149
  QUOTE: "We find somewhat higher values of $H_0$ relative to our previous work: $69.2^{+1.3}_{-1.4}$, $70.3^{+1.4}_{-1.2}$, and $69.6^{+1.3}_{-1.8}\,{\rm km\,s^{-1}\,Mpc^{-1}}$ respectively"
  ACCESS: abstract
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: medium
- [RF-08] CLAIM: Lynch, Chluba, Battye, Vasil (Oct 2026): small-scale electron-density fluctuations (an early-time, recombination-accelerating variant) with Planck + distance-ladder prior give H0 = 71.1 +- 0.7 km/s/Mpc and a better fit than LCDM, but ACT DR6 and SPT-3G D1 break the degeneracy (chiefly through the TE damping tail) and with the same prior give only H0 = 69.3 +- 0.5 km/s/Mpc with no preference over LCDM. Variance of electron density contrast < 0.21 (95% CL). Illustrates the 2025-26 pattern: ACT/SPT damping-tail data close early-time routes that Planck alone leaves open.
  SOURCE: Lynch et al., 2026, "Limits on the size of electron density fluctuations in the early universe and implications for the Hubble tension", arXiv:2610.05147, https://arxiv.org/abs/2610.05147
  QUOTE: "ACT and SPT-3G break this degeneracy, chiefly through the temperature--$E$-mode correlation in the damping tail, and with the same prior they give only $H_0 = 69.3\pm0.5\,{\rm km\,s^{-1}\,Mpc^{-1}}$ and no preference over LCDM."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  ARTIFACT: code (classito Boltzmann code, linked in the paper)
  CONFIDENCE: medium
- [RF-09] CLAIM: eROSITA eRASS1 cluster counts (Strunk et al., Sep 2026, 5259 clusters, 0.1<z<0.8; 0.1<z<0.45 subsample used) give the first cluster-count constraint on axion-like EDE: counts alone f_EDE < 0.3; combined with primary CMB + BAO + CMB lensing (no distance-ladder data) and the full external set, f_EDE = 0.10 +0.04 -0.03 (about 3.2 sigma detection) and H0 = 71.4 +- 1.4 km/s/Mpc. This is a late-2026 preprint pointing the opposite way from the damping-tail closures; its significance rests on the joint fit and has not been refereed.
  SOURCE: Strunk et al., 2026, "The SRG/eROSITA All-Sky Survey: Early dark energy and Hubble constant from the cluster mass function", arXiv:2609.07834, https://arxiv.org/abs/2609.07834
  QUOTE: "The most significant detection, at $\sim 3.2\sigma$, arises from the joint analysis of the eRASS1 sample with the full set of external datasets, yielding $f_{\rm EDE} = 0.10^{+0.04}_{-0.03}$ and $H_0 = 71.4 \pm 1.4$ km/s/Mpc."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RF-10] CLAIM: Poulin et al. (PRD 113, 063519, 2026; arXiv:2505.08051) update EDE after ACT DR6 and DESI DR2: ACT DR6 does not favour EDE over LCDM but allows a larger maximum f_EDE than Planck NPIPE; for Planck(l<1000)+ACT DR6+lensing+Pantheon+ +DESI DR2 without SH0ES, profile-likelihood intervals f_EDE = 0.09 +- 0.03 and H0 = 71.0 +- 1.1 km/s/Mpc (prior-volume effects strong in Bayesian runs); residual tension with SH0ES about 2 sigma (down from 3.7 sigma with NPIPE + SDSS BAO); with DESI the EDE model at H0=73 fits better than LCDM at H0=68.4; adding the SH0ES data raises the preference above 5 sigma (Delta chi2 = -35.4), which is a SH0ES-prior-driven number. This is the pro-EDE reading; it excludes SPT-3G and the full Planck high-l data.
  SOURCE: Poulin, Smith, Bartlett, 2026 (Poulin et al.), "Impact of ACT DR6 and DESI DR2 for early dark energy and the Hubble tension", PRD 113 063519, arXiv:2505.08051, https://arxiv.org/abs/2505.08051
  QUOTE: "A profile likelihood analysis reveals significant prior-volume effects in Bayesian analyses which do not include SH$0$ES, with confidence intervals of $f_{\rm EDE}=0.09\pm 0.03$ and $H_0= 71.0\pm1.1$ km/s/Mpc."
  ACCESS: abstract
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high (for the quoted numbers); author list in SOURCE should be read as "Poulin et al." only
- [RF-11] CLAIM: The competing SPT-3G D1 reading (Khalife et al., PRD 113, 103546, 2026; arXiv:2507.23355) is that SPT-3G and ACT, with and without Planck, plus DESI BAO, give the most up-to-date axion-EDE constraints; see abstract (not fetched in full by me, so the numerical bound is not carried). The 2025-26 literature therefore disagrees on whether SPT-3G/ACT damping-tail data close or leave open EDE; RF-10 (open), RF-08 (closed for the electron-fluctuation variant).
  SOURCE: Khalife et al., 2026, "SPT-3G D1: Axion early dark energy with CMB experiments and DESI observations", PRD 113 103546, arXiv:2507.23355
  QUOTE: "We present the most up-to-date constraints on axion early dark energy (AEDE) from cosmic microwave background (CMB) and baryon acoustic oscillation (BAO) measurements. In particular, we assess the impact of data from ground-based CMB experiments, the South Pole Telescope (SPT) and the Atacama Cosmology Telescope (ACT)"
  ACCESS: abstract
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: low (abstract truncated by the search tool; numerical bound to be filled by quantitative/critiques)
- [RF-12] CLAIM: Wang et al. (Nov 2025) show that adding EDE to w0waCDM with DESI DR2, ACT DR6 and SPT-3G D1 can make a quintessence-like component (w0+wa >= -1) consistent at 1 sigma with Planck+ACT+SPT+DESI+Pantheon+ +SH0ES, with Delta chi2 <~ -14 against w0waCDM without EDE: the evolving-dark-energy preference is degenerate with the Hubble-tension solution, so a single early-time fix may remove both anomalies (SH0ES prior included).
  SOURCE: Wang et al., 2025, "Dark energy after pre-recombination early dark energy in light of DESI DR2 and the latest ACT and SPT data", arXiv:2511.16606 (preprint), https://arxiv.org/abs/2511.16606
  QUOTE: "In the $w_0w_a$CDM model with EDE, a quintessence-like component ($w_0+w_a\geq-1$) can be 1$\sigma$ consistent with Planck+ACT+SPT+DESI+Pantheon+SH0ES datasets, and $\Delta\chi^2\lesssim -14$ compared with $w_0w_a$CDM model without EDE."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RF-13] CLAIM: LVK GWTC-5.0 cosmology paper (arXiv:2605.27227, preprint, 2026) uses 236 GW sources and obtains H0 = 71.7 +9.4 -7.5 km/s/Mpc (median with 68% symmetric credible interval), combining the source-frame mass distribution, the GW170817 + counterpart H0 and DES-Y6 galaxy-catalogue information; the H0 uncertainty is 22.0% smaller than from GWTC-4.0. Sirens remain a ~10-13% measurement, consistent with both sides. Supersedes the GWTC-4.0 value (LVK, ApJL 1007 L17, 142 of 218 sources; arXiv:2509.04348) for the headline siren H0; GWTC-4.0 number not re-quoted here (its abstract was truncated in my fetch).
  SOURCE: LVK Collaboration, 2026, "GWTC-5.0: Constraints on the Cosmic Expansion Rate and Modified Gravitational-wave Propagation", arXiv:2605.27227, https://arxiv.org/abs/2605.27227
  QUOTE: "We estimate $H_0 = {71.7}_{-7.5}^{+9.4}\,{\text{km}\,\text{s}^{-1}\,\text{Mpc}^{-1}}$ (median with $68\%$ symmetric credible interval)."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RF-14] CLAIM: Xiong et al. (Jun 2026) combine 142 GWTC-4 sirens with TDCOSMO-2025 time delays through the distance sum rule (cosmology-model-independent): H0 = 83.78 +12.53 -10.23 km/s/Mpc (13.58%) with the conservative TDCOSMO2025 hierarchical mass-sheet treatment; replacing it with the H0LiCOW method tightens this to 75.42 +3.74 -4.66 (5.57%). The precision is governed by the mass-sheet-transformation treatment; both results are consistent with Planck and SH0ES. Shows that lensing-side modelling choices move the one-step H0 by ~8 km/s/Mpc at fixed data in this combination.
  SOURCE: Xiong et al., 2026, "Model-independent H0 from GWTC-4 standard sirens and TDCOSMO 2025 strong lensing time delays", arXiv:2606.03634, https://arxiv.org/abs/2606.03634
  QUOTE: "replacing the conservative TDCOSMO2025 hierarchical framework with the H0LiCOW method tightens the constraint to $H_0 = 75.42^{+3.74}_{-4.66}\ {\rm km\,s^{-1}\,Mpc^{-1}}$, with a relative precision of $5.57\%$."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RF-15] CLAIM: Anand (Feb 2025 preprint) finds ground-based JAGB distances to nearby galaxies (the CCHP local sample, 0.5-4 Mpc) are offset from uniformly reduced HST TRGB distances by Delta mu = 0.17 +- 0.04 (stat) +- 0.06 (sys) mag (9% in distance), HST TRGB further, and argues the problem lies in the ground-based JAGB data; this challenges the CCHP claim of 1% TRGB-JAGB agreement. A rebuttal from CCHP was not found in this search.
  SOURCE: Anand, G.S., 2025, "A Sizable Discrepancy in Ground-Based JAGB Distances to Nearby Galaxies", arXiv:2502.07882, https://arxiv.org/abs/2502.07882
  QUOTE: "We uncover a significant offset between these two distance scales of $\Delta\mu$ = 0.17 $\pm$ 0.04 (stat) $\pm$ 0.06 (sys) mag (9$\%$ in distance), with the HST TRGB distances being further."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RF-16] CLAIM: Li et al. "JAGB 2.0" (ApJ 988, 97, 2025; arXiv:2502.05259; SH0ES-side authors) analyses all JWST JAGB observations in SN Ia hosts (15 galaxies, 18 SNe Ia, SH0ES + CCHP programmes): mean difference from HST Cepheid distances -0.03 +- 0.02 (stat) +- 0.05 (sys) mag; JAGB mode measurements in two NGC 4258 fields differ by 0.11 +- 0.02 mag (field-to-field variation, also seen in SH0ES fields), giving a large absolute-calibration uncertainty; JAGB-calibrated SNe Ia give H0 = 73.3 +- 1.4 (stat) +- 2.0 (sys) km/s/Mpc, i.e. the JAGB route is not systematically low once the NGC 4258 field choice and LF measure are handled this way; the CCHP JWST JAGB-only value is lower (about 67.8, per the CCHP 2025 report, secondary summary only; engineering owns the CCHP numbers).
  SOURCE: Li et al., 2025, "JAGB 2.0: Improved Constraints on the J-region Asymptotic Giant Branch-based Hubble Constant from an Expanded Sample of JWST Observations", ApJ 988 97, arXiv:2502.05259, https://arxiv.org/abs/2502.05259
  QUOTE: "Using the middle result of all JAGB measures to calibrate SNe Ia yields a Hubble constant of $H_0$ = 73.3 $\pm$ 1.4 (stat) $\pm$ 2.0 (sys) km/s/Mpc with the systematic dominated by apparent differences across NGC 4258 calibrating fields or their measures."
  ACCESS: abstract
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high
- [RF-17] CLAIM: Gaia DR4 (5.5 years of data) is scheduled for 2 December 2026: the Gaia archive goes down on Wednesday 25 November 2026 12:00 CET and re-opens on Wednesday 2 December 2026 at 12:00 CET "featuring the new Gaia DR4 release". It is the next improvement of MW Cepheid/TRGB/JAGB parallax zero points (anchor rung) and falls after this research date (30 Oct 2026); no DR4-based H0 result exists yet.
  SOURCE: ESA Gaia mission news page 2026, https://www.cosmos.esa.int/web/gaia/news-2026
  QUOTE: "In preparation of Gaia DR4, the ​​​​​​​Gaia ESA Archive will be down as of Wednesday 25 November 2026 12:00 CET. The archive will re-open on Wednesday 2 December 2026 at 12:00 CET, featuring the new Gaia DR4 release."
  ACCESS: full-text
  STATUS: secondary (institutional announcement; schedule, not a result)
  CONFIDENCE: high
- [RF-18] CLAIM: TDCOSMO 2026 companion paper (Birrer et al., arXiv:2610.14881, Oct 2026 preprint) states the tension with the Planck CMB prediction is robust to excluding any one of the SN Ia-, Cepheid- or TRGB-based methods: a 'no-SN' late-universe H0 (TDCOSMO-2026 with a DESI-BAO Omega_m instead of the SN one, combined with independent non-SN late probes) is in 3.7 sigma tension with Planck; "Even after completely excluding the LDL [local distance ladder], the tension with Planck persists at the 2.7 sigma level." This is a lensing-team result and its statistical combination is theirs; the CMB comparison is with Planck only (not Planck+SPT+ACT, which has a smaller error).
  SOURCE: Birrer et al. (TDCOSMO), 2026, "TDCOSMO 2026: new insights on the Hubble tension from strong lensing time delays", arXiv:2610.14881, https://arxiv.org/abs/2610.14881
  QUOTE: "Even after completely excluding the LDL, the tension with Planck persists at the 2.7$\sigma$ level."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RF-19] CLAIM: Percival (Jul 2026 preprint) derives the likelihood for truncated selection in correlated observables and finds mild evidence (1.3 to 2.3 sigma, depending on the distance prior) for residual Cepheid selection corrections in SN Ia calibrator hosts in recent distance-ladder data. One extra cut-off parameter for Cepheid selection lowers the recovered H0 by -1.4 km/s/Mpc; further SN Ia selection corrections lower it by -0.2 km/s/Mpc; an equal-volume distance prior rather than uniform in distance modulus lowers it by -1.0 km/s/Mpc; "When included together, these effects substantially reduce the inferred tension with CMB measurements." Sum of the three quoted shifts is -2.6 km/s/Mpc (simple arithmetic, not the paper's own combined number; effects need not add). A named rung-1 ladder systematic candidate, unrefereed and not yet answered by SH0ES in the literature I found.
  SOURCE: Percival, W.J., 2026, "Selection effects in correlated observations with application to distance-ladder observations", arXiv:2607.22425, https://arxiv.org/abs/2607.22425
  QUOTE: "Including a single extra parameter to model the unknown cut-off in Cepheid selection in SN Ia host galaxies lowers the recovered H0 by -1.4km/s/Mpc."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RF-20] CLAIM: Dong et al. (Oct 2026 preprint) test the Cepheid-host/Hubble-flow SN consistency with Pantheon+ using Planck-CMB priors on one SN sample and propagating to the other; host peculiar-velocity corrections from the Manticore-Local reconstruction shift the recovered H0 from 74.30 +1.18 -1.20 to 71.37 +1.23 -1.18 km/s/Mpc (forward) and from 60.83 +0.98 -0.97 to 63.25 +0.95 -0.93 km/s/Mpc (backward), and reduce the cosmological-intercept discrepancy from 6.8 sigma to 3.9 sigma (forward) and from 7.3 sigma to 4.3 sigma (backward); a 3.9-4.3 sigma residual persists. Relevant to premise 5 (calibrator versus Hubble-flow SN offset) and to the peculiar-velocity sub-hypothesis. Note this contradicts the H0DN/Roy Choudhury finding that SN-side reworking leaves ~7 sigma; the two differ in method (Pantheon+ only with a CMB prior versus covariance network).
  SOURCE: Dong et al., 2026, "A cosmological intercept tension in local distance ladders", arXiv:2610.31181, https://arxiv.org/abs/2610.31181
  QUOTE: "Peculiar-velocity corrections therefore partially alleviate the intercept tension, while a residual discrepancy persists within the adopted framework."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RF-21] CLAIM: Stiskalek et al. (Sep 2026 preprint) infer H0 from ~400 EDD TRGB hosts calibrated on LMC and NGC 4258 with forward-modelling of selection and conditioned on each of 80 Manticore-Local realisations of the local density/velocity field. Field-to-field scatter in H0 is 5.2 km/s/Mpc; equal weighting gives H0 = 68.4 +- 5.9 km/s/Mpc, evidence weighting 72.3 +- 2.6 km/s/Mpc (set by a single high-evidence realisation). "This ladder therefore cannot yet arbitrate the Hubble tension." Gives the local-structure facet a quantitative handle: with hosts at cz_CMB <~ 1000 km/s the limit is peculiar-velocity reconstruction variance, not the TRGB calibration.
  SOURCE: Stiskalek et al., 2026, "Two-rung ladder: H0 from Tip of the Red Giant Branch and geometric anchors alone", arXiv:2609.29996, https://arxiv.org/abs/2609.29996
  QUOTE: "whereas the field-to-field scatter in $H_0$ is 5.2 km/s/Mpc. Weighting the posteriors from each realisation equally gives $H_0 = 68.4 \pm 5.9$ km/s/Mpc, while weighting each by its Bayesian evidence gives $72.3 \pm 2.6$ km/s/Mpc."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RF-22] CLAIM: Camilleri et al. "Unite" (Sep 2026 preprint; Pantheon+ and DES-SN5YR combined, 2884 SNe Ia) gives Flat-LCDM Omega_m = 0.310 +0.012 -0.011 from SNe alone; with CMB+DES+DESI BAO and (w0,wa): (Omega_m, w0, wa) = (0.305 +- 0.004, -0.861 +0.044 -0.042, -0.60 +0.17 -0.19); preference over flat LCDM 3.3 sigma (MAP) or 3.1 sigma (max likelihood), but "only weak preference" in Bayesian evidence. The evolving-dark-energy preference persists (and is the context for RF-04/RF-05) but is not decisive.
  SOURCE: Camilleri et al., 2026, "Supernovae Unite: Combining Pantheon+ and DES-SN5YR", arXiv:2609.05053, https://arxiv.org/abs/2609.05053
  QUOTE: "The Bayesian evidence indicates only weak preference for time evolving dark energy, whereas frequentist analyses yield a preference over Flat-$\Lambda$CDM at a significance of $3.3\sigma$ ($3.1\sigma$) when using the maximum $\textit{a posteriori}$ probability (maximum likelihood)."
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RF-23] CLAIM: DES Year 6 3x2pt (Abbott et al., arXiv:2601.14559, preprint 2026): flat LCDM S8 = 0.789 +- 0.012, Omega_m = 0.333 +0.023 -0.028, a 1.8 sigma full-space (2.6 sigma in S8 alone) difference from Planck 2018 + ACT-DR6 + SPT-3G DR1; DES 3x2pt + DESI DR2 BAO + DES SNe + SPT clusters 2.3 sigma from the CMB; joint LCDM fit gives S8 = 0.806 +0.006 -0.007, Omega_m = 0.302 +-0.003, h = 0.683 +0.003 -0.002, Sum m_nu < 0.14 eV (95% CL). The S8 tension has shrunk relative to earlier KiDS/DES results, so S8 constrains EDE less sharply than assumed; the joint LCDM fit is h = 0.683 (a fit across all data, not a measurement of H0 on one side).
  SOURCE: DES Collaboration (Abbott et al.), 2026, "Dark Energy Survey Year 6 Results: Cosmological Constraints from Galaxy Clustering and Weak Lensing", arXiv:2601.14559, https://arxiv.org/abs/2601.14559
  QUOTE: "A joint fit of Y6 3$\times$2pt, CMB, and those low-redshift datasets produces the tightest $\Lambda$CDM constraints to date: $S_8 = 0.806^{+0.006}_{-0.007}$, $\Omega_{\rm m} = 0.302^{+0.003}_{-0.003}$, $h = 0.683^{+0.003}_{-0.002}$"
  ACCESS: abstract
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium
- [RF-24] CLAIM: Chen et al. review (Res. Astron. Astrophys. 26, 084003, 2026; arXiv:2606.26831) gives a "compact seven-route covariance summary" combining the Cepheid-SN Ia route with TRGB, JAGB, Mira level-1 alternatives and SBF, Tully-Fisher, SN II level-2 alternatives: H0 = 73.30 +- 0.92 km/s/Mpc, "still 5.6 sigma above Planck base-LCDM". A second, independent-ish community combination agreeing with H0DN (73.50 +- 0.81) within 0.2 km/s/Mpc; same data, so not independent confirmation.
  SOURCE: Chen et al., 2026, "Distance-ladder Measurements of the Hubble Constant: Recent Progress, Systematics, and Prospect", RAA 26 084003, arXiv:2606.26831, https://arxiv.org/abs/2606.26831
  QUOTE: "gives \(H_0=73.30\pm0.92~{\rm km~s^{-1}~Mpc^{-1}}\), still \(5.6\sigma\) above Planck base-\(\Lambda\)CDM."
  ACCESS: abstract
  STATUS: textbook-or-review
  SETTING: analysis
  CONFIDENCE: high
- [RF-25] CLAIM: Planned results with dates: Gaia DR4 on 2 Dec 2026 (RF-17); no CCHP update beyond the 2025 JWST status report (Freedman et al., arXiv:2408.06153, ApJ 2025: TRGB-only 70.39 +-1.22 (stat) +-1.33 (sys) +-0.70 (sigma_SN) km/s/Mpc, 24 SNe, per a web-search summary of the DOAJ record) and no formal CCHP reply to H0DN were found by me; no DESI DR3 BAO release was found (a July 2026 Fermilab talk titled "Recent Results from DESI" exists; its abstract does not name DR3). These are absence-of-evidence statements for 30 Oct 2026.
  SOURCE: web search summaries (DOAJ record of Freedman et al. 2025; Fermilab Indico event 72820)
  SUMMARY: "I found no 2026 CCHP result. The most recent work in these results is the 2025 Astrophysical Journal status report"; "The search didn't turn up a DR3 BAO release."
  ACCESS: search-summary
  STATUS: secondary
  CONFIDENCE: low

## Gaps
- Did not find a CCHP (Freedman, Madore) 2026 paper, nor a CCHP reply to H0DN or to the Perfect Host paper; the CCHP side is represented only by Anand's critique (RF-15), the SH0ES-side JAGB paper (RF-16) and the H0DN network variants. Critiques facet should check.
- Could not open SPT-3G D1 (Camphuis et al. 2025) and ACT DR6 (Louis et al. 2025) primary papers, nor Simons Observatory or CMB-S4 news; the CMB-side H0 67.24 +- 0.35 is carried only from H0DN (RF-02). Quantitative owns it.
- DESI DR2 BAO+BBN H0 68.51 +- 0.58 is quoted only through H0DN (RF-02).
- No 2026 result on varying m_e, primordial magnetic fields or interacting dark energy was fetched; only EDE variants (RF-08..RF-12). No Roman, Rubin LSST, LVK O5 or ELT time-delay programme timelines were checked (engineering owns).
- arXiv API timed out repeatedly; INSPIRE and arxiv.org/abs pages through fetch_text worked. Full PDFs were opened only for H0DN; all other frontier claims are ACCESS: abstract.
- Items listed by the search tool but not read: Treu 2026 lensing review (arXiv:2610.19598), Loverde et al. LBT helium (arXiv:2609.13140), CosmoVerse white paper (arXiv:2504.01669), Zaborowski follow-ups.
- PAPER TO REQUEST: none (all relevant papers are on arXiv).
