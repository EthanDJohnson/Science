"""M-CONSTRAINTS-11 (F13): statistical floor of a median-based gamma.

Asymptotic: sd(median) = 1/(2 p(m) sqrt N); gamma = (m/m0)^2 => sd(gamma) = 2 gamma sd(m)/m = gamma/(p m sqrt N).
Lens: p(m) = 1.40, m = 0.5125 (alpha = 1.3) -> 1.39 gamma/sqrt N; N = 341 -> 0.075; 6389 -> 0.017;
sigma 0.005 -> N = 77,600; 0.01 -> 19,400. Monte Carlo check at N = 3000 (lens 0.0254 analytic).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import numpy as np
from math_checks import identity, finish
from cklib import vt_sample, wmed, wquant, q

identity("2*g*(1/(2*p*sqrt(n)))/m", "g/(p*m*sqrt(n))", domain={"g": (1, 2), "p": (0.5, 2), "m": (0.3, 1), "n": (100, 1e5)})
rng = np.random.default_rng(66)
s, vv, w, r, pos = vt_sample(1500000, "1.3", rng)
vt = np.hypot(vv[:, 0], vv[:, 1])
m = wmed(vt, w)
h = 0.01
p = (wquant(vt, w, 0.5 + 0) * 0 + 1) * 0  # placeholder
lo, hi = m - h, m + h
p = w[(vt > lo) & (vt < hi)].sum() / w.sum() / (2 * h)
c = 1 / (p * m)
print(f"median {m:.4f}, pdf at median {p:.4f}, coefficient {c:.4f}")
q(p, 1.40, 1e-2, "pdf at median")
q(c, 1.39, 1e-2, "coefficient")
for N, lens in [(341, 0.075), (6389, 0.017), (3000, 0.0254)]:
    q(c / np.sqrt(N), lens, 3e-2, f"sd(gamma) at N = {N}")
q((c / 0.005) ** 2, 77600, 2e-2, "N for 0.005")
q((c / 0.01) ** 2, 19400, 2e-2, "N for 0.01")
# Monte Carlo: weighted resampling to an unweighted population, many subsamples of N = 3000
prob = w / w.sum()
est = []
for _ in range(1500):
    idx = rng.choice(len(vt), 3000, p=prob)
    est.append((np.median(vt[idx]) / m) ** 2)
sd = np.std(est)
print("MC sd(gamma) at N = 3000:", sd)
q(sd, c / np.sqrt(3000), 0.08, "MC vs asymptotic at N = 3000")
raise SystemExit(finish())
