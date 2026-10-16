# Research: engineering
status: final
Mandate: what has actually been flown (platform, speed, success rate, trials, onboard vs off-board, seen vs unseen course), released artefacts, and platforms/sensors/compute arriving next.
Access: lit_search INSPIRE not used (robotics), Crossref ok, Semantic Scholar rate-limited at times; WebFetch domains that worked: see claims

## Claims
- [RE-01] CLAIM: Swift (Kaufmann et al., UZH, 2023) raced a 75 m lap of seven square gates (30 x 30 x 8 m volume) fully onboard and won 5 of 9 races vs A. Vanover, 4 of 7 vs T. Bitmatta, 6 of 9 vs M. Schaepper (15 wins of 25 head-to-head races; 10 losses, of which 40% opponent collision, 40% gate collision, 20% simply slower). The track layout was fixed and known, and Swift's dynamics/perception residual models were fitted on that track, so this is performance on a seen course, not the brief's unseen-course metric. The brief's 90% success criterion is not reported in this form (race wins, not completion rate).
  SOURCE: Kaufmann et al. 2023, Champion-level drone racing using deep reinforcement learning, Nature 620, 982-987, doi:10.1038/s41586-023-06419-4 (published version, Europe PMC PMC10468397)
  QUOTE: "As shown in Fig. 3b , Swift wins 5 out of 9 races against A. Vanover, 4 out of 7 races against T. Bitmatta and 6 out of 9 races against M. Schaepper. Out of the 10 losses recorded for Swift, 40% were because of a collision with the opponent, 40% because of collision with a gate and 20% because of the drone being slower than the human pilot."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  ARTIFACT: code (pseudocode only) https://doi.org/10.5281/zenodo.7955278 (Zenodo; racing_data.zip with motion-capture recordings and analysis code, plus pseudocode.zip)
  CONFIDENCE: high
- [RE-02] CLAIM: Swift's perception/compute chain was fully onboard: Intel RealSense T265 VIO at 100 Hz, a gate-detection U-Net taking 40 ms per forward pass on a Jetson TX2 (FP16, 384 x 384 input), racing policy 8 ms per inference on the CPU, outputting collective thrust and body rates to a commercial STM32 (216 MHz) flight controller. The vehicle weighs 870 g with ~35 N max static thrust (static thrust-to-weight 4.1), T-Motor Velox 2306 motors, 5-inch three-blade props, Agilicious-based. Motion capture was used only to collect training residual data, not in the racing loop.
  SOURCE: Kaufmann et al. 2023, Nature 620, 982-987, doi:10.1038/s41586-023-06419-4 (published version, Europe PMC)
  QUOTE: "Each vehicle has a weight of 870 g and can produce a maximum static thrust of approximately 35 N, which results in a static thrust-to-weight ratio of 4.1." and "the racing policy is evaluated on the CPU, with one inference pass taking 8 ms. The autonomous drones carry an Intel RealSense Tracking Camera T265 that provides VIO estimates 59 at 100 Hz" and "One forward pass through the network takes 40 ms on the NVIDIA Jetson TX2."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high
- [RE-03] CLAIM: The Swift authors themselves state a sensorimotor-latency comparison and a camera-rate disadvantage: Swift 40 ms vs 220 ms average for expert human pilots, but a 30 Hz gate-camera vs 120 Hz FPV camera for the pilots. VIO drift during high-speed flight was substantial enough that it was corrected by gate detection plus a Kalman filter; the authors state the pose estimates "exhibit substantial drift during high-speed flight". Swift also benefited from the track-specific fit: "the human pilots are given a week of practice on the same track".
  SOURCE: Kaufmann et al. 2023, Nature 620, 982-987, doi:10.1038/s41586-023-06419-4 (published version, Europe PMC)
  QUOTE: "our system benefits from lower sensorimotor latency (40 ms for Swift versus an average of 220 ms for expert human pilots 39 ). On the other hand, the limited refresh rate of the camera used by Swift (30 Hz) can be considered a structural advantage for human pilots, whose cameras' refresh rate is four times as fast (120 Hz)" and "The odometry estimates from the VIO pipeline 54 exhibit substantial drift during high-speed flight."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high
