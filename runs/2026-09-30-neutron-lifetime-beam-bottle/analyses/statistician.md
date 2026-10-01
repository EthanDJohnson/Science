# Analysis: statistician (is the signal real?)
status: final

## Method applied
I rebuilt every lifetime result as numbers, keeping one value per independent dataset and dropping superseded values. I then combined the results by method class with inverse-variance means and PDG scale factors, and split the disagreement into χ² within classes and χ² between them. Tensions are two-sided, taking the side of an asymmetric error that faces the other value. Minimum Bayes factors bound the evidence against a fluctuation, and a heavy-tailed base rate sets the prior. Once a fluctuation is excluded, the explanations are ranked only by the discriminating data: J-PARC, and the SM τ_β from λ and Vud. Units are SI throughout: lifetimes in s, rates in s⁻¹; λ and branching ratios are dimensionless.

## Findings

F1. **Input set checked against the PDG encoder listing (dated 6/1/2026).**
- The current PDG UCN average uses eight storage results: 878.3 ± 0.4 s, S = 1.8, χ² = 19.7 for 7 dof, CL = 0.0031. Serebrov 18 contributes 11.7 of that χ² [new: PDG encoder listing s017, pdg.lbl.gov/encoder_listings/s017.pdf, ACCESS full-text, "878.3 ± 0.4 OUR AVERAGE ... Error includes scale factor of 1.8" and "SEREBROV 18 CNTR 11.7 ... c2 19.7 (Confidence Level = 0.0031)"].
- The listing confirms Sussex–ILL, which the dossier had not verified (D-22) [new: same, full-text, "889.2 ± 3.0 ± 3.8 BYRNE 96 CNTR Penning trap"].
- It also gives the average with the proton beam included [new: same, full-text, "If we include the one in-beam measurement with a comparable error (YUE 13), we get 878.6 ± 0.6 s, where the scale factor is now 2.2"].
- Neither J-PARC result (Hirota 2020, Fuwa 2024) is in the listing. I use the preprint value (D-23).

F2. **Correction to D-27 on supersession.** The PDG treats Musedinovic 25 as the 2018–2019 data of Gonzalez 21 plus new 2020–2022 data, and keeps Pattie 18 (2016–2017 data) as a separate result [new: same, full-text, "MUSEDINOVIC 25 result is the average value of the previously published dat a of 2018–2019 in GONZALEZ 21 with the new 2020–2022 data ... GONZALEZ 21 results are thus superseded. 2 PATTIE 18 uses a new technique"]. D-27's per-year list starts in 2018, which is consistent with this.
- I enter Pattie 18 (877.7 ± 0.7 +0.4/−0.2 s) as a separate dataset that shares the UCNτ apparatus.
- I show its systematic correlated with Musedinovic 25 (F7). Leaving Pattie 18 out changes the storage mean by only +0.06 s.

F3. **Class means.** Total error is stat ⊕ sys in quadrature, with the PDG scale factor [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-statistician_combination.py].

| Class | Mean (s) | Error (s) | χ² / dof | Notes |
|---|---|---|---|---|
| Proton-counting beam (BL1 + Sussex–ILL) | 887.97 | ± 2.04 | 0.08 / 1 | BL1 carries 82% of the weight |
| Material bottles (5) | 880.03 | ± 0.49; ± 0.70 scaled | 8.19 / 4 (p = 0.085) | S = 1.43 |
| Magnetic traps (3) | 877.82 | ± 0.27 | 0.09 / 2 | |
| All storage (8) | 878.32 | ± 0.23; ± 0.43 scaled | 24.0 / 7 (p = 0.0011) | S = 1.85 |
| J-PARC 2024 | 877.2 | +4.35/−3.98 | single result | |

My storage mean matches the PDG's 878.3 ± 0.4 s. My χ² differs from the PDG's 19.7 because I handle the asymmetric errors differently.

