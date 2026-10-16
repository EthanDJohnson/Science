"""
Examiner lens: structural tests of the question "which limit binds first on closed-loop
agility of an onboard-only quadrotor".

All quantities SI unless a line says otherwise. Inputs are taken from the dossier anchors
(A-xx) and are printed with the value used.

Sections
  A  thrust-to-weight ceiling and the mean speed it permits (hidden premise 4)
  B  perception bounds: stop-before-obstacle and lateral-dodge, with elasticities, and the
     homogeneity identity that makes range and acceleration co-equal and non-separable
  C  FoV / body-attitude coupling: ds/da < 0, so "hold every other limit fixed" is not
     available; the braking acceleration at which the flight direction leaves the camera FoV
  D  delay-limited closed-loop bandwidth mapped to a speed on a course of given turn radius,
     and the delay that would be needed for latency to bind at the demonstrated speeds
  E  bound-versus-demonstrated table: is any single-limit bound active at the demonstrated
     onboard-only speeds?
  F  trial economics of the brief's own metric: how many flights certify "at least 90 per cent"
  G  equal-per-cent (elasticity) versus equal-attainable-increment sensitivity

Verification is printed inline: closed forms are checked against numerical integration or
root-finding, elasticities against central finite differences, and the binomial results
against an independent exact enumeration.
"""

import math

g = 9.81  # m/s^2


