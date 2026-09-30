"""M-CONSTRAINTS-05: equally spaced d-level clock (hbar = 1, omega = 1 rad/s).

H_C = omega * diag(0..d-1). Time states |t> = d^-1/2 sum_n e^{-i n omega t}|n>.
Claims (F5): |<t|t+tau>| (normalized) = 0 at lattice tau = 2 pi j/(d omega) (j != 0 mod d);
= 0.90 at a quarter lattice step and 0.64 at a half step for d = 4, 16, 64;
covariant POVM (d omega/2pi) int_0^{2pi/omega} |t><t| dt = 1;
Mandelstam-Tamm resolution pi/(2 Delta E) = 1.41, 0.34, 0.085 s for d = 4, 16, 64
(Delta E = spread of H_C in a time state).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, limit, quantity, finish

x, d = sp.symbols("x d", positive=True)
# Closed form of the overlap |sum_{n<d} e^{-i n x}|/d = |sin(d x/2)/(d sin(x/2))|
dd = 7
xs = sp.symbols("xs", positive=True)
lhs = sp.Abs(sum(sp.exp(-sp.I * n * xs) for n in range(dd))) / dd
identity(lhs, sp.Abs(sp.sin(dd * xs / 2) / (dd * sp.sin(xs / 2))), domain={"xs": (0.05, 3)})

for dv, mt_exp in [(4, 1.41), (16, 0.34), (64, 0.085)]:
    step = 2 * np.pi / dv
    ov = lambda tau: abs(np.sum(np.exp(-1j * np.arange(dv) * tau))) / dv
    lat = max(ov(j * step) for j in range(1, dv))
    q, h = ov(step / 4), ov(step / 2)
    # POVM resolution of identity by quadrature over one period (trapezoid on 4d points is exact for trig polys)
    ts = np.linspace(0, 2 * np.pi, 8 * dv, endpoint=False)
    P = sum(np.outer(np.exp(-1j * np.arange(dv) * t), np.exp(1j * np.arange(dv) * t)) for t in ts) / len(ts)
    defect = np.max(np.abs(P - np.eye(dv)))
    dE = np.sqrt((dv**2 - 1) / 12.0)          # std of uniform 0..d-1
    mt = np.pi / (2 * dE)
    print(f"d={dv}: lattice max overlap {lat:.2e}, quarter {q:.4f}, half {h:.4f}, POVM defect {defect:.1e}, "
          f"dE {dE:.4f} rad/s, pi/(2dE) {mt:.4f} s")
    quantity(f"{q}", "0.90", rel_tol=0.01)
    quantity(f"{h}", "0.64", rel_tol=0.025)
    quantity(f"{mt} s", f"{mt_exp} s", rel_tol=0.01)
    print("PASS lattice orthogonality" if lat < 1e-12 else "FAIL lattice orthogonality")
    print("PASS POVM identity" if defect < 1e-12 else "FAIL POVM identity")
# large-d limits: quarter step -> sin(pi/4)/(pi/4) = 0.9003, half step -> 2/pi = 0.6366
limit(sp.sin(sp.pi / 4) / (d * sp.sin(sp.pi / (4 * d))), "d", sp.oo, 2 * sp.sqrt(2) / sp.pi)
limit(1 / (d * sp.sin(sp.pi / (2 * d))), "d", sp.oo, 2 / sp.pi)
raise SystemExit(finish())
