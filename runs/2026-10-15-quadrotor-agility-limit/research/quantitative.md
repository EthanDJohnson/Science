# Research: quantitative
status: final
Mandate: measured numbers (mass, thrust-to-weight, motor/prop time constants, IMU, camera, VIO latency, compute, aerodynamics) with units, conditions, sources. All units SI unless stated.
Access: lit_search INSPIRE ok (no robotics hits), arXiv ok, Crossref ok, Semantic Scholar rate-limited; fetch_text/find_fulltext opened arXiv PDFs and Europe PMC; publisher/ZORA pages gave bot checks; WebFetch not used; WebSearch for two items (search-summary only)

## Claims
- [RQ-01] CLAIM: The Agilicious reference platform (5.1-inch props, Xrotor 2306 2400 kV motors, 4S 1800 mAh LiPo, Jetson TX2 compute, BrainFPV Radix flight controller) is a 750 g class vehicle, quoted by its authors as ">5 g acceleration" and 131 km/h (36.4 m/s) maximal speed; component masses: frame 86 g, motors 4x27.5 g, props 4x5 g, battery 199 g, FC 6 g, ESC 15 g, Jetson TX2 154 g. Compute is the single heaviest non-battery item (about 20 per cent of mass).
  SOURCE: Foehn et al., 2022, "Agilicious: Open-source and open-hardware agile quadrotor for vision-based flight", Science Robotics 7(67) (arXiv preprint 2307.06100 of doi:10.1126/scirobotics.abl6259), https://arxiv.org/pdf/2307.06100
  QUOTE: "The design objectives resulted in creating a lightweight750 g platform with maximal speed of 131 km/h." ; "Frame Armattan Chameleon 6 inch 4 mm carbon fiber, 86 g Motor Xrotor 2306 23×6 mm stator, 2400 kV, 758 W, 4× 27.5 g Propeller Azure Power SFP 5148 5.1 inch length and 4.8 inch pitch, 4× 5 g Battery Tattoo R-Line 1800 4× 3.7 V, 1800 mA h, 199 g Flight Controller BrainFPV radix BetaFlight or custom firmware, 6 g Motor Controller HobbyWing XRotor DShot protocol, 4× 60 A, 15 g Compute Unit nVidia Jetson TX2 6× ARM 2.0 GHz, 256 × CUDA cores, 8 GB, 154 g"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  ARTIFACT: code https://github.com/uzh-rpg/agilicious
  CONFIDENCE: high

- [RQ-02] CLAIM: Agilicious measured motor time constant is 39.1 ms (first-order fit to load-cell thrust response to a 12 N collective-thrust step), and the command-to-force-onset latency is 35 ms (agiNuttx onboard FC), 40.15 ms (BetaFlight), and >75 ms with offboard command over a Laird radio link. So pipeline delay is of the same order as the motor time constant (the 39.1 ms figure includes motor, ESC and propeller; the paper uses it as the "actuator bandwidth limitation").
  SOURCE: Foehn et al., 2022, Science Robotics 7(67), arXiv preprint 2307.06100 of doi:10.1126/scirobotics.abl6259, https://arxiv.org/pdf/2307.06100
  QUOTE: "The results show that both agiNuttx has the lowest latency at 35ms, with BetaFlight slightly slower at 40.15 ms. A large delay can be observed when using offboard control and sending the commands via Laird connection to the drone, in which case the latency rises to more than 75ms." ; "the motor’s time constant of 39.1ms, which dictates the actuator bandwidth limitations, is indicated in Figure 3C."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  ARTIFACT: code https://github.com/uzh-rpg/agilicious
  CONFIDENCE: high

