"""Engineer lens: does Natario's zero-expansion drive need less Eulerian negative energy than
Alcubierre's at the same bubble radius R and wall steepness sigma?  And check the thick-wall floor.

Units: geometric (G = c = 1), lengths in metres; v in units of c. Energies are in metres
(multiply by c^4/G = 1.2103e44 J/m for SI).

Both metrics have unit lapse and flat slices: ds^2 = -dt^2 + (dx^i - beta^i dt)^2.
Then K_ij = (1/2)(d_i beta_j + d_j beta_i) (overall sign irrelevant below) and the
Hamiltonian constraint gives the Eulerian density rho = (K^2 - K_ij K^ij)/(16 pi).
- Alcubierre: beta = v f(r) x_hat.
- Natario: beta = curl[(v/2) f(r) (0, -z, y)]; with f = 1 inside this is exactly v x_hat, and
  div beta = 0 everywhere (zero expansion).
Same tanh profile f(r) = [tanh(s(r+R)) - tanh(s(r-R))]/(2 tanh(sR)) for both.
Integrate rho over all space (axisymmetric about x): E = int 2 pi r^2 sin(th) rho dr dth.
Checks: Alcubierre result vs the 1D PF form E = -(v^2/12) int r^2 f'^2 dr; grid convergence.

Thick-wall floor: minimise int r^2 f'^2 dr with f(R)=1, f(R+D)=0 -> f' = -C/r^2,
C = R(R+D)/D, giving E_min = -(v^2/12) R(R+D)/D.  Verified numerically here.
"""
import math
import time

import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
v, R, s = sp.symbols("v R s", positive=True)
r = sp.sqrt(x**2 + y**2 + z**2)
f = (sp.tanh(s * (r + R)) - sp.tanh(s * (r - R))) / (2 * sp.tanh(s * R))
X = (x, y, z)


def rho_of(beta):
    K = sp.Matrix(3, 3, lambda i, j: sp.Rational(1, 2) * (sp.diff(beta[j], X[i]) + sp.diff(beta[i], X[j])))
    trK = K.trace()
    KK = sum(K[i, j] ** 2 for i in range(3) for j in range(3))
    return (trK**2 - KK) / (16 * sp.pi), trK


beta_alc = (v * f, 0, 0)
psi = (0, -(v / 2) * f * z, (v / 2) * f * y)
curl = (sp.diff(psi[2], y) - sp.diff(psi[1], z),
        sp.diff(psi[0], z) - sp.diff(psi[2], x),
        sp.diff(psi[1], x) - sp.diff(psi[0], y))
beta_nat = tuple(curl)

t0 = time.time()
rho_a, th_a = rho_of(beta_alc)
rho_n, th_n = rho_of(beta_nat)
# numerical check that Natario expansion vanishes
div_n = sp.lambdify((x, y, z, v, R, s), th_n, "numpy")
print("Natario div(beta) at sample points:", [float(div_n(*p, 1.0, 1.0, 5.0)) for p in [(0.3, 0.9, 0.1), (1.1, 0.2, -0.4)]])
fa = sp.lambdify((x, y, z, v, R, s), rho_a, "numpy")
fn = sp.lambdify((x, y, z, v, R, s), rho_n, "numpy")
fp = sp.lambdify((x, y, z, R, s), sp.diff(f, x), "numpy")  # f'(r) along x axis gives df/dr
print(f"symbolic setup {time.time()-t0:.1f} s")


