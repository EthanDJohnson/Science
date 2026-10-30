# Analysis: examiner (Socrates: examine the question before answering it)
status: final

## Method applied
I define the brief's loaded terms (H0, "early", "local", "tension", "systematic", "settle") and test whether each definition holds up. For each hidden premise I give what supports it, what would falsify it and what the question becomes if it is false. I test rival partitions of the data with a grouped χ² (one representative per class, current values, approximately independent). I then look for a better-posed reframe and list the hardest checkable questions any answer must survive. Units throughout: H0 in km s⁻¹ Mpc⁻¹ (written km/s/Mpc), magnitudes in mag, r_d in Mpc.

## Findings

1. **"H0" in the brief is two different quantities.** The local value is a kinematic, model-light quantity: an M_B calibration converted through the SN magnitude–redshift relation at 0.023 < z < 0.15 [D-06]. The "early" value is the free parameter of flat ΛCDM, fitted to θ_*, ω_b and ω_c [D-01]. Across late-time and early-time model choices fitted to CMB(+BAO)(+SN), the "CMB H0" ranges from 63.6 (w0wa, DESI+CMB) to 71.0 (EDE profile likelihood). That is a spread of 7.40 km/s/Mpc, larger than the gap itself [D-51, D-52, D-53] [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-examiner_partitions.py]. Premise 3 ("the CMB measures H0") is false as stated. What survives model changes is the product r_d·h (BAO, D-03, D-45) and θ_* (D-40). The well-posed comparison is between quantities that are invariant under the late-time model: M_B, or r_d·H0.

2. **The size of the gap is not one number. It depends on which pair is compared** [calc: lens-examiner_partitions.py]:
   - SH0ES 73.49 vs CMB-SPA 67.19: +6.30 ± 1.00, z = 6.27; 9.38%; ΔM_B = 0.195 mag; r_d would need to fall to 134.4 Mpc (−8.57%).
   - H0DN-corrected 73.26 vs DESI BAO+BBN 68.50: 6.95%; 0.146 mag; r_d −6.50%.
   - CCHP 70.39 vs CMB-SPA: +3.20 ± 1.97, z = 1.62; 4.76%; 0.101 mag; r_d −4.55%.

   An early-time solution must therefore shrink r_d by between 4.5% and 8.6% depending on which local value is "true". D-56 quotes 7.7–8.3% against Planck 67.4, which understates the requirement against CMB-SPA. The brief's placeholder "~8%, 0.17–0.19 mag" sits inside this range but is not unique.

3. **Premise 1 (the tension is real and about 5σ) depends on the pairing, but it does not hinge on SH0ES alone** [calc: lens-examiner_partitions.py]:
   - Every local class except SH0ES lies 0.5–2.7σ from CMB-SPA on its own: CCHP 1.62σ, SBF 2.72σ, Tully–Fisher 1.49σ, TDCOSMO-2026 1.64σ, masers 1.19σ, sirens 0.53σ.
   - Combined without the SH0ES Cepheids (CCHP, SBF, TF, TD, masers, sirens), they give 71.69 ± 1.14 km/s/Mpc: 3.74σ above CMB-SPA, 2.49σ above BAO+BBN, and 1.22σ below SH0ES.
   - A rough GLS that lets CCHP and SBF share the NGC 4258 anchor error (1.45% in distance; RE-27 value, not seen by the checker) gives 71.47 ± 1.26, 3.25σ above CMB-SPA.
   - The one-step methods alone (TD, masers, sirens) give 71.27 ± 1.93: 2.07σ from CMB-SPA and 1.04σ from SH0ES. They cannot yet tell the two sides apart.

   This matches the TDCOSMO companion: 3.7σ without SNe and 2.7σ without the ladder [D-90]. **Reading:** a Cepheid-independent local excess of about 3σ exists. The "≥5σ" claim needs the SH0ES Cepheid–SN ladder or a combination dominated by it (H0DN, D-22).

