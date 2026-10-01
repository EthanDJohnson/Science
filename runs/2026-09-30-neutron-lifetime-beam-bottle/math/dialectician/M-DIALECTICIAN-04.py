"""M-DIALECTICIAN-04: SM tau_beta = 2 pi^3 hbar / (G_F^2 m_e^5 f (1+delta_R') (1+Delta_R^V) Vud^2 (1+3 lambda^2)),
built from constants (not from the lens's tool). Literature inputs (taken as given): f = 1.6887, delta_R' = 0.014902,
Delta_R^V = 0.02479 (GS2023 pairing, per U-01 / statistician check), Vud = 0.97361(32). SI seconds; G_F, m_e in GeV."""
import sys
import math
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/dialectician")
from _common import *  # noqa

hbar = 6.582119569e-25      # GeV s
GF = 1.1663788e-5           # GeV^-2
me = 0.51099895e-3          # GeV
f, dRp, DRV = 1.6887, 0.014902, 0.02479
Vud, sVud = 0.97361, 0.00032
Kft = 2 * math.pi**3 * hbar * math.log(2) / me**5
print(f"K/(hbar c)^6 = {Kft/1e-10:.4f}e-10 GeV^-4 s (literature 8120.2776e-10)")
num("K", Kft, 8120.2776e-10, unit="", rel_tol=2e-5)
C = 2 * math.pi**3 * hbar / (GF**2 * me**5 * f * (1 + dRp))
print(f"tau*Vud^2*(1+3l^2)*(1+DRV) = {C:.2f} s (compare 5024.7 s); K_eff = {C/(1+DRV):.2f} s")
num("5024.7", C, 5024.7, rel_tol=1e-4)


def tau(lam, vud=Vud):
    return C / ((1 + DRV) * vud**2 * (1 + 3 * lam**2))


tP, tA = tau(1.27641), tau(1.2668)
print(f"PERKEO III lambda 1.27641: tau = {tP:.3f} s; aSPECT 2024 lambda 1.2668: {tA:.3f} s")
num("tau PERKEO III", tP, 878.50, abs_tol=0.1)
num("tau aSPECT", tA, 889.58, abs_tol=0.1)
# ratio is constant-free: tau_A/tau_P = (1+3 lP^2)/(1+3 lA^2)
num("ratio (constant-free)", tA / tP, (1 + 3 * 1.27641**2) / (1 + 3 * 1.2668**2), unit="", rel_tol=1e-12)
print(f"Difference {tA - tP:.2f} s; implied from ratio with lens's 878.50: {878.50*(1+3*1.27641**2)/(1+3*1.2668**2):.2f} s")
# errors
sP = math.hypot(tP * 6 * 1.27641 / (1 + 3 * 1.27641**2) * 0.00056, 2 * tP * sVud / Vud)
sA = math.hypot(tA * 6 * 1.2668 / (1 + 3 * 1.2668**2) * 0.0027, 2 * tA * sVud / Vud)
print(f"errors (lambda+Vud): PERKEO {sP:.2f} s (lens 0.88 with K error), aSPECT {sA:.2f} s (lens 3.20)")
# sensitivity identity and limit lambda -> 0
identity("diff(K/(V**2*(1 + 3*l**2)), l)", "-6*l*K/(V**2*(1 + 3*l**2)**2)", domain={"K": (4000, 6000), "V": (0.9, 1), "l": (1, 1.5)})
limit("K/(V**2*(1 + 3*l**2))", "l", 0, "K/V**2", domain={"K": (4000, 6000), "V": (0.9, 1)})
units("hbar/(GeV^-4 * GeV^5)", "dimensionless") if False else units("hbar/(1 GeV)", "time")
raise SystemExit(finish())