def integrate(func, Rv, sv, nr, nth):
    rmax = Rv + 25.0 / sv
    # dense grid across the wall, coarser inside
    r_in = np.linspace(1e-6, max(Rv - 12.0 / sv, 1e-3), nr // 4)
    r_w = np.linspace(max(Rv - 12.0 / sv, 1e-3), rmax, nr)
    rr = np.unique(np.concatenate([r_in, r_w]))
    th = np.linspace(1e-6, math.pi - 1e-6, nth)
    RR, TT = np.meshgrid(rr, th, indexing="ij")
    xx, yy = RR * np.cos(TT), RR * np.sin(TT)
    val = func(xx, yy, 0.0 * xx, 1.0, Rv, sv)
    integrand = 2 * math.pi * RR**2 * np.sin(TT) * val
    return np.trapezoid(np.trapezoid(integrand, th, axis=1), rr)


def pf_1d(Rv, sv, n=200000):
    rr = np.linspace(1e-6, Rv + 25.0 / sv, n)
    fpr = fp(rr, 0.0 * rr, 0.0 * rr, Rv, sv)
    return -(1.0 / 12.0) * np.trapezoid(rr**2 * fpr**2, rr)


print("\nR = 1 m, v = 1 (geometric). Delta_PF ~ 2/sigma.")
print(f"{'sigma':>6} {'R/Delta':>8} {'E_alc(3D)':>12} {'E_alc(PF1D)':>12} {'E_nat':>12} {'nat/alc':>9} {'conv_nat':>9}")
rows = []
for sv in (4.0, 8.0, 16.0, 32.0, 64.0):
    n1, n2 = 3000, 4500
    ea = integrate(fa, 1.0, sv, n1, 241)
    en = integrate(fn, 1.0, sv, n1, 241)
    en2 = integrate(fn, 1.0, sv, n2, 361)
    e1 = pf_1d(1.0, sv)
    rows.append((sv, ea, en))
    print(f"{sv:6.0f} {sv/2:8.1f} {ea:12.4e} {e1:12.4e} {en:12.4e} {en/ea:9.2f} {abs(en2/en-1):9.1e}")

sig = np.array([r_[0] for r_ in rows]); EA = np.array([abs(r_[1]) for r_ in rows]); EN = np.array([abs(r_[2]) for r_ in rows])
pa = np.polyfit(np.log10(sig[-3:]), np.log10(EA[-3:]), 1)[0]
pn = np.polyfit(np.log10(sig[-3:]), np.log10(EN[-3:]), 1)[0]
print(f"\nlog-log slope dlog|E|/dlog(sigma) (thin-wall end): Alcubierre {pa:.2f}, Natario {pn:.2f}")
print("Thin-wall fits: |E_alc| ~ a*v^2 R^2 sigma ; |E_nat| ~ b*v^2 R^4 sigma^3 (checked by slope)")
a_coef = EA[-1] / sig[-1]
b_coef = EN[-1] / sig[-1] ** 3
print(f"  a = {a_coef:.4f} (expect 1/36 = {1/36:.4f} for tanh: v^2 R^2/(18 Delta) with Delta=2/sigma); b = {b_coef:.4f}")

# Reference case R = 100 m, Delta = 1 m (sigma = 2/m), v = 10
c4G = 299792458.0**4 / 6.67430e-11
c2G = 299792458.0**2 / 6.67430e-11
Rref, vref, Dref = 100.0, 10.0, 1.0
sref = 2.0 / Dref
Ea_ref = a_coef * vref**2 * Rref**2 * sref
En_ref = b_coef * vref**2 * Rref**4 * sref**3
print(f"\nReference R=100 m, v=10c, Delta=1 m: Alcubierre {Ea_ref*c2G:.2e} kg ; Natario (extrapolated R^4 sigma^3 law) {En_ref*c2G:.2e} kg ; ratio {En_ref/Ea_ref:.1e}")

# thick-wall floor check
print("\nThick-wall floor check (R = 1 m): optimal f' = -C/r^2 vs formula")
for D in (0.1, 1.0, 10.0):
    C = 1.0 * (1.0 + D) / D
    rr = np.linspace(1.0, 1.0 + D, 200001)
    Enum = (1 / 12) * np.trapezoid(rr**2 * (C / rr**2) ** 2, rr)
    print(f"  D = {D:5.1f}: numeric {Enum:.6f}, formula R(R+D)/(12 D) = {(1+D)/(12*D):.6f}")
print(f"total run time {time.time()-t0:.1f} s")
