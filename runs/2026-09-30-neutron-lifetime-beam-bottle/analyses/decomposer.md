# Analysis: decomposer (methodical doubt and decomposition)
status: final

## Method applied
The question is rewritten as a tree of sub-questions whose leaves can be settled by a calculation, a measurement or a cited result. Every premise is entered in an assumption ledger as measured, derived, assumed or unknown. The load-bearing assumption is named with its test, and the leaves are sorted into settled and open.

## Findings

F1. **The proton-counting side is one apparatus.** Combining BL1 887.70 ± 2.25 s [D-20] with the unverified Sussex–ILL lead 889.2 ± 4.84 s [D-22] gives 887.97 ± 2.04 s, χ² 0.08/1. BL1 carries 85% of the weight. The class mean is 887.7 ± 2.25 s with BL1 alone. [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-decomposer_tree.py]

F2. **The gap is real at about 4–5σ, whichever way it is partitioned.** BL1 against UCNτ (877.82 s, D-27) gives Δ = 9.88 ± 2.27 s (4.36σ). BL1+SIL against UCNτ gives 4.93σ, and against all seven storage results with S = 1.97 it gives 4.57σ. The fractional gap is 0.0111–0.0114, a missing rate of 1.27–1.30×10⁻⁵ s⁻¹ (SI). [calc: lens-decomposer_tree.py]

F3. **The storage results are not internally consistent.** The 7 storage results give χ² = 23.3/6 (p = 7×10⁻⁴, S = 1.97). Material bottles alone give 880.03 ± 0.70 s (scaled, S = 1.43), and magnetic traps give 877.83 ± 0.28 s. The material−magnetic difference is 2.20 s (2.9σ), which reproduces the ORNL "second anomaly" [D-32, D-73]. [calc: lens-decomposer_tree.py]

F4. **Partition test [brief premise 2].** Pooled χ² = 45.3/9 over 10 results. The between-group χ² for each partition:
- "beam (incl. J-PARC) vs bottle": 16.5/1 (4.06σ), within 28.8/8;
- "proton-counting vs rest": 21.8/1 (4.67σ), within 23.5/8;
- "BL1 vs rest": 16.9/1;
- the 4-class split (proton / electron / material / magnetic): 36.9/3 (5.46σ), with within-class χ² only 8.3/6 (p = 0.22).

"Proton-counting vs rest" beats "beam vs bottle" by Δχ² = 5.3. The 4-class split is the only one that leaves the classes internally consistent. So the data carry two anomalies: proton-beam vs rest, and material vs magnetic. "Strong field (≥4.6 T) vs weak" contains exactly the same sets as "proton-counting vs rest", so present data cannot separate a proton-counting systematic from a strong-field effect. [calc: lens-decomposer_tree.py]

F5. **J-PARC discriminates only weakly.** J-PARC 2024 877.2 +4.35/−3.98 s (total) [D-23]:
- against BL1: 2.15σ; against BL1+SIL: 2.24σ;
- against UCNτ: 0.14σ.

With the stat error scaled by its own internal S = √(15.8/3) = 2.29 [D-23, D-24], the tension with BL1 falls to 1.74σ. Its likelihood ratio for "J-PARC ≈ storage" over "J-PARC ≈ proton beam" is 18 with the quoted errors and 5.8 with scaled errors.

J-PARC is also internally split. Its three mutually consistent conditions average 869.6 ± 2.5 (stat) s, and the fourth reads 884.8 ± 2.4 s [D-24]. The printed central value therefore depends on how an unexplained χ² is handled. [calc: lens-decomposer_tree.py]

