# Brief: The lens mass sheet: why time-delay lenses prefer λ_int ≈ 0.94, and what H0 lensing implies
slug: 2026-11-05-lens-mass-sheet-time-delay-h0 | depth: standard | type: anomaly | date: 2026-11-05

## Question as asked
"Why do time-delay lenses prefer an internal mass-sheet parameter of about 0.94 when other lens samples and stacked weak lensing give about 1, and what H0 does time-delay lensing really imply?"

(Framed in another session from a review of the state of the art of ladder-free H0 methods. The user asked for this run at standard depth.)

## Question made precise
The question is read as: **what is the dominant cause of the offset between the internal mass-sheet parameter λ_int inferred for the TDCOSMO time-delay deflectors (≈ 0.94) and the value inferred for lens samples without time delays and from stacked weak lensing (≈ 0.98–1.00)? Given that cause, what H0 does strong-lensing time-delay cosmography currently support, and with what credence in each of the H0 bands below?** The answer is a ranked, mutually exclusive slate of causes. Each comes with the λ_int it implies for the time-delay deflectors, the H0 that follows, the evidence for and against it, and its predictions for the data now being taken.

Definitions of loaded terms:
- **Mass-sheet transformation (MST).** κ → λκ + (1 − λ)κ_c, with κ_c = 1 for an infinite sheet. It leaves image positions and flux ratios unchanged and scales the predicted time delays by λ. At fixed measured delays the inferred time-delay distance scales as D_Δt ∝ 1/λ, so the inferred H0 ∝ λ to first order. It splits into:
  - an **external** part, the line-of-sight convergence κ_ext, from structure along the line of sight (estimated from weighted galaxy counts calibrated on simulations);
  - an **internal** part, λ_int: any departure of the deflector's true mass profile from the assumed model (power law or composite) that acts as an approximate MST, for example a core or an extended halo component. Infinite sheets are unphysical, so the internal MST is approximate, implemented with a cored component; TDCOSMO also lets λ_int vary with r_eff/θ_E through a slope α_λ.
- **Breaking the MST.** Image data alone cannot fix λ_int; other data must:
  - stellar kinematics (σ_v² scales with λ_int at fixed lens model, and the result is degenerate with the orbital anisotropy β);
  - SN Ia standard-candle magnification (lensed SNe Ia only);
  - external lens samples assumed to share the deflectors' profiles (SLACS, SL2S);
  - stacked weak lensing of comparable galaxies.
- **"Time-delay lenses" (TD lenses).** Lensed quasars with monitored time delays used by TDCOSMO: quasar-selected, mostly quads, a few doubles. **SLACS**: galaxy–galaxy lenses selected spectroscopically in SDSS (background emission lines behind early-type galaxies). **SL2S**: galaxy–galaxy lenses selected from CFHT imaging.
- **"About 0.94" and "about 1".** Placeholders from the framing session's leads (TDCOSMO-2026 TD-only ≈ 0.935–0.942; with SLACS+SL2S ≈ 0.99–1.00; stacked weak lensing 0.978 ± 0.010). The research must establish the current values, with their correlations (notably λ_int with α_λ and with the anisotropy prior), and the statistician must compute the significance of the offset.
- **H0 bands (context only, not to be researched here).** A separate analysis of the Hubble tension found that a ladder-free, sound-horizon-free H0 would discriminate between three explanations of the local (~73) versus early-universe (~67–68.5 km/s/Mpc) gap:
  - ≤ 69 favours an error in the local distance ladder;
  - 69.4–70.6 favours a mixture (part ladder error, part a real ~3–4% smaller sound horizon);
  - ≥ 70.2–71 favours pre-recombination new physics such as early dark energy.

  Report P(H0 ≤ 69), P(69.4 ≤ H0 ≤ 70.6), P(H0 ≥ 70.2) and P(H0 ≥ 72.5) for lensing under the leading candidates. The Hubble tension itself is out of scope.
