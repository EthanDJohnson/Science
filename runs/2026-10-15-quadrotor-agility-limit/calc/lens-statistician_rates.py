"""Statistician lens: are the agility 'signals' real?

Part 1: success rates over trials (binomial), the 90 per cent threshold the brief demands.
Part 2: can the reported controller/policy rankings support themselves?
Part 3: how many trials a decisive test needs.
All counts and rates are from the dossier; units: speeds in m/s, latencies in s, accel in m/s^2.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import (sidak_global_p, wilson_interval, clopper_pearson_interval, trials_to_distinguish,
                         p_to_sigma, sigma_to_p, min_bayes_factor, prior_needed,
                         posterior_probability, tension, grouped_chi2, weighted_mean,
                         precision_needed, selftest)

print("stats_tools selftest:", selftest(verbose=False))
print()


def binom_le(k, n, p):
    """P(X <= k), X ~ Binomial(n, p)."""
    return sum(math.comb(n, i) * p**i * (1 - p)**(n - i) for i in range(0, k + 1))


def binom_ge(k, n, p):
    return sum(math.comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k, n + 1))


print("=" * 72)
print("PART 1  Success rates vs the brief's 90 per cent threshold")
print("=" * 72)
# Dossier A-20 (Loquercio et al., onboard depth, UNSEEN clutter, 40 m line):
#   100% at 3 m/s and 5 m/s; 8 of 10 at 7 m/s; 60% at 10 m/s.
#   Per-speed trial counts NOT retrieved except the 8/10. I take n=10 where a rate of
#   60% or 100% is quoted, because 60% on n<10 is impossible below n=5 and the paper's
#   own 7 m/s row is n=10. Flagged as an assumption.
# Dossier A-27 (MonoRace, SEEN track): M23 38/43; M17 5/7; M16 1/4.
rows = [
    ("A-20  3 m/s  unseen clutter", 10, 10),
    ("A-20  5 m/s  unseen clutter", 10, 10),
    ("A-20  7 m/s  unseen clutter", 8, 10),
    ("A-20 10 m/s  unseen clutter", 6, 10),
    ("A-27 M23 seen track (23 s)", 38, 43),
    ("A-27 M17 seen track", 5, 7),
    ("A-27 M16 seen track (16.56 s)", 1, 4),
    ("A-29 '100% all envs' if n=5", 5, 5),
    ("A-14 RL real (mocap) if n=20", 17, 20),
    ("A-14 contouring real if n=20", 10, 20),
    ("A-14 tracking MPC real if n=20", 0, 20),
]
print(f"{'claim':34s} {'k/n':>7s} {'rate':>6s} {'Wilson 95%':>16s} {'CP95 lower':>10s} "
      f"{'p(H0:>=0.90)':>12s} {'z1':>5s}")
for name, k, n in rows:
    w = wilson_interval(k, n)
    cp = clopper_pearson_interval(k, n)
    # one-sided test of H0: true rate >= 0.90, against the alternative that it is lower
    p_one = binom_le(k, n, 0.90)
    z = p_to_sigma(min(p_one, 0.5), two_sided=False)
    print(f"{name:34s} {k:3d}/{n:<3d} {k/n:6.3f} [{w[0]:.3f},{w[1]:.3f}]  "
          f"{cp[0]:10.3f} {p_one:12.4f} {z:5.2f}")
print()
print("Reading: a 'p(H0:>=0.90)' below 0.05 rejects the brief's threshold for that row;")
print("a Clopper-Pearson lower bound below 0.90 means the row cannot *establish* it either.")
print()

# How many flawless trials are needed to certify >= 0.90 at 95 per cent one-sided?
n_flawless = math.ceil(math.log(0.05) / math.log(0.90))
print(f"Trials needed to certify a true rate >= 0.90 with a 95% one-sided lower bound,")
print(f"  with ZERO failures: n >= ln(0.05)/ln(0.90) = {math.log(0.05)/math.log(0.90):.2f} "
      f"-> {n_flawless} consecutive successes")
for allow in (1, 2, 3):
    n = allow + 1
    while True:
        lo = clopper_pearson_interval(n - allow, n)[0]
        if lo >= 0.90:
            break
        n += 1
        if n > 2000:
            break
    print(f"  allowing {allow} failure(s): n = {n}  (k={n-allow}, CP95 lower = "
          f"{clopper_pearson_interval(n-allow, n)[0]:.3f})")
print()

print("=" * 72)
print("PART 2  Can the reported rankings support themselves?")
print("=" * 72)
pairs = [
    ("90% vs 80% (7 m/s row vs threshold)", 0.90, 0.80),
    ("90% vs 60% (10 m/s row vs threshold)", 0.90, 0.60),
    ("85% vs 50% (A-14 RL vs contouring, real)", 0.85, 0.50),
    ("100% vs 85% (A-14 RL sim vs real)", 0.99, 0.85),
    ("88.4% vs 90% (MonoRace M23 vs threshold)", 0.90, 0.884),
    ("95% vs 90% (reference case)", 0.95, 0.90),
]
for name, p1, p2 in pairs:
    n = trials_to_distinguish(p1, p2)
    print(f"{name:42s} needs {n:6.0f} trials per arm (95% conf, 80% power)")
print()

# A-14 real-world rows, two-proportion exact-ish test at the researcher-inferred n=20
for (k1, n1, k2, n2, lab) in [(17, 20, 10, 20, "RL 17/20 vs contouring 10/20 (n=20 assumed)"),
                              (17, 20, 0, 20, "RL 17/20 vs tracking 0/20 (n=20 assumed)"),
                              (9, 10, 5, 10, "same ratios at n=10")]:
    phat = (k1 + k2) / (n1 + n2)
    se = math.sqrt(phat * (1 - phat) * (1 / n1 + 1 / n2))
    if se > 0:
        z = abs(k1 / n1 - k2 / n2) / se
        p2s = sigma_to_p(z, two_sided=True)
        print(f"{lab:46s} z = {z:5.2f}, two-sided p = {p2s:.2e}")
    else:
        print(f"{lab:46s} se = 0 (degenerate)")
print()

# Lap times A-14, nominal simulation: tracking 4.92 +/- 0.10 s vs RL 5.14 +/- 0.09 s.
# The quoted +/- is a standard deviation over trials, count unknown.
print("A-14 lap-time gap, nominal sim: tracking 4.92+/-0.10 s vs RL 5.14+/-0.09 s (s.d.)")
t = tension(4.92, 0.10, 5.14, 0.09)
print(f"  treating s.d. as the uncertainty of one trial: z = {t['z']:.2f} "
      f"(two-sided p = {t['p_two_sided']:.3g})")
for n in (5, 10, 25):
    t2 = tension(4.92, 0.10 / math.sqrt(n), 5.14, 0.09 / math.sqrt(n))
    print(f"  if each mean rests on n = {n:2d} trials (s.e.m.): z = {t2['z']:5.1f}")
print("  -> the LAP-TIME ordering is well determined for any plausible n;")
print("     the SUCCESS-RATE ordering is what is undetermined.")
print()

print("=" * 72)
print("PART 3  Grouping the onboard speed claims by course type, not pooling them")
print("=" * 72)
# No source quotes an uncertainty on any demonstrated speed. I work in ln(speed) and assign a
# nominal 20 per cent fractional spread (sigma_lnv = 0.20) to every entry, then show how large
# that spread would have to be for the seen/unseen split to be a fluctuation.
groups_raw = {
    "seen gate track, onboard": [("MonoRace peak lo", 27.8), ("MonoRace peak hi", 32.2),
                                 ("A2RL 2025 (press)", 20.0)],
    "unseen clutter, onboard": [("Loquercio 7 m/s", 7.0), ("Loquercio 10 m/s", 10.0),
                                ("2026 preprint", 8.0), ("perturbed gates", 5.3)],
    "mocap state (not onboard)": [("Song peak", 30.0), ("Agilicious max", 36.4)],
}
for sig in (0.20, 0.40, 0.80):
    groups = {g: ([math.log(v) for _, v in items], [sig] * len(items))
              for g, items in groups_raw.items()}
    res = grouped_chi2(groups)
    print(f"sigma_ln v = {sig:.2f}  ({sig*100:.0f}% fractional)")
    for g, d in res["groups"].items():
        print(f"   within {g:28s} chi2 = {d['chi2']:6.2f} / {d['dof']} dof, "
              f"mean v = {math.exp(d['mean']):6.2f} m/s")
    print(f"   BETWEEN groups chi2 = {res['between_chi2']:7.2f} / {res['between_dof']} dof,"
          f" p = {res['p_between']:.3g}, z = {res['between_z']:.2f}")
    print()
pooled = weighted_mean([math.log(v) for items in groups_raw.values() for _, v in items],
                       [0.20] * 9)
print(f"pooled (wrong) weighted mean of ln v: {pooled['mean']:.3f} -> "
      f"{math.exp(pooled['mean']):.2f} m/s, chi2 = {pooled['chi2']:.1f}/{pooled['dof']} dof, "
      f"PDG scale factor S = {pooled['scale_factor']:.2f}")
print("The pooled fit smears a 3-4x split between COURSE TYPES over every measurement:")
print("this is exactly the case the method warns about.")
print()

print("=" * 72)
print("PART 4  Bayes-factor bounds and the prior each claim needs")
print("=" * 72)
claims = [
    ("A-27 M16 (16.56 s policy) is below 90%", binom_le(1, 4, 0.90) * 2),
    ("A-20 10 m/s row is below 90%", binom_le(6, 10, 0.90) * 2),
    ("A-20 7 m/s row is below 90%", binom_le(8, 10, 0.90) * 2),
    ("A-14 RL > contouring on hardware (n=20)", sigma_to_p(
        abs(17/20 - 10/20) / math.sqrt((27/40)*(13/40)*(1/20+1/20)), two_sided=True)),
]
for name, p2s in claims:
    p2s = min(p2s, 1.0)
    mbf = min_bayes_factor(p2s)
    bf_alt = mbf["max_odds_against_null"]
    need = prior_needed(bf_alt)
    print(f"{name:42s} p2 = {p2s:.4f}")
    print(f"   min Bayes factor (null:alt) = {mbf['sellke']:.3f} "
          f"-> BF(alt:null) <= {bf_alt:.2f}; prior needed for posterior 0.5 = {need:.3f}")
    for prior in (0.2, 0.3, 0.5):
        print(f"      prior {prior:.2f} -> posterior {posterior_probability(prior, bf_alt):.3f}")
print()
print(f"precision needed on a 0.10 difference in success rate for a 5-sigma call: "
      f"{precision_needed(0.10, 5.0):.4f} (i.e. s.e. of 2 percentage points -> n ~ "
      f"{0.9*0.1/0.02**2:.0f} trials at p=0.9)")
print()

print("=" * 72)
print("PART 5  Elasticities: which limit has the leverage, and in which regime")
print("=" * 72)
# Stop-before-obstacle bound (dossier D-32/A-33): v = a(-tau + sqrt(tau^2 + 2 s / a)).
# Lateral-dodge bound (D-31/A-33):               v = s / (tau + 2 sqrt(r / a)).
# Elasticities by central difference in log space; 1 per cent perturbations.


def v_stop(s, a, tau):
    return a * (-tau + math.sqrt(tau * tau + 2 * s / a))


def v_dodge(s, a, tau, r=0.5):
    return s / (tau + 2 * math.sqrt(r / a))


def elas(f, args, i, h=1e-3):
    up = list(args); dn = list(args)
    up[i] *= (1 + h); dn[i] *= (1 - h)
    return (math.log(f(*up)) - math.log(f(*dn))) / (2 * math.log((1 + h) / (1 - h)) / 2)


cases = [
    ("depth cam, Swift-class latency", 6.0, 38.0, 0.040),
    ("depth cam, 2019 latency chain", 6.0, 38.0, 0.130),
    ("depth cam, MonoRace image delay", 6.0, 38.0, 0.017),
    ("long range (LiDAR-class 20 m)", 20.0, 38.0, 0.040),
    ("short range (3 m), fast loop", 3.0, 38.0, 0.040),
    ("low thrust T/W 2 (a_h = 17 m/s2)", 6.0, 17.0, 0.040),
]
print(f"{'case':34s} {'v_stop':>7s} {'e_s':>6s} {'e_a':>6s} {'e_tau':>7s} {'|e_s/e_tau|':>11s} "
      f"{'v_dodge':>8s} {'e_tau_d':>8s}")
for name, s, a, tau in cases:
    vs = v_stop(s, a, tau)
    es = elas(v_stop, (s, a, tau), 0)
    ea = elas(v_stop, (s, a, tau), 1)
    et = elas(v_stop, (s, a, tau), 2)
    vd = v_dodge(s, a, tau)
    etd = elas(v_dodge, (s, a, tau), 2)
    print(f"{name:34s} {vs:7.2f} {es:6.3f} {ea:6.3f} {et:7.3f} {abs(es/et):11.1f} "
          f"{vd:8.2f} {etd:8.3f}")
print("units: s in m, a in m/s^2, tau in s, v in m/s; elasticities dimensionless")
print()
# Where does the latency term stop being negligible? v*tau = v^2/(2a) at v = 2 a tau.
for a, tau in ((38.0, 0.040), (38.0, 0.130), (20.0, 0.050)):
    print(f"  a = {a:4.0f} m/s^2, tau = {tau*1000:5.1f} ms: latency term equals braking term at "
          f"v = 2 a tau = {2*a*tau:5.2f} m/s")
print()
# Latency elasticity of the DODGE bound equals -tau/(tau + 2 sqrt(r/a)): solve for the tau that
# makes it reach 0.5 in magnitude (i.e. as much leverage as range).
r = 0.5
for a in (17.0, 38.0, 77.0):
    tau_half = 2 * math.sqrt(r / a)          # |e_tau| = 0.5 when tau = 2 sqrt(r/a)
    print(f"  dodge bound, a = {a:4.0f} m/s^2, r = 0.5 m: |e_tau| reaches 0.50 only at "
          f"tau = {tau_half*1000:6.1f} ms")
print()
# Empirical thrust elasticity (A-16) against the point-mass theory value (A-34 / D-33).
lap = [(2.5, 7.14), (3.6, 5.81)]
e_emp = (math.log(lap[1][1]) - math.log(lap[0][1])) / (math.log(lap[1][0]) - math.log(lap[0][0]))
print(f"A-16 planner sweep: d ln(lap)/d ln(TWR) = {e_emp:.3f} (two points, no uncertainty quoted)")
print(f"  -> elasticity of mean speed to TWR = {-e_emp:.3f}")
print(f"  point-mass theory (D-33) at T/W = 4: d ln v / d ln(T/W) = "
      f"{0.5 * 4**2/(4**2-1):.3f}")
print("  the two agree to about 6 per cent of each other; no uncertainty is quoted on either,")
print("  so no tension can be computed. Both are near +0.5.")
print()

print("=" * 72)
print("PART 7  Shared apparatus: the same split with rho = 0 and rho = 0.8")
print("=" * 72)
# Dossier section 7: A-01..A-06, A-07..A-10, A-16..A-18 and A-20..A-21 come from one group's
# platform lineage. Within a group, measurements sharing an apparatus are correlated: the error
# on a group mean of n equal-error points is sigma*sqrt((1 + (n-1) rho)/n) instead of sigma/sqrt(n).
for rho in (0.0, 0.8):
    means, errs, labels = [], [], []
    for g, items in groups_raw.items():
        n = len(items)
        m = sum(math.log(v) for _, v in items) / n
        e = 0.20 * math.sqrt((1 + (n - 1) * rho) / n)
        means.append(m); errs.append(e); labels.append(g)
    wm = weighted_mean(means, errs)
    print(f"rho = {rho:.1f}: group means (m/s) " +
          ", ".join(f"{l.split(',')[0]} {math.exp(m):.1f}+-{100*e:.0f}%"
                    for l, m, e in zip(labels, means, errs)))
    print(f"   chi2 between the 3 group means = {wm['chi2']:.2f} / {wm['dof']} dof, "
          f"p = {wm['p_consistent']:.3g}, z = {p_to_sigma(wm['p_consistent'], two_sided=True):.2f}")
print("   The seen/unseen split survives full correlation within each group.")
print()

print("=" * 72)
print("PART 6  Multiplicity in the attributions, and the failure-count problem")
print("=" * 72)
# D-21 lists five different named binding limits, one per paper, each chosen after the failures
# were seen. If each attribution is tested at a nominal local p, the chance that at least one
# of five independent 'look's gives it is the Sidak global p.
for p_local in (0.05, 0.01, 0.0037):
    for n_tries in (4, 5, 12):
        print(f"  local p = {p_local:.4f}, {n_tries:2d} candidate attributions tried -> "
              f"global p = {sidak_global_p(p_local, n_tries):.4f} "
              f"(z_global = {p_to_sigma(sidak_global_p(p_local, n_tries)):.2f})")
print("  12 = the (speed x environment x pipeline) cells actually reported in this evidence base")
print()
# Attribution rests on very few failure events.
events = [("A-20 7 m/s: 2 crashes, both blamed on perception", 2, 2),
          ("A-20 10 m/s: 4 crashes of 10 (cause mix unstated)", 4, 4),
          ("A-10 Swift: 4 of 10 losses by gate collision", 4, 10),
          ("A-10 Swift: 2 of 10 losses by being slower", 2, 10)]
for name, k, n in events:
    w = wilson_interval(k, n)
    print(f"{name:48s} share = {k/n:5.2f}, Wilson 95% [{w[0]:.2f}, {w[1]:.2f}]")
print("  A single cause can be called dominant only if its share's interval excludes 0.5;")
print("  none of these does except trivially (k = n on n = 2, lower bound 0.34).")
print()

print("=" * 72)
print("VERIFICATION")
print("=" * 72)
ok = True
# 1. binomial tail check against a hand value: P(X<=8 | n=10, p=0.9) = 1 - 10*0.9^9*0.1 - 0.9^10
hand = 1 - 10 * 0.9**9 * 0.1 - 0.9**10
chk = binom_le(8, 10, 0.90)
print(f"{'PASS' if abs(hand-chk) < 1e-12 else 'FAIL'}: binom_le(8,10,0.9) = {chk:.6f} "
      f"vs closed form {hand:.6f}")
ok &= abs(hand - chk) < 1e-12
# 2. Clopper-Pearson lower bound for k=n equals 0.05^(1/n) (one-sided 95%)
cp = clopper_pearson_interval(10, 10, 0.90)[0]      # 0.90 two-sided -> 0.95 one-sided tail
exact = 0.05 ** (1 / 10)
print(f"{'PASS' if abs(cp-exact) < 1e-6 else 'FAIL'}: CP lower for 10/10 at one-sided 95% = "
      f"{cp:.6f} vs 0.05^(1/10) = {exact:.6f}")
ok &= abs(cp - exact) < 1e-6
# 3. stop-bound elasticities must sum to 1 in the tau -> 0 limit (v = sqrt(2 s a): e_s = e_a = 1/2)
es0 = elas(v_stop, (6.0, 38.0, 1e-9), 0); ea0 = elas(v_stop, (6.0, 38.0, 1e-9), 1)
print(f"{'PASS' if abs(es0-0.5) < 1e-5 and abs(ea0-0.5) < 1e-5 else 'FAIL'}: tau->0 limit gives "
      f"e_s = {es0:.5f}, e_a = {ea0:.5f} (expect 0.5, 0.5)")
ok &= abs(es0 - 0.5) < 1e-5 and abs(ea0 - 0.5) < 1e-5
# 4. v_stop reproduces the dossier A-33 case: s=6, a=20, tau=0.05 -> 14.5 m/s, e_tau = -0.064
v_ref = v_stop(6.0, 20.0, 0.05); et_ref = elas(v_stop, (6.0, 20.0, 0.05), 2)
print(f"{'PASS' if abs(v_ref-14.5) < 0.05 and abs(et_ref+0.064) < 0.002 else 'FAIL'}: "
      f"A-33 case reproduced: v = {v_ref:.3f} m/s (dossier 14.5), e_tau = {et_ref:.4f} "
      f"(dossier -0.064)")
ok &= abs(v_ref - 14.5) < 0.05 and abs(et_ref + 0.064) < 0.002
# 5. grouped_chi2 bookkeeping: within + between = pooled chi2
g = {k: ([math.log(v) for _, v in it], [0.2] * len(it)) for k, it in groups_raw.items()}
rg = grouped_chi2(g)
tot = rg["within_chi2"] + rg["between_chi2"]
print(f"{'PASS' if abs(tot-rg['pooled']['chi2']) < 1e-9 else 'FAIL'}: within+between = {tot:.6f} "
      f"= pooled chi2 {rg['pooled']['chi2']:.6f}")
ok &= abs(tot - rg["pooled"]["chi2"]) < 1e-9
print(f"\n{'PASS' if ok else 'FAIL'}: all verification checks")
