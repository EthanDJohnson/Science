"""M-EXAMINER-02: comoving Killing norm of the Alcubierre metric and its horizon.

Geometric units, metres. ds^2 = -dt^2 + (dx - v f(r_s) dt)^2 + dy^2 + dz^2, r_s = |(x - v t, y, z)|.
Profile f(r) = [tanh(s(r+R)) - tanh(s(r-R))] / (2 tanh(sR)), R = 100 m, s = 2 1/m, v = 10.
Claim: in comoving coordinates X = x - v t the metric is stationary, g_tt = -1 + v^2 (1 - f)^2,
which changes sign at f = 1 - 1/v = 0.9, r = 99.4507 m; the shift there vanishes at the centre;
forward light on the axis stalls (dX/dt = 0) at the same radius; for v < 1 no sign change.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import mpmath as mp
from math_checks import identity, sign, inequality, limit, finish

t, X, y, z = sp.symbols("t X y z", real=True)
v = sp.symbols("v", positive=True)
F = sp.Function("F")   # f as a function of (X, y, z): stationary in comoving coords
dt, dX, dy, dz = sp.symbols("dt dX dy dz", real=True)
fX = F(X, y, z)
# Lab dx = dX + v dt
ds2 = -dt**2 + (dX + v*dt - v*fX*dt)**2 + dy**2 + dz**2
P = sp.Poly(sp.expand(ds2), dt, dX, dy, dz)
g_tt = P.coeff_monomial(dt**2)
g_tX = P.coeff_monomial(dt*dX) / 2
print("comoving g_tt =", sp.factor(g_tt), "  g_tX =", sp.factor(g_tX))
identity(g_tt, -1 + v**2*(1 - fX)**2)
# comoving shift (ADM, beta^X = g_tX since h = identity) = v(1-f): zero at the centre where f = 1
identity(g_tX.subs(fX, 1), 0)
# forward axial null speed in comoving coords: (dX + v(1-f)dt)^2 = dt^2 -> dX/dt = 1 - v(1-f)
fs = sp.symbols("fs", positive=True)
sols = sp.solve(sp.Eq((sp.Symbol("w") + v*(1 - fs))**2, 1), sp.Symbol("w"))
print("axial null speeds dX/dt:", sols)
fwd = [s_ for s_ in sols if s_.subs({v: sp.Rational(1, 2), fs: 1}) > 0][0]
identity(fwd, 1 - v*(1 - fs))
# Killing norm zero and forward stall both at f = 1 - 1/v
identity(sp.solve(sp.Eq(-1 + v**2*(1 - fs)**2, 0), fs)[0] if len(sp.solve(sp.Eq(-1 + v**2*(1 - fs)**2, 0), fs)) == 1
         else [r_ for r_ in sp.solve(sp.Eq(-1 + v**2*(1 - fs)**2, 0), fs) if r_.subs(v, 10) < 1][0], 1 - 1/v)
identity(sp.solve(sp.Eq(fwd, 0), fs)[0], 1 - 1/v)

# v < 1: with 0 <= f <= 1 the norm is negative
inequality("-1 + v**2*(1 - fs)**2", "<", "0", domain={"v": (0.01, 0.999), "fs": (0, 1)})
limit("-1 + v**2*(1 - fs)**2", "v", 0, "-1")    # flat-space limit: static Killing vector timelike

# The profile is in [0, 1] and decreasing for r >= 0 (sampled), so max v(1-f) = v as r -> infinity
mp.mp.dps = 40
R, s = mp.mpf(100), mp.mpf(2)
f = lambda r: (mp.tanh(s*(r + R)) - mp.tanh(s*(r - R))) / (2*mp.tanh(s*R))
grid = [mp.mpf(i)/10 for i in range(0, 3001)]
vals = [f(r) for r in grid]
mono = all(vals[i+1] <= vals[i] for i in range(len(vals)-1))
inrange = all(0 <= x_ <= 1 for x_ in vals)
print(f"profile decreasing on [0,300] m: {mono}; within [0,1]: {inrange}; f(0) = {mp.nstr(vals[0], 12)}")
print(("PASS" if (mono and inrange) else "FAIL") + " Alcubierre tanh profile monotone in [0,1] (sampled 0.1 m)")

# Horizon radius for v = 10
rh = mp.findroot(lambda r: f(r) - mp.mpf("0.9"), 99.4)
print(f"r where f = 0.9 (v=10, R=100 m, sigma=2 1/m): {mp.nstr(rh, 10)} m")
ok = abs(rh - mp.mpf("99.4507")) < 1e-3
print(("PASS" if ok else "FAIL") + f" horizon radius {mp.nstr(rh, 8)} m vs claimed 99.4507 m")
# closed form check: tanh(s(r-R)) ~ -(0.8) for r < R near the wall
print("closed-form approx r = R - atanh(0.8)/s =", mp.nstr(R - mp.atanh(mp.mpf("0.8"))/s, 10), "m")
raise SystemExit(finish())
