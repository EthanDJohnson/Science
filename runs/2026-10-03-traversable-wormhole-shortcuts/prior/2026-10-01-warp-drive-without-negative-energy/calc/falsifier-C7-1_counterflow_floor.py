"""Falsifier C7-1: counterflow energy floor for the rebuild profile vs the thin-sheet optimum,
and a check that the cavity Killing congruence of a uniform-shift interior is twist-free and geodesic.

Units: SI for budgets; geometric (G = c = 1) for the symbolic interior check.
Inputs (quoted from the run's math checks, not re-derived here):
  M_ADM = 4.511e27 kg (toolkit rebuild, M-MECHANIST-03)
  P_plus = 6.758e34 kg m/s at beta = 0.02 for the Fuchs eq. (28) profile (M-MECHANIST-03, verified)
  P_sheet = 4.04e34 kg m/s per stream for two thin sheets at R1, R2 (M-ENGINEER-05, verified)
Pointwise DEC: eps >= c|j| >= c|j_x|, so integrated E_flow >= c (P_plus + |P_minus|) = 2 c P_plus
(net momentum zero, so |P_minus| = P_plus).
"""
import sympy as sp

c = 2.99792458e8
M = 4.511e27
Mc2 = M * c**2
for label, P in [("rebuild profile (P_plus, M-MECHANIST-03)", 6.758e34),
                 ("thin sheets at R1,R2 (M-ENGINEER-05)", 4.04e34)]:
    E = 2 * c * P
    print(f"{label}: P per sign = {P:.3e} kg m/s; E_flow >= 2cP = {E:.3e} J = {E/Mc2:.4f} M_ADM c^2")
print(f"M_ADM c^2 = {Mc2:.4e} J")

# Symbolic: interior ds^2 = -N^2 dt^2 + (dx + b dt)^2 + dy^2 + dz^2, N, b constant.
t, x, y, z = sp.symbols('t x y z', real=True)
N, b = sp.symbols('N b', positive=True)
X = [t, x, y, z]
g = sp.Matrix([[-N**2 + b**2, b, 0, 0], [b, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
xi_flat = g * sp.Matrix([1, 0, 0, 0])  # covector of Killing field d/dt
# twist one-form components omega ~ eps^{abcd} xi_b d_c xi_d ; with constant metric d xi_flat = 0
dxi = sp.zeros(4, 4)
for a in range(4):
    for bb in range(4):
        dxi[a, bb] = sp.diff(xi_flat[bb], X[a]) - sp.diff(xi_flat[a], X[bb])
print("d(xi_flat) all zero in cavity:", all(sp.simplify(e) == 0 for e in dxi))
norm = sp.simplify((sp.Matrix([1, 0, 0, 0]).T * g * sp.Matrix([1, 0, 0, 0]))[0])
print("xi.xi =", norm, "(constant => static observers are geodesic: a = grad ln|xi| = 0)")
# Eulerian drift relative to static observers
n_up = sp.Matrix([1 / N, -b / N, 0, 0])
us = sp.Matrix([1, 0, 0, 0]) / sp.sqrt(N**2 - b**2)
gam = sp.simplify(-(n_up.T * g * us)[0])
v = sp.simplify(sp.sqrt(1 - 1 / gam**2))
print("Eulerian speed relative to static (Killing) observers:", v)
print("numeric at N=0.7607, b=0.02:", float(v.subs({N: 0.7607, b: 0.02})))