F6. **The required systematics are 5–50× the stated budgets.**
- *Proton beam:* the needed shift is 1.11% (9.9 s). That is 5.2× BL1's total systematic (1.9 s), 5.8× the 1.7 s "unassociated with fluence" line, and 20× the 0.5 s fluence-calibration uncertainty [D-20].
- *Bottles:* the needed unidentified loss is 1.27×10⁻⁵ s⁻¹ (time constant 7.9×10⁴ s ≈ 0.91 d). That is 49× UCNτ's ~0.2 s systematic in rate terms (2.6×10⁻⁷ s⁻¹) and 16× Gravitrap's 0.6 s. The same loss would also have to act on wall-free magnetic traps and on material bottles, which already differ by 2.2 s in the direction of *fewer* losses in material bottles [D-27, D-28]. [calc: lens-decomposer_tree.py]

F7. **Two internally consistent SM "worlds" exist (central finding of the decomposition).** These use GS2023 radiative corrections with the paired superallowed Vud = 0.97361(32), following [U-01].
- *World A:* the A-coefficient λ (PERKEO III, UCNA, PERKEO II combined: 1.27623 ± 0.00050, χ² 1.51/2) with the storage τ. It gives Vud 0.97410(37), 1.0σ from superallowed, and a first-row sum 0.99919(81).
- *World B:* the a-coefficient λ (aSPECT 2024: 1.2668(27)) with the beam τ. It gives Vud 0.97464(212), 0.5σ from superallowed, and a row sum 1.0002(42).
- *Mixed pairings fail:* A-λ with beam τ gives Vud 3.8σ low and a row sum 4.6σ low; aSPECT-λ with storage τ gives Vud 3.7σ high.

So the SM/CKM arbitration **does not fall to the bottle side independently**: it inherits the unresolved 3.4σ split between A-route and a-route λ (Δλ = 0.0094 ↔ 10.8 s in τ_β, almost exactly the 9.9 s lifetime gap). [calc: lens-decomposer_tree.py]; [D-42, D-74]

F8. **The two proton-sensitive measurements side together.** The a-coefficient (aSPECT, from the proton recoil spectrum) and BL1 (proton counting) are the two experiments that detect decay protons, and both sit on the "888 s" side. All electron-asymmetry, electron-counting and storage results sit on the "878 s" side. The one exception is aCORN (a from electron–proton coincidences), which gives τ_β 874.9 ± 7.1 s, bottle-like but too imprecise to count. aSPECT measures a spectral shape and BL1 an absolute rate, so no single known effect links them; the coincidence is a pattern, not a mechanism. [calc: lens-decomposer_tree.py]; [D-41, D-42, D-50/U-01]

F9. **The exotic branch bound depends on which λ is used.** Br_X = 1 − τ_UCNτ/τ_β:
- PERKEO III λ: 0.08 ± 0.11%, 95% upper 0.25%;
- PDG 2024 λ: 0.21 ± 0.19%, upper 0.51%;
- aSPECT 2024 λ: 1.32 ± 0.36%, which *favours* a ≈1.1% missing branch at 3.7σ.

The ~1.1% dark branch is excluded at >7σ on the A route and preferred on the a route [D-82, D-76]. [calc: lens-decomposer_tree.py]

F10. **λ precision is no longer the bottleneck; λ accuracy is.** For the SM prediction alone to split 877.8 s from 887.7 s at 3σ (5σ) needs σ_λ ≤ 0.0028 (0.0016), i.e. 0.22% (0.13%) relative, with the Vud+RC part fixed at 0.61 s. PERKEO III already gives 0.00056. What the λ side needs is an a-coefficient result with σ_λ well below the 0.0094 A-vs-a split: Nab's Δλ/|λ| ≈ 0.04% goal [D-107] would test aSPECT at about 18σ. [calc: lens-decomposer_tree.py]

