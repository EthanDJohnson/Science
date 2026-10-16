# Analysis: dialectician (resolve real contradictions)

status: final

## Method applied

I take the three sharpest contradictions in the evidence base — two well-supported claims that cannot
both hold as stated — state each as thesis and antithesis with its evidence, then find the regime,
definition or condition under which both are true (or show which must yield). Each synthesis is
required to predict something neither side predicted alone, and that prediction is computed, not
asserted.

## Findings

1. **The evidence base's largest single effect is not a vehicle property.** On the same airframe class
   (0.5–0.9 kg, T/W 4.1–4.5, onboard compute), onboard-only mean/peak speed is 27.8–32.2 m/s on a
   *seen, pre-mapped* gate track [D-11][D-20][A-26] and 5–10 m/s on *unseen* clutter [D-20][A-20][A-29],
   a factor of 3–6. No hardware limit changes between those two rows: what changes is the information
   available before take-off and the spatial scale of the features. Any candidate that lives in the
   vehicle has to explain why it binds at 7 m/s in one case and not at 30 m/s in the other.
2. **Thrust-to-weight is not the binding term, and this is now quantitative on two independent routes.**
   The point-mass ceiling gives elasticity d ln v / d ln(T/W) ≈ +0.5 at T/W ≥ 4 [D-33][A-34] and the
   planner sweep on a real track gives d ln(lap)/d ln(TWR) = −0.565 [A-16]. Yet the one platform with
   T/W 12.35 reaches 30 m/s peak only with motion capture in the loop on a trained track [A-11][A-12],
   i.e. three times the thrust buys nothing on the brief's metric. Set aside with a number.
