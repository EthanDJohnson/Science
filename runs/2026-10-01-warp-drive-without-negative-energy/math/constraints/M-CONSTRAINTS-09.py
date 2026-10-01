"""M-CONSTRAINTS-09: quantum-inequality and horizon numbers, Alcubierre reference case (F11; C).

Geometric units unless SI. R = 100 m, sigma = 2 /m (Delta = 1 m), v = 10.
(1) peak Eulerian density on the transverse axis: rho = -(v^2/32 pi) f'(R)^2 (own formula, M-01).
(2) curvature radius r_c = 1/sqrt(max |R_ABCD|) in the Eulerian frame at that point (toolkit curvature_at).
(3) Ford-Roman: rho_avg >= -3 hbar c/(32 pi^2 (c tau0)^4) [SI]; geometric (x G/c^4): -3 L_P^2/(32 pi^2 tau0^4), tau0 = 0.1 r_c.
(4) rho ~ Delta^-2 and r_c ~ Delta => |rho|/|bound| ~ Delta^2 => Delta_QI = Delta/sqrt(factor).
(5) Horizon: v(1 - f) = 1; kappa = v |f'| there; T_H = hbar c kappa/(2 pi k_B).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import quantity, identity, units, finish
from gr_tensors import metrics

R, s, v = 100.0, 2.0, 10.0
sech2 = lambda w: 4 * math.exp(-2 * abs(w)) / (1 + math.exp(-2 * abs(w)))**2
fpR = (s * sech2(2 * s * R) - s) / (2 * math.tanh(s * R))
rho = -(v**2 / (32 * math.pi)) * fpR**2
quantity(f"{rho}", "-0.9947", rel_tol=1e-4)
quantity(f"{rho} m^-2 * c^4/G", "-1.20e44 J/m^3", rel_tol=3e-3)
st, sy = metrics.alcubierre()
top = metrics.alcubierre_top_hat(sy)
cv = st.curvature_at((0.0, 0.0, 100.0, 0.0), params={sy["v"]: 10, sy["R"]: 100, sy["sigma"]: 2}, functions={sy["f"]: top})
rc = cv["curvature_radius"]
print("curvature at transverse wall point:", cv)
quantity(f"{rc}", "0.115", rel_tol=1e-2)
hbar, c, G, kB = 1.054571817e-34, 299792458.0, 6.67430e-11, 1.380649e-23
LP = math.sqrt(hbar * G / c**3)
tau0 = 0.1 * rc
bound = -3 * LP**2 / (32 * math.pi**2 * tau0**4)
print("FR bound (m^-2):", bound, " factor:", rho / bound)
quantity(f"{bound}", "-1.4e-64", rel_tol=0.03)
quantity(f"{bound} m^-2 * c^4/G", "-1.7e-20 J/m^3", rel_tol=0.03)
fac = rho / bound
quantity(f"{fac}", "7.1e63", rel_tol=0.03)
dqi = 1.0 / math.sqrt(fac)
quantity(f"{dqi} m", "1.19e-32 m", rel_tol=0.02)
quantity(f"{dqi / LP}", "733", rel_tol=0.02)
quantity(f"{dqi / LP / v}", "73", rel_tol=0.02)
E = v**2 * R**2 / (18 * dqi)
quantity(f"{E} m * c^2/G", "6.3e63 kg", rel_tol=0.02)
quantity(f"{E} m * c^2/G", "3.2e33 Msun", rel_tol=0.02)
quantity(f"{rc * dqi / LP}", "85", rel_tol=0.03)
# scaling exponents (symbolic): bound ~ tau0^-4 ~ Delta^-4; rho ~ Delta^-2 => ratio ~ Delta^2
D = sp.symbols("D", positive=True)
identity((D**-2) / (D**-4), D**2)
# horizon
xi = 100 + math.atanh(-0.8) / s    # [1 - tanh(s(r - R))]/2 = 0.9 (exterior tail of the other tanh negligible)
f = lambda r: (math.tanh(s * (r + R)) - math.tanh(s * (r - R))) / (2 * math.tanh(s * R))
print("horizon xi:", xi, " v(1-f):", v * (1 - f(xi)))
quantity(f"{xi}", "99.45", rel_tol=1e-4)
fp = (s * sech2(s * (xi + R)) - s * sech2(s * (xi - R))) / (2 * math.tanh(s * R))
kap = v * abs(fp)
quantity(f"{kap}", "3.6", rel_tol=1e-3)
quantity(f"hbar * c * {kap} m^-1 / (2*pi*kB)", "1.3e-3 K", rel_tol=0.02)
units("hbar * c * 1 m^-1 / kB", "K")
raise SystemExit(finish())
