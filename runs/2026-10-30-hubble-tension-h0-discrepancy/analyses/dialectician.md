# Analysis: dialectician (resolve real contradictions)
status: final
## Method applied
Pick the three most important contradictions in the dossier, state thesis and antithesis with evidence, find the regime/definition/selection under which both hold (or show which yields), and derive from each synthesis a prediction neither side made alone.

## Findings
Contradictions chosen (by weight on the answer): C-I SH0ES vs CCHP at fixed JWST data [D-80, D-81]; C-II "the gap is in r_d / M_B, so late-time physics is excluded" [D-70, D-06, D-21] vs "non-SN and one-step local methods also sit high" [D-29, D-30, D-31, D-32, D-90]; C-III "EDE is closed" [D-75, D-13, D-53 NPIPE/SPA] vs "EDE is preferred at 2-3σ" [D-53 Poulin, D-94].

1. **Per-SN calibrator scatter is 0.105–0.130 mag.** Two estimates from dossier numbers: R22 "SN calibrator statistics 0.020 mag" with 42 SNe gives 0.130 mag (dossier §6), and CCHP σ_SN = 0.70 km/s/Mpc with 24 SNe gives 0.105 mag [D-24] [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-dialectician_syntheses.py].
2. **The SH0ES–CCHP "selection" effect is too big for pure SN noise.** SH0ES says the same method (HST Cepheids) gives 71.2 on the CCHP-selected subset and 73.6–73.9 on the SH0ES-selected set [D-28]. That 2.55 km/s/Mpc gap is 2.3–2.9σ of the expected 11-of-42 subset noise (0.89–1.10 km/s/Mpc). The 11 hosts outside CCHP's 24 give 74.1 against 70.39 [D-27], which is 2.4–3.0σ of SN-only noise (1.25–1.55 km/s/Mpc); per-host distance errors, not included here, would bring this toward the "2σ" Li et al. quote [calc: same]. So "selection" is either an unlucky draw (p ≈ 0.01–0.02) or a *non-random* host property that correlates with SN standardisation.
3. **The SH0ES–CCHP JWST gap splits roughly in half.** SH0ES 73.49 minus CCHP JWST-only 68.81 = 4.68 km/s/Mpc. About 2.55 is calibrator-set selection (same method, different hosts) [D-28]. The remaining ~2.39 km/s/Mpc (0.074 mag) is method, analysis or SN-photometry on the same subset [calc: same]. Hoyt's SN-compilation dependence alone accounts for 1.2 km/s/Mpc (0.036 mag) of spread [D-25].
4. **The CCHP headline sits between the poles and is no strong witness for either.** CCHP TRGB 70.39 ± 1.94 (total) is 1.44σ from SH0ES and 1.62σ from CMB-SPA. CCHP JWST-only 68.81 ± 1.80 is 2.31σ from SH0ES and 0.88σ from CMB-SPA. These are naive figures: the shared NGC 4258 anchor and shared SNe would reduce the SH0ES-side z [calc: same].
5. **What H0 = 73.3 asks of r_d.** With DESI DR2 h·r_d = 101.54 ± 0.73 Mpc [D-45], H0 = 73.26 needs r_d = 138.6 ± 1.0 Mpc, 5.7% below CMB-SPA's 147.00 Mpc [D-44]. Against the DESI+BBN-consistent r_d (148.2 Mpc at H0 = 68.5) the cut is 6.5%. The ladder–inverse-ladder M_B offset is +0.122 mag (cosmography) to +0.141 mag (flat ΛCDM) [D-21], i.e. an H0 ratio of 1.058–1.067 [calc: same].
6. **Anchor-free one-step methods agree with each other and sit at two-thirds of the way to the ladder.** TDCOSMO-2026 71.1, masers 71.6 (stat only) and GWTC-5 sirens 71.7 [D-31, D-32, D-33] are internally consistent (χ² = 0.02/2) with a weighted mean of 71.27 ± 1.93 km/s/Mpc. That mean is 2.07σ above CMB-SPA, 1.37σ above DESI BAO+BBN, and 0.95σ below corrected H0DN [D-22]. Neither the r_d anchor nor the ladder anchors enter it [calc: same].
7. **The precision an anchor-free probe needs.** Separating 67.19 from 73.26 (Δ = 6.07 km/s/Mpc) takes σ = 2.02 km/s/Mpc (2.9%) at 3σ and 1.21 km/s/Mpc (1.7%) at 5σ. If the truth sits at the midpoint (70.2), excluding both poles at 3σ needs 1.01 km/s/Mpc (1.45%) [calc: same].
8. **Fraction of the gap EDE-class models close, against the same-data ΛCDM 68.22 [D-42].** ACT P-ACT-LB EDE closes 0.33 (residual vs H0DN 2.96σ, upper-side error). ACT P-ACT EDE closes 0.21 (3.28σ). Poulin 2026 profile closes 0.55 (1.66σ). eROSITA+ext closes 0.63 (1.15σ). Modified recombination closes 0.27 (2.85σ), PMF 0.17 (4.39σ), electron-density fluctuations on ACT+SPT 0.21 (4.18σ) [D-52, D-53, D-94, D-95]. The Planck NPIPE 95% upper H0 of 69.5 is 4.7 H0DN-σ below the ladder [D-53] [calc: same].
9. **The two EDE camps are numerically compatible in f_EDE.** The profile best fit f = 0.09 ± 0.03 is only 0.67–0.97 profile-σ above the Bayesian 95% upper limits 0.061–0.070 [D-53, D-75]. They disagree about *what the data say about H0*, not about f_EDE [calc: same].
10. **A host-type split does not push H0 low.** A pilot parallel ladder using only SNe Ia in early-type/quiescent hosts with TRGB distances gives a high value [new: Newman et al. 2026, ApJ 1006, 178 (arXiv:2508.20023), abstract via fetch_text, "We obtain a measurement of the Hubble constant, $H_0 = 75.3 \pm 2.9$ km s$^{-1}$ Mpc$^{-1}$, including statistical and estimated systematic uncertainties"]. It is a small sample, but it cuts against a reading of C-I in which CCHP's TRGB-friendly hosts carry intrinsically fainter standardised SNe. The authors also advocate host-matched subsamples, i.e. they treat host-property mismatch as a live systematic [new: same, "we advocate that future cosmological applications of SNe Ia use subsamples matched in host-galaxy"].
11. **H0 World Cup II, a 2026 common-pipeline contest with ACT and SPT (preprint, not in dossier).** It ranks early non-radiative energy injection best, and no class gets below about 3σ [new: Schöneberg, Poulin et al. 2026, arXiv:2607.13283, full text p. 45 via fetch_text, "Group E gives the best overall performance.These models reduce the residual tension to approximately 3σand are strongly favored over ΛCDM by the model-comparison metrics. •Group M provides an intermediate improvement.Its best-performing model reduces the residual tension to approximately 4σ ... •Group R performs only marginally better thanΛCDM.Its best model leaves a residual tension of approximately 4.5σ"]. Late-time models fail: "the residual tension remains above 5σfor this model, as for the other contenders in groups L and" (p. 23). Evolving dark energy makes it worse: "none of the models benefit from the inclusion of an evolving dark energy equation of state in their ability to ease the Hubble tension. For all models the tension metrics increase by up to 0.5σ" (p. 30). It also reads the DESI–CMB Ω_m discrepancy as "partially driving the preference for dynamical dark energy" (p. 30). The group labels are the paper's own: E is early energy injection plus modified gravity, M modified recombination, R extra radiation, L late-time.
12. **Sound-horizon-free H0 values sit low-to-middle, not at the ladder.** The DESI DR1 r_d-free values [D-49] are 69.2, 70.3 and 69.6. They lie 1.8–2.7σ below corrected H0DN and 1.3–2.5σ above CMB-SPA. The older set (66.7, 67.9) lies 2.6–3.5σ below H0DN and 0.3σ from CMB-SPA. These are naive figures, and all sets are correlated through DESI DR1. If "r_d is wrong and the ladder is right" (pure early-time cause), an r_d-free early-type measurement should land near 73. None does [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-dialectician_syntheses.py].
13. **The common offset a ladder systematic would need.** Taking H0DN (73.264) down to CMB-SPA (67.19) takes 0.188 mag; down to DESI BAO+BBN (68.50) takes 0.146 mag. For the ladder to be the dominant cause, this offset must be shared by Cepheid, TRGB and JAGB calibrations, which agree to ≲0.03–0.05 mag on matched hosts [D-09, D-26, D-28]. It must also survive dropping any single anchor (no NGC 4258: 73.08; no MW: 73.61 [D-23]) and carry over to the non-SN ladders (SBF 73.8, TF 73.3 [D-29, D-30]) [calc: same].

