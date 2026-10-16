"""M-STAT-08  (statistician F8; S3, S4 look-elsewhere columns)

Claims checked, stated precisely.
  (a) Sidak multiplicity: for N independent looks each with local one-sided p-value p_loc, the
      probability that at least one look reaches p_loc is p_glob = 1 - (1 - p_loc)^N. The lens
      asserts p_loc = 0.01 -> 0.049 (N = 5) and 0.114 (N = 12); p_loc = 0.05 -> 0.23 and 0.46.
  (b) The table's global entries: S4 "z = 2.1 at 5 looks" from p_loc = 0.0037, and
      S3 "z = 1.7 at 12 looks" from p_loc = 0.0128, with z = Phi^{-1}(1 - p_glob).
  (c) Wilson 95 % intervals on crash-cause shares: 2/2 -> [0.34, 1.00], 4/10 -> [0.17, 0.69],
      2/10 -> [0.06, 0.51], and the statement that no such interval excludes 0.5.
Domain: p_loc in (0,1), N a positive integer; all quantities dimensionless.

Independent derivation: p_glob from the complement of N independent non-discoveries, built with
math.log1p/expm1 for accuracy and cross-checked by a Monte-Carlo over N independent uniforms; z
from scipy.stats.norm; Wilson intervals by bisection on the score statistic and by the closed
form.
"""
import math
import sys

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, inequality, limit, quantity, series, units  # noqa: E402

Z95 = norm.ppf(0.975)


def sidak(p_loc, n):
    return -math.expm1(n * math.log1p(-p_loc))


def wilson(k, n, z=Z95):
    ph = k / n
    s = lambda p: (ph - p) ** 2 - z * z * p * (1 - p) / n
    lo = brentq(s, 1e-15, ph - 1e-9) if ph > 0 else 0.0
    hi = brentq(s, ph + 1e-9, 1 - 1e-15) if ph < 1 else 1.0
    c = (k + z * z / 2) / (n + z * z)
    h = z / (n + z * z) * math.sqrt(k * (n - k) / n + z * z / 4)
    return (lo, hi), (max(0.0, c - h), min(1.0, c + h))


print("=== M-STAT-08: multiplicity and cause-share intervals (dimensionless) ===")
rng = np.random.default_rng(3)
for p_loc in (0.01, 0.05, 0.0128, 0.0037):
    for n in (5, 12):
        mc = np.mean(np.min(rng.random((200000, n)), axis=1) <= p_loc)
        print(f"p_local = {p_loc:.4f}, {n:2d} looks: Sidak global p = {sidak(p_loc, n):.4f} "
              f"(Monte-Carlo {mc:.4f}), z = Phi^-1(1 - p_glob) = {norm.ppf(1 - sidak(p_loc, n)):.3f}")
for k, n in ((2, 2), (4, 10), (2, 10)):
    (lo, hi), (loc, hic) = wilson(k, n)
    print(f"Wilson 95 % for {k}/{n}: [{lo:.4f}, {hi:.4f}] (bisection) / [{loc:.4f}, {hic:.4f}] (closed form); "
          f"contains 0.5: {lo <= 0.5 <= hi}")

units("1", "dimensionless")
quantity(f"{sidak(0.01, 5):.6f}", "0.049", rel_tol=1e-2)
quantity(f"{sidak(0.01, 12):.6f}", "0.114", rel_tol=1e-2)
quantity(f"{sidak(0.05, 5):.6f}", "0.23", rel_tol=2e-2)
quantity(f"{sidak(0.05, 12):.6f}", "0.46", rel_tol=2e-2)
quantity(f"{norm.ppf(1 - sidak(0.0037, 5)):.4f}", "2.1", rel_tol=2e-2)
quantity(f"{norm.ppf(1 - sidak(0.0128, 12)):.4f}", "1.7", rel_tol=5e-2)   # lens's S3 global z
print(f"NOTE S3: Sidak global p at 12 looks = {sidak(0.0128, 12):.4f}, "
      f"one-sided z = {norm.ppf(1 - sidak(0.0128, 12)):.3f}, "
      f"two-sided-equivalent z = {norm.isf(sidak(0.0128, 12) / 2):.3f}; "
      f"z = 1.7 would need {math.log1p(-0.0128) and math.log(1 - norm.cdf(1.7)) / math.log1p(-0.0128):.1f} looks")
for k, n, want_lo, want_hi in ((2, 2, 0.34, 1.00), (4, 10, 0.17, 0.69), (2, 10, 0.06, 0.51)):
    (lo, hi), _ = wilson(k, n)
    quantity(f"{lo:.6f}", f"{want_lo}", rel_tol=6e-2)   # the lens quotes two decimals
    quantity(f"{hi:.6f}", f"{want_hi}", rel_tol=2e-2)
    inequality(f"abs({lo:.6f} - {want_lo})", "<=", "0.005")   # agrees to the quoted precision
    inequality(f"abs({hi:.6f} - {want_hi})", "<=", "0.005")
    inequality(f"{lo:.6f}", "<=", "0.5")
    inequality(f"{hi:.6f}", ">=", "0.5")
# limits and series the Sidak formula must obey
series("1 - (1 - p)**5", "p", 0, 3, "5*p - 10*p**2", domain={"p": (1e-6, 0.5)})
limit("1 - (1 - 0.05)**n", "n", "oo", "1", domain={"n": (1.0, 1e6)})
inequality("1 - (1 - 0.01)**12", "<=", "12*0.01")      # Sidak is below the Bonferroni bound
raise SystemExit(finish())
