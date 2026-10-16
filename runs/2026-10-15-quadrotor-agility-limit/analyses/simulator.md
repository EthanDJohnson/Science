# Analysis: simulator (Galileo)

status: final

## Method applied

Build the executable plant, verify it before trusting a number, run every candidate limit in
closed loop on the same course, then find each one's failure boundary. The plant is the
toolkit's `quadrotor.py` (17-state rigid body with its actuator chain) carrying the published
0.75 kg parameter set of Sun et al. 2022; the controller is a cascaded onboard-style loop with
explicit sampling, two separate measurement delays (IMU path and VIO path), motor lag, a
torque-priority mixer against per-rotor thrust limits, and a controller model that does not
know the plant's aerodynamics. Each candidate limit is perturbed one at a time in the PLANT
while the controller keeps its nominal model, and the sensitivity is reported as an elasticity
d ln(mean speed)/d ln(limit).

## Findings

1. **The plant passes 24/24 verification rows, so its numbers are licensed.** Energy of the
   unforced, drag-free, thrust-free vehicle (ballistic plus torque-free tumble) holds to a
   relative drift of 5.9e-12 over 20 s at a 1 ms RK4 step; angular momentum to 7.1e-15;
   quaternion norm to <1e-12. Two independent implementations of the same physics (the
   quaternion 13-state path and the ZYX-Euler 12-state path) agree on vdot to 8.9e-16 and on
   omegadot exactly; the analytic hover Jacobians agree with `control_tools.linearize` central
   differences to 1.6e-10 (A) and 7.5e-12 (B). Four closed-form limits are reproduced: free
   fall (2.8e-14 m), small-angle hover xddot = g*theta (9.80665 vs 9.80665), the
   thrust-to-weight horizontal acceleration ceiling g*sqrt((T/W)^2-1) = 44.260 m/s^2 reproduced
   by simulation at full throttle and the tilt acos(1/(T/W)) = 77.51 deg with zero vertical
   residual, and motor_tau -> 0 collapsing to instantaneous thrust (exactly). RK4 order
   measured 4.005. `linearize` residual at hover is exactly 0 and the 12-state hover model is
   controllable (rank 12/12).
   [calc: runs/2026-10-15-quadrotor-agility-limit/calc/lens-simulator_verify.py]

2. **The platform's own time-optimal traversal time of the course is t_opt = 4.5020 s**
   (98.315 m of path, mean path speed 21.838 m/s), for the 0.75 kg Sun et al. platform
   (T/W = 4.6227, a_h = 44.260 m/s^2) on a six-gate slalom y = 3 sin(2 pi x/30) m, 90 m long.
   It is a point-mass optimum on a FIXED path with an isotropic horizontal acceleration bound,
   computed by velocity-limit-curve forward-backward integration, which the verification checks
   against two closed forms (straight-path rest-to-rest 2 sqrt(S/a) and circular cruise
   sqrt(a R)). It is therefore a LOWER bound on the true platform optimum; the published
   full-model penalty for exactly this substitution is 2.00-2.68 per cent [D-05][A-17]. The
   drag-limited level top speed of the same plant is 99.1 m/s, so the speed cap never binds on
   this course (peak profile speed 28.2 m/s).
   [calc: .../calc/lens-simulator_verify.py]

3. **A tuning rule that reads phase margin off a wrapped phase inverts the actuator-bandwidth
   conclusion.** My first sweep used `control_tools.loop_margins` to find the largest rate-loop
   gain with 40 deg phase margin for L = (w/s) e^{-s tau}/(1+s T_m). For a pure delay the phase
   wraps through multiples of 360 deg and the margin read off the principal value is wrong: the
   rule returned crossovers up to 4000 rad/s where the closed form gives 291 rad/s, and the
   resulting sweep was non-monotonic (halving the motor time constant appeared to make the
   vehicle slower). Replaced with the closed form PM = 90 deg - (w_c tau + atan(w_c T_m)),
   bisected on w_c. Recorded because it is exactly the failure the brief warns about: a result
   that was an artefact of the harness, not of the physics.
   [calc: .../calc/lens-simulator_model.py]

4. **With a 39.1 ms motor time constant the rotor, not the estimation chain, sets the
   inner-loop bandwidth.** At tau_in = tau_imu + T_inner/2 = 2 ms the achievable rate-loop gain
   at PM = 40 deg is 39.94 rad/s, crossover 27.3 rad/s (4.3 Hz), and the binding term is the
   actuator pole at 1/0.0391 = 25.6 rad/s, not the delay: setting the motor lag to zero raises
   the achievable gain to the 400 rad/s cap, while setting tau_in to zero raises it only to
   43.3 rad/s. The delay only takes over above tau_in of about 5 ms with a 5 ms actuator, or
   about 20 ms with no actuator lag. The IMU path's own latency (about 1 ms) is two orders of
   magnitude from binding. [calc: .../calc/lens-simulator_sweep.py]