## Lens-specific outputs

### Contradiction I: SH0ES vs CCHP on (largely) the same JWST data
- **Thesis (CCHP).** JWST TRGB, JAGB and Cepheids give 68.8–70.4 km/s/Mpc, "consistent with ΛCDM" [D-24, D-25, D-26]. This implies the Cepheid ladder is biased high.
- **Antithesis (SH0ES and the H0DN side).** JWST confirms HST Cepheid photometry (−0.01 ± 0.03 mag; crowding rejected at 8.2σ) [D-09, D-78]. The same JWST TRGB and JAGB methods on more hosts, or on a distance-limited set, give 72.1–73.3 [D-26 Li, D-27, D-28]. The difference is calibrator selection [D-28], and removing Cepheids from H0DN leaves 72.5 [D-23].
- **Where both hold.** The *primary distance indicators* agree on matched hosts: JAGB−Cepheid −0.03 ± 0.02 ± 0.05 mag [D-26], and the three methods in one distance-limited sample span 72.1–73.4 [D-28]. Each team's photometry is then right. What differs is (a) *which SNe Ia are calibrated*, about 2.5 km/s/Mpc [D-28; F2, F3], and (b) *which low-z SN photometry system* converts them, about 1.2 km/s/Mpc between Pantheon+ and CSP [D-25]. Both statements hold if the H0 a TRGB ladder returns is set by its calibrator set, not by TRGB physics.
- **What yields.** CCHP's inference "low H0 ⇒ Cepheids are biased" yields, because on matched hosts the methods agree. SH0ES's "entirely consistent with sample selection" is *strained*, not refuted: the subset offset is 2.3–2.9σ of pure SN scatter (F2). Either the CCHP subset is a p ≈ 0.01–0.02 draw, or there is a non-random host or SN-photometry effect. The early-type parallel ladder at 75.3 ± 2.9 (F10) argues against the simplest host-type version of the latter.
- **Synthesis.** The SH0ES–CCHP dispute is a dispute about the *SN calibration sample and photometry system*, not about the *primary indicator*. It can move a ladder H0 by about 1–2.5 km/s/Mpc, a third to a half of the 6 km/s/Mpc gap, and no more.
- **Prediction neither side made alone.** (i) CCHP's own pipeline run on all ~35 TRGB hosts with Pantheon+ should return ≥ 71.5 km/s/Mpc, and with CSP about 1 km/s/Mpc lower. (ii) The CCHP–SH0ES offset should shrink roughly as √(1/n_sub − 1/N) as calibrator counts grow (Rubin and JWST take 37 to 60–80 hosts [dossier §6]). (iii) If the offset does *not* shrink, the residual must correlate with an SN or host property (colour, host mass, morphology, photometric system) rather than with the primary method. That would be an SN-standardisation systematic shared by *all* SN ladders [D-82], which neither team currently claims.

