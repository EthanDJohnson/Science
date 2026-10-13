"""M-DIALECTICIAN-08: far-zone scaling of where an outgoing shell's yield is made (F7).

Premises (as stated by the lens, labelled scaling estimate): shell of fixed energy and fixed
thickness, so number density n ~ 1/r^2; angular spread th = 1/(k r); cross section ~ G^2 s with
s ~ w^2 th^2; flux factor (1 - cos th) ~ th^2/2; shell volume ~ 4 pi r^2 dr; rate per volume
~ n^2 sigma (1 - cos th). Claim: dR/dr ~ r^-6, fraction of yield beyond r = (r0/r)^5 if the law
holds from r0 = 1/k = lambda/(2 pi). Numbers: 0.03125 at 2 r0; GW150914 150 Hz: r0 = 3.2e5 m,
beyond c tau = 1.07e12 m: ~2.3e-33; beyond 410 Mpc: ~1e-98. Also: any power p > 1 converges.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import math
from math_checks import identity, limit, quantity, finish
from unit_tools import Q

r, k, w, G, r0, x, p = sp.symbols("r k w G r0 x p", positive=True)
th = 1 / (k * r)
n = 1 / r**2
sigma = G**2 * w**2 * th**2
dRdr = n**2 * sigma * (1 - sp.cos(th)) * 4 * sp.pi * r**2
lead = sp.limit(dRdr * r**6, r, sp.oo)
print("r^6 dR/dr -> ", lead)
limit(dRdr * r**6, "r", sp.oo, lead)  # finite, nonzero => r^-6
identity(sp.simplify(lead), 2 * sp.pi * G**2 * w**2 / k**4)
tail = sp.integrate(r**-6, (r, x, sp.oo)) / sp.integrate(r**-6, (r, r0, sp.oo))
identity(tail, (r0 / x) ** 5)
quantity(f"{(1/2)**5}", "0.03125", rel_tol=1e-9)
# convergence of the tail for general power p > 1
tailp = sp.integrate(r**-p, (r, x, sp.oo), conds="none")
identity(sp.simplify(tailp.subs(p, 2)), 1 / x)
# numbers
c = Q("c").to("m/s")
r0v = c / (2 * math.pi * 150.0)
ctau = c * 3578.0
D = Q("410 Mpc").to("m")
print(f"r0 = {r0v:.4e} m, c tau = {ctau:.4e} m, (r0/c tau)^5 = {(r0v/ctau)**5:.3e}, (r0/D)^5 = {(r0v/D)**5:.3e}")
quantity(f"{r0v} m", "3.2e5 m", rel_tol=1e-2)
quantity(f"{ctau} m", "1.07e12 m", rel_tol=5e-3)
quantity(f"{(r0v/ctau)**5}", "2.3e-33", rel_tol=3e-2)
quantity(f"{(r0v/D)**5}", "1e-98", rel_tol=0.5)
raise SystemExit(finish())
