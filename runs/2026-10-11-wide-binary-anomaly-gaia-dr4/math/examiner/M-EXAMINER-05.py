"""M-EXAMINER-05 (F3 ii, P5): eccentricity-template mismatch in a median-v~ test.
Claim: template f(e) ∝ e^2 applied to truth f(e) ∝ e^1.3 gives gamma_app = (med_true/med_template)^2 = 1.107;
the reverse gives 0.903. (Lens took medians from D-48: 0.5134 (alpha 1.3), 0.4880 (alpha 2).)
Independent MC: Kepler orbits, GM = 1, a = 1, f(e) = (alpha+1) e^alpha, mean anomaly uniform,
isotropic line of sight. v~ = v_p sqrt(s) (dimensionless). Selection in a narrow s bin with dN/da ∝ a^-p
weights each configuration by (s/a)^(p-1); p = 1.6 (D-48's choice) and p = 1 (Opik, unweighted) both shown.
Noise-free, no contamination.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, inequality, limit, finish

rng = np.random.default_rng(20261011)

def kepler_vtilde(n, alpha=None, e_fixed=None, gam=1.0):
    if e_fixed is not None:
        e = np.full(n, e_fixed)
    else:
        e = rng.random(n) ** (1.0 / (alpha + 1.0))          # inverse CDF of (alpha+1) e^alpha
    M = rng.random(n) * 2 * np.pi
    E = M.copy()
    for _ in range(60):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    r = 1 - e * np.cos(E)
    f = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    pos = np.stack([r * np.cos(f), r * np.sin(f), np.zeros(n)], 1)
    vv = np.sqrt(gam / (1 - e**2))[:, None] * np.stack([-np.sin(f), e + np.cos(f), np.zeros(n)], 1)
    nn = rng.normal(size=(n, 3)); nn /= np.linalg.norm(nn, axis=1)[:, None]
    sp_ = np.linalg.norm(pos - (pos * nn).sum(1)[:, None] * nn, axis=1)
    vp = np.linalg.norm(vv - (vv * nn).sum(1)[:, None] * nn, axis=1)
    return vp * np.sqrt(sp_), sp_          # v~ with Newtonian G M = 1 in the normalisation

def wmedian(x, w):
    i = np.argsort(x); c = np.cumsum(w[i]); return x[i][np.searchsorted(c, 0.5 * c[-1])]

N = 2_000_000
# limit / anchor: circular orbits. Closed form: v~ = sqrt(1 - n_v^2) (1 - n_r^2)^(1/4), (n_r, n_v) components of a
# uniform unit vector. Compare with the Kepler machinery at e = 0.
u = rng.normal(size=(N, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
vt_closed = np.sqrt(1 - u[:, 1]**2) * (1 - u[:, 0]**2) ** 0.25
vt0, s0 = kepler_vtilde(N, e_fixed=0.0)
m_closed, m_kep = np.median(vt_closed), np.median(vt0)
print(f"circular median v~: closed form {m_closed:.4f}, Kepler machinery {m_kep:.4f} (D-48 quotes 0.6925)")
identity(sp.Float(round(m_closed, 2)), sp.Float(round(m_kep, 2)))
print(f"<sin psi> = <s/r> circular = {s0.mean():.4f} vs pi/4 = {np.pi/4:.4f}")
inequality(sp.Float(abs(float(s0.mean()) - np.pi / 4)), "<", sp.Float(0.001))
print(f"circular median v~ weighted s^0.6 (p = 1.6): {wmedian(vt0, s0 ** 0.6):.4f}")

res = {}
for alpha in (1.3, 2.0):
    vt, s = kepler_vtilde(N, alpha=alpha)
    inequality(sp.Float(float(vt.max())), "<=", sp.sqrt(2))      # bound v~ <= sqrt(2) under Newton
    for p in (1.6, 1.0):
        res[(alpha, p)] = wmedian(vt, s ** (p - 1))
    print(f"alpha = {alpha}: median v~ (p=1.6) {res[(alpha,1.6)]:.4f}, (p=1) {res[(alpha,1.0)]:.4f}, max {vt.max():.4f}")
for p in (1.6, 1.0):
    g1 = (res[(1.3, p)] / res[(2.0, p)]) ** 2
    print(f"p = {p}: template alpha=2 on truth alpha=1.3 -> gamma_app = {g1:.4f}; reverse {1/g1:.4f}")
g16 = (res[(1.3, 1.6)] / res[(2.0, 1.6)]) ** 2
inequality(sp.Float(abs(g16 - 1.107)), "<", sp.Float(0.015))   # lens 1.107 within MC/convention spread
inequality(sp.Float(abs(1 / g16 - 0.903)), "<", sp.Float(0.015))
# arithmetic with D-48's quoted medians
identity(sp.Float(round((0.5134 / 0.4880) ** 2, 3)), sp.Float(1.107))
identity(sp.Float(round((0.4880 / 0.5134) ** 2, 3)), sp.Float(0.903))
# limit: identical templates -> gamma_app = 1
a1, a2 = sp.symbols("m1 m2", positive=True)
limit((a1 / a2) ** 2, "m1", a2, "1")
raise SystemExit(finish())
