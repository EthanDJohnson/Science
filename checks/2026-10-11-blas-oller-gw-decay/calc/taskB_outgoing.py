#!/usr/bin/env python3
"""Task B (3)+(4): pair production by a PHYSICAL outgoing (retarded) gravitational wave, as a function of the inner radius
r_min of the region counted and of the radius r reached by the wave; steady sources and bursts; comparison with B&O.

Method (exact second order for a scalar proxy, gravity weight rho(s) = (pi/5) G^2 s^2 from taskB_luminosity_check.py):
  outgoing monopole psi = B e^{-iw(t - r)}/r (steady) or D_0(r - t)/(8 pi^2 i r) (burst, = the outgoing half of B&O's field),
  J = psi^2 S(r/r_min), S a smooth switch-on that removes the source region r < ~r_min. The radial transform is exact:
      I(Q0, Q) = int_0^inf dr S j_0(Qr) e^{iQ0 r} = (1/(2iQ)) [ ln(k2/k1) - phi_S(k1 r_min) + phi_S(k2 r_min) ],
      k1,2 = Q0 -+ ... (k1 = Q0 + Q, k2 = Q0 - Q),  phi_S(y) = int_0^inf (1 - S(x)) (e^{iyx} - 1)/x dx  (one universal function).
  Steady:  dP/dt = (16/pi^2) c L^2 w K(w r_min),  K = int_0^1 x^2 (1 - x^2)^2 |w I(2w, 2wx)|^2 dx,  c = pi G^2/5,
           L = GW luminosity (energy/time).  Burst (narrow band): P = c w^5 K int|D_0|^4 du / (4 pi^8)  (= steady formula
           integrated over the emission history, int L^2 dt).
  Gravity factors applied at the end: C_coh = 0.409 (module ring coherence, taskB_ring_coherence.py; proxy = 1) and the
  polarisation/pattern factor g = 4 pi int dOmega (dL/dOmega)^2 4 p+ p- / L^2 (= 1 for isotropic linear; computed here for
  a circular binary).
Also: the l = 2 (m = 0) outgoing wave h_2^(1)(wr) Y_20 with near-field terms (direct quadrature, far taper), the kinetic
"diffraction-limited ray" model, and B&O's eq. 8 applied as in their binary section (N = E_rel/w, sig = 1/t).
Units: w = 1, G = 1 unless SI is stated.
"""
import math
import sys

import numpy as np
from scipy import integrate
from scipy.interpolate import CubicSpline
from scipy.special import spherical_jn

sys.path.insert(0, "/home/user/Science/checks/2026-10-11-blas-oller-gw-decay/calc")
from taskB_common import gaunt_Y20sq  # noqa: E402

PI = math.pi
EG = 0.5772156649015329
LAM = 2 * PI

WINDOWS = {
    "exp(-(rmin/r)^2)": (lambda x: 1 - np.exp(-1.0 / x ** 2), 2),
    "exp(-(rmin/r)^4)": (lambda x: 1 - np.exp(-1.0 / x ** 4), 4),
    "r^4/(r^4+rmin^4)": (lambda x: 1.0 / (1 + x ** 4), 4),
}


def make_phi(one_minus_S, p, ymax=80.0, X=150.0, n=75001):
    """phi(y) on a log grid (numerical Simpson for y <= ymax, asymptotic -ln y - gamma + i pi/2 + c_S beyond)."""
    x = np.linspace(0.0, X, n)
    x[0] = 1e-12
    oms = one_minus_S(x)
    ys = np.concatenate([np.geomspace(1e-6, 1.0, 100, endpoint=False), np.linspace(1.0, ymax, 400)])
    vals = np.empty(ys.size, complex)
    for i, y in enumerate(ys):
        f = oms * np.expm1(1j * y * x) / x
        vals[i] = integrate.simpson(f, x=x) - X ** (-p) / p          # tail: (1-S) ~ x^-p
    cS = np.mean((vals + np.log(ys) + EG - 0.5j * PI)[ys > 0.6 * ymax])
    spread = np.ptp(np.abs((vals + np.log(ys) + EG - 0.5j * PI)[ys > 0.6 * ymax]))

    spl_re = CubicSpline(np.log(ys), vals.real)
    spl_im = CubicSpline(np.log(ys), vals.imag)

    def phi(y):
        y = np.asarray(y, float)
        ly = np.log(np.clip(y, 1e-6, ymax))
        lo = spl_re(ly) + 1j * spl_im(ly)
        lo = np.where(y < 1e-6, 1j * y * integrate.simpson(oms, x=x), lo)
        hi = -np.log(np.maximum(y, 1e-300)) - EG + 0.5j * PI + cS
        return np.where(y > ymax, hi, lo)
    return phi, cS, spread


