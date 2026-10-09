"""M-IDEALIZER-03: time-machine threshold in the point-mouth handle, and the MM-like numbers.

Model: static mouths A, B, separation d (flat exterior, c explicit). After mouth B has gained a clock
offset Delta relative to A (B's clock behind), the throat identifies (t, A) with (t + L/c - Delta, B)
in exterior synchronised time. Loop A -> throat -> B -> exterior -> A returns at t + L/c - Delta + d/c.
Closed causal curve iff L/c - Delta + d/c <= 0  <=>  Delta >= (d + L)/c.
Twin-paradox accumulation (out-and-back at speed v, exterior duration T): Delta = T (1 - sqrt(1 - v^2/c^2)).
Claim: MM-like pi*ell = 9.4e3 ly, d = 1e3 ly -> Delta >= 1.04e4 yr; T = 1.2e4 yr at 0.99c, 7.8e4 yr at 0.5c.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, sign, quantity, units, finish

L, d, c, Delta, t = sp.symbols("L d c Delta t", positive=True)
ret = t + L / c - Delta + d / c
thr = sp.solve(sp.Eq(ret - t, 0), Delta)[0]
identity(thr, (d + L) / c)
# limit L -> 0: Morris-Thorne-Yurtsever short-throat threshold Delta >= d/c
limit(thr, "L", 0, d / c)
units("(9.4e3 ly + 1e3 ly)/c", "time")
quantity("(9.4e3 ly + 1e3 ly)/c", "1.04e4 yr", rel_tol=1e-3)

v = sp.symbols("v", positive=True)
T = Delta / (1 - sp.sqrt(1 - v**2))       # v in units of c
# small-v limit: T -> 2 Delta / v^2 (offset grows only at second order)
limit(T * v**2 / Delta, "v", 0, 2, domain={"Delta": (0.1, 10)})
for vv, claim in [(0.99, 1.2e4), (0.5, 7.8e4)]:
    Tv = 1.04e4 / (1 - math.sqrt(1 - vv**2))
    print(f"v = {vv} c: exterior trip time T = {Tv:.4g} yr (claim {claim:.2g} yr)")
    quantity(f"{Tv} yr", f"{claim} yr", rel_tol=0.02)
raise SystemExit(finish())
