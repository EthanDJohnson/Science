"""M-ENGINEER-14: test gaps.
(a) Shadow critical impact parameter b_c = r_ph/sqrt(f(r_ph)) at the photon sphere, where d/dr (f/r^2) = 0.
    Schwarzschild f = 1 - 2M/r: 3 sqrt(3) M. Extremal RN f = (1 - M/r)^2: r_ph = 2M, b_c = 4M. Ratio 4/(3 sqrt 3).
(b) EHT lambda/D at 1.3 mm over Earth's diameter; shadow diameter 2 b_c/D for 1e4 Msun extremal RN at 1 and 10 kpc.
(c) Echo delay 9.4e3 yr (quoted) vs 2 yr; S2 gaps 4e-4/1e-6 and 2e-5/1e-6 (quoted inputs).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

r, M, Qc = sp.symbols("r M Qc", positive=True)   # Qc = charge in geometric units, 0 <= Qc <= M
f = 1 - 2 * M / r + Qc**2 / r**2
rph = sp.solve(sp.diff(f / r**2, r), r)
print("photon-sphere roots:", rph)
rp = (3 * M + sp.sqrt(9 * M**2 - 8 * Qc**2)) / 2
identity(sp.diff(f / r**2, r).subs(r, rp), 0, domain={"M": (1, 10), "Qc": (0, 1)})
bc = rp / sp.sqrt(f.subs(r, rp))
identity(bc.subs(Qc, 0), 3 * sp.sqrt(3) * M)
identity(sp.simplify(bc.subs(Qc, M)), 4 * M)
limit(bc / M, "Qc", 0, 3 * sp.sqrt(3), direction="+")
quantity(f"{4/(3*math.sqrt(3))} m/m", "0.770 m/m", rel_tol=1e-3)
uas = math.pi / 180 / 3600 / 1e6
quantity(f"{1.3e-3/1.2742e7/uas} m/m", "21 m/m", rel_tol=1e-2)
units("8*G*1e4*Msun/c^2/(1 kpc)", "dimensionless")
quantity(f"{8*6.67430e-11*1e4*1.98841e30/299792458.0**2/3.0856775814913673e19/uas} m/m", "0.79 m/m", rel_tol=1e-2)
s1 = 8*6.67430e-11*1e4*1.98841e30/299792458.0**2/3.0856775814913673e19/uas
print(f"gaps: EHT 1 kpc {math.log10(21.0/s1):.2f}, 10 kpc {math.log10(210.0/s1):.2f}; echo {math.log10(9.4e3/2):.2f}; S2 {math.log10(4e-4/1e-6):.2f}, {math.log10(2e-5/1e-6):.2f}")
quantity(f"{math.log10(9.4e3/2)} m/m", "3.7 m/m", rel_tol=1e-2)
quantity(f"{math.log10(400)} m/m", "2.6 m/m", rel_tol=1e-2)
quantity(f"{math.log10(20)} m/m", "1.3 m/m", rel_tol=1e-2)
raise SystemExit(finish())
