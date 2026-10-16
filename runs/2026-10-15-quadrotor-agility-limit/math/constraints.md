# Math check: constraints
status: final

Unit system: SI throughout (m, s, kg, N, N m, rad, W; g = 9.81 m/s^2). Every check was
re-derived from the stated definitions in `math/constraints/<ID>.py`; none of the lens's
scripts was imported, read for its derivation or run. Platform parameters (m, l = 0.14 m,
arm angle 56 deg, Jx, k_f = 1.51e-6 N s^2, f_max, tau_motor = 39.1 ms) and the A-18 error
data are taken as inputs from the dossier; the source checks own their provenance.

| ID | Claim (finding) | Statement checked | Checks | Verdict | Log |
|---|---|---|---|---|---|
| M-CONSTRAINTS-01 | Static envelope and jerk ceiling (F1, F3) | a_h = g sqrt((T/W)^2-1) at tilt arccos(W/T), hover throttle (mg/4)/f_max; j_z(0) = 8 k_f w_h (w_max-w_h)/(m tc), t95 = -tc ln[(w_max-w_95)/(w_max-w_h)]; T/W, m, f_max, k_f, tc > 0 | identity a_h = g tan(arccos(1/(T/W))), limits T/W -> 1 and -> oo, limit tc -> oo, units m/s^2 and m/s^3, 20 numeric values (39.0/44.3/120.8 m/s^2, 75.9/85.4 deg, 24.4/21.6/8.1 %, 514/577/1262/2011 m/s^3, 117 ms, 858 m/s^3) | verified | math/constraints/M-CONSTRAINTS-01.py.log (28 pass) |
| M-CONSTRAINTS-02 | Unidirectional-thrust torque ceiling, and the peak body rate (F2, F13) | f_i in [0, f_max], two-pair split: max tau_x at fixed T is l_eff min(T, 4 f_max - T), l_eff = l sin(56 deg) = 0.1161 m; at T = mg this is l_eff m g independent of f_max; global max l_eff 2 f_max at a 1.05 g climb; a_down = -g, a_up = (4 f_max - mg)/m; omega_peak = sqrt(theta alpha) | brute-force maximisation over 201 collectives x 2001 splits matches the closed form to 8e-16 N m, both branch identities, concavity inequality, units N m and 1/s^2, limit theta -> 0, values 0.990/0.592 N m, 396/348/812 rad/s^2, asymmetry 3.10/11.35, 1857 deg/s | verified | math/constraints/M-CONSTRAINTS-02.py.log (23 pass) |
| M-CONSTRAINTS-03 | Momentum-theory power, C-rate, lap energy (F12) | P_ideal = 4 (T/4)^1.5/sqrt(2 rho A), A = pi (0.0635 m)^2, rho = 1.225 kg/m^3, electrical = P/FoM with FoM 0.65-0.75; C = P/(14.8 V x 1.8 Ah); lap = P t/pack | identity P = T v_i with T = 2 rho A v_i^2, limit A -> oo, units W, J, 18 numeric values (71/208/588 W ideal, 94-109/277-320/784-904 W, 53-61 A, 0.41 Wh = 1.5 %); **two lens C-rate lower bounds are 8 % low** (9.6 -> 10.4 C half throttle, 27 -> 29.4 C full) | verified | math/constraints/M-CONSTRAINTS-03.py.log (25 pass, 2 fail = the two C-rate lower bounds) |
| M-CONSTRAINTS-04 | Slew and segment times with a first-order lag, and the lost distance (F4, F5) | J xddot = u, udot = (u_cmd-u)/tc, one switch, rest to rest: tc = 0 gives 2 sqrt(DJ/U); theta = 152 deg at alpha = 396.2 rad/s^2 gives 163.7 ms, 201 ms at tc = 39.1 ms (penalty 18.4 % of the lagged time), d ln t/d ln tc = +0.177; d = 10 m at A = 39.0 m/s^2 gives 1012.5 ms + 40.6 ms (4.0 %), elasticities +0.040 and -0.481; reversal distance v t | two independent models (semi-analytic phase solution; RK4 at two step sizes agreeing to 3e-6 s) plus a third model with the rotor-speed lag acting through f = k_f omega^2, which gives 200.9 ms (lens 201) and elasticity +0.179 (lens 0.177); limits tc -> 0 and U -> oo, identity d ln t0/d ln U = -1/2, units s and m, 3.01/4.02 m at 15/20 m/s | verified | math/constraints/M-CONSTRAINTS-04.py.log (27 pass) |
| M-CONSTRAINTS-05 | Hover-linearisation controllability, sigma_min and transmission zeros (F6, F7) | 12-state ZYX hover linearisation, 4 inputs: Kalman rank 12, sigma_min 0.944 (drag) / 1.149 (no drag) / 1.96 scaled; zeros of tau_x -> y: none in the RHP, two LHP zeros at -0.4828 and -0.2989 rad/s with linear rotor drag | not re-derived (budget); no candidate answer rests on it and the lens itself files both rows as "not a constraint here" | unverified | - |
| M-CONSTRAINTS-06 | Latency budget sums and the cascaded rate-loop crossover (F8) | 40 + 10/2 + 39.1 = 84.1 ms, 17 + 2/2 + 39.1 = 57.1 ms, 130 + 20/2 + 39.1 = 179.1 ms; L = k e^{-th s}/(Jx s (1+tc s)) at PM 45 deg solves atan(wc tc) + wc th = pi/4, so wc = 1/tc at th = 0: 25.58 rad/s = 4.07 Hz (tc = 39.1 ms), 30.30 (33 ms), 100 (10 ms), 23.30 (39.1 + 2 ms), and d ln wc/d ln tc = -1 | symbolic phase condition, identity wc tc = tan(pi/4), elasticity identity -1, limit tc -> 0, units s; `control_tools.loop_margins` returns PM = 45.000 deg at each predicted crossover (6 cases), elasticity -1.0000 numerically at th = 0 (-0.914 at th = 2 ms) | verified | math/constraints/M-CONSTRAINTS-06.py.log (27 pass) |
| M-CONSTRAINTS-07 | Feedback-only speed ceiling vs flatness feedforward (F9) | e = v/wc and wc <= (pi/2 - PM)/tau give v_max = e_allow (pi/2-PM)/tau with elasticity -1: 11.78 / 7.85 / 26.93 / 3.62 m/s at tau = 40 (PM 45, 60), 17.5, 130 ms, e_allow = 0.60 m; with feedforward e = a_d/wc^2 gives wc_min = sqrt(a_d/e_allow) = 0.875 rad/s, tolerating 897 ms (22.4x over 40 ms), residual 1.193 mm at 19.63 rad/s | phase-condition identity PM = pi/2 - wc tau, elasticity identity -1, three `loop_margins` checks reproducing PM = 45/45/60 deg at the predicted crossover, limit wc -> oo, units 1/s, m/s, 1/s^2, m, 11 numeric values | verified | math/constraints/M-CONSTRAINTS-07.py.log (23 pass) |
| M-CONSTRAINTS-08 | Model-error power law and the clearance crossing (F10) | log-log OLS of the A-18 replay RMSE gives e(v) = 0.0493 v^0.858 (R^2 0.83, BEM) and 0.0439 v^1.173 (R^2 0.89, Fit); with budget B = 0.60 - 0.151 = 0.449 m, v* = (B/c)^(1/k) = 13.1 and 7.3 m/s; d ln v*/d ln c = -1/k = -1.17/-0.85; d ln v*/d ln C = C/(k(C-e_est)) = +1.56/+1.14; halving c multiplies v* by 2^(1/k): 29.5 and 13.1 m/s | my own OLS from the four dossier data points reproduces c, k and R^2 to 0.5 % for both columns; symbolic elasticity identities; limit k -> 1; identity for the 2^(1/k) factor; units m; quantity check that c v*^k = B | verified | math/constraints/M-CONSTRAINTS-08.py.log (23 pass) |
| M-CONSTRAINTS-09 | Look-ahead / stop bound with reorientation, and its elasticities (F11) | v tau_tot + v^2/(2a) <= s with tau_tot = tau_sense + 2 sqrt(theta/alpha); v* = -a tau + sqrt((a tau)^2 + 2 a s); a = 39.0 m/s^2, alpha = 396.2 rad/s^2, theta = 76 deg -> 116 ms (90 deg 126 ms); v* 26.4 -> 22.5 m/s at s = 10 m and 20.1 -> 16.4 at s = 6 m; e_tau -0.056 -> -0.212 (-0.054 for tau_sense alone), e_s +0.53 to +0.64; look-ahead 1.10/2.84/5.22/8.24 m with 71/55/45/38 % reaction | identity v* tau + v*^2/(2a) = s, limits tau -> 0 (Torricelli) and a -> oo (s/tau), bang-bang closed-form identity, symbolic elasticities cross-checked by finite difference to 1e-11, sign inequality, units m and s^2, 23 numeric values including 2^0.53 = 1.44 and 2^0.040 = 1.03 | verified | math/constraints/M-CONSTRAINTS-09.py.log (31 pass) |
| M-CONSTRAINTS-10 | "The measured 84.1 ms admits a closed-loop bandwidth of only 4.40 rad/s (0.70 Hz)"; 57.1 ms -> 7.91 rad/s (F8, table row C5) | Given the lens's own LQR trace (bandwidth 2.25/4.40/7.91/14.07/25.03/44.50 rad/s against delay margin 179.37/120.59/76.74/46.58/27.25/15.26 ms, one decade of R apart), the largest closed-loop bandwidth whose delay margin covers a budget tau_eff | the trace is strictly decreasing, so the admissible bandwidth at 84.1 ms lies strictly between 4.40 (dm 120.6 ms) and 7.91 rad/s (dm 76.7 ms); log-linear interpolation gives 7.02 rad/s (1.12 Hz), and at 57.1 ms 11.12 rad/s (1.77 Hz). The quoted figures are exactly the decade-grid maxima (reproduced to 1e-6) | refuted | math/constraints/M-CONSTRAINTS-06.py.log (27 pass; section 3) |

