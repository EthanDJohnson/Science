# Research: critiques
status: final
Mandate: the case against each candidate limit (actuator, estimation latency, aerodynamics, perception range): rival-limit arguments, negative results, sim-to-real failures, benchmark/metric critiques, and the human-pilot gap.
Access: lit_search INSPIRE mostly empty for robotics (one SSL failure), arXiv ok, Crossref ok, Semantic Scholar rate-limited (HTTP 429); WebFetch not used; fetch_text.py / find_fulltext.py worked on arxiv.org, Europe PMC, fpv.ifi.uzh.ch, wikipedia; nature.com and zora.uzh.ch served bot-check pages.

Orientation for the slate builder (my reading, each point is backed by the claims below):
- Not one published onboard-only result meets the brief's metric (unseen course, at least 90 % success, stated trials, fraction of own time-optimal time). The fastest onboard gate-course results (RC-01, RC-10) are on a known, pre-mapped track; the unseen-environment onboard results (RC-08) are 3-10 m/s on a straight reference line, not a gate course.
- The critiques split by speed regime: perception field of view and latency bind at about 7 m/s in clutter (RC-08, RC-09); unmodelled aerodynamics, battery sag, motion blur and variable delay bind at 10 m/s and above, and at racing speeds (RC-04, RC-06); estimation drift is repaired with known-gate information (RC-02, RC-07).
- The human gap is argued to be mostly policy/strategy and perception robustness, not airframe: same airframe, Swift wins starts and tight turns, loses on segments (RC-03).

## Claims

- [RC-01] CLAIM: The Nature "Swift" result is on a track whose gate layout is known in advance (detected gates are matched to "the known track layout" to correct VIO drift); the track is 75 m long per lap, races are three laps head-to-head, and the human pilots had one week of practice. It is therefore a seen-course, not unseen-course, result. Sensing and compute are onboard (VIO plus a gate-corner detector on an NVIDIA Jetson TX2, 40 ms per gate-detector forward pass).
  SOURCE: Kaufmann et al. 2023, Champion-level drone racing using deep reinforcement learning, Nature 620:982-987, doi:10.1038/s41586-023-06419-4 (published version, Europe PMC PMC10468397)
  QUOTE: "ed to the closest gate in the known track layout, thus yielding a pose estimate for the drone." ; "One forward pass through the network takes 40 ms on the NVIDIA Jetson TX2." ; "The human pilots were given one week of practice on the race track."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high

- [RC-02] CLAIM: Estimation is a binding term that Swift patches with track knowledge: its VIO suffers "severe drift" at speed from motion blur, so the system corrects it with known-gate detections (Kalman filter on drift position and velocity) and fine-tunes the policy against a Gaussian-process odometry-drift model fitted to about 50 s of real flight. The same paper says earlier expert-level autonomous results "rely on near-perfect state estimation provided by an external motion-capture system".
  SOURCE: Kaufmann et al. 2023, Nature 620:982-987, doi:10.1038/s41586-023-06419-4 (published version, Europe PMC)
  QUOTE: "However, these works rely on near-perfect state estimation provided by an external motion-capture system. This makes the comparison with human pilots unfair, as humans only have access to onboard observations from the drone." ; "Navigating at high speeds results in substantial motion blur, which can lead to a loss of tracked visual features and severe drift in linear odometry estimates." ; "The odometry estimates from the VIO pipeline 54 exhibit substantial drift during high-speed flight."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high