- [RQ-03] CLAIM: Agilicious tracking of agile trajectories (MOTION CAPTURE, 400 Hz Vicon, 36 cameras - evidence on the controller, not on the onboard-only question): positional RMSE 0.322 m (agiNuttx, onboard MPC), <0.385 m (BetaFlight onboard), 0.474 m (offboard control, higher latency), at up to 60 km/h (16.7 m/s) and 4 g; simulation with BEM aerodynamics gave 0.320 m. Showing that adding ~40 ms of extra latency (35 -> >75 ms) raised tracking RMSE by about 47 per cent (0.322 -> 0.474 m) on the same airframe and same controller.
  SOURCE: Foehn et al., 2022, Science Robotics 7(67), arXiv preprint 2307.06100, https://arxiv.org/pdf/2307.06100
  QUOTE: "performance with the lowest average positional root-mean- square error (RMSE) of just 0.322m at up to 60 km/h and 4 g. Next up is the second configuration with BetaFlight, still achieving less than 0.385m average positional RMSE. Finally, the third configuration with offboard control exhibits higher latency, leading to an increased average positional RMSE of 0.474m."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  ARTIFACT: code https://github.com/uzh-rpg/agilicious
  CONFIDENCE: high

- [RQ-04] CLAIM: Agilicious onboard VIO (the vision-based state estimators it was tested with): camera at 30 Hz (Sony IMX-287, 165 deg diagonal FoV) plus 500 Hz flight-controller IMU with SVO, or the Intel RealSense T265; positional RMSE versus mocap ground truth 0.151 m / 0.217 m (RealSense on circle / lemniscate) and 0.114 m / 0.131 m (SVO+IMU on circle / lemniscate, order as in the figure labels); these are on gentle circle and lemniscate trajectories, not racing speeds.
  SOURCE: Foehn et al., 2022, Science Robotics 7(67), arXiv preprint 2307.06100, https://arxiv.org/pdf/2307.06100
  QUOTE: "a single Sony IMX-287 camera at 30Hz with a 165° diagonal field-of-view is used, combined with the IMU measurements of the flight controller at 500Hz, calibrated using the Kalibr toolbox" ; figure text: "RealSense PositionalRMSE Circle Circle Lemniscate Lemniscate SVO Groundtruth 0.151m 0.217m 0.114m 0.131m"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  ARTIFACT: code https://github.com/uzh-rpg/agilicious
  CONFIDENCE: medium (the mapping of the four RMSE numbers to labels is read from extracted figure text)

- [RQ-05] CLAIM: Swift (Nature 2023) vehicle: 870 g, ~35 N maximum static thrust, static thrust-to-weight 4.1 (T-Motor Velox 2306, 5-inch three-blade props, Agilicious-based); the same airframe was flown by human champions with ballast in place of the Jetson and RealSense. Onboard stack: Jetson TX2 (6-core 2 GHz CPU, 256 CUDA cores); racing-policy forward pass 8 ms on the CPU; gate-detection network 40 ms per forward pass on the TX2 GPU (FP16, 384x384 input, TensorRT); Intel RealSense T265 VIO at 100 Hz; camera refresh 30 Hz; commands (collective thrust + body rates) go to a Betaflight FC on a 216 MHz STM32. Authors quote Swift's sensorimotor latency as 40 ms versus an average 220 ms for expert human pilots. NB the gate-detection network is used to correct VIO drift against KNOWN gate landmarks: the track layout is known, so this is a seen-course result.
  SOURCE: Kaufmann et al., 2023, "Champion-level drone racing using deep reinforcement learning", Nature 620, 982-987 (published version via Europe PMC, doi:10.1038/s41586-023-06419-4)
  QUOTE: "Each vehicle has a weight of 870 g and can produce a maximum static thrust of approximately 35 N, which results in a static thrust-to-weight ratio of 4.1." ; "the racing policy is evaluated on the CPU, with one inference pass taking 8 ms. The autonomous drones carry an Intel RealSense Tracking Camera T265 that provides VIO estimates 59 at 100 Hz" ; "our system benefits from lower sensorimotor latency (40 ms for Swift versus an average of 220 ms for expert human pilots 39 )" ; "One forward pass through the network takes 40 ms on the NVIDIA Jetson TX2."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high