## Refuted

- M-CONSTRAINTS-10: F8's "tau_eff = 40 ms + 5 ms + 39.1 ms = 84.1 ms admits a closed-loop
  bandwidth of only 4.40 rad/s (0.70 Hz)" is a grid artefact, not the bound. 4.40 rad/s is the
  largest point of a one-decade-in-R LQR grid whose delay margin (120.6 ms) covers the budget;
  the next grid point, 7.91 rad/s, has delay margin 76.7 ms. Since delay margin falls
  monotonically along that family, the admissible bandwidth is strictly between the two, about
  **7.0 rad/s (1.1 Hz)** by log-linear interpolation, i.e. the lens understates it by ~1.6x.
  The same artefact affects the MonoRace line (57.1 ms admits ~11.1 rad/s, not 7.91 rad/s);
  the 2019 line (179.1 ms -> 2.25 rad/s) is exact because the budget lands on a grid point.
  Direction: conservative. It strengthens rather than weakens [CONSTRAINTS-D] ("estimation
  latency does not bind"), and leaves the rate-loop figure that the candidates actually quote
  (4.07 Hz, M-CONSTRAINTS-06) untouched. Correct the F8 sentence to "about 1.1 Hz" and note
  that the admissible bandwidth was read off a coarse grid.
- Sub-claim of M-CONSTRAINTS-03 (F12, table row C9): the lower C-rate bounds "9.6 C" at half
  throttle and "27 C" at full throttle are 8 per cent low. With the pack the same finding uses
  for hover (4S 1800 mAh, 14.8 V, 26.6 Wh, and the hover 3.5-4.1 C and the upper bounds
  12.0 C and 34 C all match it exactly), P/(V Ah) gives **10.4 C** and **29.4 C** at FoM 0.75.
  The finding's conclusions (energy three orders of magnitude from binding; ~30 C and 53-61 A
  at full throttle) are unaffected, and no candidate answer depends on it.