F4. **The beam–storage gap is real at about 4.6σ locally and 4.1–4.4σ globally.**
- The proton-counting beam against all storage gives Δ = 9.65 ± 2.08 s. That is z = 4.63 two-sided with the storage error scaled (4.70 unscaled), p₂ = 3.7×10⁻⁶. As fractions: 1.09% of τ, or a missing rate of 1.24×10⁻⁵ s⁻¹. This supersedes the placeholders in D-35.
- BL1 alone against storage gives 4.10σ. Sussex–ILL alone gives only 2.24σ.
- Look-elsewhere over the partitions one could have tried (beam/bottle, proton/rest, BL1/rest, material/magnetic, strong/weak field; 3 to 10 trials) gives a global significance of 4.40σ for 3 trials, 4.28σ for 5 and 4.13σ for 10.
- The gap has not faded. It was 8.6 s at 4.12σ in the 2018 averages (D-33) and is 9.65 s at 4.63σ now. [calc: combination, lambda_sm]

F5. **Grouped χ².** J-PARC is symmetrized to the mean of its two sides, 4.16 s.

| Partition | Within-class χ² / dof | Between-class χ² | Between z |
|---|---|---|---|
| Proton beam against storage | 24.1 / 8 | 22.1 / 1 | 4.70σ |
| Proton beam against everything else (J-PARC with storage) | 24.2 / 9 | 22.1 / 1 | 4.70σ |
| Beam (proton + electron) against storage | 29.5 / 9 | 16.8 / 1 | 4.10σ |
| Three classes: proton beam, electron beam, storage | 24.1 / 8 | 22.2 / 2 | 4.33σ |
| Four classes: proton beam, electron beam, material, magnetic | 8.4 / 7 (p = 0.30) | 38.0 / 3 | 5.55σ |

- One common value for all 11 results gives χ² = 46.3 for 10 dof (S = 2.15, p = 1.3×10⁻⁶).
- With four classes, the disagreement lies entirely between classes: every class agrees with itself. A pooled scale factor of 2.15 would spread this split over every result.
- A two-mean model that partitions proton counting against the rest fits better than beam against bottle, with total χ² 24.19 against 29.51 (Δχ² = 5.3). That is a likelihood ratio of 14 in favour of "proton counting against the rest", and it comes entirely from J-PARC.
- The partition "strong trapping field (4.6–5 T) against weak field" contains the same results as the proton partition in the current data, so these data cannot separate the two. [calc: combination]

F6. **J-PARC 2024**, with asymmetric errors and the side facing each value:
- against the proton beam, Δ = −10.77 ± 4.80 s, 2.24σ;
- against BL1 alone, 2.15σ;
- against storage, Δ = −1.12 ± 4.37 s, 0.26σ.

Its internal inconsistency is large: the four run conditions give χ² = 15.8 for 3 dof (D-23), or 19.6 for 3 dof with statistical errors alone. With the statistical error inflated by S = 2.29 the tensions become 1.81σ against the proton beam and 0.20σ against storage.

As a discriminator between "the electron rate equals the storage rate" and "the electron rate equals the proton-beam rate", J-PARC gives a likelihood ratio of 12:1 on its quoted errors, or 5:1 inflated. From even odds that is a posterior of 0.92, or 0.84 inflated. The minimum Bayes factor is 4:1, and a prior of 0.20 is needed for 50%.

More data from the same apparatus cannot help. With a systematic of 3.8 s and the proton-beam error of 2.04 s, the J-PARC 2024 setup can never separate the two poles at 3σ (exposure_to_reach = ∞). [calc: combination, lambda_sm]

