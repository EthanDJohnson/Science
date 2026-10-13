"""M-MECHANIST-07: the Pauli-Jordan field of a source (natural units, c = 1).

For a point source with time profile f(t) of compact support near t = 0, the retarded and advanced fields are
f(t - r)/(4 pi r) and f(t + r)/(4 pi r). Claim: their difference phi_PJ = [f(t - r) - f(t + r)]/(4 pi r) is a
SOURCE-FREE solution (regular at r = 0), equals the retarded (outgoing) field at late times and minus the advanced
(incoming, converging) field at early times.
Checks: radial wave equation, regularity limit at r -> 0, early/late-time pieces with a Gaussian profile.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, finish

t = sp.symbols("t", real=True)
r, tau = sp.symbols("r tau", positive=True)
f = sp.Function("f")
phi = (f(t - r) - f(t + r)) / (4 * sp.pi * r)
wave = sp.diff(r * phi, r, 2) / r - sp.diff(phi, t, 2)        # spherically symmetric box (flat, source-free)
identity(sp.simplify(wave), 0)
# regular at the origin (no delta source): finite limit -f'(t)/(2 pi), with f = Gaussian of width tau
g = sp.exp(-(t - r) ** 2 / tau**2); gp = sp.exp(-(t + r) ** 2 / tau**2)
limit((g - gp) / (4 * sp.pi * r), "r", 0, -sp.diff(sp.exp(-t**2 / tau**2), t) / (2 * sp.pi),
      domain={"t": (-5, 5), "tau": (0.1, 10)})
# Late times (t = r + x, x = O(tau), r >> tau): the advanced piece is exp(-(2r + x)^2/tau^2), negligible -> retarded only.
x = sp.symbols("x", real=True)
adv_late = sp.exp(-(2 * r + x) ** 2 / tau**2)
limit(adv_late, "r", sp.oo, 0, domain={"x": (-3, 3), "tau": (0.1, 10)})
# Early times (t = -r + x): the retarded piece exp(-(-2r + x)^2/tau^2) -> 0, leaving -f(t + r)/(4 pi r): converging.
ret_early = sp.exp(-(x - 2 * r) ** 2 / tau**2)
limit(ret_early, "r", sp.oo, 0, domain={"x": (-3, 3), "tau": (0.1, 10)})
raise SystemExit(finish())
