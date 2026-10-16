# Analysis: empiricist (what has actually been observed)

status: final

## Method applied

I sorted every claim in the evidence base into what was *observed on flying hardware under the brief's
onboard-only restriction* and what was *inferred* — from a simulator, from a mocap-assisted flight, or
from a point-mass bound. I then asked what the observations alone constrain, how many trials stand
behind each, what the field's own base rate is for simulated agility surviving contact with hardware,
and what an honest skeptic would still require. Units are SI (speeds m/s, accelerations m/s^2 or g with
g = 9.81 m/s^2, times s or ms, angles deg).

## Findings

**F1. The brief's agility metric has never been measured. Not once, by anyone, at any speed.** Three
conditions must hold together: unseen course, >= 90 per cent success over a stated number of trials, and
a fraction of the platform's own time-optimal time. The dossier states outright that "No source in this
evidence base reports all three" [dossier §preamble]. The closest is [A-20]: onboard-only flight through
*unseen* clutter at 100 per cent (3 and 5 m/s), 8 of 10 = 80 per cent (7 m/s), 60 per cent (10 m/s) — but
it is a 40 m straight reference line through obstacles, not a gate sequence, the per-speed trial counts
were not reported, and no time-optimal denominator is given. Everything downstream of this is inference.

**F2. The trial counts that exist cannot resolve a 90 per cent criterion.** Exact (Clopper–Pearson)
intervals on every reported hardware success rate [calc: runs/2026-10-15-quadrotor-agility-limit/calc/lens-empiricist_observations.py]:
8/10 at 7 m/s gives [0.444, 0.975] — 90 per cent is *not excluded*; 10/10 gives [0.692, 1.000] — 90 per
cent is *not established*. An all-success run needs n = 29 (one-sided 95 per cent) or n = 35–36
(two-sided) to put the lower bound at 0.90, and telling 0.9 from 0.8 needs ~199 trials per arm. The
dossier's own conclusion that "the brief's 90 per cent threshold is met in the documented sets only at or
below 5 m/s" [D-24] is therefore an over-reading of a 10-trial experiment: the data are consistent with
90 per cent at 7 m/s and with 70 per cent at 5 m/s. *Observation, with its uncertainty stated.*

