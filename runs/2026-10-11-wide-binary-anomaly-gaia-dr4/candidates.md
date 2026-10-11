# Candidate answers
exclusive: yes (anomaly slate: each candidate names a different dominant cause of the DR3 low-acceleration γ excess and of the between-family split, and implies its own band for the true γ in the scoring bin. C2 and C3 are both modified-gravity truths but are kept apart, as the brief requires, because they are disjoint in true γ (≈1.3–1.45 vs ≈1.05–1.3) and differ in which method carries the discrepancy: null-side under-recovery vs family-1 inflation)
lenses merged: statistician, empiricist, mechanist, examiner, decomposer, dialectician, constraints (with the math checks math/statistician.md, empiricist.md, mechanist.md, examiner.md, decomposer.md, dialectician.md, constraints.md)
status: final

Conventions. γ = G_eff/G and ṽ are dimensionless. g_N is in SI (m s^-2), separations s in au or kau, masses in Msun, velocities in km/s, astrometry in mas or mas/yr. "F1–F4" are the brief's estimator families: F1 full-median, F2 tail-truncated, F3 mixture-likelihood, F4 Bayesian 3D. The "scoring bin" is the brief's bin, which contains g_N = 1e-10 m s^-2 and lies below 10^-9.5 m s^-2. MOND values are SPECULATIVE physics, labelled as such. `[calc: X]` means `runs/2026-10-11-wide-binary-anomaly-gaia-dr4/calc/X`, and `[M-...]` is a row in `runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/<lens>.md`. Generator outputs (the run's `wide_binary_population` and `wide_binary_estimators`) are model-dependent. No math check re-simulated their absolute values (M-MECHANIST-11, M-STATISTICIAN-12, M-DECOMPOSER-08 and M-CONSTRAINTS-19 are unverified); the checks verified only the arithmetic and analytic premises built on them.

## C1: Newton holds; the low-acceleration excess is an artefact of the Chae-lineage calibrate-at-high-acceleration pipelines, dominated by separation-dependent hidden-companion contamination that calibration does not remove.
type: explanation
from: MECHANIST-A, MECHANIST-G, STATISTICIAN-A, EMPIRICIST-A, EXAMINER-A, EXAMINER-F (as sub-hypothesis c), DECOMPOSER-A, DECOMPOSER-C (as sub-hypothesis a), DIALECTICIAN-A, CONSTRAINTS-C, CONSTRAINTS-B (as sub-hypothesis d)
argument:
- **Causal chain.**
  - The Chae-lineage analyses fix their nuisances on Newtonian-regime pairs and carry them to g_N ≲ 1e-10 m s^-2. These are F1 (Chae 2023, 2024a, 2024b; Yoon, Tian & Chae 2025) and F4 (Chae 2025; Chae et al. 2026). F1 fixes f_multi at ≈1e-8 m s^-2 [D-15]; F4's geometric deprojection passes a high-g check at 1.00 ± 0.05 [D-25].
  - A perturbation fixed in km/s grows in ṽ units as √s. For M = 1.5 Msun, 0.1 km/s is 0.12 v_c at 2 kau and 0.39 v_c at 20 kau [calc: lens-mechanist_scales.py; M-MECHANIST-01 verified]. So every kinematic contaminant has more leverage in the wide, low-g zone than in the calibration zone.
  - A location-only median cannot tell an additive contaminant from a rescaling [DIALECTICIAN F1; M-DIALECTICIAN-01 verified that a scalar boost leaves the quantile profile flat].
  - True γ ≈ 1.00 in the scoring bin. The robust families are approximately right: E2 1.045, E3 1.05, Banik+24 γ ≈ 0.99 [D-28, D-31]. E2's small residual above 1 is the in-window small-κ contamination expected under Newton [CONSTRAINTS F22; the numerical example there is unchecked].
- **Named sub-hypotheses for the dominant effect.** The lenses suspect (a) and (b) most.
  - **(a) f_multi(s) rises with separation.** The velocity-relevant hidden-companion fraction is higher at 5–30 kau than in the calibration zone.
    - Size needed for a full-median 1.37: Δf ≈ 0.31, or 0.26–0.39 for 1.3–1.5 [M-EXAMINER-12, correcting the lens's "0.2–0.3"].
    - The decomposer's extrapolations give 0.30–0.46 [M-DECOMPOSER-03]. The constraints lens's upper-bound contamination model gives Δf_eff ≈ 0.19 [CONSTRAINTS F8; M-CONSTRAINTS-06 verified].
    - The rate dγ/df is model-dependent, ≈1 in the lens generator and ≈1.8 in the checker's toy model [M-EXAMINER-13, unverified].
    - Only directional hints exist:
      - Dynamical stability lowers inner-binary fractions at small outer s [EXAMINER F8].
      - [new: Tokovinin & Smekhov 2002, ACCESS search-summary, SUMMARY "spectroscopic sub-systems are more frequent among components of wide visual binaries (~20%) and wide tertiaries (~30%) than among components of close visual binaries (11–18%)"].
      - Bashi, Clarke & Belokurov 2026 point the other way: a 2+2 enhancement that declines toward unity at ≥ 10 kau [new: Bashi, Clarke & Belokurov 2026, arXiv:2604.06317, ACCESS abstract, "the enhancement remains strong at separations ≤ 5 000 AU, but shows a decline towards unity at the widest separations (≥ 10 000 AU)"]. It concerns 2+2 correlation, not f_multi itself [EMPIRICIST F10].
  - **(b) The leverage of long-period inner binaries grows with s at fixed f.** These have a_in ≈ 5–300 au and P well beyond the baseline, so they pass RUWE.
    - The calibrated residual TEST/CAL is 1.075 / 1.128 at f_triple = 0.2 / 0.3 [calc: lens-decomposer_transfer.py] and 1.042–1.094 [calc: lens-dialectician_shape.py; M-DIALECTICIAN-05 arithmetic verified]. A crude log-normal-period model gives ≈ +0.10 at 10 kau and +0.12 at 20 kau [CONSTRAINTS F16; M-CONSTRAINTS-19 unverified].
    - Calibration on Newtonian-regime pairs cuts the triple-induced shift by only ≈40%, leaving +0.06–0.09 at 5–16.5% residual triples. The net "≤ +0.03 against truth" in the mechanist's grid comes from cancellation with an eccentricity-gradient offset [M-MECHANIST-08 refuted the lens's "calibration removes it"].
    - a_in = 5–300 au carries most of it: 1.177 vs 1.039 for 0.1–5 au at DR4 noise [calc: lens-decomposer_dr4split.py]. M-DECOMPOSER-07 verified the baseline-averaging physics, R = 3(sin x − x cos x)/x³.
  - **(c) Unbound, flyby or dissolving comoving pairs in the wide zone.**
    - The slope is ≈ +1.5 in calibrated γ per unit unbound fraction. +0.3 needs ≈15–16% because the median responds convexly, not the 20% first stated [M-MECHANIST-09]. With the corrected triple share it needs ≈12–15% [M-MECHANIST-08].
    - Pasquini et al.: 3 of 12 RV-clean pairs at s > 13 kau are not bound [D-38].
    - Chae et al. 2026's two above-escape systems drive its F4 result [D-26]. A bound-only likelihood can absorb such a system only through γ > 1 [M-DIALECTICIAN-02 verified].
  - **(d) Under-modelled astrometric noise in faint or distant pairs.**
    - σ_ṽ ∝ d σ_μ √(s/M). Against a noise-free template, σ_ṽ = 0.10 / 0.20 / 0.30 gives γ = 1.05 / 1.20 / 1.45. DR3 σ_ṽ is 0.28–0.39 at G = 17, 200 pc and 10–20 kau [CONSTRAINTS F10, F14; M-CONSTRAINTS-08 and -12 verified].
    - Cookson et al. say a ṽ-error cut removing 20% of pairs "completely eliminates" the rising trend [D-62].
    - Weakest point: nothing shows that Chae's templates under-model noise.
  - **(e) Uncorrected perspective at 15–30 kau and d ≲ 100 pc.** It adds +0.07 at (20 kau, 100 pc) and +0.23 at (30 kau, 100 pc) in a magnitude model [CONSTRAINTS F18; M-CONSTRAINTS-14 verified the arithmetic only]. But Boufourou's angular correction raised his deep bin, from 0.97 to 1.11 [D-31].
  - **(f) Chae's calibration and template implementation, unaudited.**
    - On (Boufourou's description of) the same catalogue the values are: Chae 1.368, Boufourou's implied full median 1.12–1.20, E2 1.045.
    - In ln γ, the pipeline step is 49–74% of the gap and the estimator-family step 26–51% [calc: lens-decomposer_budget.py; M-DECOMPOSER-02 and M-DIALECTICIAN-04 verified].
    - Boufourou: "We have not audited individual published pipelines" [D-50].
- **Family-4 component.**
  - On the same 36 pairs, geometric deprojection gives 1.56–1.60 and an independent semi-major-axis prior gives 1.00 [D-17, D-26].
  - Without the two above-escape systems, Chae et al.'s Γ converts to γ = 1.21 / 1.30 / 1.48 for g_N < 10^-9.1 / 10^-9.5 / 10^-10.1 m s^-2 [M-DIALECTICIAN-03 verified].
- **Weakest link.**
  - No source measures f_multi or the inner-period distribution as a function of separation [D-86; dossier §6].
  - With separation-independent multiplicity, a Newtonian-calibrated median in the run's generator returns 0.97–1.06, not 1.37 [STATISTICIAN F9–F10; M-STATISTICIAN-12 unverified]. So (a), (c), (d) or (f) must supply ≈ +0.2–0.3 that no measurement shows.
  - The dialectician's surrogate leaves Chae's low-f_multi samples near 1.04–1.06 against a published 1.37 [DIALECTICIAN F6; M-DIALECTICIAN-05]. Those samples are the 2024b "new" sample (f_multi 0.18) and the RUWE < 1.2 sample (0.10).

predictions:
- **DR3, per family (explained, not predicted).** F1 1.1–1.4 is an artefact (published 1.32–1.49 [D-20–D-23]). F2 and F3 are ≈1.00–1.05 (published 1.045, 1.05, 0.99 [D-28, D-31]). F4 is ≈1.0 with an independent-a prior and ≈1.5 with geometric deprojection [DECOMPOSER-A].
- **DR4, if true.**
  - F1 (Chae-type pipeline) 1.08–1.35, falling toward ≲ 1.10 as NSS-acceleration and RV vetoes are applied.
  - F2 1.00–1.07; F3 0.97–1.06.
  - F4 1.0–1.1 with an independent-a prior, 1.2–1.6 with geometric deprojection at N < 100.
  - Companion-veto-ladder intercept 0.97–1.03.
  - F1's low-g quantile profile rises (S > 1).
  - EF-alignment contrast 0.
  - DR4 or RV data flag at least one of the two escaper systems as hierarchical or unbound.
- **If false.** A companion-vetted DR4 low-g sample whose measured f_multi(s) is flat still returns γ ≥ 1.25.

evidence for:
- **Family structure.** Between-family χ² is 28.7/3 (4.7σ) while within-family χ² is 2.0/4 [STATISTICIAN F3; M-STATISTICIAN-03 verified].
- **Same catalogue, different answer.** Robust estimators give 1.045–1.05 against Chae's 1.37 [D-22, D-31].
- **Significance.** The F1 headline is 2.9–3.2σ (stat + sys) locally and 2.1–2.7σ after look-elsewhere [M-STATISTICIAN-01 and -02 verified].
- **Decline over time.** Chae-camp low-g values fall from 1.43 to 1.37 to 1.32 [STATISTICIAN failure modes].
- **Independent reproduction.** Boufourou's +0.08–0.13 uncalibrated full-median bias is reproduced as +0.10–0.15 [MECHANIST F4; arithmetic M-MECHANIST-07 verified; values M-MECHANIST-11 unverified].
- **Base rate.** 0 of 8 resolved precision-method disagreements ended as new physics: Laplace 0.10, Jeffreys 0.06 [EMPIRICIST F8; M-EMPIRICIST-07 verified]. Median time to resolution is ≈3 yr, not 4 [M-EMPIRICIST-08].
- **Family 4.** Saad & Ting nest Chae's family-4 number [D-17].
- **Cookson's flip.** It fits a Newton intercept on the veto ladder [DIALECTICIAN F10; ≈61 MOND-regime pairs, so suggestive only].

evidence against:
- The load-bearing premise, separation-dependent velocity-relevant multiplicity, is unmeasured [D-86].
- After calibration, every generator leaves a triple residual of only ≈ +0.04–0.13, short of +0.37 [DECOMPOSER F2, DIALECTICIAN F3, CONSTRAINTS F16].
- The Δf required (≈0.31) is larger than the examiner first stated [M-EXAMINER-12].
- Chae 2024b's own systematic budget is +0.16 −0.09 [D-22].
- The empiricist's camp separation is z ≈ 8, not 9.7 [M-EMPIRICIST-01]. Even that is an upper bound, because the data are shared [D-11].

decisive test:
- **Companion-veto ladder on a fixed DR4 pair list.** The rungs are RUWE → ipd → nss_acceleration_astro → epoch astrometry → RV variability, with γ extrapolated to zero residual companions. C1 predicts an intercept of ≈0.97–1.03; a chae2024-strength boost predicts ≈1.26 [DIALECTICIAN F4; M-DIALECTICIAN-06]. An intercept error of ≲ 0.05 separates the two at ≈5σ (the 0.25 separation divided by 5).
- **Supporting tests.**
  - A separation-resolved census of velocity-relevant companions: RV σ ≲ 20 m/s, split at 1 kau and ≥ 5 kau [DECOMPOSER load-bearing test].
  - An audit of Chae's unchanged pipeline on a Newtonian mock with long-period-rich triples; γ ≥ 1.25 there settles (f) [DECOMPOSER-A].
- **Who and when.** Any group with DR4 after 2 Dec 2026 12:00 CET [D-12]. Boufourou's pre-registered protocol covers only E2 and E3, not F1 [D-91].

## C2: A real full-strength MOND-like boost (true γ ≈ 1.3–1.45 in the scoring bin) exists, and the tail-truncated and mixture analyses under-recover it through their nuisance modelling and cuts.
type: explanation
from: MECHANIST-B, STATISTICIAN-B, EMPIRICIST-B, EXAMINER-B, DECOMPOSER-B, DIALECTICIAN-B, CONSTRAINTS-D
argument:
- **Physics (SPECULATIVE).** QUMOND or AQUAL with the Galactic EFE, at simple-ν or MLS strength.
  - γ_MOND(1e-10 m s^-2) is 1.416 for the exact QUMOND sphere average with simple ν, 1.375 for the generator's bz18_simple preset, 1.333 for Chae's eq. 22 and 1.363 for MLS.
  - The scoring-bin median-inferred value is 1.403 (simple). Over the 2–30 kau zone it is 1.276 [CONSTRAINTS F3, F21; M-CONSTRAINTS-03 and -17 verified].
- **What it says about the data.**
  - The Chae-lineage values are right: F1 1.32–1.49 [D-20–D-23]; F4 1.48 [D-25] and 1.60 [D-26].
  - The dominant cause of the discrepancy is a systematic in F2 and F3 that lowers v² by ≈25%.
- **Named suppression channels.**
  - (i) The mixture's free close-binary or triple component absorbs the boost: f_CB 0.63–0.70 [D-36]; the f_multi–γ degeneracy [D-86]; too large an f_multi lowers the inferred γ [D-61].
  - (ii) A freed eccentricity exponent: Banik+24 fit γ_e ≈ 1.94–2.12 against Hwang's 1.32 [D-42].
  - (iii) Null-side cuts (RUWE, ipd, σ_ṽ, d < 130 pc) remove boosted pairs, and f_multi is not recalibrated after cutting (Chae & Yoon) [D-39, D-61].
  - (iv) f_multi over-subtraction, if the hidden-companion tail thins at wide s [EMPIRICIST F10; Bashi et al. 2026, ACCESS abstract].
- **Weakest link.** No channel of the needed size is demonstrated.
  - Truncation at √2 removes ≈0.5–2% of MOND pairs and costs ≤ 0.01 in γ [CONSTRAINTS F7, DECOMPOSER F5, EXAMINER F7; M-CONSTRAINTS-06, M-DECOMPOSER-05 and M-EXAMINER-09 verified].
  - A freed f(e) at α = 2 absorbs only ≈7.5–11% [M-DECOMPOSER-04].
  - In both run injection grids every family, the mixture included, recovers injected γ = 1.2 and 1.4. The mixture returns 1.208–1.255 and 1.386–1.452, within ≈5% of truth [MECHANIST F7; STATISTICIAN F9; generator outputs unverified, M-MECHANIST-11 and M-STATISTICIAN-12].
  - The mass-deficit "rescaling" route proposed for the mixture is only ≈ +0.03 at f = 0.2 [M-DIALECTICIAN-08 refuted the lens's attribution].
  - Small-κ triples bias F1 and F2 upward, not downward [CONSTRAINTS F9; M-CONSTRAINTS-07 verified].

predictions:
- **DR3, per family.** All families would read ≈1.3–1.4 if modelled correctly. The published F2 and F3 values are then biased low by ≈0.3 [DECOMPOSER-B].
- **DR4, if true.**
  - F1 1.35–1.55.
  - F2 and F3 rise to ≥ 1.25 on companion-cleaned subsamples whose Newtonian validation zone sits at 1.00 ± 0.02.
  - F4 1.3–1.6 under either deprojection prior.
  - Veto-ladder intercept ≥ 1.2 (≈1.26 for chae2024 strength).
  - Flat quantile profile, S ≈ 1, at γ 1.25–1.4.
  - EF-alignment contrast ≈ +0.12.
  - Low-minus-high mass-tercile split at s = 2–6 kau of +0.03 to +0.05.
  - Precision-RV 3D samples at s > 5 kau with N ≳ 100 give γ ≳ 1.25.
  - A Banik-type fit with the eccentricity exponent fixed to 1.3 raises α_grav by ≳ 0.3 [EXAMINER-B].
- **If false.** Companion-cleaned F2 and F3 stay ≤ 1.07, and the EF contrast is null at σ ≈ 0.03.

evidence for:
- The pro-camp values are internally consistent: 1.415 ± 0.047 with χ² 1.20/5 [corrected in M-EMPIRICIST-01].
- Chae 2025 and Chae et al. 2026 fall inside the scoring bin at 1.48 and 1.60 [D-25, D-26].
- Cookson's own Fig. 12a prefers MOND 12× at d < 150 pc without the ipd cut [D-29].
- Boufourou's deep bin, 1.11 ± 0.07, is 1.6σ above Newton [M-STATISTICIAN-05].
- The sign of the f_multi transfer bias is unobserved [EMPIRICIST F10].
- F1 Chae 2024b is 4.1σ on statistical error alone [M-STATISTICIAN-01].

evidence against:
- Boufourou's deep bin is 3.7σ below 1.37 [M-STATISTICIAN-05].
- E2's 1.045 against the zone-averaged simple-ν 1.276 is 10.4σ statistical, or 3.8σ with the f(e) band [M-CONSTRAINTS-16 and -17].
- Boufourou's E3 fits f_trip = 0.15, not a large value [D-31].
- Saad & Ting reproduce 1.56 by changing only the prior [D-17]. Without its two escapers, Chae et al. 2026 drops to 1.8–1.9σ [M-STATISTICIAN-01].
- **Odds against a fluctuation.**
  - The largest odds against a fluctuation are 42:1 locally, or 6.4:1 with look-elsewhere or correlation [M-STATISTICIAN-06].
  - Chae 2025 gives 3.0:1, needing a prior of 0.25 [M-STATISTICIAN-13 corrected].
  - These bound fluctuation only, not a systematic.
- **Priors.** The base rate is ≈0.06–0.10 [M-EMPIRICIST-07]. Galaxy-scale MOND evidence enters only as a down-weighted prior, per the brief.

decisive test:
- **EF-alignment contrast** on DR4 deep-regime pairs whose external field lies in the sky plane. Compare γ for pairs with the projected separation within 30° of the projected Galactic EF against pairs beyond 60°.
- **Predicted values.** ≈ +0.12 under simple-ν MOND; 0 under Newton and every artefact considered. Significance is 2.65σ at N = 10,000 and 4.6σ at 30,000 deep-regime pairs [CONSTRAINTS F19; M-CONSTRAINTS-15 verified; the per-pair scalar η(θ) is an approximation of order the anisotropy].
- **Complementary test.** F2 and F3 on a DR4 RV- and NSS-cleaned subsample: ≥ 1.25 under C2 vs ≤ 1.07 [DECOMPOSER-B].
- **Who and when.** Any group with DR4 after 2 Dec 2026. The usable N is unknown until release [D-95].

## C3: A weak real boost from modified gravity with a weaker transition (standard or n = 1.5 interpolating function, or two-body QUMOND) gives true γ ≈ 1.05–1.3; neither camp is right.
type: explanation
from: MECHANIST-E, STATISTICIAN-C, EXAMINER-E, DECOMPOSER-D, CONSTRAINTS-E
argument:
- **Variants (SPECULATIVE physics).**
  - (i) Standard ν: 1.074 in the scoring bin and 1.048 over 2–30 kau. The zone value equals Boufourou's measured 1.045 [CONSTRAINTS F21; M-CONSTRAINTS-17 verified].
  - (ii) n = 1.5: 1.167 [CONSTRAINTS F1, F3; M-CONSTRAINTS-01 verified].
  - (iii) Full two-body QUMOND: 1.2–1.3 in the transition regime [D-45]. This rests on one abstract, and whether it includes the EFE is unclear.
- **How the DR3 data fit.**
  - The DR3 null exclusions exclude the simple-ν test-particle template, not MOND generically.
  - Boufourou's ΔlnL implies σ_stat 0.016–0.022 [CONSTRAINTS F20; M-CONSTRAINTS-16 verified]. On that basis, as statistical / with-systematics tensions:
    - standard ν: 1.1σ / 0.4σ;
    - n = 1.5: 5.4σ / 2.0σ;
    - two-body 1.20: 6.9σ / 2.5σ;
    - two-body 1.30: 11.5σ / 4.2σ.
  - The null side is roughly right in level, and the robust deep bins carry the real signal. F1's 1.37 is additionally inflated by the C1 mechanisms; that inflation is secondary here, not the dominant cause of γ > 1.
- **Supporting values.**
  - The low-g-only measurements pool to 1.248 ± 0.050. At group level S = 2.06 and p = 0.014, so "compatible" is the soft reading [M-STATISTICIAN-03].
  - Boufourou's deep bin is 1.11 ± 0.07 [D-31].
  - C3PO at s > 3 kau gives 1.17 +0.37 −0.23 [D-27].
  - Chae et al. 2026 without the escapers gives 1.21–1.48 [M-DIALECTICIAN-03].
- **Size of the MOND span.** The examiner's "factor ~1.3 in (γ − 1)" is corrected: the span is a factor ≈1.3 in γ (1.06–1.42) and ≈6 in (γ − 1) [M-EXAMINER-11].
- **Weakest link.**
  - No analysis independently prefers a value in the 1.05–1.3 band.
  - The band is exactly where residual contamination also lands (C1, C6). Without an orientation or g_N-shape signature, C3 cannot be separated from them.
  - Galaxy rotation curves prefer a simple-like ν. That is a prior from outside this test, labelled and down-weighted per the brief [CONSTRAINTS-E].

predictions:
- **DR3.** F2 and F3 deep bins ≈1.05–1.11 are the real signal; F1 is inflated.
- **DR4, if true.**
  - F1 1.15–1.35.
  - F2 1.06–1.30 and F3 1.04–1.30. The low end is the standard-ν variant [CONSTRAINTS-E]; the high end is γ_inj = 1.2 in the mechanist's grid [MECHANIST matrix E]. Deep bins read 1.08–1.20 (σ ≈ 0.02–0.03) while the 2–30 kau global stays ≤ 1.05 under standard ν [DECOMPOSER-D].
  - F4 1.0–1.5.
  - γ(g_N) rises monotonically along the named template from 10^-9 to 10^-10.5 m s^-2.
  - The scoring bin sits above the 2–30 kau zone value (standard ν: 1.074 vs 1.048).
  - EF-alignment contrast ≈ +0.06. This is scaled from the simple-ν value and was not computed directly.
  - Veto-ladder intercept at the bin truth, 1.05–1.3. This is inferred from the dialectician's ladder logic and computed only for chae2024 strength.
- **If false.** Robust deep bins sit at 1.00 ± 0.03 with no g_N trend.

evidence for:
- The supporting values above.
- No kinematic bound in the constraints lens excludes it [CONSTRAINTS Lens-specific 2].

evidence against:
- Global E2 and E3 values of 1.045–1.05 with tight intervals disfavour > 1.07 [D-31].
- Two-body 1.2–1.3 is excluded at 2–4σ with the f(e) band [M-CONSTRAINTS-16].
- Separating 1.07 from 1.00 needs σ_total ≲ 0.02, while current systematics are ±0.03–0.05 [CONSTRAINTS-E].
- The base rate is ≈0.06–0.10 [M-EMPIRICIST-07].

decisive test:
- **Bin-resolved γ(g_N) in F2 and F3 on DR4.** The deep bin (g_N/a0 ∈ [0.03, 0.3]) reads ≥ 1.08 with σ ≤ 0.03 while the 2–30 kau global stays ≤ 1.05: a trend with g_N, not an offset [DECOMPOSER-D].
- **EF-alignment contrast** at ≈ +0.06 [CONSTRAINTS-E].
- **Statistics needed.** N ≳ 20,000 pairs in the bin [CONSTRAINTS-E], from σ_γ ≈ 1.42 γ/√N for a median [M-CONSTRAINTS-11, which corrected the coefficient from 1.39].

## C4: Differences in samples and quality cuts, not estimators, dominate the γ spread; the same estimator on matched samples would return matching γ.
type: explanation
from: MECHANIST-C, STATISTICIAN-D, EMPIRICIST-E, EXAMINER-D, DECOMPOSER-F, DIALECTICIAN-E
argument:
- **Named sub-hypotheses.**
  - **(a) Cuts change the residual hidden-companion content.**
    - A RUWE cut moves Chae's self-calibrated f_multi from 0.43 to 0.10 [D-35].
    - Dropping the ipd_frac_multi_peak cut flips Cookson's d < 150 pc result from Newton preferred 88× to MOND preferred 12× [D-29]. Across d < 130 pc with the ipd cut (Newton 1501×) and d < 150 pc without it (MOND 12×), the swing is 4.26 dex [M-EMPIRICIST-04].
  - **(b) Distance and magnitude limits set the noise level.** This is C1(d) acting through selection [CONSTRAINTS-B].
  - **(c) Separation windows set which MOND value applies.** For simple ν, 2–30 kau gives 1.276 and ≳ 5–30 kau gives 1.402 [M-CONSTRAINTS-17].
- **Size in the run's generator.** Cuts change the residual triple fraction by 2× and shift γ by 0.05 for a calibrated estimator, or 0.10–0.19 for an uncalibrated one [MECHANIST F8].
- **What it implies.** The true γ is whatever the best-vetted sample gives.
- **Weakest link.**
  - On (Boufourou's description of) Chae's own catalogue the robust estimators give 1.045–1.05 [D-31]. The 36-pair F4 swing (1.00 vs 1.56) involves no change of sample at all [D-17].
  - Whether Boufourou's 81,088 pairs are Chae's catalogue is itself open [DECOMPOSER Q1c].
  - A velocity-blind companion veto lowers γ with the same slope in Newton and MOND worlds (≈0.60–0.75 per unit triple fraction). Cuts reshuffle residual triples; they cannot turn 1.0 into 1.4 [DIALECTICIAN F4; M-DIALECTICIAN-06].

predictions:
- **DR3.** Each published value is the γ of its sample. Chae's high-f_multi samples read 1.33–1.43 [D-20]; cleaner, nearer samples read ≈1.0 [D-29].
- **DR4, if true.**
  - When both camps' pipelines run on one frozen sample, the spread falls below ≈0.1.
  - In a swap test γ follows the sample.
  - Per family: F1 1.05–1.40 depending on the sample; F2 1.00–1.10; F3 0.98–1.08; F4 0.9–1.6.
  - The veto-ladder intercepts of the two camps' samples differ.
- **If false.** On a shared sample the families still differ by ≳ 0.2.

evidence for:
- Cut and sample sensitivities [D-29, D-35, D-53].
- Boufourou kept 41,760 of 81,088 pairs (51.5%) [M-EMPIRICIST-04].
- The pipeline-plus-cuts step is 49–74% of the same-catalogue ln-gap [M-DECOMPOSER-02].

evidence against:
- The weakest-link points above.
- In linear γ the estimator alone accounts for 23–48% of the same-catalogue gap [M-EMPIRICIST-04].

decisive test:
- **Swap test.** Run each camp's unchanged pipeline on the other's DR4 sample and on one shared frozen sample.
- **Cut-toggle table.** Report γ per toggle of RUWE, ipd, σ_ṽ, R_chance and the NSS flag [MECHANIST-C; DECOMPOSER-F].
- **Precision.** DR4 σ_stat per family is 0.014–0.053 [STATISTICIAN Table 2; M-STATISTICIAN-08 verified], enough to resolve differences of 0.1.
- **Feasibility.** It needs the camps to cooperate, and none has declared such a plan [D-18, D-92].

## C5: A stellar-input systematic, photometric mass scale or eccentricity distribution, differing between acceleration bins or between analyses, dominates the discrepancy.
type: explanation
from: MECHANIST-D, STATISTICIAN-E, EMPIRICIST-F, DECOMPOSER-E, CONSTRAINTS-F
argument:
- **The brief's "common to all families" form is excluded by logic.** A shift common to all families cannot produce a split between them [CONSTRAINTS K14]. A common-mode mass bias also cancels in every calibrated or free-normalised test [DECOMPOSER F1; M-DECOMPOSER-01 verified].
- **Surviving variants.**
  - **(i) Bin-dependent mass bias.**
    - At a given s, low-g bins are low-mass bins [EXAMINER F10].
    - To fake 1.37 in a calibrated estimator, M_est/M_true must be ≈27% lower in the low-g bin than in the calibration bin [M-DECOMPOSER-01, M-EXAMINER-04; 23–27% per M-MECHANIST-05].
    - Such a bias passes one-for-one through every family [MECHANIST F8]. To explain the split it would also have to be absent from the null samples.
  - **(ii) Mass-scale error in un-normalised template comparisons.**
    - A uniform bias moves template families one-for-one (a 10% underestimate gives ×1.111) but cancels in calibrated ones, so it separates the families [MECHANIST-D; M-MECHANIST-05 verified].
    - The example is Hernandez & Kroupa's 2.0 vs 1.56 Msun normalisation in Cookson (2024), a factor of 1.282 [D-33, D-65]. That re-analysis concerns an earlier paper, not Cookson et al. 2026 [D-33].
  - **(iii) Eccentricity template.**
    - At Hwang's α the effect is ±0.03.
    - A uniform truth gives only 1.30–1.32 against an α = 1.2–1.3 template, so 1.37 needs α ≈ −0.15 to −0.2 [M-CONSTRAINTS-09]. That check refuted the lens's "α ≈ 0" and strengthens the elimination.
    - The calibrated eccentricity gradient is ±5–8% [DECOMPOSER F4].
    - Banik's α ≈ 2 lowers a Hwang-template median to 0.906–0.925 [M-CONSTRAINTS-09; M-DECOMPOSER-04].
- **Corrections to lens numbers.**
  - The statistician's figures for this candidate (+0.18 from the template; +0.28 and +0.15 from mass) are totals, not increments. The increments are ≈ +0.03–0.07 for the template, and ×1.111 (+0.11–0.13 median, +0.11 mixture) for a 10% mass underestimate [M-STATISTICIAN-15].
  - The light-based mass deficit from hidden companions belongs to C1, not here: ≈ +0.03 at f = 0.2 and separation-independent [M-DIALECTICIAN-08].

predictions:
- **If true.**
  - γ depends on M_tot at fixed g_N, M dwarfs vs FGK [EXAMINER hardest question 7].
  - Variant (i): DR4 dynamical masses (NSS orbits) and photometric masses differ by ≥ 20% at ≥ 5 kau but not at 1 kau [DECOMPOSER-E].
  - Variant (ii): the null-side γ rises by ≈1/b once masses are re-normalised, where b = M_est/M_true.
  - In the common-mode form, all families shift together from DR3 to DR4 [CONSTRAINTS-F].
  - EF-alignment contrast 0.
  - DR4 per family: F1 1.0–1.1 when calibrated, with template families shifted by the 1/b bias; F2 and F3 1.05–1.15; F4 1.0–1.3 [MECHANIST matrix D].
- **If false.** Masses agree bin by bin within ≈10%, and γ does not depend on M at fixed g_N.

evidence for:
- Hernandez & Kroupa's mass-normalisation finding [D-33].
- Chae & Yoon say Cookson et al. 2026 has "incorrect masses for a large portion of the stars" [D-65].
- No per-bin mass-bias numbers exist in the dossier, so the variant is not excluded by data [dossier §6].

evidence against:
- Boufourou's Newtonian validation zone passes at +1.4% [D-61, D-91].
- Cookson leaves the Newtonian normalisation free [D-29].
- No source measures a ≈27% bin-dependent bias.
- Eccentricity would need a departure from Hwang+22 larger than the 6–9σ the constraints lens stated [CONSTRAINTS F11; M-CONSTRAINTS-09].

decisive test:
- **γ as a function of M_tot at fixed g_N**, together with bin-by-bin dynamical masses (DR4 NSS orbits) against photometric and FLAME masses. Mass ratios are needed to ≲ 10% per bin [DECOMPOSER-E; EXAMINER F10].

## C6: No single dominant cause: several comparable separation-dependent effects (residual companions, noise, perspective, templates) plus analysis flexibility, each smaller than the gap, together produce the excess.
type: null
from: STATISTICIAN-NULL, CONSTRAINTS-A, EMPIRICIST-D, DIALECTICIAN-C
argument:
- **Components, each below the ≈ +0.3–0.4 gap.**
  - Uncalibrated or partly calibrated triple bias: +0.06–0.15 [MECHANIST F4; M-MECHANIST-08].
  - Separation-dependent triple leverage after calibration: ≈ +0.04–0.13 [DECOMPOSER F2, DIALECTICIAN F3, CONSTRAINTS F16].
  - Noise: +0.05–0.2 in faint or distant subsamples [CONSTRAINTS F14].
  - Perspective: ≤ +0.07 at d ≥ 100 pc and s ≤ 20 kau [CONSTRAINTS F18].
  - Eccentricity template: ±0.03 [CONSTRAINTS F11].
  - Light-based mass deficit: ≈ +0.01–0.05 uncalibrated, ≈0 calibrated [M-DIALECTICIAN-08].
  - Analysis flexibility: no blinding [D-18]; samples × bins × variants, with look-elsewhere factors over 5–30 trials [STATISTICIAN F2].
  - Two escaper systems in F4 [D-26].
- **Statistical status.**
  - The F1 headline is 2.9–3.2σ (stat + sys) locally and 2.1–2.7σ globally. F1 combined is 2.5–3.0σ for ρ = 0.5–0.8 [M-STATISTICIAN-01, -02, -04].
  - The same-data F1−F2 gap is 3.3–4.1σ on statistical errors, but 2.05–2.31σ with Chae's stat + sys [M-STATISTICIAN-04 note].
  - Chae 2025's odds bound is 3.0:1 (prior needed 0.25) [M-STATISTICIAN-13].
  - A pure fluctuation is eliminated for the between-family split (4.7σ) but only strained for the F1 level.
- **The robust families' residual.**
  - Their 1.045 is the expected small-κ in-window contamination of ≈ +0.04–0.05 [CONSTRAINTS F22; that example is unchecked].
  - DIALECTICIAN-C's common-mode +0.03 to +0.08 survives only marginally after M-DIALECTICIAN-08.
  - EMPIRICIST-D's "intermediate residual from a shared systematic" is this candidate. Its weakest link is that no single systematic of the right size is identified.

predictions:
- **DR4, if true.**
  - F1 regresses toward 1.1–1.25 while F3 stays ≈1.02 [STATISTICIAN-NULL].
  - Per family: F1 1.08–1.25; F2 1.00–1.07; F3 0.97–1.06; F4 0.9–1.3 [CONSTRAINTS-A].
  - Each orthogonal diagnostic removes part of the F1 excess and none removes most:
    - F1 falls with a brighter G cut, and its noise share shrinks ≈5.7× from DR3 to DR4 [(1/0.42)², M-CONSTRAINTS-12];
    - removing acceleration-flagged pairs lowers it;
    - the perspective share is confined to 15–30 kau and d ≲ 100 pc;
    - the EF-alignment contrast is 0.
- **If false.** A single diagnostic removes most of the F1 excess (→ C1, C4 or C5), or the excess survives all of them (→ C2 or C3).

evidence for:
- The statistical status above.
- The Chae-camp values decline over time (winner's curse) [STATISTICIAN failure modes].
- Every component stays inside its budget (K3–K6, K11) [CONSTRAINTS-A].

evidence against:
- The between-family split is 4.7σ on statistical errors [M-STATISTICIAN-03].
- The computed components come from different models. Nobody has shown that their sum reaches +0.37 in one consistent model.

decisive test:
- **Decompose the DR4 F1 excess on one sample** by orthogonal splits:
  - magnitude and distance (noise);
  - the veto ladder (companions);
  - separation and distance (perspective);
  - mass at fixed g_N (stellar inputs).
- C6 predicts that no single split removes most of the excess. This applies the tests named by STATISTICIAN-NULL and CONSTRAINTS-A.
- **Who and when.** Any DR4 group; the splits need the DR4 σ_stat per family of 0.014–0.053 [M-STATISTICIAN-08].

## C7: Reframe: "γ in a bin" is a property of data times nuisance model, not of DR3 projected velocities alone, and the MOND target is template-relative; only differential, externally calibrated observables are well-posed.
type: reframe
from: EMPIRICIST-C, EXAMINER-C, STATISTICIAN-F, DIALECTICIAN-D, DECOMPOSER-G, CONSTRAINTS-G, MECHANIST-F (restated per M-MECHANIST-08), DIALECTICIAN-F (eliminated by its own lens; noted)
argument:
- **Doubtful premises.** Several of the brief's premises fail [EXAMINER table B]:
  - P9, that statistics decide it;
  - P10, that MOND predicts ~1.4;
  - P11, that DR4 settles it;
  - the implicit premise that "γ in a bin" is well-posed.
- **Data side.**
  - γ_app ≈ γ_true × (M_true/M_est) × E(f(e)) × T(f_multi, inner periods) × N(noise), and each factor is of the order of the anomaly [EXAMINER F3; mass and eccentricity factors M-EXAMINER-04 and -05 verified].
  - Within one family, analyses using different triple models differ by 0.17–0.25 [D-22, D-31].
  - On the same 36 pairs the prior alone moves γ by ln 0.445, more than the whole F1 anomaly, ln 1.368 = 0.313 [M-DECOMPOSER-02].
  - The families report different functionals of one ṽ distribution [DIALECTICIAN F1]. The median reads scale (gravity, mass) and is shifted by contaminants too; the truncated and mixture estimators also read shape (triples give S > 1, f(e) gives S < 1). M-DIALECTICIAN-01 verified that a scalar boost gives S = 1; M-DIALECTICIAN-07 verified the directions, not the magnitudes.
  - MECHANIST-F, restated: the nuisance model and the calibration status matter more than the family label, but calibration cuts the triple sensitivity by ≈40% rather than removing it [M-MECHANIST-08].
- **Theory side (SPECULATIVE physics).**
  - The MOND target in the bin spans 1.06–1.42 in γ, a factor ≈6 in (γ − 1) [M-EXAMINER-01, -11].
  - The EF anisotropy runs from 1.354 to 1.560 [M-EXAMINER-02].
  - The scalar-γ approximation understates the MOND ṽ ceiling by 4.7%. This is proven only in the EF-dominated domain [M-CONSTRAINTS-02].
- **Forecast side.**
  - Per-family DR4 values stay anchored on the DR3 camp values.
  - The likelihood ratios MOND/Newton at the conditional medians are 0.50–1.84 (F1), 0.40–2.66 (F2), 0.14–29 (F3) and 0.94–1.11 (F4) [M-STATISTICIAN-09 verified].
  - σ_stat is below every family's systematic. σ_γ = 0.005 needs ≈80,700 pairs in the bin [M-CONSTRAINTS-11].
- **Well-posed replacement.**
  - Measure the differential γ_app(low g)/γ_app(control) on one pair list. Fix f_multi(s), masses and f(e) from non-velocity data (NSS, RV, resolved companions).
  - Report the result as a vector: (scale, S), zone-resolved γ(g_N), the EF-alignment contrast and the veto-ladder intercept.
- **DIALECTICIAN-F.** Its claim ("each family is right in its own regime and DR4 will not decide") was eliminated by its own lens, because those observables are decidable with DR4. It is kept only as the "DR3-only" reading of this reframe.

predictions:
- **If true.**
  - The first DR4 papers reproduce their camp's DR3 values within ≈0.1 [EMPIRICIST-C]. Chae-lineage F1 reads 1.3–1.45; the Banik, Cookson and Boufourou lineage reads 1.00–1.06 in F2 and F3.
  - The first three qualifying papers differ by > 0.2 [STATISTICIAN-F].
  - The two F4 parametrisations keep differing by ≈0.4–0.6 at N ≲ 100 [DIALECTICIAN C2; M-DIALECTICIAN-11 unverified].
  - Analyses that measure f(s) externally converge (spread < 0.05), while those that fit f_multi keep the split [EXAMINER-C].
- **If false.** All families converge within 0.1 on DR4 without any external f(s).

evidence for:
- The argument above.
- The camps are internally consistent and ≈8σ apart under independence, corrected from 9.7σ [M-EMPIRICIST-01].
- Pairwise tensions including systematics are only 2.2–2.9σ [M-EMPIRICIST-03 verified].

evidence against:
- As an explanation of the DR3 split the reframe is strained: the anisotropy averages to ≈0.015 over a sky-wide sample [CONSTRAINTS F19].
- DR4 vetting and shape statistics can make the question decidable, so "indeterminate" may hold for DR3 only [DIALECTICIAN-F reasoning].
- "DR3 cannot fix γ better than ±0.3" is an inference from the lens, not a derived result [math/empiricist.md, Unverified].

decisive test:
- **Do the first three qualifying DR4 papers differ by > 0.2 in the scoring bin?** These are the papers posted between 2 Dec 2026 and 30 Jun 2027 under the brief's scoring rule.
- **Does any analysis that fixes f_multi(s) from NSS or RV data converge with the others?** [STATISTICIAN-F; EXAMINER-C]
- **When.** The scoring date is 2027-06-30.

## Prediction matrix

Columns are independent classes of measurement:
- **F1–F4:** γ each family reports in the DR4 scoring bin.
- **Veto-ladder intercept:** γ extrapolated to zero residual companions on a fixed DR4 pair list.
- **Δf_multi census:** RV and NSS census of velocity-relevant companions, ≥ 5 kau minus ~1 kau.
- **EF-alignment contrast:** DR4 deep regime.
- **Magnitude / noise split:** F1 against the G limit, and its change from DR3 to DR4.
- **Mass split:** γ against M_tot at fixed g_N or s.
- **Precision-RV 3D samples:** s > 5 kau.

The statistician's Table 3 conditionals (median [68% interval]) are given where they apply: Newton for C1, MOND for C2. Its MOND row assumes that the F2/F3 suppression persists, recovering U(0.15, 0.8) of the boost.

| Candidate | F1 full-median (DR4) | F2 tail-truncated (DR4) | F3 mixture (DR4) | F4 Bayesian 3D (DR4) | Veto-ladder intercept | Δf_multi census | EF-alignment contrast | Magnitude / noise split | Mass split | Precision-RV 3D samples |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 | 1.08–1.35; Newton conditional 1.231 [1.137, 1.325]; 1.03–1.10 after NSS vetoes [STATISTICIAN Table 3; MECHANIST matrix A; DIALECTICIAN matrix A] | 1.00–1.07; 1.060 [1.009, 1.111] [STATISTICIAN Table 3; CONSTRAINTS-A] | 0.97–1.06; 1.020 [0.975, 1.065] [STATISTICIAN Table 3; MECHANIST matrix A] | 1.0–1.1 (independent-a prior), 1.2–1.6 (geometric, N < 100); 1.223 [0.934, 1.522] [DIALECTICIAN matrix A; STATISTICIAN Table 3] | 0.97–1.03 [M-DIALECTICIAN-06] | ≈ +0.31 (0.26–0.39) under (a) [M-EXAMINER-12]; may be flat under (b)–(f) | 0 [CONSTRAINTS F19] | (d): F1 falls with a brighter G cut, noise bias ÷≈5.7 on DR4 [CONSTRAINTS F14; M-CONSTRAINTS-12]; (a)/(b): insensitive [CONSTRAINTS-C] | Newton: low-minus-high tercile −0.015 to −0.029 at f = 0.2 [DIALECTICIAN F9; power unverified, M-DIALECTICIAN-13] | γ < 1.1 with σ < 0.08 at N ≳ 200 [EMPIRICIST mind-change]; ≥ 1 escaper flagged [DIALECTICIAN C2] |
| C2 | 1.35–1.55; MOND conditional 1.346 [1.243, 1.450] [STATISTICIAN Table 3; DIALECTICIAN matrix B; CONSTRAINTS-D] | ≥ 1.25 once cleaned (1.25–1.42) [DIALECTICIAN matrix B; CONSTRAINTS-D]; 1.149 [1.072, 1.233] if suppression persists [STATISTICIAN Table 3] | 1.28–1.40 once cleaned [CONSTRAINTS-D]; 1.149 [1.073, 1.231] if suppression persists [STATISTICIAN Table 3] | 1.3–1.6 under either prior; 1.344 [1.044, 1.627] [DIALECTICIAN matrix B; STATISTICIAN Table 3] | ≈1.26–1.27 for chae2024 strength; ≥ 1.2 [DIALECTICIAN F4; M-DIALECTICIAN-06] | flat within ±0.05 [EXAMINER hardest question 1] | ≈ +0.12 (simple ν) [M-CONSTRAINTS-15] | independent of the G cut [CONSTRAINTS-D] | +0.03 to +0.05 at s = 2–6 kau (weak) [DIALECTICIAN F9] | γ ≳ 1.25–1.3 at N ≳ 100 [EXAMINER-B; EMPIRICIST mind-change] |
| C3 | 1.15–1.35 [CONSTRAINTS-E; DECOMPOSER-D] | 1.06–1.30; deep bin 1.08–1.20 with σ ≈ 0.02–0.03 while the 2–30 kau global stays ≤ 1.05 (standard ν) [CONSTRAINTS-E; DECOMPOSER-D; MECHANIST matrix E] | 1.04–1.30 [CONSTRAINTS-E; MECHANIST matrix E] | 1.0–1.5 [CONSTRAINTS-E; MECHANIST matrix E] | at the bin truth, 1.05–1.3 (inferred from DIALECTICIAN F4; not computed for standard ν) | not computed | ≈ +0.06, scaled from simple ν, not computed directly [CONSTRAINTS-E] | independent of the G cut [CONSTRAINTS Lens-specific 4, item 3] | not computed for standard ν; ≈ +0.03–0.05 at chae2024 strength [DIALECTICIAN F9] | consistent with C3PO's 1.17 +0.37 −0.23 [D-27]; DR4-era value not computed |
| C4 | 1.05–1.40, set by the sample [MECHANIST matrix C; DIALECTICIAN matrix E] | 1.00–1.10 [MECHANIST matrix C] | 0.98–1.08 [MECHANIST matrix C] | 0.9–1.6 [MECHANIST matrix C] | the two camps' samples give different intercepts [DIALECTICIAN-E] | not computed | not computed (set by the true γ of the best sample) | (b): F1 rises with the faint limit and with d [CONSTRAINTS-B] | not computed | not computed |
| C5 | 1.0–1.1 calibrated; template families shifted by the 1/b mass bias [MECHANIST matrix D] | 1.05–1.15 [MECHANIST matrix D]; 1.02–1.08 (common-mode) [DIALECTICIAN matrix C] | 1.05–1.15 [MECHANIST matrix D]; 1.02–1.07 [DIALECTICIAN matrix C] | 1.0–1.3 [MECHANIST matrix D] | not computed | not computed | 0 (mass errors are isotropic) [CONSTRAINTS F19] | not computed | γ varies with M_tot at fixed g_N; a 10% bin-only bias gives 1.11 or 0.91 [EXAMINER F10; M-EXAMINER-04] | not computed |
| C6 | 1.08–1.25, regressing toward 1.1–1.2 [CONSTRAINTS-A; STATISTICIAN-NULL] | 1.00–1.07 [CONSTRAINTS-A] | 0.97–1.06, ≈1.02 [CONSTRAINTS-A; STATISTICIAN-NULL] | 0.9–1.3 [CONSTRAINTS-A] | partial fall toward the 0.97–1.03 Newton band; size not computed | a modest rise: +0.1 in f would give +0.06–0.1 in γ [STATISTICIAN "What would settle it"] | 0 [CONSTRAINTS-A] | partial fall with a brighter G cut; noise share ÷≈5.7 DR3→DR4 [CONSTRAINTS-A; M-CONSTRAINTS-12] | not computed | not computed |
| C7 | Chae lineage 1.3–1.45 [EMPIRICIST-C] | Boufourou/Cookson lineage 1.00–1.06 [EMPIRICIST-C] | Banik lineage 1.00–1.06 [EMPIRICIST-C] | the two parametrisations still differ by ≈0.4–0.6 at N ≲ 100 [DIALECTICIAN C2; M-DIALECTICIAN-11 unverified] | the decisive datum; value set by the physics (C1 or C2 bands) | families converge only where Δf is measured externally (spread < 0.05) [EXAMINER-C] | a scored vector component, not a nuisance [CONSTRAINTS-G] | not computed | a scored vector component [EXAMINER-C] | not computed |
