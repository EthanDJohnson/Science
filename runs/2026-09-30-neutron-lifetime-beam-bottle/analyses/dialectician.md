# Analysis: dialectician (resolve real contradictions)
status: final
## Method applied
I picked the contradictions in the dossier that carry the most weight: pairs of well-supported claims that cannot both hold as stated. For each, I state the thesis and the antithesis with their evidence. I then look for the regime, definition or condition under which both hold, or show which side must yield. Each synthesis is quantified in one script [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-dialectician_syntheses.py] and made to predict something that neither side predicted alone. Units are SI throughout: lifetimes in s, rates in s⁻¹, pressures in Pa or kPa. λ, b and branching fractions are dimensionless.

## Findings

1. **The contradictions chosen,** most load-bearing first:
   - (I) J-PARC 2024 as a clean discriminator, against J-PARC as internally inconsistent [D-71, D-23, D-24, D-25];
   - (II) the SM arbitration: β-asymmetry λ gives a bottle-like τ_β, while the a-coefficient λ gives a beam-like τ_β [D-74, U-01, D-42];
   - (III) proton-trap charge exchange as "the most probable explanation" (Serebrov), against "unlikely to have been significantly affected" (NIST) [D-72, D-17];
   - (IV) "the bottles are right", against the bottle-to-bottle scatter [D-73, D-81]. I treat IV as a sub-contradiction of the bottle-systematic candidate.
2. **aSPECT's reanalysis already states the Fierz synthesis of contradiction II.** [new: Beck et al. PRL 132, 102501 (2024), arXiv:2308.16170, full-text, "The re- sulting values for ( b,λ ) at 68% CL in combining (c) the independent datasets of PERKEO III and aSPECT are b(c) =−0.0181± 0.0065 λ(c) =−1.2724± 0.0013 . (8) With 2.82σ, the Fierz interference term b(c) obtained de- viates from zero"]. aSPECT's free (b, a) fit is strongly correlated: [new: same, full-text, "ρa,b = 0.808"].
3. **Caylor et al. 2025 quantify the H₂ charge-exchange channel in the NIST trap.**
   - Loss probability: [new: Caylor et al., PRC 112, 065501 (2025), arXiv:2506.01682, full-text, "For a typical trap time of 10 ms and assuming a trap temperature of 40 K and a pressure of 1×10 −7 Pa, one obtains a loss probability of about 0.3 %"].
   - BL1 itself: [new: same, full-text, "the detection limit of this analysis tech- nique was about 1 %. ... Regardless, analysis using a worst-case scenario for the amount of H + 2 contamination produces a shift in the measured neutron lifetime that is less than 0.5 s"].
   - A caveat from the authors: [new: same, full-text, "We do note that charge exchange producing H + 2 or other ions may be of particular concern for beam experiments"].
4. **J-PARC's internal structure (contradiction I).** The calc uses statistical errors only. Split the four configurations by pressure within each spin-flip chopper (SFC):
   - with the old SFC, τ(50 kPa) − τ(100 kPa) = −2.7 ± 8.5 s;
   - with the new SFC it is +16.5 ± 4.7 s;
   - the interaction between the two is +19.2 ± 9.7 s (2.0σ).

   A fit linear in pressure gives τ(p → 0) = 896.9 ± 5.3 s (statistical only), with slope −0.27 ± 0.07 s/kPa and χ² = 4.5/2. The sign fits an under-subtracted, gas-induced background: more gas means more background counted as β events, which shortens τ. The size fits too: the observed background is 4.9–5.4% of S_β at 100 kPa against 1.2–1.3% predicted [D-25], and a 1% mis-subtraction of S_β is about 9 s. **This fit is exploratory.** One point drives it (the 50 kPa, new-SFC configuration), and it ignores the per-condition systematics. [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-dialectician_syntheses.py]
