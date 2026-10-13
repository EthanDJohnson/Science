#!/usr/bin/env python3
"""Task C(2) and C(4): what B&O do with dP/dt (eqs. 9-12, S7, binaries, eq. 19/S12) versus the finite in-out total.

Inputs from taskC1 (B&O's own model, narrow band):  (dP/dt)_BO = R(0) = 3 G^2 N^2 w^3 sig^2/(25 pi)  [pairs per unit time at the
focus],  P_tot = R(0) x 4 pi/(3 sig) = (4/25) G^2 N^2 w^3 sig  [pairs, whole history of the packet], time profile
R(t) = R(0) sinc^4(sig t/2);  chirped packet of duration D >> 2 pi/sig:  P_tot -> (3 pi/(sig D)) x transform-limited value.
(a) symbolic algebra of eqs. 9, 10, 11, S7 (+ Poisson remark);  (b) SB's depletion example;  (c) eq. 19 / S12 energy per event;
(d) the inspiral bins (chirp);  (e) the merger.
"""
import math

import numpy as np
import sympy as sp
from scipy import constants as K_

PI = math.pi
hbar_eVs = K_.hbar / K_.e                     # eV s
MP_eV = math.sqrt(K_.hbar * K_.c ** 5 / K_.G) / K_.e   # Planck energy (non-reduced), eV
G_nat = 1.0 / MP_eV ** 2                      # eV^-2
Msun_eV = 1.98847e30 * K_.c ** 2 / K_.e      # eV
yr = 365.25 * 86400
t_univ = 13.8e9 * yr                          # s
H0 = 67.4e3 / 3.0857e22                       # s^-1
Om, Orad = 0.315, 9.1e-5
OL = 1 - Om - Orad


def Hz(z):
    return H0 * math.sqrt(Om * (1 + z) ** 3 + Orad * (1 + z) ** 4 + OL)


print("=" * 110)
print("(a) algebra (sympy)")
print("=" * 110)
G, N, N0, w, sg, t, E = sp.symbols("G N N_0 omega sigma t E", positive=True)
kap = 3 * G ** 2 * w ** 3 * sg ** 2 / (25 * sp.pi)          # (dP/dt)/N^2, pairs
Ng_lin = 2 * kap * N0 ** 2 * t                               # each reaction: 2 photons
eq9 = G ** 2 * N0 ** 2 * 6 * w ** 3 * sg ** 2 * t / (25 * sp.pi)
print(f"   2 x (dP/dt) x t - eq.9 = {sp.simplify(Ng_lin - eq9)}")
Nf = sp.Function("Nf")
sol = sp.dsolve(sp.Eq(Nf(t).diff(t), -2 * kap * Nf(t) ** 2), Nf(t), ics={Nf(0): N0})
Ng_ode = sp.simplify(N0 - sol.rhs)
S7 = (G ** 2 * N0 ** 2 * 6 * w ** 3 * sg ** 2 * t / (25 * sp.pi)) / (1 + 6 * G ** 2 * N0 * w ** 3 * sg ** 2 * t / (25 * sp.pi))
print(f"   ODE dN/dt = -2 (dP/dt)(N) solved: N_gamma = {Ng_ode};   minus S7 = {sp.simplify(Ng_ode - S7)}")
tau = sp.solve(sp.Eq(eq9, 1), t)[0]
eq10 = 25 * sp.pi / (6 * G ** 2 * E ** 2 * w * sg ** 2)
print(f"   eq.9 = 1 photon at t = {tau};  minus eq.10 (E_rel = N0 w) = {sp.simplify(tau - eq10.subs(E, N0*w))}"
      "   -> tau is the mean time per PHOTON (half a reaction)")
tau_h = sp.solve(sp.Eq(eq9, N0), t)[0]
print(f"   eq.9 = N0 at t = tau_h = {tau_h};  tau_h/tau = {sp.simplify(tau_h/tau)} (= E_rel/w_s, as in SB);  "
      f"S7 at tau_h: N_gamma/N0 = {sp.simplify(S7.subs(t, tau_h)/N0)}")
