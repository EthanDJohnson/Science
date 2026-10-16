# Analysis: constraints (Kant)
status: final

## Method applied

The question is a controlled mechanical system, so the energy-condition/quantum-inequality list
does not bind; the controlled-system list does. I audit, with numbers: (1) controllability and
underactuation (actuators vs degrees of freedom, Kalman rank, smallest singular value of the
controllability matrix, and whether the equilibria the task needs are holdable at all);
(2) structural obstructions (Brockett, non-minimum-phase zeros, unstable poles, the
unidirectional-thrust cone); (3) the actuator envelope (thrust ceiling, torque ceiling, rotor-speed
lag and slew, power and the thermal/battery limit) at the task's worst instant, not on average;
(4) sensing and timing (delay margin against the real latency budget, including T/2 for the sample
period, plus the blind distance v*tau); (5) energy and thermodynamics; (6) passivity and the region
of attraction. For each I compute what it costs in the brief's metric (mean speed on an unseen
course) and report the elasticity, then say which binds first and in which speed regime.

## Findings

### F1. The static envelope (actuator ceiling), three platforms
T/W 4.10 (Swift-like, 0.87 kg, 35 N) gives a_horiz_max = g sqrt((T/W)^2-1) = 39.0 m/s^2 (3.98 g) at a
75.9 deg tilt; T/W 4.62 (Sun2022 0.75 kg) gives 44.3 m/s^2; T/W 12.35 (0.52 kg mocap platform) gives
120.8 m/s^2 (12.3 g) at 85.4 deg. Hover throttle is 24.4 / 21.6 / 8.1 per cent of the per-rotor maximum.
Consistent with [D-33] and [A-34]. [calc: runs/2026-10-15-quadrotor-agility-limit/calc/lens-constraints_actuator.py]

### F2. Unidirectional thrust makes the envelope asymmetric and caps body torque at constant altitude
Because f_i >= 0, downward acceleration is capped at exactly -g = -9.81 m/s^2 whatever the thrust
installed, against +30.4 m/s^2 up on the Swift-like platform: an up/down asymmetry of 3.10 (11.35 on the
T/W 12.35 platform). More sharply: with two rotors at f_lo and two at f_hi, tau_max(T) = lever *
min(T, 4 f_max - T), so **at hover collective the roll/pitch torque ceiling is exactly lever * m g,
independent of T/W** (0.990 N m, alpha = 396 rad/s^2 for the Swift-like platform; 0.592 N m, 348 rad/s^2
for the T/W 12.35 platform, which is *lower* despite 3x the thrust, because its weight is lower).
`wrench_feasible(T = m g, tau_x)` refuses 1.1 x lever*m g and accepts 1.0 x, confirming the bound
numerically. The global torque maximum lever*T_max/2 (2.03 N m, 812 rad/s^2) sits at half throttle and
requires accepting a ~1 g climb. So installed thrust buys angular agility only at the price of vertical
acceleration: the two are coupled by one inequality. [calc: .../lens-constraints_actuator.py]

### F3. Jerk ceiling from the rotor-speed lag, and the time to build the envelope
With the 39.1 ms thrust time constant [A-03] and f = k_f omega^2, a full-throttle step from hover gives
j_z(0) = (1/m) 4*2 k_f omega_h (omega_max-omega_h)/tau = 514 m/s^3 (52 g/s) on the Swift-like platform
(577 m/s^3 Sun2022, 1262 m/s^3 on the T/W 12.35 platform), and collective thrust reaches 95 per cent of
maximum in 117 ms. At tau = 10 ms the jerk ceiling is 2011 m/s^3. The *rotational* route to changing the
acceleration vector gives |da/dt| ~ a*omega_peak = 860 m/s^3 at a = 39 m/s^2 and 22 rad/s, i.e. the same
order as the collective jerk ceiling, so neither route dominates the other.
[calc: .../lens-constraints_actuator.py]

