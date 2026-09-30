"""M-CONSTRAINTS-04: Goedel metric (G = c = 1, length scale a_G).

ds^2 = 4 a^2 [ -dt^2 + dr^2 + (sinh^2 r - sinh^4 r) dphi^2 + 2 sqrt2 sinh^2 r dphi dt ] + dz^2  (standard form)
Claim: the required T_ab (G_ab = 8 pi T_ab, Lambda = 0) satisfies NEC, WEC, SEC, DEC (type I) at r = 0.1..2.5,
and g_phiphi < 0 for r > asinh(1) = 0.8814 (closed timelike phi-circles).
Independent: compute G_ab with gr_tensors, identify it as a stiff fluid rho = p, check eigenvalues analytically.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import numpy as np
from gr_tensors import Spacetime
from math_checks import identity, sign, limit, quantity, finish

t, r, ph, z = sp.symbols("t r phi z", real=True)
aG = sp.symbols("aG", positive=True)
s = sp.sinh(r)
g = sp.zeros(4, 4)
g[0, 0] = -4 * aG**2
g[1, 1] = 4 * aG**2
g[2, 2] = 4 * aG**2 * (s**2 - s**4)
g[0, 2] = g[2, 0] = 4 * aG**2 * sp.sqrt(2) * s**2
g[3, 3] = 1
st = Spacetime(g, [t, r, ph, z], simplify=True)
G = st.einstein().applyfunc(sp.simplify)
# fluid 4-velocity u = d_t / (2 aG), u_a = g_{a0}/(2aG)
u_low = sp.Matrix([g[i, 0] for i in range(4)]) / (2 * aG)
rho = sp.simplify((sp.Matrix([1, 0, 0, 0]).T * G * sp.Matrix([1, 0, 0, 0]))[0] / (4 * aG**2) / (8 * sp.pi))
print("rho (rest frame) =", rho)
identity(rho, 1 / (16 * sp.pi * aG**2))
# Stiff fluid: 8 pi T_ab = 8 pi [ (rho+p) u_a u_b + p g_ab ] with p = rho
p = rho
T_fluid = (rho + p) * (u_low * u_low.T) + p * g
diff = (G - 8 * sp.pi * T_fluid).applyfunc(sp.simplify)
print("G - 8 pi T_stiff =", diff)
identity(sum(abs(e) for e in diff), "0")
# Energy conditions for a perfect fluid with rho = p = 1/(16 pi aG^2) > 0:
# NEC rho+p >= 0, WEC rho >= 0, SEC rho+3p >= 0, DEC rho >= |p| (saturated)
sign(rho + p, "positive")
sign(rho, "positive")
sign(rho + 3 * p, "positive")
sign(rho - abs(p), "nonnegative")
# gr_tensors scan at 25 radii, aG = 1
pts = [(0.0, float(rv), 0.3, 0.0) for rv in np.linspace(0.1, 2.5, 25)]
scan = st.scan_energy_conditions(pts, params={aG: 1.0})
print("scan:", scan)
# CTC: g_phiphi < 0 iff sinh r > 1
gpp = s**2 - s**4
identity(sp.asinh(1), sp.log(1 + sp.sqrt(2)))
quantity(f"{float(sp.asinh(1))}", "0.8814", rel_tol=1e-4)
sign(gpp, "negative", domain={"r": (0.8814 + 1e-3, 3)})
sign(gpp, "positive", domain={"r": (1e-3, 0.8813)})
limit(gpp / r**2, "r", 0, "1")   # small r: flat-space cylindrical behaviour g_phiphi ~ 4a^2 r^2
raise SystemExit(finish())