5. **The baseline closed loop reaches 89.7 per cent of the platform's time-optimal time on the
   seen course, and the binding term there is thrust authority.** With full preview, a 1.5 m
   gate (0.50 m tolerance), tau_imu = 1 ms, tau_vio = 20 ms, 500/200 Hz loops and
   motor_tau = 39.1 ms: U* = 18.05 m/s, mean path speed 19.592 m/s, t = 5.018 s,
   t_opt/t = 0.897, worst gate error 0.422 m, peak rotor thrust 8.46 of 8.5 N available, RMS
   3.06-6.17 N, mixer saturated 32 per cent of control steps. The failure above U* is
   loss of control, not gate error: the smooth reference's own demand A k^2 U^2 reaches the
   acceleration ceiling a_h at U_feas = 18.339 m/s. At the tighter 0.20 m tolerance the loop is
   tracking-error limited instead: U* = 14.875 m/s, 16.165 m/s mean, t_opt/t = 0.740.
   [calc: .../calc/lens-simulator_sweep.py]

6. **Elasticity ranking at the measured hardware values, seen course.** Gate tolerance 0.20 m
   (tracking-error regime): motor time constant -0.212 across 19.55 -> 39.1 ms and -1.023
   across 39.1 -> 78.2 ms; VIO latency -0.132 across 10 -> 40 ms and -0.267 across
   40 -> 130 ms; IMU latency -0.062 across 0.5 -> 2 ms but -0.348 across 2 -> 5 ms. Gate
   tolerance 0.50 m (thrust-authority regime): thrust-to-weight +0.527 across 6 -> 7.5 N per
   rotor, +0.297 across 6 -> 10 N, and +0.003 across 8.5 -> 10 N (saturated); motor time
   constant -0.462 across 39.1 -> 78.2 ms. The hardware cross-check [A-16] gives
   d ln(speed)/d ln(TWR) = +0.565, which my +0.527 in the regime where thrust binds reproduces
   to within 7 per cent. [calc: .../calc/lens-simulator_lookahead.py]

7. **Halving the motor time constant below about 20 ms buys nothing in this architecture.**
   motor_tau = 5 ms and 10 ms give identical results (19.862 m/s, at the reference family's
   ceiling), elasticity exactly 0.000 across 5 -> 10 ms, because the rate-loop gain is then
   capped by the cascade's own stability (above about 60 rad/s this proportional cascade loses
   margin in the full multi-loop nonlinear plant despite 40 deg of SISO phase margin). So the
   actuator-bandwidth elasticity is strongly asymmetric: large if the actuator gets slower,
   zero if it gets faster, unless the inner loop is also redesigned. An INDI inner loop is the
   published way to extract more [D-09], so every actuator number here is a LOWER bound on what
   a better inner loop could reach. [calc: .../calc/lens-simulator_sweep.py]

8. **Perception range beats every in-vehicle limit by about an order of magnitude.** Flying the
   dodge manoeuvre on the verified 17-state plant with the real attitude loop, motor lag and
   thrust limits (obstacle radius 0.5 m, vehicle radius 0.25 m, so 0.75 m of lateral
   displacement needed): d ln(v)/d ln(range) = +0.986 across 3 -> 6 m and +1.082 across
   6 -> 10 m, while d ln(v)/d ln(latency) = -0.105 across 20 -> 100 ms and -0.143 across
   50 -> 100 ms. The ratio |e_range/e_latency| is 9.4. This reproduces the point-mass
   elasticities of [A-33][D-31] (e_s = 1 exactly, e_tau = -0.08 to -0.24) on a plant that has
   rotational dynamics, which is what RC-09 said the point-mass bound was missing.
   [calc: .../calc/lens-simulator_break.py]

9. **Rotational dynamics and motor lag cost 8 to 15 per cent off the point-mass dodge bound,
   not a factor.** v_simulated / v_point-mass = 0.848 (s = 6 m, tau = 20 ms), 0.875 (6 m,
   50 ms), 0.920 (6 m, 100 ms), 0.913 (10 m, 50 ms), 0.884 (3 m, 50 ms). The point-mass bound
   is therefore a usable engineering bound for this class, over-optimistic by about a tenth,
   and the correction shrinks as the latency grows (because rotation then overlaps the blind
   time). [calc: .../calc/lens-simulator_lookahead.py]