### F4. The cost of the motor lag, measured two ways: 18 per cent of a slew, 4 per cent of a segment
Rest-to-rest 152 deg thrust-vector reversal (the turn-around between two maximum-acceleration tilts) at
the constant-altitude torque ceiling, full nonlinear plant: 201 ms at tau = 39.1 ms against 164 ms at
tau = 0 (closed form 2 sqrt(theta/alpha) = 163.7 ms, which the simulation reproduces to 0.2 per cent).
So the lag is 18.4 per cent of the slew time and the torque ceiling is the other 82 per cent;
d ln(t_slew)/d ln(tau_motor) = +0.177. On a 10 m rest-to-rest translation with a first-order acceleration
lag the penalty is 40.6 ms on 1012.5 ms = 4.0 per cent, with d ln(t_seg)/d ln(tau_a) = +0.040 and
d ln(t_seg)/d ln(a_max) = -0.481 (the -1/2 of [D-33], recovered numerically). Halving the motor time
constant therefore buys about 2 per cent of segment time; halving it to 10 ms buys 3 per cent.
[calc: .../lens-constraints_actuator.py]

### F5. The reversal, not the latency, is the dominant "lost distance" at speed
At 15 m/s a 152 deg thrust-vector reversal occupies 3.02 m of travel during which the acceleration is
not pointing where the trajectory wants it, against 0.60 m for a 40 ms sensorimotor latency [A-07] - a
factor of 5. At 20 m/s it is 4.02 m against 0.80 m. [calc: .../lens-constraints_actuator.py]

### F6. Underactuation is not an obstruction: rank 12, order-1 sigma_min, no Brockett problem
The 12-state Euler hover linearisation of the 0.87 kg platform has 4 inputs for 6 DOF, equilibrium
residual |f(x0,u0)| = 0 exactly, Kalman rank 12/12 (controllable), min singular value of the
controllability matrix 9.44e-01 raw with drag and 1.149 without, and 1.959 in tolerance-scaled units
(condition 4.9e3). Because the linearisation is controllable, Brockett's necessary condition is
satisfied and a smooth time-invariant stabilising feedback exists; the quadrotor is underactuated but
not nonholonomic in Brockett's sense, and no direction is effort-starved.
[calc: runs/2026-10-15-quadrotor-agility-limit/calc/lens-constraints_loop.py]

### F7. The lateral position loop is minimum-phase: no RHP-zero bandwidth ceiling ([D-28] settled for this model)
Transmission zeros of tau_x -> y in the hover linearisation: none finite with drag off (8 zeros at the
origin from the numerator trim), and with linear rotor drag on, zeros at -0.4828 and -0.2989 rad/s
(both LHP, cancelling the drag poles). RHP zeros 0, RHP poles 0 in both cases. So the right-half-plane
zero bound [D-28] has no purchase on this plant at hover, which the dossier flags as unsourced and open.
Validity: hover linearisation, ZYX chart, linear-rotor-drag aerodynamics, no motor lag in this form.
[calc: .../lens-constraints_loop.py]

### F8. Delay margin against the measured budget: 0.7 Hz single-loop, 4.07 Hz for the cascaded rate loop
LQR on the lateral chain (y, vy, phi, p) <- tau_x with Bryson tolerances and the torque ceiling from F2
traces delay margin against bandwidth: 179 ms at 2.25 rad/s, 76.7 ms at 7.91 rad/s, 46.6 ms at 14.1
rad/s, 15.3 ms at 44.5 rad/s, 0.39 ms at 3961 rad/s. The measured single-loop budget tau_eff = 40 ms
sensorimotor [A-07] + 5 ms (ZOH at 100 Hz)/2 + 39.1 ms motor lag [A-03] = 84.1 ms admits a closed-loop
bandwidth of only 4.40 rad/s (0.70 Hz); the MonoRace-class 57.1 ms admits 7.91 rad/s (1.26 Hz); the 2019
179.1 ms admits 2.25 rad/s (0.36 Hz). Cascaded instead, the rate loop sees only the motor lag and a
~2 ms IMU/ZOH/compute term: L = k/(Jx s)/(1+tau_m s) e^{-theta s} crosses over at 25.6 rad/s (4.07 Hz)
at PM 45 deg with the lag alone, 23.3 rad/s with 2 ms added, 100 rad/s if the lag were 10 ms, with
d ln(wc)/d ln(tau_motor) = -1.000. Two independent routes (the tool's delay-margin bisection and the
closed-form phase condition) agree to 5 digits. [calc: .../lens-constraints_loop.py]

