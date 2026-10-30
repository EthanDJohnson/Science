"""M-MECHANIST-03: coherent outflow needed (finding 3).
Low-z Hubble law: H_obs = (c z_cos + v)/d, H_true = c z_cos/d, so v = (H_obs/H_true - 1) c z_cos.
H_obs/H_true = 73.264/67.19 (gap); z = 0.05, 0.07; c = 299792.458 km/s. Valid for z << 1 (first order).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/mechanist")
import sympy as sp
from math_checks import identity, limit, quantity, finish
from mm_common import near

c, z, d, v, Ht = sp.symbols("c z d v H_t", positive=True)
Hobs = (c * z + v) / d
Htrue = c * z / d
identity((Hobs / Htrue - 1) * c * z, v)
limit("(r - 1)*c*z", "r", 1, "0")        # no gap -> no flow
quantity("0.0904 * 299792.458 km/s * 0.05", "1355 km/s", rel_tol=2e-3)
r = 73.264 / 67.19
near("v at z=0.05 km/s", (r - 1) * 299792.458 * 0.05, 1355, 3)
near("v at z=0.07 km/s", (r - 1) * 299792.458 * 0.07, 1897, 3)
raise SystemExit(finish())
