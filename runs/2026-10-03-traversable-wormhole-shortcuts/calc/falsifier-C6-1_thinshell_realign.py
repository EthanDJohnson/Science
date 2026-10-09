"""Falsifier C6-1: do finite thin-shell mouths re-open complete achronal throat lines
for the 'misaligned' one-sided shortcuts of M-DECOMPOSER-08?

Model (units c = 1, lengths in units of the mouth separation d = 1):
  flat exterior R^3 x time, static spherical mouths of radius a centred at A = 0, B = d e.
  Thin-shell (Visser cut-and-paste) throat: the point A + a m is identified with B + a G m,
  with interior light-time tau (the decomposer's L, static s = 0).  Orientable gluings have
  det G = -1; the decomposer writes them G = -R, R in SO(3).  Radial rays then map v -> R v
  (the point-mouth direction map used in M-DECOMPOSER-08 / M-IDEALIZER-01/02).
  A null ray crossing a thin shell keeps its tangential components and the size of its normal
  component (metric continuous across the shell), so a ray with velocity v hitting A at the
  point with outward normal n leaves B + a G n with velocity  v_out = G * reflect_n(v),
  reflect_n(v) = v - 2 (v.n) n.  For a point mouth only n = -v (radial) is kept, giving
  v_out = -G v = R v.

Realignment: v_out = v  <=>  reflect_n(v) = G^{-1} v =: w.  Any w != v is reached with
  n = (w - v)/|w - v|.  Then the in-leg is P0 - s v (t = -s), the out-leg Q0 + s v
  (t = tau + s), P0 = A + a n, Q0 = B + a G n.

Achronality check: sup over ordered pairs on the line of (line time difference - earliest
arrival).  Earliest arrival is under-estimated (conservative for proving achronality):
  exterior: straight-line distance (ignores obstruction by the balls -> lower bound);
  one throat pass A->B or B->A: min over a Fibonacci grid of hit points, minus the Lipschitz
     bound 2 a * (max grid spacing) so the value is a rigorous lower bound;
  two or more passes: >= 2 tau + dist(x, nearest sphere) + dist(y, nearest sphere).
If the sup margin is <= 0, the line is achronal (to within the pair grid; asymptotic margin
computed analytically as tau - (Q0 - P0).v).
"""
import numpy as np

d = 1.0
e = np.array([1.0, 0.0, 0.0])
A = np.zeros(3)
B = d * e


def rot(axis, ang):
    axis = np.asarray(axis, float)
    axis = axis / np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K


def fib_sphere(N):
    i = np.arange(N) + 0.5
    phi = np.arccos(1 - 2 * i / N)
    th = np.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1)


NG = 12000
M = fib_sphere(NG)
# max nearest-neighbour angular spacing of the grid (estimate): ~ sqrt(4 pi / N) * 1.2
spacing = 1.2 * np.sqrt(4 * np.pi / NG)


def best_line(G, a, tau, nv=20000):
    """Search directions v for the realigned through-line with the most negative asymptotic margin."""
    Gi = np.linalg.inv(G)
    V = fib_sphere(nv)
    W = V @ Gi.T
    diff = W - V
    nd = np.linalg.norm(diff, axis=1)
    ok = nd > 1e-9
    n = np.zeros_like(V)
    n[ok] = diff[ok] / nd[ok, None]
    Gn = n @ G.T
    P0 = A + a * n
    Q0 = B + a * Gn
    asym = tau - np.einsum('ij,ij->i', Q0 - P0, V)
    asym[~ok] = np.inf
    # legs must leave/enter from outside: v.n < 0 and (G n).v > 0
    valid = ok & (np.einsum('ij,ij->i', V, n) < -1e-12) & (np.einsum('ij,ij->i', V, Gn) > 1e-12)
    asym[~valid] = np.inf
    k = int(np.argmin(asym))
    return V[k], n[k], Gn[k], asym[k], int(valid.sum())


def _f(m, x, y, C1, C2, Gmap, a, tau):
    m = m / np.linalg.norm(m)
    return np.linalg.norm(C1 + a * m - x) + tau + np.linalg.norm(y - C2 - a * (Gmap @ m))


