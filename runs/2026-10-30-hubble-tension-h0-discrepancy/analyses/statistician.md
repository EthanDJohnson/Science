# Analysis: statistician (is the signal real?)
status: final

## Method applied
Reconstruct each H0 value as numbers (stat/sys separated as quoted), keep one value per independent dataset (superseded values excluded), and recompute every tension two-sided with asymmetric errors on the facing side; combine within and between measurement classes with grouped chi2 and with explicit correlations (rho = 0 and larger) for shared anchors / shared CMB data; bound the evidence with min Bayes factors; compute the precision a deciding measurement needs.

## Findings
1. **Headline pairwise tensions, recomputed (two-sided, uncorrelated, total errors in quadrature; km/s/Mpc).** SH0ES 2025 Cepheid–SN 73.49 ± 0.93 [D-20] against CMB-SPA 67.19 ± 0.38 [D-44]: Δ = +6.30 ± 1.00, **z = 6.27** (p₂ = 3.6×10⁻¹⁰). Against Planck PR4 67.64 ± 0.52 [D-41]: Δ = +5.85 ± 1.07, z = 5.49. Against DESI DR2 BAO+BBN 68.50 ± 0.58 [D-45], which uses no CMB anisotropies: Δ = +4.99 ± 1.10, **z = 4.55**. Against the joint DESI+CMB ΛCDM fit 68.17 ± 0.28: z = 5.48. Check: the superseded R22 73.04 ± 1.04 against PR3 67.36 ± 0.54 gives 4.85σ, against the quoted "5.0σ" [D-57], which used the M_B framing 0.176 ± 0.035 mag [D-06]. The corrected H0DN 73.264 ± 0.806 [D-22] against CMB-SPA gives z = 6.82, and against H0DN's own "67.24 ± 0.35" z = 6.86, so I reproduce the quoted 6.85σ. Against BAO+BBN it gives z = 4.80. [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-statistician_tensions.py]
2. **CCHP removes the tension pairwise, but it does not contradict SH0ES either.** CCHP TRGB 70.39 ± 1.94 (1.22 stat, 1.33 sys and 0.70 σ_SN in quadrature) [D-24] against CMB-SPA: z = 1.62; against Planck PR4: 1.37; against BAO+BBN: 0.94. CCHP against SH0ES: Δ = −3.10. That is z = 1.44 at ρ = 0, and 1.65 / 1.85 / 2.36 at ρ = 0.3 / 0.5 / 0.8 (shared NGC 4258 anchor and overlapping calibrator SNe; a positive correlation *raises* the significance of the difference). The CCHP and SH0ES-side JAGB analyses of overlapping data [D-26] differ by 5.5 ± 3.65 (1.5σ). CCHP is statistically compatible with both camps: its error is about 2× SH0ES's. [calc: lens-statistician_tensions.py]
3. **One-step methods alone carry little weight.** TDCOSMO-2026 71.1 +2.4/−2.3 [D-31] against CMB-SPA: z = 1.68; against Planck PR4: 1.47; against H0DN: 0.85; against SH0ES: 0.93. This confirms the checker's ≈0.95σ and ≈1.66σ and contradicts the researcher's 1.7σ/1.5σ [D-31, §7]. Masers 71.6 ± 3.7 (stat only) [D-32]: 1.19σ from CMB-SPA. Sirens 71.7 +9.4/−7.5 [D-33]: 0.60σ. The inverse-variance mean of the three one-step methods is 71.27 ± 1.93, **1.88σ** above the early mean 67.58 ± 0.32. [calc: lens-statistician_grouped.py]
4. **The M_B statement of the gap.** R22 M_B = −19.253 ± 0.027 mag against the inverse-ladder −19.375 (cosmography) and −19.394 (flat ΛCDM) [D-21] gives Δ = 0.122 mag (3.76σ) and 0.141 mag (4.42σ). This is smaller than the H0 framing because the inverse ladder uses DES-SN5YR + DESI DR1, not the Pantheon+ system, so the comparison mixes SN systems [D-21 caveat]. In H0 terms the gap is 5 log₁₀(73.49/67.19) = 0.195 mag (9.4%) against CMB-SPA, and 0.153 mag (7.3%) against BAO+BBN. [calc: lens-statistician_tensions.py]
5. **Grouped χ², per class** (CMB-SPA; BAO+BBN; Cepheid-SN; CCHP TRGB-SN; non-SN ladders SBF+TF; time delays; masers; sirens; asymmetric errors symmetrised as the mean of the two sides). Within-class χ² = 0.01/1, because most classes have a single current value. Between-class χ² = 49.87/7, **z = 5.66**. The pooled mean is 68.43 ± 0.29 with PDG scale factor S = 2.50. Quoting that scaled pooled mean would hide a split between methods. [calc: lens-statistician_grouped.py]
6. **Which partition fits (premise 2).**
   - P1, early (CMB-SPA, BAO+BBN) against late (all seven local classes, with CCHP as the TRGB value): within χ² = 6.50/7 (p = 0.48); between χ² = 43.4/1, **6.59σ**. The late mean is 72.77 ± 0.72 and the early mean is 67.58 ± 0.32.
   - P2, SH0ES Cepheid-SN against everything else: within χ² = 17.0/7 (**p = 0.017**); between 5.73σ.
   - P3, three groups (early | Cepheid-SN | other local): within 5.01/6. Other local = 71.69 ± 1.14, which is 3.5σ above early and 1.2σ below SH0ES.
   - P4, uses r_s against no r_s (adding the sound-horizon-free BAO H0 69.2 [D-49] to the late side): within 11.95/8 (p = 0.15); between 6.18σ.

   With the same number of groups, the early/late split fits the current data better than "SH0ES against the rest" (Δχ²_within ≈ 10.5). The non-Cepheid local values sit nearer SH0ES than the CMB, although only at about 1–3σ each. [calc: lens-statistician_grouped.py]
