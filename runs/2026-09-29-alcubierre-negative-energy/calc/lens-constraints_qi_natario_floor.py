"""Constraints lens, follow-up:
 A. QI-wall horizon: resolve kappa numerically (grid in units of Delta, R/Delta = 50, thin wall so kappa*Delta is
    R-independent) and compare with kappa = 4(v-1)/(v Delta); Hawking temperature at the QI wall.
 B. Natario zero-expansion drive: curvature radius at the wall vs sigma (toolkit curvature_at with Riemann compiled
    once per sigma) -> scaling r_c(sigma), then Ford-Roman QI-limited Delta and E at R = 100 m, v = 10c.
 C. Thick-wall floor: Cauchy-Schwarz bound int f'^2 r^2 dr >= R(R+D)/D for f from 1 at r=R to 0 at r=R+D, checked
    numerically for linear ramp, tanh-like and the optimal f' ~ 1/r^2 profile; SI values at v = 10c, R = 100 m.
 D. Natario energy conditions (v = 1) on a wall sample.
Geometric units (G = c = 1, metres) for metric quantities; SI where labelled.
"""
import math
import sys
import time

import numpy as np
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import Spacetime, horizons_1p1, to_si, PLANCK_LENGTH, HBAR, C, G_NEWTON  # noqa: E402

T0 = time.time()
MSUN = 1.989e30
KB = 1.380649e-23
T_PLANCK = 1.416784e32


def f_np(r, Rb, sig):
    return (np.tanh(sig * (r + Rb)) - np.tanh(sig * (r - Rb))) / (2 * np.tanh(sig * Rb))


print("=== A. Horizon surface gravity, thin tanh wall (units of Delta_PF, sigma = 2/Delta) ===")
for V in (1.5, 2.0, 10.0):
    Rs = 50.0
    for npts in (200001, 300001):
        xs = np.linspace(-Rs - 20, Rs + 20, npts)
        hz = horizons_1p1(lambda q: -V * (1 - f_np(np.abs(q), Rs, 2.0)), xs)
        kd = [h["kappa"] for h in hz]
        print(f"v={V}: n={npts}: kappa*Delta = {kd} ; analytic 4(v-1)/v = {4*(V-1)/V:.6f}")
DQI = 97.7 * 10.0 * PLANCK_LENGTH
kap = 4 * 9 / 10 / DQI
print(f"QI wall v=10c: Delta = {DQI:.3e} m, kappa = {kap:.3e} /m, T_H = {to_si.hawking_temperature_k(kap):.3e} K "
      f"(= {to_si.hawking_temperature_k(kap)/T_PLANCK:.2e} T_Planck), 1/(kappa c) = {1/(kap*C):.3e} s, "
      f"e-folds in 0.437 yr = {0.4372*3.15576e7*kap*C:.2e}")

print("\n=== C. Thick-wall floor (spherical Alcubierre, Eulerian): E = -(v^2/12) int f'^2 r^2 dr ===")
Rb = 100.0
for D in (1.0, 10.0, 100.0, 1e4):
    r = np.linspace(Rb, Rb + D, 400001)
    lin = np.trapezoid(np.full_like(r, 1 / D**2) * r**2, r)
    # optimal: f' = -A / r^2 with A = 1/(1/R - 1/(R+D))
    A = 1 / (1 / Rb - 1 / (Rb + D))
    opt = np.trapezoid((A / r**2) ** 2 * r**2, r)
    # smooth C^1 ramp (cosine) for comparison
    fp = (math.pi / (2 * D)) * np.sin(math.pi * (r - Rb) / D)
    cosr = np.trapezoid(fp**2 * r**2, r)
    bound = Rb * (Rb + D) / D
    E_opt_10 = -(100 / 12) * opt
    print(f"D={D:g} m: int f'^2 r^2: linear {lin:.5e}, cosine {cosr:.5e}, optimal {opt:.5e}, bound R(R+D)/D {bound:.5e} ;"
          f" E_min(v=10c) = {E_opt_10:.4e} m = {to_si.mass_kg(E_opt_10):.3e} kg = {to_si.mass_kg(E_opt_10)/MSUN:.3e} Msun")
print(f"D -> inf: E_min -> -v^2 R/12 = {-(100/12)*Rb:.4e} m = {to_si.mass_kg(-(100/12)*Rb):.3e} kg (v=10c, R=100 m)")

