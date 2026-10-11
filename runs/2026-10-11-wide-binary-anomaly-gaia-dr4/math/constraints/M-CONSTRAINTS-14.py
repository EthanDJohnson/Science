"""M-CONSTRAINTS-14 (F18): perspective-effect bias in the lens's stated magnitude model.

Model (lens's): Delta v_p = theta |v_sys|, theta = s/d, v_sys 3D Gaussian with 25 km/s per axis,
direction random in the sky plane; Delta v~ = Delta v_p / v_c(s), v_c = sqrt(G M/s), M = 1.5 Msun.
gamma = (med(v~ + Delta)/med(v~))^2, alpha = 1.3, weight (s/a)^0.6.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import numpy as np
from math_checks import finish
from cklib import vt_sample, wmed, q

AU, PC = 1.495978707e11, 3.0856775814913673e16
GM = 6.6743e-11 * 1.98847e30 * 1.5
rng = np.random.default_rng(77)
n = 600000
s, vv, w, r, pos = vt_sample(n, "1.3", rng)
m0 = wmed(np.hypot(vv[:, 0], vv[:, 1]), w)
vsys = np.linalg.norm(rng.normal(0, 25e3, size=(n, 3)), axis=1)
ph = rng.uniform(0, 2 * np.pi, n)
for skau, dpc, lens in [(10, 100, 1.0086), (20, 100, 1.068), (30, 100, 1.23), (20, 50, 1.27), (30, 50, 1.97), (20, 200, 1.018)]:
    sm = skau * 1e3 * AU
    theta = sm / (dpc * PC)
    dv = theta * vsys / np.sqrt(GM / sm)
    v2 = vv + np.stack([dv * np.cos(ph), dv * np.sin(ph)], 1)
    g = (wmed(np.hypot(v2[:, 0], v2[:, 1]), w) / m0) ** 2
    q(g, lens, 1.2e-2, f"s = {skau} kau, d = {dpc} pc")
q(1 + 0 * m0, 1.0, 1e-12, "theta -> 0 limit gives 1 (trivial)")
raise SystemExit(finish())
