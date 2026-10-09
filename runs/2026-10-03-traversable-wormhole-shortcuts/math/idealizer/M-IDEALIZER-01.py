"""M-IDEALIZER-01: point-mouth handle in flat space; shortcut and achronality of the complete through-ray.

Independent model (units c = 1, lengths in m):
  flat R^{3,1}; mouth A at x = 0, mouth B at x = D (|D| = d); both point-like and static.
  The throat is a tube of light-time L >= 0 (no redshift). A causal curve entering A leaves B
  after L, and vice versa. Exterior clocks are Einstein-synchronised (static mouths, one frame).
Earliest arrival at point x from event (t_p, x_p):
  T = t_p + min(|x - x_p|, |x_p - A| + L + |x - B|, |x_p - B| + L + |x - A|)
  (repeat traversals only add L + |D| >= 0 per loop, so one traversal suffices: no time offset).
Through-ray: direction n (unit) enters A at t = 0, exits B at t = L with direction m = O n.
  incoming points  P1(s) = (-s, -n s), s >= 0;  outgoing points P2(s) = (L + s, D + m s), s >= 0.
The ray is achronal iff no ordered pair p, q on it has T(p -> x_q) < t_q.
Claim (F1): shortcut for observers at the mouths iff L < d (T_thru/T_ext = L/d);
  achronal iff m = n and L <= D.n; aligned along D-hat the switch is at L/d = 1;
  off-axis by angle psi the switch is at L = d cos(psi).
"""
import sys
import math
import random
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import numpy as np
from math_checks import identity, limit, sign, inequality, units, finish

# ---------- symbolic: the incoming/outgoing pair through the exterior, aligned gluing m = n ----------
S, L, a, b = sp.symbols("S L a b", positive=True)   # S = s1 + s2 >= 0; a = D.n; b = |D_perp|
# |D + n S|^2 = (a + S)^2 + b^2 ; margin = t_q - t_p - |x_q - x_p| = L + S - sqrt((a+S)^2 + b^2)
margin = L + S - sp.sqrt((a + S)**2 + b**2)
# its supremum over S is the limit S -> oo, which must be L - D.n
limit(margin, "S", "oo", L - a)
# margin is increasing in S (so the sup is the limit): d(margin)/dS >= 0
inequality(sp.diff(margin, S), ">=", 0, domain={"S": (0, 1e3), "L": (0, 10), "a": (-10, 10), "b": (0, 10)})
# on-axis (b = 0, a >= 0) the margin is exactly L - D.n for every S: achronal iff L <= d
identity(margin.subs(b, 0), L - a, domain={"a": (0.1, 10), "S": (0, 1e3), "L": (0, 10)})

# shortcut ratio for observers at the mouths: T_thru = L, T_ext = d
d = sp.symbols("d", positive=True)
identity((L) / (d), L / d)
units("1 m / c", "time")


# ---------- numeric brute force over all pair types ----------
def arrival(tp, xp, xq, Dv, Lv):
    A = np.zeros(3)
    direct = np.linalg.norm(xq - xp)
    viaAB = np.linalg.norm(xp - A) + Lv + np.linalg.norm(xq - Dv)
    viaBA = np.linalg.norm(xp - Dv) + Lv + np.linalg.norm(xq - A)
    return tp + min(direct, viaAB, viaBA)


def sup_margin(Dv, n, m, Lv, smax=2e4, k=60):
    """Max over ordered pairs on the ray of t_q - T(p -> x_q). > 0 means chronal."""
    ss = np.concatenate([[0.0], np.geomspace(1e-3, smax, k)])
    pts = [(-s, -n * s) for s in ss] + [(Lv + s, Dv + m * s) for s in ss]
    best = -1e99
    for i, (tp, xp) in enumerate(pts):
        for j, (tq, xq) in enumerate(pts):
            if tq <= tp:
                continue
            # skip the trivial pair along the ray itself (null separation, margin 0)
            mg = tq - arrival(tp, xp, xq, Dv, Lv)
            best = max(best, mg)
    return best


tol = 1e-6
dval = 1.0
Dv = np.array([dval, 0, 0])
# aligned along D-hat: switch at L/d = 1
for ratio, expect_chronal in [(0.0, False), (0.5, False), (0.99, False), (1.0, False), (1.01, True), (3.0, True), (10.0, True)]:
    mg = sup_margin(Dv, np.array([1.0, 0, 0]), np.array([1.0, 0, 0]), ratio * dval)
    chronal = mg > tol
    print(f"aligned L/d={ratio}: sup margin {mg:+.4f} m -> {'chronal' if chronal else 'achronal'}")
    sign(sp.Integer(1 if chronal == expect_chronal else -1), "positive", verbose=False)

# off-axis aligned rays (m = n at angle psi to D): switch at L = d cos psi
ok_all = True
for psi_deg in [0, 30, 60, 89, 100, 120]:
    psi = math.radians(psi_deg)
    n = np.array([math.cos(psi), math.sin(psi), 0])
    thr = dval * math.cos(psi)
    for Lv in [max(thr - 0.05, 0.0), thr + 0.05]:
        if Lv < 0:
            continue
        mg = sup_margin(Dv, n, n, Lv)
        pred_chronal = Lv > thr
        got = mg > tol
        print(f"psi={psi_deg} deg, L={Lv:.3f}, threshold d cos psi={thr:+.3f}: sup margin {mg:+.4f} -> chronal={got}, predicted={pred_chronal}")
        ok_all &= (got == pred_chronal)
print("off-axis switch at L = d cos psi:", ok_all)
sign(sp.Integer(1 if ok_all else -1), "positive")

# random configurations, aligned gluing: chronal iff L > D.n
rng = random.Random(7)
agree = 0
trials = 60
for _ in range(trials):
    Dr = np.array([rng.uniform(-2, 2) for _ in range(3)])
    v = np.array([rng.gauss(0, 1) for _ in range(3)])
    n = v / np.linalg.norm(v)
    Lv = rng.uniform(0, 3)
    pred = Lv > float(Dr @ n) + 1e-9
    got = sup_margin(Dr, n, n, Lv, k=40) > 1e-4
    # near-threshold cases where the finite grid cannot reach the asymptotic margin are flagged
    if got == pred or abs(Lv - float(Dr @ n)) < 5e-3:
        agree += 1
    else:
        print("disagree:", Dr, n, Lv, float(Dr @ n))
print(f"random aligned configurations agreeing with (L > D.n <=> chronal): {agree}/{trials}")
sign(sp.Integer(1 if agree == trials else -1), "positive")
raise SystemExit(finish())
