"""M-CONSTRAINTS-10 (F12): Born contact estimate of chi-chi scattering for a vector mediator.
Yukawa V(r) = alpha' e^{-m_V r}/r, alpha' = g^2/(4 pi); Fourier transform V(q) = g^2/(q^2 + m_V^2) -> contact g^2/m_V^2
at q << m_V. Born: dsigma/dOmega = (mu/(2 pi))^2 |V(q)|^2, reduced mass mu = m_chi/2 -> sigma = m_chi^2 g^4/(4 pi m_V^4)
(distinguishable-particle normalisation; identical-fermion factors are O(1)). Born validity parameter alpha' m_chi/m_V."""
import math
import sympy as sp
from _common import near
from math_checks import identity, units, finish

m, g, mV = sp.symbols("m g m_V", positive=True)
mu = m / 2
sig = 4 * sp.pi * (mu / (2 * sp.pi)) ** 2 * (g**2 / mV**2) ** 2
identity(sig, m**2 * g**4 / (4 * sp.pi * mV**4))
units("(938 MeV)^2 * (1 / (60 MeV))^4 * (197.327 MeV fm)^2", "area")

HC = 197.3269804           # MeV fm
mchi = 937.993             # MeV
m_g = mchi * 1.78266192e-27   # g per MeV/c^2
out = {}
for r in (60.0, 45.0):     # m_V/g in MeV
    s_mev = mchi**2 / (4 * math.pi * r**4)          # MeV^-2
    s_cm2 = s_mev * HC**2 * 1e-26                   # fm^2 -> cm^2
    out[r] = s_cm2 / m_g
    print(f"   m_V/g = {r} MeV: sigma = {s_cm2:.3e} cm^2, sigma/m = {out[r]:.2f} cm^2/g, "
          f"alpha' m_chi/m_V (g=1) = {mchi / (4 * math.pi * r):.2f}")
near("sigma/m at 60 MeV", out[60.0], 1.3, 0.06)
near("sigma/m at 45 MeV", out[45.0], 4.0, 0.06)
near("Born parameter at 60 MeV", mchi / (4 * math.pi * 60), 1.2, 0.06)
near("Born parameter at 45 MeV", mchi / (4 * math.pi * 45), 1.7, 0.06)
raise SystemExit(finish())
