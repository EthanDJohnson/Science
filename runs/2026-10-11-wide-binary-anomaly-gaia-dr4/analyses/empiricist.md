# Analysis: empiricist (Hume)
status: final

## Method applied
For each claim I separate what was measured (instrument, sample, cuts, estimator, quoted error, replication) from what was inferred (γ, "MOND", "artefact"). I map each published analysis to one estimator family and give its γ in the brief's scoring bin. I set base rates from how comparable disagreements between precision methods ended, find analogues in adjacent kinematic tests, and list what an honest skeptic would require and whether it exists. Units: SI accelerations (m s⁻²); γ = G_eff/G is dimensionless.

## Findings

F1. **Everyone observes the same thing.**
- Every DR3 analysis measures the same quantities:
  - sky-plane relative proper motion (Gaia DR3, 34-month baseline; σ_μ ≈ 0.02–0.03 mas/yr at G = 9–14) [D-14];
  - parallax distances;
  - photometric masses.
- Most draw on the El-Badry et al. 2021 parent catalogue [D-10, D-11].
- γ is never observed. It is inferred from a ṽ statistic through a template, and the template assumes:
  - an eccentricity distribution;
  - f_multi;
  - a mass–light relation;
  - a projection model [D-06, D-15, D-17, D-49].
- The DR3 results are therefore correlated re-analyses of one sky dataset, not replications.
- The only independent kinematic data are small RV subsamples:
  - Saad & Ting C3PO: 85 pairs, RV precision ~8–15 m/s [D-27];
  - ESPRESSO: 26 pairs [D-38];
  - HARPS: 44 pairs [D-37];
  - the 36-pair and 312-pair 3D samples [D-25, D-26].

F2. **The disagreement sorts by camp, and each camp agrees with itself.**
- I ran a grouped χ² on the published low-acceleration γ values.
- Pro-anomaly group: weighted mean 1.436 ± 0.040, χ² = 1.92 for 5 dof (p = 0.86).
  - Members: Chae 2023; Chae 2024a; Chae 2024b including systematics; Yoon, Tian & Chae 2025; Hernandez et al. 2024; Chae 2025.
- Null group: weighted mean 1.022 ± 0.016, χ² = 3.04 for 3 dof (p = 0.39).
  - Members: Banik+24 converted to γ; Boufourou E2; Saad & Ting C3PO; Saad & Ting's 36-pair re-analysis.
- Between the camps, χ² = 93.4 for 1 dof (z ≈ 9.7). The pooled PDG scale factor is S = 3.31.
- Because the data are correlated [D-11], these χ² values overstate the independent evidence. The pattern holds anyway: **who did the analysis predicts γ better than any listed physical variable.** The analogues show the same signature in method-clustered disagreements (proton radius, muon g-2). [calc: runs/2026-10-11-wide-binary-anomaly-gaia-dr4/calc/lens-empiricist_tensions.py]

F3. **Head to head, with systematics included, the pairwise tensions are only about 2–3σ.**
- Chae 2024b (stat + syst; total error +0.189/−0.127) against Boufourou E2 on the same parent catalogue: z = 2.51. On statistical error alone, z = 3.50.
- Chae 2024b against Banik+24 converted to γ: z = 2.91.
- Chae et al. 2026 against Saad & Ting, on the same 36 pairs: z = 2.16.
- The headline significances are of a different kind:
  - "16σ against MOND" [D-28, D-31] and "5.8–9.2σ against Newton" [D-22] each reject the other side's template inside one's own model.
  - Neither is a tension between two measurements.
- Only Chae 2023's 1.43 ± 0.06 gives a large pairwise z against Banik (6.6). Its error is statistical only. [calc: same]

F4. **On the same data, analyst choices alone move γ as much as the whole dispute does.**
- (a) Chae 2024 catalogue:
  - From Chae 2024b (1.37) to Boufourou E2 (1.045), the gap is 0.325.
  - Boufourou's implied full-median value on the same sample is 1.12 (global) to 1.20 (deep) [D-31, D-90]. That assigns 23–48% of the gap to the choice of estimator.
  - The remaining 52–77% comes from the rest of the pipeline: his cuts keep 51.5% of pairs, and f_multi calibration and templates differ.