def hr(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


# ---------------------------------------------------------------- A
hr("A  Thrust-to-weight ceiling (hidden premise 4: compute it first)")

def a_horiz(twr):
    """Level-flight horizontal acceleration ceiling, point mass: a = g*sqrt(TWR^2-1)."""
    if twr <= 1:
        raise ValueError("TWR must exceed 1")
    return g * math.sqrt(twr * twr - 1.0)

def bangbang(dist, a):
    """Rest-to-rest bang-bang over `dist` with |a| bounded: time, peak speed, mean speed."""
    t = 2.0 * math.sqrt(dist / a)
    return t, a * t / 2.0, dist / t

print("TWR values from A-13 (onboard-only platforms 4.1-4.5; mocap platform 12.35)")
seg = 10.7  # m, mean gate spacing: Swift 75 m lap / 7 gates (A-10)
print(f"representative segment length = {seg:.2f} m  (75 m lap / 7 gates, A-10)")
print(f"{'TWR':>6} {'a_h m/s^2':>10} {'t_seg s':>9} {'v_peak m/s':>11} {'v_mean m/s':>11}")
rows_A = {}
for twr in (2.0, 4.1, 4.5, 12.35):
    a = a_horiz(twr)
    t, vp, vm = bangbang(seg, a)
    rows_A[twr] = (a, vm, vp)
    print(f"{twr:6.2f} {a:10.2f} {t:9.3f} {vp:11.2f} {vm:11.2f}")

# elasticity of a_h to TWR and of mean speed to a_h
def el(f, x, rel=1e-5):
    h = x * rel
    return (math.log(f(x + h)) - math.log(f(x - h))) / (math.log(x + h) - math.log(x - h))

print()
for twr in (2.0, 4.1, 12.35):
    e_num = el(a_horiz, twr)
    e_cf = twr * twr / (twr * twr - 1.0)
    print(f"  d ln a_h / d ln TWR at TWR={twr:5.2f}: numeric {e_num:.4f}  closed form {e_cf:.4f}"
          f"  (match {abs(e_num-e_cf):.2e})")
e_v_a = el(lambda a: bangbang(seg, a)[2], 38.0)
print(f"  d ln v_mean / d ln a_h (bang-bang) = {e_v_a:.4f}   exact 0.5")
print("  -> at TWR 4.1, d ln v_mean / d ln TWR = "
      f"{e_v_a * (4.1**2/(4.1**2-1)):.4f}  (+10% TWR buys about +5% speed)")
print("  cross-check against the published planner sweep A-16: d ln(lap)/d ln(TWR) = -0.565,")
print("  i.e. d ln v / d ln TWR = +0.565. Same order as 0.534.")

# ---------------------------------------------------------------- B
hr("B  Perception bounds, their elasticities, and the homogeneity identity")

def v_stop(s, a, tau):
    """Largest constant speed from which the vehicle can still stop within range s
    when it reacts after latency tau: v*tau + v^2/(2a) <= s."""
    return a * (-tau + math.sqrt(tau * tau + 2.0 * s / a))

def v_stop_numeric(s, a, tau):
    """Independent check: bisect on the stopping-distance integral."""
    def dist(v):
        # coast at v for tau, then brake at a (explicit integration, 20000 steps)
        n = 20000
        d = 0.0
        dt = tau / n if tau > 0 else 0.0
        for _ in range(n):
            d += v * dt
        t_brake = v / a
        dt2 = t_brake / n
        u = v
        for _ in range(n):
            d += u * dt2
            u -= a * dt2
        return d
    lo, hi = 0.0, 200.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if dist(mid) < s:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def v_dodge(s, r, a2, tau):
    """Falanga-type lateral dodge at constant forward speed (D-31):
    v = s / (tau + 2*sqrt(r/a2))."""
    return s / (tau + 2.0 * math.sqrt(r / a2))

cases = [
    ("A-33 case 1   s=6 m,  a=20 m/s^2, tau=50 ms", 6.0, 20.0, 0.050),
    ("A-33 case 2   s=6 m,  a=40 m/s^2, tau=20 ms", 6.0, 40.0, 0.020),
    ("A-33 case 3   s=10 m, a=20 m/s^2, tau=100 ms", 10.0, 20.0, 0.100),
    ("Swift-like    s=6 m,  a=39 m/s^2, tau=40 ms", 6.0, 39.0, 0.040),
]
print("stop bound v_max = a(-tau + sqrt(tau^2 + 2 s / a))")
print(f"{'case':<44}{'v m/s':>8}{'e_s':>8}{'e_a':>8}{'e_tau':>9}{'e_s+e_a':>9}")
rows_B = {}
for name, s, a, tau in cases:
    v = v_stop(s, a, tau)
    e_s = el(lambda x: v_stop(x, a, tau), s)
    e_a = el(lambda x: v_stop(s, x, tau), a)
    e_t = el(lambda x: v_stop(s, a, x), tau)
    rows_B[name] = (v, e_s, e_a, e_t)
    print(f"{name:<44}{v:8.2f}{e_s:8.3f}{e_a:8.3f}{e_t:9.3f}{e_s+e_a:9.3f}")

print()
print("verification of the stop bound against direct integration:")
for name, s, a, tau in cases[:3]:
    vc, vn = v_stop(s, a, tau), v_stop_numeric(s, a, tau)
    print(f"  {name:<44} closed {vc:8.4f}  integrated {vn:8.4f}  diff {abs(vc-vn):.2e} m/s")
print(f"  tau -> 0 limit: v_stop(6,20,0) = {v_stop(6.0,20.0,0.0):.4f} ;"
      f" sqrt(2as) = {math.sqrt(2*20*6):.4f}")

print()
print("Homogeneity identity. v_stop(s,a,tau) obeys v(k^2 s, k^2 a... ) -- test the exact")
print("statement instead: at tau = 0, v = sqrt(2 a s) is homogeneous of degree 1/2 in each of")
print("a and s, so e_s = e_a = 1/2 exactly and e_s + e_a = 1. For tau > 0, e_s + e_a is still")
print("1 by Euler's theorem applied to the scaling (s,a,tau) -> (k s, k a, tau) :")
for name, s, a, tau in cases:
    k = 1.37
    lhs = v_stop(k * s, k * a, tau)
    rhs = k * v_stop(s, a, tau)
    print(f"  {name:<44} v(ks,ka,tau)={lhs:8.4f}  k*v={rhs:8.4f}  diff {abs(lhs-rhs):.2e}")
print("  => v is homogeneous of degree 1 in (s,a) jointly, hence e_s + e_a = 1 identically,")
print("     and e_s/e_a is pinned near 1 for every parameter set below.")
print()
print(f"{'case':<44}{'e_s/e_a':>9}")
for name, (v, e_s, e_a, e_t) in rows_B.items():
    print(f"{name:<44}{e_s/e_a:9.3f}")

print()
print("lateral-dodge bound (D-31), r = 0.5 m:")
print(f"{'case':<44}{'v m/s':>8}{'e_s':>8}{'e_a2':>8}{'e_tau':>9}")
for name, s, a, tau in cases:
    v = v_dodge(s, 0.5, a, tau)
    e_s = el(lambda x: v_dodge(x, 0.5, a, tau), s)
    e_a = el(lambda x: v_dodge(s, 0.5, x, tau), a)
    e_t = el(lambda x: v_dodge(s, 0.5, a, x), tau)
    print(f"{name:<44}{v:8.2f}{e_s:8.3f}{e_a:8.3f}{e_t:9.3f}")
print("  e_s = 1 exactly by construction (v is linear in s).")

# ---------------------------------------------------------------- C
hr("C  FoV / attitude coupling: the partial derivative the brief asks for does not exist")

def pitch_for_accel(a):
    """Level-flight body pitch needed to produce horizontal acceleration a (point mass)."""
    return math.degrees(math.atan2(a, g))

def a_fov(hfov_deg, tilt_deg):
    """Horizontal acceleration at which the velocity/flight direction leaves the camera FoV.
    Condition: body pitch - camera up-tilt <= HFoV/2."""
    lim = math.radians(hfov_deg / 2.0 + tilt_deg)
    if lim >= math.radians(89.9):
        return float('inf')
    return g * math.tan(lim)

print("body pitch required for a given horizontal acceleration (point mass, level flight):")
for a in (5.0, 9.81, 20.0, 38.0, 55.0):
    print(f"  a = {a:5.1f} m/s^2  ->  pitch = {pitch_for_accel(a):5.1f} deg"
          f"   (= {a/g:4.2f} g horizontal)")
print()
print("D435i-class depth camera, HFoV about 90 deg (A-20); A-20 tilts it 30 deg up above 7 m/s.")
print(f"{'HFoV deg':>9}{'tilt deg':>10}{'a_fov m/s^2':>13}{'a_fov/g':>9}"
      f"{'v=sqrt(2 a_fov s), s=6 m':>26}")
for hfov, tilt in ((90, 0), (90, 30), (120, 0), (120, 30), (155, 0)):
    af = a_fov(hfov, tilt)
    vv = math.sqrt(2 * af * 6.0) if math.isfinite(af) else float('inf')
    print(f"{hfov:9.0f}{tilt:10.0f}{af:13.2f}{af/g:9.2f}{vv:26.2f}")
print()
print("Reading: with a 90 deg untilted forward camera the flight direction leaves the FoV at")
print("1.00 g of braking, capping the usable stop bound at sqrt(2 * 9.81 * 6) = "
      f"{math.sqrt(2*9.81*6):.2f} m/s,")
print("which is where A-20's success falls to 60 per cent (10 m/s). With the 30 deg up-tilt the")
print("same geometry allows 3.73 g and 21.2 m/s. So s depends on a: ds/da < 0 through body")
print("attitude, and 'relax one limit holding the others fixed' is not an available operation.")

# ---------------------------------------------------------------- D
hr("D  Delay-limited bandwidth mapped to a speed, and the delay that would bind")

def wc_max(tau_eff, pm_deg=45.0):
    """Gain crossover permitted by a pure delay on an integrator loop (A-32)."""
    return (math.pi / 2.0 - math.radians(pm_deg)) / tau_eff

def v_from_bandwidth(tau_eff, R, m, pm_deg=45.0):
    """Own construction: a course of turn radius R traversed at speed v has characteristic
    angular frequency v/R; require the position loop crossover to exceed m times it."""
    return wc_max(tau_eff, pm_deg) * R / m

print("wc <= (pi/2 - PM)/tau_eff  (A-32); PM = 45 deg -> wc*tau_eff <= 0.7854")
for tau in (0.005, 0.017, 0.040, 0.130, 0.220):
    print(f"  tau_eff = {tau*1000:6.1f} ms  ->  wc <= {wc_max(tau):7.2f} rad/s"
          f" = {wc_max(tau)/(2*math.pi):6.2f} Hz")
print()
print("map to speed with v <= wc R / m   (R = turn radius, m = frequency separation factor)")
print(f"{'tau_eff ms':>11}{'R=3,m=3':>10}{'R=5,m=3':>10}{'R=5,m=5':>10}{'R=10,m=5':>11}")
for tau in (0.017, 0.040, 0.130, 0.220):
    print(f"{tau*1000:11.1f}{v_from_bandwidth(tau,3,3):10.1f}{v_from_bandwidth(tau,5,3):10.1f}"
          f"{v_from_bandwidth(tau,5,5):10.1f}{v_from_bandwidth(tau,10,5):11.1f}")
print()
for v_target in (5.0, 7.0, 10.0, 20.0):
    for R, m in ((5, 3), (5, 5)):
        tau_bind = wc_max_inv = (math.pi/2 - math.radians(45.0)) * R / (m * v_target)
        print(f"  latency that would make the delay bound bind at {v_target:5.1f} m/s"
              f" (R={R} m, m={m}): tau_eff = {tau_bind*1000:6.1f} ms")
print()
print("Retrodiction check: the 2019 onboard racing system had about 130 ms estimation latency")
print("and its planner was illustrated with a +/-7.5 m/s velocity cap (A-22). The bound above at")
print(f"130 ms, R=5 m, m=3 gives {v_from_bandwidth(0.130,5,3):.1f} m/s - the same order, so the")
print("construction is at least consistent with the one historical case where a team chose a cap.")

# ---------------------------------------------------------------- E
hr("E  Is any single-limit bound active at the demonstrated onboard-only speeds?")

demo = [
    ("unseen clutter, 100 per cent success (A-20)", 5.0),
    ("unseen clutter, 80 per cent (8/10) (A-20)", 7.0),
    ("unseen clutter, 60 per cent (A-20)", 10.0),
    ("unseen perturbed-gate track, onboard depth (A-29)", 5.3),
    ("seen gate track, minimal sensors, peak (A-26)", 32.2),
]
bounds = {
    "thrust/TWR bang-bang mean over 10.7 m, TWR 4.4": rows_A[4.5][1],
    "thrust/TWR bang-bang peak over 10.7 m, TWR 4.4": rows_A[4.5][2],
    "stop bound s=6 m, a=39 m/s^2, tau=40 ms": v_stop(6.0, 39.0, 0.040),
    "stop bound s=6 m, a=20 m/s^2, tau=50 ms": v_stop(6.0, 20.0, 0.050),
    "dodge bound s=6 m, r=0.5 m, a=39, tau=40 ms": v_dodge(6.0, 0.5, 39.0, 0.040),
    "FoV-capped stop bound, 90 deg untilted, s=6 m": math.sqrt(2 * a_fov(90, 0) * 6.0),
    "FoV-capped stop bound, 90 deg +30 deg tilt, s=6 m": math.sqrt(2 * a_fov(90, 30) * 6.0),
    "delay bound tau=40 ms, R=5 m, m=3": v_from_bandwidth(0.040, 5, 3),
    "delay bound tau=40 ms, R=5 m, m=5": v_from_bandwidth(0.040, 5, 5),
    "paper's own latency+range bound (A-21, lowest of 3)": 12.0,
}
print(f"{'bound':<52}{'v_bound m/s':>12}")
for k, v in bounds.items():
    print(f"{k:<52}{v:12.2f}")
print()
print("ratio demonstrated / bound  (a ratio well below 1 means that bound is NOT active):")
hdr = f"{'demonstrated':<52}{'v m/s':>7}"
print(hdr + "".join(f"{i:>7}" for i in range(1, len(bounds) + 1)))
for name, v in demo:
    row = f"{name:<52}{v:7.2f}"
    for k, vb in bounds.items():
        row += f"{v/vb:7.2f}"
    print(row)
print("(columns 1-10 in the order of the bound table above)")
print()
mn = min(bounds.values())
print(f"lowest of all bounds = {mn:.2f} m/s; the best-documented >=90 per cent unseen-course")
print(f"result is 5 m/s, i.e. {5.0/mn:.2f} of the lowest bound and "
      f"{5.0/max(bounds.values()):.2f} of the highest.")

# ---------------------------------------------------------------- F
hr("F  Trial economics of the brief's own metric (is it measurable?)")

def binom_tail_le(k, n, p):
    """P(X <= k) for X ~ Bin(n,p), exact rational-free summation."""
    tot = 0.0
    for i in range(0, k + 1):
        tot += math.comb(n, i) * p**i * (1 - p)**(n - i)
    return tot

def cp_lower(k, n, alpha=0.05):
    """Clopper-Pearson one-sided lower confidence bound for p given k successes of n."""
    if k == n:
        return alpha ** (1.0 / n)
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        # lower bound solves P(X >= k | p) = alpha  <=>  P(X <= k-1 | p) = 1 - alpha
        if binom_tail_le(k - 1, n, mid) > 1 - alpha:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

print("Q1: how many consecutive successes certify p >= 0.90 at 95 per cent one-sided?")
n_need = math.ceil(math.log(0.05) / math.log(0.90))
print(f"   smallest n with 0.05^(1/n) >= 0.90 : n = {n_need}"
      f"   (0.05^(1/{n_need}) = {0.05**(1/n_need):.4f}, "
      f"0.05^(1/{n_need-1}) = {0.05**(1/(n_need-1)):.4f})")
print(f"   check via Clopper-Pearson k=n: cp_lower({n_need},{n_need}) = "
      f"{cp_lower(n_need,n_need):.4f}")
print()
print("Q2: what does the best-documented unseen-course data point actually certify?")
for k, n in ((10, 10), (8, 10), (6, 10), (38, 43), (1, 4), (5, 7)):
    print(f"   {k}/{n} successes -> point {k/n:5.3f}, 95 per cent one-sided lower bound "
          f"{cp_lower(k,n):5.3f}   (A-20 / A-27 style)")
print()
print("Q3: trials to distinguish a true 0.90 from a true 0.80 (one-sided, alpha=0.05, power 0.8):")
z_a, z_b = 1.6449, 0.8416
n_norm = (z_a * math.sqrt(0.9 * 0.1) + z_b * math.sqrt(0.8 * 0.2)) ** 2 / (0.10 ** 2)
print(f"   normal approximation: n = {n_norm:.1f} -> {math.ceil(n_norm)} trials")
# exact check by searching n for a binomial test
def exact_power(n, p0=0.90, p1=0.80, alpha=0.05):
    # reject H0 (p=p0) if failures >= c, where c is smallest c with P(fail>=c|p0) <= alpha
    c = None
    for cc in range(0, n + 1):
        # P(failures >= cc | p = p0) = P(successes <= n-cc | p0)
        if binom_tail_le(n - cc, n, p0) <= alpha:
            c = cc
            break
    if c is None:
        return 0.0, None
    # power = P(failures >= c | p1) = P(successes <= n-c | p1)
    return binom_tail_le(n - c, n, p1), c
for n in (30, 50, 69, 80, 100, 120):
    pw, c = exact_power(n)
    print(f"   exact: n = {n:4d}  reject if failures >= {c}  power against p=0.80 = {pw:5.3f}")
print()
print("Q4: the metric is a sup over speeds, so it needs this at several speed set-points.")
for npts in (3, 5):
    print(f"   {npts} speed points x {n_need} flights (certification only) = {npts*n_need} flights;")
    print(f"   {npts} speed points x {math.ceil(n_norm)} flights (discrimination) = "
          f"{npts*math.ceil(n_norm)} flights")
print("   at a 10 per cent crash rate and a racing airframe, that is tens of airframe repairs.")

# ---------------------------------------------------------------- G
hr("G  Equal-per-cent (elasticity) versus equal-attainable-increment sensitivity")

base_s, base_a, base_tau = 6.0, 39.0, 0.040
v0 = v_stop(base_s, base_a, base_tau)
print(f"baseline: s={base_s} m, a={base_a} m/s^2 (TWR 4.1), tau={base_tau*1000:.0f} ms"
      f" -> v = {v0:.2f} m/s")
print()
print("(i) equal per cent: +10 per cent on each limit")
for lbl, f in (("range s", lambda k: v_stop(base_s * k, base_a, base_tau)),
               ("braking a (thrust)", lambda k: v_stop(base_s, base_a * k, base_tau)),
               ("latency tau (-10 per cent)", lambda k: v_stop(base_s, base_a, base_tau / k))):
    v1 = f(1.10)
    print(f"   {lbl:<28} v -> {v1:6.2f} m/s   change {100*(v1/v0-1):+6.2f} per cent")
print()
print("(ii) equal attainable increment, using increments already demonstrated on hardware")
moves = [
    ("tau 40 -> 13.8 ms (event-camera loop, A-23, 1-DOF analogy)",
     v_stop(base_s, base_a, 0.0138)),
    ("tau 40 -> 17 ms (MonoRace simulated image delay, A-28)",
     v_stop(base_s, base_a, 0.017)),
    ("TWR 4.1 -> 12.35 (A-11 platform exists, mocap)",
     v_stop(base_s, a_horiz(12.35), base_tau)),
    ("s 6 -> 10 m (better depth range)", v_stop(10.0, base_a, base_tau)),
    ("s 6 -> 20 m (LiDAR class, D-39)", v_stop(20.0, base_a, base_tau)),
    ("tau -> 0 (perfect, unattainable)", v_stop(base_s, base_a, 0.0)),
]
for lbl, v1 in moves:
    print(f"   {lbl:<58} v -> {v1:6.2f} m/s  {100*(v1/v0-1):+7.2f} per cent")
print()
print("The ranking flips between (i) and (ii): per cent for per cent, range beats latency by")
print("about an order of magnitude; per attainable move, thrust and range are both large and")
print("latency is capped at the gap between tau=40 ms and tau=0, which is only")
print(f"{100*(v_stop(base_s,base_a,0.0)/v0-1):.1f} per cent on this bound.")

hr("END")
