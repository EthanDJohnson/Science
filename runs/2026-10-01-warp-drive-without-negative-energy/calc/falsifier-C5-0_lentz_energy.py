"""Falsifier C5-0 (physics): Eulerian energy budget of Lentz's gradient-shift soliton.

Units: geometric (G = c = 1, lengths in m) unless stated; SI conversion M = (c^2/G) * E_geo.
Lentz 2006.07125: N = 1, h_ij = delta_ij, N_i = d_i phi (eq. 12),
  8 pi E = (1/2)(K^2 - K_ij K^ij)  (eq. 6 with flat slices), K^2 - K.K given by his eq. 7.
Parts
 A. Lentz eq. 7 with N_i = d_i phi equals (lap phi)^2 - phi_ij phi_ij = div F  (exact divergence)
 B. Bilateral ansatz phi = psi(|x|+|y|, z) (Lentz's "bi-lateral s-projection", density kinks on x=0, y=0):
    in each quadrant 16 pi E = 4 det Hess(psi); s*detH is a 2D divergence up to an axis term, giving
    bulk integral (all four quadrants, planes excluded) = -(1/2pi) Int psi_z(0,z)^2 dz  <= 0.
 C. Numerical check of B, plus sheet (x=0, y=0) and line (x=y=0) distributional terms; total = 0.
 D. Magnitude at the reference case: axial shift N_z = v_s over a plateau of length L.
 E. Kinematics: payload comoving at v_s needs |v_s - N_z| < 1; Lentz assigns v_s = N_z(0,0).
"""
import numpy as np
import sympy as sp
from scipy import integrate

print("=== A. Lentz eq. 7 with N_i = grad phi ===")
x, y, z = sp.symbols('x y z', real=True)
phi = sp.Function('phi')(x, y, z)
N = [sp.diff(phi, v) for v in (x, y, z)]
X, Y, Z = (x, y, z)
eq7 = (2*sp.diff(N[0], x)*sp.diff(N[1], y) + 2*sp.diff(N[0], x)*sp.diff(N[2], z)
       + 2*sp.diff(N[2], z)*sp.diff(N[1], y)
       - sp.Rational(1, 2)*(sp.diff(N[1], x) + sp.diff(N[0], y))**2
       - sp.Rational(1, 2)*(sp.diff(N[2], x) + sp.diff(N[0], z))**2
       - sp.Rational(1, 2)*(sp.diff(N[1], z) + sp.diff(N[2], y))**2)
V = (x, y, z)
lap = sum(sp.diff(phi, v, 2) for v in V)
hess2 = sum(sp.diff(phi, a, b)**2 for a in V for b in V)
F = [sp.diff(phi, a)*lap - sum(sp.diff(phi, b)*sp.diff(phi, a, b) for b in V) for a in V]
divF = sum(sp.diff(F[i], V[i]) for i in range(3))
print("eq7 - [(lap phi)^2 - phi_ij phi_ij] =", sp.simplify(sp.expand(eq7 - (lap**2 - hess2))))
print("eq7 - div F                         =", sp.simplify(sp.expand(eq7 - divF)))
print("=> 16 pi E = eq7 is an exact divergence; for compactly supported phi, Int E d^3x = 0.")
# momentum constraint 8 pi J_i = d_j K_ji - d_i K with K_ij = -phi_ij
J = [sum(sp.diff(-sp.diff(phi, a, b), b) for b in V) - sp.diff(-lap, a) for a in V]
print("8 pi J_i for gradient shift:", [sp.simplify(j) for j in J], "(J = 0: E is the rest-frame density)")