F7. **Correlations.**
- Correlating the systematic parts of Serebrov 05 with Serebrov 18 (same group) and Pattie 18 with Musedinovic 25 (same apparatus) moves the storage mean from 878.321 to 878.316 s at ρ = 0.8, which is negligible.
- A stress test correlating the total errors at ρ = 0.8 gives 878.10 ± 0.22 s. The storage scale factor rises to 2.42, and the tension with the proton beam is 4.69σ.
- If BL1 and Sussex–ILL share a proton-trap method systematic at ρ = 0.8, the proton-beam mean becomes 887.64 ± 2.24 s. The tension falls from 4.63σ to 4.08σ, bounded below by BL1 alone.
- Correlations therefore move the headline by about 0.5σ at most. [calc: combination]

F8. **Size of the missing error.** To bring the gap down to 3σ, one side needs an extra systematic of 2.45 s; to 2σ, 4.35 s. For comparison, BL1 quotes 1.9 s of systematic, so its budget would have to grow about 2.3× to reach 2σ.

Alternatively, every one of the 11 errors could be inflated by the same factor: 1.57× gives 3σ and 2.35× gives 2σ. But uniform inflation would also inflate the within-class χ², which is small in the four-class split (8.4 / 7). So the disagreement is not spread evenly: it points to one class being biased. [calc: combination]

F9. **Internal splits of storage: a second anomaly, fragile.**
- Material bottles against magnetic traps: Δ = 2.22 ± 0.75 s, 2.95σ locally, about 2.41σ after a Šidák correction for about 5 post-hoc splits. The minimum Bayes factor is 20:1.
- Serebrov 18 against Musedinovic 25: 3.80σ.
- UCNτ's per-year scatter (D-27) is statistically acceptable: χ² = 6.67 for 4 dof, p = 0.155, S = 1.29. The 2020–2022 difference in D-81 is not significant once all five years are fitted.
- The material side is 5 results from 4 groups, and Serebrov 18 dominates it. [calc: combination, heavytail]

F10. **λ splits by method in the same pattern as τ.**

| Route | Inputs | λ | Within χ² / dof | SM τ_β (GS2023, Vud = 0.97361(32)) |
|---|---|---|---|---|
| β-asymmetry (A) | PERKEO III, UCNA, PERKEO II | 1.27623 ± 0.00050 | 1.51 / 2 | 878.70 ± 0.83 s |
| Proton recoil (a) | aSPECT 2024, aCORN Hassan 21 | 1.26884 ± 0.00248 | 3.58 / 1 | 887.21 ± 2.93 s |
| Proton recoil (a), aCORN swapped | aSPECT 2024, WIETFELDT 24 | 1.26752 ± 0.00247 | 0.44 / 1 | 888.74 ± 2.93 s |

- Between the two routes, χ² = 8.56 (2.93σ). With aCORN replaced by the listing's WIETFELDT 24 entry (−1.2712 ± 0.0061) [new: PDG encoder listing s017, full-text, "− 1.2712 ± 0.0061 1 WIETFELDT 24 SPEC Cold n, unpolarized"], it is 11.96 (3.46σ).
- PERKEO III against aSPECT 2024 gives 3.49σ, or 3.18σ after a look-elsewhere factor of 3.
- My reading that WIETFELDT 24 is the aCORN reanalysis is inferred, not verified.
- The pattern is that both proton-detecting routes, the lifetime and the a-coefficient, give about 888 s, and both non-proton routes give about 878 s. There are two self-consistent pairs of evidence. [calc: lambda_sm]

F11. **The SM τ_β as an arbiter depends entirely on which λ.** These use the U-01 pairing rule [calc: lambda_sm; U-01].

| λ input | τ_β (s) | Against proton beam | Against storage | Br_X = 1 − τ_storage/τ_β |
|---|---|---|---|---|
| PERKEO III | 878.50 ± 0.88 | 4.26σ | 0.18σ | 0.0002 ± 0.0011 (95% one-sided upper limit 0.0020) |
| aSPECT 2024 | 889.58 ± 3.20 | 0.42σ | 3.49σ | 0.0127 ± 0.0036 |
| PDG 2024 average (S = 2.7) | 879.65 ± 1.61 | 3.20σ | 0.80σ | 0.0015 ± 0.0019 |

