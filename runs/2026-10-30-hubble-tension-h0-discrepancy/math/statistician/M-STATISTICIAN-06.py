"""M-STATISTICIAN-06: Sidak look-elsewhere: p_global = 1 - (1 - p_local)^N, z from two-sided p (F10, F17)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
import mpmath as mp
from _common import p2_of_z, z_of_p2, close
from math_checks import series, units, finish


def glob(z, n):
    p = p2_of_z(z)
    return z_of_p2(1 - (1 - p) ** n)


for z, claims in [(6.2709, (5.90, 5.72, 5.51)), (4.7976, (4.31, 4.06, 3.77)), (3.9384, (3.35, 3.03, 2.64))]:
    for n, cl in zip((10, 30, 100), claims):
        close(f"local z = {z}, N = {n}", glob(z, n), cl, 0.015)
close("DESI w0wa 4.2 sigma, N = 3", glob(4.2, 3), 3.9, 0.06)
series("1 - (1 - p)**n", "p", 0, 2, "n*p", domain={"n": (1, 100)})   # small-p limit: Bonferroni
units("1", "dimensionless")
raise SystemExit(finish())