7. **The significance without Cepheids and without SNe.**
   - Local without SNe or Cepheids (SBF, TF, TD, masers, sirens) = 72.39 ± 1.41 against early 67.58 ± 0.32: **3.32σ**.
   - One-step only: 1.88σ.
   - H0DN without Cepheids 72.509 ± 1.296 [D-23] against CMB-SPA: 3.94σ.

   These match the TDCOSMO companion's "3.7σ no-SN" and "2.7σ no-LDL" against Planck alone [D-57, D-90] in rough size. SBF and TF share the NGC 4258/TRGB calibration with the ladders, so the "no-SN" set is not fully independent of the ladder anchors. [calc: lens-statistician_grouped.py]
8. **Correlated local combination** (GLS; shared NGC 4258 anchor with assumed weights SH0ES 1/3, CCHP 1, SBF 1, TF 0.5, one-step 0; anchor error 0, 1.5% or 2.5% of H0):
   - local = 72.77 ± 0.72 / 72.86 ± 0.80 / 73.24 ± 0.83;
   - against CMB-SPA: z = 6.85 / 6.40 / 6.66;
   - against BAO+BBN: z = 4.62 / 4.41 / 4.70.

   The anchor correlation changes the local–early significance by under 0.5σ, and my simple combination reproduces H0DN 73.26 ± 0.81 to within 0.5 km/s/Mpc. [calc: lens-statistician_grouped.py]
9. **Internal consistency of the early side.**
   - Planck PR4, ACT DR6 alone and SPT-3G alone [D-41–D-43]: χ² = 2.42/2 (p = 0.30), mean 67.03 ± 0.33. ACT and SPT share the PR4 τ prior, which is ignored here.
   - CMB against BAO+BBN: 2.20σ (CMB-SPA against BAO+BBN: 1.89σ). This is the DESI–CMB Ω_m discrepancy [D-45, D-87], and it runs *toward* the local side.
   - Adding the inverse ladder [D-48] (r_d from the CMB) at ρ = 0, 0.5 or 0.8 leaves the early mean at 67.5–67.6 ± 0.3.

   The early side is internally consistent at ≲2.2σ. [calc: lens-statistician_grouped.py]
10. **Look-elsewhere over analysis choices** (which local headline is paired with which early headline; Šidák, which is conservative because the choices are strongly correlated):
    - SH0ES against CMB-SPA: local 6.27σ, global 5.90σ / 5.72σ / 5.51σ for N = 10 / 30 / 100;
    - H0DN against BAO+BBN: local 4.80σ, global 4.31 / 4.06 / 3.77σ;
    - H0DN without Cepheids against CMB-SPA: local 3.94σ, global 3.35 / 3.03 / 2.64σ.

    The internal analysis variants are small next to the gap. The H0DN variant centres scatter by 0.40 km/s/Mpc [D-23], about 7% of the gap. [calc: lens-statistician_tensions.py]
