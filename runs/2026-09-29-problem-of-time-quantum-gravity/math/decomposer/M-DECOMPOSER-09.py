# M-DECOMPOSER-09: change in fractional clock rate at a clock a distance d from a point mass m when m is
# displaced by dx (weak field): delta = (G m / c^2) |1/d1 - 1/d2|. First order in dx/d: G m dx / (c^2 d^2).
# SI. The lens's numbers are reproduced by the first-order (dipole) form; check the exact difference too.
import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, series, finish
import unit_tools as U
units("G * 1 g / c^2 * 1 um / (1 mm)^2", "dimensionless")
series("1/d - 1/(d + x)", "x", 0, 2, "x/d**2")                       # the linearisation, valid for x << d
# case 2: 1 g displaced 1 um at 1 mm (dx/d = 1e-3): linear and exact agree
quantity("G * 1 g / c^2 * 1 um / (1 mm)^2", "7.4e-31", rel_tol=0.01)
quantity("G * 1 g / c^2 * (1/(1 mm) - 1/(1.001 mm))", "7.4e-31", rel_tol=0.01)
# case 1: QGEM, m = 1e-14 kg, dx = 250 um, d = 450 um (dx/d = 0.56): linear reproduces the lens
quantity("G * 1e-14 kg / c^2 * 250 um / (450 um)^2", "9.2e-39", rel_tol=0.01)
# exact, mass moved away (450 -> 700 um) and toward (450 -> 200 um):
for a, b in (("450 um", "700 um"), ("200 um", "450 um"), ("325 um", "575 um")):
    v = U.Q(f"G * 1e-14 kg / c^2 * (1/({a}) - 1/({b}))").si
    print(f"exact {a} -> {b}: {v:.3e}")
quantity("G * 1e-14 kg / c^2 * (1/(450 um) - 1/(700 um))", "5.9e-39", rel_tol=0.01)
quantity("G * 1e-14 kg / c^2 * (1/(200 um) - 1/(450 um))", "2.06e-38", rel_tol=0.01)
raise SystemExit(finish())
