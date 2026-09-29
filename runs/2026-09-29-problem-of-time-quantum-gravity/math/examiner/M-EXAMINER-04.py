"""M-EXAMINER-04: two-level clock in a superposition of heights; interferometric visibility and its first zero.

Claim (finding 8, EXAMINER-A prediction, hardest question 6), SI:
  V = |cos(omega Delta tau / 2)| for a clock in (|0> + |1>)/sqrt2 with gap hbar omega,
  Delta tau = g Delta h T / c^2 (fixed Earth field), first zero at Delta tau = pi/omega, i.e.
  T Delta h = pi c^2 / (omega g) = c^2/(2 f g) = 10.7 m s (Sr, f = 429 THz), 4.98e5 m s (Cs, f = 9.19 GHz), g = 9.82 m/s^2.
Independent derivation: internal state on arm k after proper time tau_k is (|0> + e^{-i omega tau_k}|1>)/sqrt2
(global phases dropped, they are the which-path phase and do not affect V). V = |<chi_1|chi_2>|.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

w, t1, t2 = sp.symbols("omega tau1 tau2", positive=True)
chi1 = sp.Matrix([1, sp.exp(-sp.I * w * t1)]) / sp.sqrt(2)
chi2 = sp.Matrix([1, sp.exp(-sp.I * w * t2)]) / sp.sqrt(2)
ov = (chi1.H * chi2)[0]
V2 = sp.simplify(sp.expand_complex(ov * sp.conjugate(ov)))
dt = sp.symbols("dtau", positive=True)
identity(V2.subs(t2, t1 + dt), sp.cos(w * dt / 2)**2)
# limit: no proper-time difference -> full visibility
limit(sp.cos(w * dt / 2)**2, "dtau", 0, 1)
# first zero: cos(omega dtau/2) = 0 at dtau = pi/omega
identity(sp.cos(w * (sp.pi / w) / 2), 0)

quantity("pi * c^2 / (2*pi*429 THz * 9.82 m/s^2)", "10.7 m*s", rel_tol=5e-3)  # 10.667 rounds to 10.7
quantity("c^2 / (2 * 429 THz * 9.82 m/s^2)", "10.7 m*s", rel_tol=5e-3)  # 10.667 rounds to 10.7
quantity("pi * c^2 / (2*pi*9.192631770 GHz * 9.82 m/s^2)", "4.98e5 m*s", rel_tol=2e-3)
units("c^2 / (429 THz * 9.82 m/s^2)", "m*s")

raise SystemExit(finish())
