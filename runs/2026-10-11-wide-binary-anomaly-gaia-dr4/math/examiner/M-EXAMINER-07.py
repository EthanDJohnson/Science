"""M-EXAMINER-07 (F5, R2, cand A, hardest-question 1): f_multi transfer.
Part 1, arithmetic on the lens's printed table (test zone 5-30 kau, Newton, median-v~ gamma_app vs f):
  f:     0     0.1    0.2    0.3    0.45   0.6
  g:   1.000  1.094  1.195  1.307  1.528  1.808     (calibration zone: 1.000 1.034 1.085 1.132 1.204 1.289)
  Mis-transfer with template f = 0.2: g(f_true)/g(0.2). R2: f needed in the wide zone for gamma_app = 1.37 (and 1.3-1.5)
  if the calibrated f is 0.2, by linear interpolation in the table.
Part 2, independent toy MC (my own model, not the run's generator): does the triple effect on the median v~
  grow with outer separation, and what is dgamma_app/df in each zone?
  Wide orbit: M_tot = 1.0 Msun, f(e) ∝ e^1.3, dN/da ∝ a^-1.6 on [150 au, 60 kau], random phase, isotropic.
  Triple: one component (0.6 Msun total, q = 0.5) is an inner circular binary, a_in log-uniform [0.1, 300] au,
  kept only if a_in < 0.3 r_out (stability); photocentre speed 0.27 sqrt(G 0.6 Msun / a_in), averaged over
  T = 2.83 yr: |<v>| = v |sin(pi T/P)/(pi T/P)|; random 3D direction, projected onto the sky. No noise, true masses.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, inequality, limit, sign, finish

f_tab = np.array([0, 0.1, 0.2, 0.3, 0.45, 0.6])
g_test = np.array([1.000, 1.094, 1.195, 1.307, 1.528, 1.808])
g_cal = np.array([1.000, 1.034, 1.085, 1.132, 1.204, 1.289])
for ft, want in ((0.45, 1.28), (0.6, 1.51), (0.0, 0.84)):
    v = np.interp(ft, f_tab, g_test) / 1.195
    print(f"mis-transfer f_true = {ft}: {v:.4f} (lens {want})")
    identity(sp.Float(round(v, 2)), sp.Float(want))
slopes = np.diff(g_test) / np.diff(f_tab)
print("local slopes dgamma/df (test zone):", np.round(slopes, 3))
print("local slopes dgamma/df (calibration zone):", np.round(np.diff(g_cal) / np.diff(f_tab), 3))
def f_needed(target, f_cal=0.2):
    return np.interp(target * np.interp(f_cal, f_tab, g_test), g_test, f_tab)
for tgt in (1.3, 1.37, 1.5):
    fn = f_needed(tgt)
    print(f"gamma_app = {tgt}: f_wide = {fn:.3f}, delta f = {fn - 0.2:.3f} (calibrated at 0.2)")
print(f"gamma_app = 1.37 with calibrated f = 0.1: delta f = {f_needed(1.37, 0.1) - 0.1:.3f}")
inequality(sp.Float(round(f_needed(1.37) - 0.2, 3)), ">", sp.Float(0.3))   # R2's "0.2-0.3" is low for 1.37

# ---------------- Part 2: toy MC
rng = np.random.default_rng(7)
G, Ms, au, yr = 6.6743e-11, 1.98892e30, 1.495978707e11, 3.15576e7
N = 1_200_000
amin, amax, p = 150.0, 60000.0, 1.6
u = rng.random(N)
a = (amin**(1 - p) + u * (amax**(1 - p) - amin**(1 - p)))**(1 / (1 - p))  # au
e = rng.random(N) ** (1 / 2.3)
M = rng.random(N) * 2 * np.pi
E = M.copy()
for _ in range(50):
    E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
r = a * (1 - e * np.cos(E))
fa = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
vscale = np.sqrt(G * Ms / (a * au * (1 - e**2)))            # m/s, M_tot = 1 Msun
pos = np.stack([r * np.cos(fa), r * np.sin(fa), np.zeros(N)], 1)
vel = vscale[:, None] * np.stack([-np.sin(fa), e + np.cos(fa), np.zeros(N)], 1)
nhat = rng.normal(size=(N, 3)); nhat /= np.linalg.norm(nhat, axis=1)[:, None]
def proj(X):
    return X - (X * nhat).sum(1)[:, None] * nhat
s = np.linalg.norm(proj(pos), axis=1)
vp_wide = proj(vel)
# triple perturbation candidates (assigned to all; switched on by f)
ain = 10 ** rng.uniform(-1, np.log10(300), N)
ok = ain < 0.3 * r
Pin = np.sqrt(ain**3 / 0.6) * yr
T = 2.83 * yr
x = np.pi * T / Pin
vin = 0.27 * np.sqrt(G * 0.6 * Ms / (ain * au)) * np.abs(np.sin(x) / x)
d3 = rng.normal(size=(N, 3)); d3 /= np.linalg.norm(d3, axis=1)[:, None]
dv = proj(vin[:, None] * d3) * ok[:, None]
draw = rng.random(N)
vc = np.sqrt(G * Ms / (s * au))
zones = {"300-700 au": (s > 300) & (s < 700), "5-30 kau": (s > 5000) & (s < 30000)}
out = {}
for zn, sel in zones.items():
    base = np.median(np.linalg.norm(vp_wide[sel], axis=1) / vc[sel])
    row = []
    for f in (0.1, 0.2, 0.3, 0.45):
        on = (draw < f)[:, None]
        vt = np.linalg.norm((vp_wide + dv * on)[sel], axis=1) / vc[sel]
        row.append((np.median(vt) / base) ** 2)
    out[zn] = row
    print(f"{zn}: n = {sel.sum()}, median v~(f=0) = {base:.4f}; gamma_app at f = 0.1/0.2/0.3/0.45: " +
          " / ".join(f"{g:.3f}" for g in row))
gc, gt = out["300-700 au"][1], out["5-30 kau"][1]
sign(sp.Float(gt - gc), "positive")         # zone contrast: effect larger at wide separation
sl = (out["5-30 kau"][2] - out["5-30 kau"][0]) / 0.2
print(f"toy dgamma/df in 5-30 kau (f 0.1 -> 0.3): {sl:.3f}")
limit(sp.Symbol("f") * 0 + 1, "f", 0, "1")    # f -> 0 gives gamma_app = 1 by construction (no perturbation)
raise SystemExit(finish())