def I_win(phi, Q0, Q, rmin):
    k1, k2 = Q0 + Q, Q0 - Q
    return (np.log(k2 / k1) - phi(k1 * rmin) + phi(k2 * rmin)) / (2j * Q)


xg = np.unique(np.concatenate([np.linspace(1e-4, 0.9, 1500), 1 - np.geomspace(0.1, 1e-9, 1500)]))


def K_of(phi, rmin):
    if phi is None:
        Ih = np.log((1 + xg) / (1 - xg)) / (4 * xg)          # |w I_full| (no window)
        return np.trapezoid(xg ** 2 * (1 - xg ** 2) ** 2 * Ih ** 2, xg)
    Ih = I_win(phi, 2.0, 2.0 * xg, rmin)                     # w = 1
    return np.trapezoid(xg ** 2 * (1 - xg ** 2) ** 2 * np.abs(Ih) ** 2, xg)


print("=== (a) universal window functions phi_S(y) ===")
PHI = {}
for name, (oms, p) in WINDOWS.items():
    phi, cS, spread = make_phi(oms, p)
    PHI[name] = phi
    print(f"  {name:18s}: c_S = {cS.real:+.6f}{cS.imag:+.6f}i  (asymptote constancy over y in [48,80]: spread {spread:.1e})")
from scipy.special import exp1 as _E1
_Ein1 = integrate.quad(lambda u: -math.expm1(-u) / u, 0, 1)[0]
print(f"  analytic c_S = -int[(1-S) - theta(1-x)]/x dx: exp(-1/x^2): {-(_Ein1 - float(_E1(1.0)))/2:+.6f};"
      f" exp(-1/x^4): {-(_Ein1 - float(_E1(1.0)))/4:+.6f}; 1/(1+x^4): +0.000000")

print("\n=== (b) validation of I(Q0,Q) against direct quadrature (window exp(-(rmin/r)^2), far taper exp(-(r/3000)^2)) ===")
phi = PHI["exp(-(rmin/r)^2)"]
rr = np.arange(0.0005, 15000.0, 0.01)
for rmin, Q in ((LAM, 1.0), (LAM, 1.9), (5 * LAM, 1.98), (0.5, 0.5)):
    Sx = np.exp(-(rmin / rr) ** 2) * np.exp(-(rr / 3000.0) ** 2)
    direct = np.trapezoid(Sx * np.sinc(Q * rr / PI) * np.exp(2j * rr), rr)
    an = I_win(phi, 2.0, Q, rmin)
    print(f"  w rmin = {rmin:7.3f}, Q = {Q:5.3f}: closed form {an:.6e}  direct {direct:.6e}  rel.diff {abs(an-direct)/abs(an):.1e}")

print("\n=== (c) K(w r_min) for the outgoing monopole (steady), three switch-on shapes ===")
K0 = K_of(None, 0)
K0_check, _ = integrate.quad(lambda x: (1 - x * x) ** 2 * math.log((1 + x) / (1 - x)) ** 2 / 16, 0, 1, limit=200)
print(f"  no window (point source down to r = 0): K0 = {K0:.6e}  (quad: {K0_check:.6e})")
rmins = [1.0, 2.0, PI, LAM, 2 * LAM, 5 * LAM, 10 * LAM, 30 * LAM, 100 * LAM, 300 * LAM, 1000 * LAM]
Ktab = {}
for name, phi in PHI.items():
    Ks = np.array([K_of(phi, rm) for rm in rmins])
    Ktab[name] = Ks
    print(f"  {name}:")
    for i, rm in enumerate(rmins):
        sl = "" if i == 0 else f"  local slope dlnK/dln r_min = {math.log(Ks[i]/Ks[i-1])/math.log(rm/rmins[i-1]):+.3f}"
        print(f"     w r_min = {rm:9.3f} ({rm/LAM:8.3f} lambda): K = {Ks[i]:.4e}   K*(w r_min)^3 = {Ks[i]*rm**3:.4e}{sl}")