print("\n=== B. Bilateral ansatz phi = psi(x+y, z) in the quadrant x>0, y>0 ===")
s = sp.symbols('s', real=True)
psi = sp.Function('psi')
phq = psi(x + y, z)
lapq = sum(sp.diff(phq, v, 2) for v in V)
hq = sum(sp.diff(phq, a, b)**2 for a in V for b in V)
e16 = sp.expand(lapq**2 - hq)
p = sp.Function('p')(s, z)
detH = sp.diff(p, s, 2)*sp.diff(p, z, 2) - sp.diff(p, s, z)**2
e16_s = e16.subs(x + y, s)  # cosmetic
chk = sp.simplify(e16.subs({}) - 4*(sp.diff(psi(x+y, z), x, 2)*sp.diff(psi(x+y, z), z, 2)
                                    - sp.diff(psi(x+y, z), x, z)**2))
print("16 pi E - 4 det Hess(psi) =", chk)
# Lentz eq. 17 form: 2 psi_zz (rho + (2/v^2) psi_zz) - 4 psi_sz^2 with rho = 2 psi_ss - (2/v^2) psi_zz
vh = sp.symbols('v_h', positive=True)
rho = 2*sp.diff(p, s, 2) - 2/vh**2*sp.diff(p, z, 2)
lentz17 = 2*sp.diff(p, z, 2)*(rho + 2/vh**2*sp.diff(p, z, 2)) - 4*sp.diff(p, s, z)**2
print("Lentz-eq.17 form - 4 detH =", sp.simplify(lentz17 - 4*detH))
# divergence form of s*detH
div_form = (sp.diff(s*sp.diff(p, s)*sp.diff(p, z, 2), s) - sp.diff(s*sp.diff(p, s)*sp.diff(p, s, z), z)
            - sp.diff(sp.diff(p, s)*sp.diff(p, z), z)*(-1)*(-1) * 0)  # placeholder, built below
lhs = s*detH
rhs = (sp.diff(s*sp.diff(p, s)*sp.diff(p, z, 2), s) - sp.diff(s*sp.diff(p, s)*sp.diff(p, s, z), z)
       - sp.diff(sp.diff(p, s)*sp.diff(p, z), z) + sp.diff(sp.diff(p, z)**2/2, s))
print("s*detH - [d_s(s p_s p_zz) - d_z(s p_s p_sz) - d_z(p_s p_z) + d_s(p_z^2/2)] =",
      sp.simplify(sp.expand(lhs - rhs)))
print("=> Int_{s>0} ds Int dz s detH = -(1/2) Int psi_z(0,z)^2 dz  (only the s=0 boundary of d_s(p_z^2/2) survives)")
print("=> bulk Int E d^3x = 4 quadrants * (1/16pi) * 4 * Int s detH ds dz = -(1/2pi) Int N_z(0,0,z)^2 dz <= 0")

print("\n=== C. Numerical check (psi = (a + b z + c s + d s z) exp(-s^2 - z^2/w^2)) ===")
def make(a, b, c, d, w):
    S, Zs = sp.symbols('S Zs', real=True)
    ps = (a + b*Zs + c*S + d*S*Zs)*sp.exp(-S**2 - Zs**2/w**2)
    f = {k: sp.lambdify((S, Zs), sp.diff(ps, *k) if k else ps, 'numpy')
         for k in [(S, S), (Zs, Zs), (S, Zs), (S,), (Zs,)]}
    return f, S, Zs