5. **J-PARC's tension with each side, with its error as quoted and inflated.** The inflation multiplies the statistical error by the paper's own scale factor S = √(15.8/3) = 2.29, giving a statistical error of 3.90 s and a total of +5.59/−5.31 s.

   | J-PARC error used | vs BL1 (887.7 ± 2.25 s) | vs UCNτ (877.82 ± 0.29 s) |
   |---|---|---|
   | as quoted | 2.15σ | 0.16σ |
   | S-inflated | 1.74σ | 0.12σ |

   J-PARC therefore agrees with the bottles in aggregate. It disfavours "J-PARC ≈ beam" only at 1.7–2.2σ. [calc: same]
6. **The Fierz synthesis (contradiction II) predicts the total lifetime.** The phase-space average is ⟨m_e/E_e⟩ = 0.6553 (Z = 1 Fermi function on; 0.6540 with it off).
   - SM with b = 0, for comparison: τ_β = 878.50 s with PERKEO III λ and 889.58 s with aSPECT 2024 λ (GS2023 pairing, Vud = 0.97361), which reproduces U-01.
   - With λ(c) = 1.2724 and b(c) = −0.0181: τ_n = 893.7 s. Its error runs from ±2.8 s to ±5.2 s depending on the unquoted combined (λ, b) correlation.
   - That value is 3.1–5.6σ above UCNτ, 2.4–3.2σ above J-PARC and 1.1–1.7σ above BL1.
   - A Fierz term changes the total rate for every method equally. It cannot create a beam-bottle gap; it can only move the SM target.
   - With PERKEO III λ, the b needed to match UCNτ is +0.0012 and the b needed to match BL1 is −0.0158.
   - The a predicted from PERKEO III λ is −0.10687. aSPECT measures −0.10402(82), 3.48σ away, a 2.7% deficit in |a|.

   [calc: same]
7. **Charge exchange (contradiction III) in numbers.**
   - To lengthen 877.82 s to 887.7 s needs a proton-loss fraction of 1.113%.
   - Caylor's 0.3%, if every exchanged proton were lost undetected, would be 2.64 s (27% of the gap).
   - Matching the whole gap with undetected ions needs an H₂ partial pressure of about 3.7×10⁻⁷ Pa, about 3.7× Caylor's assumed pressure.
   - Caylor's worst case for BL1 is below 0.5 s (below 5.1% of the gap), because the H₂⁺ ion stays trapped and is counted.

   [calc: same]
8. **Bottles (contradiction IV).**
   - If BL1 is true, the missing loss rate is 1.268×10⁻⁵ s⁻¹ for UCNτ (time constant 7.9×10⁴ s) but 7.92×10⁻⁶ s⁻¹ for Gravitrap (1.26×10⁵ s). No single common loss fits both.
   - Gravitrap − UCNτ = 3.68 s (3.8σ).
   - J-PARC, which does not store neutrons, would need a separate +10.5 s bias, 2.4× its quoted upper error.

   [calc: same]
9. **The null, with error inflation of the size seen inside the field.** The field's own internal scatter implies scale factors of about 2: J-PARC's configurations give S = 2.29 [D-24], and the bottles disagree with each other at 3.8σ (finding 8). Inflating BL1's error by 1.5×, 2× or 2.3× lowers BL1 against UCNτ from 4.36σ to 2.92σ, 2.19σ and 1.91σ. [calc: same]

## Lens-specific outputs

