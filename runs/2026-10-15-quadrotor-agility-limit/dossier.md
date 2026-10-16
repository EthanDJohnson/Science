# Dossier: What limits the agility of an autonomous quadrotor (onboard-only, 0.2–1.5 kg class)
status: final

Units are SI throughout unless a source quotes km/h or g (g = 9.81 m/s^2); conversions are given where a
source used non-SI units. Four facets were researched (theory, quantitative, critiques, engineering) and all
four have check files, so no facet is unchecked. No claims were carried from earlier runs.

**Metric warning that applies to this whole dossier.** The brief's agility metric is (i) mean speed on a course
*not seen before*, (ii) at least 90 per cent success over a stated number of trials, (iii) with the fraction of
the platform's own time-optimal time. No source in this evidence base reports all three. Every speed below is
therefore labelled by what it actually is: seen-course, unseen-course, peak, mocap-state, or simulation.

## 1. Established

- [D-01] A quadrotor subject to linear rotor-drag effects is differentially flat in position and heading;
  feed-forward thrust and body-rate commands follow algebraically from a reference trajectory and its
  derivatives. The proof is for that drag model only and says nothing about actuator limits or delay.
  (refs: RT-01) peer-reviewed, analysis, verified.
- [D-02] For a point mass with bounded acceleration norm ||a|| <= a_max, the rest-to-rest time-optimal control
  is bang-bang (a_max for t_opt/2, then -a_max for t_opt/2). A quadrotor is underactuated (thrust along body z
  only) and must rotate to redirect acceleration, so bang-bang is an approximation to its optimum, not its
  optimum. (refs: RT-02) peer-reviewed, analysis, verified.
- [D-03] Smooth polynomial (minimum-snap-type) trajectories are suboptimal in time because they touch the input
  limit only at isolated points; in the source's rest-to-rest example a 5th-order polynomial is 5.3 per cent
  slower than slope-limited bang-bang. (refs: RT-03) peer-reviewed, the paper's illustrative analysis example
  (not hardware), verified.
- [D-04] Time-optimal quadrotor planning through waypoints with single-rotor thrust constraints is non-convex;
  solutions can be local optima (e.g. an unnecessary flip) unless initialised from a point-mass bang-bang
  guess. The "platform's own optimum" is therefore a numerically computed quantity whose optimality is
  certified only if the initialisation reaches the global basin. (refs: RT-05, RC-13) peer-reviewed,
  simulation, verified.
- [D-05] Which actuator model the planner uses changes the computed platform optimum: earlier planners bounded
  collective thrust and body rates "rather than the actual constraint of limited single rotor thrusts", and the
  full single-rotor-plus-rotation model is 2.00–2.68 per cent slower than those benchmarks. A denominator for
  the agility metric taken from a collective-thrust model is therefore the wrong denominator by a few per cent.
  (refs: RT-04, RC-13, A-17) peer-reviewed, simulation, verified (benchmark range is 3–15 m, see §7).
- [D-06] A visual-inertial system (IMU plus point-feature camera) has exactly four unobservable degrees of
  freedom: three global translations and global yaw. Roll, pitch, 3-D velocity and IMU biases are observable
  given sufficient excitation. Attitude and velocity need no external reference; global position and yaw drift
  unboundedly without loop closure or a map. Observability is existence of information, not accuracy or
  latency, so it does not by itself bound agility. (refs: RT-12) peer-reviewed, analysis, verified.
- [D-07] The four-unobservable-direction result survives full online self-calibration (IMU and camera
  intrinsics, IMU-camera extrinsics including time offset and rolling-shutter readout) under fully excited
  6-axis motion; special motions (planar, constant-acceleration) make calibration parameters unobservable. So
  camera-IMU time offset is estimable, but only under excitation. (refs: RT-13) preprint, analysis, verified
  (headline only re-checked).
- [D-08] Unmodelled aerodynamics is the dominant *model* defect at high speed and in agile manoeuvres: a hybrid
  blade-element-momentum plus neural-residual model reduced positional RMSE of replayed flights from about
  0.8 m (prior art) to below 0.3 m and cut force/torque prediction error by about 50 per cent, on motion-capture
  data up to 65 km/h (18.1 m/s). This is a model-error result measured in simulation against flown data, not a
  speed gain on hardware. (refs: RQ-14, RC-06, A-18) peer-reviewed, verified.
- [D-09] Adding an INDI inner loop plus an aerodynamic drag model reduced position-tracking error by more than
  78 per cent for both NMPC and a differential-flatness controller, at up to 20 m/s and 5 g — under motion
  capture, i.e. evidence about the controller, not about onboard-only autonomy. (refs: RT-18) peer-reviewed,
  hardware (mocap), verified.
- [D-10] Autonomous racing results that reached expert-pilot lap times before 2023 relied on external
  motion-capture state; the first onboard AlphaPilot teams took almost twice as long as a professional pilot.
  (refs: RE-04, RC-02) peer-reviewed, hardware, verified.
- [D-11] The fastest published onboard gate-course results are on *known, pre-mapped* tracks. Swift matches
  detected gates "to the known track layout" to correct VIO drift, and its dynamics and perception residual
  models were fitted on that track; drone-racing competitions supply the gate map beforehand. (refs: RC-01,
  RC-07, RE-01, RE-10) peer-reviewed (Swift, Hanover survey) plus preprint (MonoRace), hardware, verified.
- [D-12] Onboard VIO drifts substantially at racing speed: motion blur "can lead to a loss of tracked visual
  features and severe drift in linear odometry estimates", and successful systems repair this with known-gate
  detections (Swift: Kalman filter on drift state, plus a Gaussian-process drift model fitted to about 50 s of
  real flight). No drift magnitude in m per m was retrieved. (refs: RQ-06, RC-02, RE-03) peer-reviewed,
  hardware; the Swift drift quotes were verified in the critiques and engineering checks and not re-checked in
  the quantitative check.
