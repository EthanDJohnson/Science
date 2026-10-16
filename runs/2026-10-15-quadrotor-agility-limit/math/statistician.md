# Math check: statistician
status: final

All quantities SI (m, s, m/s, m/s^2) or dimensionless (probabilities, chi2, elasticities, z, Bayes
factors). Every row was re-derived from the stated definitions in a fresh script; none of the
lens's `calc/` code was imported, read for its logic or run.

| ID | Claim (finding) | Statement checked | Checks | Verdict | Log |
|---|---|---|---|---|---|
| M-STAT-01 | 10/10 intervals and the 29-flight certification count (F1, S1, STAT-C) | X ~ Bin(n, p) iid; k = n = 10: Clopper-Pearson one-sided 95 % lower bound 0.741 and Wilson 95 % [0.722, 1.000] (so a true rate 0.75 is inside); ln(0.05)/ln(0.90) = 28.43, so 29 flawless flights certify p >= 0.90 at one-sided 95 % | CP by bisection vs closed form 0.05^(1/n); Wilson by score inversion vs closed form (agree to 1e-9); minimal-n search (29 works, 28 does not); n -> oo limit; units dimensionless | verified | math/statistician/M-STAT-01.py.log |
| M-STAT-02 | One-sided exact tests of H0: p = 0.90 (F2, F4; rows S2-S4) | 8/10 -> p = 0.2639, z = 0.631; 6/10 -> 0.01280, z = 2.232, two-sided 0.0256; 1/4 -> 0.00370, z = 2.678, two-sided 0.0074; 38/43 -> 0.4325 with Wilson 95 % [0.7552, 0.9493] | binomial CDF from math.comb vs scipy (1e-12); exact closed form for 1/4; monotonicity in k; k = n limit gives p = 1; large-n limit; units dimensionless | verified | math/statistician/M-STAT-02.py.log |
| M-STAT-03 | Trials per arm and precision (F3, STAT-C) | Two-proportion, two-sided alpha = 0.05, power 0.80: n = 199 (0.90 vs 0.80), 5907 (0.90 vs 0.884), 32 (0.90 vs 0.60); se = 0.10/5 = 0.0200 and n = p(1-p)/se^2 = 225 at p = 0.9 | closed-form n vs achieved normal power (>= 0.80 at n, < 0.80 at n-1) vs Monte-Carlo power 0.826 at n = 32; 1/delta^2 divergence limit; monotonicity in the gap; units dimensionless | verified | math/statistician/M-STAT-03.py.log |
| M-STAT-04 | grouped chi2 of ln(speed) by course type (F5, F11; STAT-B, STAT-H; row S5) | x_i = ln(v_i/1 m/s), assigned sigma_x = 0.20, equicorrelated within group: within 2.974/2 (26.16 m/s), 5.280/3 (7.38 m/s), 0.467/1 (33.05 m/s); between 104.21/2, p = 2.35e-23, z = 9.96; pooled 15.70 m/s, S = 3.757; sigma = 0.80 -> 6.51/2, p = 0.0385; rho = 0.8 -> 37.63/2, p = 6.73e-9, z = 5.80; unseen-group effective error 0.184 | GLS means and chi2 from C^{-1}; within + between = pooled to 1e-9; exact 1/sigma^2 scaling; invariance under v -> 3.6 v (km/h) to 1e-9; analytic var(mean) = sigma^2(1 + (n-1)rho)/n to 1e-12; units m/s | verified | math/statistician/M-STAT-04.py.log |
| M-STAT-05 | Stop-bound elasticities and the latency/braking crossover (F6, F7; STAT-D; rows S9, S10) | v*tau + v^2/(2a) = s, s = 6 m, a = 38 m/s^2: tau = 40 ms -> v = 19.888 m/s, e_range = 0.5355, e_accel = 0.4645, e_latency = -0.0710, leverage 7.54x; tau = 17 ms -> 0.5151/0.4849/-0.0302, 17.0x; tau = 130 ms -> 0.6127/0.3873/-0.2254, 2.72x; [A-33] case (a = 20, tau = 50 ms) v = 14.524 m/s, e_latency = -0.0644; crossover v = 2 a tau = 3.04 m/s | three independent solutions for v (quadratic, bisection, Euler integration of the stop manoeuvre to 6.0000 m); closed-form vs finite-difference elasticities to 1e-6; symbolic identities e_range + e_accel = 1 and e_latency = -v*tau/(v*tau + v^2/a); limits tau -> 0 (v -> sqrt(2as), 1/2, 1/2, 0) and tau -> oo (e_latency -> -1); units of m/s | verified | math/statistician/M-STAT-05.py.log |
| M-STAT-06 | Dodge-bound elasticities and the parity latencies (F6; STAT-F; row S10) | v = s/(tau + 2 sqrt(r/u2)), r = 0.5 m: e_tau = -0.0690 (tau = 17 ms, u2 = 38), -0.3617 (130 ms, 38), -0.1365 (50 ms, 20), -0.0821 (20 ms, 40), -0.2403 (s = 10 m, 100 ms, 20); e_s = 1 exactly; e_a = 0.4317 and 0.4590; \|e_tau\| = 0.50 at tau = 161.2, 229.4, 343.0 ms for u2 = 77, 38, 17 m/s^2 | closed form vs finite differences to 1e-6; parity tau by bisection vs closed form 2 sqrt(r/u2) to 1e-6; symbolic identities e_s = 1 and 2 e_a - e_tau = 1; limits tau -> 0 (e_tau -> 0, e_a -> 1/2) and u2 -> oo (v -> s/tau, e_tau -> -1); units (2 sqrt(r/u2) is a time, v a speed) | verified | math/statistician/M-STAT-06.py.log |
| M-STAT-07 | Thrust-to-weight elasticity, theory vs planner sweep (F7; STAT-A, STAT-E; row S12) | a_h = g sqrt(TW^2 - 1) = 16.99/37.99/77.86 m/s^2 at TW = 2/4/8; bang-bang 10 m: t = 1.026 s, peak 19.49 m/s, mean 9.746 m/s at TW = 4; dln t/dln a_h = -1/2 exactly, dln a_h/dln TW = 16/15 = 1.067, so e_TW = 8/15 = 0.5333; [A-16] slope ln(5.81/7.14)/ln(3.6/2.5) = -0.5653; gap to theory 5.99 % | integrated bang-bang time vs closed form (1e-3); finite-difference vs analytic e_TW (1e-6); symbolic elasticities; limits TW -> oo (e_TW -> 1/2) and TW -> 1 (a_h -> 0); units of m/s^2 and m/s. Note [A-34]'s "9.8 m/s" mean speed is 9.746 rounded up (0.6 %), not the statistician's own number | verified | math/statistician/M-STAT-07.py.log |
| M-STAT-08 | Sidak multiplicity values and crash-cause Wilson intervals (F8) | 1 - (1 - p)^N: p = 0.01 -> 0.0490 (N = 5), 0.1136 (N = 12); p = 0.05 -> 0.2262, 0.4596; S4's global z = 2.088 at 5 looks from p = 0.0037; Wilson 95 %: 2/2 [0.342, 1.000], 4/10 [0.168, 0.687], 2/10 [0.057, 0.510], none excluding 0.5 | formula vs Monte-Carlo over N independent uniforms (2e5 draws, agreement to ~1e-3); Wilson by bisection vs closed form; series 5p - 10p^2 and Sidak <= Bonferroni; N -> oo limit; units dimensionless | verified | math/statistician/M-STAT-08.py.log |
| M-STAT-09 | Two-proportion tests on [A-14] (F9; rows S6, S7) | Pooled z with n = 20 per arm: 17/20 vs 0/20 -> z = 5.437, two-sided p = 5.43e-8; 17/20 vs 10/20 -> z = 2.363, p = 0.0181; 0.85 vs 0.50 needs 27 trials per arm (alpha 0.05, power 0.80) | z from the definition; Fisher exact cross-check (2.57e-8 and 0.0407, both agreeing in direction and significance; the 0 % row stays decisive at n = 10, Fisher p = 1.2e-4); sqrt(n) scaling of z verified to 1e-6; achieved power >= 0.80 at n = 27; units dimensionless | verified | math/statistician/M-STAT-09.py.log |
| M-STAT-10 | Lap-time tension, trial-count granularity, Bayes-factor bounds (F9, F10, F4, F13) | 4.92 +/- 0.10 s vs 5.14 +/- 0.09 s: z = 1.635 per trial, z = 8.17 > 7 on means of n = 25; 44.0/76.0/20.0 % force n >= 25 and 85.0/50.0 % force n >= 20; SBB min BF_alt:null = 1/(-e p ln p) = 10.13 (p = 0.0074), 5.09 (0.018), 3.92 (0.0256) with priors 0.0899, 0.1643, 0.2032 and posterior 0.717 at prior 0.20 | quadrature z; exhaustive smallest-n search over denominators; SBB bound from its definition with the p -> 0 limit and the exact value 1 at p = 1/e; 1/sqrt(n) series and limit for the tension; units of s and dimensionless | verified | math/statistician/M-STAT-10.py.log |
| M-STAT-11 | "54 flights with one crash, 85 with three" certify p >= 0.90 at 95 % (F1, STAT-C) | Smallest n whose 95 % confidence lower bound on p reaches 0.90 with f failures, under the one-sided 95 % Clopper-Pearson rule the lens itself states for f = 0 | minimal-n search with the binomial tail from math.comb (cross-checked against scipy to 1e-12); monotonicity in f and in alpha; exact f = 0 rule 0.05^(1/n) | **refuted** | math/statistician/M-STAT-11.py.log |
| M-STAT-12 | Row S3's look-elsewhere entry "z = 1.7 at 12 looks" for the 6/10 result (F8, S3) | Sidak global p from local one-sided p = 0.0128 at N = 12 independent looks, converted to z = Phi^{-1}(1 - p_global) | same formula and Monte-Carlo as M-STAT-08; inversion of the claimed z | **refuted** | math/statistician/M-STAT-08.py.log |
| M-STAT-13 | Row S8's latency-to-RMSE log-log slope 0.51 | slope = ln(0.474/0.322)/ln(75/35) = 0.5073, dimensionless and independent of the time unit; with tau_2 > 75 ms the slope falls (0.37 at 100 ms, 0.21 at 220 ms), so 0.507 is an upper bound | definition in ms and in s (identical to 1e-12); censoring monotonicity; divergence limit as the delay ratio -> 1; units m and s | verified | math/statistician/M-STAT-13.py.log |