- [RE-04] CLAIM: Before Swift, autonomous racing results that reached expert-pilot lap times relied on motion capture; the Swift paper says prior results at human level used external state estimation and the earlier onboard AlphaPilot (2019) teams took almost twice as long as a professional pilot. This separates mocap-based controller evidence from onboard evidence (brief premise 5).
  SOURCE: Kaufmann et al. 2023, Nature 620, 982-987 (published version, Europe PMC)
  QUOTE: "the first two teams still took almost twice as long as a professional human pilot to complete the track 26 , 27 . More recently, autonomous systems have begun to reach expert human performance 28 – 30 . However, these works rely on near-perfect state estimation provided by an external motion-capture system."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high
- [RE-05] CLAIM: Loquercio et al. (UZH/Intel, 2021) flew a depth-image-to-trajectory learned policy fully onboard (Jetson TX2, RealSense D435 stereo depth + T265 state estimate; 890 g, ~40 N max thrust, T/W 4.4, 5-inch props) through forests, hangars, collapsed buildings and a derailed train, never seen in training (policy trained in simulation only). 56 real experiments in total; success was reported as reaching a goal within 5 m without crashing, and the authors say it "was always able to achieve the goal when not colliding into an obstacle". At the highest speed pushed, average 10 m/s, the success rate was 60%, with failures near openings under 1 m wide; the authors attribute the widened sim-to-real gap at 10 m/s to aerodynamics, battery power drops and motion blur. This is the best onboard unseen-environment evidence (obstacle avoidance to a goal, not a gate sequence), 5 to 7 m/s with success near 100% in their reported sets and 10 m/s with 60%; per-speed trial counts are in the paper's Fig. 3 (not extracted here).
  SOURCE: Loquercio et al. 2021, Learning high-speed flight in the wild, Science Robotics 6(59), eabg5810, doi:10.1126/scirobotics.abg5810 (arXiv preprint 2110.05113 of the published paper)
  QUOTE: "Given the good performance at 7 m s−1, we push the average flight speed even higher to 10 m s−1. At this speed, external disturbances, e.g. aerodynamics, battery power drops, and motion-blur start to play an important role and widen the simulation to reality gap. Nonetheless, we achieve a success rate of 60%, with failures mainly happening in the proximity of narrow openings less than a meter wide, where a single wrong action results in a crash."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  ARTIFACT: code https://github.com/uzh-rpg/agile_autonomy ; video (see paper Movie S1)
  CONFIDENCE: medium
- [RE-06] CLAIM: In the same paper's simulation-only controlled experiment (a 1.5 m diameter pole 6 m ahead, 3 to 13 m/s, 10 runs per speed per method), the authors compute a theoretical maximum speed set by sensing range, camera latency (inverse frame rate) and processing latency; processing latency differs by method (FastPlanner mapping pipeline 65.2 ms per frame on the Jetson TX2, higher than the learned policy), so the speed at which each method fails tracks its latency. This is a simulation result (Flightmare/RotorS), separate from the 10 m/s hardware result in RE-05.
  SOURCE: Loquercio et al. 2021, Science Robotics 6(59), eabg5810 (arXiv preprint 2110.05113)
  QUOTE: "The maximum speed depends on the sensing range, i.e. how far can an obstacle be accurately perceived, the latency of the visual sensor, i.e. the inverse of the frame rate, and the processing latency, i.e. the time to convert an observation into motor commands." and "With a total computation time of 65.2 ms per frame, FastPlanner incurs the highest processing latency."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: simulation
  ARTIFACT: code https://github.com/uzh-rpg/agile_autonomy
  CONFIDENCE: medium
- [RE-07] CLAIM: Song et al. (UZH, 2023) flew an RL policy on a 0.52 kg racing drone with 63 N maximum thrust (fully charged battery; thrust-to-weight about 12) and reached a peak speed of 108 km/h (30 m/s) and peak acceleration above 12 g on two human-designed tracks in an indoor arena. This was NOT onboard-only: state came from a Vicon motion-capture system plus an Extended Kalman Filter, and the policy ran at 100 Hz feedback. It is evidence about the controller and the thrust ceiling, not about the onboard-only metric; the course was a track the policy was trained on.
  SOURCE: Song, Romero, Müller, Koltun, Scaramuzza 2023, Reaching the limit in autonomous racing: Optimal control versus reinforcement learning, Science Robotics 8(82), doi:10.1126/scirobotics.adg1462 (arXiv preprint 2310.10943 of the published paper)
  QUOTE: "Our RL policy achieves a peak speed of 108 km/h and a peak acceleration greater than 12 g in an indoor flying arena." and "weight of only 0.52 kg and can generate a maximum thrust of 63 N (given a fully charged battery)... We use a Vicon motion capture system together with an Extended Kalman Filter to estimate the quadrotor state, including position, velocity, and orientation."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  ARTIFACT: video (Movie 1 of the paper); code https://github.com/uzh-rpg/drone_racing_rl (not checked)
  CONFIDENCE: high