- [RC-03] CLAIM: Human-gap critique from the same paper: Swift (same weight, shape and propulsion as the humans' drones) is faster overall but not on every segment; it is faster at the start (about 120 ms earlier take-off) and in tight turns such as the split-S, and the authors' hypothesis is that it "optimizes trajectories on a longer timescale" than humans, i.e. a planning/policy effect, not hardware. Humans adapt lap by lap (slow down when leading), Swift is unaware of its opponent; Swift's lap times have lower mean and variance. Per-lap speed or win rate here says nothing about the fraction of the platform's own time-optimal time.
  SOURCE: Kaufmann et al. 2023, Nature 620:982-987, doi:10.1038/s41586-023-06419-4 (published version, Europe PMC)
  QUOTE: "Although Swift is globally faster than all human pilots, it is not faster on all individual segments of the track (Extended Data Table 1 ). Swift is consistently faster at the start and in tight turns such as the split S." ; "The quadrotors used by Swift and by the human pilots have the same weight, shape and propulsion."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high

- [RC-04] CLAIM: Song et al. argue the binding term at the platform limit is model mismatch (aerodynamic effects, variable system delay, battery-voltage fluctuation) interacting with controller structure, not the optimiser and not the nominal thrust limit. Lap times and success (simulation, nominal model): trajectory-tracking MPC 4.92 +/- 0.10 s at 44 %; contouring control 5.03 +/- 0.18 s at 76 %; RL 5.14 +/- 0.09 s at 100 %. Realistic model: 0 %, 5.34 +/- 0.27 s at 20 %, 5.26 +/- 0.32 s at 100 %. Real world: trajectory tracking 0 % (crash at full thrust), contouring 5.54 +/- 0.21 s at 50 %, RL 5.35 +/- 0.15 s at 85 %. Trial counts are not in the text I extracted; the text I extracted does not say whether real-world state came from motion capture (grep for "motion capture", "Vicon", "onboard" found nothing relevant), so treat this as evidence about the controller, not about the onboard-only metric.
  SOURCE: Song, Romero, Mueller, Koltun, Scaramuzza 2023, Reaching the limit in autonomous racing: Optimal control versus reinforcement learning, Science Robotics 8(82), arXiv:2310.10943 (arXiv preprint of doi:10.1126/scirobotics.adg1462)
  QUOTE: "Real-world testing introduces additional factors that are not present in the simulation, including aerodynamic effects, variable sys- tem delay, and large battery voltage fluctuations. As a result, both OC methods fail in this setting." ; table row "Real World – 0.0 5.54± 0.21 50.0 5.35± 0.15 85.0"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: medium

- [RC-05] CLAIM: Same paper, mechanism critique: with an identical tracking objective RL does not beat MPC; RL wins because it optimises the task-level gate-progress objective directly and uses domain randomisation. So the nominal-model optimum (4.92 s in simulation, 44 % success) is a reference no hardware controller reached; the hardware result (5.35 s, 85 %) is about 9 % slower than that simulated optimum at lower reliability, a robustness-versus-speed trade rather than evidence of an actuator limit. The ratio is my arithmetic from the table values and is not a time-optimal-fraction measurement (the 4.92 s is a tracked time-optimal trajectory in simulation).
  SOURCE: Song et al. 2023, Science Robotics 8(82), arXiv:2310.10943
  QUOTE: "Our results indicate that RL does not outperform OC because RL optimizes its objective better. Rather, RL outperforms OC because it optimizes a better objective." ; "RL cannot find better solutions than OC given the same optimization objective."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: simulation
  CONFIDENCE: high

- [RC-06] CLAIM: NeuroBEM argues aerodynamics is the dominant model defect above low speed: data flown up to 65 km/h in a motion-capture arena; a hybrid blade-element-momentum plus neural residual model cuts positional RMSE when replaying flown trajectories in simulation from about 0.8 m (prior art) to below 0.3 m, and cuts force/torque prediction error by 50 %. This is a model-error result in simulation (with a known controller), not a speed gain on hardware, and the data are motion-capture based.
  SOURCE: Bauersfeld, Kaufmann, Foehn, Sun, Scaramuzza 2021, NeuroBEM: Hybrid Aerodynamic Quadrotor Model, RSS XVII, arXiv:2106.08015
  QUOTE: "Aerodynamic effects, while insigniﬁcant at low speeds, become the dominant model defect during high speeds or agile maneuvers." ; "reducing positional RMSE from ∼0.8 m for state-of-the-art approaches, down to below 0.3 m."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: simulation
  CONFIDENCE: high

- [RC-07] CLAIM: The Hanover et al. survey names two pipeline failure modes that make a plan-then-track system fail outright: unmodelled delays and VIO drift or jumps cause "compound errors"; and successful onboard racing systems reduce VIO drift by localising against a pre-known gate map, which ties onboard speed results to prior knowledge of the course.
  SOURCE: Hanover et al. 2024, Autonomous Drone Racing: A Survey, IEEE T-RO 40:3044-3067, arXiv:2301.01755
  QUOTE: "Unexpected deviations from the plan, be it in the time domain (like unmodeled system delays) or in the state-space domain (like state estimation drifts or jumps in the VIO pipeline), can lead to compound errors and ultimately, a complete system failure." ; "In drone racing competitions, a map of the track in the form of gate positions is known beforehand."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high

- [RC-08] CLAIM: Loquercio et al. (onboard sensing and compute, simulation-trained depth policy; unseen natural and urban obstacle fields; a straight 40 m reference line that collides with obstacles, so success is collision-free completion, not a gate course): no crash at 3 and 5 m/s; 7 m/s completed 8 of 10; at 10 m/s 60 % success in the forest while the paper also states "an average success rate of 70% at 10 m s-1" across environments (two figures in one paper). The authors attribute the 7 m/s failures to perception (late field-of-view entry) and the 10 m/s degradation to aerodynamics, battery sag and motion blur: the binding term changes along the speed axis. A 19-run set covered 3-7 m/s in a second environment. Baselines (mapping-plus-planning; reactive) already fail to complete all runs at 5 m/s.
  SOURCE: Loquercio, Kaufmann, Ranftl, Mueller, Koltun, Scaramuzza 2021, Learning high-speed flight in the wild, Science Robotics 6, doi:10.1126/scirobotics.abg5810 (arXiv preprint 2110.05113, latest version)
  QUOTE: "Given the good performance at 7 m s−1, we push the average ﬂight speed even higher to 10 m s−1. At this speed, external disturbances, e.g. aerodynamics, battery power drops, and motion-blur start to play an important role and widen the simulation to reality gap. Nonetheless, we achieve a success rate of 60%" ; "The two failures happened when objects entered the ﬁeld of view very late because of the high angular velocity of the platform."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high

- [RC-09] CLAIM: Loquercio et al. name the coupling of fast perception with planning as the limit for unknown environments, and cite Falanga et al.'s point-mass bound on forward speed as a function of perception latency and sensing range, extending it with rotational-dynamics latency. The point-mass origin is a critique target: it "neglects the platform's rotational dynamics". The Falanga et al. paper itself (RA-L 4:1884-1891, doi:10.1109/lra.2019.2898117) I could not open.
  SOURCE: Loquercio et al. 2021, Science Robotics 6 (arXiv:2110.05113)
  QUOTE: "The limiting factor for autonomous agile ﬂight in arbitrary unknown environments is the coupling of fast and robust perception with effective planning." ; "the authors derived an upper-bound for the forward speed at which a robot can ﬂy and avoid a single obstacle as a function of perception latency and sensing range. They modeled the robot as a point-mass, which is a limited approximation for a quadrotor as it neglects the platform’s rotational dynamics."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high

- [RC-10] CLAIM: Critique of the champion-level claim from the TU Delft group: the champion-level systems are specialised modular pipelines whose performance "depends on accurately mapped track layouts, rectangular gates of known size, precise camera calibration, and hand-tuned" EKFs; SkyDreamer (their own end-to-end alternative) is likewise defined as maximising lap speed "around a pre-mapped track", so it is not an unseen-course result either. Their abstract (lit_search) says no system had combined full sim-to-real transfer, onboard execution and champion-level performance.
  SOURCE: Verraest et al. 2025, SkyDreamer: Interpretable End-to-End Vision-Based Drone Racing with Model-Based Reinforcement Learning, arXiv:2510.14783
  QUOTE: "Their performance further depends on accurately mapped track layouts, rectangular gates of known size, precise camera calibration, and hand-tuned extended Kalman filters (EKFs)." ; "the goal is to maximize the quadcopter's lap speed around a pre-mapped track marked by gates"
  ACCESS: full-text
  STATUS: preprint
  SETTING: hardware
  CONFIDENCE: medium

- [RC-11] CLAIM: Dream to Fly (Romero et al., ICRA 2026) is a partial sim-to-real result: the pixel-to-command policy was validated hardware-in-the-loop only (simulator-rendered images fed to the network, real drone dynamics in the loop); "additional challenges remain to transfer to real camera pixel observations"; training takes about 240 h. Perception sim-to-real, not dynamics transfer, was the unresolved term there.
  SOURCE: Romero et al. 2025/2026, Dream to Fly: Model-Based Reinforcement Learning for Vision-Based Drone Flight, ICRA 2026, doi:10.1109/ICRA57385.2026.11695931, arXiv:2501.14377
  QUOTE: "While this confirms the policy's effectiveness on the real quadrotor dynamics, additional challenges remain to transfer to real camera pixel observations. Additionally, the training process is computationally intensive, requiring approximately 240 hours to converge."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high

- [RC-12] CLAIM: In AlphaPilot 2019 (onboard vision; gate map known at the event) the camera-plus-VIO chain added state-estimation latency "in the order of 130 ms", handled by IMU forward prediction; VIO ran at about 35 Hz and gate detection at 60 Hz. The planner models the vehicle as a point mass with bounded acceleration and offers a velocity cap "to limit the motion blur of the camera images" (the paper's example in Fig. 5 uses +/-7.5 m/s and +/-12 m/s^2, about 1.2 g; these are illustrative, not necessarily the race settings). Evidence that designers capped speed for perception reasons rather than thrust-to-weight.
  SOURCE: Foehn et al. 2020, AlphaPilot: Autonomous Drone Racing, RSS XVI, arXiv:2005.12813
  QUOTE: "interfacing the cameras and running VIO, introduces latency in the order of 130 ms to the system." ; "to limit the motion blur of the camera images, a velocity constraint of the form vB ≤ vB(t)≤ vB can be added" ; "The velocities are constrained to ±7.5m/s and the inputs to ±12m/s2."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: medium

- [RC-13] CLAIM: Foehn et al.'s time-optimal result is a platform-optimum and controller result in motion capture: the CPC time-optimal trajectory was "executed in a motion capture system, outperforming the best human expert". The paper states expert pilots fly "at speeds so far unreached by any autonomous system". Earlier time-optimal planners limited collective thrust and body rates "rather than the actual constraint of limited single rotor thrusts", so the published platform-optimum depends on the actuator model used; a denominator for the brief's metric taken from a collective-thrust model would be wrong.
  SOURCE: Foehn, Romero, Scaramuzza 2021, Time-optimal planning for quadrotor waypoint flight, Science Robotics 6, doi:10.1126/scirobotics.abh1221 (arXiv preprint 2108.04537, latest version)
  QUOTE: "This time-optimal ﬂight path was computed using the proposed complementary progress constraints (CPC) and executed in a motion capture system, outperforming the best human expert." ; "expert human drone racing pilots accomplish this with astonishing performance, guiding their quadrotors through race tracks at speeds so far unreached by any autonomous system."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high

- [RC-14] CLAIM: The state-estimation-binds argument in its original form: Delmerico et al.'s UZH-FPV dataset (over 27 sequences, more than 10 km, FPV racing quadrotor with camera, IMU, event data and ground truth) was built because high-speed six-DoF trajectories remained challenging for state estimators; the project page states its goal "to help advance the state of the art in high-speed state estimation". A SplitS track with peak speeds up to 100 km/h was added in December 2023. I did not obtain per-algorithm failure rates.
  SOURCE: Delmerico et al. 2019, Are We Ready for Autonomous Drone Racing? The UZH-FPV Drone Racing Dataset, ICRA 2019; project page https://fpv.ifi.uzh.ch/
  SUMMARY: "The original paper says high-speed six-DoF trajectories remain challenging for existing estimation algorithms ... Their stated aim is a dataset that is beyond the capabilities of existing state estimation algorithms ... The project page notes a SplitS track added in December 2023 with peak speeds up to 100 km/h." (WebSearch summary). The project page text printed by fetch_text.py reads: "our goal is to help advance the state of the art in high-speed state estimation."
  ACCESS: search-summary
  STATUS: peer-reviewed
  SETTING: n/a
  ARTIFACT: dataset https://fpv.ifi.uzh.ch/
  CONFIDENCE: medium

- [RC-15] CLAIM: Generalisation critique (2026): reinforcement-learning racing policies reaching human-level performance "fail to generalize; policies trained on specific environments often crash immediately in unseen configurations". The same authors' real-world deployment used a VICON motion-capture system for state and a workstation for policy inference with commands transmitted to the quadrotor, so their flights are not onboard-only. Evidence that "unseen" results are the weak point, and a labelled off-board example.
  SOURCE: Green et al. 2026, Bridging Performance and Generalization in Reinforcement Learning for Agile Flight, arXiv:2606.27348
  QUOTE: "While reinforcement learning (RL) has achieved human-level performance in this domain, current methods fail to generalize; policies trained on specific environments often crash immediately in unseen configurations." ; "For real-world deployment of the state-based model, a VICON motion capture system is used for state estimation. Inference on the control policy network is performed on a workstation and trans- mitted to the quadrotor"
  ACCESS: full-text
  STATUS: preprint
  SETTING: hardware
  CONFIDENCE: medium

- [RC-16] CLAIM: A second 2026 preprint makes the same point from the model-based side: approaches using precomputed reference trajectories or explicit 6-DoF gate pose estimation are "brittle to spatial perturbations, unmodeled track changes, and sensor noise", while end-to-end learned policies "frequently overfit to specific track layouts and struggle with zero-shot generalization".
  SOURCE: Zhao et al. 2026, Vision-Guided MPPI for Agile Drone Racing: Navigating Arbitrary Gate Poses via Neural Signed Distance Fields, arXiv:2603.07199
  QUOTE: "However, recent approaches typically rely on precom- puted spatial reference trajectories or explicit 6-DoF gate pose estimation, rendering them brittle to spatial perturbations, unmodeled track changes, and sensor noise. Conversely, end- to-end learning policies frequently overfit to specific track layouts and struggle with zero-shot generalization."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium

- [RC-17] CLAIM: Competition evidence is organiser-reported and thin: at the 2025 Abu Dhabi A2RL drone race (12 April 2025, 14 qualified teams, onboard autonomy required), an AI team (MAVLAB, TU Delft) won the "AI vs Human Challenge"; a press-release figure is two laps of a 170 m course in 17 s (average about 20 m/s if the lap length equals the course length, my arithmetic, not stated by the source). No human lap times or success rates over repeated unseen courses were disclosed, so it does not meet the brief's metric.
  SOURCE: Wikipedia, 2025 Abu Dhabi Autonomous Racing League (podium table, fetched), plus WAM press coverage found by WebSearch
  SUMMARY: "Team MavLab's AI drone outpaced a world-leading human pilot to win the AI vs Human Challenge ... MavLab's AI Grand Challenge run ... completing two laps of the 170-metre course in just 17 seconds ... Teams had to rely entirely on onboard autonomy during the race." (WebSearch summary; podium table confirmed by fetch_text.py)
  ACCESS: search-summary
  STATUS: secondary
  SETTING: hardware
  CONFIDENCE: low

## Gaps
- Falanga, Kim, Scaramuzza 2019 (doi:10.1109/lra.2019.2898117): the latency/sensing-range speed bound; open copies were bot-check or stub pages. Only the description in Loquercio 2021 is quoted.
  PAPER TO REQUEST: 10.1109/lra.2019.2898117 | How Fast Is Too Fast? The Role of Perception Latency in High-Speed Sense and Avoid | the exact bound v_max(latency, range, a_max) and its stated assumptions, to set against the usable perception range.
- Delmerico et al. 2019 (UZH-FPV): per-algorithm VIO failure rates at racing speed not obtained.
  PAPER TO REQUEST: 10.1109/ICRA.2019.8793887 | Are We Ready for Autonomous Drone Racing? The UZH-FPV Drone Racing Dataset | how far state-of-the-art VIO is from racing speeds, an estimation-binds sensitivity. (DOI not verified by me; look it up before requesting.)
- Song et al. 2023: trial counts and whether the real-world flights used motion capture were not found in the extracted arXiv text; check the published supplement.
- Not found: a controlled sensitivity study that relaxes each limit (actuator bandwidth, estimation latency, aerodynamic error, perception range) one at a time on a racing-class quadrotor. Closest are Song 2023 (model mismatch, RC-04) and Loquercio 2021 (latency and range analysis, RC-09). The brief's elasticity must come from the simulator lens.
- Not found: a paper arguing actuator (motor/rotor) bandwidth is the binding limit for onboard-only agility; one query on motor dynamics returned nothing. The only actuator-side evidence in my sources is indirect (the single-rotor thrust constraint in RC-13 and variable delay in RC-04).
- Not found: a published critique that Swift's comparison with humans is confounded by training, beyond the paper's own caveats (RC-01, RC-03); and a primary technical report for the A2RL results (RC-17).
- Semantic Scholar rate-limited throughout, so citing-paper lookups for rebuttals (refersto queries) were not completed; INSPIRE does not index this literature.