- [RQ-06] CLAIM: Swift's authors state that high-speed flight degrades the onboard estimate: motion blur "can lead to a loss of tracked visual features and severe drift in linear odometry estimates", and that VIO "exhibit[s] substantial drift during high-speed flight"; they model this drift with a Gaussian process fitted to a handful of real-world rollouts (three rollouts, about 50 s of flight) and use camera-detected gate corners to correct it. Residual dynamics (acceleration residual vs state and thrust) were fitted with k=5 nearest-neighbour regression on 800-1,000 samples. No drift magnitude in m per m is given in the text I retrieved.
  SOURCE: Kaufmann et al., 2023, Nature 620, 982-987 (published version via Europe PMC)
  QUOTE: "Navigating at high speeds results in substantial motion blur, which can lead to a loss of tracked visual features and severe drift in linear odometry estimates." ; "The odometry estimates from the VIO pipeline 54 exhibit substantial drift during high-speed flight. We use gate detection to stabilize the pose estimates produced by VIO."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high

- [RQ-07] CLAIM: In Swift's own simulation ablation, none of three baselines (two learning-based, one time-optimal MPC) completed even one lap when either the dynamics or the observations were perturbed (domain shift), although all completed it with idealised dynamics and ground-truth observations; and "No traditional method has achieved competitive lap times compared with Swift or human world champions, even when provided with highly accurate state estimation from a motion-capture system." This is a model-error / sim result, not a hardware sensitivity.
  SOURCE: Kaufmann et al., 2023, Nature 620, 982-987 (published version via Europe PMC)
  QUOTE: "When deployed in settings that feature domain shift, either in the dynamics or the observations, the performance of all baselines collapses and none of the three baselines are able to complete even a single lap."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: simulation
  CONFIDENCE: high

- [RQ-08] CLAIM: MOCAP result (controller evidence only, not onboard-only). Song et al. 2023 built a 0.52 kg, 63 N-thrust racing drone, maximum thrust-to-weight 12 (6S battery; the DJI FPV drone is about 4, the Agilicious/Swift platform 4.1 per RQ-05), peak acceleration >12 g and peak velocity 108 km/h (30 m/s), flown with a Vicon motion-capture system plus EKF for state, RL policy at 100 Hz feedback. The authors flag this explicitly: "the autonomous policy benefited from a number of structural advantages, such as access to perfect state estimation from a motion capture system".
  SOURCE: Song, Romero, Mueller, Koltun, Scaramuzza, 2023, "Reaching the limit in autonomous racing: Optimal control versus reinforcement learning", Science Robotics 8(82) (arXiv preprint 2310.10943 of doi:10.1126/scirobotics.adg1462), https://arxiv.org/pdf/2310.10943
  QUOTE: "we have built a racing drone that can produce a maximum thrust-to- weight (TWR) ratio of 12. This drone has a total weight of only0.52 kg and can generate a maximum thrust of 63 N (given a fully charged battery)." ; "We use a Vicon motion capture system together with an Extended Kalman Filter to estimate the quadrotor state, including position, velocity, and orien- tation. The RL policy is executed with a feedback control frequency of 100 Hz." ; "achieving a peak acceleration greater than 12 g and a peak velocity of 108 km/h"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  ARTIFACT: video (multimedia material cited in paper; not checked)
  CONFIDENCE: high