3. **The usable depth range may be smaller than the 6 m the published bound assumes.** A-21/A-33 are
   evaluated at s = 6 m [A-21][A-33], but the D435i used in the 5–10 m/s unseen-clutter work [A-20]
   is specified at 87° × 58° depth FoV with an operating range quoted as roughly 0.3–3 m
   [new: Intel product page via search, search-summary, SUMMARY "Intel's product page lists the depth
   field of view as H:87, V:58 for the D435i. Its operating range is listed as about 0.3 m to 3 m"].
   At s = 3 m rather than 6 m every range-limited bound halves, because the range elasticity is +1
   exactly in the dodge bound [A-33][calc: runs/2026-10-15-quadrotor-agility-limit/calc/lens-dialectician_syntheses.py].
4. **Synthesis S1 (new): a body-fixed forward camera and hard acceleration are mutually exclusive, and
   that caps acceleration far below the thrust ceiling.** To accelerate horizontally at a the vehicle
   must tilt by θ = atan(a/g) [D-33]; with a body-fixed camera whose axis sits φ above body-x, the
   horizontal direction of travel leaves the camera cone once θ > φ + VFoV/2. For the A-20 sensor
   (58° vertical depth FoV, mounted 30° up above 7 m/s [A-20]) that gives a_FoV = 16.3 m/s² = 1.66 g,
   against a thrust ceiling of 42.0 m/s² = 4.28 g at T/W 4.4 — a factor 2.57 in acceleration and 1.49
   in dodge speed [calc: .../lens-dialectician_syntheses.py]. Level-mounted, the same camera caps
   acceleration at 0.55 g. This is why the 30° tilt was introduced above 7 m/s [A-20], and it explains
   the direction of the "objects entered the field of view very late because of the high angular
   velocity of the platform" failure at 7 m/s [D-13] in a quantity rather than a narrative.
5. **Synthesis S2 (new): latency binds only when measured against the course's feature spacing.** The
   delay-limited crossover [D-25][A-32] is a frequency; a course converts it to a speed through its
   feature spacing L (gate or obstacle pitch), since the reference manoeuvre frequency is v/L. Requiring
   ω_c ≥ 2π v/L gives v ≤ ω_c L / 2π, with elasticities exactly +1 in L and exactly −1 in τ_eff
   [calc: .../lens-dialectician_syntheses.py]. With Swift's 40 ms sensorimotor latency [A-07] and a
   75 m / 7-gate track, L = 10.7 m gives 33 m/s (marginal tracking) or 17 m/s (good tracking); with a
   ~100 ms depth-plus-mapping chain (30 Hz depth + 65.2 ms mapping [A-19]) and L = 4 m clutter it gives
   5.0 m/s (marginal) — the speed at which A-20 last holds 100 per cent. The bound is tight in clutter
   and slack by ~2.6× on the gate track, which is precisely the regime split the dossier reports [D-13].
6. **Synthesis S3: actuator bandwidth is a lag, not a delay, and that is why no paper names it.**
   A first-order lag of 39.1 ms [A-03] and a pure delay of 39.1 ms permit crossovers within a factor
   1.10–1.27 of each other (25.6 vs 20.1 rad/s at PM 45°), so the two are nearly equivalent *in phase*
   [calc: .../lens-dialectician_syntheses.py]. The difference is invertibility: a known pole can be
   cancelled by lead/INDI, a transport delay cannot [D-27]. The 78 per cent tracking-error reduction
   from adding an INDI inner loop plus a drag model [D-09] is the empirical signature of that
   inversion. Residual cost of the lag is a large-signal one: the delivered fraction of commanded
   acceleration over a manoeuvre of duration T is 1 − (τ/T)(1 − e^(−T/τ)), which is 0.83 over a 230 ms
   dodge but 0.44 over a 50 ms one [calc: .../lens-dialectician_syntheses.py]. So actuator bandwidth
   becomes a first-order term only for manoeuvres shorter than ~150 ms, which on a 0.5 m-radius
   obstacle means a > 90 m/s² — a regime no onboard-only platform in the dossier operates in.
7. **Sensitivity ranking inside the clutter regime, computed one perturbation at a time.** At the
   baseline (s = 6 m, τ = 100 ms, a = 16.3 m/s² FoV-limited, r = 0.5 m) the dodge-bound elasticities
   are e_s = +1.000, e_a = +0.387, e_τ = −0.231 [calc: .../lens-dialectician_syntheses.py]. Finite,
   realisable swaps: doubling usable range 6 → 12 m gives +100 per cent speed; swapping to a
   115°-vertical-FoV camera at 30° tilt (which lifts the FoV cap above the thrust cap) gives
   +41.5 per cent; cutting latency 100 → 30 ms gives +18.4 per cent. Range and field of view dominate
   latency by 2–5× in this regime.
8. **The two "aerodynamics binds" results do not speak to the brief's metric, and their own numbers say
   how much they could.** The aerodynamic model-error gain is 0.8 m → <0.3 m positional RMSE on
   *replayed* flights [D-08], and the model-fidelity penalty on the computed optimum is 2.00–2.68 per
   cent of traversal time [D-05][A-17]. A limit worth a few per cent of lap time cannot be the limit
   that costs a factor of 3–6 (finding 1). Aerodynamics is a *soft* limit: it is absorbed, at a price in
   lap time, by optimising the task objective instead of tracking a reference [D-14][D-15].
9. **A 2026 paper the dossier lists as unread (§6, arXiv:2603.04305) independently states S1's
   mechanism and measures its cost.** It plans time-optimal laps with "full nonlinear dynamics, rotor
   actuation limits, aerodynamic effects, camera field-of-view constraints, and convex geometric gate
   representations" in one problem, and reports that on a dense track "the quadrotor must produce much
   more intense aggressive rotations than usual to keep the lap time low, which comes at the cost of
   undermined perception quality"
   [new: arXiv:2603.04305, fetched PDF p.1 and p.17, "camera field-of-view constraints, and convex
   geometric gate representations" / "the quadrotor must produce much more intense aggressive rotations
   than usual to keep the lap time low, which comes at the cost of undermined perception quality"].
   Its closed-loop ablation, **20 trials in RotorS simulation** (Table VI, so simulation and not a
   hardware sensitivity), holds the vehicle, the actuation limits and the aerodynamics fixed and varies
   only the perception objective: success 55 per cent (no perception objective) → 67 per cent
   (look-ahead) → 71 per cent (FoV constraint) → 100 per cent (position-uncertainty minimisation), with
   tracking RMSE 0.419 → 0.324 m
   [new: arXiv:2603.04305, fetched PDF p.15, "TOWP-Ours 0.3590 0.4192 55% | LA 0.3541 0.4612 67% |
   FOV 0.4634 0.3577 71% | PUM 0.2228 0.3239 100%" and "the success rate across 20 closed-loop flight
   tests"]. Real-world flight is 9.8 m/s with 0.07 m tracking error — an indoor Split-S with a Jetson
   Orin NX, i.e. a seen track. This is the closest thing in or near the evidence base to the brief's
   missing one-at-a-time sensitivity study, and the limit it moves is perception, not actuation.
   Note *which* perception: on a known track the winning objective is state-estimate uncertainty (PUM),
   not raw field of view — so the seen-track branch of the perception candidate is an **estimation**
   claim [D-21(d)], while the unseen-course branch is a **look-ahead** claim [D-21(c)].
10. **Corollary nobody in the dossier states: a fixed forward camera saturates thrust-to-weight.**
    Using a = g·tan(θ) and T/W = sec(θ), the thrust-to-weight above which extra thrust cannot be spent
    without swinging the direction of travel out of the camera cone is T/W_sat = sec(φ + VFoV/2):
    **1.14** for a level 58°-FoV depth camera, **1.94** at the A-20 30° tilt, 3.63 at a 45° tilt, and
    22.9 for a 115°-vertical-FoV camera at 30° tilt [calc: .../lens-dialectician_syntheses.py]. Every
    onboard-only platform in the dossier has T/W 4.1–4.5 [A-13]. So on an unseen course these vehicles
    carry 2–4× more thrust than their cameras let them use — which is an independent explanation of
    finding 2 (why T/W 12.35 buys nothing without motion capture) and a falsifiable claim.
11. **The metric itself is only satisfied at ≤5 m/s, and that fixes which regime the answer lives in.**
    The brief's 90-per-cent-on-an-unseen-course criterion is met in the documented sets only at or below
    5 m/s [D-24][A-20]; the 28–32 m/s results are seen-course [D-11][A-26] and the 30 m/s / 12 g result
    is mocap [A-12]. Answer (a) is therefore an answer about the 5–10 m/s regime, where by finding 7
    the range/FoV elasticity (+1.0) exceeds the latency elasticity (−0.23) by 4× and the acceleration
    elasticity (+0.39) by 2.6×.

## Lens-specific outputs

### Contradiction 1 — "aerodynamics is the dominant defect" vs "perception is the limiting factor"

**Thesis (aerodynamics).** Unmodelled aerodynamics is "the dominant model defect during high speeds or
agile maneuvers": a hybrid BEM + neural-residual model cuts positional RMSE from ~0.8 m to <0.3 m and
force/torque error by ~50 per cent on flights to 18.1 m/s [D-08][A-18]; adding an INDI loop plus a drag
model cuts tracking error by >78 per cent at 20 m/s and 5 g [D-09]; and under a realistic model a
plan-then-track controller collapses from 44 per cent to 0 per cent success [D-14][A-14].

**Antithesis (perception).** "The limiting factor for autonomous agile flight in arbitrary unknown
environments is the coupling of fast and robust perception with effective planning" [D-21(c)]; the
hardware failures at 7 m/s in unseen clutter are attributed to objects entering the field of view late
[D-13]; and the fastest onboard results exist only on pre-mapped tracks [D-11].

**Where both hold.** They are limits on different objects. Aerodynamics bounds the *fidelity of the
inner loop given a reference*; perception bounds the *existence of an admissible reference*. The two
are measured in different currencies and the dossier lets us convert both to lap time: aerodynamic
model error costs 2.00–2.68 per cent of traversal time on the computed optimum [A-17] and is further
absorbable by a task-objective policy at ~4 per cent of lap time (5.14 s RL vs 4.92 s nominal-model
tracking, [A-14]); the seen-to-unseen perception penalty is a factor of 3–6 [finding 1]. On the brief's
own definition of "binds first" — largest metric change per unit relaxation — the aerodynamic branch
must yield: its maximum possible gain, even if model error went to zero, is bounded by the few per cent
that separates a realistic-model optimum from a nominal-model optimum.

**What the synthesis predicts that neither side did.** A controller with *perfect* aerodynamics and the
A-20 sensing suite will not exceed ~13–15 m/s at 90 per cent success on unseen clutter, because the
dodge bound at s = 6 m, τ = 50 ms caps it at 15.0 m/s even with FoV-limited acceleration
[calc: .../lens-dialectician_syntheses.py]. Conversely a vehicle with a *crude* aerodynamic model but
12 m of usable range should reach ~26 m/s on the same clutter. Test: fly the same policy and airframe
with (i) the NeuroBEM-grade residual model and the stock depth camera, (ii) the stock nominal model and
a doubled sensing range (longer-range depth or LiDAR). The synthesis says (ii) wins by >50 per cent.

### Contradiction 2 — 28–32 m/s onboard vs 5–10 m/s onboard, same vehicle class

**Thesis.** Onboard-only, minimal-sensor flight reaches 27.8–32.2 m/s peak with 16.56 s two-lap
completions [A-26], and champion-beating lap times with onboard sensing [D-16][A-10].

**Antithesis.** Onboard-only flight in unseen clutter reaches 5.3–10 m/s, with 90 per cent success
documented only at ≤5 m/s [A-20][A-29][D-24].

**Where both hold.** Two mechanisms separate them and the dossier conflates them:
(a) prior knowledge — gate maps and track-fitted residual models [D-11][D-12]; and
(b) feature spacing — L ≈ 10–14 m between gates versus L ≈ 2–4 m between obstacles. S2 shows (b) alone
accounts for a factor L_gate/L_clutter ≈ 3.4 at equal latency, and with the latency difference the
L/τ bound predicts a ratio of 8.5 against an observed 2.6–3.2 [calc: .../lens-dialectician_syntheses.py].
So the bound is *tight in clutter and slack on the gate track*: in clutter the vehicle flies at its
delay-and-spacing limit, on the gate track it flies at some other limit (thrust, aero, policy) with the
latency bound 2.6× away. Neither side's claim is wrong; both are reports from opposite sides of a
crossing.

**What the synthesis predicts that neither side did.** The crossing is at the speed where
ω_c L / 2π equals the thrust-limited bang-bang speed over the same spacing. It predicts an *interaction*
no single-limit account gives: halving the latency of a clutter-flying system should raise its speed by
close to 100 per cent (e_τ = −1 in the L/τ regime), while halving the latency of a gate-racing system
should raise its speed by close to nothing. Test: run the same onboard stack on a gate track and in
clutter, with an artificial 50 ms inserted in the perception path. The synthesis predicts a ≈33 per cent
speed loss in clutter and <10 per cent on the gate track.

### Contradiction 3 — "40 ms of latency caps the loop at 3.1 Hz" vs "these vehicles fly at 30 m/s"

**Thesis.** With τ_eff = 40 ms the gain crossover cannot exceed 19.6 rad/s = 3.1 Hz at 45° phase margin
[D-25][A-32], and a 39.1 ms motor time constant sits at the same order [A-03][A-05].

**Antithesis.** Platforms with exactly those numbers fly at 30 m/s and 12 g [A-12], run controllers at
500 Hz with 0–100 per cent command changes in 2 ms [A-28], and no paper names actuator bandwidth as the
binding limit [D-21 note][§6].

**Where both hold.** The 3.1 Hz applies to the loop that *contains* the 40 ms, and that is the outer
(position/trajectory) loop closed through perception. The attitude-rate loop closes on the IMU inside
the flight controller, with transport delay of order 1–2 ms, permitting ω_c of order 260–390 rad/s
(42–63 Hz) once the actuator pole is inverted [calc: .../lens-dialectician_syntheses.py]. The cascade
is what makes both statements true: 3.1 Hz outer, tens of Hz inner. Neither side yields; the conflation
of τ_eff across loops does. The corollary is that A-32's 3.1 Hz is not a defect — a 3 Hz outer loop is
ample on a 10 m-spaced gate track at 30 m/s (one correction cycle per 0.36 s segment) and is marginal at
5 m/s on 4 m-spaced clutter.

**What the synthesis predicts that neither side did.** Actuator bandwidth should become measurable as a
limit only when the manoeuvre duration falls below ~150 ms (a_eff/a_cmd ≤ 0.76 at τ = 39.1 ms), which for
a 0.5 m obstacle clearance requires a > 90 m/s² ≈ 9 g — above every onboard-only platform in the dossier
and reachable only on the T/W-12 mocap platform [A-11]. Prediction: on that T/W-12.35 platform, and only
there, replacing the motors with faster ones (or adding rotor-speed feedback) should produce a measurable
lap-time gain; on T/W-4.4 onboard platforms it should produce essentially none. This is the one testable
form of the actuator-bandwidth hypothesis the dossier's silence leaves open.

### Assumption ledger for the syntheses

| ID | Assumption | Where it enters | If wrong |
|---|---|---|---|
| L-1 | Camera body-fixed, no gimbal; travel direction must lie in the camera cone to see what you are flying into | S1 | S1 collapses; a gimbal or omnidirectional sensing removes the cap (and is the engineering recommendation either way) |
| L-2 | Vertical depth FoV 58° and 30° up-tilt for A-20 | S1 | a_FoV scales as g·tan(φ+VFoV/2): 45° tilt gives 3.49 g, near the thrust cap |
| L-3 | Reference manoeuvre frequency ≈ v/L, one correction cycle per feature (k = 1 marginal, k = 2 good) | S2 | the crossing speed scales linearly in 1/k; only the elasticities (+1, −1) are k-free |
| L-4 | Inner-loop transport delay ~2 ms (gyro to motor on an STM32-class FC); not measured in the dossier (§6) | S3 | if the inner path really carries 35–40 ms of *transport*, the cascade argument fails and latency binds everywhere |
| L-5 | The dodge bound D-31 with r = 0.5 m, single static obstacle, point mass | S1, S2, findings 3, 7 | elasticities are robust in sign; absolute speeds are optimistic (the bound ignores estimation error and multiple obstacles) |

## Calculations

- `runs/2026-10-15-quadrotor-agility-limit/calc/lens-dialectician_syntheses.py` — three syntheses.
  - **S1, FoV-limited acceleration.** a_FoV = g·tan(φ + VFoV/2). Level 58° FoV: 5.44 m/s² (0.55 g);
    30° tilt: 16.33 m/s² (1.66 g); 45° tilt: 34.21 m/s² (3.49 g); 115° vertical FoV at 30° tilt:
    FoV no longer binds (thrust cap 42.03 m/s² = 4.28 g at T/W 4.4). Dodge speed at s = 6 m, τ = 50 ms,
    r = 0.5 m: 22.38 m/s thrust-limited vs 15.00 m/s FoV-limited (ratio 1.49 from an accel ratio 2.57).
  - **S2, latency against feature spacing.** ω_c = (π/2 − PM)/τ_eff; v ≤ ω_c L/(2πk). τ = 40 ms,
    L = 10.71 m: 33.5 m/s (k=1) / 16.7 m/s (k=2). τ = 100 ms, L = 4 m: 5.00 m/s (k=1) / 2.50 (k=2).
    τ = 30 ms, L = 4 m: 16.7 / 8.3 m/s. Predicted seen:unseen ratio 8.52 vs observed 2.57–3.22.
    Elasticities +1 in L, −1 in τ_eff (numerically confirmed to 4 decimals).
  - **S3, lag vs delay.** τ = 39.1 ms: ω_c = 25.58 rad/s (lag) vs 20.09 rad/s (delay) at PM 45°, ratio
    1.27; at PM 60°, 14.77 vs 13.39, ratio 1.10. With the pole inverted and 2 ms transport left,
    ω_c ≤ 392.7 rad/s (62.5 Hz) at PM 45°. Large-signal loss 1 − (τ/T)(1 − e^(−T/τ)): 56.4 per cent at
    T = 50 ms, 36.1 per cent at 100 ms, 24.0 per cent at 160 ms, 17.0 per cent at 230 ms, 3.9 per cent
    at 1 s.
  - **Clutter-regime sensitivity.** Baseline v = 13.33 m/s (s = 6 m, τ = 100 ms, a = 16.33 m/s²):
    e_s = +1.000, e_a = +0.387, e_τ = −0.231; finite swaps give +100 per cent (range 6→12 m),
    +41.5 per cent (wide-FoV camera), +18.4 per cent (τ 100→30 ms).
  - **S1 corollary, T/W saturation.** T/W_sat = sec(φ + VFoV/2): 1.14 (level 58° FoV), 1.94 (30° tilt,
    58° FoV), 3.63 (45° tilt), 1.86 (115° VFoV level), 22.93 (115° VFoV at 30° tilt).
  - Log: `calc/lens-dialectician_syntheses.py.log`.

## Candidate answers

- [DIAL-A] **In the regime the brief's metric actually selects (onboard-only, unseen course, ≥90 per
  cent success, i.e. ≤5–10 m/s today), what binds first is usable look-ahead distance — and it binds
  jointly with field of view, not with sensor noise or latency.** | status: surviving | why: from
  Contradiction 1 and 2. The dodge-bound elasticity in that regime is e_s = +1.000 against e_a = +0.387
  and e_τ = −0.231, and realisable swaps give +100 per cent (range 6→12 m) vs +41.5 per cent (wide-FoV
  camera) vs +18.4 per cent (latency 100→30 ms) [calc: .../lens-dialectician_syntheses.py]; the
  hardware failure mode at 7 m/s is late field-of-view entry [D-13][A-20]; usable depth range on the
  sensor that produced those results is quoted at ~0.3–3 m [finding 3], below the 6 m the bounds assume
  [A-21]. | distinguishing prediction or test: on the A-20 platform and policy, swapping the depth
  camera for one with twice the usable range (or a 3-D LiDAR [D-39]) should raise the 90-per-cent speed
  by 80–100 per cent, while a 70 ms cut in perception latency on the same platform should raise it by
  under 20 per cent. Both are one-afternoon experiments for any group with that stack (≈USD 2k of
  sensor). | confidence: medium
- [DIAL-B] **In the seen-track, >15 m/s regime, what binds first is state-estimation information
  quality along the manoeuvre — the manoeuvre needed for speed is the manoeuvre that degrades the
  estimate.** | status: surviving (regime-restricted; this is the other half of the same synthesis, not
  a rival to DIAL-A) | why: the only one-variable-at-a-time closed-loop ablation available moves success
  from 55 to 100 per cent by adding a position-uncertainty objective with vehicle, actuation and
  aerodynamics fixed (20 trials, simulation) [finding 9]; the fastest onboard results repair VIO drift
  with prior gate maps [D-11][D-12]; minimal-sensor competitors name drift as the dominant problem
  [D-19]; and aggressive rotation is stated to undermine perception quality on dense tracks [finding 9].
  | distinguishing prediction or test: on a seen track, giving the vehicle an oracle state estimate
  should improve *success rate* by tens of points while improving lap time by only a few per cent; and
  gains should scale with the fraction of the lap spent at high body rate, so the split-S and other
  tight segments should carry nearly all of the improvement [D-16]. | confidence: medium
- [DIAL-C] **Rotor and actuator bandwidth does not bind on any onboard-only platform in this class, and
  begins to bind only for manoeuvres shorter than about 150 ms (requiring a > ~90 m/s² ≈ 9 g).** |
  status: eliminated as the first-binding limit in the onboard-only regime; surviving only as a
  high-thrust-regime limit | why: Contradiction 3 — the 39.1 ms figure is a first-order lag, not a
  transport delay, so it is invertible by lead/INDI (78 per cent tracking-error cut when that inversion
  is added [D-09]); phase-wise lag and delay differ by only 1.10–1.27× [calc: ...], but with the pole
  inverted and ~2 ms of real transport left the inner loop can cross at 42–63 Hz; the large-signal loss
  1 − (τ/T)(1 − e^(−T/τ)) is 17 per cent on a 230 ms dodge and 56 per cent on a 50 ms one [calc: ...];
  and no paper in the evidence base argues actuator bandwidth binds [D-21 note][§6]. | distinguishing
  prediction or test: faster motors or rotor-speed feedback should produce a measurable lap-time gain
  **only** on the T/W-12.35 platform [A-11] and essentially none on the T/W-4.4 onboard platforms. A
  cheap version: sweep a software first-order lag from 0 to 80 ms in the command path and look for the
  knee — DIAL-C predicts the agility metric is flat below ~40 ms on an unseen course. | confidence:
  medium-high
- [DIAL-D] **Unmodelled aerodynamics is the dominant *model* defect but not the binding limit: its
  total available gain is bounded at a few per cent of traversal time, because an architecture that
  optimises the task objective already absorbs it.** | status: strained → eliminated as "binds first" |
  why: the model-fidelity penalty on the computed optimum is 2.00–2.68 per cent [D-05][A-17]; the RL
  policy pays ~4 per cent of lap time and keeps 85–100 per cent success where tracking MPC goes to zero
  [D-14][A-14]; and the model-error results are replay/mocap evidence, not speed on an unseen course
  [D-08][D-09]. A limit worth a few per cent cannot be the limit that costs a factor of 3–6 [finding 1].
  | distinguishing prediction or test: give a plan-then-track pipeline a NeuroBEM-grade model and it
  should recover most of the success-rate gap to the RL policy *without* beating it on speed by more
  than ~5 per cent. If instead the aero-corrected pipeline is >20 per cent faster on an unseen course,
  DIAL-D is wrong and aerodynamics was binding. | confidence: medium-high
- [DIAL-E] **Null: no single limit dominates.** | status: eliminated in its strong form, surviving in
  its weak form | why: *within* a regime the elasticities are not within a factor of two — in clutter
  they span +1.000 (range) to −0.231 (latency), a spread of 4.3× [calc: ...], so one limit does dominate
  there; but *across* regimes the ranking changes (the L/τ bound is tight in clutter and slack by 2.6×
  on a gate track [calc: ...]), so there is no single limit that binds for the whole question as asked.
  The honest form of the null is "the first-binding limit is a function of course feature spacing, not a
  property of the vehicle". | distinguishing prediction or test: build one course family with a
  continuously varied obstacle pitch L from 2 to 15 m at fixed sensing hardware; the null's weak form
  predicts the identity of the binding limit (detectable as which single relaxation helps most) switches
  from perception to thrust/aero at the L where ω_c L/2π crosses the bang-bang speed. | confidence:
  medium
- [DIAL-F] **Reframe: the binding limit is a coupling, not a component — the manoeuvre that produces
  agility is the manoeuvre that destroys the information needed to command it. Perception and actuation
  share one budget through the body tilt.** | status: surviving, and it is what the two syntheses jointly
  say | why: θ = atan(a/g) is forced by underactuation [D-33], so a body-fixed camera cone of half-angle
  φ + VFoV/2 caps usable acceleration at g·tan(φ + VFoV/2) = 1.66 g on the A-20 geometry against 4.28 g
  of thrust [calc: ...]; the same coupling appears in the 30° up-tilt introduced above 7 m/s [A-20], in
  late field-of-view entry at high angular velocity [D-13], in motion-blur-driven VIO drift [D-12], and
  is stated outright in finding 9. | distinguishing prediction or test: **thrust-to-weight should
  saturate**. On an unseen course with a fixed forward camera, the agility metric should stop improving
  at T/W ≈ sec(φ + VFoV/2) — about 1.94 for the A-20 geometry and 3.63 at a 45° tilt
  [calc: .../lens-dialectician_syntheses.py] — so a T/W sweep from 2 to 6 at fixed camera geometry
  should show a knee below 4, while the same sweep with a gimballed or hemispherical camera should keep
  improving. No published experiment reports this sweep; it needs one airframe, three propeller/battery
  combinations and two camera mounts. | confidence: medium-low (the cone criterion is a sufficient, not
  a necessary, condition for seeing where you are going: a wide-HFoV camera plus a yaw-based dodge
  evades it, which is itself a design recommendation)
- [DIAL-G] **Reframe on the metric: no published result satisfies the brief's definition above 5 m/s, so
  "which limit binds" currently has an answer only at 5 m/s, and the 3–6× gap between seen and unseen
  courses is the measurement the field is missing.** | status: surviving | why: [D-24][D-23][D-11]
  and finding 1; trial counts are missing for every 100-per-cent claim [A-29]. | distinguishing
  prediction or test: the November 2026 identical-hardware final [D-41] will report seen-track times;
  if nobody reports an unseen-course success rate with trial counts, the ranking question stays
  underdetermined no matter how the theory comes out. | confidence: high

## What would change my mind

- A measured inner-loop *transport* delay (gyro sample to thrust onset, excluding the first-order motor
  lag) above ~10 ms would break Contradiction 3's cascade resolution and move latency up the ranking
  everywhere; the dossier does not have this number (§6) and assumption L-4 carries it.
- A rotor-speed slew-rate measurement showing the motor response is rate-limited rather than
  first-order (§6 lists this as unretrieved) would make DIAL-C's invertibility argument fail, because a
  rate limit is not invertible by lead compensation [D-30].
- An unseen-course hardware result above ~15 m/s at 90 per cent success with a short-range depth camera
  would refute DIAL-A directly, since the dodge bound at s = 3–6 m cannot produce it.
- A T/W sweep on an unseen course that keeps improving past T/W 4 with a fixed narrow forward camera
  would refute DIAL-F's saturation prediction.
- If the published version of arXiv:2603.04305 reports the 55 → 100 per cent ablation on *hardware*
  rather than in RotorS, DIAL-B strengthens from a simulation sensitivity to a hardware one.

## Assumptions I relied on

- L-1 to L-5 in the assumption ledger above (body-fixed camera; 58° vertical depth FoV at 30° tilt;
  manoeuvre frequency ≈ v/L; ~2 ms inner-loop transport delay; the point-mass dodge bound D-31).
- The dodge and stop bounds are used only for *ratios and elasticities*, not for absolute speeds: they
  over-predict observed hardware speeds by 1.5–3× because they assume one static obstacle, exact state,
  and free choice of braking acceleration [D-31][D-32].
- Elasticities are local (10 per cent perturbations) except where a finite swap is labelled as such.
- The Loquercio-class latency of ~100 ms is my own sum of a 30 Hz depth frame period and the 65.2 ms
  mapping pipeline [A-19]; the paper does not state an end-to-end figure (§6), so S2's clutter row
  carries that construction.
- Correlated apparatus: A-01 to A-06, A-07 to A-10, A-16 to A-18 and A-20 to A-21 come from one
  platform lineage (§7), so findings 1, 4 and 7 rest largely on one group's hardware.
