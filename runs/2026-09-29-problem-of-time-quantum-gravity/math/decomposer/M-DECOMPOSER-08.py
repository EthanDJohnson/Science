# M-DECOMPOSER-08: two-level internal clock (splitting hbar*omega) in equal superposition, arms at heights
# differing by dh for lab time T. Proper-time difference dtau = g dh T / c^2 (weak field).
# Which-path information in the clock: V = |<c1|c2>| = |cos(omega dtau / 2)|. SI units.
import sys, math; sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import quantity, units, identity, series, finish
import unit_tools as U
# derive V from states: |c(tau)> = (|0> + e^{-i w tau}|1>)/sqrt2
w, t1, t2 = sp.symbols("w t1 t2", positive=True)
ov = sp.Rational(1, 2) * (1 + sp.exp(sp.I * w * (t1 - t2)))
identity(sp.simplify(sp.Abs(ov)**2), sp.cos(w * (t1 - t2) / 2)**2, domain={"w": (0.1, 10), "t1": (0.1, 10), "t2": (0.1, 10)})
units("2*pi*429 THz * g0 * 1 m * 1 s / c^2", "dimensionless")
for dh, claim in ((0.25, "0.99932"), (1.0, "0.98921")):
    phase = U.Q(f"2*pi*429 THz * g0 * {dh} m * 1 s / c^2").si / 2
    V = abs(math.cos(phase))
    print(f"dh = {dh} m: phase/2 = {phase:.6f} rad, V = {V:.6f}, 1-V = {1-V:.3e}")
    quantity(f"{V}", claim, rel_tol=2e-5)
quantity(f"{1-abs(math.cos(U.Q('2*pi*429 THz * g0 * 0.25 m * 1 s / c^2').si/2))}", "6.8e-4", rel_tol=1e-2)
quantity(f"{1-abs(math.cos(U.Q('2*pi*429 THz * g0 * 1 m * 1 s / c^2').si/2))}", "1.1e-2", rel_tol=3e-2)
# limit: small phase, 1 - V ~ (omega dtau)^2 / 8; dh -> 0 gives V -> 1
x = sp.symbols("x", positive=True)
series("1 - cos(x/2)", "x", 0, 4, "x**2/8")
raise SystemExit(finish())
