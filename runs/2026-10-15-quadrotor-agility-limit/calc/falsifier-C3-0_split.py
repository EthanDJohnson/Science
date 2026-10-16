"""falsifier-C3-0_split: attack on C3 ("prior course information is the binding term").

Three computations, all on the run's own numbers.

(A) UNIT AUDIT of C3's statistical pillar M-STAT-04. Its "seen gate track" group
    {27.8, 32.2, 20.0} m/s is *peak* speed [A-26 "27.8-32.2 m/s peak", A-31 press
    arithmetic]; its "unseen clutter" group {10, 8, 7, 5.3} m/s is *average* speed
    [A-20 "average speed", A-29]. The brief forbids mixing the two ("Where a source
    reports only peak speed ... that is a different quantity"). Convert the seen group
    to means two ways: (i) C3's own within-apparatus mean, Swift 12.88 m/s on a mapped
    track [M-EMP-03 verified]; (ii) the run's own verified bang-bang peak/mean ratio
    from A-34 (13.0/6.5, 19.5/9.8, 27.9/14.0). Recompute the grouped chi2.

(B) A DISCONFIRMING ROW the slate's grouping omits: SUPER [doi:10.1126/scirobotics.ado6187,
    Science Robotics 2025; dossier D-39 at low confidence], onboard 3-D LiDAR, no map,
    "autonomous flights at speeds exceeding 20 meters per second" in *unknown*
    environments. Put it in the unseen group at 20 m/s (abstract reading) and, as the
    conservative reading, at 20/2 = 10 m/s (treating 20 as a peak and using the same
    peak/mean = 2 conversion), and recompute.

(C) RIVAL PARTITION. On the onboard-only rows, compare the between-group chi2 of the
    "course knowledge" partition against a "sensor range class" partition of the *same*
    numbers (short-range depth camera vs long-range LiDAR / monocular gate detection).
    If the sensor partition fits as well or better, z = 10 is not evidence for
    information over range (C1).

(D) The attainability of the range route that M-EMP-04 calls out: 2.58x on the dodge
    bound (elasticity +1.000, M-STAT-06 verified) needs 2.58x usable range.

All speeds m/s. sigma_x = 0.20 in ln(speed), rho = 0, as in M-STAT-04.
"""
import numpy as np
from scipy.stats import chi2 as chi2dist
from scipy.stats import norm


def analyse(groups, sig=0.20, rho=0.0):
    means, varm, within = [], [], {}
    for name, vals in groups.items():
        x = np.log(np.array(vals, dtype=float))
        n = len(x)
        C = sig ** 2 * ((1 - rho) * np.eye(n) + rho * np.ones((n, n)))
        Ci = np.linalg.inv(C)
        one = np.ones(n)
        vm = 1.0 / (one @ Ci @ one)
        m = vm * (one @ Ci @ x)
        r = x - m
        within[name] = (float(r @ Ci @ r), n - 1, float(np.exp(m)))
        means.append(m)
        varm.append(vm)
    means, varm = np.array(means), np.array(varm)
    w = 1 / varm
    M = float(np.sum(w * means) / np.sum(w))
    between = float(np.sum(w * (means - M) ** 2))
    dof = len(means) - 1
    p = chi2dist.sf(between, dof)
    return within, between, dof, p, norm.isf(p)


def report(tag, groups, sig=0.20, rho=0.0):
    within, between, dof, p, z = analyse(groups, sig, rho)
    print(f"\n--- {tag} (sigma_x = {sig}, rho = {rho}) ---")
    for name, (c, d, gm) in within.items():
        print(f"  within {name:34s}: chi2 = {c:8.3f} / {d} dof, geo-mean = {gm:6.2f} m/s")
    print(f"  between groups: chi2 = {between:8.2f} / {dof} dof, p = {p:.3g}, z(one-sided) = {z:.2f}")
    gms = [v[2] for v in within.values()]
    print(f"  group geo-means {['%.2f' % g for g in gms]} m/s, max/min ratio = {max(gms)/min(gms):.3f}")
    return between, z, within