- With PERKEO III, the likelihood ratio for "storage true" against "proton beam true" is 8.7×10³. The Br_X the gap needs, 0.0109, lies 9.5σ above the measured value.
- With aSPECT 2024, the likelihood ratio is 2.5×10⁻³, so it favours the proton beam. Br_X is consistent with the needed 0.0109.
- With the PDG 2024 average, the likelihood ratio is 122, and the needed Br_X lies 4.9σ above the measured value.

F12. **Base rate for disagreements between precision methods.** Bailey 2017 fitted 41 000 measurements of 3200 quantities [new: Bailey, R. Soc. Open Sci. 4, 160600 (2017), ACCESS full-text via Europe PMC, "Outliers are common, with 5 σ disagreements up to five orders of magnitude more frequent than naively expected" and "all can reasonably be described by almost-Cauchy Student's t -distributions with ν ∼2−3"].
- Under Student-t with ν = 2, 3 and 4, the gap's 4.63σ has a two-sided probability of 0.044, 0.019 and 0.010, against 3.7×10⁻⁶ for a Gaussian. [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-statistician_heavytail.py]
- So a disagreement of this size between two established methods is roughly a 1-in-25 to 1-in-100 event in the historical record of undetected errors. Bailey's examples, such as a 50σ G measurement traced to a wrong assumption about the apparatus, were resolved by finding a mistake, not new physics.
- This makes "a real, non-statistical cause" near-certain, and "an unrecognized systematic" the reference-class favourite among real causes.

## Lens-specific outputs

### Signal table

| # | Claimed signal | Local significance (two-sided) | Global significance | χ² within / between methods | Systematics | Bayes-factor bound (Sellke, max odds) | Prior needed for P > 50% | Verdict | Data needed |
|---|---|---|---|---|---|---|---|---|---|
| S1 | Proton-counting beam (887.97 ± 2.04 s) against storage (878.32 ± 0.43 s): Δ = 9.65 s, 1.09% | 4.63σ (p = 3.7×10⁻⁶); 4.10σ BL1 alone | 4.28σ (5 partitions), 4.13σ (10) | 4 classes: within 8.4/7, between 38.0/3 (5.55σ); 2 classes: within 24.1/8, between 22.1/1 | BL1 sys 1.9 s (fluence line 0.5 s, "unassociated" 1.7 s carried from 2005, D-20); storage S = 1.85; ρ = 0.8 shifts at most 0.5σ | 8.0×10³ : 1 (Gaussian bound 2.2×10⁻⁵) | 1.3×10⁻⁴ (real vs fluctuation only) | **robust** as a discrepancy; rests on one dominant apparatus (82%) | More BL1-type data can never reach 5σ (systematic floor, max 4.95σ). BL2 at < 1 s gives 4.2σ against the old proton-beam value or 8.8σ against storage |
| S2 | J-PARC 2024 sides with storage | 2.24σ from proton beam (1.81σ inflated); 0.26σ from storage | 2.24σ (pre-stated test) | its own 4 conditions: χ² 15.8/3 | sys +4.0/−3.6 s; background 4–5× the MC prediction (D-25) | 4 : 1 | 0.20 | **fragile** | LiNA at about 1 s: 8.8σ from the storage pole, 4.2σ from the proton-beam pole (7σ once BL2 shrinks the proton-beam error to about 0.9 s) |
| S3 | Material (880.03 ± 0.70 s) against magnetic (877.82 ± 0.27 s) | 2.95σ; Serebrov 18 against Musedinovic 25: 3.80σ | about 2.41σ (5 splits) | within 8.19/4 (material), 0.09/2 (magnetic) | Serebrov 18 carries 11.7 of the PDG's χ² | 20 : 1 | 0.047 | **fragile** | τSPECT (< 0.3 s) or a new material bottle at < 0.5 s |
| S4 | λ split: β-asymmetry route (1.27623(50)) against a-coefficient route (1.2688(25)) | 3.49σ (PERKEO III against aSPECT 2024); between-route 2.93–3.46σ | 3.18σ | within 1.5/2 (A), 3.6/1 or 0.4/1 (a) | aSPECT proton detection and Fierz fit (D-42) | 100 : 1 | 0.010 | **fragile–robust** (≈3σ, two methods) | Nab: σ_λ ≤ 0.0018 (0.14%) separates aSPECT from PERKEO III at 5σ; its 0.04% target (σ_λ ≈ 0.0005) would put an aSPECT-like reading about 13σ from PERKEO III |
| S5 | SM τ_β (PERKEO III) against proton beam | 4.26σ | conditional on S4 | n/a | Vud 0.58 s, K 0.19 s, λ 0.64 s | about 8.7×10³ likelihood ratio (point hypotheses) | n/a | **robust if the A route is right**, otherwise reversed | Nab a-coefficient |
| S6 | Exotic branch Br_X > 0 (bottle lifetime against SM τ_β) | 0.18σ (PERKEO III); 3.5σ (aSPECT) | n/a | n/a | as S5 | none (null favoured, A route) | n/a | **noise** on the A route; follows S4 | as S5 |
| S7 | UCNτ per-year drift (2020 against 2022) | 2.3σ pairwise | χ² 6.67/4, p = 0.155 | n/a | event definition, heated UCN (D-10) | about 1.3 : 1 (Sellke, from p = 0.155) | n/a | **noise** | UCNτ+ |