### F9. Whether latency binds depends entirely on the architecture, and by a factor of 22
Feedback-only tracking of a turn gives e = v/wc, so v_max = e_allow * wc: with e_allow = 0.60 m (1.5 m
gate [A-26] half-width minus a 0.15 m vehicle radius) and wc <= (pi/2 - PM)/tau_eff, a 40 ms budget caps
the speed at 11.8 m/s (PM 45 deg) or 7.9 m/s (PM 60 deg), elasticity to tau_eff exactly -1; a 17.5 ms
budget gives 26.9 m/s; the 2019 130 ms gives 3.6 m/s. With differential-flatness feedforward [D-01] the
loop only has to reject the model-error disturbance a_d = 0.40 N / 0.87 kg = 0.46 m/s^2 [A-18], needing
wc >= sqrt(a_d/e_allow) = 0.875 rad/s, which tolerates 897 ms of pure delay at PM 45 deg - a margin of
22.4x over the measured 40 ms. At the measured 40 ms the feedforward residual error is 1.2 mm.
Conclusion: estimation latency is a hard limit only for an architecture that tracks the reference by
feedback alone; for the architecture the field actually flies it is slack by one to two orders of
magnitude, and its real cost is the blind distance v*tau (F5), not the bandwidth. [calc: .../lens-constraints_loop.py]

### F10. The model-error budget closes between 7 and 14 m/s on a 1.5 m gate, and 13-29 m/s if the model error is halved
Power-law fits to the replayed-flight positional RMSE of [A-18] give e_model(v) = 0.0493 v^0.858 m
(blade-element-momentum, log-log R^2 = 0.83) and 0.0439 v^1.173 m (polynomial fit, R^2 = 0.89). With a
0.60 m clearance (1.5 m gate [A-26], 0.15 m vehicle radius) and a T265-class estimator error of 0.151 m,
the model error fills the remaining 0.449 m at v = 13.1 m/s (BEM) or 7.3 m/s (fitted polynomial);
d ln v*/d ln(model error) = -1.17 (BEM) and -0.85 (fit), d ln v*/d ln(clearance) = +1.56 and +1.14.
Halving the model error ([D-08] reports about a 50 per cent force-error cut from a BEM+neural residual)
moves v* from 13.1 to 29.5 m/s (BEM) or 7.3 to 13.1 m/s. CAVEAT: [A-18] is open-loop replay prediction
error, so this is an upper bound on the closed-loop consequence; F9 puts the feedback-rejected residual
at about 1 mm, and the measured closed-loop figure on this platform class is 0.322 m RMSE at up to
16.7 m/s with mocap state [A-06]. The honest reading is that this bound binds a *plan-then-track or
model-based* pipeline, which is exactly where [D-14] measures 0 per cent success under a realistic model.
[calc: runs/2026-10-15-quadrotor-agility-limit/calc/lens-constraints_budget.py]

