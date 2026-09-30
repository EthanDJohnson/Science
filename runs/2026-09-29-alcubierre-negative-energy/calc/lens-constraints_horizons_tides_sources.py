"""Constraints lens: horizons, Hawking temperature, RSET e-folds, CTC threshold, ship tides, Natario scaling, and
source-side limits (Casimir, squeezed light / QI) for the reference case R = 100 m, v = 10c, Delta_PF = 1 m.
Geometric units (G = c = 1, metres) for metric quantities; SI for sources. All numbers printed with units.
"""
import math
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import metrics, horizons_1p1, to_si, qi, PLANCK_LENGTH, HBAR, C, G_NEWTON  # noqa: E402

MSUN, MJ, G0 = 1.989e30, 1.898e27, 9.80665
YEAR = 3.15576e7
R, V = 100.0, 10.0


def f_np(r, Rb, sig):
    return (np.tanh(sig * (r + Rb)) - np.tanh(sig * (r - Rb))) / (2 * np.tanh(sig * Rb))


print("=== 1. Horizons along the axis (comoving u = -v(1 - f)) and Hawking temperature ===")
for label, D in (("Delta = 1 m", 1.0), ("Delta = 10 m", 10.0), ("QI wall 97.7 v L_P", 97.7 * V * PLANCK_LENGTH)):
    sig = 2.0 / D  # thin-wall PF relation
    # work in units of D to keep the grid sane; kappa scales as 1/D
    s = sig * D  # = 2
    Rs = R / D
    xs = np.linspace(-Rs - 20, Rs + 20, 400001)
    hz = horizons_1p1(lambda q: -V * (1 - f_np(np.abs(q), Rs, s)), xs)
    for h in hz:
        kap = h["kappa"] / D  # 1/m
        T = to_si.hawking_temperature_k(kap)
        tau = 1 / (kap * C)
        efolds = 0.4372 * YEAR / tau
        print(f"{label}: horizon at xi = {h['x']*D:+.6e} m, kappa = {kap:.4e} /m, T_H = {T:.3e} K, 1/kappa = {tau:.3e} s,"
              f" RSET e-folds over a 0.437 yr trip = {efolds:.2e}")
print("(f = 1 - 1/v at the horizon; the ship at xi = 0 is inside both.)")

print("\n=== 2. Chronology: frame speed that makes a v = 10c trip run backwards in time ===")
for v in (1.5, 10.0):
    print(f"v = {v}c: Delta t' = gamma Delta t (1 - beta v) < 0 for beta > 1/v = {1/v:.3f} c")

print("\n=== 3. Tidal tensor on the ship (Eulerian = ship frame, geodesic), R = 100 m, Delta_PF = 1 m, v = 10c ===")
st, s = metrics.alcubierre()
top = metrics.alcubierre_top_hat(s)
rm = st.riemann()
t, x, y, z = st.coords
n4 = 4
params = {s["v"]: V, s["R"]: R, s["sigma"]: 2.0}
flat = [rm[a][b][c][d] for a in range(n4) for b in range(n4) for c in range(n4) for d in range(n4)]
rfn = st.compile(sp.Matrix(flat), params, {s["f"]: top})
gfn = st.compile(st.g, params, {s["f"]: top})
ffn = st.compile(top(s["r_s"]), params)


def tidal(point):
    g = np.array(gfn(*point), dtype=float).reshape(4, 4)
    rup = np.array(rfn(*point), dtype=float).reshape(4, 4, 4, 4)
    rlow = np.einsum("ae,ebcd->abcd", g, rup)
    fval = float(ffn(*point))
    nvec = np.array([1.0, V * fval, 0.0, 0.0])  # Eulerian 4-velocity (lapse 1, shift -v f x)
    E = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            ei = np.zeros(4); ei[i + 1] = 1.0
            ej = np.zeros(4); ej[j + 1] = 1.0
            E[i, j] = np.einsum("abcd,a,b,c,d->", rlow, nvec, ei, nvec, ej)
    return np.max(np.abs(np.linalg.eigvalsh(E))) * C**2 / G0  # g per metre


for axis in ("equator (y)", "axis (x)"):
    row = []
    for rr in (0.0, 50.0, 80.0, 90.0, 95.0, 97.0, 98.0, 99.0, 99.5):
        pt = (0.0, rr, 1e-3, 0.0) if axis == "axis (x)" else (0.0, 1e-3, rr, 0.0)
        if rr == 0.0:
            pt = (0.0, 1e-3, 1e-3, 1e-3)
        row.append(f"r={rr:g} m: {tidal(pt):.2e}")
    print(f"{axis}: " + "; ".join(row) + "  [g/m]")

