"""M-DIALECTICIAN-01: J-PARC 2024 tension with BL1 and UCNtau, quoted and with stat error inflated by S = sqrt(15.8/3).
Convention: z = |x - J| / sqrt(sigma_J(side facing x)^2 + sigma_x(side facing J)^2). SI, seconds."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/dialectician")
from _common import *  # noqa

S = math.sqrt(15.8 / 3)
print(f"S = {S:.4f}; inflated stat = {S*JPst:.3f} s")
num("S (dimensionless)", S, 2.29, unit="", abs_tol=0.006)
num("inflated stat", S * JPst, 3.90, abs_tol=0.006)


def tensions(st):
    up, dn = q(st, JPup_sys), q(st, JPdn_sys)
    z_bl1 = (BL1 - JP) / q(up, sBL1)                 # BL1 above J-PARC: J-PARC upper side
    z_ucn_right = (UCN - JP) / q(up, sUCN_dn)        # UCNtau above J-PARC: J-PARC upper side
    z_ucn_wrong = (UCN - JP) / q(dn, sUCN_up)        # lower side (the side facing away)
    return up, dn, z_bl1, z_ucn_right, z_ucn_wrong


for name, st in [("quoted", JPst), ("inflated", S * JPst)]:
    up, dn, zb, zu, zw = tensions(st)
    print(f"{name}: J-PARC total +{up:.3f}/-{dn:.3f} s; vs BL1 {zb:.3f} sigma; vs UCNtau {zu:.3f} sigma "
          f"(upper side, correct), {zw:.3f} sigma (lower side)")

up, dn, zb, zu, zw = tensions(JPst)
num("J-PARC vs BL1, quoted", zb, 2.15, unit="", abs_tol=0.006)
num("J-PARC vs UCNtau, quoted (facing side)", zu, 0.16, unit="", abs_tol=0.006)
up, dn, zb, zu, zw = tensions(S * JPst)
num("inflated J-PARC totals, upper", up, 5.59, abs_tol=0.006)
num("inflated J-PARC totals, lower", dn, 5.31, abs_tol=0.006)
num("J-PARC vs BL1, inflated", zb, 1.74, unit="", abs_tol=0.006)
num("J-PARC vs UCNtau, inflated (facing side)", zu, 0.12, unit="", abs_tol=0.006)

# Limit: as J-PARC's error -> infinity the tension -> 0
limit("d/sqrt(s**2 + t**2)", "s", "oo", "0", domain={"d": (0.1, 20), "t": (0.1, 5)})
# Units: a difference of lifetimes over a lifetime error is dimensionless
units("(887.7 s - 877.2 s)/(4.9 s)", "dimensionless")
# Stat-only chi2 of D-24 configurations (lens: 19.6/3, S = 2.55)
w = [1 / c[3] ** 2 for c in JCONF]
m = sum(wi * c[2] for wi, c in zip(w, JCONF)) / sum(w)
chi2 = sum(wi * (c[2] - m) ** 2 for wi, c in zip(w, JCONF))
print(f"stat-only mean {m:.3f} s, chi2 = {chi2:.3f}/3, S = {math.sqrt(chi2/3):.3f}")
num("stat-only chi2", chi2, 19.6, unit="", abs_tol=0.06)
num("stat-only S", math.sqrt(chi2 / 3), 2.55, unit="", abs_tol=0.006)
raise SystemExit(finish())