### Contradiction II: "the gap is in r_d·H0 / M_B, so late time is excluded" vs "non-SN and one-step local methods also sit high"
- **Thesis.** BAO plus uncalibrated SNe fix r_d·H0, and with the standard r_d any late-time H(z) gives H0 ≈ 67–68 [D-03, D-07, D-70]. The conflict is in M_B: ladder −19.253 against inverse −19.375/−19.394, i.e. 0.12–0.14 mag [D-21; F5]. DESI w0wa lowers H0 [D-12, D-51]. In World Cup II, late-time models leave >5σ and evolving DE worsens every model by up to 0.5σ (F11).
- **Antithesis.** The high value does not need SNe Ia: SBF gives 73.8 ± 2.4 and TF 73.3 ± 4.1 [D-29, D-30], and H0DN with SNe replaced by galaxy indicators changes by <0.1 [D-23]. The anchor-free one-step methods (lenses, masers, sirens) average 71.3 ± 1.9, and TDCOSMO's no-LDL combination stays 2.7σ above Planck [D-90; F6].
- **Where both hold.** "Late" conflates two things: the *expansion history* H(z) after recombination, and the *local absolute distance scale*, meaning the anchors plus primary indicators that every ladder, SN or not, inherits. SBF and TF are zero-pointed on the same Cepheid/TRGB/NGC 4258 rungs [D-29, D-30, D-22 "not independent"]. Their agreement therefore tests the SN rung, not the primary rung. The thesis is right that H(z) cannot be the cause. The antithesis is right that the high value is not an SN-only artefact. The contradiction is between *two absolute calibrators*: r_d, an early-physics ruler, and the geometric-anchor distance scale. Only the anchor-free methods sit outside both.
- **What yields.** The brief's "early vs late" partition yields to "r_d-calibrated vs anchor-calibrated vs calibrator-free". "The tension is in M_B" yields in part too, since it is in the absolute scale of whichever local indicator is used. Neither thesis nor antithesis yields on its core numbers.
- **Synthesis.** The dominant cause must act on r_d (a 5.7–6.5% shrink to 138.6 Mpc [F5]) or on the shared local absolute scale (0.146–0.188 mag common to Cepheid, TRGB, JAGB and all anchors [F13]). It cannot act on H(z). The arbiter is the class that uses neither ruler. It currently sits two-thirds of the way toward the ladder (71.27 ± 1.93: 2.1σ from CMB-SPA, 0.95σ from H0DN). The r_d-free early-type values sit at 66.7–70.3 (F12).
- **Prediction neither side made alone.** (i) *Pure early-time cause*: r_d-free methods (equality scale, uncalibrated BAO + θ_*) **and** anchor-free one-step methods both converge on about 73. (ii) *Shared local-scale systematic*: both converge on 67–68.5. (iii) *Neither*, the current pattern, with one-step about 71 and r_d-free about 69–70: two partial causes, which is the null. A one-step aggregate at 1.45% (1.0 km/s/Mpc) that keeps a central value of about 70–71 would exclude **both** 67.2 and 73.3 at 3σ (F7). Neither the "it's the ladder" camp nor the "it's new physics" camp predicts that outcome.

