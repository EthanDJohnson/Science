#!/usr/bin/env python3
"""Task A(3), part 1: B&O eq. S6 evaluated within THEIR model and approximations (narrow band, |k_i| = omega_s in
denominators, 2 pi delta(0) -> T, top-hat f = Theta with Theta^2 = 2 pi^2 N/(omega sigma), real eq.-6 amplitudes
summed as in eq. 7).  Does eq. 8, dP/dt = 3 G^2 N^2 omega^3 sigma^2/(25 pi), follow?

(a) exact symbolic evaluation (sympy);  (b) Monte-Carlo check of the ring Jacobian used in (a);
(c) the same coefficient from the numerical ring engine (bo_ring) that is later fed with physical amplitudes;
(d) what replacing 2 pi delta(0) -> T hides: the exact in-out total for the top-hat packet (no delta(0)).
Quantities: dP/dt is B&O's 'probability per unit time' (in-out probability of a photon PAIR final state, which at
this order equals the mean number of pairs; photons = 2 x pairs); P_total is the same quantity integrated over the
whole history of the packet."""
import math
import os
import sys

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bo_common as bc  # noqa: E402
import bo_ring as br  # noqa: E402

PI = math.pi
print("=" * 100)
print("(a) symbolic evaluation of eq. S6 with B&O's integrand (s^2 - 2tu)(s'^2 - 2t'u')/(s s')")
print("=" * 100)
G, N, w, sg, K, al, th, ph, c, Theta = sp.symbols("G N omega sigma K alpha theta phi c Theta", positive=True)
# normalisation of the top-hat: N = sum_l int d^3k/((2pi)^3 2k) |f_l|^2 with both helicities = Theta
Nexpr = 2 * Theta ** 2 * 4 * sp.pi * w * sg / (16 * sp.pi ** 3)
Theta2 = sp.solve(sp.Eq(Nexpr, N), Theta ** 2)
print("Theta^2 from N = 2 helicities x int dk~ Theta^2  ->", Theta2, " (B&O: 2 pi^2 N/(omega sigma))")
Th2 = 2 * sp.pi ** 2 * N / (w * sg)
s = 4 * w ** 2 - K ** 2
cc = sp.sin(th) * sp.cos(ph - al)                     # cosine between photon (CM) and graviton axis on the ring
integrand_ring = sp.integrate((s / 2) * (1 + cc ** 2), (al, 0, 2 * sp.pi))        # (t^2+u^2)/s = (s/2)(1+c^2)
integrand_ring = sp.simplify(integrand_ring)
print("int d alpha (t^2+u^2)/s =", integrand_ring)
ang = sp.integrate(sp.integrate(integrand_ring ** 2 * sp.sin(th), (th, 0, sp.pi)), (ph, 0, 2 * sp.pi))
ang = sp.simplify(ang)
print("int dOmega_gamma [int d alpha (t^2+u^2)/s]^2 =", sp.factor(ang))
jac = (w * sg) ** 2 / K                                # int d^3k over the ring = (omega sigma)^2/K int d alpha
pref = G ** 2 / (16384 * sp.pi ** 9 * w ** 4)          # eq. S6 prefactor
dPdt = pref * Th2 ** 2 * sp.integrate(4 * sp.pi * K ** 2 * jac ** 2 * ang, (K, 0, 2 * w))
dPdt = sp.simplify(dPdt)
print("dP/dt from eq. S6 =", dPdt, " ; coefficient of G^2 N^2 omega^3 sigma^2 =",
      sp.nsimplify(sp.simplify(dPdt / (G ** 2 * N ** 2 * w ** 3 * sg ** 2))),
      " ; B&O eq. 8: 3/(25 pi)")