print("=== falsifier-C3-0: C3's seen/unseen split under a unit audit and one omitted row ===")

SEEN_PEAK = [27.8, 32.2, 20.0]          # peak, seen gate track  [A-26, A-31]
UNSEEN_MEAN = [10.0, 8.0, 7.0, 5.3]      # average, unseen clutter [A-20, A-29]
MOCAP_PEAK = [30.0, 36.4]                # peak, mocap state       [A-12, A-02]

# (0) Reproduce M-STAT-04 as the baseline.
b0, z0, w0 = report("(0) M-STAT-04 as published: peak(seen) vs mean(unseen) vs peak(mocap)",
                    {"seen gate track (PEAK)": SEEN_PEAK,
                     "unseen clutter (MEAN)": UNSEEN_MEAN,
                     "mocap (PEAK)": MOCAP_PEAK})

# (A) Unit audit.
print("\n=== (A) UNIT AUDIT: peak -> mean on the seen group ===")
a34_peak = np.array([13.0, 19.5, 27.9])
a34_mean = np.array([6.5, 9.8, 14.0])
pm = a34_peak / a34_mean
print(f"A-34 bang-bang peak/mean ratios = {np.round(pm, 4)}; mean = {pm.mean():.4f} "
      f"(exact value for a rest-to-rest bang-bang profile is 2)")
seen_geo_peak = float(np.exp(np.mean(np.log(SEEN_PEAK))))
swift_mean = 3 * 75.0 / 17.465           # M-EMP-03 verified: 75 m lap, best three laps 17.465 s
print(f"seen-group geometric mean of PEAK speeds = {seen_geo_peak:.2f} m/s")
print(f"Swift mapped-track MEAN speed            = {swift_mean:.4f} m/s  [M-EMP-03 verified]")
print(f"implied peak/mean on a seen gate track   = {seen_geo_peak/swift_mean:.3f}  "
      f"<-- C3's own two numbers reproduce A-34's factor 2 to "
      f"{100*abs(seen_geo_peak/swift_mean - pm.mean())/pm.mean():.1f} per cent")
seen_mean_conv = [v / 2.0 for v in SEEN_PEAK]
print(f"seen group converted to means (divide by 2) = {seen_mean_conv} m/s")
bA, zA, wA = report("(A1) mean-vs-mean: seen/2 vs unseen",
                    {"seen gate track (mean)": seen_mean_conv,
                     "unseen clutter (mean)": UNSEEN_MEAN})
bA2, zA2, wA2 = report("(A2) mean-vs-mean using Swift's measured mapped mean only",
                       {"seen gate track (mean)": [swift_mean],
                        "unseen clutter (mean)": UNSEEN_MEAN})
r_pub = float(np.exp(np.mean(np.log(SEEN_PEAK)))) / float(np.exp(np.mean(np.log(UNSEEN_MEAN))))
r_fix = float(np.exp(np.mean(np.log(seen_mean_conv)))) / float(np.exp(np.mean(np.log(UNSEEN_MEAN))))
print(f"\nseen:unseen group ratio as published (peak vs mean) = {r_pub:.3f}")
print(f"seen:unseen group ratio, mean vs mean               = {r_fix:.3f}")
print(f"inflation factor of C3's headline effect size       = {r_pub/r_fix:.3f}")

# (A3) Full unit audit, row by row, keeping like with like.
print("\n=== (A3) ROW-BY-ROW UNIT AUDIT: split computed inside each speed class ===")
MEAN_SEEN = {"Swift lap mean [A-10/M-EMP-03, full-text]": 12.8829,
             "A2RL 2025 lap mean [A-31, press, low confidence]": 20.0}
MEAN_UNSEEN = {"A-20 average speed, 60 % success": 10.0,
               "A-20 average speed, 80 % success": 7.0}