### F11. The look-ahead bound's effective latency is dominated by reorientation, not by sensing
To brake, the thrust vector must first be tilted: a rest-to-rest 76 deg tilt at the constant-altitude
torque ceiling of F2 takes 2 sqrt(theta/alpha) = 116 ms (90 deg: 126 ms), against a 40 ms sensorimotor
latency [A-07] and a 17 ms image delay [A-28]. Using tau_tot = tau_sense + t_reorient in the stop bound
v tau + v^2/(2a) <= s with a = 39.0 m/s^2: at s = 10 m, v_max falls from 26.4 m/s (sensing only) to
22.5 m/s (with reorientation), and at s = 6 m from 20.1 to 16.4 m/s. The elasticity to tau_tot rises from
-0.056 to -0.212 at s = 10 m, but the elasticity to tau_sense *alone* is only -0.212 x 40/155.7 = -0.054.
Range stays the strongest term: e_s = +0.53 to +0.64. Required look-ahead: 1.10 m at 5 m/s, 2.84 m at
10 m/s, 5.22 m at 15 m/s, 8.24 m at 20 m/s, of which the reaction term is 71, 55, 45 and 38 per cent.
[calc: .../lens-constraints_budget.py]

### F12. Energy is not binding; peak current is near the pack's working range
Momentum theory for four 5-inch rotors (P_ideal = 4 T_r^1.5/sqrt(2 rho A), rho = 1.225 kg/m^3, figure of
merit 0.65-0.75): hover 71 W ideal -> 94-109 W electrical (3.5-4.1 C on a 4S 1800 mAh pack); half
throttle 208 W -> 277-320 W (9.6-12.0 C); full throttle 588 W -> 784-904 W (27-34 C, 53-61 A). A 75 m lap
[A-10] at 15 m/s costs 0.41 Wh of a 26.6 Wh pack, i.e. 1.5 per cent. So the energy store is three orders
of magnitude from binding, while the *current* at full throttle is 30 C - inside a racing pack's rating
but in the regime where sag is large, which is what [D-14] names as a failure cause (battery-voltage
fluctuation), not endurance. This is the expected result for a controlled system: the energy budget does
not bind. [calc: .../lens-constraints_budget.py]

### F13. Cross-check of the torque ceiling against flight data
The peak body rate my constant-altitude bang-bang slew reaches is 1857 deg/s (no lag) and 1396 deg/s
(39.1 ms lag) for the 0.87 kg platform. The only measured rate in the dossier is ">1600 deg/s" attitude
tracking on a 1-DOF event-camera dualcopter [A-23], and the 0.52 kg mocap platform reached 12.58 g
peak [A-12]. So the computed ceiling is the right order and slightly above what has been flown, as a
ceiling should be. [calc: .../lens-constraints_actuator.py]

### F14. What the literature does not contain
Two short `lit_search` queries (INSPIRE and arXiv, then Crossref/general) for measured rotor spin-up
asymmetry, small-signal motor bandwidth, and a measured racing rate-loop bandwidth returned nothing
usable, consistent with the dossier's own gap list ([D-21] "no paper found arguing that actuator
bandwidth is the binding limit"; maximum rotor-speed slew rate "not retrieved"). My F8 rate-loop number
therefore rests on [A-03]'s 39.1 ms, which the dossier records as a first-order fit to a 12 N collective
step - a LARGE-signal number. If the small-signal lag near hover throttle is shorter (as the 2 ms
command authority in [A-28] hints, though that is command authority and not rotor response), the
rate-loop ceiling of 4.07 Hz rises in proportion (elasticity -1), and the actuator-bandwidth candidate
weakens further rather than strengthening.

## Lens-specific outputs

### Constraint table: what binds, by how much, under which assumptions

