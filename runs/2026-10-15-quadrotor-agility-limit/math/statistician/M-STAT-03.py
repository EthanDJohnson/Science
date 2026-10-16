"""M-STAT-03  (statistician F3, STAT-C)

Claim checked, stated precisely.
  Two independent arms of n Bernoulli trials each, true rates p1 and p2. For a two-sided test at
  95 % confidence (alpha = 0.05) with 80 % power, the trials needed per arm are
    0.90 vs 0.80  -> 199;   0.90 vs 0.884 -> 5907;   0.90 vs 0.60 -> 32.
  Also: a standard error of 0.0200 on a success rate is what a 0.10 difference needs at z = 5
  (precision_needed(0.10, 5)), and at p = 0.9 that standard error needs about 225 trials.
Domain: p1, p2 in (0,1), p1 != p2; n dimensionless counts.

Independent derivation: the standard two-proportion sample-size formula
  n = [z_{1-alpha/2} sqrt(2 p_bar q_bar) + z_{power} sqrt(p1 q1 + p2 q2)]^2 / (p1 - p2)^2,
with p_bar = (p1+p2)/2, rounded up; cross-checked by a direct power calculation using the normal
approximation to the pooled two-proportion z test (the achieved power at the returned n must be
>= 0.80, and below 0.80 one trial fewer), and by an independent Monte-Carlo power estimate for the
small case. se = sqrt(p(1-p)/n) is inverted for n.
"""
import math
import sys

import numpy as np
from scipy.stats import norm

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, inequality, limit, quantity, units  # noqa: E402


def n_per_arm(p1, p2, alpha=0.05, power=0.80):
    za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)
    pb = (p1 + p2) / 2
    num = za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    return math.ceil(num ** 2 / (p1 - p2) ** 2)


def achieved_power(p1, p2, n, alpha=0.05):
    """Normal-approximation power of the pooled two-proportion z test."""
    za = norm.ppf(1 - alpha / 2)
    pb = (p1 + p2) / 2
    se0 = math.sqrt(2 * pb * (1 - pb) / n)                  # null se (pooled)
    se1 = math.sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / n)    # alternative se
    return norm.cdf((abs(p1 - p2) - za * se0) / se1)


print("=== M-STAT-03: trials per arm (dimensionless counts) ===")
cases = [(0.90, 0.80, 199), (0.90, 0.884, 5907), (0.90, 0.60, 32)]
got = {}
for p1, p2, claimed in cases:
    n = n_per_arm(p1, p2)
    got[(p1, p2)] = n
    print(f"{p1} vs {p2}: n = {n} per arm (lens: {claimed}); power at n = {achieved_power(p1, p2, n):.4f}, "
          f"at n-1 = {achieved_power(p1, p2, n - 1):.4f}")

rng = np.random.default_rng(7)
n = got[(0.90, 0.60)]
k1 = rng.binomial(n, 0.90, 40000) / n
k2 = rng.binomial(n, 0.60, 40000) / n
pb = (k1 + k2) / 2
se = np.sqrt(2 * pb * (1 - pb) / n)
z = np.abs(k1 - k2) / np.where(se > 0, se, np.inf)
print(f"Monte-Carlo power for 0.90 vs 0.60 at n = {n}: {np.mean(z > 1.959964):.3f} (40000 draws)")

prec = 0.10 / 5
n_prec = 0.9 * 0.1 / prec ** 2
print(f"precision needed for a 0.10 difference at z = 5: se = {prec:.4f}")
print(f"trials for se = {prec:.4f} at p = 0.9: n = {n_prec:.1f}")

units("1", "dimensionless")
quantity(f"{got[(0.90, 0.80)]}", "199", rel_tol=1e-6)
quantity(f"{got[(0.90, 0.884)]}", "5907", rel_tol=1e-3)
quantity(f"{got[(0.90, 0.60)]}", "32", rel_tol=1e-6)
quantity(f"{prec:.6f}", "0.0200", rel_tol=1e-3)
quantity(f"{n_prec:.3f}", "225", rel_tol=5e-3)
inequality(f"{achieved_power(0.9, 0.8, got[(0.9, 0.8)]):.6f}", ">=", "0.80")
inequality(f"{achieved_power(0.9, 0.6, got[(0.9, 0.6)]):.6f}", ">=", "0.80")
# limit: as the gap shrinks the required n diverges as 1/delta^2
limit("1/d**2", "d", 0, "oo", domain={"d": (1e-6, 0.5)})
# monotonicity: a smaller gap needs more trials
inequality(f"{n_per_arm(0.9, 0.884)}", ">", f"{n_per_arm(0.9, 0.80)}")
raise SystemExit(finish())
