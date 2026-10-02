"""M-IDEALIZER-01: thin shell with uniform interior shift (F1).
Geometric units G = c = 1. Interior: flat, ds^2 = -Nl^2 dt^2 + dx^2 + dy^2 + (dz + b dt)^2,
constant lapse Nl > |b| >= 0 (g_0z = +b, the lens's convention). Shell at r = R, at rest in (t, x).
Claims: induced h_t,theta = -b R sin(th); relabelling t = tau + b R cos(th)/(Nl^2 - b^2) removes it;
residual 2-metric R^2[(Nl^2 - b^2 cos^2)/(Nl^2 - b^2) dth^2 + sin^2 dph^2]; K(pole) = Nl^2/(R^2(Nl^2-b^2)),
K(equator) = (Nl^2 - b^2)/(Nl^2 R^2); prolate spheroid with axis ratio gamma = Nl/sqrt(Nl^2 - b^2).
Independent derivation: embed the sphere, pull back; then an exact Lorentz boost to the shell rest frame.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

t, tau, th, ph, R, Nl, b = sp.symbols("t tau theta phi R N_l b", positive=True)
T, Z, z = sp.symbols("T Z z", real=True)

# embedding of the shell r = R in interior coordinates, time t
x = R*sp.sin(th)*sp.cos(ph); y = R*sp.sin(th)*sp.sin(ph); zz = R*sp.cos(th)
q = [t, th, ph]
X = [t, x, y, zz]
g4 = sp.diag(-Nl**2 + b**2, 1, 1, 1); g4[0, 3] = g4[3, 0] = b
J = sp.Matrix([[sp.diff(Xi, qa) for qa in q] for Xi in X])
h = sp.simplify(J.T*g4*J)
print("induced metric (t, th, ph):", h)
identity(h[0, 1], -b*R*sp.sin(th), domain={"theta": (0.01, 3.13)})

# relabel t = tau + b R cos(th)/(Nl^2 - b^2)
lam = b*R*sp.cos(th)/(Nl**2 - b**2)
q2 = [tau, th, ph]
X2 = [tau + lam, x, y, zz]
J2 = sp.Matrix([[sp.diff(Xi, qa) for qa in q2] for Xi in X2])
h2 = sp.simplify(J2.T*g4*J2)
print("relabelled induced metric (tau, th, ph):", h2)
dom = {"b": (0.0, 0.5), "N_l": (0.6, 2.0), "theta": (0.01, 3.13)}
identity(h2[0, 1], 0, domain=dom)
identity(h2[0, 0], -(Nl**2 - b**2), domain=dom)
Eth = R**2*(Nl**2 - b**2*sp.cos(th)**2)/(Nl**2 - b**2)
identity(h2[1, 1], Eth, domain=dom)
identity(h2[2, 2], R**2*sp.sin(th)**2, domain=dom)

# Gaussian curvature of E dth^2 + G dph^2 (orthogonal, G = R^2 sin^2)
E_, G_ = h2[1, 1], h2[2, 2]
sqG = R*sp.sin(th)  # sqrt(G) for 0 < th < pi
K = -1/(sp.sqrt(E_)*sqG)*sp.diff(sp.diff(sqG, th)/sp.sqrt(E_), th)
K = sp.simplify(K)
Kpole = sp.simplify(sp.limit(K, th, 0))
Keq = sp.simplify(K.subs(th, sp.pi/2))
print("K(pole) =", Kpole, "  K(equator) =", Keq)
identity(Kpole, Nl**2/(R**2*(Nl**2 - b**2)), domain=dom)
identity(Keq, (Nl**2 - b**2)/(Nl**2*R**2), domain=dom)

# prolate spheroid, equatorial radius R, polar semi-axis gamma*R: E = R^2(cos^2 + gamma^2 sin^2)
gam = Nl/sp.sqrt(Nl**2 - b**2)
identity(Eth, R**2*(sp.cos(th)**2 + gam**2*sp.sin(th)**2), domain=dom)

# exact: interior is flat; boost with u = b/Nl to shell rest frame gives Z' = gamma z
u = b/Nl
Tp = gam*(Nl*t - u*(z + b*t)); Zp = gam*((z + b*t) - u*Nl*t)
identity(Zp, gam*z, domain={"b": (0.0, 0.5), "N_l": (0.6, 2.0), "z": (-5, 5), "t": (-5, 5)})
dt_, dz_ = sp.symbols("dt dz", real=True)
dT = sp.diff(Tp, t)*dt_ + sp.diff(Tp, z)*dz_; dZ = sp.diff(Zp, t)*dt_ + sp.diff(Zp, z)*dz_
identity(sp.expand(-dT**2 + dZ**2), sp.expand(-Nl**2*dt_**2 + (dz_ + b*dt_)**2),
         domain={"b": (0.0, 0.5), "N_l": (0.6, 2.0), "dt": (-3, 3), "dz": (-3, 3)})

# limit b -> 0: round sphere
limit(Kpole, "b", 0, R**-2)
# numbers, N = 1
for bv, claim in [(0.02, 1.0002), (0.04, 1.0008)]:
    gv = float(gam.subs({Nl: 1, b: bv}))
    print(f"b = {bv}: gamma = {gv:.6f} (claim {claim})")
    quantity(f"{gv}", f"{claim}", rel_tol=1e-4)
gv = float(gam.subs({Nl: 0.7614, b: 0.02}))
print(f"for reference, at the 2024 interior lapse N = 0.7614, b = 0.02: gamma = {gv:.6f}")
units("1/(10 m)^2", "1/m^2")
raise SystemExit(finish())