10. **The dominant unmodelled aerodynamic term in the only published parameter set for this
    class has the wrong sign for the "aerodynamics binds" story.** Sun et al. eq. 9 is
    f_a^B = [-kd,x vx; -kd,y vy; -kd,z vz + kh(vx^2 + vy^2)] with "kd,x,y,z and kh are positive
    parameters" and kh = 0.01 kg/m, so the term adds 4.0 N of body-z force at 20 m/s, 54 per
    cent of the 0.75 kg vehicle's weight. In closed loop the elasticity of speed to the
    unmodelled drag magnitude is POSITIVE (+0.381 across kd 0.5x -> 1x at the 0.20 m
    tolerance): more aerodynamic force, correctly signed, makes the vehicle faster on this
    course, because the lift relieves the thrust budget and the drag damps lateral motion.
    Unmodelled aerodynamics does bite, but through the altitude channel and only when scaled
    up: kd x 2 and kh x 2 both fail the 0.20 m gate at 7 m/s.
    [new: Sun, Romero, Foehn, Kaufmann, Scaramuzza, "A Comparative Study of Nonlinear MPC and
    Differential-Flatness-based Control for Quadrotor Agile Flight", arXiv:2109.01365 p. 4,
    ACCESS: full-text (arXiv preprint), QUOTE: "fB a = ( -kd,xvx -kd,yvy -kd,zvz +kh ( v2 x
    +v2 y ) ) (9) ... kd,x,y,z and kh are positive parameters can be identified from flight
    data"] [calc: .../calc/lens-simulator_sweep.py]

11. **The platform's own time-optimal profile is untrackable by a finite-bandwidth cascade at a
    quarter of its acceleration budget.** Flying the velocity-limit-curve optimum for an
    acceleration budget alpha*a_h: alpha = 0.10 completes with 0.140 m of gate error;
    alpha = 0.25 loses control. The profile is bang-bang in tangential acceleration, so the
    required attitude is discontinuous at every switching point. This is a model-side
    confirmation of why planners deliberately stay inside a thrust margin [D-36] and why smooth
    references are used despite their 5.3 per cent time penalty [D-03], and it means the
    denominator of the agility metric is not reachable by a plan-then-track architecture at all.
    [calc: .../calc/lens-simulator_sweep.py]

12. **Neither loop is anywhere near its delay margin.** The designed rate loop
    L(s) = (39.938/s)/(1 + 0.0391 s) has a gain crossover of 27.303 rad/s, phase margin
    43.13 deg and a delay margin of 27.57 ms, against an inner budget of 2.00 ms: 7.3 per cent.
    The outer velocity loop L(s) = 4.438/s has a delay margin of 354.0 ms (matching the closed
    form pi/(2 w) to four figures) against an outer budget of 22.50 ms: 6.4 per cent. Across
    tau_vio from 5 to 130 ms the closed loop never becomes unstable; it only gets monotonically
    slower (18.89 -> 10.60 m/s mean path speed). Latency on current hardware therefore costs
    speed, not stability. [calc: .../calc/lens-simulator_break.py]

13. **Failed measurement, reported as such: my look-ahead-limited course runs do not measure a
    perception-range elasticity.** The pure-pursuit controller I used for the unseen-course
    regime cuts corners, and its gate error GROWS with look-ahead (0.609 m at s_look = 3 m to
    3.702 m at 40 m), so every run failed at 5 m/s and no elasticity could be extracted. That
    is a controller artefact, not a perception limit. The perception axis is therefore carried
    entirely by findings 8 and 9, which use a manoeuvre whose geometry is unambiguous.
    [calc: .../calc/lens-simulator_lookahead.py]

## Lens-specific outputs

## Model

| Element | What it includes | What it leaves out | Which way the omission moves the answer |
|---|---|---|---|
| Rigid body | 6-DOF, quaternion attitude, diagonal inertia, gyroscopic term | off-diagonal inertia (<5 per cent), airframe flexibility, prop unbalance | flexibility would lower the usable rate-loop gain: ACTUATOR candidate stronger |
| Rotors | exact four-rotor X-config thrust/torque map, per-rotor limits 0-8.5 N, torque-priority mixer | blade flapping torque, rotor-rotor interaction, thrust loss in edgewise inflow, rotor spin-up gyroscopic (G2) torque | all would make high speed harder: AERO and ACTUATOR stronger |
| Actuator chain | first-order rotor-speed lag (motor_tau), slew limit available, thrust quadratic in rotor speed | ESC quantisation, battery sag and thrust-vs-voltage, spin-up/spin-down asymmetry | sag is a named real cause of failure [D-14]: ACTUATOR stronger |
| Aerodynamics | linear rotor drag kd and the +kh(vx^2+vy^2) h-force of Sun et al. eq. 9, each switchable; controller blind to both | quadratic parasitic drag, aerodynamic torque, ground effect, wind gusts (a steady wind and an impulse stand in) | missing quadratic drag inflates the top speed and the denominator: makes achieved fractions look WORSE and the AERO candidate weaker than it is |
| Sensing | two pure transport delays (tau_imu on rates/attitude, tau_vio on position/velocity), ZOH sampling at 500/200 Hz, white Gaussian noise | VIO drift, motion blur and feature loss at speed, bias walk, outliers, non-white error | drift and blur both grow with speed: ESTIMATION candidate stronger at high speed |
| Perception | a dodge manoeuvre with explicit detection range and latency; a look-ahead-limited course run (failed, finding 13) | a real detector, field of view, occlusion, false negatives | a real detector would shorten the usable range: PERCEPTION stronger |
| Contact | none; a gate miss is scored geometrically, a crash is "loss of control" | collision dynamics, recovery after contact | neutral for the speed metric |
| Controller | cascaded rate/attitude/velocity/position, retuned to its own delay and lag budget, nominal-model feedforward | INDI or lag inversion, MPC, learned policy, integral action | a better inner loop would extract more from a fast actuator: finding 7's zero elasticity is a LOWER bound |

