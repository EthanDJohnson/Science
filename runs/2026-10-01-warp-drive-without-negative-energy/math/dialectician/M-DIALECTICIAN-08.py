"""M-DIALECTICIAN-08 and -09: linear (first order in b), unit-lapse, flat-slice momentum density of the
Fuchs warp shift beta = (b S(r), 0, 0); geometric units (1/m^2). Codazzi/momentum constraint
8 pi j_i = D_j(K^j_i - delta^j_i K), K_ij = -(1/2)(d_i beta_j + d_j beta_i) (static, N = 1)
derived symbolically here for a generic beta_x(x, y, z).
S(r) = 1 (r < R1'), 1 - f (between), 0 (r > R2'), f = [exp(D (1/(r-R2') + 1/(r-R1'))) + 1]^-1,
R1' = R1 + Rb, R2' = R2 - Rb, D = R2' - R1' (Fuchs eq. 28 with buffered radii).
-08: net integral of j_x is zero (claimed net/total ~ -2e-6).
-09: caps b_max = rho/max|j/b| (DEC scale) and rho/(2 max|j/b|) (NEC scale), constant-density rho = 3m/(4pi(R2^3-R1^3)),
     claimed 0.027-0.054 (Rb = 0), 0.018-0.035 (Rb = 1 m), 0.010-0.020 (Rb = 2 m); rho*Delta^2 = 0.0114, invariant under
     self-similar 10x scaling; at Buchdahl 2m/R2 = 8/9 with R1 = R2/2: rho*Delta^2 ~ 0.03, b_max <~ 0.15.
"""
import sys, os, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import mpmath as mp
from math_checks import identity, quantity, limit, units, finish

which = globals().get("WHICH", os.path.basename(__file__)[:-3])
x, y, z = sp.symbols("x y z", real=True)
X = (x, y, z)
B = sp.Function("B")(x, y, z)
beta = [B, 0, 0]
K = sp.Matrix(3, 3, lambda i, j: -(sp.diff(beta[j], X[i]) + sp.diff(beta[i], X[j])) / 2)
trK = K.trace()
j8pi = [sum(sp.diff(K[jj, i], X[jj]) for jj in range(3)) - sp.diff(trK, X[i]) for i in range(3)]
identity(sp.expand(2 * j8pi[0]), sp.expand(-(sp.diff(B, y, 2) + sp.diff(B, z, 2))))   # 16 pi j_x = -(d_y^2+d_z^2) beta_x
identity(sp.expand(2 * j8pi[1]), sp.expand(sp.diff(B, x, y)))
# spherical reduction for B = S(r): (d_y^2+d_z^2)S = S'' sin^2 + (S'/r)(1+cos^2); d_x d_y S = (S''-S'/r) cos sin cos(phi)
r_, th = sp.symbols("r theta", positive=True)
Sf = sp.Function("S")
Rr = sp.sqrt(x**2 + y**2 + z**2)
lhs = sp.diff(Sf(Rr), y, 2) + sp.diff(Sf(Rr), z, 2)
pt = {x: sp.Rational(3, 7), y: sp.Rational(5, 7), z: sp.Rational(-2, 7)}
rv = Rr.subs(pt); ct = pt[x] / rv
test = {Sf(Rr): sp.exp(-Rr**2) * Rr}  # concrete S to compare
Sc = sp.exp(-r_**2) * r_
lhs_c = (sp.diff(Sc.subs(r_, Rr), y, 2) + sp.diff(Sc.subs(r_, Rr), z, 2)).subs(pt)
rhs_c = (sp.diff(Sc, r_, 2) * (1 - ct**2) + sp.diff(Sc, r_) / r_ * (1 + ct**2)).subs(r_, rv)
identity(sp.nsimplify(sp.N(lhs_c - rhs_c, 40), rational=False), 0)

mp.mp.dps = 30
def profile(R1, R2, Rb):
    a1, a2 = R1 + Rb, R2 - Rb
    D = a2 - a1
    r = sp.symbols("r", positive=True)
    S = 1 - 1 / (sp.exp(D * (1 / (r - a2) + 1 / (r - a1))) + 1)
    S1, S2 = sp.diff(S, r), sp.diff(S, r, 2)
    return a1, a2, sp.lambdify(r, S1, "mpmath"), sp.lambdify(r, S2, "mpmath")

def j_over_b_max(R1, R2, Rb, nr=600, nth=181):
    a1, a2, S1, S2 = profile(R1, R2, Rb)
    best, bestx = 0, 0
    for k in range(1, nr):
        r = a1 + (a2 - a1) * k / nr
        s1, s2 = S1(mp.mpf(r)), S2(mp.mpf(r))
        for m in range(nth):
            t = math.pi * m / (nth - 1)
            c, s = math.cos(t), math.sin(t)
            jx = float(s2 * s * s + s1 / r * (1 + c * c)) / (16 * math.pi)
            jp = float((s2 - s1 / r) * c * s) / (16 * math.pi)
            jt = math.hypot(jx, jp)
            best = max(best, jt); bestx = max(bestx, abs(jx))
    return best, bestx

