#!/usr/bin/env python3
"""M-EXAMINER-05  (examiner F8, candidate EXAMINER-C)

CLAIM, stated precisely
-----------------------
Flights are independent Bernoulli trials with success probability p (the course-completion rate).
All intervals are ONE-SIDED 95 per cent Clopper-Pearson lower confidence bounds on p from k
successes in n trials: L(k, n) = the p solving sum_{j=k}^{n} C(n,j) p^j (1-p)^(n-j) = 0.05
(L(0, n) = 0).  The lens claims:

 (i)   with no failures the bound is L(n, n) = 0.05^(1/n); the smallest n with L >= 0.90 is 29,
       since 0.05^(1/29) = 0.9019 and 0.05^(1/28) = 0.8985;
 (ii)  L(10,10) = 0.741, L(8,10) = 0.493, L(6,10) = 0.304, L(38,43) = 0.771, L(5,7) = 0.341,
       L(1,4) = 0.013;
 (iii) an exact one-sided binomial test of H0: p = 0.90 against p < 0.90 at alpha = 0.05 has
       power about 0.75 at n = 69 and about 0.87 at n = 100 when the true p = 0.80.

All quantities are dimensionless (probabilities and counts), so there are no units to check; the
"limit" checks are n -> oo and the closed-form k = n case.
"""
import math
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, limit  # noqa: E402

ALPHA = 0.05


def tail(p, k, n):
    """P(X >= k) for X ~ Bin(n, p)."""
    return sum(math.comb(n, j) * p**j * (1 - p) ** (n - j) for j in range(k, n + 1))


def cp_lower(k, n, alpha=ALPHA):
    """One-sided Clopper-Pearson lower bound: solve P(X >= k | p) = alpha by bisection."""
    if k == 0:
        return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if tail(mid, k, n) > alpha:      # tail increases with p
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# (i) closed form for k = n, and the n = 29 threshold
nsym = sp.Symbol("nsym", positive=True)
identity(sp.Rational(1, 20) ** (1 / nsym), sp.exp(sp.log(sp.Rational(1, 20)) / nsym),
         domain={"nsym": (1.0, 200.0)})
limit(sp.Rational(1, 20) ** (1 / nsym), "nsym", sp.oo, sp.Integer(1))

print("(i) no-failure bounds L(n,n) = 0.05^(1/n), checked against the bisection solver:")
for n in (28, 29):
    closed = ALPHA ** (1 / n)
    numeric = cp_lower(n, n)
    print(f"   n = {n}: closed form {closed:.4f}, bisection {numeric:.6f}")
    identity(f"{closed:.4f}", f"{numeric:.4f}")
thresh = min(n for n in range(1, 400) if ALPHA ** (1 / n) >= 0.90)
print(f"   smallest n with L(n,n) >= 0.90 : {thresh} (claimed 29)")
identity(f"{thresh}", "29")
identity(f"{ALPHA ** (1/29):.4f}", "0.9019")
identity(f"{ALPHA ** (1/28):.4f}", "0.8985")

# (ii) the published counts
print("\n(ii) Clopper-Pearson one-sided 95 per cent lower bounds:")
for k, n, want in ((10, 10, 0.741), (8, 10, 0.493), (6, 10, 0.304),
                   (38, 43, 0.771), (5, 7, 0.341), (1, 4, 0.013)):
    got = cp_lower(k, n)
    print(f"   {k}/{n}: L = {got:.4f} (claimed {want})")
    identity(f"{got:.3f}", f"{want:.3f}")
# closed form cross-check for 1/4: 1 - 0.95^(1/4)
identity(f"{1 - 0.95**0.25:.4f}", f"{cp_lower(1, 4):.4f}")

# (iii) exact power of the one-sided test
print("\n(iii) exact binomial power, H0: p = 0.90, true p = 0.80, alpha = 0.05:")


def power(n, p0=0.90, p1=0.80, alpha=ALPHA):
    cdf = lambda p, c: sum(math.comb(n, j) * p**j * (1 - p) ** (n - j) for j in range(0, c + 1))
    crit = -1
    for c in range(n + 1):
        if cdf(p0, c) <= alpha:
            crit = c
        else:
            break
    return (crit, 0.0 if crit < 0 else cdf(p1, crit))


for n, want in ((69, 0.750), (100, 0.870)):
    crit, pw = power(n)
    print(f"   n = {n}: reject if successes <= {crit}; power = {pw:.4f} (claimed {want})")
    identity(f"{pw:.2f}", f"{want:.2f}")

# monotonicity sanity: power rises with n
pw_seq = [power(n)[1] for n in (40, 69, 100, 150)]
print("   power at n = 40, 69, 100, 150:", [f"{x:.3f}" for x in pw_seq])
identity(f"{int(all(b >= a - 1e-9 for a, b in zip(pw_seq, pw_seq[1:])))}", "1")

raise SystemExit(finish())
