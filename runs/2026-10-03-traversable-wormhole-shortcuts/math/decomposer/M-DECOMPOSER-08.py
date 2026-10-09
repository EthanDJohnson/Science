"""M-DECOMPOSER-08: does a one-sided shortcut carry a complete achronal null geodesic through its throat (L6),
and does a long throat carry none (L7)?

Independent toy model (not the lens's argument): flat Minkowski exterior, c = 1, units of d = 1.
Point-like mouths A = 0 and B = d e (e = x-hat), joined by a throat of null length L, with clock shift s:
entering A at t you leave B at t + tau, tau = L + s; entering B at t you leave A at t + L - s.
A direction of travel u entering A leaves B as R u, with R a rotation (an orientable gluing of the two
mouth spheres is any orientation-reversing isometry of S^2, i.e. -R, so R is free: it is the relative
orientation of the mouths). Shortcut (A->B): tau < d. CTC: tau + d <= 0 (or L - s + d <= 0).
Null geodesic through the throat: x = A + lam u, t = lam (lam < 0); x = B + lam R u, t = tau + lam (lam > 0).
Achronal iff no pair of its points is timelike-related, i.e. for every ordered pair the earliest arrival
time over all routes (exterior, and up to 3 forward or backward throat passes) is >= the time difference.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import limit, sign, identity, finish

# --- analytic pieces: cross-pair margin for a straight-through line at angle theta to e ---
Lam, d = sp.symbols("Lam d", positive=True)
k = sp.symbols("k", real=True)  # k = cos(theta) in [-1, 1]
g = sp.sqrt(d**2 + Lam**2 + 2 * d * Lam * k) - Lam   # exterior separation minus path length, R = I
limit(g, "Lam", sp.oo, d * k, domain={"k": (-1, 1)})
limit(g, "Lam", 0, d, domain={"k": (-1, 1)})
# g is non-increasing in Lam, so the infimum over Lam is the large-Lam value d k
sign(sp.diff(g, Lam), "nonpositive", domain={"Lam": (0.01, 100), "d": (0.1, 10), "k": (-1, 1)})
# rotated mouths, line along the rotation axis n perpendicular to e: separation sqrt(d^2+(2Lam)^2) - 2Lam -> 0
limit(sp.sqrt(d**2 + 4 * Lam**2) - 2 * Lam, "Lam", sp.oo, 0)

# --- numerical sweep over complete throat-crossing null lines ---
def rot(axis, ang):
    axis = np.asarray(axis, float); axis /= np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * K @ K

A = np.zeros(3); B = np.array([1.0, 0, 0])
def earliest(x, y, tf, tb):
    """earliest arrival time from x to y (arrays (...,3)), routes with up to 3 throat passes."""
    nA_x = np.linalg.norm(x - A, axis=-1); nB_x = np.linalg.norm(x - B, axis=-1)
    nA_y = np.linalg.norm(y - A, axis=-1); nB_y = np.linalg.norm(y - B, axis=-1)
    best = np.linalg.norm(y - x, axis=-1)
    for n in (1, 2, 3):
        best = np.minimum(best, nA_x + n * tf + (n - 1) * 1.0 + nB_y)    # forward A->B, n passes, delay tf = L + s each
        best = np.minimum(best, nB_x + n * tb + (n - 1) * 1.0 + nA_y)    # backward B->A, n passes, delay tb = L - s each
    return best

lams = np.concatenate([-np.logspace(-3, 6, 46)[::-1], np.logspace(-3, 6, 46)])
def margin(u, R, tau, tb):
    """min over ordered pairs of (earliest arrival - time difference); >= 0 means achronal."""
    Ru = R @ u
    pos = np.where(lams[:, None] < 0, A + lams[:, None] * u, B + lams[:, None] * Ru)
    t = np.where(lams < 0, lams, tau + lams)
    i, j = np.triu_indices(len(lams), 1)
    dt = t[j] - t[i]
    ok = dt > 0
    m = earliest(pos[i][ok], pos[j][ok], tau, tb) - dt[ok]
    return m.min() / max(1.0, 1e-9)

def directions(n=600):
    k = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * k / n); th = math.pi * (1 + 5 ** 0.5) * k
    pts = np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1)
    extra = np.array([[1, 0, 0], [-1, 0, 0], [0, 0, 1], [0, 0, -1], [0, 1, 0], [0, -1, 0]], float)
    return np.vstack([extra, pts])

TOL = 1e-6
def best_line(R, tau, tb, axis_hint=None):
    dirs = directions()
    if axis_hint is not None:
        dirs = np.vstack([np.asarray(axis_hint, float) / np.linalg.norm(axis_hint), dirs])
    ms = np.array([margin(u, R, tau, tb) for u in dirs])
    return ms.max(), dirs[ms.argmax()]

# (name, R, L, s, axis hint, expected sign of best margin); forward delay tf = L + s, backward tb = L - s, d = 1
n60 = [0.5, 0, math.sqrt(3) / 2]
cases = [
    ("aligned mouths (R = I), static shortcut L = 0.5d", np.eye(3), 0.5, 0.0, None, "nonnegative"),
    ("aligned mouths, static long throat L = 1.5d", np.eye(3), 1.5, 0.0, None, "negative"),
    ("aligned mouths, L = 0.5d, lag s = -2d (past CTC threshold)", np.eye(3), 0.5, -2.0, None, "negative"),
    ("R = 180 deg about z (perp to e), static shortcut L = 0.5d", rot([0, 0, 1], math.pi), 0.5, 0.0, [0, 0, 1], "negative"),
    ("R = 10 deg about z (perp to e), static shortcut L = 0.5d", rot([0, 0, 1], math.radians(10)), 0.5, 0.0, [0, 0, 1], "negative"),
    ("R = 180 deg about z, zero-length throat L = 0 (thin shell), static", rot([0, 0, 1], math.pi), 0.0, 0.0, [0, 0, 1], "nonnegative"),
    ("R = 180 deg about z, L = 0.5d with lag s = -1d (tf = -0.5d)", rot([0, 0, 1], math.pi), 0.5, -1.0, [0, 0, 1], "nonnegative"),
    ("R = 90 deg about x (axis along e), static shortcut L = 0.5d", rot([1, 0, 0], math.pi / 2), 0.5, 0.0, [1, 0, 0], "nonnegative"),
    ("R = 180 deg about axis with e.n = 0.5, static L = 0.4d", rot(n60, math.pi), 0.4, 0.0, n60, "nonnegative"),
    ("R = 180 deg about axis with e.n = 0.5, static L = 0.6d", rot(n60, math.pi), 0.6, 0.0, n60, "negative"),
]
for name, R, Lt, s, hint, expect in cases:
    tau, tb = Lt + s, Lt - s
    print(f"[{name}] T_thru(A->B) = {tau:+.2f} d/c vs T_ext = 1 d/c -> {'shortcut' if tau < 1 else 'not a shortcut'}")
    m, u = best_line(R, tau, tb, hint)
    m = 0.0 if abs(m) < TOL else m
    print(f"{name}: best margin over lines = {m:.4g} at u = {np.round(u, 3)} -> "
          f"{'achronal line exists' if m >= 0 else 'every throat-crossing line chronal'}")
    sign(sp.Float(m), expect)
raise SystemExit(finish())