- (b) Same 36 pairs, deprojection model only: Δγ = 0.56 [D-17].
- (c) Cookson+26, same group and same estimator:
  - At 130 pc with the ipd = 0 cut, the data prefer Newton by 1501×.
  - At 150 pc without the ipd cut, they prefer MOND by 12×.
  - That is a 4.3-dex swing [D-29].
- (d) Eccentricity template alone, pure median: the spurious γ runs from 0.73 to 1.73 across plausible f(e) [D-49]. Boufourou's f(e) band is [0.957, 1.068] [D-31].
- These are observed sensitivities, not conjecture. The analyst degrees of freedom are as large as the effect. [calc: same]

F5. **Independent RV data are consistent with both answers.**
- Saad & Ting C3PO, with RV precision ~24× better than Gaia DR3 [D-27]:
  - s > 3 kau: γ = 1.17 +0.37/−0.23 (18 systems), 0.54σ from 1.37 and 0.74σ from 1.00;
  - s < 3 kau: γ = 1.05 +0.11/−0.08.
- These are the only kinematic data independent of Gaia proper motions, and in the regime that matters they are underpowered. [calc: same]

F6. **Boufourou's deep bin is the closest DR3 number to a direct low-g_N measurement by a robust estimator.**
- Value: 1.11 ± 0.07 after the perspective correction; 0.97 before it [D-31].
- That is 1.6σ above Newton and 3.7σ below 1.37.
- It does not fall in the brief's scoring bin:
  - g_N/a0 ∈ [0.03, 0.3] is g_N = 3.6×10⁻¹² to 3.6×10⁻¹¹ m s⁻² (log10 −11.44 to −10.44);
  - so it does not contain 10⁻¹⁰.
- Among the published values, only Chae 2025's MOND-regime bin and Chae+26's g_N < 10^-9.5 bin satisfy "wholly below 10^-9.5 and containing 10^-10". The DR4 papers will probably fall under the fallback rule. [calc: runs/2026-10-11-wide-binary-anomaly-gaia-dr4/calc/lens-empiricist_baserates.py]

F7. **Converting Banik's result to γ barely depends on which MOND value is used.**
- α_grav = −0.021 +0.065/−0.045 gives:
  - γ = 0.993 +0.022/−0.015 for γ_MOND,paper = 1.333;
  - γ = 0.991 +0.029/−0.020 for 1.44.
- The scoring conversion is therefore robust for this family. Banik's α is a global fit over 2–30 kau, not a bin [D-28], so a bin-level number from a DR4 mixture paper may differ. [calc: lens-empiricist_baserates.py]

F8. **Base rate.**
- Reference class: ten disagreements between precision methods, or anomalies claimed to be new physics. Table L3 lists them.
  - 8 are resolved, and 0 of those 8 as new physics.
  - Causes: a systematic in one method (3), a shared input (1), an estimator or model assumption (3), hidden binaries (1).
  - 2 are unresolved: neutron lifetime and the Hubble tension.
- Rule of succession: P(new physics | resolved) ≈ 0.10; with a Jeffreys prior, 0.06.
- Median time to resolution: ~4 yr (range 0.1–14 yr).
- In the three-case astrophysical-kinematics subset, all three resolved as an estimator or model assumption, or as unresolved binaries. The wide-binary dispute belongs to that subset.
- This is a prior, not a verdict. It weighs against "real" but does not eliminate it. [calc: lens-empiricist_baserates.py]
  - Key sources: [new: Bovy & Tremaine 2012, ApJ 756, 89, abstract, "We show that this result is incorrect and that it arises from the assumption that the mean azimuthal velocity of the stellar tracers is independent of Galactocentric radius at all heights."]; [new: Kirby et al. 2017, ApJ 838, 83, abstract, "Our previous measurement of sigma_v, based on six stars, was inflated by the presence of a binary star with variable radial velocity."]; [new: McLaughlin & Meylan 2003, arXiv:astro-ph/0302257, abstract, "There is no need to invoke MOND or dark matter to explain the current data."]; [new: Aliberti et al. 2025, Phys. Rept. 1143, arXiv:2505.21476, abstract, "a_mu^exp - a_mu^SM = 38(63) x 10^-11, which implies that there is no tension between the SM and experiment at the current level of precision."].

