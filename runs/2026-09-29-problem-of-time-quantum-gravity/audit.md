# Audit of report.md
| # | Report claim | Traced to | Status |
|---|---|---|---|
| 1 | 1 mm redshift: -9.8(2.3)e-20 measured vs -1.09e-19 predicted, 7.6e-21 uncertainty | dossier.md l.33-34,59-60 (D-14); M-DECOMPOSER-01 log (1.09e-19), M-EXAMINER-03 log (7.6e-21) | supported |
| 2 | Tidal/potential ratio 1.57e-10 over 1 mm | M-EXAMINER-01 log | supported |
| 3 | Height-superposition visibility V=0.98921 (dh=1 m, T=1 s); first zero T*dh=10.7 m*s | M-DECOMPOSER-08 log; M-EXAMINER-04 / M-IDEALIZER-11 logs | supported |
| 4 | Smith-Ahmadi lambda=8.71e-76 s; lambda*omega=2.35e-60 | M-IDEALIZER-03; M-EXAMINER-07, M-DECOMPOSER-07 logs; falsifier-C2-0 script | supported |
| 5 | Record-conditioned Born values 0.146447/0.5/0.853553, verified to ~1e-15; POVM defect 3e-15 | M-IDEALIZER-02, M-DIALECTICIAN-02, M-DECOMPOSER-02 logs; 3e-15 in M-IDEALIZER-02/M-CONSTRAINTS-12/M-DIALECTICIAN-04 logs. The "1e-15" figure for exact evolution is a loose paraphrase of logs that show ~3e-15 | supported (minor rounding) |
| 6 | Quantum-separation anti-Hermitian part 4.93e-2 rad/s; kinematic norm 1.000-1.091 | verdicts/C2-0.md l.15,32; calc/falsifier-C2-0; M-CONSTRAINTS-13 log (1.091). Model-unit toy result, single model | supported (model-dependent) |
| 7 | M2 infidelity 1.89e-4 -> 1.88e-10 (M=10 -> 1e4); 1-F ~ M^-2 | M-IDEALIZER-07 log | supported |
| 8 | Kiefer-Kramer scaling -247.68 (H/m_P)^2/k^3; (E/m_P)^2 = 1.42e-11 vs 6.7e-11 | verdicts/C3-0.md; verdicts/C8-0.md l.22,46 | supported |
| 9 | QGEM phase 0.226/0.565 rad; Newtonian vs superposed-proper-time differ <=1.3e-51 rad; branch-time part 1.2e-38 rad | M-IDEALIZER-15 (refuted as stated, corrected convention gives 0.226/0.565); verdicts/C1-0.md l.17,20 | supported (report notes the correction) |
| 10 | C5 tracial state: modular flow trivial 3.7e-16; modular/energy ratios 0.916 vs 0.170 | verdicts/C5-0.md; M-IDEALIZER-06 log | supported |
| 11 | GPP exponent 2.22e-27 at 1 s; Tmax factor 1.1e6; coherence 0.650 before evaporation | verdicts/C6-0.md l.17,27,31; math/decomposer.md l.16 | supported |
| 12 | tau_DP 11.6 ms -> 8.1 s at R0=1e-4 m; R0 >~ 4e-10 m | verdicts/C7-0.md l.9,12; M-CONSTRAINTS-14 log | supported |
| 13 | PQCG delta-kernel gap 1e17 | M-CONSTRAINTS-15 log | supported |
| 14 | York turning 120.5/79.9/51.2 Gyr; Godel CTC r>0.8814 | M-CONSTRAINTS-03, M-CONSTRAINTS-04 logs | supported |
| 15 | Uncertainty cost dLambda >= 9e-105 Lambda_obs | M-CONSTRAINTS-11 log | supported |
| 16 | Math refuted items (M-DECOMPOSER-10 "20-30 orders" -> 10-18; M-IDEALIZER-15) corrected and non-load-bearing; M-EXAMINER-08, M-DECOMPOSER-06 unverified | math/decomposer.md, idealizer.md, examiner.md | supported |
| 17 | Clause (iii) of C1 fails; C5 "modern form" fails; C4 branch failures | verdicts C1-0, C5-0, C4-0 (calc plus cited evidence) | supported |
| 18 | C2 exact only for uncoupled/c-number clocks; HSL restrict trinity to non-interacting clocks (full text) | M-EXAMINER-05, M-CONSTRAINTS-06/07, verdict C2-0, dossier | supported |
| 19 | Hořava |beta| <~ 1e-15 (Gümrükçüoğlu 2018) | candidates.md C4 only; no calculation or dossier trace found in my checks | weak |
| 20 | Mass gap to QGEM test 8.4 orders of magnitude | dossier l.66,220: search-summary | weak (report flags it) |
| 21 | "No 2024-26 construction found" for local constraints; Salecker-Wigner formula | search-summary only (dossier, C8 verdict); report flags it | weak (flagged) |
| 22 | Stoica 2026, Chua 2024, Feng-Vedral-Marletto 2025 and other preprint-based claims | preprints per dossier; report labels them | weak (labelled) |
| 23 | Abstract-only items (Kiefer-Wichmann 2018, Chataignier 2023, Isenberg-Rendall, Donnelly-Jacobson) used to rank C3 and C4 | abstracts only; report flags | weak (flagged) |
| 24 | Credences (C1 0.85, C8 0.85, C7 0.15, C5/C6 0.10, strong-null 0.10) and cost ranks | judgment; no derivation in run files. Report says ranks are judgments but credences are stated as numbers | weak (unsupported precision) |
| 25 | "Conservative positions differ by at most ~1e-10 in cosmology, ~1e-60 in the lab" | 1e-60 traces to lambda*omega 2.35e-60; 1e-10 traces to (E/m_P)^2 range and 1.57e-10 tidal ratio. The cosmology figure conflates different quantities | weak |
| 26 | Bottom line: "confidence high: peer-reviewed measurement plus verified calculation" for the fixed-background reconciliation | Measurement and calcs verified; the "already reconciled" claim also relies on the Kay-Radzikowski-Wald abstract and framing, and the report itself says the questioner's "absolute time" framing is only distinguished by framing | supported (modest overreach) |
| 27 | Falsifier calcs "read but not re-run" | Self-disclosed | supported |

## Summary: 27 claims checked, 7 flagged (all weak, 0 contradicted, 0 unsupported); most serious: the numeric credences (item 24) and the "~1e-10 cosmology" equivalence figure (item 25) have no direct derivation in the run, and the Hořava 1e-15 bound (item 19) rests only on candidates.md. The 1e-15 verification precision for C2 is slightly generous (logs show ~3e-15). No claim rests on a refuted math row.
