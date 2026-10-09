"""M-DIALECTICIAN-03: achronality of the B->A throat null geodesic in the window Delta_s < Delta < Delta_CTC.

Independent model (geometric units, c = 1): flat 3D exterior, mouths idealised as points B = (0,0,0),
A = (d,0,0). Throat = flat 1+1 strip of length T (= T_thru). Events in the throat are labelled by
B-gauge time: throat point s is reached from B at cost s, from A at cost (T - s) + Delta; leaving the
throat to B costs s, to A costs (T - s) - Delta. Exterior edges cost Euclidean distance.
Event Y is in the chronological future of X iff the shortest-path cost X -> Y is < t_Y - t_X.
Complete geodesic: incoming exterior ray B - r*w (time -r), throat (s, s), outgoing ray A + r'*u
(time T - Delta + r').
"""
import sys, math, itertools
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from math_checks import identity, sign, finish

T, d = 3.0, 1.0       # a long wormhole: T > d.  Delta_s = 2, Delta_ctc = 4.
TOL = 1e-9


def dist(p, q):
    return float(np.linalg.norm(np.asarray(p) - np.asarray(q)))


def chronal(Delta, w, u, include_ext=True, R=200.0, n=40):
    B, A = np.zeros(3), np.array([d, 0, 0])
    if T - Delta + d < 0:
        return "CTC"
    ev = []  # (kind, data, time)
    for s in np.linspace(0, T, n):
        ev.append(("th", s, s))
    if include_ext:
        for r in np.concatenate([np.linspace(0, 5, n), np.geomspace(5, R, n)]):
            ev.append(("ex", B - r * w, -r))
            ev.append(("ex", A + r * u, T - Delta + r))
    # all-pairs: cost from event X to node B/A and from node B/A to event Y; plus direct
    dBA, dAB = min(T - Delta, d), min(T + Delta, d)   # shortest node-to-node costs (no neg cycle)
    def to_nodes(e):
        k, x, _ = e
        if k == "th":
            return {"B": x, "A": T - x - Delta}
        return {"B": dist(x, B), "A": dist(x, A)}
    def from_nodes(e):
        k, x, _ = e
        if k == "th":
            return {"B": x, "A": T - x + Delta}
        return {"B": dist(x, B), "A": dist(x, A)}
    node = {("B", "B"): 0.0, ("A", "A"): 0.0, ("B", "A"): dBA, ("A", "B"): dAB}
    for X, Y in itertools.permutations(ev, 2):
        tx, ty = X[2], Y[2]
        best = math.inf
        if X[0] == "ex" and Y[0] == "ex":
            best = dist(X[1], Y[1])
        elif X[0] == "th" and Y[0] == "th":
            best = abs(Y[1] - X[1])
        out, inn = to_nodes(X), from_nodes(Y)
        for m1 in "BA":
            for m2 in "BA":
                best = min(best, out[m1] + node[(m1, m2)] + inn[m2])
        if best < ty - tx - TOL:
            return "chronal"
    return "achronal"


ax = np.array([1.0, 0, 0])
def rot(th):
    return np.array([math.cos(th), math.sin(th), 0.0])

Deltas = [0.0, 1.0, 1.9, 2.05, 2.5, 3.0, 3.5, 3.95, 4.1]
print(f"T={T}, d={d}: Delta_s={T-d}, Delta_ctc={T+d}")
rows = {}
for D in Deltas:
    seg = chronal(D, ax, ax, include_ext=False)
    axis = chronal(D, ax, ax)
    th60 = chronal(D, rot(math.pi / 3), rot(math.pi / 3))
    bent = chronal(D, ax, rot(math.pi / 2))
    rows[D] = (seg, axis, th60, bent)
    print(f"Delta={D:5.2f}: throat segment {seg:9s} | complete, on axis {axis:9s} | "
          f"complete, straight at 60 deg {th60:9s} | complete, bent 90 deg {bent}")

# Expected from the analytic argument: throat segment achronal iff Delta_s <= Delta < Delta_ctc
seg_ok = all((rows[D][0] == "achronal") == (T - d < D < T + d) for D in Deltas)
axis_ok = all((rows[D][1] == "achronal") == (T - d < D < T + d) for D in Deltas)
identity(str(int(seg_ok)), "1")
identity(str(int(axis_ok)), "1")
# Analytic off-axis criterion for a straight geodesic at angle th (large r): timelike pairs exist iff
# (T - Delta + r + r') - |A - B + (r + r') u| > 0 -> asymptotically d(1 - cos th) - (Delta - Delta_s) > 0.
th = math.pi / 3
print("off-axis straight geodesic at 60 deg is chronal for Delta - Delta_s < d(1-cos th) =", d * (1 - math.cos(th)))
identity(str(int(rows[2.05][2] == "chronal")), "1")   # 0.05 < 0.5 -> chronal
identity(str(int(rows[2.5][2] == "achronal")), "1")   # 0.5 = boundary; asymptotic equality -> achronal
identity(str(int(rows[3.0][2] == "achronal")), "1")
# Algebra of the two route bounds in the lens's argument
import sympy as sp
Tt, dd, Dl, s1, s2 = sp.symbols("T d Delta s1 s2", positive=True)
# exterior detour p(s1) -> B -> ext -> A -> q(s2) arrives later than the null geodesic when Delta > T - d (s1=0, s2=T worst case)
detour_minus_direct = (2 * s1 + dd + Dl + Tt - s2) - s2
sign(detour_minus_direct.subs({s1: 0, s2: Tt, Dl: Tt - dd + sp.Symbol("e", positive=True)}), "positive")
raise SystemExit(finish())