11. **Bayes-factor bounds** (null = one common H0).
    - SH0ES against CMB-SPA (z ≈ 6.3, p₂ = 3×10⁻¹⁰): Sellke bound BF_null ≥ 1.8×10⁻⁸, i.e. at most about 5.6×10⁷ : 1 against a fluctuation. An explicit Gaussian prior on the offset of width τ = 3, 6 or 10 km/s/Mpc gives BF(two/one) = 1.5×10⁷, 3.3×10⁷ and 2.8×10⁷.
    - SH0ES against BAO+BBN: BF ≈ 3–4×10³.
    - The non-Cepheid local set (z ≈ 3.9): at most 413 : 1.
    - CCHP against CMB-SPA and TDCOSMO against CMB-SPA: BF(two/one) = 0.7–1.4, i.e. no evidence either way.

    The evidence for "two values" therefore comes almost entirely from Cepheid-calibrated SNe (and from the combinations that contain them). [calc: lens-statistician_tensions.py, lens-statistician_grouped.py]

12. **Reference class: heavy tails in disagreements between precision measurements.** Bailey 2017 [new: Bailey, Royal Society Open Science 4, 160600 (doi:10.1098/rsos.160600), full-text via Europe PMC, "Outliers are common, with 5 σ disagreements up to five orders of magnitude more frequent than naively expected" and "all can reasonably be described by almost-Cauchy Student’s t -distributions with ν ∼2−3 ... The number of ‘5 σ ’ (i.e. z >5) disagreements observed is as high as 0.12, compared with the 6×10 −7 expected for a Normal distribution"].
    - Under Student-t with ν = 2 / 3 / 5, a single-pair disagreement as large as SH0ES against CMB-SPA (z = 6.27) has p₂ = 0.025 / 0.008 / 0.0015, not 3.6×10⁻¹⁰.
    - The base rate for "a ~6σ disagreement between two established precision methods" is therefore of order 1%. That rate is set by unrecognised systematics, not by chance.
    - This is the right reference class here, not 3σ particle bumps. Background knowledge, not sourced in this run: the proton-radius puzzle and past PDG world-average shifts were mostly resolved by measurement-side corrections.

    [calc: lens-statistician_robust_future.py]
13. **Robustness of the split under heavy tails.** I fitted a likelihood ratio with Student-t errors: local values centred on the early mean 67.58 against a free local mean.
    - All seven local classes: −2lnΛ = 18.2 (ν = 2) and 20.0 (ν = 3), **z ≈ 4.3–4.5**. With Gaussian errors it is 51.1 (7.2σ).
    - Without SH0ES: 3.3σ.
    - No-SN local: 3.1σ.
    - One-step only: 2.0σ.

    Heavy tails cut the all-local evidence from ~7σ to ~4.4σ, because they discount the single most precise point (SH0ES). They barely change the non-Cepheid evidence, which is spread over several weak, mutually consistent values. A pure fluctuation is excluded even under almost-Cauchy errors. What survives is a ~3σ, Cepheid-independent local excess of 3–5 km/s/Mpc. [calc: lens-statistician_robust_future.py]
14. **Is the SH0ES–CCHP split a sample-selection fluctuation?**
    - Assumed per-calibrator SN scatter 0.10–0.15 mag (not in the dossier).
    - For nested subsets, an 11-of-42 calibrator subset differs from the full set by σ = 0.84–1.31 km/s/Mpc. The ≈2.5 km/s/Mpc CCHP-JWST against full-HST difference [D-28] is then 1.9–3.0σ, consistent with Li 2026's "11 hosts ... 74.1, 2σ above the selected sample" [D-27].
    - For the 24-of-42 CCHP set the same 2.5 km/s/Mpc would be 3.7–5.6σ. There the difference cannot be subsample noise alone and must include method and SN-system effects: Hoyt's +2 km/s/Mpc Pantheon+ shift at 3.1σ [D-25].
    - Reading: the JWST-only CCHP values (67.8–68.8) look like a ~2σ low draw of a small subsample. The 24-host CCHP 70.4 contains a real (≈1.5–3σ) method or SN-photometry difference that is not yet attributed. [calc: lens-statistician_robust_future.py]