PEAK_SEEN = {"MonoRace abstract peak [A-26]": 27.8, "MonoRace table peak [A-26]": 32.2}
PEAK_UNSEEN = {"A-29 'up to' max [preprint]": 8.0, "A-29 max, perturbed-gate track [preprint]": 5.3}


def geo(d):
    return float(np.exp(np.mean(np.log(np.array(list(d.values()), dtype=float)))))


print("  The brief's metric is 'maximum average speed', so the mean class is the metric's own class.")
print(f"  MEAN class : seen {geo(MEAN_SEEN):.2f} m/s vs unseen {geo(MEAN_UNSEEN):.2f} m/s "
      f"-> ratio {geo(MEAN_SEEN)/geo(MEAN_UNSEEN):.3f}")
print(f"  MEAN class, dropping the press row: {12.8829:.2f} vs {geo(MEAN_UNSEEN):.2f} m/s "
      f"-> ratio {12.8829/geo(MEAN_UNSEEN):.3f}")
print(f"  PEAK class : seen {geo(PEAK_SEEN):.2f} m/s vs unseen {geo(PEAK_UNSEEN):.2f} m/s "
      f"-> ratio {geo(PEAK_SEEN)/geo(PEAK_UNSEEN):.3f}  (two 2026 preprints on the unseen side,"
      f" one of them a perturbed-GATE track, and peaks are not the brief's metric)")
print(f"  C3's published grouped ratio, seen PEAKS over unseen MEANS = {r_pub:.3f} "
      f"<- neither class's own value")
print("\n  Reliability audit of C3's 'firm within-apparatus leg' (12.88 vs 5-7 m/s = 2.58x):")
print("   - 12.8829 m/s is Swift's BEST THREE LAPS (17.465 s) [M-EMP-03], a best case with no"
      " stated success rate; Swift won 15 of 25 races = 60 per cent [A-10].")
print("   - 5-7 m/s is the band where A-20 still meets ~90 per cent reliability.")
print(f"   - best-case vs best-case, same quantity class: 12.8829 / 10.0 (A-20's fastest average)"
      f" = {12.8829/10.0:.3f}x, not 2.58x")
print(f"   - 2.58x therefore compares a best-of-three-laps mean with a reliability-thresholded mean;"
      f" the inflation is {(12.8829/7.0)/(12.8829/10.0):.3f}x from the threshold alone")

# (B) The omitted unseen-course row: SUPER, onboard LiDAR, unknown environment, no map.
print("\n=== (B) Adding SUPER (onboard LiDAR, UNKNOWN environment, no map, >20 m/s) ===")
for label, v_super in (("abstract reading, 20 m/s", 20.0), ("conservative, 20 m/s read as a peak -> mean 10 m/s", 10.0)):
    g = {"seen gate track (mean)": seen_mean_conv,
         "unseen (mean) + SUPER": UNSEEN_MEAN + [v_super]}
    bB, zB, wB = report(f"(B) {label}", g)
    info_ratio = float(np.exp(np.mean(np.log(seen_mean_conv)))) / float(
        np.exp(np.mean(np.log(UNSEEN_MEAN + [v_super]))))
    print(f"  seen:unseen ratio with SUPER included = {info_ratio:.3f} "
          f"(C3 claims 2.58-6.4x for 'course knowledge')")
    print(f"  SUPER alone vs the unseen-clutter geometric mean "
          f"({float(np.exp(np.mean(np.log(UNSEEN_MEAN)))):.2f} m/s) = "
          f"{v_super/float(np.exp(np.mean(np.log(UNSEEN_MEAN)))):.3f}x, bought with NO map")
    print(f"  SUPER vs Swift's mapped-track mean {swift_mean:.2f} m/s = {v_super/swift_mean:.3f}x")