### Precision needed to settle it (Δ = 9.65 s between the poles)
- **Budget on any new result.** A total uncertainty on the difference of ≤ 3.22 s gives 3σ; ≤ 1.93 s gives 5σ.
- **Against the storage pole** (± 0.43 s), a new result needs σ ≤ 3.19 s for 3σ and ≤ 1.88 s for 5σ.
- **Against the old proton-beam pole** (± 2.04 s), it needs σ ≤ 2.49 s for 3σ. 5σ is **impossible** until the proton-beam pole itself shrinks.
- **Planned experiments.** Separation between the two poles, against the storage pole / against the proton-beam pole:

| Experiment | Target σ | Against storage pole | Against proton-beam pole |
|---|---|---|---|
| BL2 / LiNA | 1 s | 8.8σ | 4.2σ |
| BL3 | 0.3 s | 18σ | 4.7σ |
| UCNProBe | 1.5 s | 6.2σ | 3.8σ |
| UCNProBe | 2 s | 4.7σ | 3.4σ |

  The targets come from D-100 to D-106; several are search-summary or preliminary.
- **SM route on its own.** A 5σ separation needs σ(τ_β) ≤ 1.93 s, so σ_λ ≤ 0.00156 (0.12%); a 3σ separation needs σ_λ ≤ 0.00274. PERKEO III already meets this. What decides is whether the a-coefficient route agrees, which is Nab's job.

### Discriminating power of existing data between explanations (not fluctuation vs real)

| Data | "Electron and total rates equal storage" (A, D, F) against "equal proton beam" (B, C) | Condition |
|---|---|---|
| J-PARC 2024 | 12 : 1 (5 : 1 inflated) | none |
| SM τ_β, PERKEO III | 8.7×10³ : 1 | A route correct |
| SM τ_β, aSPECT 2024 | 1 : 400 | a route correct |

A (a proton-counting systematic) and D (strong-field n → n′) predict identical lifetime patterns, so no lifetime statistic separates them. Only direct n → n′ searches do (D-89).

