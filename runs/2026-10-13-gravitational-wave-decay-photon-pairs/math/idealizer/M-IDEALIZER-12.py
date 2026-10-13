"""M-IDEALIZER-12/13: kinematic closures (F10, F11). Natural units.
F10: two massless gravitons, w1 + w2 <= 2 m (1 + v^2/2), produce two scalars of mass m only if s = 2 w1 w2 (1 - cos th) >= 4 m^2.
Since w1 w2 <= ((w1 + w2)/2)^2 <= m^2 (1 + v^2/2)^2: 1 - cos th >= 2/(1 + v^2/2)^2, i.e. pi - th <= arccos(2/(1+v^2/2)^2 - 1) = 2v + O(v^3).
F11: photon of plasma mass w_p; pair needs s >= 4 w_p^2; s <= 4 w1 w2 <= (w1 + w2)^2; for w1 = w2 = w the channel is closed iff w < w_p.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import series, inequality, identity, quantity, finish
import sympy as sp

v = sp.symbols("v", positive=True)
dev = sp.acos(2 / (1 + v**2 / 2)**2 - 1)
series(dev, "v", 0, 3, 2 * v)
print("pi - theta_max at v = 1e-3:", float(dev.subs(v, sp.Rational(1, 1000))), "rad (lens 2e-3)")
quantity(f"{float(dev.subs(v, sp.Rational(1, 1000)))}", "2e-3", rel_tol=1e-3)
# AM-GM step used: w1 w2 <= ((w1 + w2)/2)^2
inequality("((w1 + w2)/2)**2", ">=", "w1*w2")
# F11: s <= (w1+w2)^2 for all angles
inequality("(w1 + w2)**2", ">=", "2*w1*w2*(1 - cc)", domain={"w1": (0.1, 10), "w2": (0.1, 10), "cc": (-1, 1)})
# threshold for equal energies: max s = 4 w^2 >= 4 wp^2  <=>  w >= wp
w, wp = sp.symbols("w w_p", positive=True)
identity(sp.solve(sp.Eq(4 * w**2, 4 * wp**2), w)[0], wp)
# numbers: f_p = (1/2pi) sqrt(n_e e^2/(eps0 m_e)); IGM n_e0 = 2.2e-7 cm^-3; early universe f_p ~ (1+z)^(3/2), photon f ~ (1+z)
e, eps0, me = 1.602176634e-19, 8.8541878128e-12, 9.1093837015e-31
fp = lambda ne_cm3: math.sqrt(ne_cm3 * 1e6 * e**2 / (eps0 * me)) / (2 * math.pi)
print(f"f_p(IGM, 2.2e-7 cm^-3) = {fp(2.2e-7):.3f} Hz; f_p(0.03 cm^-3) = {fp(0.03):.0f} Hz; 150 Hz closed for 1+z > {(150/fp(2.2e-7))**2:.0f}")
quantity(f"{fp(2.2e-7)}", "4.2", rel_tol=1e-2)
quantity(f"{(150/fp(2.2e-7))**2}", "1300", rel_tol=0.05)
raise SystemExit(finish())