### Contradiction III: "EDE is closed" vs "EDE is preferred"
- **Thesis.** Bayesian fits to the full CMB give f_EDE < 0.061 (Planck NPIPE) and < 0.070 (SPT+ACT+Planck), with H0 < 69.5 at 95% and a residual of 3.6–3.7σ [D-53, D-75]. ACT DR6 says "not favored" [D-13].
- **Antithesis.** The profile likelihood (Planck ℓ<1000 + ACT + DESI DR2 + Pantheon+) gives f = 0.09 ± 0.03 and H0 = 71.0 ± 1.1 [D-53]. eROSITA plus external data give f = 0.10 (+0.04/−0.03, 3.2σ) and H0 = 71.4 ± 1.4 [D-94]. World Cup II ranks group E best, with residual about 3σ (F11).
- **Where both hold.** The f_EDE values are mutually compatible within 0.7–1.0σ (F9). Three things divide the camps. (a) *Statistics*: Bayesian prior-volume effects suppress f when H0 and z_c are poorly constrained, while a profile likelihood does not [D-75]. (b) *Data*: dropping Planck at ℓ > 1000 and SPT loosens the bound [D-83]. (c) *DESI*: adding DESI DR2 creates the preference, and SPT and World Cup II both trace it to the DESI–CMB Ω_m discrepancy [D-53 Khalife; D-83; F11]. So both are true: f ≈ 0.05–0.09 is allowed, and preferred only when DESI's low Ω_m is in the fit.
- **What yields.** "EDE resolves the tension" yields: no fit without a SH0ES prior reaches 73, and the best cases close 0.33–0.63 of the gap, leaving residuals of 1.2–3.0σ against H0DN (F8). "EDE is excluded" also yields: at f ≈ 0.06–0.09 it is alive.
- **Synthesis.** EDE-class physics is at most a *partial* cause, worth about 1.5–3 km/s/Mpc. Its present 2–3σ support is borrowed from the separate DESI–CMB Ω_m anomaly.
- **Prediction neither side made alone.** (i) The EDE preference and the BAO–CMB Ω_m discrepancy must rise and fall together. If DESI DR3/final Ω_m moves to ≥ 0.31, the EDE profile preference should fall below about 1.5σ. If the discrepancy grows, f_EDE ≈ 0.08 persists, but H0 still stops at about 71. (ii) If EDE is real at f ≈ 0.08, the ladder must still be about 2 km/s/Mpc (≈ 0.06 mag) high, so "EDE dominant" is unstable against "EDE + ladder offset", which is the null. (iii) The damping-tail and polarisation measurements of Simons Observatory and SPT-3G Ext-10k, rather than any H0 measurement, decide whether f ≈ 0.08 or f ≈ 0; the forecast σ(f) is not computed here.

