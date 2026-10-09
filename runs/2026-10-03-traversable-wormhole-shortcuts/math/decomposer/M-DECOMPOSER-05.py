"""M-DECOMPOSER-05: Ellis throat b0 = 1 m, static observers at areal radius R = 10 m on each side.

Ellis-Bronnikov metric: ds^2 = -c^2 dt^2 + dl^2 + (b0^2 + l^2) dOmega^2 (Phi = 0, so t is the
static observers' proper time). Areal radius r = sqrt(b0^2 + l^2). Radial null: dl = c dt.
T_thru = 2 l_R / c with l_R = sqrt(R^2 - b0^2). Exterior comparison T_ext = d/c (mouths treated as
embedded in one flat ambient space; the observer offsets R << d are neglected, as the lens does).
CTC lag (M-DECOMPOSER-01) = (L + d)/c with L = 2 l_R.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

l, b0, R = sp.symbols("l b0 R", positive=True)
r = sp.sqrt(b0**2 + l**2)
# proper radial distance from throat to areal radius R: integral of dl = sqrt(R^2 - b0^2)
lR = sp.solve(sp.Eq(r, R), l)[0]
identity(lR, sp.sqrt(R**2 - b0**2), domain={"R": (1.1, 10), "b0": (0.1, 1)})
# far-field limit: path length through throat -> 2R (flat-space value) when b0 -> 0
limit(2 * sp.sqrt(R**2 - b0**2), "b0", 0, 2 * R)

lR_m = math.sqrt(10**2 - 1**2)
T_thru = f"2 * {lR_m} m / c"
quantity(T_thru, "6.6e-8 s", rel_tol=1e-2)
units(T_thru, "time")
for dist, claim, tol in [("1 km", "0.020", 2e-2), ("1 au", "1.3e-10", 3e-2), ("1 ly", "2.1e-15", 2e-2)]:
    quantity(f"(2 * {lR_m} m / c) / ({dist} / c)", claim, rel_tol=tol)
# same ratio with T_ext measured between the observers on the line of centres, (d - 2R)/c, at d = 1 km
quantity(f"(2 * {lR_m} m) / (1 km - 20 m)", "0.020", rel_tol=3e-2)
# CTC lag at d = 1 ly: (L + d)/c ~ 1 yr
quantity(f"(2 * {lR_m} m + 1 ly) / c", "1 yr", rel_tol=1e-6)
raise SystemExit(finish())