def net_and_total(R1, R2, Rb):
    a1, a2, S1, S2 = profile(R1, R2, Rb)
    # angular averages: <sin^2> = 2/3, <1+cos^2> = 4/3; net = 4pi int r^2 [(2/3)S'' + (4/3)S'/r] dr
    net = 4 * mp.pi * mp.quad(lambda r: r**2 * (mp.mpf(2) / 3 * S2(r) + mp.mpf(4) / 3 * S1(r) / r), [a1, (a1 + a2) / 2, a2]) / (16 * mp.pi)
    # total |j_x|: angular integral of |S'' sin^2 + (S'/r)(1+cos^2)| numerically
    tot = mp.quad(lambda r: r**2 * 2 * mp.pi * mp.quad(lambda c: abs(S2(r) * (1 - c**2) + S1(r) / r * (1 + c**2)), [-1, 1]),
                  [a1, (a1 + a2) / 2, a2]) / (16 * mp.pi)
    return net, tot

G, cc = 6.67430e-11, 2.99792458e8
if which.endswith("08"):
    for Rb in (0.0, 1.0, 2.0):
        net, tot = net_and_total(10.0, 20.0, Rb)
        print(f"Rb = {Rb}: net int j_x/b = {mp.nstr(net, 5)}, int |j_x|/b = {mp.nstr(tot, 8)} m, net/total = {mp.nstr(net/tot, 5)}")
        identity(sp.Float(mp.nstr(net, 25)), 0)
    # analytic: net = (1/16pi)(8pi/3)[r^2 S']_0^inf = 0 since S' has compact support
    rr = sp.symbols("r", positive=True); Sg = sp.Function("S")
    identity(sp.expand(rr**2 * (sp.Rational(2, 3) * sp.diff(Sg(rr), rr, 2) + sp.Rational(4, 3) * sp.diff(Sg(rr), rr) / rr)),
             sp.expand(sp.Rational(2, 3) * sp.diff(rr**2 * sp.diff(Sg(rr), rr), rr)))
    units("1/m^2 * c^4/G / c", "kg/(m^2*s)")
else:
    m = G * 4.49e27 / cc**2
    rho = 3 * m / (4 * math.pi * (20.0**3 - 10.0**3))
    print(f"rho = {rho:.5e} 1/m^2, rho*Delta^2 = {rho*100:.5f}")
    quantity(f"{rho*100}", "0.0114", rel_tol=5e-3)
    caps = {}
    for Rb, (lo, hi) in {0.0: (0.027, 0.054), 1.0: (0.018, 0.035), 2.0: (0.010, 0.020)}.items():
        jt, jx = j_over_b_max(10.0, 20.0, Rb)
        dec, nec = rho / jt, rho / (2 * jt)
        caps[Rb] = dec
        print(f"Rb = {Rb}: max|j|/b = {jt:.4e}, max|j_x|/b = {jx:.4e} 1/m^2; |j|/rho at b=0.02: {0.02*jt/rho:.3f}; "
              f"caps NEC {nec:.4f} - DEC {dec:.4f}  (lens {lo}-{hi}); j_x-only caps {rho/(2*jx):.4f}-{rho/jx:.4f}")
        quantity(f"{dec}", f"{hi}", rel_tol=0.1)
        quantity(f"{nec}", f"{lo}", rel_tol=0.1)
    # self-similar scaling x10 (R, Rb, M all x10)
    jt10, _ = j_over_b_max(100.0, 200.0, 0.0, nr=300, nth=91)
    rho10 = 3 * (m * 10) / (4 * math.pi * (200.0**3 - 100.0**3))
    jt1, _ = j_over_b_max(10.0, 20.0, 0.0, nr=300, nth=91)
    print(f"x10 scaling: cap {rho10/jt10:.5f} vs {rho/jt1:.5f}; rho*Delta^2 {rho10*1e4:.5f}")
    quantity(f"{rho10/jt10}", f"{rho/jt1}", rel_tol=1e-6)
    # Buchdahl: 2m/R2 = 8/9, R1 = R2/2 -> rho Delta^2
    R2s = sp.symbols("R2", positive=True)
    mB = sp.Rational(4, 9) * R2s
    rhoB = 3 * mB / (4 * sp.pi * (R2s**3 - (R2s / 2) ** 3))
    rD2 = sp.simplify(rhoB * (R2s / 2) ** 2)
    print("Buchdahl rho*Delta^2 =", rD2, "=", sp.N(rD2, 6), "; cap scaled:", caps[0.0] * float(rD2) / (rho * 100))
    quantity(f"{float(rD2)}", "0.03", rel_tol=0.05)
    quantity(f"{caps[0.0] * float(rD2) / (rho * 100)}", "0.15", rel_tol=0.06)
    units("(1/m^2) * c^4/G", "J/m^3")
raise SystemExit(finish())