| # | Constraint | Value on current hardware | Elasticity of speed to it | Assumptions it needs | Status |
|---|---|---|---|---|---|
| C1 | Usable perception range on an unseen course | 6-10 m (depth camera), ~20 m claimed for LiDAR [D-39] | +0.53 (stop) to +1.00 (dodge) | single static obstacle, constant braking, range given | **binds first on unseen courses** |
| C2 | Model (aerodynamic) error against gate clearance | e_model = 0.0493 v^0.858 m (BEM fit of [A-18]) | -0.85 to -1.17 on v* per unit model error | open-loop replay error transfers to the closed loop; 0.60 m clearance | **binds first on known courses, model-based pipelines** |
| C3 | Thrust-to-weight / a_max | T/W 4.10, a_h = 39.0 m/s^2 | +0.48 to +0.53 | point mass, level flight, no rotation time | strained: real but second-order, and a planner margin is left unused [D-36] |
| C4 | Torque ceiling at constant altitude (unidirectional thrust) | tau_max = l_eff m g = 0.990 N m, alpha = 396 rad/s^2, 116-201 ms per reorientation | enters C1 as t_reorient: raises e_tau from -0.056 to -0.212 | f_i >= 0, two-rotor-pair split, rigid body | surviving, and overlooked by the dossier's four candidates |
| C5 | Estimation / sensorimotor latency | 40 ms [A-07]; 17 ms image [A-28] | -1.00 (feedback-only architecture); -0.054 (stop bound, tau_sense alone) | SISO loop, no feedforward vs flatness feedforward | eliminated as first-binding at 40 ms; re-binds above ~130 ms |
| C6 | Motor / rotor bandwidth | tau = 39.1 ms [A-03] (large-signal), 33 ms [A-04] | -0.040 (segment), -0.177 (slew), -1.00 (rate-loop bandwidth) | first-order lag on rotor speed, thrust = k_f omega^2 | eliminated as first-binding |
| C7 | Underactuation / controllability | 4 inputs, 6 DOF, rank 12, sigma_min 1.96 (scaled) | n/a (no obstruction) | hover linearisation | not a constraint here |
| C8 | RHP zeros or poles | none in tau_x -> y, drag on or off | n/a | hover linearisation, linear rotor drag | not a constraint here ([D-28] settled for this model) |
| C9 | Energy and power | lap = 1.5 % of a 26.6 Wh pack; 30 C at full throttle | ~0 for energy | momentum theory, FoM 0.65-0.75 | not binding (energy); peak current is a disturbance source, not a ceiling |

### Binding order at three speeds (unseen course, onboard only)

- **below about 5 m/s:** nothing in the vehicle binds. Required look-ahead is 1.10 m against 6-10 m
  available; model error is 0.19 m (BEM fit) against 0.45 m of budget; the reorientation time is 116 ms
  over a 1.1 m reaction distance. This is consistent with 100 per cent success at 3-5 m/s [A-20].
- **about 7-14 m/s:** C2 closes first (model error reaches the clearance at 13.1 m/s on a BEM model,
  7.3 m/s on a polynomial fit) and C1 begins to bite through the reorientation term (required look-ahead
  2.8-5.2 m, i.e. half of a 6 m depth range, and the perception failure mode of [D-13] at 7 m/s is
  "objects entered the field of view very late"). Both are inside the measured degradation band
  (80 per cent at 7 m/s, 60 per cent at 10 m/s, [A-20]).
- **above about 15 m/s:** C1 binds hard (8.24 m of look-ahead needed at 20 m/s against 6-10 m usable),
  which is why every result above 20 m/s in the dossier is on a *mapped* track [D-11], [A-26]: a map
  converts the look-ahead requirement into a memory lookup and removes C1 entirely. Then C2 and C3
  take over.

### Validity domain of every model I used

