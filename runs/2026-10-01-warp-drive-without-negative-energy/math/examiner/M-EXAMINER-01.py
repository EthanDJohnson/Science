"""M-EXAMINER-01: Alcubierre (N = 1) centre payload moves at dx/dt = v with dtau = dt.

Metric (geometric, c = 1): ds^2 = -dt^2 + (dx - v f(r_s) dt)^2 + dy^2 + dz^2, r_s = distance from
the bubble centre x_s(t) = v t. At the centre f = 1. Claim: the worldline x = v t, y = z = 0 is a
timelike geodesic with dtau = dt, and at v = 10 the 4.37 ly trip takes 0.437 yr (exterior and proper).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, sign, finish
from gr_tensors import metrics

t, v, f1 = sp.symbols("t v f1", positive=True)
dt = sp.Symbol("dt", positive=True)
# Line element along dx = v dt with f = f1 (general), then f1 = 1 at the centre
ds2 = -dt**2 + (v*dt - v*f1*dt)**2
print("ds^2 along x = v t with f = f1:", sp.simplify(ds2))
identity(ds2.subs(f1, 1), -dt**2)          # dtau^2 = dt^2 at the centre
# Off-centre (f1 < 1) the same worldline would have dtau < dt; at f1=1 exactly equal
sign((-ds2 / dt**2).subs(f1, sp.Rational(1, 2)) - 1, "negative", domain={"v": (0.01, 0.99)})

# Geodesic check with the toolkit's Alcubierre metric: the 4-velocity u = (1, v, 0, 0) at the centre
st, s = metrics.alcubierre()
print("toolkit symbols:", s)
G = st.christoffel()
top = metrics.alcubierre_top_hat(s)
u = [1, s["v"], 0, 0]
acc = [sum(G[m][a][b] * u[a] * u[b] for a in range(4) for b in range(4)) for m in range(4)]
pars = {s["v"]: 10, s["R"]: 100, s["sigma"]: 2}
for tt in (0.0, 3.0):
    pt = {s["t"]: tt, s["x"]: 10 * tt + 1e-7, s["y"]: 0, s["z"]: 0}
    vals = [float(sp.N(a_.subs(s["f"], top).subs(pars).doit().subs(pt))) for a_ in acc]
    print(f"geodesic acceleration Gamma^mu_ab u^a u^b at centre, t={tt}: {vals}")
    assert max(abs(x) for x in vals) < 1e-6, "centre worldline not geodesic"
print("PASS centre worldline x = v t is geodesic (numeric, v=10, R=100 m, sigma=2 1/m)")

# Limit: v -> 0 the payload is at rest, dtau = dt still
limit("v*f1", "v", 0, "0")

# Trip numbers, SI
quantity("4.37 ly / (10 * c)", "0.437 yr", rel_tol=1e-6)
quantity("4.37 ly / c", "4.37 yr", rel_tol=1e-6)
units("4.37 ly / (10 * c)", "time")
raise SystemExit(finish())
