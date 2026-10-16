# Math check: empiricist
status: final

Units: SI throughout (m, s, m/s, m/s^2, g = 9.81 m/s^2); probabilities and elasticities dimensionless.
Every verdict cites a log produced by `math_run.py`; no lens script was imported, copied or run.

| ID | Claim (finding) | Statement checked | Checks | Verdict | Log |
|---|---|---|---|---|---|
| M-EMP-01 | Clopper–Pearson 95% intervals on every reported success rate (F2, trial table, EMP-C) | X ~ Binomial(n, p), p in [0,1] dimensionless, iid trials; two-sided exact interval from P(X>=k\|p_L) = P(X<=k\|p_U) = 0.025, for k/n = 8/10, 10/10, 6/10, 38/43, 1/4, 17/20 | binomial-tail bisection at 30 dps vs the regularized incomplete-beta identity; k=n closed form 0.025^(1/n) at n = 4…43; limits n→∞ and n→1; dimensionless | verified (all six intervals reproduce to <6e-4) | math/empiricist/M-EMP-01.py.log |
| M-EMP-02 | n = 29 (one-sided) / 35–36 (two-sided) for an all-success 90% claim; ~199 trials per arm to tell 0.9 from 0.8 (F2, EMP-C, cost note) | smallest n with alpha^(1/n) >= 0.9, alpha = 0.05 / 0.025; two-proportion sample size at 5% two-sided, 80% power, p1 = 0.9, p2 = 0.8 | closed form ceil(ln alpha/ln 0.9) = 29 and 36, boundary n-1 fails (n=35 gives 0.899968), n per arm = 198.96, limit alpha^(1/n)→1 and n(p)→∞ as p→1, dimensionless | verified (the "35–36" pair is the correct statement of a boundary case) | math/empiricist/M-EMP-02.py.log |
| M-EMP-03 | Swift 12.88 m/s mean (75 m lap, 17.465 s best three laps) and seen/unseen ratio 2.58x (F3, EMP-A) | v = 3L/t3 with L = 75 m, t3 = 17.465 s; ratios to 5 and 7 m/s; MonoRace bracket 13–30 m/s taken as given | arithmetic (12.8829 m/s), units (speed), ratio 2.5766 and 1.8404, bracket containment, limit t→∞, sanity quantity 225 m/9 s = 25 m/s | verified (arithmetic; the 75 m lap-length and three-lap readings are source questions, not math) | math/empiricist/M-EMP-03.py.log |
| M-EMP-04 | To buy 2.58x through one limit at the dossier's elasticities needs T/W ~29, 2.6x/6.2x range, 52x less latency, and the latency route is impossible (F4, EMP-A) | constant elasticity e = dlnv/dlnX gives X_req = R^(1/e), R = 2.58: 6.656 (e=0.5) → T/W 29.3; 2.58 (e=1); 6.19 (e=0.52); 51.9 (\|e\|=0.24). Independent route: exact stop bound v·tau + v²/(2a) = d | arithmetic, identity (R^(1/e))^e = R, limits e→∞ and e→0, units; exact bound at d = 6 m, a = 40 m/s^2 gives v(0)/v(40 ms) = 1.076, limit tau→0 | verified, with a strengthening: the power-law extrapolation is only locally valid, but the exact bound shows zero latency buys at most ~8%, far below 2.58x — F4's conclusion holds a fortiori | math/empiricist/M-EMP-04.py.log |
| M-EMP-05 | Human-vs-Swift lap times imply \|e(speed,tau)\| = 0.016–0.122 for a 5.5x latency difference (F5, EMP-E elimination) | v ∝ 1/t at common lap length, so \|e\| = ln(t_h/t_s)/ln(tau_h/tau_s) with t_s = 17.465 s, t_h ∈ {17.956, 18.746, 21.160} s, tau 40 vs 220 ms | arithmetic (0.0163, 0.0415, 0.1126), arc/midpoint variant (0.020, 0.138), identity recovering p from v = C·tau^(-p), limit t_h→t_s ⇒ e = 0, dimensionless | verified (load-bearing content \|e\| ≈ 0.02–0.14 ≪ 0.5 holds on both definitions; my log-log upper end is 0.113, not the quoted 0.122 — a definitional/rounding difference that does not change F5) | math/empiricist/M-EMP-05.py.log |
| M-EMP-06 | Required stopping distance 0.51 / 1.65 / 5.80 m at 5 / 10 / 20 m/s with tau = 40 ms, a = 40 m/s^2 (F6, EMP-D) | d = v·tau + v²/(2a), straight line, no drag, constant deceleration after a pure delay | closed form (0.5125, 1.650, 5.800 m) vs 4e6-step numerical integration of the coast-then-brake profile (rel diff <1.4e-14), units (length), limits tau→0 and v→0, super-linear growth inequality | verified | math/empiricist/M-EMP-06.py.log |
| M-EMP-07 | "Latency is 5–24% of the required stopping distance above 5 m/s" (F5, calculations table; used for EMP-E) | share s(v) = v·tau/d(v) = tau/(tau + v/(2a)), tau = 40 ms, a = 40 m/s^2, v > 0 | closed form and table at v = 5…60 m/s, exact inversion of s(v), strict monotonicity via ds/dv < 0, limits v→0 and v→∞, dimensionless | **refuted as stated** — s = 39.0% at 5 m/s, 31.4% at 7 m/s, 24.2% at 10 m/s, 13.8% at 20 m/s; the band 5–24% corresponds to 10.1–60.8 m/s, not "above 5 m/s" | math/empiricist/M-EMP-07.py.log |
| M-EMP-08 | T/W 4.4 over 40 m gives a point-mass mean of 20.5 m/s; observed is 0.24–0.49 of it and 0.37–0.58 of the perception bound (F6, EMP-F) | a_max = g·sqrt((T/W)²−1) = 42.03 m/s^2 (altitude held); rest-to-rest bang-bang over L = 40 m gives v̄ = sqrt(a_max·L)/2 | closed form 20.5023 m/s vs 2e6-step integration of the triangular profile (distance 40.00000000 m), units (speed), fractions 0.2439/0.4878 and 0.3704/0.5833, limits T/W→1 and T/W→∞ | verified | math/empiricist/M-EMP-08.py.log |
| M-EMP-09 | Travel direction leaves a body-fixed FoV H at a_lat = g·tan(H/2): 1.00 g at 90°, 1.57 g at 115°, 4.51 g at 155°; tilt 76.0° at 4 g (F7, EMP-D) | T·cos θ = m·g, T·sin θ = m·a_lat ⇒ θ = atan(a_lat/g); boresight condition θ <= H/2 | identity tan(atan x) = x, atan 1 = π/4, thresholds 1.0000/1.5697/4.5107 g, tilt 75.96° at 4 g and 76.86° at the true 4.285 g of T/W 4.4, units (acceleration), limits a→0 (θ ≈ a/g) and H→180° (threshold → ∞) | verified (the lens's "4 g" is conservative: altitude-holding T/W 4.4 gives 4.285 g and 76.9°, so the quoted tilt is a lower bound) | math/empiricist/M-EMP-09.py.log |
| M-EMP-10 | Sim-to-hardware speed discounts 1.89, 2.42, 3.88, geometric mean 2.61 (F10, base rates, EMP-C) | r_i = v_sim/v_real for (10.0, 5.3), (19.4, 8.0), (19.4, 5.0) m/s; GM = (Πr_i)^(1/3) | arithmetic (1.8868, 2.4250, 3.8800; GM 2.6087), bracketing min < HM < GM < AM < max, AM–GM inequality, identity GM = exp(mean log), limit of equal ratios, dimensionless | verified (1/GM = 0.383, i.e. the "roughly 40 per cent" is 38%; the three pairs are not independent, as the lens states) | math/empiricist/M-EMP-10.py.log |
| M-EMP-11 | The range, acceleration and T/W elasticities lie within a factor of 2.3 (EMP-B) | max/min over endpoints of {0.52–1.0}, {0.43–0.48}, {0.50–0.565} | arithmetic: 1.0/0.43 = 2.3256; pairwise worst cases 2.326, 2.000, 1.314; midpoint spread 1.670; dimensionless | verified arithmetically (2.326 ≈ 2.3), but see Unverified/caveat: 2.326 > 2, so the brief's literal "within a factor of two" condition is met only on midpoints (1.67), not on endpoints | math/empiricist/M-EMP-11.py.log |
| M-EMP-12 | MonoRace mean-speed bracket 8.7–30.2 m/s from a 16.56 s lap time over 100–250 m laps (assumptions section, feeding the 4–6x in F3) | v̄ = (laps·L)/t with L ∈ [100, 250] m, t = 16.56 s | attempted reconstruction: single-lap reading gives 6.0–15.1 m/s, two-lap 12.1–30.2, three-lap 18.1–45.3 m/s | unverified — no lap-count convention reproduces 8.7–30.2 m/s from the stated inputs; the inputs behind the bracket are not fully stated | — |

## Refuted

- **M-EMP-07** (F5 / calculations-table bullet "latency is 5–24 per cent of the required stopping
  distance above 5 m/s"). With the lens's own inputs (tau = 40 ms, a = 40 m/s^2) the share
  s(v) = tau/(tau + v/(2a)) is strictly decreasing, so the quoted band fixes a speed interval:
  s = 24% at v = 10.13 m/s and s = 5% at v = 60.80 m/s. Over the regime the lens actually discusses
  (5–20 m/s) the share is **13.8–39.0 per cent**, and at 5 m/s — where the hardware is still at 100 per
  cent — latency accounts for 39 per cent of the required look-ahead, not 5–24 per cent. Corrected form:
  "latency is 14–39 per cent of the required stopping distance over 5–20 m/s, falling to 5 per cent only
  near 60 m/s". Depends on this: the "latency is a small share" leg of **F5** and of **EMP-E's**
  elimination. The elimination does not collapse — its other legs (the point-mass elasticities 0.037–0.24
  and the human-vs-Swift \|e\| ≈ 0.02–0.14, both verified in M-EMP-05 and unaffected) still put latency's
  elasticity well below the rivals — but the understated share should not be cited as independent support,
  and at the low end of the regime latency's geometric contribution is a third of the look-ahead budget,
  not a twentieth. **EMP-D** is mildly affected in the same direction: the correction makes the radial
  term slightly *more* latency-driven at 5–10 m/s, while leaving its "range is not saturated" claim
  (M-EMP-06, M-EMP-08) intact.

## Unverified

- **M-EMP-12**: the MonoRace mean-speed bracket 8.7–30.2 m/s cannot be reproduced from the inputs given
  (16.56 s lap time, 100–250 m lap length). A single-lap reading yields 6.0–15.1 m/s, a two-lap reading
  12.1–30.2 m/s, a three-lap reading 18.1–45.3 m/s; the quoted lower end 8.7 m/s matches none of these
  unless the ~40 per cent slower reliable policy is substituted for the fastest one, i.e. the bracket
  appears to mix policies or lap conventions. Where the derivations part ways: the lens does not state
  which lap count its bracket uses. This affects only the loose "4–6x" bracket in F3; the firm leg of F3
  (12.88 m/s vs 5–7 m/s, ratio 2.58x) is verified in M-EMP-03 and does not use it.
- Caveat attached to **M-EMP-11** (arithmetic verified, inference not): the endpoint spread is 2.326,
  which *exceeds* the brief's stated "within a factor of two" trigger for declaring no dominance. EMP-B's
  appeal to that trigger holds on band midpoints (spread 1.67) but not on the band endpoints the lens
  quotes.
- Not checked at all (outside this lens's derivations, by the lens's own statement): the point-mass
  elasticity values 0.037–0.24, 0.43–0.48, 0.50–0.565 and 0.52–1.0 themselves, which the lens imports
  from the dossier [A-32]–[A-34] rather than derives; and the perception bound 12.0–13.5 m/s, likewise
  imported. M-EMP-04, M-EMP-07 and M-EMP-11 take them as inputs.

## Formalizable

- M-EMP-01: for X ~ Binomial(n, p), the Clopper–Pearson endpoints satisfy P(X >= k \| p_L) = alpha/2 and
  P(X <= k \| p_U) = alpha/2, with P(X >= k \| p) = I_p(k, n−k+1); for k = n, p_L = (alpha/2)^(1/n).
- M-EMP-02: min{n ∈ N : alpha^(1/n) >= q} = ceil(ln alpha / ln q) for 0 < alpha < q < 1, and this is the
  smallest all-success sample size whose exact lower confidence bound reaches q.
- M-EMP-04: for e > 0 and R > 1, (R^(1/e))^e = R, and R^(1/e) → ∞ as e → 0+ while R^(1/e) → 1 as e → ∞.
- M-EMP-06: d(v) = v·tau + v²/(2a) is the exact coast-then-brake distance, equals ∫v dt of the two-phase
  profile, and is strictly convex and super-additive in v: d(2v) > 2 d(v) for a > 0, v > 0.
- M-EMP-07: s(v) = tau/(tau + v/(2a)) is strictly decreasing on v > 0 with s(0+) = 1, s(∞) = 0; hence
  s(v) ∈ [s1, s2] ⟺ v ∈ [s^{-1}(s2), s^{-1}(s1)], an exact interval correspondence.
- M-EMP-08: for a rest-to-rest symmetric bang-bang over distance L at magnitude a, the mean speed is
  sqrt(aL)/2 = v_peak/2 and the duration is 2 sqrt(L/a).
- M-EMP-09: tan θ = a/g with T cos θ = mg, T sin θ = ma; the boresight condition θ <= H/2 is equivalent
  to a <= g tan(H/2), monotone increasing in H on (0, π).
- M-EMP-10: for positive r_i, min r_i <= HM <= GM <= AM <= max r_i, with equality iff all r_i are equal.
- M-EMP-11: for finite positive sets, max/min is the tightest common multiplicative bound, and the
  midpoint spread of a family of intervals is never larger than its endpoint spread.