print("\n=== 4. Natario zero-expansion (Natario's own spherical example, n = f/2), 1D exact vs thin-wall law ===")
def e_nat(v, Rb, sig, npts=400001):
    w = 40.0 / sig
    r = np.linspace(max(1e-9, Rb - w), Rb + w, npts)
    a = sig * (Rb + r); b = sig * (r - Rb)
    fp = sig * (1 / np.cosh(a) ** 2 - 1 / np.cosh(b) ** 2) / (2 * np.tanh(sig * Rb))
    fpp = sig**2 * (-2 * np.tanh(a) / np.cosh(a) ** 2 + 2 * np.tanh(b) / np.cosh(b) ** 2) / (2 * np.tanh(sig * Rb))
    integrand = r**2 * (fp**2 / 2 + (fp + r * fpp / 2) ** 2 / 3)
    return -(v**2) / 4 * np.trapezoid(integrand, r)
for sig in (8.0, 16.0, 32.0):
    print(f"R=1, sigma={sig}, v=1: E_Nat = {e_nat(1.0, 1.0, sig):.4f} m ; thin-wall -v^2 R^4 sigma^3/180 = {-(sig**3)/180:.4f} m")
En = e_nat(V, R, 2.0)
En2 = e_nat(V, R, 2.0, 600001)
print(f"Reference R=100 m, Delta=1 m, v=10c: E_Nat = {En:.4e} m (1.5n {En2:.4e}) = {to_si.mass_kg(En):.3e} kg = {to_si.mass_kg(En)/MSUN:.3e} Msun;"
      f" ratio to Alcubierre (-5.556e4 m) = {En/-5.5556e4:.0f}")

print("\n=== 5. Source-side limits (SI) ===")
c4G = C**4 / G_NEWTON
for D in (1.0, 97.7 * V * PLANCK_LENGTH):
    rho_pk = V**2 / (32 * math.pi * D**2) * c4G  # J/m^3, magnitude
    a_needed = (math.pi**2 * HBAR * C / (720 * rho_pk)) ** 0.25
    print(f"Delta={D:.3e} m, v=10c: peak |rho| = {rho_pk:.3e} J/m^3 ({rho_pk/C**2:.3e} kg/m^3); ideal-Casimir gap needed a = {a_needed:.3e} m "
          f"(= {a_needed/8.41e-16:.2e} proton radii, {a_needed/3.8616e-13:.2e} reduced electron Compton wavelengths)")
    # squeezed/EM field: pulse duration at which the EM Ford-Roman bound (2x scalar) permits this density
    tau = (2 * 3 * HBAR / (32 * math.pi**2 * C**3 * rho_pk)) ** 0.25
    print(f"   EM-field QI: a Lorentzian-sampled |rho| this large is allowed only for tau0 <= {tau:.3e} s (c tau0 = {C*tau:.3e} m)")
print(f"EM QI bound at tau0 = 1 fs: {2*qi.ford_roman_si(1e-15):.4f} J/m^3 ; at 1 ps: {2*qi.ford_roman_si(1e-12):.3e} J/m^3")
# Casimir plates: minimal plate mass per |E| (two graphene-like monolayers, 7.6e-7 kg/m^2 each)
sigma_areal = 7.6e-7
for a in (1e-9, 3e-10):
    e_area = math.pi**2 * HBAR * C / (720 * a**3)
    print(f"ideal Casimir a={a:.0e} m: |E|/A = {e_area:.3e} J/m^2 ; two monolayer plates rest energy/A = {2*sigma_areal*C**2:.3e} J/m^2 ; ratio = {2*sigma_areal*C**2/e_area:.2e}")
# Hubble-volume mass for scale (H0 = 67.4 km/s/Mpc; M = c^3/(2 G H0))
H0 = 67.4e3 / 3.0857e22
print(f"mass inside the Hubble radius c^3/(2 G H0) = {C**3/(2*G_NEWTON*H0):.3e} kg (H0 = 67.4 km/s/Mpc; ours)")
# Lobo-Visser weak-field ship bound v^2 R^2 sigma <= M_ship
print(f"Lobo-Visser v^2 R^2 sigma (R=100 m, sigma=2/m): v=0.1 -> {to_si.mass_kg(0.01*1e4*2):.3e} kg ; v=10 -> {to_si.mass_kg(100*1e4*2):.3e} kg (linearized: valid only v<<1)")
