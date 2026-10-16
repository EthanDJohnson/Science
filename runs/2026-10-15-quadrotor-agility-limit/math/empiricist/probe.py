"""Probe: how to compare bare numbers with math_checks."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, inequality, quantity, units, finish

got = 0.443906
inequality(f"abs({got} - 0.444)", "<", "0.001")
quantity("12.88 m/s", "12.88 m/s", rel_tol=1e-3)
units("75 m / 5.8217 s", "velocity")
identity("atan(1)", "pi/4")
raise SystemExit(finish())
