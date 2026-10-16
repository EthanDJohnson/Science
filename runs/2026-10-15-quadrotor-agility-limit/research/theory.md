# Research: theory
status: final
Mandate: control- and estimation-theoretic bounds (delay, RHP limits, actuator rate), differential flatness and time-optimal theory, perception-latency-to-speed relation, IMU+camera observability bounds.
Access: lit_search INSPIRE ok (nothing relevant: not a HEP topic), arXiv ok (short queries only), Crossref ok, Semantic Scholar rate-limited (HTTP 429); fetch_text worked on arxiv.org/pdf, rpg.ifi.uzh.ch, http://www.cds.caltech.edu (Astrom-Murray book; https:// failed on certificate, http:// worked); WebSearch ok

## Claims
- [RT-01] CLAIM: A quadrotor with linear rotor-drag effects is differentially flat in position and heading (proved), so the feed-forward thrust and body-rate (attitude) commands follow algebraically from a reference trajectory and its derivatives. Flatness is a property of the model with that drag form only; it says nothing about actuator limits or delay.
  SOURCE: Faessler, Franchi, Scaramuzza 2018, "Differential Flatness of Quadrotor Dynamics Subject to Rotor Drag for Accurate Tracking of High-Speed Trajectories", IEEE RA-L 3:620-626, arXiv:1712.02402
  QUOTE: "In this paper, we prove that the dynamical model of a quadrotor subject to linear rotor drag effects is differen- tially ﬂat in its position and heading. We use this property to compute feed-forward control terms directly from a reference trajectory to be tracked."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high

- [RT-02] CLAIM: For a point mass with bounded acceleration norm ||a|| <= a_max moving rest-to-rest, the time-optimal control is bang-bang: accelerate at a_max for t_opt/2, decelerate at a_max for t_opt/2 (closed form). A quadrotor is underactuated (thrust only along body z), so it must rotate to change the acceleration direction, and this bang-bang relation is only an approximation to its optimum.
  SOURCE: Foehn, Romero, Scaramuzza 2021, "Time-Optimal Planning for Quadrotor Waypoint Flight", Science Robotics 6(56), arXiv:2108.04537 (appendix A)
  QUOTE: "The time- optimal solution takes the form of a bang-bang trajectory over the time topt, accelerating with amax for topt/2, followed by decelerating with amax for topt/2." and "A quadrotor would exploit the same maximal acceleration by generating the maximum thrust. However, due to the quadrotor’s underactuation, it cannot instantaneously change the acceleration direction but needs to rotate by applying differential thrust over its rotors."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  ARTIFACT: code https://github.com/uzh-rpg/rpg_time_optimal
  CONFIDENCE: high

- [RT-03] CLAIM: Smooth polynomial (flatness-based, minimum-snap-type) trajectories are provably suboptimal in time because they touch the input limit only at isolated points. In the paper's rest-to-rest example (6 m, a_max-limited, simulation/analysis) the times are 2.165 s (9th order), 1.938 s (7th), 1.699 s (5th) versus 1.614 s for bang-bang with limited slope, i.e. a 5th-order polynomial is 5.3 per cent slower than bang-bang (ratio computed from the quoted times).
  SOURCE: Foehn et al. 2021, arXiv:2108.04537, Fig. 6 and Sec. 1
  QUOTE: "Fig. 6: Bang-bang and polynomial trajectories. Multiple orders of polynomial trajectories and one bang-bang trajectory with limited slope. The polynomial trajectories only touch the input extrema in two points, while the bang-bang spends more time at the limit and achieves a lower overall time."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: simulation
  CONFIDENCE: high

- [RT-04] CLAIM: The full-model time-optimal trajectory (rotor dynamics reduced to single-rotor thrust limits, rotational dynamics included) is only about 2 to 2.7 per cent slower than the earlier point-mass-like benchmarks that assumed collective-thrust and body-rate limits, on the paper's benchmark (simulation, 6 to 15 m straight-line cases, times 0.89 s to 1.93 s). So the platform's own time-optimal time is well approximated by a thrust-limited point-mass bound when body rates are not binding; the model-fidelity gap is small compared with the gap between autonomous and optimal flight (not computed here).
  SOURCE: Foehn et al. 2021, arXiv:2108.04537, Table III and appendix B
  QUOTE: "Note that our approach is 2.00% slower than [21] and 2.68% slower than [22], because it accounts for rotation dynamics and single rotor limits."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: simulation
  CONFIDENCE: medium

