"""Consistency check for P3: eq.8 as the peak of a sinc^4 time profile.

If the two-graviton energy spectrum is a top hat of width sigma, the pair-production
amplitude as a function of time is proportional to sinc^2(sigma t / 2) (two factors of the
top-hat transform), so the rate is R(t) = R(0) sinc^4(sigma t / 2).  Then
  T_eff = Int R(t)/R(0) dt = (2/sigma) Int sinc^4(x) dx = (2/sigma)(2 pi/3) = 4 pi/(3 sigma)
and P_tot = R(0) T_eff.  With R(0) = 3 G^2 N^2 w^3 sigma^2/(25 pi) (B&O eq.8):
  P_tot = (4/25) G^2 N^2 w^3 sigma   (our report, item 5).
This script checks the integral numerically and the algebra symbolically.
It does NOT recompute the amplitude; it only checks the rate -> total bookkeeping.
"""
import sympy as sp
import numpy as np
from scipy import integrate

x = sp.symbols('x', real=True)
I_sym = sp.integrate(sp.sinc(x)**4, (x, -sp.oo, sp.oo))
print("symbolic Int sinc^4 dx =", sp.simplify(I_sym), "=", sp.N(I_sym), " (2 pi/3 =", float(2*np.pi/3), ")")

f = lambda t: np.sinc(t/np.pi)**4          # np.sinc(u)=sin(pi u)/(pi u) -> sin(t)/t
val, err = integrate.quad(f, -2000*np.pi, 2000*np.pi, limit=20000)
print("numeric  Int sinc^4 dx (|x|<2000 pi) =", val, "+-", err)

G, N, w, s = sp.symbols('G N omega sigma', positive=True)
R0 = 3*G**2*N**2*w**3*s**2/(25*sp.pi)
Teff = 4*sp.pi/(3*s)
print("R0*Teff =", sp.simplify(R0*Teff), " target (4/25) G^2 N^2 w^3 sigma:",
      sp.simplify(R0*Teff - sp.Rational(4,25)*G**2*N**2*w**3*s) == 0)
