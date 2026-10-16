# Analysis: mechanist (causes and mechanisms)

status: final

## Method applied

For each candidate binding limit I write the causal chain — the physical process that produces the
effect, what it acts on, what sustains it, what ends it — then classify the mechanism by the kind of
phenomenon it relies on and name the governing theory. Every link is cited to the dossier or marked
assumed; the weakest link is the mechanism's test. I own the brief's look-ahead calculation
(required look-ahead distance vs usable perception range, and the crossing speed), and I hunt for
mechanisms the dossier misses, including mundane ones: field-of-view/attitude coupling, stereo
depth noise, rotation-dominated motion blur, rotor spin-down asymmetry and pack sag.

## Findings

1. **The naive look-ahead bound is nowhere near binding at demonstrated speeds.** With braking
   acceleration tied to thrust-to-weight rather than left free (a_h = g sqrt(TWR^2 - 1) = 42.0 m/s^2
   at TWR 4.4, the onboard-only class [D-33] [A-13]), the required look-ahead to stop from 7 m/s is
   **0.93 m** at tau = 50 ms and **1.33 m** at tau = 107 ms
   [calc: runs/2026-10-15-quadrotor-agility-limit/calc/lens-mechanist_lookahead.py]. The stop bound
   at s = 6 m, tau = 107 ms is 18.4 m/s, and the crossing speed where required look-ahead equals the
   stated range is 12.0 m/s at s = 3 m, 18.4 m/s at s = 6 m and 24.9 m/s at s = 10 m — all well above
   the 7 m/s at which onboard unseen-clutter flight already fails 2 of 10 times, and the 10 m/s where
   it falls to 60 per cent [A-20]. **Range plus transport latency alone cannot be the binding
   mechanism at today's speeds**; something inside the perception chain fails long before the
   stopping geometry does.
