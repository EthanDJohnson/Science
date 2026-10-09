# Check: quantitative
status: final

Method: quotes re-fetched with fetch_text.py --grep; "(ours)" arithmetic spot-checked by hand (shell volume 2.93e4 m^3, density 1.5e23 kg/m^3, Rs 6.67 m, Mc^2 4.04e44 J, KE 3.2e41 J vs 7.2e18 J, 109 yr, Alcubierre -v^2R^2/(18 Delta) -> 6.72e46 J = 0.376 Msun, Fell-Heisenberg 9.25e43 J/c^2 = 1.03e27 kg, Alcubierre R=10 m v=4.37 -> 1.4e29 kg): all reproduce. The calc script and the Natario fit coefficient were not re-run.

| Claim | Verdict | Note |
|---|---|---|
| RQ-01 shell R1=10, R2=20, M=4.49e27 kg (2.365 M_J), smoothing/trial-and-error | verified | Exact text on p.13 of 2405.02709; CQG 41 095013 is the journal version. Footnote wording not re-grepped but surrounding text matches. |
| RQ-02 shell arithmetic, compactness 0.33/0.67, Fig. 4 axes | verified | Arithmetic reproduces by hand. Fig. 4 axis read not re-checked (flagged as axis-read in the claim); nuclear density unsourced, as the claim admits. |
| RQ-03 compactness cap quote | verified | p.27 quote matches exactly. |
| RQ-04 Table 1 time delays | verified | Table values match exactly (8.0, 9.1, 6.7, 0, 7.6 ns). The flagged inconsistency is real: p.27 says Alcubierre gives an "advance" while the table lists +8.0 ns. Sign convention unresolved in the source. |
| RQ-05 acceleration unsolved; Le 2026 e^{-3L} | verified | "spinning-up" quote matches (p.28). Le abstract confirms m_f/m_i = e^{-3L} for burns joined at static spheres, and that it is a preprint. |
| RQ-06 self-similar scaling to 100 m | verified | Own arithmetic, correctly labelled as an assumption (no published scaling law). Mass and energy scale linearly in R correctly. |
| RQ-07 shell KE vs payload; Earth-mass shell time slowing 4e-4 | verified | Quote on p.10 of 2102.06824 matches; arithmetic checks. |
| RQ-08 Bobrick-Martire factors (two orders, factor 3, factor 10) | verified | Abstract and p.19 quotes match. Caveat in the claim (two orders not decomposed) is accurate. Journal version CQG 38 105009 not independently checked. |
| RQ-09 B-M do not support Lentz superluminal; Van Den Broeck equivalent to Alcubierre | verified | Both quotes match (p.18, p.22). |
| RQ-10 Lentz proceedings scaling E ~ C v^2 R^2/w, "few x 1e-1 Msun v^2" | verified | Text matches (extraction drops the fraction bar, R^2/w is consistent with the "R much larger than w" context). "tens of orders of magnitude" quote confirmed p.7. Conversion to 20-50 Msun at v=10c is ours and depends on "few"=2-5. |
| RQ-11 Lentz 2021 -6e62 v_s/c kg, "few hundred Planck lengths" | verified | Both quotes match. Note the paper writes v_s/c in one place and v_s in the other; the claim already notes this. |
| RQ-12 Fell-Heisenberg 3.2e26 kg/m^3, 9.25e43 J, 1.26 shift | verified | All published numbers match (pp.13, 15, 17). Length-unit inference is flagged as ours. "Four orders of magnitude" is the authors' wording; 9.25e43/1.78e47 = 5.2e-4, so the claim's "3.3 orders" note is right. |
| RQ-13 Alcubierre reference energies | verified | Closed form reproduces 6.72e46 J = 0.376 Msun at R=100 m, Delta=1 m, v=1 (x100 at v=10). Eulerian only, as stated. |
| RQ-14 Pfenning-Ford QI wall, 6.2e65 v_b g | verified | Eq. 23 and Eq. 29 match (6.2e65 v_b grams = 6.2e62 kg). B-M "rest-mass energy of the Universe" quote matches (p.2). |
| RQ-15 Natario 8000x Alcubierre; Bolivar et al. bound | verified | Preprint quote (2609.36211) matches exactly, including the v^2 R^4/(4 Delta^3) sharp constant and the "two powers of R/Delta" statement. The own-calculation fit (-0.0445 v^2R^4/Delta^3) was not re-run, but its scaling agrees with the preprint; status is preprint. |
| RQ-16 trip comparison (rocket 40.4 mass ratio, Alcubierre 0.072 Msun) | verified | Alcubierre R=10 m figure reproduces (1.4e29 kg). The photon-rocket values were not recomputed independently; mass ratio ~40 is consistent with sqrt-form for two legs at beta 0.952. |
| RQ-17 Barzegar et al. ADM energy vanishes for R-Warp | verified | Theorem IV.19(i) matches. DEC/Minkowski sentence matches the claim's quote; the claim correctly says the class membership of specific metrics was not checked. |
| RQ-18 Warp Factory quote | verified | Abstract matches. Also worth noting for the synthesis: the same paper (p.2) states Lentz and Fell solutions have positive Eulerian density but "it has been argued that these still both violate the weak energy condition". |
| RQ-19 Fell et al. 2026 terawatt luminosity | verified | Abstract on arXiv 2608.10800 matches; preprint, and "zero ADM mass" scope is correct. Low confidence rating is appropriate. |
| RQ-20 world energy 620 EJ in 2023 | unverifiable | Energy Institute PDF returned 403, so the number rests on a search summary. The figure agrees with my own recollection of the 2024 Statistical Review but I did not confirm it from a source. Immaterial to the conclusions. |

## Summary
19 verified, 1 unverifiable, 0 contradicted, 0 misattributed, 0 status-wrong. The most serious issue is not a claim error: the source's own tension in Fuchs et al. between "advance" for Alcubierre (p.27) and a positive 8.0 ns in Table 1, so the time-delay table should not be used as a travel-time test without checking the sign convention. Second caveat: the shell's energy, density and 100 m scaling numbers are our own arithmetic or extrapolation, not published values.
