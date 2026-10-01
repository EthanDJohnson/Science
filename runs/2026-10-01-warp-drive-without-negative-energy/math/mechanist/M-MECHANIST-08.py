"""M-MECHANIST-08: start-and-stop photon-rocket budget at v = 0.04 c (SI).

Own derivation: one leg, rest mass m_i -> m_f + photons; energy m_i c^2 = gamma m_f c^2 + E_ph,
momentum 0 = gamma m_f v - E_ph/c  =>  m_i/m_f = gamma (1 + v/c) = sqrt((1+b)/(1-b)).
Start then stop (second leg from rest in the moving frame): ratio (1+b)/(1-b).
Exhaust energy (m_i - m_f) c^2 with m_f = final mass (shell + payload) = 4.511e27 kg + 1e5 kg.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, series, quantity, units, finish

b = sp.symbols("b", positive=True)
gam = 1 / sp.sqrt(1 - b**2)
identity(gam * (1 + b), sp.sqrt((1 + b) / (1 - b)), domain={"b": (0.001, 0.99)})
identity((gam * (1 + b))**2, (1 + b) / (1 - b), domain={"b": (0.001, 0.99)})
series((1 + b) / (1 - b) - 1, "b", 0, 2, "2*b")  # Newtonian limit: 2 mv c per... exhaust mass 2 m v / c
c = 2.99792458e8
Mf = 4.5114e27 + 1e5
R = 1.04 / 0.96
quantity(f"{R} m/m", "1.0833 m/m", rel_tol=1e-4)
p = Mf * 0.04 * c / (1 - 0.04**2) ** 0.5
quantity(f"{p} kg*m/s", "5.41e34 kg*m/s", rel_tol=0.003)
E = (R - 1) * Mf * c**2
quantity(f"{E} J", "3.38e43 J", rel_tol=0.003)
quantity(f"{E} J / (2.99792458e8 m/s)^2", "3.76e26 kg", rel_tol=0.003)
quantity(f"{E/c**2} kg", "0.198 Mjup", rel_tol=0.005)
quantity(f"{E} J / (592.2e18 J)", "5.7e22", rel_tol=0.01)
Ep = (R - 1) * 1e5 * c**2
quantity(f"{Ep} J", "7.49e20 J", rel_tol=0.002)
quantity(f"{Ep} J / (592.2e18 J)", "1.26", rel_tol=0.005)
quantity(f"{E/Ep}", "4.51e22", rel_tol=0.003)
P = 4.5114e27 * 9.80665 * c
quantity(f"{P} W", "1.33e37 W", rel_tol=0.005)
quantity(f"{P} W", "3.5e10 Lsun", rel_tol=0.02)
import math
tacc = c * math.atanh(0.04) / 9.80665
quantity(f"{tacc} s", "1.2268e6 s", rel_tol=0.005)
units("1 kg * (1 m/s^2) * (3e8 m/s)", "W")
raise SystemExit(finish())
