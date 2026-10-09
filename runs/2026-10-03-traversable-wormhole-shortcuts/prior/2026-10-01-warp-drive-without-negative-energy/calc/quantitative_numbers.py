"""Quantitative facet: reference numbers for the warp-drive brief (SI unless stated).

Computes, from published formulas and inputs (each labelled), the numbers that the facet
reports: 2024 shell compactness/density/pressure/boost energies, Alcubierre and Natario
Eulerian energies for the reference case, Lentz scaling, Fell-Heisenberg unit inference,
and the rocket comparison for the trip case.  Everything here is OUR arithmetic on the
quoted inputs, not a source quote.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from rocket_tools import trip, C as C_R, G0, LY, YEAR, photon_rocket_mass_ratio

c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
lP = math.sqrt(hbar * G / c**3)
MJ = 1.898e27
Msun = 1.989e30
c2 = c * c
c4G = c**4 / G   # N, converts geometric (G=c=1) energy/length to J/m... E[J] = E_geo * c^4/G * (length in m)
rho_nuc = 2.3e17   # kg/m^3, nuclear saturation mass density (standard ~2.3e17)
print("constants: c=%.9g m/s G=%.5g lP=%.4g m c^4/G=%.4g N" % (c, G, lP, c4G))

print("\n=== 1. Fuchs et al. 2024 shell: R1=10 m, R2=20 m, M=4.49e27 kg, v_warp=0.04c")
R1, R2, M = 10.0, 20.0, 4.49e27
Vsh = 4 / 3 * math.pi * (R2**3 - R1**3)
rho_mean = M / Vsh
print("M/M_J = %.4f ; M/Msun = %.3e ; Mc^2 = %.4g J" % (M / MJ, M / Msun, M * c2))
print("shell volume = %.4g m^3 ; mean mass density M/V = %.4g kg/m^3 = %.4g J/m^3 ; x nuclear = %.3g"
      % (Vsh, rho_mean, rho_mean * c2, rho_mean / rho_nuc))
rs = 2 * G * M / c2
print("Schwarzschild radius 2GM/c^2 = %.4g m ; 2GM/(c^2 R2) = %.4f ; 2GM/(c^2 R1)= %.4f ; Buchdahl limit 8/9 = %.4f"
      % (rs, rs / R2, rs / R1, 8 / 9))
# Newtonian-order hydrostatic pressure scale  P ~ G M rho_mean / R2
P_est = G * M * rho_mean / R2
print("hydrostatic pressure scale G M rho/R2 = %.3g Pa ; /(rho c^2) = %.3f" % (P_est, P_est / (rho_mean * c2)))
v = 0.04 * c
print("0.04c = %.4g m/s ; KE of shell if boosted (1/2 M v^2) = %.4g J = %.3g M c^2" % (v, 0.5 * M * v**2, 0.5 * (0.04**2)))
mpay = 1e5
print("KE of 1e5 kg payload at 0.04c = %.4g J ; ratio shell/payload = %.3g" % (0.5 * mpay * v**2, M / mpay))
print("Time-rate shift inside Earth-mass shell R=10 m (B&M 2021 quote 4e-4): GM/(c^2 R)=%.3e" % (G * 5.972e24 / c2 / 10))
for Rin in (10.0, 100.0):
    s = Rin / R1
    print("OUR scaling at fixed compactness and v/c, payload radius R1=%g m: R2=%g m, M=%.3e kg = %.2f M_J = %.3e Msun, mean rho=%.3e kg/m^3"
          % (Rin, R2 * s, M * s, M * s / MJ, M * s / Msun, M * s / (4 / 3 * math.pi * ((R2 * s)**3 - (R1 * s)**3))))
print("Mc^2 / world primary energy (6.2e20 J/yr, ~620 EJ, to be sourced) = %.3g yr" % (M * c2 / 6.2e20))
print("Mc^2 relative to Sun's... Msun c^2 = %.4g J" % (Msun * c2))
# axis-read from fig 4 of paper: density axis x1e39 J/m^3 up to ~15; pressure x1e38 J/m^3 up to ~15
print("Fig.4 axis text read: density scale 1e39 J/m^3 (0..15) -> up to ~1.5e40 J/m^3 = %.3g kg/m^3 (axis-read, low confidence)" % (1.5e40 / c2))

print("\n=== 2. Fell-Heisenberg 2021 example (rho_max=3.2e26 kg/m^3, Etot=9.25e43 J)")
Etot = 9.25e43
print("Etot/c^2 = %.4g kg = %.4f M_J = %.3e Msun ; E_sun(1.78e47 J quoted) ratio = %.2e" % (Etot / c2, Etot / c2 / MJ, Etot / c2 / Msun, Etot / 1.78e47))
print("2GM/c^2 for Etot/c^2 = %.4g m" % (2 * G * Etot / c2 / c2))
print("rho_max / nuclear = %.3g" % (3.2e26 / rho_nuc))
print("c^2/(8 pi G) = %.4g kg/m ; rho_max/(that) = %.3f m^-2  => if curvature scale ~1/L^2 with L=1 m, implied" % (c2 / (8 * math.pi * G), 3.2e26 / (c2 / (8 * math.pi * G))))
print("FH central-region radius parameter r=6 (length unit not stated); if unit=1 m: 2GM/(c^2 *6 m)=%.3f" % (2 * G * Etot / c2 / c2 / 6))

print("\n=== 3. Alcubierre Eulerian energy, R=100 m, wall Delta=1 m, v in units of c")
R = 100.0
def alc_tanh(R, Delta, v):
    # tanh profile, sigma = 2/Delta  -> E = -(v^2 R^2 sigma/36) = -(v^2 R^2/(18 Delta)) [geometric]; verify by quadrature
    sigma = 2.0 / Delta
    r = np.linspace(max(R - 40 * Delta, 1e-6 * R), R + 40 * Delta, 400001)
    f = (np.tanh(sigma * (r + R)) - np.tanh(sigma * (r - R))) / (2 * np.tanh(sigma * R))
    fp = np.gradient(f, r)
    I = np.trapezoid(fp**2 * r**2, r)
    return -(v**2 / 12.0) * I, -(v**2 * R**2 / (18 * Delta))
for vv in (1.0, 10.0):
    num, ana = alc_tanh(R, 1.0, vv)
    print("v=%gc: numerical E_geo=%.5g m ; analytic -(v^2R^2/(18 Delta))=%.5g m ; E = %.4g J = %.4g kg = %.3g Msun = %.3g MJ"
          % (vv, num, ana, num * c4G, num * c4G / c2, num * c4G / c2 / Msun, num * c4G / c2 / MJ))
print("linear-ramp wall (Pfenning-Ford style): E = -(v^2/12)(R^2/Delta) ; v=10, Delta=1: %.4g kg = %.3g Msun"
      % (-(100 / 12.0) * R**2 * c4G / c2, (100 / 12.0) * R**2 * c4G / c2 / Msun))
for vv in (1.0, 10.0):
    Dl = 100 * vv * lP
    Elin = (vv**2 / 12.0) * (R**2 / Dl) * c4G / c2
    print("QI-limited wall Delta=100 v lP=%.3e m (PF 1997 convention, alpha=1/10), v=%gc: |E| linear ramp = %.3e kg = %.3e Msun"
          % (Dl, vv, Elin, Elin / Msun))
print("thick-wall floor, linear ramp -> |E| = (v^2 R/12) c^4/G ; R=100, v=10: %.4g kg = %.3g Msun" % (100 * R / 12 * c4G / c2, 100 * R / 12 * c4G / c2 / Msun))
print("Bobrick-Martire: optimal shape f=min(r0/r,1) ~ factor 3 less; flatten by 10 -> 10x less (as quoted). v=10,R=100,Delta=1 case /3 = %.3g Msun" %
      (num * c4G / c2 / Msun / 3))

print("\n=== 4. Natario zero-expansion shift, same profile, E = -(1/16pi) K_ij K^ij (flat 3-metric, unit lapse), v=1c, R=100 m, Delta=1 m")
x, y, z = sp.symbols("x y z", real=True)
Rs, sg = sp.symbols("Rs sg", positive=True)
r = sp.sqrt(x**2 + y**2 + z**2)
g = (sp.tanh(sg * (r + Rs)) - sp.tanh(sg * (r - Rs))) / (2 * sp.tanh(sg * Rs))
fN = g / 2
# X = 2 f cos(th) e_r - (2 f + r f') sin(th) e_th  with f(r) -> Cartesian: X = 2 f ez... derive via Cartesian components
rr = sp.Symbol("rr", positive=True)
fr = sp.Function("fr")
# Cartesian: e_r = (x,y,z)/r ; e_th = (x z/ (r rho), y z/(r rho), -rho/r) ; sin th = rho/r, cos th = z/r
rho = sp.sqrt(x**2 + y**2)
fp = sp.diff(fN, x) * x / r + sp.diff(fN, y) * y / r + sp.diff(fN, z) * z / r  # f'(r) (radial derivative)
cth = z / r
sth = rho / r
er = sp.Matrix([x, y, z]) / r
eth = sp.Matrix([x * z / (r * rho), y * z / (r * rho), -rho / r])
X = 2 * fN * cth * er - (2 * fN + r * fp) * sth * eth
# interior f=1/2 => X = (cos th e_r - sin th e_th) = e_z  (uniform shift of unit magnitude, times v)
J = X.jacobian([x, y, z])
S = (J + J.T) / 2
K2 = 4 * sum(S[i, j]**2 for i in range(3) for j in range(3)) / 4  # K_ij = -S_ij => K_ij K^ij = S_ij S_ij ; (kept explicit)
K2 = sum(S[i, j]**2 for i in range(3) for j in range(3))
div = J.trace()
fK2 = sp.lambdify((x, z, Rs, sg), K2.subs(y, 0), "numpy")
fdiv = sp.lambdify((x, z, Rs, sg), div.subs(y, 0), "numpy")
Delta = 1.0
sigma = 2.0 / Delta
rgrid = np.arange(R - 12 * Delta, R + 12 * Delta, Delta / 8)
th = np.linspace(1e-4, math.pi - 1e-4, 721)
# integrate wall region only (interior f=1/2 gives uniform shift, K=0; exterior f=0)
Rg, Tg = np.meshgrid(rgrid + 0.0, th, indexing="ij")
Kv = fK2(Rg * np.sin(Tg), Rg * np.cos(Tg), R, sigma)
Dv = fdiv(Rg * np.sin(Tg), Rg * np.cos(Tg), R, sigma)
integrand = Kv * Rg**2 * np.sin(Tg)
Iang = np.trapezoid(integrand, th, axis=1)
Itot = np.trapezoid(Iang, rgrid)
E_nat_geo = -(1 / (16 * math.pi)) * 2 * math.pi * Itot
print("max |div X| on grid = %.3e (should be ~0)" % np.max(np.abs(Dv)))
print("Natario E_geo (v=1) = %.5g m ; E = %.4g J = %.4g kg = %.3g Msun" % (E_nat_geo, E_nat_geo * c4G, E_nat_geo * c4G / c2, E_nat_geo * c4G / c2 / Msun))
num1, ana1 = alc_tanh(R, 1.0, 1.0)
print("Alcubierre same profile E_geo = %.5g m ; ratio Natario/Alcubierre = %.3f" % (num1, E_nat_geo / num1))
print("Natario at v=10c: %.3g Msun (E ~ v^2)" % (E_nat_geo * 100 * c4G / c2 / Msun))

print("\n=== 5. Lentz 2021 proceedings scaling: E_tot ~ C v^2 R^2 / w, R=100 m, w=1 m -> (few) x 1e-1 Msun v^2")
for few in (2, 3, 5):
    print("few=%d: v=1c: %.2e Msun = %.2e kg ; v=10c: %.2e Msun = %.2e kg" % (few, few * 0.1, few * 0.1 * Msun, few * 10, few * 10 * Msun))
print("Alcubierre tanh same R,w (E=-v^2R^2/(18 w)) v=1: %.3f Msun" % (R**2 / 18 * c4G / c2 / Msun))
print("Etot ~ v^2 R^2/w check: R=10 m -> /100; R=100 m, w=0.1 m -> x10")

print("\n=== 6. Trip: 1e5 kg payload, 4.37 ly, rocket comparison (rocket_tools.py)")
d = 4.37 * LY
for a, ve, lab in ((G0, C_R, "1 g photon rocket, accelerate half/brake half"),):
    t = trip(distance=d, accel=a, v_exhaust=ve)
    print(lab, {k: (round(val, 4) if isinstance(val, float) else val) for k, val in t.items()})
    mr = t["mass_ratio"]
    print("  initial mass for 1e5 kg payload (mass ratio %.3g) = %.3e kg ; propellant mass-energy = %.3e J" % (mr, mr * mpay, (mr - 1) * mpay * c2))
for beta in (0.1, 0.5):
    print("photon-rocket mass ratio for single accelerate to beta=%.1f: %.3f (stop too: squared %.3f)" % (beta, photon_rocket_mass_ratio(beta), photon_rocket_mass_ratio(beta)**2))
print("1e5 kg rest energy = %.3e J; at cruise beta=0.1 coast to 4.37 ly takes %.1f yr (flat-space)" % (mpay * c2, 4.37 / 0.1))
print("Warp-drive reference (Alcubierre tanh, R=10 m payload bubble, Delta=1 m, v=4.37c ~ 1 yr trip) : E = %.3e kg = %.3e Msun"
      % (4.37**2 * 10**2 / 18 * c4G / c2, 4.37**2 * 10**2 / 18 * c4G / c2 / Msun))
print("Same but R=100 m: %.3e Msun" % (4.37**2 * 100**2 / 18 * c4G / c2 / Msun))
print("2024 shell mass / (1e5 kg payload) = %.3g ; 2024 shell Mc^2 vs photon-rocket propellant energy (1 g round trip) = %.3g" %
      (M / mpay, M * c2 / ((trip(distance=d, accel=G0, v_exhaust=C_R)['mass_ratio'] - 1) * mpay * c2)))

print("\n=== 7. Reference energies")
print("Planck length = %.4e m (from hbar,G,c)" % lP)
print("Msun c^2 = %.4g J ; MJ c^2 = %.4g J ; world primary energy ~6.2e20 J/yr (to be sourced)" % (Msun * c2, MJ * c2))
print("Msun c^2 / world yearly energy = %.3g yr" % (Msun * c2 / 6.2e20))

print("\n=== 4b. Natario scaling and convergence (our calculation)")
def nat(Rv, Dl, dr_over, nth_n):
    sgm = 2.0 / Dl
    rg = np.arange(max(Rv - 14 * Dl, 1e-3), Rv + 14 * Dl, Dl / dr_over)
    t = np.linspace(1e-4, math.pi - 1e-4, nth_n)
    Rg2, Tg2 = np.meshgrid(rg, t, indexing="ij")
    K = fK2(Rg2 * np.sin(Tg2), Rg2 * np.cos(Tg2), Rv, sgm)
    I = np.trapezoid(np.trapezoid(K * Rg2**2 * np.sin(Tg2), t, axis=1), rg)
    return -(1 / (16 * math.pi)) * 2 * math.pi * I
for Rv, Dl in ((100.0, 1.0), (100.0, 2.0), (100.0, 4.0), (50.0, 1.0), (100.0, 20.0)):
    e = nat(Rv, Dl, 8, 721)
    ea = -(Rv**2 / (18 * Dl))
    print("R=%g m Delta=%g m: Natario E_geo(v=1)=%.5g m ; Alcubierre %.5g m ; ratio %.4g ; (R/Delta)^2=%.4g ; E*Delta^3/R^4 = %.4g"
          % (Rv, Dl, e, ea, e / ea, (Rv / Dl)**2, e * Dl**3 / Rv**4))
print("convergence R=100,Delta=1: dr=Delta/8,nth=721: %.6g ; dr=Delta/16,nth=1441: %.6g" % (nat(100.0, 1.0, 8, 721), nat(100.0, 1.0, 16, 1441)))
