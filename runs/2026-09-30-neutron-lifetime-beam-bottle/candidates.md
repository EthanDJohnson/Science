# Candidate answers
exclusive: yes (anomaly slate: C1–C6 each name a different dominant cause of the ~1.1% proton-beam/storage gap; C7 is the no-dominant-cause null; C8's sharp form names one proton-detection cause shared by the lifetime and λ splits, which excludes C1's requirement that aSPECT's λ is wrong for an unrelated reason)
lenses merged: statistician, empiricist, mechanist, examiner, decomposer, dialectician, constraints (math checks: math/statistician.md, math/empiricist.md, math/mechanist.md, math/examiner.md, math/decomposer.md, math/dialectician.md, math/constraints.md)
status: final

Units: SI throughout (lifetimes in s, rates in s⁻¹, fields in T, pressures in Pa or mbar); particle masses and energies in MeV or neV with ħ = c = 1; λ, Vud, b and branching ratios dimensionless. Reference gap (statistician, the brief's reference): proton-counting beam 887.97 ± 2.04 s against all storage 878.32 ± 0.43 s (S = 1.85), Δ = 9.65 ± 2.08 s, 4.63σ, 1.09% of τ, missing rate 1.24×10⁻⁵ s⁻¹ [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-statistician_combination.py; M-STATISTICIAN-02 verified]. BL1 alone against UCNτ: 9.88 s, 1.113%, 1.268×10⁻⁵ s⁻¹ [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-examiner_premises.py; M-EXAMINER-04 verified].

## C1: An unidentified systematic in the proton-counting beam method (BL1, Sussex–ILL) makes it read about 1.1% long; the storage value near 878 s is the true lifetime.
type: explanation
from: STATISTICIAN-A, EMPIRICIST-A, MECHANIST-A, EXAMINER-A, DECOMPOSER-A, DIAL-A, CONSTRAINTS-A (the "BL1 against everything" readings of STATISTICIAN-F, EMPIRICIST-F, MECHANIST-E and DECOMPOSER-F enter here as the scope sub-hypothesis A-BL1; their premise critique is carried by C8)
argument:
- Causal chain. BL1 extracts τ = L Ṅ_α+t ε_p/(Ṅ_p ε_0 v_0) from the slope of proton rate against trap length [new: Nico et al. 2005, arXiv nucl-ex/0411041, ACCESS full-text, eq. 6 as quoted by the mechanist; D-08]. The slope cancels additive (length-independent) end effects, so a 1.1% error must be multiplicative in ε_p/ε_0: either ε_0 is 1.16% too low or 1.14% of trapped protons are lost uncounted [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-mechanist_required_sizes.py; M-MECHANIST-02 verified]. Beam attenuation between trap and monitor is < 0.001% [new: Nico 2005, full-text], so the neutron side can fail only through the absolute monitor efficiency.
- Named rival effects (sub-hypotheses):
  - **A1, ⁶Li fluence-monitor absolute efficiency.** Needs ε_0 1.16% higher than assumed: 20× the 2013 Alpha-Gamma uncertainty (0.5 s), and opposite in sign to the 2013 recalibration, which moved τ by +1.4 s [D-07, D-20; M-MECHANIST-03 verified]. The mechanist and dialectician rank it plausible; the decomposer ranks it least likely.
  - **A2, a proton loss proportional to stored protons.** Candidates: residual-gas charge exchange with the product ions escaping detection; halo protons (1.0 s budget); a mis-sized trap-nonlinearity/end-region correction (−5.3 ± 0.8 s, a 2× error needed) [D-21]. Caylor et al. measured the H₂ channel: [new: Caylor et al., PRC 112, 065501 (2025), arXiv:2506.01682, ACCESS full-text, "For a typical trap time of 10 ms and assuming a trap temperature of 40 K and a pressure of 1×10 −7 Pa, one obtains a loss probability of about 0.3 %"] and [same, "analysis using a worst-case scenario for the amount of H + 2 contamination produces a shift in the measured neutron lifetime that is less than 0.5 s"]. A 0.3% loss with every ion lost would be 2.64 s (27% of the gap). The whole gap needs H₂ near 3.7×10⁻⁷ Pa with undetected ions [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-dialectician_syntheses.py; M-DIALECTICIAN-06 verified]. For H⁺ + H₂ cross sections of 10⁻²⁰–10⁻¹⁹ m² (the lens's assumption), it needs n_H₂ ≈ 10¹⁴–10¹⁵ m⁻³, i.e. 4×10⁻⁷ to 4×10⁻⁶ Pa at 300 K [M-MECHANIST-04, arithmetic verified]. The weakest link is whether the H₂⁺ product escapes detection; Caylor determines that ion detection efficiency [new: Caylor 2025, ACCESS abstract].
  - **A3, proton detection.** Backscatter, dead layer or Si scattering (budgets 0.4 s and 0.5 s; would need to be 20–25× larger) [D-21; M-MECHANIST-03].
  - **A4, a mis-signed or doubled large correction.** ⁶Li absorption (+5.4 s) or trap nonlinearity (−5.3 s); either at 100% error supplies 54% of the gap [D-21; calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-decomposer_tree.py; M-DECOMPOSER-12 verified].
  - **Scope.** Either **A-BL1**: the error belongs to the single BL1 dataset (2005 data, re-analysed 2013 [D-07]), the brief's "BL1 against everything" reading, so BL2 reads about 878 s as built. Or **A-gen**: the error is generic to Penning-trap proton counting, so BL2 also reads long until the effect is found. Sussex–ILL's agreement with BL1 favours A-gen.
- Room in the budget: none as itemised. The shift is 4.4× BL1's total error, 5.2× its systematic and 5.8× the un-remeasured 1.7 s "unassociated with fluence" line. No itemised entry has room at < 4σ, so the effect must be unlisted, or a correction mis-sized at about 2× [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_consistency.py; M-CONSTRAINTS-12 verified].
- Shift by class: proton beam +9.6 to +9.9 s (sign: long). Zero in J-PARC, material bottles, magnetic traps, in-bottle β counting and the SM route.
- Weakest link: no named effect reaches 9.9 s at its quoted size.
predictions: If true, BL2 (< 1 s) and BL3 (0.3 s) read ≈ 878 s: as built under A-BL1, or once the effect is found and corrected under A-gen. Under A2, the loss scales with trapping time, not trap length: BL1's 10 ms and 5 ms subsets differ by ≈ 5.1 s (≈ 6.8 s if the published value is an equal mix) [M-MECHANIST-04]. Under Serebrov's reading, a BL2 trap-time scan shows about +2.6 s per 10 ms at 1×10⁻⁷ Pa H₂; under NIST's reading, < 0.5 s [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-dialectician_syntheses.py]. LiNA ≈ 878 s at every gas pressure. UCNProBe's β-rate lifetime equals its storage lifetime. Nab gives a ≈ −0.1069 (|λ| ≈ 1.2764) with b ≈ 0. If false, BL2/BL3 reproduce ≈ 888 s with a new flux monitor and characterised residual gas, or LiNA/UCNProBe read ≈ 888 s.
evidence for:
- The partition prefers it. Proton counting against the rest has within-class χ² 24.2 against 29.5 for beam against bottle (Δχ² = 5.3, profile likelihood ratio ≈ 14), and all of that comes from J-PARC. The four-class split leaves only 8.4/7 within classes [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-statistician_combination.py; M-STATISTICIAN-04, M-STATISTICIAN-06 verified; M-EXAMINER-01, M-DECOMPOSER-04 concur].
- J-PARC 2024 (877.2 ± 1.7 +4.0/−3.6 s, preprint) sits 0.14σ from UCNτ, 0.26σ from all storage and 2.15σ from BL1 [D-23; M-STATISTICIAN-05, M-EXAMINER-03 verified].
- The SM β-asymmetry (A) route gives τ_β(PERKEO III) = 878.50 ± 0.88 s, and the A group gives 878.70 ± 0.83 s. That is 0.18σ from storage and 4.26σ from the proton beam [U-01; calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_sm_tau.py; M-CONSTRAINTS-01/-02, M-STATISTICIAN-11 verified].
- The first-row CKM sum is 0.99898(87) (−1.2σ) with UCNτ + PERKEO III, against 0.98842(251) (−4.6σ) with BL1 + PERKEO III [M-CONSTRAINTS-04 verified]. Raising Vud to close the Cabibbo deficit shortens τ_β, away from the beam [M-EXAMINER-07 verified].
- The beam side is essentially one dataset. BL1 carries 82% of the proton-class weight (the decomposer's 85% is corrected by M-DECOMPOSER-01). Without BL1, proton against rest is 2.2σ [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-empiricist_partitions.py; M-EMPIRICIST-03 verified]. No BL2 lifetime has been published [D-100; new: WebSearch, ACCESS search-summary, SUMMARY "found that the result of the beam neutron lifetime performed at NIST is unlikely to have been significantly affected by charge exchange with molecular hydrogen"].
- Base rates. [new: Bailey 2017, R. Soc. Open Sci. 4, 160600, ACCESS full-text, "Outliers are common, with 5 σ disagreements up to five orders of magnitude more frequent than naively expected"]. With Student-t ν = 2–4, P(> 4.63σ) = 0.010–0.044 [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-statistician_heavytail.py; M-STATISTICIAN-12 verified]. None of the 7 sourced precision disagreements ended in new physics. In the resolved cases the older, less-replicated method was wrong [empiricist Lens output 2; three of the seven cases are search-summaries; M-EMPIRICIST-10 checks only the Laplace arithmetic].
- Proton charge exchange does occur in a BL-type trap [D-17, D-72].
evidence against:
- No effect of the needed size has been identified. Caylor's worst case for BL1 is < 0.5 s [new: Caylor 2025, full-text]. The NIST group judges BL1 "unlikely to have been significantly affected" [D-17]. Wietfeldt 2023: "None of the issues raised lead us to alter the value" [D-72, abstract].
- Sussex–ILL, an independent apparatus using the same method, agrees with BL1: 889.2 ± 3.0 ± 3.8 s [new: PDG encoder listing s017, ACCESS full-text, "889.2 ± 3.0 ± 3.8 BYRNE 96 CNTR Penning trap"]. On its own it is 2.24σ from storage [M-STATISTICIAN-02]. It also biases A-gen over A-BL1.
- C1 depends on the A-route λ. If the proton-recoil (a) route is right (τ_β = 887.21 ± 2.93 s, or 889.58 ± 3.20 s with aSPECT 2024), C1 fails the SM route at 3.2σ [M-CONSTRAINTS-03 verified]. PERKEO III and aSPECT 2024 differ by 3.49σ [M-STATISTICIAN-10]. Beck 2024's combined Fierz fit would give τ = 893.7 ± 4.2 s for every method [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-decomposer_fierz.py; M-DECOMPOSER-11 verified, error assumes no b–λ correlation].
- J-PARC is a weak arbiter. Its four run conditions disagree (χ² 15.8/3; 19.6/3 on statistics alone), and its background is 4–5× the MC prediction [D-24, D-25]. With its error inflated by S = 2.29 it is only 1.74σ from BL1 [M-DIALECTICIAN-01]. A fit linear in pressure extrapolates to 896.9 ± 5.3 s at 0 kPa (stat only), but a single point drives it: without that point the slope is +0.031 ± 0.163 s/kPa [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-dialectician_syntheses.py; M-DIALECTICIAN-02 verified]. Desai argues for a pressure-dependent effect [D-71, abstract].
- C1 leaves the storage-internal split unexplained. Material bottles are 2.22 ± 0.75 s above magnetic traps (2.95σ scaled) [M-STATISTICIAN-09]. That residual belongs to the null (C7) as a second-order effect.
decisive test: BL2 (NIST/Tulane; < 1 s; "next few years", search-summary) or BL3 (NIST; 0.3 s; in construction, no date) [D-100, D-101]. C1 predicts ≈ 878 s. Because BL1's own 2.25 s error caps any test against BL1 at 4.4σ, a BL2 reading of 878 ± 1 s sits 3.8σ from BL1 (4.2σ from the proton-class pole), and BL3 at 0.3 s sits 4.1–4.7σ [M-EXAMINER-11 (refutes the examiner's "≥ 5σ" claim), M-EMPIRICIST-08, M-STATISTICIAN-14, M-CONSTRAINTS-05]. Cheaper tests inside existing data: BL1's published 5 ms against 10 ms comparison (≈ 5 s under A2), and an independent re-calibration of the ⁶Li deposit (A1 predicts ε_0 about 1.2% higher). Runner-up: LiNA (J-PARC, ~1 s) with a pressure scan, which should read ≈ 878 s flat in pressure [D-102].

## C2: An unidentified loss of about 1.2×10⁻⁵ s⁻¹ common to material and magnetic UCN traps shortens every storage result; the proton-beam value near 888 s is the true lifetime.
type: explanation
from: STATISTICIAN-B, EMPIRICIST-B, MECHANIST-B, EXAMINER-D, DECOMPOSER-B, DIAL-B, CONSTRAINTS-B
argument:
- Size. With BL1 true, the missing loss is 1.268×10⁻⁵ s⁻¹ in UCNτ (time constant 7.9×10⁴ s ≈ 0.91 d), 49× its +0.20 s systematic. In Gravitrap it is 7.92×10⁻⁶ s⁻¹, 10× its 0.6 s. One mechanism would therefore have to be 38% weaker in the material trap [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_consistency.py; M-CONSTRAINTS-12, M-DIALECTICIAN-07, M-DECOMPOSER-06 verified]. A constant-rate loss is exactly degenerate with β decay in a single-exponential fit, so only absolute rate estimates guard against it [M-MECHANIST-06 verified].
- Named rival effects (sub-hypotheses):
  - **B-mag (magnetic traps).** Depolarisation: the needed rate is 130× UCNτ's assigned bound [new: Gonzalez et al. 2021, arXiv:2106.10375, ACCESS full-text, "we assign a depolariza- tion rate of λdp = 0.0+1.0 −0.0× 10−7 s−1"]. Or marginally trapped or heated UCN: a time-dependent loss would bend the storage curve and change with dagger height [D-10].
  - **B-mat (material bottles).** An unmodelled energy dependence of wall loss that survives the size extrapolation [D-12]. It cannot reach wall-free UCNτ.
  - **B-gas (residual-gas upscattering in all traps).** At 300 K it needs N₂ ≈ 6×10⁻⁴ mbar, H₂ ≈ 2×10⁻⁵ mbar or He ≈ 5×10⁻³ mbar (cross sections assumed by the lens), ≈ 90× UCNτ's measured gas correction of +0.11 ± 0.06 s [new: Gonzalez 2021, full-text, "Residual gas scattering +0.11 ±0.06"; M-MECHANIST-05, -06 arithmetic verified]. Effectively eliminated.
  - **B-pop (a shared stored-population effect).** By analogy with orthopositronium, where two methods with "radically different systematic effects" shared one thermalisation error [new: Nico et al. 1990, PRL 65, 1344, ACCESS abstract; new: Vallery et al. 2003, PRL 90, 203402, ACCESS abstract, "The fitted decay rate requires only a 500 ppm correction for nonthermal o−Ps effects"].
- Auxiliary requirements:
  - J-PARC stores no UCN, so it needs its own independent −10.5 to −10.8 s error. A candidate agent exists: gas-borne γ background left unsubtracted, needing 1.23% of S_β, which is 0.3–0.5 of the observed excess over MC [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-mechanist_required_sizes.py; M-MECHANIST-07 verified].
  - The SM route needs the a-route λ, so the three β-asymmetry experiments would share a ≈ 0.7% λ error [decomposer F15].
- The dialectician's objection: a loss identical in wall-free and material traps is a bulk disappearance, which by the brief's definition is new physics (C3), not a systematic.
- Shift by class: material −6.5 s (Gravitrap) and magnetic −9.9 s (UCNτ), sign short. J-PARC shifted −10.8 s by the separate artefact. Proton beam and in-bottle β rate unchanged.
- Weakest link: one agent must act on walled and wall-free traps alike and also reach J-PARC, which it cannot.
predictions: If true, UCNProBe's β-rate lifetime reads ≈ 888 s while its own storage lifetime reads ≈ 878 s (a ≈ 10 s difference in one trap). LiNA reads ≈ 888 s once its background falls. BL2/BL3 read ≈ 888 s. Nab gives |λ| ≈ 1.2668. The lenses disagree on a new magnetic trap: τSPECT reads ≈ 888 s if the loss is specific to UCNτ's geometry (mechanist), ≈ 878 s if it is common to all storage (constraints). If false, UCNProBe's β rate equals its storage rate and LiNA reads ≈ 878 s.
evidence for:
- The a route: τ_β(aSPECT 2024) = 889.58 ± 3.20 s is 0.42σ from the proton beam [U-01; calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-statistician_lambda_sm.py; M-STATISTICIAN-11]. The world of beam τ plus a-route λ closes first-row unitarity at +0.1σ [M-CONSTRAINTS-04, M-DECOMPOSER-08].
- Storage has a record of unrecognised systematics of ~6 s (though with the opposite sign; see below): [new: Serebrov & Fomin 2010, arXiv:1005.4312, ACCESS full-text, "Systematic errors of about 6 s are found in each of the experiments"]. Storage also scatters internally: Gravitrap vs UCNτ 3.80σ, material vs magnetic 2.95σ scaled [M-STATISTICIAN-09].
- The o-Ps precedent: a shared stored-population systematic did fool two methods [empiricist F3].
- No published external critique of UCNτ's marginal-UCN or depolarisation budget exists (a dossier gap, §6).
evidence against:
- J-PARC contradicts it at 2.15–2.24σ: likelihood ratio ≈ 10–12 : 1 as quoted, 4.5–5 : 1 inflated [M-STATISTICIAN-06, M-CONSTRAINTS-11, M-EXAMINER-03].
- The A-route τ_β is 3.8σ below the BL1 value that C2 takes as true [M-CONSTRAINTS-03].
- The needed rate is 130× UCNτ's depolarisation bound, ≈ 90× its gas correction, and 49× its systematic [M-MECHANIST-06, M-CONSTRAINTS-12].
- Material bottles read longer than magnetic traps (880.03 against 877.82 s), the wrong sense for an extra loss in walled traps [D-73; M-STATISTICIAN-01].
- The documented past storage systematics had the opposite sign (results too long) [empiricist F10].
- UCNτ's in-situ dagger and cleaning tests found no time-dependent loss at the 0.2 s level [D-10; empiricist Lens output 3].
- χ² ledger with the A route: 41.27/9 (p = 4×10⁻⁶), against 23.33/9 for C1 [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_consistency.py; M-CONSTRAINTS-14 unverified].
decisive test: UCNProBe (LANL, Krivos and Morris; in-bottle β counting; 1–2 s target, search-summary; no date) [D-106]. C2 predicts a β-rate lifetime ≈ 888 s against a storage lifetime ≈ 878 s in the same trap. A 888 s reading at 1.5 s is 6.2σ from the storage pole [M-STATISTICIAN-14]. Runner-up: Nab's a coefficient (ORNL SNS; 0.04% goal; no a value yet [D-107]). C2 needs |λ| ≈ 1.2668, and at 0.04% an aSPECT-like reading would sit 12.7–13σ from the A route [M-CONSTRAINTS-05, M-DECOMPOSER-10].

## C3: A proton-less, electron-less dark-decay branch of about 1.1% (invisible n → χφ, χχχ or χA′) makes beams measure τ_β while bottles measure the true total lifetime (speculative).
type: explanation
from: STATISTICIAN-C, EMPIRICIST-C, MECHANIST-C, EXAMINER-C, DECOMPOSER-C, DIAL-C, CONSTRAINTS-C (DIAL-G's Fierz term enters as the λ-escape sub-hypothesis C-b, not as a separate cause)
argument:
- Mechanism (SPECULATIVE; Fornal–Grinstein EFT). The branch needs Br_X ≈ 1.09–1.11%. A proton-counting beam measures τn/Br(n → p + anything), bottles measure the total, and J-PARC counts electrons, so it also reads τ_β [D-06].
- Kinematic window. ⁹Be → 2α + χ gives m_χ > 937.993 MeV, 92 keV tighter than Fornal–Grinstein's 937.900 MeV [new: McKeen, Pospelov & Raj 2020, PRL 125, 231803, ACCESS full-text, "There is also a lower limit on the χ mass of mχ > 938.0 MeV from the stability of 9Be"; calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_darkwindow.py; M-CONSTRAINTS-07 verified].
- Channel variants (sub-hypotheses):
  - **C-γ, n → χγ.** Excluded over the dark-matter window E_γ = 0.782–1.571 MeV (narrowed) [D-60, D-85]. The non-DM case with E_γ → 0 is not covered [D-85].
  - **C-ee, n → χe⁺e⁻.** Excluded except T_ee < 32 keV, 5.8% of the narrowed mass window [D-61, D-86; M-CONSTRAINTS-07]. Nobody has checked whether J-PARC's TPC would count such low-energy pairs as β decays [examiner premise 7].
  - **C-inv, invisible n → χφ, χχχ, χA′.** No laboratory search applies; only λ/Vud and neutron stars constrain them [D-87, D-98].
- Escapes it needs (sub-hypotheses):
  - **C-a (λ route).** Either the a-coefficient (aSPECT) λ is right, or **C-b**: a Fierz term b ≈ −0.0158 [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_sm_tau.py; M-CONSTRAINTS-06 verified]. That is 1.6σ from [new: Saul et al. 2020, PRL 125, 112501, ACCESS abstract, "We obtain a limit of b = 0.017(21) at 68.27 C.L."] and 0.3σ from aSPECT's b. A Fierz term alone cannot cause the gap: it moves every method's rate alike, to 893.7 s, 3.1–5.5σ above UCNτ [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-dialectician_syntheses.py; M-DIALECTICIAN-05 verified].
  - **C-NS (neutron stars).** χ–χ repulsion with m_V/g ≲ ~50 MeV in the lens's toy EOS. The math check finds this threshold depends on the EOS: it could lie anywhere from about 50 to 100 MeV [M-CONSTRAINTS-09, threshold unverified]. Published escapes are Cline–Cornell (m_A′/g′ ≲ 45–60 MeV), Bastero-Gil's scalar and Strumia's χχχ [D-77].
- Shift by class: proton beam and J-PARC both +9.7 s (they measure τ_β). Bottles unchanged (true τn). In-bottle β-rate lifetime ≈ 888 s.
- Weakest link: the λ route.
predictions: If true, LiNA reads ≈ 888 s, with no pressure trend once its background is cut. UCNProBe's β-rate lifetime reads ≈ 888 s against its storage lifetime ≈ 878 s. BL2/BL3 read ≈ 888 s with no dependence on trap field, gas or trap time. Nab gives |λ| ≈ 1.2668, or b ≈ −0.016 under C-b. Material and magnetic traps agree: C3 cannot produce their 2.2 s split. If false, LiNA reads ≈ 878 s, and a PERKEO-like Nab λ bounds Br_X below 0.25%.
evidence for:
- On the a route, Br_X = 1.32 ± 0.36% (aSPECT 2024) or 1.06 ± 0.33% (a group), consistent with the needed 1.11% [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_sm_tau.py; M-CONSTRAINTS-03, M-DECOMPOSER-09 verified]. That world closes unitarity at +0.1σ [M-CONSTRAINTS-04].
- [new: Beck et al., PRL 132, 102501 (2024), arXiv:2308.16170, ACCESS full-text, "With 2.82σ, the Fierz interference term b(c) obtained de- viates from zero"] (for the combined PERKEO III + aSPECT fit).
- The invisible channels are untested in the laboratory [D-87], and the neutron-star bound is model-dependent [D-77, D-88].
evidence against:
- The A route gives Br_X = 0.077 ± 0.106%, one-sided 95% upper limit 0.25%, with the needed value 9.5–10σ away. PDG-average λ gives an upper limit of 0.51% (4.9σ) [M-EXAMINER-06, M-CONSTRAINTS-03, M-STATISTICIAN-11 verified; consistent with D-82].
- J-PARC 877.2 s is 2.15–2.24σ below C3's ≈ 888 s: likelihood ratio ≈ 10–12 : 1, 4.5–5 : 1 inflated [M-CONSTRAINTS-11, M-STATISTICIAN-06].
- Minimal dark decay collapses neutron stars to M_max = 0.69–0.70 M☉, against ~2 M☉ observed [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_nstar.py; M-CONSTRAINTS-09 verified for the collapse; D-88].
- Single-χ mixing with m_χ < m_H: the math check corrects the rate prefactor to 1/(128π). A 1.113% branch then needs θ = 2.7–6.5×10⁻¹⁰, giving τ_H = 0.06–0.9×10²⁹ s, below the ≳ 10²⁹ s bound by 1.1–17×, not "marginal" as the lens wrote [M-CONSTRAINTS-08 refuted the lens; McKeen's formula taken as quoted]. This strengthens the case against those variants.
- The o-Ps precedent: the proposed invisible decay was wrong there [empiricist F2–F3]. None of the 7 sourced precedents ended in new physics [empiricist].
- χ² ledger: 28.17/8 without an SM input and 41.27/9 with the A route [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_consistency.py; M-CONSTRAINTS-14 unverified].
decisive test: LiNA (J-PARC, Mishima; solenoid TPC; ~1 s; background expected to fall ×50; commissioned Feb 2024; no result date) [D-102]. C3 predicts ≈ 888 s. A reading of 888 ± 1 s would be 8.8σ from the storage pole. A reading of 878 ± 1 s would be only 4.2σ from the proton pole (3.9σ from BL1), because BL1's error caps that side until BL2/BL3 shrink it [M-STATISTICIAN-14, M-EXAMINER-11]. Co-decisive: Nab a at 0.04%, since C3 needs an aSPECT-like λ [D-107]; and UCNProBe (β rate ≈ 888 s against storage ≈ 878 s) [D-106].

## C4: Neutron–mirror-neutron conversion in the 4.6–5 T proton-trap field removes about 1.1% of beam neutrons, lengthening the proton-beam lifetime; bottles and J-PARC read the true value (speculative).
type: explanation
from: STATISTICIAN-D, EMPIRICIST-D, MECHANIST-D, EXAMINER-E, DECOMPOSER-D, DIAL-D, CONSTRAINTS-D
argument:
- Mechanism (SPECULATIVE; Berezhiani, two-level mixing with Landau–Zener passage). A mirror neutron with Δm ≈ 280 neV comes into resonance at B_res = 4.64 T (|µn| = 60.3 neV/T) inside the trap [D-05, D-56, D-89].
  - P_trap ≈ 1.13–1.14% needs θ0 = 1.0–2.2×10⁻³, depending on the solenoid profile (1.66×10⁻³ in the lens's profile) [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-mechanist_nnprime_jparc.py; M-MECHANIST-09 verified, profile-dependent].
  - The monitor field is weak, so P_det ≈ 5.5×10⁻⁶. The beam therefore reads long.
  - Δm must lie within ≲ 20–40 neV above |µn|B_centre. Below that the beam crosses resonance before the monitor and reads *short*. The sign is verified; the size is model-dependent: −19 to −25 s at 260 neV in the check, against −9 s in the lens [M-MECHANIST-10].
- Variants (sub-hypotheses):
  - **D-strong:** Berezhiani, as above.
  - **D-Tan:** Tan's inverse variant. Wall-bounce conversion shortens the bottles and the beam is true [D-96].
  - **D-weak:** mirror-field (B′) and peV-splitting variants [D-63, D-64].
- Every current lifetime class predicts the same as under C1: the strong-field and proton-counting partitions have identical members [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-statistician_combination.py; examiner F3; decomposer F4].
- Shift by class: proton beam +9.9 s. J-PARC < 0.01 s. Material bottles: a per-bounce loss of 5.5×10⁻⁶ that the size extrapolation removes. Magnetic traps ≈ 0 [M-MECHANIST-11].
- Weakest link: SNS regeneration.
predictions: If true, a BL-type beam run at a different trap field (for example 3 T against 4.6 T) shifts by several seconds or reverses sign. A regeneration signal of ~P² ≈ 1.3×10⁻⁴ appears at SNS, assuming equal conversion per passage. Every material bottle has a per-bounce loss floor near 5.5×10⁻⁶. LiNA and J-PARC read ≈ 878 s, UCNProBe equals storage, and the SM A route holds. If false, the proton-beam lifetime shows no field dependence.
evidence for:
- The pattern matches the data: beam long, while J-PARC, the bottles and the A-route τ_β sit near 878 s [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-mechanist_nnprime_jparc.py].
- Whether every field-profile or attenuation variant is closed by the SNS search was not established [D-89; dossier §6].
evidence against:
- The SNS 6.6 T regeneration limit, p < 2.5×10⁻⁸, excludes Δm > 10 neV [D-62, D-89]. With equal passages that caps P at ≤ 1.6×10⁻⁴ per passage, 70× too small, and caps the beam shift at ≈ 0.14 s [M-CONSTRAINTS-13, M-MECHANIST-11 verified as arithmetic; the equal-passage premise is unverified, and the exclusion itself rests on the source].
- Berezhiani's own worked example gives P_trap = 0.0043, a τ ratio of 1.0043 against the 1.0113 needed [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_consistency.py; profile-dependent, not re-derived in M-CONSTRAINTS-13].
- Δm needs fine tuning. UCN anomalous-loss limits exclude θ0 ≳ 10⁻³ for Δm ≲ 60 neV [D-89].
- D-Tan predicts UCNτ and J-PARC ≈ 888 s (contradicted [D-27, D-23]) and fails the A-route exotic-branch bound by 9.8σ [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_sm_tau.py].
- D-weak: PSI excludes the claimed weak-field anomaly region in 99.98% of 4π at 95% CL [D-63, D-90].
- The Berezhiani–Tan sign conflict dissolves because both variants fall [dialectician; D-79].
decisive test: A proton-counting lifetime run at two trap fields (NIST BL2/BL3; the dossier gives no date). Under C4 a ~10 s effect would shift by far more than a < 1 s error; under C1 it would not move. Or: a regeneration search reproducing BL1's 4.6–5 T field profile with sensitivity P < 10⁻⁴ per passage (the SNS n → n′ group [D-62]).

## C5: A baryon-number-violating branch n → X⁺e⁻ν̄ of about 1.1% yields an electron but no proton, so proton counting reads long while electron counting and bottles read true (speculative).
type: explanation
from: CONSTRAINTS-E, DECOMPOSER-H, MECHANIST-G (its X⁺ part)
argument:
- Mechanism (SPECULATIVE; Veselský, Moustakidis et al. 2025, arXiv:2507.17340, preprint, unchecked). In n → X⁺e⁻ν̄ with X⁺ → 2A⁰ + e⁺, every decay yields an electron, but ~1% yield no proton [D-95].
  - It gives up baryon-number conservation and needs a charged X⁺ that has not been seen [D-95; constraints F18].
  - It is the only candidate that fits proton beam ≈ 888 s and J-PARC ≈ bottles while keeping the proton-beam value equal to the true Γ(n → p e ν̄).
- It therefore needs the SM τ_β to equal ≈ 887.7 s, i.e. the a-route λ [decomposer F15].
- Shift by class: proton beam +9.9 s (long). J-PARC, bottles and UCNProBe unchanged.
- Weakest link: the λ route, and the unseen X⁺.
predictions: If true, BL2/BL3 read ≈ 888 s with no dependence on field, gas or trap time. LiNA and J-PARC read ≈ 878 s. UCNProBe's β rate equals its storage rate, ≈ 878 s. Nab gives |λ| ≈ 1.2668. Extra positrons or charged X⁺ tracks appear in the J-PARC/LiNA TPC. If false, Nab is PERKEO-like, or BL2 reads ≈ 878 s.
evidence for: J-PARC ≈ bottle, which C3 cannot accommodate [D-23]. The a-route τ_β of 887.21 ± 2.93 s matches the proton beam [M-CONSTRAINTS-02].
evidence against:
- The A-route τ_β (878.70 ± 0.83 s) fails the required Γ(p e ν̄) = 1/887.7 s⁻¹ at 3.8σ [M-CONSTRAINTS-03 verified].
- χ² ledger 40.94/9 with the A route [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_consistency.py; M-CONSTRAINTS-14 unverified].
- The preprint itself asks "why such charged particle is not seen" [D-95]. It is unchecked, and baryon-number violation is costly.
decisive test: Nab's a coefficient (ORNL; Δλ/|λ| ≈ 0.04%) [D-107]. A PERKEO-like λ excludes C5 at ≈ 3.8σ on the SM route alone [M-CONSTRAINTS-05]. The unique signature of C5 is the combination BL2 ≈ 888 s, LiNA ≈ 878 s and UCNProBe ≈ 878 s, plus a charged-track or extra-positron search in the J-PARC TPC data (precision and date not computed).

## C6: The β-decay rate of recently produced beam neutrons differs from that of stored UCN (an excited neutron state n* or a field dependence), lengthening beam lifetimes (speculative).
type: explanation
from: MECHANIST-G (its excited-neutron and SM field-dependence parts)
argument:
- Mechanism: the rate depends on the neutron's history or environment, not on an extra final state. Sub-hypotheses:
  - **F-n\* (SPECULATIVE; Koch–Hummel).** An excited state n* with a longer β lifetime that de-excites faster than UCN holding times [D-97]. Stored UCN would decay at the true rate, while beam neutrons (milliseconds after production) would decay more slowly.
  - **F-field (SM).** A field dependence of the decay rate. The Zeeman energy is 3.6–3.9×10⁻¹³ of Q at 4.6–5 T. That falls short of the 1.14% needed by ~3×10¹⁰ (~6×10⁹ with Γ ∝ Q⁵). M-MECHANIST-13 corrects the lens's "10¹³ too small"; the elimination stands [D-05].
- Because the ground-state β rate is unchanged, the SM A route (τ_β ≈ 878.5 s) agrees with storage.
- Not computed by any lens:
  - whether n* survives the flight to J-PARC's decay volume. If it does, electron counting should also read long (the slate builder's inference from D-97's definition; unchecked);
  - the shift in each beam as a function of flight time.
- Weakest link: partial exclusion by UCNτ holding-time and loading-time data [D-93].
predictions: If F-n* is true, the beam lifetime depends on the time since production, i.e. on the flight path or velocity [mechanist MECHANIST-G]. Bottles are unaffected. The SM A route agrees with storage. UCNτ's holding-time and loading-time data are the existing storage-side test [D-93]. The J-PARC/LiNA prediction is not computed. If false, beam lifetimes show no dependence on flight time.
evidence for: The ground-state τ_β on the A route agrees with storage, so C6 does not contradict the λ route [U-01]. F-n* is only partly excluded [D-93].
evidence against:
- UCNτ holding-time (20–4000 s) and loading-time (150, 300 s) data exclude part of the n* parameter space (Blatnik et al., preprint; region size not read). Nab's Dalitz-plot paper (PRC 113, 035501, 2026) constrains it too, but its limit was not read [D-93].
- F-field is eliminated [M-MECHANIST-13].
- Only one lens supports C6.
decisive test: A beam lifetime measured against flight time since production (a pulsed or velocity-selected beam; J-PARC/LiNA or BL2/BL3 with different flight paths), together with a full reading of the Blatnik and Nab n* exclusion regions [D-93]. Required precision and timing not computed.

## C7: No single dominant cause: a statistical fluctuation plus several modestly underestimated uncertainties (BL1, J-PARC, material bottles), none of which dominates, produce the gap.
type: null
from: STATISTICIAN-E, EMPIRICIST-E, MECHANIST-F, EXAMINER-F, EXAMINER-B (its "several underestimated systematics, not one cause" clause), DECOMPOSER-E, DIAL-E, CONSTRAINTS-F
argument:
- The pure-fluctuation form is effectively eliminated.
  - Local p₂ = 3.7×10⁻⁶ (4.63σ); globally 4.1–4.4σ over 3–10 partitions [M-STATISTICIAN-02, -03 verified].
  - The maximum odds against a fluctuation are ~8000 : 1 [M-STATISTICIAN-13].
  - EXAMINER-F marks it eliminated (4.33σ after a 5-partition look-elsewhere correction) [M-EXAMINER-08].
- The live form is heavy tails plus diffuse error underestimation.
  - Under Bailey's ν = 2–4, P(> 4.63σ) = 0.010–0.044 [M-STATISTICIAN-12, M-EMPIRICIST-07].
  - The field's own scale factors are about 2: J-PARC S = 2.29, storage S = 1.85, material S = 1.43 [M-STATISTICIAN-01, -05].
  - Inflating BL1's error by 1.5×, 2× or 2.3× gives 2.92σ, 2.19σ or 1.91σ against UCNτ [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-dialectician_syntheses.py; M-DIALECTICIAN-08 verified].
  - An extra 4.35 s systematic on one side brings the gap to 2σ [M-STATISTICIAN-08].
- Independent tensions exist:
  - proton against rest, 4.7σ;
  - material against magnetic, 2.95σ scaled (3.88σ unscaled). Its missing rate is only 2.9–4.1×10⁻⁶ s⁻¹; M-EXAMINER-12 corrects the examiner's 4.8×10⁻⁶ s⁻¹, which is Gravitrap against UCNτ;
  - λ from A against λ from a, 3.5σ.
  The non-proton results alone have χ² 23.4/7 (S = 1.83) [M-EXAMINER-01, M-EXAMINER-02]. Every single-cause fit leaves χ² ≈ 23 of storage-internal scatter [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_consistency.py; M-CONSTRAINTS-14 unverified].
- Within BL1, charge exchange (≈ 2.6 s at most if every ion were lost; < 0.5 s by Caylor's worst case), a mis-scaled nonlinearity or absorption correction, and halo could each contribute 1–3σ with the same sign [mechanist F-null; decomposer F13].
- Shift by class: scattered. BL1 +3 to +6 s, J-PARC ±several s by run condition, material +2 s, magnetic ≈ 0.
predictions: If true, BL2/BL3 land between the poles (for example 880–886 s) with no identifiable effect or trend. LiNA, τSPECT and UCNτ+ scatter by about ±3 s with no class pattern. Class means converge slowly as errors are re-assessed, and no single correction is ever published that moves BL1 by ≈ 10 s. If false, BL2 lands at one pole with an identified effect.
evidence for: The heavy-tail base rate [new: Bailey 2017, ACCESS full-text; M-STATISTICIAN-12]. Internal scatter inside J-PARC [D-24] and inside storage [M-STATISTICIAN-09]. The λ split [M-STATISTICIAN-10]. No named effect reaches the gap on either side [C1, C2].
evidence against:
- The disagreement is structured by class: with four classes the between-class χ² is 38.0/3 (5.55σ) and the within-class χ² only 8.4/7 (p = 0.30) [M-STATISTICIAN-04 verified].
- Uniform inflation needs 2.35× on every error to reach 2σ, but that would also inflate the small within-class χ² [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-statistician_combination.py].
- Every proton-counting result is high and every non-proton result low, which a random spread does not produce [constraints F16].
- Mechanistically it needs at least three unrelated BL1 items, each 2–4× their errors, all with the same sign [mechanist MECHANIST-F].
decisive test: BL2 (< 1 s) and BL3 (0.3 s) together with LiNA (~1 s) and τSPECT (< 0.3 s) [D-100–D-103]. C7 predicts BL2/BL3 at an intermediate value with no named correction, and the non-proton methods scattering without a class pattern. The significance with which an intermediate reading would exclude both poles was not computed.

## C8: Beam versus bottle is the wrong partition: the split is proton-detecting measurements (essentially BL1, plus aSPECT's λ) versus all others, with one proton-side cause behind both lifetime and λ tensions.
type: reframe
from: CONSTRAINTS-G, DECOMPOSER-G, DIAL-F, STATISTICIAN-F, EMPIRICIST-F, MECHANIST-E, DECOMPOSER-F, EXAMINER-B (its "three tensions, not one puzzle" premise critique)
argument:
- Doubtful premise 2 ("beam against bottle" is the right partition). It is false as stated: J-PARC is a beam and reads like a bottle. Proton counting against the rest beats beam against bottle by Δχ² = 5.3 [M-STATISTICIAN-04, M-EXAMINER-01]. In current data the strong-field partition has exactly the same members [examiner F3].
- Doubtful premise 6 (the SM arbitrates independently). It is false as stated:
  - The λ split maps one-to-one onto the lifetime split: Δλ = 0.0094 corresponds to 10.9–11.0 s in τ_β, against the 9.9 s gap [M-DECOMPOSER-07, M-CONSTRAINTS-02 verified].
  - Two closed worlds are self-consistent. Bottle τ with A-route λ gives a unitarity sum at −1.2σ; beam τ with a-route λ gives +0.1σ. The mixed pairings fail at 3–5σ [M-CONSTRAINTS-04, M-DECOMPOSER-08 verified].
- The pattern:
  - Every beam-like result detects decay protons: BL1 and Sussex–ILL count them absolutely after ~30 kV acceleration onto Si; aSPECT measures the proton recoil spectrum.
  - Every bottle-like result uses electrons or surviving UCN: PERKEO II and III, UCNA, J-PARC, UCNτ, Gravitrap.
  - The one exception is aCORN (electron–proton coincidence), at 874.86 ± 7.07 s, too imprecise to count [U-01; constraints F4].
- **R-strong (the candidate).** One proton-detection-side cause biases both an absolute proton count and a recoil-spectrum shape. No physical effect linking the two observables has been identified; DECOMPOSER-G and DIAL-F rate it strained, and CONSTRAINTS-G and STATISTICIAN-F rate the partition surviving.
- **R-weak ("BL1 against everything", the brief's own suggested reframe).**
  - The > 3σ gap is one 2005 dataset against a replicated non-proton cluster. UCNτ carries ~73% of the storage weight [M-EXAMINER-09], so structurally it is one experiment against one.
  - J-PARC is a ~2σ arbiter with a pressure/SFC split.
  - Storage and λ carry separate tensions.
  - R-weak names no new cause. If the refuters narrow C8 to it, it reduces to C1's A-BL1 sub-hypothesis plus the null's residual tensions.
- What the reframe gives up: the SM route as an independent arbiter, and "which single number is right" as the question. Settling it needs a pair of measurements: a non-proton absolute rate and a new a coefficient [examiner premise 11].
- Shift by class under R-strong: proton-counting beam +9.9 s; aSPECT-type a-coefficient |a| low by ≈ 2.7% (a = −0.10402 measured against −0.10687 predicted from PERKEO III λ, 3.48σ) [M-DIALECTICIAN-05 verified]. Everything else is true.
predictions: If R-strong is true, a new proton-detecting a measurement (Nab, proton time-of-flight in Si) sides with aSPECT (a ≈ −0.1040, b ≈ 0), while LiNA and UCNProBe read ≈ 878 s and BL2/BL3 move toward 878 s once the proton-side effect is found. If Nab gives a ≈ −0.1069 (PERKEO-like), the proton-detection link is broken and C8 collapses to R-weak, i.e. to C1. Under C3, by contrast, an aSPECT-like Nab comes with LiNA ≈ 888 s.
evidence for: The partition statistics [M-STATISTICIAN-04]. The two-worlds closure [M-CONSTRAINTS-04]. The same proton/non-proton split appears in λ (2.9–3.5σ between routes) [M-STATISTICIAN-10]. Without BL1 the gap is 2.2σ [M-EMPIRICIST-03].
evidence against:
- No mechanism links an absolute proton count after post-acceleration with a recoil-spectrum shape [decomposer F8; dialectician II].
- aCORN, another proton-involving λ measurement, goes the other way, though at low weight [D-41].
- The a-route rests on essentially one experiment, aSPECT [decomposer F12].
- The "BL1 alone" partition fits slightly worse than the proton-counting one (Δχ² ≈ 5 within, under 2.3σ) [M-STATISTICIAN-04].
decisive test: Nab's a (ORNL SNS; Δλ/|λ| ≈ 0.04% goal; upgraded for precision running Nov 2025; no a value yet) [D-107], read together with LiNA or UCNProBe [D-102, D-106]. At 0.04%, an aSPECT-like Nab result sits 12.7–13σ from the A route, and a PERKEO-like one sits 3.5σ from aSPECT [M-CONSTRAINTS-05, M-DECOMPOSER-10]. R-strong alone predicts "Nab aSPECT-like and LiNA ≈ 878 s".

## Prediction matrix
Observed, for reference:
- proton beam 887.97 ± 2.04 s (BL1 887.7 ± 2.25 s);
- J-PARC 877.2 +4.35/−3.98 s (preprint);
- material bottles 880.03 ± 0.70 s (scaled);
- magnetic traps 877.82 ± 0.27 s;
- in-bottle β counting: no result yet;
- space 887 ± 14 s;
- SM τ_β 878.70 ± 0.83 s on the A route and 887.21 ± 2.93 s on the a route;
- direct searches null;
- neutron stars observed up to ~2 M☉.

Sources: [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-statistician_combination.py] [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-constraints_sm_tau.py] [D-23, D-34, D-88].

| Candidate | Proton-counting beam (BL1; BL2/BL3) | Electron-counting beam (J-PARC 2024; LiNA) | Material bottles | Magnetic traps (UCNτ; τSPECT, UCNτ+) | In-bottle β counting (UCNProBe) | Space-based (Lunar Prospector, MESSENGER) | SM τ_β from λ, Vud (A route / a route; Nab) | Direct searches (n→χγ, n→χe⁺e⁻, n→n′, ¹¹Be) | Neutron-star bounds |
|---|---|---|---|---|---|---|---|---|---|
| C1 proton-beam systematic | BL1 biased +9.6 to +9.9 s. BL2/BL3 ≈ 878 s (as built under A-BL1, after correction under A-gen). Under A2: 5 ms against 10 ms ≈ 5.1 s [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-mechanist_required_sizes.py; M-MECHANIST-04] | ≈ 878 s at every pressure. J-PARC 0.14σ from UCNτ ✓ [M-EXAMINER-03] | ≈ 878 s plus own scatter (880.03 observed; residual to C7) [M-STATISTICIAN-01] | ≈ 878 s ✓ | β rate = storage rate, ≈ 878 s [constraints matrix C] | uninformative at ±14 s [D-13, D-34] | A route 878.70 ± 0.83 s ✓; needs the a route wrong (3.2σ otherwise) [M-CONSTRAINTS-03]. Nab a ≈ −0.1069, \|λ\| ≈ 1.2764, b ≈ 0 | all null ✓ | no constraint |
| C2 common storage loss | ≈ 888 s (BL1 true); BL2/BL3 ≈ 888 s | ≈ 888 s; J-PARC 877.2 is 2.15–2.24σ against; needs a separate −10.8 s J-PARC artefact [M-MECHANIST-07] | reads short: loss 7.9×10⁻⁶ s⁻¹ in Gravitrap [M-DIALECTICIAN-07] | reads short: loss 1.27×10⁻⁵ s⁻¹, 130× UCNτ's depolarisation bound [M-MECHANIST-06]; τSPECT ≈ 888 (geometry-specific) or ≈ 878 (common) | β-rate lifetime ≈ 888 s against storage lifetime ≈ 878 s in the same trap [D-106; constraints matrix C] | uninformative [D-13] | needs τ_β ≈ 888: A route 3.8σ against; a route ✓ [M-CONSTRAINTS-03]; Nab \|λ\| ≈ 1.2668 | null | n/a |
| C3 invisible dark decay | ≈ 888 s = τ_β; BL2/BL3 ≈ 888 s with no field, gas or trap-time dependence | ≈ 888 s (no electron); J-PARC 2.15–2.24σ against, likelihood ratio 10–12 : 1 (4.5–5 : 1 inflated) [M-CONSTRAINTS-11, M-STATISTICIAN-06] | ≈ 878 s (true τn); cannot produce the material–magnetic split | ≈ 878 s ✓ | β-rate lifetime ≈ 888 s against storage lifetime ≈ 878 s [constraints matrix C] | uninformative [D-13] | needs Br_X ≈ 1.1%: A-route upper limit 0.25% (needed value 9.5–10σ away); a route 1.32 ± 0.36% ✓; Fierz escape b ≈ −0.0158 (1.6σ from b = 0.017(21)) [M-CONSTRAINTS-03, -06]; Nab \|λ\| ≈ 1.2668 | χγ excluded in the DM window; χe⁺e⁻ open only for T_ee < 32 keV (5.8% of the window); invisible modes untested [D-85–D-87; M-CONSTRAINTS-07]; ¹¹Be ceiling 2×10⁻⁴ applies below 939.064 MeV; H → χν below its bound for single-χ mixing [M-CONSTRAINTS-08] | free χ: M_max 0.69–0.70 M☉ ✗; escape needs χ–χ repulsion with m_V/g ≲ 50–100 MeV (EOS-dependent) [M-CONSTRAINTS-09] |
| C4 strong-field n → n′ | ≈ 888 s, depends on field; sign reverses if Δm sits below µB_centre [M-MECHANIST-10]; BL at 3 T against 4.6 T shows a large shift | ≈ 878 s (shift < 0.01 s) ✓ [M-MECHANIST-11] | ≈ 878 s after extrapolation; per-bounce loss floor 5.5×10⁻⁶ [M-MECHANIST-11] | ≈ 878 s (no crossing below 4.64 T) | = storage, ≈ 878 s | uninformative at ±14 s [D-13] | A route ✓ (τ_β ≈ 878.5 s) | SNS regeneration must show ~1.3×10⁻⁴ against a limit of 2.5×10⁻⁸ ✗ (P needed 70× the cap) [D-62; M-CONSTRAINTS-13]; PSI weak-field anomaly region excluded [D-63] | pulsar and NS-cooling bounds model-dependent [D-91] |
| C5 electron-always X⁺ branch | ≈ 888 s; BL2/BL3 ≈ 888 s | ≈ 878 s (electrons always) ✓ | ≈ 878 s | ≈ 878 s | ≈ 878 s (electrons always) [constraints matrix C] | uninformative at ±14 s [D-13] | needs Γ(p e ν̄) = 1/887.7 s⁻¹: A route 3.8σ against; a route ✓ [M-CONSTRAINTS-03]; Nab \|λ\| ≈ 1.2668 | charged X⁺ not seen [D-95]; charged-track or extra-e⁺ search in the TPC not computed | not computed |
| C6 state- or field-dependent rate (n*) | long by an amount depending on time since production (not computed); field variant eliminated (short by ~3×10¹⁰) [M-MECHANIST-13] | not computed (long if n* survives the flight; slate builder's inference from D-97) | ≈ 878 s (n* de-excited) | ≈ 878 s; UCNτ holding and loading data partly exclude n* [D-93] | = storage, ≈ 878 s (not computed) | uninformative at ±14 s [D-13] | A route ✓ (ground-state rate unchanged) | Nab Dalitz and UCNτ limits on n* (values not read) [D-93] | not computed |
| C7 null (no dominant cause) | BL2/BL3 in between (~880–886 s), no trend | 878–890 s depending on pressure/SFC [calc: runs/2026-09-30-neutron-lifetime-beam-bottle/calc/lens-dialectician_syntheses.py] | 878–882 s | 877–880 s | ≈ storage, 878–882 s [empiricist matrix] | uninformative [D-13] | either route; no class pattern | null | n/a |
| C8 reframe: proton-detecting vs rest (R-strong) | BL1 and Sussex–ILL biased by the proton-side effect; BL2/BL3 → ≈ 878 s once it is found | ≈ 878 s ✓ | ≈ 878 s (own scatter to C7) | ≈ 878 s | ≈ 878 s | uninformative at ±14 s [D-13] | A route right; the aSPECT a biased (\|a\| low by 2.7%, 3.48σ) [M-DIALECTICIAN-05]; Nab (proton TOF) a ≈ −0.1040 under R-strong, or ≈ −0.1069 if R-weak | null | no constraint |
