# Analysis: examiner (Socrates — examine the question before answering it)
status: final

## Method applied

Take the question apart before answering it: define each loaded term ("closed-loop agility", "binds
first", "limit", "onboard only"), test whether each definition survives, test each hidden premise
against the dossier and against calculation, and look for a better-posed nearby question. The
brief's own test for "binds first" is a partial derivative, so the first thing to check is whether
the variables are separable enough for one to exist; the second is whether the metric it acts on is
measurable at all.

## Findings

**F1. The agility metric's denominator is non-causal, so the ratio it defines is not a property of
the vehicle.** The brief asks for "the fraction of the platform's own time-optimal traversal time"
on a course "it has not seen before". The time-optimal traversal time is computed with the whole
course known; the vehicle has only its look-ahead. The ratio therefore adds a *dynamics* deficit
(the vehicle cannot fly its own optimum) to an *information* deficit (it does not know where the
course goes), and no hardware change removes the second term. The dossier records that the two
families of result in this field do not even agree on what generalisation names [D-23], and that
the fastest onboard results repair drift against a *known* track layout [D-11]. Repair: report two
denominators — the full-information optimum and the optimum of a receding-horizon planner limited
to the vehicle's actual look-ahead distance.

**F2a. Hidden premise 2 (separability) fails exactly, not approximately, in the perception regime.**
For the stop-before-obstacle bound v = a(-tau + sqrt(tau^2 + 2s/a)) [D-32, A-33], v is homogeneous
of degree 1 in (s, a) jointly: v(ks, ka, tau) = k v(s, a, tau) to machine precision at k = 1.37 on
all four dossier parameter cases, so e_s + e_a = 1.000 identically, and e_s/e_a lies in
1.155–1.221 across those cases [calc: runs/2026-10-15-quadrotor-agility-limit/calc/lens-examiner_structure.py].
Perception range and braking acceleration (hence thrust-to-weight) are near-perfect substitutes in
this bound. "Which of these two binds first" has no answer: the bound depends on the product a*s,
and a 1 per cent gain in either buys the same 0.5 per cent of speed. The latency elasticity in the
same cases is -0.036 to -0.100, i.e. 5–15 times smaller.

**F2b. The partial derivative the brief asks for is not an operation available on hardware: s
depends on a.** Level-flight pitch for horizontal acceleration a is atan(a/g) — 45.0 deg at 1 g,
63.9 deg at 2.04 g, 75.5 deg at 3.87 g [calc]. With a forward-pointing 90 deg-HFoV depth camera
(the D435i class used in the best-documented unseen-course result, A-20), the flight direction
leaves the field of view at exactly 1.00 g of braking; the usable stop bound at s = 6 m then caps
at sqrt(2 * 9.81 * 6) = 10.85 m/s. The A-20 system tilts its camera 30 deg up above 7 m/s, which
raises the limit to 3.73 g and 20.96 m/s [calc; A-20, which states the tilt]. That the authors
engineered the tilt is evidence the coupling is real, and D-13's attribution of the 7 m/s failures
to "objects entered the field of view very late because of the high angular velocity of the
platform" is the same effect. So ds/da < 0 through attitude, and "relaxing one limit holding every
other limit fixed" is not well defined for this pair. Suggestive, not decisive: the untilted figure
10.85 m/s falls where A-20's success drops to 60 per cent (10 m/s).

**F3. Hidden premise 4 answered with a number: thrust-to-weight is not the answer, in elasticity
terms.** At the onboard-only platforms' T/W of 4.1–4.5 [A-13], a_h = g sqrt(TWR^2 - 1) = 39.0–43.0
m/s^2; rest-to-rest bang-bang over a 10.7 m gate spacing (75 m lap / 7 gates, A-10) gives mean
speed 10.21–10.73 m/s and peak 20.4–21.5 m/s. d ln a_h / d ln TWR = 1.063 at T/W 4.1 (closed form
matched numerically to 1.2e-11) and d ln v / d ln a_h = 0.500 exactly, so d ln v / d ln TWR =
0.532 — within 6 per cent of the published planner sweep's 0.565 [A-16] on a real track, which is
the only empirical elasticity in the evidence base [calc].

**F4. No single-limit bound is active at the demonstrated onboard-only unseen-course speeds.** Ten
bounds computed from the dossier's own anchors range from 10.73 m/s (thrust bang-bang mean, T/W
4.5) to 32.72 m/s (delay bound at 40 ms, R = 5 m, m = 3). The best-documented onboard-only result
with 100 per cent success on unseen clutter is 5 m/s [A-20], which is 0.47 of the *lowest* bound
and 0.15 of the highest; the 80 per cent point at 7 m/s is 0.21–0.65; the 60 per cent point at 10
m/s is 0.31–0.93 [calc]. A system operating at a quarter to a half of every limit is not limited by
any of them. The one demonstrated number that does reach the bounds is the *seen*-track peak of
32.2 m/s [A-26], which is 0.98–3.00 of them — consistent with seen-track flight being
hardware-limited and unseen-course flight not being.

