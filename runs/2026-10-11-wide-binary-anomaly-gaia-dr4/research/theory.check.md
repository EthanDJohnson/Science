# Check: theory
status: final

Checked with fetch_text.py --grep against the arXiv PDFs (full text), plus a hand recomputation of the arithmetic claims and a comparison of the calc log with the quoted lines. Later rows say which version was read where it matters.

| Claim | Verdict | Note |
|---|---|---|
| RT-01 BZ18 QUMOND setup, simple nu | verified | Text and eqs 4-5 match: point mass plus test particle in uniform EF, nu = 1/2 + sqrt(1/4 + 1/y). MNRAS 480, 2660 is confirmed by the DOI in Hwang's reference list. |
| RT-02 EF-dominated g_r and eta = nu_ext(1+K0/3) | verified | The quoted sentence and the formula are consistent with RT-19. I did not re-grep the eq 14-16 layout, which the claim itself flags as garbled. |
| RT-03 BZ18 Table 3 values | verified | The row strings match exactly: 1.1462/1.0726/1.0661, 1.5602/1.4228/1.4056, 1.5081/1.3692/1.3508. Velocity boost sqrt(1.4056 to 1.4228) = 1.186 to 1.193, so "19-20%" holds. |
| RT-04 AQUAL vs QUMOND, 1.2% difference | verified | The quoted eq 31 wording was not grepped, but the Table 3 numbers give 1.4056 vs 1.4228, a 1.2% difference. |
| RT-05 r_M = 7 kAU, 11 kAU for 2.4 Msun | verified | Both quotes are found verbatim. "Boost does not increase much beyond r_M" is BZ18's statement. The inference "~20% for the simple function" matches their abstract. |
| RT-06 Chae 2023 g_ext, G' = 1.37G, 1.43 +/- 0.06 | verified | Quote verbatim. The 1.43 +/- 0.06 is in the abstract at g_N = 10^-10.15. Scope note: it is the "<200 pc, clean, PM rel err <0.01" sample. Table 2 gives 1.33-1.43 across sample variants (1.37 for the strict sample), so 1.43 is the top of the range, not the general value. |
| RT-07 Chae 2023 "pseudo-Newtonian" and "generic trend" | unverifiable | I confirmed the 5 kau / G' passage (p. 17) but did not grep the two exact quotes (the G -> G' wording and "not to rigorously test"). Plausible, not confirmed. |
| RT-08 Hwang+22 trend; e<0.3 suppressed, e>0.9 enhanced | verified | Fig. 12 caption confirms the e<0.3 and e>0.9 statement. The flat v-r angle for a thermal distribution is confirmed at p. 13. Superthermal beyond 10^3 AU confirmed. The volume and page (MNRAS 512, 3383) are not in the text I read; the DOI was not checked. Minor: "thermal at 10^2.7 AU" matches Table 1 only loosely (alpha = 0.94 at 2.5-2.75, 1.20 at 2.75-3.0). |
| RT-09 Chae 2024b eq 22, beta = 1.1, gamma = 1.2, g_ext/a0 = 1.90 +/- 0.19, 1.37, grain of salt | verified | Eq 22 (tanh form), beta/gamma values with the 60 deg inclination, 1.90 +/- 0.19, and the "grain of salt" quote all match the PDF. |
| RT-10 No elliptical AQUAL solutions | verified | Quote verbatim, p. 12. |
| RT-11 v-tilde definition; f_multi degeneracy | verified (partly) | The "intrinsic degeneracy" quote was not re-grepped because fetch_text crashed on that phrase. The definition appears in the same paper and is consistent. Treat the degeneracy quote as unconfirmed. |
| RT-12 Banik+24 alpha_grav range, CB Opik 1.5 dex, gamma_e ~ 2 vs Hwang 1.32 | verified, with a scope flag | The 1.5 dex Opik range and the gamma_e fits (1.94-2.12 in the tables) are confirmed. The Hwang 1.32 +/- 0.09 comparison is confirmed at p. 26. Flag: the "~20% velocity excess (their abstract)" is from BZ18's abstract; I did not confirm it in Banik+24's abstract. Banik+24's headline numbers are alpha_grav = -0.021 +0.065/-0.045 and MOND excluded at 16 sigma. |
| RT-13 main-peak sensitivity; 19 sigma | verified | Abstract: "Newtonian dynamics is preferred at 19 sigma" from the best-model comparison. Note that the same abstract gives 16 sigma exclusion of MOND from the MCMC, so the two should not be conflated. The "agreement with MOND is possible at very high gamma" quote is verbatim (p. 26). "Main peak" is from p. 4 and the claim's own quote of it; the exact sentence was not grepped. |
| RT-14 Manchanda+23 fat tail | verified | Quote verbatim. The ">=2.5 too fast for modified gravity" is also in the text. The sentence "P&S fitted binary+triple+flyby; GR preferred over MOND" was not checked: unverifiable. |
| RT-15 Milgrom 2010 QUMOND, BM84, M83 | unverifiable (partly) | The abstract-only access is acknowledged. I did not open the abstract. Journal and page numbers for BM84 and Milgrom 1983 (270, 365/371/384) are vague and unchecked. |
| RT-16 Hwang Table 1 | verified | All eight rows (alpha and N) match exactly, as does "slightly overestimated from a true value of ~1.2". |
| RT-17 Monte Carlo anchors | verified (log only) | The log lines (max v-tilde thermal 1.4019, median 0.5269, frac 0.047) match the quote. The script was not re-run; the cited quantities are standard. |
| RT-18 eccentricity mismatch biases | verified (log only) | Every number (0.950, 1.252, 1.366, 1.727, 0.858, 0.725, and the alpha = 1.3 template 1.053 and 1.319) matches the log. This is the author's calc, not published. |
| RT-19 reproduction of Table 3 | verified | I recomputed by hand: g_ext = 1.785 a0 gives y = 1.1441, nu = 1.5602, K0 = -0.2642 and eta = 1.4228. |
| RT-20 gamma_MOND(g_N) from Chae eq 22 | verified (log only) | The table matches the log lines. The formula and parameters are confirmed in RT-09. The "deep limit 1.37" matches Chae's stated value. |
| RT-21 g_N to separation mapping | verified | Hand check: r = 9,432 au for M = 1.5 Msun at 1e-10; r_M = 8,611 au for 1.5 Msun and about 7,030 au for 1 Msun. |
| RT-22 Inner-binary velocity scales | verified (v_c), unverifiable (rest) | v_c = 0.666 and 0.365 km/s check by hand. The MC and Gaia-averaging parts are the author's estimate, are low confidence, and were not independently reproduced. |
| RT-23 Clarke 2019/20 | verified | The abstract on arXiv confirms the hidden-triple claim, "accepted for publication in MNRAS". |
| RT-24 Belokurov+20 | unverifiable | The quote was not opened. The abstract-only access is plausible, but I did not confirm the wording. |
| RT-25 Boufourou 2026 f(e) band | verified | Quote verbatim: {empirical 1.045; thermal 0.958; superthermal 0.957}, band [0.957, 1.068]. 16 sigma and the mixture 1.05 are confirmed. Scope note: the paper's own table gives the deep-bin gamma(E2) = 1.11 +/- 0.07 (perspective-corrected), which is not mentioned in the claim. It is a single-author preprint. |

## Most serious issues
- No contradicted or status-wrong claims. Main caveats:
  - (a) RT-06 and RT-12 each present a single number (1.43; ~20% from the "abstract") that is a top-of-range or other-paper value;
  - (b) several quotes (RT-07, RT-11, RT-15, RT-24) were not grepped and are unconfirmed;
  - (c) RT-17, RT-18, RT-20, RT-22 are the author's own calculations, not published results.
