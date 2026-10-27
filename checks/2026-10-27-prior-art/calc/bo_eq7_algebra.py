"""Check that B&O eq. 7's kinematic factor (s^2 - 2tu)/s is the equal-sign sum of the eq. 6 magnitudes.

Eq. 6:  A++++ = A---- = 8 pi G t^2/s ,  A++-- = A--++ = 8 pi G u^2/s .
Eq. 7 prefactor: 4 pi G (s^2 - 2 t u)/s.
For four massless particles s + t + u = 0, so s^2 - 2tu = (t+u)^2 - 2tu = t^2 + u^2.
Hence eq. 7 prefactor = (1/2)(A_t + A_u) with A_t = 8 pi G t^2/s, A_u = 8 pi G u^2/s: the two eq. 6
amplitude types added with the SAME (positive) sign, no relative phase.
"""
import sympy as sp

s, t, u, G = sp.symbols("s t u G")
pref = 4 * sp.pi * G * (s**2 - 2 * t * u) / s
At = 8 * sp.pi * G * t**2 / s
Au = 8 * sp.pi * G * u**2 / s
diff = sp.simplify((pref - sp.Rational(1, 2) * (At + Au)).subs(s, -t - u))
print("eq7 prefactor - (A_t + A_u)/2 with s = -t-u  ->", diff)

# the relative sign matters: with a relative minus sign the factor would be t^2 - u^2 instead
alt = sp.simplify((4 * sp.pi * G * (t**2 - u**2) / s).subs(s, -t - u))
print("with opposite relative sign the factor would be 4piG(t-u)(t+u)/s =", alt)
