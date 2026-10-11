"""M-CONSTRAINTS-07 (F9): full vs truncated median under isotropic velocity kicks of a fraction f = 0.2.

Kick: 3D isotropic Delta v with |Delta v| = kappa v_c(s); its sky projection is added to the sky velocity,
so in normalised units v~_vec -> v~_vec + kappa * (u_x, u_y), u isotropic unit vector.
gamma_full = (med(mixed)/med(clean))^2; gamma_trunc = (med(mixed | v~ < c)/med(clean))^2, c = sqrt2 or 2.5.
Base orbit law alpha = 1.3 (lens base), weight (s/a)^0.6.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import numpy as np
from math_checks import finish
from cklib import vt_sample, wmed, q

rng = np.random.default_rng(33)
n = 800000
s, vv, w, r, pos = vt_sample(n, "1.3", rng)
vt0 = np.hypot(vv[:, 0], vv[:, 1])
m0 = wmed(vt0, w)
trip = rng.random(n) < 0.2
u = rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
lens = {0.3: (1.028, 1.027), 0.5: (1.073, 1.069), 0.75: (1.146, 1.131), 1.0: (1.221, 1.176),
        1.5: (1.318, 1.165), 2.0: (1.358, 1.093), 4.0: (1.391, 1.016)}
for k, (lf, lt) in lens.items():
    v2 = vv + np.where(trip[:, None], k * u[:, :2], 0.0)
    vt = np.hypot(v2[:, 0], v2[:, 1])
    gf = (wmed(vt, w) / m0) ** 2
    kp = vt < 2 ** 0.5
    gt = (wmed(vt[kp], w[kp]) / m0) ** 2
    q(gf, lf, 4e-3, f"kappa {k} full median")
    q(gt, lt, 4e-3, f"kappa {k} truncated < sqrt2")
    if k == 4.0:
        kp = vt < 2.5
        q((wmed(vt[kp], w[kp]) / m0) ** 2, 1.075, 4e-3, "kappa 4 truncated < 2.5")
# limit kappa -> 0
v2 = vv + np.where(trip[:, None], 1e-9 * u[:, :2], 0.0)
q((wmed(np.hypot(v2[:, 0], v2[:, 1]), w) / m0) ** 2, 1.0, 1e-6, "kappa -> 0 limit")
raise SystemExit(finish())
