"""M-CONSTRAINTS-15 (F19): EF-alignment contrast with the per-pair instantaneous EF-limit boost.

eta(theta) = nu_e (1 + K sin^2 theta / 2), theta = angle between 3D separation and EF; v~_obs = sqrt(eta) v~_N.
EF in the sky plane (x axis): split by phi = angle between projected separation and x:
aligned |phi| < 30 deg, perpendicular |phi| > 60 deg. gamma_group = (med_group/med_Newton)^2.
Significance: sd per group = c gamma / sqrt(N/3), c = 1/(p m) from M-CONSTRAINTS-11 (1.42).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import numpy as np
import mpmath as mp
from math_checks import finish
from cklib import vt_sample, wmed, q, ef_state

ye, nue, K = [float(v) for v in ef_state("simple", mp.mpf("1.785"))]
rng = np.random.default_rng(88)
n = 1500000
s, vv, w, r, pos = vt_sample(n, "1.3", rng)
vt = np.hypot(vv[:, 0], vv[:, 1])
m0 = wmed(vt, w)
u = pos / r[:, None]
def gam(ef_axis, mask=None):
    c = u[:, ef_axis]
    eta = nue * (1 + K * (1 - c * c) / 2)
    v = np.sqrt(eta) * vt
    if mask is None:
        return (wmed(v, w) / m0) ** 2
    return (wmed(v[mask], w[mask]) / m0) ** 2
# isotropic EF direction: average over three axes ~ angle average
q(np.mean([gam(0), gam(1), gam(2)]), 1.4229, 2e-3, "axis-averaged")
q(gam(0), 1.4267, 2e-3, "EF in sky plane, all pairs")
q(gam(2), 1.4117, 2e-3, "EF along line of sight")
cphi = np.abs(pos[:, 0]) / np.hypot(pos[:, 0], pos[:, 1])
al = cphi > np.cos(np.radians(30))
pe = cphi < np.cos(np.radians(60))
ga, gp = gam(0, al), gam(0, pe)
q(ga, 1.487, 3e-3, "aligned within 30 deg")
q(gp, 1.368, 3e-3, "more than 60 deg")
q(ga - gp, 0.12, 0.06, "contrast")
c = 1.42
for N, lens in [(3000, 1.4), (10000, 2.5), (30000, 4.3)]:
    sd = np.hypot(c * ga / np.sqrt(N / 3), c * gp / np.sqrt(N / 3))
    q((ga - gp) / sd, lens, 0.06, f"significance N = {N}")
# Newton limit: nu_e = 1, K = 0 gives zero contrast by isotropy
gN_a = (wmed(vt[al], w[al]) / m0) ** 2; gN_p = (wmed(vt[pe], w[pe]) / m0) ** 2
q(1 + gN_a - gN_p, 1.0, 3e-3, "Newton contrast ~ 0 (1 + contrast)")
raise SystemExit(finish())
