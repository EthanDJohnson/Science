# Audit of report.md
status: final
| # | Report claim | Traced to | Status |
|---|---|---|---|
| 1 | Ellis phantom throat passes a light-speed signal with 28 e-folds to spare (62.5 available vs 34.5 needed at R = 10 b0) | falsifier-C1-0_ellis_lifetime.py.log: 62.47 available (1 kg), 34.47 needed; difference 28.0 | supported |
| 2 | Ghost-scalar light crossing 23.5–34.5 e-folds vs 58–80 available | falsifier-C4-0_ghost_lifetime.py.log (23.52; 58.2/62.5/80.1); C1-0 log (34.47) | supported |
| 3 | Slow 10 km/s crossing needs 1.1×10⁵ e-folds; ghost-scalar human throat b₀ ≈ 7×10⁶ m, ~4.7×10³ M☉ at ≥0.05c | C4-0 log: 1.113e5 e-folds; b0_min 6.8e6 m, 4.6e3 M☉, v_min 0.0502c | supported |
| 4 | SM-MMP is 24.2–29.1 orders short of 1 kg binding energy | falsifier-C2-0 log: log10 = −29.10 (N=1), −25.63 (N=54); lens-engineer_cost_table.py.log gives 25.6; 24.2 follows from the g=0.30, N=54 row (5.23e-8 J vs 8.99e16 J), not printed directly | supported |
| 5 | Field gap 34.2 orders (1.76×10³⁷ T vs 1200 T); formation 4.8×10²⁵ J = 8×10⁴ yr world energy; 2.7×10⁸ kg per mouth; |E_min| 4.5 MeV–13 GeV; T < 0.3–17 mK | lens-engineer_cost_table.py.log, section 3 | supported (1200 T anchor is a search summary, as the report says) |
| 6 | Classical throat vs Casimir 38–57 orders; negative mass 1.35–2.7×10²⁷ kg/m; QI band ≤ 1.84×10⁻²¹ m; 1.6×10⁶² species | cost_table log (38.0–56.6; 2.69e27 kg); C3-2_scale log (w = 1.841e-21 m; N_min 1.603e62) | supported |
| 7 | Free-field throat a_max = 4.9×10³ √N l_P; 7.9×10⁻³¹ m at N = 100 | falsifier-C3-2_scale.py.log (4.886e3; 7.897e-31 m) | supported |
| 8 | EDM gap 15.8–21.9 orders in q/μ; fermion 7×10¹⁷–4×10¹⁸ GeV | cost_table log: gaps 15.6–21.9; masses 6.95e17–3.70e18 GeV. The 15.8 figure appears in no log or math row | contradicted (minor: lower end is 15.6) |
| 9 | EDM throats 1.2–8.1×10⁻³³ m | cost_table log (Kain 75–500 l_P) | supported |
| 10 | Dirac sector violates NEC at any flare-out throat (G_kk = −2r″/r, Maxwell T_kk = 0); BKR "not solutions", Kain collapse, Weinbaum partial, Dzhunushaliev negative frequency | verdicts/C5-0.md, C5-1.md, falsifier-C5-0_edm_nec.py.log; critiques are full-text per report | supported |
| 11 | Thresholds Δ_s = T_thru − d/c, Δ_CTC = T_thru + d/c; MM at d = 1000 ly gives 8.4×10³ and 1.04×10⁴ yr; verified six times | M-MECHANIST-01/02, M-DECOMPOSER-01/03 (verified) | supported |
| 12 | "20,000 random cases" re-check of thresholds | verdicts/C7-0.md and cruxes/C7.md state it. M-MECHANIST-01 itself reports 2000 random cases. No separate log was found | weak (self-reported by one refuter) |
| 13 | Toy equilibrium lost at 0.25–0.56 Δ_s; closing-ray negative null energy shrinks (M-MECHANIST-05/06 refuted, corrected) | math/mechanist.md (corrected range 0.25–0.56) | supported |
| 14 | MM reaches Δ_s in 10⁷–10⁸ yr at β ≤ 0.03; 18 orders inside 3×10²⁶ yr; mouth mass 2×10³⁴ kg, ≥10⁴⁹ J | M-MECHANIST-03 (0.1c: 9×10⁴⁸ J, 1.7×10⁶ yr); the β ≤ 0.03 circuit is from the C7-2 log (not re-opened) | weak (partly unopened) |
| 15 | M-DECOMPOSER-08 refuted: point-mouth bridge fails for misaligned mouths; finite-mouth line thresholds L* = 1.16–1.20 d at a = 0.1d; band ≤ 1.5a/c = 0.075 s for MM | math/decomposer.md; falsifier-C6-2_finite_mouth_line.py.log (1.2000, 1.1643; 1.50 a; 7.498e-2 s) | supported |
| 16 | Ellis: T_thru = 6.64×10⁻⁸ s; ratios 2.0×10⁻², 1.3×10⁻¹⁰, 2.1×10⁻¹⁵ | M-DECOMPOSER-05 verified | supported |
| 17 | MM: T_thru = 9.42×10³ yr, ratio π at d = ℓ, τ = 0.157 s | M-DECOMPOSER-06, M-EXAMINER-04 | supported |
| 18 | Processor test: N = 20 is 1.5–2.1 orders in gate error; N = 50–100 is 2.3–3.5; required 3.5×10⁻⁶–2.3×10⁻⁵ | falsifier-C8-2_scale.py.log: N=20 sourced 1.49–2.11; N=50 2.28–2.91; N=100 up to 3.51 | supported |
| 19 | MQ transfer faster by (J/μ)^{1/3} | C8-2 log, section 4 | supported |
| 20 | Gate error demonstrated 4.2×10⁻³ (2022), 2.2×10⁻³ (2025); Byun N = 8 and Granet are preprints | C8-2 log; the report labels these preprints | weak (preprints) |
| 21 | Residual band and finite-mouth results hold only in flat exteriors | the report states this; C6-2 log is flat-exterior only | supported |
| 22 | SM-MMP capacity 8.8–2.6×10⁴ electrons, 2.6×10¹³–1.4×10¹⁵ gap quanta | falsifier-C2-0/1/2_capacity.py.log (|E_min| ratio −29.10 and −25.63 confirmed; quanta counts not individually re-read) | weak (partly unopened) |
| 23 | Flat-space QIs inapplicable: sampling time exceeds l_B by 3.3×10⁵–2.8×10¹⁸ | M-CONSTRAINTS-10 (verified with the lower-end correction) | supported |
| 24 | MQ ANEC −φ_r/(4πG) | M-CONSTRAINTS-11: normalisation not checked, as the report says | supported (caveat stated) |
| 25 | Radial ANEC of any static two-ended throat strictly negative (M-CONSTRAINTS-02 verified); Ellis ANEC −E/(8b₀) | M-CONSTRAINTS-01/02 verified; C3-2 log: −1/(8a), 1.51×10⁴³ J/m² | supported |
| 26 | M-IDEALIZER-07 (refuted) removed the "universal cost floor" wording | math/idealizer.md row 11 refuted | supported |
| 27 | MM 1 g criterion throat 1.35×10⁸ m is scaling only | M-DECOMPOSER-09 refuted and corrected to 1.35e8 m | supported |
| 28 | Astronomical: S2 needs 10⁻⁶ m/s², achieved 4×10⁻⁴; EHT 21 µas vs 0.79 µas; echo 9.4×10³ yr vs 2 yr | cost_table log section 8 | supported |
| 29 | Candidate mutual exclusivity and probabilities | candidates.md: `exclusive: no`. Credences (0.90, 0.90, 0.85, 0.80, 0.80, 0.75, 0.15, 0.03) need not sum to 1 | supported (no sum check applies) |
| 30 | Casimir 0.27 J/m³ at 0.2 µm; 38 pK; 592 EJ/yr (5.92×10²⁰ J/yr) | cost_table log anchors | supported |

## Summary: 30 claims checked, 4 flagged; most serious: the EDM q/μ gap lower bound of 15.8 orders is not in the logs, which print 15.6 (minor). The other flags are weak, not wrong: the 20,000-case threshold re-check is a refuter's self-report, and the β ≤ 0.03 circuit timing and capacity quanta counts were not re-derived here. No candidate rests on refuted mathematics as corrected.
