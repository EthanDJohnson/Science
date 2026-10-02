"""Dialectician lens: does a C^0 Eulerian density rescue Lentz from the divergence argument? (synthesis S3)

Zero-vorticity, unit-lapse, flat-slice warp drives (Lentz, Fell-Heisenberg) have shift beta_i = d_i phi and
K_ij = +-d_i d_j phi, so the Eulerian density is
    16 pi rho_E = K^2 - K_ij K^ij = (lap phi)^2 - phi_ij phi_ij = d_i F_i,
    F_i = phi_i lap(phi) - phi_j phi_ij.
Part 1 checks the identity symbolically. Part 2 tests three regularity classes with phi = g(x) h(y) h(z):
  (a) smooth g: integral of rho_E over space = 0;
  (b) C^1 g with a jump only in g'' at x=0 (density has a jump, F stays continuous): integral = 0 still;
  (c) C^0 g with a kink at x=0 (phi_x jumps): bulk integral != 0, compensated exactly by a distributional
      Eulerian sheet sigma = (1/8 pi)[phi_x](phi_yy + phi_zz) at x=0 (delta^2 terms cancel).
Geometric units; phi in m^2 (shift dimensionless), rho_E in m^-2. Integrals in units of 1/(16 pi).
"""
import sympy as sp

x, y, z = sp.symbols('x y z', real=True)
phi = sp.Function('phi')(x, y, z)
X = [x, y, z]
lap = sum(sp.diff(phi, v, 2) for v in X)
H = [[sp.diff(phi, a, b) for b in X] for a in X]
rho16 = lap**2 - sum(H[i][j]**2 for i in range(3) for j in range(3))
F = [sp.diff(phi, X[i])*lap - sum(sp.diff(phi, X[j])*H[i][j] for j in range(3)) for i in range(3)]
divF = sum(sp.diff(F[i], X[i]) for i in range(3))
print("Identity 16*pi*rho_E - div F == 0 :", sp.simplify(sp.expand(rho16 - divF)) == 0)

# separable test functions
h = sp.exp(-y**2)

import numpy as np
from scipy.integrate import quad

def oneD(f, lo, hi):
    fn = sp.lambdify(x, f, 'numpy')
    return quad(fn, lo, hi, limit=400)[0]

hh = sp.exp(-x**2)        # h written in x for 1D quadrature
hp, hpp = sp.diff(hh, x), sp.diff(hh, x, 2)
n_ = oneD(hh**2, -np.inf, np.inf); a_ = oneD(hh*hpp, -np.inf, np.inf); bb = oneD(hp**2, -np.inf, np.inf)
print(f"1D h integrals: n={n_:.6f}, a=int h h''={a_:.6f}, b=int h'^2={bb:.6f} (a = -b expected)")

def bulk_and_sheet(gp, gn, label):
    # bulk: 16 pi rho = 2(phi_xx phi_yy + phi_xx phi_zz + phi_yy phi_zz) - 2(phi_xy^2 + phi_xz^2 + phi_yz^2)
    A = sum(oneD(g*sp.diff(g, x, 2), lo, hi) for g, lo, hi in [(gp, 0, np.inf), (gn, -np.inf, 0)])
    B = sum(oneD(sp.diff(g, x)**2, lo, hi) for g, lo, hi in [(gp, 0, np.inf), (gn, -np.inf, 0)])
    G0 = sum(oneD(g**2, lo, hi) for g, lo, hi in [(gp, 0, np.inf), (gn, -np.inf, 0)])
    bulk = 2*(2*A*a_*n_ + G0*a_**2) - 2*(2*B*bb*n_ + G0*bb**2)
    g0 = float(gp.subs(x, 0)); jump = float(sp.diff(gp, x).subs(x, 0) - sp.diff(gn, x).subs(x, 0))
    sheet = 2*jump*g0*(2*a_*n_)        # 16 pi * integral of sigma over the plane x=0
    jump2 = float(sp.diff(gp, x, 2).subs(x, 0) - sp.diff(gn, x, 2).subs(x, 0))
    print(f"[{label}] [g']={jump:+.3f}, [g'']={jump2:+.3f}: 16pi*bulk = {bulk:+.6e}, 16pi*sheet = {sheet:+.6e}, total = {bulk+sheet:+.3e}")
    return bulk, sheet

g_s = sp.exp(-x**2)*(1 + x**2)
bulk_and_sheet(g_s, g_s, "(a) smooth")
k = sp.Rational(1, 2)
bulk_and_sheet(sp.exp(-x**2)*(1 + k*x**2), sp.exp(-x**2)*(1 - k*x**2), "(b) C1, jump in g'' only")
for kk in [sp.Rational(1, 2), -sp.Rational(1, 2), 2]:
    bulk_and_sheet(sp.exp(-x**2)*(1 + kk*x), sp.exp(-x**2)*(1 - kk*x), f"(c) C0 kink, k={kk}")
print("Reading: a positive bulk Eulerian energy (case c with the sign of g(0)[g'] that makes bulk > 0) is always"
      " cancelled by a negative Eulerian sheet of equal size on the kink plane; for C1 potentials the bulk alone integrates to zero.")
