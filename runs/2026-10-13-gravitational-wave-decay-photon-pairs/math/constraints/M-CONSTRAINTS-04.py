"""M-CONSTRAINTS-04: hbar counting of B&O eqs. 8, 11, 12; pairs per burst; hoop cap.
Eq. 8 (natural units): dP/dt = 3 G^2 N^2 w^3 sigma^2/(25 pi). Restore SI by the dimensionless coupling
G_nat w^2 -> G hbar w^2/c^5 and the overall 1/time from w: dP/dt = (3/(25 pi)) (G hbar w^2/c^5)^2 N^2 sigma^2 / w.
N = E/(hbar w). Eq. 11: W = 2 hbar w dP/dt (two photons of energy hbar w each per pair).
Eq. 12: W = (3/(50 pi)) (r_m/l)^2 hbar w^2 with r_m = 2 G E/c^4, l = c/sigma (dossier D-24: l = c dt).
Pairs per burst = dP/dt * (1/sigma). Hoop cap r_m <= l, eps = sigma/w = 0.1.
Stimulated: W_st = W (1 + 2f), f = kT/(hbar w) (RJ), leading term 2f.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, units, limit, quantity, finish

G, E, w, sg, c, hb, kT = sp.symbols("G E_rel omega sigma c hbar kT", positive=True)
N = E / (hb * w)
rate = sp.Rational(3, 25) / sp.pi * (G * hb * w**2 / c**5)**2 * N**2 * sg**2 / w
rate = sp.simplify(rate)
print("dP/dt SI =", rate)
identity(rate, 3 * G**2 * E**2 * w * sg**2 / (25 * sp.pi * c**10))
identity(sp.diff(rate, hb), 0)
units("G^2 * (1 J)^2 * (1 Hz)^3 / c^10", "Hz")
W11 = 2 * hb * w * rate
identity(W11, 6 * G**2 * hb * E**2 * w**2 * sg**2 / (25 * sp.pi * c**10))
rm, l = 2 * G * E / c**4, c / sg
W12 = sp.Rational(3, 50) / sp.pi * (rm / l)**2 * hb * w**2
identity(W11, W12)
units("hbar * (1 Hz)^2", "W")
pairs = rate / sg
identity(pairs, sp.Rational(3, 100) / sp.pi * (rm / l)**2 * (w / sg))
# hoop cap: r_m = l, eps = 0.1
cap = sp.Rational(3, 100) / sp.pi * 10
print("cap at eps=0.1:", sp.N(cap))
quantity(f"{float(cap)}", "0.095", rel_tol=0.01)
# stimulated power: W (1 + 2 kT/(hbar w)) leading in hbar -> 0
Wst = W11 * (1 + 2 * kT / (hb * w))
limit(Wst, "hbar", 0, 12 * G**2 * E**2 * kT * w * sg**2 / (25 * sp.pi * c**10))
raise SystemExit(finish())
