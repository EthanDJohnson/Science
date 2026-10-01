"""M-IDEALIZER-08: Sagnac offset along the axis (F8, F13). Linear theory, unit lapse; SI for times.
Metric along the axis: -dt^2 + (dz + w dt)^2, w = beta S(|z|). Null: dz/dt = +-1 - w, so
t(+) - t(-) = int dz [1/(1 - w) - 1/(1 + w)] = 2 int w/(1 - w^2) dz ~ 2 beta int S dz.
Claims: int S(|z|) dz = 30.0 m for all three profiles (R1 = 10, R2 = 20); Delta t = 8.0 ns at beta = 0.04;
cavity lapse factor 1/0.579 = 1.73; whole-path upper estimate 13.8 ns.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/idealizer")
import numpy as np
import sympy as sp
from math_checks import identity, series, quantity, units, finish
from profiles import S_of, C_SI

wv, zz = sp.symbols("w z", positive=True)
identity(sp.simplify(1/(1 - wv) - 1/(1 + wv)), 2*wv/(1 - wv**2), domain={"w": (0, 0.9)})
series(1/(1 - wv) - 1/(1 + wv), "w", 0, 2, "2*w")
zs = np.linspace(0, 25, 2_500_001)
for kind in ("sigmoid", "cubic", "quintic"):
    S = S_of(kind, zs, 10.0, 20.0)
    I = 2*np.trapezoid(S, zs)
    print(f"{kind}: int S(|z|) dz = {I:.5f} m")
    quantity(f"{I} m", "30.0 m", rel_tol=1e-4)
beta = 0.04
dt = 2*beta*30.0/C_SI
print(f"Delta t (beta = 0.04, N = 1) = {dt*1e9:.4f} ns")
quantity(f"2*0.04*30 m / (2.99792458e8 m/s)", "8.0 ns", rel_tol=0.005)
units("2*0.04*30 m / (2.99792458e8 m/s)", "s")
# exact (non-linearised in w) along the axis, cavity part dominates: tiny correction
exact = 2*np.trapezoid(beta*S_of("cubic", zs, 10, 20)/(1 - (beta*S_of("cubic", zs, 10, 20))**2), zs)*2
print(f"non-linearised in w: {exact/C_SI*1e9:.4f} ns")
quantity(f"{1/0.579}", "1.73", rel_tol=0.003)
quantity(f"{dt*1e9/0.579}", "13.8", rel_tol=0.005)
raise SystemExit(finish())
