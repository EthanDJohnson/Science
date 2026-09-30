"""Falsifier C7-0: is Natario's (R/Delta)^2 energy penalty a property of zero expansion,
or only of the COMPACT-support shift Natario chose?

Units: geometric (G = c = 1), lengths in metres, v in units of c, energies in metres
(x 1.2103e44 J/m for SI, / c^2 -> x 1.3466e27 kg/m).

Natario-class, unit lapse, flat slices: beta = curl[(v/2) h(r) (0, -z, y)].
  h = 1 inside -> beta = v x_hat exactly; div beta = 0 everywhere (zero expansion).
  rho_Eul = (K^2 - K_ij K^ij)/(16 pi) = -K_ij K^ij/(16 pi) <= 0.
Profiles (same wall width D, same C^2 quintic smoothstep S on [R, R+D]):
  Alcubierre   : beta = v f x_hat, f = 1 - S
  Natario (compact, as published): h = 1 - S      -> h = 0 outside R+D
  Natario-dipole (non-compact): h = (1 - S) + S * (R/r)^3  -> exterior is potential dipole flow
      (curl-free AND div-free outside, decays as r^-3, asymptotically flat).
Also the tanh profile of the candidate (R=1, sigma=8,16,32) to reproduce its numbers.

Method: (a) direct sympy K_ij in Cartesian coordinates, 2D (r, theta) quadrature over the
axisymmetric slice; (b) cross-check against 1D Natario formula
  E = -(v^2/2) int r^2 [n'^2 + (2/3)(n' + r n''/2)^2] dr, n = h/2.
"""
import math
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
rr = sp.symbols("r", positive=True)
X = (x, y, z)
V = 1.0


def K_density(beta):
    K = sp.Matrix(3, 3, lambda i, j: sp.Rational(1, 2) * (sp.diff(beta[j], X[i]) + sp.diff(beta[i], X[j])))
    trK = K.trace()
    KK = sum(K[i, j] ** 2 for i in range(3) for j in range(3))
    return (trK**2 - KK) / (16 * sp.pi), trK


def shifts(hfun):
    """hfun: sympy expr in rr. Returns Alcubierre-type and Natario-type shifts with profile hfun."""
    r = sp.sqrt(x**2 + y**2 + z**2)
    h = hfun.subs(rr, r)
    psi = (0, -(V / 2) * h * z, (V / 2) * h * y)
    curl = (sp.diff(psi[2], y) - sp.diff(psi[1], z),
            sp.diff(psi[0], z) - sp.diff(psi[2], x),
            sp.diff(psi[1], x) - sp.diff(psi[0], y))
    return (V * h, 0, 0), curl


def energy2d(rho_expr, rgrid, nth=121):
    """Integrate rho over all space, axisymmetric about x: points (r cos th, r sin th, 0)."""
    fr = sp.lambdify((x, y, z), rho_expr, "numpy")
    th = np.linspace(0, math.pi, nth)
    Rg, Tg = np.meshgrid(rgrid, th, indexing="ij")
    vals = fr(Rg * np.cos(Tg), Rg * np.sin(Tg), 0 * Rg)
    vals = np.broadcast_to(vals, Rg.shape)
    integrand = 2 * math.pi * Rg**2 * np.sin(Tg) * vals
    inner = np.trapezoid(integrand, th, axis=1)
    return np.trapezoid(inner, rgrid)


def energy1d_nat(hexpr, rgrid):
    n = hexpr / 2
    n1 = sp.diff(n, rr)
    n2 = sp.diff(n, rr, 2)
    fi = sp.lambdify(rr, rr**2 * (n1**2 + sp.Rational(2, 3) * (n1 + rr * n2 / 2) ** 2), "numpy")
    return -(V**2 / 2) * np.trapezoid(np.broadcast_to(fi(rgrid), rgrid.shape), rgrid)


def energy1d_alc(fexpr, rgrid):
    f1 = sp.diff(fexpr, rr)
    fi = sp.lambdify(rr, rr**2 * f1**2, "numpy")
    return -(V**2 / 12) * np.trapezoid(np.broadcast_to(fi(rgrid), rgrid.shape), rgrid)


def smoothstep(Rv, D):
    u = (rr - Rv) / D
    q = 6 * u**5 - 15 * u**4 + 10 * u**3
    return sp.Piecewise((0, rr <= Rv), (q, rr < Rv + D), (1, True))