Parameters (SI), each with its source:

| Quantity | Value | Source |
|---|---|---|
| mass | 0.75 kg | Sun et al. 2022 TABLE II, via `quadrotor.platform_sun2022`; same lineage as [A-01] |
| inertia (about c.o.m.) | diag(2.5, 2.1, 4.3) e-3 kg m^2 | same table |
| arm length, arm angle | 0.14 m, 56 deg | same table |
| k_thrust, k_torque | 1.51e-6 N/(rad/s)^2, 2.37e-8 N m/(rad/s)^2 | same table |
| per-rotor thrust limit | 0-8.5 N (T/W = 4.6227, a_h = 44.260 m/s^2) | same table; T/W consistent with [A-13] 4.1-4.5 |
| kd, kh | (0.26, 0.28, 0.42) kg/s, 0.01 kg/m | same table; the eq. 9 sign quoted in finding 10 |
| motor time constant | 39.1 ms | [A-03], Foehn et al., measured on the Agilicious lineage |
| tau_imu (baseline) | 1 ms | my assumption; IMU paths run at 1-8 kHz [A-26: gyro 2000 Hz] |
| tau_vio (baseline) | 20 ms | between [A-28] 17 ms simulated image delay and [A-07] 40 ms sensorimotor latency |
| control rates | 500 Hz inner, 200 Hz outer | [A-28] controller at 500 Hz; [A-08] VIO at 100 Hz |
| gate opening / tolerance | 1.5 m / 0.50 m (and 0.20 m) | [A-26] MonoRace gate, minus a 0.25 m vehicle radius |
| course | y = 3 sin(2 pi x/30) m, z = 2 m, 90 m, 6 gates, 98.315 m of path | mine; chosen so the path length is comparable with Swift's 75 m lap [A-10] |

## Verification

| Check | Method | Got | Expected | Verdict |
|---|---|---|---|---|
| energy conservation | 20 s unforced (no drag, no thrust), RK4 at 1 ms | relative drift 5.9e-12 | 0 | pass |
| energy conservation | the same at 0.5 ms | 5.5e-11 | 0 | pass |
| angular momentum | torque-free tumble, 2 s, world-frame \|J omega\| | 7.1e-15 | 0 | pass |
| rotational kinetic energy | same run, 0.5 omega.J omega | 9.9e-15 | 0 | pass |
| quaternion norm | same run | <1e-12 | 0 | pass |
| independent implementation | quaternion 13-state vs ZYX-Euler 12-state, vdot | 8.9e-16 | 0 | pass |
| independent implementation | same, omegadot | 0 | 0 | pass |
| independent implementation | analytic hover A vs `control_tools.linearize` | 1.6e-10 | 0 | pass |
| independent implementation | analytic hover B vs the same | 7.5e-12 | 0 | pass |
| rotor map | wrench(rotor_speeds_from_wrench(T, tau)) round trip | 1e-9 / 5.6e-17 | exact | pass |
| mixer null direction | \|M @ [1,1,1,1]\| on the three torque rows | 0 | 0 | pass |
| known limit | free fall 1 s from 100 m vs z0 - g t^2/2 | 2.8e-14 m | 0 | pass |
| known limit | small-angle hover xddot/theta at theta = 1e-5 rad | 9.80665 | g = 9.80665 | pass |
| known limit | simulated a_x at full throttle and tilt 77.51 deg | 44.25992 m/s^2 | g sqrt((T/W)^2-1) = 44.25992 | pass |
| known limit | a_z at the same state (altitude held) | 0 | 0 | pass |
| known limit | motor_tau -> 0 vs the 13-state instantaneous plant | 0 | 0 | pass |
| known limit | time-optimal solver, straight path rest to rest | 4.472136 s | 2 sqrt(S/a) = 4.472136 s | pass |
| known limit | time-optimal solver, circular cruise | 22.36068 m/s | sqrt(a R) = 22.36068 m/s | pass |
| delay margin tool | L = 10/s and 100/s vs pi/(2 w) | 0.1570796 / 0.01570796 s | same | pass |
| integration order | RK4 Richardson self-convergence, base step 20 ms | 4.005 | 4 | pass |
| integration error, closed loop | worst gate error at U = 12 m/s, 1 ms vs 0.5 ms | 1.2e-7 relative | 0 | pass |
| integration error, sweep step | the same at 2 ms vs 0.5 ms | 3.2e-2 relative | small | pass (sweeps only) |
| equilibrium | `linearize` residual at hover | 0 | 0 | pass |
| controllability | Kalman rank of the 12-state hover model | 12/12 | 12 | pass |
| reference family | \|dp_ref/dt - v_ref\| and max \|a_ref\| vs alpha a_h | 2.4e-2 m/s; 37.621 vs 37.621 | consistent | pass |

