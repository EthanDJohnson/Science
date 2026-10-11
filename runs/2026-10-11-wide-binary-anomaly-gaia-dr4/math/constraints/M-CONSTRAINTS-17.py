"""M-CONSTRAINTS-17 (F21): zone-averaged, median-inferred MOND gamma.

Population: dN/da ~ a^-1.6 (log-uniform draw in a over 100 au - 1e6 au, weight a^-0.6), alpha = 1.3 orbits,
M ~ U(1, 2) Msun, isotropic orientation; boost gamma(g_N(r)) = exact QUMOND sphere average
(M-CONSTRAINTS-03 method, g_ext = 1.785 a0), applied per pair as v~ -> sqrt(gamma) v~.
gamma_inferred(zone) = (med v~_MOND / med v~_N)^2 within the zone (selection on s, or on g_N(s) proxy).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import numpy as np
import mpmath as mp
from math_checks import finish
from cklib import kepler, wmed, q, ef_state, sphere_boost, A0

mp.mp.dps = 15
AU = 1.495978707e11; GMs = 1.32712440018e20
grid = np.arange(-13.0, -6.49, 0.125)
tab = {}
for name in ["simple", "standard"]:
    gNe = ef_state(name, mp.mpf("1.785"))[0]
    tab[name] = np.array([float(sphere_boost(name, mp.mpf(10) ** lg / A0, gNe)) for lg in grid])
rng = np.random.default_rng(99)
n = 1200000
pos, vel = kepler(n, "1.3", rng)
a = 10 ** rng.uniform(2, 6, n) * AU
wt = (a / AU) ** -0.6
M = rng.uniform(1, 2, n) * GMs
su = np.hypot(pos[:, 0], pos[:, 1]); ru = np.linalg.norm(pos, axis=1)
s = su * a; r = ru * a
vt = np.hypot(vel[:, 0], vel[:, 1]) * np.sqrt(su)   # v~ is scale-free
lgr = np.log10(M / r ** 2); lgs = np.log10(M / s ** 2)
zones = {"2-30 kau": (s > 2e3 * AU) & (s < 3e4 * AU), "5-30 kau": (s > 5e3 * AU) & (s < 3e4 * AU),
         "1-30 kau": (s > 1e3 * AU) & (s < 3e4 * AU), "bin (s proxy)": (lgs > -10.5) & (lgs < -9.5)}
lens = {"2-30 kau": (1.276, 1.048), "5-30 kau": (1.402, 1.073), "1-30 kau": (1.18, 1.031), "bin (s proxy)": (1.403, 1.074)}
for zn, m in zones.items():
    print(f"{zn}: N = {m.sum()}, median log g_N(r) = {np.median(lgr[m]):.2f}")
    for name, lv in zip(["simple", "standard"], lens[zn]):
        g = np.interp(lgr[m], grid, tab[name])
        gi = (wmed(np.sqrt(g) * vt[m], wt[m]) / wmed(vt[m], wt[m])) ** 2
        q(gi, lv, 6e-3, f"{zn} {name}")
q(np.median(lgr[zones["2-30 kau"]]), -9.69, 5e-3, "2-30 kau median log g_N (unweighted)")
raise SystemExit(finish())