- [RT-05] CLAIM: Time-optimal quadrotor planning through multiple waypoints with single-rotor thrust constraints is a non-convex problem; solutions can be local optima (e.g. a solution performing a flip) unless initialised from a point-mass bang-bang guess. So "the platform's own optimum" is a numerically computed, not closed-form, quantity, and published optima are only certified optimal if the initialisation reaches the global basin.
  SOURCE: Foehn et al. 2021, arXiv:2108.04537, Sec. IV-D and appendix B-F
  QUOTE: "We can resolve this problem of local optimality by initializing the prob- lem from a bang-bang point-mass guess."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: simulation
  CONFIDENCE: medium

- [RT-06] CLAIM: Perception-latency-to-speed relation (analysis): for a robot modelled as a linear second-order system with bounded lateral acceleration, flying at constant forward speed toward an unknown obstacle of radius r first sensed at range s with total perception latency tau, the maximum safe forward speed is v_max = s / (tau + 2 sqrt(r / u2_max)) (Eq. 9 of the source; the extracted PDF text prints the root as a stacked fraction "2 sqrt(r / u2)"). Equivalent: tau_max = s/v - 2 sqrt(r/u2_max) (Eq. 8). Where the right side is negative the platform cannot avoid the obstacle at that speed whatever the latency; then more acceleration or longer sensing range is required. Scope: lateral dodge at constant longitudinal speed (the vehicle may not slow), single static obstacle, no estimation error; not a stop-before-obstacle bound, and not validated on an unseen multi-gate course.
  SOURCE: Falanga, Kim, Scaramuzza 2019, "How Fast is Too Fast? The Role of Perception Latency in High-Speed Sense and Avoid", IEEE RA-L, https://rpg.ifi.uzh.ch/docs/RAL19_Falanga.pdf
  QUOTE: "We can study (7) to compute the maximum latency ¯τ the system can tolerate such that the avoidance can still be performed safely: ¯τ = s ˆ v1 − 2 √ r ¯ u2 . (8)" and "¯ v1 = s τ + 2 √ r ¯ u2 . (9)" and "for some speeds ˆ v1 the robot is unable to perform the avoidance maneuver safely given its actuation capabilities and the sensing range of its sensor."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: medium (symbol layout reconstructed from PDF extraction; see calc file for a re-derivation)

- [RT-07] CLAIM: Time delay is a fundamental, non-removable limit on closed-loop speed: Astrom and Murray state that non-minimum-phase dynamics (time delays, RHP poles and zeros) "impose severe limits", and that delays "cannot generally be avoided by choice of sensor or actuator location" so must be removed by architecture (computing and communications design).
  SOURCE: Astrom and Murray, "Feedback Systems: An Introduction for Scientists and Engineers", 2nd ed. draft (24 Jul 2020), ch. 14 Fundamental Limits, pp. 465-469 of PDF, http://www.cds.caltech.edu/~murray/books/AM08/pdf/fbs-public_24Jul2020.pdf
  QUOTE: "Non-minimum phase dynamics, due to time de lays and right half- plane poles and zeros impose severe limits." and "elays cannot generally be avoided by cho ice of sensor or actuator location, and hence they should be avoided by prope r design of the system’s computing and communications architecture."
  ACCESS: full-text
  STATUS: textbook-or-review
  SETTING: analysis
  CONFIDENCE: high