**F3. The largest observed difference in onboard-only mean speed is not any vehicle limit — it is
whether the course was known in advance.** Firm numbers: Swift's best three-lap time-to-finish was
17.465 s [new: Kaufmann et al., Nature 2023 author PDF, full-text, "Swift versus human pilots 25
17.465 s 15 10 0.60"] over a 75 m lap [A-10], i.e. **12.88 m/s mean**, onboard sensing and compute, on a
*seen, pre-mapped* track. Against 5 m/s (unseen clutter, onboard, 100 per cent point estimate) and 7 m/s
(80 per cent) [A-20], the ratio is **2.58x**, rising to 4–6x if MonoRace's seen-track mean speed is
13–30 m/s [A-26, A-27; lap length not reported, so I bracketed it]. *Caveat that my method requires: this
is a between-apparatus comparison* — different group, different sensor (RGB + known gate map + T265 vs
stereo depth), different task (gates vs clutter). It is not a controlled perturbation. The within-system
versions of the same effect are [D-18] (all three Swift baselines completed laps with ideal dynamics and
ground-truth state, zero laps under domain shift — *simulation ablation*) and [A-29] (10.0 m/s in the
paper's own simulation vs 5.3 m/s real).

**F4. To buy that same 2.58x through any of the brief's four limits, at the elasticities the dossier
itself computes, you would need absurd hardware.** At e(speed, T/W) = 0.5 [A-34], 2.58x needs T/W ~ 29
(from 4.4). At e(speed, range) = 1.0 (dodge bound) you need 2.6x range; at e = 0.52 (stop bound), 6.2x.
At |e(speed, latency)| = 0.24 you need latency cut by a factor of 52, which is unachievable because tau
cannot go below zero [calc]. *Inference from point-mass bounds, not observation.*

**F5. Sensorimotor latency is observationally the weakest of the candidates, by two independent routes.**
(a) The point-mass stop/dodge bounds give |e(v, tau)| = 0.037–0.24 [A-33], the smallest elasticity in the
dossier. (b) A cross-controller hardware comparison: expert human pilots run ~220 ms sensorimotor latency
against Swift's 40 ms — a 5.5x difference [A-07] — on drones of "the same weight, shape and propulsion"
[D-16], and their best three-lap times were 17.956 / 18.746 / 21.160 s against Swift's 17.465 s [new:
Nature 2023 PDF, full-text]. That is a 2.8–21.2 per cent time penalty for 5.5x the latency, i.e. an
implied |e(speed, tau)| = 0.016–0.122 [calc]. It is a controller swap, not a latency perturbation, so it
bounds the *joint* effect of a 5.5x latency difference — and that bound is small. Two routes, one
point-mass and one hardware, agree on ~0.1. *This is the single strongest quantitative result I have,
and it eliminates latency as the dominant term in the seen-course 11–20 m/s regime.*

**F6. At the speeds where onboard hardware actually fails, the geometric look-ahead requirement is
satisfied several times over.** With tau = 40 ms and a = 40 m/s^2, the required stopping distance is
0.51 m at 5 m/s, 1.65 m at 10 m/s, 5.80 m at 20 m/s [calc]; the D435i used in [A-20] has metres of usable
range. Yet that system was at 80 per cent by 7 m/s and 60 per cent at 10 m/s. Its own paper's
latency-and-range bound was 12.0–13.5 m/s [A-21], so the hardware reached only 0.37–0.58 of its own
computed perception bound and 0.24–0.49 of the point-mass thrust bound (T/W 4.4 over the same 40 m line
gives a mean of 20.5 m/s) [calc]. **Both named bounds overpredict the observed reliable speed by a factor
of 2–4.** Whatever binds is therefore not captured by either bound as written.

**F7. The one perception term that *is* saturated at the observed speeds is angular, not radial.** To
hold altitude while accelerating laterally at a_lat a multirotor must tilt theta = atan(a_lat/g). A
body-fixed forward camera of horizontal FoV H sees its own direction of travel only while theta <= H/2.
For H = 90 deg that fails at exactly 1.00 g; for 115 deg at 1.57 g; for 155 deg at 4.51 g [calc]. At the
4 g a T/W 4.4 platform can produce, the tilt is 76.0 deg — outside a 90 deg camera entirely. This is not
my construction: the [A-20] team tilted their depth camera 30 deg upward above 7 m/s, MonoRace chose a
155 x 115 deg lens [A-26], the 2019 AlphaPilot planner capped acceleration at ~1.2 g "to limit the motion
blur of the camera images" [A-22], and the observed 7 m/s failures are attributed to "objects entered the
field of view very late because of the high angular velocity of the platform" [D-13]. Four independent
engineering choices and one failure attribution all point at the same term, and it is a
*perception-geometry-times-attitude coupling* that none of the brief's four candidates names cleanly.

**F8. No one has ever observed actuator bandwidth binding, and the hardware refutes it.** No paper in the
evidence base argues it [dossier §6: "No paper found arguing that actuator (motor/rotor) bandwidth is the
binding limit"]. The actuator observations are good ones — 39.1 ms thrust time constant on an ATI Mini40
load cell under a 12 N step [A-03], 33 ms rotor-speed time constant [A-04] — but the *same airframe
class* has been flown at 30.0 m/s and 12.58 g [A-12, mocap state] and is quoted at 36.4 m/s [A-02]. A
limit that permits 30 m/s cannot be what caps 5–7 m/s. *Eliminated by direct observation of the same
hardware in a different information regime.*

**F9. Unmodelled aerodynamics is the best-measured model defect and the worst-measured agility limit.**
The numbers are excellent of their kind — positional RMSE 0.232 m (BEM) vs 0.381 m (polynomial fit) on a
slanted circle at 6.92 m/s mean / 10.75 m/s max, force RMSE 0.352–0.365 N, over 1.8 M points from 96
flights [A-18] — but every one of them is a *replay* against motion-capture ground truth, i.e. a
model-error result, not a speed. The controller-side result (>78 per cent tracking-error reduction at up
to 20 m/s and 5 g with INDI plus a drag model) was obtained under motion capture [D-09]. **There is no
hardware experiment in which improving the aerodynamic model raised an onboard-only unseen-course speed.**
That demonstration is also the cheapest missing one in the field (see "What a skeptic would require").

**F10. The field's own sim-to-hardware discount is a factor of ~2.6 in speed and can be total in success
rate.** Measured pairs: 10.0 m/s sim vs 5.3 m/s real on the same compact track [A-29]; 19.4 m/s in
unseen simulated clutter vs 5–8 m/s on unseen real clutter [D-40, A-29] — ratios 1.89, 2.42, 3.88,
geometric mean 2.61 [calc]. In success rate the collapse can be complete: a trajectory-tracking MPC went
44.0 per cent (nominal sim) -> 0.0 per cent (realistic sim) -> 0.0 per cent (real) [A-14]. This is the
base rate my lens needs: **a simulated agility number in this field should be discounted by 2–4x in
speed, and a method's simulated ranking does not predict its hardware ranking** (in [A-14] the
sim-fastest method was the real-world-worst).

**F11. Several of the "best" numbers in the field have a success rate attached that nobody quotes.**
MonoRace's 16.56 s policy, the one behind "speeds up to 100 km/h", succeeded 1 time in 4 (25 per cent,
CP 95 per cent interval [0.006, 0.806]); its reliable policy class ran 38 of 43 = 88.4 per cent [0.749,
0.961] at a ~40 per cent longer lap time [A-27, calc]. The dossier flags that the hardware-vs-simulation
setting of the 4- and 7-trial rows is not certain. Swift's 15 wins in 25 races is a win rate, not a
completion rate [A-10]. *So the field's fastest published onboard numbers are, where counts exist,
single-digit-trial events.*

