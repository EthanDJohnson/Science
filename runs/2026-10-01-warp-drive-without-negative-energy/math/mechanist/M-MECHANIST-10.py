"""M-MECHANIST-10: induction drag kappa = 4GM/(c^2 R) (linear theory, pushing stresses ignored).

Inside a thin shell (mass M, radius R) moving with velocity U(t): harmonic gauge h_tx = -4 M U(t)/R,
h_tt = 2M/R (uniform; geometric units). Slow test particle: d^2x/dt^2 = -Gamma^x_tt (first order).
Claim: d^2x/dt^2 = kappa dU/dt with kappa = 4M/R; numbers 1.34 (R1 = 10 m), 0.67 (R2 = 20 m) for
M = 4.51e27 kg; 0.056 for 1 Mjup at 100 m; 3.0e-24 (1e3 kg, 1 m); 3.0e-22 (1e6 kg, 10 m).
Cross-check: Einstein, Meaning of Relativity, linear eqs: (1 + sigma) a = dA/dt with A = 4 G M U /(c^2 R).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

t, x, y, z = sp.symbols("t x y z", real=True)
M, R = sp.symbols("M R", positive=True)
U = sp.Function("U")(t)
X = [t, x, y, z]
g = sp.diag(-1 + 2 * M / R, 1 + 2 * M / R, 1 + 2 * M / R, 1 + 2 * M / R)
g[0, 1] = g[1, 0] = -4 * M * U / R
gi = g.inv()
Gam_x_tt = sum(gi[1, k] * (2 * sp.diff(g[k, 0], t) - sp.diff(g[0, 0], X[k])) / 2 for k in range(4))
acc = -Gam_x_tt
lin = sp.series(sp.simplify(acc), M, 0, 2).removeO()
print("coordinate acceleration of a test particle at rest, first order in M:", sp.simplify(lin))
identity(sp.simplify(lin), 4 * M / R * sp.diff(U, t))
limit(4 * M / R, "M", 0, "0")
G, c = 6.67430e-11, 2.99792458e8
k = lambda m, r: 4 * G * m / (c**2 * r)
for (m, r, cl) in [(4.5114e27, 10, "1.34"), (4.5114e27, 20, "0.67"), (1.8981e27, 100, "0.056"),
                   (1e3, 1, "3.0e-24"), (1e6, 10, "3.0e-22")]:
    print(f"M={m:.4g} kg, R={r} m: kappa = {k(m, r):.4g}")
    quantity(f"{k(m, r)} m/m", f"{cl} m/m", rel_tol=0.01)
units("4 * (6.674e-11 m^3/(kg*s^2)) * 1 kg / ((3e8 m/s)^2 * 1 m)", "1")
raise SystemExit(finish())
