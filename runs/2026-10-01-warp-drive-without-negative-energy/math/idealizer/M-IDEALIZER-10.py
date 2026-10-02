"""M-IDEALIZER-10/11/12 arithmetic and kinematics (F10, F11, F12). Covers three claim IDs; the log is shared.
F10: interior metric -N^2 dt^2 + (dz + b dt)^2 (constant), g_00 = -(N^2 - b^2) fixed at 0.5793 (toolkit value,
quoted). Eulerian n = (1/N)(1, -b) vs shell-static u_s = (1/sqrt(N^2 - b^2), 0): relative speed b/N exactly.
F11: photon rocket accelerate + stop: m_i/m_f = (1 + v)/(1 - v); propellant = (ratio - 1) m_f.
F12: thin shell (M, R) moving with U(t), harmonic gauge interior h_0x = -4 M U/R, h_00 = 2M/R constant:
slow particle a_x = -Gamma^x_00 = (4M/R) dU/dt.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/idealizer")
import sympy as sp
from math_checks import identity, quantity, limit, units, finish
from profiles import KG_TO_M, C_SI

Nl, b, t = sp.symbols("N_l b t", positive=True)
g = sp.Matrix([[-Nl**2 + b**2, b], [b, 1]])
n = sp.Matrix([1/Nl, -b/Nl]); us = sp.Matrix([1/sp.sqrt(Nl**2 - b**2), 0])
dom = {"b": (0.0, 0.5), "N_l": (0.6, 2.0)}
identity((n.T*g*n)[0, 0], -1, domain=dom)
gam = -(us.T*g*n)[0, 0]
identity(sp.sqrt(1 - 1/gam**2), b/Nl, domain=dom)
limit(b/Nl, "b", 0, 0)
for bv, claim, tcl in [(0.02, 0.026, 2.5e-6), (0.04, 0.053, 1.3e-6)]:
    N = (0.5793 + bv**2)**0.5
    v = bv/N
    print(f"beta = {bv}: N = {N:.5f}, v = {v:.5f} c; 20 m crossing {20/(v*C_SI)*1e6:.3f} us; 10 m {10/(v*C_SI)*1e6:.3f} us")
    quantity(f"{v}", f"{claim}", rel_tol=0.02)
    quantity(f"20 m / ({v} * 2.99792458e8 m/s)", f"{tcl} s", rel_tol=0.03)
quantity(f"{(0.5793 + 0.0004)**0.5}", "0.7614", rel_tol=1e-4)
quantity(f"{0.5793**0.5}", "0.7611", rel_tol=1e-4)
units("20 m / (0.026 * 2.99792458e8 m/s)", "s")
# F11
v = sp.Rational(1, 25)
ratio = (1 + v)/(1 - v)
print("mass ratio", float(ratio))
quantity(f"{float(ratio)}", "1.0833", rel_tol=1e-4)
quantity(f"{float(ratio - 1)} * 4.49e27 kg", "3.74e26 kg", rel_tol=0.002)
quantity(f"{float(ratio - 1)} * 1e5 kg", "8.3e3 kg", rel_tol=0.005)
quantity(f"{float(ratio - 1)} * 4.49e27 / 1.898e27", "0.197", rel_tol=0.003)
quantity("4.49e27 / 1e5", "4.5e22", rel_tol=0.003)
vv = sp.symbols("v", positive=True)
identity(sp.sqrt((1 + vv)/(1 - vv))**2, (1 + vv)/(1 - vv), domain={"v": (0, 0.9)})
limit((1 + vv)/(1 - vv) - 1, "v", 0, 0)
# F12
Mm, R, x = sp.symbols("M R x", positive=True)
Uf = sp.Function("U")(t)
h0x = -4*Mm*Uf/R; h00 = 2*Mm/R
Gam_x_00 = (2*sp.diff(h0x, t) - sp.diff(h00, x))/2     # linear: Gamma^x_00 = d_t h_0x - (1/2) d_x h_00
acc = -Gam_x_00
identity(sp.simplify(acc - 4*Mm/R*sp.diff(Uf, t)), 0)
Mg = 4.49e27*KG_TO_M
for Rv, claim in [(20.0, 0.67), (10.0, 1.33)]:
    print(f"4GM/(c^2 R), R = {Rv}: {4*Mg/Rv:.4f}")
    quantity(f"{4*Mg/Rv}", f"{claim}", rel_tol=0.005)
units("4 * 6.6743e-11 m^3/(kg s^2) * 4.49e27 kg / ((2.99792458e8 m/s)^2 * 20 m)", "1")
raise SystemExit(finish())
