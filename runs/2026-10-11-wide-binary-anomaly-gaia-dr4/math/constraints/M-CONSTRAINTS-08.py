"""M-CONSTRAINTS-08 (F10, F14): median bias from Gaussian per-axis noise sigma on v~ vs a noise-free template.

v~_vec_obs = v~_vec + sigma * N(0, I_2); gamma = (med(obs)/med(clean))^2; alpha = 1.3; weight (s/a)^0.6.
Small-sigma scaling: bias proportional to sigma^2 (checked by ratio at sigma = 0.05 vs 0.10).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import numpy as np
from math_checks import finish
from cklib import vt_sample, wmed, q

rng = np.random.default_rng(44)
n = 800000
s, vv, w, r, pos = vt_sample(n, "1.3", rng)
m0 = wmed(np.hypot(vv[:, 0], vv[:, 1]), w)
z = rng.normal(size=(n, 2))

def g(sig, trunc=None):
    v2 = vv + sig * z
    vt = np.hypot(v2[:, 0], v2[:, 1])
    if trunc:
        k = vt < trunc
        return (wmed(vt[k], w[k]) / m0) ** 2
    return (wmed(vt, w) / m0) ** 2

for sig, lens in [(0.05, 1.013), (0.10, 1.050), (0.15, 1.114), (0.20, 1.202), (0.30, 1.454)]:
    q(g(sig), lens, 4e-3, f"sigma {sig}")
q(g(0.20, 2 ** 0.5), 1.194, 4e-3, "sigma 0.20 truncated < sqrt2")
# F14 mapped values
for sig, lens in [(0.104, 1.055), (0.044, 1.009), (0.279, 1.39), (0.117, 1.07), (0.394, 1.79), (0.166, 1.14)]:
    q(g(sig), lens, 1e-2, f"F14 sigma {sig}")
# F10 'sigma ~ 0.27 alone would mimic 1.37'
q(g(0.27), 1.37, 1e-2, "sigma 0.27 -> 1.37")
# small-sigma scaling: (g(0.1)-1)/(g(0.05)-1) ~ 4
print("ratio of biases 0.10/0.05:", (g(0.10) - 1) / (g(0.05) - 1))
q(g(1e-6), 1.0, 1e-6, "sigma -> 0 limit")
raise SystemExit(finish())