15. **Analysis-flexibility audit.**
    - **Blinding.** CCHP blinded zero points, but [new: Freedman et al. 2025, arXiv:2408.06153, full-text, "In practice, the blinding experiment was (completely) successful only for the JAGB analysis"]. SH0ES R22: a text search of arXiv:2112.04510 for "blind" returned only a passage on artificial-star tests [new: Riess et al. 2022, arXiv:2112.04510, full-text, "an important test of any photometry algorithm that can be completed blindly and in advance of an independent determination of H 0"]. I found no statement that the R22 H0 analysis itself was blinded, which matches the dossier gap [§6]. TDCOSMO-2026 [D-31] and H0DN (binding votes) [D-22] were fixed before the result.
    - **Variants.** The SH0ES and H0DN variants scatter by 0.40 km/s/Mpc [D-23]. The CCHP internal variants span 69.29–70.73 [D-24]. Both are small next to the 6.3 km/s/Mpc gap, but comparable to the 3.1 km/s/Mpc SH0ES–CCHP difference.
    - **Calibrator subsets.** Subset choice is the main flexibility (finding 14), and each team's preferred subset favours its own result.
16. **The signal fading as data accumulate: the one-step and alternative methods regressed toward ~71.** Superseded → current, km/s/Mpc:
    - Time delays: TDC4 74.5 → TDCOSMO-2025 71.6 → 71.1 [D-31].
    - Masers: 73.9 → 71.6 after peculiar-velocity correction [D-32].
    - Sirens: 75.4 → 71.7 [D-33].
    - SN standardisation (Wojtak & Hjorth): 70.5–71.5 on the SH0ES data [D-35].

    SH0ES moved the other way: 73.04 → 73.17 → 73.49 [D-20]. The CMB moved little: 67.36 (PR3) → 67.64 (PR4), with the CMB-SPA combination at 67.19. This is the winner's-curse pattern for early one-step reports (higher first values, error budgets that later grew, as with MSD [D-16]). The Cepheid-SN headline has not faded.
17. **Early-time new physics, scored without a SH0ES prior.**
    - ACT EDE Δχ² = 4.3 and 6.6 for 3 extra parameters [D-52] gives p = 0.23 and 0.086 (1.2σ and 1.7σ): no independent detection.
    - The best fits close 30–67% of the SH0ES–CMB-SPA gap: PMF 69.1 (30%), e-density 69.3 (33%), modified recombination 69.6 (38%), ACT EDE 69.9 (43%), Poulin EDE 71.0 (60%), eROSITA EDE 71.4 (67%).
    - Residual tension with SH0ES: 4.2σ, 4.0σ, 2.9σ, 2.9σ, 1.7σ and 1.2σ respectively [D-52, D-53, D-94, D-95].
    - The only ≥3σ no-ladder EDE preference is eROSITA (3.2σ) [D-94]. Since SPT+ACT+Planck gives f_EDE < 0.070 [D-53], the significance depends on the dataset.
    - The DESI w0wa preference of 2.8–4.2σ across three SN samples is 3.9σ after a look-elsewhere correction over the three samples. It moves H0 *down* [D-12, D-51], so it does not help close the gap. [calc: lens-statistician_robust_future.py]
18. **Local structure as a fluctuation.** The gap is 20.3σ (SH0ES against CMB-SPA), 16.7σ (local GLS against early) and 10.3σ (CCHP against CMB-SPA) in units of the ΛCDM cosmic variance σ(H0^loc) = 0.31 km/s/Mpc [D-10, D-37]. Even the smallest local value needs a ≥10σ structure. Under ΛCDM this is not a fluctuation, and it is separately excluded by the SN Hubble diagram [D-11]. [calc: lens-statistician_robust_future.py]
19. **What would settle it** (precision_needed; total 1σ on H0 from an independent, non-ladder method):
    - Ladder-systematic world (67.6) against a real local value (73.3): 1.91 km/s/Mpc (2.7%) for 3σ, **1.14 (1.6%) for 5σ**.
    - Early mean 67.6 against the best EDE-type value 71.0: 1.14 (1.6%) for 3σ, **0.68 (1.0%) for 5σ**.
    - 71.0 against 73.3: 0.77 (1.1%) for 3σ, 0.46 (0.7%) for 5σ.

    For time delays, with the stat/MSD split not published:
    - With the 11-lens error purely statistical: 17 lenses give 3σ and ~50 give 5σ between 67.6 and 73.3. Separating 67.6 from 71.0 at 3σ needs ~51.
    - With a 1% (0.71 km/s/Mpc) floor: 79 lenses for 5σ at 67.6 against 73.3, and 5σ at 67.6 against 71.0 is never reached.

    The review forecast of ~40 lenses for 1% [D-§6] corresponds roughly to the no-floor case. Bright sirens at ~15% each (assumed) need N ≈ 30 for 3σ and ≈ 84 for 5σ between 67.6 and 73.3.

    The SH0ES–CCHP difference is capped at z = 3.10/1.33 = 2.33 by CCHP's quoted systematic. More hosts alone can never reach 3σ; halving that systematic would allow 3σ with 4.6× the statistical data. That treats all of CCHP's 1.33 as non-cancelling; the shared NGC 4258 part would partly cancel. [calc: lens-statistician_robust_future.py]