- [D-13] Along the speed axis the reported binding term changes. In unseen clutter with a depth camera, the
  7 m/s failures are attributed to perception ("objects entered the field of view very late because of the high
  angular velocity of the platform"), while degradation at 10 m/s is attributed to aerodynamics, battery power
  drops and motion blur widening the sim-to-real gap. (refs: RC-08, RE-05, RQ-10) peer-reviewed, hardware,
  verified.
- [D-14] Plan-then-track pipelines fail outright under model error, while a policy optimised on the task
  objective degrades gracefully: with a nominal model, trajectory-tracking MPC gave the fastest lap (4.92 s)
  at 44 per cent success; under a realistic model and in the real world its success fell to 0 per cent, while
  the RL policy held 100 per cent (sim) and 85 per cent (real, mocap state) at 5.35 s. The named causes are
  aerodynamic effects, variable system delay and large battery-voltage fluctuation. (refs: RQ-09, RC-04, RE-08,
  A-14) peer-reviewed; sim rows simulation, real row hardware with Vicon state (so controller evidence, not
  onboard-only). Verified.
- [D-15] The RL-over-optimal-control advantage is attributed by its authors to the objective, not the
  optimiser: "RL does not outperform OC because RL optimizes its objective better. Rather, RL outperforms OC
  because it optimizes a better objective", and "RL cannot find better solutions than OC given the same
  optimization objective". (refs: RT-11, RC-05) peer-reviewed, verified.
- [D-16] The human-pilot gap, on the one head-to-head comparison with identical airframes, is argued to be
  policy and timescale rather than hardware: Swift and the pilots flew drones of "the same weight, shape and
  propulsion"; Swift was globally faster but "not faster on all individual segments", consistently faster at
  the start (about 120 ms earlier take-off) and in tight turns such as the split-S. Swift had lower sensorimotor
  latency (40 ms vs about 220 ms) but a slower camera (30 Hz vs 120 Hz). (refs: RC-03, RE-03, A-07) peer-reviewed,
  hardware, verified.
- [D-17] Learned racing policies generalise poorly: policies "trained on specific environments often crash
  immediately in unseen configurations", and model-based pipelines relying on precomputed references or explicit
  gate-pose estimation are "brittle to spatial perturbations, unmodeled track changes, and sensor noise".
  (refs: RC-15, RC-16) preprints (2026), verified quotes.
- [D-18] Under domain shift in either dynamics or observations, all three of Swift's baselines (two learned, one
  time-optimal MPC) failed to complete even one lap, though all completed laps with idealised dynamics and
  ground-truth observations. Simulation ablation, not a hardware sensitivity. (refs: RQ-07) peer-reviewed,
  simulation; quote not re-checked in the quantitative check (see §7).
- [D-19] In the 2025–26 minimal-sensor competition regime (one monocular camera plus a low-quality IMU, no
  external localisation), competitors name the estimation chain, not thrust, as the dominant engineering
  problem: the sensor limit "makes the system susceptible to drift from Visual-Inertial Odometry". (refs: RE-13,
  RE-12) preprint, hardware (competition); the inference that estimation rather than thrust dominates is the
  researcher's, not the paper's.
- [D-20] Current onboard-only hardware demonstrations sort by what the course is, not by the airframe: seen gate
  track with minimal sensors reaches 27.8–32.2 m/s peak (MonoRace); unseen cluttered environments with a depth
  camera reach 5.3–10 m/s; mocap-state results reach 30 m/s peak at 12.58 g on the same airframe class.
  (refs: RE-22 as corrected, RE-05, RE-07, RE-10, RE-16, RE-17, A-10, A-20, A-26) mixed; this row is a
  tabulation by the engineering researcher, not a source statement, and it inherits the corrections in §7.

## 2. Quantitative anchors

All values as quoted by their source; no uncertainties were combined. "mocap" marks a value measured with
external motion capture in the loop (controller evidence, not onboard-only).

