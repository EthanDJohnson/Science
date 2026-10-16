# Candidate answers
exclusive: yes (each candidate names the limit that *dominates* at the operating point the brief's metric selects — onboard-only, unseen course, reading (a), 2026 hardware — so at most one can be first; several are regime-complementary, and where a candidate claims a different regime it says so, which the judge should read as a ranking rather than a contradiction. C7 is their negation; C8 says the quantity is not yet defined or measured.)
lenses merged: examiner, empiricist, mechanist, dialectician, statistician, constraints, simulator
status: final

Units are SI throughout (m, s, m/s, m/s^2, N, N m, rad/s; g = 9.81 m/s^2). Elasticities are
dimensionless d ln(speed)/d ln(limit). "mocap" marks a result with external motion capture in the
loop, which the brief counts as controller evidence, not onboard-only evidence.

Three facts constrain every candidate below and are not repeated in each:
(i) no published result measures the brief's three-part metric [dossier preamble, D-24];
(ii) the best-documented onboard-only unseen-course set is 100 per cent at 3 and 5 m/s, 8/10 at
7 m/s, 60 per cent at 10 m/s on a 40 m clutter line [A-20], against 27.8–32.2 m/s peak on a *seen*
gate track [A-26];
(iii) no controlled one-at-a-time sensitivity study exists on this vehicle class [dossier §6], so
every elasticity on this slate is computed in a model, two of them cross-checked against the one
hardware-anchored number, the planner thrust-to-weight sweep [A-16].

## C1: On a course it has not seen, the perceived volume ahead binds first — usable look-ahead range, together with the solid angle still visible at the attitude the manoeuvre demands
type: mechanism
from: CONSTRAINTS-A, SIMULATOR-A, DIAL-A, STAT-D, MECH-A, EMP-D, EXAMINER-B (coupling leg)
argument: Two sub-hypotheses, acting through one product (range x solid angle), each with its own
number. **(1a) Radial range.** Required look-ahead with braking tied to the platform
(a_h = 39.0 m/s^2 at T/W 4.10) and the reorientation time included is 1.10 m at 5 m/s, 2.84 m at
10 m/s, 5.22 m at 15 m/s and 8.24 m at 20 m/s, against a 6–10 m depth-camera range — so the budget
closes in the 10–20 m/s band [calc: constraints_budget, M-CONSTRAINTS-09 verified]. Range is the
largest single elasticity anywhere in this run: +0.53 to +0.64 on the stop bound, +1.000 exactly on
the lateral-dodge bound [M-STAT-05, M-STAT-06, M-DIAL-06 verified], and +0.986 (3 -> 6 m) to +1.082
(6 -> 10 m) when the dodge is flown on a 17-state plant with real rotational dynamics, motor lag and
per-rotor thrust limits, which is 1.9–7.6 times every in-vehicle rival and 9.4 times perception
latency [M-SIMULATOR-08, M-SIMULATOR-12 as corrected]. Stereo geometry caps the *usable* range well
below the datasheet: sigma_z = z^2 sigma_d/(f b) makes depth noise equal a 0.1 m obstacle's own size
at 4.1–5.8 m for a 50 mm baseline [M-MECH-06 verified]. **(1b) Angular: field of view times
attitude.** Underactuation forces tilt theta = atan(a/g), so with a body-fixed camera the direction
of travel leaves the image once a > g tan(half-FoV + mount tilt): 5.44 m/s^2 (0.55 g) for a
level-mounted 58 deg vertical depth FoV, 16.33 m/s^2 (1.66 g) at the 30 deg up-tilt the A-20 team
adopted above 7 m/s, 44.3 m/s^2 for a 155 deg lens [M-MECH-02, M-DIAL-01 verified]. The coupled stop
bound is then 7.4 m/s level-mounted and 11.8 m/s tilted — against a measured failure onset at 7 m/s
and 60 per cent at 10 m/s [A-20] — and the cap predicts thrust-to-weight saturation at
T/W_sat = sec(half-FoV + tilt) = 1.94 on that geometry, while every onboard-only platform carries
T/W 4.1–4.5 [A-13, M-DIAL-02 verified]. Regime: begins as soon as the geometry ahead is unknown;
absent on a pre-mapped track, where a map converts look-ahead into a memory lookup.
predictions: if true, doubling usable range at fixed latency (longer-baseline stereo or 3-D LiDAR,
6 -> 12 m) raises the 90-per-cent-success speed by 2^0.53 = 1.44x on the stop bound and by 2.0x on
the dodge bound, and swapping a 58 deg for a 155 deg vertical FoV moves the 90-per-cent speed from
about 7.4 to above 17 m/s [M-MECH-02 verified]; a T/W sweep at fixed narrow optics shows a knee
below T/W 4, while the same sweep with a gimbal or hemispherical view keeps improving. If false,
mean speed is flat in an artificially clipped sensing horizon, and the lens swap changes nothing.
evidence for: [A-20] [A-21] [D-13] [D-31] [D-32] [D-39] [A-26] [calc: runs/2026-10-15-quadrotor-agility-limit/calc/lens-simulator_break.py] [calc: .../calc/lens-constraints_budget.py] [calc: .../calc/lens-mechanist_blindtime.py] [calc: .../calc/lens-dialectician_syntheses.py] [new: Qin et al., arXiv:2603.04305v1, full-text, "The camera's limited field of view introduces discontinuities as features abruptly enter or exit the image boundaries, rendering the objective function non-differentiable"]
evidence against: the mechanist's headline ranking "FoV > range" is **refuted** by its own math check —
a +10 per cent relaxation of the half-FoV gives +4.67 per cent, not +10.5 per cent (that figure
perturbs half-FoV *plus* mount tilt), so at that operating point range (+5.85 per cent) exceeds FoV
and sub-hypothesis (1b) is the smaller of the two [M-MECH-03 refuted]. "Range elasticity 2 to 10
times every rival" is **refuted**: against thrust-to-weight (+0.527) the ratio is 1.87
[M-SIMULATOR-12]. "At s = 3 m every range-limited bound halves" is **refuted** for the stop bound,
which falls 32.6 per cent [M-DIAL-09]. The simulator's own look-ahead-limited course run failed as a
measurement (pure-pursuit corner-cutting), so the perception axis rests on a dodge manoeuvre, not a
course [simulator F13]. The required look-ahead at 7 m/s is only 0.93–1.33 m against a multi-metre
sensor [mechanist F1], i.e. the naive radial bound is *not* active where hardware actually fails;
and the short-usable-range input (about 0.3–3 m for the D435i) is a search summary only
[dialectician F3]. The 7 m/s perception attribution rests on 2 crash events, Wilson [0.34, 1.00]
[statistician F8].
decisive test: one airframe, one policy, one afternoon: fly the same unseen clutter course with the
depth stream software-clipped at 3, 6, 10 and 20 m (sub-hypothesis 1a) and, separately, with the
lens swapped 58 -> 115 -> 155 deg vertical FoV or gimballed (1b), >= 29 trials per setting to
support a 90-per-cent claim [M-EXAMINER-05, M-STAT-01 verified]. Precision needed: speed resolved to
about 0.5 m/s and success to 10 points, i.e. about 29–46 flights per cell, roughly 120–250 flights
total. Who: UZH RPG (the A-20 stack), TU Delft MAVLab, or an A2RL team; no new hardware for the clip
arm, a few lenses for the FoV arm. Expected: the November 2026 identical-hardware final is the
natural venue if onboard compute is mandated [D-41].

## C2: State estimation binds first — not through its latency but through drift and feature loss during the manoeuvre, which today is repaired only by prior track knowledge
type: mechanism
from: MECH-B, DIAL-B, EMP-E (narrowed survivor), EXAMINER-E (narrowed survivor), SIMULATOR-C, STAT-F (latency sub-hypothesis)
argument: **Sub-hypothesis (2a), estimation reliability (surviving).** Agile manoeuvres demand
hundreds of deg/s of body rate, and image blur is rotation-dominated at racing conditions: at
f = 447 px, 500 deg/s smears 3.90 px per ms of exposure against 1.79 px for 20 m/s of translation at
5 m, ratio 2.18, with rotation dominating above omega = v/d = 229 deg/s [M-MECH-07 verified]. Blur
and field-of-view loss destroy tracked features, producing "loss of tracked visual features and
severe drift" [D-12]; global position and yaw are unobservable, so the error has no self-correction
[D-06]; and the one repair the field uses is matching detected gates to a *known* layout [D-11],
which the brief's unseen clause forbids. Competitors in the 2025–26 minimal-sensor regime name the
estimation chain as the dominant engineering problem [D-19], MonoRace's authors note their simulator
"does not accurately model vision-based state estimation errors that occasionally caused real-world
crashes" [A-28], and the nearest thing to a controlled sensitivity study moves only the planner's
perception objective and lifts closed-loop success from 55 to 100 per cent when that objective is
state-estimate uncertainty (20 trials, RotorS simulation) [new: arXiv:2603.04305v1]. The simulator
lens records this as the largest gap between its model and reality: its loop has latency and white
noise but no drift and no blur, and says so explicitly [SIMULATOR-C]. **Sub-hypothesis (2b),
transport latency (eliminated at 2026 values, re-binding above about 130 ms).** At 17–40 ms
[A-07, A-28] the stop-bound elasticity is -0.030 to -0.225 and the dodge-bound elasticity -0.069 to
-0.362; parity with range needs tau = 161–343 ms [M-STAT-05, M-STAT-06 verified]. Both loops of a
verified closed-loop model sit at 6–7 per cent of their delay margins (27.57 ms inner against a
2.00 ms budget; 354.0 ms outer against 22.50 ms), and raising tau_vio from 5 to 130 ms never
destabilises the loop — it only costs speed, 18.89 -> 10.60 m/s [M-SIMULATOR-05 verified]. With
differential-flatness feedforward the loop needs only wc >= 0.875 rad/s, tolerating 897 ms of delay,
22.4x the measured 40 ms [M-CONSTRAINTS-07 verified]. Expert human pilots run about 220 ms against
Swift's 40 ms on drones of the same weight, shape and propulsion and lose only 2.8–21.2 per cent of
lap time, implying |e| = 0.016–0.113 [M-EMP-05 verified, D-16]. Latency re-binds only in a
feedback-only architecture (v_max = e_allow x wc = 11.8 m/s at 40 ms, elasticity exactly -1) or at
the historical 130 ms chain [A-22].
predictions: if true, sweeping commanded body rate at fixed forward speed makes VIO drift scale with
omega x t_exposure rather than with v; an oracle (or map-corrected) state estimate raises *success
rate* by tens of points while improving lap time by only a few per cent; and shortening exposure or
fitting an event camera moves the speed at which 90-per-cent success fails. If false, measured drift
at 10–15 m/s is small while obstacle detections are late (which would favour C1), or injecting
40 ms of extra estimator delay costs as much speed as the drift does (which would revive 2b).
evidence for: [D-06] [D-11] [D-12] [D-19] [A-22] [A-28] [D-37] [calc: .../calc/lens-mechanist_lookahead.py] [calc: .../calc/lens-simulator_break.py] [new: Qin et al., arXiv:2603.04305v1, full-text, "TABLE VI ... TOWP-Ours 0.3590 0.4192 55% LA 0.3541 0.4612 67% FOV 0.4634 0.3577 71% PUM 0.2228 0.3239 100%"]
evidence against: the dossier records **no measured VIO drift in m per m and no measured end-to-end
VIO latency at racing speed** [dossier §6], so the step from blur to crash is inference, not
measurement [mechanist chain 4 weakest link]. One leg of the latency elimination is **refuted**:
"latency is 5–24 per cent of the required stopping distance above 5 m/s" is actually 14–39 per cent
over 5–20 m/s and reaches 5 per cent only near 60 m/s, so at 5–10 m/s the reaction term is a third
of the look-ahead budget [M-EMP-07]; the elimination survives on its other legs (elasticities and
the human-pilot comparison, both verified). The event-camera analogue cuts against (2a) as well as
(2b): a sensor with about 10 us latency and 140 dB dynamic range has produced 5 m/s onboard tree
avoidance, not 50 [A-24, A-30]. [D-18]'s domain-shift ablation rests on a quote unverified in the
quantitative pass.
decisive test: log onboard VIO against ground truth while sweeping commanded body rate (0–600 deg/s)
at fixed forward speed and fixed exposure, and report drift in m per m and feature count; then rerun
the same unseen course with an oracle state estimate supplied off-board for the *estimate only*
(labelled as such). Precision: drift resolved to 0.01 m per m; >= 29 trials per condition for the
success-rate arm. Who: any group with a UZH-FPV-style rig, or a replay of that dataset through the
candidate's own estimator — the dataset exists and the paper is on the dossier's request list
[dossier §6]. Cost: days, not money.

## C3: The binding term is in the task, not the vehicle: prior information about the course (a map or a trained track) is what a fast onboard flight actually uses, and the metric forbids it
type: mechanism
from: EMP-A, STAT-B, CONSTRAINTS-F, MECH-REFRAME (information leg), DIAL finding 1
argument: Grouping every onboard-only speed in the evidence base by course type and working in
ln(speed) with an assigned 20 per cent spread gives within-group chi2 of 2.97/2 (seen gate track,
mean 26.2 m/s), 5.28/3 (unseen clutter, 7.4 m/s) and 0.47/1 (mocap, 33.0 m/s) against a
**between-group chi2 of 104.2 on 2 dof, p = 2.4e-23, z = 10.0**, surviving an assigned spread of
80 per cent (p = 0.039) and full within-group correlation at rho = 0.8 (z = 5.8)
[M-STAT-04 verified]. Nothing else in the record splits like that: it is a factor of 2.6–6.4 on the
same airframe class, with no hardware parameter changing between the rows [M-DIAL-10]. The firm
within-apparatus leg is Swift at 12.88 m/s mean (75 m lap, 17.465 s best three laps, onboard sensing
and compute) on a *seen, pre-mapped* track [M-EMP-03 verified arithmetic] against 5–7 m/s unseen
[A-20], a ratio of 2.58x. To buy that same factor through any one of the brief's four limits at the
dossier's own elasticities would need T/W about 29 (from 4.4), 2.6x range on the dodge bound or
6.2x on the stop bound, or a 52x latency cut, which is impossible since tau cannot go below zero
[M-EMP-04 verified]. The mechanism is concrete: Swift matches detected gates "to the known track
layout" to correct VIO drift and fits its residual models on that track [D-11, D-12]; competitions
supply the gate map beforehand [D-11]; and the fastest onboard results above 20 m/s are all mapped
[A-26]. Regime: the whole of reading (a), because the metric is defined on an unseen course.
predictions: if true, a course-knowledge ablation on one vehicle — same airframe, same policy, flown
(a) on a pre-mapped gate track, (b) on the same track with gates displaced 1–2 m, (c) on a track it
has never seen — drops the 90-per-cent speed by a factor of 3–4 with the vehicle untouched, and the
drop is larger than any single hardware relaxation produces. If false, speed falls by less than
about 30 per cent from (a) to (c), and the seen/unseen split was a task-difficulty or feature-spacing
artefact rather than an information one.
evidence for: [D-11] [D-12] [D-17] [D-20] [D-23] [A-10] [A-20] [A-26] [A-29] [calc: .../calc/lens-statistician_rates.py] [calc: .../calc/lens-empiricist_observations.py] [new: Kaufmann et al., Nature 2023 author PDF, full-text, "Swift versus human pilots 25 17.465 s 15 10 0.60"]
evidence against: the 2.58x is a **between-apparatus** comparison — different group, different
sensors, and a gate sequence against an obstacle field, which are not the same task [empiricist F3,
D-23]. The dialectician's rival reading attributes much of the split to *feature spacing* rather than
information (gate pitch about 10.7 m against clutter spacing about 4 m), and the spacing-and-latency
bound predicts a ratio of 6.70 against an observed 2.78–3.22, i.e. it over-predicts
[M-DIAL-03 refuted the 8.52 figure; corrected value 6.70, gate-track slack 2.08x]. Swift's 15 wins
of 25 is a win rate, not a completion rate [A-10], and the seen-course speeds carry no quoted
uncertainty, so the 20 per cent spread in the grouping is an assumption [statistician assumptions].
The unseen-clutter group reduces to one sensor configuration on one group's airframe [statistician
F11], so the low side of the split may be an apparatus property (see C7's apparatus note).
decisive test: the course-knowledge ablation above, on one platform, one day: >= 29 trials per
condition, mapped / displaced-gate / never-seen, with the gate-map term switched in and out of the
estimator only. It needs no new hardware and about 90–140 flights; UZH RPG, TU Delft MAVLab or an
A2RL team could run it. This is the cheapest decisive experiment on the whole slate and no one has
run it [statistician "what data would settle it", empiricist skeptic table].

## C4: No hardware limit is active: what binds is the robustness of the perception–estimation–policy stack and the margin designers deliberately leave inside the hardware envelope
type: mechanism
from: EXAMINER-A, STAT-I, MECH-REFRAME (objective leg), DIAL-D (absorption leg)
argument: Ten bounds computed from the dossier's own anchors span 10.73–32.72 m/s (factor 3.05), and
the best-documented onboard-only unseen-course operating point of 5 m/s sits at 0.47 of the *lowest*
and 0.15 of the highest; 7 m/s is 0.21–0.65 and 10 m/s is 0.31–0.93 [M-EXAMINER-08 verified]. A
system running at a quarter to a half of every limit is limited by none of them. What does move the
metric is software: on identical hardware and the same track, trajectory-tracking MPC goes from
4.92 s and 44 per cent in nominal simulation to 0 per cent under a realistic model and 0 per cent in
the real world, while an RL policy holds 85 per cent at 5.35 s — 0/20 against 17/20 is z = 5.44,
two-sided p = 5.4e-8, the only signal in the evidence base below 1e-6 [M-STAT-09 verified, A-14,
D-14]. The authors attribute the advantage to the objective, not the optimiser [D-15]. Planners are
run deliberately inside the thrust bound "to maintain controllability under disturbances" [D-36],
and on a verified plant the platform's own time-optimal profile is untrackable by a finite-bandwidth
cascade at a quarter of its acceleration budget (loss of control at alpha = 0.25, completion at
alpha = 0.10) [simulator F11], so the margin is not timidity but a property of the architecture. The
field's own named culprits are architecture-level in three of five cases [D-21 b, c, e], and learned
policies "trained on specific environments often crash immediately in unseen configurations"
[D-17, D-18].
predictions: if true, a five-arm ablation on one airframe has the architecture arm (plan-then-track
replaced by a task-objective policy, or an INDI/lag-inverting inner loop) beating each hardware arm
by more than a factor of two in the metric, and no single hardware relaxation at its *attainable*
increment moves the unseen-course metric by more than about 20 per cent. If false, one hardware arm
(range, FoV, thrust) produces a larger gain than the architecture arm.
evidence for: [D-14] [D-15] [D-17] [D-18] [D-21] [D-36] [A-14] [calc: .../calc/lens-examiner_structure.py] [calc: .../calc/lens-simulator_sweep.py] [new: arXiv:2310.10943 (preprint of doi:10.1126/scirobotics.adg1462), full-text, "Nominal 4.92± 0.10 44.0 ... Real World – 0.0 5.54± 0.21 50.0 5.35± 0.15 85.0"]
evidence against: the 0-versus-85-per-cent result's real-world rows used Vicon plus an EKF, so it is
controller evidence, not onboard-only evidence [D-14], and its trial counts are not stated — they
are inferred from the granularity of the reported percentages, which makes the z-values lower bounds
[statistician F9]. "No hardware limit is active" is a claim about *bounds*, and the bounds are
point-mass and optimistic (no rotation time, no drag, no battery sag), which pushes them toward the
operating point rather than away [examiner assumptions]; on a verified plant the baseline closed loop
*did* fail against thrust authority with the mixer saturated 32 per cent of control steps and peak
rotor thrust at 8.46 of 8.5 N [simulator F5], which is a hardware limit being touched. The claim also
leaves the 5–10 m/s unseen ceiling unexplained by any quantity, whereas C1–C3 each name one.
decisive test: five-arm ablation on one airframe with the metric measured as >= 29 unseen-course runs
per speed set-point: (i) baseline; (ii) wide-FoV or gimballed camera; (iii) T/W raised 4.1 -> 8;
(iv) tau_eff cut 40 -> 15 ms; (v) plan-then-track replaced by a task-objective policy (and, as a
cheaper variant, an INDI inner loop on stock rotors [D-09]). Precision: 10 points of success rate per
arm, i.e. 29–46 flights per cell; of order 150–400 flights, a few airframes' attrition, plausibly
USD 50–150k and a few months for a group that already owns the stack [examiner decisive experiment].

## C5: The actuator envelope binds first — thrust authority and the constant-altitude torque ceiling, not the motor time constant — and it binds in the seen-course 15–20 m/s regime
type: mechanism
from: SIMULATOR-B, CONSTRAINTS-C, STAT-E, EXAMINER-F / EMP-F / MECH-D / DIAL-C (as the eliminated narrow form)
argument: Three named sub-hypotheses, in order of surviving strength. **(5a) Thrust authority.** On a
verified 17-state plant (24/24 verification rows, two independent implementations, four closed-form
limits) the baseline run on a seen slalom fails by loss of control with the mixer saturated 32 per
cent of control steps at 89.7 per cent of the platform's time-optimal time, and the elasticity of
mean speed to per-rotor thrust is +0.527 across 6 -> 7.5 N — reproducing the only hardware-anchored
elasticity in the evidence base, the planner sweep's +0.565, to within 7 per cent
[M-SIMULATOR-07, M-STAT-07 verified; A-16]. **(5b) The constant-altitude torque ceiling.** Because
f_i >= 0, roll/pitch torque at hover collective is exactly l_eff m g = 0.990 N m
(alpha = 396 rad/s^2) independent of installed thrust, confirmed by brute-force maximisation to
8e-16 N m [M-CONSTRAINTS-02 verified]; a 152 deg thrust-vector reversal then takes 164 ms with no
lag and 201 ms with the measured 39.1 ms lag, occupying 3.02 m of travel at 15 m/s against 0.60 m
for a 40 ms sensorimotor latency — a factor of 5 [M-CONSTRAINTS-04 verified]. This term is absent
from the brief's four candidates. **(5c) Rotor/motor bandwidth (eliminated as first-binding).** The
39.1 ms thrust time constant [A-03] gives d ln(segment time)/d ln(tau) = +0.040 and
d ln(slew)/d ln(tau) = +0.177 [M-CONSTRAINTS-04], and d ln v/d ln(motor tau) = -0.019 in the
look-ahead chain, so halving it buys about 1 per cent of speed [M-MECH-04 as corrected]; on the
verified plant the elasticity is -0.212 at the measured value but **exactly 0.000 across 5 -> 10 ms**
— relaxing it below about 20 ms buys nothing in that architecture, while doubling it to 78.2 ms
costs a factor of two (-1.023) [M-SIMULATOR-07 verified]. Regime: seen or mapped course at 15–20 m/s
on a 0.75–0.87 kg, T/W 4.1–4.6 platform; below about 10 m/s nothing in the envelope binds, and above
about 20 m/s the model's omitted effects (drift, blur, quadratic drag) take over.
predictions: if true, re-flying a fixed seen track with a rotor set whose measured time constant is
near 15 ms at the same static thrust gains little, while an INDI inner loop on the stock rotors
recovers most of what the faster rotors do [simulator distinguishing test]; a vehicle allowed to
climb through the turn (collective 2 m g) reorients sqrt(2) = 1.41x faster than one holding altitude
— a free, measurable gain no published controller claims; and a T/W sweep 4 -> 8 with a wide-FoV or
gimballed camera raises mean speed by about 2^0.5 = 1.4x. If false, the motor swap, the climbing turn
and the T/W doubling all move the metric by under a few per cent.
evidence for: [A-03] [A-04] [A-13] [A-16] [D-05] [D-30] [D-33] [D-36] [A-34] [calc: .../calc/lens-simulator_sweep.py] [calc: .../calc/lens-constraints_actuator.py] [calc: .../calc/lens-simulator_verify.py]
evidence against: **no paper in the evidence base argues that actuator or rotor bandwidth is the
binding limit, and the critiques researcher searched for one** [dossier §6, D-21]. The same airframe
class flies at 30.0 m/s and 12.58 g with mocap state [A-12] and is specified to 36.4 m/s [A-02], so a
limit that permits 30 m/s is not what caps 5–7 m/s [EMP-F]. The simulator's supporting contrast is
**refuted**: zeroing the inner delay raises the achievable rate-loop gain by +18.7 per cent, not
8 per cent (the corrected contrast is +18.7 per cent against x10.93, which raises the value of
cutting inner-loop latency) [M-SIMULATOR-11]; and the mechanist's blind-time decomposition is
**refuted** — the lagged reorientation takes 133.9 ms, not 95.6 ms, so the lag costs about 42 ms and
is comparable to the inertia term rather than 10x smaller, though the elasticity conclusion is
unchanged [M-MECH-04]. The constraints lens's "84.1 ms admits 0.70 Hz" is a coarse-grid artefact; the
admissible bandwidth is about 1.1 Hz [M-CONSTRAINTS-10 refuted, direction conservative]. Thrust is
also predicted to saturate against the camera cone at T/W about 1.9 (C1, sub-hypothesis 1b), which
would null (5a) on an unseen course; and planners leave the thrust ceiling unused by design [D-36].
The 39.1 ms figure is a large-signal fit to a 12 N step; a shorter small-signal value weakens (5c)
further [constraints F14].
decisive test: two arms on one seen track, 20+ trials each: (i) stock rotors with an INDI or
lag-inverting inner loop against stock rotors with the stock cascade; (ii) a rotor/propeller set with
a bench-measured time constant near 15 ms at matched static thrust. Bench prerequisite: spin down a
5-inch rotor with ESC braking off and fit omega_0/(1 + t/t_c) to settle the rotor inertia the slew
model assumes [M-MECH-05 verified; dossier §6 lists the slew rate as not retrieved]. Cost: a bench
afternoon plus two flight sessions; any racing-quadrotor lab. For (5b), fly the same turn with
altitude held and with a 1 g climb allowed and compare reorientation times — pure firmware.

## C6: Unmodelled aerodynamics binds first, as model error against gate or obstacle clearance, and only for model-based pipelines above about 13 m/s
type: mechanism
from: CONSTRAINTS-B, EXAMINER-G, EMP-G, MECH-E
argument: Power-law fits to the replayed-flight positional RMSE of [A-18] give
e_model(v) = 0.0493 v^0.858 m (blade-element-momentum, log-log R^2 = 0.83) and 0.0439 v^1.173 m
(polynomial fit, R^2 = 0.89), reproduced independently to 0.5 per cent [M-CONSTRAINTS-08 verified].
With a 0.60 m clearance (1.5 m gate [A-26] minus a 0.15 m vehicle radius) and a T265-class estimator
error of 0.151 m, model error fills the remaining 0.449 m at v* = 13.1 m/s (BEM) or 7.3 m/s
(polynomial fit), with d ln v*/d ln(model error) = -1.17 and -0.85 — and halving the model error,
which a BEM-plus-neural-residual model achieves on force error [D-08], moves v* to 29.5 or 13.1 m/s.
That is the only single perturbation in the constraints analysis that moves a speed ceiling by more
than 50 per cent. Aerodynamics is also the field's own most-cited culprit: "the dominant model defect
during high speeds or agile maneuvers", cutting replay positional RMSE from about 0.8 m to below
0.3 m [D-08], and the named cause, with variable system delay and battery-voltage fluctuation, of a
plan-then-track controller collapsing to 0 per cent success [D-14]. Regime: model-based
(plan-then-track or MPC) pipelines on courses tight enough that 0.3–0.5 m of error matters, above
about 7–13 m/s.
predictions: if true, the speed at which a model-based onboard pipeline loses 90-per-cent success
scales as the inverse 0.86–1.17 power of its force-prediction error, so a NeuroBEM-grade model buys
1.8–2.2x the speed of a polynomial drag model on the same airframe and track, and buys a learned
end-to-end policy much less. If false, measured closed-loop error at 15–20 m/s stays near 0.05 m
rather than approaching the open-loop 0.4 m, and the aero-model-on/off arm moves the unseen-course
metric by under 10 per cent at 7 and 15 m/s.
evidence for: [D-08] [D-09] [D-14] [D-21(a)] [A-06] [A-17] [A-18] [calc: .../calc/lens-constraints_budget.py] [calc: .../calc/lens-mechanist_blindtime.py]
evidence against: every aerodynamic number in the evidence base is an **open-loop replay** error
against motion capture [A-18] or a mocap-controller result [D-09]; there is no hardware experiment in
which a better aero model raised an onboard-only unseen-course speed [EMP-G]. The residual force
error of the best model class, 0.352–0.365 N on 0.75 kg = 0.487 m/s^2, integrates to only 0.68 cm of
position error over a braking manoeuvre from 7 m/s, 1.38 cm from 10 m/s and 5.51 cm from 20 m/s
against clearances of order 0.5 m [M-MECH-08 verified], so below about 15 m/s it is a
tracking-accuracy mechanism, not a collision mechanism. With flatness feedforward the loop has only
to reject a 0.46 m/s^2 disturbance, leaving a 1.2 mm residual at the measured 40 ms
[M-CONSTRAINTS-07 verified]. The model-fidelity penalty on the computed optimum is 2.00–2.68 per cent
of traversal time [A-17], and a limit worth a few per cent cannot explain a factor of 2.8–6.4
[M-DIAL-10 verified inequality]. On the only published parameter set for this class the dominant
unmodelled term has the **wrong sign**: the h-force +k_h(vx^2 + vy^2) adds 4.0 N of body-z force at
20 m/s, 54 per cent of the vehicle's weight, and the closed-loop elasticity of speed to the
unmodelled drag magnitude is **positive** (+0.381) [M-SIMULATOR-09 verified; simulator F10]. The
power-law extrapolation from 1.67–6.92 m/s data out to 13–29 m/s is a 2–4x extrapolation and is
flagged by its own author as the weakest step [M-CONSTRAINTS-08 unverified as physics].
decisive test: same airframe, same policy, same course, residual aero model on and off, onboard only,
at 7 and 15 m/s, >= 29 trials per cell — and in parallel measure *closed-loop* tracking error at
15–20 m/s to see whether it follows the open-loop power law (about 0.4 m) or is rejected (about
0.05 m). The second measurement is the cheap discriminator and decides C6 against C1 and C4 directly
[constraints "what would change my mind"]. Who: any group with the NeuroBEM model and an
Agilicious-class platform; cost is flight time only.

## C7: Null — no single limit dominates: the leading candidates sit within a factor of about two at the operating point, and which one is first changes with regime
type: null
from: EMP-B, STAT-A, CONSTRAINTS-E, MECH-NULL, SIMULATOR-D, EXAMINER-D, EXAMINER-B (substitution leg)
argument: Four independent routes. **(i) Elasticities cluster.** Usable range +0.52 to +0.61,
braking/lateral acceleration +0.39 to +0.49, thrust-to-weight +0.50 to +0.565 (including the one
hardware-anchored sweep) lie within a factor of 2.33 at the endpoints and 1.67 on midpoints
[M-EMP-11 verified], which is the brief's own "within a factor of two" trigger for declaring no
dominance; model error at -0.85 to -1.17 joins them [M-CONSTRAINTS-08]. **(ii) Exact
substitutability.** In the stop bound v is jointly homogeneous of degree 1 in (range, acceleration),
so e_range + e_accel = 1 *identically* and the bound depends on the product a x s: a 1 per cent gain
in either buys the same 0.5 per cent of speed, and "which of these two binds" has no answer
[M-EXAMINER-01 verified, M-STAT-05]. **(iii) The seen-course regime on a verified plant.** At the
measured hardware values the elasticities are thrust-to-weight +0.527, motor time constant -0.462,
unmodelled-aero magnitude +0.381 and VIO latency -0.132 to -0.267: largest over smallest 3.99, and
the two biggest within 15 per cent [M-SIMULATOR-07 verified]. **(iv) The perception terms co-bind.**
Range (+5.85 per cent per +10 per cent) and half-FoV (+4.67 per cent) act through one product and
differ by a factor 1.25 after correction [M-MECH-03]. And the two lowest of ten independent bounds —
the thrust bang-bang mean 10.73 m/s and the FoV-capped stop bound 10.85 m/s — agree to 1.1 per cent,
so in the 10–11 m/s band where [A-20] degrades to 60 per cent two constraints become active at once
[M-EXAMINER-08 verified].
predictions: if true, a one-at-a-time sensitivity study finds no single perturbation moving the
unseen-course 90-per-cent speed by more than about 1.5x, and two or more perturbations moving it by
1.4–2.2x; relaxing range or thrust alone near 10–11 m/s gains little while relaxing both gains a lot.
If false, one arm shows an elasticity above about 1.0 while every other stays below 0.5.
evidence for: [D-21] [D-33] [A-16] [A-33] [A-34] [dossier §6] [calc: .../calc/lens-statistician_rates.py] [calc: .../calc/lens-examiner_structure.py] [calc: .../calc/lens-simulator_lookahead.py]
evidence against: the endpoint spread 2.326 **exceeds** the brief's literal factor-of-two trigger, so
the null's central appeal holds on midpoints only [M-EMP-11 caveat]. In the unseen regime the
dodge-bound range elasticity of +1.000 (and +0.986/+1.082 on the verified plant) is 1.9–7.6 times
every in-vehicle rival, which is a clear ranking rather than a tie [M-SIMULATOR-12 as corrected,
M-DIAL-06 proved e_s > |e_tau| and e_s > e_a over the whole parameter domain]. The ten bounds span a
factor of 3.05, so the strong null is false across the range and survives only in the 10–11 m/s band
[M-EXAMINER-08]. And a null that averages over regimes hides the one result everyone reproduces: the
2.8–6.4x seen/unseen split (C3).
decisive test: the one-at-a-time sweep itself, on a single platform, each arm with >= 32 trials
(enough to tell 0.90 from 0.60) and preferably 46 (enough to certify 0.90 with one failure): inject
40 ms of delay at a fixed radio link, mask the depth camera at 3/6/12 m, cap thrust at T/W 3/4/6,
enable and disable the aerodynamic residual model. About 500 flights; the null is confirmed if no arm
exceeds 1.5x and at least two reach 1.4x [statistician "what data would settle it"].

## C8: The metric is not yet an observable and "binds first" is not a well-defined partial derivative, so the asked-for ranking does not currently exist
type: reframe
from: EXAMINER-C, EXAMINER-B, EMP-C, STAT-C, SIMULATOR-E, DIAL-G, DIAL-F, MECH-REFRAME (metric leg)
argument: Four defects, each computed. **(1) The reliability clause is unmeasured.** Certifying
p >= 0.90 at one-sided 95 per cent needs 29 consecutive successes (0.05^(1/29) = 0.9019), or 46
flights with one failure and 76 with three; the best published onboard-only point, 10/10 at 5 m/s,
certifies only 0.741, and 8/10 at 7 m/s does not even reject 0.90 (one-sided p = 0.264), while
telling 0.90 from 0.80 needs about 199 trials per arm [M-EXAMINER-05, M-STAT-01, M-STAT-02,
M-STAT-03, M-EMP-01, M-EMP-02 verified]. **(2) The denominator is non-causal.** The platform's
time-optimal time is computed with the whole course known while the vehicle has only its look-ahead,
so the ratio adds an information deficit to a dynamics deficit, and no hardware change removes the
first [examiner F1]. On a verified plant the denominator is also unreachable: the time-optimal
profile is bang-bang and loses control at a quarter of its acceleration budget, and the smooth family
that *can* be flown already costs 9.01 per cent of t_opt [M-SIMULATOR-03 verified; t_opt = 4.5020 s
flying-start, against 5.039 s rest-to-rest — a convention the lens never states, worth 12 per cent of
every reported fraction, M-SIMULATOR-01 note]. **(3) The partial derivative does not exist as an
operation.** Perception range and braking acceleration are exact substitutes in the stop bound
(e_s + e_a = 1 identically) and are coupled through body attitude, since tilt atan(a/g) swings the
flight direction out of a body-fixed camera cone at 1.00 g for a 90 deg lens; so "relax one limit
holding the others fixed" is not an available move [M-EXAMINER-01, M-EXAMINER-02 verified]. **(4) Two
of the four named limits are mis-levelled.** "Unmodelled aerodynamics" is not one signed quantity —
its dominant published term makes the vehicle faster [M-SIMULATOR-09] — and "state-estimation
latency" is two limits entering different loops with elasticities differing by a factor of 20
(IMU path -0.062 at 0.5–2 ms, VIO path -0.132 at 10–40 ms) [M-SIMULATOR-07]. Repair: report mean
speed with a Clopper–Pearson lower bound at a stated n; two denominators (full-information and
receding-horizon at the vehicle's own look-ahead); and directional derivatives along attainable
engineering moves rather than per-cent elasticities, since 1 per cent of 40 ms is 0.4 ms and
1 per cent of 6 m is 6 cm.
predictions: if true, any future claim of "90 per cent on an unseen course" will carry n < 29, and
independent labs will keep producing mutually inconsistent rankings of the same four limits, which is
what [D-21] already records. If false, someone publishes 29/29 (or 65/69) at a stated speed on a
stated unseen-course distribution, which converts the question into an answerable one.
evidence for: [D-11] [D-17] [D-23] [D-24] [A-20] [A-27] [A-14] [dossier preamble and §6] [calc: .../calc/lens-examiner_structure.py] [calc: .../calc/lens-empiricist_observations.py] [calc: .../calc/lens-statistician_rates.py] [calc: .../calc/lens-simulator_verify.py]
evidence against: the trial-count arithmetic was partly **refuted**: at the one-sided 95 per cent
convention the counts are 29 / 46 / 76 for 0 / 1 / 3 failures, not 29 / 54 / 85, which mixes two
confidence conventions and overstates two of the three by 12–17 per cent [M-STAT-11]; and the claim
that the 6/10 result at 10 m/s rejects 90 per cent after multiplicity is **refuted** — the global z
is 1.07, not 1.7 [M-STAT-12], so that row survives only as a prespecified local comparison. The
equal-per-cent latency sensitivity is **refuted** in detail (+0.722 per cent, not +0.66)
[M-EXAMINER-06]. More substantively, a reframe does not answer the question: the brief asks for a
ranked slate anyway, and C1–C6 show that computable bounds *do* separate by factors of 2–10 within a
stated regime, so "no answer exists" is stronger than the evidence requires.
decisive test: cheap and definitive — publish one success-versus-speed curve with stated trial counts
on a stated unseen-course distribution: 29 flawless (or 46 with one failure) flights per speed bin at
5, 7, 9 and 11 m/s, about 120–185 flights, a 2–3 week session on one airframe for any of the three
groups that own a stack. The November 2026 identical-hardware final could produce one by construction
if organisers mandate onboard compute and report per-trial outcomes [D-41, A-31].

## Sensitivity and regime summary

Elasticities are d ln(speed)/d ln(limit) unless noted; "verified" means the run's math check
re-derived it independently. Every row carries the regime in which it was computed.

| Candidate | Limit's measured value | Elasticity at the operating point | Regime where it binds | Evidence class |
|---|---|---|---|---|
| C1 (1a) range | 6–10 m usable depth; ~3 m quoted for the D435i (search-summary) | +0.53 to +0.64 (stop), +1.000 (dodge), +0.986/+1.082 on a verified 17-state plant [M-SIMULATOR-08, M-STAT-05/06] | unseen course, 7–20 m/s; absent on a mapped track | verified model; no hardware sweep exists |
| C1 (1b) FoV x attitude | 58 deg vertical depth FoV at 30 deg tilt -> a_u = 16.33 m/s^2 | +0.467 per +10 per cent half-FoV [M-MECH-03, corrected] | unseen course with a body-fixed camera; predicts T/W saturation at 1.94 | verified geometry; one failure attribution [D-13] |
| C2 (2a) estimation drift | no measured drift in m per m at racing speed [dossier §6] | not computed (model has no drift) | unseen course and fast mapped tracks alike | inference from blur ratio 2.18 [M-MECH-07] plus one simulation ablation |
| C2 (2b) latency | 40 ms sensorimotor [A-07]; 17 ms image delay [A-28] | -0.030 to -0.225 (stop), -0.069 to -0.362 (dodge), -0.132 closed-loop [M-STAT-05/06, M-SIMULATOR-07] | above about 130 ms, or feedback-only architectures | verified model plus a hardware cross-controller comparison |
| C3 course knowledge | binary: map in the loop or not | effect size 2.6–6.4x, between-group z = 10.0 [M-STAT-04] | the whole unseen-course regime | hardware demonstrations, between-apparatus |
| C4 architecture | 0 vs 85 per cent success on fixed hardware [A-14] | z = 5.44 on the success rate [M-STAT-09] | all regimes; the bounds sit 2–7x above the operating point | hardware (mocap state), so controller evidence |
| C5 (5a) thrust | T/W 4.10–4.62, a_h 39.0–44.3 m/s^2 | +0.527 model vs +0.565 measured planner sweep [M-SIMULATOR-07, M-STAT-07] | seen course, 15–20 m/s | verified model plus one hardware-anchored sweep |
| C5 (5b) torque ceiling | l_eff m g = 0.990 N m, 396 rad/s^2, 164–201 ms per reversal | enters C1 as blind time: raises e_tau from -0.056 to -0.212 [M-CONSTRAINTS-09] | every regime with large attitude changes | verified model; absent from the dossier's four candidates |
| C5 (5c) motor lag | 39.1 ms thrust time constant [A-03] | -0.019 (look-ahead), -0.040 (segment), -0.212 at the measured value, 0.000 below 20 ms [M-MECH-04, M-CONSTRAINTS-04, M-SIMULATOR-07] | only if the lag exceeds about 40 ms, or for manoeuvres under 150 ms (a > 90 m/s^2) | verified model; no source argues it binds |
| C6 model error | 0.0493 v^0.858 m replay RMSE; force RMSE 0.352–0.365 N | -0.85 to -1.17 on v* [M-CONSTRAINTS-08] | model-based pipelines above 7–13 m/s | model-error result (replay and mocap), extrapolated 2–4x |
| C7 null | — | leading elasticities within 1.67x (midpoints) to 2.33x (endpoints) [M-EMP-11] | 10–11 m/s band, and the seen-course regime | arithmetic on the rows above |
| C8 reframe | 29 flawless flights to certify 0.90; best published 10/10 -> 0.741 | n/a | all regimes | verified arithmetic |
