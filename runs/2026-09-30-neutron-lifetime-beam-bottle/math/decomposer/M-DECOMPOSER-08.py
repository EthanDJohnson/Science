"""M-DECOMPOSER-08 (F7): 'worlds' A and B. Vud = sqrt(C / (tau (1+3 lam^2)(1+dRV))), errors from lambda, tau, dRV;
row sum Vud^2 + Vus^2 (Vub^2 ~ 1.6e-5 shown separately); comparison with superallowed 0.97361(32). SI (s)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/decomposer")
from math_checks import identity, finish
from _inputs import near, q, BL1, UCNT
from _sm import *

lA, sA = 1.27623, 0.00050   # A route (verified in M-07)
la, sa = LAM["aSPECT 2024"]
def world(tau, stau, lam, slam, C):
    v = vud_from(tau, lam, C=C)
    ev = v * q(3 * lam * slam / (1 + 3 * lam ** 2), 0.5 * stau / tau, 0.5 * DRV_E / (1 + DRV))
    zs = (v - VUD) / q(ev, VUD_E)
    row = v ** 2 + VUS ** 2; erow = q(2 * v * ev, 2 * VUS * VUS_E)
    return v, ev, zs, row, erow, (row - 1) / erow
for C in (C_GS, C_TAN):
    print(f"--- C = {C} s")
    res = {}
    for tag, tau, lam, sl in (("A: A-lam + UCNtau", UCNT, lA, sA), ("B: aSPECT + BL1", BL1, la, sa),
                              ("mixed: A-lam + BL1", BL1, lA, sA), ("mixed: aSPECT + UCNtau", UCNT, la, sa)):
        r = world(tau[0], tau[1], lam, sl, C); res[tag] = r
        print(f"{tag}: Vud {r[0]:.5f}({r[1]*1e5:.0f}e-5), {r[2]:+.2f} sigma vs superallowed; row {r[3]:.5f} +- {r[4]:.5f} ({r[5]:+.2f} sigma)")
    if C == C_TAN:
        A = res["A: A-lam + UCNtau"]; B = res["B: aSPECT + BL1"]
        M1 = res["mixed: A-lam + BL1"]; M2 = res["mixed: aSPECT + UCNtau"]
        near("World A Vud", A[0], 0.97410, 0.00003); near("World A error", A[1], 0.00037, 0.00001)
        near("World A z", A[2], 1.0, 0.1); near("World A row", A[3], 0.99919, 0.00005); near("World A row err", A[4], 0.00081, 0.00002)
        near("World B Vud", B[0], 0.97464, 0.00003); near("World B error", B[1], 0.00212, 0.00002)
        near("World B z", B[2], 0.5, 0.1); near("World B row", B[3], 1.0002, 0.0001); near("World B row err", B[4], 0.0042, 0.0001)
        near("mixed A-lam+beam Vud z", M1[2], -3.8, 0.1); near("mixed A-lam+beam row z", M1[5], -4.6, 0.1)
        near("mixed aSPECT+storage Vud z", M2[2], 3.7, 0.1)
print(f"Vub^2 (4e-3)^2 = {(4e-3)**2:.1e} (negligible)")
# identity: dVud/Vud = -(3 lam^2/(1+3 lam^2)) dlam/lam - dtau/(2 tau)
import sympy as sp
t, l, Cc = sp.symbols("t l Cc", positive=True)
Vexpr = sp.sqrt(Cc / (t * (1 + 3 * l ** 2)))
identity(sp.diff(Vexpr, l) / Vexpr, -3 * l / (1 + 3 * l ** 2))
identity(sp.diff(Vexpr, t) / Vexpr, -1 / (2 * t))
raise SystemExit(finish())
