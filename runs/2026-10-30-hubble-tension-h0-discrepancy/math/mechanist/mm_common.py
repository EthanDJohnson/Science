"""Shared helpers for the mechanist math checks (written by the math checker, not the lens)."""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import inequality  # noqa: E402

LN10 = math.log(10.0)


def dmag(ha, hb):
    """Distance-modulus / M_B offset equivalent to H0 ratio ha/hb: Δm = 5 log10(ha/hb) (mag)."""
    return 5.0 * math.log10(ha / hb)


def near(label, got, claim, tol):
    """PASS if |got - claim| <= tol; prints both numbers."""
    print(f"  {label}: recomputed {got:.6g}, lens claims {claim}, tol {tol}")
    return inequality(f"Abs({got!r} - ({claim!r}))", "<=", f"{tol!r}")


def tension(a, sa, b, sb):
    return abs(a - b) / math.hypot(sa, sb)
