"""M-IDEALIZER-02: thin-shell Sagnac flux and Killing twist vanish (F2).
Geometric units. Interior ds^2 = -Nl^2 dt^2 + dx^2 + dy^2 + (dz + b dt)^2, constant Nl > b >= 0.
Exterior static Schwarzschild (g_0i = 0). Sagnac 1-form A = g_0i/(-g_00) dx^i.
Claims: interior chord pole-to-pole contributes 2Rb/(Nl^2 - b^2); the matching relabelling differs
by exactly that between the two crossings; the loop integral is zero; xi = d_t is twist-free.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, finish

t, tau, R, Nl, b = sp.symbols("t tau R N_l b", positive=True)
x, y, z = sp.symbols("x y z", real=True)
dom = {"b": (0.0, 0.5), "N_l": (0.6, 2.0)}
g = sp.diag(-Nl**2 + b**2, 1, 1, 1); g[0, 3] = g[3, 0] = b
A = [g[0, i]/(-g[0, 0]) for i in (1, 2, 3)]
chord = sp.integrate(A[2], (z, -R, R))
print("interior chord integral:", sp.simplify(chord))
identity(chord, 2*R*b/(Nl**2 - b**2), domain=dom)
# relabelling lam(theta) = b R cos(th)/(Nl^2 - b^2); north pole minus south pole
th = sp.symbols("theta")
lam = b*R*sp.cos(th)/(Nl**2 - b**2)
jump = lam.subs(th, 0) - lam.subs(th, sp.pi)
identity(jump, chord, domain=dom)
# total loop: chord (interior, t) - relabelling jump + exterior arc (A = 0) = 0
identity(chord - jump + 0, 0, domain=dom)
# stronger: in tau = t - b z/(Nl^2 - b^2) the interior metric is static (no cross term)
coords = [tau, x, y, z]
X = [tau + b*z/(Nl**2 - b**2), x, y, z]
Jm = sp.Matrix([[sp.diff(Xi, c) for c in coords] for Xi in X])
gt = sp.simplify(Jm.T*g*Jm)
print("interior metric in (tau, x, y, z):", gt)
identity(gt[0, 3], 0, domain=dom)
identity(gt[3, 3], Nl**2/(Nl**2 - b**2), domain=dom)
# twist of xi = d_t: xi_mu = g_mu0 constant -> d(xi) = 0 -> xi ^ d xi = 0
xi = [g[0, m] for m in range(4)]
allc = [t, x, y, z]
dxi = [[sp.diff(xi[n], allc[m]) - sp.diff(xi[m], allc[n]) for n in range(4)] for m in range(4)]
identity(sum(abs(e) for row in dxi for e in row), 0, domain=dom)
limit(chord, "b", 0, 0)
raise SystemExit(finish())
