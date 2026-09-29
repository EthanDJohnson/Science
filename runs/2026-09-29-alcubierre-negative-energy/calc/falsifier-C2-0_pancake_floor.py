#!/usr/bin/env python3
"""Falsifier C2-0: is -v^2 R/12 a floor on the Eulerian negative energy of an
Alcubierre-form shift beta = (-v F(x,y,z), 0, 0), unit lapse, flat slices?

Units: geometric (G = c = 1), lengths in metres; converted to kg via c^2/G.

Part 1 (symbolic, gr_tensors): rho_Euler for a GENERAL F(x,y,z).
Part 2 (numeric): spherical floor -(v^2/12) R (R+D)/D reproduced.
Part 3 (numeric): non-spherical 'pancake' F = g(x) h(rho_perp) with the ship ball
         (radius R) inside F = 1; Eulerian energy vs transverse log-extent Lambda.
Part 4: Bobrick-Martire flattening arithmetic using the candidate's own E -> E/alpha_X.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from gr_tensors import Spacetime, to_si

C = 299_792_458.0
G = 6.67430e-11
MSUN = 1.3271244e20 / G
KG_PER_M = C**2 / G

# ---------------- Part 1 ----------------
t, x, y, z, v = sp.symbols("t x y z v", real=True)
F = sp.Function("F")(x, y, z)
st = Spacetime.from_adm(1, [-v * F, 0, 0], sp.eye(3), [t, x, y, z])
rho = sp.simplify(st.energy_density())
target = -v**2 / (32 * sp.pi) * (sp.diff(F, y) ** 2 + sp.diff(F, z) ** 2)
print("Part 1: rho_Euler for general F(x,y,z) =", rho)
print("        rho - [-(v^2/32pi)(F_y^2+F_z^2)] simplifies to:", sp.simplify(rho - target))
print("        depends on dF/dx?", rho.has(sp.Derivative(F, x)))

# ---------------- Part 2 ----------------
R = 100.0  # m
vv = 10.0  # units of c


def sph_floor(D):
    return -(vv**2 / 12.0) * R * (R + D) / D


def sph_numeric(D, n=400001):
    # optimal profile f' = -A/r^2 on [R, R+D], A = R(R+D)/D
    r = np.linspace(R, R + D, n)
    A = R * (R + D) / D
    fp = -A / r**2
    integ = np.trapezoid(fp**2 * r**2, r)
    return -(vv**2 / 12.0) * integ


print("\nPart 2: spherical optimal-profile floor (R = 100 m, v = 10c)")
for D in (1.0, 10.0, 100.0, 1e6):
    e_a, e_n = sph_floor(D), sph_numeric(D)
    print(f"  D = {D:9.0f} m: E = {e_a:.5e} m (geom) = {e_a*KG_PER_M:.4e} kg = {e_a*KG_PER_M/MSUN:.3f} M_sun ; numeric {e_n*KG_PER_M:.4e} kg")
print(f"  D -> inf: -v^2 R/12 = {-(vv**2)*R/12*KG_PER_M:.4e} kg")

# ---------------- Part 3 ----------------
# F = g(x) h(p), p = transverse radius. g = 1 on |x| <= R, drops to 0 over width w (any w;
# rho has no dF/dx so w costs no Eulerian energy). h = 1 for p <= R,
# h = 1 - ln(p/R)/ln(Lam) for R < p < Lam R, 0 beyond.  Ball |r| <= R lies inside F = 1.
# E = -(v^2/32pi) * int g^2 dx * int |grad h|^2 d^2p


def pancake(Lam, w=1.0, n=200001):
    # x-integral of g^2 with a linear ramp of width w on each side
    xs = np.linspace(0, R + w, n)
    g = np.where(xs <= R, 1.0, 1.0 - (xs - R) / w)
    Ix = 2 * np.trapezoid(g**2, xs)
    # transverse integral, log-spaced grid
    u = np.linspace(0.0, math.log(Lam), n)  # u = ln(p/R)
    p = R * np.exp(u)
    hp = -1.0 / (p * math.log(Lam))
    Ip = np.trapezoid(hp**2 * 2 * math.pi * p * p, u)  # dp = p du
    return -(vv**2) / (32 * math.pi) * Ix * Ip, Ip, 2 * math.pi / math.log(Lam)


E_sph_inf = -(vv**2) * R / 12 * KG_PER_M
print("\nPart 3: pancake F = g(x) h(p), ship ball R = 100 m inside F = 1, v = 10c, x-ramp w = 1 m")
for Lam in (math.e**1.5, 10.0, 1e3, 1e6, 1e12, 1e30, 1e100):
    E, Ip, Ip_exact = pancake(Lam)
    Ekg = E * KG_PER_M
    print(f"  Lambda = {Lam:9.3e} (transverse extent {Lam*R:9.3e} m): transverse int = {Ip:.5f} "
          f"(exact 2pi/lnL = {Ip_exact:.5f}); E = {Ekg:.4e} kg = {Ekg/MSUN:.4e} M_sun; E/E_sph_inf = {Ekg/E_sph_inf:.4f}")
# convergence check
E1, _, _ = pancake(1e6, n=100001)
E2, _, _ = pancake(1e6, n=300001)
print(f"  convergence (Lambda=1e6): n=1e5 -> {E1*KG_PER_M:.6e} kg, n=3e5 -> {E2*KG_PER_M:.6e} kg")
# w-independence check
for w in (1e-3, 1.0, 10.0):
    E, _, _ = pancake(1e6, w=w)
    print(f"  x-ramp w = {w:g} m: E = {E*KG_PER_M:.5e} kg")
# Lambda required for given reduction factor k relative to -v^2 R/12 (w -> 0):
# E = -(v^2/32pi)(2R)(2pi/lnL) = -v^2 R/(8 lnL); ratio to v^2R/12 is 1.5/lnL
for k in (10, 100, 1e27):
    lnL = 1.5 * k
    print(f"  reduction x{k:g}: ln(Lambda) = {lnL:.3g}, transverse extent = R*exp({lnL:.3g}) = 10^{(lnL/math.log(10))+2:.3g} m")

# ---------------- Part 4 ----------------
alpha = 1 + vv**2
print("\nPart 4: Bobrick-Martire flattening E -> E/alpha_X, alpha_X = 1 + v^2 =", alpha)
Ef = E_sph_inf / alpha
print(f"  flattened D->inf floor: {Ef:.4e} kg = {Ef/MSUN:.4e} M_sun  (vs claimed 'at least' {E_sph_inf:.4e} kg)")
print(f"  candidate's own flattened figures: 2.5e29 kg and 7.4e29 kg, both < {abs(E_sph_inf):.3e} kg")
print(f"  v-independent limit v>>1: R/12 = {R/12*KG_PER_M:.4e} kg")
