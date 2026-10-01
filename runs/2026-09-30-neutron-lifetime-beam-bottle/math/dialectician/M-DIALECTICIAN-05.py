"""M-DIALECTICIAN-05: Fierz synthesis. Total rate Gamma = Gamma_SM(lambda) (1 + b <m_e/E_e>), so
tau_F = tau_SM(lambda)/(1 + b x), x = <m_e/E_e> = 0.6553 (from M-03). Inputs (aSPECT 2024 combination, D-42/new):
|lambda| = 1.2724(13), b = -0.0181(65); PERKEO III |lambda| = 1.27641(56); aSPECT a = -0.10402(82).
Constants as in M-04 (K_eff built from 2 pi^3 hbar/(G_F^2 m_e^5 f(1+dR')(1+DRV))). SI seconds."""
import sys
import math
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/dialectician")
from _common import *  # noqa

hbar, GF, me = 6.582119569e-25, 1.1663788e-5, 0.51099895e-3
Keff = 2 * math.pi**3 * hbar / (GF**2 * me**5 * 1.6887 * 1.014902 * 1.02479)
Vud, sVud, sK = 0.97361, 0.00032, 0.19
x = 0.6553
tsm = lambda l: Keff / (Vud**2 * (1 + 3 * l**2))
lc, slc, bc, sbc = 1.2724, 0.0013, -0.0181, 0.0065
tF = tsm(lc) / (1 + bc * x)
print(f"K_eff = {Keff:.2f} s; tau_SM(1.2724) = {tsm(lc):.2f} s; tau_F = {tF:.2f} s")
num("tau_F", tF, 893.7, abs_tol=0.06)
dl = -tF * 6 * lc / (1 + 3 * lc**2)          # d tau / d|lambda|
db = -tF * x / (1 + bc * x)                   # d tau / d b
dV = 2 * tF * sVud / Vud
print(f"partials: dtau/dl*sl = {dl*slc:.3f} s, dtau/db*sb = {db*sbc:.3f} s, Vud {dV:.3f} s, K {sK} s")
errs = {}
for rho in (-0.8, 0.0, 0.8):
    v = (dl * slc) ** 2 + (db * sbc) ** 2 + 2 * rho * (dl * slc) * (db * sbc)
    errs[rho] = (math.sqrt(v), math.sqrt(v + dV**2 + sK**2))
    print(f"rho(|l|,b) = {rho:+.1f}: sigma = {errs[rho][0]:.2f} s (l,b only), {errs[rho][1]:.2f} s (+Vud,K)")
lo, hi = errs[-0.8][1], errs[0.8][1]
num("sigma low", lo, 2.8, abs_tol=0.1); num("sigma high", hi, 5.2, abs_tol=0.1)
JPup = q(JPst, JPup_sys)
for name, xv, sx, want in [("UCNtau", UCN, sUCN_up, (3.1, 5.6)), ("J-PARC", JP, JPup, (2.4, 3.2)), ("BL1", BL1, sBL1, (1.1, 1.7))]:
    zs = [(tF - xv) / q(s, sx) for s in (hi, lo)]
    print(f"tau_F vs {name}: {zs[0]:.2f}-{zs[1]:.2f} sigma (lens {want[0]}-{want[1]})")
    num(f"{name} low z", zs[0], want[0], unit="", abs_tol=0.06); num(f"{name} high z", zs[1], want[1], unit="", abs_tol=0.06)
# b needed with PERKEO III lambda
tP = tsm(1.27641)
for name, target, want in [("UCNtau", UCN, 0.0012), ("BL1", BL1, -0.0158)]:
    b = (tP / target - 1) / x
    print(f"b needed to match {name}: {b:+.5f} (tau_SM = {tP:.2f} s)")
    num(f"b for {name}", b, want, unit="", abs_tol=0.00006)
# a coefficient: a = (1 - l^2)/(1 + 3 l^2)
a = (1 - 1.27641**2) / (1 + 3 * 1.27641**2)
sa_P = 8 * 1.27641 / (1 + 3 * 1.27641**2) ** 2 * 0.00056
z_a = (-0.10402 - a) / 0.00082
z_a2 = (-0.10402 - a) / math.hypot(0.00082, sa_P)
print(f"a(PERKEO) = {a:.5f} (+- {sa_P:.5f}); aSPECT offset {z_a:.2f} sigma (aSPECT error only), {z_a2:.2f} (both); deficit {(a+0.10402)/a*100:.2f}%")
num("a", a, -0.10687, unit="", abs_tol=0.000006)
num("a tension", z_a, 3.48, unit="", abs_tol=0.006)
num("deficit %", (a + 0.10402) / a * 100, 2.7, unit="", abs_tol=0.05)
identity("diff((1 - l**2)/(1 + 3*l**2), l)", "-8*l/(1 + 3*l**2)**2", domain={"l": (1, 1.5)})
limit("T/(1 + b*x)", "b", 0, "T", domain={"T": (800, 900), "x": (0.5, 0.8)})
sign("T/(1 + b*x) - T", "positive", domain={"T": (800, 900), "x": (0.5, 0.8), "b": (-0.05, -0.001)})
units("893.7 s - 877.82 s", "time")
raise SystemExit(finish())
