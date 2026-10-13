"""M-EXAMINER-11: profile dependence of the narrow-band coherent-fusion total (natural units).
Own derivation: for fixed q = k1 + k2 (|q| >> sigma), the pair amplitude ∝ angular factor x (a*a)(q0), with a(k) the
radial amplitude profile and (a*a) its autoconvolution; N ∝ Int a^2 dk. So at fixed N, w and sigma:
  c_tot ∝ Int (a*a)(q0)^2 dq0 / (Int a^2)^2.
B&O's 2 pi delta(0) -> T bookkeeping (definition taken from the toolkit docstring, as a convention):
  T_eff = 2 pi Int (a*a)^2 dq0 / (Int a dk)^4.
Profiles: top hat a = Theta on [w - sigma/2, w + sigma/2]; Gaussian a = Theta exp(-(k-w)^2/(2 sigma^2)).
Claims: T_eff = (4 pi/3)/sigma and sqrt(pi/2)/sigma; c_tot(Gauss)/c_tot(top hat) = 0.60/0.16 = 3.76;
c_rate = c_tot/(sigma T_eff) ratio Gauss/top hat = 12.57 (lens: 12.6)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, finish

x, y, s, Th = sp.symbols("x y sigma Theta", positive=True)
xr = sp.Symbol("xr", real=True)
# top hat centred at 0: autoconvolution triangle Theta^2 (sigma - abs(x)) on [-sigma, sigma]
tri = Th ** 2 * (s - xr)
J_top = 2 * sp.integrate(tri ** 2, (xr, 0, s))
N_top = Th ** 2 * s
I_top = Th * s
# Gaussian: (a*a)(x) = Theta^2 sigma sqrt(pi) exp(-x^2/(4 sigma^2)); verify the autoconvolution directly
u = sp.Symbol("u", real=True)
conv = sp.integrate(Th * sp.exp(-u ** 2 / (2 * s ** 2)) * Th * sp.exp(-(xr - u) ** 2 / (2 * s ** 2)), (u, -sp.oo, sp.oo))
identity(sp.simplify(conv), Th ** 2 * s * sp.sqrt(sp.pi) * sp.exp(-xr ** 2 / (4 * s ** 2)), domain={"xr": (-3, 3)})
J_g = sp.integrate(sp.simplify(conv) ** 2, (xr, -sp.oo, sp.oo))
N_g = sp.integrate(Th ** 2 * sp.exp(-u ** 2 / s ** 2), (u, -sp.oo, sp.oo))
I_g = sp.integrate(Th * sp.exp(-u ** 2 / (2 * s ** 2)), (u, -sp.oo, sp.oo))
T_top = sp.simplify(2 * sp.pi * J_top / I_top ** 4)
T_g = sp.simplify(2 * sp.pi * J_g / I_g ** 4)
print("T_eff top hat =", T_top, "; Gaussian =", T_g)
identity(T_top, 4 * sp.pi / (3 * s))
identity(T_g, sp.sqrt(sp.pi / 2) / s)
ctot_ratio = sp.simplify((J_g / N_g ** 2) / (J_top / N_top ** 2))
print("c_tot Gauss/top =", ctot_ratio, "=", sp.N(ctot_ratio), "; 0.16 x that =", sp.N(sp.Rational(4, 25) * ctot_ratio))
identity(ctot_ratio, sp.Rational(3, 2) * sp.sqrt(2 * sp.pi))
crate_ratio = sp.simplify(ctot_ratio * (T_top / T_g))
print("c_rate Gauss/top =", crate_ratio, "=", sp.N(crate_ratio))
identity(crate_ratio, 4 * sp.pi)
# cross-check against the toolkit docstring constants J_f/(N^2 sigma/w^2): 16 sqrt(2pi) pi^4 vs 32 pi^4/3
identity(16 * sp.sqrt(2 * sp.pi) * sp.pi ** 4 / (32 * sp.pi ** 4 / 3), ctot_ratio)
# limit/consistency: both c_tot scale as sigma^1 at fixed N (J/N^2 ∝ sigma) -> ratio sigma-independent
limit(ctot_ratio, "sigma", 0, sp.Rational(3, 2) * sp.sqrt(2 * sp.pi))
raise SystemExit(finish())