def via(x, y, C1, C2, Gmap, a, tau, ncand=2):
    """one-pass arrival time x -> sphere(C1) -> sphere(C2) -> y: grid minimum, then a
    pattern-search refinement on the sphere from the best few grid points (converged to
    step 1e-12 rad), so the minimum is resolved far below the margins reported."""
    h1 = C1 + a * M
    h2 = C2 + a * (M @ Gmap.T)
    t = np.linalg.norm(h1 - x, axis=1) + tau + np.linalg.norm(y - h2, axis=1)
    best = t.min()
    for k in np.argsort(t)[:ncand]:
        m = M[k].copy()
        fm = t[k]
        step = spacing
        while step > 1e-11:
            # tangent basis
            ref = np.array([1.0, 0, 0]) if abs(m[0]) < 0.9 else np.array([0, 1.0, 0])
            t1 = np.cross(m, ref); t1 /= np.linalg.norm(t1)
            t2 = np.cross(m, t1)
            improved = False
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                mm = m + step * (dx * t1 + dy * t2)
                mm /= np.linalg.norm(mm)
                fv = _f(mm, x, y, C1, C2, Gmap, a, tau)
                if fv < fm - 1e-15:
                    m, fm, improved = mm, fv, True
                    break
            if not improved:
                step *= 0.5
        best = min(best, fm)
    return best


def dist_sph(x, a):
    return min(np.linalg.norm(x - A), np.linalg.norm(x - B)) - a


def full_check(G, a, tau, v, n, Gn, svals):
    Gi = np.linalg.inv(G)
    P0 = A + a * n
    Q0 = B + a * Gn
    pts = [(P0 - s * v, -s, 'in') for s in svals] + [(Q0 + s * v, tau + s, 'out') for s in svals]
    worst = -np.inf
    worst_pair = None
    for i, (x, tx, li) in enumerate(pts):
        for j, (y, ty, lj) in enumerate(pts):
            dt = ty - tx
            if dt <= 0 or i == j:
                continue
            ext = np.linalg.norm(y - x)
            ab = via(x, y, A, B, G, a, tau)
            ba = via(x, y, B, A, Gi, a, tau)
            two = 2 * tau + max(dist_sph(x, a), 0) + max(dist_sph(y, a), 0)
            earliest = min(ext, ab, ba, two)
            m = dt - earliest
            if m > worst:
                worst = m
                worst_pair = (li, round(float(-tx if li == 'in' else tx - tau), 4),
                              lj, round(float(-ty if lj == 'in' else ty - tau), 4))
    return worst, worst_pair


svals = np.concatenate([[0.0], np.geomspace(1e-3, 1e3, 14)])

print("Model: flat exterior, d = 1, c = 1; thin-shell mouths radius a; tau = interior light-time (units of d/c)")
print("Hit-point minimisation: Fibonacci grid (spacing %.4f rad) + pattern-search refinement to 1e-11 rad" % spacing)
cases = [
    ("aligned R = I (G = -I)", -np.eye(3)),
    ("R = 10 deg about z (perp to e)", -rot([0, 0, 1], np.radians(10))),
    ("R = 180 deg about z (perp to e)", -rot([0, 0, 1], np.pi)),
    ("R = 90 deg about z (perp to e)", -rot([0, 0, 1], np.pi / 2)),
    ("non-orientable translation gluing G = +I (idealizer 'mirror', radial m = -n)", np.eye(3)),
]
tau = 0.5
for a in (0.05, 0.01):
    print("\n=== mouth radius a = %.3f d, tau = L = %.2f d (shortcut: T_thru/T_ext = %.2f in point limit) ===" % (a, tau, tau / d))
    for name, G in cases:
        v, n, Gn, asym, nvalid = best_line(G, a, tau)
        print("\nCase:", name, "| det G = %+.0f" % np.linalg.det(G))
        if not np.isfinite(asym):
            print("  no direction v admits a realigned through-ray (v_out = v) except grazing incidence; valid directions = %d" % nvalid)
            continue
        print("  best v = %s, hit normal n = %s, |n.v| = %.4f" % (np.round(v, 4), np.round(n, 4), abs(n @ v)))
        print("  asymptotic margin tau - (Q0-P0).v = %+.5f d (negative => achronal at large separation)" % asym)
        print("  realigned-line threshold: achronal for tau <= %.5f d" % (tau - asym))
        worst, pair = full_check(G, a, tau, v, n, Gn, svals)
        print("  full pair check (15+15 points, s up to 1e3 d; margin 0 = the line itself, null-related): sup margin = %+.5f d at pair %s" % (worst, pair))
        print("  verdict: %s" % ("ACHRONAL complete throat line exists" if worst <= 1e-7 else "chronal (some pair timelike-related)"))

# Analytic threshold for R = 180 deg about axis k perp e: sqrt(d^2 + 4 a^2)
for a in (0.05, 0.01):
    print("\nAnalytic check R=180deg (k perp e): threshold sqrt(d^2+4a^2) = %.5f d at a = %.2f" % (np.sqrt(d ** 2 + 4 * a ** 2), a))