## Lens-specific outputs

### Observation / inference ledger

| # | Claim | Side | Instrument and conditions | Replication | Uncertainty |
|---|---|---|---|---|---|
| 1 | 8/10 success at 7 m/s, unseen clutter, onboard only [A-20] | **observation** | 890 g quad, Jetson TX2, D435i depth 30 Hz, T265 200 Hz; 40 m reference line; goal within 5 m, no crash | one group, one platform; 56 real experiments in total | CP 95%: [0.444, 0.975] [calc] |
| 2 | 100% at 3 and 5 m/s, same setup [A-20] | **observation** (counts not reported) | as above | same | if n = 10, [0.692, 1.000] [calc] |
| 3 | Swift best three-lap 17.465 s on a 75 m lap -> 12.88 m/s mean, onboard [new: Nature 2023 PDF] | **observation** | 870 g, T/W 4.1, onboard VIO + gate detection; *seen, pre-mapped* track; >300 laps per contestant | one platform, one track | lap length from [A-10]; label mapping on the median panel garbled, so single-lap mean is bracketed 11.0–13.6 m/s |
| 4 | 39.1 ms motor thrust time constant [A-03] | **observation** | ATI Mini40 load cell, 12 N collective-thrust step, first-order fit | single fit, one airframe lineage | no uncertainty quoted; [A-04]'s 33 ms is a different quantity, correlated apparatus |
| 5 | 35 ms command-to-force-onset latency onboard [A-05] | **observation** | agiNuttx FC, same airframe | same group | the >75 ms comparison changes link *and* latency, confounded |
| 6 | +40 ms latency -> +47% position RMSE [A-06] | **observation, confounded** | 400 Hz Vicon, 36 cameras, to 16.7 m/s and 4 g | one sweep | confounded with the radio link; RMSE is not speed |
| 7 | 30.0 m/s peak, 12.58 g on a 0.52 kg T/W 12.35 platform [A-12] | **observation, not onboard** | Vicon + EKF state, trained track | one platform | peak, not a mean; controller evidence only |
| 8 | Aero model error 0.232–0.381 m RMSE at 6.9–10.8 m/s [A-18] | **observation of a model's error** | replay of 96 mocap flights, 1.8 M points | large dataset, one platform | no agility consequence measured |
| 9 | 12.0–13.5 m/s perception-latency speed bound [A-21] | **inference** (simulation/analysis) | pole 1.5 m diameter at 6 m, quad as 0.2 m sphere | — | assumptions: single static obstacle, no estimation error |
| 10 | Elasticities 0.037–1.0 for latency, range, accel, T/W [A-32, A-33, A-34] | **inference** (point mass, own calcs) | closed form, verified by integration | re-derived | ignores rotation time, drag, body-rate limits, estimation error |
| 11 | "All three baselines fail under domain shift" [D-18] | **inference** (simulation ablation) | Swift's simulator | — | quote unverified in the quantitative pass |
| 12 | 19.4 m/s in unseen simulated clutter [D-40] | **inference** (simulation), search-summary | — | — | lead only |
| 13 | Tilt 76 deg at 4 g; travel direction outside a 90 deg FoV above 1.00 g [calc] | **inference, but from exact kinematics**, corroborated by four engineering choices [A-20, A-22, A-26, D-13] | — | — | assumes a body-fixed camera and level flight |
| 14 | Human pilots at 220 ms latency match Swift's lap times on the same airframe [A-07, D-16, new: Nature PDF] | **observation** | same race track, same week, >300 laps each | three pilots, one track | a controller swap, not a latency perturbation |

