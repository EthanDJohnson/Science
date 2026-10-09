"""Crux C6: cross-checks of the three verdicts' finite-mouth results.

1. Hemisphere argument (verdict C6-2): for any gluing G in O(3) and unit u,
   there is a unit n with n.u <= 0 and (G n).u >= 0, so the via-handle path
   length excess a*u.(n - G n) <= 0 and every far-pair minimiser threads the
   throat when L < d. Checked on random G (both determinants).
2. Thin-shell 180-degree threshold sqrt(d^2 + 4a^2) (verdict C6-1) at a = 0.01 d.
3. Residual (unbanned) window converted to SI time for the brief's mouth sizes,
   using verdict C6-0's Ellis delta(L=0) = 1.39738 b0 and verdict C6-2's
   ~1.5 a observer-wrap band (aligned mouths share the latter).
Units: geometric (c = 1) for 1-2, SI for 3.
"""
import numpy as np

rng = np.random.default_rng(6)
c = 2.99792458e8  # m/s

def rand_O3(det_sign):
    q, r = np.linalg.qr(rng.normal(size=(3, 3)))
    q = q @ np.diag(np.sign(np.diag(r)))
    if np.sign(np.linalg.det(q)) != det_sign:
        q[:, 0] *= -1
    return q

# 1. hemisphere argument
u = np.array([1.0, 0.0, 0.0])
pts = rng.normal(size=(200000, 3)); pts /= np.linalg.norm(pts, axis=1)[:, None]
worst = -np.inf
for det_sign in (+1, -1):
    for k in range(200):
        G = rand_O3(det_sign)
        a1 = pts @ u            # n.u
        a2 = (pts @ G.T) @ u    # (G n).u
        ok = (a1 <= 0) & (a2 >= 0)
        assert ok.any(), "no admissible n found"
        best_excess = np.min(a1[ok] - a2[ok])   # u.(n - G n), want <= 0
        worst = max(worst, best_excess)
print(f"1. Hemisphere check: 400 random G in O(3) (200 per det sign); every G has admissible n; "
      f"largest best-case excess u.(n - Gn) = {worst:.3e} (<= 0 means via-handle <= s+t+L)")
print("PASS hemisphere" if worst <= 0 else "FAIL hemisphere")
tol = 1e-3
for name, G in (("mirror +I", np.eye(3)), ("aligned -I", -np.eye(3)),
                ("rot180 about z, -R", -np.diag([-1.0, -1.0, 1.0]))):
    a1 = pts @ u; a2 = (pts @ G.T) @ u; ok = (a1 <= tol) & (a2 >= -tol)
    print(f"   {name}: admissible n (tol {tol}) exists = {ok.any()}, best excess = {np.min(a1[ok]-a2[ok]):.4f}"
          " (mirror: only n perp u qualifies, excess 0 -> via-handle = s+t+L exactly)")

# 2. thin-shell 180-degree threshold
for a in (0.05, 0.01):
    v = np.sqrt(1+4*a*a)
    print(f"2. Thin shell, rot180, a = {a} d: sqrt(d^2+4a^2) = {v:.5f} d")
    print("PASS threshold>d" if v > 1 else "FAIL threshold>d")

# 3. residual window in SI
rows = [("SM-MMP r_e (Q-11)", 2e-19), ("1 m throat", 1.0), ("MM r_e (Q-01)", 1.5e7)]
for name, a in rows:
    t_ellis = 1.39738 * a / c
    t_wrap = 1.5 * a / c
    t_extra = 0.36 * a / c
    print(f"3. {name}: a = {a:.2e} m; Ellis delta(0) = {t_ellis:.3e} s; "
          f"observer-wrap band ~1.5a/c = {t_wrap:.3e} s; misalignment-specific widening <= 0.36a/c = {t_extra:.3e} s")
d_ly = 9.4607e15
print(f"3b. MM r_e window as fraction of d = 1 ly: {1.39738*1.5e7/d_ly:.3e}")