### Contradiction I: is J-PARC 2024 a clean discriminator?
- **Thesis.** J-PARC counts electrons and normalises on ³He(n,p) in the same gas, with no ⁶Li deposit and no strong field [D-09]. It gives 877.2 ± 1.7 +4.0/−3.6 s, consistent with the bottles and 2.3σ (authors' figure) from the proton beams [D-23, D-26]. So the anomaly is "proton counting against the rest", and dark decay without an electron is disfavoured.
- **Antithesis.** J-PARC's four configurations disagree (χ²/DOF = 15.8/3) [D-23], and one of them sits 14–17 s above the others [D-24]. The gas-induced background is 4–5× the Monte Carlo prediction, and the paper names it as its dominant limitation [D-25]. Desai argues for pressure-dependent detector effects [D-71]. So J-PARC does not discriminate.
- **Where both hold.** The thesis is true of the *aggregate*, and the antithesis is true of the *pressure dependence*. Both can hold if J-PARC carries a bias proportional to gas pressure with the sign of under-subtracted background (Finding 4).
  - The aggregate is then a pressure-weighted mean pulled low by the 100 kPa runs, which dominate the statistics.
  - It agrees with the bottles at 0.1σ and disagrees with BL1 at only 1.7–2.2σ (Finding 5).
  - J-PARC is a valid discriminator today at the ~2σ level, not at the 4σ level the thesis implies.
- **Prediction neither side made.** J-PARC's value should move with pressure and background fraction.
  - LiNA runs at lower pressure or background (the background expected to fall ×50, or to 2% [D-102]). If LiNA lands near 878 s at every pressure, the bias hypothesis dies and J-PARC becomes a strong bottle-side point.
  - If LiNA's value rises as its background falls, with the naive extrapolation pointing to about 890–897 s, then J-PARC's 2024 agreement with the bottles was an artefact. In that case the "proton-counting systematic" and "J-PARC ≈ bottle ⇒ no invisible dark decay" arguments both lose their independent leg.
  - Separating 877.8 s from 887.7 s at 5σ needs σ ≈ 2.0 s (3σ needs 3.3 s) [calc].
  - The pressure scan inside LiNA is the test, not the combined value.

### Contradiction II: which λ arbitrates?
- **Thesis.** The β-asymmetry λ (PERKEO III, UCNA and PERKEO II, which agree with each other [D-15]) with superallowed Vud gives τ_β = 878.50 ± 0.88 s [U-01]. That matches the bottles and implies BR_X < ~0.3% [D-82], so the beam is wrong.
- **Antithesis.** The a-coefficient λ (aSPECT 2024, −1.2668(27) [D-42]) gives τ_β = 889.58 ± 3.20 s [U-01], matching the beam. On this route the SM does not favour the bottles.
- **Candidate synthesis 1: a Fierz term makes both measurements correct.** aSPECT itself proposes it: b(c) = −0.0181(65), λ(c) = −1.2724(13) (Finding 2). It predicts a total lifetime of 893.7 ± 2.8–5.2 s for every method (Finding 6). That value is 3.1–5.6σ above UCNτ and 2.4–3.2σ above J-PARC.
  - So the Fierz synthesis does not reconcile the three facts {A, a, τ_storage}. At least one of aSPECT's a, the storage lifetime, or b = 0 must yield.
  - The bottles, J-PARC and the β-asymmetry route agree with each other. aSPECT stands alone.
  - **aSPECT's a-coefficient is the side that yields.** This synthesis fails as physics but succeeds as a diagnostic.
  - It also yields a result the dossier lacks: **a Fierz term is not a new-physics explanation of the beam–bottle gap.** It is common to all methods, and the b that would make BL1 the SM value (−0.0158) makes the bottles 1.1% too short instead.
- **Candidate synthesis 2 (reframe): the a-coefficient and BL1 share a proton-side systematic.** The outlying measurements, the ones that support the beam value, all detect protons: aSPECT (proton recoil spectrum), BL1 and Sussex–ILL (proton counting). The electron and storage measurements (PERKEO III, UCNA, J-PARC, UCNτ, Gravitrap) all lie on the bottle side. aCORN (proton–electron coincidence, 874.9 ± 7.1 s [U-01]) is uninformative.
  - I label this pattern only. I found no single physical effect that biases both an absolute proton count after about 30 kV of post-acceleration and a recoil-spectrum shape. It is strained.
  - It predicts that Nab's a, obtained from proton time-of-flight in Si detectors [D-107], will side with aSPECT (|a| low). Synthesis 1 with aSPECT yielding predicts that Nab's a will match PERKEO III: a = −0.10687.
- **Prediction neither side made.** Nab's a and b decide contradiction II directly, and λ-precision alone is not the bottleneck (the dossier's estimate in §5c says the same).
  - If Nab finds a ≈ −0.1069 with b consistent with 0, the SM route closes at 878.5 s. The beam must then be wrong, or a proton-less branch exists, and BR_X is bounded by the SM route.
  - If Nab finds b ≈ −0.018, all three storage and electron results are wrong by about 16 s. That would be a far larger anomaly than the one posed.
  - If Nab finds a ≈ −0.1040 with b ≈ 0, there is a genuine A–a conflict inside the SM, and the SM arbitration is void.

