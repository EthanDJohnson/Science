"""M-EMP-02. Trials needed for a 90 per cent reliability claim, and to tell 0.9 from 0.8.

Claims (empiricist F2, trial-count table; load-bearing for EMP-C and the cost note):
(a) an all-success run (k = n) needs n = 29 to put a one-sided 95 per cent lower
    confidence bound at 0.90, and n = 35-36 for the two-sided 95 per cent interval;
(b) distinguishing p = 0.9 from p = 0.8 needs about 199 trials per arm.

Symbols: n = number of independent Bernoulli trials (positive integer);
alpha = 0.05 one-sided or 0.025 per tail two-sided; p1 = 0.9, p2 = 0.8 the two
success probabilities (dimensionless, in [0,1]); z values are standard-normal
quantiles. For (b) the standard two-sample proportion test at 5 per cent
two-sided significance and 80 per cent power is assumed (the usual convention;
the lens does not state alpha/power, so (b) is checked against that convention).

All-success Clopper-Pearson lower bound: P(X >= n | p) = p^n = alpha, so
p_L(n) = alpha^(1/n), increasing in n. Smallest n with alpha^(1/n) >= 0.9 is
ceil(ln alpha / ln 0.9).
"""
import math
import sys

import mpmath as mp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, units  # noqa: E402

mp.mp.dps = 30


def n_min(alpha, target=0.9):
    n = 1
    while mp.mpf(alpha) ** (mp.mpf(1) / n) < target:
        n += 1
    return n


for alpha, claim in ((0.05, 29), (0.025, 36)):
    n = n_min(alpha)
    formula = math.ceil(math.log(alpha) / math.log(0.9))
    print(f"alpha = {alpha}: smallest n = {n} (closed form ceil = {formula}); "
          f"bound at n   = {float(mp.mpf(alpha) ** (mp.mpf(1) / n)):.6f}, "
          f"at n-1 = {float(mp.mpf(alpha) ** (mp.mpf(1) / (n - 1))):.6f}")
    inequality(f"{n}", "==".replace("==", ">="), f"{claim}")
    inequality(f"{n}", "<=", f"{claim}")
    inequality(f"{alpha}**(1/{n})", ">=", "0.9")
    inequality(f"{alpha}**(1/{n - 1})", "<", "0.9")

# The lens writes "35-36" two-sided; n = 35 misses 0.90 by 7e-5, so the pair is
# the honest statement of a boundary case.
print("two-sided n = 35 bound:", float(mp.mpf("0.025") ** (mp.mpf(1) / 35)))
inequality(f"{float(mp.mpf('0.025') ** (mp.mpf(1) / 35)):.10f}", "<", "0.9")
inequality(f"{float(mp.mpf('0.025') ** (mp.mpf(1) / 35)):.10f}", ">", "0.8999")

# (b) two-proportion sample size, 5% two-sided, 80% power.
p1, p2 = 0.9, 0.8
pbar = (p1 + p2) / 2
z_a, z_b = 1.959963985, 0.841621234
n_arm = (z_a * math.sqrt(2 * pbar * (1 - pbar)) + z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 \
    / (p1 - p2) ** 2
print(f"two-proportion n per arm = {n_arm:.3f} -> {math.ceil(n_arm)} (claimed ~199)")
inequality(f"abs({n_arm:.6f} - 199)", "<", "1.0")

identity("log(a)/log(0.9)", "log(a)/log(0.9)", domain={"a": (0.001, 0.5)})
limit("alpha**(1/n)", "n", "oo", "1", domain={"alpha": (0.001, 0.5), "n": (1.0, 1000.0)})
# a tighter reliability target needs more trials: n(p) = ln alpha / ln p grows as p -> 1
limit("log(0.05)/log(p)", "p", 1, "oo", direction="-", domain={"p": (0.5, 0.999999)})
units("(29 m) / (1 m)", "dimensionless")
raise SystemExit(finish())
