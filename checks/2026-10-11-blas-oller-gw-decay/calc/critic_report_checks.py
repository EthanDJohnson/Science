"""Critic pass: small derived numbers quoted in report.md that no other script prints.

(1) B&O's validity condition tau << 1/sigma ~ t_m for the GW150914-like anchors (E_rel = 2 Msun c^2,
    nu = 150 Hz, t_m = 5 ms), with and without B&O's CMB stimulation factor (1 + 2f), which B&O apply
    "in all the previous formulae" (so tau -> tau/(1 + 2f)).  Also c*tau for footnote 4.
(2) B&O switch profile between eq. 5 (Gaussian) and eqs. 7/S6 (top hat): ratio of the two eq.-8-type
    coefficients at equal N and equal sigma parameter, taken from taskC1 section (e) closed forms.
Independent constants (CODATA 2018), plain arithmetic; no imports from other check scripts.
"""
import math

G, c, hbar, kB, Msun = 6.67430e-11, 2.99792458e8, 1.054571817e-34, 1.380649e-23, 1.98847e30
E = 2 * Msun * c**2
nu = 150.0
w = 2 * math.pi * nu
tm = 5e-3
eps = 0.15  # not used for tau; B&O's tau uses sigma_w = 1/t_m-type bandwidth below
# B&O eq. 10 in SI: tau = 25 pi c^10 / (6 G^2 E^2 w delta^2) with delta = 1/t_m (their sigma ~ 1/delta t)
delta = 1 / tm
tau = 25 * math.pi * c**10 / (6 * G**2 * E**2 * w * delta**2)
f = 1 / math.expm1(hbar * w / (kB * 2.7255))
tau_st = tau / (1 + 2 * f)
lam = c / nu
print("(1) GW150914-like anchors: E_rel = 2 Msun c^2, nu = 150 Hz, t_m = 5 ms, sigma = 1/t_m")
print(f"   tau (eq. 10, vacuum) = {tau:.4e} s;  tau/t_m = {tau/tm:.3e}")
print(f"   CMB f(150 Hz) = {f:.4e};  1 + 2f = {1+2*f:.4e}")
print(f"   tau with (1 + 2f) = {tau_st:.4e} s;  tau/t_m = {tau_st/tm:.3e}")
print(f"   c tau (vacuum) = {c*tau:.4e} m = {c*tau/lam:.3e} wavelengths;  c tau (stimulated) = {c*tau_st:.4e} m = {c*tau_st/lam:.3e} wavelengths (lambda = {lam/1e3:.1f} km)")

# (2) profile dependence (taskC1 (e) closed forms, re-evaluated)
R0_ratio = 4 * math.pi
Ptot_tophat = 4 / 25
Ptot_gauss = 6 * math.sqrt(2) * math.sqrt(math.pi) / 25
print("(2) profile dependence at equal N and equal sigma parameter (taskC1 (e) closed forms):")
print(f"   peak-rate ratio Gaussian/top-hat = 4 pi = {R0_ratio:.4f};  P_tot: top hat {Ptot_tophat:.5f}, Gaussian {Ptot_gauss:.5f} G^2N^2w^3sig (ratio {Ptot_gauss/Ptot_tophat:.4f})")
