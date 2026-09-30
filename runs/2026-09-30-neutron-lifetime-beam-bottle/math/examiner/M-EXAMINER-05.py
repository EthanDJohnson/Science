"""M-EXAMINER-05: SM tau_beta per lambda input (F9).
tau_beta = 2 pi^3 hbar / (G_F^2 m_e^5 f (1+delta_R') (1+DeltaR^V) Vud^2 (1+3 lambda^2))  (natural units, hbar converts to s)
Route (a): constants from scratch (G_F muon 1.1663788e-5 GeV^-2, m_e 0.51099895e-3 GeV, hbar 6.582119569e-25 GeV s,
           f = 1.6887, delta_R' = 0.014902 from D-49).
Route (b): literature K = 5024.7 s (Gorchtein-Seng, D-49) / (1+DeltaR^V).
DeltaR^V = 0.02479(21) (GS2023, D-48), Vud = 0.97361(32) (D-43), paired as in U-01. Errors: lambda, Vud, DeltaR^V in quadrature."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/examiner")
import sympy as sp
from math_checks import identity, limit, units, finish
from _inputs import *
from _h import cmp

GF, me, hbar, f, dRp = 1.1663788e-5, 0.51099895e-3, 6.582119569e-25, 1.6887, 0.014902
K0a = 2 * math.pi**3 / (GF**2 * me**5) * hbar / (f * (1 + dRp))
print(f"route (a) K0 = {K0a:.2f} s (literature 5024.7 / 5024.46 s; ratio {K0a/5024.7:.5f})")
units("1/((1.1663788e-5 GeV^-2)^2 * (0.51099895e-3 GeV)^5) * 6.582119569e-25 GeV*s", "s")

def tau(K0, lam, vud=VUD, drv=DRV):
    return K0 / ((1 + drv) * vud**2 * (1 + 3 * lam**2))

def err(K0, lam, slam):
    t = tau(K0, lam)
    e_l = t * 6 * lam / (1 + 3 * lam**2) * slam
    e_v = t * 2 * SVUD / VUD
    e_r = t * SDRV / (1 + DRV)
    return t, math.sqrt(e_l**2 + e_v**2 + e_r**2), e_l, e_v, e_r

claims = {"PERKEO III": (878.50, 0.88), "UCNA": (877.60, 2.36), "PERKEO II": (880.34, 1.35),
          "PDG 2024": (879.65, 1.61), "aSPECT 2024": (889.58, 3.20), "aCORN": (874.86, 7.07)}
for k, (lam, sl) in LAM.items():
    ta, sa, *_ = err(K0a, lam, sl)
    tb, sb, el, ev, er = err(5024.7, lam, sl)
    print(f"{k}: |lambda| {lam}({sl:.5f}): (a) {ta:.2f} +- {sa:.2f} s; (b) {tb:.2f} +- {sb:.2f} s [lam {el:.2f}, Vud {ev:.2f}, RC {er:.2f}]")
    c, ce = claims[k]
    cmp(f"{k} tau_beta (route a)", ta, c, 0.006, "s")
    cmp(f"{k} sigma", sb, ce, 0.01, "s")

tP, sP, *_ = err(K0a, *LAM["PERKEO III"])
tA, sA, *_ = err(K0a, *LAM["aSPECT 2024"])
tD, sD, *_ = err(K0a, *LAM["PDG 2024"])
sU_up = q(U_STAT, U_UP)
zs = {"PERKEO III vs BL1": ((BL1[0] - tP) / q(sP, BL1[1]), 3.81),
      "PERKEO III vs UCNtau": ((tP - U_X) / q(sP, sU_up), 0.73),
      "PDG vs BL1": ((BL1[0] - tD) / q(sD, BL1[1]), 2.91),
      "aSPECT vs BL1": ((tA - BL1[0]) / q(sA, BL1[1]), 0.48),
      "aSPECT vs UCNtau": ((tA - U_X) / q(sA, sU_up), 3.66)}
for k, (z, c) in zs.items():
    cmp(k, z, c, 0.015)
ta_P = tau(K0a, LAM["PERKEO III"][0])
print(f"route (a) PERKEO III tau = {ta_P:.2f} s -> {(BL1[0]-ta_P)/q(sP, BL1[1]):.2f} sigma from BL1")

# lambda implied by a lifetime: 1 + 3 lam^2 = K/((1+DRV) Vud^2 tau)
for lab, t, c in (("BL1", BL1[0], 1.2684), ("UCNtau", U_X, 1.2770)):
    lb = math.sqrt((5024.7 / ((1 + DRV) * VUD**2 * t) - 1) / 3)
    la = math.sqrt((K0a / ((1 + DRV) * VUD**2 * t) - 1) / 3)
    print(f"lambda implied by {lab}: (b) {lb:.5f}; (a) {la:.5f}")
    cmp(f"lambda from {lab}", lb, c, 0.00006)

# PERKEO III vs aSPECT 2024 in lambda
zl = (LAM["PERKEO III"][0] - LAM["aSPECT 2024"][0]) / q(LAM["PERKEO III"][1], LAM["aSPECT 2024"][1])
cmp("PERKEO III vs aSPECT lambda z", zl, 3.49, 0.005)

# symbolic: sensitivity and limit
K, V, l = sp.symbols("K V l", positive=True)
T = K / (V**2 * (1 + 3 * l**2))
identity(sp.diff(T, l) / T, -6 * l / (1 + 3 * l**2))
identity(sp.diff(T, V) / T, -2 / V)
limit(T, "l", 0, K / V**2)  # pure Fermi limit
raise SystemExit(finish())