| Model | Validity | Is this regime inside it? |
|---|---|---|
| `quadrotor.py` rigid body with first-order rotor-speed lag | rigid airframe, diagonal inertia, k_f constant (static thrust at zero inflow), no rotor gyroscopic torque, no battery sag, no wind; "treat results above about 20 m/s as model-error-limited" (module docstring) | yes below 20 m/s; my slew and segment results are at hover-to-4 g, inside it. The quoted agility speeds of 27-32 m/s [A-26] are outside it, so I do not compute at those speeds |
| ZYX Euler linearisation | abs(pitch) <= 85 deg, hover equilibrium | yes for F6-F9 (hover); NOT for the 75.9 deg sustained tilt, where I used the quaternion plant instead |
| Delay-margin bound wc <= (pi/2 - PM)/tau_eff | LTI SISO, pure transport delay, no saturation | yes for the small-signal loop; NOT during bang-bang saturation, which is a large-signal regime [D-30] |
| Momentum theory P = T^1.5/sqrt(2 rho A) | hover, no forward speed, uniform inflow; FoM absorbs profile and tip losses | approximate: at 15 m/s edgewise the induced power falls and profile power rises, so the hover number is conservative for cruise and right for the worst instant (a maximum-thrust pull-up) |
| Power-law extrapolation of [A-18] | fitted on 1.67-6.92 m/s mean speed | extrapolating to 13-29 m/s is a 2-4x extrapolation and is the weakest step in this analysis; flagged in F10 |
| Energy conditions, quantum inequalities, Ford-Roman bounds | semiclassical gravity | **not applicable**: this is a controlled mechanical system, and those bounds say nothing about it. Stated because the lens's default checklist includes them |

## Calculations

- `runs/2026-10-15-quadrotor-agility-limit/calc/lens-constraints_actuator.py` - static envelope, the
  unidirectional-thrust torque ceiling tau_max(T) = l_eff min(T, 4 f_max - T), the jerk ceiling from the
  rotor lag, the rest-to-rest 152 deg thrust-vector reversal on the full nonlinear plant, and the
  segment-time penalty with elasticities. Verification: integrator angular-momentum drift 7.1e-15,
  rotational-energy drift 9.9e-15, quaternion-norm drift 2.2e-16, free-fall error 2.8e-14, RK4 order
  4.005; no-lag slew 164.0 ms against the closed form 163.7 ms; dt and dt/1.5 agree to 0.17 ms on the
  slew and to 3.3e-5 s on the segment; the tau -> 0 segment time 1.0127 s against 2 sqrt(d/A) = 1.01253 s.
- `.../calc/lens-constraints_loop.py` - underactuation and controllability, transmission zeros, LQR delay
  margins on the lateral chain, the rate-loop bandwidth with the motor lag, and the feedback-only versus
  feedforward speed ceilings. Verification: equilibrium residual exactly 0, linearisation step
  sensitivity 2.6e-13, and the tool's delay-margin bisection reproduces the closed-form phase condition
  (PM 45.0 deg at the predicted crossover) to 5 digits at all seven test points.
- `.../calc/lens-constraints_budget.py` - the model-error budget power-law fit, the look-ahead bound with
  the reorientation time, momentum-theory power and battery C-rate, and the elasticity table.
  Verification: quadrature of the braking distance equals the closed form to 0.00e+00 at n = 1000 and
  1500; v_stop inverted back to s = 10.000000 m; the reorientation closed form 163.7 ms matches the
  independent full-plant simulation's 164.0 ms.

## Candidate answers

- [CONSTRAINTS-A] **On a course it has not seen, the usable perception range binds first** - not any
  actuator, loop or aerodynamic limit. | status: surviving | why: range has the largest elasticity of any
  single limit (+0.53 on the stop bound, +1.00 on the lateral-dodge bound [D-31]), 10-25x the elasticity
  of sensing latency (-0.054 for tau_sense alone) and 13x that of the motor time constant (-0.040); and
  the required look-ahead (2.84 m at 10 m/s, 8.24 m at 20 m/s) crosses a 6-10 m depth-camera range
  exactly in the band where measured success collapses (80 per cent at 7 m/s, 60 per cent at 10 m/s,
  [A-20]) [calc: .../lens-constraints_budget.py] | prediction: give the same airframe and compute a
  longer-range sensor at equal latency (3-D LiDAR or a stereo baseline doubling usable range from 6 to
  12 m) and the 90-per-cent-success speed on unseen clutter should rise by 2^0.53 = 1.44x, i.e. from
  about 5 to about 7.2 m/s, while halving the motor time constant on the same vehicle moves it by
  2^0.040 = 1.03x. Both are one-afternoon experiments on an existing platform | confidence: medium-high
