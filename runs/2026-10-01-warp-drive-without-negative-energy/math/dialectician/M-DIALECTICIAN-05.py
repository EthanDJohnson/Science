"""M-DIALECTICIAN-05: constant-density TOV shell at R1 = 10 m, R2 = 20 m, M = 4.49e27 kg.
Claims: m = GM/c^2 = 3.334 m; 2m/R2 = 0.333; alpha(R2) = 0.816; alpha_in = 0.761 (TOV) / 0.769 (pressure-free);
P(R1) = 0.073 rho (unbalanced). Geometric units for m, rho (1/m^2), P (1/m^2).
"""
import sys, os
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from math_checks import quantity, identity, limit, units, finish
from tovshell import shell

s = shell(4.49e27, 10.0, 20.0, pressure=True)
s0 = shell(4.49e27, 10.0, 20.0, pressure=False)
s_half = shell(4.49e27, 10.0, 20.0, pressure=True, n=100000)
print(f"m = {s['m']:.5f} m, 2m/R2 = {2*s['m']/20:.5f}, rho0 = {s['rho0']:.5e} 1/m^2")
print(f"alpha(R2) = {s['alpha_R2']:.5f}; alpha_in TOV = {s['alpha_in']:.5f} (n/2: {s_half['alpha_in']:.7f}); pressure-free = {s0['alpha_in']:.5f}")
print(f"P(R1)/rho = {s['P_R1']/s['rho0']:.5f}")
quantity("G*4.49e27 kg/c^2", "3.334 m", rel_tol=5e-4)
quantity(f"{2*s['m']/20}", "0.333", rel_tol=2e-3)
quantity(f"{s['alpha_R2']}", "0.816", rel_tol=1e-3)
quantity(f"{s['alpha_in']}", "0.761", rel_tol=1e-3)
quantity(f"{s0['alpha_in']}", "0.769", rel_tol=1e-3)
quantity(f"{s['P_R1']/s['rho0']}", "0.073", rel_tol=1e-2)
# pressure-free closed form check: d ln alpha/dr = m/(r(r-2m)) with constant-density m(r): compare tiny-M limit alpha -> 1
t = shell(1e20, 10.0, 20.0, pressure=True)
print("tiny-mass limit alpha_in =", t["alpha_in"])
quantity(f"{t['alpha_in']}", "1", rel_tol=1e-6)
# weak-field limit: alpha_in ≈ 1 - Phi_in, Phi_in = (3/2) m (R2^2 - R1^2)/(R2^3 - R1^3) for a uniform shell (Newtonian potential at centre)
Mw = 1e24
w = shell(Mw, 10.0, 20.0, pressure=False)
phi_c = 1.5 * w["m"] * (20**2 - 10**2) / (20**3 - 10**3)
print(f"weak field: 1 - alpha_in = {1-w['alpha_in']:.6e}, Newtonian Phi_c = {phi_c:.6e}")
quantity(f"{1-w['alpha_in']}", f"{phi_c}", rel_tol=1e-3)
units("G*1 kg/c^2", "m")
raise SystemExit(finish())