| ID | Quantity | Value (units), as quoted | Conditions; current or preliminary; supersedes | Source refs | Access |
|---|---|---|---|---|---|
| A-01 | Agilicious take-off mass | 750 g | 5.1-inch props, 4S 1800 mAh, Jetson TX2 (154 g, 1.33 TFLOPS); current | RQ-01, RE-09 | full-text |
| A-02 | Agilicious quoted maximum speed / acceleration | 131 km/h = 36.4 m/s; ">5 g" | Platform maximum, not an onboard-VIO or unseen-course speed; current | RQ-01, RE-09 | full-text |
| A-03 | Motor time constant (thrust) | 39.1 ms | First-order fit to load-cell (ATI Mini40) thrust response to a 12 N collective-thrust step; the paper calls it the "actuator bandwidth limitation"; current | RQ-02 | full-text |
| A-04 | Rotor-speed time constant | 33 ms | First-order rotor-speed model, identified on a 752 g airframe; a different quantity from A-03 (rotor speed vs force), not a supersession | RQ-13 | full-text |
| A-05 | Command-to-force-onset latency | 35 ms (agiNuttx onboard FC); 40.15 ms (BetaFlight); >75 ms (offboard over Laird radio) | Same airframe; the >75 ms case changes both latency and link, so it is confounded; current | RQ-02 | full-text |
| A-06 | Tracking RMSE vs added latency (mocap) | 0.322 m (35 ms); <0.385 m (BetaFlight); 0.474 m (offboard, >75 ms); 0.320 m in BEM simulation | Up to 60 km/h (16.7 m/s) and 4 g, 400 Hz Vicon, 36 cameras; +47 per cent RMSE for +40 ms (confounded with the radio link); log-log slope <= 0.51 | RQ-03, RQ-17 | full-text |
| A-07 | Swift sensorimotor latency; camera rates | 40 ms (Swift) vs about 220 ms (expert human pilots); camera 30 Hz (Swift) vs 120 Hz (pilots) | Seen 75 m track, onboard compute; current | RQ-05, RE-03 | full-text |
| A-08 | Swift compute budget | gate-detection U-Net 40 ms per forward pass (Jetson TX2, FP16, 384x384, TensorRT); policy 8 ms per inference on CPU; T265 VIO at 100 Hz; FC an STM32 at 216 MHz | Onboard; current | RQ-05, RE-02 | full-text |
| A-09 | Swift vehicle | 870 g; about 35 N max static thrust; static thrust-to-weight 4.1 (computed 4.10) | T-Motor Velox 2306, 5-inch three-blade, Agilicious-based; current | RQ-05, RQ-17, RE-02 | full-text |
| A-10 | Swift race record | 15 wins of 25 head-to-head races (5/9, 4/7, 6/9); of 10 losses, 40 per cent opponent collision, 40 per cent gate collision, 20 per cent slower | 75 m lap, 7 square gates, 30x30x8 m, three-lap races; humans had one week of practice; seen course; a win rate, not a completion rate, so it does not address the 90 per cent criterion | RE-01, RC-01 | full-text |
| A-11 | High-thrust racing platform (mocap) | 0.52 kg; 63 N max thrust (fully charged); thrust-to-weight 12 (computed 12.35) | Vicon + EKF state, RL policy at 100 Hz; controller evidence only; current | RQ-08, RE-07 | full-text |
| A-12 | Peak speed and acceleration on that platform (mocap) | 108 km/h = 30.0 m/s peak; peak acceleration 12.58 g (paper: ">12 g") | Indoor arena, trained track, mocap state; a peak, not an unseen-course mean; current | RQ-08, RE-07 | full-text |
| A-13 | Thrust-to-weight of the onboard-only platforms | 4.1 (Swift), 4.4 (Loquercio), 4.5 (NeuroBEM/Agilicious-class), about 4 (DJI FPV); 12.35 on the mocap platform | Static, full battery; current | RQ-17, RQ-05, RQ-10, RQ-13 | full-text |
| A-14 | Lap time and success, same track, three controllers | Nominal sim: tracking 4.92 +/- 0.10 s / 44.0 %; contouring 5.03 +/- 0.18 s / 76.0 %; RL 5.14 +/- 0.09 s / 100.0 %. Realistic sim: -- / 0.0 %; 5.34 +/- 0.27 s / 20.0 %; 5.26 +/- 0.32 s / 100.0 %. Real (mocap): -- / 0.0 %; 5.54 +/- 0.21 s / 50.0 %; 5.35 +/- 0.15 s / 85.0 % | s.d. as quoted. Trial counts NOT stated in the retrieved text (25 sim / 20 real were inferred by the researcher and are not supported). Real rows used Vicon + EKF, so not onboard-only; current | RQ-09, RC-04, RE-08 | full-text |
| A-15 | Fraction of the model optimum reached | 4.92 / 5.35 = 0.92 (RL real-world lap vs nominal-model time-optimal tracking lap) | Derived arithmetic across two settings (sim vs mocap hardware), not a measured fraction. The "about 4.9 s" theoretical optimum is read off a dashed line, not a stated number, and the authors state the truly time-optimal value for the physical vehicle is unknown; preliminary | RQ-09, RC-05, RE-08 | derived from full-text |
| A-16 | Lap time vs thrust-to-weight (planner sweep) | TWR 2.5 -> 7.14 s; TWR 3.6 -> 5.81 s; flown at planner TWR 3.15 -> 6.27 s and 3.3 -> 6.10 s | ~0.8 kg drone, platform TWR about 4, mocap track; planner bound deliberately below the platform limit "to maintain controllability under disturbances". Elasticity d ln(lap)/d ln(TWR) = -0.565 [calc: runs/2026-10-15-quadrotor-agility-limit/calc/quantitative_elasticity.py]; current | RQ-15, RE-19 | full-text |
| A-17 | Model-fidelity penalty on the computed optimum | full single-rotor + rotation model 2.00 % and 2.68 % slower than two earlier collective-thrust/body-rate benchmarks; benchmark times 0.89–1.93 s over 3–15 m | Simulation benchmark; current | RT-04 | full-text |
| A-18 | Aerodynamic model error vs speed (positional RMSE, replayed flights) | Lemniscate (mean 1.67, max 3.51 m/s): Fit 0.061, BEM 0.059, BEM+NN 0.049, RotorS 0.114 m. Random points (2.38 / 8.25): 0.167, 0.138, --, 0.239 m. Lemniscate (3.21 / 7.04): 0.183, 0.146, --, 0.148 m. Slanted circle (6.92 / 10.75): Fit 0.381, BEM 0.232 m. Force RMSE 0.352–0.365 N; torque RMSE 4.67–6.53e-3 N m | 752 g quad, mocap data, 96 flights, 1 h 15 min, 1.8 M points, to 65 km/h. Column order inferred from the header. In the 3.21 m/s row RotorS (0.148) is almost equal to BEM (0.146), so RotorS is not worst in every row; current | RQ-14 | full-text |
| A-19 | Onboard perception/planning compute latency | FastPlanner mapping pipeline 65.2 ms per frame on Jetson TX2; the learned end-to-end network 41.6 ms onboard (about 24 Hz) | Measured on the TX2; current | RQ-11, RE-06 | full-text |
| A-20 | Unseen-environment onboard success vs speed (hardware) | 100 % at 3 and 5 m/s; 8 of 10 (80 %) at 7 m/s; 60 % at 10 m/s average speed | 890 g, ~40 N, T/W 4.4; Jetson TX2, D435i depth 30 Hz VGA (~90 deg HFoV, tilted 30 deg above 7 m/s), T265 at 200 Hz; success = reach a goal within 5 m without a crash on a 40 m straight reference line through unseen clutter, NOT a gate sequence; 56 real experiments in total (31 natural + 19 human-made over 3–7 m/s); per-speed trial counts not retrieved. Supplement reports 10 m/s giving 90 % on the low-difficulty and 60 % on the high-difficulty task; current. This supersedes the researcher's "near 100 % at 5–7 m/s" and the claim that 90 % is met at <= 7 m/s (see §7) | RQ-10, RC-08, RE-05 | full-text |
| A-21 | Theoretical maximum speed from sensing range and latency (same paper) | 12.0 / 13.2 / 13.5 m/s for the three methods | Controlled pole experiment: 1.5 m diameter pole at 6 m, quad modelled as a 0.2 m radius sphere; simulation/analysis, extends the point-mass latency bound with rotational dynamics; from the paper's Table S3, retrieved by the source-checker, not by the researcher; current | RQ-11 + quantitative.check note | full-text |
| A-22 | State-estimation latency in a 2019 onboard racing system | "in the order of 130 ms" camera + VIO chain, handled by IMU forward prediction; VIO about 35 Hz, gate detection 60 Hz; planner velocity cap illustrated at +/-7.5 m/s and +/-12 m/s^2 (about 1.2 g) "to limit the motion blur of the camera images" | AlphaPilot 2019, onboard vision, gate map known; the +/-7.5 m/s figure is the paper's illustrative example, not necessarily the race setting; superseded as a state of the art by A-07/A-08 (40 ms sensorimotor latency, same research group lineage) but retained as the historical latency figure | RC-12 | full-text |
| A-23 | Event-camera estimator latency | 12 ms estimator latency at 1 kHz update, attitude tracking >1600 deg/s; 13.8 ms full closed-loop vision-driven delay | 1-DOF roll dualcopter, NOT a quadrotor: evidence by analogy only; current | RQ-12 + quantitative.check note | full-text |
| A-24 | Event-camera sensor latency | about 10 us on the lab bench, sub-millisecond in the real world; 140 dB dynamic range; about 3 kHz DVS pixel bandwidth in bright light | Survey; the 140 dB and 3 kHz figures were not re-checked; current | RQ-16(b) | full-text |
| A-25 | Racing-grade IMU noise (datasheet level) | gyro 2.8 mdps/sqrt(Hz) = 0.0028 deg/s/sqrt(Hz); accelerometer 70 ug/sqrt(Hz) (65 on X,Y; 70 on Z) | ICM-42688-P, datasheet v1.8 (2023-07-27); NOT verified against the datasheet text — search summary only; preliminary | RQ-16(a) | search-summary |
| A-26 | MonoRace (minimal-sensor, seen track) | Fastest completion 16.56 s (two laps); abstract "speeds up to 100 km/h" = 27.8 m/s; the paper's own table lists per-policy maxima up to 32.2 m/s (about 116 km/h) | One monocular rolling-shutter camera (155x115 deg, 820x616 px at 90 Hz, cropped to 384x384) + IMU (accel 1000 Hz, gyro 2000 Hz) on a Jetson Orin NX; 11 square gates (1.5 m opening) in a 100x30 m hall; organiser-supplied identical hardware, external localisation banned; teams practised and trained on the track, so seen-course. arXiv v1 preprint of a Science Robotics paper (doi:10.1126/scirobotics.aee9250) that was NOT opened: numbers preliminary pending the published version | RE-10 | full-text (preprint) |
| A-27 | MonoRace speed-vs-reliability trade | M23 (23 s class): 43 flights, 88.4 % success (38/43), most mishaps development- or hardware-related. M16: 16.56 s mean completion, 1 success of 4 trials = 25.0 %. M17: 5 of 7 = 71.4 %. In simulation (100 randomised rollouts per network, 30 % parameter randomisation) all networks about 90 % | Hardware for M23 per the text; the extracted table places a "Simulation (30% randomization)" label next to these rows, so the setting of the 4- and 7-trial rows is not certain. Preliminary. This supersedes the researcher's statement that no success rate is given for the 16.56 s policy (see §7) | RE-11 + engineering.check note | full-text (preprint) |
| A-28 | MonoRace latency-relevant numbers | Controller at 500 Hz with motor commands changing 0–100 % in 2 ms (command authority, not rotor response); simulated image delay 17 ms and IMU delay 0.5 ms in software-in-the-loop; estimator tolerates about 50 % corrupted frames and IMU saturation | Preliminary (preprint); the authors note the simulator "does not accurately model vision-based state estimation errors that occasionally caused real-world crashes" | RE-12 | full-text (preprint) |
| A-29 | Onboard-only, unseen-obstacle hardware speeds (2026 preprints) | up to 8 m/s real world / 10 m/s hardware-in-the-loop, "100 % success rates in all obstacle-rich environments" (Raspberry Pi + D435i); 5.3 m/s maximum on a compact perturbed-gate track with onboard depth only, vs 10.0 m/s in that paper's own simulation | Trial counts not reported, so the 100 % figure carries little weight; gate order fixed, obstacles randomised; preliminary (preprints, not reproduced) | RE-16, RE-17 | full-text (preprints) |
| A-30 | Event-camera quadrotor flight | 5 m/s avoidance of trees, purely onboard, with success improving as speed increased (1 m/s harder than 5 m/s) | Monocular event camera, static obstacles; no event-camera result above 20 m/s or on a gate sequence found; preliminary (preprint) | RE-20 | full-text (preprint) |
| A-31 | Competition results reported only by press | 2025 A2RL: two laps of a 170 m course in 17 s (about 20 m/s if lap = course length; the ratio is the researcher's arithmetic, not the source's), 14 qualified teams, onboard autonomy required. 2026 A2RL: fastest autonomous lap 12.032 s (TII Racing), 12.832 s (MAVLAB); a human world FPV champion narrowly won a best-of-nine; one monocular camera + IMU, no GPS/LiDAR/external positioning | Press releases and a Wikipedia podium table only; the 2026 track and metric differ from 2025, so the times are not comparable; preliminary, low confidence | RC-17, RE-14 | search-summary |
| A-32 | Delay-limited closed-loop bandwidth (own calculation) | For L = (wc/s) e^{-s tau_eff}: wc <= (pi/2 - PM)/tau_eff, i.e. wc*tau_eff <= 0.785 (PM 45 deg) or 0.524 (PM 60 deg). tau_eff = 5 ms -> wc <= 157 rad/s (25 Hz); 20 ms -> 39 rad/s (6.2 Hz); 40 ms -> 19.6 rad/s (3.1 Hz). A PD loop on a double integrator with its zero at wc/3 has PM 71.6 deg and tolerates 1.249/wc of extra delay (12.5 ms at wc = 100 rad/s). Elasticity of bandwidth to delay is exactly -1 | Generic inputs, not measured; excludes motor lag, RHP dynamics, saturation. Tool delay margin matched the closed form pi/(2 wc) to 5 digits at three test points; re-derived independently in the theory check; current | RT-15 [calc: runs/2026-10-15-quadrotor-agility-limit/calc/theory_delay_lookahead.py] | own calculation |
| A-33 | Stop-before-obstacle speed bound and its elasticities (own calculation) | v*tau + v^2/(2a) <= s, so v_max = a(-tau + sqrt(tau^2 + 2s/a)). At s = 6 m, a = 20 m/s^2, tau = 50 ms: v_max = 14.5 m/s with e_s = +0.53, e_a = +0.47, e_tau = -0.064. At s = 6 m, a = 40 m/s^2, tau = 20 ms: v = 21.1 m/s, e_s = 0.52, e_a = 0.48, e_tau = -0.037. Falanga lateral-dodge bound with r = 0.5 m, same inputs: e_s = 1 exactly, e_tau = -0.14 and -0.08, e_a = 0.43 and 0.46. At s = 10 m, tau = 100 ms, a = 20: stop bound e_tau = -0.10, dodge bound e_tau = -0.24. The latency term v*tau equals the braking term only at v = 2*a*tau (2 m/s for a = 20 m/s^2, tau = 50 ms) | Single static obstacle, constant braking, no estimation error, s given, a a free parameter (no check that the vehicle can brake at a while holding altitude). Verified by direct integration (3 cases, agreement to 0.0005 m) and the tau -> 0 limit sqrt(2as); re-derived in the theory check. Range-vs-latency advantage is a factor of roughly 4 to 14 across these cases (NOT "5 to 15", see §7); current | RT-16 [calc: .../theory_delay_lookahead.py] | own calculation |
| A-34 | Thrust-to-weight acceleration ceiling (own calculation) | a_h = g sqrt((T/W)^2 - 1): 16.99 m/s^2 (T/W 2), 37.99 (4), 77.86 (8). Rest-to-rest 10 m bang-bang: 1.53 / 1.03 / 0.72 s; peak speed 13.0 / 19.5 / 27.9 m/s; mean speed 6.5 / 9.8 / 14.0 m/s. Elasticity of time to a_h = -1/2 exactly; of a_h to T/W = (T/W)^2/((T/W)^2-1) = 1.33 / 1.07 / 1.02. So +10 per cent T/W buys about +5 per cent point-mass speed at T/W >= 4 | Level flight at constant altitude; neglects rotation time, rotor dynamics, drag, body-rate limits, gate geometry; the full-model optimum is a few per cent slower (A-17). Closed form matched by integration to 4 digits; re-derived by hand in the theory check; current | RT-17 [calc: .../theory_delay_lookahead.py] | own calculation |