F9. **How these disagreements end matters for DR4.**
- In the resolved cases, the decisive evidence was new data whose systematics were orthogonal to the old ones:
  - proton radius: PRad scattering and new H spectroscopy (general knowledge, not quoted here; the Xiong & Peng abstract confirms the setup [new: Xiong & Peng 2023, arXiv:2302.13818, abstract, "the large discrepancy between r_E^p measurements from muonic hydrogen spectroscopy, and those from ep elastic scattering and ordinary hydrogen sp..."]);
  - Triangulum II: multi-epoch RVs;
  - muon g-2: lattice HVP replacing e⁺e⁻ input.
- When the same camps re-analysed the same data, the cases did not close: Moni Bidin et al. 2015 still dispute Bovy & Tremaine [new: Moni Bidin et al. 2015, A&A 573, A91, abstract, "This result was challenged by Bovy & Tremaine (2012, ApJ, 756, 89), who claimed that the observational data are consistent with the expected dark matter density if a one-dimensional approach is adopted."].
- DR4 brings the same kind of data as DR3 (more and better proper motions), plus one orthogonal handle on the key nuisance: epoch astrometry and acceleration and NSS solutions that detect hidden companions [D-12, D-85, D-93].
- Expectation: in the first papers each camp keeps its estimator and its γ. Movement comes only from analyses that use the orthogonal companion census.

F10. **The f_multi transfer premise has no direct observational support, and the one relevant measurement shows a separation dependence.**
- Bashi, Clarke & Belokurov 2026 [new: Bashi, Clarke & Belokurov 2026, MNRAS stag730, arXiv:2604.06317, abstract, "suggesting an enhancement factor κ = P_{2+2}/p^2 = 2.34_{-0.11}^{+0.12} ... the enhancement remains strong at separations ≤ 5 000 AU, but shows a decline towards unity at the widest separations (≥ 10 000 AU)"].
  - The statistic that varies with s is a correlation of hidden close binaries (2+2 quadruples), not f_multi itself.
  - This is an observed s-dependence across exactly the boundary between Chae's calibration regime and the low-g_N regime [D-03, D-15].
- Direction, as my inference: if the hidden-multiple velocity tail thins at wide s, a template calibrated at small s over-subtracts at large s and biases γ low. That would help the anomaly, not hurt it.
- The other observations point the other way: 46% RV-variable at s > 13 kau (ESPRESSO, archival) [D-38]; 27% (HARPS) [D-37]; ≲ 5% (C3PO) [D-27].
- Net: the direction of the f_multi transfer bias is unobserved, and the samples disagree by a factor of ~10 because of selection [D-68].