## Unverified

- M-CONSTRAINTS-05 (F6, F7): I did not rebuild the 12-state hover linearisation, so the Kalman
  rank 12, the controllability-matrix sigma_min (0.944 / 1.149 / 1.96 scaled) and the
  transmission zeros of tau_x -> y (none in the RHP; -0.4828 and -0.2989 rad/s with drag) are
  unchecked. Nothing in the slate rests on them: F6 and F7 conclude "not a constraint here",
  and the two reported LHP zeros equal kd_z/m = 0.42/0.87 = 0.483 and kd_x/m = 0.26/0.87 =
  0.299 s^-1, which is what decoupled drag modes would give, so the numbers are at least
  self-consistent. A full check needs the hover Jacobian and a generalised-eigenvalue zero
  computation.
- Two further limitations of otherwise verified claims, recorded because they bound what the
  verifications mean and not because the arithmetic is in doubt: (i) M-CONSTRAINTS-04's 201 ms
  slew is reproduced only with the rotor-speed lag acting through f = k_f omega^2 (my model
  with a first-order lag on *torque* gives 207.1 ms and elasticity +0.198, 3 per cent slower,
  because the quadratic map makes the initial torque slope sqrt(2) times larger); the lens's
  "18.4 per cent" is the penalty divided by the *lagged* slew time (22.8 per cent if divided by
  the lag-free time). (ii) M-CONSTRAINTS-08 verifies the fit and the algebra, not the physical
  extrapolation of a fit made on 1.67-6.92 m/s data out to 13-29 m/s, which the lens itself
  flags as its weakest step.