4. **Premise 2 (the partition): the data cannot yet choose between "early vs late", "uses r_s vs not" and "anchored ladders vs everything else"** [calc: lens-examiner_partitions.py]. Grouped χ² results, 12 classes, pooled χ² = 54.03 for 11 dof:

   | Partition | Between-group z | Within-group χ² | p (within) |
   |---|---|---|---|
   | P1 early (incl. r_s-free shape) vs late | 6.73 | 8.76/10 | 0.555 |
   | P2 uses r_s vs does not | 6.45 | 12.40/10 | 0.259 |
   | P4 NGC 4258/LMC-anchored ladders (SH0ES, CCHP, SBF, TF) vs rest | 6.51 | 11.64/10 | 0.31 |
   | P5 three groups (r_s 67.51 ± 0.29; ladders 73.02 ± 0.78; one-step + r_s-free 69.93 ± 1.17) | 6.50 (2 dof) | 7.56/9 | 0.579 |
   | P3 SH0ES alone vs everything else | 5.87 | 19.58/10 | **0.034** |

   - P1, P2 and P4 all fit acceptably. The swing class (time delays, masers, sirens, r_s-free BAO and the equality scale) sits at 69.93 ± 1.17. That is about 2.0σ from the r_s group and about 2.2σ from the ladder group, so it does not yet adjudicate.
   - P3 is the worst partition: SBF, Tully–Fisher and the one-step methods do not sit with the CMB.
   - The reframe "SH0ES against everything else" is therefore **strained** by the data. The reframe "anchored distance ladders against everything else" is **as good as** "early vs late".

5. **The null as stated (one H0, quoted errors) fails. A null with uniformly inflated errors needs a scale factor of 2.22.** Pooled mean 68.25 ± 0.26, χ² = 54.03/11, p = 1.17×10⁻⁷ [calc: lens-examiner_partitions.py]. Every within-class χ² is acceptable (P5 within p = 0.58). The excess scatter therefore sits between classes, not spread evenly across measurements. A "many small underestimated errors" null predicts excess scatter within classes, and none is seen. That strains the null.

6. **Premise 8 (the tension is about M_B, not H0) is better posed but does not shrink the slate. It moves the question.**
   - Restated as ΔM_B: 0.10–0.195 mag, depending on the pair (Finding 2).
   - The published direct M_B pair is ladder −19.253 ± 0.027 vs inverse ladder −19.375 / −19.394 mag [D-21]. Its naive difference of 0.12–0.14 mag is **not** a valid comparison, because the SN systems differ (Pantheon+ vs DES-SN5YR) [calc: lens-examiner_partitions.py].
   - The M_B framing makes late-time H(z) changes irrelevant by construction [D-06, D-70]. It leaves three places for the error: the ladder calibration of M_B; a z-dependent M_B (D-92, speculative); or r_d (early-time physics).
   - The r_d framing, r_d·h fixed [D-03, D-45], is equivalent. The DESI 2025 w0wa preference moves the CMB+BAO H0 *down* [D-12, D-51], so it cannot rescue a late-time H(z) solution.
   - Camarena & Marra already pose the problem this way [new: Camarena et al. 2023, arXiv:2307.02434, abstract, "We extend the analysis by SH0ES to an arbitrary cosmographic model"].

7. **The r_s-free class is the sharpest existing test of early-time new physics, and so far it sides with the CMB** [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-examiner_rsfree.py].
   - An r_s reduction leaves H0 values that bypass r_s at the true H0. If early-time new physics were the whole answer, they would read about 73.
   - The DESI DR1 r_s-free values are 66.7–70.3. They sit 1.90–3.50σ below SH0ES and 0.27–2.47σ from CMB-SPA [D-49]. The equality-scale values are 65.1 and 70.6, 0.76–2.67σ below SH0ES [D-50].
   - Caveats: the D-49 sets are correlated through DESI DR1. The equality scale depends on N_eff, so the test is clean against EDE-like r_s reduction but not against ΔN_eff.
   - An r_s-free H0 at about 1.0 km/s/Mpc (1.5%) would separate 73.3 from 67.5 at about 5.8σ.