print("\n=== (d) window-free cross-check: share of pairs with s < s0 in the unwindowed spectrum (formation length 4w/s) ===")
for rm in (LAM, 10 * LAM, 100 * LAM):
    s0 = 4.0 / rm                     # pairs whose formation length 2 Q0/s = 4/s exceeds r_min
    x0 = math.sqrt(1 - s0 / 4.0)
    sel = xg > x0
    Ih = np.log((1 + xg) / (1 - xg)) / (4 * xg)
    part = np.trapezoid((xg ** 2 * (1 - xg ** 2) ** 2 * Ih ** 2)[sel], xg[sel])
    print(f"  r_min = {rm/LAM:6.1f} lambda: K0 x frac(s < 4w/r_min) = {part:.4e}   vs windowed K = {Ktab['exp(-(rmin/r)^2)'][rmins.index(rm)]:.4e}")

print("\n=== (e) l = 2 outgoing wave with near-field terms: see taskB_outgoing_l2.py ===")

print("\n=== (f) gravity factors ===")
Ccoh = 0.40922
cgrid = np.linspace(-1, 1, 200001)
Ap2, Am2 = (1 + cgrid) ** 4 / 16, (1 - cgrid) ** 4 / 16          # |h_{+-2}|^2 pattern of a circular binary
dLdO = Ap2 + Am2
norm = 2 * PI * np.trapezoid(dLdO, cgrid)
g_bin = 4 * PI * 2 * PI * np.trapezoid(4 * Ap2 * Am2, cgrid) / norm ** 2
g_bin_lin = 4 * PI * 2 * PI * np.trapezoid(dLdO ** 2, cgrid) / norm ** 2
print(f"  C_coh (ring coherence of the gravity amplitude, module) = {Ccoh}")
print(f"  circular binary: g = 4pi int (dL/dOmega)^2 4p+p- /L^2 = {g_bin:.5f}  (pattern alone, if every direction were"
      f" linearly polarised: {g_bin_lin:.5f})")

print("\n=== (g) STEADY source: pair rate in units of G^2 L^2 w ===")
c = PI / 5
bo_applied = 3 / (25 * PI)
Kpj = integrate.quad(lambda Q: 4 * PI * Q * Q * (4 - Q * Q) ** 2 * (PI ** 2 / Q) ** 2, 0, 2)[0]
stand = c * Kpj / (2 * PI) ** 3 / (2 * PI) ** 2          # A^4 = (L/2pi)^2, J~ = A^2 pi^2/(w^2 Q), w = 1
print(f"  B&O eq.8 as applied to binaries (N = E/w, sig = 1/t):     {bo_applied:.5f}")
print(f"  free standing wave j0 (Pauli-Jordan, incoming+outgoing):     {stand:.5f}   (closed form 32 pi/75 = {32*PI/75:.5f})")
kin_pref = (2.5) ** 4 / 25
for i, rm in enumerate(rmins):
    K = Ktab["exp(-(rmin/r)^2)"][i]
    Ks = [Ktab[n][i] for n in Ktab]
    proxy = 16 / PI ** 2 * c * K
    print(f"  outgoing, r > r_min = {rm/LAM:8.3f} lambda: proxy {proxy:.3e} (window spread {min(Ks)/K:.2f}-{max(Ks)/K:.2f}x);"
          f" x C_coh: {proxy*Ccoh:.3e}; x C_coh x g_binary: {proxy*Ccoh*g_bin:.3e};  kinetic-ray model {kin_pref/rm**5:.3e};"
          f"  ratio (x C_coh)/B&O-applied = {proxy*Ccoh/bo_applied:.3e}")

print("\n=== (h) BURST: outgoing half of B&O's own top-hat packet, yield from r > r_min vs B&O's exact S-matrix total ===")
P_PJ_proxy = 0.14156          # taskB_pj_exact.py, top hat, sig -> 0 (proxy weight), units G^2 N^2 w^3 sig
P_BO_exact = 0.15923          # taskB_pj_exact.py, B&O kernel, sig = 0.01
for i, rm in enumerate(rmins):
    K = Ktab["exp(-(rmin/r)^2)"][i]
    Pout = 16 / (3 * PI ** 3) * c * K        # top hat: P_out/(N^2 w^3 sig)
    print(f"  r_min = {rm/LAM:8.3f} lambda: P_out = {Pout:.3e} G^2N^2w^3sig;  / P_PJ(proxy) = {Pout/P_PJ_proxy:.3e};"
          f"  x C_coh / P_BO(exact) = {Pout*Ccoh/P_BO_exact:.3e}")