## Lens-specific outputs

### A. Signal table (one row per claimed signal; km/s/Mpc; two-sided)

| # | Signal | Local z | Global z (look-elsewhere) | χ² within / between methods | Systematics | Min Bayes factor bound (max odds against null) | Prior needed for P = 0.5 | Verdict | Data needed |
|---|---|---|---|---|---|---|---|---|---|
| S1 | SH0ES 73.49 ± 0.93 against CMB-SPA 67.19 ± 0.38 [D-20, D-44] | 6.27 (Planck PR4: 5.49) | 5.90 / 5.72 / 5.51 (N = 10 / 30 / 100); single-pair heavy-tail p₂ = 0.008–0.025 (ν = 3–2) | n/a (pair) | SH0ES stat/sys split not in dossier; photometry bound −0.01 ± 0.03 mag [D-78] (SH0ES-only, not replicated); no blinding statement found for R22 | Sellke 5.6×10⁷ : 1; Gaussian-prior BF(two/one) 1.5–3.3×10⁷ (τ = 3–10) | 1.8×10⁻⁸ | **Robust** as a discrepancy between these two numbers; not a fluctuation | Non-Cepheid replication at ≤1.1 km/s/Mpc |
| S2 | H0DN 73.26 ± 0.81 against CMB-SPA / BAO+BBN [D-22] | 6.82 / 4.80 | BAO+BBN pair: 4.31 / 4.06 / 3.77 | — | Not independent of S1; corrected Pantheon+ shift −0.2 to −0.4 | not computed for H0DN (at least S1 for the CMB-SPA pair); SH0ES against BAO+BBN Gaussian-prior BF(two/one) 3–4×10³ | not computed (≪10⁻³ implied) | **Robust** (same caveat as S1) | As S1 |
| S3 | All local classes (7) against early (CMB-SPA + BAO+BBN) | 6.59 (between) | Heavy-tail LR: 4.3–4.5σ | within 6.50/7 (p = 0.48); between 43.4/1. Per-class: within 0.01/1, between 49.9/7 (5.66σ); pooled S = 2.50 | Shared NGC 4258 anchor (GLS: 6.4–6.9σ against CMB-SPA); shared Pantheon+ | not computed (heavy-tail LR −2lnΛ = 18–20 ⇒ likelihood ratio ≈ 10⁴) | not computed (≲10⁻⁴ implied) | **Robust** that local > early at ≳4σ even with heavy tails | — |
| S4 | Local without Cepheids or SNe (SBF, TF, TD, masers, sirens) against early | 3.32 (H0DN without Cepheids against CMB-SPA: 3.94) | H0DN without Cepheids: 3.35 / 3.03 / 2.64 (N = 10/30/100); heavy-tail LR 3.1 | within 4.32/5 | SBF and TF share NGC 4258/TRGB calibration; maser stat only | ≤413 : 1 (z = 3.9) | 2.4×10⁻³ | **Fragile** (3σ, partly shared calibration) | One-step H0 at ≤1.1–1.9 km/s/Mpc |
| S5 | One-step only (TD, masers, sirens) against early | 1.88 | heavy-tail 2.0 | within 0.02/2 | TD MSD-dominated [D-16]; maser stat only (preliminary) | ≤2.6 : 1 | 0.28 | **Noise / undetermined** | ~50 lenses, or ~84 bright sirens, for 5σ (finding 19) |
| S6 | SH0ES against CCHP TRGB 70.39 ± 1.94 [D-24] | 1.44 (ρ = 0) – 2.36 (ρ = 0.8) | — | — | CCHP sys 1.33 caps z at 2.33; subset variance 0.84–1.31 for 11-host sets | ≤1.4 : 1 | 0.42 | **Undetermined** (consistent with both) | CCHP sys ≤0.6 and common SN photometry; ≤0.62 on the difference for 5σ |
| S7 | CCHP against CMB-SPA / BAO+BBN | 1.62 / 0.94 | — | — | as S6 | ~1 (BF 0.7–1.4) | — | **Noise** (no tension) | as S6 |
| S8 | Early side internal: Planck/ACT/SPT; CMB against BAO+BBN | χ² 2.42/2; 2.20 | — | CMB within 2.42/2; between (CMB, BAO+BBN) 4.85/1 | ACT and SPT share the PR4 τ prior | — | — | **Consistent** (2.2σ, runs toward local) | DESI final, SO |
| S9 | M_B: R22 ladder against inverse ladder [D-21] | 3.76 (cosmography) / 4.42 (flat ΛCDM) | — | — | Different SN systems (Pantheon+ against DES-SN5YR) | — | — | **Robust in sign, size uncertain** | Same-SN-system M_B comparison |
| S10 | EDE preference without SH0ES (ACT; eROSITA) | 1.2 / 1.7 (Δχ² 4.3, 6.6 for 3 params); eROSITA 3.2 | — | — | Prior-volume effects; dataset choice (SPT+ACT+Planck f < 0.070) | ≤~3 : 1 (ACT) | ~0.3 | **Fragile / noise** | SO damping tail; independent LSS |
| S11 | DESI w0wa [D-51] | 2.8–4.2 | 3.94 (N = 3 SN samples) | — | SN-sample offset 0.04 mag [D-85] | — | — | **Fragile**; lowers H0, so irrelevant to closing the gap | DESI final + new SN samples |
| S12 | Local void (cosmic variance) [D-10] | needs 10–20σ in ΛCDM | — | — | — | — | — | **Eliminated** as ΛCDM fluctuation | — |

