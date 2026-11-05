"""M-EMPIRICIST-09: precision a single one-step H0 needs to separate two values at k sigma.
Separating hypothesis H_true = 73.0 from reference 67.19 +- 0.38: need Δ/sqrt(σ^2 + σ_ref^2) >= k, so
σ <= sqrt((Δ/k)^2 - σ_ref^2). For 73 vs 70 (hypothesis values, no reference error): σ <= Δ/k.
Claims: 1.90 (2.6%) at 3σ, 1.10 (1.5%) at 5σ; 1.00 (1.4%) at 3σ, 0.60 (0.8%) at 5σ; km/s/Mpc.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
from math_checks import identity, limit, units, finish
from _common import cmp

identity("(d/sqrt((sqrt((d/k)**2 - r**2))**2 + r**2))", "k", domain={"d": (5, 10), "k": (1, 5), "r": (0, 0.5)})
limit("sqrt((d/k)**2 - r**2)", "r", 0, "d/k")
units("(((5.81 km/s/Mpc)/3)^2 - (0.38 km/s/Mpc)^2)^0.5", "km/s/Mpc")


def need(d, k, r):
    return ((d / k) ** 2 - r**2) ** 0.5


for (d, k, r, q, pct) in [(73.0 - 67.19, 3, 0.38, 1.90, 2.6), (73.0 - 67.19, 5, 0.38, 1.10, 1.5),
                          (3.0, 3, 0.0, 1.00, 1.4), (3.0, 5, 0.0, 0.60, 0.8)]:
    s = need(d, k, r)
    cmp(f"σ needed, Δ = {d:.2f}, {k}σ", s, q, 0.006, "km/s/Mpc")
    cmp(f"  as % of 73", 100 * s / 73.0, pct, 0.06)
raise SystemExit(finish())
