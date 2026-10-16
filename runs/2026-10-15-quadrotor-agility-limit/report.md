# What limits the agility of an autonomous quadrotor: report
*Run 2026-10-15-quadrotor-agility-limit · 2026-10-16 · depth standard · question: "For a quadrotor flying autonomously on onboard sensing and computation alone, which limit binds first on closed-loop agility — rotor and actuator bandwidth, state-estimation latency, unmodelled aerodynamics, or how far ahead it can perceive — and what would it take to move that limit?"*

## Bottom line

On a course the vehicle has not seen, how much of the world it can see ahead binds first: the usable detection range of its depth sensor (about 4–6 m in practice, not the datasheet 10 m) multiplied by how much of that view survives the tilt a hard manoeuvre demands. Credence about 0.40, with "no single limit" and "estimator breakdown" as the main alternatives. The biggest reason: on a verified simulation of a 0.75 kg racing quadrotor, doubling detection range raises the safe speed by about 118 per cent while doubling thrust gives 28 per cent and halving latency, motor lag or aerodynamic model error gives under 6 per cent each, and that ordering is proved to hold for every parameter value. The caveat that matters: nobody has measured the brief's metric on hardware, so this is a model ranking with one hardware cross-check, and a one-day depth-clip experiment would settle it.

## Ranked answers

Exclusive slate (candidates.md): probabilities sum to 1 with an explicit "none of these". Performance here is a closed-loop property, so the orders-of-magnitude gap is zero and the column reports the evidence rung each candidate reached (rule 4).

| # | Candidate | Fits the evidence? | Key obstacle | Evidence rung reached (verified model / model-error / hardware) | Credence |
|---|---|---|---|---|---|
| 1 | C1 Perceived volume ahead (usable range x visible solid angle at manoeuvre attitude) | Yes, narrowed: largest elasticity by 4x on the verified plant; active above ~10 m/s; hardware failure at 7 m/s attributed to late field-of-view entry | Bound may be slack at 5–7 m/s; range elasticity measured on an isolated dodge, not a course | Verified model (24/24 rows); hardware attribution rests on 2 crash events; cross-apparatus LiDAR point only | 0.40 |
| 2 | C2 Estimation: drift/feature loss (not latency) | Partly: a real wall at ~15–20 m/s (classical VIO ATE 47–98 m on a 19.4 m/s track); but drift elasticity in the unseen regime is -0.02 to -0.19 | "Repaired only by prior track knowledge" is false (camera-free IMU odometry 0.56 m vs 0.48 m ATE) | Hardware estimator-accuracy data (mocap-scored, seen track); no drift in m/m at racing speed | 0.12 |
| 3 | C7 Null: no single limit dominates | Partly: two lowest bounds coincide at 10.73 and 10.85 m/s (1.1 per cent); range and braking are near-substitutes in the stop bound | In the improving direction the top elasticity leads by 4.2x; seven of seven spreads exceed 2 | Arithmetic on verified model rows | 0.11 |
| 4 | C4 Stack robustness and designer margin, no hardware limit active | Refuted as stated: one hardware swap (range 6 -> 10 m) gives +74 per cent against its own 20 per cent threshold; lowest hardware cap 9.55 m/s on the A-20 geometry | Architecture is a large term (0 vs 85 per cent on fixed hardware) but that result used motion capture on a seen track | Hardware (mocap state) for the architecture effect; verified model for the refutation | 0.10 |
| 5 | None of these (e.g. battery sag/power, compute throughput, a body-rate coupling no candidate names) | Unquantified; pack sag costs ~10 per cent of speed [M-MECH-09 corrected] | No candidate or measurement isolates it | — | 0.07 |
| 6 | C3 Course knowledge (map) is what fast flights use | Refuted as "first": in the metric's own mean-speed class the seen/unseen split is 1.2–1.9x, not 2.6–6.4x | An unmapped LiDAR flight above 20 m/s exceeds the best mapped mean (12.9 m/s); ablation never run | Hardware, between-apparatus; SUPER abstract plus press only | 0.06 |
| 7 | C5 Actuator envelope (thrust authority, torque ceiling) | Refuted: elasticity to installed thrust is 0.00 at the measured 8.5 N per rotor; regime (seen course, 15–20 m/s) lies outside the metric | No paper argues it; +0.527 arc was below installed thrust | Verified model plus one hardware planner sweep (+0.565, a commanded bound) | 0.05 |
| 8 | C6 Unmodelled aerodynamics above ~13 m/s | Refuted: closed-loop error 0.15–0.20 m at 13–15 m/s against the 0.45 m open-loop law; removing all aero model error makes the plant slower (x0.59–0.77) | Hardware decomposition puts the aero term 2.5x behind inner-loop lag inversion | Model-error (open-loop replay, mocap); regime above every unseen-course speed flown | 0.05 |
| 9 | C8 Reframe: metric is not an observable; ranking does not exist | Metrology half survives (no bin reaches n = 29); non-existence half refuted: partials exist in closed form and are strictly ordered at 80/80 points | A sum rule on derivatives is not their non-existence | Verified arithmetic | 0.04 |

