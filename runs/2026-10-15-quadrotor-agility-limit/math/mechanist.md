# Math check: mechanist
status: final

All derivations below are independent: built from the stated definitions, the Sun et al. TABLE II
parameters in `runs/2026-10-15-quadrotor-agility-limit/tools/quadrotor.py` (m = 0.75 kg,
l = 0.14 m, arm angle 56 deg, J = diag(2.5, 2.1, 4.3) g m^2, f_max = 8.5 N, k_f = 1.51e-6
N s^2/rad^2, k_m = 2.37e-8 N m s^2/rad^2) and the numbers the lens quotes. The lens's own calc
scripts were neither read nor run. SI units throughout; angles in degrees where stated.

| ID | Claim (finding) | Statement checked | Checks | Verdict | Log |
|---|---|---|---|---|---|
| M-MECH-01 | Stop look-ahead bound, braking acceleration, crossing speeds (F1, MECH-REFRAME) | a_h = g sqrt(W^2-1) from T cos(theta) = m g; s_req = v tau + v^2/(2 a_h); v* = a(sqrt(tau^2 + 2s/a) - tau); a_h = 42.03 m/s^2 at W = 4.4; s_req = 0.933 / 1.332 m at v = 7 m/s, tau = 50/107 ms; v* = 12.01 / 18.41 / 24.84 m/s at s = 3/6/10 m; d ln a_h/d ln W = W^2/(W^2-1) = 1.067 at W = 4 | identity (tilt geometry, exact inversion s_req(v*) = s), limits W -> 1, W -> oo, tau -> 0 (sqrt(2 a s)), s -> 0, units | verified | math/mechanist/M-MECH-01.py.log (19 PASS) |
| M-MECH-02 | FoV cap on usable acceleration and the coupled stop bound (F2, MECH-A) | theta = atan(a_x/g) = 27.01/45.55/63.87/75.52 deg; a_u = min(a_h, g tan(half-FoV + mount)) = 5.438 / 16.327 / 44.250 m/s^2 at phi = 29 / 59 / 77.5 deg; coupled bound at s = 6 m, tau_sense = 107 ms = 7.376 / 11.797 m/s (half the bang-bang rotation added as blind time); MECH-A's three-optics prediction 7.38 / 11.52 / 17.24 m/s | identity, limit phi -> 0 (no usable tilt) and phi -> 85 deg (cap inactive, a_u = a_h), units, 17 quantity comparisons | verified | math/mechanist/M-MECH-02.py.log (17 PASS) |
| M-MECH-03 | Elasticity ranking FoV > range >> latency > actuator > thrust (F3, MECH-A, MECH-NULL) | one-at-a-time +10 % at s = 6 m, tau_sense = 107 ms, half-FoV 29 deg, mount 30 deg: half-FoV **+4.67 %** (lens +10.5 %), range +5.85 %, latency +1.23 %, motor tau +0.19 %, T/W +0.00 %; analytic d ln v/d ln s = (r+tau)/(2r) = +0.598, d ln v/d ln a = +0.402, d ln v/d ln tau = -tau/r = -0.197 | identity (three closed-form elasticities), numeric perturbations, quantity | **refuted** (in the FoV row only) | math/mechanist/M-MECH-03.py.log (11 PASS, 1 FAIL) |
| M-MECH-04 | Reorientation blind time and motor-lag elasticity (F4, MECH-D) | tau_max = 1.3309 N m, alpha_max = 633.8 rad/s^2, theta_t = 77.50 deg; ideal bang-bang 92.40 ms (closed form 2 sqrt(theta/alpha)); with the 39.1 ms first-order rotor-speed lag and thrust ~ omega^2, **133.9 ms** (132.9 ms with the lag on torque instead), i.e. the lag costs 41.6 ms, not 3-9 ms; d ln tau_rot/d ln motor_tau = +0.27, d ln v/d ln motor_tau = -0.019, halving the lag = +1.04 % speed | identity, ODE integration with bisection on the switch time, monotone lag -> 0 limit recovering the closed form, units | **refuted** (the 95.6 ms lagged time; the elasticity conclusion stands) | math/mechanist/M-MECH-04.py.log (7 PASS, 1 FAIL) |
| M-MECH-05 | Rotor spin-down closed form and the J_r it implies (F5) | J_r omega' = -k_m omega^2 solved exactly by omega = omega_0/(1 + t/t_c), t_c = J_r/(k_m omega_0); t_c = 39.1 ms -> J_r = 1.022e-6 kg m^2, 33 ms -> 8.627e-7; J_r = 1e-5 -> t_c = 382.5 ms and 20.69 ms to shed 10 % of thrust | identity (ODE residual = 0), limits t -> 0 and t -> oo, series to first order, units, quantity | verified | math/mechanist/M-MECH-05.py.log (9 PASS) |
| M-MECH-06 | Stereo depth-noise ceiling (F6) | f = W_px/(2 tan(HFoV/2)) = 337.21 px (640 px, 87 deg); sigma_z = z^2 sigma_d/(f b) by propagation of z = f b/d; sigma_z = 0.1 m at z = 4.106 m (0.1 px) and 5.807 m (0.05 px) with b = 50 mm; 10 cm spans 3 px at 11.24 m | identity (error propagation), limit z -> 0, sqrt(sigma_d) scaling, units, quantity | verified | math/mechanist/M-MECH-06.py.log (8 PASS) |
| M-MECH-07 | Motion blur is rotation-dominated (F7, MECH-B) | f = 446.80 px (848 px, 87 deg); blur_rot = f omega t_exp = 3.899 px/ms at 500 deg/s; blur_trans = f v t_exp/d = 1.787 px/ms at 20 m/s, 5 m; ratio = omega d/v = 2.182; rotation dominates for omega > v/d = 229 deg/s | identity (closed-form ratio), limit d -> 0, units (px dimensionless), quantity | verified | math/mechanist/M-MECH-07.py.log (8 PASS) |
| M-MECH-08 | Aero residual position error (F8, MECH-E) | a_err = 0.365 N/0.75 kg = 0.487 m/s^2; dx = a_err v^2/(2 a_h^2) = 0.675 / 1.377 / 5.509 cm at 7 / 10 / 20 m/s; 2 N gives 30.2 cm at 20 m/s; dx ~ v^2 | identity, limits v -> 0 and a_h -> oo, v^2 scaling, units, quantity | verified | math/mechanist/M-MECH-08.py.log (11 PASS) |
| M-MECH-09 | Burst power, pack sag and the T/W and speed it costs (F9) | momentum theory P = T v_i, v_i = sqrt(T/(2 rho A)), P_elec = P/(FM eta): 1130.2 W at 35 N and 2729.3 W at 63 N (four 5-inch discs, A = 0.0507 m^2) but **1380.8 W at 40 N** (lens 1354 W); 76.4 / 184.4 A at 14.8 V, 42-102 C on 1800 mAh; 90 A x 20 mOhm = 10.7 % of 16.8 V -> T/W 3.508, a_h 32.98 m/s^2; that is d ln a_h = -24.3 %, so at d ln v/d ln a = 0.40 the speed cost is **-9.7 %**, not -4 % | identity (momentum theory), limit T -> 0, T^1.5 scaling, units, quantity | **refuted** (two numbers; the "second-order" conclusion survives) | math/mechanist/M-MECH-09.py.log (13 PASS, 2 FAIL) |
| M-MECH-10 | Latency-vs-braking regime crossover (F11, MECH-C) | v tau = v^2/(2a) has the unique positive root v* = 2 a tau; the ratio (v^2/2a)/(v tau) = v/(2 a tau) is monotone and > 1 above v*; v* = 3.363 / 8.995 / 4.898 m/s for (42.03, 40 ms), (42.03, 107 ms), (16.33, 150 ms) | identity, inequality above v*, limit v -> 0, units, quantity | verified | math/mechanist/M-MECH-10.py.log (8 PASS) |

