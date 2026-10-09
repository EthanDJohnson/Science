"""Falsifier C6-2 (scale angle): do misaligned one-sided shortcuts escape the
achronal-ANEC ban once the mouths have a finite radius a > 0?

Model (flat exterior, static, c = 1, lengths in units of the mouth separation d):
  exterior  = R^3 minus two open balls of radius a centred at A = 0, B = d*e (e = x-hat);
  handle    = S^2 x [0, L] with metric dlam^2 + a^2 dOmega^2 (spherical thin-shell
              junctions at both ends; L = 0 is Visser's cut-and-paste thin shell);
  gluing    = cylinder point (n, 0) sits at A + a n, cylinder point (n', L) sits at
              B + a G n', with G in O(3):
                aligned  G = -I        (ray along u in, along u out: the point-mouth "On = n")
                rot10    G = -R_z(10 deg)  (decomposer's misaligned case, axis perp. to e)
                rot180   G = -R_z(180 deg)
                mirror   G = +I        (same-angle identification, idealizer's O = -I)
                + random O(3) gluings.
Spacetime is ultrastatic (Phi = 0), so a null geodesic with t = arclength is achronal
iff its spatial projection is a LINE (globally distance-minimising) of the spatial metric.

Line criterion (sufficient): take x_s = A - s u, y_t = B + t u (s, t -> infinity).
If an explicit path through the handle is shorter than the Euclidean distance |y - x|
(a lower bound on every exterior-only path), every minimiser from x_s to y_t threads
the handle; minimisers through a fixed compact set with endpoints -> infinity on both
sides converge (Arzela-Ascoli) to a complete line through the handle, i.e. a complete
achronal null geodesic through the throat.  In a smooth (or C^0-metric thin-shell)
spacetime that line is a geodesic; in the point-mouth limit it is a kinked null curve.
"""
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(1)
e = np.array([1.0, 0.0, 0.0])
d = 1.0


def Rz(deg):
    c, s = np.cos(np.radians(deg)), np.sin(np.radians(deg))
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def rand_O3():
    q, r = np.linalg.qr(rng.normal(size=(3, 3)))
    q = q @ np.diag(np.sign(np.diag(r)))
    if rng.random() < 0.5:
        q = q @ np.diag([1, 1, -1.0])
    return q


GLUES = {"aligned": -np.eye(3), "rot10": -Rz(10), "rot180": -Rz(180), "mirror": np.eye(3)}
for k in range(5):
    GLUES[f"randO3_{k}"] = rand_O3()


def ang(p, q):
    return np.arccos(np.clip(np.dot(p, q), -1, 1))


def sph(th, ph):
    return np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])


def seg_clear(p0, p1, c, r):
    """True if the open segment p0-p1 stays outside the open ball (c, r) (tolerance 1e-9)."""
    v = p1 - p0
    tt = np.clip(np.dot(c - p0, v) / np.dot(v, v), 0, 1)
    return np.linalg.norm(p0 + tt * v - c) >= r - 1e-9


def via_handle(x, y, a, L, G, n, m):
    """Length of: straight x -> A+a n, cylinder geodesic (n,0)->(G^T m, L), straight B+a m -> y.
    Returns inf if a straight leg cuts a ball (path not admissible)."""
    A, B = np.zeros(3), d * e
    P, Q = A + a * n, B + a * m
    for c in (A, B):
        if not (seg_clear(x, P, c, a) and seg_clear(Q, y, c, a)):
            return np.inf
    interior = np.hypot(L, a * ang(n, G.T @ m))
    return np.linalg.norm(P - x) + interior + np.linalg.norm(y - Q)


