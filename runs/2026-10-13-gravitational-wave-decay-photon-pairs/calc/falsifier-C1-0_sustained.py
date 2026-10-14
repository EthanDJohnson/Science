#!/usr/bin/env python3
"""Falsifier C1-0 (physics angle): does B&O's own model give a SUSTAINED pair rate?

Part A (natural units, w, sigma in one energy unit, time in its inverse):
  In the narrow-band model the pair amplitude depends on the pair energy K0 only through
  C(K0) = int da f(a) f(K0 - a)  (toolkit docstring; B&O S6). The conjugate variable of K0 is the
  emission time, and FT[C](t) = (FT f)(t)^2 = a(t)^2 (convolution theorem), so the time-resolved
  production weight is |a(t)|^4 and the total is J_f = int |C|^2 dK0 = 2 pi int |a(t)|^4 dt (Parseval).
  We compute (independently of the toolkit) J_f by direct convolution, the Parseval time integral,
  T_eff = 2 pi J_f / I_f^4, and the fraction of production at |t| > T for top-hat and Gaussian profiles.
Part B (SI): GW150914 at B&O's inputs: rate, T_eff, total, and the fraction of the model's own production
  made later than t_prop(410 Mpc), against the sustained reading R * t_prop.
Part C (symbolic): Lorentz scaling of a sustained count R * Delta t along a null ray under a boost along
  the propagation direction (N invariant; w, sigma and Delta t all scale by k = gamma (1 - beta)).
"""
import math
import numpy as np
import sympy as sp

print("=== Part A: time profile of production inside B&O's own model (natural units, w = 1) ===")
w = 1.0
for sigma in (0.05, 0.02):
    # top hat amplitude f = 1 on [w - s/2, w + s/2]
    n = 20001
    a = np.linspace(w - sigma, w + sigma, n)
    da = a[1] - a[0]
    f = ((a >= w - sigma / 2) & (a <= w + sigma / 2)).astype(float)
    If = f.sum() * da
    C = np.convolve(f, f) * da                      # C(K0) on grid of spacing da
    J = (C ** 2).sum() * da
    # time domain: a(t) = int f(k) e^{-ikt} dk, |a|^4 = (sigma sinc)^4
    t = np.linspace(-4000 / sigma, 4000 / sigma, 800001)
    dt = t[1] - t[0]
    at = sigma * np.sinc(sigma * t / (2 * math.pi))  # |int_{w-s/2}^{w+s/2} e^{-ikt} dk| = sigma |sinc(sigma t/2)|
    J_time = (at ** 4).sum() * dt / (2 * math.pi)   # Parseval with a(t) = int f e^{-ikt} dk: J_f = (1/2pi) int |a|^4 dt
    Teff = 2 * math.pi * J / If ** 4
    print(f"tophat sigma={sigma}: J_f(conv) = {J:.6e}, (1/2pi) int|a|^4 dt = {J_time:.6e}, analytic 2 s^3/3 = {2*sigma**3/3:.6e}")
    print(f"   T_eff = 2 pi J_f/I_f^4 = {Teff:.6f} (1/energy); 4 pi/(3 sigma) = {4*math.pi/(3*sigma):.6f}")
    tot = (at ** 4).sum()
    for Tm in (1, 3, 10, 30, 100, 1000):
        frac = (at[np.abs(t) > Tm / sigma] ** 4).sum() / tot
        print(f"   fraction of production at |t| > {Tm:>5}/sigma: {frac:.3e}   (analytic 3/(pi (sigma T)^3) = {3/(math.pi*Tm**3):.3e})")
# analytic asymptotic tail for top hat: |a|^4 = s^4 sinc^4(s t/2) ~ 16 sin^4/t^4, cycle average 6/t^4
# fraction beyond |t| > T = (2 int_T^inf 6/t^4 dt) / (int |a|^4 dt = 2 pi J_f = 4 pi s^3/3) = 3/(pi (s T)^3)
print("top-hat analytic tail fraction beyond |t| > T: 3/(pi (sigma T)^3) (cycle-averaged)")
# Gaussian amplitude profile exp(-(k-w)^2/(2 s^2)) -> |a(t)|^4 ~ exp(-2 s^2 t^2)
s = 1.0
for Tm in (1, 2, 3, 5):
    frac = math.erfc(math.sqrt(2) * Tm)
    print(f"gaussian: fraction of production at |t| > {Tm}/sigma = erfc(sqrt2 * {Tm}) = {frac:.3e}")

