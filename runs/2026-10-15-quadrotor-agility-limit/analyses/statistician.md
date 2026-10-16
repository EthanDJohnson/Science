# Analysis: statistician (is the signal real?)
status: final

## Method applied

The "signals" this question rests on are not excesses over background. They are (i) success rates
over 4 to 43 hardware trials, (ii) single-condition sensitivity measurements with no quoted
uncertainty, and (iii) algebraic elasticities. I therefore reconstructed each claimed signal as
counts, used binomial-interval and two-proportion machinery from
`.claude/skills/conundrum/scripts/stats_tools.py` instead of ratios, computed how many trials each
reported ranking would actually need, grouped the speed claims by course type rather than pooling
them (with rho = 0 and rho = 0.8 for shared apparatus), counted the attributions tried, and weighed
what survived against a base rate for "one named limit binds" claims in agile-flight robotics.
All numbers are SI (m/s, s, m/s^2) unless marked.

## Findings

**F1 — No source establishes the brief's metric at any speed.** The best-documented unseen-course
set is 10/10 at 3 and 5 m/s, 8/10 at 7 m/s, 60 per cent at 10 m/s [D-24, A-20]. Ten of ten gives a
Clopper-Pearson one-sided 95 per cent lower bound of 0.741 and a Wilson 95 per cent interval
[0.722, 1.000]: it is consistent with a true rate of 0.75, i.e. with *failing* the 90 per cent
criterion by a wide margin. Certifying a true rate >= 0.90 at 95 per cent needs
ln(0.05)/ln(0.90) = 28.4, i.e. **29 consecutive flawless unseen-course flights**, or 54 flights with
one crash, 85 with three [calc: runs/2026-10-15-quadrotor-agility-limit/calc/lens-statistician_rates.py].
No published onboard unseen-course set approaches this.

**F2 — The dossier's own threshold statement is too strong in both directions.** [D-24] says the
90 per cent threshold is met "only at or below 5 m/s". Statistically: the 7 m/s row (8/10) does
**not** reject a true rate >= 0.90 (one-sided p = 0.264, z = 0.63), and the 5 m/s row does not
establish one (F1). Only the 10 m/s row rejects it (6/10, one-sided p = 0.0128, z = 2.23;
two-sided p = 0.0256) and the fastest MonoRace policy does (1/4, one-sided p = 0.0037, z = 2.68)
[calc: .../lens-statistician_rates.py]. **The speed at which 90 per cent reliability fails is
unmeasured anywhere between 5 and 10 m/s.** This is the single largest statistical hole in the
evidence base, and it sits exactly on the brief's dependent variable.

**F3 — The field is roughly 20x under-powered for its own criterion.** Telling 90 per cent from
80 per cent apart takes 199 trials per arm (95 per cent confidence, 80 per cent power); 88.4 from
90 per cent takes 5907; 90 from 60 per cent takes only 32 [calc: .../lens-statistician_rates.py].
The largest single-condition hardware set in the dossier is 43 flights [A-27] and the typical set is
4 to 10 [A-20, A-27, A-14]. A decisive call on a 10-point difference in success rate needs a
standard error of 0.02, i.e. about 225 trials at p = 0.9 (`precision_needed(0.10, 5) = 0.0200`).

**F4 — MonoRace's speed-reliability trade is real at its extremes and unmeasurable in its middle.**
M23 at 38/43 = 88.4 per cent is fully consistent with >= 90 per cent (p = 0.43; Wilson
[0.755, 0.949]); M16 at 1/4 is not (p = 0.0037, two-sided 0.0074, minimum Bayes factor for the
alternative <= 10.1, prior needed for a posterior of 0.5 = 0.09) [A-27]. So the headline 16.56 s /
"up to 100 km/h" number [A-26] is statistically established *not* to be a 90 per cent-reliable
speed, while the 23 s class cannot be told from the threshold at any affordable trial count.