W = sp.simplify(w * sp.diff(eq9, t))
eq11 = 6 * G ** 2 * E ** 2 * w ** 2 * sg ** 2 / (25 * sp.pi)
print(f"   W = w dN_gamma/dt = {W};  minus eq.11 = {sp.simplify(W - eq11.subs(E, N0*w))}")
print(f"   photons expected within T = 1/sig: (1/sig)/tau = 1/(sig tau) -> relative Poisson error sqrt(sig tau)  (B&O: sqrt(sig tau))")
Ptot = sp.Rational(4, 25) * G ** 2 * N0 ** 2 * w ** 3 * sg
Ng_tot = 2 * Ptot
print(f"   in-out total photons N_gamma,tot = 2 P_tot = {Ng_tot} = {sp.simplify(Ng_tot*sg*tau)} /(sig tau)")
print(f"   fraction of the packet ever converted = N_gamma,tot/N0 = {sp.simplify(Ng_tot/N0*sg*tau_h)} /(sig tau_h)")
print(f"   eq.9 exceeds the in-out total for t > {sp.simplify(sp.solve(sp.Eq(eq9, Ng_tot), t)[0]*sg)}/sig")

print("\n" + "=" * 110)
print("(b) SB example: E_rel = M_sun c^2, eps = 0.15 (sig = eps w_s): 'tau_h shorter than the age of the universe for w_s >~ 1e4 eV'")
print("=" * 110)
E_rel = Msun_eV
eps = 0.15


def times(ws):
    sig = eps * ws
    tau_ = 25 * PI / (6 * G_nat ** 2 * E_rel ** 2 * ws * sig ** 2) * hbar_eVs      # s
    N0_ = E_rel / ws
    tauh = tau_ * N0_
    return tau_, tauh, hbar_eVs / sig, N0_


ws_star = (25 * PI / (6 * G_nat ** 2 * E_rel * eps ** 2) * hbar_eVs / t_univ) ** 0.25
print(f"   w_s with tau_h = 13.8 Gyr: {ws_star:.3e} eV   (B&O: ~1e4 eV)")
for ws in (1e4, ws_star):
    tau_, tauh, isig, N0_ = times(ws)
    frac = (4 * PI / 3) * isig / tauh
    print(f"   w_s = {ws:.3e} eV: N0 = {N0_:.3e}, tau = {tau_:.3e} s, tau_h = {tauh:.3e} s, 1/sig = {isig:.3e} s;"
          f"  fraction of packet ever converted = (4pi/3)/(sig tau_h) = {frac:.3e} (in-out photons N0 x that = {N0_*frac:.3e})")
# w_s for which the whole packet would be converted within its own lifetime: sig tau_h = 4 pi/3
ws_dep = (75 / (24 * G_nat ** 2 * E_rel * eps)) ** (1 / 3)
print(f"   w_s needed for (4pi/3)/(sig tau_h) = 1 (depletion within the packet, B&O model): {ws_dep:.3e} eV")

print("\n" + "=" * 110)
print("(c) eq. 19 / S12: each event radiates W_gamma for the whole propagation time (E_j ~ W_gamma x int dz'/H).")
print("    In B&O's own model the energy per event is w_s x 2 P_tot = W_gamma x 4 pi/(3 sig).  Ratio ~ 3 sig/(4 pi H(z))")
print("    (order of magnitude: propagation time taken as 1/H(z) at the injection redshift; eps = 0.1, ratio scales as eps)")
print("=" * 110)
eps_c = 0.1
zs = (0, 1e3, 1e5, 2e6)
print("   w_s [eV]   " + "".join(f"  z={z:<9.0e}" for z in zs) + "   (ratio; bound on sqrt(Gamma) eps E_rel too strong by sqrt(ratio))")
for ws in (1e-10, 1e-5, 1.0, 1e5, 1e10):
    sig_s = eps_c * ws / hbar_eVs
    row = [3 * sig_s / (4 * PI * Hz(z)) for z in zs]
    print(f"   {ws:8.0e}  " + "".join(f"  {r:11.2e}" for r in row))