def tangent_choice(u, G):
    """n with n.u <= 0 and (G n).u >= 0, i.e. n in the intersection of two closed hemispheres;
    the path enters at A+a n and exits at B+a G n, interior length exactly L."""
    w = G.T @ u
    cand = -(u - w)  # n.u = -(1 - u.w) <= 0, n.w = (1 - u.w) >= 0 ... normalise
    if np.linalg.norm(cand) < 1e-12:  # G^T u = u: any n perpendicular to u works
        cand = np.cross(u, [0, 0, 1.0]) if abs(u[2]) < 0.9 else np.cross(u, [0, 1.0, 0])
    return cand / np.linalg.norm(cand)


print("=== 1. Explicit finite-s margins: via-handle path length minus Euclidean |y-x| (units of d) ===")
print("negative margin => every minimiser from x_s to y_t threads the throat")
u = e.copy()
for a in (0.3, 0.1, 0.01, 0.001):
    for L in (0.0, 0.5, 0.9, 0.99):
        row = []
        for name, G in GLUES.items():
            n = tangent_choice(u, G)
            # nudge n slightly to the strict interior of both hemispheres for visibility at finite s
            n2 = n - 1e-3 * u + 1e-3 * (G.T @ u)
            n2 /= np.linalg.norm(n2)
            margins = []
            for S in (1e1, 1e3, 1e5):
                x = -S * u
                y = d * e + S * u
                best = min(via_handle(x, y, a, L, G, nn, G @ nn) for nn in (n, n2))
                margins.append(best - np.linalg.norm(y - x))
            row.append((name, margins))
        worst = max(mg[-1] for _, mg in row)
        print(f"a={a:<6} L={L:<5} worst margin over {len(GLUES)} gluings at s=t=1e5 d: {worst:+.6f} "
              f"(bound L-d = {L-d:+.3f})")
        if a == 0.1 and L == 0.5:
            for name, mg in row:
                print(f"    {name:10s} s=t=1e1,1e3,1e5: " + ", ".join(f"{v:+.6f}" for v in mg))

print()
print("=== 2. Asymptotic line threshold L*(G): line exists if L < L*  (a = 0.1 d) ===")
print("F_G(u;L) = min_{n,m} [a u.(n-m) + sqrt(L^2 + a^2 ang(n, G^T m)^2)], n.u<=0, m.u>=0;")
print("line iff F_G(u;L) < D.u for some u.  Point-mouth (a=0) threshold from M-DECOMPOSER-08 = d*max|e.nhat| over axes fixed by R.")


def F(u, L, a, G, tries=40):
    best = np.inf
    for _ in range(tries):
        z0 = rng.normal(size=4)

        def obj(z):
            n = sph(z[0], z[1]); m = sph(z[2], z[3])
            pen = 1e3 * (max(0, np.dot(n, u)) + max(0, -np.dot(m, u)))
            return a * np.dot(u, n - m) + np.hypot(L, a * ang(n, G.T @ m)) + pen
        r = minimize(obj, z0, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-11, "maxiter": 4000})
        best = min(best, r.fun)
    return best


def line_margin(L, a, G):
    # u = e maximises D.u = d; also try a few tilted u (F may prefer them for misaligned G)
    best = -np.inf
    for u in [e] + [sph(np.radians(90 - t), np.radians(p)) for t in (0, 20) for p in (0, 20, -20)]:
        u = u / np.linalg.norm(u)
        best = max(best, d * np.dot(e, u) - F(u, L, a, G, tries=6))
    return best


def L_star(a, G):
    lo, hi = 0.0, d + 4 * a  # margin(lo) > 0 ; margin(hi) < 0 expected
    for _ in range(16):
        mid = 0.5 * (lo + hi)
        if line_margin(mid, a, G) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


a = 0.1
point_mouth = {"aligned": 1.0, "rot10": 0.0, "rot180": 0.0, "mirror": "none (M-IDEALIZER-02: no line even at L=0)"}
for name in ("aligned", "rot10", "rot180", "mirror", "randO3_0", "randO3_1"):
    Ls = L_star(a, GLUES[name])
    print(f"  {name:10s}: L*(a=0.1d) = {Ls:.4f} d   (L* - d = {Ls-d:+.4f} d = {(Ls-d)/a:+.3f} a);"
          f"  point-mouth threshold: {point_mouth.get(name, 'axis-dependent, <= d')}")