## 3. Contested or conflicting

- [D-21] **Which limit binds, by paper.** No source ranks all four candidates; each names a different one.
  (a) Aerodynamics is "the dominant model defect during high speeds or agile maneuvers" (RQ-14, RC-06).
  (b) Model mismatch *as mediated by controller structure* — aerodynamics plus variable system delay plus
  battery-voltage fluctuation — is what turns a 4.92 s / 44 per cent plan-then-track controller into
  0 per cent, while leaving an RL policy at 85 per cent (RC-04, RQ-09).
  (c) "The limiting factor for autonomous agile flight in arbitrary unknown environments is the coupling of
  fast and robust perception with effective planning" (RC-09, RE-06).
  (d) Estimation: VIO drift at speed, repaired only by prior track knowledge (RC-02, RC-07, RE-13, RE-12).
  (e) The objective/policy, not any hardware limit (RT-11, RC-05, RC-03).
  No source argues actuator (motor/rotor) bandwidth is the binding limit; the critiques researcher searched for
  one and found none (see §6). These are not strictly contradictory — they are claims about different speed
  regimes and different pipeline architectures — but they are not reconcilable into a single ranking from this
  evidence base.
- [D-22] **Whether the human-pilot gap still exists, and in which direction.** The 2021 time-optimal paper
  states expert pilots fly "at speeds so far unreached by any autonomous system" (RC-13), while its own
  mocap flight outperformed the best human expert on that track (RC-13, RE-19); Swift won 15 of 25 races
  against three champions on a seen track with onboard sensing (RE-01); MonoRace beat three world champions in
  a knockout (RE-10); and at the 2026 A2RL a human champion narrowly beat the fastest AI team (RE-14, press
  only). The gap's existence is therefore track- and format-dependent, not settled.