## Refuted

- **M-STAT-11 — the "54 with one crash, 85 with three" flight counts.** F1 and candidate STAT-C
  state: "Certifying a true rate >= 0.90 at 95 per cent needs ln(0.05)/ln(0.90) = 28.4, i.e. 29
  consecutive flawless unseen-course flights, or 54 flights with one crash, 85 with three." The
  first number fixes the convention: ln(0.05)/ln(0.90) is the *one-sided* 95 % Clopper-Pearson
  rule (0.9^n <= 0.05). Under that same rule the minimal counts are **46** with one failure
  (CP lower bound 0.9004 at n = 46; at n = 45 it is 0.8975) and **76** with three (0.9008 at
  n = 76), not 54 and 85. The lens's 54 and 85 are exactly the counts for alpha = 0.025, i.e. the
  lower end of a *two-sided* 95 % interval (and that convention would make the flawless-record
  count 36, not 29). So the three numbers are not computed at one confidence level; two of the
  three are about 17 and 12 per cent too large.
  Corrected form: at one-sided 95 %, 29 / 46 / 76 flights for 0 / 1 / 3 failures; at the
  two-sided-95 % lower end, 36 / 54 / 85.
  Depends on it: F1 and F3's "about 20x under-powered" rhetoric, the data-needed item "29 flawless
  flights (or 54 with one crash) per speed bin on an unseen course, at 5, 7, 9 and 11 m/s: about
  150-220 flights", and candidate **STAT-C**. The error is conservative (it demands more flights
  than needed), so the direction of F1/F3/STAT-C survives — the largest published single-condition
  set is 43 flights, still below even the corrected 46 — but the per-bin flight budget in "What
  data would settle it" should read 29/46 rather than 29/54, i.e. about 120-185 flights.
  [log: math/statistician/M-STAT-11.py.log]
