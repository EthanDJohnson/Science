"""M-EMP-11. The elasticity spread that EMP-B (the null) rests on.

Claim (empiricist EMP-B and the skeptic table): the computed elasticities for
range (0.52-1.0), braking/lateral acceleration (0.43-0.48) and thrust-to-weight
(0.50-0.565) "lie within a factor of 2.3 of each other", which the brief's
factor-of-two condition for "no dominance" is then compared against.

Statement checked: with the set S of interval endpoints, max(S)/min(S) = 2.3 to
the stated precision, and no single candidate's elasticity exceeds another's by
more than that factor. Dimensionless throughout (an elasticity is a ratio of
relative changes). Domain: all elasticities positive.
Also checked: whether the spread satisfies the brief's own stated "within a
factor of two" criterion, since 2.33 > 2.
"""
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, units  # noqa: E402

bands = {"range": (0.52, 1.00), "acceleration": (0.43, 0.48), "T/W": (0.50, 0.565)}
lows = [lo for lo, _ in bands.values()]
highs = [hi for _, hi in bands.values()]
spread = max(highs) / min(lows)
print("bands:", bands)
print(f"max endpoint {max(highs)} / min endpoint {min(lows)} = {spread:.4f} (claimed 2.3)")
inequality(f"abs({spread:.6f} - 2.3)", "<", "0.04")
inequality(f"{spread:.6f}", ">", "2.0")      # it does NOT meet a strict factor-of-two criterion
inequality(f"{spread:.6f}", "<", "2.4")

# pairwise worst-case ratios between candidates (worst endpoint against worst endpoint)
names = list(bands)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a_lo, a_hi = bands[names[i]]
        b_lo, b_hi = bands[names[j]]
        r = max(a_hi / b_lo, b_hi / a_lo)
        print(f"  worst-case ratio {names[i]} vs {names[j]} = {r:.4f}")
        inequality(f"{r:.6f}", "<", "2.4")

# midpoint comparison: if each band is replaced by its midpoint the spread shrinks
mids = {k: (lo + hi) / 2 for k, (lo, hi) in bands.items()}
spread_mid = max(mids.values()) / min(mids.values())
print("midpoints:", {k: round(v, 4) for k, v in mids.items()}, f"spread = {spread_mid:.4f}")
inequality(f"{spread_mid:.6f}", "<", f"{spread:.6f}")
inequality(f"{spread_mid:.6f}", "<", "2.0")   # on midpoints the factor-of-two condition is met

identity("a/b", "exp(log(a) - log(b))", domain={"a": (0.1, 10.0), "b": (0.1, 10.0)})
limit("a/b", "a", 0.43, "1", domain={"b": (0.43, 0.43)})   # equal elasticities -> ratio 1
inequality("a/b", ">=", "1", domain={"a": (1.0, 2.0), "b": (0.4, 1.0)})
units("(1.0 m/s) / (0.43 m/s)", "dimensionless")
raise SystemExit(finish())
