"""M-EMPIRICIST-02: pairwise tensions, uncorrelated Gaussian, two-sided.
n = |H_a - H_b| / sqrt(sigma_a^2 + sigma_b^2), H in km/s/Mpc, sigma > 0.
For asymmetric errors two conventions are checked: (i) symmetrised (mean of up and down),
(ii) directional (the error on the side facing the other value).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
from math_checks import identity, limit, units, finish
from _common import H, tension, cmp

# symbolic: tension of a vs b equals that of b vs a; when sigma_b -> 0 it reduces to |Δ|/sigma_a
identity("(a-b)**2/(sa**2+sb**2)", "(b-a)**2/(sb**2+sa**2)", domain={"a": (60, 80), "b": (60, 80)})
limit("d/sqrt(sa**2+sb**2)", "sb", 0, "d/sa")
units("(73.49 km/s/Mpc - 67.19 km/s/Mpc)/((0.93 km/s/Mpc)^2 + (0.38 km/s/Mpc)^2)^0.5", "dimensionless")

cmb = H["CMB"]
directional = {"TDCOSMO": (71.1, 2.3), "sirens": (71.7, 7.5)}   # lower errors face the CMB value
quoted = {"SH0ES": 6.27, "CCHP": 1.62, "SBF": 2.72, "TDCOSMO": 1.68, "masers": 1.19, "sirens": 0.60}
for k, q in quoted.items():
    sym = tension(H[k], cmb)
    print(f"  {k}: symmetrised {sym:.3f}, directional {tension(directional.get(k, H[k]), cmb):.3f}")
    cmp(f"{k} vs CMB-SPA (directional/lens convention) [sigma]", tension(directional.get(k, H[k]), cmb), q, 0.006)
cmp("SH0ES vs CCHP [sigma]", tension(H["SH0ES"], H["CCHP"]), 1.44, 0.006)
cmp("non-SH0ES mean 71.56+-1.19 vs BAO+BBN [sigma]", tension((71.56, 1.19), H["BAOBBN"]), 2.31, 0.006)
cmp("correlated mean 71.47+-1.27 vs BAO+BBN [sigma] (lower end of '2.1-2.3')", tension((71.47, 1.27), H["BAOBBN"]), 2.1, 0.05)
raise SystemExit(finish())