## Calculations
- `runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-statistician_combination.py` (log beside it) computes:
  - the class means and scale factors;
  - the tensions, including J-PARC with asymmetric and inflated errors;
  - grouped χ² for five partitions;
  - the partition likelihood ratio;
  - GLS with ρ = 0 and 0.8;
  - the extra systematic needed, look-elsewhere, Bayes bounds and the precision needed.

  Key results: proton beam 887.97 ± 2.04 s; storage 878.32 ± 0.43 s (S = 1.85); Δ = 9.65 ± 2.08 s, 4.63σ; four-class between χ² 38.0/3; Δχ² = 5.3 (proton/rest over beam/bottle); maximum odds against a fluctuation 7969:1.
- `runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-statistician_lambda_sm.py` computes:
  - the λ grouped χ² by route;
  - τ_β for each route and input, through `neutron_beta_decay.py` with GS2023 and Vud = 0.97361(32);
  - Br_X;
  - the UCNτ per-year χ²;
  - gap stability from 2018 to 2026;
  - the J-PARC likelihood ratio;
  - the λ precision needed.

  Key results: τ_β(A route) 878.70 ± 0.83 s; τ_β(PERKEO III) 878.50 ± 0.88 s; τ_β(aSPECT 2024) 889.58 ± 3.20 s; Br_X(PERKEO III) = 0.0002 ± 0.0011.