### B. Significance by choice of local result (against CMB-SPA 67.19 ± 0.38 / against BAO+BBN 68.50 ± 0.58)
SH0ES 6.27 / 4.55 · H0DN 6.82 / 4.80 · H0DN without Cepheids 3.94 / — · SH0ES-side JAGB 2.47 / 1.91 · SBF 2.72 / 2.14 · Wojtak–Hjorth alternative standardisation 2.81 / 1.62 · TDCOSMO 1.68 / 1.10 · CCHP 1.62 / 0.94 · masers 1.19 / 0.83 · sirens 0.60 / 0.43 · CCHP JWST JAGB 0.22 / 0.25. **The tension's significance is mainly set by the inclusion of the Cepheid-calibrated SN ladder (≥5σ with it, ≈3–4σ for the best non-Cepheid sets, <2σ for any single non-Cepheid method).** [calc: lens-statistician_tensions.py]

### C. Partition test (premise 2)
| Partition | within χ²/dof (p) | between z |
|---|---|---|
| early against late | 6.50/7 (0.48) | 6.59 |
| uses r_s against no r_s (+ sound-horizon-free BAO) | 11.95/8 (0.15) | 6.18 |
| SH0ES against everything else | 17.04/7 (0.017) | 5.73 |
| early / Cepheid-SN / other local | 5.01/6 (0.54) | 6.38 |
The early/late partition fits best. The "SH0ES against the rest" reframe leaves a 3.3σ local excess inside "the rest". The three-way split is as good as early/late, with other-local 71.69 ± 1.14 lying 1.2σ from SH0ES and 3.5σ from early.

### D. Shared-data notes
- SH0ES, CCHP, SBF and TF share NGC 4258 (GLS, finding 8).
- SH0ES and H0DN share Pantheon+, and H0DN contains SH0ES: never combined here.
- CMB-SPA contains Planck/ACT/SPT. I used CMB-SPA, or the three alone, never both.
- The inverse ladder uses the CMB r_d (ρ scan, finding 9).
- Wojtak–Hjorth, Li 2026 TRGB, the SH0ES-side JAGB and Dong 2026 re-use SH0ES/CCHP data. They are analysis variants, not independent measurements.

## Calculations
- `runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-statistician_tensions.py` (log beside it). Computes every local × early pairwise tension (two-sided, facing-side asymmetric errors), SH0ES–CCHP with ρ = 0–0.8, the M_B framing, Šidák look-elsewhere over pair choices, and the Sellke/Gaussian Bayes bounds with the prior needed. Key results: SH0ES–CMB-SPA 6.27σ; H0DN–CMB-SPA 6.82σ; SH0ES–BAO+BBN 4.55σ; CCHP–CMB-SPA 1.62σ; TDCOSMO–CMB-SPA 1.68σ; SH0ES–CCHP 1.44–2.36σ; M_B 0.122–0.141 mag (3.8–4.4σ).
- `runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-statistician_grouped.py`. Computes grouped χ² per class and for four partitions, a GLS local combination with the shared NGC 4258 anchor, the early combination with the inverse-ladder correlation, and BF(two/one) with Gaussian priors on the offset. Key results: early 67.58 ± 0.32; local 72.77 ± 0.72 (GLS 72.86–73.24); between 6.59σ; within 6.50/7.
- `runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-statistician_robust_future.py`. Computes Student-t tail probabilities and a heavy-tail likelihood ratio, calibrator-subsample variance, residual tension after early-time fits, the cosmic-variance multiple, precision_needed and exposure_to_reach. Key results: heavy-tail all-local 4.3–4.5σ and no-SN 3.1σ; EDE best fits close 30–67% of the gap; 5σ test needs 1.14 km/s/Mpc (67.6 against 73.3) or 0.68 (67.6 against 71.0).