## Formalizable

- M-CONSTRAINTS-02: for f in [0, f_max]^4 with sum f = T fixed, max of l_eff (f_1+f_4-f_2-f_3)
  equals l_eff min(T, 4 f_max - T); and the corollary that the value at T = m g is independent
  of f_max whenever m g <= 2 f_max. A bounded linear programme in four variables.
- M-CONSTRAINTS-02: for a double integrator with |u| <= U, the rest-to-rest minimum-time
  solution through theta has peak rate sqrt(theta U/J) and duration 2 sqrt(theta J/U).
- M-CONSTRAINTS-09: v* = -a tau + sqrt((a tau)^2 + 2 a s) is the unique positive root of
  v tau + v^2/(2a) = s; d ln v*/d ln tau = -(1 - a tau/R) a tau/v* with R = sqrt((a tau)^2+2as)
  lies in (-1, 0), and d ln v*/d ln s = a s/(R v*) lies in (0, 1), for all a, s, tau > 0.
- M-CONSTRAINTS-08: for e(v) = c v^k and v* = ((C-e_est)/c)^(1/k) with 0 < e_est < C and
  c, k > 0: d ln v*/d ln c = -1/k, d ln v*/d ln C = C/(k(C-e_est)), and halving c scales v* by
  2^(1/k) > 1.
- M-CONSTRAINTS-06: for L(s) = k e^{-th s}/(J s (1 + tc s)) the phase-margin-PM crossover
  satisfies atan(wc tc) + wc th = pi/2 - PM, which has a unique positive root; at th = 0 and
  PM = pi/4 it is wc = 1/tc, with elasticity d ln wc/d ln tc = -1 exactly, and |elasticity| < 1
  for th > 0.
- M-CONSTRAINTS-07: for a pure delay with an integrator-like loop, wc = (pi/2 - PM)/tau, so
  v_max = e_allow wc has elasticity exactly -1 in tau; and e = a_d/wc^2 is strictly decreasing
  to 0 in wc.
- M-CONSTRAINTS-10: if a finite sequence (w_i, d_i) is strictly decreasing in d and
  d_{j+1} < B < d_j, then max{w : d(w) >= B} lies in (w_j, w_{j+1}) for any monotone
  interpolant; hence a grid maximum is a strict lower bound on the admissible bandwidth.
