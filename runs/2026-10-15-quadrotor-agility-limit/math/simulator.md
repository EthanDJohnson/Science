# Math check: simulator
status: final

Unit system: SI throughout (g = 9.80665 m/s^2, m = 0.75 kg, 4 x 8.5 N of thrust). No
gravitational units are used. Every check was re-derived from the stated definitions in
`math/simulator/*.py`; nothing was imported from `calc/lens-simulator_*.py`.

| ID | Claim (finding) | Statement checked | Checks | Verdict | Log |
|---|---|---|---|---|---|
| M-SIMULATOR-01 | t_opt = 4.5020 s, path 98.315 m, mean 21.838 m/s, peak 28.2 m/s (F2; the metric's denominator) | point-mass time optimum on the FIXED path y = 3 sin(2 pi x/30) m, 0 <= x <= 90 m, isotropic horizontal bound \|a\| <= a_h = 44.260 m/s^2, a_t^2 + (kappa v^2)^2 <= a_h^2, flying start and finish | own velocity-limit-curve forward-backward solver, grid convergence 2e3/2e4/2e5, limits (straight rest-to-rest 2 sqrt(S/a), circular cruise sqrt(aR)), units | verified | math/simulator/M-SIMULATOR-01.py.log |
| M-SIMULATOR-02 | a_h = g sqrt((T/W)^2 - 1) = 44.260 m/s^2, T/W = 4.6227, tilt 77.51 deg, zero vertical residual (F1, F2) | level flight with thrust along body z: cos(theta) = 1/r, a_x = g sqrt(r^2 - 1), r = T/(mg) > 1 | identity (two algebraic forms), limits r -> 1 and r -> oo, inequality a_h < T/m, units | verified | math/simulator/M-SIMULATOR-02.py.log |
| M-SIMULATOR-03 | U_feas = 18.339 m/s; the smooth family costs 9.01 per cent of t_opt at its ceiling (F5, F11, SIMULATOR-E) | constant-x-speed reference: \|a\| peaks at A k^2 U^2 (A = 3 m, k = 2 pi/30 m^-1); U_feas = sqrt(a_h/(A k^2)); t = 90/U | symbolic second derivative, brute-force max over a period (44.25992 vs a_h), penalty arithmetic, units | verified | math/simulator/M-SIMULATOR-03.py.log |
| M-SIMULATOR-04 | PM = 90 deg - (w_c tau + atan(w_c T_m)); at tau = 2 ms, T_m = 39.1 ms, PM = 40 deg gives w = 39.94 rad/s, w_c = 27.3 rad/s; pole 25.6 rad/s; no-lag case exceeds the 400 rad/s cap; 291 rad/s is the pure-delay closed form (F3, F4, SIMULATOR-B) | SISO loop L = (w/s) e^{-s tau}/(1 + s T_m); \|L(j w_c)\| = 1; bisection on w_c | formula vs direct complex evaluation of arg L at three frequencies, bisection, limits tau -> 0 and T_m -> 0, units | verified | math/simulator/M-SIMULATOR-04.py.log |
| M-SIMULATOR-05 | delay margins 27.57 ms (inner, PM 43.13 deg, w_c 27.303 rad/s) and 354.0 ms (outer) against 2.00 / 22.50 ms budgets, 7.3 / 6.4 per cent used (F12, SIMULATOR-C) | DM = PM(rad)/w_c for L = 39.938/(s(1+0.0391 s)) and L = 4.438/s | own crossover solve, closed form pi/(2w) to 1e-9, limit T_m -> 0, monotonicity of DM in w_c, units | verified | math/simulator/M-SIMULATOR-05.py.log |
| M-SIMULATOR-06 | the actuator pole, not the delay, caps the rate loop at the measured values; delay "takes over" above ~5 ms with a 5 ms actuator and ~20 ms with no lag (F4, SIMULATOR-B) | phase split at the PM = 40 deg crossover; threshold tau*(T_m) under two reconstructed criteria (R1 equal phase contributions; R2 delay-only gain matched to the 39.938 rad/s baseline) | phase split 46.871 deg lag vs 3.129 deg delay (factor 15.0); R1 gives tau* = 4.679 ms at T_m = 5 ms; R2 gives tau* = 21.851 ms with no lag; gain sweeps in tau and T_m; identity, inequality, units | verified (see note) | math/simulator/M-SIMULATOR-06.py.log |
| M-SIMULATOR-07 | the elasticity table is the arc elasticity ln(v2/v1)/ln(x2/x1) of the reported speeds, and the seen-course comparisons hold (F6, F7, SIMULATOR-B/D) | motor_tau -1.023; range +0.986/+1.082; thrust +0.003; ratio 9.4; largest/smallest < 4; two biggest within 15 per cent; +0.527 vs hardware +0.565 within 7 per cent | recomputation from the lens's own speeds (-1.0231, +0.9863, +1.0824, +0.0031, 9.3905, 3.992, 14.07 per cent, 6.73 per cent); two independent routes to v(10 N) agree to 0.014 per cent; tau_vio chain monotone and consistent (-0.1773 composite); log-space identities | verified | math/simulator/M-SIMULATOR-07.py.log |
| M-SIMULATOR-08 | point-mass dodge bound with e_range = 1 exactly, and v_sim/v_pm = 0.848-0.920 (F8, F9, SIMULATOR-A) | v = s/(tau + t_man) with d = 0.75 m, a = a_h; t_man = sqrt(4 d/a) (symmetric bang-bang) or sqrt(2 d/a) (one-sided) | both models evaluated; symmetric reproduces 0.8752 / 0.8836 / 0.9128 against the lens's 0.875 / 0.884 / 0.913 and the latency elasticities -0.1053 / -0.1435 against -0.105 / -0.143; one-sided is off by 0.21 (so the lens used the symmetric form); symbolic e_s = 1 and e_tau = -tau/(tau+t_man); limits tau -> 0 and tau -> oo; units | verified | math/simulator/M-SIMULATOR-08.py.log |
| M-SIMULATOR-09 | h-force 4.0 N at 20 m/s = 54 per cent of weight; drag-limited level top speed 99.1 m/s, so the speed cap never binds (F10, F2) | Sun et al. eq. 9 in the body frame with kd = (0.26, 0.28, 0.42) kg/s, kh = 0.01 kg/m; steady level flight at T = 34 N solved in (V, theta) | kh V^2 = 4.0000 N, 54.38 per cent of 7.355 N; full eq. 9 gives V_top = 97.509 m/s at 73.82 deg (1.6 per cent below the lens's 99.1 m/s); kh = 0 gives 79.7 m/s, isotropic world drag 127.7 m/s; residual < 1e-14 N; V_top > 2 x 28.2 m/s; units | verified | math/simulator/M-SIMULATOR-09.py.log |
| M-SIMULATOR-10 | mean speed = S/t and fraction = t_opt/t in every closed-loop row; Wilson 95 per cent [0.886, 1.000] for 30/30 (F5, tables) | S = 98.315 m, t_opt = 4.5020 s; Wilson score interval with z = 1.959964 | all eight scored rows close (worst 0.004 per cent on speed, 0.091 per cent on fraction); Wilson [0.886487, 1.000000]; identity (S/t)/(S/t_opt) = t_opt/t | verified | math/simulator/M-SIMULATOR-10.py.log |
| M-SIMULATOR-11 | "setting tau_in to zero raises [the achievable gain] only to 43.3 rad/s", i.e. "zeroing the delay gains 8 per cent of bandwidth" (F4, SIMULATOR-B) | same loop as M-SIMULATOR-04 with tau = 0 and T_m = 39.1 ms at PM = 40 deg | bisection: tau = 0 gives w = 47.418 rad/s (+18.7 per cent), not 43.3; 43.275 rad/s is the tau = 1 ms case | refuted | math/simulator/M-SIMULATOR-04.py.log |
| M-SIMULATOR-12 | "the range elasticity is 2 to 10 times every rival" (SIMULATOR-A) | ratio of +0.986 / +1.082 to each rival elasticity quoted in the same sentence | worst case 0.986/0.527 = 1.871 < 2 (thrust-to-weight); the true span is 1.87-7.57 x, or 9.4 x only against perception latency | refuted | math/simulator/M-SIMULATOR-07.py.log |
| M-SIMULATOR-13 | "baseline closed loop at U = 12 m/s (mean 13.053 m/s, 72 per cent of t_opt)" (failure-boundary table) | fraction = t_opt/t with t = S/13.053 m/s | t = 7.5320 s, t_opt/t = 0.5977, so 59.8 per cent; 0.723 is 13.053/18.05, a ratio to U*, not to t_opt | refuted | math/simulator/M-SIMULATOR-10.py.log |

Note on M-SIMULATOR-06: the load-bearing part (at the measured values the actuator lag
contributes 46.87 deg of the 50 deg phase budget against the delay's 3.13 deg, a factor of
15, and the crossover sits at 1.07 times the actuator pole) is reproduced exactly. The two
quoted thresholds reproduce only under two *different* reconstructed criteria -- 4.679 ms
from equal phase contributions with a 5 ms actuator, 21.851 ms from matching the delay-only
achievable gain to the 39.938 rad/s baseline -- so the sentence's "takes over" is not one
criterion. Both numbers are right under a stated reading, which is why this is verified
rather than unverified, but a downstream agent should quote the criterion with the number.

## Refuted
- M-SIMULATOR-11: zeroing the inner delay raises the achievable rate-loop gain from
  39.938 to **47.418 rad/s (+18.7 per cent)**, not to 43.3 rad/s (+8 per cent). The 43.275
  rad/s figure is what you get at tau = 1 ms, i.e. zeroing tau_imu only and keeping the
  500 Hz ZOH half-period; the lens labelled it "tau_in to zero" while tau_in = tau_imu +
  T_inner/2 = 2 ms by its own definition. Affects finding 4 and candidate [SIMULATOR-B]
  ("zeroing the delay gains 8 per cent of bandwidth, zeroing the lag gains a factor of 10"):
  the correct contrast is +18.7 per cent against x10.93. The direction and the ranking are
  unchanged -- the actuator lag still dominates the delay by a factor of ~15 in phase and
  ~10 in achievable gain -- so [SIMULATOR-B] survives with a corrected number, and the
  corrected figure slightly *raises* the value of removing inner-loop latency.
- M-SIMULATOR-12: the dodge range elasticity is **1.87 to 7.6 times** its rivals, not
  "2 to 10 times": against thrust-to-weight (+0.527) the ratio is 1.871 with the +0.986 arc
  and 2.05 with the +1.082 arc, and the 9.4 figure holds only against perception latency
  (-0.105). Affects the "why" of [SIMULATOR-A]. The qualitative claim (range is the only
  elasticity near unity, and the largest in the slate) stands; the quantitative span should
  read "about 1.9 to 7.6 times every in-vehicle rival, and 9.4 times perception latency".
- M-SIMULATOR-13: the U = 12 m/s row of the failure-boundary table is **59.8 per cent of
  t_opt**, not 72 per cent (t = 98.315/13.053 = 7.532 s, t_opt/t = 0.5977). 0.723 is
  13.053/18.05, the ratio of that run's mean path speed to U* at the 0.50 m tolerance.
  Affects only that table cell; no candidate rests on it.

## Unverified
- Nothing material. Two inputs could not be settled from the analysis alone and are recorded
  as assumptions I had to supply, both of which reproduce the lens's numbers:
  (i) M-SIMULATOR-01's boundary condition -- t_opt = 4.5020 s is the **flying-start**
  optimum (my solver: 4.50079 s); rest-to-rest on the same path and bound gives 5.03924 s,
  12 per cent longer, which would raise every "fraction of t_opt" by the same factor. The
  lens never states which, and its closed-loop runs do start flying, so the flying-start
  reading is the consistent one, but the denominator of the whole agility metric depends on
  this choice and should be stated explicitly.
  (ii) M-SIMULATOR-09(b): my steady-level-flight solution of Sun et al. eq. 9 at full thrust
  gives 97.509 m/s against the lens's 99.1 m/s (1.6 per cent apart, within my 5 per cent
  tolerance). The residual difference is most likely a different projection of the body-frame
  aero force or a slightly different thrust cap; it changes nothing, since the claim that
  matters is only that the cap (97-99 m/s) is far above the 28.2 m/s peak profile speed.
- Everything in the lens's verification table that is a property of ITS implementation
  (energy drift 5.9e-12, quaternion norm, RK4 order 4.005, two-implementation agreement,
  `linearize` residuals) is outside a math check: those are reproducible only by rerunning
  its scripts, which this check is forbidden to do. Their plausibility is unaffected by my
  verdicts, and the closed-form rows they contain (free fall, g*theta, the T/W ceiling, the
  two time-optimal limits, pi/(2w)) are independently reproduced here in M-SIMULATOR-01,
  -02 and -05.

## Formalizable
- M-SIMULATOR-02: for r > 1 and g > 0, g sqrt(r^2 - 1) = g r sqrt(1 - 1/r^2) =
  sqrt((g r)^2 - g^2), it is strictly increasing in r, strictly below g r, and tends to 0 as
  r -> 1 and to g r as r -> oo. Finite real algebra.
- M-SIMULATOR-04 / -05: for w, T_m > 0 and tau >= 0, the map w_c |-> w_c sqrt(1 + (w_c T_m)^2)
  is a strictly increasing bijection of (0, oo), so the gain crossover is unique; and
  PM(w_c) = pi/2 - w_c tau - atan(w_c T_m) is strictly decreasing, so the PM = const
  equation has at most one root and the bisection is exact. The delay margin
  DM = PM(w_c)/w_c satisfies DM <= pi/(2 w_c) with equality iff tau = T_m = 0.
- M-SIMULATOR-08: for s, d, a > 0 and tau >= 0 with t_man = sqrt(4 d/a),
  v(s, tau) = s/(tau + t_man) satisfies (s/v) dv/ds = 1 identically and
  (tau/v) dv/dtau = -tau/(tau + t_man) in (-1, 0], monotone decreasing in tau, with limits 0
  and -1. Pure calculus in finitely many variables.
- M-SIMULATOR-07: arc elasticity e(v1, v2; x1, x2) = ln(v2/v1)/ln(x2/x1) is invariant under
  simultaneous exchange of the endpoint pairs, is additive over a chain in log space, and
  equals 1 exactly for v = c x. Finite-dimensional identity.
- M-SIMULATOR-10: the Wilson score interval at k = n, p = 1 has lower endpoint
  (1 + z^2/2n - z sqrt(z^2/4n^2))/(1 + z^2/n) = 1/(1 + z^2/n), which for n = 30,
  z = 1.959964 is 0.886487; an exact closed form worth stating as a lemma.
- M-SIMULATOR-01 (heavier): on a fixed C^2 path with the isotropic bound
  a_t^2 + (kappa v^2)^2 <= a_h^2, the pointwise minimum of the forward and backward
  integrations clipped to v <= sqrt(a_h/kappa) is the pointwise-maximal feasible speed
  profile, hence time-optimal. A statement in optimal control, provable but not finite.
