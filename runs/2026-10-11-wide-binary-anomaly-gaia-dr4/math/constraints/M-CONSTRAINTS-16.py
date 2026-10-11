"""M-CONSTRAINTS-16 (F20, F21): quadratic-likelihood sigma from Delta lnL and tension arithmetic.

Gaussian likelihood: Delta lnL(gamma) = (gamma - g_hat)^2 / (2 sigma^2) => sigma = |gamma - g_hat| / sqrt(2 Delta lnL).
Tension t = (gamma_MOND - g_hat)/sigma; with systematic half-band b in quadrature: sqrt(sigma^2 + b^2).
Inputs quoted from the dossier (not checked here): g_hat = 1.05, Delta lnL(1.4) = 129, Delta lnL(1.0) = 4.8, b = 0.055.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
from math import sqrt
from math_checks import identity, finish
from cklib import q

identity("(g - h)**2/(2*(abs(g - h)/sqrt(2*L))**2)", "L", domain={"g": (1.1, 2), "h": (0.9, 1.05), "L": (0.1, 200)})
s1 = 0.35 / sqrt(2 * 129); s2 = 0.05 / sqrt(2 * 4.8)
q(s1, 0.0218, 3e-3, "sigma from DlnL(1.4)"); q(s2, 0.0161, 3e-3, "sigma from DlnL(1.0)")
st = sqrt(s1 ** 2 + 0.055 ** 2)
for gm, a, b in [(1.073, 1.1, 0.4), (1.167, 5.4, 2.0), (1.20, 6.9, 2.5), (1.30, 11.5, 4.2), (1.321, 12.4, 4.6), (1.393, 15.7, 5.8), (1.276, 10.0, 3.8)]:
    q((gm - 1.05) / s1, a, 0.05 if a > 1 else 0.1, f"{gm} stat"); q((gm - 1.05) / st, b, 0.06, f"{gm} with band")
for gm, want in [(1.42, 4.5), (1.25, 2.0), (1.07, 0.5)]:
    q((gm - 1.11) / 0.07, want, 0.05, f"deep bin 1.11 +- 0.07 vs {gm}")
raise SystemExit(finish())