## Why, candidate by candidate

**C1 (0.40).** For: on the lens's 17-state plant (energy drift 5.9e-12, angular momentum 7.1e-15, RK4 order 4.005, two implementations agreeing to 8.9e-16, parameters from Sun et al. measurements, motor time constant 39.1 ms from a load-cell fit [A-03]), an equal factor-of-two relaxation of each limit on the dodge task gives range +117.8 per cent, thrust +28.3, motor lag +5.9, latency +5.5, drag +1.8 (calc/falsifier-C7-0_factor2.py.log). The range elasticity (+0.986/+1.082, M-SIMULATOR-07 verified) is reproduced by three refuters to 0.13 per cent, and e_s = 1 > e_a < 1/2 > |e_tau| is proved over the whole domain (M-DIAL-06, M-EXAMINER-01). The only hardware attribution at the failure onset names "objects entered the field of view very late because of the high angular velocity" [D-13], which is the solid-angle leg in its dynamic form. The one large range increment ever taken on hardware (3-D LiDAR, SUPER) reports "over 20 m/s in unknown environments", about 3x the depth-camera figures. Against: C1's refuter shows both legs slack by 1.6–3.8x at 7 m/s and A-21's own bound (same paper as A-20) at 12.0–13.5 m/s, so the bound is active only above about 10 m/s; the near-unity elasticity is a homogeneity identity that carries no information about activity. I weigh this less than the refuter does because 8/10 at 7 m/s does not reject 0.90 (one-sided p = 0.264, Clopper–Pearson lower bound 0.49, M-STAT-02), so the hardware record locates the 90-per-cent ceiling only somewhere in 5–10 m/s, which the 9.5–14 m/s model caps bracket. The mechanist's "FoV > range" ordering was refuted (M-MECH-03: +4.67 vs +5.85 per cent), so leg (1a) leads leg (1b). Decisive test: same airframe and policy, depth stream clipped at 3/6/10/20 m and lens swapped 58 -> 155 deg, >= 29 trials per cell (about 120–250 flights; UZH RPG, TU Delft, or an A2RL team).

**C2 (0.12).** For: classical VIO fails outright at 19.4 m/s on a racing track (ATE 98.2 and 47.2 m, Cioffi et al. 2023), blur is rotation-dominated above 229 deg/s (M-MECH-07 verified), and the simulator's model card names drift and blur as its largest omission. Against: with a drift channel added to the verified plant, the relative-frame elasticity is -0.023 to -0.191, below the latency term C2 itself eliminated (falsifier-C2-0_drift.py.log); A-20's architecture tolerates 12.5 per cent of distance in global error; and the "only prior track knowledge" clause is refuted by a camera-free estimator at 0.56 m ATE. Latency sub-hypothesis (2b) is eliminated at 2026 values by verified elasticities (-0.03 to -0.36) and the human-pilot comparison (|e| = 0.02–0.11, M-EMP-05). Decisive test: log VIO drift in m per m against body rate at fixed speed, then rerun with an oracle estimate.

