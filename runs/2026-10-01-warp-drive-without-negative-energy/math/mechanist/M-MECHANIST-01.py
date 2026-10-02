"""M-MECHANIST-01: linearized momentum density of a localized uniform shift on a flat slice.

Claim (F3): metric ds^2 = -dt^2 + (dx + b0 f(r) dt)^2 + dy^2 + dz^2 (G = c = 1, unit lapse,
flat slice). To first order in b0 the Eulerian momentum density is
    j_x = -(b0/16 pi) [ f'' sin^2(th) + f' (1 + cos^2 th)/r ],  th measured from the x axis,
and int j_x d^3x = -(b0/16pi)(8pi/3) [r^2 f']_0^inf = 0 for compact-support f'.

Independent derivation: linearized Ricci tensor of h_{mu nu} with h_tx = b0 f(r) only
(g_tt = -1 + b0^2 f^2 is O(b0^2), dropped). R_{mn} = 1/2 (d_r d_m h^r_n + d_r d_n h^r_m - box h_mn - d_m d_n h).
Eulerian observer n^mu = (1, -beta^i); j_i = -T_{mu i} n^mu = -T_{ti} + O(b0^2).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, sign, units, finish

t, x, y, z = sp.symbols("t x y z", real=True)
b0 = sp.symbols("b0", positive=True)
F = sp.Function("F")
X = [t, x, y, z]
r = sp.sqrt(x**2 + y**2 + z**2)
eta = sp.diag(-1, 1, 1, 1)
h = sp.zeros(4, 4)
h[0, 1] = h[1, 0] = b0 * F(r)
hup = eta * h  # h^r_n = eta^{r a} h_{a n} (eta is its own inverse)
trh = sum(eta[i, i] * h[i, i] for i in range(4))


def box(e):
    return sum(eta[i, i] * sp.diff(e, X[i], 2) for i in range(4))


Ric = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        e = 0
        for rr in range(4):
            e += sp.diff(hup[rr, n], X[rr], X[m]) + sp.diff(hup[rr, m], X[rr], X[n])
        e = e - box(h[m, n]) - sp.diff(trh, X[m], X[n])
        Ric[m, n] = e / 2
Rs = sum(eta[i, i] * Ric[i, i] for i in range(4))
Gtx = sp.simplify(Ric[0, 1] - sp.Rational(1, 2) * eta[0, 1] * Rs)
jx = -Gtx / (8 * sp.pi)

# express in spherical: r, cos th = x/r
rs, th = sp.symbols("r theta", positive=True)
fs = sp.Function("f")
sub = {x: rs * sp.cos(th), y: rs * sp.sin(th), z: 0}
jx_sph = jx.subs(sub).doit()
# replace derivatives of F(sqrt(...)) by f(r)
jx_sph = sp.simplify(jx_sph)
print("j_x (raw, at y-plane) =", jx_sph)

claimed = -(b0 / (16 * sp.pi)) * (sp.Derivative(fs(rs), rs, 2) * sp.sin(th)**2
                                   + sp.Derivative(fs(rs), rs) * (1 + sp.cos(th)**2) / rs)

# test on concrete profiles (polynomial/Gaussian) to avoid Subs objects
for prof in [lambda q: sp.exp(-q**2), lambda q: 1 / (1 + q**4), lambda q: sp.cos(q) * sp.exp(-q**2 / 3)]:
    ex = jx.subs(F(r), prof(r)).doit() if False else None
    Fexpr = prof(r)
    hh = sp.zeros(4, 4)
    hh[0, 1] = hh[1, 0] = b0 * Fexpr
    hu = eta * hh
    RR = sp.zeros(4, 4)
    for m in range(4):
        for n in range(4):
            e = 0
            for rr in range(4):
                e += sp.diff(hu[rr, n], X[rr], X[m]) + sp.diff(hu[rr, m], X[rr], X[n])
            e = e - box(hh[m, n])
            RR[m, n] = e / 2
    R_s = sum(eta[i, i] * RR[i, i] for i in range(4))
    G_tx = RR[0, 1] - sp.Rational(1, 2) * eta[0, 1] * R_s
    j_lin = (-G_tx / (8 * sp.pi)).subs(sub)
    fr = prof(rs)
    cl = -(b0 / (16 * sp.pi)) * (sp.diff(fr, rs, 2) * sp.sin(th)**2 + sp.diff(fr, rs) * (1 + sp.cos(th)**2) / rs)
    identity(sp.simplify(j_lin), cl, domain={"b0": (0.01, 1), "r": (0.1, 5), "theta": (0, 3.1)})

# check R_00 and R (O(b0)) vanish for a static h_tx: energy density is O(b0^2)
print("R_tt linear =", sp.simplify(Ric[0, 0]), "; R linear =", sp.simplify(Rs))

# angular integrals and total
ang1 = sp.integrate(sp.integrate(sp.sin(th)**2 * sp.sin(th), (th, 0, sp.pi)), (sp.Symbol("ph"), 0, 2 * sp.pi))
ang2 = sp.integrate(sp.integrate((1 + sp.cos(th)**2) * sp.sin(th), (th, 0, sp.pi)), (sp.Symbol("ph"), 0, 2 * sp.pi))
print("angular integrals:", ang1, ang2)
identity(ang1, "8*pi/3")
identity(ang2, "16*pi/3")
g = sp.Function("g")(rs)
radial = rs**2 * (ang1 * sp.diff(g, rs, 2) + ang2 * sp.diff(g, rs) / rs)
identity(radial, sp.Rational(8, 3) * sp.pi * sp.diff(rs**2 * sp.diff(g, rs), rs))

# explicit compact-ish profile: f = 1 for r<R1, smooth step to 0 at R2 (here a polynomial smoothstep)
R1, R2 = 1, 2
s = (rs - R1) / (R2 - R1)
step = 1 - (6 * s**5 - 15 * s**4 + 10 * s**3)
tot = sp.integrate(sp.Rational(8, 3) * sp.pi * (rs**2 * sp.diff(step, rs, 2) + 2 * rs * sp.diff(step, rs)), (rs, R1, R2))
print("total of r^2 f'' + 2 r f' over wall (smoothstep):", sp.simplify(tot))
identity(tot, "0")
# limit: b0 -> 0 gives j -> 0 (flat)
limit("-(b0/(16*pi))*(2*sin(t)**2+3*(1+cos(t)**2)/r)", "b0", 0, "0", domain={"t": (0, 3), "r": (0.1, 10)})
# units: j (geometric) = G T^{0x}/c^4 in 1/m^2 ; b0 f'/r is 1/m^2
units("1 / (1 m) / (1 m)", "1/m^2")
units("(6.674e-11 m^3/(kg*s^2)) * (1 J/m^3) / (2.998e8 m/s)^4", "1/m^2")
raise SystemExit(finish())
