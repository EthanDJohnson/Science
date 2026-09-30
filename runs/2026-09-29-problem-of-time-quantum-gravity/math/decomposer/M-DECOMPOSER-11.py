# M-DECOMPOSER-11: Planck time t_P = sqrt(hbar G / c^5), SI
import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish
units("(hbar*G/c^5)^(1/2)", "s")
quantity("(hbar*G/c^5)^(1/2)", "5.39e-44 s", rel_tol=2e-3)
raise SystemExit(finish())