# (C) Rival partition of the same onboard-only rows.
print("\n=== (C) RIVAL PARTITION on the same onboard-only numbers ===")
rows = [  # (speed m/s, course known?, long-range sensing?)
    (27.8, True, True), (32.2, True, True), (20.0, True, True),   # seen gate tracks, monocular gate detection
    (20.0, False, True),                                          # SUPER: unseen, 3-D LiDAR
    (10.0, False, False), (8.0, False, False), (7.0, False, False), (5.3, False, False),  # D435i clutter
]
part_know = {"course known": [r[0] for r in rows if r[1]],
             "course unseen": [r[0] for r in rows if not r[1]]}
part_sens = {"long-range sensing": [r[0] for r in rows if r[2]],
             "short-range depth cam": [r[0] for r in rows if not r[2]]}
bK, zK, _ = report("(C1) partition by COURSE KNOWLEDGE (C3's variable)", part_know)
bS, zS, _ = report("(C2) partition by SENSOR RANGE CLASS (C1's variable)", part_sens)
print(f"\nbetween-group chi2: course knowledge = {bK:.2f}, sensor range = {bS:.2f}; "
      f"sensor/knowledge = {bS/bK:.2f}")
print("Same eight numbers, same model: the partition that fits better is the one with the"
      " larger between-group chi2 and the smaller within-group chi2.")

# (D) Attainability of the range route M-EMP-04 lists.
print("\n=== (D) The range route to 2.58x ===")
for e, name in ((1.000, "dodge bound [M-STAT-06 verified]"), (0.527, "stop bound"), (0.500, "T/W route")):
    print(f"  elasticity {e:+.3f} ({name}): factor needed in the limit = 2.58^(1/{e:.3f}) = "
          f"{2.58 ** (1/e):.2f}x")
print("  usable depth-camera range 6 m -> required 15.5 m on the dodge bound; a 3-D LiDAR of the"
      " class SUPER flies is described by its authors as giving 'accurate, long-range obstacle"
      " detection' and is the only sensor change in that result.")
print("\n=== (E) Mean-class split with SUPER, the metric's own units ===")
for label, v in (("SUPER at 20 m/s", 20.0), ("SUPER read as a peak -> 10 m/s", 10.0)):
    u = dict(MEAN_UNSEEN); u["SUPER (unknown env, no map)"] = v
    print(f"  {label}: seen {12.8829:.2f} m/s vs unseen {geo(u):.2f} m/s -> ratio "
          f"{12.8829/geo(u):.3f}")

pk = dict(PEAK_UNSEEN); pk["SUPER >20 m/s as a peak"] = 20.0
print(f"  honesty check, PEAK class with SUPER added to the unseen side: seen {geo(PEAK_SEEN):.2f}"
      f" vs unseen {geo(pk):.2f} m/s -> ratio {geo(PEAK_SEEN)/geo(pk):.3f} (the peak class is NOT"
      f" the brief's metric, which is maximum average speed)")

print("\n=== SUMMARY ===")
print(f"1. C3's z = {z0:.2f} split compares PEAK (seen) with MEAN (unseen) speeds; inside the"
      f" metric's own mean class the ratio is {geo(MEAN_SEEN)/geo(MEAN_UNSEEN):.2f}x"
      f" (or {12.8829/geo(MEAN_UNSEEN):.2f}x on full-text rows only), not {r_pub:.2f}x;"
      f" the uniform factor-2 conversion gives {r_fix:.2f}x and z = {zA:.2f}.")
print(f"2. One published onboard-only UNSEEN-environment result at >20 m/s (no map) exceeds Swift's"
      f" mapped-track mean of {swift_mean:.2f} m/s by {20.0/swift_mean:.2f}x; even read as a peak"
      f" (mean 10 m/s) it leaves at most {swift_mean/10.0:.2f}x for course knowledge, not 2.58x.")
print(f"3. The same numbers separate by sensor range class at chi2 = {bS:.1f} against"
      f" {bK:.1f} for course knowledge.")