### Contradiction III: charge exchange in the proton trap
- **Thesis (Serebrov, a competing group).** Charge exchange of trapped protons on residual gas, "even the presence of only H₂", is the most probable cause of the anomaly [D-72].
- **Antithesis (NIST).** Caylor measured H₂⁺ in the NIST trap. For BL1 the worst case shifts τ by less than 0.5 s, so it is "unlikely to be the cause" (Finding 3) [D-17].
- **Where both hold.** Charge exchange occurs at the ~0.3% level for 10 ms trapping at 1×10⁻⁷ Pa and 40 K (Finding 3). That is a real proton *loss*, equal to 2.6 s if nothing replaced it (Finding 7). But the exchange p + H₂ → H + H₂⁺ leaves a slow ion, born inside the trap, that is itself trapped and detected. The *counting* loss is therefore only the fraction with a different detection efficiency, below 0.5 s.
  - Serebrov is right about the process, and NIST is right about the net effect.
  - To explain the whole 1.11% gap, three things would all be needed: undetected products (neutral, or ions below threshold), an H₂ partial pressure near 3.7×10⁻⁷ Pa (Finding 7), and a BL1 H₂⁺ fraction below the ~1% detection limit (Finding 3).
  - That is possible at the margin but not favoured. **The charge-exchange sub-hypothesis yields to a strained status.**
- **Prediction neither side made.** Loss per proton scales with trapping time, not trap length, so BL1's trap-length slope method does not cancel it [D-08].
  - BL2's trap-time and pressure scans [D-100] should show τ independent of trapping time within 0.5 s per doubling if the NIST reading holds.
  - Under the Serebrov reading, τ shifts by about +2.6 s per 10 ms at 1×10⁻⁷ Pa and grows linearly with H₂ pressure.
  - The residual BL1 offset, if real, must then sit in the fluence normalisation or in the proton efficiency/backscatter, not in residual gas.

### Contradiction IV: are the bottles right?
- **Thesis.** UCNτ is blinded, uses four analyses and in-situ dagger tests, and gives 877.82 ± 0.29 s [D-10, D-27]. J-PARC, which stores no neutrons, agrees [D-23].
- **Antithesis.** Gravitrap reads 881.5 s, 3.8σ above UCNτ (Finding 8). Material bottles average 880.0 against 877.8 s for magnetic ones [D-32]. UCNτ's own year-to-year values scatter by 2.46 s (2.3σ) [D-81]. The bottles historically drifted by about 6σ [brief premise 3].
- **Where both hold.** Bottle-specific systematics do exist, at the scale of the inter-bottle spread (about 4 s), but no single common missing loss exists at the 10 s scale.
  - If BL1 were true, UCNτ and Gravitrap would need different missing rates (1.27×10⁻⁵ against 7.9×10⁻⁶ s⁻¹), which rules out one common loss. J-PARC would need its own independent +10.5 s error of the same sign (Finding 8).
  - The sign pattern is also wrong for a common loss. The trap with the most loss channels, the material bottle whose walls add loss channels, reads *longer*. The simplest reading is wall-extrapolation or marginal-UCN systematics of a few s, not a missing bulk loss.
  - Any loss equal in wall-free and material traps is a bulk disappearance of the neutron, which is new physics by the brief's definition, not a bottle systematic.
