"""Falsifier C7-0: Diosi-Penrose decoherence time for the QGEM geometry as a function of the free R0.

SI units throughout.
Model: uniform diamond sphere (m = 1e-14 kg, rho = 3510 kg/m^3) whose mass density is convolved with a
Gaussian of width R0 (Donadi/Figurato smearing mu ~ exp(-r^2/(2 R0^2))). Granular (lattice) structure is
neglected, which the candidate itself shows is negligible (M-CONSTRAINTS-14).
Candidate's convention (M-CONSTRAINTS-14): E_G(d) = G * Int Int drho drho'/|r-r'| / 2 ... which for R0 -> 0 and d >= 2R
reduces to E_G = G m^2 (6/(5R) - 1/d).  In Fourier space:
   E_G(d) = G m^2 (2/pi) Int_0^inf dk F(kR)^2 exp(-k^2 R0^2) (1 - sin(kd)/(kd)),
   F(x) = 3 (sin x - x cos x)/x^3  (form factor of a uniform sphere).
tau_DP = hbar / E_G.  The ratio tau(R0)/tau(R0->0) is independent of the factor-2 convention.
Also: QGEM entangling phase for comparison (Bose et al. geometry, closest approach 200 um, split 250 um):
   dphi = G m^2 t / (hbar) * (1/d_close - 1/d_far) using the two-arm pair with the largest phase difference.
"""
import numpy as np
from scipy.integrate import quad

G = 6.67430e-11      # m^3 kg^-1 s^-2
hbar = 1.054571817e-34  # J s
m = 1e-14            # kg
rho = 3510.0         # kg/m^3
R = (3 * m / (4 * np.pi * rho)) ** (1 / 3)  # m
d = 250e-6           # m, superposition size


def F(x):
    x = np.asarray(x, dtype=float)
    out = np.where(np.abs(x) < 1e-3, 1 - x**2 / 10, 3 * (np.sin(x) - x * np.cos(x)) / np.where(x == 0, 1, x) ** 3)
    return out


def EG(R0, d=d):
    # integrate in u = k R ; dk = du/R
    def integrand(u):
        k = u / R
        return float(F(u) ** 2 * np.exp(-(k * R0) ** 2) * (1 - np.sinc(k * d / np.pi)))
    # split the range for oscillatory convergence
    umax = 400.0 if R0 < R else min(400.0, 12 * R / R0 + 50)
    edges = np.linspace(0, umax, 4001)
    tot = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        tot += quad(integrand, a, b, limit=200)[0]
    return G * m**2 * (2 / np.pi) * tot / R


print(f"Inputs (SI): m = {m:.3e} kg, rho = {rho} kg/m^3, R = {R:.4e} m, d = {d:.3e} m")
analytic0 = G * m**2 * (6 / (5 * R) - 1 / d)
print(f"Analytic R0->0 E_G = G m^2 (6/(5R) - 1/d) = {analytic0:.4e} J, tau = {hbar/analytic0*1e3:.3f} ms")
# convergence check on the analytic limit: use tiny R0 and the tail correction
num0 = EG(1e-12)
print(f"Numerical E_G at R0 = 1e-12 m: {num0:.4e} J (ratio to analytic {num0/analytic0:.5f}; residual is the truncated 1/u^4 tail)")

print("\nR0 (m)      E_G (J)       tau_DP (s)    tau/tau0")
tau0 = hbar / num0
rows = []
for R0 in [4e-10, 1e-8, 1e-7, 5e-7, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4]:
    e = EG(R0)
    tau = hbar / e
    rows.append((R0, e, tau))
    print(f"{R0:9.2e}  {e:12.4e}  {tau:12.4e}  {tau/tau0:10.3e}")

# Gaussian-blob closed form check for R0 >> R: E_G = G m^2 [1/(sqrt(pi) s) - erf(d/(2 s))/d], s^2 = R0^2 + R^2/5*... use s = R0
from math import erf, sqrt, pi
for R0 in [3e-5, 1e-4]:
    s = R0
    eg = G * m**2 * (1 / (sqrt(pi) * s) - erf(d / (2 * s)) / d)
    print(f"Gaussian-blob closed form at R0 = {R0:.0e} m: E_G = {eg:.4e} J, tau = {hbar/eg:.3e} s")

# QGEM phase accumulation for comparison (both conventions of the lens: 200 um closest approach)
dmin = 200e-6
dmax = dmin + 2 * d  # far arms (200/700 um convention of the dossier)
rate = G * m**2 / hbar * (1 / dmin - 1 / dmax)  # rad/s, differential phase rate between closest and farthest arm pairs
print(f"\nQGEM differential phase rate (200/700 um convention): {rate:.4f} rad/s")
for R0, e, tau in rows:
    # entangling phase accrued within one DP decoherence time
    print(f"R0 = {R0:9.2e} m: phase accrued in tau_DP = {rate*tau:.4e} rad; coherence remaining at t = 1 s: exp(-1/tau) = {np.exp(-1/tau):.3e}")
