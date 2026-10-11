"""M-DIALECTICIAN-02 (F7): with r >= s (projection never lengthens a separation), a pair with
v3D^2 > 2 G M / s has v3D^2 > 2 G M / r, i.e. positive Newtonian energy, whatever deprojection is used.
Equivalently v~ <= sqrt(2 gamma) for every bound pair. Also: a bound-only likelihood must explain such a pair by
gamma > v3D^2 s / (2 G M) > 1 (or a larger mass)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/dialectician")
import numpy as np
import sympy as sp
from math_checks import inequality, sign, identity, quantity, units, finish
from kep import sample_e, kepler_vtilde

GM, s, k, w, v2, gam = sp.symbols("GM s k w v2 gam", positive=True)
r = s * (1 + k)                         # r = s(1+k), k >= 0
# escape speed squared at r is 2GM/r <= 2GM/s
inequality(2 * GM / s, ">=", 2 * GM / r, domain={"GM": (0.1, 10), "s": (0.1, 10), "k": (0, 50)})
# if v2 = 2GM/s (1 + w), w > 0, then specific energy v2/2 - GM/r > 0 for every k >= 0
E = (2 * GM / s * (1 + w)) / 2 - GM / r
sign(E, "positive", domain={"GM": (0.1, 10), "s": (0.1, 10), "k": (0, 50), "w": (1e-6, 5)})
# bound under gamma G requires gamma > v2 r/(2GM) >= v2 s/(2GM) = 1 + w > 1
sign((2 * GM / s * (1 + w)) * r / (2 * GM) - 1, "positive", domain={"GM": (0.1, 10), "s": (0.1, 10), "k": (0, 50), "w": (1e-6, 5)})
# limit: at k = 0 (pair in sky plane) the bound is attained: energy = GM w / s
identity(E.subs(k, 0), GM * w / s)

# Monte Carlo: Kepler orbits with gamma = 1 and 1.4, max of v~ / sqrt(2 gamma) and max of v3D^2 s/(2 gamma GM)
rng = np.random.default_rng(5)
for gm in (1.0, 1.4):
    vt, ss, rr, v3 = kepler_vtilde(200000, sample_e(200000, "thermal", rng), rng, gm, return_all=True)
    m1 = vt.max() / np.sqrt(2 * gm)
    m2 = (v3 ** 2 * ss / (2 * gm)).max()
    print(f"gamma={gm}: max v~/sqrt(2 gamma) = {m1:.6f}; max v3D^2 s/(2 gamma GM) = {m2:.6f}")
    quantity(f"{min(m1, 1.0)}", f"{m1}", rel_tol=1e-12)   # passes only if m1 <= 1
    quantity(f"{min(m2, 1.0)}", f"{m2}", rel_tol=1e-12)
units("(1 km/s)^2 * 1.5e15 m / (6.674e-11 m^3/(kg s^2) * 2e30 kg)", "dimensionless")
raise SystemExit(finish())