8. **Even without a SH0ES prior, early-time fits close only part of the gap** [calc: lens-examiner_partitions.py]. Gap closed against SH0ES–CMB-SPA, and residual against SH0ES:

   | Fit | Source | Gap closed | Residual vs SH0ES |
   |---|---|---|---|
   | EDE P-ACT-LB | [D-52] | 43% | 2.43σ |
   | Poulin 2026 profile | [D-53] | 60% | 1.73σ |
   | eROSITA EDE | [D-94] | 67% | 1.24σ |
   | Modified recombination | [D-52] | 38% | 2.85σ |
   | PMF | [D-52] | 30% | 4.16σ |

   No early-time model fitted to all data reaches 73. The best case moves the CMB value into the swing class (about 71). The "early versus late new physics" dichotomy in the brief therefore misses a real third option: partial early-time physics plus a smaller ladder correction. That option violates the brief's "mutually exclusive" requirement unless it is listed as its own candidate.

9. **Premise 4 (local = global) is well tested and holds.** ΛCDM cosmic variance is σ = 0.31 km/s/Mpc, and the gap is about 18–20σ of it [D-10, D-37]. LTB voids with |δ| > 20% are excluded at 4–5σ [D-11]. Flow corrections act the wrong way: they *raise* the SN H0 by about 0.6 km/s/Mpc [D-36]. The local-structure candidate is eliminated within ΛCDM. The only survivor is the non-Copernican or backreaction version, which is speculative and was not covered by any facet [D-97]. Timescape proponents claim SN evidence against FRW [new: Seifert et al. 2025, MNRAS 537 L55, abstract via arXiv:2412.15143, full-text of abstract page, "When considering the entire Pantheon+ sample, we find very strong evidence ($\ln B> 5$) in favour of timescape over $\Lambda$CDM"], but that abstract makes no H0-gap claim, and the claim is minority and unreplicated here.

10. **Premise 6 (JWST settled crowding) is true only in a narrow sense.**
    - JWST bounds Cepheid photometric bias at 0.01–0.03 mag [D-09, D-78], against the 0.1–0.15 mag P–L intercept bias that would be needed [D-79b]. Photometry is therefore closed as a full explanation.
    - It does not test the Cepheid–TRGB–JAGB zero-point and selection disputes [D-80, D-81, D-88] or SN calibrator–Hubble-flow standardisation [D-35, D-82]. Those are each 1–3 km/s/Mpc levers (Percival −1.4 / −0.2 / −1.0; Dong 74.30 → 71.37; Wojtak & Hjorth 70.6–71.5). Together they could account for a large part of the ladder–CMB gap, but they "need not add" [D-88].

11. **Premise 9 (early-time solutions viable): viable only as "partial" models.** Bayesian bounds give f_EDE < 0.061–0.12 [D-75]. Profile likelihoods allow f_EDE = 0.09 ± 0.03 [D-53]. The dispute is about the statistical method (prior volume), not the data [D-83]. The sound-horizon-only no-go [D-73] predicts exactly this pattern of partial closure.

12. **"Settle" needs a stated target.** The precision a deciding total uncertainty needs [calc: lens-examiner_partitions.py]:

    | Separate | Gap | For 3σ | For 5σ |
    |---|---|---|---|
    | 73.3 from 67.2 | 6.1 | 2.03 (2.77%) | 1.22 (1.66%) |
    | 73.3 from 70 (SH0ES-like vs CCHP-like) | 3.3 | 1.10 (1.50%) | 0.66 (0.90%) |
    | 73.3 from 68.5 | 4.8 | 1.60 (2.18%) | 0.96 (1.31%) |

    All values in km/s/Mpc. No current one-step method is below 3% [D-31, D-32, D-33]. Lensed supernovae remain at about 15% [new: Pierel et al. 2025, arXiv:2509.12301, full-text (abstract page), "$H_0=66.9_{-8.1}^{+11.2} \rm{km} \rm{s}^{-1}\rm{Mpc}^{-1}$"]. The forecast route to 1% is about 40 time-delay lenses [D-dossier §6, Treu 2026 review forecast].

