"""M-EMPIRICIST-08: Sellke-Bayarri-Berger minimum Bayes factor B >= -e p ln p (for p < 1/e);
maximum odds against the null = 1/(-e p ln p). p is the two-sided Gaussian p-value of the stated tension.
Claims: 6.27σ -> ~4.7e7; 3.24σ -> ~45; 2.07σ -> ~2.9.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
import mpmath as mp
from math_checks import limit, inequality, finish
from _common import two_sided_gauss, cmp

# bound is <= 1 on (0, 1/e]: -e p ln p <= 1, with equality at p = 1/e
inequality("-E*p*log(p)", "<=", "1", domain={"p": (1e-9, 0.36787944)})
# vanishes as p -> 0
limit("-p*log(p)", "p", 0, "0", direction="+")


def odds(n):
    p = mp.mpf(two_sided_gauss(n))
    return float(1 / (-mp.e * p * mp.log(p))), float(p)


for n, q, tol in [(6.27, 4.7e7, 0.06e7), (3.24, 45, 1.0), (2.07, 2.9, 0.06)]:
    o, p = odds(n)
    print(f"  n = {n}: p = {p:.3g}")
    cmp(f"max odds at {n} sigma", o, q, tol)
o, p = odds(3.23)
print(f"  sensitivity: at 3.23 sigma (M-EMPIRICIST-04 recomputation) max odds = {o:.1f}")
raise SystemExit(finish())