### Contradiction-to-candidate map
| Contradiction | What yields | Candidate it feeds | Its distinctive prediction |
|---|---|---|---|
| I SH0ES vs CCHP | "Cepheids biased"; partly "pure random selection" | A (ladder systematic, SN-calibration sub-hypothesis), D (null) | CCHP pipeline on all ~35 TRGB hosts ≥ 71.5; the offset shrinks with N or tracks an SN/host property |
| II no-go vs non-SN highs | "early vs late" partition; "only M_B" | E (reframe), C eliminated, A strained | One-step and r_d-free converge together at 73 (early), at 67–68.5 (local scale), or at 70–71 (null) |
| III EDE closed vs open | "EDE resolves"; "EDE excluded" | B (early-time), D (null) | EDE preference tracks the DESI Ω_m anomaly; H0 ceiling about 71 |

## Calculations
- `runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-dialectician_syntheses.py` (log beside it). It computes:
  - per-SN calibrator scatter: 0.105–0.130 mag;
  - subset-noise σ: 0.89–1.10 km/s/Mpc for 11-of-42, 1.25–1.55 km/s/Mpc for 24 vs 11 disjoint; the SH0ES-reported selection effect of 2.55 km/s/Mpc is 2.3–2.9σ of it;
  - the SH0ES−CCHP-JWST decomposition: 4.68 = 2.55 (selection) + 2.39 (0.074 mag residual) km/s/Mpc;
  - naive CCHP tensions: 1.44σ (to SH0ES) and 1.62σ (to CMB-SPA) for 70.39; 2.31σ and 0.88σ for 68.81;
  - required r_d from DESI h·r_d: 138.6 Mpc for 73.26 (−5.7% vs 147.00 Mpc);
  - M_B offset: 0.122–0.141 mag;
  - one-step mean: 71.27 ± 1.93 km/s/Mpc (χ² 0.02/2), 2.07σ from CMB-SPA and 0.95σ from H0DN;
  - precision needed: 2.02 km/s/Mpc (2.9%) at 3σ, 1.21 km/s/Mpc (1.74%) at 5σ, and 1.01 km/s/Mpc (1.45%) to exclude both poles from the midpoint;
  - r_d-free tensions (F12);
  - the ladder common-offset need: 0.146–0.188 mag;
  - fraction of the gap closed by each EDE-class fit (0.17–0.63) and its residual (1.15–4.39σ);
  - f_EDE compatibility: 0.07–0.97σ.
- All tensions are naive (uncorrelated, two-sided, side-facing error for asymmetric values). Correlations (NGC 4258, Pantheon+, DESI DR1) are not modelled; the statistician owns them.

## Candidate answers (at least 3; the null and a reframe count)
- [DIALECTICIAN-A] **Null: no single dominant cause.**
  - **Claim.** The gap is the sum of comparable partial contributions: about 1–2.5 km/s/Mpc from SN-calibrator sample, photometry and peculiar-velocity choices on the ladder side; about 1.5–3 km/s/Mpc possibly from early-time physics such as EDE at f ≈ 0.05–0.09, or from the DESI–CMB Ω_m anomaly; plus statistical fluctuation.
  - **Status.** Surviving.
  - **Why.** It is the synthesis of all three contradictions. In C-I the SH0ES–CCHP dispute is worth about a third to a half of the gap and no more (F2–F4). In C-II the anchor-free one-step mean (71.3 ± 1.9) and the r_d-free values (69–70) sit between the poles (F6, F12). In C-III the best EDE fits stop at about 71 and close 0.3–0.6 of the gap (F8, F11).
  - **Distinguishing prediction.** An anchor-free one-step aggregate (time delays, masers, sirens) reaching 1.45% (1.0 km/s/Mpc) with a central value of 70–71 excludes both 67.2 and 73.3 at 3σ. Neither pole camp predicts this. CCHP's pipeline on all ~35 TRGB hosts should rise to ≥ 71.5 while staying below SH0ES.
  - **Confidence.** Medium.