## Lens-specific outputs

### A. Definitions tested

| Term | Brief's definition | Does it survive? | Repair |
|---|---|---|---|
| H0 | ȧ/a today of the FRW background, a global quantity | Partly. Locally it is an M_B → magnitude–redshift conversion [D-06]; "early" it is a ΛCDM fit parameter whose value moves by 7.4 km/s/Mpc across models (F1) | Compare model-invariant quantities: M_B (SN-normalised) or r_d·h |
| "Early-universe H0" | CMB/BAO under ΛCDM | Survives as a definition, but BAO+BBN, the inverse ladder and CMB all share standard pre-recombination physics. They are one class, "uses r_s", not three | Group by "uses r_s" |
| "Local H0" | z ≲ 0.15, ladder or one-step | Mixes two different things: anchored ladders (sharing NGC 4258, LMC, MW) and one-step absolute methods. The data place them at different means (73.0 vs 69.9; F4) | Split into "anchored ladder" and "one-step" |
| Tension | difference with its significance | Ill-defined until the pair is chosen: 1.6σ to 6.9σ (F2, F3) | State the pair, correlations and the class-level χ² |
| Unidentified systematic | an effect > quoted error, missing from the budget | Sound. But "named effect + size" makes a sum of several 1–2 km/s/Mpc effects (D-88, D-82) look like no candidate at all | Allow a "sum of named ladder effects" sub-hypothesis with its correlation stated |
| New physics, early vs late | two classes | The late-time H(z) class is empty by construction under the M_B framing (D-70). M_B/G_eff transitions are a third class (D-92). A hybrid partial-EDE plus ladder correction is a fourth option | Re-partition as: r_d changes / M_B changes / ladder error / H(z) changes |
| "Dominant cause" | a single cause | Not guaranteed. Partial early-time closure (30–67%, F8) plus ladder levers is a live mixed answer | Admit "mixed" as a candidate |
| Settle | ≥3σ separation by 2036 | Sound, with a number: about 1.1 km/s/Mpc (1.5%) total error on a ladder-free H0 to split 73 from 70 at 3σ; about 2.0 (2.8%) to split 73 from 67 at 3σ (F12) | Use these targets |

### B. Premise ledger

| # | Premise | Support | Would falsify | If false, the question becomes | Verdict |
|---|---|---|---|---|---|
| 1 | Real, about 5σ | SH0ES vs CMB-SPA 6.27σ; all-local vs CMB-SPA 6.85σ (independent approx.) [calc] | Non-SH0ES local results converging on 67–68 | "Why is the SH0ES ladder 0.19 mag off?" | Holds at ≥5σ only with SH0ES Cepheids; about 3–3.7σ without them (F3) |
| 2 | Early vs late is the right partition | P1 between z 6.73, within p 0.56 | A partition with higher between-group and better within-group χ² | "r_s users vs non-users" or "anchored ladders vs rest" | Undetermined: P1, P2 and P4 are statistically equivalent; P3 is strained (F4) |
| 3 | CMB measures H0 | θ_* to 0.03% [D-01] | — | "Which r_d and which late-time model?" | False as stated; model spread 7.4 km/s/Mpc (F1) |
| 4 | Local = global | σ_CV 0.31 [D-10] | A void with δ ≈ −0.5 to −0.8 on about 100 h⁻¹ Mpc | Local-structure candidate | Holds within ΛCDM (F9) |
| 5 | Rungs independent | SBF has no Cepheids and no SNe [D-29] | Showing that SBF/TF and SH0ES share a biased zero point | Shared-anchor (NGC 4258) systematic | Partly false: NGC 4258 is shared by SH0ES, CCHP, SBF-JWST and the masers [D-dossier §7]; TF uses the same hosts [D-30] |
| 6 | JWST settled crowding | 0.01–0.03 mag [D-78] | — | Photometry is still open | True for photometry only; selection, zero point and SN-side issues remain open (F10) |
| 7 | Late-time solutions excluded | β_BAO, inverse ladder 67.2–67.7 [D-03, D-48]; DESI w0wa lowers H0 [D-12] | Non-standard r_d, or a z-evolving M_B | M_B/G_eff transition | Holds for smooth H(z); M_B transitions escape it by construction (D-92) |
| 8 | Tension is about H0 | — | — | M_B or r_d·h | Better posed as M_B / r_d·h (F6) |
| 9 | Early-time solutions viable | Profile likelihood f_EDE 0.09 ± 0.03 [D-53] | f_EDE < 0.06 robust to prior volume [D-75] | "Partial" solutions | Viable only as partial (30–67% closure) (F8, F11) |
| 10 (new) | A single dominant cause exists | Within-class χ² acceptable (F5) | Several named ladder levers each confirmed at 1–2 km/s/Mpc | Mixed answer | Open |
| 11 (new) | Superseded/preprint values are current | Dossier §7 | Retractions or revisions | Gap size changes | Many anchors are 2026 preprints (TDCOSMO-2026, masers, GWTC-5, Percival, Dong); treat as provisional |