- [CONSTRAINTS-B] **On a known course, the error budget against gate clearance binds first, and
  unmodelled aerodynamics is the term that fills it** | status: surviving | why: e_model(v) =
  0.0493 v^0.858 m fills the 0.449 m left after a 0.151 m estimator error at 13.1 m/s, and halving the
  model error moves that to 29.5 m/s - the only perturbation in this analysis that moves the speed
  ceiling by more than 50 per cent [calc: .../lens-constraints_budget.py]; it also explains [D-14]'s
  0 per cent success for plan-then-track under a realistic model while an RL policy holds 85 per cent |
  prediction: the speed at which a *model-based* onboard pipeline loses 90 per cent success should scale
  as the inverse 0.86-1.17 power of its force-prediction error; a BEM+NN model ([D-08], 50 per cent force
  error cut) should buy 1.8-2.2x the speed of a polynomial drag model on the same airframe and the same
  track, and should buy a learned end-to-end policy much less | confidence: medium
- [CONSTRAINTS-C] **The actuator-side term that matters is the torque ceiling at constant altitude, not
  the motor time constant** - tau_max = l_eff m g, independent of installed thrust, giving 116-201 ms per
  thrust-vector reorientation, 3-5x the sensorimotor latency | status: surviving (and absent from the
  dossier's four candidates) | why: at hover collective, f_i >= 0 caps roll/pitch torque at l_eff m g
  (0.990 N m, 396 rad/s^2), which `wrench_feasible` refuses to exceed; the measured 39.1 ms motor lag adds
  only 18.4 per cent to a 152 deg reversal (201 vs 164 ms) and 4.0 per cent to a 10 m segment, so the
  ceiling, not the bandwidth, owns the time [calc: .../lens-constraints_actuator.py] | prediction: the
  reorientation time should scale as sqrt(Jx/(l_eff m g)), so a vehicle with the same T/W but a 2x longer
  arm should reorient 1.4x faster if its inertia grows no faster than l^1; and a vehicle allowed to climb
  through the turn (collective 2 m g) should reorient sqrt(2) = 1.41x faster than one holding altitude -
  a measurable, free gain that no published controller claims | confidence: medium
- [CONSTRAINTS-D] **Estimation latency does not bind on 2026 hardware** | status: eliminated as the
  first-binding limit (strained, not refuted, as a *conditional*) | why: with differential-flatness
  feedforward [D-01] the loop needs only wc >= sqrt(a_d/e_allow) = 0.875 rad/s, which tolerates 897 ms of
  delay at PM 45 deg - 22.4x the measured 40 ms; the feedforward residual at 40 ms is 1.2 mm against a
  0.60 m clearance [calc: .../lens-constraints_loop.py]. It re-binds in two regimes: a feedback-only
  architecture (v_max = e_allow wc = 11.8 m/s at 40 ms, elasticity -1), and latencies above about 130 ms
  [A-22], where the admissible closed-loop bandwidth falls to 2.25 rad/s | prediction: injecting 40 ms of
  *extra* delay into a flatness- or RL-based onboard pipeline should cost little speed (the 47 per cent
  RMSE rise in [A-06] is confounded with a radio-link change), whereas the same injection into a
  feedback-only controller should cost about 40 per cent of its speed ceiling | confidence: medium
- [CONSTRAINTS-E] **Null: no single limit dominates; three limits sit within a factor of two** |
  status: surviving as the honest reading of the elasticities | why: perception range +0.53, T/W +0.50 and
  model error -0.86 to -1.17 are all within about 2x of each other, while latency (-0.054) and motor
  bandwidth (-0.040) are 10-25x smaller. So the brief's four-way question has a two-way answer (range and
  model error), not a one-way one, and two of its four named candidates are eliminated rather than ranked
  [calc: all three scripts] | prediction: a one-at-a-time sensitivity study on one airframe will find no
  single perturbation that moves the unseen-course 90-per-cent speed by more than about 1.5x, and will
  find two that move it by 1.4-2.2x | confidence: medium-high
