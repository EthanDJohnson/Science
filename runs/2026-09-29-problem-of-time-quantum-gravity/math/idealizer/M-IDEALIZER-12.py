"""M-IDEALIZER-12 (F12): clock near a source mass m in a superposition of distances d1, d2 (SI, Newtonian, O(1/c^2)).
Proper-time difference rate: Phi_i = -G m / d_i => d(tau_1 - tau_2)/dt = G m (1/d2 - 1/d1)/c^2 in magnitude G m (1/d1 - 1/d2)/c^2.
Phase: dphi = omega G m (1/d1 - 1/d2) t / c^2. For dphi = 1 rad in t = 1 s: m* = c^2/(omega G (1/d1 - 1/d2) t).
Claim (Sr, omega = 2 pi 429.2 THz): 1.8e8 kg (200/450 um), 1.0e9 kg (1/2 mm), 1.0e10 kg (1/2 cm).
Compton clock omega_C = m' c^2/hbar: dphi = G m m' t (1/d1 - 1/d2)/hbar. m = m' = 1e-14 kg: 0.176 rad (1 s), 0.440 rad (2.5 s);
omega_C = 8.5e36 rad/s, ratio to Sr 3.2e21.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, units, limit, finish

G, m, mp_, t, c, hbar, d1, d2, w = sp.symbols("G m m_p t c hbar d_1 d_2 omega", positive=True)
dphi = w * G * m * (1 / d1 - 1 / d2) * t / c**2
identity(dphi.subs(w, mp_ * c**2 / hbar), G * m * mp_ * t * (1 / d1 - 1 / d2) / hbar)
limit(dphi, "d_2", "oo", w * G * m * t / (d1 * c**2))   # far branch at infinity: single-potential redshift
w_sr = "(2*pi*429.2e12 Hz)"
units(f"c^2 / ({w_sr} * G * (1/(200 um) - 1/(450 um)) * 1 s)", "kg")
quantity(f"c^2 / ({w_sr} * G * (1/(200 um) - 1/(450 um)) * 1 s)", "1.8e8 kg", rel_tol=0.01)
quantity(f"c^2 / ({w_sr} * G * (1/(1 mm) - 1/(2 mm)) * 1 s)", "1.0e9 kg", rel_tol=0.01)
quantity(f"c^2 / ({w_sr} * G * (1/(1 cm) - 1/(2 cm)) * 1 s)", "1.0e10 kg", rel_tol=0.01)
quantity("1e-14 kg * c^2 / hbar", "8.5e36 Hz", rel_tol=0.01)
quantity(f"1e-14 kg * c^2 / hbar / {w_sr}", "3.2e21", rel_tol=0.02)
units("G * (1e-14 kg)^2 * 1 s * (1/(200 um) - 1/(450 um)) / hbar", "1")
quantity("G * (1e-14 kg)^2 * 1 s * (1/(200 um) - 1/(450 um)) / hbar", "0.176", rel_tol=3e-3)
quantity("G * (1e-14 kg)^2 * 2.5 s * (1/(200 um) - 1/(450 um)) / hbar", "0.440", rel_tol=3e-3)
raise SystemExit(finish())