### Trial-count and resolvability table

| Result | k/n | point estimate | CP 95% interval | Does it settle the 90% criterion? |
|---|---|---|---|---|
| unseen clutter, 7 m/s [A-20] | 8/10 | 0.800 | [0.444, 0.975] | no — 90% not excluded |
| unseen clutter, 5 m/s [A-20] | 10/10 (n assumed) | 1.000 | [0.692, 1.000] | no — 90% not established |
| unseen clutter, 10 m/s [A-20] | 6/10 (n assumed) | 0.600 | [0.262, 0.878] | yes, 90% excluded (below) |
| MonoRace M23, seen track [A-27] | 38/43 | 0.884 | [0.749, 0.961] | no — straddles 90% |
| MonoRace M16, fastest [A-27] | 1/4 | 0.250 | [0.006, 0.806] | yes, 90% excluded (below) |
| RL policy, real, mocap [A-14] | 17/20 (n assumed) | 0.850 | [0.621, 0.968] | no |
| required for a 90% claim | n/n | 1.000 | lower bound 0.90 at n = 29 (one-sided) / 35–36 (two-sided) | this experiment has never been run |

### Base rates

- **In-field, simulation -> hardware speed:** discount factor 1.89, 2.42, 3.88; geometric mean **2.61**
  [calc, from A-29 and D-40]. A simulated agility claim in this field survives contact with hardware at
  roughly 40 per cent of its headline speed.
- **In-field, simulation -> hardware ranking:** fails. The sim-fastest controller in [A-14] was 0 per cent
  in the real world; all three of [D-18]'s baselines went from completing laps to completing none under
  domain shift; learned policies "trained on specific environments often crash immediately in unseen
  configurations" [D-17].
- **In-field, seen -> unseen course:** no system has carried its seen-course speed to an unseen course.
  The gap is 2.6–6x [F3].
- **Reference class outside the field.** Anomalous-thrust claims: TU Dresden's re-test attributed the
  apparent EmDrive thrust to a thermal artefact and reported it refuted "by at least 3 orders of
  magnitude" [new: Wikipedia / Universe Today / Big Think via web search, search-summary, SUMMARY "We
  found out that the cause of the 'thrust' was a thermal effect ... Our measurements refute all EmDrive
  claims by at least 3 orders of magnitude"]. Room-temperature superconductivity claims of 2020–23 did
  not replicate (background, uncited here). The pattern in both: the headline survived only until an
  independent group varied the one condition the original had held fixed. The analogous untested
  condition here is **the course**, and the analogous untested instrument is **trial count**.
- **The reference class this question actually sits in,** though, is not an anomaly but an engineering
  attribution: "which of four limits binds". Those are usually settled by a one-factor-at-a-time sweep on
  one apparatus, and in this field **no such sweep exists** [dossier §6]. Historically, attributions made
  without the sweep have a poor record — compare [A-14], where a paper's own simulated ranking inverted on
  hardware.

### Analogues