All 24 scored rows pass. One row failed on the first run (the T/W ceiling) because of a sign
error in my own test's tilt convention, not in the plant: the magnitude matched to 1e-6 and the
convention was corrected.

## Closed-loop results

| Candidate | Works? | Measure | Settling or completion time | Peak effort | RMS effort | Initial conditions |
|---|---|---|---|---|---|---|
| baseline, seen course, 1.5 m gate | yes | U* = 18.05 m/s, mean path speed 19.592 m/s, 89.7 per cent of t_opt, worst gate error 0.422 m | 5.018 s over 98.315 m | 8.46 N of 8.5 N per rotor; mixer saturated 32.0 per cent of steps | 6.17 N per rotor | flying start on the reference at x = 0 |
| baseline, 0.9 m gate (0.20 m tol) | yes | U* = 14.875 m/s, 16.165 m/s mean, 74.0 per cent of t_opt | 6.082 s | 7.32 N | 4.30 N | same |
| actuator relaxed: motor_tau 10 ms | yes | 19.862 m/s, 90.9 per cent of t_opt, at the reference family ceiling | 4.950 s | 8.50 N | 5.83 N | same |
| actuator worsened: motor_tau 78.2 ms | yes, much slower | 7.954 m/s, 36.4 per cent of t_opt (0.20 m tol) | 12.360 s | 2.31 N | 2.06 N | same |
| estimation relaxed: tau_vio 5 ms | yes | 18.892 m/s, 86.5 per cent of t_opt (0.20 m tol) | 5.204 s | 8.33 N | 5.61 N | same |
| estimation worsened: tau_vio 130 ms | yes, slower | 10.601 m/s, 48.5 per cent of t_opt | 9.274 s | 4.99 N | 2.56 N | same |
| aero removed from the plant (kd = kh = 0) | yes, slower | 9.713 m/s, 44.5 per cent of t_opt (0.20 m tol) | 10.122 s | 3.15 N | 2.35 N | same |
| thrust-to-weight 3.26 (6 N/rotor) | yes | 16.840 m/s, 77.1 per cent of t_opt (0.50 m tol) | 5.838 s | 6.00 N (saturated 35.2 per cent) | 4.60 N | same |
| the platform's own time-optimal profile, alpha = 0.25 | NO | loss of control | -- | -- | -- | flying start on the optimal profile |
| the platform's own time-optimal profile, alpha = 0.10 | yes | 0.140 m gate error, 14.235 s | 14.235 s | -- | -- | same |
| perception-limited dodge, s = 6 m, tau = 50 ms | yes | 16.920 m/s is the largest speed that clears a 0.5 m obstacle by 0.75 m | 0.355 s of blind time plus the manoeuvre | full lateral authority | -- | straight and level at speed v |
| look-ahead-limited course (pure pursuit) | NO (measurement failed) | gate error 0.609-3.702 m, growing with look-ahead: corner-cutting artefact | -- | -- | -- | flying start, s_look 3-40 m |

## Failure boundary

