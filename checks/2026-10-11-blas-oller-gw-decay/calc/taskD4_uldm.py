#!/usr/bin/env python3
"""Task D(4): ULDM channel g g -> phi phi (B&O main text eqs. 16-18, SM SD eqs. S10-S11).

Complements taskA4_scalar_channel.py (which checked S10 vs qft_second_order, crossing, and the ring integrals) with
INDEPENDENT routes:
 (1) hand/sympy derivation of the 7/54 ratio in B&O's isotropic narrow-band model: the gravitons that feed a given
     final pair lie (in the pair CM) on the ring perpendicular to the pair momentum K; ring averages
     <c^2> = sin^2(theta)/2 (c = cos angle graviton-final particle, theta = final particle vs K) give
       photons (eq. 7):  4 pi G (t^2+u^2)/s -> pi G s (2 + sin^2 theta), 2 photon polarisations (delta_{mu1 mu2})
       scalars (S10, m=0, amplitude-level sum (1/2) sum_{l1 l2} A_{l1 l2} = -8 pi G t u/s) -> -pi G s (2 - sin^2 theta)
     ratio = int (2 - sin^2)^2 / [2 int (2 + sin^2)^2];
     and, for contrast, the ratio of PHYSICAL unpolarised cross sections (no ring coherence), sigma_phiphi/sigma_gamgam
     at m = 0, by hand (int (1-c^2)^2 vs int (1+c^2)^2 ...) and from qft_second_order.sigma_total;
 (2) eq. S11: massless limit -> 7/(450 pi) by sympy; tau_phi/tau from eq. 9/10 definitions;
 (3) resonant regime: asymptotics of S11 for w_s = m(1 + delta), delta -> 0 (mpmath), vs eq. 17
     dP/dt = G^2 m^5 N0^2 v^6 N_phi/128 with sigma_w = m v^2/2, delta = v^2/2;
 (4) eq. 16 (N_phi), the W_phi formula, eq. 18 (1e14 W, 1e54 s^-1) in SI; caveats (bandwidth of a real merger,
     inverse process phi phi -> g g when N_phi exceeds the graviton phase-space occupation).
Usage: python3 taskD4_uldm.py
"""
import math
import os
import sys

import mpmath as mp
import sympy as sp
from scipy import constants as K

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "conundrum", "scripts"))
import qft_second_order as q2  # noqa: E402

PI = math.pi