2. **The mechanism the dossier misses: field-of-view/attitude coupling.** A quadrotor is
   underactuated, so any horizontal acceleration a_x needs tilt theta = atan(a_x/g): 27.0 deg at
   5 m/s^2, 45.5 deg at 10 m/s^2, 63.9 deg at 20 m/s^2, 75.5 deg at 38 m/s^2
   [calc: .../lens-mechanist_lookahead.py]. With a body-fixed camera of half-FoV plus mount tilt phi,
   the direction of travel — and the obstacle being braked for — leaves the image once
   |a_x| > g tan(phi). For a level-mounted D435i depth stream (58 deg vertical FoV) that is
   **5.44 m/s^2 = 0.55 g**, and the coupled stop bound is **7.35 m/s** (s = 6 m, tau_sense = 107 ms)
   — the same speed at which that hardware result began to fail, and the stated reason its authors
   tilted the camera 30 deg up above 7 m/s [A-20]. Re-mounted 30 deg up, phi = 59 deg gives
   a_u = 16.3 m/s^2 and v = 11.8 m/s (vs a measured 60 per cent success at 10 m/s); MonoRace's
   155 deg horizontal lens gives a_u = 44.3 m/s^2, i.e. no FoV limit at all on the horizontal axis
   [A-26] [calc: .../lens-mechanist_blindtime.py]. The coincidence of three independent numbers
   (level-mount bound 7.4 m/s, failure onset 7 m/s, the authors' remedy of tilting the camera) is the
   strongest mechanism-to-observation match I found.
3. **At the real operating point the elasticities rank FoV > range >> latency > actuator > thrust.**
   Per 10 per cent relaxation, one limit at a time, at s = 6 m, tau_sense = 107 ms, camera 30 deg up:
   half-FoV **+10.5 %**, range **+5.7 %**, sensing latency **+1.2 %**, motor time constant
   **+0.11 %**, thrust-to-weight **+0.00 %** (thrust is not what sets the usable acceleration once
   the FoV caps the tilt) [calc: .../lens-mechanist_blindtime.py]. In the no-FoV-limit version of the
   same bound the ranking is range +5.8 %, usable acceleration +3.9 %, latency +2.0 %
   [calc: .../lens-mechanist_lookahead.py]. Elasticities: d ln v/d ln s = +0.58 to +0.60,
   d ln v/d ln a = +0.40, d ln v/d ln tau = -0.08 to -0.20, d ln v/d ln(half-FoV) = +0.55 at 29 deg
   rising to +1.6 at 70 deg.
4. **Actuator bandwidth enters as blind time, not as a bandwidth, and it is small.** The thrust
   vector must be rotated before any braking force exists. With the mix matrix at the per-rotor
   thrust limit (Sun et al. TABLE II through this run's `quadrotor.py`), max pitch torque is
   1.331 N m and alpha_max = 634 rad/s^2; a rest-to-rest bang-bang rotation to the full-brake tilt
   (77.5 deg) takes **91.6 ms with no motor lag and 95.6 ms with the measured 39.1 ms lag** [A-03] —
   so the motor constant costs 3–9 ms of manoeuvre time while **rotational inertia costs ~90 ms**.
   Counting half the rotation as latency, d ln v/d ln tau_rot = -0.09 and
   d ln tau_rot/d ln motor_tau = +0.21, so d ln v/d ln motor_tau ~ -0.02: a 10 per cent faster motor
   buys 0.1–0.2 per cent speed [calc: .../lens-mechanist_blindtime.py]. This is the quantitative
   reason no paper argues actuator bandwidth binds [D-21, dossier section 6].
5. **Why the motor constant is what it is, and what would move it.** For a fixed-pitch unidirectional
   rotor with no active braking, thrust can only fall as the rotor slows against its own drag torque:
   J_r omega' = -k_m omega^2, exactly omega(t) = omega_0/(1 + t/t_c), t_c = J_r/(k_m omega_0). With
   k_m = 2.37e-8 N m s^2/rad^2 and omega_hover = 1103 rad/s, the measured 39.1 ms thrust constant
   corresponds to J_r = 1.0e-6 kg m^2 and the 33 ms rotor-speed constant to 8.6e-7 kg m^2, while a
   1e-5 kg m^2 rotor group would give t_c = 382 ms (20.7 ms to shed 10 per cent of thrust)
   [calc: .../lens-mechanist_blindtime.py]. Spin-down is inertia-limited and asymmetric with spin-up;
   moving it needs lighter/smaller rotors, an actively braking ESC, or more rotors — and by finding 4
   the pay-off is negligible. (This fills the dossier's gap "maximum rotor-speed slew rate ... not
   retrieved" with a mechanism rather than a datasheet; J_r itself is assumed, not sourced.)
6. **The depth-range mechanism has its own ceiling, from stereo geometry, not from the datasheet.**
   sigma_z = z^2 sigma_d/(f b): with b = 50 mm and 640 px over 87 deg (f = 337 px), depth noise
   equals a 0.1 m obstacle's own size at z = 4.1 m (sigma_d = 0.1 px) or 5.8 m (0.05 px), and a 10 cm
   obstacle subtends 3 px only within 11.2 m [calc: .../lens-mechanist_lookahead.py]. So the *usable*
   range for thin unseen obstacles is a few metres whatever the advertised range — which is why range
   is the second-largest elasticity in finding 3, and why a wider-baseline or longer-focal sensor
   (or LiDAR [D-39]) is a real lever.
7. **Motion blur is rotation-dominated, which feeds agility back into estimation error.** At
   f = 447 px (848 px over 87 deg), a 500 deg/s body rate smears 3.9 px per ms of exposure against
   1.8 px for 20 m/s of translation at 5 m — ratio 2.2 at (500 deg/s, 20 m/s, 5 m)
   [calc: .../lens-mechanist_lookahead.py]. The dossier's named failure mode, "loss of tracked visual
   features and severe drift" [D-12], is therefore produced mainly by the angular rate the manoeuvre
   itself demands, not by forward speed. This is the same geometric coupling as finding 2, acting on
   the estimator instead of on obstacle visibility, and it is why the two cannot be fully separated.
8. **Unmodelled aerodynamics is too small to explain the blind phase.** The best model class's
   measured force RMSE is 0.352–0.365 N on a 0.75 kg vehicle [A-18], i.e. 0.48 m/s^2; integrated
   over a full braking manoeuvre that is 0.7 cm of position error from 7 m/s, 1.4 cm from 10 m/s and
   5.4 cm from 20 m/s; even a 2 N error gives 30 cm at 20 m/s
   [calc: .../lens-mechanist_blindtime.py]. Against gate and obstacle clearances of order 0.5 m this
   is a tracking-accuracy mechanism, not a collision mechanism below about 15 m/s — consistent with
   the dossier labelling [D-08] a *model* defect measured in replay, and with [D-14]'s finding that
   its effect is mediated by controller structure, not by force magnitude.
9. **Burst power: real, mundane, second-order.** Momentum theory at the thrust ceiling gives
   P_elec = 1130 W for Swift's 35 N [A-09], 1354 W for 40 N [A-20] and 2729 W for the 63 N mocap
   platform [A-11] — 76, 91 and 184 A at 14.8 V, i.e. 42–102 C on an 1800 mAh pack
   [calc: .../lens-mechanist_blindtime.py]. With an assumed 20 mOhm pack resistance, 90 A sags a 4S
   pack 10.7 per cent, which at thrust ~ V^2 turns TWR 4.40 into 3.51 and a_h from 42.0 into
   33.0 m/s^2. That is the physical content of "large battery-voltage fluctuation" [D-14] — but since
   d ln v/d ln a ~ 0.4 it costs ~4 per cent of speed, not a crash. Pack resistance is assumed; the
   dossier lists pack power limits as not retrieved.
10. **A near-controlled sensitivity exists after all, and it moves the *planner's* perception
    objective, not any hardware number.** A 2026 perception-aware time-optimal planning preprint
    reports closed-loop success rising **from 55 per cent to 100 per cent over 20 closed-loop tests**
    on a Split-S track by adding a perception objective to the same time-optimal problem — with a
    field-of-view objective alone reaching 71 per cent and a position-uncertainty objective 100 per
    cent — and real-world flight to 9.8 m/s with 0.07 m tracking error on a Jetson Orin NX with a
    fisheye camera
    [new: Qin et al., arXiv:2603.04305v1, full-text, "Experiments demonstrate real-world flight
    speeds up to 9.8 m/s with 0.07 m average tracking error, and closed-loop success rates improved
    from 55% to 100% on a challenging Split-S course."; and
    "TABLE VI: Close-loop execution benchmarking. Methods Pos. Uncertainty (m) Track. Error (m)
    Success Rate TOWP-Ours 0.3590 0.4192 55% LA 0.3541 0.4612 67% FOV 0.4634 0.3577 71% PUM 0.2228
    0.3239 100%"]. The success-rate table is simulation (RotorS dynamics, 20 tests); the 9.8 m/s is
    hardware, and whether its state estimate was onboard is not established in what I read. The same
    paper states the field of view is what makes perception non-differentiable in the planner:
    "The camera's limited field of view introduces discontinuities as features abruptly enter or exit
    the image boundaries, rendering the objective function non-differentiable"
    [new: arXiv:2603.04305v1, full-text]. This is the dossier's gap "no controlled sensitivity study
    exists" partly closed, and it closes it on the *coupling* term, not on a component.
11. **Where each candidate's regime begins and ends.** The latency term v*tau equals the braking term
    v^2/(2a) at v = 2 a tau: 3.4 m/s for (a = 42, tau = 40 ms), 9.0 m/s at 107 ms, and 4.9 m/s for
    the FoV-capped a = 16.3 m/s^2 at tau_eff = 150 ms [calc: .../lens-mechanist_lookahead.py,
    .../lens-mechanist_blindtime.py]. So above roughly 5–9 m/s the *perceived volume* (range x solid
    angle), not the loop delay, dominates the look-ahead budget; below it, latency does. Aerodynamics
    crosses into relevance only above about 15 m/s (finding 8); actuator bandwidth never crosses
    within this class (finding 4).

## Lens-specific outputs

### Causal chains, link by link

Each link is cited `[D-..]`, `[calc: ...]`, `[new: ...]` or marked **assumed**.

**Chain 1 — Perception/attitude geometric coupling (FoV).**
(i) The task requires a lateral or braking acceleration a_x on an unseen course [D-13] [A-20].
(ii) Underactuation: thrust lies along body z, so a_x demands tilt atan(a_x/g) — established
rigid-body dynamics [D-01] [calc: lookahead].
(iii) The camera is body-fixed, so the tilt rotates the sensed cone away from the flight direction;
beyond |a_x| = g tan(half-FoV + mount) the obstacle and the future path leave the image
[calc: blindtime] — projective camera geometry, assumed model (no source states this bound).
(iv) Sustained by: every subsequent correction needs more tilt, so the manoeuvre is self-blinding;
the estimator loses the same features (chain 4).
(v) Ended by: wider optics or a second/omnidirectional camera, a gimbal or a tilted mount [A-20]
[A-26], or a sensing modality with no narrow cone (LiDAR [D-39], event cameras of wide FoV [D-37]).
Weakest link: (iii) — a planner can keep the gates/obstacles in view by *yawing* rather than
pitching, trading time for visibility; my bound assumes the shortest-time attitude.

**Chain 2 — Transport latency (sense + compute + ZOH + actuator).**
(i) Measured chain: 35–40 ms command-to-force [A-05], 40 ms sensorimotor latency with a 40 ms U-Net
and 8 ms policy [A-07] [A-08], historically ~130 ms [A-22], 17 ms simulated image delay [A-28].
(ii) Delay caps linear crossover: wc <= (pi/2 - PM)/tau_eff [D-25] [A-32], elasticity exactly -1.
(iii) In the look-ahead budget it enters only additively as v*tau [D-32].
(iv) Sustained by camera exposure + readout + inference; ended by faster sensors (event cameras,
10 us sensor latency [A-24]) or by IMU forward prediction, which already removed 130 ms once [D-35]
[A-22]. Weakest link: (iii) vs (ii) — the bound that latency tightens hard (attitude bandwidth) is
not the quantity the agility metric measures, and the quantity it does enter has elasticity -0.08 to
-0.20 [calc: lookahead, blindtime]. The only hardware latency datum is confounded with a radio link
[A-06].

**Chain 3 — Actuator and rotor bandwidth.**
(i) Commanded rotor speed reaches the rotor through a first-order lag, 33–39 ms [A-03] [A-04].
(ii) Mechanism of the lag: rotor polar inertia against propeller drag torque, J_r omega' = -k_m
omega^2 on spin-down with no active braking [calc: blindtime] — blade-element/momentum theory plus
rigid-body rotation; J_r assumed.
(iii) It acts on the body-torque step, hence on the time to reach the braking attitude: 95.6 vs
91.6 ms with and without the lag [calc: blindtime].
(iv) Ended by: lighter rotors, active braking, more rotors. Weakest link: the whole chain is
dominated by (ii)'s *inertia* term, not by the electrical lag, and the composite elasticity
d ln v/d ln motor_tau ~ -0.02 is the smallest of all candidates. Eliminated.

**Chain 4 — Estimation-side coupling (blur, feature loss, drift).**
(i) Agile manoeuvres demand body rates of hundreds of deg/s (chain 1 (ii)).
(ii) Blur ~ f omega t_exp dominates translational blur by ~2x at racing conditions
[calc: lookahead].
(iii) Blur and FoV loss destroy tracked features -> "severe drift in linear odometry estimates"
[D-12]; competitors in the minimal-sensor regime name exactly this [D-19].
(iv) Sustained because drift in global position has no observable correction (four unobservable
DoF: three translations and yaw [D-06]); ended today only by matching detected gates to a known
track layout [D-11] — which is precisely what the brief's "unseen" clause forbids.
(v) Or ended by shorter exposure (needs light), a global-shutter high-rate camera, event cameras
[D-37], or a planner that keeps features in view [new: arXiv:2603.04305v1].
Weakest link: no measured drift in m per m at racing speed exists [dossier section 6], so the step
from blur to failure is inference, not measurement.

**Chain 5 — Unmodelled aerodynamics.**
(i) Rotor drag, blade flapping and rotor interaction produce forces the model omits [D-08].
(ii) Magnitude: 0.35–0.37 N force RMSE for the best model, 0.8 m -> 0.3 m replay position RMSE
[A-18] [D-08].
(iii) It acts on tracking error during the manoeuvre; integrated over a braking phase it is
0.7–5.4 cm below 20 m/s [calc: blindtime].
(iv) Sustained by speed (error grows with v [A-18]); ended by a learned residual model [D-08], an
INDI inner loop [D-09], or a controller whose objective tolerates it [D-14] [D-15].
Weakest link: (iii) — the measured magnitude is an order of magnitude below the clearances that
matter at the speeds where unseen-course flight actually fails. Strained below 15 m/s.

**Chain 6 — Thrust and power.**
(i) T/W 4.1–4.5 on every onboard-only platform [A-13]; a_h = 42 m/s^2 [D-33].
(ii) Elasticity of speed to a is +0.40 and of a_h to T/W is 1.07 at T/W 4 [D-33] [A-34]; planner
sweeps on hardware give d ln(lap)/d ln(TWR) = -0.565 [A-16].
(iii) Burst power 1.1–2.7 kW and pack sag reduce the delivered T/W by ~10 per cent within a lap
[calc: blindtime] [D-14].
(iv) Ended by a bigger pack (mass penalty) or by the 63 N / T/W 12 class, which exists only with
mocap state [A-11] [A-12]. Weakest link: a planner already leaves a deliberate thrust margin [D-36],
so the hardware ceiling is not the operative one; and once FoV caps the tilt, extra thrust buys
exactly zero [calc: blindtime].

### Mechanism classification (kind of phenomenon; governing theory)

| Chain | Kind of phenomenon | Governing established theory | Verdict |
|---|---|---|---|
| 1 FoV/attitude coupling | **geometry** (underactuation x projective imaging); the engineering analogue of a kinematic constraint | rigid-body dynamics with underactuation [D-01]; pinhole/fisheye projection | surviving, largest elasticity |
| 2 Transport latency | **measurement artefact / loss channel** (delay in the sensing-compute path) | sampled-data LTI control, delay margin [D-25] [D-26] [D-27] | strained |
| 3 Actuator bandwidth | **material property** (rotor polar inertia) + classical rotor aerodynamics | blade-element/momentum theory; Newton-Euler rotation | eliminated |
| 4 Blur, feature loss, drift | **measurement artefact** (detector integration time, normalisation of feature count) | estimation theory, VIO observability [D-06] [D-07] | surviving, co-binding with 1 |
| 5 Unmodelled aerodynamics | **classical field** (flow around rotors and body) | blade-element-momentum plus residual learning [D-08] | strained below ~15 m/s |
| 6 Thrust/power | **material property** (pack chemistry, motor constants) | momentum theory; Thevenin pack model (assumed R_int) | set aside with a number |
| 7 Metric/task | **measurement artefact at the level of the experiment** (what "unseen" and "success" normalise to) | none; definitional [D-11] [D-23] [D-24] | reframe, surviving |

No mechanism in this problem needs a quantum-vacuum, exotic-matter or new-interaction class; the
closest analogue of "new particle" is a new *component class* (event camera, LiDAR, neuromorphic
compute), all of which are frontier and unproven at this scale [D-37] [D-39] [D-42].

### Weakest links and how to test them

| Chain | Weakest link | Test |
|---|---|---|
| 1 | Does the vehicle actually have to point the camera away? A yaw-based plan might not | Same airframe, same policy, three optics (58 deg, 115 deg, 155 deg vertical FoV), unseen clutter, 20 trials each; predicted mean speed at 90 per cent success 7.4 / 11.5 / >17 m/s [calc: blindtime] |
| 2 | Latency's elasticity is small in the look-ahead bound; the hardware datum is confounded with a radio link [A-06] | Inject 0, 20, 40, 80 ms of pure delay into the *estimator* path only, onboard, unseen course; predicted speed change -1.2 per cent per 10 per cent of delay |
| 3 | Rotor inertia J_r is assumed | Spin-down a 5-inch rotor on a bench with ESC braking off and fit omega_0/(1+t/t_c); predicted t_c = J_r/(k_m omega_0) |
| 4 | No measured drift in m per m vs body rate | Log VIO against a ground truth while sweeping commanded body rate at fixed speed; drift should scale with omega t_exp, not with v |
| 5 | Whether 0.35 N matters at the clearance scale | Replay the same unseen course with and without the residual aero model, onboard, 20 trials; predicted success change small below 15 m/s |
| 6 | Pack internal resistance | Measure terminal voltage and current during a lap; predicted a_h loss ~4 per cent per 10 per cent sag |
| 7 | Whether any published result meets the metric | Re-run the best policies on a course the system has never seen, 20+ trials, and publish the trial counts [D-24] |

## Calculations

- `runs/2026-10-15-quadrotor-agility-limit/calc/lens-mechanist_lookahead.py` — required look-ahead vs
  usable range with braking acceleration tied to T/W; crossing speeds (12.0 m/s at s = 3 m, 18.4 at
  6 m, 24.9 at 10 m); stereo depth-noise usable range (4.1–5.8 m for a 10 cm obstacle); FoV/tilt
  geometry (a_x,max = 5.44 m/s^2 level-mounted D435i, 16.3 tilted, 44.3 for a 155 deg lens); motion
  blur in px; blind-phase aero position error; elasticities.
- `runs/2026-10-15-quadrotor-agility-limit/calc/lens-mechanist_blindtime.py` — independent
  verification of both look-ahead bounds by direct integration (stop bound reproduces s to 1e-5 m at
  three operating points; tau -> 0 limit equals sqrt(2 a s); dodge bound reproduces r = 0.5 m
  exactly); blind time from bang-bang reorientation with motor lag (91.6 ms ideal, 95.6 ms with
  39.1 ms lag, lag -> 0 matches 2 sqrt(theta/alpha)); rotor spin-down closed form vs numerical
  integration; burst power and pack sag; the coupled FoV + blind-time bound (7.35 m/s level mount,
  11.76 m/s tilted 30 deg) and its one-at-a-time elasticities (+10.5 % FoV, +5.7 % range, +1.2 %
  latency, +0.11 % motor, +0.00 % thrust). **10 PASS, 0 FAIL.**

Both scripts use SI units (m, s, rad, N, kg, W, A); angles reported in degrees where stated. The
second imports this run's `tools/quadrotor.py` for the mix matrix, hover equilibrium and the
measured platform parameters.

## Candidate answers

- [MECH-A] **The binding mechanism is perception/attitude geometric coupling: the manoeuvre the task
  demands points a body-fixed camera away from what must be seen, so the usable braking or dodging
  acceleration is capped at g tan(half-FoV + mount tilt) — 0.55 g level-mounted, 1.7 g tilted —
  rather than by thrust, latency or actuators.** | status: surviving | why: it is the largest
  elasticity at the measured operating point (+10.5 per cent speed per +10 per cent half-FoV, vs
  +5.7 range, +1.2 latency, +0.11 motor, 0.00 thrust [calc: blindtime]); its bound reproduces the
  observed 7 m/s failure onset and the authors' own remedy of tilting the camera [A-20]; and a
  planner-side FoV objective alone raises closed-loop success from 55 to 71 per cent with hardware
  unchanged [new: arXiv:2603.04305v1] | test: identical airframe and policy, three optics (58, 115,
  155 deg vertical FoV), unseen clutter, 20 trials each — predicted 90-per-cent-success mean speeds
  7.4 / 11.5 / >17 m/s; any lab with an Agilicious-class platform, cost a few lenses and a week |
  confidence: medium
- [MECH-B] **The binding mechanism is estimation-side visual degradation during the manoeuvre
  (rotation-dominated blur and feature loss causing VIO drift), which today is repaired only by prior
  track knowledge — exactly what an unseen course removes.** | status: surviving | why: blur is
  2.2x rotation-dominated at racing conditions [calc: lookahead]; drift is the named failure mode
  [D-12] and the named dominant problem in the minimal-sensor regime [D-19]; global position and yaw
  are unobservable so the error has no self-correction [D-06]; every fast onboard result uses a known
  track to repair it [D-11]; and a position-uncertainty planning objective raises closed-loop success
  to 100 per cent [new: arXiv:2603.04305v1] | test: sweep commanded body rate at fixed forward speed
  and log VIO against ground truth; drift should scale with omega*t_exp rather than with v, and an
  event camera or a 2x shorter exposure should shift the speed at which 90 per cent success fails |
  confidence: medium
- [MECH-C] **Transport latency (sensing plus computation) binds first.** | status: strained | why:
  it tightens the *attitude-loop bandwidth* hard (elasticity exactly -1 [D-25] [A-32]) but enters the
  agility-relevant look-ahead budget only as v*tau, with elasticity -0.08 to -0.20, and the latency
  term is smaller than the braking term above 3.4–9.0 m/s [calc: lookahead]; the one hardware latency
  datum is confounded with a radio link [A-06]; 130 ms was already forward-predicted away in 2019
  [A-22] [D-35] | test: inject pure delay into the estimator path only (0/20/40/80 ms), onboard,
  unseen course, 20 trials; MECH-C predicts a steep speed loss, MECH-A and MECH-B predict ~1 per cent
  per 10 ms | confidence: medium
- [MECH-D] **Rotor and actuator bandwidth binds first.** | status: eliminated | why:
  d ln v/d ln motor_tau ~ -0.02, i.e. a 10 per cent faster motor buys 0.1–0.2 per cent speed; the
  39.1 ms lag adds 4 ms to a 92 ms reorientation whose length is set by rotor inertia and the thrust
  limit, not by the ESC [calc: blindtime]; halving the motor constant moves the stop bound from 19.49
  to 19.70 m/s; and no paper in the dossier argues this limit binds [D-21] | test: fly the same
  platform with 2x and 0.5x effective motor lag (firmware filter) and measure unseen-course speed; a
  change above 2 per cent would resurrect it | confidence: high
- [MECH-E] **Unmodelled aerodynamics binds first.** | status: strained below ~15 m/s, plausible
  above | why: the best model's residual force error, 0.35 N on 0.75 kg, integrates to 0.7–5.4 cm of
  position error across a braking manoeuvre from 7–20 m/s — an order of magnitude below the
  clearances that decide a collision [calc: blindtime] [A-18]; its documented effect is on *model*
  RMSE in replay [D-08] and on plan-then-track controllers' brittleness [D-14], which is a controller
  structure mechanism, not a force magnitude one [D-15] | test: same course, same policy, with and
  without the learned residual model, onboard, 20 trials, at 7 and 15 m/s; MECH-E predicts a large
  gap only at the higher speed | confidence: medium
- [MECH-NULL] **No single limit dominates: the perceived-volume terms (range and solid angle)
  co-bind within a factor of two, and the remaining candidates are 10–100x smaller.** | status:
  surviving in a narrow form | why: at the operating point half-FoV (+10.5 per cent) and range
  (+5.7 per cent) are within a factor 1.8 and act through the same product (range x solid angle =
  perceived volume), while latency, actuator and thrust are 9x, 95x and infinitely smaller
  [calc: blindtime]. The brief's strong null — all four candidates within a factor of two — is
  **eliminated** by those ratios; the narrow null (two perception terms co-bind) is the honest
  reading | test: the two-factor experiment of MECH-A crossed with sensor range (stereo baseline
  50 vs 100 mm, or LiDAR [D-39]); if speed scales with the product and not with either factor alone,
  the null in this narrow form is right | confidence: medium
- [MECH-REFRAME] **The limit is in the task, not the vehicle: for stopping, the required look-ahead
  at 7 m/s is under 1.5 m, so what binds is not how far ahead the vehicle can see but how reliably it
  can detect, estimate and plan inside the small volume it does see — a question about information
  and objective, not about bandwidth.** | status: surviving | why: required look-ahead 0.93–1.33 m at
  7 m/s against a multi-metre sensor [calc: lookahead]; the fastest onboard results are fast because
  the track is known [D-11] [D-20]; the human-pilot gap is attributed to policy and objective rather
  than hardware [D-15] [D-16]; and the only near-controlled sensitivity in the literature changes the
  *objective*, not a component, and moves success 55 -> 100 per cent [new: arXiv:2603.04305v1]. It
  also exposes the metric premise: no published result meets the brief's three-part metric [D-23]
  [D-24] | test: hold all hardware fixed and swap only the planning/learning objective on an unseen
  course with 20+ trials; if objective choice moves the 90-per-cent-success speed more than any
  hardware knob, the reframe stands | confidence: medium

## What would change my mind

- A measurement of VIO drift (m per m) versus body rate and exposure at 7–15 m/s. If drift is small
  while obstacle detections are late, MECH-A strengthens against MECH-B; if drift is large at
  moderate tilt, MECH-B takes precedence.
- An unseen-course result at 90 per cent success above 12 m/s with a *narrow* FoV sensor would refute
  MECH-A's quantitative bound outright (its prediction is 7.4–11.8 m/s for 58–118 deg of total
  vertical FoV).
- A demonstration that yaw-dominated planning keeps obstacles in view at high lateral acceleration
  would remove chain 1's weakest link and demote MECH-A to a planner choice rather than a geometric
  limit.
- Any hardware latency sweep (not confounded with a radio link) showing speed elasticity to delay
  worse than about -0.4 would revive MECH-C.
- A measured rotor-speed slew rate far below what J_r/(k_m omega) implies — for example a current- or
  thermally-limited ESC — would revive MECH-D.

## Assumptions I relied on

1. The look-ahead bounds (stop and lateral dodge) treat a single static obstacle, constant braking
   and no estimation error [D-31] [D-32]; they are upper bounds on speed, so the real binding speed
   is lower than every number here.
2. `a_u = min(a_h, g tan(half-FoV + mount))` is **my model**, not a sourced bound. It assumes a
   body-fixed camera, a plan that uses pitch/roll rather than yaw to redirect thrust, and that an
   obstacle outside the image is unusable. It ignores map memory, which is exactly what partially
   relaxes it in practice (and what an unseen course limits).
3. Rotation time uses bang-bang on a single axis with the full per-rotor thrust limit spent on
   torque, so alpha_max = 634 rad/s^2 is an upper bound; real tau_rot is longer and MECH-D's
   elasticity therefore even smaller in magnitude.
4. Rotor polar inertia J_r, pack internal resistance, propeller figure of merit (0.65), motor+ESC
   efficiency (0.8) and camera intrinsics (b = 50 mm, 87 deg HFoV, 0.05–0.2 px disparity noise,
   1–10 ms exposure) are plausible engineering values, **not retrieved from datasheets** — the
   dossier lists all of them as gaps.
5. Platform parameters come from Sun et al. TABLE II via this run's `quadrotor.py` (0.75 kg,
   J = diag(2.5, 2.1, 4.3) g m^2, 8.5 N per rotor, T/W 4.62), which is one research group's airframe
   lineage; the dossier warns these anchors share an apparatus and are not independent replications.
6. Elasticities are computed one limit at a time in a closed-form bound, not in a verified
   closed-loop simulator; they describe the *bound's* sensitivity, which is an upper bound on the
   metric's sensitivity, not the metric itself.