**F5 — Grouped by course type, the speeds split 3.5-fold, and nothing else in the record splits
like that.** Working in ln(speed) with an assigned 20 per cent fractional spread (no source quotes
an uncertainty on a demonstrated speed — this is my assumption), `grouped_chi2` gives within-group
chi2 of 2.97/2 (seen gate track, mean 26.2 m/s), 5.28/3 (unseen clutter, 7.4 m/s) and 0.47/1
(mocap, 33.0 m/s), against a **between-group chi2 of 104.2/2 dof, p = 2.4e-23, z = 10.0**. The split
survives an assigned spread of 80 per cent (between chi2 6.5/2, p = 0.039) and survives full
within-group correlation at rho = 0.8 (between chi2 37.6/2, p = 6.7e-9, z = 5.8). The pooled
weighted mean is 15.7 m/s with a PDG scale factor S = 3.76 — pooling smears a real split between
methods over every measurement, which is exactly what the method warns against
[calc: .../lens-statistician_rates.py; groups from A-20, A-26, A-29, A-31, A-12, A-02].

**F6 — Elasticities rank the four candidate limits, and latency comes last in the current regime.**
Re-deriving the dossier's own bounds [D-31, D-32, A-33] and perturbing one input at a time:
for the stop-before-obstacle bound at s = 6 m, a_h = 38 m/s^2 (T/W 4.1, [A-13]) and tau = 40 ms
(Swift sensorimotor latency, [A-07]), e_range = +0.536, e_accel = +0.464, e_latency = -0.071, so
range has **7.5x** the leverage of latency; at MonoRace's 17 ms image delay [A-28] the ratio is 17x;
only at the 2019 130 ms chain [A-22] does it fall to 2.7x. On the kinder lateral-dodge bound
e_latency runs -0.07 to -0.36, and |e_latency| reaches 0.50 — parity with range — only at
tau = 161 ms (a = 77 m/s^2), 229 ms (38) or 343 ms (17) [calc: .../lens-statistician_rates.py].
The latency term v*tau equals the braking term v^2/(2a) at v = 2 a tau = 3.0 m/s for 38 m/s^2 and
40 ms: above a walking pace, stopping distance, not reaction distance, dominates.

**F7 — Range and thrust-side acceleration are within 15 per cent of each other in elasticity, which
is the null's signature.** e_range = 0.52-0.61 and e_accel = 0.39-0.49 on the stop bound (F6); the
planner sweep [A-16] gives d ln(lap)/d ln(TWR) = -0.565, i.e. an elasticity of mean speed to
thrust-to-weight of +0.565, against the point-mass value 0.533 at T/W = 4 [D-33, A-34]. The two
agree to 6 per cent; neither carries a quoted uncertainty, so **no tension can be computed** and I
will not invent one. The brief's hidden premise 1 ("several limits may be within a factor of two")
is satisfied by these two: 0.5 vs 0.5.

**F8 — The attributions are post hoc, multiply-looked and rest on 2 to 4 crash events.** Five
different papers name five different binding limits [D-21]; the reported record has about 12
(speed x environment x pipeline) cells. A local p of 0.01 on an attribution becomes a Sidak global
p of 0.049 at 5 looks and 0.114 at 12; a local 0.05 becomes 0.23 and 0.46
[calc: .../lens-statistician_rates.py]. Worse, the causal shares themselves are tiny counts: the
7 m/s perception attribution rests on 2 crashes, both blamed on late field-of-view entry
[D-13, A-20] — share 2/2, Wilson [0.34, 1.00], i.e. consistent with perception causing only a third
of failures; Swift's loss breakdown is 4/10 gate collision (Wilson [0.17, 0.69]) and 2/10 "slower"
([0.06, 0.51]) [A-10]. **No cause-share interval in this evidence base excludes 0.5**, so no source
has the statistics to call its own named limit dominant. No analysis here was blinded or
preregistered, and no sensitivity study exists at all [D, §6].

