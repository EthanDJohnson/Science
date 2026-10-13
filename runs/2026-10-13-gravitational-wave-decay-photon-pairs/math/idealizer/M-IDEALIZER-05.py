"""M-IDEALIZER-05: sigma(R L -> gamma gamma) = (4 pi/5) G^2 s and eq. 14 Gamma = (8 pi/15) G^2 rho^2.

Natural units. Opposite-helicity graviton pair; summed over photon helicities
|M|^2 = (8 pi G)^2 (t^4 + u^4)/s^2 (the physical, sum-of-squares form; magnitudes t^2/s, u^2/s per configuration).
dsigma/dOmega = |M|^2/(64 pi^2 s); identical photons: 1/2. Bath: isotropic, unpolarised, so the pair (R,L),(L,R)
fraction is 1/2 and same-helicity pairs give zero; Gamma = (1/2) Int dn1 dn2 sigma_unpol v_rel, v_rel = 1 - cos,
s = 2 w1 w2 (1 - cos).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, units, limit, finish
import sympy as sp

G, s, c, w1, w2, rho = sp.symbols("G s c w1 w2 rho", positive=True)
cc = sp.symbols("cc", real=True)
t, u = -s * (1 - cc) / 2, -s * (1 + cc) / 2
M2 = (8 * sp.pi * G)**2 * (t**4 + u**4) / s**2
sig = sp.Rational(1, 2) * 2 * sp.pi * sp.integrate(M2 / (64 * sp.pi**2 * s), (cc, -1, 1))
print("sigma(RL) =", sp.simplify(sig))
identity(sig, 4 * sp.pi / 5 * G**2 * s)
sig_unpol = sp.Rational(1, 4) * (2 * sig)       # RL + LR out of four helicity pairs
# Gamma for two monochromatic isotropic lines n1 (w1), n2 (w2) and identical-line self term
n1, n2 = sp.symbols("n1 n2", positive=True)
def pair(wa, wb):
    sv = sig_unpol.subs(s, 2 * wa * wb * (1 - cc)) * (1 - cc)
    return sp.integrate(sv, (cc, -1, 1)) / 2           # isotropic angle average
Gam = sp.Rational(1, 2) * (n1**2 * pair(w1, w1) + 2 * n1 * n2 * pair(w1, w2) + n2**2 * pair(w2, w2))
rho_tot = n1 * w1 + n2 * w2
identity(sp.expand(Gam), sp.expand(8 * sp.pi / 15 * G**2 * rho_tot**2))
# independent route: Gamma = (2 pi/5) G^2 T_mn T^mn with isotropic T = diag(rho, rho/3, rho/3, rho/3)
TT = rho**2 * (1 + 3 * sp.Rational(1, 9))
identity(sp.Rational(2, 5) * sp.pi * G**2 * TT, 8 * sp.pi / 15 * G**2 * rho**2)
# SI: Gamma_nat [J^4] -> per m^3 per s: divide by (hbar c)^3 hbar; G_nat = G/(hbar c^5); rho_nat = rho_E (hbar c)^3
hb, cl, GS, rE = sp.symbols("hbar c_l G_S rho_E", positive=True)
GSI = sp.simplify(8 * sp.pi / 15 * (GS / (hb * cl**5))**2 * (rE * (hb * cl)**3)**2 / ((hb * cl)**3 * hb))
print("SI form:", GSI)
identity(GSI, 8 * sp.pi / 15 * GS**2 * rE**2 / cl**7)
units("(6.674e-11 m^3/(kg s^2))^2 * (1 J/m^3)^2 / (299792458 m/s)^7", "1/(m^3 s)")
limit(sig / s, "s", 0, 4 * sp.pi / 5 * G**2)
raise SystemExit(finish())