## Candidate answers (at least 3; the null and a reframe count)
- [STATISTICIAN-A] **Distance-ladder systematic shared by the SN-calibrated ladders** (SN Ia calibrator–Hubble-flow standardisation, calibrator selection, peculiar velocities, or an NGC 4258/anchor-scale error common to Cepheid, TRGB and SBF ladders), worth ~0.15–0.19 mag. | status: **surviving** | Why: the ≥5σ evidence comes almost entirely from Cepheid-calibrated SNe (table B). The Cepheid-free one-step set is only 1.9σ above early (BF ≤ 2.6), so it cannot exclude a true H0 ≈ 67.6. Every known lever on the SN rung moves H0 down by 1–3 km/s/Mpc: Wojtak–Hjorth 70.6–71.5 (2.8σ remaining) [D-35]; Dong peculiar velocities −2.9 [D-82]; Percival selection −1.4, −0.2 and −1.0 [D-88]. Against: SBF (no SNe) sits at 73.8 ± 2.4, and the no-SN local set is 3.1–3.3σ above early, which a SN-only effect cannot move. | Test: one-step H0 at ≤1.1 km/s/Mpc (≈50 time-delay lenses without a floor, or ≈84 bright sirens) predicts 67.6 here, against 73 if the ladder is right. | confidence: medium
- [STATISTICIAN-B] **Cepheid-specific systematic** (photometry, metallicity or P–L zero point) in SH0ES only. | status: **strained** | Why: the "SH0ES against the rest" partition fits worse (within χ² 17.0/7, p = 0.017) than early/late (6.5/7). Removing Cepheids still leaves a 3.3–3.9σ local excess. The JWST photometry bound (−0.01 ± 0.03 mag, SH0ES-only) is ≈6× below the 0.18 mag needed [D-78]. | Test: an independent-team JWST Cepheid reanalysis; Cepheid–TRGB–JAGB agreement host by host on a common SN photometry. | confidence: medium
- [STATISTICIAN-C] **Early-time new physics** (EDE-like, r_s reduction). | status: **strained** | Why: there is no independent detection without SH0ES (ACT Δχ² gives 1.2–1.7σ with 3 parameters; eROSITA 3.2σ against SPT+ACT+Planck f < 0.070). The best all-data fits close only 30–67% of the gap, leaving 1.2–4.2σ to SH0ES (finding 17). It is consistent with the local mean 72.8 only at the upper end (71.0–71.4). | Test: a one-step measurement at ≤0.68 km/s/Mpc separating 71 from 67.6; SO damping-tail and polarisation bounds on f_EDE. | confidence: medium
- [STATISTICIAN-D] **Early-universe analysis systematic** (CMB likelihood or foregrounds, BAO). | status: **strained → near-eliminated as dominant** | Why: Planck, ACT and SPT agree (χ² 2.42/2). BAO+BBN uses no CMB anisotropies and is 4.55σ from SH0ES. It differs from the CMB by 2.2σ, but *toward* higher H0, which is only 21% of the gap ((68.50 − 67.19)/(73.49 − 67.19)). A common-mode error would have to shift independent instruments and BBN-calibrated BAO by the same ~6 km/s/Mpc. | Test: SPT-3G Ext-10k / SO against Planck; a BAO+BBN H0 with updated nuclear rates. | confidence: high
- [STATISTICIAN-E] **Late-time new physics in H(z)** (w0wa, phantom, interacting DE). | status: **eliminated** for H(z)-only variants; **strained** for M_B/G_eff transitions (not testable by my method) | Why: the inverse ladder 67.19–67.67 sits inside the early group (χ² changes by <0.3), and the DESI w0wa preference (3.9σ after LEE) moves H0 down to 63.6–67.5 [D-12, D-51]. | Test: the SN Hubble diagram at 0.01 < z < 0.1 for an M_B step; growth data. | confidence: high (H(z)-only)
- [STATISTICIAN-F] **Local structure (void or bulk flow).** | status: **eliminated** | Why: it needs a 10–20σ fluctuation of ΛCDM cosmic variance (σ = 0.31), and LTB voids of |δ| > 20% are excluded at 4–5σ [D-11]. Measured flow corrections are +0.6 to +1.4 or −0.5 to −2.9 km/s/Mpc (both signs) [D-36, D-82]. | Test: the PV-corrected Hubble flow from Rubin/ZTF. | confidence: high
- [STATISTICIAN-G] **Null: statistical fluctuation plus several modestly underestimated errors, none dominant.** | status: **eliminated as a pure fluctuation; strained as diffuse underestimated errors** | Why: Gaussian p₂ = 3.6×10⁻¹⁰ (Bayes bound 5.6×10⁷ : 1). Even under Bailey's almost-Cauchy tails the all-local excess is 4.3–4.5σ, and the Cepheid-free excess is 3.1σ, coherent in sign across 5 independent methods. For a diffuse explanation, several of the 1–3 km/s/Mpc levers (finding 17 and A) must add in the same direction, with no single one dominant. That is possible: they sum to roughly 3–6 km/s/Mpc if they add, which the papers do not establish. It is then hard to tell apart from A. | Test: whether successive corrections keep moving SH0ES down or stall. | confidence: medium
- [STATISTICIAN-H] **Reframe: the anomaly is "Cepheid-calibrated SN M_B against everything else", with the true local H0 ≈ 70–72 between the camps. "Early against late at 6σ" overstates a ~2–3σ problem for any non-Cepheid method.** | status: **surviving** | Why: the significance collapses from 6.3σ (SH0ES) to 3.3σ (no SN), 1.9σ (one-step only) and 1.6σ (CCHP). The non-Cepheid local mean 71.7 ± 1.1 is 1.2σ from SH0ES and 3.5σ from early, so the data cannot yet place it. Every one-step method has drifted down toward ~71 while SH0ES has not (finding 16). Against: the partition test still prefers early/late over SH0ES-against-rest. | Test: a 1% Cepheid-independent local H0 (TDCOSMO ~40–50 lenses; sirens in O5; JWST TRGB/JAGB on the full SH0ES calibrator set with common SN photometry). | confidence: medium

