"""M-DIALECTICIAN-09 and -10: kinetic theory of an isotropic graviton gas reproduces B&O eq. 14;
collinear suppression of sigma (1 - cos th).

Natural units. Input (literature, verified separately as M-MECHANIST-01): tree g g -> gamma gamma
helicity amplitudes, nonzero only for opposite graviton helicities, abs(M) = 8 pi G t^2/s and
8 pi G u^2/s into the two opposite-helicity photon final states.
CM 2 -> 2 massless: dsigma/dOmega = sum abs(M)^2/(64 pi^2 s); identical photons: factor 1/2 over
the full sphere. Unpolarised: average over the 4 graviton helicity pairs (RL, LR nonzero).
Gas: monochromatic energy w, number density n, rho = n w. Two gravitons at angle th:
s = 2 w^2 (1 - cos th), Moller flux factor v = 1 - cos th. Gamma/V = (1/2) n^2 <sigma v>_iso.
Claim (09): Gamma/V = 8 pi G^2 rho^2/15. Claim (10): sigma (1 - cos th) -> (2 pi/5) G^2 w^2 th^4.
SI form: Gamma/V = (8 pi/15) G^2 rho^2 / c^7 (hbar cancels); at rho = 1e-15 J/m^3 ~ 3e-110 m^-3 s^-1.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, series, units, quantity, finish

G, s, w, n, th, hb, cl, rho = sp.symbols("G s w n theta hbar c_l rho", positive=True)
cc = sp.symbols("c", real=True)
t = -s * (1 - cc) / 2
u = -s * (1 + cc) / 2
sumM2 = (8 * sp.pi * G) ** 2 * (t**4 + u**4) / s**2
sig_RL = sp.Rational(1, 2) * 2 * sp.pi * sp.integrate(sumM2 / (64 * sp.pi**2 * s), (cc, -1, 1))
sig_RL = sp.simplify(sig_RL)
print("sigma_RL =", sig_RL)
identity(sig_RL, 4 * sp.pi / 5 * G**2 * s)
sig_un = sp.simplify((2 * sig_RL + 0 + 0) / 4)
identity(sig_un, 2 * sp.pi / 5 * G**2 * s)

# isotropic average over relative angle: <F> = (1/2) int_{-1}^{1} F dcos
sv = sig_un.subs(s, 2 * w**2 * (1 - cc)) * (1 - cc)
avg = sp.integrate(sv, (cc, -1, 1)) / 2
rate = sp.simplify(sp.Rational(1, 2) * n**2 * avg)
print("Gamma/V =", rate)
identity(rate, 8 * sp.pi / 15 * G**2 * (n * w) ** 2)

# limit check: all gravitons head-on (th = pi) would give (1/2) n^2 sigma(4w^2) * 2
print("head-on sanity:", sp.simplify(sp.Rational(1, 2) * n**2 * sv.subs(cc, -1)))

# SI conversion: G_nat = G/(hbar c^5); rho_nat = rho (hbar c)^3; rate_SI = rate_nat/((hbar c)^3 hbar)
rate_si = sp.simplify(8 * sp.pi / 15 * (G / (hb * cl**5)) ** 2 * (rho * (hb * cl) ** 3) ** 2 / ((hb * cl) ** 3 * hb))
identity(rate_si, 8 * sp.pi / 15 * G**2 * rho**2 / cl**7)
units("(6.674e-11 m^3/(kg s^2))^2 * (1 J/m^3)^2 / (2.998e8 m/s)^7", "1/(m^3 s)")
val = float(8 * sp.pi / 15) * 6.6743e-11**2 * (1e-15) ** 2 / 299792458.0**7
print(f"Gamma/V at rho = 1e-15 J/m^3: {val:.3e} m^-3 s^-1")
quantity(f"{val} / (m^3 s)", "3.4e-110 / (m^3 s)", rel_tol=3e-2)

# M-10: collinear limit of sigma (1 - cos th) at s = 2 w^2 (1 - cos th)
f_un = (2 * sp.pi / 5) * G**2 * 2 * w**2 * (1 - sp.cos(th)) ** 2
f_RL = (4 * sp.pi / 5) * G**2 * 2 * w**2 * (1 - sp.cos(th)) ** 2
print("unpolarised leading:", sp.series(f_un, th, 0, 6).removeO())
print("RL pair leading:", sp.series(f_RL, th, 0, 6).removeO())
series(f_un, "theta", 0, 6, sp.pi / 5 * G**2 * w**2 * th**4)
series(f_RL, "theta", 0, 6, 2 * sp.pi / 5 * G**2 * w**2 * th**4)
# lens numeric at th = 0.1 (G = w = 1): 1.2545e-4
print(f"theta=0.1, G=w=1: unpolarised {float(f_un.subs({G:1, w:1, th:0.1})):.4e}, RL {float(f_RL.subs({G:1, w:1, th:0.1})):.4e}")
raise SystemExit(finish())