**F9 — One signal is statistically robust: the collapse of plan-then-track under model error.**
Trajectory-tracking MPC goes 4.92 s / 44 per cent in nominal simulation to 0 per cent under a
realistic model and 0 per cent in the real world, while the RL policy holds 100/100/85 per cent
[A-14, D-14]. The trial counts are not stated in the text, but the reported percentages pin them
down: 44.0, 76.0 and 20.0 are integer multiples of 1/25 and 85.0 and 50.0 of 1/20, so n >= 25
(simulation) and n >= 20 (real) — my inference from the granularity, and it makes my z-values lower
bounds. At n = 20, RL 17/20 vs tracking 0/20 gives z = 5.44 (two-sided p = 5.4e-8); RL vs contouring
10/20 gives z = 2.36 (p = 0.018, minimum Bayes factor for the alternative <= 5.1, prior needed 0.165)
[calc: .../lens-statistician_rates.py]. The 0 per cent rows are robust at any n >= 10; the
85-vs-50 ordering is marginal and needs 27 trials per arm, about what was run.
[new: arXiv:2310.10943 (preprint of doi:10.1126/scirobotics.adg1462), full-text,
"Nominal 4.92± 0.10 44.0 5.03± 0.18 76.0 5.14± 0.09 100.0 Realistic – 0.0 5.34± 0.27 20.0
5.26± 0.32 100.0 Real World – 0.0 5.54± 0.21 50.0 5.35± 0.15 85.0"]

**F10 — Lap times are well measured; reliability is not.** The nominal-simulation gap 4.92 +/- 0.10 s
vs 5.14 +/- 0.09 s is z = 1.6 treating the quoted s.d. as a single trial's uncertainty and z > 7 on
means of n = 25 [calc: .../lens-statistician_rates.py]. Timing claims in this literature carry
10-40x more information per experiment than reliability claims, which is why the field's rankings
are stated in lap times and its failures in anecdotes. The brief's metric is a joint (speed,
reliability) claim and only one half of it is measurable at current trial counts.

**F11 — The apparatus is shared far more than the citation count suggests.** A-01 to A-06, A-07 to
A-10, A-16 to A-18 and A-20 to A-21 all come from one group's Agilicious-derived lineage (750-890 g,
T/W 4.1-4.5) [dossier §7]. The unseen-clutter group is effectively **one** sensor configuration
(D435i, 30 Hz VGA, ~90 deg HFoV, tilted above 7 m/s [A-20]) measured once, not four independent
replications. Only A-11/A-12 (0.52 kg, T/W 12.35, mocap) and A-26 to A-28 (TU Delft, Orin NX) are
genuinely separate platforms. There is no independent replication of any headline agility number in
this evidence base.

**F12 — The winner's-curse signature is present in the dossier's own correction history.** Of the
corrections in §7, the two that touched reliability both moved it *down*: "near 100 per cent at
5-7 m/s" became 80 per cent at 7 m/s, and "no success rate given" for the 16.56 s policy became
1 of 4. Independently, [D-17] and [D-18] report that policies working in-distribution "crash
immediately in unseen configurations" and that all three Swift baselines failed to complete one lap
under domain shift. Both are the expected pattern for first reports selected on success: effect
sizes shrink and reliability falls when the condition is not the one the system was tuned on.

**F13 — Base rate and the prior each claim needs.** The right reference class is not "3-sigma
particle-physics anomalies" but "a single named bottleneck identified post hoc in a complex robotic
pipeline, later confirmed by a controlled one-at-a-time study". The dossier records zero such
controlled studies ([D] §6: "No controlled sensitivity study exists"), five mutually incompatible
attributions [D-21], and a documented history of sim-to-real reversals [D-14, D-17, D-18]. I take a
base rate of 0.15-0.30 for any *particular* named limit being the dominant one. The strongest
reliability-side p-values here (0.0037, 0.0074 two-sided) bound the Bayes factor for the
alternative at <= 10.1, which needs a prior of 0.09 to reach a posterior of 0.5; at a prior of 0.20
the posterior is 0.72. The attribution claims, whose p-values are 0.05-0.26 before multiplicity and
0.23-0.46 after (F8), carry a Bayes factor of about 1: they move nothing. Note that these p-values
only separate "a real effect" from "a fluctuation"; once a real 3.5x seen-vs-unseen gap is granted
(F5), they cannot rank its explanations, which must be separated by the tests in "What data would
settle it".

## Lens-specific outputs

### One row per claimed signal