F11. **The evidence an honest skeptic would require mostly does not exist yet.** Table L4 has the detail.
- No blinded analysis exists [D-18].
- No camp has run the other camp's estimator on its own catalogue. Boufourou is a third party, and his work is unreplicated [D-50, D-90].
- No result shows γ depending on g_N at fixed s (varying the mass). That test would separate an acceleration law from separation-dependent multiplicity or eccentricity systematics. I found none in the dossier.
- No test of the EFE anisotropy signature has been run: ~15% larger boost along the external field [D-02].
- No independent RV-clean deep-regime sample has a σ(γ) < 0.1 (C3PO's large-s σ is ~0.3) [D-27].

## Lens-specific outputs

### L1. Mapping of published analyses to estimator families, with γ in or near the scoring bin

| Analysis | Family (justification) | γ (bin; g_N definition) | Sample, N | Error as quoted | Data independence |
|---|---|---|---|---|---|
| Chae 2023 [D-20] | 1 full-median (acceleration plane, MC-calibrated; researchers' mapping [D-69]) | 1.43 ± 0.06 at g_N = 10^-10.15; variants 1.33–1.43 at ~6×10⁻¹¹ m s⁻² | DR3, d < 200 pc, 26,615 | stat only | parent of Chae 2024b's "2023a sample" |
| Chae 2024a [D-21] | 1 (no triple component; sample claimed pure) | 1.49 +0.21/−0.19 (g ≲ 10⁻¹⁰) | 2463 "pure" | stat | Chae DR3 apparatus |
| Chae 2024b [D-22] | 1 ("Most analyses of this work are based on the medians of ṽ") | 1.37 +0.10/−0.09 stat +0.16/−0.09 syst (s/r_M ≳ 0.7, s ≳ 5 kau) | 6389 (new), 3557, 19716 | stat + syst | overlaps Chae 2023; re-analysed by Boufourou |
| Yoon, Tian & Chae 2025 [D-23] | unassigned; nearest is 1 (2D, Chae pipeline) | 1.26 +0.12/−0.10 at 10^-10.3; 1.32 +0.12/−0.11 for g_N ≲ 10⁻¹⁰ | DR3 to 50 kau, N not given | stat | Chae DR3 apparatus |
| Hernandez et al. 2024 [D-24] | unassigned (1 or 3) | 1.5 ± 0.2 (r_2D > 0.01 pc) | pure-binary clean sample, N not extracted | stat | DR3, separate cuts |
| Banik et al. 2024 [D-28] | 3 mixture (close-binary and LOS components) | α_grav = −0.021 +0.065/−0.045 → γ ≈ 0.99 +0.03/−0.02 (global 2–30 kau, not a bin) | d < 250 pc, 8611 | MCMC | DR3, El-Badry parent |
| Pittordis, Sutherland & Shepherd 2025 [D-30] | 3 | no γ; Newton "significantly better" | DR3, FLAME masses, r_p > 2 kau | n/a | supersedes P&S 2023 |
| Cookson et al. 2026 [D-29] | 2 tail-truncated (median after ṽ < 2.5 cut [D-69]) | no γ; Newton 535–1501× at d < 130 pc; MOND 12× at d < 150 pc without ipd cut | 1216–1421 | n/a | DR3, small-d subset |
| Boufourou 2026, E2 [D-31] | 2 | 1.045 [1.025, 1.068] (2–30 kau); deep bin 1.11 ± 0.07 (log g_N −11.44 to −10.44) | Chae 2024 catalogue, 41,760 of 81,088 | 68% bootstrap, stat | same data as Chae 2024b |
| Boufourou 2026, E3 [D-31] | 3 | 1.05 [1.04, 1.07] | same | stat | same |
| Chae 2025 [D-25] | 4 Bayesian 3D | 1.48 +0.33/−0.23 (10^-11.0 to 10^-9.5; inside the scoring bin) | 312 total, 35 in bin | stat | DR3 + RVs; may overlap Chae+26 |
| Chae et al. 2026 [D-26] | 4 | 1.60 +0.24/−0.14 (g_N < 10^-9.5; inside the scoring bin); 1.48 without the two dominant systems (< 10^-10.1) | 36 | stat | same 36 pairs as Saad & Ting |
| Saad & Ting 2026, 36-pair [D-17] | 4 | 1.00 +0.24/−0.19 | 36 | stat | same data as Chae+26 |
| Saad & Ting C3PO [D-27] | 4 (RV-based) | 1.17 +0.37/−0.23 (s > 3 kau); 1.05 +0.11/−0.08 (s < 3 kau) | 57 bound | stat | **independent RVs** |
| Makarov 2026 [D-32] | none (orbital-momentum test) | no γ | 103,169 | n/a | DR3 |

### L2. Observation vs inference ledger

| Claim | What was observed (instrument, conditions) | What was inferred | Replication status |
|---|---|---|---|
| "Wide binaries at low g move ~20% too fast" | DR3 PM differences; median ṽ rising with s/r_M in Chae samples [D-22] | γ ≈ 1.37 via an f_multi-calibrated template | Same apparatus; not reproduced by any other group's estimator on the same data. Boufourou gets 1.12–1.20 with E1 on the same catalogue, not 1.37 [D-31] |
| "MOND excluded at 16σ" | DR3 PM differences for 8611 pairs [D-28] | α_grav via a mixture model with a fitted f_CB ≈ 0.63–0.70 and a fitted γ_e ≈ 2 | Partly echoed by Boufourou E3 (also 16σ, statistical only). Template-conditional |
| "Fat ṽ tail" | ṽ values of 1.5–6 [D-08] | hidden triples | The tail is directly observed. The triple attribution is supported by RV monitoring (27–46% variable in archival samples) [D-37, D-38] |
| "Two systems exceed escape speed" | 3D velocities [D-26] | MOND boost (Chae) vs unbound or perturbed pairs [D-94] | Two objects, not replicated. Pasquini finds 3/12 such pairs in a Newton-agnostic sample [D-38] |
| "Quality cuts create the null" | Cookson's flip under the ipd/distance cut [D-29] | cuts bias toward Newton (Chae & Yoon) or remove contaminants (Cookson) | Observed sensitivity; the causal direction is not observed |
| "f_multi transfers from 10⁻⁸ to 10⁻¹⁰ m s⁻²" | not observed | assumption [D-15, D-86] | One multiplicity statistic varies with s (F10) |

### L3. Base-rate table (reference class: disagreements between precision methods, or claimed new physics, decided by later work)

| Case | Years open | How it ended | Lesson for this run |
|---|---|---|---|
| Proton radius, μH vs eH/ep | 2010–2019 | systematic in the older method (general knowledge; setup quoted F9) | new, orthogonal data decided it, not re-analysis |
| Muon g-2 vs SM | 2021–2025 | shared input (HVP); "no tension" [new: Aliberti et al. 2025, abstract, quote in F8] | the disputed piece was a calibration input, like f_multi here |
| Local DM density (Moni Bidin vs Bovy & Tremaine) | 2012 | estimator assumption [new: Bovy & Tremaine 2012, quote in F8] | a Gaia-type kinematic anomaly from one estimator assumption; the original authors still dispute it [new: Moni Bidin 2015] |
| ω Cen outskirts "MOND flattening" | 2003 | consistent with Newton and earlier data [new: McLaughlin & Meylan 2003] | the closest prior low-acceleration kinematic MOND claim; not confirmed |
| Triangulum II dispersion | 2015–2017 | one hidden binary inflated σ_v [new: Kirby et al. 2017] | hidden binaries inflating velocities is the exact mechanism disputed here |
| Pioneer anomaly | ~1998–2012 | thermal recoil (general knowledge) | unmodelled systematic in a precision measurement |
| OPERA superluminal ν | 2011–2012 | hardware fault (general knowledge) | — |
| Fifth force from the Eötvös re-analysis | 1986–~1990 | not confirmed by new experiments (general knowledge) | a re-analysis anomaly died under new dedicated data |
| Neutron lifetime, beam vs bottle | 2005– | unresolved (general knowledge) | method-clustered and persistent; both camps keep their values |
| Hubble tension | 2016– | unresolved (general knowledge) | intermediate methods (TRGB) give intermediate values, an analogue of the "intermediate γ" candidate |

Tally: 8 resolved, 0 as new physics; Laplace P ≈ 0.10, Jeffreys ≈ 0.06 [calc: lens-empiricist_baserates.py]. Caveat: the reference class is chosen by me, the general-knowledge rows are not quoted, and a small N gives a wide interval.

### L4. What an honest skeptic would require, and whether it exists

| Requirement | Exists? | Evidence |
|---|---|---|
| A blinded analysis, or one pre-registered before the data | No for DR3. Partly for DR4: Boufourou's protocol, still draft v0.95 | [D-18, D-91, D-70] |
| Each camp's estimator run on the other camp's catalogue, and each camp's injection-recovery run on the other's generator | No. Only Boufourou (third party, unreplicated) | [D-50, D-90] |
| γ dependent on g_N at fixed s (by mass), not on s at fixed g_N | Not found | — |
| The EFE anisotropy signature (boost larger along g_ext by ~15%) | Not tested | [D-02] |
| A direct hidden-companion census at s ≳ 5 kau with N ≳ 10³ | No. Only N ≈ 26–85 RV samples with conflicting rates | [D-27, D-37, D-38]; DR4 NSS/acceleration solutions are the first chance [D-12] |
| An independent RV-clean deep-regime γ with σ < 0.1 | No (C3PO σ ≈ 0.3 at s > 3 kau) | [D-27] |
| The same answer from more than one research group using a family-1 estimator | No. All family-1 values come from the Chae pipeline or Hernandez | L1 |

## Calculations

- `runs/2026-10-11-wide-binary-anomaly-gaia-dr4/calc/lens-empiricist_tensions.py` (log beside it) computes pairwise tensions, the grouped χ² by camp and by family, and the same-data gap decomposition. Results:
  - z = 2.51 for Chae 2024b vs Boufourou E2, including systematics;
  - z = 2.91 vs Banik;
  - z = 2.16 for Chae+26 vs Saad & Ting;
  - between camps, χ² = 93.4 for 1 dof (z = 9.7) with within-camp p = 0.76;
  - between families, χ² = 56.2 for 3 dof (z = 6.9);
  - the estimator share of the Chae-vs-robust gap is 23–48%;
  - the Cookson cut swing is 4.26 dex.
- `runs/2026-10-11-wide-binary-anomaly-gaia-dr4/calc/lens-empiricist_baserates.py` computes three things:
  - the base-rate tally: 0 of 8 resolved as new physics; Laplace 0.100, Jeffreys 0.056; median time to resolution 4 yr;
  - Boufourou's deep-bin range, log10 g_N = −11.44 to −10.44 (m s⁻²), which does not contain −10;
  - the α_grav → γ conversion: 0.991–0.993, insensitive to γ_MOND,paper between 1.333 and 1.44.

## Candidate answers (at least 3; the null and a reframe count)

- [EMPIRICIST-A] **Null, estimator plus pipeline artefact.** True γ ≈ 1.00–1.05 in the scoring bin. The pro-anomaly values come from full-median and acceleration-plane estimators combined with pipeline choices: f_multi transfer, missing ṽ-error and companion cuts, and geometric deprojection.
  - status: **surviving.**
  - Observations it rests on:
    - on the same data, choices move γ by 0.3–0.6 (F4);
    - the robust and mixture families agree with each other (F2);
    - Saad & Ting reproduce 1.56 from the same pairs by switching only the deprojection [D-17];
    - the analogues in the hidden-binary and estimator-assumption subset (F8, L3).
  - Weakest link: the robust estimators' ability to recover an injected boost is shown only by Boufourou's unreplicated grid [D-50]. His own implied E1 value is 1.12–1.20, not 1.37, so the estimator explains only 23–48% of the gap and the remainder is attributed but not demonstrated.
  - Distinguishing test: DR4 acceleration and NSS flags remove hidden-companion hosts. A family-1 γ that then falls toward ≲ 1.15 in the clean subsample supports A.
  - DR4 per family: F1 ≈ 1.10–1.35 (falling as companions are flagged); F2 ≈ 1.00–1.06; F3 ≈ 0.98–1.05; F4 ≈ 1.0–1.6 (model-dependent).
  - confidence: medium.

- [EMPIRICIST-B] **Real low-acceleration boost.** γ ≈ 1.3–1.5. The robust and mixture families absorb it through a fitted triple fraction and a too-eccentric template.
  - status: **strained.**
  - Observations it rests on:
    - six internally consistent pro-anomaly values (χ²/dof = 1.92/5);
    - two Bayesian 3D fits inside the scoring bin: 1.48 and 1.60 [D-25, D-26];
    - Cookson's own 12× MOND at d < 150 pc [D-29].
  - Why strained:
    - all of these come from one pipeline lineage plus Hernandez, not independent data (F1);
    - the 1.60 is dominated by two pairs above escape speed [D-26];
    - the only independent high-precision RV result is 1.17 +0.37/−0.23, uninformative between the two answers (F5);
    - the base rate for "new physics" in this reference class is ~0.06–0.10 (F8).
  - Not eliminated: the f_multi transfer bias has an unobserved sign (F10), and Boufourou's deep bin of 1.11 ± 0.07 is 1.6σ above 1.
  - Distinguishing test:
    - γ rises with decreasing g_N at fixed s (by mass);
    - the boost is anisotropic relative to g_ext;
    - it survives DR4 companion flagging.
  - DR4 per family: F1 ≈ 1.3–1.45; F2 ≈ 1.15–1.35 if not diluted; F3 ≈ 1.1–1.35; F4 ≈ 1.3–1.6.
  - confidence: low–medium.

- [EMPIRICIST-C] **Reframe: the DR3 "measurement" is method-indeterminate, so it is a dispute about analyst degrees of freedom, not about γ.** DR3 proper motions alone cannot fix γ to better than ~±0.3 once f(e), f_multi and the projection prior are free.
  - status: **surviving.**
  - Observations it rests on:
    - camp clustering with χ²_within/dof = 5.0/8 and a between-camp z of 9.7 (F2);
    - pairwise tensions with systematics of only 2–3σ (F3);
    - single-choice sensitivities of 0.3–0.6 in γ and 4.3 dex in Bayes factor (F4);
    - the "same camps re-analysing" endings in L3.
  - Prediction: the first DR4 papers reproduce their camp's DR3 value within ~0.1. A family-1 paper from the Chae lineage gives γ ≈ 1.3–1.45, and family 2 or 3 from the Banik, Cookson or Boufourou lineage gives 1.00–1.06. The spread closes only when DR4 epoch-astrometry companion censuses or large RV samples fix f_multi(s) and f(e) empirically, which is unlikely by 2027-06-30.
  - This candidate is compatible with A or B as the eventual physical truth. Its claim is about what the data can currently decide.
  - confidence: medium–high for the "camp persistence" prediction.

- [EMPIRICIST-D] **Intermediate residual.** True γ_eff in the deep bin is 1.05–1.2, from a small unmodelled shared systematic (mass scale, perspective, or a weak f_multi(s) trend) that neither camp fully removes.
  - status: **surviving (weakly).**
  - Observations:
    - Boufourou's deep bin is 1.11 ± 0.07, raised from 0.97 by the perspective correction [D-31, D-62];
    - C3PO's large-s γ is 1.17 [D-27];
    - Hernandez & Kroupa's mass-normalisation finding [D-33];
    - the Hubble-tension analogue, where intermediate methods give intermediate values.
  - Weakest link: no single systematic of the right size is identified.
  - DR4: robust families ≈ 1.05–1.15 in the deep bin; F1 ≈ 1.2–1.35.
  - confidence: low.

- [EMPIRICIST-E] **The γ spread comes mainly from sample and selection differences.**
  - status: **strained.**
  - For: Cookson's cut flip [D-29], and the different d, s and RUWE cuts [D-53].
  - Against:
    - Boufourou's robust estimators on Chae's own catalogue give 1.045, so the same sample does not yield the same γ (F4a);
    - the Saad & Ting 36-pair swing involves no sample change at all.
  - Selection matters in part, but estimator and model choices on fixed data are at least as large.
  - confidence: medium (that it is not the main cause).

- [EMPIRICIST-F] **A mass or eccentricity systematic common to all families.**
  - status: **strained.**
  - A common-mode shift cannot produce a camp-clustered 0.4 split (F2). The eccentricity sensitivity is family-specific: the pure median is most affected [D-49], and the E2 f(e) band is narrow [D-31].
  - It survives only as a component of D.
  - confidence: medium.

## What would change my mind
- Toward B:
  - a DR4 analysis with the hidden-companion hosts removed by NSS/acceleration flags, by a group outside the Chae lineage, that still finds γ ≥ 1.25 in the scoring bin with any estimator;
  - or a γ that tracks g_N at fixed s and shows the EFE orientation dependence;
  - or a replicated injection-recovery showing E2/E3 absorb an injected 1.4 to ~1.05.
- Toward A:
  - Chae-lineage family-1 γ dropping below ~1.15 on companion-cleaned DR4 data;
  - or an RV sample of N ≳ 200 at s > 5 kau giving γ < 1.1 with σ < 0.08.
- Against C: the DR4 values from the two camps converge to within 0.1 in their first papers.

## Assumptions I relied on
- The dossier's family mapping [D-69]. I placed Yoon et al. 2025 and Hernandez et al. 2024 in family 1 provisionally for the grouped χ²; Chae 2023's 1.43 is the top of its variant range.
- Symmetrised errors, (up + down)/2, in grouped_chi2. These are treated as independent even though the data are correlated, so the χ² values are upper bounds.
- Boufourou's "implied full-median 1.12–1.20" as he states it [D-31]. It is not independently reproduced; the mechanist owns that.
- My choice of reference class for the base rates, including general-knowledge rows that are not quoted (proton radius resolution detail, Pioneer, OPERA, the fifth force, neutron lifetime, Hubble).
- My reading of Bashi et al. 2026's direction of effect on f_multi transfer. It concerns 2+2 correlation, not the triple fraction directly.
