"""M-EMPIRICIST-05: adding the lensed SNe Refsdal 64.8 +4.4/-4.3 and H0pe 75.4 +8.1/-5.5 (symmetrised 4.35, 6.8).
Claims: one-step 70.53 +- 1.71 (1.91σ vs CMB-SPA); non-SH0ES 71.21 +- 1.13 (3.37σ). Diagonal GLS, km/s/Mpc.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
from math_checks import inequality, finish
from _common import H, gls, tension, cmp

# adding a measurement always shrinks the combined variance: 1/(W + w) < 1/W for W, w > 0
inequality("1/(W + w)", "<", "1/W")
sets = {
    "one-step + lensed SNe": (["TDCOSMO", "masers", "sirens", "Refsdal", "H0pe"], 70.53, 1.71, 1.91),
    "non-SH0ES + lensed SNe": (["CCHP", "SBF", "TDCOSMO", "masers", "sirens", "Refsdal", "H0pe"], 71.21, 1.13, 3.37),
}
for k, (names, m, s, n) in sets.items():
    mu, sig = gls(names)
    cmp(f"{k} mean", mu, m, 0.006, "km/s/Mpc")
    cmp(f"{k} sigma", sig, s, 0.006, "km/s/Mpc")
    cmp(f"{k} tension vs CMB-SPA [sigma]", tension((mu, sig), H["CMB"]), n, 0.006)
raise SystemExit(finish())
