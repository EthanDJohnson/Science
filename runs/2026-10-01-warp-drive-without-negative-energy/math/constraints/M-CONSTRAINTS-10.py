"""M-CONSTRAINTS-10: momentum, photon-rocket, clock and reframe numbers (F13, CONSTRAINTS-B, E, F).

SI. M_ADM = 4.511e27 kg (toolkit, input). Momentum per leg gamma M v. Photon rocket, own derivation:
one leg m_i/m_f = sqrt((1+b)/(1-b)); start + stop (1+b)/(1-b). Radiated mass m_i - m_f.
Clock: interior static observers tick e^a = 0.761 of shell time; shell time = exterior time/gamma.
Rocket with equal time dilation: 1/gamma = 0.761 => b = sqrt(1 - 0.761^2). Trip 4.37 ly at b.
Interior Eulerian speed relative to the shell b_w/N with N = e^a (M-MECHANIST-06 form, lowest order).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, series, quantity, finish

b = sp.symbols("b", positive=True)
g = 1 / sp.sqrt(1 - b**2)
identity(g * (1 + b), sp.sqrt((1 + b) / (1 - b)), domain={"b": (0.001, 0.99)})
series((1 + b) / (1 - b), "b", 0, 2, "1 + 2*b")
c = 299792458.0
M = 4.511e27
for bb, p in ((0.0244, "3.30e34"), (0.04, "5.41e34")):
    quantity(f"{M * bb * c / math.sqrt(1 - bb**2)} kg*m/s", f"{p} kg*m/s", rel_tol=3e-3)
ratio = 1.0244 / 0.9756
quantity(f"{ratio}", "1.050", rel_tol=1e-3)
rad_init = M * (1 - 1 / ratio)      # 4.511e27 kg taken as the INITIAL mass
rad_final = M * (ratio - 1)         # taken as the FINAL mass
print("radiated, M initial:", rad_init, " M final:", rad_final)
quantity(f"{rad_init} kg", "2.15e26 kg", rel_tol=3e-3)
quantity(f"{rad_init} kg * c^2", "1.93e43 J", rel_tol=3e-3)
pay_final = 1e5 * (ratio - 1); pay_init = 1e5 * (1 - 1 / ratio)
print("payload radiated, 1e5 final:", pay_final, " 1e5 initial:", pay_init)
quantity(f"{pay_final} kg", "5.0e3 kg", rel_tol=3e-3)
ea = 0.761
quantity(f"{math.sqrt(1 - ea**2)}", "0.649", rel_tol=1e-3)
ly_yr = 4.37
t_out = ly_yr / 0.0244
t_in = t_out * ea * math.sqrt(1 - 0.0244**2)
print("trip outside", t_out, "inside", t_in)
quantity(f"{t_out} yr", "179 yr", rel_tol=3e-3)
quantity(f"{t_in} yr", "136 yr", rel_tol=3e-3)
quantity(f"{0.02 / ea}", "0.026", rel_tol=2e-2)
quantity(f"{0.0244 / ea}", "0.032", rel_tol=1e-2)
quantity(f"{0.02386 / ea}", "0.0314", rel_tol=1e-2)    # corrected beta_crit
raise SystemExit(finish())