- [RT-08] CLAIM: Right-half-plane zero bound (proved via the gain crossover frequency inequality): a RHP zero at s = z caps the gain crossover at omega_gc <= z tan(phi_ap/2); with an admissible all-pass phase lag phi_ap = pi/3 this is omega_gc < 0.6 z. Slow zeros limit more than fast ones. Relevance: it applies to a quadrotor only if the controlled output has a RHP zero (not the case for the flat output position with symmetric rotors to first order; this applicability is my reading, not a quoted statement).
  SOURCE: Astrom and Murray 2020 draft, Sec. 14.3, eq. (14.11)
  QUOTE: "The inequality (14.10) then gives the following bound on the crossover frequency: ωgc ≤z tan (ϕap/2). (14.11) With ϕap =π/3 we get ωgc < 0.6z. We can thus conclude that a right half-plane zero limits the achievable gain crossover frequency ωgc, and slow right half-plane zeros (z small) give lower crossover frequency than fast right half-plane zeros."
  ACCESS: full-text
  STATUS: textbook-or-review
  SETTING: analysis
  CONFIDENCE: high for the bound; medium for its (non-)applicability to quadrotors

- [RT-09] CLAIM: Bode's integral formula (waterbed effect): sensitivity cannot be made small over a wide frequency band; the area of log|S| above zero equals the area below (plus a term from RHP poles of the open loop, which makes the trade-off worse). So any added loop delay that forces a lower crossover raises the sensitivity peak elsewhere; disturbance rejection (e.g. unmodelled aerodynamics, treated as a disturbance) and noise amplification cannot both be improved freely.
  SOURCE: Astrom and Murray 2020 draft, Sec. 14.2, Theorem 14.3
  QUOTE: "There is an invariant (conserved qua ntity) called Bode’s integral formula that implies that reducing the sensitivity at one frequency increases it at another, and the situation is worse if the process has ri ght half-plane poles. Control design is thus always a compromise."
  ACCESS: full-text
  STATUS: textbook-or-review
  SETTING: analysis
  CONFIDENCE: high

- [RT-10] CLAIM: Large-signal limits from limited actuator rate and power are listed alongside delay and RHP dynamics as fundamental limits; the book treats rate saturation as a separate (nonlinear) limit from linear bandwidth limits.
  SOURCE: Astrom and Murray 2020 draft, ch. 14 intro
  QUOTE: "Large signal limits can be caused by limited rate and power of actuators, or by constraints required to pr otect the process."
  ACCESS: full-text
  STATUS: textbook-or-review
  SETTING: analysis
  CONFIDENCE: high

