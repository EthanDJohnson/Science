# Audit of report.md
status: final
| # | Report claim | Traced to | Status |
|---|---|---|---|
| 1 | Reference gap: SH0ES 73.49 vs CMB-SPA 67.19 = +6.30 ± 1.00, 6.27σ, 0.195 mag; H0DN 6.82σ; vs BAO+BBN 4.55σ | math/statistician.md M-STATISTICIAN-01 (z = 6.271, 6.816, 4.553) and M-04 (0.1946 mag), verified | supported |
| 2 | Probabilities sum to 1 (0.44+0.20+0.20+0.09+0.03+0.02+0.02) | Sum = 1.00; C7/C8 rank-only and excluded | supported |
| 3 | H0DN SN-step share +0.002 ± 0.047 mag (73.50 vs 73.434 ± 1.795) | calc/falsifier-C1-2_bounds.py.log lines 18-26 (0.0020; 0.0474/0.0582; 73.434 ± 1.795) | supported |
| 4 | H0DN no-SN 73.43 sits 2.8–2.9σ above 68.5 | falsifier-C1-2_bounds.py.log prints 2.75σ vs 68.50 (3.03σ vs 68.0). Rounds to 2.8; the "2.9" end is not printed, minor | supported |
| 5 | Non-SH0ES local mean 71.69 ± 1.14; 3.74σ (SPA), 2.49σ (BAO+BBN); 4.15σ vs SPT+ACT | M-EXAMINER-03 verified (3.743/2.494); 4.15 appears in verdicts/C8-2.md | supported |
| 6 | SN-free local set 72.39 ± 1.41, 3.32σ | M-STATISTICIAN-05 (72.385 ± 1.413, z = 3.316), verified | supported |
| 7 | One-step mean 71.27 ± 1.93, 1.9–2.1σ | M-STATISTICIAN-03 (1.882), M-EXAMINER-03 (2.07), verified | supported |
| 8 | Heavy-tail all-local excess 4.3–4.5σ, no-SN 3.1σ | M-STATISTICIAN-14 verified (4.26/4.47; no-SN 3.06–3.10) | supported |
| 9 | Sellke cap 4.7e7:1 "corrected" | M-STATISTICIAN-15 refuted the lens's 5.6e7 and gives 4.7e7 | supported |
| 10 | Base rate 0/12 single-team anomalies, Wilson upper 0.24 | calc/lens-empiricist_baserates.py.log line 23; M-EMPIRICIST-11 verified (0.2425) | supported |
| 11 | r_d needed 138.6 ± 1.8 (−5.7%) to 134.8 (−8.3%) | M-CONSTRAINTS-02 verified | supported |
| 12 | f_EDE needed 0.065–0.072 (midpoint) / 0.124–0.19 (full) | M-CONSTRAINTS-07 verified (0.1247–0.1899); the 0.065–0.072 midpoint figure traces to C3-0, not re-derived in math | supported |
| 13 | C2: ω_c −13.0 to −13.3% (13σ), ω_b ×1.26 | M-MECHANIST-06/07 (corrected numbers) | supported |
| 14 | C2: θ_* +1.73% at 58–60σ; BAO needs Ω_m 0.338 at 4.7–10σ; BBN 10.5–30σ | M-MECHANIST-05 and calc/falsifier-C2 logs cited; M-CONSTRAINTS-04 carries a caveat on the θ_* baseline (68.03 vs 67.35), not noted in the report | weak |
| 15 | C5: δ ≈ −0.46 to −0.51 over ≳430 h⁻¹ Mpc, 84σ; cosmic variance 0.31 km/s/Mpc, gap 18–20σ | M-CONSTRAINTS-12 verified (84σ); M-STATISTICIAN-11 (20.3, 16.7) | supported |
| 16 | GC age 13.81 ± 0.34 vs 12.66–12.89 Gyr (2.7–3.4σ) | M-CONSTRAINTS-06 verified (2.70/3.39σ) | supported |
| 17 | C6 balance window 69.43–70.60; P = 0.06–0.26 | calc/crux-C6_balance.py.log: window edges 69.43 and 70.6; weights 0.067–0.104 (flat), 0.261 (capped). The low end 0.06 is 0.067, and the "0.08–0.26" capped range is not fully visible in the printed lines | supported |
| 18 | Precision needed: 1.21 (5σ), 0.83, 0.45, 0.33 | M-CONSTRAINTS-15 (1.21); 0.83/0.45/0.33 from the cruxes, not separately math-checked | weak |
| 19 | Lenses for 5σ ≈ 50 (no floor), ≈ 79 (1% floor) | M-STATISTICIAN-12 verified (50.3, 78.7) | supported |
| 20 | SH0ES–CCHP: 11-of-42 subset scatters 0.84–1.31, so CCHP-JWST is a 1.9–3.0σ low draw | M-STATISTICIAN-09 verified; the report is faithful to the math note that the range mixes H0 choices | supported |
| 21 | Difference 2.5–3.1 is 1.4–2.4σ for ρ = 0–0.8 | M-STATISTICIAN-02 (1.443–2.356) | supported |
| 22 | Late-time inverse ladder 67.2–67.7 refutes smooth H(z) (M-CONSTRAINTS-10 verified) | M-CONSTRAINTS-10 verified, with a sign-convention caveat in constraints.md | supported |
| 23 | EDE fits: 71.0 ± 1.1 (Poulin 2026), 71.4 ± 1.4 (eROSITA, 3.2σ); f < 0.061, < 0.070 | dossier lines 100–101, 172; verdicts/C3-1.md. Published fits; some are preprints. The report's own caveats section flags this | supported |
| 24 | Lyα f < 0.03 (Goldstein 2023) | cited from dossier and C3-1; not re-checked in this audit | weak |
| 25 | C1 narrowed lever: Dong 2026 peculiar-velocity 0.087 mag | Single preprint; the report flags it as contested, cited from the dossier without a URL | weak |
| 26 | C4: Huang 73.4 ± 1.0, Kenworthy 73.1 +2.6/−2.3 | Dossier and C4-1; the report says the error budget is unverified | weak |
| 27 | Nájera 2026 offset 0.065 ± 0.039 mag, 1.65σ | Single preprint, flagged by the report | weak |
| 28 | "Math checks refuted seven lens numbers" | math/*.md contains 12 refuted rows (statistician 1, dialectician 3, mechanist 3, examiner 2, empiricist 2, decomposer 1). The report names only some, and several are minor numeric ones (M-DIALECTICIAN-03/13, M-EMPIRICIST-14). The count is understated, and none changes a candidate status | contradicted (count only) |
| 29 | Candidate verdicts: C2, C5 refuted; C4 smooth-H(z) and G-step excluded; C1 SN-step-only locus 3–4σ short | verdicts/C1-*, C2-*, C4-*, C5-* and the cruxes; consistent with calc logs | supported |
| 30 | C3 credence cites "advocate conceded stands behind C6", and C1 conceded in crux | cruxes/C3.md and cruxes/C1.md exist; consistent with the report's use of them | supported |

## Summary: 30 claims checked, 8 flagged; most serious: the report's "seven refuted lens numbers" understates the 12 refuted math rows (count only; no candidate status changes). Weak items are the single-preprint levers (Dong 2026, Nájera 2026, Huang), the Lyα bound, and the precision-needed figures that lack a math-check row.