**F5. The latency candidate, mapped to a speed, is inactive by a factor of 3–6, and plausibly was
active in 2019.** tau_eff = 40 ms [A-07] permits wc <= 19.63 rad/s (3.12 Hz) [A-32]. Mapping to
speed by requiring the position-loop crossover to exceed m times the course's characteristic
frequency v/R (my own construction, labelled as such) gives 19.6–32.7 m/s at R = 5 m for m = 5 and
3. The latency that would make this bind at 7 m/s is 112–187 ms; at 10 m/s, 79–131 ms [calc].
Retrodiction: the 2019 onboard racing system had about 130 ms estimation latency and its planner was
illustrated with a +/-7.5 m/s velocity cap [A-22]; the same construction at 130 ms gives 6.0–10.1
m/s. So the mapping reproduces the one historical case where a team chose a cap, and says the
40 ms and 17 ms systems of 2023–26 [A-07, A-28] are nowhere near it.

**F6. The human-pilot comparison all but eliminates latency, and the elimination survives
disaggregation.** Swift's sensorimotor latency was 40 ms against about 220 ms for the expert
pilots, on drones of "the same weight, shape and propulsion"; Swift was globally faster but "not
faster on all individual segments" [D-16, A-07]. A 5.5-fold latency penalty therefore costs a human
a few per cent of lap time, not a factor. The obvious objection is that the human's 220 ms is a
different loop; it is, and that strengthens the argument: racing pilots fly in acro/rate mode, where
the inner angular-rate loop is closed onboard from the gyro and the stick commands a rate
[new: oscarliang.com and unmannedtechshop.co.uk via WebSearch, search-summary, SUMMARY "Acro mode
is rate control: the stick controls the drone's angular velocity of rotation instead of the angle;
self-levelling modes use gyro and accelerometer, rate mode uses only the gyro; most racing pilots
settle in acro"]. The human's 220 ms thus sits in the *outer* position/path loop — which is exactly
where VIO latency sits too. Same loop, 5.5 times the delay, comparable speed.

**F7. "Unmodelled aerodynamics" is not a limit of the vehicle; it is a sensitivity of one pipeline.**
On one track with one model error, trajectory-tracking MPC went from 4.92 s / 44 per cent in
nominal simulation to 0 per cent under a realistic model and in the real world, while an RL policy
held 85 per cent at 5.35 s [D-14, A-14]; the named causes are aerodynamic effects, variable system
delay and battery-voltage fluctuation. A quantity whose effect on the metric can be moved from
fatal to tolerable by rewriting software, with the airframe untouched, is not a hardware limit. The
best aerodynamic-modelling result in the evidence base is likewise a model-error result, not a speed
gain: positional RMSE 0.8 m -> below 0.3 m on replayed motion-capture flights [D-08].

**F8. The metric the brief defines has never been measured because it is unaffordable, and that is
checkable.** To certify p >= 0.90 at 95 per cent one-sided confidence needs 29 consecutive successes
(0.05^(1/29) = 0.9019; 0.05^(1/28) = 0.8985) [calc]. What the evidence base actually certifies, as
one-sided 95 per cent lower bounds: 10/10 -> 0.741; 8/10 -> 0.493; 6/10 -> 0.304; 38/43 -> 0.771;
5/7 -> 0.341; 1/4 -> 0.013 [calc, on the counts in A-20 and A-27]. So *no* published onboard-only
point estimate establishes 90 per cent at any speed, including the 5 m/s one. Discriminating a true
0.90 from a true 0.80 needs about 69 trials for 0.75 power and 100 for 0.87 (exact binomial) [calc];
the metric is a supremum over speeds, so 3–5 set-points cost 87–145 flights for bare certification
and 207–345 for discrimination. At the crash rates involved that is tens of airframe rebuilds. This
is the mechanical explanation of D-24.

**F9. "Onboard only" is the one term in the brief that is sharp, and it cuts the evidence base to
two platforms.** It excludes the T/W 12.35, 30 m/s, 12.58 g platform [A-11, A-12] and the real-world
rows of A-14, all of which used Vicon [D-14]. What remains is seen-track minimal-sensor racing
[A-26/A-27/A-28] and unseen-clutter depth flight [A-20, A-29], and the dossier warns that A-01 to
A-06, A-07 to A-10, A-16 to A-18 and A-20 to A-21 share one group's platform lineage (§7). Any
answer to reading (a) rests on two genuinely independent apparatus.

**F10. Elasticity and attainable increment give different rankings, so "binds first" has two
answers.** +10 per cent on each limit at the Swift-like operating point (s = 6 m, a = 39 m/s^2,
tau = 40 ms, v = 20.13 m/s): range +5.23 per cent, braking/thrust +4.51 per cent, latency (-10 per
cent) +0.66 per cent. Per *demonstrated attainable move*: T/W 4.1 -> 12.35 (a platform that exists,
A-11) +66.6 per cent; s 6 -> 20 m (LiDAR class, D-39) +88.6 per cent; s 6 -> 10 m +31.2 per cent;
tau 40 -> 17 ms +4.2 per cent; and tau -> 0, which is unattainable, only +7.5 per cent [calc].
Latency's entire remaining headroom on this bound is under 8 per cent. Elasticity says range ~ thrust
>> latency; engineering effort says the same, more strongly. Nothing in either ranking puts
estimation latency or actuator bandwidth first.

## Lens-specific outputs

### Term ledger: does each loaded term survive scrutiny?

| Term | Definition as given | Survives? | Repair |
|---|---|---|---|
| closed-loop agility | max mean speed on an unseen course at >= 90 per cent success, plus fraction of platform time-optimal | **No** | Denominator is non-causal (F1) and the 90 per cent clause is unmeasurable at published n (F8). Use: (i) mean speed with a Clopper-Pearson lower bound at a stated n; (ii) fraction of a *receding-horizon* optimum at the vehicle's own look-ahead; (iii) fraction of the full-information optimum, reported separately |
| binds first | the limit whose relaxation, holding others fixed, moves the metric most; stated as an elasticity | **No, as a partial derivative** | ds/da < 0 through body attitude and FoV (F2b), and e_s + e_a = 1 identically in the stop bound (F2a). Use directional derivatives along *attainable* engineering moves (F10), or name the active constraint and admit that non-active constraints have elasticity exactly zero |
| limit | rotor bandwidth / estimation latency / unmodelled aerodynamics / perception range | **Not a single kind** | Three are hardware quantities; "unmodelled aerodynamics" is a model error that only binds through a controller (F7). Split into hardware constraints, model-error sensitivities and architecture choices |
| onboard only | all sensing and compute on the vehicle; trained policies allowed | **Yes** | None needed; it is the brief's sharpest definition and it is what makes the evidence base small (F9) |
| unseen course | a course it has not seen before | **No** | "Unseen" is a distribution, not a binary. Specify the course distribution and the magnitude of shift; otherwise the metric is not a number [D-17, D-23] |
| per cent change in the limit | dimensionless elasticity | **Partly** | Dimensionless but not effort-normalised: 1 per cent of 40 ms is 0.4 ms, 1 per cent of 6 m is 6 cm. These are not comparable engineering acts (F10) |

### Hidden-premise test table

| Premise | What supports it | What would falsify it | What the question becomes if false |
|---|---|---|---|
| 1. One limit dominates | A min-of-constraints structure does have a unique active constraint | Bounds clustering within a factor of ~2 at the operating point; or all bounds far above the operating point | If all bounds are far above (F4): "what keeps the vehicle at a quarter of its limits?" — an engineering-competence question, not a physics one. My bounds span 10.73–32.72 m/s, a factor of 3.0, and the two lowest (thrust bang-bang 10.73, FoV-capped stop 10.85) agree to 1.1 per cent — a near-degeneracy in the 10–11 m/s band |
| 2. The limits are separable | They have independent datasheet values | e_s + e_a = 1 identically (F2a); ds/da < 0 (F2b) | **Falsified.** The question becomes "what is the binding *product*?" — usable look-ahead at the attitude the manoeuvre requires, times available braking |
| 3. The limit may be in the task | The metric is defined on an unseen course, so look-ahead is part of the task | A system reaching the same speed on unseen and seen courses | Partly true: the seen/unseen split is the largest single discriminator in the data (32.2 m/s seen vs 5.0–8 m/s unseen, A-26 vs A-20/A-29) — a factor of 4–6, larger than any within-vehicle elasticity |
| 4. T/W is not simply the answer | Elasticity 0.53 is modest and the published sweep agrees at 0.565 | A T/W-12 onboard-only system flying ~1.7x faster on unseen courses | Supported as stated: T/W is not the elasticity answer (F3). But it is the largest *attainable* move (+67 per cent, F10), and nobody has flown it onboard-only — a loud silence |
| 5. Published speeds measure the asked quantity | — | — | **Falsified by the dossier itself** (metric warning; D-23, D-24). No source reports all three components |
| 6. The autonomy gap is a limit of the same kind | Human pilots fly these airframes fast | A human with 5.5x the loop delay matching autonomous speed | **Falsified for latency** (F6). The gap is in the outer loop's *content* (what to do), not its delay |

### A reframe that is better posed

Replace "which limit binds first on closed-loop agility" with:

> **On one airframe, with the pipeline held fixed, which single intervention — raising usable
> look-ahead at manoeuvring attitude, raising thrust-to-weight, cutting outer-loop latency, or
> replacing the plan-then-track architecture with a task-objective policy — raises the mean speed
> at which a 29-flight unseen-course run completes without a crash?**

This is better posed because: it names interventions rather than abstract limits, so the derivative
exists; it fixes the confidence requirement at the cheapest level that certifies 90 per cent (F8);
it drops the non-causal denominator (F1); and it puts the architecture arm on the same footing as the
hardware arms, which the original question's four-way choice does not allow even though D-14 shows
the architecture arm is worth 0 per cent vs 85 per cent on identical hardware.

It also has a clearer answer: the two large arms are look-ahead-at-attitude and thrust (F10), the
architecture arm is the only one with a measured 85-point swing [A-14], and latency is capped at
+7.5 per cent even if driven to zero.

### The ten hardest questions any proposed answer must survive

1. Name one onboard-only system whose unseen-course success rate has a 95 per cent lower confidence
   bound at or above 0.90 at any speed. (Current best: 10/10 -> 0.741, F8.) If none exists, on what
   is the ranking of limits being computed?
2. If thrust-to-weight is not binding, why does a demonstrated T/W 12.35 airframe [A-11] exist while
   every onboard-only result runs at 4.1–4.5? If it *is* binding, why has nobody taken the free
   +67 per cent (F10)?
3. State the physical operation that raises usable perception range by 10 per cent while holding
   braking acceleration and latency fixed on a real airframe. If you cannot, the brief's elasticity
   is undefined (F2b).
4. How does a pilot with about 220 ms of outer-loop latency fly within a few per cent of a 40 ms
   autonomous system, if 40 ms of latency is what binds (F6)?
5. Is a 1 per cent change equally costly across latency, range, thrust and aerodynamic model error?
   Give the cost per per cent. If they differ by an order of magnitude, elasticity is the wrong
   ranking criterion (F10).
6. Which denominator is the "fraction of time-optimal"? Computed with the course known, or with the
   vehicle's look-ahead? What fraction of the shortfall is informational rather than dynamic (F1)?
7. Does the answer change when only the software changes? A-14 says the same hardware and the same
   aerodynamic error give 0 and 85 per cent. In what sense is the limit then in the vehicle (F7)?
8. At what speed does your candidate's bound cross the operating point, and is the operating point
   currently at 0.2 or at 0.9 of it? A candidate whose bound sits at 4x the demonstrated speed is
   not binding (F4).
9. What is the measured end-to-end VIO latency (exposure to pose) and drift in m per m at 10 m/s?
   The dossier records both as not retrieved (§6); every latency claim rests on one system's 40 ms
   sensorimotor figure.
10. Over what distribution of courses is "unseen" defined, and what is the shift magnitude? Without
    it the metric is a number only relative to one course set [D-17, D-23].

### Decisive experiment that separates the candidates

A five-arm ablation on one airframe, with the agility metric measured as 29 consecutive unseen-course
runs per speed set-point: (i) baseline; (ii) wide-FoV or gimbal-stabilised camera, attacking
look-ahead-at-attitude (F2b); (iii) T/W raised 4.1 -> 8 (thrust arm); (iv) tau_eff cut 40 -> 15 ms
with event camera or faster compute (latency arm); (v) plan-then-track replaced by a task-objective
policy (architecture arm). Predicted outcome if EXAMINER-A holds: arm (v) >> arms (ii), (iii) >>
arm (iv), with arm (iv) under 10 per cent. Cost: of order 150–400 flights, a few airframes'
attrition, plausibly USD 50–150k and a few months for a group that already has the stack — UZH RPG,
TU Delft MAVLab, or an A2RL team. The November 2026 identical-hardware final [D-41] is the natural
venue for arms (ii)–(v) if organisers mandate onboard compute.

## Calculations

- `runs/2026-10-15-quadrotor-agility-limit/calc/lens-examiner_structure.py` (log beside it).
  Sections: (A) T/W acceleration ceiling and bang-bang mean speed, with elasticities — a_h =
  39.0–43.0 m/s^2 at T/W 4.1–4.5, v_mean 10.21–10.73 m/s over 10.7 m, d ln v/d ln TWR = 0.532;
  (B) stop and dodge bounds with elasticities and the homogeneity identity e_s + e_a = 1.000,
  e_s/e_a = 1.155–1.221, e_tau = -0.036 to -0.100; (C) pitch-for-acceleration and the FoV cutoff
  a_fov = 9.81 m/s^2 (90 deg, untilted), 36.61 m/s^2 (90 deg + 30 deg tilt), 44.25 m/s^2 (155 deg),
  giving FoV-capped stop speeds 10.85 / 20.96 / 23.04 m/s at s = 6 m; (D) delay-limited bandwidth
  mapped to speed, 19.6–32.7 m/s at 40 ms and 6.0–10.1 m/s at 130 ms, with the binding latency
  112–187 ms at 7 m/s; (E) ten bounds against five demonstrated speeds, ratios 0.15–0.47 at 5 m/s;
  (F) binomial trial economics, 29 consecutive successes to certify 0.90, lower bounds 0.741 (10/10)
  and 0.493 (8/10), 69–100 trials to discriminate 0.90 from 0.80; (G) equal-per-cent (+5.23 / +4.51 /
  +0.66 per cent for range / thrust / latency) versus equal-attainable-increment (+88.6 / +66.6 /
  +4.2 per cent) sensitivity.
  Verification printed in the log: closed-form stop bound against direct integration (3 cases, max
  disagreement 5.1e-4 m/s), the tau -> 0 limit against sqrt(2as) (exact to 4 decimals), elasticities
  against closed forms (match to 1e-11), homogeneity against k-scaling at k = 1.37 (diff 0.0),
  Clopper-Pearson k = n against the closed form 0.05^(1/n), and the normal-approximation sample size
  against an exact binomial power calculation (n = 69 -> power 0.750).
  Left out: rotor and motor lag, drag, rotation time between manoeuvres, body-rate limits, battery
  sag, estimation error, multiple and occluding obstacles, gate geometry, and any model of the
  policy. The delay-to-speed map in (D) is my own construction, not a sourced bound.

## Candidate answers

- [EXAMINER-A] **The premise is wrong: none of the four hardware limits binds on current onboard-only
  autonomy. What binds is the robustness of the perception-estimation-policy stack, plus the margin
  designers deliberately leave.** | status: **surviving** | why: demonstrated onboard-only
  unseen-course speeds sit at 0.15–0.47 of every one of ten bounds computed from the dossier's own
  anchors (F4); the one architecture swap measured on fixed hardware moves success from 0 to 85 per
  cent [D-14, A-14]; planners are deliberately run inside the thrust bound [D-36]; and the field's
  own named culprits are architecture-level (D-21 b, c, e). | distinguishing test: in the five-arm
  ablation, arm (v) (architecture) beats arms (ii)–(iv) (hardware) by more than a factor of two in
  the metric; equivalently, relaxing any single hardware limit by its attainable increment moves the
  unseen-course metric by less than 20 per cent. | confidence: medium-high
- [EXAMINER-B] **The question has no answer as posed in the perception-limited regime, because
  perception range and thrust are not separable rivals: the bound depends on their product.**
  | status: **surviving** | why: e_s + e_a = 1.000 identically by homogeneity, e_s/e_a = 1.155–1.221
  across the dossier's own parameter cases, and ds/da < 0 through body attitude and camera FoV
  (F2a, F2b) — with the FoV cutoff at exactly 1.00 g for an untilted 90 deg camera, which is why
  A-20 tilts its camera. | distinguishing test: a wide-FoV or gimbal arm and a thrust arm, applied
  separately, each give roughly half the speed gain of the two applied together, and the gain from
  thrust alone *saturates* at the FoV-limited acceleration g tan(HFoV/2 + tilt) — a prediction
  EXAMINER-A does not make and the thrust and perception candidates both contradict. | confidence:
  high (within the point-mass stop-bound model)
- [EXAMINER-C] **The metric is wrong: its denominator is non-causal and its 90 per cent clause is
  unmeasurable at affordable trial counts, so the asked-for number does not exist for any system.**
  | status: **surviving** | why: F1 and F8 — 29 consecutive successes are needed to certify 0.90,
  the best published onboard-only point (10/10 at 5 m/s) certifies only 0.741, 8/10 at 7 m/s
  certifies 0.493, and a sup over speeds costs 87–345 flights. | distinguishing test: inspect any
  future claim of "90 per cent on an unseen course" for its n; if n < 29 with no failures, or n < 69
  with failures, the claim cannot support the threshold. Falsified if someone publishes 29/29 at a
  stated speed on a stated unseen-course distribution. | confidence: high (arithmetic)
- [EXAMINER-D] **Null: no single limit dominates — several sit within a factor of two near the
  operating point.** | status: **strained, but surviving in one narrow band** | why: the ten bounds
  span a factor of 3.0, so the null is false across the whole range; but the two lowest — thrust
  bang-bang mean 10.73 m/s and FoV-capped stop bound 10.85 m/s — agree to 1.1 per cent, so in the
  10–11 m/s band (exactly where A-20 degrades to 60 per cent) two constraints become active
  simultaneously and no ranking exists there (F4). | distinguishing test: relaxing *either* thrust or
  FoV/range alone produces almost no gain at 10–11 m/s, while relaxing both produces a large one —
  the signature of simultaneous activity, distinct from EXAMINER-A (where neither helps) and from
  EXAMINER-B (where either helps by half). | confidence: low-medium
- [EXAMINER-E] **State-estimation latency binds first.** | status: **eliminated as stated; narrowed
  survivor is estimation *accuracy and drift*, not latency** | why: at 40 ms the delay-to-speed map
  gives 19.6–32.7 m/s against a 5–7 m/s operating point (F5); the latency that would bind at 7 m/s
  is 112–187 ms; driving tau to zero buys at most +7.5 per cent on the stop bound (F10); and a human
  pilot with 5.5x the outer-loop latency flies within a few per cent of Swift (F6). What survives is
  the *drift* claim [D-12, D-19], which is an accuracy quantity, repaired in practice by known-gate
  priors [D-11] — and the dossier records no measured drift magnitude in m per m (§6). | distinguishing
  test: a latency arm cutting 40 -> 15 ms yields under 10 per cent speed gain, while supplying an
  accurate relative-gate observation (or a map) yields far more. | confidence: medium-high
- [EXAMINER-F] **Rotor and actuator bandwidth binds first.** | status: **eliminated** | why: no
  source in the evidence base argues it, and the critiques researcher searched for one (§6); the
  39.1 ms thrust time constant [A-03] enters only through tau_eff, whose bound is inactive by 3–6x
  (F5); and the demonstrated unseen-course speeds are 0.47 of a thrust bound that already assumes
  *instantaneous* thrust (F4), so adding rotor lag cannot make a limit that is already slack by a
  factor of two become the binding one. | distinguishing test: raising ESC/DShot rate or fitting
  lower-inertia props produces no measurable change in the unseen-course metric, while the same
  airframe at T/W 8 does. | confidence: medium-high
- [EXAMINER-G] **Unmodelled aerodynamics binds first.** | status: **strained; reclassified** | why:
  it is the dominant *model* defect [D-08] but binds only through a controller that depends on the
  model — same hardware, same error, 0 per cent for plan-then-track and 85 per cent for a
  task-objective policy [D-14, A-14]; and the best aerodynamic result is an RMSE reduction on
  replayed mocap flights, not a speed gain [D-08]. | distinguishing test: add the hybrid BEM+NN model
  to a *policy* pipeline and measure the unseen-course metric; EXAMINER-G predicts a large gain,
  EXAMINER-A predicts a small one. If the gain is large for the MPC pipeline and small for the policy
  pipeline, the limit is the architecture, not the aerodynamics. | confidence: medium

## What would change my mind

- A published onboard-only run of 29/29 (or 65/69) on a stated unseen-course distribution at 10 m/s
  or above would move the operating point to 0.9 of the lowest bound and make F4 — the backbone of
  EXAMINER-A — collapse into a genuine hardware-limited regime, probably the thrust/FoV degeneracy of
  EXAMINER-D.
- A measured VIO latency (exposure to pose) above about 120 ms on a current onboard racing stack
  would revive EXAMINER-E, because that is where my delay-to-speed map starts to bind at 7 m/s. The
  dossier lists this measurement as missing (§6), so EXAMINER-E is eliminated on an *inferred* rather
  than a measured latency, and that is its weakest point.
- A demonstration that the delay-to-speed map in section D is wrong by an order of magnitude — for
  example a proof that the required frequency separation m is 20–30 rather than 3–5, or that the
  effective turn radius on a racing course is under 1 m — would put the 40 ms bound at 2–7 m/s and
  make latency binding after all. This map is my own construction and is the most fragile step in
  F5.
- Evidence that the 90 deg HFoV figure for the D435i class is wrong, or that the systems in A-20 and
  A-29 use a stabilised or wide view throughout, would remove F2b and weaken EXAMINER-B to its
  algebraic half (F2a) alone.
- A controlled result in which raising thrust-to-weight on an onboard-only platform from 4.1 to 8–12
  raised the unseen-course metric by the predicted ~1.4–1.7x would make thrust the answer and reduce
  EXAMINER-A to a claim about 2026 software only.

## Assumptions I relied on

- Point-mass dynamics with a thrust-magnitude bound for every speed bound; no rotation time between
  manoeuvres, no drag, no body-rate limit, no battery sag. All of these make my bounds *optimistic*,
  which cuts in favour of F4 being an underestimate of the gap, not an overestimate — except that
  rotation time and drag would lower the thrust bound toward the operating point.
- Level flight for the pitch-versus-acceleration relation in F2b, and a camera fixed to the body with
  a stated horizontal FoV. A gimbal or a derotated image invalidates the coupling.
- The delay-to-speed mapping v <= wc R / m with R = 3–10 m and m = 3–5 is my own and is not a sourced
  bound; its only external check is the 2019 retrodiction (F5).
- Independent Bernoulli trials for the F8 statistics. Real flights are correlated through battery
  state, airframe wear and operator intervention, so the true trial counts needed are *larger*, not
  smaller.
- The dossier's labels: I treated every mocap-state result as controller evidence only [D-09, D-14,
  A-11, A-12], per the brief, and I did not use A-15 as a time-optimal fraction, per §7.
- One search-summary citation (acro/rate mode) and no re-checked primary source for it; the F6
  argument stands without it, slightly weakened.