def hdr(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


hdr("(1) ring-average derivation of the scalar/photon ratio in B&O's model; physical cross-section ratio")
x, c = sp.symbols("x c", real=True)       # x = cos(theta) (final particle vs K)
s2 = 1 - x ** 2
ph = sp.integrate((2 + s2) ** 2, (x, -1, 1))
sc = sp.integrate((2 - s2) ** 2, (x, -1, 1))
print(f"  int (2+sin^2)^2 dx = {ph}, int (2-sin^2)^2 dx = {sc};  ratio scalar/photon (2 photon pols) = {sp.nsimplify(sc/(2*ph))}")
print(f"  x 3/(25 pi): {sp.nsimplify(sc/(2*ph))*sp.Rational(3,25)}/pi  (B&O: 7/(450 pi))")
# ring average check: n perpendicular to K, final direction p at angle theta to K: <(n.p)^2> = sin^2/2
phi_ = sp.symbols("phi", real=True)
th = sp.symbols("theta", real=True)
avg = sp.integrate((sp.sin(th) * sp.cos(phi_)) ** 2, (phi_, 0, 2 * sp.pi)) / (2 * sp.pi)
print(f"  ring average <(n.p)^2> = {sp.simplify(avg)}")
# physical unpolarised: photons: opposite graviton helicities only, |M|^2 summed = (8piG)^2 (t^4+u^4)/s^2,
# scalars m=0: same-helicity amp ~ m^4 -> 0, opposite: |M| = 8 pi G t u/s (S10 at m = 0)
ph_phys = sp.integrate(((1 - c) ** 4 + (1 + c) ** 4) / 16, (c, -1, 1))
sc_phys = sp.integrate(((1 - c ** 2) ** 2) / 16, (c, -1, 1))
print(f"  physical (incoherent) sigma_phiphi/sigma_gamgam at m = 0, by hand: {sp.nsimplify(sc_phys/ph_phys)}")
for s_ in (1.0, 3.0):
    rp = q2.sigma_total(s_, "R", "L", final="scalar", m=0.0) / q2.sigma_total(s_, "R", "L", final="photon")
    print(f"  module sigma_total(R,L) scalar/photon at s={s_}: {rp:.10f}")

hdr("(2) eq. S11 massless limit and tau_phi/tau")
S, w, m = sp.symbols("s omega m", positive=True)
I0 = sp.integrate(7 * S ** 2 / sp.sqrt(4 * w ** 2 - S), (S, 0, 4 * w ** 2))
coef0 = sp.simplify(I0 / (15360 * sp.pi * w ** 2) / w ** 3)
print(f"  S11 at m = 0, N_phi = 0: dP/dt = {coef0} G^2 N^2 w^3 sigma^2   (B&O: 7/(450 pi))")
# eq. 9/10: N_gamma = 2 x (3/(25 pi)) G^2 N^2 w^3 sigma^2 t; tau = 1/(2 dP/dt). Same definition for scalars:
print(f"  tau_phi/tau = (2 x 3/(25 pi))/(2 x 7/(450 pi)) = {sp.Rational(3,25)/sp.Rational(7,450)}  (B&O: 54/7)")


hdr("(3) resonant regime: S11 for w_s = m (1 + delta), delta -> 0; eq. 17 needs dP/dt -> G^2 N^2 sigma^2 N_phi m^3 delta/16")
mp.mp.dps = 40


def s11_integral(wv, mv):
    """int ds [...]/(s^{3/2} sqrt(4 w^2 - s)) of eq. S11 (bracket as printed), via s = 4 m^2 + u^2
    (sqrt(s - 4 m^2) = u exactly, no cancellation at threshold)."""
    wv, mv = mp.mpf(wv), mp.mpf(mv)
    umax = mp.sqrt(4 * wv ** 2 - 4 * mv ** 2)

    def integrand(u):
        sv = 4 * mv ** 2 + u ** 2
        rs = mp.sqrt(sv)
        sig = u / rs
        br = (sv * rs * sig * (912 * mv ** 4 - 136 * mv ** 2 * sv + 7 * sv ** 2)
              + 7680 * mv ** 7 * mp.atan(u / (2 * mv))          # arccot(2m/u) = atan(u/(2m)) for u > 0
              + 480 * mv ** 4 * (sv - 14 * mv ** 2) * rs * mp.asinh(u / (2 * mv)))
        return br / (sv * rs * mp.sqrt(umax ** 2 - u ** 2)) * 2 * u   # ds = 2 u du
    return mp.quad(integrand, [0, umax])


for d in (mp.mpf("1e-2"), mp.mpf("1e-4"), mp.mpf("1e-6")):
    wv = 1 + d
    J = s11_integral(wv, mp.mpf(1))
    # dP/dt = G^2 N^2 sigma^2 (1 + 2 N_phi) J/(15360 pi w^2); keep the 2 N_phi part, divide by N_phi m^3 delta
    val = 2 * J / (15360 * mp.pi * wv ** 2) / d
    print(f"  delta = {mp.nstr(d, 3)}: [dP/dt]/(G^2 N^2 sigma^2 N_phi m^3 delta) = {mp.nstr(val, 12)}   (1/16 = 0.0625)")
print("  with sigma = m v^2/2, delta = v^2/2: G^2 N^2 (m^2 v^4/4) N_phi m^3 (v^2/2)/16 = G^2 m^5 N^2 v^6 N_phi/128 (eq. 17)")
# sanity: m -> 0 limit numerically
print(f"  check S11 numerics at m = 1e-4, w = 1: J/(15360 pi) = {mp.nstr(s11_integral(1, mp.mpf('1e-4'))/(15360*mp.pi), 12)};"
      f"  7/(450 pi) = {mp.nstr(7/(450*mp.pi), 12)}")

hdr("(4) eqs. 16-18 in SI")
hbar, cc, G, eV = K.hbar, K.c, K.G, K.e
Msun = 1.98892e30
H0 = 67.4e3 / 3.0856775814913673e22
rho_c = 3 * H0 ** 2 / (8 * PI * G) * cc ** 2         # J/m^3
Om = 0.26
for mDM_eV, v in ((1e-22, 1e-3), (1e-21, 1e-3)):
    mJ = mDM_eV * eV
    n = Om * rho_c / mJ                                # m^-3
    p = mJ * v / cc                                    # momentum (kg m/s)
    cell = (2 * PI * hbar) ** 3                        # phase-space cell
    N_sphere = n / ((4 * PI / 3) * p ** 3 / cell)
    N_cube = n / (p ** 3 / cell)
    print(f"  m = {mDM_eV:g} eV, v = {v:g}: N_phi = n/[(4pi/3)(m v)^3/(2 pi hbar)^3] = {N_sphere:.2e};  n/[(m v)^3/(2 pi hbar)^3] = {N_cube:.2e}"
          f"   (eq. 16 scaling: 6e87 (1e-22 eV/m)^4 = {6e87*(1e-22/mDM_eV)**4:.1e})")
# closed form in natural units: N_phi = 6 pi^2 rho/(m^4 v^3) = 9 pi H0^2 Omega/(4 G m^4 v^3); W = 2 m dP/dt
mm, vv, N0, GG, H, Omega = sp.symbols("m v N0 G H0 Omega", positive=True)
Nphi = 9 * sp.pi * H ** 2 * Omega / (4 * GG * mm ** 4 * vv ** 3)
W = 2 * mm * GG ** 2 * mm ** 5 * N0 ** 2 * vv ** 6 * Nphi / 128
print(f"  W_phi = 2 m x eq.17 with N_phi = 9 pi H0^2 Omega/(4 G m^4 v^3): {sp.simplify(W)}   (B&O: 9 pi G m^2 v^3 N0^2 H0^2 Omega_DM/256)")

print("\n  eq. 18: m = w_s (ISCO: w_s = 8800 pi (Msun/M) rad/s), E_rel = 2 Msun c^2 (M/65 Msun), N0 = E_rel/(hbar w_s)")
for mDM_eV in (1e-21, 1e-22):
    ws = mDM_eV * eV / hbar
    M_over_Msun = 8800 * PI / ws
    Erel = 2 * Msun * cc ** 2 * M_over_Msun / 65
    N0v = Erel / (hbar * ws)
    v = 1e-3
    # natural units -> SI: G m^2 H0^2 -> (G/(hbar c^5)) (m c^2)^2 (hbar H0)^2 / hbar  [J/s]
    Wsi = 9 * PI / 256 * v ** 3 * N0v ** 2 * Om * (G / (hbar * cc ** 5)) * (mDM_eV * eV) ** 2 * (hbar * H0) ** 2 / hbar
    rate_pairs = Wsi / (2 * mDM_eV * eV)
    print(f"  m = {mDM_eV:g} eV: w_s = {ws:.3e} rad/s, M = {M_over_Msun:.2e} Msun, E_rel = {Erel:.2e} J, N0 = {N0v:.2e};"
          f" W_phi (x_MW = 1, v = 1e-3) = {Wsi:.2e} W;  W/(m c^2) = {Wsi/(mDM_eV*eV):.1e} s^-1 (scalars), pairs {rate_pairs:.1e} s^-1")
    print(f"     x_MW = 1e5: W_phi = {Wsi*1e5:.2e} W, scalars {Wsi*1e5/(mDM_eV*eV):.1e} s^-1")
    # caveat 1: real merger bandwidth ~ 1/t_m vs resonant band m v^2/2
    t_m = 5e-3 * M_over_Msun / 65
    sig_res = ws * v * v / 2
    frac = sig_res * t_m
    print(f"     merger duration t_m = 5 ms (M/65 Msun) = {t_m:.2e} s -> natural bandwidth ~ 1/t_m = {1/t_m:.2e} s^-1;"
          f" resonant band m v^2/2 = {sig_res:.2e} s^-1; fraction of N0 in band ~ {frac:.1e};"
          f" rate ~ (N sigma)^2 -> suppression of eq. 17 by ~ {frac**2:.1e} if the band is filled at the merger's spectral density")
    print(f"     time to accumulate the resonant band: 1/(m v^2/2) = {1/sig_res:.2e} s = {1/sig_res/3.156e7:.1e} yr (eq. 8 needs tau << 1/sigma)")
    # caveat 2: inverse process. graviton phase-space occupation f_g ~ 2 pi^2 N0/(w R)^2 (Liouville), R ~ 6 G M/c^2
    R = 6 * G * M_over_Msun * Msun / cc ** 2
    fg = 2 * PI ** 2 * N0v / max(ws * R / cc, 1.0) ** 2
    Nphi_MW = 9 * PI * (hbar * H0) ** 2 * Om / (4 * (G / (hbar * cc ** 5)) * (mDM_eV * eV) ** 4 * v ** 3) * 1e5
    print(f"     inverse process: net ~ f_g^2 (1 + 2 N_phi) - N_phi^2 (1 + 2 f_g); f_g ~ {fg:.1e}, N_phi (x_MW = 1e5) ~ {Nphi_MW:.1e}"
          f" -> forward wins iff f_g > N_phi: {fg > Nphi_MW}")
