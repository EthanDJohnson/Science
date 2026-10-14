"""Falsifier C3-2 (scale angle): source size and multipole.  Does a retarded QUADRUPOLE field,
with the source's near zone included down to a source radius a, yield substantially less than
the time-symmetric (standing, Pauli-Jordan) field with the same outgoing wave?

Toy (natural units, k = w = 1, q0 = 2, monochromatic, dimensionless; rates per unit time):
  psi_ret = h_l^(1)(r) Y_lm      (outgoing wave of a point multipole)
  psi_sym = 2 j_l(r) Y_lm = h^(1) + h^(2)   (time-symmetric: same outgoing part)
  sum-frequency source j = psi^2 = R(r)^2 Y_lm^2 = R^2 sum_L c_L Y_L,2m
  pair rate  Y = sum_L |c_L|^2 Int_0^2 dq q^2 (4 - q^2)^p |I_L(q)|^2,
             I_L(q) = Int_a^inf r^2 R(r)^2 j_L(q r) dr   (region r < a removed: source interior)
p = 2 mimics graviton fusion |M|^2 ~ s^2; p = 0 is a contact vertex.
Validation: l = 0 must give ret/sym = 1/12 (p=0) and 0.0200 (p=2) [M-EXAMINER-03].
Tails beyond r1 by contour rotation r -> r1 + i t (each piece decays in its half plane).
"""
import numpy as np
from math import factorial, pi
from scipy import integrate, special

def hn1(n, z):
    z = np.asarray(z, dtype=complex)
    s = sum((1j) ** k * factorial(n + k) / (factorial(k) * factorial(n - k)) / (2 * z) ** k for k in range(n + 1))
    return (-1j) ** (n + 1) * np.exp(1j * z) / z * s

def hn2(n, z):
    z = np.asarray(z, dtype=complex)
    s = sum((-1j) ** k * factorial(n + k) / (factorial(k) * factorial(n - k)) / (2 * z) ** k for k in range(n + 1))
    return (1j) ** (n + 1) * np.exp(-1j * z) / z * s

def cquad(f, a, b, **kw):
    re = integrate.quad(lambda t: np.real(f(t)), a, b, limit=400, **kw)[0]
    im = integrate.quad(lambda t: np.imag(f(t)), a, b, limit=400, **kw)[0]
    return re + 1j * im

R1 = 3.0

def p1(n, z):  # h^(1)_n(z) = e^{iz} p1(n, z)
    z = np.asarray(z, dtype=complex)
    s = sum((1j) ** k * factorial(n + k) / (factorial(k) * factorial(n - k)) / (2 * z) ** k for k in range(n + 1))
    return (-1j) ** (n + 1) / z * s

def p2(n, z):  # h^(2)_n(z) = e^{-iz} p2(n, z)
    z = np.asarray(z, dtype=complex)
    s = sum((-1j) ** k * factorial(n + k) / (factorial(k) * factorial(n - k)) / (2 * z) ** k for k in range(n + 1))
    return (1j) ** (n + 1) / z * s

def tailA(l, L, q):
    """Int_{R1}^inf r^2 h1_l(r)^2 j_L(q r) dr along r = R1 + i t, exponentials combined (decay e^{-(2-q)t})."""
    def f(t):
        z = R1 + 1j * t
        return 1j * z * z * p1(l, z) ** 2 * 0.5 * (np.exp(1j * (2 + q) * z) * p1(L, q * z) + np.exp(1j * (2 - q) * z) * p2(L, q * z))
    T = 60.0 / (2 - q)
    return cquad(f, 0, T)

def tailC(l, L, q):
    """Int_{R1}^inf r^2 |h_l(r)|^2 j_L(q r) dr = Re Int z^2 h1 h2 (z) h1_L(qz) dz on r = R1 + i t (decay e^{-q t})."""
    def f(t):
        z = R1 + 1j * t
        return 1j * z * z * p1(l, z) * p2(l, z) * np.exp(1j * q * z) * p1(L, q * z)
    T = 60.0 / q
    return np.real(cquad(f, 0, T))

SMOOTH = False   # if True: smooth window W = (1 + erf((r - a)/D))/2, D = a/8, instead of a sharp cut at a

def window(a):
    if SMOOTH and a > 0:
        D = a / 8.0
        return (lambda r: 0.5 * (1 + special.erf((r - a) / D))), max(0.0, a - 6 * D)
    return (lambda r: 1.0), a

def I_ret(l, L, q, a):
    W, lo = window(a)
    head = cquad(lambda r: W(r) * r * r * hn1(l, r) ** 2 * special.spherical_jn(L, q * r), lo, R1)
    return head + tailA(l, L, q)