- [D-23] **Whether "unseen" results are unseen.** The TU Delft group's critique says champion-level systems
  depend on "accurately mapped track layouts, rectangular gates of known size, precise camera calibration, and
  hand-tuned" EKFs — and their own alternative is likewise defined on "a pre-mapped track" (RC-10). The
  unseen-environment results (A-20, A-29) are on obstacle fields, not gate sequences. So neither family
  satisfies the brief's metric, and the two sides of the field do not agree on what "generalisation" names.
- [D-24] **Does a high success rate at a given speed exist on hardware at all?** The 100 per cent claims at
  8 m/s and in "all obstacle-rich environments" (A-29) come with no trial counts; the best-documented onboard
  unseen-course numbers are 80 per cent at 7 m/s and 60 per cent at 10 m/s (A-20); the fastest seen-course
  policy ran 1 of 4 (A-27). The brief's 90 per cent threshold is met in the documented sets only at or below
  5 m/s on an unseen obstacle course (A-20).

## 4. Constraints: theorems, bounds and no-go results

- [D-25] **Delay-limited bandwidth.** For an integrator-like loop with effective delay tau_eff, phase margin
  PM = pi/2 - wc*tau_eff, so wc <= (pi/2 - PM)/tau_eff. Assumptions: single-input single-output, loop gain
  wc/s, pure transport delay, linear small-signal operation; no saturation, no RHP dynamics, no actuator lag.
  Domain: the quantity bounded is the linear crossover frequency, not the achievable speed; the mapping to speed
  is not part of the bound. (refs: A-32, RT-15)
- [D-26] **Effective delay is a sum.** tau_eff = tau_sense + tau_compute + T/2 (zero-order hold adds about half
  a sample period) + actuator lag. Assumption: sampled-data linear loop with ZOH. Source caveat: the cited
  slides support only the qualitative statement that half-sample phase loss can destabilise a loop; the T/2
  result is standard sampled-data theory and is not quoted from a primary source here. (refs: RT-14)