- **"Really imply."** The H0 that time-delay cosmography supports once the mass-sheet question is weighed, in flat ΛCDM with an external Ω_m (or relative-distance) anchor. The answer must also say how far the value moves in w0waCDM and with which anchor.

Admissible physics:
- **Established:** GR gravitational lensing (thin-lens and multi-plane); stellar dynamics (spherical Jeans, axisymmetric JAM, orbital anisotropy); the galaxy mass profiles and halo models of ΛCDM structure formation; the statistics of lens selection and magnification bias; FRW distances in flat ΛCDM and its standard extensions.
- **Speculative, allowed only when labelled:** modified gravity at galaxy scales, unusual dark-matter profiles beyond ΛCDM expectations.

"Viable" has two tiers:
- **Now:** consistent with every current lensing, kinematic and weak-lensing constraint, within its stated assumptions.
- **Decidable:** a measurement expected by about 2030 (JWST Cycle 5 resolved kinematics, SN Requiem's reappearance, Rubin- and Euclid-era samples) would confirm or exclude it.

## Hidden premises to test
1. **The λ_int offset is real.** TDCOSMO calls the TD-only versus joint difference about a 1σ fluctuation, and λ_int is anti-correlated with α_λ ("partly two expressions of the same feature of the data"). Test its significance, with the intrinsic scatter σ(λ_int) = 0.093 (TD-only) versus 0.131 (joint) and only 11 TD lenses.
2. **TD lenses and SLACS/SL2S deflectors are drawn from one population.** Li, Collett et al. 2025 model the selection functions and predict lower λ_int for quasar-selected deflectors (0.87 +0.07/−0.06), with H0 ≈ 66. TDCOSMO-2025 rejected this as "in stark contrast" with the then-measured value, but the TD-only value has since moved toward it. Other selection estimates (Collett & Cunnington 2016; Sonnenfeld et al. 2023; Baldwin & Schechter 2024) are reported as sub-percent. Test which selection model holds, and why they differ.
3. **Kinematics actually constrain λ_int.** The TDCOSMO-2026 anisotropy posterior is "largely set by" its U(0.87, 1.12) prior. Forés-Toribio, Kochanek & Muñoz 2026 list Δσ²/σ² biases of 2–18% (anisotropy model), 1–10% (light-profile mismatch), 2–6% (σ versus v_rms) and 1–5% (ground-based PSF). Verma & Minor 2026 find −0.9% ± 1.9% for constant β but +11.5% ± 1.3% for Osipkov–Merritt. Hu et al. 2026 find that free-anisotropy preferences depend on the tracer profile. Test how much of the 6% λ offset (≈ 6% in σ²) a dynamical-modelling choice can produce.
4. **The approximate-MST parametrisation captures the real profile freedom.** Blum, Castorina & Simonović 2020 argue a cored component acts as an approximate MST that "could bring the lensing measurements of H0 into accordance with the CMB/LSS value". Kochanek 2020 says current lens H0 values are unlikely to be better than about 10%. Gomer & Williams 2020–2022 find ellipse-plus-shear and power-law biases. Li, Tian et al. 2026 find that a composite JWST model of WFI2033 has an H0–halo-scale-radius degeneracy. Test whether the α_λ/core parametrisation could itself produce or hide the offset.
5. **Stacked weak lensing applies to TD deflectors.** Fujikawa et al. 2026 (λ_c = 0.978 ± 0.010; 0.99 ± 0.03 with three cored components) use massive early-type galaxies at 0.4 < z < 0.6 and assume large cores, and say the constraint "can be relaxed". Test transferability to the TD deflectors' masses, redshifts, environments and r_eff/θ_E.
6. **Line-of-sight convergence is under control.** Teodori et al. 2022 showed the observer–lens and lens–source terms matter; TDCOSMO XXXI (Johnson et al. 2026) now includes them; Tang et al. 2025 find line-of-sight selection biases of about 0.1% for galaxy–quasar lenses. Test briefly that κ_ext cannot mimic the offset.
7. **Lensed supernovae are an independent check.** The SN Refsdal analyses cluster at 65–66 km/s/Mpc, but all share one delay and largely the same image constraints, and Schuldt 2026 v2 states that its 3% omits external-convergence and parametrisation systematics. SN H0pe uses SN Ia magnifications as an MST breaker (75.7 +8.1/−5.5), but a different delay and microlensing analysis gives 69.3. Cluster models have shape degeneracies "invisible in comparisons of independent models" (Meena et al. 2026). Test what lensed SNe can and cannot say about λ_int and H0.
8. **Lensing H0 is cosmology-free.** In flat ΛCDM the external Ω_m prior matters at about 1%. In w0waCDM, TDCOSMO-2026 Table V gives 65.2–70.6 depending on the relative-distance anchor (DESI BAO, DES-Dovekie SNe, Planck+BAO). Test how this conditions the answer.
9. **A population mean is the right quantity.** Per-lens λ_int spans about 0.89–1.12 (J1537: 0.89; SDSSJ1433: 1.12), and TDCOSMO-2026 says per-lens λ_int "may be necessary to reduce the scatter". This may make the question partly mis-posed (a reframe).

## What counts as an answer
- **A ranked, mutually exclusive slate with credences** for the dominant cause of the TD-versus-other λ_int offset. It must include at least:
  - **selection:** TD deflectors really have lower λ_int, so the TD-only H0 (or lower, toward Li & Collett) is right;
  - **a kinematic or dynamical-modelling systematic** that biases the TD-lens λ_int low, so true λ_int ≈ 1 and H0 ≈ 73–75.5;
  - **a bias in the comparison samples** (SLACS/SL2S kinematics, apertures, selection; stacked-weak-lensing assumptions) that biases them high, so the TD-only value is right;
  - **a lens-model parametrisation artefact** (approximate-MST/core/α_λ form, composite-profile degeneracies);
  - **line-of-sight or environment** effects;
  - **the null:** a statistical fluctuation with no real offset, given N = 11 and σ(λ_int) = 0.093;
  - **a reframe:** λ_int is not a single population parameter, so the population-mean comparison is mis-posed.
- **For each candidate:**
  - the λ_int it implies for TD lenses and for SLACS/SL2S;
  - the implied lensing H0 with uncertainty, and P(H0 ≤ 69), P(69.4–70.6), P(≥ 70.2), P(≥ 72.5);
  - its causal chain and weakest link;
  - the evidence for and against it, by dossier ID;
  - its prediction for the data now being taken.
- **A prediction matrix,** with one column per independent class of evidence:
  - TD-only hierarchical λ_int (TDCOSMO-2026);
  - SLACS/SL2S λ_int;
  - stacked weak lensing;
  - per-lens λ_int from resolved kinematics;
  - lensed SNe in clusters (Refsdal, H0pe, Encore/Requiem);
  - galaxy-scale lensed SNe (SN 2025wny);
  - SN Ia magnification as an MST breaker;
  - mock and simulation challenges (Gomer et al. 2022; Verma & Minor 2026; Hu et al. 2026);
  - SN Requiem's reappearance date;
  - the forecast GO-7184/GO-9637 resolved-kinematics sample.
- **The lensing H0 verdict:** one credence distribution for the H0 that time-delay lensing implies now, in flat ΛCDM, with the w0waCDM spread stated.
- **The deciding measurement:** the single observation or analysis that would settle the λ_int question, with who, the precision it needs and when; and a runner-up.

## Research facets
- **theory:**
  - owns: MST physics, both external and internal; the approximate MST via cored components; the source-position transformation; multi-plane MST; the hierarchical λ_int/α_λ formalism (Birrer et al. 2016, 2020; Schneider & Sluse 2013–2014; Blum et al. 2020; Teodori 2022, 2026);
  - owns: the dynamics: spherical Jeans and JAM, the mass–anisotropy degeneracy, how σ_v² scales with λ_int, and how tracer-profile and anisotropy-model choices propagate to λ_int;
  - owns: the theory of lens selection: how quasar-quad selection and magnification bias, versus emission-line or imaging selection, shift the deflector profile and λ_int (Li & Collett 2025; Collett & Cunnington 2016; Sonnenfeld et al. 2023; Baldwin & Schechter 2024);
  - leaves numbers to quantitative, critiques and replies to critiques, and data and programmes to engineering.
- **quantitative:**
  - owns: every number, as quoted with its correlations:
    - TDCOSMO-2026 hyperposteriors (λ_int, α_λ, σ(λ_int), anisotropy prior and posterior, Ω_m-prior variants, Table V cosmology dependence) and the per-lens values in its tables;
    - TDCOSMO-2025, TDCOSMO-IV and H0LiCOW values, for the trajectory;
    - per-lens λ_int (Sheu 2026; Galan 2026; Paic 2026; Williams 2026, TDCOSMO XXVII);
    - SLACS/SL2S λ_int (Knabel 2025, 2026);
    - stacked weak lensing (Fujikawa 2026);
    - the Li & Collett 2025 predictions;
    - the r_eff/θ_E, velocity-dispersion, redshift and environment distributions of the TD, SLACS and SL2S samples;
    - κ_ext distributions;
    - lensed-SN H0 values, with notes on shared data;
  - leaves interpretation of disputes to critiques.
- **critiques:**
  - owns: published objections, rebuttals and replies, both sides with sources:
    - Kochanek 2020 and 2021; Blum et al. 2020; Gomer & Williams 2020–2022; Forés-Toribio, Kochanek & Muñoz 2026; Hu et al. 2026;
    - Li & Collett 2025 against TDCOSMO-2025 Sec. 11.2.1, and anything since;
    - Verma & Minor 2026; Denzel et al. 2021 (free-form); Li, Tian et al. 2026 (composite);
    - for lensed SNe: Meena et al. 2026, the Schuldt 2026 v2 caveats, and the Pascale-versus-Grayling H0pe disagreement;
    - the Treu 2026 review's error budget and its "?" entries;
  - leaves the formalism to theory and the numbers to quantitative.
- **engineering:**
  - owns: the data and how it is taken:
    - lens samples and selection pipelines;
    - time-delay measurement (COSMOGRAIL, TDCOSMO-XVII);
    - kinematics instruments (JWST-NIRSpec IFU, MUSE, KCWI) and their PSF and aperture handling (STARRED; Krizic et al. 2026, ALPACA I);
    - blinding, and the modelling codes and their cross-checks (lenstronomy, GLEE, Herculens);
  - owns: the running and planned programmes, each with who runs it, its target precision and when results are expected:
    - JWST GO-7184 (PI Millon) and GO-9637 (PI Treu, Cycle 5);
    - SN Requiem's reappearance (HST 18069, JWST ToO 9330);
    - new lensed quasars (Sheu et al. 2026, 17 systems; Gaia GraL counts);
    - Rubin LSST, Euclid DR1 and Roman;
    - any planned blind modelling challenge;
  - leaves values to quantitative.

Every facet: the field moves fast and this standard run has no separate frontier facet. Within its own area, each facet covers the newest results through November 2026, newest first, labels preprints as such, and names any value they supersede.

## Worked calculations
- **statistician:**
  - the significance of the TD-only λ_int against SLACS/SL2S and against stacked weak lensing, using the published correlations (λ_int–α_λ, the scatter difference 0.093 versus 0.131) and N = 11;
  - whether the per-lens λ_int values (0.89–1.12) are consistent with one population;
  - P(H0 in each band) for the TD-only, joint and "λ_int = 1" readings, and under each candidate;
  - the precision a future measurement of λ_int needs to separate the leading candidates at 3σ.

  This is the reference for the offset's significance.
- **constraints:**
  - the MST algebra (H0 ∝ λ_int; σ_v² scaling at fixed lens model);
  - how far the anisotropy can move λ_int within U(0.87, 1.12), and the size of the kinematic bias (in Δσ²/σ²) needed to turn 1.00 into 0.94, against the published bias bounds;
  - the κ_ext budget;
  - the cosmology-anchor dependence (Table V).

  Use `.claude/skills/conundrum/scripts/cosmo_background.py` for distances, and the run's lensing calculator if one is built.
- **mechanist:**
  - the selection causal chain: which deflector property (core, slope, environment, r_eff/θ_E) quasar-quad selection favours, and how large a λ_int shift it produces;
  - reproduce or refute Li & Collett's 0.87 and TDCOSMO's rebuttal;
  - compare with the measured differences between the samples.

## Known constraints, prior attempts, and user-supplied data
No user-supplied data.

Starting points for the researchers. They come from a framing-session review (two researchers plus two adversarial source checkers, 2026-11-05). They are leads, not established claims: each must be found and quoted again before use, and any value or reference here may be wrong. Access was mostly arXiv abstracts or full text, as marked.

**TDCOSMO-2026 and the λ_int question**
- TDCOSMO Collaboration (Birrer, Millon, Galan, Mozumdar et al.) 2026, "TDCOSMO 2026: A 3% measurement of the Hubble constant from strong lensing and stellar kinematics", arXiv:2610.14781 (v2 29 Oct 2026; submitted to PRD; full text seen). Values:
  - baseline (11 lensed quasars, flat ΛCDM with a DES-Dovekie Ω_m prior, blind, MST free): H0 = 71.1 +2.4/−2.3 (3.3%); with a uniform Ω_m prior 70.6 +3.9/−3.1;
  - with SLACS+SL2S: 71.3 +2.2/−2.1; with DESI DR2 BAO: 71.7 +2.5/−2.3 (TD only) and 72.2 ± 2.2 (with SLACS+SL2S);
  - nine lenses have resolved kinematics (6 JWST-NIRSpec, plus MUSE and KCWI); dynamics are axisymmetric JAM; κ_ext is calibrated on Euclid Flagship;
  - robustness runs shift H0 by −0.20 to +0.7 σ, and the baseline lies "at the lower end of the range spanned by the alternative choices".
- Sec. VIII.A of the same paper:
  - TD-only λ_int ≈ 0.935–0.942, and "rescaling our value to λ_int = 1 gives ~75.5 km/s/Mpc";
  - α_λ = −0.038 +0.082/−0.088, anti-correlated with λ_int ("partly two expressions of the same feature of the data");
  - with SLACS+SL2S: λ_int = 1.002 +0.050/−0.046 (0.993 +0.042/−0.041 in another variant), α_λ = 0.016 +0.051/−0.056, H0 = 72.1 +4.1/−3.4 (uniform Ω_m);
  - σ(λ_int) = 0.093 +0.038/−0.026 (TD only), "significantly non-zero", which "sets a floor on how well the population mean can be determined from only eleven lenses"; 0.131 +0.029/−0.022 joint, which "may indicate that the SLACS deflectors differ slightly from the time-delay deflectors";
  - "A larger sample of time-delay lenses with resolved kinematics will show whether the time-delay deflectors differ … or whether this is a statistical fluctuation."
- Same paper, Table V (cosmology dependence):
  - w0waCDM: 66.1 +4.0/−3.0 (with DESI BAO), 70.6 ± 2.1 (DES-Dovekie), 65.2 +2.7/−2.4 (with Planck+BAO);
  - TDCOSMO alone: 69.8 +5.9/−6.1 (w0waCDM) and 67.9 ± 6.0 (wCDM).
- Companion letter, arXiv:2610.14881 (submitted to PRL): its 2.7σ tension with Planck is for TDCOSMO-2026 combined with megamasers and globular clusters, not lensing alone. Its words: "our precision is not quite sufficient to test the Hubble tension independently of all other methods."
- Trajectory (superseded):
  - TDCOSMO-2025, A&A 704, A63 (arXiv:2506.03023): 71.6 +3.9/−3.3, and 74.3 +3.1/−3.7 with SLACS+SL2S. Its Sec. 11.2.1 rebuts Li & Collett.
  - TDCOSMO-IV (Birrer et al. 2020, A&A 643, A165, arXiv:2007.02941): 74.5 +5.6/−6.1, and 67.4 +4.1/−3.2 with SLACS. Freeing the MST raised the error from 2% to 8% for the same 7 lenses.
  - H0LiCOW: 73.3 +1.7/−1.8 (assumed profiles).
  - Adding SLACS moved H0 by −7.1 (2020), +2.7 (2025) and +0.2 (2026) km/s/Mpc.
- Per-lens values (λ_int free unless stated):
  - SDSSJ1433: 73.2 +4.8/−4.7, λ_int = 1.12 +0.05/−0.06 (Sheu et al., PRD 114, 063509, arXiv:2604.14145);
  - J1537−3010: 75.5 +9.3/−5.8, λ_int = 0.89 +0.09/−0.07 (Galan et al., arXiv:2609.00179);
  - HE1104 (first double): 64.2 +5.8/−5.0 × λ_int (Paic et al., A&A 706, A270, arXiv:2512.03178);
  - TDCOSMO XXVII, JWST-NIRCam models of WFI2033, HE0435 and PG1115: combined 73.5 +2.7/−2.8 × λ_int (Williams et al., arXiv:2608.27566).
- SLACS: λ_int = 1.01 ± 0.03, scatter 0.11 ± 0.03 (Knabel et al. 2026, arXiv:2604.12155); Knabel et al. 2025 on kinematics accuracy (arXiv:2502.16034).
- Stacked weak lensing: Fujikawa et al. 2026, "Stacked strong and weak lensing united", arXiv:2609.39040 (full text seen). HSC stacked weak lensing of massive early-type galaxies at 0.4 < z < 0.6, plus 13 strong lenses: λ_c = 0.978 ± 0.010 for one cored component, 0.99 ± 0.03 for three; the constraint "can be relaxed".
- Selection: Li, Collett et al. 2025, "Correcting for selection biases in the determination of the Hubble constant from time-delay cosmography", MNRAS 538, 2375 (arXiv:2410.16171). Galaxy–galaxy lenses "have systematically higher mass-sheet components than galaxy-quasar lenses"; H0 = 66 ± 4 (stat) ± 1 (model sys) ± 2 (measurement sys); predicted λ_int = 0.87 +0.07/−0.06 for the TDCOSMO-4 quads. TDCOSMO-2025 also cites Collett & Cunnington 2016, Sonnenfeld et al. 2023 and Baldwin & Schechter 2024 as sub-percent estimates.

**Critiques and modelling systematics**
- Kochanek 2020, MNRAS 493, 1725 (arXiv:1911.05083): current lens H0 estimates are unlikely to be more accurate than about 10%. Kochanek 2021 follow-up.
- Blum, Castorina & Simonović 2020, ApJL 892, L27 (arXiv:2001.07182): cored components as an approximate MST.
- Forés-Toribio, Kochanek & Muñoz 2026, ApJ 1005, 228 (arXiv:2602.03934): the dynamical biases listed under premise 3; "measuring H0 to 2% requires Δ(σ²)/σ² < 2%".
- Verma & Minor 2026, ApJ 1000, 264 (arXiv:2602.07159): constant-β bias −0.9% ± 1.9% with joint lensing+kinematics; +11.5% ± 1.3% for Osipkov–Merritt.
- Huang et al. 2026 (arXiv:2503.00235): triaxiality below 1%.
- Hu et al. 2026, arXiv:2605.19615 (v2 21 Oct 2026, submitted to ApJ): across 107 lenses, power-law tracer fits give ΔBIC > 6 in 50–60% of isotropic Hernquist/Sérsic simulations, against 0.5–1% for matched tracers.
- Gomer & Williams 2020 (arXiv:1907.08638) and 2021 (arXiv:2103.16359), and Gomer et al. 2022 mock tests: biases from ellipse-plus-shear and power-law assumptions.
- Li, Tian et al. 2026, arXiv:2607.08576: composite stars + gNFW JWST model of WFI2033; the H0–R_s degeneracy "prevents a robust standalone constraint".
- Denzel et al. 2021, MNRAS 501, 784 (arXiv:2007.14398): free-form, 8 quads, no kinematics, 71.8 +3.9/−3.3; can reconstruct images "constraining to either value of H0".
- Colaço et al. 2025, EPJC 85, 577: model-independent 70.55 ± 7.44 from 7 TDCOSMO systems plus Pantheon+.
- Line of sight:
  - Teodori et al. 2022, JCAP 07, 027 (arXiv:2201.05111);
  - Johnson et al. 2026, TDCOSMO XXXI (arXiv:2609.11652), the first κ_ext including the observer–lens and lens–source terms;
  - Teodori 2026, JCAP 05, 046 (arXiv:2602.02802), multi-plane MST;
  - Tang et al. 2025, JCAP 10, 043 (arXiv:2506.04201), line-of-sight selection bias of about 0.1% for galaxy–AGN lenses.
- PSF: Krizic et al. 2026, ALPACA I (arXiv:2609.04312). Holding an imperfect PSF fixed "biases D_Dt by up to 14%"; joint PSF reconstruction brings this to the percent level.
- Review: Treu 2026, arXiv:2610.19598. Error-budget table: about 3% random and below 1% bias per galaxy lens; cluster-lens bias "?". It calls time-delay monitoring "the single most important limiting factor", a new modelling challenge "timely", and says the earlier challenge "turned out to be inconclusive".
- Microlensing time delay: Tie & Kochanek 2018; Chen et al. 2018 (subpercent); seen only as cited in Treu 2026.
- Xiong et al. 2026, arXiv:2606.03634: its ~8 km/s/Mpc difference between MST treatments is not at fixed data (RXJ1131 alone versus RXJ1131+WGD2038) and sits inside a siren sum-rule fit. Not a clean measure of the MST effect.

**Lensed supernovae**
- SN Refsdal (MACS J1149):
  - Kelly et al. 2023, Science 380, abh1322: 64.8 +4.4/−4.3 (8 models), 66.6 +4.1/−3.3 (2 best);
  - Grillo et al. 2024, A&A 684, L23: 65.1 +3.5/−3.4;
  - Liu et al. 2025, PRD 111 (23 models): 70.0 +4.7/−4.9; PRD 112: 66.0 ± 4.3;
  - Liu & Oguri 2026, arXiv:2609.39796: 65.9 +3.5/−3.4;
  - Schuldt et al. 2026, arXiv:2610.12595 v2: 65.0 +2.0/−1.8, with the cluster mass parametrisation fixed and κ_ext omitted.
  - All share the SX–S1 delay (Kelly et al. 2023, ApJ 948, 93), so they are not independent.
- SN H0pe (PLCK G165.7+67.0):
  - Pascale et al. 2025, ApJ 979, 13: 75.7 +8.1/−5.5 using SN Ia magnifications; 71.8 +9.2/−8.1 from delays and 7 models only;
  - Grayling et al. 2026, MNRAS 548 (arXiv:2510.11719): 69.3 +12.6/−7.8;
  - Agrawal et al. 2026: lens models overestimate the magnification by more than 1 mag.
- SN Encore and SN Requiem (MACS J0138):
  - Pierel et al. ApJ 998, 219 and Suyu et al. A&A 708, A291: Encore 66.9 +11.2/−8.1;
  - Bazzanini et al. 2026, arXiv:2606.25205: Encore+Requiem 69.2 +9.6/−8.0.
  - SN Requiem image 2d is predicted to appear April–December 2026 if H0 = 73, March–November 2027 if H0 = 67 (Suyu et al.), and January–May 2027 for H0 = 70 (Bazzanini: 3902 +72/−67 d). No detection paper had been found as of 2026-11-05.
  - Meena et al. 2026 (arXiv:2610.15999): shape degeneracies add 2.8–3.7% to the predicted reappearance and "transfer one-to-one to H0".
- SN 2025wny ("SN Winny"), z = 2.015, lensed by two galaxies at z = 0.376 (ZTF/GOTO; discovery ApJL 995, L17): Mörtsell et al. 2026, arXiv:2608.28430, 66.7 +7.6/−6.3 (isothermal) and 70.8 +8.2/−6.1 (free slopes); Johansson et al. 2026 and Townsend et al. 2026 (arXiv:2608.28416, 2608.28427). The photometric magnification is "a factor of ~2–4 higher than mass-modeling estimates".
- Cluster-lensed quasars: Napier et al. 2023 (74.1 ± 8.0); Martínez-Arrizabalaga et al. 2024 for J1004+4112 (74 +9/−13; strongly BCG-dependent).

**Data and programmes**
- JWST GO-7184 (PI Millon) and GO-9637 (PI Treu, Cycle 5, "A definitive test of the Hubble tension – independent of the local distance ladder"): NIRCam-imaged quads go from 3 to 19 and NIRSpec quads from 6 to 18, with a forecast 1.5% H0 in flat ΛCDM. Treu 2026: "on track to reach a conclusion in 1–2 years". About 40 lenses for 1% (Birrer & Treu 2021). A simple extrapolation of the per-lens information achieved so far (≈ 10.9% per lens) suggests closer to 120 lenses; this is the framing session's estimate, not published.
- Counts:
  - 364 confirmed lensed quasars (277 doubles, 87 quads or triples); 195 delays from 73 systems; "only 12 … with 2% precision or better" (Ducourant et al. 2026, A&A 707, A345; Treu 2026);
  - 22 new delays in TDCOSMO-XVII (Dux et al. 2025, A&A 697, A139);
  - 17 new lensed quasars modelled by Sheu et al. 2026 (arXiv:2608.07470), 6 "excellent" (≤ 3% D_Δt);
  - doubles could enlarge the sample "by a factor of five" (Paic et al. 2026); Brady et al. 2026 (TDCOSMO-XXVI, 8 doubles).
- Rubin LSST began its survey on 29 June 2026 (search summary). Forecasts: about 40 lensed SNe Ia and 80 lensed SNe II per year, about 10 Ia per year usable; O(1000) lensed AGN with delays, about 90% doubles. Erickson et al. 2025 (arXiv:2511.13669): about 800 LSST lensed AGN give about 2.5% on H0 in w0waCDM with the MST and anisotropy fully marginalised.
- Euclid: Q1 found 497 galaxy–galaxy lenses in 63 deg²; DR1-Foundation is planned for November 2026 (search summary).
- Roman: about 10 lensed SNe per year. No ELT time-delay timeline found.

**Gaps the framing review could not close:** whether SN Requiem image 2d has been detected; full-text error budgets for the lensed-SN papers; any 2026 response by Kochanek, Blum or Teodori aimed at TDCOSMO-2026; the assumptions behind the ~40-lens forecast; whether a new blind modelling challenge is planned.

## Prior runs
- 2026-10-30-hubble-tension-h0-discrepancy (2026-10-30): ignore. Complete and source-checked, but it is about the Hubble tension as a whole. The material relevant here (TDCOSMO values, the MST error budget, the H0 bands) is carried above as leads and context, at the user's request, so agents don't take on the wider tension.
- All other earlier runs (warp drives, wormholes, problem of time, neutron lifetime, gravitational-wave decay): ignore. Unrelated.
