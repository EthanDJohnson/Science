"""Check of the authors' own later black-hole estimate, Gambini-Porto-Pullin Braz.J.Phys. 35, 266 (2005),
arXiv:gr-qc/0501027, eqs. (12), (16), (18).  Angle: versions (how the PRL result was later revised).

Their model: omega12(t) = 1/((8 pi)^2 tP) (tP/(Tmax-t))^(1/3)   [eq. 12, same prefactor as PRL eq. 4],
clock window of width tau centred on t, rho12(t) = rho12(0)/tau * Int_{t-tau/2}^{t+tau/2} dv exp(i phi12(v)),
phi12(v) = Int_0^v omega12 dT   [eq. 16], evaluated at t = Tmax with tau(Tmax) = tP^(2/3) Tmax^(1/3), and the
authors' convention Tmax/tP = (M/M_P)^3.   They quote |rho12(Tmax)|/|rho12(0)| ~ (M_P/M_sun)^(2/3) ~ 1e-28.

I re-derive the integral from (12) and (16) myself (not from their garbled eq. 17):
  u^3 = (Tmax - v)/tP, dv = -3 tP u^2 du,  phi12 = c [ (Tmax/tP)^(2/3) - u^2 ],  c = 3/(2 (8 pi)^2),
  |rho12(Tmax)/rho12(0)| = | Int_{-U}^{U} 3 u^2 exp(-i c u^2) du | / (2 U^3),   U^3 = tau/(2 tP).
Closed form: Int_{-U}^{U} u^2 e^{-i c u^2} du = 2 [ -U e^{-i c U^2}/(2 i c) + (1/(2 i c)) (1/2) sqrt(pi/(i c)) erf(sqrt(i c) U) ].

Run:  python3 checks/2026-10-27-prior-art/calc/gpp_2005_window_check.py
"""
import mpmath as mp

mp.mp.dps = 80
pi = mp.pi
c = 3 / (2 * (8 * pi) ** 2)


def ratio(U):
    U = mp.mpf(U)
    I = 2 * (-U * mp.e ** (-1j * c * U**2) / (2j * c) + (1 / (2j * c)) * mp.mpf(1) / 2 * mp.sqrt(pi / (1j * c)) * mp.erf(mp.sqrt(1j * c) * U))
    return abs(3 * I) / (2 * U**3)


print("c = 3/(2 (8 pi)^2) =", mp.nstr(c, 8))
# sanity: small-U limit is 1 (no dephasing), and quadrature agrees with the closed form at moderate U
for U in ("0.01", "1", "30"):
    q = abs(mp.quad(lambda u: 3 * u**2 * mp.e ** (-1j * c * u**2), mp.linspace(-mp.mpf(U), mp.mpf(U), 41))) / (2 * mp.mpf(U) ** 3)
    print(f"  U={U:>5}: closed form {mp.nstr(ratio(U), 10)}   quadrature {mp.nstr(q, 10)}")

# solar mass in the authors' convention
G = mp.mpf("6.67430e-11"); cc = mp.mpf("299792458"); hbar = mp.mpf("1.054571817e-34")
mP = mp.sqrt(hbar * cc / G)
M = mp.mpf("1.98847e30")
x = M / mP  # M/M_P
U = (x / 2) ** (mp.mpf(1) / 3)  # tau(Tmax)/tP = (Tmax/tP)^(1/3) = M/M_P  -> U^3 = M/(2 M_P)
r = ratio(U)
print(f"M/M_P = {mp.nstr(x, 5)} ; U = {mp.nstr(U, 5)} ; c U^2 = {mp.nstr(c*U**2, 5)}")
print(f"  |rho12(Tmax)/rho12(0)| from eq.(16) with eq.(12) = {mp.nstr(r, 5)}  (log10 = {mp.nstr(mp.log10(r), 5)})")
asym = 3 / (c * 2 * U**2)
print(f"  large-U asymptote 3/(2 c U^2) = {mp.nstr(asym, 5)}  (log10 = {mp.nstr(mp.log10(asym), 5)})")
print(f"  authors' scaling (M_P/M)^(2/3) = {mp.nstr(x**(-mp.mpf(2)/3), 5)}  (log10 = {mp.nstr(mp.log10(x**(-mp.mpf(2)/3)), 5)});  paper quotes ~1e-28")
print(f"  ratio mine/(M_P/M)^(2/3) = {mp.nstr(r / x**(-mp.mpf(2)/3), 5)}  (analytic 3 * 2^(2/3)/(2c) = {mp.nstr(3*2**(mp.mpf(2)/3)/(2*c), 5)})")
tauT = mp.mpf(1) * mp.sqrt(hbar * G / cc**5) * x  # tau(Tmax) = tP * M/M_P in seconds
print(f"  clock resolution at evaporation tau(Tmax) = tP*(M/M_P) = {mp.nstr(tauT, 4)} s (>> tP)")