for (a, b, c, d, w) in [(1.0, 0.5, 0.3, -0.2, 1.5), (0.2, 1.0, -0.7, 0.4, 0.8), (1.0, 0.0, 0.0, 0.0, 2.0)]:
    f, S, Zs = make(a, b, c, d, w)
    pss, pzz, psz, ps_, pz_ = f[(S, S)], f[(Zs, Zs)], f[(S, Zs)], f[(S,)], f[(Zs,)]
    L = 9.0
    # bulk: 4 quadrants, weight s from dx dy -> s ds
    bulk = 4*(1/(16*np.pi))*integrate.dblquad(lambda zz, ss: ss*4*(pss(ss, zz)*pzz(ss, zz) - psz(ss, zz)**2),
                                               0, L, -L*w, L*w, epsabs=1e-12, epsrel=1e-11)[0]
    # direct 3D quadrant check of the weight (one quadrant, coarse) for the first case only
    closed = -(1/(2*np.pi))*integrate.quad(lambda zz: pz_(0.0, zz)**2, -L*w, L*w, epsabs=1e-13)[0]
    # sheets: plane x=0 : 16 pi sigma = 2 [phi_x] (phi_yy + phi_zz), [phi_x] = 2 psi_s(|y|,z); both planes, both signs of y
    sheet = 2*2*(1/(16*np.pi))*integrate.dblquad(lambda zz, ss: 2*2*ps_(ss, zz)*(pss(ss, zz) + pzz(ss, zz)),
                                                 0, L, -L*w, L*w, epsabs=1e-12, epsrel=1e-11)[0]
    # line x=y=0: 16 pi lambda = 2 [phi_x][phi_y] = 8 psi_s(0,z)^2
    line = (1/(16*np.pi))*integrate.quad(lambda zz: 8*ps_(0.0, zz)**2, -L*w, L*w, epsabs=1e-13)[0]
    print(f"(a,b,c,d,w)=({a},{b},{c},{d},{w}): bulk = {bulk:+.10f}  closed form -(1/2pi)Int psi_z(0,z)^2 = {closed:+.10f}"
          f"  sheets = {sheet:+.10f}  line = {line:+.10f}  total = {bulk+sheet+line:+.2e}  [geo, m per unit amplitude^2]")

# direct 3D quadrature on the quadrant for case 1 to confirm the s-weight (no ansatz shortcut)
f, S, Zs = make(1.0, 0.5, 0.3, -0.2, 1.5)
pss, pzz, psz = f[(S, S)], f[(Zs, Zs)], f[(S, Zs)]
g = np.linspace(0, 9, 721); gz = np.linspace(-13.5, 13.5, 1081)
XX, YY = np.meshgrid(g, g, indexing='ij')
SS = XX + YY
acc = 0.0
for zz in gz:
    acc += np.trapezoid(np.trapezoid(4*(pss(SS, zz)*pzz(SS, zz) - psz(SS, zz)**2), g, axis=1), g)*(gz[1]-gz[0])
print(f"direct 3D grid, 4 quadrants: bulk = {4*acc/(16*np.pi):+.6f} (compare first line)")

print("\n=== D. Magnitude at the reference case ===")
c = 2.99792458e8; G = 6.67430e-11; Msun = 1.989e30
for vs, Lp in [(10.0, 200.0), (10.0, 100.0), (1.0, 200.0), (0.5, 200.0)]:
    Egeo = -vs**2*Lp/(2*np.pi)   # metres, upper bound on bulk (plateau only; tails add more negative)
    Mkg = Egeo*c**2/G
    print(f"v_s={vs:5.1f} c, axial plateau L={Lp:6.1f} m: bulk Int E <= {Egeo:+.4e} m (geo) = {Mkg:+.3e} kg = {Mkg/Msun:+.3f} M_sun")
print("Lentz's claim at R=100 m, w=1 m: E_tot ~ +(few)x0.1 M_sun v_s^2 = +20..50 M_sun at v_s=10 (D-30a) -- opposite sign to the bulk.")

print("\n=== E. Kinematics (N = 1, h = delta, Lentz eq. 1: ds^2 = -dt^2 + (dx^i - N^i dt)^2) ===")
for vs in [0.5, 0.99, 1.5, 10.0]:
    Nz = vs  # Lentz assigns v_s = N_z(0,0)
    print(f"v_s = {vs:5.2f}: payload comoving needs N_z in ({vs-1:+.2f}, {vs+1:+.2f}); Lentz's N_z(0,0) = {Nz:.2f};"
          f" N_iN^i = {Nz**2:.2f} -> {'<1 (DEC per Lentz ok)' if Nz**2 < 1 else '>=1 (outside Lentz DEC condition; horizons)'}")