print()
print("=== Part B: GW150914 at B&O inputs (SI) ===")
G = 6.67430e-11; c = 2.99792458e8; Msun = 1.98892e30; pc = 3.0856775814913673e16
E = 2 * Msun * c ** 2           # J
f0 = 150.0                      # Hz
wr = 2 * math.pi * f0           # rad/s
sig = 200.0                     # rad/s
R = 3 * G ** 2 * E ** 2 * wr * sig ** 2 / (25 * math.pi * c ** 10)   # pairs/s (hbar-free form of eq. 8)
Teff = 4 * math.pi / (3 * sig)
P = R * Teff
D = 410e6 * pc
tprop = D / c
print(f"E = {E:.4e} J, R(eq.8) = {R:.4e} pairs/s, T_eff = {Teff:.5f} s, P_total = R T_eff = {P:.4e} pairs")
print(f"t_prop(410 Mpc, Euclidean) = {tprop:.4e} s; sustained reading R t_prop = {R*tprop:.4e} pairs; over-count = {R*tprop/P:.3e}")
print(f"sigma t_prop = {sig*tprop:.4e}; model's own fraction of production after t_prop (top hat, 3/(pi (s t)^3)) = {3/(math.pi*(sig*tprop)**3):.3e}")
print(f"   -> pairs made at |t| > t_prop inside B&O's own model = {P*3/(math.pi*(sig*tprop)**3):.3e} (vs sustained {R*tprop:.3e})")
hbar = 1.054571817e-34
print(f"energy fraction removed over whole history: 2 hbar w P / E = {2*hbar*wr*P/E:.3e}; sustained reading 2 hbar w R t_prop / E = {2*hbar*wr*R*tprop/E:.3e}")
# what a true sustained process would do to the S-matrix total: P(T) = R T diverges
for T in (1.0, 1e3, 1e9, tprop):
    print(f"   sustained decay would give in-out total R*T at T = {T:.2e} s: {R*T:.3e} (B&O S-matrix total stays {P:.3e})")

print()
print("=== Part C: Lorentz scaling of a sustained path count (symbolic) ===")
k, Nn, ww, ss, Dt, Gs = sp.symbols('k N omega sigma Delta_t G', positive=True)
Rexpr = sp.Rational(3, 25) / sp.pi * Gs ** 2 * Nn ** 2 * ww ** 3 * ss ** 2
count = Rexpr * Dt
count_b = count.subs({ww: k * ww, ss: k * ss, Dt: k * Dt}, simultaneous=True)
print("count = R*Delta_t =", count)
print("boosted/original =", sp.simplify(count_b / count), " (N invariant; w, sigma, Delta_t along the null ray scale by k)")
# check the null-ray time scaling explicitly
beta = sp.symbols('beta', positive=True)
gam = 1 / sp.sqrt(1 - beta ** 2)
t_ = sp.symbols('t', positive=True)
tprime = sp.simplify(gam * (t_ - beta * t_))       # event (t, z = t)
wprime = sp.simplify(gam * (1 - beta))             # w'/w for a wave moving along +z
print("t'/t on the ray =", sp.simplify(tprime / t_), "; w'/w =", wprime, "; equal:", sp.simplify(tprime / t_ - wprime) == 0)
P_tot_b = (Rexpr * 1 / ss).subs({ww: k * ww, ss: k * ss}, simultaneous=True) / (Rexpr / ss)
print("total P = R*T_eff ~ G^2 N^2 w^3 sigma scales as", sp.simplify(P_tot_b), "-> defined only in the packet's CM frame (B&O state has zero net momentum)")
for kv in (0.1, 10.0):
    print(f"   k = {kv}: sustained count changes by factor {kv**6:.1e}; a Lorentz-invariant pair count cannot")
