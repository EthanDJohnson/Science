"""M-CONSTRAINTS-09: plasma kinematic threshold (F1, F2). SI; hbar w in eV.
Photon in cold plasma: w^2 = k^2 c^2 + w_p^2, effective mass hbar w_p. g g -> gamma gamma needs
s >= 4 (hbar w_p)^2; two gravitons of energy hbar w at angle theta: s = 2 (hbar w)^2 (1 - cos theta)
= 4 (hbar w)^2 sin^2(theta/2) -> threshold sin(theta/2) >= w_p/w (needs w > w_p).
Far zone (lens's s ~ 4 w c/r, units 1/s^2 x hbar^2): s >= 4 w_p^2 -> r <= c w / w_p^2.
f_pe = 8980 Hz sqrt(n_e/cm^-3) [from w_p^2 = n e^2/(eps0 m_e)]. Cosmic: n_e(z) = n_e0 (1+z)^3.
Fixed observed f0: f0 (1+z) > f_p(z) -> f0 > f_p0 sqrt(1+z).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, inequality, quantity, limit, finish

e, eps0, me, c, h = 1.602176634e-19, 8.8541878128e-12, 9.1093837015e-31, 299792458.0, 6.62607015e-34
fp = lambda n_cm3: math.sqrt(n_cm3 * 1e6 * e**2 / (eps0 * me)) / (2 * math.pi)
quantity(f"{fp(1.0)} Hz", "8980 Hz", rel_tol=1e-3)
th, w, wp = sp.symbols("theta w w_p", positive=True)
identity(2 * w**2 * (1 - sp.cos(th)), 4 * w**2 * sp.sin(th / 2)**2, domain={"theta": (0, 3.14159), "w": (0.1, 10)})
# s_max = 4 w^2 at theta = pi; threshold requires w >= w_p
limit(2 * w**2 * (1 - sp.cos(th)), "theta", sp.pi, 4 * w**2)
for n, want in [(2.2e-7, 4.2), (2.75e-8, 1.5), (3e-3, 492), (0.03, 1560), (0.08, 2540)]:
    print(f"n_e={n} cm^-3: f_pe={fp(n):.4g} Hz")
    quantity(f"{fp(n)} Hz", f"{want} Hz", rel_tol=0.03)
f = 150.0
thmin = 2 * math.degrees(math.asin(fp(2.2e-7) / f))
print("theta_min at 150 Hz, mean IGM:", thmin, "deg")
quantity(f"{thmin}", "3.2", rel_tol=0.02)
for n, want in [(2.2e-7, 4.0e8), (2.75e-8, 3.2e9)]:
    rmax = c * (2 * math.pi * f) / (2 * math.pi * fp(n))**2
    print(f"r_max (n={n}) = {rmax:.3e} m = {rmax/(c/f):.0f} lambda")
    quantity(f"{rmax} m", f"{want} m", rel_tol=0.03)
# n_e above which 150 Hz production is forbidden: (150/8980)^2
print("n_e threshold at 150 Hz:", (150 / 8980)**2, "cm^-3")
quantity(f"{(150/8980)**2}", "2.8e-4", rel_tol=0.01)
for zz, want in [(1100, 6.4e-10), (1e4, 1.7e-8), (1e5, 5.5e-7), (3e6, 9.1e-5)]:
    E = h * fp(2.2e-7 * (1 + zz)**3) / e
    print(f"z={zz:g}: hbar w_p = {E:.3e} eV")
    quantity(f"{E}", f"{want}", rel_tol=0.03)
for zz, want in [(1e5, 1.3e3), (2e6, 6.0e3)]:
    f0 = fp(2.2e-7) * math.sqrt(1 + zz)
    print(f"z={zz:g}: f0 > {f0:.4g} Hz")
    quantity(f"{f0}", f"{want}", rel_tol=0.03)
print("f0 threshold at z = 1100:", fp(2.2e-7) * math.sqrt(1101), "Hz (> 25 Hz, so LVK band makes none at z > 1100)")
inequality(f"{fp(2.2e-7)} * sqrt(1 + zz)", ">", "25", domain={"zz": (1100, 1e7)})
raise SystemExit(finish())