- **The human pilot is the best available analogue of "same hardware, different controller".** 5.5x the
  latency, 4x the camera rate, a vastly better world model, comparable lap times [F5]. This says the
  40–220 ms band of sensorimotor latency is not where the agility of this airframe class is decided, and
  that what the human brings — knowing the track, and a policy that degrades gracefully — is worth more
  than the latency he gives up.
- **Event cameras as the latency analogue:** 12 ms estimator latency at 1 kHz tracking >1600 deg/s, but on
  a **1-DOF dualcopter**, not a quadrotor [A-23]; onboard quadrotor tree avoidance at only 5 m/s, with
  success *improving* as speed rose from 1 to 5 m/s [A-30]. If latency were binding, the 300x sensor
  latency advantage [A-24] should already have shown up as speed on a quadrotor. It has not. This is the
  analogue that most directly undercuts the latency candidate.
- **Fixed-camera FoV and manoeuvre tilt** is a known constraint in other aerial and automotive systems
  (gimbals, wide-angle front cameras, and the general practice of widening FoV rather than range). Here it
  reappears quantitatively: 1.00 g for a 90 deg lens [F7].
- **Analogue from power electronics / sampled control generally:** adding a predictor buys back
  measurement delay to the accuracy of the model [D-35], and a 2019 racing system did exactly that for
  ~130 ms [A-22]. So latency is partly *purchasable*, which is another reason it is not the hard limit;
  range and reliability are not purchasable the same way.

### What a skeptic would require

| Candidate | Evidence a skeptic would demand | Does it exist? |
|---|---|---|
| Actuator/rotor bandwidth binds | Two otherwise identical vehicles differing only in motor time constant (e.g. 39 ms vs 20 ms), flown on the same unseen course, >= 30 trials each | **No.** And no paper even argues the claim [dossier §6] |
| Estimation latency binds | A one-factor latency injection (10/20/40/80 ms) into an onboard loop, same vehicle, same unseen course, speed-at-90-per-cent-success as the output | **No.** [A-06] injected latency but measured mocap tracking RMSE, and confounded it with the radio link |
| Unmodelled aerodynamics binds | Same vehicle, same policy, aero model on vs off, onboard-only, unseen course, success-vs-speed curves | **No.** All aero evidence is replay [A-18] or mocap-controller [D-09] |
| Perception range binds | Sensor range swept (3/6/12 m) with FoV and latency held fixed, unseen course, >= 30 trials per setting | **No.** The nearest is [A-21], a simulated bound, which the same paper's hardware missed by 2–3x [F6] |
| Perception FoV x attitude binds | Same vehicle, same policy, lens swapped 90 -> 155 deg (or gimbal/camera-tilt swept), unseen course | **No**, but three systems *chose* the wide or tilted option [A-20, A-26] and one failure mode is attributed to it [D-13] |
| Course knowledge (prior map) binds | One system, one platform, one day: the same track flown with and without the gate map in the loop, >= 30 trials each | **No.** This is the cheapest decisive experiment in the whole question: one existing platform, one afternoon, ~60 flights, no new hardware |
| "No single limit dominates" | Any of the above sweeps showing two elasticities within a factor of two | Partly: the *computed* elasticities for range (0.52–1.0), acceleration (0.43–0.48) and T/W (0.50–0.565) already sit within a factor of 2.3 [calc] |

Cost note, as my method requires. Of the seven rows above, five need no hardware that does not exist:
an Agilicious-class platform, an afternoon, and 30–60 logged flights per condition (the 90 per cent
criterion needs n >= 29 per condition [F2]). The expensive ones are the ones nobody has done, and they
are expensive only in flight-test discipline, not in money: on a rough reckoning, a racing airframe plus
spares and an onboard compute module is a low-five-figure USD capital item that several labs already own.
**The reason the question is open is not that the experiment is hard; it is that nobody has run a
one-factor-at-a-time sweep and published the success-vs-speed curves.**

## Calculations

