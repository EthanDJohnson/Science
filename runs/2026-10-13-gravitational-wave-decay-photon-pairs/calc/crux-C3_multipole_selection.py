"""Crux C3: angular selection rule for the sum-frequency (q0 = 2w) source psi^2.

Scalar toy of verdicts C3-0/1/2 (natural units, k = w = 1). The positive-frequency
field of a mode (l, m) is psi = R_l(r) Y_lm e^{-iwt}; the fusion source at q0 = 2w is
psi_a * psi_b (positive x positive frequency). Expand Y_la,ma * Y_lb,mb in Y_LM
(Gaunt coefficients) and count the small-r behaviour of each L-part of the Fourier
amplitude J_L(q) = Int r^2 dr R_a R_b j_L(q r), with near zone R_l ~ (kr)^-(l+1):
integrand ~ r^(2 - (la+1) - (lb+1) + L). Converges at r -> 0 iff exponent > -1.
If divergent with exponent e < -1, J ~ a^(e+1) and yield |J|^2 ~ a^(2(e+1)).
"""
import sympy as sp

th, ph = sp.symbols('theta phi', real=True)


def Y(l, m):
    return sp.simplify(sp.Ynm(l, m, th, ph).expand(func=True))


def gaunt_parts(la, ma, lb, mb):
    prod = Y(la, ma) * Y(lb, mb)
    out = {}
    M = ma + mb
    for L in range(abs(la - lb), la + lb + 1):
        if abs(M) > L:
            continue
        c = sp.integrate(sp.integrate(prod * sp.conjugate(Y(L, M)) * sp.sin(th),
                                      (ph, 0, 2 * sp.pi)), (th, 0, sp.pi))
        c = sp.nsimplify(sp.simplify(c))
        if c != 0:
            out[L] = c
    return M, out


cases = [
    ("circular binary, dominant (2,+2)x(2,+2)", 2, 2, 2, 2),
    ("circular binary cross (2,+2)x(3,+3)", 2, 2, 3, 3),
    ("circular binary cross (2,+2)x(2,+1) [mass asymmetry]", 2, 2, 2, 1),
    ("linear/head-on quadrupole (2,0)x(2,0)", 2, 0, 2, 0),
    ("monopole (0,0)x(0,0)", 0, 0, 0, 0),
]
for name, la, ma, lb, mb in cases:
    M, parts = gaunt_parts(la, ma, lb, mb)
    print(f"{name}: M = {M}")
    for L, c in parts.items():
        e = 2 - (la + 1) - (lb + 1) + L
        if e > -1:
            note = "converges at r->0 (no near-zone divergence)"
        else:
            note = f"diverges: yield ~ (ka)^{2*(e+1)}"
        print(f"   L = {L}: Gaunt coeff = {c} ~ {float(c):.4f}; small-r integrand ~ r^{e}; {note}")
print("Note: monopole retarded h0 ~ 1/(kr) gives r^0 for L=0 -> converges (finite 1/12 ratio).")
