"""M-CONSTRAINTS-12: ULDM kinematics and resonance time (F13). Natural units for kinematics, SI for times.
Two gravitons of energy w = m each (resonance), deviating by delta from head-on: |k1 + k2| = 2 w sin(delta/2) ~ w delta.
Two NR scalars with speeds <= v: |p1 + p2| <= 2 m v -> delta <= 2 v (w = m). Solid-angle fraction ~ pi delta^2/(4 pi) = delta^2/4.
Resonance width sigma = m v^2/(2 hbar); resolving time 1/sigma. Binary at ISCO with GW w = m/hbar:
M = 0.136 c^3/(G w). Equal masses, chirp mass Mc = M (1/4)^{3/5}; quadrupole df/dt = (96/5) pi^{8/3} (G Mc/c^3)^{5/3} f^{11/3};
time in band Dt = (sigma/2pi)/(df/dt). Claims: delta = 2e-3 rad, fraction 1e-6, hbar c/m = 2e14 m (1e-21 eV),
1/sigma = 1.3e12 s (1e-21 eV), 1.3e13 s (1e-22 eV), M = 1.8e10 / 1.8e11 Msun, Dt = 12 / 120 s, shortfall 1.1e11.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, finish

dl, w = sp.symbols("delta w", positive=True)
# k1 = w zhat, k2 = -w (sin d, 0, cos d)
k1 = sp.Matrix([0, 0, w]); k2 = -w * sp.Matrix([sp.sin(dl), 0, sp.cos(dl)])
mag = sp.sqrt(sp.simplify((k1 + k2).dot(k1 + k2)))
identity(sp.simplify(mag**2), (2 * w * sp.sin(dl / 2))**2, domain={"delta": (0, 3), "w": (0.1, 10)})
limit(mag / (w * dl), "delta", 0, 1)
v = 1e-3
print("delta_max =", 2 * v, "; fraction =", (2 * v)**2 / 4)
quantity(f"{(2*v)**2/4}", "1e-6", rel_tol=1e-6)
G, c, hbar_eVs, hbarc_eVm, Msun = 6.67430e-11, 299792458.0, 6.582119569e-16, 1.973269804e-7, 1.98841e30
quantity(f"{hbarc_eVm/1e-21} m", "2e14 m", rel_tol=0.02)
prev = None
for m, want_t, want_M, want_dt in [(1e-21, 1.3e12, 1.8e10, 12), (1e-22, 1.3e13, 1.8e11, 120)]:
    sig = m * v**2 / 2 / hbar_eVs
    wg = m / hbar_eVs
    M = 0.136 * c**3 / (G * wg)
    Mc = M * 0.25**0.6
    f = wg / (2 * math.pi)
    fdot = 96 / 5 * math.pi**(8 / 3) * (G * Mc / c**3)**(5 / 3) * f**(11 / 3)
    dt = (sig / (2 * math.pi)) / fdot
    print(f"m={m} eV: 1/sigma={1/sig:.3e} s, M={M/Msun:.3e} Msun, fdot={fdot:.3e} Hz/s, Dt={dt:.3g} s, shortfall={1/sig/dt:.3e}")
    quantity(f"{1/sig}", f"{want_t}", rel_tol=0.03)
    quantity(f"{M/Msun}", f"{want_M}", rel_tol=0.03)
    quantity(f"{dt}", f"{want_dt}", rel_tol=0.05)
    quantity(f"{1/sig/dt}", "1.1e11", rel_tol=0.05)
raise SystemExit(finish())