| Claimed signal | Numbers (counts / effect) | Local significance | Global (look-elsewhere) | Systematics | BF bound (alt:null) | Prior needed | Verdict | Data needed |
|---|---|---|---|---|---|---|---|---|
| S1: ">= 90 % success at 5 m/s, unseen clutter" [A-20] | 10/10; Wilson [0.722, 1.000]; CP95 lower 0.741 | cannot establish >= 0.90 (no test possible) | n/a | one sensor config, one group (F11) | n/a | n/a | **fragile** (true rate may be 0.75) | 29 flawless unseen-course flights |
| S2: "90 % fails above 7 m/s" [D-24] | 8/10 at 7 m/s | one-sided p = 0.264, z = 0.63 | — | per-speed counts unretrieved [D §6] | ~1 | 0.50 | **noise** (does not reject 0.90) | 199 trials/arm to tell 0.90 from 0.80 |
| S3: "60 % at 10 m/s" [A-20] | 6/10 | one-sided p = 0.0128, z = 2.23 | z = 1.7 at 12 looks | difficulty-dependent (90 % on low-difficulty [A-20]) | <= 3.9 | 0.203 | **robust-ish** (threshold failed) | 32 trials/arm suffices here |
| S4: "MonoRace 16.56 s / up to 100 km/h" [A-26, A-27] | 1/4 success | one-sided p = 0.0037, z = 2.68 (threshold rejected) | z = 2.1 at 5 looks | sim-vs-hardware row label uncertain [A-27] | <= 10.1 | 0.090 | **robust** as a *non*-90 % speed | published version; per-row setting |
| S5: seen vs unseen course speed gap (26.2 vs 7.4 m/s) | within chi2 2.97/2, 5.28/3, 0.47/1; between **104.2/2** | z = 10.0 (rho = 0) | survives 80 % assigned spread (p = 0.039) | speeds carry no quoted uncertainty; assigned 20 % | large | <0.01 | **robust** | z = 5.8 at rho = 0.8 (F5) |
| S6: plan-then-track collapses under model error [A-14] | 0/20 vs 17/20 | z = 5.44, p = 5.4e-8 | single prespecified comparison | mocap state, not onboard [D-14] | >> 100 | <0.01 | **robust** | onboard-state repeat |
| S7: RL 85 % > contouring 50 % [A-14] | 17/20 vs 10/20 | z = 2.36, p = 0.018 | 3 controllers compared | one track, one tuning budget per arm | <= 5.1 | 0.165 | **fragile** | 27 trials/arm (about what was run) |
| S8: latency drives tracking error [A-06] | RMSE 0.322 -> 0.474 m for 35 -> >75 ms; log-log slope 0.51 | no uncertainty quoted; n = 1 condition | — | **confounded with the radio link** [A-05, A-06] | n/a | n/a | **fragile** (and RMSE is not the metric) | onboard-only delay injection at fixed link |
| S9: perception range binds (e_range ~ 0.53) | elasticity 0.52-0.61 | algebraic, not statistical | — | assumes a_h free of the thrust budget [D-32] | n/a | n/a | **robust as an elasticity**, not as a dominance claim | one-at-a-time hardware sweep |
| S10: estimation latency binds (e_tau ~ -0.07) | -0.030 to -0.225 (stop), -0.069 to -0.362 (dodge) | algebraic | — | parity with range needs tau > 160-340 ms | n/a | n/a | **eliminated** for tau <= 130 ms | measured end-to-end VIO latency (missing) |
| S11: actuator/rotor bandwidth binds | 39.1 ms thrust time constant [A-03]; enters only inside tau_eff | no paper argues it [D §6] | — | A-03/A-04 are correlated, same group | n/a | n/a | **eliminated** (zero direct evidence + small elasticity) | rotor slew-rate measurement (missing) |
| S12: thrust-to-weight binds (e_TWR ~ 0.55) | -0.565 from two planner points [A-16] vs theory 0.533 [A-34] | two points, no uncertainty: no tension computable | — | planner bound deliberately below the platform limit [D-36] | n/a | n/a | **surviving, tied with S9** | sweep T/W 4 -> 8 on one airframe |

### Failure modes present