def chirp_ratio(sD):
    """P_tot(chirp of duration D)/P_tot(transform-limited), narrow band, top hat (same as taskC1(f))."""
    from scipy import integrate, special
    if sD == 0:
        return 1.0
    c = sD / 4.0

    def inner(Y):
        zz = Y * math.sqrt(2 * c / PI)
        S, Cf = special.fresnel(zz)
        return 4 * (PI / (2 * c)) * (Cf ** 2 + S ** 2)
    v, _ = integrate.quad(lambda x: inner(1 - x), 0, 1, limit=400, epsabs=0, epsrel=1e-10)
    return 2 * v / (8.0 / 3.0)


print("\n" + "=" * 110)
print("(d0) fixed GW power L, bin of duration D and bandwidth sig, N = L D/w.  In units of G^2 L^2 w:")
print("     eq. 8 (real Theta, transform-limited packet)        = (3/(25 pi)) (sig D)^2   [depends on the bin choice]")
print("     in-out total / D for the same bin, chirped to last D = (4/25) sig D x chirp_ratio(sig D)   [-> 12 pi/25 for sig D >> 2 pi]")
print("=" * 110)
for sD in (2 * PI, 20.0, 100.0, 1000.0):
    e8 = 3 / (25 * PI) * sD ** 2
    io = 4 / 25 * sD * chirp_ratio(sD)
    print(f"   sig D = {sD:7.2f}:  eq.8 = {e8:10.4f}   in-out P_tot/D = {io:7.4f}   (12 pi/25 = {12*PI/25:.4f}; transform-limited"
          f" bins of width 2 pi/sig: 8 pi/25 = {8*PI/25:.4f})   ratio = {e8/io:10.3f}")

print("\n" + "=" * 110)
print("(d) inspiral bins (eps = 0.1, equal mass, M = 2^(6/5) M_c): when t_eps > 1/(eps w) the bin is a chirp of duration")
print("    t_eps >> 2 pi/sig; eq. 8 with N = E_rel/w and sig = eps w treats it as a transform-limited packet of duration ~1/sig.")
print("    taskC1(f): eq.8 / [chirp P_tot / t_eps] -> (sig t_eps)^2/(4 pi^2) = (eps n)^2, n = w t_eps/(2 pi) cycles in the bin")
print("=" * 110)
eps_b = 0.1
GMsun_s = K_.G * 1.98847e30 / K_.c ** 3
for M in (1.0, 10.0, 65.0, 1e3, 1e6):
    Mc = M / 2 ** 1.2
    nu_isco = 1 / (6 ** 1.5 * PI * GMsun_s * M)
    for nu in (1e-3, 1e-1, 10.0, 1e3):
        if nu >= nu_isco:
            continue
        wv = 2 * PI * nu
        teps = 5 * eps_b / (12 * (2 * (GMsun_s * Mc) ** 5 * wv ** 8) ** (1 / 3))
        n = wv * teps / (2 * PI)
        sD = eps_b * wv * teps
        if teps > 1 / (eps_b * wv):
            over = 3 * sD / (4 * PI * chirp_ratio(sD)) if sD < 3e4 else (eps_b * n) ** 2
            tag = f"B&O use sig = eps w; eq.8 / in-out average over t_eps = {over:9.3e}  ((eps n)^2 = {(eps_b*n)**2:9.3e})"
        else:
            tag = "B&O use sig ~ 1/t_eps (transform-limited): O(1) only"
        print(f"   M = {M:8.0e} Msun, nu = {nu:7.0e} Hz (ISCO {nu_isco:8.2e}): t_eps = {teps:9.3e} s, 1/(eps w) = {1/(eps_b*wv):9.3e} s,"
              f" sig t_eps = {sD:9.3e}: {tag}")

print("\n" + "=" * 110)
print("(e) merger (B&O: nu ~ 150 Hz (65 Msun/M), t_m ~ 5 ms (M/65 Msun), eps ~ 0.15): sig t_m is M-independent")
print("=" * 110)
nu, tm, e = 150.0, 5e-3, 0.15
print(f"   sig t_m = eps 2 pi nu t_m = {e*2*PI*nu*tm:.3f}  (transform-limited: the delta(0)->T step costs only the O(1) factor of taskC1(b))")
