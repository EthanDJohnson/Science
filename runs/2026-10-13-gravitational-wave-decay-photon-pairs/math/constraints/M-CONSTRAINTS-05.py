"""M-CONSTRAINTS-05/06/07/14: GW150914 numbers, conversion fraction, overcount, depletion. SI units.
Inputs (lens, B&O): f = 150 Hz, w = 2 pi f, sigma = 1/t_m = 200 s^-1, E = 2 or 3 Msun c^2, T_CMB = 2.7255 K,
eps = 0.1, t_H = 4.36e17 s, D_L = 410 Mpc, calibration 11.29 %, FIRAS 6e-5, N_eff ratio 0.068.
Independent formulas (derived in M-CONSTRAINTS-04): rate = 3 G^2 E^2 w sigma^2/(25 pi c^10),
W = 2 hbar w rate, L_GW = E sigma, W/L = (6/(25 pi)) (L/L_P) (hbar w/E_P)^2, L_P = c^5/G, E_P = sqrt(hbar c^5/G).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, finish

G, c, hbar, kB, eV = 6.67430e-11, 299792458.0, 1.054571817e-34, 1.380649e-23, 1.602176634e-19
Msun = 1.98841e30
Mpc = 3.0856775814913673e22
LP = c**5 / G
EP = math.sqrt(hbar * c**5 / G)
print("L_P =", LP, "W ; E_P =", EP / eV, "eV")

# symbolic: W/L identity
Gs, E, w, sg, cs, hb = sp.symbols("G E omega sigma c hbar", positive=True)
W = 6 * Gs**2 * hb * E**2 * w**2 * sg**2 / (25 * sp.pi * cs**10)
L = E * sg
identity(W / L, sp.Rational(6, 25) / sp.pi * (L / (cs**5 / Gs)) * (hb * w)**2 / (hb * cs**5 / Gs))

w = 2 * math.pi * 150.0
sig = 200.0
fCMB = kB * 2.7255 / (hbar * w)
print("1 + 2f at 150 Hz:", 1 + 2 * fCMB)
quantity(f"{1+2*fCMB}", "7.6e8", rel_tol=0.01)
res = {}
for Em, want_p, want_C in [(2, 7.0e-7, 3.9e-85), (3, 1.6e-6, 5.8e-85)]:
    E_ = Em * Msun * c**2
    rate = 3 * G**2 * E_**2 * w * sig**2 / (25 * math.pi * c**10)
    pairs = rate / sig
    rm_l = (2 * G * E_ / c**4) * sig / c
    Wg = 2 * hbar * w * rate
    Lg = E_ * sig
    C = Wg / Lg
    print(f"E={Em} Msun c^2: pairs/burst={pairs:.3e}, r_m/l={rm_l:.3e}, stimulated pairs={pairs*(1+2*fCMB):.3e}, W/L={C:.3e}")
    quantity(f"{pairs}", f"{want_p}", rel_tol=0.05)
    quantity(f"{C}", f"{want_C}", rel_tol=0.05)
    res[Em] = (E_, Wg, C)
quantity(f"{(2*G*2*Msun/c**2)*sig/c}", "3.9e-3", rel_tol=0.03)
quantity(f"{7.0e-7*(1+2*fCMB)}", "5.3e2", rel_tol=0.03)

# threshold conversion and required hbar w at L = L_P
thr = 6e-5 / 0.068
print("threshold conversion:", thr)
quantity(f"{thr}", "8.8e-4", rel_tol=0.01)
x = math.sqrt(thr * 25 * math.pi / 6)
print("hbar w / E_P needed at L = L_P:", x, " =", x * EP / eV, "eV")
quantity(f"{x}", "0.11", rel_tol=0.05)
# stimulated version: (12/(25 pi)) (L/L_P) hbar w kT / E_P^2 = thr
for z, want in [(3e6, 1e51), (1e3, 3.6e54)]:
    kT = 8.617333e-5 * 2.7255 * (1 + z)   # eV
    hw = thr * 25 * math.pi * (EP / eV)**2 / (12 * kT)
    print(f"z={z}: kT={kT:.3g} eV, needed hbar w={hw:.3e} eV (>> kT, RJ violated)")
    quantity(f"{hw}", f"{want}", rel_tol=0.3)

# F10 overcount X = eps w t_H, energy corner
tH = 4.36e17
for EeV, want in [(1e-10, 6.6e21), (10, 6.6e32), (2.2e6, 1.5e38), (1e10, 6.6e41)]:
    X = 0.1 * EeV * eV / hbar * tH
    print(f"{EeV} eV: X={X:.3e}, sqrt X={math.sqrt(X):.2e}")
    quantity(f"{X}", f"{want}", rel_tol=0.03)
def conv(EeV, LoverLP): return 6 / (25 * math.pi) * LoverLP * (EeV * eV / EP)**2
CX = conv(1e10, 1e-3) * 0.1 * 1e10 * eV / hbar * tH
CXh = conv(1e9, 0.5) * 0.1 * 1e9 * eV / hbar * tH
print("C x X at 1e10 eV (L=1e-3 L_P):", CX, "; tau_h/t_H =", 1 / CX, "; hoop at 1e9 eV:", CXh)
quantity(f"{CX}", "34", rel_tol=0.05)
quantity(f"{CXh}", "17", rel_tol=0.05)
quantity(f"{conv(1e10,1e-3)}", "5e-41", rel_tol=0.05)
# hoop: r_m = l <=> E sigma = c^5/(2G) = L_P/2
Gs2, Es, ss, cs2 = sp.symbols("G E sigma c", positive=True)
sol = sp.solve(sp.Eq(2 * Gs2 * Es / cs2**4, cs2 / ss), Es)[0]
identity(sol * ss, cs2**5 / (2 * Gs2))
# EBL: conversion at 10 eV and deposited energy
quantity(f"{conv(10,1e-3)}", "5.1e-59", rel_tol=0.03)
quantity(f"{conv(10,0.5)}", "2.6e-56", rel_tol=0.03)
dep = 7.67e-10 * conv(10, 0.5)
print("deposit:", dep, "J/m^3 ; /rho_CMB:", dep / 4.1748e-14)
quantity(f"{dep}", "2e-65", rel_tol=0.05)
quantity(f"{conv(150*2*math.pi*hbar/eV, 1e-3)*(1+2*fCMB)}", "1.5e-76", rel_tol=0.05)

# F5 depletion: energy e-folding length bound and B&O face value
D = 410 * Mpc
Lmin = D / (2 * -math.log(1 - 0.1129))
print("L_min =", Lmin, "m =", Lmin / Mpc, "Mpc")
quantity(f"{Lmin} m", "5.3e25 m", rel_tol=0.02)
E2, W2, C2 = res[2]
tau_h = E2 / W2
dep_vac = (D / c) / tau_h
print("tau_h =", tau_h, "s ; depletion over 410 Mpc vac:", dep_vac, " stimulated:", dep_vac * (1 + 2 * fCMB))
quantity(f"{dep_vac}", "3.3e-66", rel_tol=0.05)
quantity(f"{dep_vac*(1+2*fCMB)}", "2.5e-57", rel_tol=0.05)
print("Jones-Singleton exponent D/(2*1e11 m):", D / 2e11)
quantity(f"{D/2e11}", "6.3e13", rel_tol=0.02)
raise SystemExit(finish())