- [DIALECTICIAN-B] **Distance-ladder systematic, dominant (≥ 0.15 mag).**
  - **Sub-hypotheses, as the C-I/C-II syntheses rank them:**
    - (b1) an SN-calibration-sample or photometry-system effect shared by all SN ladders, the only one with a mechanism that matches the SH0ES–CCHP pattern;
    - (b2) Cepheid selection (Percival, D-88);
    - (b3) Hubble-flow peculiar velocities (Dong, D-82);
    - (b4) an anchor-scale error;
    - (b5) Cepheid crowding or metallicity, already bounded at about 0.03 mag [D-09, D-15].
  - **Status.** Strained.
  - **Why.** C-II's synthesis needs a 0.146–0.188 mag offset (F13). It must be shared by Cepheid, TRGB and JAGB, which agree to ≲0.05 mag on matched hosts, and by all anchors (dropping any one moves H0DN by ≤ 0.4). (b1) also fails to explain SBF and TF at 73–74, which bypass SNe. The anchor-free methods lean against it at 2.1σ (F6). The C-I effects are real but sized at about 1–2.5 km/s/Mpc.
  - **Distinguishing prediction.** Anchor-free one-step methods *and* r_d-free early-type methods converge on 67–68.5. CCHP and SH0ES offsets track an SN or host property, not the primary method.
  - **Confidence.** Low–medium.
- [DIALECTICIAN-C] **Early-time new physics, dominant (r_d shrunk by 5.7–6.5% to about 138.6 Mpc).**
  - **Variants.** EDE (best, World Cup II group E); modified recombination or varying m_e; extra radiation or SIDR; PMF; electron-density fluctuations.
  - **Status.** Strained.
  - **Why.** C-III's synthesis allows f ≈ 0.05–0.09, but no fit without a SH0ES prior reaches 73 (69.1–71.4; residual 1.2–4.4σ) (F8). World Cup II leaves about 3σ (E), about 4σ (M) and about 4.5σ (R) (F11). The present preference is tied to the DESI Ω_m anomaly. C-II adds that r_d-free H0 values (66.7–70.3) do not rise to 73, as a pure r_d cause would require (F12). Varying m_e+Ω_k and PMF are weaker than EDE once ACT and DESI are included [D-17, D-76].
  - **Distinguishing prediction.** If dominant, the anchor-free one-step methods and the r_d-free methods both converge on about 73. The EDE preference survives a DESI Ω_m that moves to ≥ 0.31. The SO/SPT damping tail detects f ≈ 0.1.
  - **Confidence.** Low as dominant, medium as a partial contributor (which folds into A).
- [DIALECTICIAN-D] **Reframe: two absolute calibrators disagree, not early vs late.**
  - **Claim.** The anomaly is "r_d-calibrated distances vs anchor-calibrated distances", which makes M_B too narrow a statement and "early vs late" the wrong partition. The deciding class is calibrator-free one-step H0.
  - **Status.** Surviving.
  - **Why.** It is the C-II synthesis. The inverse-ladder no-go and the non-SN highs hold at once only under this partition [D-07, D-29, D-30, D-70, D-90]. It also explains why late-time H(z) models fail everywhere (World Cup II >5σ; DESI w0wa lowers H0) (F11, D-12) while the local high value is not SN-specific.
  - **Distinguishing prediction.** No modification of H(z) at 0 < z < 2 changes the gap by more than about 0.5σ. The ratio of the one-step H0 to the ladder H0 and to the r_d-based H0 is the diagnostic: it needs 1.7% (5σ) or 2.9% (3σ) precision on the one-step class (F7).
  - **Confidence.** Medium–high, as a statement of the problem rather than a cause.