### C. Reframe
The better-posed question: **"Is the SN Ia absolute magnitude calibrated by geometric anchors through stellar standard candles (M_B ≈ −19.25 in the Pantheon+ system) consistent with the one implied by r_d-calibrated BAO plus uncalibrated SNe? If not, does the error sit in the anchored ladders or in r_d?"**

This framing removes the late-time H(z) class, which is empty by construction [D-70]. It makes the arbiters explicit: H0 values that use neither r_d nor the anchored ladders (time delays, masers, sirens, r_s-free BAO/equality). Those currently sit at 69.9 ± 1.2 and favour neither side by more than about 2σ (F4). Its answer is clearer in one direction: the r_s-free values favour "r_d is standard" at about 2–3.5σ (F7). Against that, SBF and the one-step methods favour a local H0 above 67 at about 3σ (F3).

### D. Hardest questions any answer must survive
1. **Pairing:** with which local and which early value, and with what correlations, is the significance computed? Does the answer change if SH0ES Cepheids are removed? (Without them: 71.5–71.7 ± 1.1–1.3, 3.3–3.7σ above CMB-SPA.)
2. **Swing class:** which value does the candidate predict for H0 from time delays, masers and sirens (now 71.3 ± 1.9) and from r_s-free BAO/equality (66.7–70.6)? Is the prediction outside the current 1σ band of at least one of them?
3. **r_s-free check (early-time candidates):** if r_d is 4.5–8.6% smaller, why do the DESI DR1 r_s-free H0 values sit at 66.7–70.3, 1.9–3.5σ below SH0ES?
4. **SBF check (ladder-systematic candidates):** which named effect also biases SBF (73.8 ± 2.4, no Cepheids, no SNe) and Tully–Fisher high? Or does the candidate accept SBF as a 2.7σ fluctuation?
5. **Size:** does the named ladder effect reach 0.10–0.195 mag (the range from F2) once it is propagated through the SH0ES fit? Are the JWST photometric bound (≤ 0.03 mag) and the H0DN leave-one-out dispersion (0.40 km/s/Mpc, D-23) respected?
6. **Fit to all data:** what H0 does the new-physics model give with no ladder prior, against ACT DR6 + SPT-3G + DESI DR2 + SNe? What fraction of the gap does it close (30–67% for the current best)? Does it hold under both profile and Bayesian treatments?
7. **Collateral:** what does the candidate predict for S8 (DES Y6 0.789 ± 0.012), N_eff (2.86 ± 0.13), the DESI–CMB Ω_m offset (2.3–2.8σ) and the GC age (13.81 ± 0.34 Gyr)?
8. **Decidability:** which measurement by 2036 reaches about 1.1 km/s/Mpc (1.5%) on an H0 independent of both r_d and the anchored ladder? What does the candidate predict for it? (Candidates: TDCOSMO about 40 lenses at about 1%; Gaia DR4 (2 Dec 2026) for the MW anchor; an independent low-z SN calibration.)
9. **Null:** a common-H0 null needs every error inflated by 2.22. Why then are the within-class χ² values normal (P5 within p = 0.58)?
10. **Mutual exclusivity:** if the answer is "partial EDE plus a ladder correction", is it listed as its own candidate with its own predictions, rather than double-counted under both?

