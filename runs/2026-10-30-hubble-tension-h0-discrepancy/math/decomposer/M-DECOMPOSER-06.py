"""M-DECOMPOSER-06: error inflation the null needs (F6).

(a) sigma_L needed so that D / sqrt(sigma_L^2 + s_E^2) = k: sigma_L = sqrt((D/k)^2 - s_E^2),
    D = 73.264 - 67.19, s_E = 0.38 km/s/Mpc; inflation = sigma_L / 0.806.
(b) Ten-result set with chosen errors scaled: one-mean chi2 (9 dof), p, and the common mean.
    "Ladder" is ambiguous in the lens text; both readings are evaluated.
"""
import sys
import math
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/decomposer")
from _common import TEN, EARLY, LOCAL, wmean, chi2_about_mean, chi2_sf, num, finish, limit, units, identity

D, sE, sL0 = 73.264 - 67.19, 0.38, 0.806
for k, sl_l, fac_l in [(3, 1.99, 2.5), (2, None, 3.7)]:
    sl = math.sqrt((D / k) ** 2 - sE ** 2)
    if sl_l:
        num(f"sigma_L for {k} sigma", sl, sl_l, 0.006)
    num(f"inflation factor for {k} sigma", sl / sL0, fac_l, 0.06)
num("inflation for 3 sigma, 3 s.f. (Calculations: x2.47)", math.sqrt((D / 3) ** 2 - sE ** 2) / sL0, 2.47, 0.006)


def scaled(names, f):
    return [(x, s * f) if n in names else (x, s) for n, (x, s) in TEN.items()]


for label, grp in [("ladders = SH0ES, CCHP, SBF", ["SH0ES", "CCHP", "SBF"]),
                   ("ladders = all six local", LOCAL),
                   ("ladders = SH0ES, CCHP", ["SH0ES", "CCHP"])]:
    it = scaled(grp, 2.5)
    c = chi2_about_mean(it)
    m, _ = wmean(it)
    print(f"  {label} x2.5: mean {m:.3f}, chi2 {c:.3f}/9, p {chi2_sf(c, 9):.4f}")
it = scaled(["SH0ES", "CCHP", "SBF"], 2.5)
num("ladder x2.5 chi2", chi2_about_mean(it), 16.3, 0.06)
num("ladder x2.5 p", chi2_sf(chi2_about_mean(it), 9), 0.06, 0.006)
num("ladder x2.5 common H0", wmean(it)[0], 67.9, 0.06)
it = scaled(EARLY, 3.0)
c = chi2_about_mean(it)
print(f"  early x3 (all four early): mean {wmean(it)[0]:.3f}, chi2 {c:.3f}/9, p {chi2_sf(c, 9):.5f}")
for lab, grp in [("CMB, BAO+BBN", ["CMB", "BAOBBN"]), ("CMB, BAO+BBN, r_s-free", ["CMB", "BAOBBN", "RSFREE"]),
                 ("CMB only", ["CMB"])]:
    itx = scaled(grp, 3.0)
    cx = chi2_about_mean(itx)
    print(f"  early x3 [{lab}]: mean {wmean(itx)[0]:.3f}, chi2 {cx:.3f}/9, p {chi2_sf(cx, 9):.5f}")
itq = scaled(["CMB", "BAOBBN"], 3.0)
num("early x3 p, reading 'CMB and BAO+BBN' (Q3b wording)", chi2_sf(chi2_about_mean(itq), 9), 0.004, 0.0006)
# Robust conclusion: inflating early errors x3 still leaves p < 0.01 under every reading
from _common import inequality
inequality(f"{chi2_sf(c, 9)!r}", "<", "0.01")
inequality(f"{chi2_sf(chi2_about_mean(itq), 9)!r}", "<", "0.01")

limit("sqrt((D/k)**2 - s**2)", "s", 0, "D/k")
identity("D/sqrt(sqrt((D/k)**2 - s**2)**2 + s**2)", "k", domain={"D": (5, 7), "k": (1, 3), "s": (0.1, 0.5)})
units("((6.074 km/s/Mpc / 3)^2 - (0.38 km/s/Mpc)^2)^0.5", "km/s/Mpc")
raise SystemExit(finish())