def I_sym(l, L, q, a):
    W, lo = window(a)
    head = integrate.quad(lambda r: W(r) * r * r * 4 * special.spherical_jn(l, r) ** 2 * special.spherical_jn(L, q * r), lo, R1, limit=400)[0]
    return head + 2 * np.real(tailA(l, L, q)) + 2 * tailC(l, L, q)

def gaunt(l, m):
    """c_L = Int Y_lm Y_lm conj(Y_L,2m) dOmega (phi integral done analytically: 2 pi)."""
    out = {}
    for L in range(0, 2 * l + 1, 2):
        if abs(2 * m) > L:
            continue
        f = lambda th: (special.sph_harm_y(l, m, th, 0.0) ** 2 * np.conj(special.sph_harm_y(L, 2 * m, th, 0.0)) * np.sin(th)).real
        out[L] = 2 * pi * integrate.quad(f, 0, pi)[0]
    return out

xg, wg = np.polynomial.legendre.leggauss(28)
qs = 1.0 + xg      # nodes on (0, 2)
ws = wg

def rate(l, m, kind, a, p):
    cL = gaunt(l, m)
    tot = 0.0
    for L, c in cL.items():
        if abs(c) < 1e-12:
            continue
        acc = 0.0
        for q, w in zip(qs, ws):
            I = I_ret(l, L, q, a) if kind == 'ret' else I_sym(l, L, q, a)
            acc += w * q * q * (4 - q * q) ** p * abs(I) ** 2
        tot += c * c * acc
    return tot

if __name__ == "__main__":
    # sanity: z^2 h1 h2 for l=2 equals 1 + 3/z^2 + 9/z^4
    z = 1.7 + 0.4j
    print("check z^2 h1 h2 (l=2):", (z * z * hn1(2, z) * hn2(2, z)), "vs", 1 + 3 / z ** 2 + 9 / z ** 4)
    print("check j_4 closed form vs scipy at x=0.9:", (0.5 * (hn1(4, 0.9) + hn2(4, 0.9))).real, special.spherical_jn(4, 0.9))
    print("gaunt l=2 m=0:", gaunt(2, 0), " l=2 m=2:", gaunt(2, 2))
    for p in (0, 2):
        s0 = rate(0, 0, 'sym', 0.0, p); r0 = rate(0, 0, 'ret', 0.0, p)
        print(f"VALIDATION monopole p={p}: ret/sym = {r0/s0:.4f}  (expect {'0.0833' if p==0 else '0.0200'})")
    p = 2
    for (l, m, name) in [(2, 2, 'circular binary (l=2,m=2)'), (2, 0, 'linear quadrupole (l=2,m=0)')]:
        s0 = rate(l, m, 'sym', 0.0, p)
        print(f"\n{name}, p=2; normalised to the whole-space time-symmetric rate Y_sym(a=0) = {s0:.5e}")
        print("  cut a (=k a)   Y_ret(r>a)/Y_sym(0)   Y_sym(r>a)/Y_sym(0)   ret/sym at same cut")
        for a in ([0.0, 0.1, 0.3, 0.5, 1.0, 2.0] if m == 2 else [0.1, 0.2, 0.3, 0.5, 1.0, 2.0]):
            yr = rate(l, m, 'ret', a, p); ys = rate(l, m, 'sym', a, p)
            print(f"  {a:5.2f}          {yr/s0:12.4e}          {ys/s0:10.4e}          {yr/ys:10.4e}")

    # ---- smooth window (D = a/8), to remove sharp-cut leakage (cf. M-EXAMINER-04) ----
    SMOOTH = True
    print("\nSMOOTH WINDOW W = (1+erf((r-a)/(a/8)))/2, p=2")
    for (l, m, name) in [(0, 0, 'monopole'), (2, 2, 'circular (m=2)'), (2, 0, 'linear (m=0)')]:
        R1 = 3.0
        s0 = rate(l, m, 'sym', 0.0, p); r0 = rate(l, m, 'ret', 0.0, p) if m != 0 or l == 0 else float('nan')
        print(f" {name}: whole-space ret/sym = {r0/s0:.4e}")
        print("  a(=ka)  Y_ret(>a)/Y_sym(0)  Y_sym(>a)/Y_sym(0)  Y_ret(>a)/Y_ret(0)")
        for a in [0.3, 0.5, 1.0, 2.0, 3.0]:
            R1 = max(3.0, a + 6 * a / 8 + 0.5)
            yr = rate(l, m, 'ret', a, p); ys = rate(l, m, 'sym', a, p)
            print(f"  {a:4.1f}    {yr/s0:12.4e}      {ys/s0:10.4e}       {yr/r0:10.4e}")