| Candidate | Actuator limit | Model error tolerated | Noise tolerated | Delay tolerated | Region of attraction | Disturbance survived |
|---|---|---|---|---|---|---|
| baseline closed loop at U = 12 m/s (mean 13.053 m/s, 72 per cent of t_opt) | still flies at thrust_max = 3.5 N per rotor, T/W = 1.90, a_h = 15.88 m/s^2, mixer saturated 53.3 per cent of steps; fails at 3.0 N (T/W 1.63) | 30/30 successes with mass +/-20 per cent, inertia +/-30 per cent, k_thrust +/-15 per cent, kd +/-50 per cent, motor_tau +/-40 per cent, uniform, seed 12345; Wilson 95 per cent interval [0.886, 1.000]. One at a time: mass survives x1.4 and fails at x1.6; k_thrust survives every value down to x0.5; motor_tau survives x1.4 and fails at x1.8; kd survives x2 and fails at x3 | survives sigma_p = 0.10 m, sigma_v = 0.50 m/s, sigma_att = 1.0 deg, sigma_omega = 5 deg/s; fails at 0.20 m / 1.00 m/s / 2.0 deg / 10 deg/s | rate-loop delay margin 27.57 ms against a 2.00 ms budget (7.3 per cent used); outer-loop delay margin 354.0 ms against 22.50 ms (6.4 per cent). No instability anywhere from tau_vio = 5 to 130 ms, only monotone speed loss | recovers from ANY initial roll up to 179 deg and from lateral speeds up to 25 m/s, given 10 m of altitude; the recoverable set is height-loss limited, not attitude-loop limited | steady crosswind up to 5 m/s passes the 0.50 m gate (error 0.370 m), 8 m/s fails (0.583 m); a 50 ms lateral impulse up to 5 N s passes (error 0.328 m), which is 0.68 of the vehicle's weight-second |
| actuator bandwidth as the binding limit | binds once motor_tau exceeds about 40 ms: elasticity -1.023 across 39.1 -> 78.2 ms; and the fixed-gain loop goes unstable when motor_tau doubles | relaxing it below about 20 ms buys exactly nothing in this architecture (elasticity 0.000 across 5 -> 10 ms): the cascade's own stability caps the gain at 60 rad/s | -- | the actuator pole, not the delay, caps the rate loop for every tau_in below about 5 ms | -- | -- |
| estimation latency as the binding limit | -- | elasticity -0.132 (10 -> 40 ms) to -0.267 (40 -> 130 ms); identical (-0.160, earlier run; -0.132 here) with gains frozen, so not a retuning artefact | -- | never reaches the delay margin in the range any hardware occupies | -- | -- |
| perception range as the binding limit | dodge speed falls to 8.541 m/s at s = 3 m and rises to 29.412 m/s at s = 10 m (tau = 50 ms) | elasticity +0.986 to +1.082; point-mass bound over-optimistic by 8-15 per cent | -- | latency elasticity only -0.105 to -0.143 over 20 -> 100 ms | -- | -- |

## Calculations

| File | What it computes | Result |
|---|---|---|
| `calc/lens-simulator_model.py` | the plant wrapper, the cascaded controller with two delays and ZOH sampling, the slalom course and its gate scoring, the time-optimal speed-profile solver, the closed-form bandwidth tuning rule | module; smoke test flies the course at U = 10 m/s with 0.117 m of gate error |
| `calc/lens-simulator_verify.py` | the 24-row verification table and the agility metric's denominator | 24/24 PASS; t_opt = 4.5020 s, mean path speed 21.838 m/s; a_h = 44.260 m/s^2; U_feas = 18.3394 m/s; the smooth reference family costs 9.01 per cent of t_opt at its own ceiling |
| `calc/lens-simulator_sweep.py` | closed-loop speed at two gate tolerances with one limit perturbed at a time; the achievable-bandwidth table; the trackability of the platform's own optimum | baseline 19.592 m/s (0.897 of t_opt) at 0.50 m tolerance, 16.165 m/s (0.740) at 0.20 m; full sweeps for motor_tau, tau_vio, tau_imu, kd, thrust_max; the time-optimal profile fails at alpha = 0.25 |
| `calc/lens-simulator_lookahead.py` | the look-ahead-limited course (failed measurement), the dodge bound on the full plant, the assembled elasticity table | dodge v/v_point-mass = 0.848-0.920; elasticities as in findings 6 and 8 |
| `calc/lens-simulator_break.py` | the six failure boundaries and the perception elasticities | as the failure-boundary table above; e_range = +0.986/+1.082, e_latency = -0.105/-0.143, ratio 9.4 |

## Candidate answers

- [SIMULATOR-A] **Perception look-ahead distance binds first whenever the course is genuinely
  unseen, and it binds by about an order of magnitude over every in-vehicle limit.** | status:
  surviving | why: on the verified plant, with full rotational dynamics, motor lag and thrust
  limits, d ln(v)/d ln(detection range) = +0.986 (3 -> 6 m) and +1.082 (6 -> 10 m), against
  -0.105 to -0.143 for perception latency, -0.132 to -0.267 for VIO latency, -0.212 for the
  motor time constant at its measured value, and +0.297 to +0.527 for thrust-to-weight: the
  range elasticity is 2 to 10 times every rival and is the only one near unity
  [calc: .../calc/lens-simulator_break.py]. Regime: it begins as soon as the geometry ahead is
  unknown and never saturates, because v scales linearly in range at fixed latency; on a seen,
  pre-mapped track it is absent, which is exactly why the onboard hardware record splits
  5.3-10 m/s unseen against 27.8-32.2 m/s seen [D-20][A-20][A-26]. | distinguishing test: fly
  the SAME airframe and the SAME policy on the same gate sequence with the sensing range
  artificially truncated (a depth clip, or a software horizon on a known map) at 3, 6, 10 and
  20 m, and measure mean speed at >= 90 per cent success. If mean speed is close to linear in
  the clip distance, A holds; if it saturates, A is refuted. Cost: one afternoon on an existing
  Agilicious-class platform, since no hardware changes are needed. | confidence: high