- **Prediction neither side made.** τSPECT (a magnetic trap of different geometry) [D-103] should land in the 877.8–881.5 s band, not near 888 s. Its position within that band says which effect causes the ~4 s spread. If UCNτ is short because of residual marginally trapped UCN, τSPECT, with a different marginal-UCN regime, should read nearer Gravitrap, about 880–881 s. If Gravitrap is long because of its wall-loss extrapolation, τSPECT should read ≈ UCNτ, about 878 s.
  - UCNProBe [D-106] counts β electrons inside a bottle. If the missing thing is a storage loss, UCNProBe's β-rate lifetime will exceed its storage lifetime by about 10 s. Otherwise the two coincide.

### Sign conflict D-79 (Berezhiani against Tan on n → n′), resolved by elimination
The two models make opposite predictions about which side is "true", but both rest on the strong-field resonance with Δm of about 100–300 neV. The SNS regeneration search excludes that for Δm > 10 neV [D-62, D-89]. Neither side survives, so this is not a real contradiction that needs synthesis. It is marked here so the judge does not re-open it.

### Prediction matrix (by synthesis; values in s unless stated)
| Candidate | p-beam (BL2/BL3) | e-beam (LiNA pressure scan) | material bottle | magnetic trap (τSPECT) | in-bottle β (UCNProBe) | SM λ route (Nab a, b) | direct searches | NS bounds |
|---|---|---|---|---|---|---|---|---|
| DIAL-A p-beam systematic | ≈878–881; no trap-time dependence (III) | ≈878 at all pressures | 878–882 | ≈878 | β-rate = storage | a ≈ −0.1069, b ≈ 0 | null | n/a |
| DIAL-B bottle loss | ≈888 | ≈888 (needs J-PARC 2024 wrong) | lower than truth by 6–10 | lower by 10 | β-rate τ ≈ 888 > storage | SM route ≈ 888 needs aSPECT-like λ | null | n/a |
| DIAL-C invisible dark decay | ≈888 | ≈888 (J-PARC 2024 against, 1.7–2.2σ) | ≈878 | ≈878 | β-rate τ ≈ 888 | a ≈ −0.1069 and τ_β = 878.5 would contradict (BR_X bound) | χγ, χe⁺e⁻ null (invisible modes untested) | must be evaded |
| DIAL-D strong-field n→n′ | ≈888 | ≈878 | ≈878 | ≈878 | = storage | SM = 878.5 | SNS regeneration null already | n/a |
| DIAL-E null (inflated errors) | 880–885 drift | 878–890 depending on pressure | 878–882 | 877–880 | = storage | any | null | n/a |
| DIAL-F proton-detection reframe | ≈878 once the proton effect is found | ≈878 | ≈878 | ≈878 | = storage | Nab a ≈ aSPECT (−0.1040) with b ≈ 0 | null | n/a |
| DIAL-G Fierz b | all methods ≈894 | ≈894 | ≈894 | ≈894 | = storage | b ≈ −0.018 | n/a | n/a |

