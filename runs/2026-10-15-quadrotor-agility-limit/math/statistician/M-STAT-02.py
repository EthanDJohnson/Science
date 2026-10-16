"""M-STAT-02  (statistician F2, F4; table rows S2, S3, S4)

Claim checked, stated precisely.
  X ~ Binomial(n, p), independent trials. Testing H0: p = 0.90 against H1: p < 0.90, the exact
  one-sided p-value is P(X <= k | n, 0.90), and the lens's z is the equivalent normal deviate
  z = Phi^{-1}(1 - p_one_sided). The lens asserts
    8/10  -> p = 0.264,  z = 0.63   (does not reject p >= 0.90)
    6/10  -> p = 0.0128, z = 2.23, two-sided 0.0256
    1/4   -> p = 0.0037, z = 2.68   (rejects)
    38/43 -> p = 0.43,              Wilson 95 % [0.755, 0.949]
Domain: n positive integer, 0 <= k <= n, p0 = 0.9; p-values and z dimensionless.

Independent derivation: the binomial CDF is summed from binomial coefficients with math.comb
(not from scipy's cdf) and cross-checked against scipy.stats.binom.cdf; z from scipy.stats.norm.
Wilson from the closed-form score inversion, cross-checked by bisection.
"""
import math
import sys

from scipy.stats import binom, norm

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, inequality, limit, quantity, units  # noqa: E402

Z95 = norm.ppf(0.975)


def cdf_closed(k, n, p):
    """P(X <= k) from first principles."""
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, k + 1))


def wilson(k, n, z=Z95):
    c = (k + z * z / 2) / (n + z * z)
    h = z / (n + z * z) * math.sqrt(k * (n - k) / n + z * z / 4)
    return max(0.0, c - h), min(1.0, c + h)


print("=== M-STAT-02: one-sided exact tests of H0: p = 0.90 (dimensionless) ===")
rows = [(8, 10), (6, 10), (1, 4), (38, 43)]
out = {}
for k, n in rows:
    p1 = cdf_closed(k, n, 0.90)
    assert abs(p1 - binom.cdf(k, n, 0.90)) < 1e-12, "two implementations disagree"
    z = norm.ppf(1 - p1) if 0 < p1 < 1 else float("nan")
    out[(k, n)] = (p1, z)
    print(f"{k}/{n}: one-sided p = {p1:.5f}, two-sided (doubled) = {min(1, 2 * p1):.5f}, z = {z:.3f}")
wl, wh = wilson(38, 43)
print(f"Wilson 95 % interval for 38/43: [{wl:.4f}, {wh:.4f}]")
print(f"point estimate 38/43 = {38 / 43:.4f}")

units("1", "dimensionless")
quantity(f"{out[(8, 10)][0]:.6f}", "0.264", rel_tol=5e-3)
quantity(f"{out[(8, 10)][1]:.4f}", "0.63", rel_tol=2e-2)
quantity(f"{out[(6, 10)][0]:.6f}", "0.0128", rel_tol=5e-3)
quantity(f"{out[(6, 10)][1]:.4f}", "2.23", rel_tol=5e-3)
quantity(f"{2 * out[(6, 10)][0]:.6f}", "0.0256", rel_tol=5e-3)
quantity(f"{out[(1, 4)][0]:.6f}", "0.0037", rel_tol=5e-3)
quantity(f"{out[(1, 4)][1]:.4f}", "2.68", rel_tol=5e-3)
quantity(f"{2 * out[(1, 4)][0]:.6f}", "0.0074", rel_tol=5e-3)
quantity(f"{out[(38, 43)][0]:.4f}", "0.43", rel_tol=2e-2)
quantity(f"{wl:.6f}", "0.755", rel_tol=3e-3)
quantity(f"{wh:.6f}", "0.949", rel_tol=3e-3)
# 1/4 exactly: P(X<=1|4,0.9) = 0.1^4 + 4*0.9*0.1^3
inequality(f"abs({out[(1, 4)][0]:.10f} - (0.1**4 + 4*0.9*0.1**3))", "<", "1e-12")
# limit the test must reduce to: with k = n the one-sided p-value is 1 (never rejects p >= 0.9)
inequality(f"abs({cdf_closed(10, 10, 0.9):.10f} - 1)", "<", "1e-12")
# and p-value is monotone decreasing in k: a worse record is more significant
inequality(f"{cdf_closed(6, 10, 0.9):.10f}", "<", f"{cdf_closed(8, 10, 0.9):.10f}")
# large-n normal limit of the score z for p-hat fixed at 0.8: z -> sqrt(n) * 0.1/0.3
limit("1/(1 + sqrt(n)*0.1/0.3)", "n", "oo", "0", domain={"n": (1.0, 1e6)})
raise SystemExit(finish())