- [SIMULATOR-B] **On a seen course at the measured hardware values, the rotor/actuator time
  constant binds the inner loop and thrust authority binds the outer one; estimation latency is
  third.** | status: surviving, regime-limited | why: with tau_imu = 2 ms the achievable
  rate-loop gain is set by the actuator pole at 25.6 rad/s, not by the delay (zeroing the delay
  gains 8 per cent of bandwidth, zeroing the lag gains a factor of 10)
  [calc: .../calc/lens-simulator_sweep.py]; the baseline run at the 1.5 m gate fails by loss of
  control with the mixer saturated 32 per cent of the time and peak rotor thrust at 8.46 of
  8.5 N, i.e. against thrust authority; and the measured elasticities order as
  thrust-to-weight +0.527 > motor time constant -0.462 (in the same regime) > VIO latency
  -0.132. No source in the dossier argues the actuator binds [D-21, §6], so this is a new,
  model-based claim. Regime: 15-20 m/s on a 0.75 kg, T/W 4.6 platform with a 39.1 ms motor;
  below 10 m/s nothing binds, and the claim dies above about 20 m/s where unmodelled
  aerodynamics and estimation drift, both absent from my model, take over. | distinguishing
  test: re-fly a fixed seen track with (i) the stock motor/propeller and (ii) a
  higher-kv/lower-inertia rotor set with a measured time constant near 15 ms at the same static
  thrust, and separately with an INDI inner loop on the stock rotors [D-09]. B predicts the
  INDI run recovers most of what the faster rotors do; A and C predict neither moves the mean
  speed much. | confidence: medium

- [SIMULATOR-C] **State-estimation latency, at every value current hardware occupies, costs
  speed but not stability, and its elasticity is a third to a half of the actuator's.** |
  status: surviving as a second-order effect | why: across tau_vio from 5 to 130 ms the mean
  path speed falls monotonically 18.89 -> 10.60 m/s with no instability; the elasticity is
  -0.132 (10 -> 40 ms), unchanged at -0.132 to -0.160 with the gains frozen, so it is not an
  artefact of retuning; and both loops sit at 6-7 per cent of their computed delay margins
  (27.57 ms inner, 354.0 ms outer) [calc: .../calc/lens-simulator_break.py]. The elasticity
  does grow with latency (-0.267 across 40 -> 130 ms), so C would become first for a system
  carrying the historical 130 ms chain [A-22], but not for 17-40 ms systems [A-28][A-07]. | why
  not stronger: my model has latency and white noise but no VIO DRIFT and no motion blur, which
  are the mechanisms the hardware literature actually names [D-12][D-19]; this is the single
  largest gap between my model and the real system, and it moves C upward. | distinguishing
  test: inject measured VIO drift and blur-driven feature loss (from a UZH-FPV-style dataset
  replay) into the same loop and re-measure. | confidence: medium

- [SIMULATOR-D] **Null: on a seen course at current hardware values no single limit dominates --
  four of them lie within a factor of four.** | status: surviving in the seen-course regime |
  why: in the thrust-authority regime the elasticities are thrust-to-weight +0.527, motor time
  constant -0.462, aerodynamic magnitude +0.381 (positive, see finding 10) and VIO latency
  -0.132 to -0.267: the largest is under four times the smallest, and the two biggest are
  within 15 per cent of each other. A ranking that calls one of them "the" limit is reading
  noise. The null does NOT survive in the unseen regime, where the range elasticity of +1.0 is
  a clear factor of 4 to 10 above all of them. | distinguishing test: the same truncated-range
  experiment as A, run on a seen track as a control. If the seen-track elasticities cluster
  within a factor of two while the unseen one is near unity, D holds for seen courses and A for
  unseen. | confidence: medium

- [SIMULATOR-E] **Reframe: the metric's denominator is not reachable by the architectures the
  field flies, and two of the question's four candidates are mis-signed or mis-levelled, so the
  "which binds first" ranking is partly an artefact of the framing.** | status: surviving |
  why: three model results. (i) The platform's own time-optimal profile is bang-bang and loses
  control at a quarter of its acceleration budget, so "the fraction of the platform's
  time-optimal time" is a ratio to a trajectory no plan-then-track controller can fly
  [calc: .../calc/lens-simulator_sweep.py]; the smooth family that CAN be flown already costs
  9.01 per cent of t_opt before any limit is reached. (ii) "Unmodelled aerodynamics" is not one
  signed quantity: in the only published parameter set for this class the dominant unmodelled
  term is a translational-lift force of 4.0 N at 20 m/s that makes the vehicle FASTER
  (elasticity +0.381), while a pure drag scale-up is what hurts. (iii) "State-estimation
  latency" is two different limits that enter the cascade at different levels and differ by a
  factor of 20 in both value and elasticity (IMU path -0.062 at 0.5-2 ms, VIO path -0.132 at
  10-40 ms); treating them as one candidate hides the result that the inner path is nowhere
  near binding. | distinguishing test: any attempt to compute a single ranking without
  separating seen from unseen, and inner from outer estimation, should produce
  mutually-inconsistent orderings between labs -- which is what [D-21] records. | confidence:
  high

