"""M-EMP-01. Clopper-Pearson two-sided 95% intervals on the reported success rates.

Claim (empiricist F2 and the trial-count table, load-bearing for EMP-C and F2):
for k successes in n independent Bernoulli trials with unknown success probability
p in [0, 1], the exact (Clopper-Pearson) two-sided 95 per cent interval is

    8/10  -> [0.444, 0.975]
    10/10 -> [0.692, 1.000]
    6/10  -> [0.262, 0.878]
    38/43 -> [0.749, 0.961]
    1/4   -> [0.006, 0.806]
    17/20 -> [0.621, 0.968]

Definition used (independent of the lens's script): with alpha = 0.05,
  p_L solves  P(X >= k | n, p_L) = alpha/2   (p_L = 0 when k = 0)
  p_U solves  P(X <= k | n, p_U) = alpha/2   (p_U = 1 when k = n)
with X ~ Binomial(n, p). Probabilities are dimensionless; trials are assumed
independent and identically distributed, which the lens states as an assumption.

Two independent routes: (a) bisection on the exact binomial tail sum built from
mpmath binomials; (b) the incomplete-beta identity P(X >= k) = I_p(k, n-k+1),
checked with mpmath's regularized betainc at the root found in (a).
"""
import sys

import mpmath as mp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, units  # noqa: E402

mp.mp.dps = 30
ALPHA = mp.mpf("0.05")


def tail_ge(k, n, p):
    """P(X >= k) for X ~ Binomial(n, p)."""
    return mp.fsum([mp.binomial(n, i) * p**i * (1 - p) ** (n - i) for i in range(k, n + 1)])


def tail_le(k, n, p):
    """P(X <= k)."""
    return mp.fsum([mp.binomial(n, i) * p**i * (1 - p) ** (n - i) for i in range(0, k + 1)])


def bisect(f, lo, hi):
    lo, hi = mp.mpf(lo), mp.mpf(hi)
    flo = f(lo)
    for _ in range(200):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def cp(k, n, alpha=ALPHA):
    lo = mp.mpf(0) if k == 0 else bisect(lambda p: tail_ge(k, n, p) - alpha / 2, 0, 1)
    hi = mp.mpf(1) if k == n else bisect(lambda p: tail_le(k, n, p) - alpha / 2, 0, 1)
    return lo, hi


CLAIMS = {
    (8, 10): (0.444, 0.975),
    (10, 10): (0.692, 1.000),
    (6, 10): (0.262, 0.878),
    (38, 43): (0.749, 0.961),
    (1, 4): (0.006, 0.806),
    (17, 20): (0.621, 0.968),
}

print("inputs: alpha = 0.05 two-sided, X ~ Binomial(n, p), p dimensionless in [0,1]")
for (k, n), (cl, cu) in CLAIMS.items():
    lo, hi = cp(k, n)
    print(f"k/n = {k}/{n}: mine [{float(lo):.4f}, {float(hi):.4f}]  claimed [{cl:.3f}, {cu:.3f}]"
          f"  point {k / n:.3f}")
    # route (b): incomplete-beta identity at the root
    if 0 < k:
        beta_tail = mp.betainc(k, n - k + 1, 0, lo, regularized=True)
        print(f"    I_pL({k}, {n - k + 1}) = {float(beta_tail):.8f} (should be 0.025)")
        inequality(f"abs({mp.nstr(beta_tail, 12)} - 0.025)", "<", "1e-9")
    inequality(f"abs({mp.nstr(lo, 12)} - {cl})", "<", "0.0006")
    inequality(f"abs({mp.nstr(hi, 12)} - {cu})", "<", "0.0006")

# k = n closed form: P(X >= n) = p^n = alpha/2 so p_L = 0.025^(1/n).
for n in (4, 10, 20, 29, 43):
    lo, _ = cp(n, n)
    closed = mp.mpf("0.025") ** (mp.mpf(1) / n)
    print(f"k = n = {n}: bisection {float(lo):.12f} vs closed form {float(closed):.12f}")
    inequality(f"abs({mp.nstr(lo, 15)} - {mp.nstr(closed, 15)})", "<", "1e-10")

identity("0.025**(1/n)", "exp(log(0.025)/n)", domain={"n": (1.0, 100.0)})
limit("0.025**(1/n)", "n", "oo", "1")           # more trials -> lower bound -> 1
limit("0.025**(1/n)", "n", 1, "0.025")          # one trial -> the trivial bound
# 90 per cent is inside [0.444, 0.975] (8/10) and outside [0.262, 0.878] (6/10)
lo8, hi8 = cp(8, 10)
lo6, hi6 = cp(6, 10)
inequality(f"{mp.nstr(hi8, 10)}", ">", "0.90")
inequality(f"{mp.nstr(hi6, 10)}", "<", "0.90")
inequality(f"{mp.nstr(cp(10, 10)[0], 10)}", "<", "0.90")
units("(0.8 m) / (1 m)", "dimensionless")
raise SystemExit(finish())