- [RT-11] CLAIM: Optimal-control versus learned-policy theory of the autonomy gap (hardware evidence, with caveats): Song et al. report that on a racing quadrotor an RL policy beat optimal-control (OC) pipelines and argue the cause is the objective, not the optimiser: OC "decomposes the problem into planning and control with an explicit intermediate representation, such as a trajectory", which limits the range of expressible policies. Peak acceleration >12 g and peak velocity 108 km/h are reported for the RL controller, a peak not an unseen-course average (different quantity from the brief's metric). Whether this study used motion capture is not checked here; leave to engineering facet.
  SOURCE: Song, Romero, Mueller, Koltun, Scaramuzza 2023, "Reaching the Limit in Autonomous Racing: Optimal Control versus Reinforcement Learning", Science Robotics, arXiv:2310.10943
  QUOTE: "Our study indicates that the fundamental advantage of RL over OC is not that it optimizes its objective better but that it optimizes a better objective. OC decomposes the problem into planning and control with an explicit intermediate representation, such as a trajectory, that serves as an interface."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: medium

- [RT-12] CLAIM: Estimation-theoretic bound (proved, nonlinear and linearised models): a visual-inertial system (IMU plus point-feature camera) has exactly four unobservable degrees of freedom, three global translations and one global rotation about the gravity vector (yaw). Roll, pitch, 3-D velocity and IMU biases are observable (Martinelli's result as cited), given sufficient excitation. Consequence: attitude and velocity do not need an external reference, but position and yaw drift unboundedly without loop closure or a map; observability states existence of information, not accuracy or latency, so it does not itself bound agility. Scope: point features, known IMU-camera calibration in the base result; excitation requirement (non-trivial accelerations) is an assumption.
  SOURCE: Hesch, Kottas, Bowman, Roumeliotis 2014, "Camera-IMU-based localization: Observability analysis and consistency improvement", Int. J. Robotics Research 33(1):182-201 (author-hosted PDF)
  QUOTE: "ability properties of both the nonlinear VINS model and its linearized counterpart to prove that they have four unob- servable DOF , corresponding to three-DOF global transla- tions and one-DOF global rotation about the gravity vector." and (citing Martinelli 2012) "the IMU biases, 3D velocity, and absolute roll and pitch angles are observ- able for VINS."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: analysis
  CONFIDENCE: high

- [RT-13] CLAIM: The four-unobservable-direction result survives full online self-calibration: with IMU intrinsics, camera intrinsics and IMU-camera spatial-temporal extrinsics (including time offset and rolling-shutter readout time) estimated, monocular VINS still has 4 unobservable directions (global yaw and translation) given fully excited 6-axis motion; special motions (e.g. planar, constant-acceleration) make calibration parameters unobservable. So camera-IMU time offset is observable only under excitation, a theory-level reason that a sensor-synchronisation latency can be estimated but not for free.
  SOURCE: Yang, Geneva, Zuo, Huang 2022, "Online Self-Calibration for Visual-Inertial Navigation Systems: Models, Analysis and Degeneracy", arXiv:2201.09170 (preprint; IEEE T-RO version not checked)
  QUOTE: "The analysis results prove that, as intuitively assumed in the literature, VINS with full sensor calibration has four unobservable directions, corresponding to the system’s global yaw and translation, while all sensor calibration parameters are observable given fully-excited 6-axis motion."
  ACCESS: full-text
  STATUS: preprint
  SETTING: analysis
  CONFIDENCE: medium

- [RT-14] CLAIM: Sampling and computation delay enter the loop as additive effective delay: a zero-order hold adds about half a sample period (T/2) of delay (phase lag omega*T/2), on top of sensing latency and computation time, so tau_eff = tau_sense + tau_compute + T/2 (+ actuator lag, treated as a further lag). The Astrom-Murray textbook quote for T/2 was not reached; the source here is course slides (secondary), the statement itself is standard sampled-data theory.
  SOURCE: Byl, ECE 147B lecture 2 slides, UC Santa Barbara, 2013, https://courses.ece.ucsb.edu/ECE147/147B_W13Byl/lecture/Lecture2_slides.pdf
  QUOTE: "ZOH Consequences in FREQUENCY DOMAIN • The PHASE LOSS due to half-­‐sample delay may DESTABILIZE the closed-­‐loop system!"
  ACCESS: full-text
  STATUS: secondary
  SETTING: analysis
  CONFIDENCE: medium

- [RT-15] CLAIM: Delay-limited bandwidth (my calculation, verified): for an integrator-like loop L = (wc/s) exp(-s tau_eff), the phase margin is pi/2 - wc*tau_eff, so wc <= (pi/2 - PM)/tau_eff, i.e. wc*tau_eff <= 0.785 for PM = 45 deg and <= 0.524 for PM = 60 deg; tool delay margin matched the closed form pi/(2 wc) to 5 digits at three test points. Example (SI): tau_eff = 5 ms gives wc <= 157 rad/s (25 Hz) at PM 45 deg; 20 ms gives 39 rad/s (6.2 Hz); 40 ms gives 19.6 rad/s (3.1 Hz). A PD loop on a double integrator with its zero at wc/3 has PM = atan(3) = 71.6 deg and tolerates a total extra delay of 1.249/wc (e.g. 12.5 ms at wc = 100 rad/s). Inputs are generic, not measured; the bandwidth is proportional to 1/tau_eff, elasticity of the achievable bandwidth to delay is exactly -1 in this model. The tau_eff values come from the quantitative facet, not from here. Not included: motor lag, RHP dynamics, saturation.
  SOURCE: [calc: runs/2026-10-15-quadrotor-agility-limit/calc/theory_delay_lookahead.py] (uses .claude/skills/conundrum/scripts/control_tools.py loop_margins)
  QUOTE: n/a (own calculation; the log prints the verification against closed form)
  ACCESS: full-text
  STATUS: secondary
  SETTING: analysis
  CONFIDENCE: high for the algebra, not a measured-hardware claim

- [RT-16] CLAIM: Perception-latency-to-speed relation, own derivation with verification: to stop before an obstacle first seen at range s with total latency tau and braking deceleration a, v*tau + v^2/(2a) <= s, so v_max = a(-tau + sqrt(tau^2 + 2s/a)); checked by direct integration (3 cases, agreement to 0.0005 m) and tau=0 limit sqrt(2as). The latency term v*tau equals the braking term only at v_x = 2*a*tau (2 m/s for a = 20 m/s^2, tau = 50 ms), so above a few m/s the look-ahead requirement is dominated by v^2/(2a). Elasticities of v_max (analytic = finite difference): at s = 6 m, a = 20 m/s^2, tau = 50 ms, v_max = 14.5 m/s, e_s = +0.53, e_a = +0.47, e_tau = -0.064; at s = 6 m, a = 40, tau = 20 ms: v = 21.1 m/s, e_s = 0.52, e_a = 0.48, e_tau = -0.037. For Falanga's lateral-dodge bound (r = 0.5 m) same inputs: e_s = 1 exactly, e_tau = -0.14 and -0.08, e_a = 0.43 and 0.46. At s = 10 m, tau = 100 ms, a = 20: stop bound e_tau = -0.10, Falanga bound e_tau = -0.24. Reading: under these bounds a 10 per cent range gain beats a 10 per cent latency cut by roughly 5 to 15 times; latency matters most at long latency (>= 100 ms), long range, and for dodge-type avoidance. Scope: single static obstacle at constant braking, no estimation error, perception range s treated as given, no confirmation that a quadrotor can actually brake at a with the same thrust that holds altitude (a here is a free parameter). Mechanist lens owns the full calculation.
  SOURCE: [calc: runs/2026-10-15-quadrotor-agility-limit/calc/theory_delay_lookahead.py]; Falanga et al. 2019 for the second bound
  QUOTE: n/a (own calculation; log prints verification)
  ACCESS: full-text
  STATUS: secondary
  SETTING: analysis
  CONFIDENCE: high for algebra; medium for relevance to unseen-course racing

- [RT-17] CLAIM: Thrust-to-weight ceiling (own calculation, verified): for level flight at constant altitude the horizontal acceleration is a_h = g sqrt((T/W)^2 - 1) (T/W = 2: 16.99 m/s^2; 4: 37.99; 8: 77.86), and rest-to-rest bang-bang over d = 10 m takes t = 2 sqrt(d/a_h) (1.53 s, 1.03 s, 0.72 s; closed form matched by integration to 4 digits), peak speed sqrt(a_h d) (13.0, 19.5, 27.9 m/s) and mean speed 6.5, 9.8, 14.0 m/s. Elasticity of time to a_h is exactly -1/2, and of a_h to T/W is (T/W)^2/((T/W)^2-1) = 1.33, 1.07, 1.02 at T/W = 2, 4, 8; so a 10 per cent T/W gain raises point-mass speed on a short rest-to-rest segment by roughly 5 per cent at T/W >= 4. Neglects rotation time, rotor dynamics, drag, body-rate limits and gate geometry; the true full-model optimum is a few per cent slower than point mass at the benchmark in RT-04.
  SOURCE: [calc: runs/2026-10-15-quadrotor-agility-limit/calc/theory_delay_lookahead.py]; bang-bang form from Foehn et al. 2021 (RT-02)
  QUOTE: n/a (own calculation)
  ACCESS: full-text
  STATUS: secondary
  SETTING: analysis
  CONFIDENCE: high for algebra

- [RT-18] CLAIM: Flatness-based and NMPC trackers compared on hardware under motion capture (so evidence about the controller, not about onboard-only autonomy): at speeds up to 20 m/s and accelerations up to 5 g, adding an INDI inner loop plus an aerodynamic drag model reduced position-tracking error by more than 78 per cent for both NMPC and the differential-flatness controller. This is a model-error result: the unmodelled drag/actuation error is large enough to dominate tracking error until modelled or compensated, and NMPC tracks dynamically infeasible references better at the cost of compute time and convergence risk.
  SOURCE: Sun, Romero, Foehn, Kaufmann, Scaramuzza 2022, "A Comparative Study of Nonlinear MPC and Differential-Flatness-Based Control for Quadrotor Agile Flight", IEEE T-RO, arXiv:2109.01365
  QUOTE: "Our real-world experiments, performed in one of the world’s largest motion capture systems, demonstrate more than 78% tracking error reduction of both NMPC and DFBC, indicating the necessity of using an inner-loop controller and aerodynamic drag model for agile trajectory tracking."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: hardware
  CONFIDENCE: high

- [RT-19] CLAIM: Loop delay limits feedback gain on a real-model quadrotor in simulation: raising the NMPC position weight beyond a point destabilised the simulated drone, which the authors attribute to actuator dynamics introducing system delay; they note real latency from state estimation and signal transmission is larger and lowers the permitted maximum weight further. Qualitative support for RT-07 and RT-15; no latency number is given in the passage.
  SOURCE: Sun et al. 2022, arXiv:2109.01365, Sec. on NMPC parameter study
  QUOTE: "We believe that this is due to the presence of actuator dynamics in the simulation, which introduces system delay and causes instability with high gain controllers. Note that in real-world experiments, system latency can be larger due to state estimation algorithms and signal transmissions, which further reduces the permitted maximum Qξ."
  ACCESS: full-text
  STATUS: peer-reviewed
  SETTING: simulation
  CONFIDENCE: medium

- [RT-20] CLAIM: A pure delay in the measurement can in principle be compensated by a model-based predictor (Smith predictor), but only to the accuracy of the model of the delayed plant and for stable (or separately stabilised) plant dynamics; the textbook architecture places a model with the same delay in parallel with the process. Implication for the question: estimator-side delay can be partially removed by forward prediction with the IMU-driven dynamics, so the binding quantity is then the unmodelled-disturbance error accumulated over the delay (aerodynamics), not the delay as such. This inference is mine; the textbook passage only describes the architecture.
  SOURCE: Astrom and Murray 2020 draft, Sec. 15.4
  QUOTE: "The Smith predictor is a special controller architecture fo r systems with time delays. A block diagram of the controller is shown in Figure 15.18. Th e controller is provided with a model ˆP = ˆP0e−sτ , in parallel with the process P =P0e−sτ ."
  ACCESS: full-text
  STATUS: textbook-or-review
  SETTING: analysis
  CONFIDENCE: medium

## Gaps
- No theorem found that ranks delay, actuator bandwidth, aerodynamics and look-ahead against each other: the sensitivity ordering is model- and speed-dependent and has to be computed (simulator lens). Proved results here are bounds on single limits (delay: wc*tau; RHP zero; Bode integral; stopping distance; thrust ceiling), not a ranking.
- Not shown: whether a quadrotor's position or attitude loop has a RHP zero or pole that sets a bound (symmetric planar rotor layout is minimum phase to first order in the usual cascaded model; I did not find a source stating this for quadrotors, so RT-08's applicability remains my reading). Astrom-Murray's explicit delay+RHP-pole bound (p*T product) was found only through search summary (not quoted): lecture-note constants of about omega_gc*T_d < 0.4 and p*T < 0.16 (Ms<2), unverified.
- Mellinger-Kumar 2011 (minimum snap, original flatness-for-quadrotors) has no free copy: PAPER TO REQUEST: 10.1109/icra.2011.5980409 | Minimum snap trajectory generation and control for quadrotors | original flatness statement and actuator-constraint treatment (low priority; Faessler 2018 restates flatness).
- Falanga 2019 Eq. 9: PDF text extraction garbles the square root; the layout v = s/(tau + 2 sqrt(r/u2_max)) is reconstructed and the dimension check (s/(s + sqrt(m/(m/s^2)))) is consistent; formula checked only against the stated limits, not against the paper's figures.
- Not searched for lack of budget: Cramer-Rao style bounds on VIO position drift versus speed/feature-tracking motion blur; rotor-bandwidth/jerk theory (constraints lens); perception-aware planning theory (Qin 2026 preprint arXiv:2603.04305 appeared in search, not read).
- Semantic Scholar was rate-limited throughout; citation counts for the cited papers were not retrieved.
