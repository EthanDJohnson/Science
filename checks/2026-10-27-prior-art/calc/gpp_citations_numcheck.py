"""Independent re-check of the finding's numbers from GPP's printed eqs (2),(4),(5) (hep-th/0406260).
(1) omega12^2 * sigma * (Tmax-T) should be a constant; compare with (8 pi)^-4 and (8 pi)^-2.
(2) coherence left one Planck time before Tmax: ((Tmax-T)/Tmax)^k at Tmax-T = t_P, for both k.
(3) Tmax - T at which one e-fold of decoherence is reached: Tmax * exp(-1/k).
Units: SI seconds. t_P = 5.391247e-44 s. Tmax values as in the verdict: 6.6e74 s (solar mass), 8.4e19 s (1e12 kg).
"""
import sympy as sp
from mpmath import mp, mpf, log, exp, pi, log10

# (1) symbolic
tP, Tm, T = sp.symbols("t_P T_max T", positive=True)
x = Tm - T
omega12 = 1 / ((8 * sp.pi) ** 2 * tP) * (tP / x) ** sp.Rational(1, 3)   # eq (4)
sigma = (tP / x) ** sp.Rational(1, 3) * tP                               # stated sigma(T)
prod = sp.simplify(omega12 ** 2 * sigma * x)
print("omega12^2 * sigma * (Tmax-T) =", prod, " == (8 pi)^-4 ?", sp.simplify(prod - (8 * sp.pi) ** -4) == 0)
print("(8 pi)^-4 =", sp.N((8 * sp.pi) ** -4), "  (8 pi)^-2 =", sp.N((8 * sp.pi) ** -2))

# (2), (3) numeric
mp.dps = 30
t_P = mpf("5.391247e-44")
k_paper = 1 / (8 * pi) ** 2
k_cons = 1 / (8 * pi) ** 4
for name, Tmax in (("solar mass", mpf("6.6e74")), ("1e12 kg", mpf("8.4e19"))):
    for label, k in (("paper k=(8pi)^-2", k_paper), ("consistent k=(8pi)^-4", k_cons)):
        left = exp(k * log(t_P / Tmax))          # |rho12|/|rho12(0)| at Tmax - T = t_P (phase drops out)
        efold = log10(Tmax) - 1 / (k * mp.log(10))  # log10 of (Tmax - T) where coherence = 1/e
        print(f"{name:11s} {label:22s} coherence at Tmax-t_P = {mp.nstr(left, 6):>10s}   log10(Tmax-T at 1 e-fold) = {mp.nstr(efold, 6)}")
print("log10(t_P) =", mp.nstr(log10(t_P), 5))
