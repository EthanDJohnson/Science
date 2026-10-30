"""M-EMPIRICIST-04: non-SH0ES mean with an NGC 4258 anchor term common to CCHP and SBF.
Model: covariance diag(s_i^2) plus an off-diagonal term (f*H_CCHP)(f*H_SBF), f = 0.015 (1.5% anchor), the
anchor error being already inside each total error. GLS mean and sigma. Claim: 71.47 +- 1.27, 3.24σ vs CMB-SPA.
Variants: off-diagonal f^2 * H_ref^2 with H_ref = 73 or the pair mean, to show sensitivity.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
import numpy as np
from math_checks import identity, inequality, finish
from _common import H, gls, tension, cmp

# symbolic: two-measurement GLS sigma^2 with correlation c = (s1^2 s2^2 - c^2)/(s1^2 + s2^2 - 2c); c -> 0 reduces
identity("(s1**2*s2**2 - c**2)/(s1**2 + s2**2 - 2*c)", "s1**2*s2**2/(s1**2+s2**2)", domain={"c": (0, 0)})
# positive correlation (c below min(s1^2, s2^2)) never decreases the combined variance
inequality("(s1**2*s2**2 - c**2)/(s1**2 + s2**2 - 2*c)", ">=", "s1**2*s2**2/(s1**2+s2**2)",
           domain={"s1": (1, 3), "s2": (1, 3), "c": (0, 0.9)})

names = ["CCHP", "SBF", "TDCOSMO", "masers", "sirens"]
f = 0.015
for label, offd in {"f^2*H_CCHP*H_SBF": f**2 * H["CCHP"][0] * H["SBF"][0],
                    "f^2*73^2": (f * 73) ** 2,
                    "f^2*mean^2": (f * (H["CCHP"][0] + H["SBF"][0]) / 2) ** 2}.items():
    cov = np.diag([H[n][1] ** 2 for n in names])
    cov[0, 1] = cov[1, 0] = offd
    mu, sig = gls(names, cov)
    print(f"  variant {label}: {mu:.3f} +- {sig:.3f}, {tension((mu, sig), H['CMB']):.3f} sigma")
# variant: anchor term added on top of the quoted total errors (not inside them)
covb = np.diag([H[n][1] ** 2 for n in names]); covb[0, 0] += (f*H["CCHP"][0])**2; covb[1, 1] += (f*H["SBF"][0])**2
covb[0, 1] = covb[1, 0] = f**2 * H["CCHP"][0] * H["SBF"][0]
mb, sb = gls(names, covb); print(f"  variant added-on-top: {mb:.3f} +- {sb:.3f}, {tension((mb, sb), H['CMB']):.3f} sigma")
print(f"  from rounded 71.47 +- 1.27: {tension((71.47, 1.27), H['CMB']):.3f} sigma")
cov = np.diag([H[n][1] ** 2 for n in names]); cov[0, 1] = cov[1, 0] = f**2 * H["CCHP"][0] * H["SBF"][0]
mu, sig = gls(names, cov)
cmp("correlated mean [km/s/Mpc]", mu, 71.47, 0.006, "km/s/Mpc")
cmp("correlated sigma [km/s/Mpc]", sig, 1.27, 0.006, "km/s/Mpc")
cmp("correlated tension vs CMB-SPA [sigma]", tension((mu, sig), H["CMB"]), 3.24, 0.006)
raise SystemExit(finish())
