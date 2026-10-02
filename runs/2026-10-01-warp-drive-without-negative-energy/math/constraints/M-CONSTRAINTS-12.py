"""M-CONSTRAINTS-12: shell density and stress arithmetic (F14; B). SI.
Inputs (toolkit outputs, not re-derived): eps_peak = 1.38e40 J/m^3, p_t peak 3.87e39 Pa.
rho = eps/c^2; nuclear saturation 0.16 fm^-3 x m_n = 2.68e17 kg/m^3 (the lens used ~2.3e17, unsourced).
Max |p|/eps from the toolkit's zero-shift profiles (own max over the grid). Also eps_peak in geometric units.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import numpy as np
from math_checks import quantity, finish
from warp_shell import build_shell

quantity("1.38e40 J/m^3 / c^2", "1.53e23 kg/m^3", rel_tol=5e-3)
quantity("1.38e40 J/m^3 / c^2 / (2.3e17 kg/m^3)", "6.7e5", rel_tol=1e-2)
quantity("1.38e40 J/m^3 / c^2 / (0.16e45 m^-3 * 1.674927e-27 kg)", "5.7e5", rel_tol=1e-2)
quantity(f"{math.log10(3.87e39 / 1e12)}", "27.6", rel_tol=2e-3)
sh = build_shell(4.49e27, 10.0, 20.0)
pr = sh.profiles()
eps, p_r, p_t = pr["eps"], pr["p_r"], pr["p_t"]
mask = eps > 1e-6 * eps.max()
w = np.max(np.maximum(np.abs(p_r[mask]), np.abs(p_t[mask])) / eps[mask])
print("eps max", eps.max(), " p_t max", p_t.max(), " p_t min", p_t.min(), " max |p|/eps", w)
quantity(f"{eps.max()}", "1.38e40", rel_tol=1e-2)
quantity(f"{p_t.max()}", "3.87e39", rel_tol=1e-2)
quantity(f"{w}", "0.596", rel_tol=1e-2)
quantity("1.35e40 J/m^3 * G/c^4", "1.115e-4 m^-2", rel_tol=3e-3)
raise SystemExit(finish())
