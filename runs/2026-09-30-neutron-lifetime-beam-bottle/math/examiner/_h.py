import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity  # noqa


def cmp(label, got, claim, abs_tol, unit=""):
    """Compare my number to the lens's printed number within its rounding (abs_tol)."""
    rel = (abs_tol * 1.0001) / abs(claim)
    print(f"  {label}: mine = {got:.6g} {unit}  lens = {claim} {unit}")
    u = f" {unit}" if unit else ""
    return quantity(f"{got!r}{u}", f"{claim!r}{u}", rel_tol=rel)


def z_of_p2(p):
    """two-sided p -> z"""
    import mpmath as mp
    return float(mp.sqrt(2) * mp.erfinv(1 - p))


def p2_of_z(z):
    return math.erfc(z / math.sqrt(2))


def chi2_sf(x, k):
    import mpmath as mp
    return float(mp.gammainc(k / 2.0, x / 2.0, mp.inf, regularized=True))