| Failure mode | Applies? | Where |
|---|---|---|
| Multiple comparisons / analysis flexibility | **yes, severely** | 5 named limits, ~12 reported cells; global p 0.23-0.46 for a local 0.05 (F8) |
| Optional stopping | **likely** | hardware sessions of 4, 7, 10, 43 flights with no preregistered n; battery and airframe life stop the session (F3) |
| Selection and publication bias | **yes** | every headline speed is the best policy of several (M16 chosen on time, 1/4 success) [A-27] |
| Winner's curse | **yes** | both reliability corrections in dossier §7 moved downward (F12) |
| Regression to the mean | **yes** | domain shift collapses all baselines [D-18]; "crash immediately in unseen configurations" [D-17] |
| Unmodelled systematics | **yes** | battery-voltage droop, variable system delay, aerodynamics all named as causes in one paper [D-14]; no error budget anywhere |
| Signal fading with more data | **untested** | no claim here has been independently replicated (F11) |
| Unequal tuning effort between arms | **probable** | the RL arm was trained 240 h in one case [D-38]; MPC baselines were not retuned per condition [A-14] |
| Test condition chosen after seeing results | **yes** | the "unseen" courses are obstacle fields, the gate tracks are pre-mapped [D-23]; no system is tested on the brief's metric |

### Seeds as the unit of replication

Where a method is stochastic, the number of trained policies, not episodes, is the sample. MonoRace
reports per-policy maxima and per-policy success rates [A-26, A-27]: at least 3 networks, with
88.4 per cent, 71.4 per cent and 25.0 per cent success — a spread across policies (0.25 to 0.88)
that is far larger than any gap claimed between methods. Song et al. report one policy [A-14, F9].
The simulation ablation [D-18] uses 10 forest seeds per method [dossier §7 correction to RC-08], the
only properly seeded comparison in the base. **A spread across seeds that exceeds the gap between
methods means the method comparison is undetermined**, and that is the case for MonoRace.

### What data would settle it

- **The 90 per cent crossing speed.** 29 flawless flights (or 54 with one crash) per speed bin on an
  unseen course, at 5, 7, 9 and 11 m/s: about 150-220 flights. That is a 2-3 week session on one
  airframe, within any of the three groups' means. Nothing cheaper can locate the brief's metric.
- **The elasticity table, measured.** One-at-a-time perturbation on a single platform, each arm with
  >= 32 trials (enough for a 0.90-vs-0.60 call, F3): inject 40 ms of delay at a fixed radio link
  (separating the confound in S8/[A-06]); mask the depth camera beyond 3 m, 6 m, 12 m; cap thrust at
  T/W 3, 4, 6; enable and disable the aerodynamic residual model. Predicted outcome if F6-F7 hold:
  range and thrust arms move mean speed by about 0.5 per cent per per cent, the delay arm by
  0.03-0.2 per cent per per cent. ~500 flights total.
- **The test that separates a real limit from the likeliest artefact (one apparatus, one sensor).**
  Repeat the unseen-clutter protocol on a *different* platform and depth sensor at the same T/W. If
  the 5-10 m/s ceiling is a property of the class it reproduces; if it is a property of the D435i
  configuration [F11] the ceiling moves.
- **The test that separates the leading explanations.** Course-knowledge ablation on one vehicle:
  the same airframe, same policy, flown (a) on a pre-mapped gate track, (b) on the same track with
  gates displaced by 1-2 m, (c) on a track it has never seen, >= 29 trials each. F5 predicts a
  3-4x speed drop from (a) to (c) with the vehicle untouched; any vehicle-limit candidate predicts a
  small drop. This is the cheapest decisive experiment in the whole slate and no one has run it.
- **Where more data cannot help.** `exposure_to_reach` is the wrong tool for S8: the latency-to-RMSE
  slope is limited by a confound (radio link changed with the delay [A-06]), not by statistics, so
  more flights of the same design never resolve it. The design must change.

## Calculations