- `runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-statistician_heavytail.py` computes Student-t tail probabilities (Bailey's base rate), the Šidák correction for the internal splits, and the Bayes bounds for S2 to S4.

## Candidate answers (at least 3; the null and a reframe count)
- [STATISTICIAN-A] **A proton-counting-beam systematic** makes the beams read about 9.6 s (1.09%) long. Its sub-hypotheses are the absolute efficiency of the ⁶Li fluence monitor, proton loss in the trap (charge exchange, end regions) and proton detection efficiency.
  - status: surviving.
  - Why:
    - It is the best-fitting two-mean partition (χ² 24.2 against 29.5 for beam/bottle; likelihood ratio 14, all from J-PARC).
    - J-PARC agrees with storage at 0.26σ.
    - The β-asymmetry SM τ_β agrees with storage at 0.18σ and sits 4.26σ from the beam.
    - It needs a shift about 5× BL1's quoted 1.9 s systematic. No named effect of that size has been identified; Caylor measured about 0.3% for H₂ (D-17).
  - Test: BL2 (< 1 s) reading about 878 s, together with LiNA at about 1 s reading about 878 s.
  - confidence: medium.
- [STATISTICIAN-B] **A common bottle systematic**: an unidentified loss of about 1.24×10⁻⁵ s⁻¹ shared by material and magnetic traps.
  - status: strained.
  - Why:
    - Two non-storage measures agree with storage: J-PARC (likelihood ratio 12:1 against B) and the A-route SM τ_β (likelihood ratio 8.7×10³:1 against B, conditional on λ).
    - The two trap types differ by 2.2 s in the opposite sense to a shared shortening, and their mechanisms differ.
    - It survives only if the aSPECT λ is right (τ_β = 889.6 ± 3.2 s).
  - Test: UCNProBe in-bottle β counting at 1–2 s reading about 888 s; Nab a-coefficient.
  - confidence: low.
- [STATISTICIAN-C] **Dark decay**: a branch of about 1.1% with neither proton nor electron (the invisible χφ or χχχ channels are the only open variants).
  - status: strained.
  - Why:
    - It predicts J-PARC equal to the proton-beam value; the data disfavour this by 12:1 (2.24σ, fragile).
    - On the A route, Br_X = 0.0002 ± 0.0011, with 0.0109 excluded at 9.5σ. On the PDG λ average it is excluded at 4.9σ.
    - It is allowed only on the aSPECT route (Br_X = 0.0127 ± 0.0036).
  - Test: LiNA at about 1 s (predicts about 888 s); Nab a (predicts λ ≈ 1.268).
  - confidence: low.
- [STATISTICIAN-D] **Strong-field n → n′ conversion** in the 4.6–5 T proton trap, lengthening the beam value.
  - status: strained.
  - Why: statistically it is indistinguishable from A, since it predicts the same pattern of J-PARC equal to storage and SM equal to storage. It is excluded by the SNS regeneration limit for Δm > 10 neV (D-62, D-89), not by any lifetime statistic.
  - Test: BL2 or BL3 run at a different trap field (a field-dependent shift); any regeneration signal.
  - confidence: low.
- [STATISTICIAN-E] **Null**: no single dominant cause, only a statistical fluctuation, or several modestly underestimated uncertainties spread across experiments.
  - status: strained.
  - Why:
    - A pure fluctuation needs p₂ = 3.7×10⁻⁶ (4.1–4.4σ global). The maximum odds against it are 8000:1, and heavy-tailed history gives it about 10⁻³ of the weight of an unrecognized error (density ratio 400–1000), so the fluctuation reading is effectively eliminated.
    - Diffuse inflation needs every error inflated by 2.35× to reach 2σ, yet the four-class within-class χ² is only 8.4/7. The disagreement sits between classes, not spread over them.
  - Test: BL2 and LiNA both landing between the poles (about 883 s) would revive it.
  - confidence: low.
- [STATISTICIAN-F] **Reframe: "BL1 against everything", or more broadly proton detection against the rest.**
  - status: surviving.
  - Why:
    - The beam side is essentially one apparatus: BL1 carries 82% of the weight, and Sussex–ILL on its own is only 2.24σ from storage.
    - A "BL1 alone" partition fits slightly worse than the proton-counting one (χ² 29.2 against 24.2), because Sussex–ILL agrees with BL1. That difference is under 2.3σ, so "BL1-specific" and "proton-counting-generic" cannot yet be told apart.
    - The same proton/non-proton split appears in λ (aSPECT and aCORN against the β-asymmetry results, 2.9–3.5σ), a pattern with only two a-route datasets.
    - A second, weaker anomaly exists inside the storage class (material against magnetic, 2.4σ global).
  - Test: BL2, an independent apparatus with the same method, at < 1 s. Reading about 888 s makes it method-generic (A, C or D); reading about 878 s makes it BL1-specific.
  - confidence: medium.

## What would change my mind
- **LiNA or another electron-counting beam at about 1 s reading about 888 s.** This would flip the J-PARC likelihood ratio and revive B and C.
- **Nab measuring a consistent with aSPECT** (λ ≈ 1.268 at ≤ 0.1%). The SM arbiter would then favour the beam, and B or C would lead.
- **BL2 reading about 878 s.** This would collapse A into F (a BL1-specific error).
- **A published itemization of BL1's 1.7 s "unassociated" line** showing a missed term of several seconds. This would turn A from a statistical inference into an identified mechanism.
- **A J-PARC journal version with the four-condition χ² resolved** and errors of about 2 s, which would firm up S2.

## Assumptions I relied on
- Stat and sys errors add in quadrature. Asymmetric errors are symmetrized as the mean of the two sides in weighted means and χ², and taken from the side facing the other value in tensions.
- Sussex–ILL's value comes from the PDG listing, not the original paper. Ezhov 18 rests on a search summary (D-30). Arzumanov 15's stat/sys split is unknown, so I used a total of 1.2 s.
- Pattie 18 is independent data (per the PDG), contrary to D-27.
- The J-PARC preprint value is final. The columns of its per-condition table beyond stat are unlabelled, so my inflated-error variant (S = 2.29 on stat) is a stress test.
- The SM τ_β uses the U-01 pairing (GS2023, Vud = 0.97361(32)), and its errors treat Vud and RC as independent.
- The WIETFELDT 24 λ entry is read from the PDG listing, and its identity as aCORN is inferred.
- Bailey's ν = 2–4 Student-t base rate applies to this pair of methods.
- The likelihood ratios are point-hypothesis ratios using each pole's measured value, not marginalized over model parameters.
- The planned-experiment precisions come from dossier items D-100 to D-107, several of them search-summary or preliminary.
