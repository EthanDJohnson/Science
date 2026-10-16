"""M-STAT-11  (statistician F1, STAT-C: the "54 with one crash, 85 with three" counts)

Claim checked, stated precisely.
  "Certifying a true rate >= 0.90 at 95 per cent needs ln(0.05)/ln(0.90) = 28.4, i.e. 29
  consecutive flawless unseen-course flights, or 54 flights with one crash, 85 with three."
  Read literally: with f failures in n independent Bernoulli trials, the smallest n whose 95 %
  confidence lower bound on p reaches 0.90 is claimed to be 29 (f = 0), 54 (f = 1), 85 (f = 3).
  The confidence rule used for f = 0 is explicitly the one-sided 95 % Clopper-Pearson bound
  (that is what ln(0.05)/ln(0.90) computes: P(X = n | p = 0.9) = 0.9^n <= 0.05).
Domain: n, f non-negative integers with f < n; p in (0,1); dimensionless.

Independent derivation: for each f, the smallest n with CP lower bound >= 0.90 is found by direct
search, where the CP lower bound L(k, n) solves P(X >= k | n, L) = alpha, with the binomial tail
summed from math.comb (independent of scipy) and cross-checked against scipy.stats.binom.sf. Both
conventions are evaluated: alpha = 0.05 (one-sided 95 %, the rule the lens states) and
alpha = 0.025 (the lower end of a two-sided 95 % interval).
"""
import math
import sys

from scipy.optimize import brentq
from scipy.stats import binom

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, inequality, quantity, units  # noqa: E402


def tail_ge(k, n, p):
    """P(X >= k) summed from binomial coefficients."""
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def cp_lower(k, n, alpha):
    if k == 0:
        return 0.0
    f = lambda p: tail_ge(k, n, p) - alpha
    return brentq(f, 1e-15, 1 - 1e-15, xtol=1e-14)


def smallest_n(f, alpha, target=0.90, nmax=600):
    return next(n for n in range(f + 1, nmax) if cp_lower(n - f, n, alpha) >= target)


print("=== M-STAT-11: smallest n certifying p >= 0.90 with f failures (dimensionless) ===")
assert abs(tail_ge(53, 54, 0.9) - binom.sf(52, 54, 0.9)) < 1e-12, "two tail implementations disagree"
for f in (0, 1, 3):
    n05, n025 = smallest_n(f, 0.05), smallest_n(f, 0.025)
    print(f"f = {f}: one-sided 95 % (alpha = 0.05) -> n = {n05}  [CP lower = {cp_lower(n05 - f, n05, 0.05):.4f}];"
          f"  two-sided 95 % lower end (alpha = 0.025) -> n = {n025} "
          f"[CP lower = {cp_lower(n025 - f, n025, 0.025):.4f}]")
print(f"at the lens's n = 54 with one failure, the one-sided 95 % CP lower bound is "
      f"{cp_lower(53, 54, 0.05):.4f}; at n = 46 it is {cp_lower(45, 46, 0.05):.4f}")
print(f"at the lens's n = 85 with three failures, the one-sided 95 % CP lower bound is "
      f"{cp_lower(82, 85, 0.05):.4f}; at n = 76 it is {cp_lower(73, 76, 0.05):.4f}")

units("1", "dimensionless")
quantity(f"{smallest_n(0, 0.05)}", "29", rel_tol=1e-6)           # the lens's f = 0 count: correct
quantity(f"{smallest_n(1, 0.05)}", "54", rel_tol=1e-6)           # the lens's f = 1 count
quantity(f"{smallest_n(3, 0.05)}", "85", rel_tol=1e-6)           # the lens's f = 3 count
# the corrected counts under the rule the lens itself states (one-sided 95 %):
quantity(f"{smallest_n(1, 0.05)}", "46", rel_tol=1e-6)
quantity(f"{smallest_n(3, 0.05)}", "76", rel_tol=1e-6)
# and the lens's numbers are exactly the alpha = 0.025 (two-sided 95 %) counts:
quantity(f"{smallest_n(1, 0.025)}", "54", rel_tol=1e-6)
quantity(f"{smallest_n(3, 0.025)}", "85", rel_tol=1e-6)
# consistency: more failures demand more flights, and a tighter alpha demands more flights
inequality(f"{smallest_n(3, 0.05)}", ">", f"{smallest_n(1, 0.05)}")
inequality(f"{smallest_n(1, 0.025)}", ">", f"{smallest_n(1, 0.05)}")
# sanity limit: with f = 0 the rule is exactly 0.05^(1/n) >= 0.9
inequality(f"{0.05 ** (1 / 29):.10f}", ">=", "0.9")
inequality(f"{0.05 ** (1 / 28):.10f}", "<", "0.9")
raise SystemExit(finish())
