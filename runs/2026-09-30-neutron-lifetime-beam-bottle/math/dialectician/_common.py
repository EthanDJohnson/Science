"""Shared helpers and my own transcription of inputs (dossier D-20, D-23, D-24, D-27, D-28). SI: lifetimes in s."""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, identity, limit, series, sign, inequality, units, finish  # noqa: E402,F401


def q(x, x2):
    return math.sqrt(x * x + x2 * x2)


# BL1 (Yue 2013, D-20): 887.7 +- 1.2 (stat) +- 1.9 (sys) s
BL1, sBL1 = 887.7, q(1.2, 1.9)
# UCNtau (Musedinovic 2025, D-27): 877.82 +- 0.22 (stat) +0.20/-0.17 (sys) s
UCN = 877.82
sUCN_up, sUCN_dn = q(0.22, 0.20), q(0.22, 0.17)
sUCN_sym = q(0.22, (0.20 + 0.17) / 2)
# J-PARC 2024 (D-23): 877.2 +- 1.7 (stat) +4.0/-3.6 (sys) s
JP, JPst, JPup_sys, JPdn_sys = 877.2, 1.7, 4.0, 3.6
# Gravitrap (Serebrov 2018, D-28): 881.5 +- 0.7 +- 0.6 s
GRV, sGRV = 881.5, q(0.7, 0.6)
# J-PARC per-condition (D-24), stat only: (pressure kPa, SFC, tau s, stat s)
JCONF = [(100, "old", 870.9, 3.5), (100, "new", 868.3, 4.0), (50, "old", 868.2, 7.7), (50, "new", 884.8, 2.4)]


def num(label, got, want, unit="s", rel_tol=None, abs_tol=None):
    """Compare got to the lens's printed value; tolerance set by the lens's rounding."""
    got = float(got)
    if rel_tol is None:
        rel_tol = abs(abs_tol / want) if abs_tol else 1e-3
    print(f"  {label}: mine = {got:.6g} {unit}, lens = {want} {unit}")
    return quantity(f"{got!r} {unit}", f"{want!r} {unit}", rel_tol=rel_tol)
