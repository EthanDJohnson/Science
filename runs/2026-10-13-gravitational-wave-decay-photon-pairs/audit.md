# Audit of report.md
status: final
| # | Report claim | Traced to | Status |
|---|---|---|---|
| 1 | Eq. 8 total per packet ≈ 2.93e-6 pairs (6.6e-6 at E = 3 M☉c²); rate 1.40e-4 /s | M-IDEALIZER-09 log (2.92671e-06); M-MECHANIST-05; falsifier-C1-2 log (1.3975e-04) | supported |
| 2 | Sustained reading over 410 Mpc gives 5.9e12 pairs; over-count 2.0e18 | M-DIALECTICIAN-01 log (5.897e12, 2.015e18); falsifier-C1-0 log | supported |
| 3 | τσ = 7.2e5 breaks B&O's validity condition | M-DIALECTICIAN-01 log (7.156e5) | supported |
| 4 | Bound A: 2.9e-6 pairs beyond λ, 4.6e-25 beyond 410 Mpc | crux-C2_discriminators log (2.911e-06); falsifier-C2-2 log (4.60e-25) | supported |
| 5 | Toy yield 0.0632 (kR)^-3 for l=2, m=2 | M-IDEALIZER-07/08 (math/idealizer.md, exact asymptote); no .log line printed this value | supported (math table; not in a calc log) |
| 6 | Ambient-background lifetime 5.2e124 s (ΔN_eff = 0.3) | falsifier-C2-0 log (5.24e124); C2-2 log (5.16e124); crux-C2 log (5.165e124) | supported |
| 7 | Eq. 14 rate 2.8e-109 pairs m^-3 s^-1 at ΔN_eff = 0.3; ≥ 1e71 below FIRAS | M-CONSTRAINTS-02 log (2.77e-109); the 1e71 FIRAS gap was not located in a grep | supported (rate); weak-to-supported (gap) |
| 8 | k = 67/(630π) = 0.0339; N_lin = 3.1e-4 pairs, ratio 107 | falsifier-C4-1, C5-0, C5-1, crux-C4 logs (0.033852; 3.143e-04; 107.4) | supported |
| 9 | C5-2 finite-source k 0.025–0.036 | C5-2 log shows 0.0339; the 0.025 end is not seen in the grep | weak |
| 10 | GW170817 chirp N_lin = 3.8e-5 vs 2.8e-8 (ratio 1.3e3) | C4-1 log cited; grep did not surface the line | weak (untraced in this audit) |
| 11 | Retarded/time-symmetric ratio 0.028 at σ/ω = 0.21; 2.9e-3 for circular (2,2) | falsifier-C3-2_bandwidth log (0.0282); C3-2_quadrupole log (2.906e-03) | supported |
| 12 | Monopole ratios 1/12 and 0.020 | M-EXAMINER-03 cited; not re-opened | weak (untraced in this audit) |
| 13 | Eq. 16: N_φ ≈ 6e87 confirmed at 5.75e87 | M-EMPIRICIST-01 log (5.753e87) | supported |
| 14 | ULDM: 1.32e12 s needed, 12 s in band, shortfall 9.2e-12 | M-EMPIRICIST-03 log (1.316e12; 9.18e-12) | supported |
| 15 | Best over binary masses 1.6 W·x_MW | verdicts/C8-2.md (1.6 W·x_MW at Mc = 7.5e9 M☉) | supported |
| 16 | Kinetic ceiling 1.6e-38 of R at 410 Mpc | falsifier-C1-2 log (1.5598e-38) | supported |
| 17 | Variant (b) would attenuate GW150914 by exp(−6.3e13) | M-CONSTRAINTS-14 log (6.33e13) | supported |
| 18 | h^(2)-only R/R at 90°: 8.26 vs full 0 | falsifier-C7-0 log (8.2604, full 4.7e-31, i.e. numerically 0) | supported |
| 19 | Two-beam rate ω⁴h⁴(1−cos θ)²/(1280π c³) | M-MECHANIST-03 (verified) | supported |
| 20 | Eq. 6 amplitudes confirmed (KLT to 7e-15) | M-MECHANIST-01 (verified) | supported |
| 21 | Eq. 7 "per-axis range [0, 12/7]× B&O" with "corrected form" | M-MECHANIST-02 is refuted. The report acknowledges this and uses the corrected form, which the check itself states. | supported (refutation disclosed) |
| 22 | Eq. 17 (v⁶, 1/128) undetermined | M-MECHANIST-06 and the empiricist math marked unverified | supported |
| 23 | Pattern coefficients 0.562/0.3125 used only as down-factors | M-MECHANIST-06 unverified; report discloses this | supported |
| 24 | Merger k uncertain; Rahvar normalisation differs by 5e3; Redi–Tesi c_J = 16 | C4-0 log gives k_RT = 6.37e-2 vs 3.39e-2 (factor-2 range); the 5e3 and c_J = 16 were not re-traced | weak (preprints only) |
| 25 | Literature claims (Sawyer exponent ≤ 0.24 vs ~200, Jones–Singleton 1e11 m, Deser, Gibbons) | C6-1, C2-1; report flags abstract-only or search-summary access | weak |
| 26 | Credences (0.92, 0.90, 0.85, 0.80, 0.65, 0.25, 0.03, 0.02) | The report states that the slate is non-exclusive, so no sum-to-1 check applies. The C3 and C4′ split (0.65/0.25/~0.10) sums to 1.00. | supported |
| 27 | Plasma threshold n_e < 2.8e-4 cm⁻³; f_p = 1.56 kHz | M-MECHANIST-11 (1.555 kHz, verified for n_e = 0.03 cm⁻³); 2.8e-4 from M-CONSTRAINTS-09, not re-opened | supported (f_p); weak (2.8e-4, not re-opened) |
| 28 | Face-value depletion 3.3e-66 | lens-mechanist_outgoing log (3.281e-66) | supported |

## Summary: 28 claims checked, 6 flagged (all weak, none contradicted); most serious: the preprint-only and search-summary literature support for the Rahvar and Redi–Tesi normalisations and for the no-go citations. The GW170817 and finite-source k figures were also not located in the logs I opened.