| File | What it computes | Key results |
|---|---|---|
| `runs/2026-10-15-quadrotor-agility-limit/calc/lens-empiricist_observations.py` | (1) exact Clopper–Pearson intervals on every reported hardware success rate; (2) trials needed for a 90 per cent claim; (3) mean speeds of the onboard demonstrations; (4) observed speed as a fraction of its own published bounds; (5) measured sim-to-hardware discount; (6) all elasticities on one axis; (7) observed elasticity of lap time to sensorimotor latency; (8) latency's share of the required look-ahead; (9) tilt required to accelerate vs camera FoV | 8/10 -> [0.444, 0.975]; n = 29 (one-sided) or 35–36 (two-sided) for a 90 per cent claim; 199 trials/arm to tell 0.9 from 0.8; Swift 12.88 m/s mean (seen course, onboard); seen/unseen ratio 2.58–6x; observed speed = 0.37–0.58 of the perception bound and 0.24–0.49 of the point-mass thrust bound; sim-to-real speed discount geometric mean 2.61; \|e(speed, tau)\| = 0.016–0.122 from the human-vs-Swift comparison; latency is 5–24 per cent of the required stopping distance above 5 m/s; travel direction leaves a 90 deg FoV at exactly 1.00 g, a 155 deg FoV at 4.51 g |

Verification inside the script: the Clopper–Pearson solver matches the closed form 0.025^(1/n) for k = n
to 4e-13 at nine values of n; the bang-bang distance closed form matches numerical integration to
7.9e-14 relative with final speed 5e-15 m/s; atan(1) = 45.000 deg.

## Candidate answers

- [EMP-A] **On hardware as of 2026, what binds first in the brief's own metric is not a vehicle bandwidth
  but the vehicle's prior information about the course: the required look-ahead term, in the specific form
  of a prior map or trained track.** | status: **surviving** | why: it is the only limit whose relaxation
  has ever been observed to move mean speed by more than a factor of two on onboard-only hardware —
  12.88 m/s seen [new: Nature 2023 PDF, F3] vs 5–7 m/s unseen [A-20]; every fast onboard result is on a
  pre-mapped or trained track [D-11, D-23]; Swift repairs VIO drift *with the known track layout* [D-12];
  and the computed elasticities say no admissible change in thrust, range or latency could buy the same
  factor [F4]. Weakness my method must concede: the 2.58x is a between-apparatus comparison, and the two
  tasks (gates vs clutter) are not the same task. | test: one platform, one day, same track flown with
  and without the gate map in the loop, >= 29 trials per condition; if the speed-at-90-per-cent-success
  falls by less than ~30 per cent, EMP-A is refuted. | confidence: medium
- [EMP-B] **Null: no single limit dominates in this class; the observations do not separate perception
  range, achievable acceleration and thrust-to-weight, and the metric itself is unmeasured.** | status:
  **surviving** | why: the computed elasticities for range (0.52–1.0), braking/lateral acceleration
  (0.43–0.48) and T/W (0.50–0.565, including the one hardware-anchored planner sweep [A-16]) lie within a
  factor of 2.3 of each other [calc], which is the brief's own "factor of two" condition for declaring no
  dominance; no theorem ranks the four [dossier §6]; no one-factor-at-a-time sweep exists; and the
  hardware falls 2–4x short of *both* named bounds [F6], which is what you expect when several
  partially-saturated terms and a reliability floor act together rather than one binding constraint. |
  test: any single one-factor sweep that produces an elasticity above ~1.0 for one limit while the others
  stay below 0.5 refutes it. | confidence: medium-high
- [EMP-C] **Reframe: the metric as posed is not yet an observable, so "which binds first" is at present a
  question about models, not about vehicles.** | status: **surviving** (and it is the honest reading of my
  ledger) | why: no source reports the three required conditions together [dossier preamble]; the best
  unseen-course dataset is 10 trials wide, which cannot distinguish 80 from 90 per cent [F2, needing 199
  trials/arm]; and the field's simulated numbers carry a measured 2.6x discount and do not even preserve
  the *ranking* of methods [F10]. Until success-vs-speed curves with n >= 29 per point exist, every
  ranking of the four limits is an inference from a point-mass bound or a simulator. | test: publication
  of any unseen-course success-vs-speed curve with stated trial counts converts this from a reframe into
  an answerable question; the A2RL / identical-hardware series [D-41, A-31] could produce one by
  construction. | confidence: high
