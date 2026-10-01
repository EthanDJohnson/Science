"""M-DECOMPOSER-07 (U-01 as used in L7/L11/Q6a; F7, F12): Delta_R^V cancellation and SM tau_beta by lambda.
Superallowed: Vud^2 = K0 / (Ft (1 + dRV)). Neutron: tau (1 + 3 lam^2) = Kn / (Vud^2 (1 + dRV)) (with f, delta_R'
absorbed into Kn). Errors: lambda |dtau/dlam| s_lam, Vud 2 tau s_V/V, RC tau s_dR/(1+dR), in quadrature. SI (s)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/decomposer")
import sympy as sp
from math_checks import identity, limit, units, finish
from _inputs import near, q, BL1, UCNT
from _sm import *

# (1) cancellation, symbolic
K0, Kn, Ft, dR, lam = sp.symbols("K0 Kn Ft dR lam", positive=True)
V2 = K0 / (Ft * (1 + dR))
tau = Kn / (V2 * (1 + 3 * lam ** 2) * (1 + dR))
identity(sp.diff(tau, dR), sp.Integer(0))
identity(tau, Kn * Ft / (K0 * (1 + 3 * lam ** 2)))
limit("C/(v**2*(1+3*l**2))", "l", 0, "C/v**2")   # lambda -> 0: pure Fermi rate
units("5024.7 s", "s")
# numeric pairing consistency: tau(1+3 lam^2) for each paired (C, dRV, Vud)
for tag, C, drv, v in (("GS2023", C_GS, 0.02479, 0.97361), ("Tan/AVG2020", C_TAN, 0.02454, 0.97373)):
    print(f"{tag}: tau(1+3lam^2) = {C/(v**2*(1+drv)):.2f} s (CMS 2018 with its own Vud 0.97420: 5172.0(1.1) s)")
# mixed pairing of D-50: K = 4908.6 s (CMS, RC inside) with Vud 0.97367
lP = LAM["PERKEO III"][0]
mixed = 4908.6 / (0.97367 ** 2 * (1 + 3 * lP ** 2))
print(f"D-50 mixed pairing PERKEO III: {mixed:.2f} s")
# (2) SM tau_beta by lambda
def tb_err(lam, sl, C):
    t = tau_beta(lam, C=C)
    el = abs(dtau_dlam(lam, t)) * sl; ev = 2 * t * VUD_E / VUD; er = t * DRV_E / (1 + DRV)
    return t, q(el, ev, er), el, ev, er
for C in (C_GS, C_TAN):
    t, e, el, ev, er = tb_err(lP, LAM["PERKEO III"][1], C)
    print(f"C={C}: PERKEO III tau_beta {t:.3f} +- {e:.3f} (lam {el:.3f}, Vud {ev:.3f}, RC {er:.3f})")
t_P, e_P, *_ = tb_err(lP, LAM["PERKEO III"][1], C_TAN)
near("PERKEO III tau_beta (Tan C)", t_P, 878.50, 0.02); near("PERKEO III error", e_P, 0.88, 0.02)
near("D-50 mixed-pairing offset (+0.91 s)", mixed - t_P, 0.91, 0.02)
# A route combination of PERKEO III, UCNA, PERKEO II
ws = [1 / LAM[k][1] ** 2 for k in ("PERKEO III", "UCNA", "PERKEO II")]
xs = [LAM[k][0] for k in ("PERKEO III", "UCNA", "PERKEO II")]
lA = sum(w * x for w, x in zip(ws, xs)) / sum(ws); sA = 1 / math.sqrt(sum(ws))
c2A = sum(w * (x - lA) ** 2 for w, x in zip(ws, xs))
print(f"A route lambda {lA:.5f} +- {sA:.5f}, chi2 {c2A:.3f}/2")
near("A-route lambda", lA, 1.27623, 0.00001); near("A-route sigma", sA, 0.00050, 0.000005)
near("A-route chi2 (F7: 1.51)", c2A, 1.51, 0.01); near("A-route chi2 (ledger L8: 2.14)", c2A, 2.14, 0.01)
t_A, e_A, *_ = tb_err(lA, sA, C_TAN)
la, sa = LAM["aSPECT 2024"]
t_a, e_a, *_ = tb_err(la, sa, C_TAN)
print(f"A route tau_beta {t_A:.3f} +- {e_A:.3f}; aSPECT {t_a:.3f} +- {e_a:.3f}; difference {t_a-t_A:.3f} s")
near("A-route tau_beta", t_A, 878.70, 0.03); near("A-route error", e_A, 0.83, 0.02)
near("aSPECT tau_beta", t_a, 889.58, 0.03); near("aSPECT error", e_a, 3.20, 0.02)
near("Delta tau for Delta lambda (10.8 s)", t_a - t_A, 10.8, 0.1)
dl = lA - la; zl = dl / q(sA, sa); zlP = (lP - la) / q(LAM["PERKEO III"][1], sa)
print(f"Delta lambda {dl:.5f}, A-route vs aSPECT {zl:.3f} sigma; PERKEO III vs aSPECT {zlP:.3f}")
near("Delta lambda", dl, 0.0094, 0.00005); near("split z (3.4)", zl, 3.4, 0.05)
# F12 tensions
zA = (BL1[0] - t_A) / q(BL1[1], e_A); za = (t_a - UCNT[0]) / q(e_a, UCNT[1])
print(f"A route vs BL1 {zA:.3f} sigma; a route vs UCNtau {za:.3f} sigma")
near("A-route vs BL1", zA, 3.75, 0.02); near("a-route vs UCNtau", za, 3.7, 0.05)
raise SystemExit(finish())