- [DIALECTICIAN-E] **Late-time new physics, dominant.**
  - **Variants.** Phantom/w0wa, interacting DE, sign-switching Λ, low-z M_B/G_eff transition.
  - **Status.** Eliminated (except the M_B/G_eff transition, which is strained).
  - **Why.** The thesis of C-II stands unrefuted: r_d·H0 is fixed by BAO+SN [D-70]. DESI w0wa lowers H0 to 63.6–67.5 [D-51]. In World Cup II, late-time groups leave >5σ and evolving DE worsens every model by up to 0.5σ (F11). The M_B/G_eff escape [D-92] changes M_B, not H(z). But a μ_G jump at z ≈ 0.01 would leave non-SN ladders (SBF, TF) and the one-step methods unaffected, while those methods also read high or middle; that makes it strained.
  - **Distinguishing prediction.** A G_eff transition predicts that SN calibrators at D < 40 Mpc and Hubble-flow SNe differ by about 0.2 mag in standardised M_B, while SBF→Hubble-flow ladders read low. They read 73.8, so that disfavours it.
  - **Confidence.** High that it is not dominant.
- [DIALECTICIAN-F] **Local structure (void or bulk flow), dominant.**
  - **Status.** Eliminated.
  - **Why.** No real contradiction exists here. ΛCDM cosmic variance is 0.31 km/s/Mpc (gap ≈ 18–20σ). The SN Hubble diagram excludes |δ| > 20% at 4–5σ. Flow corrections are +0.6 to +1.4, the wrong sign for closing the gap [D-10, D-11, D-36, D-37, D-77]. The only "for" is a minority preprint [D-84].
  - **Distinguishing prediction.** If true, H0 measured at 0.15 < z < 0.5 by one-step methods would be about 67. The TDCOSMO lenses at z ~ 0.3–0.7 give 71.1, which does not support it.
  - **Confidence.** High.
- [DIALECTICIAN-G] **Early-universe analysis systematic (CMB likelihood, foregrounds, BAO), dominant.**
  - **Status.** Eliminated.
  - **Why.** Planck, ACT and SPT with independent instruments agree at 66.5–67.6 [D-02, D-41–D-43]. The A_L anomaly fades in PR4 [D-79a]. BAO+BBN without CMB anisotropies gives 68.5 [D-08]. The likelihood choice moves P-ACT by 0.24 [D-41].
  - **Distinguishing prediction.** If true, SO would shift ΛCDM H0 by ≥ 2 km/s/Mpc relative to Planck, ACT and SPT. Nothing points to that.
  - **Confidence.** High.

## What would change my mind
- An anchor-free one-step aggregate at ≤ 1.7% precision landing at ≥ 72.5 together with an r_d-free value ≥ 72 would promote C (early-time) over A. Landing at ≤ 68.5 would promote B (ladder).
- CCHP running its pipeline on the full ~35 TRGB host set and still getting ≤ 70 with Pantheon+ would mean the SH0ES–CCHP split is methodological after all, and would raise B (b1/b5).
- DESI DR3 Ω_m converging on the CMB value while the EDE profile preference stays ≥ 2.5σ would break the C-III synthesis (EDE independent of the Ω_m anomaly) and raise C.
- A verified correlated combination (statistician) showing the one-step mean is ≥ 3σ from CMB-SPA would weaken A in favour of a local-high truth.
- Evidence that SBF and TF zero points are in fact independent of the Cepheid/TRGB rung would weaken the C-II synthesis that "non-SN highs test only the SN rung".

## Assumptions I relied on
- Per-SN calibrator scatter of 0.105–0.130 mag, derived from dossier error terms, ignoring per-host primary-distance errors. That makes the "2.3–2.9σ selection" figure an upper estimate.
- The SH0ES-reported HST predictions for the CCHP- and SH0ES-selected subsets (71.2; 73.6–73.9) [D-28, not individually checked] are taken at face value.
- Naive, uncorrelated tensions throughout. The shared NGC 4258 anchor, Pantheon+ and DESI DR1 correlations are not modelled.
- The maser value 71.6 ± 3.7 is statistical only. Siren and TDCOSMO errors are symmetrised as (up + down)/2.
- The same-data ΛCDM baseline for "fraction of gap closed" is P-ACT-LB 68.22 for every EDE-class result, although the Poulin and eROSITA fits use different data.
- World Cup II is a July 2026 preprint, quoted from full text. Its group-level residual-σ figures are its own metric (DMAP against its local calibration dataset), not this run's statistician's.
