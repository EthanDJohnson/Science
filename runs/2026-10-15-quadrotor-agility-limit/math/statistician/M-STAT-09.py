"""M-STAT-09  (statistician F9; table rows S6, S7)

Claims checked, stated precisely.
  Two independent arms of n = 20 Bernoulli trials (the lens's granularity inference, M-STAT-10).
  The pooled two-proportion z statistic is
      z = (p1 - p2) / sqrt(p_pool (1 - p_pool) (1/n1 + 1/n2)),  p_pool = (k1 + k2)/(n1 + n2),
  with two-sided p = 2(1 - Phi(|z|)). The lens asserts
      17/20 vs 0/20  -> z = 5.44, p = 5.4e-8
      17/20 vs 10/20 -> z = 2.36, p = 0.018
  and that telling 0.85 from 0.50 at 95 % confidence and 80 % power needs 27 trials per arm.
Domain: 0 <= k_i <= n_i, n_i > 0; all quantities dimensionless.

Independent derivation: z from the definition; the two-sided p from scipy.stats.norm; Fisher's
exact test (hypergeometric, summed from math.comb) as an independent cross-check that does not use
the normal approximation; the sample size from the two-proportion formula used in M-STAT-03,
cross-checked by its achieved power.
"""
import math
import sys

from scipy.stats import fisher_exact, norm

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, inequality, limit, quantity, units  # noqa: E402


def two_prop_z(k1, n1, k2, n2):
    p1, p2 = k1 / n1, k2 / n2
    pp = (k1 + k2) / (n1 + n2)
    se = math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    return (p1 - p2) / se


def n_per_arm(p1, p2, alpha=0.05, power=0.80):
    za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)
    pb = (p1 + p2) / 2
    num = za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    return math.ceil(num ** 2 / (p1 - p2) ** 2)


def achieved_power(p1, p2, n, alpha=0.05):
    za = norm.ppf(1 - alpha / 2)
    pb = (p1 + p2) / 2
    se0 = math.sqrt(2 * pb * (1 - pb) / n)
    se1 = math.sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / n)
    return norm.cdf((abs(p1 - p2) - za * se0) / se1)


print("=== M-STAT-09: two-proportion tests on [A-14] (dimensionless) ===")
for k1, k2, label in ((17, 0, "RL 17/20 vs plan-then-track 0/20"), (17, 10, "RL 17/20 vs contouring 10/20")):
    z = two_prop_z(k1, 20, k2, 20)
    p2s = 2 * norm.sf(abs(z))
    fp = fisher_exact([[k1, 20 - k1], [k2, 20 - k2]])[1]
    print(f"{label}: z = {z:.3f}, two-sided normal p = {p2s:.3g}, Fisher exact p = {fp:.3g}")
n27 = n_per_arm(0.85, 0.50)
print(f"trials per arm for 0.85 vs 0.50 (alpha 0.05, power 0.80): {n27}; "
      f"power at n = {achieved_power(0.85, 0.50, n27):.4f}, at n-1 = {achieved_power(0.85, 0.50, n27 - 1):.4f}")
print(f"robustness of the 0 per cent row at n = 10: z = {two_prop_z(9, 10, 0, 10):.3f} (9/10 vs 0/10), "
       f"Fisher p = {fisher_exact([[9, 1], [0, 10]])[1]:.3g}")

z1, z2 = two_prop_z(17, 20, 0, 20), two_prop_z(17, 20, 10, 20)
units("1", "dimensionless")
quantity(f"{z1:.4f}", "5.44", rel_tol=3e-3)
quantity(f"{2 * norm.sf(abs(z1)):.6g}", "5.4e-8", rel_tol=3e-2)
quantity(f"{z2:.4f}", "2.36", rel_tol=3e-3)
quantity(f"{2 * norm.sf(abs(z2)):.6f}", "0.018", rel_tol=3e-2)
quantity(f"{n27}", "27", rel_tol=1e-6)
inequality(f"{achieved_power(0.85, 0.50, n27):.6f}", ">=", "0.80")
# Fisher's exact test must agree in direction and keep both comparisons significant / marginal
inequality(f"{fisher_exact([[17, 3], [0, 20]])[1]:.8g}", "<", "1e-6")
inequality(f"{fisher_exact([[17, 3], [10, 10]])[1]:.8g}", "<", "0.05")
# z grows as sqrt(n) at fixed rates: doubling n multiplies z by sqrt(2)
inequality(f"abs({two_prop_z(34, 40, 20, 40):.9f} - {math.sqrt(2) * z2:.9f})", "<", "1e-6")
limit("sqrt(2)*2.3631/sqrt(k)", "k", "oo", "0", domain={"k": (1.0, 1e6)})
raise SystemExit(finish())
