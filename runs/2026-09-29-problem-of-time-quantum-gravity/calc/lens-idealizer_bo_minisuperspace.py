#!/usr/bin/env python3
"""Idealizer lens, model M2: one heavy "minisuperspace" variable x + light system S under ONE constraint

    [ -(1/(2M)) d^2/dx^2 - M e(x) + H_S ] Psi(x) = 0          (hbar = 1, dimensionless model units)

M plays the role of m_P^2 (Wheeler-DeWitt: heavy gravitational sector), x the scale factor, H_S the matter
Hamiltonian. Exact solution for constant e(x) = e0:  Psi = sum_n c_n exp(i k_n x)|n>,  k_n = sqrt(2M(M e0 - E_n)).
Born-Oppenheimer/WKB: classical heavy velocity v = sqrt(2 e0), semiclassical time t = x / v.
  order M^0 : i d/dt chi = H_S chi                     (Schroedinger equation emerges)
  order M^-1: i d/dt chi = [H_S + H_S^2/(2 M v^2)] chi  (Kiefer-Singh-type correction, square of H_S)
Parts
 A. fidelity of emergent Schroedinger evolution vs exact conditional state, and scaling with M
 B. x-dependent e(x): Schroedinger-norm populations drift (apparent non-unitarity) at O(E/(M e)),
    while the Klein-Gordon current k_n |a_n|^2 is conserved -> facet 3 (inner product) shows up at O(1/M)
 C. turning point (facet 4, global time): linear e(x) = e0 - g x; Airy width l = (2 M^2 g)^(-1/3),
    WKB-time breakdown window in semiclassical time Delta t ~ sqrt(2 l / g) ~ M^(-1/3)
 D. multiple choice (facet 2): two heavy variables; correction term depends on which one is the clock
"""
import numpy as np
from scipy.special import airy
from scipy.integrate import solve_ivp

ES = np.array([0.0, 1.0, 2.5])          # system energies (model units)
c = np.array([1.0, 1.0, 1.0]) / np.sqrt(3)
e0 = 50.0                                # heavy-sector energy per unit M
v = np.sqrt(2 * e0)

def exact_cond(M, t):
    x = v * t
    k = np.sqrt(2 * M * (M * e0 - ES))
    ph = np.exp(1j * (k - k[0]) * x)      # remove common phase (global phase of heavy WKB wave)
    return c * ph

def schr(t, H):
    return c * np.exp(-1j * H * t)

def fid(a, b):
    return abs(np.vdot(a, b)) ** 2 / (np.vdot(a, a).real * np.vdot(b, b).real)

print("=== A. emergent Schroedinger time vs exact solution (e0=50, E_S = 0, 1, 2.5; t = 10) ===")
t = 10.0
print(" M        1-F(order M^0)   1-F(order M^-1)  predicted 1-F0 ~ t^2 Var(H^2)/(2Mv^2)^2")
H2 = ES ** 2
var = np.sum(np.abs(c) ** 2 * H2 ** 2) - np.sum(np.abs(c) ** 2 * H2) ** 2
prev = None
for M in (1e1, 1e2, 1e3, 1e4, 1e5):
    ex = exact_cond(M, t)
    f0 = 1 - fid(ex, schr(t, ES - ES[0]))
    f1 = 1 - fid(ex, schr(t, ES + ES ** 2 / (2 * M * v ** 2) - (ES[0] + ES[0] ** 2 / (2 * M * v ** 2))))
    pred = t ** 2 * var / (2 * M * v ** 2) ** 2
    print(f" {M:8.0e}  {f0:.4e}       {f1:.4e}       {pred:.4e}")
print(" -> 1-F0 ~ M^-2 (phase error ~ E^2 t/(2 M v^2)); first-order correction removes it to ~M^-4")

print("\n=== B. slowly varying heavy potential: Schroedinger norm vs KG current (M=100) ===")
M = 100.0
def e_of_x(x):
    return e0 * (1 + 0.5 * np.tanh((x - 50) / 20))   # heavy kinetic energy changes by factor 3 over the run