def rgrid_for(Rv, D, rmax_factor=60.0, nwall=4000, nout=20000):
    a = np.linspace(1e-6, Rv, 200, endpoint=False)
    w = np.linspace(Rv, Rv + D, nwall, endpoint=False)
    o = np.geomspace(Rv + D, rmax_factor * (Rv + D), nout)
    return np.concatenate([a, w, o])


print("=== 0. Reproduce candidate: tanh profile, R=1 m, v=1 (1D formulas; energies in m) ===")
for sg in (8.0, 16.0, 32.0):
    Rv = 1.0
    ftanh = (sp.tanh(sg * (rr + Rv)) - sp.tanh(sg * (rr - Rv))) / (2 * math.tanh(sg * Rv))
    g = np.linspace(1e-6, 4.0, 200001)
    Ea = energy1d_alc(ftanh, g)
    En = energy1d_nat(ftanh, g)
    print(f"sigma={sg:5.1f}: E_Alc={Ea:+.4f}  E_Nat(compact)={En:+.4f}  ratio={En/Ea:7.2f}  (sigma R)^2/5={(sg*Rv)**2/5:7.2f}")

print("\n=== 1. Direct 3D K_ij check of the 1D Natario formula (smoothstep, R=1, D=0.25) ===")
Rv, D = 1.0, 0.25
S = smoothstep(Rv, D)
for name, h in (("compact", 1 - S), ("dipole ", (1 - S) + S * (Rv / rr) ** 3)):
    _, bn = shifts(h)
    rho_n, th_n = K_density(bn)
    g2 = rgrid_for(Rv, D, rmax_factor=40, nwall=600, nout=3000)
    E2 = energy2d(rho_n, g2)
    E1 = energy1d_nat(h, rgrid_for(Rv, D, rmax_factor=40))
    fth = sp.lambdify((x, y, z), th_n, "numpy")
    pts = [(0.3, 1.1, 0.2), (1.12, 0.1, -0.3), (2.0, 1.0, 0.5)]
    maxth = max(abs(float(fth(*p))) for p in pts)
    print(f"{name}: E_3D={E2:+.5f} m  E_1D={E1:+.5f} m  max|div beta| at test pts={maxth:.1e}")

print("\n=== 2. Same wall width D (quintic smoothstep), v=1: Alcubierre vs Natario compact vs Natario dipole ===")
print("    R/D       E_Alc(m)       E_NatCompact(m)   ratio_c    E_NatDipole(m)   ratio_d   exterior(-3/8 v^2 R)")
for Rv, D in ((1.0, 0.25), (1.0, 0.125), (1.0, 1/16), (1.0, 1/32), (1.0, 1/100), (100.0, 1.0)):
    S = smoothstep(Rv, D)
    g = rgrid_for(Rv, D)
    Ea = energy1d_alc(1 - S, g)
    Ec = energy1d_nat(1 - S, g)
    Ed = energy1d_nat((1 - S) + S * (Rv / rr) ** 3, g)
    # convergence: double the grid
    g2 = rgrid_for(Rv, D, rmax_factor=120, nwall=8000, nout=40000)
    Ed2 = energy1d_nat((1 - S) + S * (Rv / rr) ** 3, g2)
    print(f"{Rv/D:7.1f}  {Ea:+.4e}   {Ec:+.4e}   {Ec/Ea:9.2f}   {Ed:+.4e}   {Ed/Ea:6.2f}   {-0.375*Rv:+.3e}  (conv {abs(Ed2/Ed-1):.1e})")

print("\n=== 3. Reference case R=100 m, D=1 m, v=10 (energies scale as v^2); SI mass ===")
Rv, D, v = 100.0, 1.0, 10.0
S = smoothstep(Rv, D)
g = rgrid_for(Rv, D)
KG_PER_M = 1.3466e27
Ea = energy1d_alc(1 - S, g) * v**2
Ec = energy1d_nat(1 - S, g) * v**2
Ed = energy1d_nat((1 - S) + S * (Rv / rr) ** 3, g) * v**2
for nm, E in (("Alcubierre", Ea), ("Natario compact", Ec), ("Natario dipole", Ed)):
    print(f"{nm:16s}: E = {E:+.3e} m = {E*KG_PER_M:+.3e} kg = {E*KG_PER_M/1.989e30:+.3e} Msun")
print(f"ratio compact/Alc = {Ec/Ea:.3e};  dipole/Alc = {Ed/Ea:.3f}")
