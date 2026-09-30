"""M-CONSTRAINTS-12: Gambini-Porto-Pullin realistic-clock decoherence (SI).

Dossier Q-15 formula: ln(rho12(T)/rho12(0)) = -(3/2) t_P^(4/3) T^(2/3) omega^2 (dimensionless: s^(4/3) s^(2/3) s^-2).
Clock-time uncertainty consistent with it: exponent = (3/2) omega^2 dT^2 with dT = t_P^(2/3) T^(1/3)
(the analysis does not state its dT formula; this is the reading that reproduces it).
Claims (F12): dT(1 s) = 1.43e-29 s, dT(92 h) = 9.9e-28 s; Sr 92 h timing 7.6e-21 * 92 h = 2.5e-15 s; gap 2.5e12;
exponent (omega = 2 pi 429 THz) = 2.2e-27 (1 s), 2.2e-22 (1 yr), 1.3e-15 (13.8 Gyr);
1% coherence loss in 1 s needs omega = 5.7e27 rad/s, hbar omega = 3.8e12 eV.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, units, finish

tP, T, w = sp.symbols("t_P T w", positive=True)
dT = tP**sp.Rational(2, 3) * T**sp.Rational(1, 3)
identity(sp.Rational(3, 2) * w**2 * dT**2, sp.Rational(3, 2) * tP**sp.Rational(4, 3) * T**sp.Rational(2, 3) * w**2)
units("t_P^(4/3) * (1 s)^(2/3) * (2*pi*429 THz)^2", "dimensionless")
quantity("t_P^(2/3) * (1 s)^(1/3)", "1.43e-29 s", rel_tol=5e-3)
quantity("t_P^(2/3) * (92 h)^(1/3)", "9.9e-28 s", rel_tol=5e-3)
quantity("7.6e-21 * 92 h", "2.5e-15 s", rel_tol=0.02)
quantity("7.6e-21 * 92 h / (t_P^(2/3) * (92 h)^(1/3))", "2.5e12", rel_tol=0.03)
ex = "1.5 * t_P^(4/3) * ({})^(2/3) * (2*pi*429 THz)^2"
quantity(ex.format("1 s"), "2.2e-27", rel_tol=0.02)
quantity(ex.format("1 yr"), "2.2e-22", rel_tol=0.03)
quantity(ex.format("13.8 Gyr"), "1.3e-15", rel_tol=0.03)
# 1% loss: exponent = -ln(0.99) = 0.01005
quantity("(0.01005/(1.5 * t_P^(4/3) * (1 s)^(2/3)))^0.5", "5.7e27 1/s", rel_tol=0.01)
quantity("hbar*(0.01005/(1.5 * t_P^(4/3) * (1 s)^(2/3)))^0.5", "3.8e12 eV", rel_tol=0.01)
raise SystemExit(finish())