**C7 (0.11).** For: the thrust bang-bang mean (10.73 m/s) and FoV-capped stop bound (10.85 m/s) coincide to 1.1 per cent exactly where A-20 degrades to 60 per cent (M-EXAMINER-08 verified); in the stop bound e_s + e_a = 1 identically, so range and braking are near-substitutes. Against: by the brief's definition (elasticity in the improving direction, holding others fixed) the top term leads by 4.16x, and all seven spreads C7 cites exceed 2 (M-EMP-11 caveat: 2.33 on endpoints). It survives only as "two bounds are active at 10–11 m/s", which is a regime statement, not a tie between rival candidates. Would revive if a dense-clutter measurement returned e_s near 0.6.

**C4 (0.10).** For: 0/20 vs 17/20 on fixed hardware is the only p < 1e-6 signal in the record (M-STAT-09, trial counts inferred), and the time-optimal profile is untrackable at a quarter of its acceleration budget (simulator F11). Against: on its own plant and anchors a single attainable hardware swap moves the metric +74 per cent, and the lowest hardware-capped ceiling on the A-20 geometry is 9.55 m/s, 0.96x the 10 m/s point (falsifier-C4-0_hardware_active.py.log). Note the two refuters disagree on whether the 58 deg vertical FoV cap applies to a lateral dodge (C1's refuter: a roll keeps the velocity on the optical axis, so the cap is 9.9–17.4 m/s); either way the caps bracket the 10 m/s point. The surviving core, that architecture fills the gap between 7 m/s and the 9.5–14 m/s caps, is why it keeps 0.10.

## Eliminated, and what eliminated them

- **C3** — verdicts/C3-0.md (calculation): the z = 9.9 split compares seen peaks with unseen means; inside the mean class it is 1.54–1.92x; best-case vs best-case 1.29x; the same eight numbers partition better by sensor range (chi2 71.8 vs 53.3).
- **C5** — verdicts/C5-0.md (calculation): elasticity to installed thrust +0.0000 at 8.5 -> 12 N (tight tolerance, 0.0 per cent mixer saturation); +0.527 was the 6 -> 7.5 N arc below installed thrust; halving the motor lag it dismissed gives +15.8 per cent.
- **C6** — verdicts/C6-0.md (calculation plus hardware): closed-loop error 0.15 m at 13 m/s vs 0.445 m predicted; exact aero feedforward slows the plant; Sun et al. Table VIII puts the drag model at 0.147 m of RMSE against 0.371 m for the inner loop; Tal & Karaman 6.6 cm at 12.9 m/s on hardware.
- **C7 and C4** are refuted as stated (verdicts/C7-0.md, C4-0.md) and kept at 0.11 and 0.10 for the narrowed residues above.
- **C8** — verdicts/C8-0.md (calculation): partials exist in closed form, strictly ordered at 80/80 points; the certification protocol costs 26 min of air time, so the metric is unmeasured, not unobservable. M-STAT-11 and M-STAT-12 refuted two of its statistical legs.

## Assumptions every surviving answer shares

1. The verified plant's omissions (VIO drift, blur, battery sag, blade flapping, quadratic drag) do not reorder the elasticities; the model card says each would strengthen estimation, actuator or aero candidates at high speed.
2. The dodge manoeuvre's range elasticity transfers to a cluttered course; the lens's own course-based measurement failed (simulator F13), so the perception axis rests on a single-obstacle geometry.
3. The A-20 platform (890 g, T/W 4.4, D435i, T265) is representative; it is the only unseen-course hardware set with per-speed numbers, and all Agilicious-lineage anchors share one apparatus.
4. The metric is defined at the 90-per-cent ceiling, whose location on hardware is known only to within 5–10 m/s.
5. The time-optimal denominator is the flying-start point-mass optimum (4.502 s on the model course); rest-to-rest is 12 per cent longer (M-SIMULATOR-01 note).

## What would change this verdict

1. **Within-apparatus depth-clip sweep** (UZH RPG or TU Delft, one day of flying, >= 29 trials per cell; the November 2026 identical-hardware final could produce it if onboard compute is mandated [D-41]). Mean speed flat under clipping at 3–10 m would halve C1 to about 0.2 and lift C4/C2; a gain of 1.4–2x per doubling would raise C1 to about 0.7.
2. **Measured VIO drift in m per m against body rate at 7–15 m/s** (replay of the UZH-FPV dataset through a current estimator; days, no money). Drift above about 5 per cent per metre at 10 m/s would move C2 to parity with C1; below 1 per cent would push C2 under 0.05.
3. **Per-trial outcomes at n >= 29 per speed bin from any onboard-only unseen-course flight.** Locating the 90-per-cent ceiling at 5–6 m/s (well below every computed cap) would move probability from C1 to C4 and "none"; locating it at 9–11 m/s would confirm the hardware caps and C1.

Reading (b): once perceived volume is relaxed to LiDAR-class range, the next walls on the record are estimator integrity at 15–20 m/s (classical VIO divergence; relative-frame drift tolerance fails somewhere between 5 and 20 per cent per metre) and thrust/braking authority (second elasticity, +28 per cent per doubling), with inner-loop lag inversion (INDI) the cheap route to the latter.

## Key numbers

| Quantity | Value (units) | Source or calc |
|---|---|---|
| Factor-2 relaxation gains, dodge task (SI) | range +117.8 %, thrust +28.3 %, motor tau +5.9 %, latency +5.5 %, drag +1.8 % | calc/falsifier-C7-0_factor2.py.log |
| Range elasticity on verified plant | +0.986 (3 -> 6 m), +1.082 (6 -> 10 m) | M-SIMULATOR-07 verified |
| Lowest hardware-capped ceiling, A-20 geometry | 9.55 m/s (4.1 m range, a_u = 16.3 m/s^2) to 17.4 m/s (horizontal FoV reading) | falsifier-C4-0, falsifier-C1-0 logs |
| A-21 perception bound, same paper as A-20 | 12.0 / 13.2 / 13.5 m/s | dossier A-21 |
| Unseen-course hardware success | 10/10 at 5 m/s (CP lower 0.741); 8/10 at 7 m/s (p = 0.264 vs 0.90); 6/10 at 10 m/s | dossier A-20, M-STAT-02 |
| Usable stereo range (depth noise = 0.1 m obstacle) | 4.1–5.8 m at 50 mm baseline | M-MECH-06 verified |
| Elasticity to installed thrust at measured value | +0.0000 (8.5 -> 12 N, tight tolerance) | falsifier-C5-0_envelope.py.log |
| Hardware T/W sweep elasticity (commanded bound) | d ln(lap)/d ln(TWR) = -0.565 | dossier A-16, M-STAT-07 |
| Relative-frame drift elasticity | -0.023 (0.5 -> 2 %/m), -0.191 (2 -> 5 %/m) | falsifier-C2-0_drift.py.log |
| Classical VIO at 19.4 m/s racing track | ATE 98.2 m (OpenVINS), 47.2 m (SVO); Gate-IO 0.48 m; IMO 0.56 m | Cioffi et al. 2023, via verdicts/C2-0.md |
| Seen/unseen split, mean-speed class | 1.54–1.92x (published grouping 3.54x) | falsifier-C3-0_split.py.log |
| Closed-loop gate error, no aero model | 0.151 m at 13 m/s, 0.202 m at 15 m/s (open-loop law 0.445 / 0.503 m) | falsifier-C6-0_aero.py.log |
| Delay margins, inner / outer loop | 27.57 ms vs 2.00 ms budget; 354.0 ms vs 22.5 ms | M-SIMULATOR-05 verified |
| Human vs Swift latency elasticity | \|e\| = 0.016–0.113 (220 vs 40 ms) | M-EMP-05 verified |
| Flights to certify p >= 0.90 (one-sided 95 %) | 29 / 46 / 76 for 0 / 1 / 3 failures | M-STAT-11 corrected |
| Time-optimal denominator, model course | 4.502 s flying start (5.039 s rest-to-rest), 98.315 m | M-SIMULATOR-01 |

## Caveats

- No published result measures the brief's three-part metric; A-20's per-speed trial counts were not retrieved; A-29's "100 per cent" has no counts.
- SUPER (Ren et al., Science Robotics 2025, doi:10.1126/scirobotics.ado6187) is cited by two refuters from an abstract and an institutional news page; whether 20 m/s is a mean or a peak, the clutter density, trial counts and the erratum's content are unknown. Request it; it decides how much of C3's residual and C1's cross-regime support survive.
- MonoRace numbers (A-26 to A-28) are from the arXiv v1 preprint; the published version was not opened.
- The "0.3–3 m usable D435i range" input is a search summary; the verified 4.1–5.8 m stereo-noise ceiling is used instead.
- The A-14 architecture result used Vicon state and inferred trial counts; it is controller evidence.
- Two refuters disagree on whether the vertical or horizontal FoV caps a lateral dodge; the caps bracket the 10 m/s point either way, but the 9.55 m/s figure is convention-dependent.
- Math checks refuted: M-MECH-03 (FoV > range), M-SIMULATOR-11/12/13, M-DIAL-03/09, M-STAT-11/12, M-EXAMINER-06, M-CONSTRAINTS-10, M-MECH-04/09, M-EMP-07; none reversed a ranking, and M-MECH-03 demoted leg (1b) below (1a) within C1.
- Semantic Scholar was rate-limited during research, so 2025–26 coverage is incomplete.

## Sources

- Dossier: runs/2026-10-15-quadrotor-agility-limit/dossier.md (anchors A-01 to A-34, claims D-01 to D-42).
- Loquercio et al., "Learning high-speed flight in the wild", Science Robotics 2021 — dossier [A-20], [A-21], [D-13].
- Kaufmann et al., "Champion-level drone racing using deep reinforcement learning", Nature 2023 — dossier [A-07] to [A-10], [D-11], [D-12], [D-16].
- Falanga, Kim, Scaramuzza, RA-L 2019, doi:10.1109/lra.2019.2898117 — dossier [D-31].
- Sun, Romero, Foehn, Kaufmann, Scaramuzza, T-RO 2022, doi:10.1109/TRO.2022.3177279, https://arxiv.org/abs/2109.01365 — plant parameters, [D-09], Table VIII.
- Bauersfeld et al., NeuroBEM — dossier [A-18], [D-08].
- Song et al., Science Robotics 2023, doi:10.1126/scirobotics.adg1462, https://arxiv.org/abs/2310.10943 — [A-14], [D-14], [D-15].
- Cioffi, Bauersfeld, Kaufmann, Scaramuzza, RA-L 2023, doi:10.1109/lra.2023.3252342, https://arxiv.org/abs/2210.15287 — IMO ATE table.
- Ren et al., SUPER, Science Robotics 2025, doi:10.1126/scirobotics.ado6187; abstract via https://researchportal.hkust.edu.hk/en/publications/safety-assured-high-speed-navigation-for-mavs/ and https://mech.hku.hk/safety-assured-high-speed-navigation-for-mavs-a-paper-in-science-robotics/ (no free full text).
- Tal and Karaman, doi:10.1109/TCST.2020.3001117 — 6.6 cm RMS at 12.9 m/s.
- Bahnam et al., MonoRace, https://arxiv.org/abs/2601.15222 (preprint) — [A-26] to [A-28].
- Qin et al., https://arxiv.org/abs/2603.04305 — perception-aware planning ablation.
- Foehn et al., Agilicious — dossier [A-01] to [A-03].
- Run files: candidates.md; verdicts/C1-0.md to C8-0.md; math/*.md; analyses/simulator.md; calc/falsifier-C*-0_*.py.log.