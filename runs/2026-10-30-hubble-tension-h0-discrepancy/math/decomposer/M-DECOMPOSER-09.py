"""M-DECOMPOSER-09: precision needed to separate two hypotheses, and naive counts (F9).

Separating H_a from H_b at k sigma with one measurement of error sigma: sigma <= |H_a - H_b|/k
(the hypotheses' own uncertainties neglected, as in the lens). Percent quoted against the midpoint.
1/sqrt(N) scaling: N = N0 (p0/p)^2.
"""
import sys
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/decomposer")
from _common import num, finish, limit, units, sym

cases = [(67.19, 73.264, 3, 2.0, 2.9), (67.19, 73.264, 5, 1.2, 1.7), (67.19, 71.0, 3, 1.27, 1.8),
         (67.19, 71.0, 5, 0.76, 1.1), (68.5, 71.0, 3, 0.83, 1.2)]
for a, b, k, sl, pl in cases:
    sg = (b - a) / k
    num(f"sigma for {a} vs {b} at {k} sigma", sg, sl, 0.03)
    num(f"  as % of midpoint {(a + b) / 2:.2f}", 100 * sg / ((a + b) / 2), pl, 0.06)
for p, nl in [(2.0, 30), (1.5, 53), (1.0, 120)]:
    num(f"lenses for {p}% from 3.3% with 11", 11 * (3.3 / p) ** 2, nl, 0.6)
num("GWTC-5.0 fractional error (symmetrised) %", 100 * sym(9.4, 7.5) / 71.7, 11.8, 0.06)
num("siren information factor for 2%", (11.8 / 2.0) ** 2, 35, 0.6)
# limit: N -> N0 when p -> p0
limit("N0*(p0/p)**2", "p", "oo", "0")
units("(73.264 km/s/Mpc - 67.19 km/s/Mpc)/3", "km/s/Mpc")
raise SystemExit(finish())