- [RE-08] CLAIM: In the same paper the model-sensitivity of optimal-control (OC) racing is quantified. Lap times and success rates (as printed in the paper's Fig. 2C): nominal model, Trajectory Tracking 4.92 +- 0.10 s / 44.0%, Contouring Control 5.03 +- 0.18 s / 76.0%, RL 5.14 +- 0.09 s / 100.0%; realistic drone model, Trajectory Tracking no completion / 0.0%, Contouring 5.34 +- 0.27 s / 20.0%, RL 5.26 +- 0.32 s / 100.0%; real world (mocap), Trajectory Tracking no completion / 0.0%, Contouring 5.54 +- 0.21 s / 50.0%, RL 5.35 +- 0.15 s / 85.0%. Trial counts are not stated in the extracted table. Reading: a 4.92 s nominal-model time-optimal tracking lap is the closest published figure to the platform's own optimum on that track (so the RL real-world lap is about 92% as fast, ratio 4.92/5.35, derived here from two numbers measured in different settings, not quoted), and the only controller that kept at least 85% success in the real world was the one that tolerates model error. The unmodelled-dynamics effect is therefore a model-error result: it is large for controllers that track a precomputed optimal trajectory (success falls from 44% to 0%) and small for RL (100% to 85%).
  SOURCE: Song et al. 2023, Science Robotics 8(82), doi:10.1126/scirobotics.adg1462 (arXiv preprint 2310.10943)
  QUOTE: "Nominal 4.92± 0.10 44.0 5.03± 0.18 76.0 5.14± 0.09 100.0 Realistic – 0.0 5.34± 0.27 20.0 5.26± 0.32 100.0 Real World – 0.0 5.54± 0.21 50.0 5.35± 0.15 85.0"
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware (real-world row, with motion capture) and simulation (nominal and realistic rows)
  CONFIDENCE: medium
- [RE-09] CLAIM: Agilicious (Foehn et al., UZH, 2022) is an open-hardware/open-software quadrotor platform: 750 g, maximal speed 131 km/h, onboard NVIDIA Jetson TX2 with GPU, real-time flight controller, supports model-based and neural-network controllers. The platform paper's own latency experiment shows off-board computation degrades tracking markedly because of added latency, referenced against a motor time constant of 39.1 ms. Its VIO tests (Intel T265 and a second VIO) were flown on a 4 m radius circle at 5 m/s and a lemniscate up to 7 m/s (the 131 km/h figure is a maximum, not an onboard-VIO speed; the VIO accuracy tests run at 5 to 7 m/s).
  SOURCE: Foehn et al. 2022, Agilicious: Open-source and open-hardware agile quadrotor for vision-based flight, Science Robotics 7(67), doi:10.1126/scirobotics.abl6259 (arXiv preprint 2307.06100)
  QUOTE: "The design objectives resulted in creating a lightweight 750 g platform with maximal speed of 131 km/h." and "offloading computation from the drone and controlling it remotely significantly impacts performance. This is due to the massively increased latency, depicted in Figure C, where, for reference, the motor time constant of 39.1 ms is marked as a dashed line" and "a circle trajectory with radius of 4 m at a speed of 5 m/s, and a Lemniscate trajectory with an amplitude of 5 m at a speed of up to 7 m/s."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  ARTIFACT: code https://github.com/uzh-rpg/agilicious (hardware and software; not opened this run)
  CONFIDENCE: medium
- [RE-10] CLAIM: MonoRace (TU Delft MAVLab, A2RL x DCL, Abu Dhabi, 11-12 April 2025) is the strongest onboard-only demonstration to date with a minimal sensor set: one monocular rolling-shutter camera (155 x 115 deg field of view, 820 x 616 px at 90 Hz, adaptively cropped to 384 x 384) plus an IMU (accelerometer 1000 Hz, gyro 2000 Hz) on a Jetson Orin NX; GateNet segmentation feeds a delay-compensated Kalman filter, and a small 3 x 64 neuron guidance-and-control network runs at 500 Hz on the flight controller and outputs motor commands directly (no inner attitude loop). Track: 11 square gates (1.5 m inner opening) in a 100 x 30 m indoor hall, two laps timed. Fastest completion time 16.56 s; the paper reports speeds up to 100 km/h (27.8 m/s) and beat three human FPV world champions in a three-round knockout. The organizers supplied identical drone hardware, banned external localisation and banned modification or precision measurement of the track; but teams practised on the track over the event and trained policies against it, so this is a seen-course result, not the brief's unseen-course metric. This arXiv version is a preprint (v1, 21 Jan 2026) of the Science Robotics 2026 paper doi:10.1126/scirobotics.aee9250; numbers should be re-checked against the published version.
  SOURCE: Bahnam et al. 2026, MonoRace: Winning Champion-Level Drone Racing with Robust Monocular AI, arXiv:2601.15222 (published as Science Robotics 11, doi:10.1126/scirobotics.aee9250)
  QUOTE: "The proposed approach won the 2025 Abu Dhabi Autonomous Drone Racing Competition (A2RL), outperforming all competing AI teams and three human world champion pilots in a direct knockout tournament. It set a new milestone in autonomous drone racing research, reaching speeds up to 100 km/h on the competition track" and "Our controller achieved the fastest completion time of 16.56 s, outperforming three world champion- level FPV pilots." and "All computation is performed onboard, using an NVIDIA Jetson Orin NX as the main processing unit."
  ACCESS: full-text
  STATUS: preprint (journal version exists)
  SETTING: hardware
  ARTIFACT: none found (code not located this run)
  CONFIDENCE: medium
- [RE-11] CLAIM: MonoRace states an explicit speed-versus-reliability trade-off across its 17+ deployed policies on hardware: the most reliable network (M23, 23 s class) completed 43 flights with an 88.4% success rate (most mishaps development- or hardware-related), while the fastest policies (M16, M17) were more aggressive and less reliable; the paper does not give a success rate for the 16.56 s policy. In simulation (100 randomised rollouts per network, 30% parameter randomisation) all networks held about 90% success. So the brief's 90% success threshold is met on a seen course only by the slower policy, about 23 s versus 16.56 s for the fastest (a 1.39x lap-time penalty, derived here from the two quoted numbers).
  SOURCE: Bahnam et al. 2026, arXiv:2601.15222
  QUOTE: "Remarkably, our most reliable network M23, completed 43 flights with an 88.4% success rate, where most mishaps were development or hardware-related." and "more aggressive controllers consistently produced faster laps, whereas more conservative controllers prioritized safety and reliability."
  ACCESS: full-text
  STATUS: preprint
  SETTING: hardware (M23 flights) and simulation (100 rollouts per network)
  CONFIDENCE: medium
- [RE-12] CLAIM: MonoRace reports end-to-end latency-relevant numbers: motor commands output by the 500 Hz network "from 0-100% in 2 ms" (command-level full throttle authority, not rotor speed response); image-to-state delays handled by timestamp-aware fusion with pre-calibrated delays, with simulated image delay of 17 ms and IMU delay 0.5 ms in the software-in-the-loop tests; and a failure mode that is estimation, not actuation: the state estimator tolerates about 50% corrupted frames and IMU saturation, and the authors note that simulated crash rates were less predictive of real crashes because the simulator "does not accurately model vision-based state estimation errors that occasionally caused real-world crashes". This is direct evidence that on this platform, vision-based estimation errors are what limit reliability at the faster setting.
  SOURCE: Bahnam et al. 2026, arXiv:2601.15222
  QUOTE: "the controller operated at 500 Hz with full throttle authority, allowing the motor commands to change from 0-100% in 2 ms." and "Simulated crash rates, in contrast, were less predictive, as the simulator does not accurately model vision-based state estimation errors that occasionally caused real-world crashes."
  ACCESS: full-text
  STATUS: preprint
  SETTING: hardware
  CONFIDENCE: medium
- [RE-13] CLAIM: The A2RL x DCL competition's sensor rule is itself a statement about the task: teams may use only a single camera and a low-quality IMU, a set the organisers describe as mirroring human FPV pilots. A separate team (Azhari et al., Dec 2025) reports that this sensor limit makes the system "susceptible to drift from Visual-Inertial Odometry (VIO)". So in 2025-26 racing the estimation chain, not thrust, is named by the participants as the dominant engineering problem, in a regime of about 27 m/s peak.
  SOURCE: Azhari et al. 2025, Drift-Corrected Monocular VIO and Perception-Aware Planning for Autonomous Drone Racing, arXiv:2512.20475
  QUOTE: "The Abu Dhabi Autonomous Racing League(A2RL) x Drone Champions League competition(DCL) requires teams to perform high-speed autonomous drone racing using only a single camera and a low-quality inertial measurement unit -- a minimal sensor set that mirrors expert human drone racing pilots. This sensor limitation makes the system susceptible to drift from Visual-Inertial Odometry (VIO), particularl"
  ACCESS: abstract
  STATUS: preprint
  SETTING: hardware (competition)
  CONFIDENCE: medium
- [RE-14] CLAIM: The 2026 A2RL Drone Championship (21-22 January 2026, UMEX, Abu Dhabi) was reported by press release: TII Racing posted the fastest autonomous lap at 12.032 s in the "AI Speed Challenge" and MAVLAB 12.832 s; a human world FPV champion (MinChan Kim) narrowly beat TII Racing in a best-of-nine; sensors again limited to one forward monocular camera plus IMU. The 2026 lap format differs from 2025 (different track and metric), so the times are not comparable to RE-10. Press summary only; the publisher page timed out.
  SOURCE: Business Wire / Bernama press release, 26 Jan 2026, A2RL Drone Championship Sets the Pace for AI in Autonomous Flight, https://www.businesswire.com/news/home/20260126735530/en/A2RL-Drone-Championship-Sets-the-Pace-for-AI-in-Autonomous-Flight
  SUMMARY: "TII Racing posted the fastest autonomous lap of the event, at 12.032 seconds in the AI Speed Challenge. MAVLAB was second at 12.832 seconds. Autonomous drones flew with a single forward-facing monocular camera and an inertial measurement unit, with no GPS, LiDAR or external positioning permitted." (WebSearch summary, not verbatim from page)
  ACCESS: search-summary
  STATUS: secondary
  SETTING: hardware
  CONFIDENCE: low
- [RE-15] CLAIM: Planned experiment: Anduril's AI Grand Prix (with Drone Champions League; all teams fly identical Neros drones, no hardware modification, human pilots banned): virtual qualifier roughly May to July 2026, in-person physical qualifier in September 2026 in Southern California (indoor, consistent lighting, obstacles and visual distractions), final "AI Grand Prix Ohio" planned for November 2026 (Columbus), prize pool reported at USD 500k. Whether teams must run compute onboard is not stated in what I could read; the official FAQ page lists the schedule. Results not available as of 15 Oct 2026; the final is about a month away.
  SOURCE: theaigrandprix.com FAQ, https://theaigrandprix.com ; press coverage https://dronelife.com/2026/01/28/anduril-launches-500k-drone-racing-ai-grand-prix
  QUOTE: "The virtual qualification phase runs May – July, with a cutoff for Round 2 targeted around the end of July (approx.). Selected teams will be invited to an in-person physical qualifier in September 2026 in Southern California. The final event – the AI Grand Prix Ohio – is planned for November."
  ACCESS: full-text
  STATUS: preliminary
  SETTING: n/a (planned)
  CONFIDENCE: medium
- [RE-16] CLAIM: Hardware, onboard-only, unseen-obstacle racing (SJTU/TU Delft group, arXiv Feb 2026): a Raspberry Pi plus Intel D435i depth camera quadrotor flew random-obstacle racetracks in the real world at speeds up to 8 m/s, claimed 100% success in all obstacle-rich environments (hardware-in-the-loop up to 10 m/s); curriculum RL, one end-to-end network. Real-world trial counts per condition not extracted this run. Preprint, not yet independently reproduced; gate order/layout of the racetrack is fixed by the task, obstacles are random.
  SOURCE: SJTU-ViSYS team et al. 2026, vision-based curriculum RL for drone racing with unseen obstacles, arXiv:2602.24030
  QUOTE: "Validated through hardware-in-the-loop and real-world flights across three distinct racetracks, our method achieves speeds up to 10 m/s and 8 m/s respectively, with 100% success rates in all obstacle-rich environments."
  ACCESS: full-text
  STATUS: preprint
  SETTING: hardware (8 m/s) and hardware-in-the-loop (10 m/s)
  ARTIFACT: code https://github.com/SJTU-ViSYS-team/CRL-Drone-Racing
  CONFIDENCE: low
- [RE-17] CLAIM: Hardware, onboard depth, perturbed unseen gate placement (ZJU, arXiv Mar 2026): Gate-SDF + MPPI controller tolerates random gate position (0.3 to 1.0 m) and yaw (30, 60 deg) perturbations using only onboard depth; in simulation it holds 100% success up to 10.0 m/s with no noise and 7.0 m/s at about 0.3 m position noise (90% at 8.0 m/s), but the real-world compact track gave a maximum of 5.3 m/s. The comparison table's baseline [26] reached 5.3 m/s at no noise (best environment). The sim-versus-hardware gap in speed (10.0 vs 5.3 m/s) is part of the evidence that these are different quantities.
  SOURCE: Zhao et al. 2026, Vision-Guided MPPI with Gate-SDF, arXiv:2603.07199
  QUOTE: "Notably, the quadrotor achieved a maximum flight speed of 5.3 m/s within this highly compact track, relying exclusively on onboard depth perception." and the table row "No Noise 100% 5.3 100% 10.0 Pos. Noise (∼0.3m) 100% 5.1 100% 7.0"
  ACCESS: full-text
  STATUS: preprint
  SETTING: hardware (5.3 m/s) and simulation (10.0 m/s table)
  ARTIFACT: video https://zhaofangguo.github.io/vision_guided_mppi/
  CONFIDENCE: low
- [RE-18] CLAIM: A caveat on all "generalisation" claims: a 2025-26 web survey (summary only) of learned racing policies describes them as tending to overfit the training track; sim-only generalisation to unseen cluttered environments is shown at up to 70 km/h (19.4 m/s), and the unseen-track hardware flights above are 5 to 8 m/s, i.e. a factor of 3 to 5 below the 27.8 m/s seen-track MonoRace figure and 30 m/s mocap figure. Treat as a lead, not a measurement.
  SOURCE: WebSearch summary of ICRA25 Wang (Environment as Policy), arXiv:2411.04246, 2602.24030, 2603.07199
  SUMMARY: "Domain randomization over track and obstacle configurations before each rollout produced policies that fly in unseen cluttered simulated environments at speeds up to 70 km/h. This is simulation-only." (model-written search summary)
  ACCESS: search-summary
  STATUS: secondary
  SETTING: simulation
  CONFIDENCE: low
- [RE-19] CLAIM: Time-optimal planning (Foehn et al., UZH, 2021) beat two professional human pilots on a 3D track in a roughly 25 x 30 x 8 m Vicon motion-capture arena, but the flight used motion capture for state, and the trajectory was generated "at a slightly lower thrust bound than what the platform can deliver" to keep controllability under disturbances, i.e. even the optimum-seeking planner ran inside a thrust margin. Human best runs each contained 7 laps and the humans trained for hours on the track. It is controller/planner evidence with an external reference, not the onboard metric; its significance here is that it gives the platform-optimum construction (the denominator in the brief's metric) and shows the deployed margin below the thrust limit.
  SOURCE: Foehn, Romero, Scaramuzza 2021, Time-optimal planning for quadrotor waypoint flight, Science Robotics 6(56), doi:10.1126/scirobotics.abh1221 (arXiv preprint 2108.04537)
  QUOTE: "We generate the trajectory at a slightly lower thrust bound than what the platform can deliver, to maintain controllability under disturbances as mentioned in Section A-D and discussed in Section IV-E."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware (motion capture)
  ARTIFACT: code https://github.com/uzh-rpg/rpg_time_optimal
  CONFIDENCE: high
- [RE-20] CLAIM: Event-camera flight is demonstrated onboard but slower than frame-camera racing: a monocular event-camera quadrotor avoided static obstacles (trees) purely onboard at 5 m/s, and the authors report that success improved with speed (1 m/s harder than 5 m/s) because event-based depth estimation improves with motion. A 2026 UZH follow-up (Messikommer et al.) addresses event-sim cost for training. No event-camera result at racing speeds (above 20 m/s) or on a gate sequence was found; event cameras are at the obstacle-avoidance demonstration stage at about 5 m/s.
  SOURCE: Bhattacharya et al. 2024, Monocular Event-Based Vision for Obstacle Avoidance with a Quadrotor, arXiv:2411.03303 (preprint)
  QUOTE: "High-speed (5m/s) real-world avoidance of trees with purely onboard computation, and demonstrating that avoidance using event-based vision improves as speed increases."
  ACCESS: full-text
  STATUS: preprint
  SETTING: hardware
  ARTIFACT: code and data stated as open-source in the paper (URL not extracted)
  CONFIDENCE: medium
- [RE-21] CLAIM: Lidar-based high-speed navigation reaches higher speed in unknown space than camera-only systems: SUPER (HKU, Science Robotics 2025, with a published erratum, doi:10.1126/scirobotics.adx3476) is reported by secondary press to exceed 20 m/s in unknown environments using a 3D LiDAR, with the published abstract stating the problem is vehicle weight, size and sensing for safe high-speed MAV navigation. A LiDAR is an admissible rangefinder only if it fits the brief's mass class; the quadrotor's mass and the speed/trials are not verified here. Full text was not reachable.
  SOURCE: Ren et al. 2025, Safety-assured high-speed navigation for MAVs, Science Robotics 10, doi:10.1126/scirobotics.ado6187
  QUOTE: "Micro air vehicles (MAVs) capable of high-speed autonomous navigation in unknown environments have the potential to improve applications like search and rescue and disaster relief, where timely and safe navigation is critical. However, achieving autonomous, safe, and high-speed MAV navigation faces systematic challenges, necessitating reduced vehicle weight and size for high-speed maneuvering, st"
  ACCESS: abstract
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: low
- [RE-22] CLAIM: Across the onboard-only demonstrations collected here, speeds sort by what the course is: (i) seen gate track, minimal sensors: about 27.8 m/s peak (MonoRace, 2025, single competition, 2-lap time 16.56 s, 88.4% success only for the slower M23 policy); (ii) seen gate track, stereo/VIO and gate detection: Swift, 75 m lap, wins 15 of 25 races versus champions (no peak speed extracted); (iii) unseen cluttered environments, depth camera, onboard: 7 m/s with success near 100% and 10 m/s with 60% (Loquercio 2021, 56 experiments), 8 m/s with 100% (SJTU 2026 preprint), 5.3 m/s on a compact perturbed-gate track (ZJU 2026 preprint). Mocap-state results reach 30 m/s peak (108 km/h) at 12 g. No hardware result found satisfies the brief's full definition (unseen gate sequence, at least 90% success over a stated number of trials, with the fraction of own time-optimal time reported); the nearest are (iii).
  SOURCE: synthesis of RE-01, RE-05, RE-07, RE-10, RE-11, RE-16, RE-17 (each with its own source)
  SUMMARY: "see cited claims; synthesis row, not a source quote" (this is the researcher's tabulation, not a source statement)
  ACCESS: search-summary
  STATUS: secondary
  SETTING: hardware
  CONFIDENCE: medium
## Gaps
- Swift's peak speed and acceleration (the Nature paper's extended data) were not extracted; the fraction of Swift's lap time relative to the platform's time-optimal lap was not found in the text I opened.
- MonoRace published Science Robotics version (doi:10.1126/scirobotics.aee9250) was not opened; numbers are from arXiv v1. MonoRace code or hardware mass/thrust-to-weight not found.
- A2RL 2026 result only via press summary; no paper found for the TII Racing 12.032 s run or the human-vs-AI best-of-nine details.
- SUPER (Science Robotics 2025): no free copy found; speed/mass/trial counts unverified. PAPER TO REQUEST: doi:10.1126/scirobotics.ado6187 | Safety-assured high-speed navigation for MAVs | would settle onboard sensing/mass class, speed, and trial count of the fastest unknown-environment hardware result, plus what the erratum doi:10.1126/scirobotics.adx3476 changed.
- Event-camera flight at racing speeds: none found. Neuromorphic or ASIC onboard compute on a >=200 g quadrotor in agile flight: none found; the Agilicious paper names Navion, Movidius and PULP as future directions only.
- Next-generation platforms with dates and target numbers (Agilicious successor, Jetson Orin-based platforms other than MonoRace) were not found beyond MonoRace's Orin NX; AI Grand Prix identical-drone (Neros) hardware specification and onboard-compute rule not found.
- Trial counts per speed for Loquercio 2021 (Fig. 3) and per-condition real-world counts for the SJTU and ZJU preprints were not extracted.
- Semantic Scholar was rate-limited for much of the run; coverage of 2025-26 conference papers (ICRA/IROS/CoRL) is incomplete.