- [D-27] **Delay is not removable by sensor or actuator placement.** Non-minimum-phase dynamics (time delays,
  RHP poles and zeros) "impose severe limits", and delays "cannot generally be avoided by choice of sensor or
  actuator location" — they must be designed out of the computing and communications architecture. Domain: LTI
  feedback systems. (refs: RT-07) textbook.
- [D-28] **Right-half-plane zero bound.** A RHP zero at s = z caps the gain crossover at
  wc <= z tan(phi_ap/2); with an admissible all-pass phase lag of pi/3, wc < 0.6 z. Assumptions: LTI,
  admissible all-pass phase lag chosen by the designer. **Domain caveat: applicability to a quadrotor is not
  established.** The theory researcher's note that the flat-output position of a symmetric quadrotor is
  minimum-phase to first order is explicitly their own reading, not a sourced statement, and the check confirms
  it is unsourced. (refs: RT-08)
- [D-29] **Bode's integral / waterbed.** Sensitivity cannot be made small over a wide band: the area of
  log|S| above zero equals the area below, plus a term from open-loop RHP poles that makes the trade worse.
  Consequence drawn (standard, but an inference not a quote): forcing a lower crossover with added delay raises
  the sensitivity peak elsewhere, so rejecting unmodelled aerodynamics as a disturbance and limiting noise
  amplification cannot both be improved freely. Assumptions: LTI, stable loop, the usual integrability
  conditions. (refs: RT-09) textbook.
- [D-30] **Large-signal limits are a separate (nonlinear) class.** Limited actuator rate and power, and
  constraints imposed to protect the process, are listed as fundamental limits distinct from linear bandwidth
  limits. (refs: RT-10) textbook.
- [D-31] **Perception-latency speed bound (lateral dodge).** For a second-order system with bounded lateral
  acceleration u2_max, flying at constant forward speed toward an obstacle of radius r first sensed at range s
  with total perception latency tau: v_max = s / (tau + 2 sqrt(r/u2_max)), equivalently
  tau_max = s/v - 2 sqrt(r/u2_max). Where the right side is negative, no latency suffices at that speed.
  Assumptions and domain: lateral dodge at constant longitudinal speed (the vehicle may not slow), a single
  static obstacle, no estimation error, point-mass model — explicitly criticised for neglecting the platform's
  rotational dynamics (RC-09). Not a stop-before-obstacle bound and not validated on an unseen multi-gate
  course. The symbol layout was reconstructed from garbled PDF extraction and the dimensions check out; the
  checker confirmed Eq. 8 rearranges to the claimed form. (refs: RT-06, RC-09)
- [D-32] **Stop-before-obstacle bound.** v*tau + v^2/(2a) <= s gives v_max = a(-tau + sqrt(tau^2 + 2s/a)).
  Same assumptions as D-31 minus the constant-speed restriction, plus: constant braking deceleration a, which
  is a free parameter not tied to the thrust available while holding altitude. (refs: A-33)
- [D-33] **Thrust-to-weight acceleration ceiling.** At constant altitude, a_h = g sqrt((T/W)^2 - 1); the
  elasticity of a_h to T/W falls to about 1.07 at T/W = 4, and that of traversal time to a_h is exactly -1/2,
  so a 10 per cent thrust-to-weight gain buys about 5 per cent speed on a short rest-to-rest segment at
  T/W >= 4. Assumptions: point mass, level flight, no drag, no rotation time, no body-rate limit. Empirical
  cross-check from a planner sweep on a real track: d ln(lap)/d ln(TWR) = -0.565 (A-16), i.e. the same order.
  (refs: A-34, A-16, RT-17, RQ-15)
- [D-34] **Observability, not accuracy.** D-06 and D-07 bound what *can* be estimated, not how well or how
  fast; they therefore place no bound on agility by themselves. Assumptions: point features, known or
  self-calibrated IMU-camera parameters, sufficient 6-axis excitation. (refs: RT-12, RT-13)
- [D-35] **Delay can be partly predicted away, at a price.** A pure measurement delay can be compensated by a
  model-based predictor (Smith predictor), but only to the accuracy of the model of the delayed plant and for
  stable or separately stabilised dynamics. The inference drawn — that estimator-side delay can be forward-
  predicted with IMU-driven dynamics so that the binding quantity becomes the unmodelled-disturbance error
  accumulated over the delay — is the theory researcher's, not the textbook's. Note that a 2019 onboard racing
  system did exactly this for about 130 ms of latency (A-22). (refs: RT-20, RC-12) textbook plus inference.
- [D-36] **A planner-side margin is deliberately left below the thrust limit.** The time-optimal planner
  generated trajectories "at a slightly lower thrust bound than what the platform can deliver, to maintain
  controllability under disturbances" — so even the optimum-seeking result runs inside a thrust margin, and the
  published platform optimum is not at the hardware ceiling. (refs: RE-19, RQ-15) peer-reviewed, verified.

## 5. Frontier and speculative (labelled; not established)

- [D-37] **Event-camera sensing as a latency escape.** Sensor latency about 10 us on the bench and sub-ms in
  the real world (A-24); a 12 ms, 1 kHz estimator tracking >1600 deg/s on a **1-DOF dualcopter**, not a
  quadrotor (A-23); onboard quadrotor tree avoidance at 5 m/s with success improving as speed rose (A-30). No
  event-camera result at racing speed or on a gate sequence exists in this evidence base. Frontier.
- [D-38] **End-to-end learned pixel-to-command policies.** A model-based RL policy was validated
  hardware-in-the-loop only (simulator-rendered images, real drone dynamics); "additional challenges remain to
  transfer to real camera pixel observations", and training took about 240 h. Perception sim-to-real, not
  dynamics transfer, was the unresolved term. (refs: RC-11) peer-reviewed (ICRA 2026), partial result.
- [D-39] **LiDAR for high speed in unknown space.** A 2025 system is reported by secondary press to exceed
  20 m/s in unknown environments with 3-D LiDAR; the published abstract frames the problem as vehicle weight,
  size and sensing. Mass class, speed and trial counts are unverified and full text was unreachable; there is
  also a published erratum (doi:10.1126/scirobotics.adx3476) whose content is unknown. (refs: RE-21)
  low confidence, abstract plus press only.