## Calculations
- `runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-dialectician_syntheses.py` (log beside it). It computes:
  - (I) J-PARC per-configuration χ² (statistical only: 19.6/3, S = 2.55; the paper gives 15.8/3), the tension with BL1 and UCNτ (quoted 2.15σ / 0.16σ; inflated 1.74σ / 0.12σ), the pressure × SFC decomposition (interaction +19.2 ± 9.7 s), and the linear pressure extrapolation (896.9 ± 5.3 s, statistical only);
  - (II) ⟨m_e/E_e⟩ = 0.6553; τ_β for PERKEO III λ = 878.50 s and aSPECT 2024 λ = 889.58 s; the Fierz synthesis τ = 893.7 ± (2.8–5.2) s; b needed for UCNτ (+0.0012) and for BL1 (−0.0158); a-coefficient deficit 3.48σ;
  - (III) the proton loss needed (1.113%), the 0.3% loss ↦ 2.64 s, the H₂ pressure needed (3.7×10⁻⁷ Pa), and <0.5 s ↦ <5.1% of the gap;
  - (IV) missing loss rates of 1.268×10⁻⁵ and 7.92×10⁻⁶ s⁻¹, Gravitrap − UCNτ = 3.68 s (3.81σ), and the J-PARC shift needed (+10.5 s);
  - (null) BL1-vs-UCNτ significance under BL1 error scale factors of 1, 1.5, 2 and 2.3: 4.36σ, 2.92σ, 2.19σ and 1.91σ.
- Uses the run's calculator `tools/neutron_beta_decay.py` (tau_beta, GS2023 constants) for the SM baseline, which reproduces U-01's 878.50 ± 0.88 s.

## Candidate answers (at least 3; the null and a reframe count)
- [DIAL-A] **Dominant cause: an unidentified systematic in proton-counting beams (BL1, with Sussex–ILL).** It is most likely in the neutron-fluence normalisation or the proton detection/backscatter efficiency. Residual-gas charge exchange is demoted to a sub-effect of at most a few s.
  - status: surviving.
  - Why: it comes from syntheses II and IV.
    - The β-asymmetry route, the storage lifetimes and J-PARC agree, and aSPECT is the side that yields (II).
    - The bottles cannot share one missing loss, and a bottle-only story needs an independent 10.5 s J-PARC error (IV).
    - Synthesis III limits charge exchange to <0.5 s as measured, or about 2.6 s at most with undetected ions. That covers under 27% of the 1.11% needed, so the remainder must lie in fluence or efficiency.
  - Weakest link: J-PARC's discriminating power is only 1.7–2.2σ, and its pressure structure could hide a beam-ward bias (I).
  - Distinguishing test: BL2/BL3 with scans of trap time and pressure. The prediction is τ ≈ 878–881 s, no trap-time dependence within 0.5 s, and the offset traced to fluence or efficiency. Nab should give a ≈ −0.1069 with b ≈ 0.
  - confidence: medium.
- [DIAL-B] **Dominant cause: an unidentified loss common to all storage experiments.**
  - status: strained.
  - Why: from synthesis IV.
    - Material and magnetic traps would need different missing rates (1.27×10⁻⁵ against 7.9×10⁻⁶ s⁻¹).
    - The trap with more loss channels reads longer.
    - J-PARC, which stores no neutrons, would need its own same-sign +10.5 s error.
    - A loss equal in all traps is a bulk disappearance, which would make this new physics, not a systematic.
  - Distinguishing test: UCNProBe's β-rate lifetime about 10 s above its storage lifetime; τSPECT near 888 s. Neither is expected.
  - confidence: low.
- [DIAL-C] **Dominant cause: a proton-less dark decay,** with the surviving invisible channels n → χφ or χχχ plus a neutron-star escape [D-87, D-77].
  - status: strained.
  - Why:
    - The λ/Vud route bounds BR_X at the level set by the β-asymmetry λ [D-82].
    - The Fierz synthesis cannot rescue it, because b shifts every method alike (II).
    - J-PARC ≈ bottle disfavours it at 1.7–2.2σ (I).
    - The e⁺e⁻ and γ channels are excluded over most of the window [D-85, D-86].
    - It survives only if J-PARC's pressure bias is real and the a-coefficient route is right.
  - Distinguishing test: LiNA reading about 888 s at low background; Nab's a matching aSPECT.
  - confidence: low.
