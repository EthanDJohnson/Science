"""M-STAT-01  (statistician F1, S1, STAT-C)

Claim checked, stated precisely.
  Let X ~ Binomial(n, p) count successful unseen-course flights, p in (0,1) the true per-flight
  success probability, trials independent and identically distributed (the lens's own assumption).
  (a) For k = n = 10 successes, the Clopper-Pearson one-sided 95 % lower confidence bound on p is
      0.741, and the two-sided 95 % Wilson (score) interval is [0.722, 1.000].
  (b) To certify p >= 0.90 at 95 % confidence one needs ln(0.05)/ln(0.90) = 28.4, i.e. 29
      consecutive flawless flights; 54 flights with one failure; 85 with three.
Domain: n a positive integer, 0 <= k <= n, confidence level 0.95, p in (0,1), dimensionless.

Independent derivation (no lens code used):
  CP one-sided lower bound L: the largest p with P(X >= k | n, p) <= alpha, i.e. the root of
  sf(k-1; n, p) = alpha, found by bisection on the binomial CDF built from scipy.stats.binom.
  Wilson interval: invert the score test |k/n - p| = z sqrt(p(1-p)/n), solved by bisection on the
  score function, and compared with the closed form (k + z^2/2 +- z sqrt(k(n-k)/n + z^2/4))/(n+z^2).
  Certification n: smallest n whose CP lower bound at k = n - f successes reaches 0.90, for
  f = 0, 1, 3, under both the one-sided 95 % rule (alpha = 0.05) and the lower end of a two-sided
  95 % interval (alpha = 0.025).
"""
import sys

import numpy as np
from scipy.optimize import brentq
from scipy.stats import binom, norm

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, inequality, limit, quantity, units  # noqa: E402

Z95 = norm.ppf(0.975)        # 1.959964, two-sided 95 %


def cp_lower(k, n, alpha):
    """Largest p with P(X >= k | n, p) <= alpha; 0 when k = 0."""
    if k == 0:
        return 0.0
    f = lambda p: binom.sf(k - 1, n, p) - alpha
    return brentq(f, 1e-15, 1 - 1e-15, xtol=1e-14)


def wilson(k, n, z=Z95):
    """Score-test interval, by bisection on s(p) = (k/n - p)^2 - z^2 p(1-p)/n."""
    ph = k / n
    s = lambda p: (ph - p) ** 2 - z * z * p * (1 - p) / n
    lo = brentq(s, 1e-15, ph - 1e-9) if ph > 0 else 0.0
    hi = brentq(s, ph + 1e-9, 1 - 1e-15) if ph < 1 else 1.0
    return lo, hi


def wilson_closed(k, n, z=Z95):
    c = (k + z * z / 2) / (n + z * z)
    h = z / (n + z * z) * np.sqrt(k * (n - k) / n + z * z / 4)
    return max(0.0, c - h), min(1.0, c + h)


def n_needed(failures, alpha, target=0.90, nmax=4000):
    for n in range(failures + 1, nmax):
        if cp_lower(n - failures, n, alpha) >= target:
            return n
    return None


print("=== M-STAT-01: binomial intervals and certification counts (all dimensionless) ===")
L10 = cp_lower(10, 10, 0.05)
print(f"CP one-sided 95 % lower bound, k = n = 10 : {L10:.6f}   (closed form 0.05^(1/10) = {0.05 ** 0.1:.6f})")
wl, wh = wilson(10, 10)
wlc, whc = wilson_closed(10, 10)
print(f"Wilson 95 % interval, 10/10 (bisection)   : [{wl:.4f}, {wh:.4f}]")
print(f"Wilson 95 % interval, 10/10 (closed form) : [{wlc:.4f}, {whc:.4f}]")
print(f"ln(0.05)/ln(0.90)                         : {np.log(0.05) / np.log(0.90):.4f}")
for f in (0, 1, 3):
    n1, n2 = n_needed(f, 0.05), n_needed(f, 0.025)
    print(f"failures f = {f}: smallest n with CP lower >= 0.90 -> one-sided 95 %: n = {n1};"
          f"  lower end of two-sided 95 %: n = {n2}")
print("P(X >= 53 | n = 54, p = 0.9) =", f"{binom.sf(52, 54, 0.9):.5f}", "(<= 0.025 rule)")
print("P(X >= 82 | n = 85, p = 0.9) =", f"{binom.sf(81, 85, 0.9):.5f}", "(<= 0.025 rule)")
print("true rate 0.75 is inside the 10/10 Wilson interval:", wl <= 0.75 <= wh)

# --- checks ------------------------------------------------------------------
units("1", "dimensionless")                                   # probabilities carry no units
quantity(f"{L10:.8f}", "0.741", rel_tol=2e-3)                 # lens's CP lower bound
quantity(f"{wl:.8f}", "0.722", rel_tol=2e-3)                  # lens's Wilson lower
quantity(f"{wh:.8f}", "1.000", rel_tol=2e-3)                  # lens's Wilson upper
inequality(f"abs({wl:.8f} - {wlc:.8f})", "<", "1e-9")         # bisection == closed form
quantity(f"{np.log(0.05) / np.log(0.90):.6f}", "28.43", rel_tol=2e-3)
quantity(f"{n_needed(0, 0.05)}", "29", rel_tol=1e-6)
quantity(f"{n_needed(1, 0.025)}", "54", rel_tol=1e-6)
quantity(f"{n_needed(3, 0.025)}", "85", rel_tol=1e-6)
# the lens's own stated rule (one-sided 95 %) gives smaller counts for f = 1 and f = 3:
print(f"NOTE one-sided-95 % counts: f=1 -> {n_needed(1, 0.05)}, f=3 -> {n_needed(3, 0.05)}")
# limit the claim must reduce to: a perfect record certifies any target as n grows
limit("1 - 0.05**(1/n)", "n", "oo", "0", domain={"n": (1.0, 1e6)})
# and the one-sided CP bound for k = n is exactly alpha^(1/n) -- spot value at n = 29
inequality(f"abs({cp_lower(29, 29, 0.05):.10f} - {0.05 ** (1 / 29):.10f})", "<", "1e-9")
inequality(f"{cp_lower(29, 29, 0.05):.10f}", ">=", "0.90")
inequality(f"{cp_lower(28, 28, 0.05):.10f}", "<", "0.90")
raise SystemExit(finish())