- [EMP-D] **The binding perception quantity is angular, not radial: field of view multiplied by the
  attitude the vehicle must adopt to accelerate (plus motion blur), not range in metres.** | status:
  **surviving but under-tested** | why: the required stopping distance at the speeds where hardware fails
  is 0.5–2.9 m, far inside the sensor's range [F6], so range is not saturated — but the direction of
  travel leaves a 90 deg lens at exactly 1.00 g and a 155 deg lens at 4.51 g [calc, F7], and the observed
  failures at 7 m/s are attributed to objects entering the FoV late because of body angular velocity
  [D-13], with three systems independently widening or tilting the camera [A-20, A-26] and one planner
  capping acceleration at ~1.2 g explicitly for motion blur [A-22]. | test: lens swap (90 -> 155 deg) or a
  gimbal, same vehicle, same policy, unseen course; predicted large gain for EMP-D, little for EMP-F. |
  confidence: medium
- [EMP-E] **State-estimation *latency* binds first.** | status: **eliminated, in the band that exists** |
  why: two independent routes give |e(speed, tau)| ~ 0.1 — the point-mass bounds (0.037–0.24, [A-33]) and
  the human-vs-Swift hardware comparison (0.016–0.122 for a 5.5x latency difference, [F5]); latency is
  only 5–24 per cent of the required look-ahead distance above 5 m/s [calc]; a 300x-lower-latency sensor
  has produced 5 m/s, not 50 [A-30, A-24]; and delay is partly purchasable by prediction [D-35, A-22]. The
  claim that survives this elimination is a *different* one — estimation **reliability** (VIO drift and
  outright divergence under motion blur) — which is a discrete failure mode, not a bandwidth, and is
  named by competitors in the minimal-sensor regime [D-19] and by MonoRace's own authors ("does not
  accurately model vision-based state estimation errors that occasionally caused real-world crashes"
  [A-28]). | test: a latency-injection sweep with speed-at-90-per-cent-success as the output; |e| > 0.5
  would reinstate it. | confidence: medium-high for the elimination of the latency form
- [EMP-F] **Rotor and actuator bandwidth (or thrust-to-weight) binds first.** | status: **eliminated** |
  why: the same airframe class flies at 30.0 m/s and 12.58 g [A-12] and is specified to 36.4 m/s [A-02],
  so a limit that permits 30 m/s is not what caps 5–7 m/s; observed speeds are 0.24–0.49 of the
  point-mass thrust bound on the very course where they were measured [F6]; the elasticity is ~0.5
  measured two ways [A-16, A-34]; planners deliberately stay *inside* the thrust bound for controllability
  [D-36]; and no paper argues the claim [dossier §6]. The actuator measurements themselves (39.1 ms,
  [A-03]) are among the best observations in the dossier — they just do not bind. | test: the motor-swap
  experiment above; it has never been run, and I expect it to show |e| <= 0.6. | confidence: high
- [EMP-G] **Unmodelled aerodynamics binds first.** | status: **strained** | why: it is the dominant *model*
  defect, measured well and repeatedly [A-18, D-08], and model error is the named cause when plan-then-
  track controllers collapse [D-14]; but there is no hardware experiment in which a better aero model
  raised an onboard-only unseen-course speed, and the demonstrated fix was obtained under motion capture
  [D-09]. By my method this is a model-error result awaiting its agility demonstration. Its strongest
  form is not "aerodynamics" but "model error mediated by controller structure" [D-21(b)], which is
  closer to EMP-B than to a single binding limit. | test: aero-model-on/off, onboard-only, unseen course,
  n >= 29 per point; a > 30 per cent shift in the 90-per-cent speed would move it to surviving. |
  confidence: medium

Mutually exclusive on "which dominates": EMP-A, EMP-D, EMP-E, EMP-F, EMP-G are rivals; EMP-B is their
negation; EMP-C says the contest is currently undecidable by observation. My method ranks them
EMP-C ~ EMP-B > EMP-A > EMP-D > EMP-G > EMP-E > EMP-F.

## What would change my mind