for x in (0.0, 50.0, 100.0):
    k = np.sqrt(2 * M * (M * e_of_x(x) - ES))
    a2 = np.abs(c) ** 2 * k[0] / k * 1.0          # WKB amplitude^2 ~ 1/k with KG current fixed = |c|^2 k0
    # normalise Schroedinger populations
    pS = a2 / a2.sum()
    print(f" x={x:5.1f}: heavy e(x)={e_of_x(x):6.2f}  Schroedinger populations {np.round(pS, 7)}  KG-current weights {np.round(np.abs(c)**2,7)}")
print(" -> population drift between x=0 and x=100 is O(E/(M e)) ~",
      f"{(ES[2]-ES[0])/(2*M*e0):.1e} x (fractional change of e) : apparent non-unitarity in the Schroedinger norm")

# numerical confirmation of WKB populations by integrating the exact ODE for each component
M = 3.0   # smaller M keeps the ODE cheap (k ~ 30, ~3000 rad of phase); WKB still accurate
print(f" numeric check (ODE, M={M}): current conserved, and |psi|^2 follows WKB k0/k?")
for n in (0, 2):
    def rhs(x, y):
        psi, dpsi = y[0] + 1j * y[1], y[2] + 1j * y[3]
        dd = -2 * M * (M * e_of_x(x) - ES[n]) * psi
        return [dpsi.real, dpsi.imag, dd.real, dd.imag]
    k0 = np.sqrt(2 * M * (M * e_of_x(0.0) - ES[n]))
    sol = solve_ivp(rhs, (0, 100), [1, 0, 0, k0], method="DOP853", rtol=1e-10, atol=1e-12)
    psi_end = sol.y[0, -1] + 1j * sol.y[1, -1]
    dpsi_end = sol.y[2, -1] + 1j * sol.y[3, -1]
    J_end = (np.conj(psi_end) * dpsi_end).imag
    kend = np.sqrt(2 * M * (M * e_of_x(100.0) - ES[n]))
    print(f"  n={n}: current start {k0:.6f}, end {J_end:.6f}; |psi|^2 end {abs(psi_end)**2:.6f} vs WKB k0/k_end {k0/kend:.6f}")

print("\n=== C. turning point: Airy width and breakdown of semiclassical time ===")
g = 1.0
for M in (1e1, 1e2, 1e3, 1e4):
    ell = (2 * M ** 2 * g) ** (-1 / 3)
    dt_break = np.sqrt(2 * ell / g)
    print(f" M={M:7.0e}: Airy width l={ell:.4e} (x units), semiclassical-time window ~ {dt_break:.4e}, l*M^(2/3)={ell*M**(2/3):.4f}")
# check: WKB phase vs exact Airy at s = distance/l from turning point
for s in (1.0, 3.0, 10.0):
    z = -s
    ai, _, bi, _ = airy(z)
    zeta = (2 / 3) * s ** 1.5
    wkb = np.sin(zeta + np.pi / 4) / (np.sqrt(np.pi) * s ** 0.25)
    print(f"  s={s:5.1f} l from turning point: Ai={ai:+.5f}, WKB={wkb:+.5f}, rel.err={abs(ai-wkb)/np.sqrt(ai**2+bi**2):.2e} (asymptotic 5/(72 zeta)={5/(72*zeta):.2e})")

print("\n=== D. multiple choice: which heavy variable is the clock ===")
Mx, ex_, My, ey_ = 100.0, 50.0, 300.0, 5.0      # two heavy sectors with different kinetic energies
Kx, Ky = Mx * 2 * ex_, My * 2 * ey_             # M v^2 for each
print(f" correction H_S^2/(2 M v^2): clock x -> 1/(2 M v^2) = {1/(2*Kx):.3e}; clock y -> {1/(2*Ky):.3e}")
print(" the two deparametrizations agree at O(M^0) and differ at O(E_S/(M v^2)); relative phase after t=10 for E=2.5:",
      f"{abs(2.5**2*(1/(2*Kx)-1/(2*Ky))*10):.3e} rad")
