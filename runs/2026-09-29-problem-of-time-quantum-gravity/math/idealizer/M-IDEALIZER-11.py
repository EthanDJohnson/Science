"""M-IDEALIZER-11 (F11): Sr clock (omega = 2 pi x 429.2 THz) in a superposition of heights dh near Earth's surface (SI).
Weak-field proper-time rate difference: d(tau)/dt = 1 + Phi/c^2, Phi = g h => d(tau_1 - tau_2)/dt = g dh / c^2.
Phase rate between branches for a clock transition omega: d(dphi)/dt = omega g dh / c^2 (rad/s).
Internal-state (which-path) visibility |cos(dphi/2)| first vanishes at dphi = pi: t = pi c^2/(omega g dh).
Claim: 2.94e-4, 2.94e-3, 0.294, 2.94 rad/s for dh = 1 mm, 1 cm, 1 m, 10 m; zeros at 1.07e4, 1.07e3, 10.7, 1.07 s.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import quantity, units, series, finish

# derive the height term from Schwarzschild: sqrt(1 - 2GM/(r c^2)) with r = R + h, to first order in 1/c^2 and h
G, Mm, R, h, c = sp.symbols("G M R h c", positive=True)
x = sp.symbols("x", positive=True)   # x = 1/c^2
rate = sp.sqrt(1 - 2 * G * Mm * x / (R + h))
d = sp.diff(sp.series(rate, x, 0, 2).removeO(), h).subs(h, 0)   # d(rate)/dh at h = 0, first order in x
series(sp.diff(rate, h).subs(h, 0), "x", 0, 2, G * Mm * x / R**2)   # = g/c^2 with g = GM/R^2
print("d(dtau/dt)/dh =", sp.simplify(d))

w = "2*pi*429.2e12 Hz"
units(f"{w} * 9.807 m/s^2 * 1 mm / c^2", "1/s")
for dh, rate_want, t_want in [("1 mm", "2.94e-4 1/s", "1.07e4 s"), ("1 cm", "2.94e-3 1/s", "1.07e3 s"),
                               ("1 m", "0.294 1/s", "10.7 s"), ("10 m", "2.94 1/s", "1.07 s")]:
    quantity(f"{w} * 9.807 m/s^2 * {dh} / c^2", rate_want, rel_tol=3e-3)
    quantity(f"pi * c^2 / ({w} * 9.807 m/s^2 * {dh})", t_want, rel_tol=5e-3)
raise SystemExit(finish())
