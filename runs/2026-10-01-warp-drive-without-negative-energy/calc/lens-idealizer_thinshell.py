"""Idealizer lens: Israel thin-shell model of a 'warp shell'.

Geometric units G = c = 1, lengths in metres.
Model: flat cavity r < R with constant lapse N and a UNIFORM shift beta (along z),
   ds^2 = -N^2 dt^2 + (dx + beta_vec dt)^2           (shift convention: g_0i = +beta_i)
glued across a thin shell at r = R (shell at rest in these x coordinates, i.e. at rest
relative to the exterior) to a static Schwarzschild exterior of mass M.

Questions:
 (a) What is the induced 3-metric of the tube r = R seen from inside? Can it match the
     exterior's round static tube (Israel's first junction condition)?
 (b) Static thin-shell surface energy and stresses (Israel), and their energy conditions.
 (c) Is there a gauge-invariant interior 'warp' left once the matching is done properly
     (Killing-vector twist / Sagnac loop integral)?
"""
import sympy as sp

t, th, ph, R, N, b, M, lam = sp.symbols('t theta phi R N beta M lambda', positive=True)

print("=== (a) Induced metric on r = R from inside, uniform shift beta along z ===")
# embedding x = R n(theta, phi), at rest in x coordinates
x = R*sp.sin(th)*sp.cos(ph); y = R*sp.sin(th)*sp.sin(ph); z = R*sp.cos(th)
X = sp.Matrix([x, y, z])
coords3 = [t, th, ph]
# 4-metric pulled back: ds^2 = -N^2 dt^2 + |dX + beta zhat dt|^2
dX = X.jacobian([th, ph])           # 3x2
bvec = sp.Matrix([0, 0, b])
h = sp.zeros(3, 3)
# components: index 0 = t, 1 = theta, 2 = phi
h[0, 0] = -N**2 + b**2
for a in range(2):
    h[0, a+1] = h[a+1, 0] = sp.simplify((bvec.T*dX[:, a])[0])
    for c in range(2):
        h[a+1, c+1] = sp.simplify((dX[:, a].T*dX[:, c])[0])
print("h_ab (t,theta,phi) =", h)
# cross term h_t,theta = -beta R sin(theta) = d/dtheta (beta R cos theta): an exact form
print("h_t,theta - d/dtheta(beta R cos theta) =", sp.simplify(h[0, 1] - sp.diff(b*R*sp.cos(th), th)))

# reparametrize t = tau + lam*R*cos(theta) to remove the cross term
J = sp.Matrix([[1, -lam*R*sp.sin(th), 0], [0, 1, 0], [0, 0, 1]])   # d(t,th,ph)/d(tau,th,ph)
h2 = sp.simplify(J.T*h*J)
lam_sol = sp.solve(sp.Eq(h2[0, 1], 0), lam)[0]
h2 = sp.simplify(h2.subs(lam, lam_sol))
print("lambda that removes cross term =", lam_sol)
print("h_ab in (tau,theta,phi) =", h2)
g2 = h2[1:, 1:]
print("2-metric of the shell's spatial section seen from inside:", g2)
# Gaussian curvature of 2-metric E dth^2 + G dph^2 (orthogonal)
E = g2[0, 0]; Gm = g2[1, 1]
Kraw = -1/(2*sp.sqrt(E*Gm))*(sp.diff(sp.diff(Gm, th)/sp.sqrt(E*Gm), th))
K = N**2*(N**2 - b**2)/(R**2*(N**2 - b**2*sp.cos(th)**2)**2)   # candidate closed form
chk = [float((Kraw - K).subs({N: 0.8, b: 0.3, R: 2.0, th: tv})) for tv in (0.3, 0.9, 1.4, 2.2)]
print("Gaussian curvature K(theta) =", K, "; numeric check of closed form (should be ~0):", chk)
Kpole = sp.simplify(K.subs(th, 0)); Keq = sp.simplify(K.subs(th, sp.pi/2))
print("K(pole) =", Kpole, " K(equator) =", Keq, " (round sphere would give 1/R^2 everywhere)")
# Fractional non-roundness and area
eps = b**2/(N**2 - b**2)
print("non-roundness parameter beta^2/(N^2-beta^2) = beta^2/N^2 * gamma^2 ; e.g.")
for Nv, bv in [(1.0, 0.02), (1.0, 0.04), (0.6, 0.04), (1.0, 0.5)]:
    print(f"  N={Nv}, beta={bv}: eps = {float(eps.subs({N: Nv, b: bv})):.4e}, "
          f"axis ratio (meridian elongation) gamma = {float(sp.sqrt(1+eps).subs({N: Nv, b: bv})):.6f}")
print("=> Israel's first condition (round exterior tube) FAILS at O(beta^2) unless the cavity is")
print("   built prolate (Lorentz-elongated); at O(beta) the mismatch is removed purely by the")
print("   time relabelling t = tau + beta R cos(theta)/(N^2-beta^2), i.e. by gauge.")

print()
print("=== (b) Static thin shell (no shift): Israel surface energy and pressure ===")
# interior flat with lapse N_in = sqrt(1-2M/R) (continuity of g_tt), exterior Schwarzschild
f = 1 - 2*M/R
sigma = (1 - sp.sqrt(f))/(4*sp.pi*R)
p = ((1 - M/R)/sp.sqrt(f) - 1)/(8*sp.pi*R)
print("sigma =", sigma, "; p =", sp.simplify(p))
# DEC: p <= sigma ; solve for compactness C = 2M/R
Cc = sp.symbols('C', positive=True)
sig_C = (1 - sp.sqrt(1 - Cc))/(4*sp.pi)
p_C = ((1 - Cc/2)/sp.sqrt(1 - Cc) - 1)/(8*sp.pi)
sol = sp.nsolve(p_C - sig_C, Cc, (0.5, 0.99), solver='bisect')
print("DEC (p <= sigma) holds for 2M/R <=", sol, " (exact 24/25 =", 24/25, ")")
for Cv in [0.0667, 0.333, 0.667, 0.96]:
    print(f"  2M/R = {Cv}: R*sigma = {float(sig_C.subs(Cc, Cv)):.5f}, R*p = {float(p_C.subs(Cc, Cv)):.5f}, "
          f"p/sigma = {float((p_C/sig_C).subs(Cc, Cv)):.4f}")
print("NEC/WEC hold for all 2M/R < 1 (sigma > 0, p > 0); SEC holds. Surface momentum S_tA = 0.")

print()
print("=== (c) Gauge-invariant content: Sagnac loop / Killing twist ===")
# Sagnac time difference for a loop: dt_S = 2 * oint (g_0i / (-g_00)) dx^i  (c = 1)
# Interior chord along z through centre: oint part = int_{-R}^{R} beta/(N^2-beta^2) dz
chord = sp.integrate(b/(N**2 - b**2), (sp.Symbol('zz'), -R, R))
print("interior chord contribution to oint g_0i/(-g_00) dx^i =", sp.simplify(chord))
print("time jump needed at the two shell crossings (theta=0 and pi) by the Israel matching:",
      sp.simplify(lam_sol*R*sp.cos(0) - lam_sol*R*sp.cos(sp.pi)))
print("=> they are equal: with the junction done as Israel requires, the loop integral, i.e. the")
print("   Sagnac delay and the twist of the Killing vector d/dt, VANISH for a thin shell.")
print("   A uniform interior shift around a thin shell is a coordinate artefact (plus an O(beta^2)")
print("   shape change). Any physical gravitomagnetic flux must live inside a wall of finite")
print("   thickness, where it needs momentum currents (see lens-idealizer_thickwall.py).")