print("\n" + "=" * 100)
print("(b) Monte-Carlo check of the ring volume  V(K) = vol{k : |K/2 - k|, |K/2 + k| in [w - sg/2, w + sg/2]}")
print("    claimed exactly 2 pi (w sg)^2/K for sg < K < 2w - sg")
print("=" * 100)
rng = np.random.default_rng(7)
wv, sgv = 1.0, 0.02
for Kv in (0.3, 1.0, 1.7):
    Kvec = np.array([0, 0, Kv])
    # sample k in a box around the ring (|k_par| <= sg/K + small, rho around sqrt(w^2 - K^2/4))
    rho0 = math.sqrt(wv ** 2 - Kv ** 2 / 4)
    hpar = 1.2 * wv * sgv / Kv + 0.01
    hrho = 1.2 * sgv / (rho0 / wv) + 0.01
    n = 4_000_000
    kpar = rng.uniform(-hpar, hpar, n)
    rho = rng.uniform(rho0 - hrho, rho0 + hrho, n)
    a = np.sqrt(Kv ** 2 / 4 - Kv * kpar + kpar ** 2 + rho ** 2)
    b = np.sqrt(Kv ** 2 / 4 + Kv * kpar + kpar ** 2 + rho ** 2)
    inside = (np.abs(a - wv) <= sgv / 2) & (np.abs(b - wv) <= sgv / 2)
    vol = 2 * PI * np.mean(inside * rho) * (2 * hpar) * (2 * hrho)
    err = 2 * PI * np.std(inside * rho) * (2 * hpar) * (2 * hrho) / math.sqrt(n)
    print(f"   K = {Kv}: MC volume = {vol:.6e} +- {err:.1e};  2 pi (w sg)^2/K = {2*PI*(wv*sgv)**2/Kv:.6e}")

print("\n" + "=" * 100)
print("(c) numerical ring engine with B&O's real amplitudes (validates the engine normalisation used for physics)")
print("=" * 100)
ref = 3 / (25 * PI)
C = br.coefficient(lambda k1, k2, q1, q2, s_: br.m_photon_bo(k1, k2, q1, q2, s_, "bo_plus"),
                   NK=8, NthK=4, nth=8, nph=16, na=32)
print(f"   isotropic top-hat, B&O model: C = {C:.12f};  3/(25 pi) = {ref:.12f};  ratio = {C/ref:.12f}")
Clin = br.coefficient(lambda k1, k2, q1, q2, s_: br.m_photon_bo(k1, k2, q1, q2, s_, "linear"),
                      NK=12, NthK=12, nth=8, nph=24, na=48, splitK=False)
Clin2 = br.coefficient(lambda k1, k2, q1, q2, s_: br.m_photon_bo(k1, k2, q1, q2, s_, "linear"),
                       NK=16, NthK=16, nth=10, nph=32, na=64, splitK=False)
print(f"   linear-quadrupole profile f_+ = f_- = (sin^2 th/2)/norm, B&O model: C = {Clin:.10f} (finer grid {Clin2:.10f});"
      f"  C/(3/(25 pi)) = {Clin2/ref:.6f}")

print("\n" + "=" * 100)
print("(d) the exact energy delta instead of 2 pi delta(0) -> T (same model, same narrow band)")
print("=" * 100)
x = sp.symbols("x", real=True)
# density at 0 of d1 + d2 - d1' - d2', each uniform on [-1/2, 1/2] (unit width): Irwin-Hall n = 4 at its centre
u = sp.Piecewise((1, sp.And(x >= -sp.Rational(1, 2), x <= sp.Rational(1, 2))), (0, True))
y = sp.symbols("y", real=True)
tri = sp.Piecewise((1 - sp.Abs(y), sp.Abs(y) <= 1), (0, True))           # density of d1 + d2 (and of -(d1'+d2'))
dens0 = sp.integrate((1 - sp.Abs(y)) ** 2, (y, -1, 1))                   # (tri * tri)(0)
print(f"   int d^4(delta k) delta(d1 + d2 - d1' - d2') over the band^4 = sigma^3 x {dens0}  (Irwin-Hall density at 0)")
rngv = rng.uniform(-0.5, 0.5, size=(4, 2_000_000))
X = rngv[0] + rngv[1] - rngv[2] - rngv[3]
h = 0.01
print(f"   Monte Carlo density of d1+d2-d1'-d2' at 0: {np.mean(np.abs(X) < h/2)/h:.4f}")
Teff = 2 * sp.pi * dens0                                                  # in units of 1/sigma
print(f"   => P_total = (dP/dt) x T_eff with T_eff = 2 pi x {dens0}/sigma = {sp.simplify(Teff)}/sigma = {float(Teff):.4f}/sigma")
print(f"   => P_total (mean number of photon PAIRS over the whole packet history, B&O model) = "
      f"{sp.nsimplify(sp.Rational(3, 25) / sp.pi * Teff)} G^2 N^2 omega^3 sigma"
      f" = {float(3/(25*PI)*Teff):.6f} G^2 N^2 omega^3 sigma;  photons = 2 x pairs.")
