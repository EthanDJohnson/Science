"""Falsifier C7-0 (physics): does the achronal-ANEC barrier act at the shortcut lag
Delta_s = T_thru - d, as C7 says, for every orientable gluing of a point-mouth handle?

Toy model (geometric units c = 1, flat exterior, static point mouths A = 0, B = d e):
- throat delay A->B is tau = T_thru - Delta (B's clock offset Delta);
- a ray entering A along unit u leaves B along R u.
Sphere gluing: point A + r (|r| small) is identified with B + M r, M in O(3).
A ray entering A along u hits A's sphere at r = -u, reappears at B + M(-u) and moves
outward along -M u, so R = -M.  The handle is orientable iff the sphere map is
orientation reversing, det M = -1, hence det R = +1: R in SO(3).

Achronality of the complete straight null line through the throat (exterior route test):
margin(Lp, Lq) = |d e + Lp u + Lq R u| - Lp - Lq - tau ;  achronal iff inf margin >= 0.
(M-DECOMPOSER-08 formula: achronal for some u iff tau <= d * max{e.u : R u = u}.)
"""
import numpy as np

rng = np.random.default_rng(7)
YR = 1.0  # work in years and light-years (c = 1 ly/yr)


def rand_rot():
    q = rng.normal(size=4); q /= np.linalg.norm(q)
    a, b, c, dd = q
    return np.array([[a*a+b*b-c*c-dd*dd, 2*(b*c-a*dd), 2*(b*dd+a*c)],
                     [2*(b*c+a*dd), a*a-b*b+c*c-dd*dd, 2*(c*dd-a*b)],
                     [2*(b*dd-a*c), 2*(c*dd+a*b), a*a-b*b-c*c+dd*dd]])


def axis(R):
    w, v = np.linalg.eig(R)
    k = np.argmin(abs(w - 1))
    n = np.real(v[:, k]); return n / np.linalg.norm(n)


Lgrid = np.concatenate([[0.0], np.logspace(-3, 7, 150)])  # affine params in units of d


def inf_margin(u, R, d, tau):
    Ru = R @ u
    Lp, Lq = np.meshgrid(Lgrid * d, Lgrid * d, indexing="ij")
    vec = d * np.array([1.0, 0, 0])[:, None, None] + Lp[None] * u[:, None, None] + Lq[None] * Ru[:, None, None]
    m = np.linalg.norm(vec, axis=0) - Lp - Lq - tau
    return m.min()


def best_over_u(R, d, tau, nrand=80):
    us = rng.normal(size=(nrand, 3)); us /= np.linalg.norm(us, axis=1)[:, None]
    n = axis(R)
    cands = list(us) + [n, -n]
    return max(inf_margin(u, R, d, tau) for u in cands)


e = np.array([1.0, 0, 0])
d = 1.0
print("== 1. Orientable gluings: every R = -M with det M = -1 lies in SO(3) and has a fixed axis ==")
ok = 0
for i in range(200):
    M = -rand_rot()            # det(-R) = -1 for R in SO(3)
    R = -M
    assert abs(np.linalg.det(M) + 1) < 1e-9
    n = axis(R)
    ok += np.allclose(R @ n, n, atol=1e-9)
print(f"random orientable gluings with a fixed direction: {ok}/200")
P = np.diag([-1.0, 1, 1])     # mirror across the midplane, det -1 (orientable)
print("midplane-mirror gluing M = P: R = -P =", np.diag(-P), "axis =", axis(-P), "(along e: aligned)")
print("point-reflection gluing M = -I: R = I (every direction fixed: aligned)")
print("translation gluing M = +I (det +1, NON-orientable): R = -I, no fixed direction")

print("\n== 2. Brute-force achronality threshold vs formula tau_a = d|e.n| (d = 1) ==")
mism = 0; rows = []
for i in range(12):
    R = rand_rot()
    n = axis(R)
    tau_a = d * abs(e @ n)
    for tau in (tau_a - 0.15, tau_a + 0.15):
        b = best_over_u(R, d, tau)
        pred = tau <= tau_a
        got = b >= -1e-6
        mism += (pred != got)
        rows.append((abs(e @ n), tau, b, pred, got))
for r in rows[:8]:
    print(f"|e.n|={r[0]:.3f} tau={r[1]:+.3f} best inf margin={r[2]:+.4f} formula achronal={r[3]} brute={r[4]}")
print(f"mismatches formula vs brute force: {mism}/{len(rows)}")

print("\n== 3. Non-orientable translation gluing R = -I: best margin for tau in window (-d, d) ==")
for tau in (0.9, 0.0, -0.5, -0.95):
    print(f"tau={tau:+.2f}d best inf margin={best_over_u(-np.eye(3), d, tau):+.4f} (achronal iff >= 0)")

print("\n== 4. MM numbers: thresholds in yr (T_thru = pi*3000 ly/c, d = 1000 ly) ==")
T = np.pi * 3000.0; D = 1000.0
Ds, Dctc = T - D, T + D
print(f"T_thru = {T:.1f} yr; Delta_s = {Ds:.1f} yr; Delta_CTC = {Dctc:.1f} yr; window = {Dctc-Ds:.1f} yr")
for ang in (0, 30, 60, 90):
    c = np.cos(np.radians(ang))
    Da = T - D * c
    print(f"axis at {ang:2d} deg to e: barrier (achronal) lag Delta_a = {Da:.1f} yr; "
          f"unconstrained shortcut band Delta_a - Delta_s = {Da-Ds:.1f} yr; lead over CTC = {Dctc-Da:.1f} yr")
# fraction of Haar-random rotations whose axis lies within 5 deg of +/- e
axes = np.array([axis(rand_rot()) for _ in range(20000)])
frac = np.mean(abs(axes @ e) > np.cos(np.radians(5)))
print(f"Haar fraction of rotation axes within 5 deg of the separation: {frac:.4f} (analytic 1-cos5 = {1-np.cos(np.radians(5)):.4f})")
print(f"mean |e.n| over Haar rotations: {np.mean(abs(axes @ e)):.3f} (analytic 0.5) -> mean band {D*(1-np.mean(abs(axes@e))):.0f} yr")

print("\n== 5. Loop check (cycle weights) for the thresholds, random cases ==")
bad = 0
for _ in range(20000):
    T_, d_, Dl = rng.uniform(0, 5), rng.uniform(0.01, 5), rng.uniform(-12, 12)
    w_ab = min(T_ - Dl, d_); w_ba = min(T_ + Dl, d_)
    ctc = (w_ab + w_ba) <= 0
    bad += (ctc != (Dl >= T_ + d_ or -Dl >= T_ + d_))
    bad += ((T_ - Dl < d_) != (Dl > T_ - d_))
print("threshold mismatches:", bad)