1. **A latency-injection sweep on an onboard loop with speed-at-90-per-cent-success as the output.** If
   |e(speed, tau)| came out above 0.5, F5 and EMP-E's elimination both fail, because my two routes to
   ~0.1 are a point-mass bound and a cross-controller comparison, neither of which is a perturbation.
2. **A single unseen-course result at >= 15 m/s with n >= 29 and no prior map.** That would refute EMP-A
   directly and make EMP-C obsolete. The identical-hardware series [D-41] could produce it within months
   of this run's date.
3. **Trial counts for [A-20] at 3, 5 and 10 m/s.** If the 5 m/s row is 30/30 rather than 10/10, F2's
   central complaint weakens considerably and [D-24] becomes defensible.
4. **A measured end-to-end VIO latency *and* drift in m/m at 15–30 m/s.** The dossier has neither
   [§6], and the reliability form of EMP-E stands or falls on them.
5. **The published MonoRace version** [doi:10.1126/scirobotics.aee9250], which would tell whether the
   1-of-4 and 5-of-7 rows are hardware or simulation [A-27]. If they are simulation, the only
   high-speed onboard success rates in the evidence base vanish and F11 strengthens.
6. **A gimbal or wide-FoV ablation.** If swapping a 90 deg lens for a 155 deg one changes nothing, EMP-D
   is dead and the FoV coincidences in F7 were coincidences.

## Assumptions I relied on

- **Trial counts I had to assume:** n = 10 per speed for [A-20]'s 3, 5 and 10 m/s rows (by analogy with
  the reported 8/10 at 7 m/s) and n = 20 for [A-14]'s real-world rows. The dossier says both are
  unsupported (§7). Those rows are illustrative of a 10- or 20-trial experiment's resolving power, not of
  a stated interval. The 8/10, 38/43, 5/7 and 1/4 rows are as reported.
- **The human-vs-Swift lap times in F5** come from the paper's head-to-head table, whose extracted text
  reads "A. Vanover versus Swift 9 17.956 s4 5 0.44 / T. Bitmatta versus Swift 7 18.746 s3 4 0.43 /
  M. Schaepper versus Swift 9 21.160 s3 6 0.33 / Swift versus human pilots 25 17.465 s 15 10 0.60" under
  a column headed "Best time-to-/f_inish" [new: Kaufmann et al., Nature 2023 author PDF, full-text].
  Reading the three first numbers as each *pilot's* best three-lap time and 17.465 s as *Swift's* is my
  interpretation of that table; if instead they are the best time in each matchup regardless of
  contestant, the implied latency elasticity in F5 is smaller still, not larger, so the finding's
  direction is safe either way.
- **Swift's mean speed** uses the 75 m lap length from [A-10] with the 17.465 s best three-lap time I
  read from the paper. If the "lap" in [A-10] is not the distance flown per lap, 12.88 m/s is wrong in
  proportion. The single-lap median panel's label order was garbled in PDF extraction, so I bracketed it
  (11.0–13.6 m/s) rather than assign medians to contestants.
- **MonoRace lap length is unknown,** so its mean speed is a bracket over 100–250 m laps (8.7–30.2 m/s),
  not a number.
- **Independence:** [A-01]–[A-06], [A-07]–[A-10], [A-16]–[A-18] and [A-20]–[A-21] share one group's
  platform lineage (§7). I treated the seen/unseen comparison as between-apparatus for exactly this
  reason, and I did not average correlated results.
- **The elasticities I compare are point-mass results** ([A-32]–[A-34]) and inherit their assumptions:
  level flight, no drag, no rotation time, no body-rate limit, a single static obstacle, perfect state.
  They sit on the inference side of my ledger throughout, and the only one with a hardware anchor is the
  T/W elasticity [A-16], itself from a planner sweep under motion capture.
- **The FoV argument assumes a body-fixed camera and altitude-holding flight.** A gimbal, a tilted mount
  or a deliberate climb changes the geometry; [A-20]'s 30 deg tilt is precisely that mitigation.
- I did not read the other lenses' files, and I computed my own numbers where the brief assigns a
  calculation to another lens (the time-optimal denominator and the delay margin are the simulator
  lens's; I used the dossier's [A-32]–[A-34] rather than redo them).
