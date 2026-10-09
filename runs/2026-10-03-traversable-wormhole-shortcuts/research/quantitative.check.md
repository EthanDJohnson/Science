# Check: quantitative
status: final
Rechecked after the 2026-10-08 relaunch (RQ-08 and RQ-12 rewritten; RQ-19 to RQ-27 added). Rows RQ-01 to RQ-07, RQ-09, RQ-13 to RQ-18 carried from the earlier check of the unchanged claims.

| Claim | Verdict | Note |
|---|---|---|
| RQ-01 | verified | Eq. 3.26 quote matches via fetch_text (20g, size 0.5 m, r_e > 1.5e7 m ~ .05 s). sqrt(0.5 c^2/(20*9.8)) = 1.5e7 m. |
| RQ-02 | verified | Eq. 3.27 quote matches exactly (r_e .05 s, c_2 7e72, ell 3e3 ly, gamma 2e12, E_bin -5e9 kg). |
| RQ-03 | verified | "always longer than through the outside, pi*ell > d" and proper time ~ pi*r_e confirmed. "Tens of thousands of years" vs pi*3e3 ly = 9.4e3 yr is the paper's loose rounding; the claim notes this. |
| RQ-04 | verified | Eq. 2.16 quote matches (N_f > 1e52). Eq. 2.15 scaling not separately checked. |
| RQ-05 | verified | Refrigerator/CMB quote matches; "exceedingly impractical" is a fair paraphrase of "exceedingly difficult". |
| RQ-06 | verified | Eq. 2.5 form consistent with the paper; M_e = r_e c^2/G = 2.0e34 kg arithmetic correct. |
| RQ-07 | verified | Abstract quote matches; gloss about ANEC still required is consistent with the paper's intro. |
| RQ-08 | verified | Rewrite fixes the earlier problem. Ford-Roman Conclusions quote ("only slightly larger than the Planck length", p. 22) and the scope ("much smaller than the minimum local radius of curvature and/or the distance to any boundaries") match gr-qc/9510071. Eq. 69 and the 1 m / 1 ly / 1e5 ly figures (1e14 lp, 2e19 lp = 0.2 fermi, 1e21 lp = 1e-14 m) match p. 16. Own arithmetic: (r0/(8 f^4 lp))^(1/3) lp at r0 = 1 m gives 9.2e13 lp. Kontou "would not be traversable" quote matches (p. 25); it refers to a generic Planck-scale throat. The r0 <~ lp/f^2 and lp/(2f^2) equations (eq. 51, 91) were not re-grepped; the claim labels them as such. |
| RQ-09 | verified | Three-kind list quoted exactly (Kontou p. 13). |
| RQ-12 | verified | Rewritten as secondary. Weinstein abstract wording ("sparse N = 7 SYK model with 5 terms") matches the INSPIRE abstract; Brown et al. "7 and 6 qubits" and 80% (Quantinuum, no mitigation) match arXiv 2205.14081; Jafferis reply sentence matches arXiv 2303.15423. The Kobrin quote was verified earlier. N=7 and 5 terms remain secondary-source only; the claim says so. Note IBM fidelity was 20% (+15% mitigated), the 80% is Quantinuum only; the claim's "about 80%" for both machines is loose. |
| RQ-13 | verified | Quote verified earlier (r_0, Q_e < r_0, Q_e/M > 1). The closed-form M formula was not seen in the grep; mu scaling is labelled inference. |
| RQ-14 | verified | KZ quote matches. Negative ADM mass applies to solutions near the critical line, not smooth solutions in general (minor scope tightening). |
| RQ-15 | verified | t_min = d + logs quote and d^{3/2} merger time confirmed. Journal ref not checked. |
| RQ-16 | verified | Takahashi-Asada abstract numbers match. 50,836 quasars and the Yoo et al. femtolensing numbers not checked. |
| RQ-17 | verified | Recomputed earlier: M_e 2.0e34 kg, 2.5e-25 ratio, gamma 1.9e12, pi*ell 9.4e3 yr, pi*r_e/c 0.157 s. All correct; q flagged illustrative. |
| RQ-18 | verified | Quote matches Kontou p. 15, but ref [78] unidentified; low confidence stands. |
| RQ-19 | verified | Kuhfittig quote matches (5e41 dyn/cm^2 (10 m/r0)^2; neutron star at 3 km). My arithmetic: (c^4/G)/(8 pi) = 4.82e42 Pa for b0 = 1 m; Omega = -2 b0 = -2.69e27 kg for 1 m (b0 c^2/G = 1.35e27 kg). The ANEC integral -E/(8 b0) was not independently re-derived. Own calculation, so source-level status is secondary as the claim says. |
| RQ-20 | verified | Recomputed sigma = -sqrt(1-2M/a)/(2 pi a) at a = 4430 m: -2.5e39 J/m^2; shell mass -6.9e30 kg. Matches. Poisson-Visser used only for method (abstract). |
| RQ-21 | verified | Fewster-Eveson eq. 5.5-5.6 quote matches (-27/(2048 pi^2 tau^4), 9/64 of Ford-Roman). SI restoration checked: 27/(2048 pi^2) hbar/(c^3 tau^4) = 5.2e-27 J/m^3 at 1 ns and 5.2e-3 at 1 fs. |
| RQ-22 | verified | Pfenning-Ford eq. 23 quote matches (Delta <= 1e2 v_b L_Planck for alpha = 1/10); 1e2 x 1.616e-35 = 1.6e-33 m. Carried from the warp run but re-found in the source. |
| RQ-23 | verified | MSY Discussion quote matches (p. 36). The gloss on the null window and "1 kg" payload is the author's own scope comment. |
| RQ-24 | verified | GJW footnote 8 quote ("Presumably there is some limit...") and the 3/2 Delta t eikonal statement match; Delta t formula appears just before p. 13 excerpt. Linearised Einstein equation not re-grepped. |
| RQ-25 | verified | Eq. 3.8 quote matches arXiv:1807.07917 p. 13. |
| RQ-26 | verified | MMP quote matches (p. 29, "r_E ~ q ... pi ell ∝ q^2"). Journal ref not checked. |
| RQ-27 | unverifiable | Morris-Thorne 1 g criterion is search-summary only, as the claim states. Own arithmetic sqrt(0.5 c^2/9.8) = 6.8e7 m is correct, but a naive scaling, not from the paper. |

## Summary
- verified: 25 (RQ-01 to RQ-09, RQ-12 to RQ-26)
- unverifiable: 1 (RQ-27, Morris-Thorne criterion; flagged low confidence by the author)
- contradicted / misattributed / status-wrong: 0
- Most serious issue: none material. Minor: RQ-12 attributes "about 80%" to both IBM and Quantinuum runs, but the 80% is Quantinuum only (IBM about 20%, 35% mitigated); RQ-18 rests on an unidentified reference; RQ-13 closed-form mass not seen in the text.