- **M-STAT-12 — row S3's global significance "z = 1.7 at 12 looks".** With the lens's own Sidak
  machinery, a local one-sided p = 0.0128 over 12 looks gives a global p of 0.1432, hence
  z = Phi^{-1}(1 - 0.1432) = **1.07** (1.46 if one converts the global p two-sidedly). Reaching
  z = 1.7 from that local p would need about 3 looks, not 12; at 12 looks z = 1.7 would require a
  local p near 0.004. The table's own F8 numbers are right (a local 0.01 becomes 0.114 at 12
  looks), so this is an isolated transcription-level error in the S3 row, not a method error.
  Depends on it: the S3 verdict "robust-ish (threshold failed)" for the 60 % at 10 m/s result.
  With the corrected global z = 1.07, the 6/10 row's rejection of the 90 % threshold does **not**
  survive a 12-look multiplicity correction; it survives only as a prespecified single comparison
  (local p = 0.0128). This weakens, but does not reverse, F2's statement that only the 10 m/s row
  rejects the threshold, since F2's claim is explicitly local. Candidate STAT-C is unaffected.
  [log: math/statistician/M-STAT-08.py.log]

## Unverified

- None. Two items were checked only as arithmetic on quoted inputs and are flagged inside their
  rows rather than left unverified: [A-34]'s mean speed 9.8 m/s is 9.746 m/s rounded up
  (M-STAT-07), and the S8 slope 0.51 is an upper bound because the source's second delay is
  ">75 ms" (M-STAT-13). The *group membership* behind M-STAT-04 was reconstructed from the dossier
  speeds the lens cites (seen {27.8, 32.2, 20.0}, unseen {10, 8, 7, 5.3}, mocap {30.0, 36.4} m/s);
  it reproduces all three group means and every chi2 to three digits, so the reconstruction is
  confirmed, but the grouping itself (e.g. placing two numbers from [A-26] in one group) is an
  evidence judgement, not mathematics, and is outside this check.