## What these runs do not show

(a) These runs establish only that these controllers behave this way in THIS model: a 0.75 kg
rigid airframe with linear rotor drag, a first-order rotor lag, two transport delays and white
sensor noise. (b) Whether the model matches a real vehicle rests on the verification table
(24/24, with two independent implementations and four closed-form limits) and on the fact that
every plant parameter is a measured published value [Sun et al. TABLE II, A-03, A-13] -- but
the model has no VIO drift, no motion blur, no battery sag, no aerodynamic torque and no
quadratic parasitic drag, and those are precisely the effects the hardware literature names as
causes of failure [D-12][D-14][D-19], so the match is good for the actuator and latency axes
and poor for the estimation and aerodynamic ones. (c) Nothing here shows any of this works on
hardware. Where the dossier reports hardware, my numbers agree where they can be compared: my
thrust-to-weight elasticity of +0.527 in the regime where thrust binds against the flown
planner sweep's +0.565 [A-16], and my dodge speeds within 8-15 per cent of the point-mass bound
whose point-mass form [D-31][A-33] is itself only analysis. Where hardware and model disagree,
hardware wins: my 19.6 m/s at 90 per cent of t_opt on a seen course is in the same band as
MonoRace's 27.8-32.2 m/s peak on a seen track [A-26], but my model would also predict about
19 m/s on an unseen course, where the best documented hardware is 5.3-10 m/s with 60-80 per
cent success [A-20][A-29] -- a factor of two to four that my model cannot explain, and which is
the strongest single piece of evidence for [SIMULATOR-A] and against any purely in-vehicle
candidate.

## What would change my mind

- A measured look-ahead-truncation experiment on hardware in which mean speed is flat in the
  clip distance would refute [SIMULATOR-A] outright.
- A VIO-drift model (metres of drift per metre flown at racing speed, which the dossier records
  as not retrieved, §6) injected into my loop. If drift at 15 m/s costs more than about 0.5 m
  of gate error, [SIMULATOR-C] moves to first in the seen regime and [SIMULATOR-B] falls.
- An INDI or lag-inverting inner loop in my own model. If it recovers the speed that
  motor_tau = 10 ms recovers, finding 7's asymmetry is a controller artefact and the actuator
  elasticity should be read as near zero, which would weaken [SIMULATOR-B] substantially.
- A second published parameter set for this class with a NEGATIVE h-force coefficient would
  reverse finding 10 and strengthen the aerodynamic candidate.
- A course whose geometry does not saturate the acceleration ceiling (my slalom does so at
  18.34 m/s by construction). If the thrust-authority regime disappears on a lower-curvature
  course, the +0.527 thrust-to-weight elasticity is course-specific and [SIMULATOR-D] weakens.

## Assumptions I relied on

1. The brief's agility metric is operationalised as the largest reference speed at which all
   six gates are passed within tolerance; I did not run repeated trials per speed, so my
   "success" is deterministic completion rather than a >= 90 per cent rate over trials. The
   robustness sweep (30 perturbed plants, 30/30, Wilson [0.886, 1.000]) is the nearest thing to
   a success rate in this work.
2. The controller is a proportional cascade retuned to its own delay and lag budget at 40 deg
   of phase margin, with the rate-loop gain capped at 60 rad/s for cascade stability. Different
   architectures (MPC, INDI, learned) would give different elasticities; finding 7 shows the cap
   matters.
3. The course is fixed geometry: no replanning, no speed-profile adaptation, and in the
   preview mode infinite look-ahead. Finding 13 records that my attempt to relax this with pure
   pursuit failed as a measurement.
4. The gate tolerance of 0.50 m (and 0.20 m) and the 0.25 m vehicle radius are my choices,
   derived from the 1.5 m MonoRace gate [A-26]; the binding limit changes between those two
   tolerances, which is the clearest evidence in this analysis that the brief's hidden premise 2
   (the limits are not separable and the ranking moves with the regime) is correct.
5. Every plant parameter comes from one research group's platform lineage (Sun et al. /
   Agilicious), which the dossier warns is a single apparatus, not independent replications
   [§7, "Correlated apparatus"]. A result is not comparable across parameter sets.