- [D-40] **Generalisation to unseen clutter in simulation only.** A search-summary lead reports domain
  randomisation over track and obstacle configurations producing policies flying unseen cluttered *simulated*
  environments at up to 70 km/h (19.4 m/s), against 5–8 m/s on unseen-course hardware. Treat as a lead, not a
  measurement. (refs: RE-18) search-summary.
- [D-41] **Scheduled decisive experiments.** An identical-hardware autonomous racing series (all teams on the
  same airframe, human pilots banned) had a physical qualifier in September 2026 and a final planned for
  November 2026 (about a month after this run's date), with a reported USD 500k prize pool; whether onboard
  compute is mandated was not established. (refs: RE-15) page could not be re-opened by the checker;
  preliminary.
- [D-42] **Neuromorphic or ASIC onboard compute** on a >= 200 g agile quadrotor: none found. Named as future
  directions only (Navion, Movidius, PULP). (refs: engineering Gaps) absence of evidence.

## 6. Unknowns and gaps

Measurement gaps that bear directly on the question:

- No controlled sensitivity study exists that relaxes each candidate limit (actuator bandwidth, estimation
  latency, aerodynamic error, perception range) one at a time on a racing-class quadrotor. The brief's
  elasticities must be computed by the lenses; the only published near-equivalents are A-16 (thrust-to-weight
  sweep), A-06 (one confounded latency step) and A-21 (latency/range bound in simulation).
- No theorem ranks delay, actuator bandwidth, aerodynamics and look-ahead against each other; all proved results
  here bound one limit at a time (D-25 to D-34).
- **No paper found arguing that actuator (motor/rotor) bandwidth is the binding limit.** The only actuator-side
  evidence is indirect: the single-rotor thrust constraint (D-05), variable system delay (D-14) and the 39.1 ms
  motor time constant sitting at the same order as the whole command latency (A-03, A-05).
- Maximum rotor-speed slew rate (rad/s^2) for 5-inch racing motors, and its spin-up/spin-down asymmetry under
  no active braking: not retrieved. Only first-order time constants were (A-03, A-04).
- Gyro bias stability; measured IMU-to-actuator delay in flight; ESC/DShot update rates: not retrieved.
- End-to-end VIO latency (exposure to pose) and drift in m per m at racing speed: not retrieved. The best
  available are "substantial drift" with no magnitude (D-12) and low-speed RMSEs (see §7's RQ-04 correction).
- Rotor-drag coefficients (dx, dy), blade-flapping and rotor-interaction coefficients with their speeds: not
  retrieved; the only aerodynamic magnitudes here are A-18.
- Motion-blur and exposure numbers for onboard cameras at racing speed: not retrieved.
- Battery specific energy and discharge-power limits for 4S–6S racing packs: not retrieved, though
  battery-voltage fluctuation is named as a cause of failure (D-14).
- Trial counts: per-speed counts for A-20, per-condition counts for A-29, and the counts behind A-14 are all
  missing; the 25-sim/20-real counts in the quantitative facet were inferred and are not supported.
- Swift's peak speed and acceleration, and its lap time as a fraction of its platform's time-optimal lap, were
  not found.
- Whether a quadrotor's position or attitude loop carries a RHP zero or pole that sets a bound (D-28): unsourced.
  The textbook's explicit delay-plus-RHP-pole bound (lecture-note constants of about wc*T_d < 0.4 and p*T < 0.16
  at Ms < 2) was seen only in a search summary and is unverified.
- Cramer-Rao style bounds on VIO drift versus speed and motion blur; rotor-bandwidth/jerk theory;
  perception-aware planning theory (a 2026 preprint, arXiv:2603.04305, was seen in search and not read).
- Coverage of 2025–26 ICRA/IROS/CoRL work is incomplete: Semantic Scholar was rate-limited (HTTP 429) across
  all four facets, so citing-paper and rebuttal searches were not completed, and INSPIRE does not index this
  literature.

Papers to request (deduplicated):

- 10.1109/lra.2019.2898117 | Falanga, Kim, Scaramuzza, "How Fast Is Too Fast? The Role of Perception Latency in
  High-Speed Sense and Avoid" | the exact bound v_max(latency, range, a_max), its stated assumptions, and the
  paper's measured latencies, to set against a usable perception range. (The theory facet did reach an
  author-hosted PDF and quoted Eqs. 8–9; the critiques facet could not. Requesting the published version would
  settle the garbled square-root layout against the paper's own figures.)
- 10.1109/ICRA.2019.8793887 (DOI unverified — look it up before requesting) | Delmerico et al., "Are We Ready
  for Autonomous Drone Racing? The UZH-FPV Drone Racing Dataset" | per-algorithm VIO failure rates at racing
  speed, i.e. a direct estimation-binds sensitivity.
- 10.1126/scirobotics.ado6187 (plus its erratum 10.1126/scirobotics.adx3476) | Ren et al., "Safety-assured
  high-speed navigation for MAVs" | onboard sensing and mass class, speed and trial count of the fastest
  unknown-environment hardware result, and what the erratum changed.
- 10.1126/scirobotics.aee9250 | Bahnam et al., MonoRace (published version of arXiv:2601.15222) | whether the
  A-26/A-27/A-28 numbers survive review, and the setting (hardware vs simulation) of the 4- and 7-trial rows.
- 10.1109/icra.2011.5980409 | Mellinger, Kumar, "Minimum snap trajectory generation and control for quadrotors"
  | the original flatness statement and its actuator-constraint treatment (low priority; D-01 restates flatness).
- The published supplement of Song et al. 2023 (10.1126/scirobotics.adg1462) | the trial counts behind A-14.

## 7. Source-quality notes

**Dropped (contradicted):**
- The sub-claim in RQ-10 that the urban simulation reached "100 per cent at 7 m/s and 80 per cent at 10 m/s",
  and the conclusion that the brief's 90 per cent threshold is met at speeds up to 7 m/s, are **dropped**. The
  check found the "no failure up to 7 m/s, 60 per cent at 10 m/s" sentence belongs to the narrow-gap simulation,
  not the urban one; the "two failures" are real-world forest runs at 7 m/s (8 of 10 = 80 per cent); and the
  supplement reports 90 per cent at 10 m/s only on the low-difficulty task. A-20 carries the corrected figures.
- RE-11's statement that MonoRace gives no success rate for its 16.56 s policy is **dropped**: the paper's table
  gives M16 at 1 of 4 trials (25.0 per cent) with a 16.56 s mean completion time, and M17 at 5 of 7
  (71.4 per cent). A-27 carries both, and the correction materially weakens any reading of 16.56 s as routine.

**Corrected (misattributed):**
- RQ-04's VIO RMSE mapping was wrong. Correct values: RealSense T265 = 0.151 m (circle) and 0.114 m
  (lemniscate); monocular SVO + IMU = 0.217 m (circle) and 0.131 m (lemniscate). The trajectories run up to
  7 m/s, so calling them "gentle" is loose. Because the mapping was the only content of the claim's ranking,
  no conclusion in this dossier rests on which estimator was better.
- RC-08's "average success rate of 70 per cent at 10 m/s" is a **simulation** benchmark figure (Flightmare, 10
  forest seeds per method), not a second real-world figure; the simulated forest figure is 60 per cent. The
  "two figures in one paper" reading is a hardware-versus-simulation difference, not an internal contradiction.