- `runs/2026-10-15-quadrotor-agility-limit/calc/lens-statistician_rates.py` — binomial intervals and
  one-sided threshold tests for all 11 reported success rates; trials needed to certify >= 0.90
  (29 flawless / 54 with one failure / 85 with three); `trials_to_distinguish` for six pairings
  (199 per arm for 0.90 vs 0.80; 5907 for 0.884 vs 0.90; 32 for 0.90 vs 0.60); two-proportion tests
  on [A-14] (z = 5.44 and 2.36); `tension` on the lap-time gap (z = 1.6 per trial, >7 on n = 25);
  `grouped_chi2` on ln(speed) by course type (within 2.97/2, 5.28/3, 0.47/1; between 104.2/2,
  z = 10.0; pooled S = 3.76) at assigned spreads of 20, 40 and 80 per cent and at rho = 0 and 0.8
  (between 37.6/2, z = 5.8); `min_bayes_factor` and `prior_needed` for four claims;
  elasticities of the stop and dodge bounds to range, acceleration and latency over six regimes;
  `sidak_global_p` for 4, 5 and 12 attributions; Wilson intervals on crash-cause shares.
  Verification: binomial tail against the closed form (exact), Clopper-Pearson lower bound for
  k = n against 0.05^(1/n) (exact), the tau -> 0 limit of the elasticities (0.5, 0.5 as required),
  reproduction of the dossier's own A-33 case (14.524 m/s vs 14.5; e_tau -0.0644 vs -0.064), and
  within + between = pooled chi2 to 1e-9. All five PASS.

## Candidate answers

- [STAT-A] **Null: no single limit dominates.** The two largest elasticities — usable perception
  range (0.52-0.61) and thrust-side acceleration / T/W (0.39-0.49 computed, 0.533 theory at T/W 4, 0.565 measured on a real
  track) — are within 15 per cent of each other, and the brief's own premise 1 then makes "none
  dominates" the honest answer. | status: **surviving** | why: F6, F7; [A-16], [A-33], [A-34],
  [D-33]; and no controlled sensitivity study exists to break the tie [D §6] | test: the
  one-at-a-time elasticity sweep (>= 32 trials per arm); the null predicts the range and thrust arms
  move speed by a similar amount and neither by more than twice the other | confidence: high
- [STAT-B] **Reframe: the binding variable in the measured record is course knowledge, not any
  vehicle limit.** Grouping every onboard speed by course type gives a between-group chi2 of 104/2
  (z = 10.0, and 5.8 at rho = 0.8) against within-group chi2 of 0.5-5.3: seen 26.2 m/s vs unseen
  7.4 m/s on the same airframe class. | status: **surviving** | why: F5, F11; [A-20], [A-26],
  [A-29], [D-11], [D-23] | test: the course-knowledge ablation (pre-mapped / displaced / unseen,
  same vehicle, >= 29 trials each): a 3-4x drop with the vehicle untouched | confidence: high
- [STAT-C] **Reframe: the metric is unmeasurable at the trial counts anyone runs, so no ranking in
  this literature is statistically supported.** Certifying >= 90 per cent needs 29 flawless flights;
  telling 90 from 80 per cent needs 199 per arm; the biggest set published is 43 and the median is
  10. | status: **surviving** | why: F1, F2, F3, F8; `wilson_interval`, `trials_to_distinguish`
  [calc] | test: any group reporting 29 consecutive unseen-course successes at a stated speed would
  refute the "unmeasurable in practice" half | confidence: high
- [STAT-D] **Perception look-ahead (usable range) binds first.** Largest single elasticity of the
  agility metric, +0.52 to +0.61, and 2.7-17x that of latency in every regime computed.
  | status: **strained** as a *dominance* claim (it ties with thrust, STAT-A), surviving as "the
  largest single elasticity" | why: F6; [D-31], [D-32], [A-21], [A-33]; the 7 m/s perception
  attribution it is usually cited for rests on 2 crashes, Wilson [0.34, 1.00] (F8) | test: mask the
  depth camera at 3 / 6 / 12 m; range elasticity ~0.5 | confidence: medium
- [STAT-E] **Thrust-to-weight / actuator acceleration ceiling binds first.** The only candidate with
  a measured elasticity on a real track (-0.565 lap time per T/W [A-16]) agreeing with theory
  (0.533) to 6 per cent. | status: **strained** (ties with STAT-D; and planners deliberately run
  inside the thrust margin [D-36], so the ceiling is not being touched) | why: F7; [A-16], [A-34],
  [D-33], [D-36] | test: sweep T/W 4 -> 8 on one airframe, mocap state held fixed; STAT-E predicts
  about +20 per cent mean speed for a doubling, STAT-D predicts almost none | confidence: medium