## Calculations
- `runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-examiner_partitions.py`, which computes:
  - grouped χ² for five partitions of 12 class representatives: P1 between z 6.73 (within p 0.555); P2 6.45 (0.259); P3 5.87 (0.034); P4 6.51 (0.31); P5 6.50 (0.579);
  - the null: pooled 68.25 ± 0.26 km/s/Mpc, χ² 54.03/11, p 1.17×10⁻⁷, S = 2.22;
  - pairwise z against CMB-SPA, with SH0ES at 6.27;
  - local combinations without Cepheids: 71.69 ± 1.14 (3.74σ); GLS with the NGC 4258 anchor shared, 71.47 ± 1.26 (3.25σ); one-step only, 71.27 ± 1.93 (2.07σ);
  - restatements of the gap: ΔM_B 0.059–0.195 mag; r_d reduction 2.7–8.6%;
  - the model spread of "CMB H0", 7.40 km/s/Mpc;
  - early-time closure fractions, 30–67%;
  - deciding precision: 1.22 km/s/Mpc for 5σ on 73.3 vs 67.2, and 1.10 km/s/Mpc for 3σ on 73.3 vs 70.
  - Errors are symmetrised as the mean of the two sides, and classes are treated as independent except in the GLS line.
- `runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-examiner_rsfree.py` computes the r_s-free H0 values against SH0ES (z 0.76–3.50) and against CMB-SPA (z 0.27–2.47).