- [CONSTRAINTS-F] **Reframe: the metric puts the limit in the task, not the vehicle** | status: surviving |
  why: the same airframes reach 27.8-32.2 m/s on a mapped track [A-26] and 5.3-10 m/s on unseen clutter
  [A-20], [A-29] - a factor of 3-5 that no vehicle-side limit in this table can produce (the largest
  single-limit elasticity, +1.0 on the dodge bound, needs a 3-5x range increase to cover it). A map
  removes C1 by converting look-ahead into memory. And on the brief's own 90-per-cent criterion the
  documented set clears it only at or below 5 m/s [D-24], so the metric is currently unmeasured above
  that speed | prediction: a system that keeps every hardware parameter fixed and only adds a prior map
  should gain the full 3-5x, which would settle the question against every hardware candidate at once |
  confidence: medium-high

## What would change my mind

- A measured small-signal rotor/thrust bandwidth much faster than the large-signal 39.1 ms of [A-03]
  would not change the ranking (it weakens C6 further), but a measured value *slower* than about 80 ms,
  or a measured rotor-speed slew limit that binds before the first-order lag, would raise C6's slew-time
  elasticity from -0.18 towards -0.5 and make it comparable to C3.
- A demonstration that closed-loop tracking error at 15-20 m/s follows the open-loop model error of
  [A-18] rather than being rejected (i.e. measured closed-loop error near 0.4 m rather than near 0.05 m)
  would promote C2 above C1 even on unseen courses.
- A published measurement that usable perception range at racing speed is much shorter than 6 m because
  of motion blur or exposure (the dossier lists these as not retrieved) would strengthen C1 and could
  make it dominate outright rather than tie.
- An onboard-only, unseen-course result at 90 per cent success above 12 m/s with a 6 m sensor range would
  refute C1's numbers directly.
- Any source showing a RHP zero or an unstable pole in the position loop of a symmetric quadrotor at the
  operating points used in racing (my F7 covers hover only) would reopen [D-28] and add a constraint I
  have ruled out.

## Assumptions I relied on

1. The vehicle is the 0.75-0.87 kg Agilicious-class platform of [A-01], [A-09] with the published
   inertia and coefficients; the "Swift-like" variant keeps that geometry and inertia and changes only
   mass and per-rotor thrust, so its Jx is borrowed, not measured, and the reorientation times scale as
   sqrt(Jx).
2. A 0.60 m clearance: a 1.5 m gate opening [A-26] minus a 0.15 m vehicle radius. A tighter gate or a
   bigger airframe moves every speed in F10 and C2 down with elasticity +1.1 to +1.6.
3. The dossier's correlated-apparatus warning: [A-01] to [A-06], [A-07] to [A-10] and [A-16] to [A-21]
   share one research group's platform lineage, so my inputs are not independent replications.
4. [A-18]'s open-loop replay errors are treated as an upper bound on the error a model-based pipeline
   inherits, and the power-law extrapolation beyond 7 m/s is mine, not the source's.
5. The look-ahead bound is the single-static-obstacle, constant-braking form of [D-32], with the braking
   deceleration tied to the platform (a_h = 39.0 m/s^2) rather than left free, and with the reorientation
   time added - both of which are my corrections to the dossier's version, not the source's.
6. Elasticities are local (computed at +-20 per cent or +-0.1 per cent), one limit at a time, in models
   whose validity domains are tabulated above; they are not measured sensitivities on hardware.