## What would change my mind
- A Cepheid-independent, non-SN H0 at ≤1.2 km/s/Mpc landing at ≥72.5 would make A and H strained and C (or an unnamed local-side new physics) favoured. One landing at ≤68.5 would make A near-decisive.
- An independent (non-SH0ES) reanalysis of the JWST Cepheid photometry that reproduces −0.01 ± 0.03 mag would further strain B. A CCHP analysis of the full 35–55 calibrator set on Pantheon+ photometry that returns ≈73 would fold the SH0ES–CCHP difference into calibrator selection.
- An early-side shift: SO or SPT Ext-10k finding f_EDE > 0 at ≥3σ without a ladder prior, or a revised BBN rate moving BAO+BBN up by ≥2 km/s/Mpc.
- A published SH0ES stat/sys split showing the 0.93 km/s/Mpc is sys-dominated would lower the robustness of S1 under a heavy-tailed reading.

## Assumptions I relied on
- Total errors are the stat, sys and σ_SN components added in quadrature, independent unless stated. Asymmetric errors take the facing side in `tension` and the mean of the sides in `grouped_chi2`/GLS.
- One current value per dataset: SH0ES 2025 Cepheid-SN (not R22 or Breuval); CCHP 2025 24-host TRGB as the CCHP headline (JWST-only and JAGB shown, not combined); TDCOSMO-2026; Stiskalek masers (stat only, preliminary); GWTC-5; Jensen SBF; Planck PR4; CMB-SPA as the CMB combination; DESI DR2 BAO+BBN. Several of these are preprints [D-31, D-32, D-33, D-45].
- NGC 4258 weights in the GLS (SH0ES 1/3, CCHP 1, SBF 1, TF 0.5) and anchor errors of 1.5–2.5% are my assumptions. The ACT/SPT shared τ prior is ignored.
- Per-calibrator SN scatter 0.10–0.15 mag, the TDCOSMO systematic floors of 0–1.5%, and ~15% per bright siren are assumed, not taken from the dossier.
- A Student-t with ν = 2–3 (Bailey 2017) is the reference error distribution for disagreements between established methods.
