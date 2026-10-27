"""Arithmetic cross-checks used in the GPP citecheck (2026-10-27).

Not a re-derivation of the finding; it only checks numbers that the searchers or
the authors' later papers quote.

(A) Coefficient: for omega12 = 1/((8 pi)^k tP) (tP/(Tmax-T))^(1/3) and
    sigma = c * tP * (tP/(Tmax-T))^(1/3),  omega12^2 * sigma * (Tmax-T) = c/(8 pi)^(2k).
    k=1 : single 8 pi, as in IJMPD 13, 2315 (hep-th/0405183), omega = 1/(8 pi M)
    k=2 : (8 pi)^2, as printed in PRL eq. (4), Braz.J.Phys. eq. (12), GRG eq. (19)
    c=1 : PRL sigma;  c=1/36 : Braz.J.Phys. eq. (21) sigma.
(B) Braz.J.Phys. eq. (18): |rho12(Tmax)| ~ (M_P/M_sun)^(2/3) ~ 1e-28 ?
    Evaluate (M_P/M_sun)^(2/3) and the authors' own eq. (16)-(17) window integral.
"""
from mpmath import mp, mpf, pi, sqrt, erf, exp, log10, fabs, mpc

mp.dps = 40

# ---------------- (A) coefficient ----------------
print("(A) omega12^2 * sigma * (Tmax-T) in units of 1:")
for k in (1, 2):
    for c, label in ((mpf(1), "sigma=PRL (c=1)"), (mpf(1) / 36, "sigma=Braz (c=1/36)")):
        coef = c / (8 * pi) ** (2 * k)
        print(f"  k={k}  {label:22s} -> {float(coef):.6e}   (= 1/(8pi)^{2*k} x {float(c):.4g})")
print("  PRL eq.(5) printed coefficient 1/(8pi)^2 =", float(1 / (8 * pi) ** 2))
print("  1/(8pi)^4 =", float(1 / (8 * pi) ** 4))

# ---------------- (B) the 1e-28 residual ----------------
MP = mpf("2.176434e-8")      # Planck mass, kg (CODATA 2018)
MSUN = mpf("1.98847e30")     # kg
R = MSUN / MP                # M/M_P
print("\n(B) M_sun/M_P =", float(R), " log10 =", float(log10(R)))
print("    (M_P/M_sun)^(2/3) =", float(R ** (-mpf(2) / 3)), " log10 =", float(log10(R ** (-mpf(2) / 3))))
print("    authors print ~1e-28 (Braz.J.Phys. eq. 18; GRG eq. 20 text; Discrete space-time eq. 62 text)")


def window_integral(k):
    """|rho12(Tmax)/rho12(0)| from Braz.J.Phys. eqs. (16)-(17):
    (1/tau) |int dv e^{i phi(v)}| with u^3=(Tmax-v)/tP, phi = (3/(2(8pi)^k)) [ (Tmax/tP)^(2/3) - u^2 ],
    window |v-Tmax| < tau/2, tau = tP^(2/3) Tmax^(1/3) = tP * R  (Tmax/tP = R^3 as in the paper).
    ratio = (3 tP/tau) * | int_{-U}^{U} u^2 e^{-i a u^2} du |,  U = (tau/(2 tP))^(1/3) = (R/2)^(1/3).
    """
    a = mpf(3) / (2 * (8 * pi) ** k)
    U = (R / 2) ** (mpf(1) / 3)
    b = mpc(0, a)
    sb = sqrt(b)
    half = -U * exp(-b * U ** 2) / (2 * b) + sqrt(pi) / (4 * b * sb) * erf(sb * U)
    integral = 2 * half
    return 3 * fabs(integral) / R, a, U


for k in (2, 1):
    val, a, U = window_integral(k)
    print(f"    eq.(16)-(17) window integral with (8pi)^{k} in omega12: ratio = {float(val):.3e}"
          f"  (a={float(a):.4e}, U={float(U):.4e}, log10 = {float(log10(val)):.2f})")

# simple asymptotic form 3U/(a R)
for k in (2, 1):
    a = mpf(3) / (2 * (8 * pi) ** k)
    U = (R / 2) ** (mpf(1) / 3)
    print(f"    asymptotic 3U/(aR), k={k}: {float(3 * U / (a * R)):.3e}")
