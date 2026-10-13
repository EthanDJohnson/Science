"""M-EMPIRICIST-05: GW170817 c_M bound -> GW/EM luminosity-distance ratio.
Running Planck mass: alpha_M = d ln M*^2 / d ln a. Friction term modifies h ~ 1/(M* d_EM), so
d_GW/d_EM = M*(0)/M*(z) = exp( (1/2) int_0^z alpha_M(z') dz'/(1+z') ).  Assume alpha_M = c_M (const) at z << 1.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, series, quantity, finish

cM, z, zp = sp.symbols("c_M z zp", real=True)
ratio = sp.exp(sp.Rational(1, 2) * sp.integrate(cM / (1 + zp), (zp, 0, z)))
identity(sp.simplify(ratio), (1 + z)**(cM / 2), domain={"c_M": (-40, 20), "z": (0, 0.1)})
# small-z limit: ratio - 1 ~ c_M z / 2
series(ratio, "z", 0, 2, 1 + cM * z / 2)

zz = 0.0099
lo, hi = -9 - 28, -9 + 21
r_lo = (1 + zz)**(lo / 2) - 1
r_hi = (1 + zz)**(hi / 2) - 1
r_c = (1 + zz)**(-9 / 2) - 1
print(f"c_M range [{lo}, {hi}]; d_GW/d_EM - 1 in [{r_lo:.4f}, {r_hi:.4f}], central {r_c:.4f}")
quantity(f"{r_lo}", "-0.17", rel_tol=0.03)
quantity(f"{r_hi}", "0.06", rel_tol=0.03)
# distance at z = 0.0099 for H0 = 70 km/s/Mpc, low-z Hubble law (the '~40 Mpc')
D = 299792.458 * zz / 70
print(f"D ~ {D:.1f} Mpc")
quantity(f"{D} Mpc", "42 Mpc", rel_tol=0.03)
raise SystemExit(finish())