print("  yield per unit time while the shell passes radius r (= -dP_out/dr_min at r_min = r), in units of B&O's eq.8 rate:")
Ks = Ktab["exp(-(rmin/r)^2)"]
lr = np.log(np.array(rmins))
for sig in (0.1, 0.01):
    print(f"   sig = {sig} w:")
    for i in range(1, len(rmins)):
        rmid = math.sqrt(rmins[i] * rmins[i - 1])
        dKdr = (Ks[i] - Ks[i - 1]) / (rmins[i] - rmins[i - 1])
        rate = -16 / (3 * PI ** 3) * c * dKdr * sig        # dP/dt in units N^2 w^3 sig^2 ... times sig/sig
        rate_units = -16 / (3 * PI ** 3) * c * dKdr / sig  # / (N^2 w^3 sig^2)
        print(f"     r = {rmid/LAM:9.3f} lambda: dP/dt = {rate_units:.3e} G^2N^2w^3sig^2 = {rate_units/(3/(25*PI)):.3e} x eq.8"
              f"   (x C_coh: {rate_units*Ccoh/(3/(25*PI)):.3e})")
slope = np.polyfit(lr[-4:], np.log(Ks[-4:]), 1)[0]
print(f"  large-r_min power law of K: slope {slope:.3f}  -> yield beyond r ~ r^{slope:.2f}, rate at radius r ~ r^{slope-1:.2f}")

print("\n=== (i) GW150914-like merger (B&O's anchors: E_rel = 2 Msun c^2, nu = 150 Hz, t_m = 5 ms), SI ===")
Gs, cs, hb, kB, Msun = 6.67430e-11, 2.99792458e8, 1.054571817e-34, 1.380649e-23, 1.98847e30
E = 2 * Msun * cs ** 2
nu, tm = 150.0, 5e-3
om = 2 * PI * nu
lE = Gs * E / cs ** 4                    # G E in natural units (length)
k = om / cs
ks = 1 / (cs * tm)                       # sig = 1/t_m
N0 = E / (hb * om)
rate_BO = 3 / (25 * PI) * lE ** 2 * k * ks ** 2 * cs          # pairs/s, B&O eq.8 with N = E/w, sig = 1/t_m
tau = 25 * PI / (6 * lE ** 2 * k * ks ** 2) / cs
fcmb = 1 / math.expm1(hb * om / (kB * 2.7255))
print(f"  G E/c^4 = {lE:.4e} m, N0 = {N0:.4e}, B&O dP/dt = {rate_BO:.4e} pairs/s, tau (eq.10) = {tau:.4e} s,"
      f" N_gamma(tau) by eq.9 = {2*rate_BO*tau:.3f} photons")
print(f"  B&O photon luminosity 2 dP/dt = {2*rate_BO:.4e} /s; with CMB stimulation (1 + 2 f), f(150 Hz) = {fcmb:.4e}:"
      f" {2*rate_BO*(1+2*fcmb):.4e} /s")
G2L2w_tm = lE ** 2 * k * ks        # G^2 E^2 w / t_m (dimensionless): = G^2 L^2 w t_m for a flat-top burst of length t_m
print(f"  G^2 E^2 w/t_m = {G2L2w_tm:.4e}")
for rm in (1.0, LAM, 10 * LAM):
    i = rmins.index(rm)
    K = Ktab["exp(-(rmin/r)^2)"][i]
    pairs = 16 / PI ** 2 * c * K * Ccoh * g_bin * G2L2w_tm
    print(f"  in-in, outgoing wave beyond r_min = {rm/LAM:5.2f} lambda ({rm/k/1e3:8.1f} km): total pairs over the merger = {pairs:.3e}"
          f"  (x(1+2f): {pairs*(1+2*fcmb):.3e});  B&O-rate x t_m = {rate_BO*tm:.3e};  B&O-rate x tau = {rate_BO*tau:.3e}")
print("  B&O footnote 4 places the photons on a sphere of radius c*tau =", f"{cs*tau:.3e} m = {cs*tau/(LAM/k):.3e} wavelengths;")
for Rm, lab in ((1.496e11, "1 AU"), (3.086e16, "1 pc"), (410 * 3.086e22, "410 Mpc")):
    x = Rm * k
    # rate at radius r relative to B&O's constant rate, extrapolated with the fitted power law of K
    i = len(rmins) - 1
    Kr = Ks[i] * (x / rmins[i]) ** slope
    dKdr = slope * Kr / x
    ratio = (-16 / (3 * PI ** 3) * c * dKdr / ks / (cs / cs)) * k / (3 / (25 * PI))   # sig = ks/k in w units
    print(f"   burst shell at {lab:8s} (w r = {x:.3e}): in-in rate / B&O constant rate = {ratio*Ccoh:.3e}")