- RE-05's "5 to 7 m/s with success near 100 per cent" is corrected to 100 per cent only up to 5 m/s and
  80 per cent (8 of 10) at 7 m/s (A-20). RE-22 inherits this correction, and so does D-20.
- RE-10's "27.8 m/s peak" understates the paper's own table, which lists per-policy maxima up to 32.2 m/s
  (about 116 km/h); A-26 carries both numbers.
- RT-04's benchmark distance range is 3 to 15 m, not 6 to 15 m (the 0.89 s time is the 3 m case). The
  2.00 / 2.68 per cent figures are unaffected (A-17).
- RT-16's claim that a range gain beats a latency cut by "5 to 15 times" is corrected to roughly 4 to 14 times
  across its own cases (the 10 m, 100 ms dodge case gives 4.2) (A-33).
- RQ-02's gloss that the 39.1 ms time constant "includes motor, ESC and propeller" is the researcher's
  inference; the paper says only "motor time constant" (A-03). Likewise RQ-13's reading of the 33 ms vs 39.1 ms
  difference as rotor-speed-vs-force is an inference, retained as such in A-04.
- RE-13's inference that "estimation, not thrust, is dominant" is the researcher's, not the paper's (D-19).
- RT-08's applicability to quadrotors is the researcher's own reading and is flagged as unestablished (D-28).

**Status corrections:** none needed. RT-11/RQ-08/RE-07 (Song et al.) was correctly labelled peer-reviewed; the
check added that the real-world flights used Vicon motion capture plus an EKF, confirming that those rows are
controller evidence and not onboard-only — this is now stated in D-14 and A-14. RE-10/RE-11/RE-12 are correctly
labelled preprint even though a journal version exists, because only the arXiv version was opened. Conference
proceedings (RSS, ICRA) are treated as peer-reviewed per the schema.

**Unverifiable, kept with their labels:**
- RQ-06 and RQ-07 (Swift VIO-drift quotes; the domain-shift ablation) were not re-checked in the quantitative
  pass, but the same drift quotes were verified in the critiques and engineering checks, so D-12 is supported
  and D-18 rests on an unverified-in-this-pass quote.
- RQ-16(a) (ICM-42688-P noise figures, A-25): search summary only, datasheet not opened.
- RC-14 (UZH-FPV dataset), RC-17 (2025 A2RL press), RE-14 (2026 A2RL press), RE-18 (overfitting lead),
  RE-15 (AI Grand Prix schedule, page timed out), RE-21 (SUPER, abstract plus press), RE-22 (the engineering
  researcher's own synthesis row): all unverifiable or search-summary and kept as such.

**Superseded values:**
- A-22 (about 130 ms state-estimation latency, AlphaPilot 2019) is superseded as the state of the art by A-07
  (40 ms sensorimotor latency, Swift 2023) and A-28 (17 ms simulated image delay, MonoRace 2026). It is kept as
  the historical figure, not as a rival anchor; do not count it as independent evidence about present hardware.
- A-26/A-27/A-28 (MonoRace, arXiv v1) are preliminary pending the published Science Robotics version
  (doi:10.1126/scirobotics.aee9250), which was not opened. If the published numbers differ, they supersede these.
- A-04 (33 ms rotor-speed time constant) does **not** supersede A-03 (39.1 ms thrust time constant): they are
  different quantities measured on near-identical airframes by the same research group, so treat them as
  correlated rather than independent.
- Correlated apparatus more generally: A-01 to A-06, A-07 to A-10, A-16 to A-18 and A-20 to A-21 come from one
  research group's platform lineage (Agilicious and its derivatives, 750–890 g, T/W 4.1–4.5). A statistician
  should treat these as sharing an apparatus, not as independent replications. A-11/A-12 (0.52 kg, T/W 12.35)
  and A-26 to A-28 (TU Delft, Orin NX) are the two genuinely different platforms in this evidence base.
- A-15 (0.92 of the model optimum) mixes a simulation number with a mocap-hardware number and rests on a value
  read off a dashed line; it is marked preliminary and should not be used as the brief's time-optimal fraction.

**Share of claims resting only on search summaries:** 76 claims were compiled (theory 20, quantitative 17,
critiques 17, engineering 22). Five carry `ACCESS: search-summary` as their whole basis (RC-14, RC-17, RE-14,
RE-18, RE-22) and one is part search-summary (RQ-16(a)), i.e. about 7 per cent (6 of 76). Two more rest on
abstracts only (RE-13, RE-21). All four facets have check files; no facet is unchecked.

**Facets named in the brief and present:** theory, quantitative, critiques, engineering — all four were
researched and all four were checked. No facet named in the brief is missing.

**Claims carried from earlier runs:** none. The brief lists five prior runs, all in general relativity,
quantum field theory or particle physics, all marked `ignore`; no `prior/` material exists for this run, so zero
claims were carried and zero re-verified.

**Fringe excluded:** none; no claim in any facet was labelled fringe.