## Refuted

- **M-MECH-03 (the FoV row, and with it finding 3's ranking headline).** At the operating point
  the lens states (s = 6 m, tau_sense = 107 ms, half-FoV 29 deg, camera mounted 30 deg up), a
  +10 per cent relaxation of the **half-FoV** (29 -> 31.9 deg, i.e. a 58 -> 63.8 deg lens) raises
  the coupled stop bound by **+4.67 per cent**, not +10.5 per cent; the +10.5 per cent corresponds
  to perturbing the *sum* phi = half-FoV + mount tilt by 10 per cent (59 -> 64.9 deg), which my
  re-derivation reproduces at +10.01 per cent. Since the mount tilt is a separate, already-used
  knob, the stated perturbation is the first one. Consequence: at that operating point the range
  elasticity (+5.85 per cent, and +5.75 per cent in the no-motor-lag version) **exceeds** the
  half-FoV elasticity (+4.67 per cent; +4.78 per cent without the lag), ratio 0.80, so the claimed
  ranking "FoV > range" inverts to "range > FoV" and the factor-1.8 separation in [MECH-NULL]
  becomes a factor 1.25 the other way. The FoV *mechanism* of finding 2 is untouched
  (M-MECH-02 verified, including a_u = g tan(phi) and the 7.4 / 11.5 / 17 m/s three-optics
  prediction): what is refuted is the claim that the half-FoV is the largest elasticity, which is
  [MECH-A]'s first stated reason and the quantitative basis of [MECH-NULL]'s "within a factor 1.8"
  and of finding 3's ordering. The rest of finding 3 is verified: range +5.85 (lens +5.7), latency
  +1.23 (+1.2), motor +0.19 (+0.11), thrust +0.00 (+0.00), d ln v/d ln s = +0.598 (+0.58..0.60),
  d ln v/d ln a = +0.402 (+0.40), d ln v/d ln tau = -0.197 (-0.08..-0.20); the level-mount
  d ln v/d ln(half-FoV) is +0.52 at 29 deg (lens +0.55) and +1.38 at 70 deg (lens +1.6, 14 per
  cent high).
- **M-MECH-04 (finding 4's blind-time decomposition).** With the plant's own actuator model (a
  first-order lag on rotor speed, thrust ~ omega^2) the rest-to-rest bang-bang rotation to
  77.5 deg takes **133.9 ms** at motor_tau = 39.1 ms, against 92.4 ms with no lag; a first-order
  lag on the torque itself gives 132.9 ms, and the time rises monotonically with the lag
  (92.4 / 93.4 / 97.8 / 103.7 / 115.3 / 133.9 / 150.0 ms at 0 / 1 / 5 / 10 / 20 / 39.1 / 60 ms),
  recovering 2 sqrt(theta/alpha) as the lag vanishes. So the lens's 95.6 ms is too small by about
  38 ms, and the statement "the motor constant costs 3-9 ms of manoeuvre time while rotational
  inertia costs ~90 ms" is wrong: the two contributions are comparable (92 ms inertia-and-torque
  limited, +42 ms from the lag). The *conclusion* of finding 4 and of [MECH-D] survives my own
  numbers: d ln tau_rot/d ln motor_tau = +0.27 and d ln v/d ln motor_tau = -0.019, and halving the
  motor constant buys +1.04 per cent speed (lens: +1.08 per cent), so actuator bandwidth still has
  the smallest elasticity of the slate. Note the two errors partly cancel in the lens's chain. The
  lens's ideal 91.6 ms is also 0.9 per cent below my 92.40 ms with its own alpha_max = 633.8
  rad/s^2 and theta = 77.50 deg.
- **M-MECH-09 (two numbers in finding 9).** (a) With four 5-inch discs (A = 0.0507 m^2, FM 0.65,
  eta 0.8) momentum theory gives 1380.8 W at 40 N, not 1354 W; 1354 W would require
  A = 0.0527 m^2 (R = 6.5 cm, 5.1-inch props). The 35 N (1130.2 W) and 63 N (2729.3 W) figures,
  the currents (76.4 / 184.4 A) and the 42-102 C range are verified. (b) The speed cost of pack
  sag is mis-chained: the sag takes a_h from 42.03 to 32.98 m/s^2, which is d ln a_h = -24.3 per
  cent, so at d ln v/d ln a = 0.40 the cost is **-9.7 per cent** of speed, not "~4 per cent"
  (the 4 per cent is 0.40 x the 10.7 per cent *voltage* sag, which skips the V^2 -> sqrt(W^2-1)
  amplification the same paragraph derives). The qualitative verdict ("real, mundane,
  second-order", and exactly zero once the FoV caps the tilt) is unaffected, but the number is
  2.4x larger than stated.

## Unverified

- Nothing was left unsettled. Two caveats that are conventions rather than errors, recorded
  because downstream agents may rely on them:
  - **M-MECH-02's coupled bound needs a blind-time convention the analysis states only loosely.**
    With tau_sense = 107 ms alone the bound is 7.52 / 12.36 m/s; adding half the bang-bang
    rotation gives 7.38 / 11.80 m/s, which is what matches the lens's 7.35 / 11.76 m/s (and 7.24 /
    11.27 m/s if the whole rotation counts). My verdict uses the half-rotation reading, as the
    analysis says ("counting half the rotation as latency"); the three numbers differ by up to
    8 per cent, so the quoted "7.35 m/s vs an observed 7 m/s failure onset" coincidence is
    convention-dependent at that level.
  - **M-MECH-05's J_r inference is convention-dependent.** Equating t_c with the quoted 39.1 ms
    gives J_r = 1.02e-6 kg m^2, as the lens says; but t_c is the time at which omega has *halved*,
    not its 1/e time, and if 39.1 ms is the thrust 1/e time then t_c = 60.3 ms and
    J_r = 1.58e-6 kg m^2 (1.6x). J_r is an assumed value either way, as the lens states.

## Formalizable

- M-MECH-01: for a, s > 0 and tau >= 0, v* = a(sqrt(tau^2 + 2s/a) - tau) is the unique positive
  root of v tau + v^2/(2a) = s, and lim_{tau -> 0} v* = sqrt(2 a s).
- M-MECH-01: for W > 1, d ln sqrt(W^2 - 1)/d ln W = W^2/(W^2 - 1) > 1, strictly decreasing in W.
- M-MECH-03: with r = sqrt(tau^2 + 2s/a) and v = a(r - tau), the elasticities are exactly
  d ln v/d ln s = (r + tau)/(2r), d ln v/d ln a = 1 - (r + tau)/(2r) and d ln v/d ln tau = -tau/r;
  hence d ln v/d ln s + d ln v/d ln a = 1 and both lie in (0, 1) for tau > 0.
- M-MECH-03: the composite d ln v/d ln(half-FoV) through a_u = g tan(phi) is strictly increasing
  in phi on (0, pi/2) while the cap is active, with the mount tilt entering only additively in phi
  — so perturbing phi and perturbing the half-FoV differ by the factor (half-FoV + mount)/half-FoV.
- M-MECH-05: omega(t) = omega_0/(1 + t k_m omega_0/J_r) is the unique solution of
  J_r omega' = -k_m omega^2, omega(0) = omega_0, for J_r, k_m, omega_0 > 0, and it is positive and
  strictly decreasing with omega -> 0 as t -> oo.
- M-MECH-06: first-order propagation of z = f b/d gives sigma_z = z^2 sigma_d/(f b) exactly, so
  the range at which sigma_z equals a fixed length scales as sqrt(f b/sigma_d).
- M-MECH-10: for a, tau, v > 0, v^2/(2a) > v tau if and only if v > 2 a tau, and the ratio
  v/(2 a tau) is strictly increasing in v.