F11. **The λ split may instead be read as a Fierz term, which pushes the SM prediction further toward the beam.** The aSPECT reanalysis authors fit PERKEO III and aSPECT together, allowing a Fierz term. [new: Beck et al., "Reanalysis of the β−ν̄e angular correlation measurement from the aSPECT experiment with new constraints on Fierz interference", PRL 132, 102501 (2024), accepted manuscript via OSTI https://www.osti.gov/pages/servlets/purl/2583794, full-text, "The resulting values for ( b,λ ) at 68% CL in combining (c) the independent datasets of PERKEO III and aSPECT are b(c) =−0.0181± 0.0065 λ(c) =−1.2724± 0.0013"]. They also state: [same source, full-text, "For the SM analysis (b≡ 0) of the two measurements, the λ values of PERKEO III and aSPECT disagree by 3.4 standard deviations"]. My calc reproduces the 3.4σ (F7).

With Γ ∝ (1 + 3λ²)(1 + b⟨m_e/E⟩), where my phase-space average is ⟨m_e/E⟩ = 0.6555 (relativistic Fermi function), this (b, λ) gives τ_β = 893.7 ± 4.2 s: 1.3σ above BL1 and 3.8σ above UCNτ. A Fierz term changes Γ_total for every method alike, so it cannot itself split beam from bottle. It only removes the SM's support for the bottle side. The same source says b(c) "is in tension with constraints from" other data (sentence truncated in the extraction), and superallowed b_F ≤ 0.0033 [D-66] constrains only the scalar part. [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-decomposer_fierz.py]

F12. **The SM arbitration (brief premise 6) is conditional, not independent.** Of the three λ readings:
- the A route favours storage (τ_β 878.7 ± 0.8 s, 3.75σ from BL1);
- the a route favours the beam (889.6 ± 3.2 s, 3.7σ from UCNτ);
- the Fierz fit favours the beam more strongly (893.7 ± 4.2 s).

The A route rests on three mutually consistent experiments (PERKEO II, PERKEO III, UCNA) with different detectors. The a route rests on one (aSPECT); aCORN, the other a measurement, goes the other way at low weight. So the SM leans toward the bottles by weight of evidence, but not decisively: the premise "gA and Vud arbitrate" carries the same one-experiment fragility as the proton beam side. [calc: lens-decomposer_tree.py, lens-decomposer_fierz.py]; [D-41, D-42]

F13. **The gap as a >3σ fact rests on BL1 alone.**
- Leave BL1 out and Sussex–ILL against UCNτ is 2.35σ (2.22σ against all storage).
- Leave UCNτ out and BL1 against the other storage results (879.92 ± 0.64 s, S = 1.34) is 3.33σ. Against Gravitrap alone it is 2.55σ.

Two effects each reach only part of the 9.9 s needed:
- the quoted ~0.3% H₂ charge-exchange loss [D-17] is 2.7 s, 27% of the gap;
- a 100% error in either of BL1's two largest corrections (−5.3 s trap nonlinearity, +5.4 s ⁶Li absorption [D-21]) is 54% of the gap.

So no single named proton-beam effect reaches 9.9 s at its quoted size. It would take a named effect underestimated by 2–4×, or two effects acting in the same direction. [calc: lens-decomposer_tree.py]

F14. **No independent proton-beam value has been published.** BL2 has published a charge-exchange study (Dec 2025) but no lifetime [new: WebSearch on "NIST BL2 neutron lifetime beam result 2026", search-summary, SUMMARY "Recent results using the BL2 experimental apparatus at NIST were published on December 12, 2025 ... found that the result of the beam neutron lifetime performed at NIST is unlikely to have been significantly affected by charge exchange with molecular hydrogen."]. This matches [D-17, D-100]. The proton-counting class therefore still has one modern dataset (BL1, 2005 data).

F15. **The candidates fall into two groups by what they need λ to be.** Every candidate in which the proton-counting beam measures the true Γ(n → p e ν̄) needs the SM prediction τ_β ≈ 888 s. That group is: an unidentified bottle loss, dark decay (any channel), Tan's bottle-side n → n′ variant, and Veselský's X⁺ channel. For them, λ must be the a-route value 1.2668 (or the Fierz fit), and the three A-route experiments must share a ≈0.7% error in λ (F7, F12).

Only two candidates keep τ_β ≈ 878 s and need the beam to read *long*: a proton-counting systematic, and Berezhiani's strong-field n → n′. Hence:
- a precise a-coefficient λ (Nab) splits the slate into these two groups;
- J-PARC/LiNA and UCNProBe split it the same way, except for Veselský, where every decay yields an electron.

[calc: lens-decomposer_tree.py]; [D-79, D-95, D-96]

## Lens-specific outputs

### Sub-question tree
Q0. What is the dominant cause of the ~10 s (1.1%) gap between proton-counting beam and storage lifetimes, with what credence, and what measurement decides it?

- **Q1. Is there a gap to explain?**
  - Q1a. Combined values and tension. **Settled:** 4.4–4.9σ (F2).
  - Q1b. Does it survive leaving out single experiments? **Settled, negatively:** without BL1 it is 2.35σ (F13). The >3σ gap is "BL1 vs the rest".
  - Q1c. Are the storage results themselves consistent? **Settled:** no. χ² 23.3/6; material vs magnetic 2.9σ (F3).
  - Q1d. Look-elsewhere and heavy tails. Statistician's leaf, not computed here; open to me.
- **Q2. Which partition carries the tension?**
  - Q2a. Beam vs bottle, or proton-counting vs rest? **Settled:** proton-counting vs rest fits better, Δχ² = 5.3; 4 classes leave within-class χ² 8.3/6 (F4).
  - Q2b. Proton-counting vs strong field? **Open:** the two partitions contain exactly the same sets. It needs a proton beam at varied trap field, or an electron-counting beam in a ≥4.6 T field.
- **Q3. Do beam and bottle measure the same quantity in the SM?** **Settled:** yes. Bound-state and radiative branches are ≤4×10⁻⁶ or counted by both [D-04, D-06].
- **Q4. Can a systematic of the required size hide in a published budget?**
  - Q4a. Proton beam: 9.9 s = 5.2× sys, 20× fluence unc. (F6). Named effects reach 27–54% each (F13). **Open:** BL2/BL3 [D-100, D-101].
    - Q4a-i. Fluence (⁶Li deposit, α+t efficiency) — needs 20× its uncertainty.
    - Q4a-ii. Trap end/nonlinearity model — correction −5.3 s.
    - Q4a-iii. Proton loss by charge exchange / residual gas — ~0.3% ≈ 2.7 s, large uncertainty [D-17, D-72].
    - Q4a-iv. Proton detection / backscatter / dead layer — 0.4 s quoted.
  - Q4b. Bottles: a common loss of 1.27×10⁻⁵ s⁻¹ (τ ≈ 0.9 d), 16–49× the budgets, identical in material and wall-free traps (F6). **Mostly settled against;** UCNProBe would close it [D-106].
  - Q4c. J-PARC: internal χ²/dof = 15.8/3 unexplained [D-24, D-71]. **Open.**
- **Q5. Is any new physics viable now?**
  - Q5a. Visible dark channels (χγ in the DM window; χe⁺e⁻ above 32 keV). **Settled:** excluded [D-85, D-86].
  - Q5b. Invisible dark channels (χφ, χχχ). Only λ and neutron stars constrain them; the λ constraint is **conditional on Q6** (F9), and the neutron-star constraint is model-dependent [D-88].
  - Q5c. Strong-field n → n′. **Settled against** for Δm > 10 neV [D-89]. The weak-field anomaly regions are excluded [D-90].
  - Q5d. J-PARC against the "beam is true" group: 1.7–2.2σ, likelihood ratio 6–18 (F5). **Partly settled;** it depends on Q4c.
- **Q6. Does the SM (λ, Vud, CKM) arbitrate?**
  - Q6a. Radiative-correction uncertainty. **Settled:** 10⁻⁴, and ΔR^V cancels when paired [D-02, U-01].
  - Q6b. Which λ? **Open:** A route vs a route at 3.4σ; the Fierz fit (F7, F11, F12). This leaf decides the arbitration.
  - Q6c. The Cabibbo anomaly. Both self-consistent worlds (A and B) fit superallowed Vud; the mixed pairings fail at 3.7σ (F7). The CKM deficit cannot pick a side by itself.
- **Q7. Which measurement decides?** It follows from Q2b, Q4a, Q4c and Q6b; see the discrimination table below.

### Assumption ledger
| # | Premise | Class | Basis / derived from | If it fails |
|---|---|---|---|---|
| L1 | BL1's 887.7 ± 2.3 s is accurate to its budget | measured (one apparatus, one 2005 dataset, re-analysed 2013) | D-07, D-20, D-21 | The >3σ gap dissolves (F13) |
| L2 | Sussex–ILL 889.2 s is as quoted | unknown (lead, not opened) | D-22 | Little: it carries 15% of the proton-beam weight |
| L3 | UCNτ 877.82 s is accurate | measured (blinded, 4 analyses) | D-10, D-27; per-year spread 2.3σ [D-81] | Gap shrinks to 3.3σ (F13) |
| L4 | No loss is common to all storage traps | assumed; partly tested | material vs magnetic differ in the "wrong" direction (F3, F6) | Candidate B becomes viable |
| L5 | J-PARC 877.2 s is reliable | measured, preprint, internal χ² 15.8/3 unexplained | D-23–D-25, D-71 | The only non-proton beam point is lost; Q5d is void |
| L6 | Beam and bottle measure the same Γ in the SM | derived (SM branches) | D-04, D-06 | The question's frame changes (no sign that it fails) |
| L7 | Master formula and RC good to 10⁻⁴ | derived | D-01–D-03, U-01 | None at the 1% scale |
| L8 | A-route λ (PERKEO II/III, UCNA) is the true λ | measured by 3 experiments | D-40, D-41; χ² 2.14/2 | The SM prediction flips to about 889 s; bottle-short candidates revive (F7, F9) |
| L9 | No Fierz term (b = 0) | assumed (SM) | the combined fit suggests b = −0.018 at 2.8σ (F11) | τ_β ≈ 894 s; the SM favours the beam |
| L10 | Superallowed Vud (nuclear δNS, δC) is right | derived | D-43, D-47 | It shifts both worlds; not decisive (F7) |
| L11 | Vud paired with its own ΔR^V | derived | U-01 | It would bias τ_β by +0.9 s (small) |
| L12 | Dark decay invisible to bottles and J-PARC | derived per channel | D-84–D-87 | Some variants would move J-PARC or UCNτ |
| L13 | The neutron-star bound applies to dark decay | assumed (EOS, no self-repulsion) | D-77, D-88 | Dark decay escapes via its variants; it is not a decider |
| L14 | The Berezhiani model's field profile and Landau–Zener treatment | model-derived | D-89 | Some variant might evade SNS (not established) |
| L15 | Only proton traps have ≥4.6 T fields | measured | D-20, D-09, D-102 | — (this is why Q2b is open) |
| L16 | Gaussian errors, no heavy tails | assumed | — | Tension falls; the null gains |
| L17 | "878 s" is one number | assumed by the framing | contradicted at 2.9σ (F3) | A second anomaly must be carried |
| L18 | A single dominant cause exists | assumed by the framing | — | The null |
| L19 | Magnetic traps: marginal trapping and depolarisation controlled | measured in situ (UCNτ dagger), no external critique | D-10, gap in §6 | Magnetic traps read short; this could fold into B |

### Load-bearing assumption
**L1: BL1's value is accurate to its stated 2.3 s.** Every >3σ statement of the anomaly depends on this one apparatus and its 2005 data. Without it the gap is 2.35σ (F13), and every "the beam is the true β rate" candidate loses its only evidence. What tests it:
- an independent proton-counting dataset with re-measured fluence and trap systematics: BL2 at <1 s [D-100], BL3 at 0.3 s [D-101];
- non-proton absolute-rate measurements at ~1–2 s: LiNA ~1 s [D-102], UCNProBe 1–2 s [D-106].

The second load-bearing premise is **L8, the A-route λ**, and it decides which side the SM favours. A 3.4σ split rests on a single a-route experiment, and a coincidence makes it matter: the split maps to 10.8 s in τ_β, the same size as the lifetime gap. What tests it: Nab a at Δλ/|λ| ≈ 0.04% [D-107], which would resolve 0.0094 at about 18σ (F10).

### Settled vs open
- **Settled by the dossier plus my calculations:**
  - Q1a–c: the gap is 4.4–4.9σ, BL1-dependent, and the storage results are internally split;
  - Q2a: the partition analysis;
  - Q3: both methods measure the same quantity in the SM;
  - Q4b: largely against a common bottle loss;
  - Q5a, Q5c: visible dark channels and strong-field n → n′ are excluded;
  - Q6a: the radiative corrections;
  - Q6c: the CKM deficit is not decisive.
- **Open:**
  - Q1d: look-elsewhere and heavy tails (statistician);
  - Q2b: proton counting vs strong field;
  - Q4a: which proton-beam effect, and whether any reaches 9.9 s;
  - Q4c: J-PARC's internal χ²;
  - Q5b: invisible dark channels, which depend on Q6b;
  - Q6b: which λ.

### Discrimination table (predictions by candidate; values in s)
| Candidate | BL2/BL3 (proton beam) | LiNA / J-PARC (e-count) | UCNProBe absolute β rate | Material vs magnetic | Nab a → λ, τ_β |
|---|---|---|---|---|---|
| A proton-beam systematic | ≈878 once the effect is found; may show a trap/gas dependence | ≈878 | ≈878 | may differ (separate issue) | A-route, ≈879 |
| B common bottle loss | ≈888 | ≈888 | ≈888 | differ (loss depends on trap) | a-route, ≈889 |
| C dark decay (invisible) | ≈888 | ≈888 | ≈888 (β rate) | equal | a-route or Fierz, ≈889–894 |
| D n → n′ strong field | ≈888 (field-dependent) | ≈878 | ≈878 | equal | A-route, ≈879 |
| E null (fluctuation + underestimates) | anywhere in 878–888, no trend | 878–888 | 878–888 | no pattern | either |
| F reframe: BL1-specific plus separate material-bottle offset | BL2 ≈ 878 with BL2 ≠ BL1 | ≈878 | ≈878 | material ≈ +2 s, older bottles | A-route |
| G Veselský X⁺ (speculative) | ≈888 | ≈878 | ≈878 | equal | a-route, ≈888 |

## Calculations
- `runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-decomposer_tree.py` (log beside it) computes the following, in SI units with λ and Vud dimensionless:
  - class means: proton beam 887.97 ± 2.04 s; magnetic 877.83 ± 0.28 s; material 880.03 ± 0.70 s (S = 1.43); all storage 878.38 ± 0.49 s (S = 1.97);
  - partition χ²: pooled 45.3/9; between groups for proton vs rest 21.8/1 and for beam vs bottle 16.5/1; 4-class within 8.3/6;
  - tensions: BL1–UCNτ 4.36σ; J-PARC–BL1 2.15σ (1.74σ with S = 2.29);
  - required sizes: 1.11%, 5.2× BL1 sys; 1.27×10⁻⁵ s⁻¹, 49× UCNτ;
  - SM τ_β by λ: PERKEO III 878.50 ± 0.88 s; aSPECT 2024 889.58 ± 3.20 s;
  - worlds A and B: Vud 0.97410(37) and 0.97464(212); mixed pairings off by 3.7–3.8σ;
  - Br_X by λ: 0.08 ± 0.11%, 0.21 ± 0.19%, 1.32 ± 0.36%;
  - λ precision for 3σ/5σ: 0.0028/0.0016;
  - leave-one-out: 2.35σ without BL1, 3.33σ without UCNτ.
- `runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-decomposer_fierz.py` (log beside it) computes:
  - ⟨m_e/E⟩ = 0.6555 (relativistic Fermi), 0.6542 (no Coulomb);
  - τ_β with the Beck 2024 combined (b, λ): 893.70 ± 4.18 s;
  - A-route τ_β 878.70 ± 0.83 s.

## Candidate answers (at least 3; the null and a reframe count)
- [DECOMPOSER-A] **An unidentified proton-counting-beam systematic in BL1** makes it read ~10 s long; the beam value is not the true β rate. Sub-hypotheses, in the order my decomposition leaves them:
  - (i) proton loss in the trap by charge exchange with residual gas: ~0.3% quoted, large uncertainty, needs ~4×;
  - (ii) an error in the trap-nonlinearity or end-region model (−5.3 s correction);
  - (iii) the absolute fluence/⁶Li deposit efficiency, which needs 20× its uncertainty and is least likely;
  - (iv) proton detection, backscatter or dead layer.

  | status: surviving | why: it is the partition the data prefer (F4), it matches J-PARC (F5) and the A-route SM prediction (F7), and it needs no new physics. Its weakest link: no named effect reaches 9.9 s at its quoted size (F13). | distinguishing test: BL2/BL3 or LiNA/UCNProBe land at 878 ± 1 s, and Nab gives the A-route λ; an in-situ gas-pressure or trap-length dependence in BL2 would name the effect. | confidence: medium
- [DECOMPOSER-B] **An unidentified loss common to all storage traps** (~1.27×10⁻⁵ s⁻¹, a time constant of ~0.9 d) shortens every bottle; the beam is right. Sub-hypotheses: marginally trapped UCN or depolarisation in magnetic traps; energy-dependent wall losses in material bottles.

  | status: strained | why: it needs 16–49× the published budgets; the loss must be the same in wall-free and wall traps, yet they differ by 2.2 s in the opposite sense; J-PARC disfavours it (likelihood ratio 6–18); and it needs the a-route λ with three A-route experiments wrong (F6, F15). | distinguishing test: UCNProBe's absolute in-bottle β rate reads 888 s while its storage time reads 878 s; LiNA reads 888 s. | confidence: low
- [DECOMPOSER-C] **SPECULATIVE dark decay (~1.1% proton-less branch)** in an invisible channel (χφ, χχχ, χA′), or χe⁺e⁻ with E_ee < 32 keV.

  | status: strained | why: the visible channels are excluded [D-85, D-86]; on the A route the branch is excluded at >7σ (Br_X < 0.25% at 95% CL); only the a route or the Fierz fit allow it (F9, F11); J-PARC disfavours it at ~2σ; it needs a neutron-star escape [D-88]. | distinguishing test: LiNA or UCNProBe at ~1 s read 888 s; Nab gives λ ≈ 1.267; all trap types agree once the material offset is resolved. | confidence: low
- [DECOMPOSER-D] **SPECULATIVE n → n′ conversion in the strong proton-trap field** (Berezhiani) makes the beam read long.

  | status: eliminated (for Δm > 10 neV) | why: the SNS regeneration search at 6.6 T gives p < 2.5×10⁻⁸ [D-89]; Tan's bottle-side variant relies on the excluded mechanism, and PSI closes the weak-field anomaly regions [D-90, D-96]. | distinguishing test: a proton-beam lifetime that depends on the trap field (BL3 at varied B); this is the only test of Q2b. | confidence: medium (closure of every field-profile variant is not established)
- [DECOMPOSER-E] **Null: no single dominant cause.** A fluctuation plus modestly underestimated uncertainties spread over BL1, the material bottles and J-PARC.

  | status: strained | why: the disagreement is structured by class (between-class χ² 36.9/3, 5.5σ; within-class 8.3/6), not scattered, and a 4.4σ BL1 fluctuation has p ≈ 10⁻⁵ before look-elsewhere. It is not eliminated: without BL1 everything is ≤2.4σ (F13), and J-PARC's and UCNτ's internal scatter show that errors are underestimated at the 2σ level. | distinguishing test: BL2 lands between 878 and 888 s with no identifiable effect, and the class means converge slowly without a named correction. | confidence: low-medium
- [DECOMPOSER-F] **Reframe: the anomaly is "BL1 against everything", plus a separate ~2.9σ material-vs-magnetic offset.** "Beam vs bottle" is the wrong partition: J-PARC is a beam that agrees with bottles, and "878 s" hides a storage split. Under this reading the question "which new physics" is unmotivated until a second proton-counting dataset exists.

  | status: surviving (compatible with A; it restates what the evidence is, not the mechanism) | why: F4, F13; proton vs rest beats beam vs bottle by Δχ² 5.3; the 4-class split is the only internally consistent one. | distinguishing test: BL2 differs from BL1, and new material bottles (Gravitrap upgrade) converge on 878 s. | confidence: medium
- [DECOMPOSER-G] **Reframe: "proton-detecting experiments vs the rest".** Both measurements that detect decay protons (BL1 counts, the aSPECT recoil spectrum) sit at the 888 s side, and all electron- and UCN-based ones at 878 s.

  | status: strained | why: no single known mechanism links an absolute proton count with a spectral shape, and aCORN (proton–electron coincidence) goes the other way at low weight (F8). | distinguishing test: Nab (which also detects protons, in a different geometry) gives the A-route λ, which breaks the pattern; a Nab a matching aSPECT would strengthen it. | confidence: low
- [DECOMPOSER-H] **SPECULATIVE: Veselský's X⁺ channel.** ~1% of decays give an electron but no proton, which reproduces J-PARC ≈ bottle.

  | status: strained | why: it violates baryon-number conservation, no X⁺ has been seen, it still needs the a-route λ (F15), and the preprint is unchecked [D-95]. | distinguishing test: J-PARC/LiNA ≈ 878 s but Nab λ ≈ 1.267; a search for the charged X⁺. | confidence: low

## What would change my mind
- **A BL2 or BL3 value at 888 ± 1 s** from an independent dataset with re-measured fluence and gas conditions. Together with LiNA at 888 s, it would move me from A to B or C.
- **A Nab a-coefficient λ ≈ 1.267** (aSPECT-like). This would flip the SM arbitration (F7) and revive C and B, and G if the pattern holds.
- **UCNProBe's absolute β rate differing from its own storage lifetime by ~1%.** This would single out B or C over A.
- **A resolution of J-PARC's 15.8/3 internal χ² that moves its value toward 885 s** (the 50 kPa/new-SFC point). This would remove the only non-proton beam support for A.

## Assumptions I relied on
- I used the dossier values as quoted. Sussex–ILL [D-22] is an unverified lead, and I show every result with and without it. Ezhov [D-30] rests on a search summary.
- Errors are Gaussian and independent across experiments. I symmetrised asymmetric errors as the mean of the two sides for pooled χ², and used the side facing the other value for pairwise tensions.
- The older material-bottle values [D-29] come from one group's table, and I treated them as independent.
- For J-PARC's scale factor I applied S = √(15.8/3) to its statistical error only. That is my choice, not the authors'.
- I used the GS2023 radiative corrections with the paired Vud 0.97361(32), following [U-01], which still awaits an independent math check.
- The Fierz rate factor 1 + b⟨m_e/E⟩ is the standard form. The calculator for ⟨m_e/E⟩ is my own.
- The dossier's λ values for UCNA and PERKEO II were symmetrised: PERKEO II error taken as the quadrature total 0.00132 (stat 0.0008 with sys ±0.00105 symmetrised); UCNA 0.0020 as quoted.
