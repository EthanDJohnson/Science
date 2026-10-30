"""M-EMPIRICIST-03: inverse-variance weighted means (diagonal covariance) and their tension with CMB-SPA.
Mean = sum(x_i/s_i^2)/sum(1/s_i^2), sigma = (sum 1/s_i^2)^(-1/2); asymmetric errors symmetrised.
Claims: one-step (TDCOSMO, masers, sirens) 71.27 +- 1.93, 2.07σ; non-SH0ES (CCHP, SBF + one-step)
71.56 +- 1.19, 3.50σ; no-SN (SBF + one-step) 72.26 +- 1.51, 3.27σ.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
from math_checks import identity, limit, finish
from _common import H, gls, tension, cmp

# symbolic: two-point weighted mean; equal errors -> arithmetic mean; s2 -> oo -> x1
identity("(x1/s1**2 + x2/s2**2)/(1/s1**2 + 1/s2**2)", "(x1*s2**2 + x2*s1**2)/(s1**2 + s2**2)")
limit("(x1*s2**2 + x2*s1**2)/(s1**2 + s2**2)", "s2", "oo", "x1")

sets = {
    "one-step": (["TDCOSMO", "masers", "sirens"], 71.27, 1.93, 2.07),
    "non-SH0ES": (["CCHP", "SBF", "TDCOSMO", "masers", "sirens"], 71.56, 1.19, 3.50),
    "no-SN": (["SBF", "TDCOSMO", "masers", "sirens"], 72.26, 1.51, 3.27),
}
for k, (names, m, s, n) in sets.items():
    mu, sig = gls(names)
    cmp(f"{k} mean [km/s/Mpc]", mu, m, 0.006, "km/s/Mpc")
    cmp(f"{k} sigma [km/s/Mpc]", sig, s, 0.006, "km/s/Mpc")
    cmp(f"{k} tension vs CMB-SPA [sigma]", tension((mu, sig), H["CMB"]), n, 0.006)
raise SystemExit(finish())