## Candidate answers (at least 3; the null and a reframe count)
- [EXAMINER-A] **Reframe (the premise is wrong):** the anomaly is a 0.10–0.20 mag conflict between the anchored-ladder M_B and the r_d-calibrated BAO+SN M_B (equivalently in r_d·h), not an "early vs late H0" gap. Current data cannot say which side holds the error, because the swing class (one-step and r_s-free) sits midway at 69.9 ± 1.2. | status: surviving | why: P1, P2 and P4 are statistically equivalent, and late-time H(z) is excluded by construction [D-70, F4, F6] | distinguishing test: a ladder-free, r_d-free H0 at ≤ 1.1 km/s/Mpc (TDCOSMO about 40 lenses, sirens, r_s-free BAO from DESI DR2/DR3). A predicts it lands decisively on one side; it does not predict which | confidence: high (as a framing)
- [EXAMINER-B] **Anchored-distance-ladder systematic:** a sum of ladder-side effects shifts the SH0ES-dominated local value up by about 3–6 km/s/Mpc. These are calibrator selection [D-88], SN calibrator vs Hubble-flow standardisation and peculiar velocities [D-35, D-82], and the TRGB/JAGB zero point [D-80, D-81], not photometry [D-78]. | status: strained | why: SBF (73.8 ± 2.4) and TF are high without Cepheids or SNe, and the non-Cepheid local combination is 71.5–71.7, about 3.3–3.7σ above CMB-SPA (F3). "SH0ES vs everything" fits worst (p_within 0.034, F4). It survives only if the true H0 is about 70–71 and the CMB also errs, or if SBF is a 2.7σ fluctuation | distinguishing prediction: one-step/r_s-free H0 converges on 67–69; SH0ES reanalyses with Percival/Dong corrections fall to ≤ 71; Gaia DR4 MW anchor shifts SH0ES down | confidence: medium
- [EXAMINER-C] **Early-time new physics (r_d reduced 4.5–8.6%), as a partial solution:** EDE-like physics raises the r_s-based H0 to about 69–71 [D-52, D-53, D-94]. | status: strained | why: the fit to all data closes only 30–67% of the gap; r_s-free H0 values sit 1.9–3.5σ below SH0ES, against this candidate's prediction of about 73 (F7, F8); Bayesian bounds f_EDE < 0.06–0.07 [D-75] | distinguishing prediction: r_s-free BAO/equality H0 ≈ 71–73; CMB damping tail and TE deviations visible to SO / SPT-3G Ext-10k; higher ω_c and S8 | confidence: low–medium
- [EXAMINER-D] **Hybrid (partial early-time physics plus a smaller ladder correction):** about 2–4 km/s/Mpc from r_d and about 2–3 km/s/Mpc from ladder levers. | status: surviving | why: it is the only reading in which both the one-step class (about 70–71) and the best EDE fits (about 71) are "right"; it is not excluded by any finding here, but it is less parsimonious | distinguishing prediction: the ladder-free/r_d-free class converges at 70–71, distinct from both 67.5 and 73 | confidence: low
- [EXAMINER-E] **Null (one H0, errors underestimated everywhere):** | status: strained | why: it needs a uniform error inflation of S = 2.22 (χ² 54/11, p 1.2×10⁻⁷), yet within-class χ² values are normal; the excess sits between classes (F5) | distinguishing prediction: future within-class scatter grows; the class means drift together | confidence: low
- [EXAMINER-F] **Late-time H(z) new physics:** | status: eliminated | why: the inverse ladder fixes r_d·h [D-03, D-48, D-70], and DESI w0wa moves H0 down [D-12, D-51]. Only a z-dependent M_B/G_eff (D-92, speculative) escapes, and that is properly a calibration-physics candidate | distinguishing prediction: an M_B step at z ≈ 0.01 visible in a calibrator vs Hubble-flow intercept test | confidence: high (for smooth H(z))
- [EXAMINER-G] **Local structure (void or bulk flow) within ΛCDM:** | status: eliminated | why: the gap is 18–20σ of cosmic variance; LTB |δ| > 20% excluded at 4–5σ; flow corrections raise H0 [D-10, D-11, D-36] | distinguishing prediction: H0 converging to the CMB value for z ≳ 0.2 (Banik) | confidence: high
- [EXAMINER-H] **Early-universe analysis systematic (CMB/BAO):** | status: eliminated (as a sole cause) | why: Planck, ACT and SPT agree; BAO+BBN without CMB anisotropies gives 68.50 ± 0.58, still 4.6σ below the all-local mean [D-02, D-08, calc] | distinguishing prediction: a CMB-independent r_d (BBN + BAO) shifting to about 137 Mpc | confidence: high

## What would change my mind
- A ladder-free, r_d-free H0 (time delays + sirens + r_s-free BAO) at ≤ 1.5% landing at ≥ 72.5 or ≤ 69. That would collapse the partition ambiguity in F4 and decide EXAMINER-A in favour of C or B respectively.
- Independent confirmation that the Percival/Dong/Wojtak corrections are additive and accepted by SH0ES. That would move B from strained to surviving.
- A Bayesian EDE fit to ACT+SPT+DESI DR2 that reaches H0 ≥ 72 with no ladder prior and is robust to prior volume. That would lift C.
- SBF or TF being shown to share a zero-point bias with the Cepheid ladder (via the NGC 4258 anchor) would remove the main obstacle to B.

## Assumptions I relied on
- Dossier values are current. Several are 2026 preprints: TDCOSMO-2026, masers, GWTC-5, D-49, D-88, D-82. Superseded values are excluded per §7.
- Class representatives are treated as independent, except for one rough GLS on the NGC 4258 anchor (1.45%, from RE-27, not seen by the checker). Sharing among the r_s users (CMB r_d enters the inverse ladder) is ignored, which slightly overstates the r_s group's precision.
- Asymmetric errors are symmetrised as the mean of the two sides in the grouped χ²; tension() uses the facing side.
- The partition tests use one representative per class. Using H0DN (D-22) in place of SH0ES would not change the qualitative result (H0DN 73.26 ± 0.81 vs SH0ES 73.49 ± 0.93); I checked this only by inspection, not by calculation.
- The r_s-free values assume standard N_eff. They test EDE-like r_s reduction, not ΔN_eff.