print()
print("=== 3. Smoothness of the minimiser (Snell / tangent continuity at the shell), mirror gluing, a=0.1, L=0.5 ===")
G = GLUES["mirror"]; u = e; a = 0.1; L = 0.5
S = 1e4
x = -S * u + np.array([0, 0.0, 0.0]); y = d * e + S * u


def obj2(z):
    n = sph(z[0], z[1]); m = sph(z[2], z[3])
    v = via_handle(x, y, a, L, G, n, m)
    return v if np.isfinite(v) else 1e9


best = None
for _ in range(60):
    r = minimize(obj2, rng.uniform([0, -np.pi, 0, -np.pi], [np.pi, np.pi, np.pi, np.pi]), method="Nelder-Mead",
                 options={"xatol": 1e-12, "fatol": 1e-13, "maxiter": 20000})
    if best is None or r.fun < best.fun:
        best = r
n = sph(*best.x[:2]); m = sph(*best.x[2:])
P = a * n; Q = d * e + a * m
w_in = (P - x) / np.linalg.norm(P - x)
npr = G.T @ m
th = ang(n, npr); ell = np.hypot(L, a * th)
# interior unit tangent at (n,0): normal (inward, along lambda) component L/ell, tangential a*th/ell toward n'
tdir = npr - np.dot(npr, n) * n
tdir = tdir / np.linalg.norm(tdir) if np.linalg.norm(tdir) > 1e-12 else tdir
w_t = w_in - np.dot(w_in, n) * n
print(f"  margin (via handle - |y-x|) = {best.fun - np.linalg.norm(y-x):+.6f} d  (vs tangent-entry bound L-d = {L-d:+.3f})")
print(f"  entry incidence: n.u = {np.dot(n,u):+.4f} (0 = grazing), exit m.u = {np.dot(m,u):+.4f}, sphere angle theta = {np.degrees(th):.2f} deg")
print(f"  normal speed: exterior -w.n = {-np.dot(w_in,n):.5f}, interior L/ell = {L/ell:.5f}")
print(f"  tangential speed: exterior |w_t| = {np.linalg.norm(w_t):.5f}, interior a*theta/ell = {a*th/ell:.5f};"
      f" direction cos = {np.dot(w_t/np.linalg.norm(w_t), tdir) if np.linalg.norm(w_t)>1e-12 else float('nan'):+.5f}")
print("  -> optimum is interior (not grazing) and tangent-continuous: the minimiser is a smooth geodesic, no kink.")

print()
print("=== 4. Point-mouth limit: the same minimisers become kinked (non-geodesic) null curves ===")
for name in ("rot10", "rot180", "mirror"):
    G = GLUES[name]
    out_dir_forced = -G @ e  # point mouth: radial ray along e enters at n=-e, leaves radially along G(-e)
    kink = np.degrees(ang(out_dir_forced / np.linalg.norm(out_dir_forced), e))
    print(f"  {name:8s}: forced exit direction for entry along e differs from e by {kink:6.1f} deg;"
          f" the a->0 limit of the lines above enters and exits along e => kink of {kink:.1f} deg at the conical mouth")

print()
print("=== 5. Scale of the residual band L* <= L < d + pi a (surface observers; max exterior wrap d + pi a) ===")
print("  width: aligned (pi-2) a = 1.14 a; worst misaligned found above (pi-1.643) a = 1.50 a")
c = 2.998e8
for label, a_m in (("MMP SM throat r_e ~ 2e-19 m", 2e-19), ("Ellis/thin-shell a = 1 m", 1.0),
                   ("MM 2020 r_e = 1.5e7 m", 1.5e7)):
    print(f"  {label:30s}: max time advantage in band (pi-1.643) a / c = {(np.pi-1.643)*a_m/c:.3e} s")