- [RQ-09] CLAIM: Fraction of own time-optimum, MOCAP and known track, 4S drone (Song et al. 2023, Fig. 2C, 25 trials per sim cell as read from success percentages; real-world 20 trials as read from 85 per cent): lap time (mean +/- s.d.) and success rate. Nominal model: trajectory tracking of time-optimal plan 4.92 +/- 0.10 s (44 per cent success), contouring control 5.03 +/- 0.18 s (76 per cent), RL 5.14 +/- 0.09 s (100 per cent). Realistic (perturbed) model: tracking none (0 per cent), contouring 5.34 +/- 0.27 s (20 per cent), RL 5.26 +/- 0.32 s (100 per cent). Real world: tracking none (0 per cent), contouring 5.54 +/- 0.21 s (50 per cent), RL 5.35 +/- 0.15 s (85 per cent). The theoretical time-optimal lap time computed with an approximate drone model is about 4.9 s, and the authors state the truly time-optimal value for the physical vehicle is unknown. So the best 90-per-cent-style real result (RL, 85 per cent success, below the brief's 90 per cent) reaches 4.9/5.35 = 0.92 of the model optimum (my arithmetic). Model error, not hardware, is what turns 4.92 s/44 per cent into 0/0 per cent for the plan-then-track controllers.
  SOURCE: Song et al. 2023, Science Robotics 8(82), arXiv preprint 2310.10943, https://arxiv.org/pdf/2310.10943
  QUOTE: "Nominal 4.92± 0.10 44.0 5.03± 0.18 76.0 5.14± 0.09 100.0 Realistic – 0.0 5.34± 0.27 20.0 5.26± 0.32 100.0 Real World – 0.0 5.54± 0.21 50.0 5.35± 0.15 85.0" ; "Note that the truly time-optimal solution for the physical vehicle is unknown and the theoretical time-optimal trajectory, computed with respect[...]" (text truncated in extraction)
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: medium (the table's row/column assignment is from extracted text; trial counts not stated in the lines I retrieved)

- [RQ-10] CLAIM: The nearest published result to the brief's metric: Loquercio et al. 2021, purely onboard sensing and computation, UNSEEN natural and human-made environments, policy trained in simulation only. Platform: 890 g, about 40 N maximum thrust, thrust-to-weight 4.4 (Armattan Chameleon 6 inch, Hobbywing XRotor 2306, 5-inch three-blade props), Jetson TX2, RealSense T265 VIO at 200 Hz, RealSense D435i depth at 30 Hz VGA (about 90 deg horizontal field of view; tilted 30 deg for >=7 m/s). Average flight speeds 3 to 10 m/s; success = reaching a goal within 5 m without a crash; 56 real-world experiments in total. In SIMULATION (tree/forest, 3-10 m/s): 100 per cent success up to 5 m/s, 60 per cent at 10 m/s, baselines (mapping+FastPlanner, reactive) 0 successful runs at 10 m/s. In the simulated urban environment: up to 100 per cent at 7 m/s and 2 failures in 10 runs at 10 m/s (80 per cent). In the REAL world the authors report 60 per cent success at 10 m/s average speed, failures "mainly happening in the proximity of narrow openings less than a meter wide". This is 10 m/s at 60 per cent; the brief's 90 per cent threshold is met only at <=7 m/s (the per-speed real-world trial counts are in the paper's Fig. 3D-E, not retrieved). The same airframe class reaches 60 km/h (16.7 m/s) at 4 g under mocap on a known trajectory (RQ-03), so the unseen-course onboard speed is about 0.6 of that known-trajectory figure (my ratio, different tasks, indicative only).
  SOURCE: Loquercio, Kaufmann, Ranftl, Mueller, Koltun, Scaramuzza, 2021, "Learning high-speed flight in the wild", Science Robotics 6(59), arXiv preprint 2110.05113, https://arxiv.org/pdf/2110.05113
  QUOTE: "At a low speed of 3 m s−1, all methods successfully complete every run. As speed increases, the success rates of the baselines quickly degrade. At 10 m s−1, no baseline completes even a single run successfully. In contrast, our approach is very robust at higher speeds. It achieves 100% success rate up to 5 m s−1. At the highest speed of 10 m s−1, our approach still keeps a success rate of 60%." (simulation); "we push the average flight speed even higher to 10 m s−1. At this speed, external disturbances, e.g. aerodynamics, battery power drops, and motion-blur start to play an important role and widen the simulation to reality gap. Nonetheless, we achieve a success rate of 60%, with failures mainly happening in the proximity of narrow openings less than a meter wide" (real world); "The platform has a total weight of 890 grams and can produce a maximum thrust of about 40 N, which results in a thrust-to-weight ratio of 4.4."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware (real-world 10 m/s, 60 per cent) and simulation (per-speed tables); trial counts per speed not retrieved, 56 real-world experiments total
  ARTIFACT: code https://github.com/uzh-rpg/agile_autonomy
  CONFIDENCE: high for quoted numbers; the speed "ceiling" interpretation is mine

- [RQ-11] CLAIM: Sensing-range/latency inputs used by Loquercio et al. for the perception-limited speed bound (extends Falanga et al. 2019 point-mass model with rotational latency): quadrotor with initial forward velocity v at 6 m from a 1.5 m diameter pole, modelled as 0.2 m radius sphere; maximum speed depends on sensing range, the visual-sensor latency (inverse of frame rate) and processing latency. Measured Jetson TX2 processing: FastPlanner pipeline 65.2 ms per frame (highest), with the end-to-end network faster; the learned network runs at about 24 Hz onboard (see paper). The theoretical max speeds per method are in the paper's Fig. 5 (not retrieved).
  SOURCE: Loquercio et al. 2021, Science Robotics 6(59), arXiv preprint 2110.05113, https://arxiv.org/pdf/2110.05113
  QUOTE: "With a total computation time of 65.2 ms per frame, FastPlanner incurs the highest processing latency." ; "The maximum speed depends on the sensing range, i.e. how far can an obstacle be accurately perceived, the latency of the visual sensor, i.e. the inverse of the frame rate, and the processing latency, i.e. the time to convert an observation into motor commands."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: medium

- [RQ-12] CLAIM: Event-camera state-estimation latency (hardware, a dualcopter, 1-DOF roll, not a quadrotor): update rate 1 kHz, latency 12 ms, attitude tracking at over 1600 deg/s. The 12 ms is for the full event Hough-transform + Kalman estimator, versus about 30-100 ms for frame-based VIO pipelines in RQ-05/RQ-10 (frame period alone 33 ms at 30 Hz). Evidence by analogy only for a 4-rotor vehicle.
  SOURCE: Dimitrova, Gehrig, Brescianini, Scaramuzza, 2020, "Towards Low-Latency High-Bandwidth Control of Quadrotors using Event Cameras", ICRA 2020, arXiv preprint 1911.04553, https://arxiv.org/pdf/1911.04553
  QUOTE: "the state estimator performs with an update rate of 1 kHz and a latency determined to be 12 ms, enabling attitude tracking at speeds of over 1600◦/s."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high

- [RQ-13] CLAIM: Rotor-speed time constant and platform, NeuroBEM data (MOCAP, Vicon, 96 flights, 1 h 15 min, 1.8 million data points, speeds to 65 km/h = 18 m/s): platform 752 g, ~33 N static thrust, static thrust-to-weight 4.5; first-order rotor-speed model with identified tau_Omega = 33 ms (compare 39.1 ms thrust time constant measured on the near-identical Agilicious airframe, RQ-02; the difference is the quantity measured: rotor speed versus force).
  SOURCE: Bauersfeld, Kaufmann, Foehn, Sun, Scaramuzza, 2021, "NeuroBEM: Hybrid Aerodynamic Quadrotor Model", RSS XVII, arXiv preprint 2106.08015 (doi:10.15607/RSS.2021.XVII.042), https://arxiv.org/pdf/2106.08015
  QUOTE: "the motors are modeled as a first-order system ... where Ωcmd is the commanded propeller speed and τΩ is the motor time constant. For the quadrotor platform used throughout the experiments, the time constant was identified to be τΩ = 33 ms." ; "The platform has a total weight of 752 g and can produce a maximum static thrust of approximately 33 N, which results in a static thrust-to-weight ratio of 4.5."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high

- [RQ-14] CLAIM: Aerodynamic model error grows with speed (positional RMSE between simulated and real-flown trajectories, MOCAP flights, 752 g quad; columns Fit = quadratic-rotor fitted model, BEM = blade-element-momentum model, BEM+NN = hybrid, RotorS = standard simulator; read from extracted table text, columns by header order): Lemniscate (mean 1.67 m/s, max 3.51 m/s): Fit 0.061 m, BEM 0.059 m, BEM+NN 0.049 m, RotorS 0.114 m. Random points (mean 2.38, max 8.25 m/s): Fit 0.167 m, BEM 0.138 m, RotorS 0.239 m. Lemniscate (mean 3.21, max 7.04 m/s): Fit 0.183 m, BEM 0.146 m, RotorS 0.148 m. Slanted circle (mean 6.92, max 10.75 m/s): Fit 0.381 m, BEM 0.232 m. The authors' headline: hybrid BEM+NN "reproduces the flown trajectories in simulation with a positional RMSE error reduction of over 50% compared to state-of-the-art". Aerodynamic effects "become the dominant model defect during high speeds or agile maneuvers". Force-prediction RMSE of the hybrid network on a held-out test set: 0.35-0.37 N (about 1 per cent of the 33 N static thrust, or ~5 per cent of the 7.4 N weight of the vehicle; my ratios), torque RMSE 4.7-6.5 x10^-3 N m.
  SOURCE: Bauersfeld et al. 2021, RSS XVII, arXiv preprint 2106.08015, https://arxiv.org/pdf/2106.08015
  QUOTE: "vmean [m/s] vmax [m/s] Fit BEM PolyFit [13] None+NN Fit+NN BEM+NN (ours) ... Lemniscate 1.67 3.51 0.061 0.059 0.043 0.046 0.049 0.059 0.046 0.049 0.048 0.053 0.114" ; "Aerodynamic effects, while insignificant at low speeds, become the dominant model defect during high speeds or agile maneuvers."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware (data), simulation (the RMSE is of simulation versus flight)
  ARTIFACT: dataset (NeuroBEM dataset, referred to in paper; URL not retrieved)
  CONFIDENCE: medium (table column assignment inferred from header order)

- [RQ-15] CLAIM: Platform's own time-optimum depends on thrust-to-weight: Foehn et al. 2021 (MOCAP track roughly 25 x 30 x 8 m, ~0.8 kg drone with theoretical TWR ~4) planned time-optimal point-mass-plus-rates trajectories with the thrust bound set at a TWR from 2.5 (lap 7.14 s) to 3.6 (lap 5.81 s); two real flights at planner TWR 3.15 (6.27 s) and 3.3 (6.10 s) beat the best human lap. Planner thrust bound was kept below the ~4 absolute limit "to maintain controllability under disturbances". From these published pairs, d ln(lap time)/d ln(TWR) = -0.565 over 2.5 to 3.6 (speed elasticity about +0.57 if path length were fixed; it is not exactly, since the optimal path changes) [calc: runs/2026-10-15-quadrotor-agility-limit/calc/quantitative_elasticity.py]. This is a planner-model sensitivity (known track, MOCAP), the number needed to set thrust-to-weight aside or establish it (hidden premise 4).
  SOURCE: Foehn, Romero, Scaramuzza, 2021, "Time-optimal planning for quadrotor waypoint flight", Science Robotics 6(56) eabh1221 (arXiv preprint 2108.04537 of doi:10.1126/scirobotics.abh1221), https://arxiv.org/pdf/2108.04537
  QUOTE: "we plan the trajectory for a multitude of thrust-to-weight ratios reaching from 2.5 with a lap time of 7.14 s to a maximum of 3.6 resulting in a lap time of 5.81 s. As expected, the time shrinks with higher thrust-to-weight capabilities. We evaluate two configurations with thrust-to-weight ratios of 3.15 (6.27 s) and 3.3 (6.10 s) in our real-world experiments"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: simulation (the TWR sweep); hardware with motion capture for the two flown cases
  ARTIFACT: code https://github.com/uzh-rpg/rpg_time_optimal
  CONFIDENCE: high for the quoted pairs; medium for the elasticity as a general result

- [RQ-16] CLAIM: Sensor-side numbers, datasheet level. TDK InvenSense ICM-42688-P (IMU common on racing flight controllers): gyroscope noise 2.8 mdps/sqrt(Hz) (= 0.0028 deg/s/sqrt(Hz)), accelerometer noise 70 ug/sqrt(Hz) (65 on X and Y, 70 on Z), datasheet v1.8 (2023-07-27). Event cameras: latency about 10 us on the lab bench and sub-millisecond in the real world (survey), 140 dB dynamic range, ~3 kHz DVS pixel bandwidth in bright light. Neither gyro bias stability nor a flight-measured IMU-to-actuator delay was retrieved (see Gaps).
  SOURCE: (a) TDK InvenSense ICM-42688-P product page and datasheet DS-000347 as summarised by search, https://invensense.tdk.com/products/icm-42688-p/ ; (b) Gallego et al., 2020, "Event-based Vision: A Survey", IEEE TPAMI (arXiv preprint 1904.08405), https://arxiv.org/pdf/1904.08405
  QUOTE: (b) "Hence, event cameras have minimal latency: about 10 µs on the lab bench, and sub-millisecond in the real world." (a) SUMMARY: "TDK's product page lists the noise as 2.8 mdps/√Hz ... The headline spec is 70 µg/√Hz ... XY: 65, Z: 70 ... Version 1.8, updated 2023-07-27" (search summary, not verified against the datasheet text)
  ACCESS: full-text for (b); search-summary for (a)
  STATUS: peer-reviewed for (b); secondary for (a)
  SETTING: n/a
  CONFIDENCE: high for (b); medium for (a)

- [RQ-17] CLAIM: Derived ratios from the sources above, all my arithmetic [calc: runs/2026-10-15-quadrotor-agility-limit/calc/quantitative_elasticity.py]: (i) command-to-force latency 35 ms (agiNuttx) and 40.15 ms (BetaFlight) are 0.90 and 1.03 times the 39.1 ms thrust time constant (RQ-02); (ii) a 30 Hz camera frame period is 33.3 ms, i.e. about the same as the motor time constant and about the whole 35 ms actuation latency; the 100 Hz T265 output has a 10 ms period; (iii) in Agilicious, +40 ms of command latency (35 to >75 ms, together with a change from the onboard FC to a radio link, so the effect is confounded) raised MOCAP tracking RMSE by 47 per cent, a log-log slope of at most 0.51 (RQ-03); (iv) thrust-to-weight: Swift 4.10 (35 N, 870 g), Loquercio platform 4.4, Agilicious/NeuroBEM 4.5 (752 g), Song 12.35 (63 N, 0.52 kg); (v) unit conversion: 131 km/h = 36.4 m/s, 108 km/h = 30.0 m/s, 65 km/h = 18.1 m/s.
  SOURCE: computed from RQ-02, RQ-03, RQ-05, RQ-08, RQ-10, RQ-13, RQ-15
  SUMMARY: "see calc log"
  ACCESS: full-text (inputs)
  STATUS: secondary (derived)
  SETTING: analysis
  CONFIDENCE: medium

## Gaps
- Gyro bias stability, IMU-to-controller sample/delay, ESC/DShot update rates and the maximum rotor-speed slew rate (rad/s^2) for 5-inch racing motors were not retrieved; only first-order time constants (33 ms rotor speed, 39.1 ms thrust) were. The slew rate is asymmetric (spin-up faster than spin-down with no active braking) and I have no measured source for that asymmetry here.
- Falanga et al. 2019 ("How Fast Is Too Fast", doi:10.1109/lra.2019.2898117): free copy not retrievable (bot-checks, landing pages only); the closed-form latency/range/speed relation and measured latencies were not quoted. Only its use inside Loquercio et al. (RQ-11) was seen. This belongs to the theory facet.
- Rotor-drag coefficients: Faessler et al. 2018 (arXiv 1712.02402) was opened but numerical dx, dy values were not retrieved. Blade-flapping and rotor-interaction coefficients with speeds were not obtained; the only aerodynamic magnitudes retrieved are the NeuroBEM RMSE table (RQ-14).
- End-to-end VIO latency (camera exposure to pose) and drift in m per m at racing speeds: not retrieved. Swift says "substantial drift" without a magnitude in the text I read (RQ-06); the Agilicious VIO RMSEs (RQ-04) are at low speeds.
- Event-camera quadrotor closed-loop flight with the full 4-rotor vehicle (Falanga et al. 2020, Science Robotics, dynamic obstacles) not retrieved; RQ-12 is a 1-DOF dualcopter.
- Battery specific energy and discharge-power limits (LiPo, racing 4S-6S) not retrieved; Song 2023 mentions a voltage drop lengthening one lap, but I did not quote it.
- Motion blur and exposure numbers for onboard cameras at racing speed: not retrieved (Loquercio and Swift only say motion blur matters).
- Onboard compute throughput beyond Jetson TX2 (1.33 TFLOPS per the Agilicious Table 1, 154 g) and newer platforms: belongs to engineering; not collected here.
- Newer work (2024-2026) on onboard-only racing or unseen-course speed: one lit_search --since 2024 returned only irrelevant hits; no result newer than the ones above was found for this facet. No erratum or re-analysis of the cited measurements was found, but I did not run `refersto:` searches because the papers are robotics and are not indexed by INSPIRE.
- Semantic Scholar rate-limited (HTTP 429) on two searches; Crossref worked.