print("\n=== B. Natario zero-expansion: curvature radius at the wall vs sigma (R = 1, v = 1) ===")
t, x, y, z = sp.symbols("t x y z", real=True)
v, R, sg = sp.symbols("v R sigma", positive=True)
f = sp.Function("f")
xi = x - v * t
rs = sp.sqrt(xi**2 + y**2 + z**2)
F = f(rs)
fy, fz = sp.diff(F, y), sp.diff(F, z)
X = [v * (F + (y * fy + z * fz) / 2), -v * xi * fy / 2, -v * xi * fz / 2]
st = Spacetime.from_adm(1, [-c for c in X], sp.eye(3), [t, x, y, z])
rr = sp.symbols("r", positive=True)
top = sp.Lambda(rr, (sp.tanh(sg * (rr + R)) - sp.tanh(sg * (rr - R))) / (2 * sp.tanh(sg * R)))
funcs = {f: top}
rho = st.energy_density()
rm = st.riemann()
flat = [rm[a][b][c][d] for a in range(4) for b in range(4) for c in range(4) for d in range(4)]
eul = st.eulerian_observer()
print(f"symbolic setup {time.time()-T0:.0f}s", flush=True)
from gr_tensors import _orthonormal_frame  # noqa: E402

res = []
for sig in (8.0, 16.0, 32.0):
    params = {v: 1.0, R: 1.0, sg: sig}
    rfn = st.compile(sp.Matrix(flat), params, funcs)
    gfn = st.compile(st.g, params, funcs)
    ufn = st.compile(eul, params, funcs)
    rhofn = st.compile(rho, params, funcs)
    best_peak, best_pt, rho_min = 0.0, None, 0.0
    D = 2.0 / sig
    for th in np.linspace(0.02, math.pi / 2, 9):
        for dr in np.linspace(-1.5 * D, 1.5 * D, 13):
            rr_ = 1.0 + dr
            pt = (0.0, rr_ * math.cos(th), rr_ * math.sin(th), 1e-4)
            g = np.array(gfn(*pt), dtype=float).reshape(4, 4)
            r_up = np.array(rfn(*pt), dtype=float).reshape(4, 4, 4, 4)
            r_low = np.einsum("ae,ebcd->abcd", g, r_up)
            e = _orthonormal_frame(g, np.array(ufn(*pt), dtype=float).reshape(4))
            fr = np.einsum("Aa,Bb,Cc,Dd,abcd->ABCD", e, e, e, e, r_low)
            pk = float(np.max(np.abs(fr)))
            if pk > best_peak:
                best_peak, best_pt = pk, pt
            rho_min = min(rho_min, float(rhofn(*pt)))
    rc = 1 / math.sqrt(best_peak)
    res.append((sig, rc, rho_min))
    print(f"sigma={sig}: Delta_PF={D:.4f}: min r_c = {rc:.4e} m at {tuple(round(q,4) for q in best_pt)} ; r_c*sigma^2 = {rc*sig**2:.4f} ;"
          f" min rho = {rho_min:.4e} /m^2 ; rho_min/sigma^4 = {rho_min/sig**4:.4e}  [{time.time()-T0:.0f}s]", flush=True)

# fit r_c = b * Delta^2/(v R) and rho_pk = -a v^2 R^2/Delta^4 (thin-wall scalings) from the sigma=32 point
sig, rc, rmin = res[-1]
D = 2 / sig
b = rc / D**2
a = -rmin * D**4
print(f"thin-wall fits (sigma=32): r_c ~ {b:.4f} Delta^2/(v R) ; rho_pk ~ -{a:.4e} v^2 R^2/Delta^4")
# QI: |rho_pk| <= 3 L_P^2/(32 pi^2 (alpha r_c)^4), r_c = b Delta^2/(v R)  ->  Delta^4 <= 3 L_P^2 v^2 R^2 / (32 pi^2 alpha^4 b^4 a)... solve
for alpha in (0.1, 0.01):
    Rr, V = 100.0, 10.0
    # a v^2 R^2 / D^4 <= 3 L^2 v^4 R^4 /(32 pi^2 alpha^4 b^4 D^8)  ->  D^4 <= 3 L^2 v^2 R^2/(32 pi^2 alpha^4 b^4 a)
    D4 = 3 * PLANCK_LENGTH**2 * V**2 * Rr**2 / (32 * math.pi**2 * alpha**4 * b**4 * a)
    Dq = D4 ** 0.25
    En = -(V**2) * Rr**4 / (22.5 * Dq**3)
    print(f"alpha={alpha}: Natario QI wall Delta <= {Dq:.3e} m ; E_Nat = {En:.3e} m = {to_si.mass_kg(En):.3e} kg = {to_si.mass_kg(En)/MSUN:.3e} Msun")

print("\n=== D. Natario energy conditions at v = 1 on the wall (R = 1, sigma = 8) ===")
pts = []
for th in np.linspace(0.1, math.pi - 0.1, 7):
    for rr_ in (0.85, 0.95, 1.0, 1.05, 1.15):
        pts.append((0.0, rr_ * math.cos(th), rr_ * math.sin(th), 0.05))
sc = st.scan_energy_conditions(pts, {v: 1.0, R: 1.0, sg: 8.0}, funcs)
print(f"points {sc['points']}, violations {sc['violations']}, worst NEC {sc['worst']['nec_min'][0]:.3e}  [{time.time()-T0:.0f}s]")