- [DIAL-D] **Dominant cause: strong-field n → n′ conversion (Berezhiani; Tan's reversed-sign variant).**
  - status: eliminated.
  - Why: both signs rely on Δm ≈ 100–300 neV, which the SNS regeneration search excludes for Δm > 10 neV [D-89]. The D-79 conflict dissolves because both sides fall.
  - Distinguishing test: none left beyond other field profiles. It would predict J-PARC ≈ bottle, which is observed but not specific to it.
  - confidence: medium.
- [DIAL-E] **Null: no single dominant cause.** Errors underestimated by about 2× across several experiments, of the size seen inside J-PARC (S = 2.3) and between bottles (3.8σ), bring BL1 against UCNτ to 2.2σ, a fluctuation-plus-scatter.
  - status: surviving (strained).
  - Why: it needs BL1's quoted budget to be too small by a factor of 2 with no identified item. The field's own scatter supports such factors.
  - Distinguishing test: BL2/BL3 land at an intermediate 880–885 s, and LiNA and τSPECT scatter at ±3 s rather than clustering.
  - confidence: low–medium.
- [DIAL-F] **Reframe: the anomaly is "proton detection against everything else", not "beam against bottle".** BL1, Sussex–ILL and aSPECT (all proton-based) point beam-like; every electron or storage measurement points bottle-like.
  - status: strained.
  - Why: the pattern holds, but no single mechanism has been identified that biases both an absolute proton count and a recoil spectrum shape.
  - Distinguishing test: Nab's proton-TOF a agrees with aSPECT (a ≈ −0.1040) while its A-free λ disagrees with PERKEO III; BL2 moves toward 878 s once a proton-side effect is found.
  - confidence: low.
- [DIAL-G] **New physics: a scalar/tensor Fierz term b ≈ −0.018** reconciles A and a (aSPECT's own combination).
  - status: eliminated as an explanation of the gap.
  - Why: b changes the total rate equally for beams and bottles. It predicts τ_n = 893.7 s for every method, 3.1–5.6σ above UCNτ and 2.4–3.2σ above J-PARC (II).
  - Distinguishing test: Nab's b at the 10⁻³ scale. b = −0.018 would appear at high significance. Nab's b-precision target is not in the dossier.
  - confidence: medium.

## What would change my mind
- LiNA's lifetime rising toward about 888 s as its background falls, or a J-PARC pressure scan with a significant negative slope. Either would restore the beam side and revive DIAL-B and DIAL-C.
- Nab measuring a ≈ −0.1040 with b ≈ 0 (voids the SM arbitration), or b ≈ −0.018 (voids the storage results).
- BL2 finding a trapping-time or H₂-pressure dependence of several s per 10 ms (charge exchange restored as the named BL1 effect, which strengthens DIAL-A's sub-hypothesis).
- τSPECT or UCNProBe reading about 888 s.

## Assumptions I relied on
- The J-PARC per-configuration values in D-24 are as printed. I combined only the statistical errors for the pressure decomposition, because the column meanings for the systematics are unlabelled. The linear extrapolation is exploratory and one point drives it.
- For the Fierz calculation: the leading-order effect of b on the total rate is (1 + b⟨m_e/E_e⟩), with ⟨m_e/E_e⟩ = 0.655 from a Z = 1 relativistic Fermi-function spectrum that neglects recoil. b is assumed tensor-dominated, so superallowed Vud is unchanged (the scalar b_F ≤ 0.0033 [D-66]). The unquoted (λ, b) correlation in aSPECT's combination was scanned over −0.8 to +0.8.
- The SM baseline uses the consistent Vud–RC pairing of U-01 (GS2023, Vud = 0.97361(32)); I re-derived it with the run's calculator.
- For charge exchange: loss scales linearly with the H₂ density (Caylor eq. 2, small-probability limit). Trapped H₂⁺ ions are detected as charge, which is how I read Caylor's "worst-case ... less than 0.5 s".
- Sussex–ILL [D-22] is unverified in this run, so the proton-counting side is effectively BL1 alone.