- [STAT-F] **State-estimation latency binds first.** | status: **eliminated by my method** for
  current hardware: at tau = 17-40 ms [A-07, A-28] the elasticity is -0.03 to -0.15 and parity with
  range needs tau > 160-340 ms (F6); the one measurement offered [A-06] is a single confounded
  condition with no uncertainty (S8). It survives only as a historical statement about the 130 ms
  regime [A-22], where e_tau reaches -0.23 to -0.36. | test: inject 40 ms at a fixed radio link
  | confidence: medium
- [STAT-G] **Rotor and motor bandwidth binds first.** | status: **eliminated**: no source argues it
  [D §6], its 39.1 ms time constant enters only inside tau_eff whose elasticity is small (F6), and
  the two numbers that exist [A-03, A-04] share an apparatus so they are one measurement, not two
  | test: measured rotor slew rate against the commanded jerk of a time-optimal trajectory
  | confidence: medium
- [STAT-H] **A systematic in one named method: the 5-10 m/s unseen-course ceiling is a property of
  one depth-camera configuration on one group's airframe, not of the vehicle class.** The four
  "independent" unseen-clutter points reduce to one apparatus (D435i, 30 Hz VGA, ~90 deg HFoV,
  tilted above 7 m/s), one group, one protocol [F11, A-20, A-21, dossier §7]; at rho = 0.8 that group
  carries an 18 per cent effective error on its own mean. | status: **surviving** | why: F11, F12;
  no independent replication of any headline number exists | test: repeat the protocol on a
  different platform and depth sensor at matched T/W; if the ceiling moves by more than a factor
  1.5, the ceiling was the apparatus | confidence: medium
- [STAT-I] **Model error mediated by controller structure (plan-then-track fragility) binds first.**
  The only signal in the base with a p-value below 1e-6: 0/20 vs 17/20 under a realistic model
  (z = 5.44). | status: **strained**: robust as a statement about *pipelines*, but it was measured
  with mocap state [D-14], so it is controller evidence, and it says a limit is removable by a
  software choice rather than naming a physical limit | why: F9, F10 | test: repeat the three-way
  comparison with onboard VIO state | confidence: high (for the effect), low (for "binds first")

## What would change my mind

- A published set of >= 29 consecutive successful unseen-course flights at a stated speed. That
  single artefact would convert STAT-C from "unmeasurable" to "measured" and give the brief's metric
  a denominator.
- A one-at-a-time sensitivity study in which the latency arm moved mean speed by more than about
  0.2 per cent per per cent. That would refute F6 and revive STAT-F, and would most likely mean the
  stop/dodge bounds [D-31, D-32] are the wrong model of what latency does (for example, that its
  real cost is estimator divergence, not reaction distance — a mechanism no bound here captures).
- Any demonstration that an unseen cluttered course can be flown above about 15 m/s on onboard
  sensing. That would collapse the seen/unseen group split in F5 and undercut STAT-B.
- Quoted uncertainties on the planner-sweep elasticity [A-16] showing it differs from 0.5 by more
  than its error, which would let a tension be computed and could separate STAT-D from STAT-E.

## Assumptions I relied on

- Where [A-20] quotes a rate of 60 or 100 per cent without a count I take n = 10, because the
  paper's own 7 m/s row is 8/10 and 60 per cent needs n >= 5. If the true n is 5 the intervals widen
  and every conclusion in F1-F3 strengthens.
- Trial counts for [A-14] are inferred from the granularity of the reported percentages (multiples
  of 1/25 in simulation, 1/20 in the real world), so my z-values there are lower bounds. The counts
  are still not stated in the paper's text (F9).
- No source quotes an uncertainty on a demonstrated speed. For F5 I assign a 20 per cent fractional
  spread in ln(speed) and show the result at 40 and 80 per cent as well; this is my assumption, not
  a measurement.
- Elasticities are computed from the dossier's own point-mass bounds [D-31, D-32], which neglect
  rotational dynamics (a criticism the dossier itself records at [RC-09]), estimation error and the
  coupling between braking acceleration and the thrust budget. They rank candidates; they do not
  predict a speed.
- Success rates are treated as independent Bernoulli trials. Battery state, airframe wear and
  operator learning within a session all violate this, in the direction of making the intervals
  above too narrow.