## Formalizable

- M-STAT-01: for X ~ Bin(n, p), the one-sided level-alpha Clopper-Pearson lower bound at k = n is
  exactly alpha^(1/n); and min{n : alpha^(1/n) >= q} = ceil(ln alpha / ln q) for 0 < alpha, q < 1.
- M-STAT-02: P(X <= k | n, p) is strictly decreasing in k and strictly decreasing in p on (0,1);
  P(X <= n | n, p) = 1.
- M-STAT-04: for x in R^N partitioned into groups with equicorrelated covariance
  C = sigma^2[(1-rho)Id + rho J], the GLS group mean has variance sigma^2(1 + (n-1)rho)/n, and the
  chi2 decomposition sum_g chi2_within(g) + chi2_between = chi2_pooled holds exactly; both are
  invariant under x -> x + c*1 (i.e. under rescaling the speeds).
- M-STAT-05: for s, a, tau > 0 and v the positive root of v*tau + v^2/(2a) = s, with
  D = v*tau + v^2/a: dln v/dln s = s/D, dln v/dln a = (v^2/2a)/D, dln v/dln tau = -(v*tau)/D, and
  therefore dln v/dln s + dln v/dln a = 1 identically, with limits 1/2, 1/2, 0 as tau -> 0.
- M-STAT-06: for v = s/(tau + 2 sqrt(r/u)) with s, r, u > 0, tau >= 0: dln v/dln s = 1,
  2 dln v/dln u - dln v/dln tau = 1, and |dln v/dln tau| = 1/2 iff tau = 2 sqrt(r/u).
- M-STAT-07: for t(a) = 2 sqrt(d/a), dln t/dln a = -1/2 exactly; and for a(TW) = g sqrt(TW^2 - 1)
  with TW > 1, dln a/dln TW = TW^2/(TW^2 - 1), which is > 1 and decreasing to 1.
- M-STAT-08: 1 - (1 - p)^N <= Np for p in [0,1], N a positive integer, with equality iff N = 1 or
  p = 0; and 1 - (1 - p)^N = Np - C(N,2)p^2 + O(p^3).
- M-STAT-10: -e p ln p <= 1 on (0, 1/e], with equality iff p = 1/e; hence the SBB minimum Bayes
  factor 1/(-e p ln p) >= 1 there and diverges as p -> 0.
- M-STAT-11: the minimal n with CP lower bound >= q is non-decreasing in the failure count f and
  non-increasing in alpha; with the two conventions alpha = 0.05 and 0.025 the minima at q = 0.9
  are (29, 46, 76) and (36, 54, 85) for f = 0, 1, 3.
