"""M-CONSTRAINTS-08 (F11, K7): mixing angle theta needed for a 1.113% n -> chi gamma-type branch, and tau_H.
Independent derivation. A spin-1/2 -> spin-1/2 + gamma magnetic-dipole transition with transition moment mu_T has
  Gamma = mu_T^2 k^3 / pi   (natural units, Heaviside-Lorentz, e^2 = 4 pi alpha).
Calibration (known limit): Sigma0 -> Lambda gamma, Gamma = alpha k^3/m_p^2 (mu_T/mu_N)^2 with |mu_T| = 1.61 mu_N,
k = 74.5 MeV must reproduce tau(Sigma0) = 7.4e-20 s.
For n-chi mixing: mu_T = theta mu_n = theta g_n e/(4 m_n) with g_n = -3.826 (mu_n = -1.913 mu_N), k = m_n(1-x^2)/2:
  Gamma = g_n^2 e^2 theta^2 m_n (1-x^2)^3 / (128 pi).
The lens writes the prefactor as g_n^2 e^2/(8 pi): 16x larger, theta 4x smaller."""
import math
import sympy as sp
from _common import near
from math_checks import identity, quantity, finish

hbar = 6.582119569e-22  # MeV s
alpha = 1 / 137.035999
mp_, mn, me = 938.27209, 939.56542, 0.51100
# calibration against Sigma0
G_sig = alpha * 74.5**3 / mp_**2 * 1.61**2
print(f"   Sigma0: Gamma = {G_sig*1e3:.2f} keV, tau = {hbar/G_sig:.3e} s (PDG 7.4e-20 s)")
quantity(f"{hbar/G_sig!r} s", "7.4e-20 s", rel_tol=0.05)

# symbolic: mu_T^2 k^3/pi with mu_T = theta g e/(4m), k = m(1-x^2)/2
th, g, e, m, x = sp.symbols("theta g e m x", positive=True)
G = (th * g * e / (4 * m)) ** 2 * (m * (1 - x**2) / 2) ** 3 / sp.pi
identity(G, g**2 * e**2 * th**2 * m * (1 - x**2) ** 3 / (128 * sp.pi))
# consistency with the Sigma0 form: alpha k^3 (mu/mu_N)^2/m_p^2 where mu = (g/2) mu_N theta, m_p -> m
k = sp.symbols("k", positive=True)
identity((th * g * e / (4 * m)) ** 2 * k**3 / sp.pi, (e**2 / (4 * sp.pi)) * k**3 * (th * g / 2) ** 2 / m**2)

dGamma = (1 / 877.82 - 1 / 887.7) * hbar   # MeV
gn, e2 = -3.826, 4 * math.pi * alpha
out = {}
for mchi in (937.993, 938.7):
    xx = mchi / mn
    c = gn**2 * e2 * mn * (1 - xx**2) ** 3
    th_mine = math.sqrt(dGamma / (c / (128 * math.pi)))
    th_lens = math.sqrt(dGamma / (c / (8 * math.pi)))
    Q = (mp_ + me) - mchi
    tH = lambda t: 1e29 * (1e-10 / t) ** 2 * (me / Q) ** 2
    out[mchi] = (th_mine, th_lens, tH(th_mine), tH(th_lens))
    print(f"   m_chi {mchi}: theta (1/128pi) = {th_mine:.3e}, theta (lens 1/8pi) = {th_lens:.3e}; "
          f"tau_H = {tH(th_mine):.3e} s (mine) vs {tH(th_lens):.3e} s (lens form); Q = {Q:.3f} MeV")
# lens's numbers reproduce with its prefactor (arithmetic check)
near("lens theta at 937.993 (its 1/8pi form)", out[937.993][1], 6.7e-11, 6e-13)
near("lens theta at 938.7 (its 1/8pi form)", out[938.7][1], 1.6e-10, 6e-12)
near("lens tau_H low (1e29 s)", out[937.993][3] / 1e29, 0.94, 0.006)
near("lens tau_H high (1e29 s)", out[938.7][3] / 1e29, 14, 0.6)
# the corrected values vs the lens's claim
near("theta at 937.993 with 1/(128 pi) vs lens (expected FAIL: 4x)", out[937.993][0], 6.7e-11, 6e-12)
raise SystemExit(finish())
