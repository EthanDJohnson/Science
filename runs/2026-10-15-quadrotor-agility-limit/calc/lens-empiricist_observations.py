"""
Empiricist lens: what the HARDWARE observations alone constrain.

All inputs are quoted numbers from the dossier (SI units; speeds in m/s, times in s).
Nothing here is a dynamics simulation: every number is either (a) an exact binomial
statement about a reported trial count, (b) arithmetic on a reported time and a
reported course length, or (c) a ratio of two reported numbers.

Sections
  1. Resolvability of the brief's "90 per cent success" criterion given the trial
     counts that actually exist (Clopper-Pearson, exact).
  2. How many trials the criterion would need. Verification: closed form
     0.05**(1/n) for an all-success run is compared with the Clopper-Pearson solver.
  3. Mean speed of the onboard-only demonstrations, seen vs unseen course.
  4. Observed speed as a fraction of each published/computed bound at the same
     operating point (perception-latency bound, thrust-to-weight point-mass bound).
  5. Simulation-to-hardware discount factors actually measured in this literature
     (the base rate my lens needs).
  6. The dossier's own elasticities, ranked, with the observed seen/unseen ratio
     put on the same axis.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import stats_tools as st

print("=" * 72)
print("1. EXACT BINOMIAL INTERVALS ON EVERY REPORTED HARDWARE SUCCESS RATE")
print("=" * 72)
# (label, successes, trials, speed m/s, setting)
obs = [
    ("Loquercio unseen forest, 7 m/s [A-20]", 8, 10, 7.0, "onboard, unseen clutter"),
    ("Loquercio unseen, 10 m/s (60%, n assumed 10) [A-20]", 6, 10, 10.0, "onboard, unseen clutter"),
    ("Loquercio unseen, 5 m/s (100%, n assumed 10) [A-20]", 10, 10, 5.0, "onboard, unseen clutter"),
    ("Loquercio unseen, 3 m/s (100%, n assumed 10) [A-20]", 10, 10, 3.0, "onboard, unseen clutter"),
    ("MonoRace M23 (seen track) [A-27]", 38, 43, None, "onboard, seen track"),
    ("MonoRace M17 (seen track) [A-27]", 5, 7, None, "onboard, seen track"),
    ("MonoRace M16 fastest policy (seen track) [A-27]", 1, 4, None, "onboard, seen track"),
    ("Song RL policy, real, mocap state (n assumed 20) [A-14]", 17, 20, None, "mocap state"),
    ("Song contouring MPC, real, mocap (n assumed 20) [A-14]", 10, 20, None, "mocap state"),
]
print(f"{'case':52s} {'k/n':>7s} {'p':>6s} {'CP 95% lower':>13s} {'upper':>7s}  90% excluded?")
for label, k, n, v, setting in obs:
    lo, hi = st.clopper_pearson_interval(k, n, 0.95)
    excl = "yes (below)" if hi < 0.90 else ("yes (above)" if lo > 0.90 else "NO")
    print(f"{label:52s} {k:3d}/{n:<3d} {k/n:6.3f} {lo:13.3f} {hi:7.3f}  {excl}")
print()
print("Note: the per-speed trial counts for A-20 at 3, 5 and 10 m/s were NOT reported;")
print("n = 10 is assumed by analogy with the 7 m/s row (8 of 10). The A-14 counts (20)")
print("are likewise unsupported (dossier section 7). Rows so marked are illustrative of")
print("the resolving power of a 10- or 20-trial experiment, not of a stated result.")

print()
print("=" * 72)
print("2. TRIALS NEEDED TO ESTABLISH OR REFUTE THE 90 PER CENT CRITERION")
print("=" * 72)
for n in (10, 15, 20, 25, 29, 30, 35, 40, 60):
    lo, hi = st.clopper_pearson_interval(n, n, 0.95)
    # verification: for k = n the two-sided CP lower bound is exactly alpha/2 ** (1/n)
    closed = 0.025 ** (1.0 / n)
    print(f"  n consecutive successes = {n:3d}: CP lower bound = {lo:.4f} "
          f"(closed form 0.025^(1/n) = {closed:.4f}, diff {abs(lo-closed):.2e})")
n_one = math.ceil(math.log(0.05) / math.log(0.90))
n_two = math.ceil(math.log(0.025) / math.log(0.90))
print(f"  -> smallest all-success n with a ONE-sided 95% lower bound >= 0.90: n = {n_one}")
print(f"  -> smallest all-success n with a TWO-sided 95% (CP) lower bound >= 0.90: n = {n_two}")
for p1, p2 in ((0.90, 0.80), (0.90, 0.60), (0.95, 0.85)):
    n = st.trials_to_distinguish(p1, p2, 0.95, power=0.8)
    print(f"  trials per arm to tell p={p1} from p={p2} (95%, 80% power): {n}")

print()
print("=" * 72)
print("3. MEAN SPEED OF THE ONBOARD-ONLY DEMONSTRATIONS (course length / time)")
print("=" * 72)
# Swift: best three-lap time-to-finish 17.465 s [new: Nature23_Kaufmann.pdf]; lap 75 m [A-10]
swift_lap_m = 75.0
for t3, what in ((17.465, "best three-lap time-to-finish"),):
    v = 3 * swift_lap_m / t3
    print(f"  Swift, {what} = {t3} s over 3 x {swift_lap_m} m -> mean {v:.2f} m/s")
for tlap, what in ((5.52, "lowest median single-lap figure on the panel"),
                   (6.80, "highest median single-lap figure on the panel")):
    print(f"  Swift, single lap {tlap} s over {swift_lap_m} m -> mean {75.0/tlap:.2f} m/s  ({what})")
print("  (the panel's label-to-median mapping is garbled in extraction, so 11.0-13.6 m/s")
print("   is the bracket, and 12.88 m/s from the stated 17.465 s is the firm number)")
print()
# MonoRace: 11 gates in a 100 x 30 m hall, two laps; lap length not reported.
for lap_m in (100.0, 150.0, 200.0, 250.0):
    for t2, pol in ((16.56, "M16 (1/4 success)"), (23.0, "M23 (38/43 = 88.4%)")):
        print(f"  MonoRace {pol:22s} lap {lap_m:5.0f} m -> mean {2*lap_m/t2:5.2f} m/s")
print("  A2RL 2025 press: 170 m course, two laps in 17 s -> mean "
      f"{2*170/17:.1f} m/s if lap = course length [A-31, press only]")
print()
print("  Best-documented onboard-only UNSEEN-course speed meeting >=90% point estimate: 5 m/s [A-20]")
print("  Onboard-only SEEN-course mean speeds: Swift 12.9 m/s; MonoRace 13-30 m/s (lap length unknown)")
for seen in (12.88, 13.0, 20.0, 30.0):
    print(f"    ratio seen/unseen at 5 m/s: {seen/5.0:.2f}")

print()
print("=" * 72)
print("4. OBSERVED SPEED AS A FRACTION OF ITS OWN PUBLISHED BOUND")
print("=" * 72)
# A-21: the same paper's own perception-latency/range bound, 12.0 / 13.2 / 13.5 m/s
for bound, name in ((12.0, "A-21 low"), (13.5, "A-21 high")):
    for v, vname in ((5.0, "100% point estimate"), (7.0, "80% (8/10)"), (10.0, "60%")):
        print(f"  v = {v:4.1f} m/s ({vname:20s}) / perception bound {bound} m/s ({name}) "
              f"= {v/bound:.2f}")
# thrust-to-weight point-mass bound over the same 40 m reference line, T/W = 4.4
g = 9.81
for twr in (4.4,):
    a_h = g * math.sqrt(twr**2 - 1)
    for d in (40.0,):
        t = 2 * math.sqrt(d / a_h)          # bang-bang rest-to-rest
        v_mean = d / t
        v_peak = math.sqrt(a_h * d)
        print(f"  T/W {twr}: a_h = {a_h:.2f} m/s^2; {d:.0f} m rest-to-rest bang-bang "
              f"t = {t:.2f} s, mean {v_mean:.2f} m/s, peak {v_peak:.2f} m/s")
        for v in (5.0, 7.0, 10.0):
            print(f"    observed {v:4.1f} m/s / point-mass mean {v_mean:.2f} m/s = {v/v_mean:.2f}")
        # verification: closed form vs numeric integration of bang-bang
        n = 200000
        dt = t / n
        x = 0.0; u = 0.0
        for i in range(n):
            acc = a_h if i < n / 2 else -a_h
            u += acc * dt
            x += u * dt
        print(f"    verification: integrated distance {x:.4f} m vs {d:.4f} m "
              f"(rel err {abs(x-d)/d:.2e}), final speed {u:.3e} m/s")

print()
print("=" * 72)
print("5. MEASURED SIMULATION-TO-HARDWARE DISCOUNT (the base rate)")
print("=" * 72)
pairs = [
    ("A-29 compact perturbed-gate track: own sim 10.0 m/s vs real 5.3 m/s", 10.0, 5.3),
    ("D-40 unseen clutter: sim 19.4 m/s vs best real unseen 8.0 m/s", 19.4, 8.0),
    ("D-40 unseen clutter: sim 19.4 m/s vs 90%-reliable real 5.0 m/s", 19.4, 5.0),
    ("A-20 vs its own sim forest at 10 m/s: 60% real vs 60% sim (success, not speed)", 0.60, 0.60),
]
ratios = []
for label, s, r in pairs:
    if s > 1:
        ratios.append(s / r)
        print(f"  {label:66s} ratio {s/r:.2f}")
    else:
        print(f"  {label:66s} ratio {s/r:.2f}")
print(f"  speed discount factors: {['%.2f' % x for x in ratios]}; "
      f"geometric mean {math.exp(sum(math.log(x) for x in ratios)/len(ratios)):.2f}")
print("  success-rate collapse under domain shift [A-14]: tracking MPC 44.0% (nominal sim)"
      " -> 0.0% (realistic sim) -> 0.0% (real); contouring 76.0 -> 20.0 -> 50.0; RL 100 -> 100 -> 85")
print("  [D-18] all three Swift baselines: laps completed with ideal dynamics and "
      "ground-truth state, zero laps completed under domain shift (simulation ablation)")

print()
print("=" * 72)
print("6. ELASTICITIES ON ONE AXIS (per cent speed per per cent limit)")
print("=" * 72)
rows = [
    ("perception range s, stop bound [A-33]", 0.52, 0.53, "own calc, point mass"),
    ("perception range s, dodge bound [A-33]", 1.00, 1.00, "own calc, point mass"),
    ("braking/lateral accel a [A-33]", 0.43, 0.48, "own calc, point mass"),
    ("thrust-to-weight, point mass [A-34]", 0.50, 0.54, "own calc (0.5 * e(a_h,TWR))"),
    ("thrust-to-weight, planner sweep on a real track [A-16]", 0.565, 0.565, "mocap hardware + planner"),
    ("total perception latency tau [A-33]", 0.037, 0.24, "own calc, point mass"),
    ("closed-loop bandwidth vs delay [A-32]", 1.0, 1.0, "own calc; bandwidth, NOT speed"),
]
print(f"{'limit':55s} {'|e| low':>8s} {'|e| high':>9s}  basis")
for name, lo, hi, basis in rows:
    print(f"{name:55s} {lo:8.3f} {hi:9.3f}  {basis}")
print()
print("  The course-known binary is not an elasticity but a step: "
      f"{12.88/5.0:.2f}x in mean speed on the same airframe class and sensing class,")
print("  observed, hardware, onboard-only on both sides.")
print("  To match a 2.58x speed gain through thrust alone at e = 0.5 needs a T/W factor of "
      f"{2.58**(1/0.5):.1f}x, i.e. T/W {4.4*2.58**(1/0.5):.0f} from 4.4.")
print("  To match it through perception range alone at e = 1.0 needs "
      f"{2.58**(1/1.0):.1f}x range; at e = 0.52, {2.58**(1/0.52):.1f}x range.")
print("  To match it through latency alone at |e| = 0.24 needs tau reduced by a factor of "
      f"{2.58**(1/0.24):.0f} (impossible: tau > 0).")

print()
print("=" * 72)
print("7. OBSERVED ELASTICITY OF LAP TIME TO SENSORIMOTOR LATENCY (cross-controller)")
print("=" * 72)
tau_swift, tau_human = 0.040, 0.220
cases = [
    ("best three-lap, Swift 17.465 s vs Vanover 17.956 s", 17.465, 17.956),
    ("best three-lap, Swift 17.465 s vs Bitmatta 18.746 s", 17.465, 18.746),
    ("best three-lap, Swift 17.465 s vs Schaepper 21.160 s", 17.465, 21.160),
    ("single-lap medians, extremes of the panel 5.52 s vs 6.80 s", 5.52, 6.80),
]
r_tau = tau_human / tau_swift
print(f"  latency ratio human/Swift = {r_tau:.2f}x  (220 ms vs 40 ms [A-07])")
for label, t_fast, t_slow in cases:
    r_t = t_slow / t_fast
    e = math.log(r_t) / math.log(r_tau)
    print(f"  {label:54s} time ratio {r_t:.3f} -> |e(speed, tau)| = {e:.3f}")
print("  (a controller swap, not a latency perturbation: it changes policy, camera rate and")
print("   information at once, so it bounds the JOINT effect of a 5.5x latency difference.)")

print()
print("=" * 72)
print("8. WHERE LATENCY BEGINS TO MATTER: ITS SHARE OF THE REQUIRED LOOK-AHEAD")
print("=" * 72)
print("  required stopping distance s(v) = v*tau + v^2/(2a); latency share = v*tau / s")
for a in (20.0, 40.0):
    for tau in (0.040, 0.130):
        v_cross = 2 * a * tau
        print(f"  a = {a:4.1f} m/s^2, tau = {tau*1000:5.1f} ms: latency and braking terms "
              f"equal at v = {v_cross:5.2f} m/s")
        for v in (5.0, 10.0, 20.0, 30.0):
            s = v * tau + v * v / (2 * a)
            print(f"      v = {v:4.1f} m/s: s = {s:6.2f} m, latency share "
                  f"{v*tau/s:5.1%}, braking share {(v*v/(2*a))/s:5.1%}")

print()
print("=" * 72)
print("9. THE ANGULAR, NOT RADIAL, PERCEPTION LIMIT: TILT REQUIRED TO ACCELERATE")
print("=" * 72)
print("  A multirotor must tilt theta = atan(a_lat/g) to produce lateral acceleration a_lat")
print("  while holding altitude. A body-fixed forward camera of horizontal FoV H sees the")
print("  direction of travel only while theta <= H/2.")
for H in (90.0, 115.0, 155.0):
    a_edge = g * math.tan(math.radians(H / 2))
    print(f"  FoV {H:5.1f} deg (half {H/2:5.1f} deg): travel direction leaves the FoV at "
          f"a_lat = {a_edge:6.2f} m/s^2 = {a_edge/g:5.2f} g")
for a_lat_g in (0.5, 1.0, 2.0, 4.0, 12.58):
    a_lat = a_lat_g * g
    theta = math.degrees(math.atan(a_lat / g))
    print(f"  a_lat = {a_lat_g:5.2f} g = {a_lat:6.2f} m/s^2 -> tilt {theta:5.1f} deg "
          f"(inside 90 deg FoV? {'yes' if theta <= 45 else 'NO'}; "
          f"inside 155 deg FoV? {'yes' if theta <= 77.5 else 'NO'})")
print("  Observed engineering response: the depth camera in [A-20] was tilted 30 deg")
print("  upward above 7 m/s, and [A-26] used a 155 x 115 deg camera. Both are this term.")
print("  Verification: at a_lat = g the tilt is exactly 45.000 deg ->",
      f"{math.degrees(math.atan(1.0)):.3f} deg")
